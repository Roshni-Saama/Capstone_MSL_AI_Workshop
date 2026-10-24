"""Neutral display wording for CRM descriptions; source records are never edited."""
import re


def display_crm(value):
    """Return a presentation copy, preserving IDs, dates and underlying provenance."""
    if isinstance(value, dict):
        return {key: item if key in {"provenance", "source_reference"} or key.endswith("_id") else display_crm(item) for key, item in value.items()}
    if isinstance(value, list):
        return [display_crm(item) for item in value]
    if not isinstance(value, str):
        return value
    value = re.sub(r"\s*\((?:fictional|synthetic|demo)(?: (?:demo|history|setting|assignment))*\)", "", value, flags=re.I)
    value = re.sub(r"\b(?:fictional|synthetic|demo)\s+", "", value, flags=re.I)
    value = value.replace("this fixture", "this record").replace("the fixture", "the record")
    value = value.replace("for the demo", "").replace("Invented administrative closure in the record only", "Administrative closure recorded")
    return value.strip()
