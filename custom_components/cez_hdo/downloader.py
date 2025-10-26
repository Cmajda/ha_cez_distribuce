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


def calculate_duration(from_time: time, to_time: time) -> timedelta:
    """Calculate duration between two times, handling overnight periods."""
    today = datetime.today().date()
    
    if from_time <= to_time:
        datetime1 = datetime.combine(today, from_time)
        datetime2 = datetime.combine(today, to_time)
    else:
        datetime1 = datetime.combine(today, from_time)
        datetime2 = datetime.combine(today + timedelta(days=1), to_time)

    return datetime2 - datetime1


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
    
    # Choose appropriate calendar (weekday vs weekend)
    day_calendar = json_calendar[0] if current_time.weekday() < 5 else json_calendar[1]
    
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
                high_duration = timedelta(0)
                
            # Check high tariff
            elif start_time_high != end_time_high and time_in_range(start_time_high, end_time_high, checked_time):
                high_tariff_active = True
                high_start = start_time_high
                high_end = end_time_high
                high_duration = calculate_duration(checked_time, end_time_high)
                
    except (KeyError, TypeError, ValueError) as err:
        _LOGGER.error("Error processing calendar data: %s", err)
        
    return (low_tariff_active, low_start, low_end, low_duration,
            high_tariff_active, high_start, high_end, high_duration)


# Backwards compatibility - deprecated functions
def getCorrectRegionName(region: str) -> str | None:
    """Deprecated: Use get_correct_region_name instead."""
    _LOGGER.warning("getCorrectRegionName is deprecated, use get_correct_region_name")
    return get_correct_region_name(region)


def getRequestUrl(region: str, code: str) -> str:
    """Deprecated: Use get_request_url instead."""
    _LOGGER.warning("getRequestUrl is deprecated, use get_request_url")
    return get_request_url(region, code)
