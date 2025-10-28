"""CEZ HDO data downloader and processor."""
from __future__ import annotations
import logging
from datetime import datetime, timedelta, time
from typing import NamedTuple, cast

try:
    # python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:
    # python 3.6-3.8
    from backports.zoneinfo import ZoneInfo  # type: ignore[no-redef]

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/"
CEZ_TIMEZONE = ZoneInfo("Europe/Prague")
SUPPORTED_REGIONS = {"zapad", "sever", "stred", "vychod", "morava"}


class HdoData(NamedTuple):
    """HDO data structure."""

    low_tariff_active: bool
    low_tariff_start: time | None
    low_tariff_end: time | None
    low_tariff_duration: timedelta | None
    high_tariff_active: bool
    high_tariff_start: time | None
    high_tariff_end: time | None
    high_tariff_duration: timedelta | None


def get_correct_region_name(region: str) -> str | None:
    """Get correct region name from user input."""
    region_lower = region.lower()
    for supported_region in SUPPORTED_REGIONS:
        if supported_region in region_lower:
            return supported_region
    _LOGGER.warning("Unsupported region: %s", region)
    return None


def get_request_url(region: str, code: str) -> str:
    """Build request URL for CEZ API."""
    correct_region = get_correct_region_name(region)
    if correct_region is None:
        raise ValueError(f"Unsupported region: {region}")
    return f"{BASE_URL}{correct_region}?code={code.upper()}"


def time_in_range(start: time, end: time, check_time: time) -> bool:
    """Check if time is in range, handling overnight periods."""
    if start <= end:
        return start <= check_time <= end
    return start <= check_time or check_time <= end


def parse_time(time_str: str | None) -> time:
    """Parse time string to time object."""
    if not time_str:
        return datetime.min.time()
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError as err:
        _LOGGER.error("Error parsing time string '%s': %s", time_str, err)
        return datetime.min.time()


def format_duration(duration: timedelta) -> str:
    """Format timedelta to string without microseconds."""
    if duration is None:
        return "0:00:00"

    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours}:{minutes:02d}:{seconds:02d}"


def calculate_duration(from_time: time, to_time: time) -> timedelta:
    """Calculate duration between two times."""
    now = datetime.now(tz=CEZ_TIMEZONE)
    from_datetime = datetime.combine(now.date(), from_time, tzinfo=CEZ_TIMEZONE)
    to_datetime = datetime.combine(now.date(), to_time, tzinfo=CEZ_TIMEZONE)

    # If to_time is before from_time, assume it's the next day
    if to_datetime <= from_datetime:
        to_datetime += timedelta(days=1)

    duration = to_datetime - from_datetime
    return duration


def is_czech_holiday(date: datetime) -> bool:
    """Check if date is Czech public holiday."""
    year = date.year

    # Fixed holidays
    fixed_holidays = [
        (1, 1),  # New Year's Day
        (5, 1),  # Labor Day
        (5, 8),  # Liberation Day
        (7, 5),  # Saints Cyril and Methodius Day
        (7, 6),  # Jan Hus Day
        (9, 28),  # Czech Statehood Day
        (10, 28),  # Independence Day
        (11, 17),  # Freedom Day
        (12, 24),  # Christmas Eve
        (12, 25),  # Christmas Day
        (12, 26),  # St. Stephen's Day
    ]

    for month, day in fixed_holidays:
        if date.month == month and date.day == day:
            return True

    # Easter Monday (variable date)
    # Simple calculation for Easter Monday
    # For precise calculation, we'd need a proper Easter algorithm
    # This is a simplified version for common years
    easter_monday_dates = {
        2024: (4, 1),  # April 1, 2024
        2025: (4, 21),  # April 21, 2025
        2026: (4, 6),  # April 6, 2026
        2027: (3, 29),  # March 29, 2027
        2028: (4, 17),  # April 17, 2028
        2029: (4, 2),  # April 2, 2029
        2030: (4, 22),  # April 22, 2030
    }

    if year in easter_monday_dates:
        easter_month, easter_day = easter_monday_dates[year]
        if date.month == easter_month and date.day == easter_day:
            return True

    return False


