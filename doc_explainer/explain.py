"""Explainers. The offline one is deterministic; the Claude one is optional.
Both only ever see REDACTED text."""
import os

from genai_lab.pii import redact

from .extract import find_actions, find_amounts, find_dates, sentences

PROMPT = (
    "You help people understand official letters. Rewrite the document below in plain language "
    "(grade 6 reading level), in the same language as the document. Use this structure: "
    "1) What is this? 2) What do I have to do? 3) By when? 4) How much? "
    "Use ONLY facts present in the document; never invent dates, amounts or names. "
    "If something is unclear, say 'not stated in the document'. Tokens like [EMAIL] are hidden private data.\n\n"
)


def offline_explain(clean):
    actions = find_actions(clean)
    lines = ["What is this?", "  " + " ".join(sentences(clean)[:3]), "", "What do I have to do?"]
    lines += [f"  - {a['text']}" for a in actions] or ["  - not stated in the document"]
    lines += ["", "Key dates: " + (", ".join(find_dates(clean)) or "not stated in the document"),
              "Amounts: " + (", ".join(find_amounts(clean)) or "not stated in the document")]
    return "\n".join(lines)


def claude_explain(clean, model="claude-opus-5-5", max_tokens=700):
    """Needs `pip install anthropic` and ANTHROPIC_API_KEY. Only redacted text is sent."""
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("Install the SDK first: pip install anthropic") from e
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable.")
    msg = anthropic.Anthropic().messages.create(
        model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": PROMPT + clean}])
    return msg.content[0].text


def explain(text, use_claude=False):
    """Full pipeline: redact -> explain -> fact-guard -> trust report."""
    from .factguard import check
    clean, pii = redact(text)
    body = claude_explain(clean) if use_claude else offline_explain(clean)
    unsupported = check(body, clean)
    actions = find_actions(clean)
    return {
        "explanation": body,
        "mode": "claude" if use_claude else "offline",
        "privacy": {"redacted": pii, "sent_to_model": "redacted text only" if use_claude else "nothing (offline)"},
        "certain": {"dates": find_dates(clean), "amounts": find_amounts(clean),
                    "actions": [a["text"] for a in actions]},
        "urgent": [a["text"] for a in actions if a["has_deadline"]],
        "warnings": ([f"Not found in the source document, verify: {', '.join(unsupported)}"] if unsupported else []),
        "disclaimer": "Informational only. Confirm anything important with the official source or a professional.",
    }


def format_report(r):
    out = [r["explanation"], "", "--- TRUST REPORT ---",
           f"Mode: {r['mode']} | Privacy: {r['privacy']['sent_to_model']} | Redacted: {r['privacy']['redacted'] or 'nothing'}"]
    if r["urgent"]:
        out += ["TIME-SENSITIVE:"] + [f"  ! {u}" for u in r["urgent"]]
    out += [f"WARNING: {w}" for w in r["warnings"]] or ["Fact guard: every date and amount in the explanation exists in the source."]
    out.append(r["disclaimer"])
    return "\n".join(out)
