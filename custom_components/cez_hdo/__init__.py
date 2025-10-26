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
    _LOGGER.info("Setting up ČEZ HDO integration")
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
            # Use the modern web server registration method
            hass.http.register_static_path(
                "/hacsfiles/cez-hdo-card",
                str(frontend_dir),
                cache_headers=True
            )
            
            _LOGGER.info("ČEZ HDO frontend resources registered successfully")
        else:
            _LOGGER.warning("Frontend directory not found at %s, custom card will not be available", frontend_dir)
            
    except AttributeError:
        # Fallback for newer HA versions
        try:
            from homeassistant.components.http.static import StaticPathConfig
            
            integration_dir = Path(__file__).parent
            frontend_dir = integration_dir / "frontend" / "dist"
            
            if frontend_dir.exists():
                static_config = StaticPathConfig(
                    url_path="/hacsfiles/cez-hdo-card",
                    path=str(frontend_dir),
                    cache_headers=True
                )
                hass.http.register_static_path(static_config)
                _LOGGER.info("ČEZ HDO frontend resources registered successfully (fallback method)")
            
        except Exception as fallback_err:
            _LOGGER.warning("Could not register frontend resources with fallback method: %s", fallback_err)
            _LOGGER.info("Custom card will need to be installed manually")
            
    except Exception as err:
        _LOGGER.error("Failed to register frontend resources: %s", err)