# ai-portfolio — a mini LLM from scratch + a responsible Gen AI toolkit

Two small, readable projects built to learn how generative AI works and how to use it responsibly.

**FR :** Deux petits projets pédagogiques : (1) un mini-LLM de type GPT écrit de zéro avec PyTorch, (2) une boîte à outils d'IA générative responsable (protection des renseignements personnels, résumé, évaluation).

## 1. `mini_llm/` — a tiny GPT from scratch (PyTorch, CPU)

| File | What it does |
|---|---|
| `tokenizer.py` | Character-level tokenizer (text ⇄ integers) |
| `model.py` | Transformer: embeddings, causal multi-head self-attention, MLP blocks, sampling with temperature / top-k |
| `train.py` | Training loop (AdamW, one-cycle LR, gradient clipping, validation loss) |
| `generate.py` | Load a checkpoint and generate text |

```bash
pip install -r requirements.txt
python data/make_corpus.py          # builds a small original corpus
python -m mini_llm.train --steps 1200   # ~6 min on 2 CPU cores, ~0.8M parameters
python -m mini_llm.generate --prompt "Q: What is a token?" --tokens 200
```

Sample output after 1200 steps (final validation loss ≈ 0.13), prompt `A chatbot`:

```
A chatbot should never share two tools on the same task to kep the work fair and transparent.
```

Fluent in style, but it recombines phrases (and even misspells one) rather than reasoning.

**Honest limits:** the model is tiny and trained on ~40 KB of template-generated text, so it learns the *style and vocabulary* of the corpus and often produces fluent-looking but meaningless sentences. That is exactly the point: it shows next-token prediction, and why real systems need far more data, scale and human review.

## 2. `genai_lab/` — responsible Gen AI toolkit

- `pii.py` — redacts emails, phone numbers, SIN-format numbers, card numbers and Canadian postal codes **before** text reaches any model (pattern-based first line of defence, not a guarantee).
- `evaluate.py` — compares a generated summary with a human reference (ROUGE-1 F1, key-term coverage, compression).
- `summarize.py` — offline extractive baseline + optional Claude adapter (`pip install anthropic`, key read from `ANTHROPIC_API_KEY`, never stored in code).
- `cli.py` — command line.

```bash
python -m genai_lab.cli redact examples/note.txt
python -m genai_lab.cli summarize examples/article.txt
python -m genai_lab.cli compare examples/reference.txt examples/baseline.txt
```

Design follows the Government of Canada's FASTER principles: Fair, Accountable, Secure, Transparent, Educated, Relevant.

## 3. `doc_explainer/` — "Explain my document" (privacy-first assistant)

**Problem:** people receive tax notices, statements and contracts they do not understand, but should not paste private data into a chatbot.

**Pipeline:** mask personal data on your machine → explain in plain language (offline rules, or Claude on the *masked* text only) → **fact guard** → trust report.

- `extract.py` — finds dates, amounts and "what you must do" sentences (English + French), with deadline detection.
- `factguard.py` — every date or amount in an explanation must exist in the source; otherwise a warning is raised (catches an AI turning `$1,250` into `$1,520`).
- `explain.py` — offline explainer, optional Claude explainer, trust report (what was masked, what is certain, what is time-sensitive, what to verify).
- `cli.py`, `web.py` — command line and a local web page bound to `127.0.0.1`.

```bash
python -m doc_explainer.cli examples/notice.txt
python -m doc_explainer.web        # then open http://127.0.0.1:8000
```

**Limits:** masking is pattern-based and does **not** detect names or street addresses; the offline mode is rule-based and can miss unusual wording; the fact guard checks numbers and dates, not meaning. Not legal or tax advice.

## 4. `coop_copilot/` — Étudiant-Coop Copilot (honest interview and job-search assistant)

**Problem:** co-op students repeat the same tasks (match a CV to an offer, prepare STAR answers) and are tempted to embellish.

- `profile.py` — your profile is a JSON file of your **real** experiences (see `examples/profile.example.json`, a placeholder template: replace every field with your own).
- `match.py` — compares a job offer to your profile: covered skills with evidence, and honest gaps.
- `star.py` — builds a STAR answer from the best-fitting experience; if none fits it says so instead of inventing one.
- `grounding.py` — flags any skill or number in a draft that is not in your profile.
- `claude_adapter.py` — **optional Claude layer**: rewrites your true story as a ~90-second spoken answer, then the grounding check verifies Claude added nothing new. Local-first: without an API key everything runs offline.

```bash
python -m coop_copilot.cli match examples/offer.txt examples/profile.example.json
python -m coop_copilot.cli star "Tell me about a disagreement in your team" examples/profile.example.json
python -m coop_copilot.cli star "Tell me about a disagreement in your team" examples/profile.example.json --claude --offer examples/offer.txt
python -m coop_copilot.cli check my_draft.txt examples/profile.example.json
```

**Limits:** skill detection uses a small keyword lexicon; the Claude layer needs your API key and sends only the story and offer text you choose (use the PII guard from `genai_lab` on anything personal). The tool cannot make a weak experience strong: practise the answers aloud.

## Tests

```bash
python -m pytest -q
```

## Notes on authorship

This project was generated with the help of Claude (Anthropic) and is meant as a learning base. Read the code, run it and be able to explain every part before presenting it.

## License

MIT
