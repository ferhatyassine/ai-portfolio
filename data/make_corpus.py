"""Builds data/corpus.txt: a small, original, template-generated corpus about
responsible generative AI in a public-sector setting. Original text, no external data."""
import random
from pathlib import Path

random.seed(7)

subjects = ["A language model", "A generative AI tool", "A chatbot", "An analyst", "A project team",
            "A digital innovation team", "A reviewer", "A student developer"]
verbs = ["should check", "must protect", "can summarize", "needs to document", "has to test",
         "ought to explain", "can compare", "should never share"]
objects = ["the source of every answer", "personal information", "a long report in plain language",
           "each step of the process", "the output against a human reference",
           "how the result was produced", "two tools on the same task", "sensitive data with an outside service"]
endings = ["before anything is published.", "so that users can trust the result.",
           "because accuracy matters more than speed.", "and asks a person to review it.",
           "to keep the work fair and transparent.", "while staying secure and respectful.",
           "so that mistakes are found early.", "in every project, large or small."]

facts = [
    "A large language model predicts the next token from the tokens that came before it.",
    "Training adjusts millions of weights so that the predicted token matches the real one.",
    "Self-attention lets every token look at the earlier tokens and decide which ones matter.",
    "A small model trained on a small text can only repeat and remix what it has seen.",
    "Generative AI can draft, summarize and translate, but it can also be confidently wrong.",
    "Good prompts give context, a clear task, and the format of the answer.",
    "Evaluation means comparing the output with a trusted reference, not just reading it once.",
    "Personal and protected information must be removed before text leaves a secure environment.",
    "Responsible use is fair, accountable, secure, transparent, educated and relevant.",
    "A human stays accountable for any decision that affects a real person.",
    "Documentation lets the next developer understand why a tool was built the way it was.",
    "Testing a tool on a few simple cases finds many bugs before users do.",
]

qa = [
    ("What is a token?", "A token is a small piece of text, such as a word or a character, turned into a number."),
    ("What is training?", "Training is repeating predict, measure the error and adjust until the error is small."),
    ("What is a prompt?", "A prompt is the text we give a model so that it can continue it."),
    ("Why evaluate a summary?", "Because a fluent summary can still miss the key point or invent a detail."),
    ("Why remove personal data?", "Because private information must never be sent to a tool that is not approved."),
    ("What is a hallucination?", "It is an answer that sounds right but is not supported by any source."),
]

lines = []
for _ in range(220):
    lines.append(f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)} {random.choice(endings)}")
for _ in range(12):
    lines.extend(facts)
for _ in range(14):
    for q, a in qa:
        lines.append(f"Q: {q}\nA: {a}")
random.shuffle(lines)
out = Path(__file__).parent / "corpus.txt"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out, out.stat().st_size, "bytes")
