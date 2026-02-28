import re


def categorize_by_keywords(text: str) -> str:
    """Categorize a logistics inquiry based on keyword matching."""
    lower = text.lower()

    if any(kw in lower for kw in ["pakke", "sporing", "tracking", "track"]):
        return "pakke_sporing"
    if any(kw in lower for kw in ["klage", "misfornøyd", "problem"]):
        return "klage"
    if any(kw in lower for kw in ["adresse", "endre", "flytte"]):
        return "adresse_endring"
    return "generell_henvendelse"


def extract_tracking_number(text: str) -> str | None:
    """Extract a tracking number (NO\\d{17} or \\d{18}) from text."""
    match = re.search(r"NO\d{17}|\d{18}", text)
    return match.group() if match else None
