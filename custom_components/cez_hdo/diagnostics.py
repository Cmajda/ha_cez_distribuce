"""Diagnostics support for ČEZ HDO integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import DOMAIN, DATA_COORDINATOR

# Keys to redact from diagnostics
TO_REDACT = {"ean", "partner", "vkont", "vstelle", "anlage"}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
    coordinator = entry_data.get(DATA_COORDINATOR)

    diagnostics_data: dict[str, Any] = {
        "config_entry": {
            "entry_id": entry.entry_id,
            "version": entry.version,
            "domain": entry.domain,
            "title": entry.title,
            "data": async_redact_data(dict(entry.data), TO_REDACT),
            "options": dict(entry.options),
        },
    }

    if coordinator:
        # Coordinator info
        diagnostics_data["coordinator"] = {
            "ean_redacted": _redact_ean(coordinator.ean),
            "signal": coordinator.signal,
            "update_interval_seconds": coordinator.update_interval.total_seconds()
            if coordinator.update_interval
            else None,
            "last_update_success": coordinator.last_update_success,
        }

        # Current data state
        data = coordinator.data
        if data:
            diagnostics_data["current_state"] = {
                "last_update": data.last_update.isoformat() if data.last_update else None,
                "low_tariff_active": data.low_tariff_active,
                "high_tariff_active": data.high_tariff_active,
                "low_tariff_start": str(data.low_tariff_start) if data.low_tariff_start else None,
                "low_tariff_end": str(data.low_tariff_end) if data.low_tariff_end else None,
                "high_tariff_start": str(data.high_tariff_start) if data.high_tariff_start else None,
                "high_tariff_end": str(data.high_tariff_end) if data.high_tariff_end else None,
                "low_tariff_price": data.low_tariff_price,
                "high_tariff_price": data.high_tariff_price,
                "schedule_days": len(data.schedule) if data.schedule else 0,
            }

            # Raw data structure (redacted)
            if data.raw_data:
                diagnostics_data["raw_data_structure"] = _get_redacted_raw_data(data.raw_data)
    else:
        diagnostics_data["coordinator"] = "Not available"

    # Cache info
    diagnostics_data["cache"] = await _get_cache_info(hass, coordinator)

    return diagnostics_data


def _redact_ean(ean: str | None) -> str | None:
    """Redact EAN number, showing only last 4 digits."""
    if not ean:
        return None
    if len(ean) > 4:
        return "*" * (len(ean) - 4) + ean[-4:]
    return "****"


def _get_redacted_raw_data(raw_data: dict[str, Any]) -> dict[str, Any]:
    """Get structure of raw data with sensitive fields redacted."""
    result: dict[str, Any] = {}

    if "data" in raw_data:
        data = raw_data["data"]
        result["data"] = {
            "signals_count": len(data.get("signals", [])),
            "amm": data.get("amm"),
            "switchClock": data.get("switchClock"),
            "unknown": data.get("unknown"),
            "partner": "**REDACTED**" if data.get("partner") else None,
            "vkont": "**REDACTED**" if data.get("vkont") else None,
            "vstelle": "**REDACTED**" if data.get("vstelle") else None,
            "anlage": "**REDACTED**" if data.get("anlage") else None,
        }

        # Include signal names (not sensitive)
        signals = data.get("signals", [])
        if signals:
            result["data"]["signal_names"] = list(set(s.get("signal", "") for s in signals))
            result["data"]["signal_dates"] = [s.get("datum", "") for s in signals[:3]]  # First 3 dates

    result["statusCode"] = raw_data.get("statusCode")

    return result


async def _get_cache_info(hass: HomeAssistant, coordinator) -> dict[str, Any]:
    """Get cache file information and content."""
    from datetime import datetime
    from pathlib import Path
    import json

    cache_info: dict[str, Any] = {}

    if coordinator:
        cache_file = coordinator._cache_file
        prices_file = coordinator._prices_file

        def get_file_info(file_path: Path, include_content: bool = False) -> dict[str, Any]:
            if file_path.exists():
                stat = file_path.stat()
                age_seconds = datetime.now().timestamp() - stat.st_mtime
                info = {
                    "exists": True,
                    "size_bytes": stat.st_size,
                    "age_hours": round(age_seconds / 3600, 2),
                    "path": str(file_path),
                }
                if include_content:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            info["content"] = json.load(f)
                    except Exception as err:
                        info["content_error"] = str(err)
                return info
            return {"exists": False, "path": str(file_path)}

        # Cache file - include content but redact it
        cache_file_info = await hass.async_add_executor_job(get_file_info, cache_file, True)
        if "content" in cache_file_info:
            cache_file_info["content"] = _redact_cache_content(cache_file_info["content"])
        cache_info["cache_file"] = cache_file_info

        # Prices file - include full content (no sensitive data)
        cache_info["prices_file"] = await hass.async_add_executor_job(get_file_info, prices_file, True)

    return cache_info


def _redact_cache_content(content: dict[str, Any]) -> dict[str, Any]:
    """Redact sensitive data from cache content."""
    import copy

    if not isinstance(content, dict):
        return content

    # Deep copy to avoid modifying original
    result = copy.deepcopy(content)

    # Redact sensitive fields in nested structure
    def redact_dict(d: dict) -> None:
        for key in ("partner", "vkont", "vstelle", "anlage"):
            if key in d and d[key]:
                d[key] = "**REDACTED**"
        for value in d.values():
            if isinstance(value, dict):
                redact_dict(value)

    redact_dict(result)
    return result
