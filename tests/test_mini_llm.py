import torch

from mini_llm import GPT, GPTConfig, CharTokenizer


def test_tokenizer_roundtrip():
    tok = CharTokenizer.from_text("hello world")
    assert tok.decode(tok.encode("hello")) == "hello"
    assert CharTokenizer.from_json(tok.to_json()).itos == tok.itos


def _tiny():
    return GPT(GPTConfig(vocab_size=20, block_size=16, n_layer=2, n_head=2, n_embd=32, dropout=0.0))


def test_forward_shapes_and_loss():
    m = _tiny()
    x = torch.randint(0, 20, (3, 16))
    logits, loss = m(x, x)
    assert logits.shape == (3, 16, 20) and loss.item() > 0


def test_causality_future_tokens_do_not_change_past_logits():
    m = _tiny().eval()
    a = torch.randint(0, 20, (1, 10))
    b = a.clone(); b[0, -1] = (b[0, -1] + 1) % 20
    la, _ = m(a); lb, _ = m(b)
    assert torch.allclose(la[:, :-1], lb[:, :-1], atol=1e-5)


def test_generate_length():
    m = _tiny()
    out = m.generate(torch.zeros((1, 1), dtype=torch.long), 25)
    assert out.shape == (1, 26)


def test_can_overfit_tiny_batch():
    torch.manual_seed(0)
    m = _tiny()
    x = torch.randint(0, 20, (4, 16)); y = torch.roll(x, -1, dims=1)
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3)
    first = m(x, y)[1].item()
    for _ in range(60):
        opt.zero_grad(); m(x, y)[1].backward(); opt.step()
    assert m(x, y)[1].item() < first * 0.5
