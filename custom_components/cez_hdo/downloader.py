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


def get_request_data(ean: str) -> dict:
    """Build request data for CEZ API."""
    return {"ean": ean}


def normalize_datum(datum_str: str | None) -> str | None:
    """Normalize various date formats to 'DD.MM.YYYY' used by CEZ HDO."""
    if not datum_str:
        return None
    s = str(datum_str).strip()

    # Common CEZ format, sometimes without leading zeros.
    parts = [p.strip() for p in s.split(".")]
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        day, month, year = parts
        if len(year) == 2:
            year = f"20{year}"
        try:
            return f"{int(day):02d}.{int(month):02d}.{int(year):04d}"
        except ValueError:
            pass

    # Fallback: try a few known formats.
    for fmt in ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%d.%m.%Y")
        except ValueError:
            continue

    return s


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

    # Podpora více úrovní vnoření (pro kompatibilitu s různými API odpověďmi)
    signals = None
    if not json_data or "data" not in json_data:
        _LOGGER.error("Invalid API response structure: missing 'data'")
        return []
    data_level = json_data["data"]
    # Pokud je další úroveň 'data', použij ji
    if isinstance(data_level, dict) and "data" in data_level:
        data_level = data_level["data"]
    if isinstance(data_level, dict) and "signals" in data_level:
        signals = data_level["signals"]
    if signals is None:
        _LOGGER.error("Invalid API response structure: missing 'signals'")
        return []

    current_time = datetime.now(tz=CEZ_TIMEZONE)
    today_date = current_time.strftime("%d.%m.%Y")

    # Find all today's schedules
    today_signals = []
    for signal in signals:
        if normalize_datum(signal.get("datum")) == today_date:
            today_signals.append(signal)

    if not today_signals:
        # Extra diagnostics: show which dates exist (normalized)
        available_dates = sorted(
            {normalize_datum(s.get("datum")) for s in signals if s.get("datum")},
        )
        _LOGGER.warning(
            "No schedule found for today %s (available: %s)",
            today_date,
            ", ".join([d for d in available_dates if d]),
        )
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

    return parse_time_periods(casy)


def _extract_signals(json_data: dict) -> list[dict]:
    """Extract signals list from API response.

    Supports both structures:
    - {"data": {"signals": [...]}}
    - {"data": {"data": {"signals": [...]}}}
    """
    if not json_data or "data" not in json_data:
        return []

    data_level = json_data.get("data")
    if isinstance(data_level, dict) and "data" in data_level:
        data_level = data_level.get("data")

    if isinstance(data_level, dict):
        signals = data_level.get("signals")
        if isinstance(signals, list):
            return signals
    return []


def get_schedule_for_date(
    json_data: dict,
    target_date: datetime,
    preferred_signal: str | None = None,
) -> list[tuple[time, time]]:
    """Get schedule for a specific date from API response."""
    signals = _extract_signals(json_data)
    if not signals:
        _LOGGER.error("Invalid API response structure: missing 'signals'")
        return []

    date_str = target_date.strftime("%d.%m.%Y")
    day_signals = [s for s in signals if normalize_datum(s.get("datum")) == date_str]

    if not day_signals:
        return []

    if preferred_signal:
        for signal in day_signals:
            if signal.get("signal") == preferred_signal:
                casy = signal.get("casy", "")
                return parse_time_periods(casy)

    # Fallback: first available signal for that day
    casy = day_signals[0].get("casy", "")
    return parse_time_periods(casy)


