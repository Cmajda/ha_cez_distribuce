"""DataUpdateCoordinator for ČEZ HDO integration."""
from __future__ import annotations

import json
import logging
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any, Callable

import requests

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import downloader
from .const import ean_suffix, mask_ean

_LOGGER = logging.getLogger(__name__)

# Update interval for API data - HDO data changes rarely (once per day typically)
API_UPDATE_INTERVAL = timedelta(hours=1)

# Update interval for state recalculation - needs to be frequent for countdown
STATE_UPDATE_INTERVAL = timedelta(seconds=5)

# Cache directory and file - stored in custom_components/cez_hdo/data/
CACHE_SUBDIR = "custom_components/cez_hdo/data"
# File names are per-EAN: cache_{ean}.json, prices_{ean}.json


class CezHdoData:
    """Class to hold parsed HDO data."""

    def __init__(self) -> None:
        """Initialize HDO data container."""
        self.raw_data: dict[str, Any] | None = None
        self.last_update: datetime | None = None

        # Parsed current state
        self.low_tariff_active: bool = False
        self.low_tariff_start: time | None = None
        self.low_tariff_end: time | None = None
        self.low_tariff_duration: timedelta | None = None

        self.high_tariff_active: bool = False
        self.high_tariff_start: time | None = None
        self.high_tariff_end: time | None = None
        self.high_tariff_duration: timedelta | None = None

        # Schedule for card
        self.schedule: list[dict[str, Any]] = []

        # Prices (stored separately)
        self.low_tariff_price: float = 0.0
        self.high_tariff_price: float = 0.0


