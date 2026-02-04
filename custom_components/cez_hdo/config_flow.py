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
CONF_CAPTCHA = "captcha"


CONF_LOW_TARIFF_PRICE = "low_tariff_price"
CONF_HIGH_TARIFF_PRICE = "high_tariff_price"


async def validate_input_with_captcha(
    hass: HomeAssistant, ean: str, captcha_code: str, cookies: dict[str, str]
) -> dict[str, Any]:
    """Validate the user input with CAPTCHA.

    Args:
        hass: Home Assistant instance.
        ean: EAN number to validate.
        captcha_code: CAPTCHA code entered by user.
        cookies: Session cookies from CAPTCHA request.

    Returns:
        Dictionary with title and available signals.

    Raises:
        CannotConnect: If API connection fails.
        InvalidEan: If EAN is invalid.
        InvalidCaptcha: If CAPTCHA code is invalid.
    """
    try:
        json_data = await hass.async_add_executor_job(downloader.validate_ean_with_captcha, ean, captcha_code, cookies)

        signals = json_data.get("data", {}).get("signals", [])

        if not signals:
            raise InvalidEan("No signals found for this EAN")

        # Get available signal names
        available_signals = list(set(s.get("signal", "") for s in signals if s.get("signal")))

        _LOGGER.debug("EAN %s validated, found signals: %s", mask_ean(ean), available_signals)

        return {
            "title": f"ČEZ HDO ({ean[-6:]})",
            "available_signals": available_signals,
            "raw_data": json_data,
        }

    except ValueError as err:
        if str(err) == "invalid_captcha":
            raise InvalidCaptcha("Invalid CAPTCHA code") from err
        _LOGGER.error("Failed to validate EAN: %s", err)
        raise CannotConnect(str(err)) from err
    except Exception as err:
        _LOGGER.error("Failed to validate EAN: %s", err)
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
        self._captcha_session: downloader.CaptchaSession | None = None
        self._raw_data: dict[str, Any] | None = None

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step - EAN input."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._ean = user_input[CONF_EAN]
            # Proceed to CAPTCHA step
            return await self.async_step_captcha()

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

    async def async_step_captcha(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle CAPTCHA verification step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            captcha_code = user_input.get(CONF_CAPTCHA, "").strip()

            if not captcha_code:
                errors["base"] = "captcha_required"
            elif self._captcha_session is None:
                errors["base"] = "captcha_expired"
            elif self._ean is None:
                errors["base"] = "unknown"
            else:
                try:
                    info = await validate_input_with_captcha(
                        self.hass,
                        self._ean,
                        captcha_code,
                        self._captcha_session.cookies,
                    )
                    self._available_signals = info.get("available_signals", [])
                    self._raw_data = info.get("raw_data")

                    # Clear CAPTCHA session after successful validation
                    self._captcha_session = None

                    # Proceed to signal selection
                    return await self.async_step_signal()

                except InvalidCaptcha:
                    errors["base"] = "invalid_captcha"
                    # Fetch new CAPTCHA for retry
                    self._captcha_session = None
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                except InvalidEan:
                    errors["base"] = "invalid_ean"
                except Exception:
                    _LOGGER.exception("Unexpected exception during CAPTCHA validation")
                    errors["base"] = "unknown"

        # Fetch CAPTCHA image if not already fetched or on error
        if self._captcha_session is None:
            try:
                self._captcha_session = await self.hass.async_add_executor_job(downloader.fetch_captcha)
            except Exception as err:
                _LOGGER.error("Failed to fetch CAPTCHA: %s", err)
                errors["base"] = "captcha_fetch_failed"

        # Build CAPTCHA image URL for display
        captcha_image = ""
        if self._captcha_session:
            captcha_image = f"data:image/png;base64,{self._captcha_session.image_base64}"

        return self.async_show_form(
            step_id="captcha",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CAPTCHA): cv.string,
                }
            ),
            errors=errors,
            description_placeholders={
                "captcha_image": captcha_image,
                "ean": self._ean or "",
            },
        )

    async def async_step_signal(self, user_input: dict[str, Any] | None = None) -> FlowResult:
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
                    vol.Required(CONF_SIGNAL, default=default_signal): vol.In(signal_options),
                }
            ),
            description_placeholders={
                "signal_count": str(signal_count),
            },
            errors=errors,
        )

    async def async_step_entity_suffix(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle entity suffix configuration step."""
        if user_input is not None:
            self._entity_suffix = user_input.get(CONF_ENTITY_SUFFIX, "")
            # Proceed to prices step
            return await self.async_step_prices()

        # Generate default suffix from EAN and signal
        ean_suffix = self._ean[-4:] if self._ean else "0000"
        signal_safe = self._signal.lower().replace("|", "_") if self._signal else "signal"
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

    async def async_step_prices(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle prices configuration step."""
        if user_input is not None:
            low_price = user_input.get(CONF_LOW_TARIFF_PRICE, 0.0)
            high_price = user_input.get(CONF_HIGH_TARIFF_PRICE, 0.0)

            # Ensure EAN is set (should always be at this point)
            if self._ean is None:
                return self.async_abort(reason="missing_ean")

            # Store prices in hass.data BEFORE creating entry
            # (coordinator will pick them up during async_setup_entry)
            self.hass.data.setdefault("cez_hdo_initial_prices", {})[self._ean] = {
                "low_tariff_price": low_price,
                "high_tariff_price": high_price,
            }

            # Store raw data from CAPTCHA validation for coordinator to use
            # This avoids the need for another API call which would require CAPTCHA
            # MUST be set BEFORE async_create_entry() because setup happens immediately
            if self._raw_data:
                self.hass.data.setdefault("cez_hdo_initial_data", {})[self._ean] = self._raw_data
                _LOGGER.debug(
                    "Stored initial data for EAN %s before creating entry",
                    mask_ean(self._ean),
                )

            # Create the config entry - this triggers async_setup_entry immediately
            return self.async_create_entry(
                title=f"ČEZ HDO ({self._ean[-6:]})",
                data={
                    CONF_EAN: self._ean,
                    CONF_SIGNAL: self._signal,
                    CONF_ENTITY_SUFFIX: self._entity_suffix,
                },
            )

        return self.async_show_form(
            step_id="prices",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_LOW_TARIFF_PRICE, default=0.0): vol.Coerce(float),
                    vol.Optional(CONF_HIGH_TARIFF_PRICE, default=0.0): vol.Coerce(float),
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
        self._captcha_session: downloader.CaptchaSession | None = None

    @property
    def config_entry(self) -> config_entries.ConfigEntry:
        """Return the config entry."""
        return self._config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial options step - EAN input."""
        errors: dict[str, str] = {}

        # Get current EAN as default
        current_ean = self._config_entry.data.get(CONF_EAN, "")

        if user_input is not None:
            self._ean = user_input.get(CONF_EAN, "")
            # Proceed to CAPTCHA step
            return await self.async_step_captcha()

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EAN, default=current_ean): cv.string,
                }
            ),
            errors=errors,
        )

    async def async_step_captcha(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle CAPTCHA verification step in options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            captcha_code = user_input.get(CONF_CAPTCHA, "").strip()

            if not captcha_code:
                errors["base"] = "captcha_required"
            elif self._captcha_session is None:
                errors["base"] = "captcha_expired"
            else:
                try:
                    info = await validate_input_with_captcha(
                        self.hass,
                        self._ean or "",
                        captcha_code,
                        self._captcha_session.cookies,
                    )
                    self._available_signals = info.get("available_signals", [])

                    # Clear CAPTCHA session after successful validation
                    self._captcha_session = None

                    # Proceed to signal selection
                    return await self.async_step_signal()

                except InvalidCaptcha:
                    errors["base"] = "invalid_captcha"
                    # Fetch new CAPTCHA for retry
                    self._captcha_session = None
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                except InvalidEan:
                    errors["base"] = "invalid_ean"
                except Exception:
                    _LOGGER.exception("Unexpected exception during CAPTCHA validation")
                    errors["base"] = "unknown"

        # Fetch CAPTCHA image if not already fetched or on error
        if self._captcha_session is None:
            try:
                self._captcha_session = await self.hass.async_add_executor_job(downloader.fetch_captcha)
            except Exception as err:
                _LOGGER.error("Failed to fetch CAPTCHA: %s", err)
                errors["base"] = "captcha_fetch_failed"

        # Build CAPTCHA image URL for display
        captcha_image = ""
        if self._captcha_session:
            captcha_image = f"data:image/png;base64,{self._captcha_session.image_base64}"

        return self.async_show_form(
            step_id="captcha",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CAPTCHA): cv.string,
                }
            ),
            errors=errors,
            description_placeholders={
                "captcha_image": captcha_image,
                "ean": self._ean or "",
            },
        )

    async def async_step_signal(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle signal selection step in options."""
        if user_input is not None:
            self._signal = user_input.get(CONF_SIGNAL)
            # Proceed to prices step
            return await self.async_step_prices()

        # Get current signal as default (if same EAN)
        current_signal = self._config_entry.data.get(CONF_SIGNAL, "")
        if self._ean != self._config_entry.data.get(CONF_EAN):
            # EAN changed, use first signal as default
            current_signal = self._available_signals[0] if self._available_signals else ""

        # Build signal options
        signal_options = {s: s for s in self._available_signals}

        # Signal count for description
        signal_count = len(self._available_signals)

        return self.async_show_form(
            step_id="signal",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SIGNAL, default=current_signal): vol.In(signal_options),
                }
            ),
            description_placeholders={
                "signal_count": str(signal_count),
            },
        )

    async def async_step_prices(self, user_input: dict[str, Any] | None = None) -> FlowResult:
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
                    vol.Optional(CONF_LOW_TARIFF_PRICE, default=current_low_price): vol.Coerce(float),
                    vol.Optional(CONF_HIGH_TARIFF_PRICE, default=current_high_price): vol.Coerce(float),
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


class InvalidCaptcha(HomeAssistantError):
    """Error to indicate invalid CAPTCHA code."""
