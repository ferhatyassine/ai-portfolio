"""Summarizers: an offline extractive baseline and an optional Claude adapter.
Every text is passed through the PII guard first."""
import os
import re
from collections import Counter

from .evaluate import tokens, _STOP
from .pii import redact


def extractive_summary(text, n_sentences=2):
    """Pick the n sentences with the highest average word frequency (no model needed)."""
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    if len(sents) <= n_sentences:
        return " ".join(sents)
    freq = Counter(t for t in tokens(text) if t not in _STOP)

    def sc(s):
        ts = [t for t in tokens(s) if t not in _STOP]
        return sum(freq[t] for t in ts) / (len(ts) or 1)

    top = sorted(range(len(sents)), key=lambda i: sc(sents[i]), reverse=True)[:n_sentences]
    return " ".join(sents[i] for i in sorted(top))  # keep original order


def claude_summary(text, model="claude-opus-5-5", max_tokens=300):
    """Optional: needs `pip install anthropic` and ANTHROPIC_API_KEY in the environment.
    The key is never stored in code; PII is redacted before the call."""
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("Install the SDK first: pip install anthropic") from e
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable.")
    clean, _ = redact(text)
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model, max_tokens=max_tokens,
        messages=[{"role": "user", "content": f"Summarize in 2 sentences:\n\n{clean}"}],
    )
    return msg.content[0].text
