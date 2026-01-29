"""Config flow for ČEZ HDO integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from . import downloader

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"

# Configuration keys
CONF_EAN = "ean"
CONF_SIGNAL = "signal"


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from the schema with values provided by the user.
    """
    ean = data[CONF_EAN]
    
    # Try to fetch data from API to validate EAN
    try:
        import requests
        
        url = downloader.BASE_URL
        request_data = downloader.get_request_data(ean)
        
        response = await hass.async_add_executor_job(
            lambda: requests.post(
                url,
                json=request_data,
                timeout=10,
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                },
            )
        )
        
        if response.status_code != 200:
            raise CannotConnect(f"API returned status {response.status_code}")
        
        json_data = response.json()
        signals = json_data.get("data", {}).get("signals", [])
        
        if not signals:
            raise InvalidEan("No signals found for this EAN")
        
        # Get available signal names
        available_signals = list(set(s.get("signal", "") for s in signals if s.get("signal")))
        
        _LOGGER.debug("EAN %s validated, found signals: %s", ean, available_signals)
        
        return {
            "title": f"ČEZ HDO ({ean[-6:]})",
            "available_signals": available_signals,
        }
        
    except Exception as err:
        _LOGGER.error("Failed to validate EAN: %s", err)
        if isinstance(err, (CannotConnect, InvalidEan)):
            raise
        raise CannotConnect(str(err)) from err


class CezHdoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ČEZ HDO."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._ean: str | None = None
        self._available_signals: list[str] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step - EAN input."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                self._ean = user_input[CONF_EAN]
                self._available_signals = info.get("available_signals", [])
                
                # Check if already configured
                await self.async_set_unique_id(self._ean)
                self._abort_if_unique_id_configured()
                
                # If we have multiple signals, ask user to choose
                if len(self._available_signals) > 1:
                    return await self.async_step_signal()
                
                # Single signal or no signal - create entry
                signal = self._available_signals[0] if self._available_signals else None
                return self.async_create_entry(
                    title=info["title"],
                    data={
                        CONF_EAN: self._ean,
                        CONF_SIGNAL: signal,
                    },
                )
                
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidEan:
                errors["base"] = "invalid_ean"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EAN): cv.string,
                }
            ),
            errors=errors,
            description_placeholders={
                "ean_help": "Číslo EAN najdete na faktuře od ČEZ Distribuce",
            },
        )

    async def async_step_signal(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle signal selection step."""
        if user_input is not None:
            return self.async_create_entry(
                title=f"ČEZ HDO ({self._ean[-6:]})",
                data={
                    CONF_EAN: self._ean,
                    CONF_SIGNAL: user_input.get(CONF_SIGNAL),
                },
            )

        # Build signal options
        signal_options = {s: s for s in self._available_signals}

        return self.async_show_form(
            step_id="signal",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SIGNAL): vol.In(signal_options),
                }
            ),
            description_placeholders={
                "signal_help": "Vyberte HDO signál pro vaši lokalitu",
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return CezHdoOptionsFlow(config_entry)


class CezHdoOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for ČEZ HDO."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current signal
        current_signal = self.config_entry.data.get(CONF_SIGNAL, "")

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_SIGNAL, default=current_signal): cv.string,
                }
            ),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidEan(HomeAssistantError):
    """Error to indicate invalid EAN."""
