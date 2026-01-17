"""Base entity for CEZ HDO sensors."""
from __future__ import annotations
import json
import logging
import time
from pathlib import Path
import requests
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

class CezHdoBaseEntity:

    def __init__(self, ean: str, name: str, signal: str | None = None) -> None:
        self.ean = ean
        self.name = name
        self.signal = signal
        self._response_data = None
        self._last_update_success = False
        self._last_update_time = None  # datetime poslední aktualizace
        self._update_in_progress = False
        self._last_update_attempt_time = None  # datetime posledního pokusu o update
        # Nastav výchozí cestu k cache (přizpůsob podle potřeby)
        self.cache_file = "/config/www/cez_hdo/cez_hdo.json"

    async def _async_update_in_executor(self) -> None:
        """Run blocking update() in HA executor without blocking event loop."""
        if getattr(self, "hass", None) is None:
            return
        if self._update_in_progress:
            return

        self._update_in_progress = True
        self._last_update_attempt_time = datetime.now()
        try:
            await self.hass.async_add_executor_job(self.update)
        finally:
            self._update_in_progress = False

    def update(self) -> None:
        """Aktualizuje cache: včerejší signály z cache (pokud nejsou v API), dnešní a dalších 6 dní z API."""
        from datetime import timedelta
        from . import downloader

        today = datetime.now().strftime("%d.%m.%Y")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
        cache_file = self.cache_file

        # 1. Načti včerejší signály z cache (pokud existují)
        yesterday_signals = []
        if Path(cache_file).exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_content = json.load(f)
                cache_data = cache_content.get("data", cache_content)
                if isinstance(cache_data, dict) and "data" in cache_data:
                    cache_data = cache_data["data"]
                cache_signals = cache_data.get("signals", [])
                # Včerejší signály, které nejsou v API, přidáme později
                yesterday_signals = [
                    s
                    for s in cache_signals
                    if downloader.normalize_datum(s.get("datum")) == yesterday
                ]
                if yesterday_signals:
                    _LOGGER.info("CEZ HDO: Loaded yesterday's signals from cache (%s)", cache_file)
            except Exception as e:
                _LOGGER.warning("CEZ HDO: Failed to read yesterday's signals from cache %s: %s", cache_file, e)

        # 2. Získej signály z API (API obsahuje vždy 7 dní)
        api_url = downloader.BASE_URL
        request_data = downloader.get_request_data(self.ean)
        try:
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
            _LOGGER.info("CEZ HDO: API REQUEST URL: %s", api_url)
            _LOGGER.info("CEZ HDO: API REQUEST PAYLOAD: %s", json.dumps(request_data, ensure_ascii=False))
            _LOGGER.info("CEZ HDO: HTTP Response status: %d", response.status_code)
            try:
                _LOGGER.info("CEZ HDO: API RAW RESPONSE: %s", response.content.decode("utf-8"))
            except Exception as log_err:
                _LOGGER.warning("CEZ HDO: Chyba při logování API odpovědi: %s", log_err)

            if response.status_code == 200:
                content_str = response.content.decode("utf-8")
                json_data = json.loads(content_str)
                signals_api = json_data.get("data", {}).get("signals", [])
                # Z API vezmi všechny signály (7 dní)
                api_datums = {downloader.normalize_datum(s.get("datum")) for s in signals_api}
                # Přidej včerejší signály z cache, pokud nejsou v API
                extra_yesterday = [
                    s
                    for s in yesterday_signals
                    if downloader.normalize_datum(s.get("datum")) not in api_datums
                ]
                result_signals = extra_yesterday + signals_api

                # 4. Vytvořit novou strukturu s těmito signály
                filtered_json_data = json_data.copy()
                if "data" in filtered_json_data:
                    filtered_json_data["data"] = filtered_json_data["data"].copy()
                    filtered_json_data["data"]["signals"] = result_signals
                signals_count = len(result_signals)
                _LOGGER.info("✅ CEZ HDO: API success, signals for cache: %d (yesterday extra: %d, api: %d)", signals_count, len(extra_yesterday), len(signals_api))

                # 5. Uložit pouze tyto data do cache
                cache_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": filtered_json_data,
                }
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)
                _LOGGER.info("💾 CEZ HDO: Data saved to cache: %s (signals: %d, timestamp: %s)", cache_file, signals_count, cache_data["timestamp"])

                self._response_data = filtered_json_data
                self._last_update_success = True
                self._last_update_time = datetime.now()
                _LOGGER.info("CEZ HDO: DATA SOURCE = ONLINE (API)")
                return
            else:
                _LOGGER.warning("CEZ HDO: API request failed, status: %d", response.status_code)
        except Exception as e:
            _LOGGER.warning("CEZ HDO: API request exception: %s", e)
        # Pokud vše selže
        _LOGGER.warning("CEZ HDO: Both cache and API failed")
        self._last_update_success = False
    def _save_to_cache(self, cache_file: str, content: str) -> None:
        """Save content to cache file."""
        try:
            cache_dir = Path(cache_file).parent
            cache_dir.mkdir(parents=True, exist_ok=True)
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
                try:
                    self._last_update_time = datetime.fromisoformat(timestamp)
                except Exception:
                    self._last_update_time = datetime.now()
            else:
                # Starý formát - přímo data
                json_data = cache_data
                _LOGGER.info("CEZ HDO: Loaded legacy cache from %s", cache_file)
                self._last_update_time = datetime.now()

            self._response_data = json_data
            self._last_update_success = True
            return True

        except Exception as e:
            _LOGGER.warning("CEZ HDO: Failed to load cache from %s: %s", cache_file, e)
            return False

    def _get_hdo_data(self) -> tuple[bool, any, any, any, bool, any, any, any]:
        """Get HDO data from response. Pokud je třeba, aktualizuje data (max 1x za hodinu)."""
        from datetime import datetime, timedelta
        from . import downloader

        # 0) Preferuj existující cache (umožní fungovat i bez API)
        if self._response_data is None:
            self._load_from_cache(self.cache_file)

        now = datetime.now()
        # 1) Pokud jsou data starší než hodinu, update naplánuj na pozadí.
        if not self._last_update_time or (now - self._last_update_time) > timedelta(hours=1):
            # Neplánuj update příliš často (např. při burstu zápisů stavů).
            if (
                self._last_update_attempt_time is None
                or (now - self._last_update_attempt_time) > timedelta(minutes=5)
            ):
                _LOGGER.info("CEZ HDO: Plánuji update() na pozadí (data jsou stará/není update).")
                if getattr(self, "hass", None) is not None:
                    self.hass.async_create_task(self._async_update_in_executor())
                else:
                    # Fallback mimo HA context (např. testy)
                    self._last_update_attempt_time = now
                    self.update()
                    if self._response_data is None:
                        self._load_from_cache(self.cache_file)

        if self._response_data is None:
            _LOGGER.warning("CEZ HDO: No data available for parsing (cache+api failed)")
            return False, None, None, None, False, None, None, None
        try:
            preferred_signal = None
            if self.signal:
                preferred_signal = self.signal
            else:
                get_signal = getattr(self, "_get_signal", None)
                if callable(get_signal):
                    preferred_signal = get_signal(self._response_data)

            today = datetime.now().strftime("%d.%m.%Y")
            _LOGGER.debug("CEZ HDO: _get_hdo_data preferred_signal=%s, datum=%s", preferred_signal, today)

            # Pokud preferred_signal není známý, nevadí: downloader.get_today_schedule
            # zvolí první dostupný signál pro dnešní den.
            result = downloader.isHdo(self._response_data, preferred_signal=preferred_signal)
            _LOGGER.info("CEZ HDO: Parser result: %s", result)
            return result
        except Exception as err:
            _LOGGER.error("Error processing HDO data: %s", err)
            return False, None, None, None, False, None, None, None
