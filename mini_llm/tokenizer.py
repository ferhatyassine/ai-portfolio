"""Character-level tokenizer: the simplest possible way to turn text into integers."""
import json


class CharTokenizer:
    def __init__(self, chars):
        self.itos = list(chars)
        self.stoi = {c: i for i, c in enumerate(self.itos)}

    @classmethod
    def from_text(cls, text):
        return cls(sorted(set(text)))

    @property
    def vocab_size(self):
        return len(self.itos)

    def encode(self, text):
        # Unknown characters are skipped so generation prompts never crash.
        return [self.stoi[c] for c in text if c in self.stoi]

    def decode(self, ids):
        return "".join(self.itos[i] for i in ids)

    def to_json(self):
        return json.dumps(self.itos)

    @classmethod
    def from_json(cls, s):
        return cls(json.loads(s))
