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
from .const import mask_ean

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"

# Configuration keys
CONF_EAN = "ean"
CONF_SIGNAL = "signal"
CONF_ENTITY_SUFFIX = "entity_suffix"


CONF_LOW_TARIFF_PRICE = "low_tariff_price"
CONF_HIGH_TARIFF_PRICE = "high_tariff_price"


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
        available_signals = list(
            set(s.get("signal", "") for s in signals if s.get("signal"))
        )

        _LOGGER.debug(
            "EAN %s validated, found signals: %s", mask_ean(ean), available_signals
        )

        return {
            "title": f"ČEZ HDO ({ean[-6:]})",
            "available_signals": available_signals,
        }

    except Exception as err:
        _LOGGER.error("Failed to validate EAN: %s", err)
        if isinstance(err, (CannotConnect, InvalidEan)):
            raise
        raise CannotConnect(str(err)) from err


class CezHdoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """Handle a config flow for ČEZ HDO."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._ean: str | None = None
        self._signal: str | None = None
        self._entity_suffix: str | None = None
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

                # Proceed to signal selection (unique_id check will be done after signal selection)
                return await self.async_step_signal()

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
        errors: dict[str, str] = {}

        if user_input is not None:
            self._signal = user_input.get(CONF_SIGNAL)

            # Check if this EAN+signal combination is already configured
            unique_id = f"{self._ean}_{self._signal}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            # Proceed to entity suffix step
            return await self.async_step_entity_suffix()

        # Build signal options
        signal_options = {s: s for s in self._available_signals}

        # Set default to first signal
        default_signal = self._available_signals[0] if self._available_signals else None

        # Choose description based on signal count
        signal_count = len(self._available_signals)

        return self.async_show_form(
            step_id="signal",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SIGNAL, default=default_signal): vol.In(
                        signal_options
                    ),
                }
            ),
            description_placeholders={
                "signal_count": str(signal_count),
            },
            errors=errors,
        )

    async def async_step_entity_suffix(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle entity suffix configuration step."""
        if user_input is not None:
            self._entity_suffix = user_input.get(CONF_ENTITY_SUFFIX, "")
            # Proceed to prices step
            return await self.async_step_prices()

        # Generate default suffix from EAN and signal
        ean_suffix = self._ean[-4:] if self._ean else "0000"
        signal_safe = (
            self._signal.lower().replace("|", "_") if self._signal else "signal"
        )
        default_suffix = f"{ean_suffix}_{signal_safe}"

        return self.async_show_form(
            step_id="entity_suffix",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENTITY_SUFFIX, default=default_suffix): cv.string,
                }
            ),
            description_placeholders={
                "example_entity": default_suffix,
            },
        )

    async def async_step_prices(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle prices configuration step."""
        if user_input is not None:
            low_price = user_input.get(CONF_LOW_TARIFF_PRICE, 0.0)
            high_price = user_input.get(CONF_HIGH_TARIFF_PRICE, 0.0)

            # Ensure EAN is set (should always be at this point)
            if self._ean is None:
                return self.async_abort(reason="missing_ean")

            # Create the config entry
            result = self.async_create_entry(
                title=f"ČEZ HDO ({self._ean[-6:]})",
                data={
                    CONF_EAN: self._ean,
                    CONF_SIGNAL: self._signal,
                    CONF_ENTITY_SUFFIX: self._entity_suffix,
                },
            )

            # Store prices in options (will be loaded by coordinator)
            # We can't set prices directly here because coordinator doesn't exist yet
            # Prices will be stored in hass.data and loaded after setup
            self.hass.data.setdefault("cez_hdo_initial_prices", {})[self._ean] = {
                "low_tariff_price": low_price,
                "high_tariff_price": high_price,
            }

            return result

        return self.async_show_form(
            step_id="prices",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_LOW_TARIFF_PRICE, default=0.0): vol.Coerce(float),
                    vol.Optional(CONF_HIGH_TARIFF_PRICE, default=0.0): vol.Coerce(
                        float
                    ),
                }
            ),
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
        self._config_entry = config_entry
        self._ean: str | None = None
        self._signal: str | None = None
        self._available_signals: list[str] = []

    @property
    def config_entry(self) -> config_entries.ConfigEntry:
        """Return the config entry."""
        return self._config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial options step - EAN input."""
        errors: dict[str, str] = {}

        # Get current EAN as default
        current_ean = self._config_entry.data.get(CONF_EAN, "")

        if user_input is not None:
            ean = user_input.get(CONF_EAN, "")

            # Try to validate EAN and get signals
            try:
                info = await validate_input(self.hass, {CONF_EAN: ean})
                self._ean = ean
                self._available_signals = info.get("available_signals", [])

                # Proceed to signal selection
                return await self.async_step_signal()

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidEan:
                errors["base"] = "invalid_ean"
            except Exception:
                _LOGGER.exception("Unexpected exception in options flow")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EAN, default=current_ean): cv.string,
                }
            ),
            errors=errors,
        )

    async def async_step_signal(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle signal selection step in options."""
        if user_input is not None:
            self._signal = user_input.get(CONF_SIGNAL)
            # Proceed to prices step
            return await self.async_step_prices()

        # Get current signal as default (if same EAN)
        current_signal = self._config_entry.data.get(CONF_SIGNAL, "")
        if self._ean != self._config_entry.data.get(CONF_EAN):
            # EAN changed, use first signal as default
            current_signal = (
                self._available_signals[0] if self._available_signals else ""
            )

        # Build signal options
        signal_options = {s: s for s in self._available_signals}

        # Signal count for description
        signal_count = len(self._available_signals)

        return self.async_show_form(
            step_id="signal",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SIGNAL, default=current_signal): vol.In(
                        signal_options
                    ),
                }
            ),
            description_placeholders={
                "signal_count": str(signal_count),
            },
        )

    async def async_step_prices(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle prices configuration step."""
        if user_input is not None:
            low_price = user_input.get(CONF_LOW_TARIFF_PRICE, 0.0)
            high_price = user_input.get(CONF_HIGH_TARIFF_PRICE, 0.0)

            # Ensure EAN is set (should always be at this point)
            if self._ean is None:
                return self.async_abort(reason="missing_ean")

            # Update config entry data
            new_data = {
                CONF_EAN: self._ean,
                CONF_SIGNAL: self._signal,
            }

            # Update unique_id if EAN changed
            old_ean = self._config_entry.data.get(CONF_EAN)
            if self._ean != old_ean:
                # Update title and unique_id
                self.hass.config_entries.async_update_entry(
                    self._config_entry,
                    title=f"ČEZ HDO ({self._ean[-6:]})",
                    data=new_data,
                    unique_id=self._ean,
                )
            else:
                # Just update data
                self.hass.config_entries.async_update_entry(
                    self._config_entry,
                    data=new_data,
                )

            # Save prices to coordinator
            await self._save_prices(low_price, high_price)

            # Return empty options - all config is in data
            return self.async_create_entry(title="", data={})

        # Get current prices from coordinator
        current_low_price = 0.0
        current_high_price = 0.0

        from . import DOMAIN, DATA_COORDINATOR

        entry_data = self.hass.data.get(DOMAIN, {}).get(self._config_entry.entry_id, {})
        coordinator = entry_data.get(DATA_COORDINATOR)
        if coordinator and coordinator.data:
            current_low_price = coordinator.data.low_tariff_price
            current_high_price = coordinator.data.high_tariff_price

        return self.async_show_form(
            step_id="prices",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_LOW_TARIFF_PRICE, default=current_low_price
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_HIGH_TARIFF_PRICE, default=current_high_price
                    ): vol.Coerce(float),
                }
            ),
        )

    async def _save_prices(self, low_price: float, high_price: float) -> None:
        """Save prices to coordinator."""
        from . import DOMAIN, DATA_COORDINATOR

        entry_data = self.hass.data.get(DOMAIN, {}).get(self._config_entry.entry_id, {})
        coordinator = entry_data.get(DATA_COORDINATOR)

        if coordinator:
            await coordinator.async_set_prices(low_price, high_price)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidEan(HomeAssistantError):
    """Error to indicate invalid EAN."""
