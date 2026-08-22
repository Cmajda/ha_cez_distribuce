"""Constants for ČEZ HDO integration."""

from homeassistant.util import slugify

DOMAIN = "cez_hdo"

# Configuration keys
CONF_AUTO_REFRESH = "auto_refresh"

# Auto-refresh configuration
DEFAULT_AUTO_REFRESH = True
MAX_DAILY_OCR_ATTEMPTS = 24  # Maximum OCR attempts per day
AUTO_REFRESH_START_HOUR = 1  # Start auto-refresh attempts after 1:00
AUTO_REFRESH_END_HOUR = 23  # End auto-refresh attempts before 23:00
MIN_RETRY_DELAY_MINUTES = 10  # Minimum delay between failed refresh attempts


def mask_ean(ean: str) -> str:
    """Mask EAN for logging - show only first 2 and last 2 digits.

    Example: 859182400603967606 -> 85**************06
    """
    if not ean or len(ean) < 4:
        return ean or ""
    return f"{ean[:2]}{'*' * (len(ean) - 4)}{ean[-2:]}"


def ean_suffix(ean: str) -> str:
    """Get EAN suffix for file names and entity IDs.

    Returns last 6 digits of EAN.
    Example: 859182400603967606 -> 967606
    """
    if not ean or len(ean) < 6:
        return ean or ""
    return ean[-6:]


def ean_short(ean: str) -> str:
    """Get short EAN suffix for entity IDs.

    Returns last 4 digits of EAN.
    Example: 859182400603967606 -> 7606
    """
    if not ean or len(ean) < 4:
        return ean or ""
    return ean[-4:]


def sanitize_signal(signal: str) -> str:
    """Sanitize signal name for use in entity IDs.

    Replaces special characters with underscores and converts to lowercase.
    Example: 601D45H1810000000001|1 -> 601d45h1810000000001_1
    """
    if not signal:
        return ""
    # Replace special characters with underscore
    sanitized = signal.lower()
    for char in '|/\\:*?"<>':
        sanitized = sanitized.replace(char, "_")
    return sanitized


def sanitize_suffix(suffix: str | None) -> str:
    """Sanitize the user-defined entity suffix for use in entity IDs.

    The suffix comes straight from free-text user input in the config flow,
    so it may contain uppercase letters, spaces or diacritics - none of which
    are valid in an entity ID. Slugify is the same helper Home Assistant uses
    when it builds entity IDs itself, so the result is exactly what HA would
    have coerced the value to anyway.

    Example: CEZ -> cez, "Můj dům" -> muj_dum
    """
    if not suffix:
        return ""
    return slugify(suffix)
