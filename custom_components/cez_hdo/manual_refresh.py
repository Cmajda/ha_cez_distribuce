"""User-assisted manual HDO data refresh via Home Assistant WebSocket."""

from __future__ import annotations

import logging
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from . import downloader
from .config_flow import CannotConnect, InvalidCaptcha, InvalidEan, validate_input_with_captcha
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
    available_signals: list[str] = field(default_factory=list)
    raw_data: dict[str, Any] | None = None


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
        session = sessions.get(msg["captcha_id"])
        if session is None or session.expires_at <= time.monotonic():
            sessions.pop(msg["captcha_id"], None)
            _LOGGER.warning("Manual CAPTCHA submission rejected: session missing or expired")
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "CAPTCHA vypršela, načtěte nový obrázek")
            return

        entry_id = _get_entry_id(hass, msg["entity_id"])
        if entry_id is None or entry_id != session.entry_id:
            _LOGGER.warning("Manual CAPTCHA submission rejected: config entry does not match CAPTCHA session")
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "ČEZ HDO config entry not found")
            return

        entry_data = hass.data.get(DOMAIN, {}).get(entry_id, {})
        coordinator = entry_data.get(DATA_COORDINATOR)
        ean = entry_data.get("ean")
        signal = entry_data.get("signal")
        captcha_code = msg["captcha_code"].strip()
        if coordinator is None or not ean or not captcha_code:
            _LOGGER.warning(
                "Manual CAPTCHA submission rejected: missing coordinator, EAN, or CAPTCHA code"
            )
            connection.send_error(msg["id"], websocket_api.ERR_INVALID_FORMAT, "Chybí koordinátor nebo CAPTCHA kód")
            return

        if session.raw_data is not None:
            connection.send_error(
                msg["id"],
                websocket_api.ERR_INVALID_FORMAT,
                "Tato CAPTCHA už byla ověřena. Načtěte nový obrázek.",
            )
            return

        _LOGGER.info("Manual CAPTCHA submission received for EAN %s", mask_ean(ean))
        try:
            info = await validate_input_with_captcha(
                hass,
                ean,
                captcha_code,
                session.captcha.cookies,
            )
        except InvalidCaptcha:
            sessions.pop(msg["captcha_id"], None)
            _LOGGER.info("Manual CAPTCHA rejected by ČEZ API for EAN %s", mask_ean(ean))
            connection.send_error(
                msg["id"],
                websocket_api.ERR_INVALID_FORMAT,
                "CAPTCHA nebyla přijata. Načtěte nový obrázek a zkuste to znovu.",
            )
            return
        except InvalidEan:
            sessions.pop(msg["captcha_id"], None)
            _LOGGER.warning("Manual refresh returned no signals for EAN %s", mask_ean(ean))
            connection.send_error(msg["id"], websocket_api.ERR_UNKNOWN_ERROR, "Odpověď ČEZ neobsahuje žádné HDO signály")
            return
        except CannotConnect as err:
            sessions.pop(msg["captcha_id"], None)
            _LOGGER.warning("Manual refresh validation failed for EAN %s: %s", mask_ean(ean), err)
            connection.send_error(msg["id"], websocket_api.ERR_UNKNOWN_ERROR, "ČEZ API požadavek neověřilo")
            return
        except Exception:
            sessions.pop(msg["captcha_id"], None)
            _LOGGER.exception("Manual refresh failed for EAN %s", mask_ean(ean))
            connection.send_error(msg["id"], websocket_api.ERR_UNKNOWN_ERROR, "Obnovu se nepodařilo dokončit")
            return

        available_signals = info["available_signals"]
        raw_data = info["raw_data"]
        if not available_signals or not raw_data:
            sessions.pop(msg["captcha_id"], None)
            _LOGGER.warning("Manual refresh returned no usable signal data for EAN %s", mask_ean(ean))
            connection.send_error(
                msg["id"],
                websocket_api.ERR_UNKNOWN_ERROR,
                "Odpověď ČEZ neobsahuje použitelná HDO data",
            )
            return

        session.available_signals = available_signals
        session.raw_data = raw_data
        _LOGGER.info(
            "Manual CAPTCHA accepted for EAN %s; returned_signal_count=%d",
            mask_ean(ean),
            len(available_signals),
        )
        connection.send_result(
            msg["id"],
            {
                "available_signals": available_signals,
                "configured_signal": signal if signal in available_signals else None,
            },
        )

    @websocket_api.websocket_command(
        {
            "type": "cez_hdo/manual_refresh/select_signal",
            "entity_id": str,
            "captcha_id": str,
            "signal": str,
        }
    )
    @websocket_api.async_response
    async def websocket_select_refresh_signal(
        hass: HomeAssistant,
        connection: Any,
        msg: dict[str, Any],
    ) -> None:
        """Apply the user-selected signal from the verified CEZ response."""
        sessions = hass.data.get(DATA_MANUAL_CAPTCHA_SESSIONS, {})
        session = sessions.get(msg["captcha_id"])
        if session is None or session.expires_at <= time.monotonic():
            sessions.pop(msg["captcha_id"], None)
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "CAPTCHA vypršela, načtěte nový obrázek")
            return

        entry_id = _get_entry_id(hass, msg["entity_id"])
        if entry_id is None or entry_id != session.entry_id:
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "ČEZ HDO config entry not found")
            return

        entry_data = hass.data.get(DOMAIN, {}).get(entry_id, {})
        coordinator = entry_data.get(DATA_COORDINATOR)
        ean = entry_data.get("ean")
        selected_signal = msg["signal"]
        raw_data = session.raw_data
        if (
            coordinator is None
            or not ean
            or raw_data is None
            or selected_signal not in session.available_signals
        ):
            connection.send_error(msg["id"], websocket_api.ERR_INVALID_FORMAT, "Vybraný HDO signál není dostupný")
            return

        config_entry = hass.config_entries.async_get_entry(entry_id)
        if config_entry is None:
            connection.send_error(msg["id"], websocket_api.ERR_NOT_FOUND, "ČEZ HDO config entry not found")
            return

        signal_changed = selected_signal != entry_data.get("signal")
        old_signal = entry_data.get("signal")
        if signal_changed:
            updated_data = {**config_entry.data, "signal": selected_signal}
            hass.config_entries.async_update_entry(config_entry, data=updated_data)
            entry_data["signal"] = selected_signal
            coordinator.signal = selected_signal

        coordinator.parse_data(raw_data)
        coordinator.data.raw_data = raw_data
        coordinator.data.last_update = datetime.now(downloader.CEZ_TIMEZONE)
        await coordinator.async_save_to_cache(raw_data)
        await coordinator.async_mark_refresh_successful()
        coordinator.async_set_updated_data(coordinator.data)
        sessions.pop(msg["captcha_id"], None)

        if signal_changed and not await hass.config_entries.async_reload(entry_id):
            _LOGGER.error("Manual refresh updated signal but failed to reload entry for EAN %s", mask_ean(ean))
            connection.send_error(
                msg["id"],
                websocket_api.ERR_UNKNOWN_ERROR,
                "Signál byl uložen, ale entry se nepodařilo načíst",
            )
            return
        if signal_changed and old_signal:
            _cleanup_old_signal_device(hass, entry_id, ean, old_signal)

        _LOGGER.info(
            "Manual refresh successful for EAN %s with selected signal %s",
            mask_ean(ean),
            selected_signal,
        )
        connection.send_result(msg["id"], {"success": True})

    websocket_api.async_register_command(hass, websocket_get_captcha)
    websocket_api.async_register_command(hass, websocket_submit_manual_refresh)
    websocket_api.async_register_command(hass, websocket_select_refresh_signal)