class CezHdoCoordinator(DataUpdateCoordinator[CezHdoData]):
    """Coordinator for ČEZ HDO data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        ean: str,
        signal: str | None = None,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="ČEZ HDO",
            update_interval=API_UPDATE_INTERVAL,
        )
        self.ean = ean
        self.signal = signal
        self._state_update_unsub: Callable[[], None] | None = None

        # Use hass.config.path() for proper path resolution
        # Cache files use EAN suffix (last 6 digits) to support multiple instances
        self._cache_dir = Path(hass.config.path(CACHE_SUBDIR))
        ean_short = ean_suffix(ean)
        self._cache_file = self._cache_dir / f"cache_{ean_short}.json"
        self._prices_file = self._cache_dir / f"prices_{ean_short}.json"

        # Initialize data container
        self.data = CezHdoData()

        _LOGGER.debug(
            "CezHdoCoordinator initialized: ean=%s, signal=%s, cache=%s",
            mask_ean(self.ean),
            self.signal,
            self._cache_file,
        )

    async def async_initialize(self) -> None:
        """Initialize coordinator - load cache and perform first refresh.

        This method is for YAML-based platforms. For config entry platforms,
        use async_config_entry_first_refresh() instead.
        """
        # Ensure cache directory exists
        await self.hass.async_add_executor_job(self._ensure_cache_dir)

        # Load prices from storage
        await self._async_load_prices()

        # Try to load from cache first for quick startup
        cache_loaded = await self.hass.async_add_executor_job(self._load_from_cache)
        if cache_loaded:
            _LOGGER.debug("CezHdoCoordinator: Loaded initial data from cache")

        # Then do the actual refresh (doesn't raise ConfigEntryError)
        await self.async_refresh()

        # Start periodic state recalculation (every 5 seconds)
        self._start_state_updates()

    def _start_state_updates(self) -> None:
        """Start periodic state recalculation."""
        if self._state_update_unsub is not None:
            return  # Already started

        self._state_update_unsub = async_track_time_interval(
            self.hass,
            self._async_recalculate_state,
            STATE_UPDATE_INTERVAL,
        )
        _LOGGER.debug(
            "CezHdoCoordinator: Started state updates every %s", STATE_UPDATE_INTERVAL
        )

    def stop_state_updates(self) -> None:
        """Stop periodic state recalculation."""
        if self._state_update_unsub is not None:
            self._state_update_unsub()
            self._state_update_unsub = None
            _LOGGER.debug("CezHdoCoordinator: Stopped state updates")

    @callback
    def _async_recalculate_state(self, _now: datetime | None = None) -> None:
        """Recalculate current state based on cached data.

        This is called every 5 seconds to update countdown timers
        and active tariff states without fetching from API.
        """
        if self.data.raw_data is None:
            return  # No data to recalculate from

        # Re-parse data with current time
        self._parse_data(self.data.raw_data)

        # Notify all listeners that data has changed
        self.async_set_updated_data(self.data)

    def _ensure_cache_dir(self) -> None:
        """Ensure cache directory exists."""
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    async def _async_update_data(self) -> CezHdoData:
        """Fetch data from API."""
        try:
            # Fetch from API in executor
            raw_data = await self.hass.async_add_executor_job(self._fetch_from_api)

            if raw_data:
                # Save to cache
                await self.hass.async_add_executor_job(self._save_to_cache, raw_data)

                # Parse data
                self._parse_data(raw_data)
                self.data.raw_data = raw_data
                self.data.last_update = datetime.now()

                _LOGGER.debug(
                    "CezHdoCoordinator: Data updated successfully, low_tariff=%s",
                    self.data.low_tariff_active,
                )
                return self.data

            # API failed, try cache
            cache_loaded = await self.hass.async_add_executor_job(self._load_from_cache)
            if cache_loaded:
                _LOGGER.warning("CezHdoCoordinator: API failed, using cached data")
                return self.data

            raise UpdateFailed(
                "Failed to fetch HDO data from API and no cache available"
            )

        except Exception as err:
            # Try cache on any error
            cache_loaded = await self.hass.async_add_executor_job(self._load_from_cache)
            if cache_loaded:
                _LOGGER.warning(
                    "CezHdoCoordinator: Update failed (%s), using cached data",
                    err,
                )
                return self.data
            raise UpdateFailed(f"Failed to update HDO data: {err}") from err

    def _fetch_from_api(self) -> dict[str, Any] | None:
        """Fetch data from ČEZ API (blocking)."""
        try:
            url = downloader.BASE_URL
            request_data = downloader.get_request_data(self.ean)

            response = requests.post(
                url,
                json=request_data,
                timeout=10,
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                },
            )

            if response.status_code == 200:
                json_data = response.json()
                signals_count = len(json_data.get("data", {}).get("signals", []))
                _LOGGER.debug(
                    "CezHdoCoordinator: API success, signals count: %d",
                    signals_count,
                )
                return json_data

            _LOGGER.warning(
                "CezHdoCoordinator: API request failed, status: %d",
                response.status_code,
            )
            return None

        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: API request exception: %s", err)
            return None

    def _save_to_cache(self, data: dict[str, Any]) -> None:
        """Save data to cache file (blocking)."""
        try:
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": data,
            }
            with open(self._cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            _LOGGER.debug("CezHdoCoordinator: Data saved to cache")
        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to save cache: %s", err)

    def _load_from_cache(self) -> bool:
        """Load data from cache file (blocking). Returns True if successful."""
        try:
            if not self._cache_file.exists():
                return False

            with open(self._cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Support new format with timestamp and old format
            if "data" in cache_data and "timestamp" in cache_data:
                raw_data = cache_data["data"]
                try:
                    self.data.last_update = datetime.fromisoformat(
                        cache_data["timestamp"]
                    )
                except Exception:
                    self.data.last_update = datetime.now()
            else:
                # Old format - data directly
                raw_data = cache_data
                self.data.last_update = datetime.now()

            self.data.raw_data = raw_data
            self._parse_data(raw_data)

            _LOGGER.debug("CezHdoCoordinator: Loaded data from cache")
            return True

        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to load cache: %s", err)
            return False

    def _parse_data(self, raw_data: dict[str, Any]) -> None:
        """Parse raw API data into structured format."""
        try:
            result = downloader.isHdo(raw_data, preferred_signal=self.signal)

            # result is tuple: (low_active, low_start, low_end, low_duration,
            #                   high_active, high_start, high_end, high_duration)
            self.data.low_tariff_active = bool(result[0])
            self.data.low_tariff_start = result[1]
            self.data.low_tariff_end = result[2]
            self.data.low_tariff_duration = result[3]

            self.data.high_tariff_active = bool(result[4])
            self.data.high_tariff_start = result[5]
            self.data.high_tariff_end = result[6]
            self.data.high_tariff_duration = result[7]

            # Parse schedule for card
            self._parse_schedule(raw_data)

        except Exception as err:
            _LOGGER.error("CezHdoCoordinator: Failed to parse data: %s", err)

    def _parse_schedule(self, raw_data: dict[str, Any]) -> None:
        """Parse schedule data for the card."""
        try:
            # Use existing function from downloader
            self.data.schedule = downloader.generate_schedule_for_graph(
                raw_data,
                preferred_signal=self.signal,
                days_ahead=7,
            )
        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to parse schedule: %s", err)
            self.data.schedule = []

    async def _async_load_prices(self) -> None:
        """Load prices from storage."""
        prices = await self.hass.async_add_executor_job(self._load_prices)
        self.data.low_tariff_price = prices.get("low_tariff_price", 0.0)
        self.data.high_tariff_price = prices.get("high_tariff_price", 0.0)

    def _load_prices(self) -> dict[str, float]:
        """Load prices from file (blocking)."""
        try:
            if self._prices_file.exists():
                with open(self._prices_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    _LOGGER.debug("CezHdoCoordinator: Loaded prices: %s", data)
                    return data
        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to load prices: %s", err)
        return {"low_tariff_price": 0.0, "high_tariff_price": 0.0}

    async def async_set_prices(self, low_price: float, high_price: float) -> None:
        """Set tariff prices and save to storage."""
        self.data.low_tariff_price = low_price
        self.data.high_tariff_price = high_price

        await self.hass.async_add_executor_job(self._save_prices, low_price, high_price)

        # Notify listeners that data changed
        self.async_set_updated_data(self.data)

        _LOGGER.debug(
            "CezHdoCoordinator: Prices set: NT=%.2f, VT=%.2f",
            low_price,
            high_price,
        )

    def _save_prices(self, low_price: float, high_price: float) -> None:
        """Save prices to file (blocking)."""
        try:
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            with open(self._prices_file, "w", encoding="utf-8") as f:
                json.dump(
                    {"low_tariff_price": low_price, "high_tariff_price": high_price},
                    f,
                )
            _LOGGER.debug(
                "CezHdoCoordinator: Saved prices: NT=%.2f, VT=%.2f",
                low_price,
                high_price,
            )
        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to save prices: %s", err)

    @property
    def current_price(self) -> float:
        """Get current electricity price based on active tariff."""
        if self.data.low_tariff_active:
            return self.data.low_tariff_price
        return self.data.high_tariff_price
