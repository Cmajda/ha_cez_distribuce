"""Base entity for CEZ HDO sensors."""
from __future__ import annotations
import json
import logging
import time
from pathlib import Path
import requests
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

from . import downloader

class CezHdoBaseEntity:
    def __init__(self, ean: str, name: str, signal: str | None = None) -> None:
        self.ean = ean
        self.name = name
        self.signal = signal
        self._response_data = None
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

            cache_data = json.loads(content)

            # Podporovat nový formát s timestampem i starý
            if "data" in cache_data and "timestamp" in cache_data:
                json_data = cache_data["data"]
                timestamp = cache_data["timestamp"]
                _LOGGER.info(
                    "CEZ HDO: Loaded cache from %s (timestamp: %s)",
                    cache_file,
                    timestamp,
                )
            else:
                # Starý formát - přímo data
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
