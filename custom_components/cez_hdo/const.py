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
