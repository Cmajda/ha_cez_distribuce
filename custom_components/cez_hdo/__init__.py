"""ČEZ HDO integration for Home Assistant."""
from __future__ import annotations

import asyncio
import logging
import shutil
from pathlib import Path

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import add_extra_js_url
try:
    # Prefer official helper; available on older HA versions where hass.http.register_static_path is missing.
    from homeassistant.components.http import async_register_static_path  # type: ignore
except Exception:  # pragma: no cover
    async_register_static_path = None  # type: ignore
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"

# Track if frontend is already registered to avoid duplicates
_FRONTEND_REGISTERED = False

# Prefer serving frontend directly from the integration folder.
_FRONTEND_STATIC_REGISTERED = False

# Configuration schema - integrace se konfiguruje pouze přes platformy
CONFIG_SCHEMA = vol.Schema({DOMAIN: cv.empty_config_schema}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ČEZ HDO component."""
    _LOGGER.info("Setting up ČEZ HDO integration")

    # Deploy and register frontend card automatically.
    # Do it after HA has started to avoid race conditions (HTTP/Lovelace readiness)
    # which can surface as 404 and "Custom element doesn't exist" on hard refresh.
    async def _on_started(event) -> None:  # noqa: ANN001
        await _ensure_frontend_card(hass)

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _on_started)

    # Register service to reload frontend card
    async def reload_frontend_card(call):
        """Service to reload frontend card."""
        # Re-register static path (if needed) and refresh the file copy.
        await _register_frontend_static_path(hass)
        await _deploy_frontend_file(hass)
        _LOGGER.info("🔄 ČEZ HDO frontend card reloaded (file updated only)")

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

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ČEZ HDO from a config entry."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def _deploy_frontend_file(hass: HomeAssistant) -> None:
    """Deploy frontend file without registration."""
    try:
        # Get integration directory
        integration_dir = Path(__file__).parent
        frontend_file = integration_dir / "frontend" / "dist" / "cez-hdo-card.js"

        # Get Home Assistant www directory
        www_dir = Path(hass.config.config_dir) / "www" / "cez_hdo"
        www_file = www_dir / "cez-hdo-card.js"

        # Create www directory if it doesn't exist
        try:
            www_dir.mkdir(parents=True, exist_ok=True)
        except Exception as err:
            _LOGGER.error("Failed to create WWW directory %s: %s", www_dir, err)
            return

        # Copy frontend file if it exists
        if frontend_file.exists():
            await hass.async_add_executor_job(shutil.copy2, frontend_file, www_file)
            _LOGGER.info("📋 ČEZ HDO frontend file deployed to %s", www_file)
        else:
            _LOGGER.error("ČEZ HDO frontend source file not found at %s", frontend_file)

    except Exception as err:
        _LOGGER.error("Failed to deploy ČEZ HDO frontend file: %s", err)


async def _register_frontend_static_path(hass: HomeAssistant) -> bool:
    """Register a static URL for the frontend card served from the integration directory.

    This is more reliable than relying purely on /local (config/www) during hard refresh.
    """
    global _FRONTEND_STATIC_REGISTERED
    if _FRONTEND_STATIC_REGISTERED:
        return True

    try:
        integration_dir = Path(__file__).parent
        dist_dir = integration_dir / "frontend" / "dist"
        frontend_file = dist_dir / "cez-hdo-card.js"

        if not frontend_file.exists():
            _LOGGER.warning(
                "ČEZ HDO frontend source file not found at %s (static path not registered)",
                frontend_file,
            )
            return False

        # Register a directory, so the module is available at /cez_hdo/cez-hdo-card.js
        url_path = "/cez_hdo"

        if async_register_static_path is not None:
            async_register_static_path(
                hass,
                url_path,
                str(dist_dir),
                cache_headers=False,
            )
        else:
            # Fallback for very old HA versions.
            hass.http.app.router.add_static(url_path, str(dist_dir), show_index=False)

        _FRONTEND_STATIC_REGISTERED = True
        _LOGGER.info("✅ ČEZ HDO frontend static path registered at /cez_hdo/cez-hdo-card.js")
        return True

    except Exception as err:
        _LOGGER.warning("Failed to register static path for ČEZ HDO frontend: %s", err)
        return False


async def _ensure_frontend_card(hass: HomeAssistant) -> None:
    """Ensure frontend card is available and registered."""
    global _FRONTEND_REGISTERED

    try:
        # Prefer a static path directly from integration (no copy needed for runtime reliability).
        static_ok = await _register_frontend_static_path(hass)

        # Also deploy the file into /config/www as a fallback for users who reference /local.
        await _deploy_frontend_file(hass)

        # Register the frontend card only once
        if not _FRONTEND_REGISTERED:
            import time

            cache_buster = int(time.time())
            if static_ok:
                frontend_url = f"/cez_hdo/cez-hdo-card.js?v={cache_buster}"
            else:
                frontend_url = f"/local/cez_hdo/cez-hdo-card.js?v={cache_buster}"
            add_extra_js_url(hass, frontend_url)
            _FRONTEND_REGISTERED = True
            _LOGGER.info("✅ ČEZ HDO frontend card registered at %s", frontend_url)
        else:
            _LOGGER.info("ℹ️ ČEZ HDO frontend card already registered, skipping")

    except Exception as err:
        _LOGGER.error("Failed to setup ČEZ HDO frontend card: %s", err)
