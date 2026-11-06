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

## Tests

```bash
python -m pytest -q
```

## Notes on authorship

This project was generated with the help of Claude (Anthropic) and is meant as a learning base. Read the code, run it and be able to explain every part before presenting it.

## License

MIT
