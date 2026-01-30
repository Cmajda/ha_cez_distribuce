"""ČEZ HDO integration for Home Assistant."""
from __future__ import annotations

import logging
from pathlib import Path

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .frontend import CezHdoCardRegistration

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"

# Keys for hass.data[DOMAIN]
DATA_COORDINATOR = "coordinator"

# Configuration schema - integrace se konfiguruje pouze přes platformy
CONFIG_SCHEMA = vol.Schema({DOMAIN: cv.empty_config_schema}, extra=vol.ALLOW_EXTRA)


def get_cache_dir(hass: HomeAssistant) -> Path:
    """Get path to data directory using hass.config.path()."""
    return Path(hass.config.path("custom_components", "cez_hdo", "data"))


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ČEZ HDO component."""
    _LOGGER.info("Setting up ČEZ HDO integration")

    # Initialize domain data storage
    hass.data.setdefault(DOMAIN, {})

    # Ensure data directory exists
    cache_dir = get_cache_dir(hass)
    await hass.async_add_executor_job(
        lambda: cache_dir.mkdir(parents=True, exist_ok=True)
    )

    # Register service to reload frontend card
    async def reload_frontend_card(call):
        """Service to reload frontend card."""
        cards = CezHdoCardRegistration(hass)
        await cards.async_register()
        _LOGGER.debug("CEZ HDO: Frontend card reloaded")

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
                _LOGGER.debug("CEZ HDO: Found signals: %s", ", ".join(signal_names))

            else:
                _LOGGER.error(
                    "CEZ HDO: Failed to fetch signals, HTTP status: %s",
                    response.status_code,
                )

        except Exception as e:
            _LOGGER.error("CEZ HDO: Error fetching signals: %s", e)

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

    # Register service to set tariff prices
    async def set_prices(call):
        """Service to set tariff prices for CurrentPrice sensor."""
        low_price = call.data.get("low_tariff_price", 0.0)
        high_price = call.data.get("high_tariff_price", 0.0)

        coordinators_updated = 0

        # Check YAML coordinator (stored under DATA_COORDINATOR key)
        coordinator = hass.data[DOMAIN].get(DATA_COORDINATOR)
        if coordinator:
            await coordinator.async_set_prices(low_price, high_price)
            coordinators_updated += 1

        # Check config entry coordinators (stored under entry_id keys)
        for key, value in hass.data[DOMAIN].items():
            if isinstance(value, dict) and DATA_COORDINATOR in value:
                entry_coordinator = value[DATA_COORDINATOR]
                await entry_coordinator.async_set_prices(low_price, high_price)
                coordinators_updated += 1

        if coordinators_updated == 0:
            # Fallback for when coordinator not yet initialized
            # Store in hass.data for sensors to access
            hass.data[DOMAIN]["low_tariff_price"] = low_price
            hass.data[DOMAIN]["high_tariff_price"] = high_price
            _LOGGER.debug(
                "CEZ HDO: Prices stored (no coordinator): NT=%.2f, VT=%.2f",
                low_price,
                high_price,
            )
        else:
            _LOGGER.debug(
                "CEZ HDO: Prices set on %d coordinator(s): NT=%.2f, VT=%.2f",
                coordinators_updated,
                low_price,
                high_price,
            )

    hass.services.async_register(
        DOMAIN,
        "set_prices",
        set_prices,
        schema=vol.Schema(
            {
                vol.Required("low_tariff_price"): vol.Coerce(float),
                vol.Required("high_tariff_price"): vol.Coerce(float),
            }
        ),
    )

    # Register frontend card during setup
    cards = CezHdoCardRegistration(hass)
    await cards.async_register()

    return True


# Platforms to set up from config entry
PLATFORMS = ["sensor", "binary_sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ČEZ HDO from a config entry."""
    _LOGGER.debug("async_setup_entry Start for %s", entry.entry_id)

    # Register frontend card
    cards = CezHdoCardRegistration(hass)
    await cards.async_register()

    # Get config data
    ean = entry.data.get("ean")
    signal = entry.data.get("signal")

    if not ean:
        _LOGGER.error("No EAN in config entry")
        return False

    # Create coordinator
    from .coordinator import CezHdoCoordinator

    coordinator = CezHdoCoordinator(hass, ean, signal)
    await coordinator.async_initialize()

    # Check for initial prices from config flow
    initial_prices = hass.data.get("cez_hdo_initial_prices", {}).pop(ean, None)
    if initial_prices:
        await coordinator.async_set_prices(
            initial_prices.get("low_tariff_price", 0.0),
            initial_prices.get("high_tariff_price", 0.0),
        )
        _LOGGER.debug("Set initial prices from config flow: %s", initial_prices)

    # Store coordinator in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_COORDINATOR: coordinator,
        "ean": ean,
        "signal": signal,
    }

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug("async_setup_entry Complete for %s", entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry for %s", entry.entry_id)

    # Stop state updates on coordinator before unloading
    entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
    coordinator = entry_data.get(DATA_COORDINATOR)
    if coordinator:
        coordinator.stop_state_updates()

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Remove coordinator from hass.data
        hass.data[DOMAIN].pop(entry.entry_id, None)

    # Unregister frontend card if no more entries
    if not hass.data[DOMAIN]:
        cards = CezHdoCardRegistration(hass)
        await cards.async_unregister()

    _LOGGER.debug("async_unload_entry Done for %s", entry.entry_id)
    return unload_ok
