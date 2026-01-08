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

BASE_URL = "https://dip.cezdistribuce.cz/irj/portal/anonymous/casy-spinani?path=switch-times/signals"
CEZ_TIMEZONE = ZoneInfo("Europe/Prague")


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


def get_request_data(ean: str, days: int = 0) -> dict:
    """Build request data for CEZ API. Parametr days: 0=dnes, -1=včera, 1=zitra."""
    return {"ean": ean, "days": days}


def time_in_range(start: time, end: time, check_time: time) -> bool:
    """Check if time is in range, handling overnight periods."""
    if start <= end:
        return start <= check_time <= end
    return start <= check_time or check_time <= end


def parse_time(time_str: str | None) -> time | None:
    """Parse time string to time object."""
    if not time_str:
        return None
    try:
        # Handle 24:00 as 00:00 (midnight of next day)
        if time_str.strip() == "24:00":
            return datetime.strptime("00:00", "%H:%M").time()
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError as err:
        _LOGGER.error("Error parsing time string '%s': %s", time_str, err)
        return None


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


def parse_time_periods(casy_string: str) -> list[tuple[time, time]]:
    """Parse time periods from casy string like '00:00-06:00; 07:00-09:00'."""
    periods: list[tuple[time, time]] = []
    if not casy_string:
        return periods

    # Split by semicolon and clean up whitespace
    time_ranges = [
        period.strip() for period in casy_string.split(";") if period.strip()
    ]

    for time_range in time_ranges:
        if "-" in time_range:
            start_str, end_str = time_range.split("-", 1)
            start_time = parse_time(start_str.strip())
            end_time = parse_time(end_str.strip())
            if start_time is not None and end_time is not None:
                periods.append((start_time, end_time))

    return periods


def get_today_schedule(
    json_data: dict, preferred_signal: str | None = None
) -> list[tuple[time, time]]:
    """Get today's schedule from API response."""
    if not json_data or "data" not in json_data or "signals" not in json_data["data"]:
        _LOGGER.error("Invalid API response structure")
        return []

    current_time = datetime.now(tz=CEZ_TIMEZONE)
    today_date = current_time.strftime("%d.%m.%Y")

    # Find all today's schedules
    today_signals = []
    for signal in json_data["data"]["signals"]:
        if signal.get("datum") == today_date:
            today_signals.append(signal)

    if not today_signals:
        _LOGGER.warning("No schedule found for today %s", today_date)
        return []

    # If preferred signal is specified, try to find it
    if preferred_signal:
        for signal in today_signals:
            if signal.get("signal") == preferred_signal:
                casy = signal.get("casy", "")
                signal_name = signal.get("signal", "unknown")
                _LOGGER.info(
                    "Found preferred signal %s for today %s: %s",
                    signal_name,
                    today_date,
                    casy,
                )
                return parse_time_periods(casy)
        _LOGGER.warning(
            "Preferred signal %s not found for today, using first available",
            preferred_signal,
        )

    # If no preferred signal or not found, pick the first one
    first_signal = today_signals[0]
    casy = first_signal.get("casy", "")
    signal_name = first_signal.get("signal", "unknown")
    _LOGGER.info("Using signal %s for today %s: %s", signal_name, today_date, casy)

    periods_today = parse_time_periods(casy)
    # Debug logování vypnuto

    # Pokud první interval dne začíná v 00:00, spoj s posledním intervalem předchozího dne, pokud navazují
    if periods_today and periods_today[0][0].strftime("%H:%M") == "00:00":
        # Debug logování vypnuto
        prev_date = (current_time - timedelta(days=1)).strftime("%d.%m.%Y")
        prev_signal = None
        for signal in json_data["data"]["signals"]:
            if signal.get("datum") == prev_date and signal.get("signal") == signal_name:
                prev_signal = signal
                break
        if prev_signal:
            prev_casy = prev_signal.get("casy", "")
            periods_prev = parse_time_periods(prev_casy)
            if periods_prev and periods_prev[-1][1].strftime("%H:%M") in [
                "00:00",
                "24:00",
            ]:
                # Debug logování vypnuto
                merged_period = (periods_prev[-1][0], periods_today[0][1])
                # Odstraň všechny dnešní intervaly začínající v 00:00 a končící stejně jako merged_period
                periods_today = [merged_period] + [
                    p
                    for p in periods_today[1:]
                    if not (
                        p[0].strftime("%H:%M") == "00:00" and p[1] == merged_period[1]
                    )
                ]
    # Stále platí i logika spojování přes půlnoc na konci dne
    if periods_today and periods_today[-1][1].strftime("%H:%M") == "00:00":
        # Debug logování vypnuto
        next_date = (current_time + timedelta(days=1)).strftime("%d.%m.%Y")
        next_signal = None
        for signal in json_data["data"]["signals"]:
            if signal.get("datum") == next_date and signal.get("signal") == signal_name:
                next_signal = signal
                break
        if next_signal:
            next_casy = next_signal.get("casy", "")
            periods_next = parse_time_periods(next_casy)
            # Pokud první interval zítřka začíná v 00:00, spoj je
            if periods_next and periods_next[0][0].strftime("%H:%M") == "00:00":
                # Debug logování vypnuto
                merged_period = (periods_today[-1][0], periods_next[0][1])
                # Odstraň všechny dnešní intervaly začínající v 00:00 a končící stejně jako merged_period
                periods_today = [
                    p
                    for p in periods_today[:-1]
                    if not (
                        p[0].strftime("%H:%M") == "00:00" and p[1] == merged_period[1]
                    )
                ]
                periods_today.append(merged_period)
                # Necháme pouze dnešní intervaly, zítřejší už nepřidáváme (patří do dalšího dne)
            else:
                # Pokud by vznikl interval 00:00-00:00, odstraň ho
                if periods_today[-1][0].strftime("%H:%M") == "00:00":
                    # Debug logování vypnuto
                    periods_today = periods_today[:-1]
    # Debug logování vypnuto
    return periods_today


