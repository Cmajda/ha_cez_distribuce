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

    # Auto-copy frontend card to www directory
    await _ensure_frontend_card(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ČEZ HDO from a config entry."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def _ensure_frontend_card(hass: HomeAssistant) -> None:
    """Ensure frontend card is available in www directory."""
    try:
        # Get integration directory
        integration_dir = Path(__file__).parent
        frontend_file = integration_dir / "frontend" / "dist" / "cez-hdo-card.js"

        # Get Home Assistant www directory
        www_dir = Path(hass.config.config_dir) / "www"
        www_file = www_dir / "cez-hdo-card.js"

        # Create www directory if it doesn't exist
        www_dir.mkdir(exist_ok=True)

        # Copy frontend file if it exists and is newer or doesn't exist in www
        if frontend_file.exists():
            if (
                not www_file.exists()
                or frontend_file.stat().st_mtime > www_file.stat().st_mtime
            ):
                # Use executor for file I/O to avoid blocking the event loop
                await hass.async_add_executor_job(shutil.copy2, frontend_file, www_file)
                _LOGGER.info("ČEZ HDO frontend card copied to /local/cez-hdo-card.js")
            else:
                _LOGGER.debug("ČEZ HDO frontend card already up to date")
        else:
            _LOGGER.warning(
                "ČEZ HDO frontend card source file not found at %s", frontend_file
            )

    except Exception as err:
        _LOGGER.error("Failed to copy ČEZ HDO frontend card: %s", err)
