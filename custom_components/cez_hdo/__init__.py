"""ČEZ HDO integration for Home Assistant."""
from __future__ import annotations

import logging
import os
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ČEZ HDO component."""
    # Register frontend resources
    await _register_frontend_resources(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ČEZ HDO from a config entry."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def _register_frontend_resources(hass: HomeAssistant) -> None:
    """Register frontend resources for the custom card."""
    try:
        # Get the path to the frontend files
        integration_dir = Path(__file__).parent
        frontend_dir = integration_dir / "frontend" / "dist"
        
        if frontend_dir.exists():
            # Register the frontend card files
            hass.http.register_static_path(
                "/hacsfiles/cez-hdo-card",
                str(frontend_dir),
                cache_headers=False,
            )
            
            _LOGGER.info("ČEZ HDO frontend resources registered successfully")
        else:
            _LOGGER.warning("Frontend directory not found at %s, custom card will not be available", frontend_dir)
            
    except Exception as err:
        _LOGGER.error("Failed to register frontend resources: %s", err)