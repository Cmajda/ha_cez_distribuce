"""ČEZ HDO integration for Home Assistant."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .frontend import CezHdoCardRegistration

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"

# Configuration schema - integrace se konfiguruje pouze přes platformy
CONFIG_SCHEMA = vol.Schema({DOMAIN: cv.empty_config_schema}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ČEZ HDO component."""
    _LOGGER.info("Setting up ČEZ HDO integration")

    # Register service to reload frontend card
    async def reload_frontend_card(call):
        """Service to reload frontend card."""
        cards = CezHdoCardRegistration(hass)
        await cards.async_register()
        _LOGGER.info("🔄 ČEZ HDO frontend card reloaded")

    # Register service to list available signals
    async def list_signals(call):
        """Service to list available signals for given EAN."""
        ean = call.data.get("ean")
        if not ean:
            _LOGGER.error("EAN parameter is required for list_signals service")
            return

        from . import downloader
        import requests

        try:
            url = downloader.BASE_URL
            data = downloader.get_request_data(ean)

            response = await hass.async_add_executor_job(
                lambda: requests.post(
                    url,
                    json=data,
                    timeout=10,
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    },
                )
            )

            if response.status_code == 200:
                json_data = response.json()
                signals = json_data.get("data", {}).get("signals", [])

                # Group signals by signal name
                signal_groups = {}
                for signal in signals:
                    signal_name = signal.get("signal", "unknown")
                    if signal_name not in signal_groups:
                        signal_groups[signal_name] = []
                    signal_groups[signal_name].append(
                        {
                            "den": signal.get("den", ""),
                            "datum": signal.get("datum", ""),
                            "casy": signal.get("casy", ""),
                        }
                    )

                # Log results - simplified
                signal_names = list(signal_groups.keys())
                _LOGGER.warning(
                    f"📡 Nalezené signály pro EAN {ean}: {', '.join(signal_names)}"
                )

            else:
                _LOGGER.error(f"Failed to fetch signals: HTTP {response.status_code}")

        except Exception as e:
            _LOGGER.error(f"Error fetching signals for EAN {ean}: {e}")

    hass.services.async_register(DOMAIN, "reload_frontend_card", reload_frontend_card)
    hass.services.async_register(
        DOMAIN,
        "list_signals",
        list_signals,
        schema=vol.Schema(
            {
                vol.Required("ean"): cv.string,
            }
        ),
    )

    # Register frontend card during setup
    cards = CezHdoCardRegistration(hass)
    await cards.async_register()

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ČEZ HDO from a config entry."""
    _LOGGER.debug("async_setup_entry Start")

    # Register frontend card
    cards = CezHdoCardRegistration(hass)
    await cards.async_register()

    _LOGGER.debug("async_setup_entry Complete")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry")

    # Unregister frontend card
    cards = CezHdoCardRegistration(hass)
    await cards.async_unregister()

    _LOGGER.debug("async_unload_entry Done")
    return True
