"""ČEZ HDO integration for Home Assistant."""
from __future__ import annotations

import logging
import json
import os

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .frontend import CezHdoCardRegistration

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"
PRICES_STORAGE_DIR = "/config/www/cez_hdo"
PRICES_STORAGE_FILE = "cez_hdo_prices.json"

# Configuration schema - integrace se konfiguruje pouze přes platformy
CONFIG_SCHEMA = vol.Schema({DOMAIN: cv.empty_config_schema}, extra=vol.ALLOW_EXTRA)


def _get_prices_file_path(hass: HomeAssistant) -> str:
    """Get path to prices storage file."""
    return os.path.join(PRICES_STORAGE_DIR, PRICES_STORAGE_FILE)


def _load_prices(hass: HomeAssistant) -> dict:
    """Load prices from persistent storage."""
    file_path = _get_prices_file_path(hass)
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                _LOGGER.debug("Loaded prices from storage: %s", data)
                return data
    except Exception as err:
        _LOGGER.warning("Failed to load prices from storage: %s", err)
    return {"low_tariff_price": 0.0, "high_tariff_price": 0.0}


def _save_prices(hass: HomeAssistant, low_price: float, high_price: float) -> None:
    """Save prices to persistent storage."""
    file_path = _get_prices_file_path(hass)
    try:
        # Ensure directory exists
        os.makedirs(PRICES_STORAGE_DIR, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(
                {"low_tariff_price": low_price, "high_tariff_price": high_price}, f
            )
        _LOGGER.debug(
            "Saved prices to storage: NT=%.2f, VT=%.2f", low_price, high_price
        )
    except Exception as err:
        _LOGGER.warning("Failed to save prices to storage: %s", err)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ČEZ HDO component."""
    _LOGGER.info("Setting up ČEZ HDO integration")

    # Ensure cache directory exists (for fresh HA installations without www folder)
    await hass.async_add_executor_job(
        lambda: os.makedirs(PRICES_STORAGE_DIR, exist_ok=True)
    )

    # Load prices from persistent storage at startup
    prices = await hass.async_add_executor_job(_load_prices, hass)
    hass.data[DOMAIN] = {
        "low_tariff_price": prices.get("low_tariff_price", 0.0),
        "high_tariff_price": prices.get("high_tariff_price", 0.0),
    }
    _LOGGER.debug(
        "CEZ HDO: Prices loaded from storage: NT=%.2f, VT=%.2f",
        hass.data[DOMAIN]["low_tariff_price"],
        hass.data[DOMAIN]["high_tariff_price"],
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
                _LOGGER.debug(
                    "CEZ HDO: Found signals: %s", ", ".join(signal_names)
                )

            else:
                _LOGGER.error("CEZ HDO: Failed to fetch signals, HTTP status: %s", response.status_code)

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

        # Store prices in hass.data for sensors to access
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}
        hass.data[DOMAIN]["low_tariff_price"] = low_price
        hass.data[DOMAIN]["high_tariff_price"] = high_price

        # Save prices to persistent storage
        await hass.async_add_executor_job(_save_prices, hass, low_price, high_price)

        _LOGGER.debug(
            "CEZ HDO: Prices set: NT=%.2f, VT=%.2f",
            low_price,
            high_price,
        )
        _LOGGER.debug("hass.data[%s] = %s", DOMAIN, hass.data.get(DOMAIN))

        # Force update all CurrentPrice sensors by searching entity registry
        from homeassistant.helpers import entity_registry as er

        registry = er.async_get(hass)

        for entity in registry.entities.values():
            # Match by platform and entity_id pattern
            if entity.platform == DOMAIN and (
                "currentprice" in entity.entity_id.lower()
                or "aktualni_cena" in entity.entity_id.lower()
                or "current_price" in entity.entity_id.lower()
            ):
                _LOGGER.debug("Triggering update for entity: %s", entity.entity_id)
                try:
                    await hass.services.async_call(
                        "homeassistant",
                        "update_entity",
                        {"entity_id": entity.entity_id},
                        blocking=False,
                    )
                except Exception as err:
                    _LOGGER.warning(
                        "Failed to update entity %s: %s", entity.entity_id, err
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
