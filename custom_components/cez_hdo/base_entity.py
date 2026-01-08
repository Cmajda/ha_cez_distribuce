"""Base entity for CEZ HDO sensors."""
from __future__ import annotations
import json
import logging
import time
from datetime import timedelta, datetime
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

    def __init__(self, ean: str, name: str, signal: str | None = None) -> None:
        """Initialize the sensor."""
        self.ean = ean
        self.signal = signal
        self._name = name
        self._response_data: dict[str, Any] | None = None
        self._last_update_success = False
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
            # Získej aktuální a následující NT intervaly
            try:
                result = self._get_hdo_data()
                (
                    low_tariff_active,
                    low_start,
                    low_end,
                    low_duration,
                    high_tariff_active,
                    high_start,
                    high_end,
                    high_duration,
                    next_low_start,
                    next_low_end,
                ) = result if len(result) == 10 else (*result, None, None)

                # Aktuální NT interval
                if low_tariff_active and low_start and low_end:
                    attributes["nt_aktualni_zacatek"] = low_start.strftime("%H:%M:%S")
                    attributes["nt_aktualni_konec"] = low_end.strftime("%H:%M:%S")
                # Následující NT interval
                if next_low_start and next_low_end:
                    attributes["nt_dalsi_zacatek"] = next_low_start.strftime("%H:%M:%S")
                    attributes["nt_dalsi_konec"] = next_low_end.strftime("%H:%M:%S")
                # Aktuální VT interval
                if high_tariff_active and high_start and high_end:
                    attributes["vt_aktualni_zacatek"] = high_start.strftime("%H:%M:%S")
                    attributes["vt_aktualni_konec"] = high_end.strftime("%H:%M:%S")
                # Následující VT interval (mezi NT intervaly)
                # Najdi další VT interval podle pořadí intervalů
                # Pokud jsme v NT, další VT je mezi aktuálním a následujícím NT
                if low_tariff_active and low_end and next_low_start:
                    attributes["vt_dalsi_zacatek"] = low_end.strftime("%H:%M:%S")
                    attributes["vt_dalsi_konec"] = next_low_start.strftime("%H:%M:%S")
                # Pokud jsme ve VT, další VT je až po následujícím NT
                if high_tariff_active and next_low_end and next_low_start:
                    attributes["vt_dalsi_zacatek"] = next_low_end.strftime("%H:%M:%S")
                    # Najdi konec dalšího VT (začátek dalšího NT, pokud existuje)
                    # Získáme seznam všech NT intervalů
                    nt_intervals = []
                    if self._response_data is not None:
                        try:
                            result2 = self._get_hdo_data()
                            (
                                _lta, _ls, _le, _ld, _hta, _hs, _he, _hd, nls, nle
                            ) = result2 if len(result2) == 10 else (*result2, None, None)
                            if nls and nle:
                                nt_intervals.append((nls, nle))
                        except Exception:
                            pass
                    # Pokud existuje další NT interval po next_low_end
                    if len(nt_intervals) > 0:
                        # Najdi první NT interval, který začíná po next_low_end
                        dalsi_nt = None
                        for s, e in nt_intervals:
                            if s > next_low_end:
                                dalsi_nt = (s, e)
                                break
                        if dalsi_nt:
                            attributes["vt_dalsi_konec"] = dalsi_nt[0].strftime("%H:%M:%S")
                        else:
                            attributes["vt_dalsi_konec"] = None
                    else:
                        attributes["vt_dalsi_konec"] = None
            except Exception as err:
                attributes["hdo_error"] = str(err)
            attributes["response_json"] = self._response_data
        return attributes

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self) -> None:
        """Fetch new state data for the sensor with cache fallback and validity check."""
        cache_paths = [
            "/config/www/cez_hdo/cez_hdo.json",
            "/config/www/cez_hdo_debug.json",
        ]

        # Zkusit načíst platná data z cache
        for cache_path in cache_paths:
            if self._load_from_cache(cache_path, check_validity=True):
                _LOGGER.info("CEZ HDO: Loaded valid cache: %s", cache_path)
                return

        # Pokud cache není dostupná nebo je neplatná, zkusit API
        for attempt in range(2):
            try:
                api_url = downloader.BASE_URL
                # Stáhnout data pro předchozí den i pro dnešek
                request_data_today = downloader.get_request_data(self.ean, days=0)
                request_data_prev = downloader.get_request_data(self.ean, days=-1)

                _LOGGER.info(
                    "🌐 CEZ HDO: Cache not found or expired, trying API (attempt %d/2) - URL: %s, EAN: %s",
                    attempt + 1,
                    api_url,
                    self.ean,
                )

                response_today = requests.post(
                    api_url,
                    json=request_data_today,
                    timeout=10,
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    },
                )
                response_prev = requests.post(
                    api_url,
                    json=request_data_prev,
                    timeout=10,
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    },
                )

                _LOGGER.info("CEZ HDO: HTTP Response status (today): %d", response_today.status_code)
                _LOGGER.info("CEZ HDO: HTTP Response status (prev): %d", response_prev.status_code)

                if response_today.status_code == 200 and response_prev.status_code == 200:
                    try:
                        content_today = response_today.content.decode("utf-8")
                        content_prev = response_prev.content.decode("utf-8")
                        json_today = json.loads(content_today)
                        json_prev = json.loads(content_prev)

                        # Sloučit signály z obou odpovědí
                        signals_today = json_today.get("data", {}).get("signals", [])
                        signals_prev = json_prev.get("data", {}).get("signals", [])
                        merged_signals = signals_prev + signals_today
                        merged_json = json_today
                        if "data" not in merged_json:
                            merged_json["data"] = {}
                        merged_json["data"]["signals"] = merged_signals

                        signals_count = len(merged_signals)
                        _LOGGER.info(
                            "✅ CEZ HDO: API success, merged signals: %d", signals_count
                        )

                        # Uložit nová data do cache
                        for cache_path in cache_paths:
                            try:
                                cache_dir = Path(cache_path).parent
                                cache_dir.mkdir(parents=True, exist_ok=True)
                                cache_data = {
                                    "timestamp": datetime.now().isoformat(),
                                    "data": merged_json,
                                }
                                with open(cache_path, "w", encoding="utf-8") as f:
                                    json.dump(
                                        cache_data, f, ensure_ascii=False, indent=2
                                    )
                                _LOGGER.info(
                                    "💾 CEZ HDO: Data saved to cache: %s (signals: %d)",
                                    cache_path,
                                    signals_count,
                                )
                            except Exception as cache_err:
                                _LOGGER.warning(
                                    "CEZ HDO: Failed to save cache: %s (%s)",
                                    cache_path,
                                    cache_err,
                                )
                        self._response_data = merged_json
                        self._last_update_success = True
                        return
                    except Exception as parse_err:
                        _LOGGER.error("CEZ HDO: Failed to parse/merge API response: %s", parse_err)
                else:
                    _LOGGER.error("CEZ HDO: API HTTP error: today=%d, prev=%d", response_today.status_code, response_prev.status_code)
            except Exception as e:
                _LOGGER.error("CEZ HDO: API request failed: %s", e)
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

    def _load_from_cache(self, cache_file: str, check_validity: bool = False) -> bool:
        """Load data from cache file. Returns True if successful and valid."""
        try:
            if not Path(cache_file).exists():
                return False

            with open(cache_file, "r", encoding="utf-8") as f:
                content = f.read()

            cache_data = json.loads(content)

            # Nový formát s timestampem
            if "data" in cache_data and "timestamp" in cache_data:
                json_data = cache_data["data"]
                timestamp = cache_data["timestamp"]
                cache_time = datetime.fromisoformat(timestamp)
                now = datetime.now()
                age = now - cache_time
                if check_validity and age > timedelta(days=1):
                    _LOGGER.info(
                        "CEZ HDO: Cache expired (%s, age: %s), ignoring.",
                        cache_file,
                        age,
                    )
                    return False
                _LOGGER.info(
                    "CEZ HDO: Loaded cache from %s (timestamp: %s)",
                    cache_file,
                    timestamp,
                )
            else:
                # Starý formát - přímo data, vždy považovat za neplatné pokud je vyžadována validita
                if check_validity:
                    _LOGGER.info("CEZ HDO: Legacy cache format, ignoring for validity.")
                    return False
                json_data = cache_data
                _LOGGER.info("CEZ HDO: Loaded legacy cache from %s", cache_file)

            self._response_data = json_data
            self._last_update_success = True
            return True

        except Exception as e:
            _LOGGER.warning("CEZ HDO: Failed to load cache from %s: %s", cache_file, e)
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
            # Pass signal parameter to isHdo if specified
            if self.signal:
                result = downloader.isHdo(
                    self._response_data, preferred_signal=self.signal
                )
            else:
                result = downloader.isHdo(self._response_data)
            _LOGGER.info("CEZ HDO: Parser result: %s", result)
            return result
        except (KeyError, TypeError) as err:
            _LOGGER.error("Error processing HDO data: %s", err)
            return False, None, None, None, False, None, None, None
