"""Fact guard: any number, date or amount in an explanation must exist in the source.
This is how we catch an AI changing '$1,250' into '$1,520' before the reader acts on it."""
import re
from .extract import find_dates, find_amounts

_NUM = re.compile(r"\d[\d,.\s ]*\d|\d")


def _norm(s):
    return re.sub(r"[\s ,$]", "", s).replace(".", "")


def check(explanation, source):
    """Return facts present in the explanation but NOT supported by the source."""
    src_nums = {_norm(m.group(0)) for m in _NUM.finditer(source)}
    src_dates = {d.lower() for d in find_dates(source)}
    bad = []
    for d in find_dates(explanation):
        if d.lower() not in src_dates:
            bad.append(d)
    for a in find_amounts(explanation):
        if _norm(a) not in src_nums:
            bad.append(a)
    return list(dict.fromkeys(bad))
