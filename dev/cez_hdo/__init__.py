"""ČEZ HDO integration for Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import add_extra_js_url
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"

# Track if frontend is already registered to avoid duplicates
_FRONTEND_REGISTERED = False

# Configuration schema - integrace se konfiguruje pouze přes platformy
CONFIG_SCHEMA = vol.Schema({DOMAIN: cv.empty_config_schema}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ČEZ HDO component."""
    _LOGGER.info("Setting up ČEZ HDO integration")

    # Deploy and register frontend card automatically
    await _ensure_frontend_card(hass)

    # Register service to reload frontend card
    async def reload_frontend_card(call):
        """Service to reload frontend card."""
        global _FRONTEND_REGISTERED
        _FRONTEND_REGISTERED = False
        await _ensure_frontend_card(hass)

    async def clear_cache(call):
        """Service to clear ČEZ HDO cache."""
        import glob
        from pathlib import Path
        
        # Use Home Assistant config directory dynamically
        config_dir = Path(hass.config.config_dir)
        
        cache_patterns = [
            str(config_dir / "www" / "cez_hdo" / "cez_hdo_*.json"),
            str(config_dir / "www" / "cez_hdo_debug_*.json"),
        ]
        
        removed_count = 0
        for pattern in cache_patterns:
            try:
                cache_files = glob.glob(pattern)
                for cache_file in cache_files:
                    try:
                        Path(cache_file).unlink(missing_ok=True)
                        removed_count += 1
                        _LOGGER.info("ČEZ HDO: Cache file removed: %s", cache_file)
                    except Exception as e:
                        _LOGGER.warning("ČEZ HDO: Failed to remove cache file %s: %s", cache_file, e)
            except Exception as e:
                _LOGGER.warning("ČEZ HDO: Error processing pattern %s: %s", pattern, e)
        
        _LOGGER.info("ČEZ HDO: Cache cleared, %d files removed", removed_count)

    hass.services.async_register(DOMAIN, "reload_frontend_card", reload_frontend_card)
    hass.services.async_register(DOMAIN, "clear_cache", clear_cache)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ČEZ HDO from a config entry."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def _ensure_frontend_card(hass: HomeAssistant) -> None:
    """Ensure frontend card is available and registered."""
    try:
        # Get integration directory
        integration_dir = Path(__file__).parent
        frontend_file = integration_dir / "frontend" / "dist" / "cez-hdo-card.js"

        # Get Home Assistant www directory
        www_dir = Path(hass.config.config_dir) / "www" / "cez_hdo"
        www_file = www_dir / "cez-hdo-card.js"

        _LOGGER.info("ČEZ HDO: Setting up frontend card")

        # Create www directory if it doesn't exist
        try:
            www_dir.mkdir(parents=True, exist_ok=True)
            _LOGGER.info("WWW directory created/verified: %s", www_dir)
        except Exception as err:
            _LOGGER.error("Failed to create WWW directory %s: %s", www_dir, err)
            return

        # Copy frontend file if it exists and is newer or doesn't exist in www
        if frontend_file.exists():
            if (
                not www_file.exists()
                or frontend_file.stat().st_mtime > www_file.stat().st_mtime
            ):
                # Use executor for file I/O to avoid blocking the event loop
                await hass.async_add_executor_job(shutil.copy2, frontend_file, www_file)
                _LOGGER.info("ČEZ HDO frontend card copied to %s", www_file)
            else:
                _LOGGER.info("ČEZ HDO frontend card already up to date")

            # Register the frontend card automatically
            frontend_url = "/local/cez_hdo/cez-hdo-card.js"
            add_extra_js_url(hass, frontend_url)
            _LOGGER.info(
                "ČEZ HDO frontend card automatically registered at %s", frontend_url
            )

        else:
            _LOGGER.error(
                "ČEZ HDO frontend card source file not found at %s", frontend_file
            )

    except Exception as err:
        _LOGGER.error("Failed to setup ČEZ HDO frontend card: %s", err)
