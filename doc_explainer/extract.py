"""Rule-based extraction of the facts a person must not miss: dates, amounts, actions.
Works offline, in English and French. Every item keeps the exact source snippet."""
import re

MONTHS = ("january|february|march|april|may|june|july|august|september|october|november|december|"
          "janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre")
DATE_RES = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(rf"\b(?:{MONTHS})\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}\b", re.I),
    re.compile(rf"\b\d{{1,2}}(?:er)?\s+(?:{MONTHS})\s+\d{{4}}\b", re.I),
]
AMOUNT_RES = [
    re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?"),
    re.compile(r"\b\d[\d\s ]*(?:,\d{2})?\s?\$"),
]
ACTION_RE = re.compile(
    r"\b(must|shall|required to|need to|should|please|pay|submit|file|send|provide|respond|"
    r"doit|devez|dois|veuillez|payer|produire|soumettre|fournir|répondre|repondre|envoyer)\b", re.I)
DEADLINE_RE = re.compile(r"\b(by|before|no later than|due|deadline|within|avant le|d'ici|au plus tard|dans les|date limite)\b", re.I)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def find_dates(text):
    found = []
    for r in DATE_RES:
        found += [m.group(0) for m in r.finditer(text)]
    return list(dict.fromkeys(found))


def find_amounts(text):
    found = []
    for r in AMOUNT_RES:
        found += [m.group(0).strip() for m in r.finditer(text)]
    return list(dict.fromkeys(found))


def find_actions(text):
    """Sentences that ask the reader to do something; flagged urgent if they carry a deadline cue."""
    out = []
    for s in sentences(text):
        if ACTION_RE.search(s):
            out.append({"text": s, "has_deadline": bool(DEADLINE_RE.search(s) or find_dates(s))})
    return out
