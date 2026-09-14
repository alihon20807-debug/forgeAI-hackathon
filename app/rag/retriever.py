"""In-memory Policy Document Retriever for ClaimGuard."""

from __future__ import annotations

import re
from typing import Any, Dict, List

from app.rag.corpus import POLICY_CORPUS, RAGChunk


class PolicyRetriever:
    """Fast lexical and keyword retriever over NH48 insurance corpus."""

    def __init__(self, chunks: List[RAGChunk] = POLICY_CORPUS) -> None:
        self.chunks = chunks

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b\w{2,}\b", text)]

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_tokens = set(self._tokenize(query))
        if not query_tokens:
            return []

        scored_chunks = []
        for chunk in self.chunks:
            chunk_tokens = set(self._tokenize(chunk.content + " " + chunk.title))
            keyword_set = {k.lower() for k in chunk.keywords}

            # Overlap score
            token_overlap = len(query_tokens.intersection(chunk_tokens))
            kw_overlap = len(query_tokens.intersection(keyword_set)) * 3

            score = token_overlap + kw_overlap
            if score > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, chunk in scored_chunks[:top_k]:
            results.append({
                "chunk_id": chunk.chunk_id,
                "section": chunk.section,
                "title": chunk.title,
                "content": chunk.content,
                "score": score,
            })
        return results


_GLOBAL_RETRIEVER = PolicyRetriever()


def get_retriever() -> PolicyRetriever:
    return _GLOBAL_RETRIEVER
