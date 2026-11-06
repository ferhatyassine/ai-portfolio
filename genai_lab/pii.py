"""PII guard: redact common personal identifiers BEFORE text goes to any LLM.
Pattern-based, so it is a first line of defence, not a guarantee."""
import re

PATTERNS = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")),
    ("SIN", re.compile(r"\b\d{3}[ -]\d{3}[ -]\d{3}\b")),  # Canadian Social Insurance Number format
    ("CARD", re.compile(r"\b(?:\d[ -]?){13,16}\b")),
    ("PHONE", re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")),
    ("POSTAL", re.compile(r"\b[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d\b")),  # Canadian postal code
]


def redact(text):
    """Return (clean_text, findings) where findings maps label -> count."""
    findings = {}
    for label, pat in PATTERNS:
        text, n = pat.subn(f"[{label}]", text)
        if n:
            findings[label] = n
    return text, findings


def has_pii(text):
    return bool(redact(text)[1])
