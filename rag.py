import json
import numpy as np
from sentence_transformers import SentenceTransformer


class StrategyStore:
    def __init__(self, path: str, model_name: str = "all-MiniLM-L6-v2"):
        with open(path, encoding="utf-8") as f:
            self.strategies = json.load(f)

        self.model = SentenceTransformer(model_name)
        texts = []
        for s in self.strategies:
            texts.append(self._to_text(s))
        self.embeddings = self.model.encode(texts, normalize_embeddings=True)

    @staticmethod
    def _to_text(s: dict) -> str:
        """Combine the fields that describe a strategy into one string to embed."""
        return f"{s['title']}. {s['when_to_use']} {s['how_it_works']}"

    def search_strategies(self, query: str, k: int = 3) -> list[dict]:
        """Return the k strategies most similar to the query."""
        query_vec = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.embeddings @ query_vec
        top = np.argsort(scores)[::-1][:k]
        return [{**self.strategies[i], "score": round(float(scores[i]), 3)} for i in top]