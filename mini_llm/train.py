"""Train the tiny GPT on data/corpus.txt.  Usage: python -m mini_llm.train --steps 1500"""
import argparse
import time
from pathlib import Path

import torch

from .model import GPT, GPTConfig
from .tokenizer import CharTokenizer

ROOT = Path(__file__).resolve().parent.parent


def get_batch(data, block_size, batch_size):
    ix = torch.randint(len(data) - block_size - 1, (batch_size,))
    x = torch.stack([data[i:i + block_size] for i in ix])
    y = torch.stack([data[i + 1:i + block_size + 1] for i in ix])  # shifted by one
    return x, y


@torch.no_grad()
def estimate_loss(model, data, block_size, batch_size, iters=20):
    model.eval()
    losses = [model(*get_batch(data, block_size, batch_size))[1].item() for _ in range(iters)]
    model.train()
    return sum(losses) / len(losses)


def train(corpus_path, out_path, steps=1500, batch_size=32, block_size=128, lr=3e-3,
          n_layer=4, n_head=4, n_embd=128, seed=1337, log_every=100):
    torch.manual_seed(seed)
    text = Path(corpus_path).read_text(encoding="utf-8")
    tok = CharTokenizer.from_text(text)
    data = torch.tensor(tok.encode(text), dtype=torch.long)
    split = int(0.9 * len(data))
    train_data, val_data = data[:split], data[split:]

    cfg = GPTConfig(tok.vocab_size, block_size, n_layer, n_head, n_embd)
    model = GPT(cfg)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"vocab={tok.vocab_size} chars={len(data)} params={n_params:,}")

    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.1)
    t0 = time.time()
    for step in range(1, steps + 1):
        x, y = get_batch(train_data, block_size, batch_size)
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        if step % log_every == 0 or step == steps:
            val = estimate_loss(model, val_data, block_size, batch_size)
            print(f"step {step:5d} | train {loss.item():.3f} | val {val:.3f} | {time.time() - t0:.0f}s")

    torch.save({"config": model.config_dict(), "state": model.state_dict(),
                "tokenizer": tok.to_json()}, out_path)
    print(f"saved -> {out_path}")
    return model, tok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(ROOT / "data" / "corpus.txt"))
    ap.add_argument("--out", default=str(ROOT / "mini_llm.pt"))
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--batch-size", type=int, default=32)
    a = ap.parse_args()
    train(a.corpus, a.out, steps=a.steps, batch_size=a.batch_size)
