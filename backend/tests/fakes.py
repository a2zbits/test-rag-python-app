import hashlib
from types import SimpleNamespace

import openai

DIM = 16


def fake_vector(text: str) -> list[float]:
    """Deterministic bag-of-words vector: texts sharing words are similar."""
    vec = [0.0] * DIM
    for word in text.lower().split():
        h = int(hashlib.md5(word.strip(".?,").encode()).hexdigest(), 16)
        vec[h % DIM] += 1.0
    return vec


class FakeEmbeddings:
    def __init__(self, fail: bool = False) -> None:
        self.calls: list[dict] = []
        self.fail = fail

    def create(self, model: str, input: list[str]):
        self.calls.append({"model": model, "input": input})
        if self.fail:
            raise openai.OpenAIError("boom")
        # return out of order to prove the service restores input order
        data = [SimpleNamespace(index=i, embedding=fake_vector(t)) for i, t in enumerate(input)]
        return SimpleNamespace(data=list(reversed(data)))


class FakeOpenAI:
    def __init__(self, fail: bool = False) -> None:
        self.embeddings = FakeEmbeddings(fail)
