"""Full-text search index over claims.

Pure Python inverted index — no external dependencies.
Indexes: title, open_questions, evidence descriptions, status_reason notes.

Supports optional disk caching to avoid rebuilding the index every time.

Usage:
    python -m universe_explorer.reader.search_index "gravitational wave"
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from ..axes import derive, diverges
from ..model import Claim, Topic

_CACHE_DIR = Path(__file__).parent.parent.parent / "cache" / "search_index"


@dataclass
class SearchResult:
    """One search hit."""

    claim_id: str
    topic_id: str
    title: str
    score: float             # hit count (higher = more relevant)
    matched_fields: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "topic_id": self.topic_id,
            "title": self.title,
            "score": self.score,
            "matched_fields": self.matched_fields,
        }


class ClaimSearchIndex:
    """Inverted index over claim text fields."""

    def __init__(self, topics: List[Topic], use_cache: bool = True):
        self._index: Dict[str, Set[Tuple[str, str, str]]] = defaultdict(set)
        # token → {(claim_id, topic_id, field_name)}
        self._claims: Dict[str, Tuple[str, Claim]] = {}
        # claim_id → (topic_id, Claim)

        # Try to load from cache.
        if use_cache and self._try_load_cache(topics):
            return

        for topic in topics:
            for claim in topic.claims:
                self._claims[claim.id] = (topic.id, claim)
                self._index_claim(claim, topic.id)

        # Save to cache.
        if use_cache:
            self._save_cache(topics)

    def _index_claim(self, claim: Claim, topic_id: str):
        """Index all text fields of a claim."""
        fields = [
            ("title", claim.title),
        ]
        for i, oq in enumerate(claim.open_questions):
            fields.append((f"open_question_{i}", oq))
        for ev in claim.evidence:
            fields.append((f"evidence", ev.description))
        for ca in claim.status_reason:
            fields.append((f"status_reason", ca.note))
        for cm in claim.competing_models:
            fields.append((f"competing", f"{cm.name} {cm.supporting} {cm.opposing}"))

        for field_name, text in fields:
            for token in _tokenize(text):
                self._index[token].add((claim.id, topic_id, field_name))

    def search(self, query: str) -> List[SearchResult]:
        """Search claims by query. Returns results sorted by score (desc)."""
        tokens = _tokenize(query)
        if not tokens:
            return []

        # Count hits per claim.
        hits: Dict[str, Tuple[str, str, float, Set[str]]] = {}
        # claim_id → (topic_id, title, score, matched_fields)

        for token in tokens:
            # Prefix matching for partial words.
            matches = set()
            for indexed_token, entries in self._index.items():
                if indexed_token.startswith(token):
                    matches.update(entries)

            for claim_id, topic_id, field_name in matches:
                if claim_id not in hits:
                    claim = self._claims[claim_id][1]
                    hits[claim_id] = (topic_id, claim.title, 0, set())
                tid, title, score, fields = hits[claim_id]
                hits[claim_id] = (tid, title, score + 1, fields | {field_name})

        results = []
        for cid, (tid, title, score, fields) in hits.items():
            results.append(SearchResult(
                claim_id=cid,
                topic_id=tid,
                title=title,
                score=score,
                matched_fields=sorted(fields),
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results

    def suggest(self, prefix: str) -> List[str]:
        """Return matching tokens for auto-complete."""
        prefix = prefix.lower().strip()
        if not prefix:
            return []
        matches = [t for t in self._index if t.startswith(prefix)]
        matches.sort()
        return matches[:20]

    def _cache_key(self, topics: List[Topic]) -> str:
        """Compute a cache key based on claim count and ids."""
        ids = sorted(c.id for t in topics for c in t.claims)
        content = f"{len(ids)}:{','.join(ids)}"
        return hashlib.md5(content.encode()).hexdigest()

    def _try_load_cache(self, topics: List[Topic]) -> bool:
        """Try to load index from cache. Returns True if successful."""
        if not _CACHE_DIR.exists():
            return False

        key = self._cache_key(topics)
        cache_file = _CACHE_DIR / f"{key}.json"
        if not cache_file.exists():
            return False

        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
            # Rebuild claims map from topics.
            for topic in topics:
                for claim in topic.claims:
                    self._claims[claim.id] = (topic.id, claim)

            # Rebuild index from cached data.
            for token, entries in data.get("index", {}).items():
                for entry in entries:
                    self._index[token].add(tuple(entry))

            return True
        except Exception:
            return False

    def _save_cache(self, topics: List[Topic]):
        """Save index to cache."""
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        key = self._cache_key(topics)
        cache_file = _CACHE_DIR / f"{key}.json"

        # Convert sets to lists for JSON serialization.
        index_data = {}
        for token, entries in self._index.items():
            index_data[token] = [list(e) for e in entries]

        cache_file.write_text(
            json.dumps({"index": index_data}, ensure_ascii=False),
            encoding="utf-8",
        )


def _tokenize(text: str) -> List[str]:
    """Split text into tokens. Handles both ASCII and Unicode (e.g. Chinese)."""
    # Split on whitespace and ASCII punctuation, keep Unicode word chars together
    tokens = re.findall(r'[a-z0-9]+|[\u4e00-\u9fff\u3400-\u4dbf]+', text.lower())
    # ASCII tokens need length > 2; Chinese tokens are valid at any length
    return [t for t in tokens if len(t) > 2 or re.match(r'[\u4e00-\u9fff]', t)]


if __name__ == "__main__":
    import sys
    from ..data.registry import TOPICS

    if len(sys.argv) < 2:
        raise SystemExit('usage: python -m universe_explorer.reader.search_index "query"')

    index = ClaimSearchIndex(TOPICS)
    query = " ".join(sys.argv[1:])
    results = index.search(query)
    print(f"Search: {query!r} — {len(results)} result(s)")
    for r in results:
        print(f"  [{r.claim_id}] {r.title} (score={r.score}, "
              f"fields={r.matched_fields})")