def isHdo(
    json_calendar: list[dict],
) -> tuple[
    bool,
    time | None,
    time | None,
    timedelta | None,
    bool,
    time | None,
    time | None,
    timedelta | None,
]:
    """
    Determine HDO state for current timestamp.

    Args:
        json_calendar: JSON calendar schedule from CEZ

    Returns:
        Tuple with HDO data: (low_tariff_active, low_start, low_end, low_duration,
                             high_tariff_active, high_start, high_end, high_duration)
    """
    if not json_calendar or len(json_calendar) < 2:
        _LOGGER.error("Invalid calendar data")
        return False, None, None, None, False, None, None, None

    current_time = datetime.now(tz=CEZ_TIMEZONE)

    # Choose appropriate calendar (weekday vs weekend/holiday)
    # Use weekend calendar for Saturday, Sunday, and public holidays
    is_weekend_or_holiday = (
        current_time.weekday() >= 5  # Saturday (5) or Sunday (6)
        or is_czech_holiday(current_time)  # Czech public holiday
    )
    day_calendar = json_calendar[0] if not is_weekend_or_holiday else json_calendar[1]

    _LOGGER.warning(
        "🗓️  HDO Calendar Selection: Date=%s, Weekday=%d, Is_Holiday=%s, Using=%s calendar, PLATNOST=%s",
        current_time.date(),
        current_time.weekday(),
        is_czech_holiday(current_time),
        "weekend/holiday" if is_weekend_or_holiday else "weekday",
        day_calendar.get("PLATNOST", "Unknown"),
    )

    checked_time = current_time.time()

    # Initialize return values
    low_tariff_active = False
    low_start = low_end = None
    low_duration = None
    high_tariff_active = False
    high_start = high_end = None
    high_duration = None

    try:
        # Build list of all low tariff periods
        low_periods = []

        # Process up to 10 time periods
        for i in range(1, 11):
            start_time = parse_time(day_calendar.get(f"CAS_ZAP_{i}"))
            end_time = parse_time(day_calendar.get(f"CAS_VYP_{i}"))

            if start_time is not None and end_time is not None:
                low_periods.append({"start": start_time, "end": end_time, "index": i})

        # Sort periods by start time
        low_periods.sort(key=lambda x: cast(time, x["start"]))

        _LOGGER.warning(
            "🔍 Low tariff periods: %s",
            [f"{p['start']}-{p['end']}" for p in low_periods],
        )

        # Check if we're currently in a low tariff period
        current_low_period = None
        for period in low_periods:
            period_start = cast(time, period["start"])
            period_end = cast(time, period["end"])
            if time_in_range(period_start, period_end, checked_time):
                current_low_period = period
                break

        if current_low_period:
            # We're in LOW tariff period
            low_tariff_active = True
            low_start = cast(time, current_low_period["start"])
            low_end = cast(time, current_low_period["end"])
            low_duration = calculate_duration(checked_time, low_end)

            # Find next high tariff (starts when current low ends)
            high_start = cast(time, current_low_period["end"])

            # Find next low period after current one
            current_index = low_periods.index(current_low_period)
            next_low_period = low_periods[(current_index + 1) % len(low_periods)]
            high_end = cast(time, next_low_period["start"])
            high_duration = timedelta(0)  # Not active now

            _LOGGER.warning(
                "✅ IN LOW TARIFF: %s-%s, remaining: %s",
                low_start,
                low_end,
                format_duration(low_duration),
            )
        else:
            # We're in HIGH tariff period
            high_tariff_active = True

            # Find which high tariff period we're in
            # by finding the low period that ended before current time
            # and the low period that starts after current time
            prev_low = None
            next_low = None

            for i, period in enumerate(low_periods):
                period_start = cast(time, period["start"])
                if period_start > checked_time:
                    next_low = period
                    if i > 0:
                        prev_low = low_periods[i - 1]
                    else:
                        # Current time is before first low period
                        # Previous low period is the last one (from previous day)
                        prev_low = low_periods[-1] if low_periods else None
                    break

            # If no next_low found, it means we're after last period
            if next_low is None and low_periods:
                next_low = low_periods[0]  # First period of next day
                prev_low = low_periods[-1]  # Last period of today

            if prev_low and next_low:
                high_start = cast(time, prev_low["end"])
                high_end = cast(time, next_low["start"])
                high_duration = calculate_duration(checked_time, high_end)

                # Next low tariff info
                low_start = cast(time, next_low["start"])
                low_end = cast(time, next_low["end"])
                low_duration = calculate_duration(checked_time, low_start)

                _LOGGER.warning(
                    "🔴 IN HIGH TARIFF: %s-%s, remaining: %s, next low: %s",
                    high_start,
                    high_end,
                    format_duration(high_duration),
                    low_start,
                )
            else:
                _LOGGER.error("Could not determine high tariff period boundaries")

    except (KeyError, TypeError, ValueError) as err:
        _LOGGER.error("Error processing calendar data: %s", err)

    return (
        low_tariff_active,
        low_start,
        low_end,
        low_duration,
        high_tariff_active,
        high_start,
        high_end,
        high_duration,
    )
