"""Sample text from a trained checkpoint.
Usage: python -m mini_llm.generate --prompt "Generative AI " --tokens 300"""
import argparse
from pathlib import Path

import torch

from .model import GPT, GPTConfig
from .tokenizer import CharTokenizer

ROOT = Path(__file__).resolve().parent.parent


def load(path):
    ck = torch.load(path, map_location="cpu", weights_only=True)
    model = GPT(GPTConfig(**ck["config"]))
    model.load_state_dict(ck["state"])
    model.eval()
    return model, CharTokenizer.from_json(ck["tokenizer"])


def complete(model, tok, prompt, tokens=300, temperature=0.8, top_k=20):
    ids = tok.encode(prompt) or [0]
    idx = torch.tensor([ids], dtype=torch.long)
    out = model.generate(idx, tokens, temperature=temperature, top_k=top_k)
    return tok.decode(out[0].tolist())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=str(ROOT / "mini_llm.pt"))
    ap.add_argument("--prompt", default="Generative AI ")
    ap.add_argument("--tokens", type=int, default=300)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    torch.manual_seed(a.seed)
    m, t = load(a.ckpt)
    print(complete(m, t, a.prompt, a.tokens, a.temperature))