def isHdo(
    json_data: dict,
    preferred_signal: str | None = None,
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
        json_data: JSON response from CEZ new API
        preferred_signal: Optional preferred signal name

    Returns:
        Tuple with HDO data: (low_tariff_active, low_start, low_end, low_duration,
                             high_tariff_active, high_start, high_end, high_duration,
                             next_low_start, next_low_end)
    """
    # Get today's schedule with preferred signal
    low_periods = get_today_schedule(json_data, preferred_signal)

    if not low_periods:
        _LOGGER.error("No schedule data available")
        return False, None, None, None, False, None, None, None, None, None

    current_time = datetime.now(tz=CEZ_TIMEZONE)
    checked_time = current_time.time()

    # Initialize return values
    low_tariff_active = False
    low_start = low_end = None
    low_duration = None
    high_tariff_active = False
    high_start = high_end = None
    high_duration = None
    next_low_start = next_low_end = None

    try:
        # Convert periods to the same format as before
        periods_list = []
        for i, (start_time, end_time) in enumerate(low_periods):
            periods_list.append({"start": start_time, "end": end_time, "index": i})

        # Najdi aktuální a následující NT interval
        current_low_period = None
        next_low_period = None
        for i, period in enumerate(periods_list):
            period_start = cast(time, period["start"])
            period_end = cast(time, period["end"])
            if time_in_range(period_start, period_end, checked_time):
                current_low_period = period
                # Další NT interval je ten následující v seznamu (pokud existuje)
                if i + 1 < len(periods_list):
                    next_low_period = periods_list[i + 1]
                else:
                    next_low_period = None
                break
        # Pokud jsme nenašli aktuální NT, najdi nejbližší následující NT interval
        if not current_low_period:
            for period in periods_list:
                period_start = cast(time, period["start"])
                if period_start > checked_time:
                    next_low_period = period
                    break
            # Pokud není žádný další NT dnes, použij první zítra
            if not next_low_period:
                # Zkus najít první NT zítra
                next_date = (current_time + timedelta(days=1)).strftime("%d.%m.%Y")
                next_signal = None
                for signal in json_data["data"]["signals"]:
                    if signal.get("datum") == next_date:
                        next_signal = signal
                        break
                if next_signal:
                    next_casy = next_signal.get("casy", "")
                    periods_next = parse_time_periods(next_casy)
                    if periods_next:
                        next_low_period = {"start": periods_next[0][0], "end": periods_next[0][1], "index": 0}

        if current_low_period:
            # Jsme v NT intervalu
            low_tariff_active = True
            low_start = cast(time, current_low_period["start"])
            low_end = cast(time, current_low_period["end"])
            low_duration = calculate_duration(checked_time, low_end)
            high_start = cast(time, current_low_period["end"])
            # Další NT interval
            if next_low_period:
                next_low_start = cast(time, next_low_period["start"])
                next_low_end = cast(time, next_low_period["end"])
            else:
                next_low_start = next_low_end = None
            # Najdi začátek dalšího VT (mezi NT intervaly)
            if next_low_period:
                high_end = cast(time, next_low_period["start"])
            else:
                high_end = None
            high_duration = timedelta(0)
        else:
            # Jsme ve VT intervalu
            high_tariff_active = True
            # Najdi předchozí NT interval
            prev_low = None
            for i, period in enumerate(periods_list):
                period_start = cast(time, period["start"])
                if period_start > checked_time:
                    if i > 0:
                        prev_low = periods_list[i - 1]
                    else:
                        prev_low = periods_list[-1] if periods_list else None
                    break
            if next_low_period:
                high_end = cast(time, next_low_period["start"])
                next_low_start = cast(time, next_low_period["start"])
                next_low_end = cast(time, next_low_period["end"])
            else:
                high_end = next_low_start = next_low_end = None
            if prev_low:
                high_start = cast(time, prev_low["end"])
            else:
                high_start = None
            high_duration = calculate_duration(checked_time, high_end) if high_end else None
            # low_start/low_end/low_duration nejsou relevantní, nastavíme None
            low_start = low_end = None
            low_duration = timedelta(0)
    except (KeyError, TypeError, ValueError) as err:
        _LOGGER.error("Error processing schedule data: %s", err)

    return (
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
    )