def _get_entry_id(hass: HomeAssistant, entity_id: str) -> str | None:
    """Return the config entry ID owning an entity."""
    entity = er.async_get(hass).async_get(entity_id)
    return entity.config_entry_id if entity else None


def _cleanup_old_signal_device(
    hass: HomeAssistant,
    entry_id: str,
    ean: str,
    old_signal: str,
) -> None:
    """Remove the previous signal device when it no longer has entities."""
    old_identifier = f"{ean}_{old_signal}"
    device_registry = dr.async_get(hass)
    old_device = next(
        (
            device
            for device in dr.async_entries_for_config_entry(device_registry, entry_id)
            if (DOMAIN, old_identifier) in device.identifiers
        ),
        None,
    )
    if old_device is None:
        return

    if any(entity.device_id == old_device.id for entity in er.async_get(hass).entities.values()):
        _LOGGER.warning(
            "Leaving previous signal device for EAN %s because it still has entities",
            mask_ean(ean),
        )
        return

    device_registry.async_update_device(old_device.id, remove_config_entry_id=entry_id)
    _LOGGER.info(
        "Removed empty previous signal device for EAN %s (signal %s)",
        mask_ean(ean),
        old_signal,
    )


def _purge_expired_sessions(sessions: dict[str, ManualCaptchaSession]) -> None:
    """Remove expired CAPTCHA sessions from memory."""
    now = time.monotonic()
    for captcha_id in [key for key, value in sessions.items() if value.expires_at <= now]:
        sessions.pop(captcha_id, None)
