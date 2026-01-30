"""Constants for ČEZ HDO integration."""

DOMAIN = "cez_hdo"


def mask_ean(ean: str) -> str:
    """Mask EAN for logging - show only last 6 digits.

    Example: 859182400603967606 -> ***...967606
    """
    if not ean or len(ean) < 6:
        return ean or ""
    return f"***...{ean[-6:]}"


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
    for char in "|/\\:*?\"<>":
        sanitized = sanitized.replace(char, "_")
    return sanitized
