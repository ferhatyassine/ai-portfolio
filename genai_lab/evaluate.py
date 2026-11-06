"""Dependency-free metrics to compare a generated text against a human reference."""
import re
from collections import Counter

_STOP = set("a an the of to and or in on for with is are was be it this that as at by from".split())


def tokens(text):
    return re.findall(r"[a-zà-ÿ0-9']+", text.lower())


def rouge1_f(candidate, reference):
    """Unigram overlap F1 (a simplified ROUGE-1)."""
    c, r = Counter(tokens(candidate)), Counter(tokens(reference))
    overlap = sum((c & r).values())
    if not overlap:
        return 0.0
    p, rec = overlap / sum(c.values()), overlap / sum(r.values())
    return 2 * p * rec / (p + rec)


def key_term_coverage(candidate, reference):
    """Share of the reference's content words that the candidate also uses."""
    ref = {t for t in tokens(reference) if t not in _STOP and len(t) > 2}
    if not ref:
        return 0.0
    return len(ref & set(tokens(candidate))) / len(ref)


def compression(candidate, source):
    """Length ratio candidate/source; a summary should be well below 1."""
    s = len(tokens(source))
    return len(tokens(candidate)) / s if s else 0.0


def score(candidate, reference, source=None):
    out = {"rouge1_f": round(rouge1_f(candidate, reference), 3),
           "key_term_coverage": round(key_term_coverage(candidate, reference), 3)}
    if source:
        out["compression"] = round(compression(candidate, source), 3)
    return out


def compare(candidates, reference, source=None):
    """candidates: {name: text}. Returns list of (name, scores) best-first."""
    rows = [(n, score(t, reference, source)) for n, t in candidates.items()]
    return sorted(rows, key=lambda r: (r[1]["rouge1_f"], r[1]["key_term_coverage"]), reverse=True)
