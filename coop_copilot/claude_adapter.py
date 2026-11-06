"""Optional Claude layer. Claude only REPHRASES a story that is already in your profile;
the grounding check then verifies it did not add skills or numbers you never mentioned.
Needs `pip install anthropic` and ANTHROPIC_API_KEY (never stored in code)."""
import os

from .grounding import check_claims

SYSTEM = (
    "You coach a co-op student for a job interview. Rewrite the STAR story below as a natural spoken "
    "answer in English, first person, about 90 seconds (150-200 words). "
    "STRICT RULES: use ONLY the facts given; never add tools, numbers, names, results or skills; "
    "if a part is missing, leave it out rather than inventing it. "
    "If a job description is given, you may choose which true details to emphasise, nothing more."
)


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("Install the SDK first: pip install anthropic") from e
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable.")
    return anthropic.Anthropic()


def polish(question, star_ans, profile, offer_text="", model="claude-opus-5-5", client=None):
    """Return {'text', 'grounded', 'flags'}. `client` can be injected for tests."""
    client = client or _client()
    star = "\n".join(f"{k}: {v}" for k, v in star_ans["star"].items() if v)
    user = f"Interview question: {question}\n\nMY TRUE STORY ({star_ans['experience']}):\n{star}"
    if offer_text:
        user += f"\n\nJob description (for emphasis only):\n{offer_text}"
    msg = client.messages.create(model=model, max_tokens=600, system=SYSTEM,
                                 messages=[{"role": "user", "content": user}])
    text = msg.content[0].text
    g = check_claims(text, profile)
    return {"text": text, "grounded": g["grounded"], "flags": g["flags"]}
