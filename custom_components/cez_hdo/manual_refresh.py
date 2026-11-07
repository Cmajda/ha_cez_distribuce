"""User-assisted manual HDO data refresh via Home Assistant WebSocket."""

from __future__ import annotations

import logging
import secrets
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from . import downloader
from .const import DOMAIN, mask_ean

_LOGGER = logging.getLogger(__name__)

DATA_COORDINATOR = "coordinator"
DATA_MANUAL_CAPTCHA_SESSIONS = "cez_hdo_manual_captcha_sessions"
CAPTCHA_SESSION_TTL = timedelta(minutes=5)


@dataclass
class ManualCaptchaSession:
    """Store a short-lived CAPTCHA session for one config entry."""

    entry_id: str
    captcha: downloader.CaptchaSession
    expires_at: float


def async_register_websocket_commands(hass: HomeAssistant) -> None:
    """Register WebSocket commands used by the manual refresh dialog."""

    @websocket_api.websocket_command(
        {
            "type": "cez_hdo/manual_refresh/captcha",
            "entity_id": str,
        }
    )
    @websocket_api.async_response
    async def websocket_get_captcha(
        hass: HomeAssistant,
        connection: Any,
        msg: dict[str, Any],
    ) -> None:
        """Fetch a fresh CAPTCHA image for the selected HDO entity."""
        entry_id = _get_entry_id(hass, msg["entity_id"])
        if entry_id is None:
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "ČEZ HDO config entry not found")
            return

        try:
            captcha = await hass.async_add_executor_job(downloader.fetch_captcha)
        except Exception:
            _LOGGER.exception("Failed to fetch manual CAPTCHA")
            connection.send_error(msg["id"], websocket_api.ERR_UNKNOWN_ERROR, "CAPTCHA se nepodařilo načíst")
            return

        captcha_id = secrets.token_urlsafe(24)
        sessions = hass.data.setdefault(DATA_MANUAL_CAPTCHA_SESSIONS, {})
        _purge_expired_sessions(sessions)
        sessions[captcha_id] = ManualCaptchaSession(
            entry_id=entry_id,
            captcha=captcha,
            expires_at=time.monotonic() + CAPTCHA_SESSION_TTL.total_seconds(),
        )
        connection.send_result(
            msg["id"],
            {
                "captcha_id": captcha_id,
                "image_base64": captcha.image_base64,
            },
        )

    @websocket_api.websocket_command(
        {
            "type": "cez_hdo/manual_refresh/submit",
            "entity_id": str,
            "captcha_id": str,
            "captcha_code": str,
        }
    )
    @websocket_api.async_response
    async def websocket_submit_manual_refresh(
        hass: HomeAssistant,
        connection: Any,
        msg: dict[str, Any],
    ) -> None:
        """Validate the user-entered CAPTCHA and refresh the selected entry."""
        sessions = hass.data.get(DATA_MANUAL_CAPTCHA_SESSIONS, {})
        session = sessions.pop(msg["captcha_id"], None)
        if session is None or session.expires_at <= time.monotonic():
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "CAPTCHA vypršela, načtěte nový obrázek")
            return

        entry_id = _get_entry_id(hass, msg["entity_id"])
        if entry_id is None or entry_id != session.entry_id:
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "ČEZ HDO config entry not found")
            return

        entry_data = hass.data.get(DOMAIN, {}).get(entry_id, {})
        coordinator = entry_data.get(DATA_COORDINATOR)
        ean = entry_data.get("ean")
        signal = entry_data.get("signal")
        captcha_code = msg["captcha_code"].strip()
        if coordinator is None or not ean or not captcha_code:
            connection.send_error(msg["id"], websocket_api.ERR_INVALID_FORMAT, "Chybí koordinátor nebo CAPTCHA kód")
            return

        try:
            raw_data = await hass.async_add_executor_job(
                downloader.validate_ean_with_captcha,
                ean,
                captcha_code,
                session.captcha.cookies,
            )
        except ValueError as err:
            if str(err) == "invalid_captcha":
                connection.send_error(
                    msg["id"],
                    websocket_api.ERR_INVALID_FORMAT,
                    "CAPTCHA nebyla přijata. Načtěte nový obrázek a zkuste to znovu.",
                )
                return
            _LOGGER.warning("Manual refresh validation failed for EAN %s: %s", mask_ean(ean), err)
            connection.send_error(msg["id"], websocket_api.ERR_UNKNOWN_ERROR, "ČEZ API požadavek neověřilo")
            return
        except Exception:
            _LOGGER.exception("Manual refresh failed for EAN %s", mask_ean(ean))
            connection.send_error(msg["id"], websocket_api.ERR_UNKNOWN_ERROR, "Obnovu se nepodařilo dokončit")
            return

        signals = downloader._extract_signals(raw_data)
        if not signals or (signal and not any(item.get("signal") == signal for item in signals)):
            connection.send_error(
                msg["id"],
                websocket_api.ERR_UNKNOWN_ERROR,
                "Odpověď ČEZ neobsahuje vybraný HDO signál",
            )
            return

        coordinator.parse_data(raw_data)
        coordinator.data.raw_data = raw_data
        coordinator.data.last_update = datetime.now(downloader.CEZ_TIMEZONE)
        await coordinator.async_save_to_cache(raw_data)
        await coordinator.async_mark_refresh_successful()
        coordinator.async_set_updated_data(coordinator.data)

        _LOGGER.info("Manual refresh successful for EAN %s", mask_ean(ean))
        connection.send_result(msg["id"], {"success": True})

    websocket_api.async_register_command(hass, websocket_get_captcha)
    websocket_api.async_register_command(hass, websocket_submit_manual_refresh)


def _get_entry_id(hass: HomeAssistant, entity_id: str) -> str | None:
    """Return the config entry ID owning an entity."""
    entity = er.async_get(hass).async_get(entity_id)
    return entity.config_entry_id if entity else None


def _purge_expired_sessions(sessions: dict[str, ManualCaptchaSession]) -> None:
    """Remove expired CAPTCHA sessions from memory."""
    now = time.monotonic()
    for captcha_id in [key for key, value in sessions.items() if value.expires_at <= now]:
        sessions.pop(captcha_id, None)
