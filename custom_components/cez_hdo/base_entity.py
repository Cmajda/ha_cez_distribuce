"""Base entity for CEZ HDO sensors."""
from __future__ import annotations
import json
import logging
import time
    def update(self) -> None:
        """Fetch new state data for the sensor with cache fallback."""
        cache_paths = [
            "/config/www/cez_hdo/cez_hdo.json",
            "/config/www/cez_hdo_debug.json",
            "/mnt/ha-config/www/cez_hdo/cez_hdo.json",
            "/mnt/ha-config/www/cez_hdo_debug.json",
        ]

        # Nejdříve zkusit načíst z cache
        for cache_path in cache_paths:
            if self._load_from_cache(cache_path):
                # _load_from_cache už loguje timestamp a cestu
                _LOGGER.info("CEZ HDO: DATA SOURCE = CACHE (%s)", cache_path)
                return

        # Pokud cache není dostupná, zkusit API se zkrácenými timeouty
        for attempt in range(2):  # Až 2 pokusy
            try:
                api_url = downloader.BASE_URL
                request_data = downloader.get_request_data(self.ean)

                _LOGGER.info(
                    "🌐 CEZ HDO: Cache not found, trying API (attempt %d/2) - URL: %s, EAN: %s",
                    attempt + 1,
                    api_url,
                    self.ean,
                )

                response = requests.post(
                    api_url,
                    json=request_data,
                    timeout=10,
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    },
                )

                _LOGGER.info("CEZ HDO: HTTP Response status: %d", response.status_code)

                if response.status_code == 200:
                    try:
                        content_str = response.content.decode("utf-8")
                        _LOGGER.debug(
                            "CEZ HDO: Response content length: %d bytes",
                            len(content_str),
                        )

                        json_data = json.loads(content_str)

                        # Check if we have signals data
                        signals_count = len(
                            json_data.get("data", {}).get("signals", [])
                        )
                        _LOGGER.info(
                            "✅ CEZ HDO: API success, signals: %d", signals_count
                        )

                        # Vždy uloží data do cache pro budoucí použití (i když jsou prázdná)
                        for cache_path in cache_paths:
                            try:
                                cache_dir = Path(cache_path).parent
                                cache_dir.mkdir(parents=True, exist_ok=True)
                                # Přidáme timestamp pro debugging
                                cache_data = {
                                    "timestamp": datetime.now().isoformat(),
                                    "data": json_data,
                                }
                                with open(cache_path, "w", encoding="utf-8") as f:
                                    json.dump(
                                        cache_data, f, ensure_ascii=False, indent=2
                                    )
                                _LOGGER.info(
                                    "💾 CEZ HDO: Data saved to cache: %s (signals: %d, timestamp: %s)",
                                    cache_path,
                                    signals_count,
                                    cache_data["timestamp"],
                                )
                                break
                            except Exception as cache_err:
                                _LOGGER.warning(
                                    "CEZ HDO: Failed to save cache to %s: %s",
                                    cache_path,
                                    cache_err,
                                )

                        self._response_data = json_data
                        self._last_update_success = True
                        _LOGGER.info("CEZ HDO: DATA SOURCE = ONLINE (API)")
                        return
                    except Exception as e:
                        _LOGGER.warning("CEZ HDO: Failed to parse API response: %s", e)
                else:
                    _LOGGER.warning("CEZ HDO: API request failed, status: %d", response.status_code)
            except Exception as e:
                _LOGGER.warning("CEZ HDO: API request exception: %s", e)

                _LOGGER.info("CEZ HDO: HTTP Response status: %d", response.status_code)

                if response.status_code == 200:
                    try:
                        content_str = response.content.decode("utf-8")
                        _LOGGER.debug(
                            "CEZ HDO: Response content length: %d bytes",
                            len(content_str),
                        )

                        json_data = json.loads(content_str)

                        # Check if we have signals data
                        signals_count = len(
                            json_data.get("data", {}).get("signals", [])
                        )
                        _LOGGER.info(
                            "✅ CEZ HDO: API success, signals: %d", signals_count
                        )

                        # Vždy uloží data do cache pro budoucí použití (i když jsou prázdná)
                        for cache_path in cache_paths:
                            try:
                                cache_dir = Path(cache_path).parent
                                cache_dir.mkdir(parents=True, exist_ok=True)
                                # Přidáme timestamp pro debugging
                                cache_data = {
                                    "timestamp": datetime.now().isoformat(),
                                    "data": json_data,
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
                                break
                            except Exception as cache_err:
                                _LOGGER.warning(
                                    "CEZ HDO: Cache save failed for %s: %s",
                                    cache_path,
                                    cache_err,
                                )

                        if signals_count > 0:
                            self._response_data = json_data
                            self._last_update_success = True
                            return
                        else:
                            _LOGGER.warning("CEZ HDO: API returned empty signals array")
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
