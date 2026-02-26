"""DataUpdateCoordinator for ČEZ HDO integration."""

from __future__ import annotations

import json
import logging
import random
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any, Callable

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_point_in_time, async_track_time_interval
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import downloader
from .const import (
    AUTO_REFRESH_END_HOUR,
    AUTO_REFRESH_START_HOUR,
    CONF_AUTO_REFRESH,
    DEFAULT_AUTO_REFRESH,
    MAX_DAILY_OCR_ATTEMPTS,
    MIN_RETRY_DELAY_MINUTES,
    ean_suffix,
    mask_ean,
)

_LOGGER = logging.getLogger(__name__)

# Data validity period - HDO data is valid for 6 days
DATA_VALIDITY_DAYS = 6
DATA_WARNING_DAYS = 5  # Show warning 1 day before expiry

# Update interval for state recalculation - needs to be frequent for countdown
STATE_UPDATE_INTERVAL = timedelta(seconds=5)

# Update interval for data expiry check
DATA_CHECK_INTERVAL = timedelta(hours=1)

# Cache directory - stored in .storage/cez_hdo/ (survives integration updates)
# Previously was in custom_components/cez_hdo/data/ which got deleted on updates
CACHE_SUBDIR = ".storage/cez_hdo"
OLD_CACHE_SUBDIR = "custom_components/cez_hdo/data"  # For migration
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
        auto_refresh: bool = DEFAULT_AUTO_REFRESH,
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

        # Auto-refresh configuration
        self._auto_refresh_enabled: bool = auto_refresh
        self._daily_attempts: int = 0
        self._last_attempt_date: date | None = None
        self._data_fetch_successful_today: bool = False
        self._next_attempt_unsub: Callable[[], None] | None = None
        self._next_attempt_time: datetime | None = None

        # Use hass.config.path() for proper path resolution
        # Cache files use EAN suffix (last 6 digits) to support multiple instances
        self._cache_dir = Path(hass.config.path(CACHE_SUBDIR))
        ean_short = ean_suffix(ean)
        self._cache_file = self._cache_dir / f"cache_{ean_short}.json"
        self._prices_file = self._cache_dir / f"prices_{ean_short}.json"
        self._refresh_state_file = self._cache_dir / f"refresh_state_{ean_short}.json"

        # Initialize data container
        self.data = CezHdoData()

        _LOGGER.debug(
            "CezHdoCoordinator initialized: ean=%s, signal=%s, cache=%s, auto_refresh=%s",
            mask_ean(self.ean),
            self.signal,
            self._cache_file,
            self._auto_refresh_enabled,
        )

    async def async_initialize(self) -> None:
        """Initialize coordinator - load cache and perform first refresh.

        This method is for YAML-based platforms. For config entry platforms,
        use async_config_entry_first_refresh() instead.
        """
        # Ensure cache directory exists
        await self.hass.async_add_executor_job(self._ensure_cache_dir)

        # Migrate data from old location (custom_components/cez_hdo/data/)
        await self.hass.async_add_executor_job(self._migrate_old_cache)

        # Load prices from storage
        await self._async_load_prices()

        # Load auto-refresh state
        await self._async_load_refresh_state()

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
            # Mark as successful fetch today
            self._data_fetch_successful_today = True
            self._last_attempt_date = date.today()
            await self._async_save_refresh_state()
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

        # Schedule auto-refresh if enabled and data is expiring
        if self._auto_refresh_enabled:
            await self._async_schedule_auto_refresh()

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

    def stop_auto_refresh(self) -> None:
        """Stop scheduled auto-refresh attempts."""
        if self._next_attempt_unsub is not None:
            self._next_attempt_unsub()
            self._next_attempt_unsub = None
            self._next_attempt_time = None
            _LOGGER.debug("CezHdoCoordinator: Stopped auto-refresh scheduling")

    async def _async_load_refresh_state(self) -> None:
        """Load auto-refresh state from storage."""
        state = await self.hass.async_add_executor_job(self._load_refresh_state)
        if state:
            stored_date = state.get("last_attempt_date")
            if stored_date:
                try:
                    self._last_attempt_date = date.fromisoformat(stored_date)
                except ValueError:
                    self._last_attempt_date = None

            # Reset counters if it's a new day
            if self._last_attempt_date != date.today():
                self._daily_attempts = 0
                self._data_fetch_successful_today = False
                self._last_attempt_date = date.today()
            else:
                self._daily_attempts = state.get("daily_attempts", 0)
                self._data_fetch_successful_today = state.get("successful_today", False)

            # Load next attempt time (informational only, not used for scheduling)
            next_time_str = state.get("next_attempt_time")
            if next_time_str:
                try:
                    self._next_attempt_time = datetime.fromisoformat(next_time_str)
                except ValueError:
                    self._next_attempt_time = None

            _LOGGER.debug(
                "CezHdoCoordinator: Loaded refresh state - attempts: %d, successful: %s, next: %s",
                self._daily_attempts,
                self._data_fetch_successful_today,
                self._next_attempt_time.strftime("%H:%M:%S") if self._next_attempt_time else None,
            )

    def _load_refresh_state(self) -> dict[str, Any] | None:
        """Load refresh state from file (blocking)."""
        try:
            if self._refresh_state_file.exists():
                with open(self._refresh_state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to load refresh state: %s", err)
        return None

    async def _async_save_refresh_state(self) -> None:
        """Save auto-refresh state to storage."""
        await self.hass.async_add_executor_job(self._save_refresh_state)

    def _save_refresh_state(self) -> None:
        """Save refresh state to file (blocking)."""
        try:
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            state = {
                "last_attempt_date": self._last_attempt_date.isoformat() if self._last_attempt_date else None,
                "daily_attempts": self._daily_attempts,
                "successful_today": self._data_fetch_successful_today,
                "next_attempt_time": self._next_attempt_time.isoformat() if self._next_attempt_time else None,
            }
            with open(self._refresh_state_file, "w", encoding="utf-8") as f:
                json.dump(state, f)
            _LOGGER.debug("CezHdoCoordinator: Saved refresh state")
        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to save refresh state: %s", err)

    async def _async_schedule_auto_refresh(self, min_delay_minutes: int = 0, after_failure: bool = False) -> None:
        """Schedule the next auto-refresh attempt if needed.

        Args:
            min_delay_minutes: Minimum delay in minutes before next attempt (used after failure).
            after_failure: If True, log scheduling as WARNING (visible in default logs).
        """
        if not self._auto_refresh_enabled:
            return

        # Check if it's a new day - reset counters
        today = date.today()
        if self._last_attempt_date != today:
            self._daily_attempts = 0
            self._data_fetch_successful_today = False
            self._last_attempt_date = today
            await self._async_save_refresh_state()

        # Don't schedule if already successful today
        if self._data_fetch_successful_today:
            _LOGGER.debug("CezHdoCoordinator: Already fetched data successfully today, skipping")
            return

        # Don't schedule if we've used all attempts for today
        if self._daily_attempts >= MAX_DAILY_OCR_ATTEMPTS:
            _LOGGER.debug(
                "CezHdoCoordinator: Used all %d attempts for today",
                MAX_DAILY_OCR_ATTEMPTS,
            )
            return

        # Calculate next attempt time
        now = datetime.now()
        current_hour = now.hour

        # Only schedule during allowed hours
        if current_hour < AUTO_REFRESH_START_HOUR:
            # Schedule for start hour
            next_time = now.replace(hour=AUTO_REFRESH_START_HOUR, minute=random.randint(0, 59), second=0, microsecond=0)
        elif current_hour >= AUTO_REFRESH_END_HOUR:
            # Schedule for tomorrow
            tomorrow = now + timedelta(days=1)
            next_time = tomorrow.replace(
                hour=AUTO_REFRESH_START_HOUR, minute=random.randint(0, 59), second=0, microsecond=0
            )
        else:
            # Schedule randomly within remaining hours today
            remaining_attempts = MAX_DAILY_OCR_ATTEMPTS - self._daily_attempts
            remaining_hours = AUTO_REFRESH_END_HOUR - current_hour

            if remaining_hours <= 0 or remaining_attempts <= 0:
                return

            # Spread attempts evenly, add some randomness
            hours_per_attempt = remaining_hours / remaining_attempts
            next_hour_offset = random.uniform(0.5, min(hours_per_attempt, 2.0))
            next_time = now + timedelta(hours=next_hour_offset)

        # Apply minimum delay if specified (e.g., 10 minutes after failure)
        if min_delay_minutes > 0:
            min_next_time = now + timedelta(minutes=min_delay_minutes)
            if next_time < min_next_time:
                next_time = min_next_time

        # Cancel any existing scheduled attempt
        if self._next_attempt_unsub is not None:
            self._next_attempt_unsub()

        # Log at WARNING level after failure, INFO otherwise
        if after_failure:
            _LOGGER.warning(
                "CezHdoCoordinator: Next auto-refresh attempt %d/%d scheduled at %s",
                self._daily_attempts + 1,
                MAX_DAILY_OCR_ATTEMPTS,
                next_time.strftime("%H:%M:%S"),
            )
        else:
            _LOGGER.info(
                "CezHdoCoordinator: Next auto-refresh attempt %d/%d scheduled at %s",
                self._daily_attempts + 1,
                MAX_DAILY_OCR_ATTEMPTS,
                next_time.strftime("%H:%M:%S"),
            )

        # Store for state file and schedule
        self._next_attempt_time = next_time
        await self._async_save_refresh_state()

        self._next_attempt_unsub = async_track_point_in_time(
            self.hass,
            self._async_auto_refresh_attempt,
            next_time,
        )

    async def _async_auto_refresh_attempt(self, _now: datetime | None = None) -> None:
        """Perform an automatic data refresh attempt using OCR."""
        self._next_attempt_unsub = None  # Clear the subscription
        self._next_attempt_time = None  # Clear scheduled time
        self._daily_attempts += 1

        _LOGGER.info(
            "CezHdoCoordinator: Starting auto-refresh attempt %d/%d for EAN %s",
            self._daily_attempts,
            MAX_DAILY_OCR_ATTEMPTS,
            mask_ean(self.ean),
        )

        try:
            # Try to fetch data with automatic CAPTCHA solving
            new_data = await self.hass.async_add_executor_job(
                downloader.fetch_data_with_auto_captcha,
                self.ean,
            )

            if new_data and new_data.get("data"):
                _LOGGER.info(
                    "CezHdoCoordinator: Auto-refresh successful for EAN %s!",
                    mask_ean(self.ean),
                )

                # Save to cache
                await self.hass.async_add_executor_job(self._save_to_cache, new_data)

                # Update data
                self._parse_data(new_data)
                self.data.raw_data = new_data
                self.data.last_update = datetime.now()

                # Mark as successful
                self._data_fetch_successful_today = True
                self._next_attempt_time = None  # No more attempts needed today
                self._warning_shown = False
                self._expired_shown = False

                # Notify listeners
                self.async_set_updated_data(self.data)

                # Show success notification
                await self._show_auto_refresh_notification(success=True)

                # Log next refresh info
                _LOGGER.info(
                    "CezHdoCoordinator: Next auto-refresh scheduled for tomorrow after %02d:00",
                    AUTO_REFRESH_START_HOUR,
                )

            else:
                _LOGGER.warning(
                    "CezHdoCoordinator: Auto-refresh attempt %d/%d failed",
                    self._daily_attempts,
                    MAX_DAILY_OCR_ATTEMPTS,
                )

                # Schedule next attempt with minimum delay (log as warning)
                await self._async_schedule_auto_refresh(min_delay_minutes=MIN_RETRY_DELAY_MINUTES, after_failure=True)

        except Exception as err:
            _LOGGER.error(
                "CezHdoCoordinator: Auto-refresh error: %s",
                err,
            )
            # Schedule next attempt with minimum delay (log as warning)
            await self._async_schedule_auto_refresh(min_delay_minutes=MIN_RETRY_DELAY_MINUTES, after_failure=True)

        # Save state
        await self._async_save_refresh_state()

    async def _show_auto_refresh_notification(self, success: bool) -> None:
        """Show notification about auto-refresh result."""
        lang = self.hass.config.language or "en"

        if success:
            if lang == "cs":
                title = "ČEZ HDO - Data aktualizována"
                message = "HDO data byla úspěšně automaticky obnovena pomocí OCR."
            else:
                title = "ČEZ HDO - Data Updated"
                message = "HDO data has been automatically refreshed using OCR."

            await self._show_notification(
                title=title,
                message=message,
                notification_id=f"cez_hdo_auto_refresh_{self.ean}",
            )

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

    def _migrate_old_cache(self) -> None:
        """Migrate cache files from old location to new location.

        Old location: custom_components/cez_hdo/data/
        New location: .storage/cez_hdo/

        This ensures data survives integration updates via HACS.
        """
        import shutil

        old_cache_dir = Path(self.hass.config.path(OLD_CACHE_SUBDIR))
        if not old_cache_dir.exists():
            return

        ean_short = ean_suffix(self.ean)
        files_to_migrate = [
            f"cache_{ean_short}.json",
            f"prices_{ean_short}.json",
            f"refresh_state_{ean_short}.json",
        ]

        migrated_count = 0
        for filename in files_to_migrate:
            old_file = old_cache_dir / filename
            new_file = self._cache_dir / filename

            if old_file.exists() and not new_file.exists():
                try:
                    shutil.copy2(old_file, new_file)
                    _LOGGER.info(
                        "CezHdoCoordinator: Migrated %s to new location",
                        filename,
                    )
                    migrated_count += 1
                except Exception as err:
                    _LOGGER.warning(
                        "CezHdoCoordinator: Failed to migrate %s: %s",
                        filename,
                        err,
                    )

        if migrated_count > 0:
            _LOGGER.info(
                "CezHdoCoordinator: Migrated %d files from old cache location",
                migrated_count,
            )

    async def _async_update_data(self) -> CezHdoData:
        """Check data validity, load from cache, and trigger auto-refresh if needed.

        This method:
        1. Loads data from cache
        2. Checks data validity and shows notifications when expiring
        3. Schedules automatic refresh attempts if enabled and data is old
        """
        try:
            # Load data from cache
            cache_loaded = await self.hass.async_add_executor_job(self._load_from_cache)

            if not cache_loaded:
                raise UpdateFailed("No cached HDO data available. Please reconfigure the integration.")

            # Check data age and show notifications
            await self._check_data_validity()

            # Schedule auto-refresh if data is expiring
            if self._auto_refresh_enabled and self.data_age_days >= DATA_WARNING_DAYS:
                await self._async_schedule_auto_refresh()

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
            title, message = await self._get_notification_text("warning", days_old, days_remaining)
            await self._show_notification(
                title=title,
                message=message,
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
            title, message = await self._get_notification_text("expired", days_old, 0)
            await self._show_notification(
                title=title,
                message=message,
                notification_id=f"cez_hdo_expired_{self.ean}",
            )
            _LOGGER.error("CezHdoCoordinator: Data has expired (%d days old)", days_old)

    async def _get_notification_text(
        self, notification_type: str, days_old: int, days_remaining: int
    ) -> tuple[str, str]:
        """Get localized notification text based on Home Assistant language.

        Args:
            notification_type: Type of notification ('warning' or 'expired').
            days_old: How many days old the data is.
            days_remaining: Days remaining until expiry.

        Returns:
            Tuple of (title, message) in the appropriate language.
        """
        # Get Home Assistant language setting
        lang = self.hass.config.language or "en"

        # Notification texts in supported languages
        texts = {
            "cs": {
                "warning": {
                    "title": "ČEZ HDO - Data brzy vyprší",
                    "message": (
                        f"HDO data jsou stará {days_old} dní. "
                        f"Zbývá {days_remaining} den/dny do vypršení. "
                        "Prosím překonfigurujte integraci pro načtení nových dat."
                    ),
                },
                "expired": {
                    "title": "ČEZ HDO - Data vypršela!",
                    "message": (
                        f"HDO data jsou stará {days_old} dní a již nejsou platná. "
                        "Prosím smažte a znovu přidejte integraci pro načtení nových dat."
                    ),
                },
            },
            "en": {
                "warning": {
                    "title": "ČEZ HDO - Data expiring soon",
                    "message": (
                        f"HDO data is {days_old} days old. "
                        f"{days_remaining} day(s) remaining until expiry. "
                        "Please reconfigure the integration to fetch new data."
                    ),
                },
                "expired": {
                    "title": "ČEZ HDO - Data expired!",
                    "message": (
                        f"HDO data is {days_old} days old and no longer valid. "
                        "Please delete and re-add the integration to fetch new data."
                    ),
                },
            },
        }

        # Use Czech for Czech, English for everything else
        lang_texts = texts.get(lang, texts["en"])
        notification = lang_texts.get(notification_type, lang_texts["warning"])
        return notification["title"], notification["message"]

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
            _LOGGER.debug(
                "CezHdoCoordinator._save_to_cache: saving to %s, data keys=%s",
                self._cache_file,
                list(data.keys()) if isinstance(data, dict) else "not a dict",
            )
            with open(self._cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            _LOGGER.debug("CezHdoCoordinator: Data saved to cache at %s", self._cache_file)
        except Exception as err:
            _LOGGER.warning("CezHdoCoordinator: Failed to save cache: %s", err)

    def _load_from_cache(self) -> bool:
        """Load data from cache file (blocking). Returns True if successful."""
        try:
            _LOGGER.debug(
                "CezHdoCoordinator._load_from_cache: checking file %s, exists=%s",
                self._cache_file,
                self._cache_file.exists(),
            )
            if not self._cache_file.exists():
                _LOGGER.debug("CezHdoCoordinator._load_from_cache: file does not exist")
                return False

            with open(self._cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            _LOGGER.debug(
                "CezHdoCoordinator._load_from_cache: loaded cache, keys=%s",
                list(cache_data.keys()) if isinstance(cache_data, dict) else "not a dict",
            )

            # Support new format with timestamp and old format
            if "data" in cache_data and "timestamp" in cache_data:
                raw_data = cache_data["data"]
                try:
                    self.data.last_update = datetime.fromisoformat(cache_data["timestamp"])
                except Exception:
                    self.data.last_update = datetime.now()
                _LOGGER.debug(
                    "CezHdoCoordinator._load_from_cache: new format, timestamp=%s",
                    self.data.last_update,
                )
            else:
                # Old format - data directly
                raw_data = cache_data
                self.data.last_update = datetime.now()
                _LOGGER.debug("CezHdoCoordinator._load_from_cache: old format detected")

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
