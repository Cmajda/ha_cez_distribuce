"""DataUpdateCoordinator for ČEZ HDO integration."""

from __future__ import annotations

import json
import logging
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any, Callable

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import downloader
from .const import ean_suffix, mask_ean

_LOGGER = logging.getLogger(__name__)

# Data validity period - HDO data is valid for 6 days
DATA_VALIDITY_DAYS = 6
DATA_WARNING_DAYS = 5  # Show warning 1 day before expiry

# Update interval for state recalculation - needs to be frequent for countdown
STATE_UPDATE_INTERVAL = timedelta(seconds=5)

# Update interval for data expiry check
DATA_CHECK_INTERVAL = timedelta(hours=1)

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
            update_interval=DATA_CHECK_INTERVAL,
        )
        self.ean = ean
        self.signal = signal
        self._state_update_unsub: Callable[[], None] | None = None
        self._warning_shown: bool = False
        self._expired_shown: bool = False

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

        # Check if we have initial data from config flow (CAPTCHA validation)
        _LOGGER.debug(
            "CezHdoCoordinator.async_initialize: checking for initial data, ean=%s, hass.data keys=%s",
            mask_ean(self.ean),
            list(self.hass.data.get("cez_hdo_initial_data", {}).keys()),
        )
        initial_data = self.hass.data.get("cez_hdo_initial_data", {}).get(self.ean)
        if initial_data:
            _LOGGER.info(
                "CezHdoCoordinator: Using initial data from config flow for EAN %s",
                mask_ean(self.ean),
            )
            # Save to cache and use it
            await self.hass.async_add_executor_job(self._save_to_cache, initial_data)
            self._parse_data(initial_data)
            self.data.raw_data = initial_data
            self.data.last_update = datetime.now()
            # Clean up the temporary data
            self.hass.data.get("cez_hdo_initial_data", {}).pop(self.ean, None)
            _LOGGER.debug("CezHdoCoordinator: Initial data saved to cache")
        else:
            _LOGGER.debug("CezHdoCoordinator: No initial data found, trying cache")
            # Try to load from cache first for quick startup
            cache_loaded = await self.hass.async_add_executor_job(self._load_from_cache)
            if cache_loaded:
                _LOGGER.debug("CezHdoCoordinator: Loaded initial data from cache")

            # Then do the actual refresh (doesn't raise ConfigEntryError)
            await self.async_refresh()

        # Start periodic state recalculation (every 5 seconds)
        self._start_state_updates()

    @property
    def data_valid_until(self) -> datetime | None:
        """Return datetime when cached data expires."""
        if self.data.last_update is None:
            return None
        return self.data.last_update + timedelta(days=DATA_VALIDITY_DAYS)

    @property
    def data_is_valid(self) -> bool:
        """Return True if cached data is still valid."""
        valid_until = self.data_valid_until
        if valid_until is None:
            return False
        return datetime.now() < valid_until

    @property
    def days_until_expiry(self) -> int:
        """Return number of days until data expires (can be negative if expired)."""
        valid_until = self.data_valid_until
        if valid_until is None:
            return 0
        delta = valid_until - datetime.now()
        return delta.days

    @property
    def data_age_days(self) -> int:
        """Return how many days old the data is."""
        if self.data.last_update is None:
            return 0
        return (datetime.now() - self.data.last_update).days

    def _start_state_updates(self) -> None:
        """Start periodic state recalculation."""
        if self._state_update_unsub is not None:
            return  # Already started

        self._state_update_unsub = async_track_time_interval(
            self.hass,
            self._async_recalculate_state,
            STATE_UPDATE_INTERVAL,
        )
        _LOGGER.debug("CezHdoCoordinator: Started state updates every %s", STATE_UPDATE_INTERVAL)

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
        """Check data validity and load from cache.

        Due to CAPTCHA protection on ČEZ API, we only fetch data during
        initial configuration. This method only checks cache validity
        and shows notifications when data is about to expire.
        """
        try:
            # Load data from cache
            cache_loaded = await self.hass.async_add_executor_job(self._load_from_cache)

            if not cache_loaded:
                raise UpdateFailed("No cached HDO data available. Please reconfigure the integration.")

            # Check data age and show notifications
            await self._check_data_validity()

            _LOGGER.debug(
                "CezHdoCoordinator: Data loaded from cache, low_tariff=%s",
                self.data.low_tariff_active,
            )
            return self.data

        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Failed to load HDO data: {err}") from err

    async def _check_data_validity(self) -> None:
        """Check if cached data is still valid and show notifications."""
        if self.data.last_update is None:
            return

        data_age = datetime.now() - self.data.last_update
        days_old = data_age.days

        # Show warning notification at day 5
        if days_old >= DATA_WARNING_DAYS and not self._warning_shown:
            self._warning_shown = True
            days_remaining = DATA_VALIDITY_DAYS - days_old
            await self._show_notification(
                title="ČEZ HDO - Data brzy vyprší",
                message=(
                    f"HDO data jsou stará {days_old} dní. "
                    f"Zbývá {days_remaining} den/dny do vypršení. "
                    "Prosím překonfigurujte integraci pro načtení nových dat."
                ),
                notification_id=f"cez_hdo_warning_{self.ean}",
            )
            _LOGGER.warning(
                "CezHdoCoordinator: Data is %d days old, will expire in %d days",
                days_old,
                days_remaining,
            )

        # Show expired notification at day 6
        if days_old >= DATA_VALIDITY_DAYS and not self._expired_shown:
            self._expired_shown = True
            await self._show_notification(
                title="ČEZ HDO - Data vypršela!",
                message=(
                    f"HDO data jsou stará {days_old} dní a již nejsou platná. "
                    "Prosím smažte a znovu přidejte integraci pro načtení nových dat."
                ),
                notification_id=f"cez_hdo_expired_{self.ean}",
            )
            _LOGGER.error("CezHdoCoordinator: Data has expired (%d days old)", days_old)

    async def _show_notification(self, title: str, message: str, notification_id: str) -> None:
        """Show a persistent notification in Home Assistant."""
        await self.hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": title,
                "message": message,
                "notification_id": notification_id,
            },
        )

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
                    self.data.last_update = datetime.fromisoformat(cache_data["timestamp"])
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
