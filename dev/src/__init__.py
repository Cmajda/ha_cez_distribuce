"""ČEZ HDO integration for Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ČEZ HDO component."""
    _LOGGER.info("Setting up ČEZ HDO integration")

    # Auto-copy frontend card to www directory for YAML configuration
    await _ensure_frontend_card(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ČEZ HDO from a config entry."""
    # Auto-copy frontend card to www directory for UI configuration
    await _ensure_frontend_card(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def _ensure_frontend_card(hass: HomeAssistant) -> None:
    """Ensure frontend card is available in www/cez_hdo directory."""
    try:
        # Get integration directory
        integration_dir = Path(__file__).parent
        frontend_file = integration_dir / "frontend" / "dist" / "cez-hdo-card.js"

        # Get Home Assistant www/cez_hdo directory
        www_cez_hdo_dir = Path(hass.config.config_dir) / "www" / "cez_hdo"
        www_file = www_cez_hdo_dir / "cez-hdo-card.js"

        _LOGGER.info("ČEZ HDO: Checking frontend installation")
        _LOGGER.info(
            "Source file: %s (exists: %s)", frontend_file, frontend_file.exists()
        )
        _LOGGER.info("Target directory: %s", www_cez_hdo_dir)
        _LOGGER.info("Target file: %s", www_file)

        # Create www/cez_hdo directory if it doesn't exist
        www_cez_hdo_dir.mkdir(parents=True, exist_ok=True)
        _LOGGER.info("ČEZ HDO directory created/verified: %s", www_cez_hdo_dir)

        # Copy frontend file if it exists and is newer or doesn't exist in www
        if frontend_file.exists():
            if (
                not www_file.exists()
                or frontend_file.stat().st_mtime > www_file.stat().st_mtime
            ):
                # Use executor for file I/O to avoid blocking the event loop
                await hass.async_add_executor_job(shutil.copy2, frontend_file, www_file)
                _LOGGER.info(
                    "ČEZ HDO frontend card copied to /local/cez_hdo/cez-hdo-card.js"
                )
            else:
                _LOGGER.info("ČEZ HDO frontend card already up to date")
        else:
            _LOGGER.error(
                "ČEZ HDO frontend card source file not found at %s", frontend_file
            )

    except Exception as err:
        _LOGGER.error("Failed to copy ČEZ HDO frontend card: %s", err)
