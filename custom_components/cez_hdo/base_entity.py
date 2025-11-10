"""Base entity for CEZ HDO sensors."""
from __future__ import annotations
import json
import logging
import time
from datetime import timedelta
from pathlib import Path
from typing import Any

import requests
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from . import downloader

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=3600)
_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"


class CezHdoBaseEntity(Entity):
    """Base class for CEZ HDO entities."""

    def __init__(self, region: str, code: str, name: str, hass=None) -> None:
        """Initialize the sensor."""
        self.region = region
        self.code = code
        self._name = name
        self._response_data: dict[str, Any] | None = None
        self._last_update_success = False
        self._hass = hass
        self.update()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{DOMAIN}_{self._name}"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"{DOMAIN}_{self._name}"

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state."""
        return True

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attributes = {}
        if self._response_data is not None:
            attributes["response_json"] = self._response_data
        return attributes

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self) -> None:
        """Fetch new state data for the sensor with cache fallback."""
        # Pokusit se načíst z cache jako první priorita - s region/code v názvu
        cache_filename = f"cez_hdo_{self.region}_{self.code}.json"
        debug_filename = f"cez_hdo_debug_{self.region}_{self.code}.json"

        # Use dynamic config directory if hass is available
        if (
            self._hass
            and hasattr(self._hass, "config")
            and hasattr(self._hass.config, "config_dir")
        ):
            config_dir = Path(self._hass.config.config_dir)
            cache_paths = [
                str(config_dir / "www" / "cez_hdo" / cache_filename),
                str(config_dir / "www" / debug_filename),
            ]
        else:
            # Fallback to standard paths
            cache_paths = [
                f"/config/www/cez_hdo/{cache_filename}",
                f"/config/www/{debug_filename}",
            ]

        # Nejdříve zkusit načíst z cache
        for cache_path in cache_paths:
            if self._load_from_cache(cache_path):
                _LOGGER.info("CEZ HDO: Loaded from cache: %s", cache_path)
                return

        # Pokud cache není dostupná, zkusit API se zkrácenným timeoutem
        for attempt in range(2):  # Až 2 pokusy
            try:
                api_url = downloader.get_request_url(self.region, self.code)
                _LOGGER.info(
                    "🌐 CEZ HDO: Cache not found, trying API (attempt %d/2) - URL: %s",
                    attempt + 1,
                    api_url,
                )

                response = requests.get(api_url, timeout=10)

                _LOGGER.info("CEZ HDO: HTTP Response status: %d", response.status_code)

                if response.status_code == 200:
                    try:
                        content_str = response.content.decode("utf-8")
                        _LOGGER.debug(
                            "CEZ HDO: Response content length: %d bytes",
                            len(content_str),
                        )

                        json_data = json.loads(content_str)
                        data_count = len(json_data.get("data", []))
                        _LOGGER.info("✅ CEZ HDO: API success, records: %d", data_count)

                        if data_count > 0:
                            self._response_data = json_data
                            self._last_update_success = True

                            # Uložit do cache
                            for cache_path in cache_paths:
                                try:
                                    cache_dir = Path(cache_path).parent
                                    cache_dir.mkdir(parents=True, exist_ok=True)
                                    with open(cache_path, "w", encoding="utf-8") as f:
                                        json.dump(
                                            json_data, f, ensure_ascii=False, indent=2
                                        )
                                    _LOGGER.info(
                                        "💾 CEZ HDO: Data saved to cache: %s",
                                        cache_path,
                                    )
                                    break
                                except Exception as cache_err:
                                    _LOGGER.warning(
                                        "CEZ HDO: Cache save failed for %s: %s",
                                        cache_path,
                                        cache_err,
                                    )
                            return
                        else:
                            _LOGGER.warning("CEZ HDO: API returned empty data array")
                    except (json.JSONDecodeError, UnicodeDecodeError) as parse_err:
                        _LOGGER.error(
                            "CEZ HDO: Failed to parse API response: %s", parse_err
                        )
                elif response.status_code == 502:
                    _LOGGER.warning(
                        "CEZ HDO: Server error 502 - retrying in 3 seconds..."
                    )
                    if attempt == 0:  # Pouze při prvním pokusu čekej
                        time.sleep(3)
                        continue
                else:
                    _LOGGER.error(
                        "CEZ HDO: API request failed - Status: %d", response.status_code
                    )

            except requests.RequestException as req_err:
                _LOGGER.error(
                    "CEZ HDO: Network error (attempt %d/2): %s", attempt + 1, req_err
                )
                if attempt == 0:  # Pouze při prvním pokusu čekej
                    time.sleep(2)
                    continue
            except Exception as general_err:
                _LOGGER.error(
                    "CEZ HDO: Unexpected error during API call: %s", general_err
                )

            break  # Ukončit smyčku pokud nedošlo k 502 nebo network error

        # Pokud vše selže
        _LOGGER.warning("CEZ HDO: Both cache and API failed")
        self._last_update_success = False

    def _save_to_cache(self, cache_file: str, content: str) -> None:
        """Save content to cache file."""
        try:
            # Zajistit že složka existuje
            cache_dir = Path(cache_file).parent
            cache_dir.mkdir(parents=True, exist_ok=True)

            # Uložit soubor
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(content)
            _LOGGER.debug("CEZ HDO: Data cached to %s", cache_file)
        except Exception as e:
            _LOGGER.warning("CEZ HDO: Cache save failed: %s", str(e)[:50])

    def _load_from_cache(self, cache_file: str) -> bool:
        """Load data from cache file. Returns True if successful."""
        try:
            if not Path(cache_file).exists():
                return False

            with open(cache_file, "r", encoding="utf-8") as f:
                content = f.read()

            json_data = json.loads(content)
            self._response_data = json_data
            self._last_update_success = True
            return True

        except Exception:
            return False

    def _get_hdo_data(self) -> tuple[bool, Any, Any, Any, bool, Any, Any, Any]:
        """Get HDO data from response."""
        if self._response_data is None or not self._last_update_success:
            _LOGGER.warning(
                "CEZ HDO: No data available for parsing (data=%s, success=%s)",
                self._response_data is not None,
                self._last_update_success,
            )
            return False, None, None, None, False, None, None, None

        try:
            result = downloader.isHdo(self._response_data["data"])
            _LOGGER.info("CEZ HDO: Parser result: %s", result)
            return result
        except (KeyError, TypeError) as err:
            _LOGGER.error("Error processing HDO data: %s", err)
            return False, None, None, None, False, None, None, None