def isHdo(
    json_data: dict,
    preferred_signal: str | None = None,
    now: datetime | None = None,
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
                             high_tariff_active, high_start, high_end, high_duration)
    """
    current_time = now.astimezone(CEZ_TIMEZONE) if now is not None else datetime.now(tz=CEZ_TIMEZONE)

    # Initialize return values
    low_tariff_active = False
    low_start = low_end = None
    low_duration = None
    high_tariff_active = False
    high_start = high_end = None
    high_duration = None

    try:
        # Build low-tariff intervals as datetimes across yesterday/today/tomorrow.
        # This fixes edge cases like 17:00-24:00 + 00:00-06:00 (next day) which should be displayed as 17:00-06:00.
        days = [
            current_time.date() - timedelta(days=1),
            current_time.date(),
            current_time.date() + timedelta(days=1),
        ]

        low_intervals: list[tuple[datetime, datetime]] = []
        for day in days:
            day_dt = datetime.combine(day, time(0, 0), tzinfo=CEZ_TIMEZONE)
            periods = get_schedule_for_date(json_data, day_dt, preferred_signal)
            for start_t, end_t in periods:
                start_dt = datetime.combine(day, start_t, tzinfo=CEZ_TIMEZONE)
                end_dt = datetime.combine(day, end_t, tzinfo=CEZ_TIMEZONE)
                if end_dt <= start_dt:
                    end_dt += timedelta(days=1)
                low_intervals.append((start_dt, end_dt))

        if not low_intervals:
            import json as _json
            try:
                _LOGGER.error(
                    "No schedule data available for %s±1 day. Raw json_data: %s",
                    current_time.strftime("%d.%m.%Y"),
                    _json.dumps(json_data, ensure_ascii=False, indent=2),
                )
            except Exception as log_err:
                _LOGGER.error(
                    "No schedule data available. (Chyba při logování json_data: %s)",
                    log_err,
                )
            return False, None, None, None, False, None, None, None

        low_intervals.sort(key=lambda x: x[0])

        # Merge overlapping/adjacent intervals (adjacent is important for midnight joins).
        merged: list[tuple[datetime, datetime]] = []
        for start_dt, end_dt in low_intervals:
            if not merged:
                merged.append((start_dt, end_dt))
                continue
            last_start, last_end = merged[-1]
            if start_dt <= last_end:
                merged[-1] = (last_start, max(last_end, end_dt))
            else:
                merged.append((start_dt, end_dt))

        # Find current low interval, if any (end is treated as exclusive to avoid overlaps).
        current_low: tuple[datetime, datetime] | None = None
        for start_dt, end_dt in merged:
            if start_dt <= current_time < end_dt:
                current_low = (start_dt, end_dt)
                break

        if current_low is not None:
            low_tariff_active = True
            low_start_dt, low_end_dt = current_low
            low_start = low_start_dt.time()
            low_end = low_end_dt.time()
            low_duration = low_end_dt - current_time

            # Next high tariff window is the gap until next low interval.
            next_low = next((p for p in merged if p[0] >= low_end_dt), None)
            high_start = low_end
            high_end = next_low[0].time() if next_low is not None else None
            high_duration = timedelta(0)

            _LOGGER.debug(
                "✅ IN LOW TARIFF: %s-%s, remaining: %s",
                low_start,
                low_end,
                format_duration(low_duration),
            )
        else:
            high_tariff_active = True

            next_low = next((p for p in merged if p[0] > current_time), None)
            prev_low = None
            for start_dt, end_dt in merged:
                if end_dt <= current_time:
                    prev_low = (start_dt, end_dt)
                else:
                    break

            # Determine high interval boundaries.
            if prev_low is not None:
                high_start = prev_low[1].time()
            else:
                high_start = time(0, 0)

            if next_low is not None:
                high_end = next_low[0].time()
                high_duration = next_low[0] - current_time

                # Next low tariff info (for display)
                low_start = next_low[0].time()
                low_end = next_low[1].time()
                low_duration = timedelta(0)

                _LOGGER.debug(
                    "🔴 IN HIGH TARIFF: %s-%s, remaining: %s, next low: %s",
                    high_start,
                    high_end,
                    format_duration(high_duration),
                    low_start,
                )
            else:
                _LOGGER.error("Could not determine next low tariff period")

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
    )
