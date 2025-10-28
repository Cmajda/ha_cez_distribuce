"""CEZ HDO data downloader and processor."""
from __future__ import annotations
import logging
from datetime import datetime, timedelta, time
from typing import NamedTuple

try:
    # python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:
    # python 3.6-3.8
    from backports.zoneinfo import ZoneInfo

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


def format_duration(duration: timedelta) -> str:
    """Format timedelta to h:mm:ss without microseconds."""
    if duration is None:
        return "0:00:00"
    
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours}:{minutes:02d}:{seconds:02d}"


def is_czech_holiday(date: datetime) -> bool:
    """Check if date is Czech public holiday."""
    year = date.year
    
    # Fixed holidays
    fixed_holidays = [
        (1, 1),   # New Year's Day
        (5, 1),   # Labor Day
        (5, 8),   # Liberation Day
        (7, 5),   # Saints Cyril and Methodius Day
        (7, 6),   # Jan Hus Day
        (9, 28),  # Czech Statehood Day
        (10, 28), # Independence Day
        (11, 17), # Freedom Day
        (12, 24), # Christmas Eve
        (12, 25), # Christmas Day
        (12, 26), # St. Stephen's Day
    ]
    
    for month, day in fixed_holidays:
        if date.month == month and date.day == day:
            return True
    
    # Easter Monday (variable date)
    # Simple calculation for Easter Monday
    # For precise calculation, we'd need a proper Easter algorithm
    # This is a simplified version for common years
    easter_monday_dates = {
        2024: (4, 1),   # April 1, 2024
        2025: (4, 21),  # April 21, 2025
        2026: (4, 6),   # April 6, 2026
        2027: (3, 29),  # March 29, 2027
        2028: (4, 17),  # April 17, 2028
        2029: (4, 2),   # April 2, 2029
        2030: (4, 22),  # April 22, 2030
    }
    
    if year in easter_monday_dates:
        easter_month, easter_day = easter_monday_dates[year]
        if date.month == easter_month and date.day == easter_day:
            return True
    
    return False


def isHdo(json_calendar: list[dict]) -> tuple[bool, time | None, time | None, timedelta | None, bool, time | None, time | None, timedelta | None]:
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
        current_time.weekday() >= 5 or  # Saturday (5) or Sunday (6)
        is_czech_holiday(current_time)   # Czech public holiday
    )
    day_calendar = json_calendar[0] if not is_weekend_or_holiday else json_calendar[1]
    
    _LOGGER.warning("🗓️  HDO Calendar Selection: Date=%s, Weekday=%d, Is_Holiday=%s, Using=%s calendar, PLATNOST=%s", 
                    current_time.date(), current_time.weekday(), 
                    is_czech_holiday(current_time),
                    "weekend/holiday" if is_weekend_or_holiday else "weekday",
                    day_calendar.get("PLATNOST", "Unknown"))
    
    checked_time = current_time.time()
    
    # Initialize return values
    low_tariff_active = False
    low_start = low_end = None
    low_duration = None
    high_tariff_active = False
    high_start = high_end = None
    high_duration = None
    
    try:
        # Process up to 10 time periods
        for i in range(1, 11):
            next_index = 1 if i < 10 else 0
            
            start_time_low = parse_time(day_calendar.get(f"CAS_ZAP_{i}"))
            end_time_low = parse_time(day_calendar.get(f"CAS_VYP_{i}"))
            start_time_high = parse_time(day_calendar.get(f"CAS_VYP_{i}"))
            end_time_high = parse_time(day_calendar.get(f"CAS_ZAP_{i + next_index}"))
            
            # Check low tariff
            if start_time_low != end_time_low and time_in_range(start_time_low, end_time_low, checked_time):
                low_tariff_active = True
                low_start = start_time_low
                low_end = end_time_low
                low_duration = calculate_duration(checked_time, end_time_low)
                high_start = end_time_low
                high_end = end_time_high  # Set high tariff end time
                high_duration = timedelta(0)
                
            # Check high tariff
            elif start_time_high != end_time_high and time_in_range(start_time_high, end_time_high, checked_time):
                high_tariff_active = True
                high_start = start_time_high
                high_end = end_time_high
                high_duration = calculate_duration(checked_time, end_time_high)
                low_end = start_time_low  # Set low tariff end time for next period
                
    except (KeyError, TypeError, ValueError) as err:
        _LOGGER.error("Error processing calendar data: %s", err)
        
    return (low_tariff_active, low_start, low_end, low_duration,
            high_tariff_active, high_start, high_end, high_duration)
