"""Full-text search index over claims.

Pure Python inverted index — no external dependencies.
Indexes: title, open_questions, evidence descriptions, status_reason notes,
claim ids, and Chinese presentation overlay (translations_zh).

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
# Bump when index fields / tokenization rules change so stale caches are ignored.
_INDEX_VERSION = "v3-zh-short-token"

# Map common Greek letters used in physics notation to ASCII so queries like
# "lcdm" match authored "ΛCDM" text (Python lowercases Λ → λ).
_GREEK_TO_ASCII = str.maketrans({
    "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e", "ζ": "z",
    "η": "e", "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m",
    "ν": "n", "ξ": "x", "π": "p", "ρ": "r", "σ": "s", "τ": "t",
    "υ": "u", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "w",
})

# Unicode subscripts/superscripts used in H₀, ¹⁰, etc. → ASCII digits/letters.
_SUB_SUPER = str.maketrans({
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "₀": "0",  # keep explicit
})


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
        """Index all text fields of a claim (EN + ZH overlay + id tokens)."""
        fields = [
            ("title", claim.title),
            ("claim_id", claim.id.replace("_", " ")),
        ]
        for i, oq in enumerate(claim.open_questions):
            fields.append((f"open_question_{i}", oq))
        for ev in claim.evidence:
            fields.append(("evidence", ev.description))
        for ca in claim.status_reason:
            fields.append(("status_reason", ca.note))
        for cm in claim.competing_models:
            fields.append((
                "competing",
                f"{cm.name} {cm.supporting} {cm.opposing}",
            ))

        # Chinese presentation overlay (view layer only; never mutates claims).
        for field_name, text in _zh_fields(claim.id):
            fields.append((field_name, text))

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
        prefix = _normalize_text(prefix).strip()
        if not prefix:
            return []
        matches = [t for t in self._index if t.startswith(prefix)]
        matches.sort()
        return matches[:20]

    def _cache_key(self, topics: List[Topic]) -> str:
        """Compute a cache key based on version + claim count and ids."""
        ids = sorted(c.id for t in topics for c in t.claims)
        content = f"{_INDEX_VERSION}:{len(ids)}:{','.join(ids)}"
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


def _zh_fields(claim_id: str) -> List[Tuple[str, str]]:
    """Collect Chinese overlay strings for a claim id (if present)."""
    try:
        from ..data.translations_zh import CLAIMS as ZH_CLAIMS
        from ..data.translations_zh import TOPIC_ZH
    except Exception:
        return []

    out: List[Tuple[str, str]] = []
    zh = ZH_CLAIMS.get(claim_id)
    if not isinstance(zh, dict):
        return out

    title = zh.get("title")
    if title:
        out.append(("title_zh", str(title)))

    for i, oq in enumerate(zh.get("open_questions") or []):
        out.append((f"open_question_zh_{i}", str(oq)))

    for i, ev in enumerate(zh.get("evidence") or []):
        out.append((f"evidence_zh_{i}", str(ev)))

    reasons = zh.get("reasons") or {}
    if isinstance(reasons, dict):
        for cond, note in reasons.items():
            out.append((f"status_reason_zh_{cond}", str(note)))

    for i, cm in enumerate(zh.get("competing") or []):
        if isinstance(cm, dict):
            blob = " ".join(
                str(cm.get(k, ""))
                for k in ("name", "for", "against", "limits")
            )
            out.append((f"competing_zh_{i}", blob))

    # Topic-level Chinese title helps "黑洞" → black_hole claims when query
    # is domain-ish; only attach if claim is under that topic key is unknown
    # here — skip topic title unless we can map. Callers index per claim only.
    _ = TOPIC_ZH  # keep import intentional for future domain-level search
    return out


def _normalize_text(text: str) -> str:
    """Lowercase + map Greek / subscripts to ASCII (ΛCDM → lcdm, H₀ → h0)."""
    if not text:
        return ""
    return text.lower().translate(_GREEK_TO_ASCII).translate(_SUB_SUPER)


def _keep_token(token: str) -> bool:
    """Whether a token is searchable.

    - Chinese: any length
    - ASCII with a digit (H0, E1, GW150914): length >= 2
    - Pure ASCII letters: length > 2 (drops 'of', 'to', 'is')
    """
    if not token:
        return False
    if re.search(r"[\u4e00-\u9fff\u3400-\u4dbf]", token):
        return True
    if re.search(r"\d", token):
        return len(token) >= 2
    return len(token) > 2


def _cjk_grams(run: str) -> List[str]:
    """CJK unigrams + bigrams (no external segmenter; pure stdlib).

    Whole-run Chinese tokens fail for queries like 「霍金」 against a long
    title that only *contains* those characters. Grams fix that.
    """
    chars = [c for c in run if "\u4e00" <= c <= "\u9fff" or "\u3400" <= c <= "\u4dbf"]
    if not chars:
        return []
    grams = list(chars)  # unigrams
    for i in range(len(chars) - 1):
        grams.append(chars[i] + chars[i + 1])
    return grams


def _tokenize(text: str) -> List[str]:
    """Split text into tokens. Handles ASCII, Greek→ASCII, and Chinese."""
    norm = _normalize_text(text)
    tokens: List[str] = []
    for m in re.finditer(
        r"[a-z0-9]+|[\u4e00-\u9fff\u3400-\u4dbf]+",
        norm,
    ):
        piece = m.group(0)
        if re.fullmatch(r"[a-z0-9]+", piece):
            if _keep_token(piece):
                tokens.append(piece)
        else:
            tokens.extend(_cjk_grams(piece))
    return tokens


if __name__ == "__main__":
    import sys
    from ..data.registry import TOPICS

    if len(sys.argv) < 2:
        raise SystemExit(
            'usage: python -m universe_explorer.reader.search_index "query"'
        )

    index = ClaimSearchIndex(TOPICS)
    query = " ".join(sys.argv[1:])
    results = index.search(query)
    print(f"Search: {query!r} — {len(results)} result(s)")
    for r in results:
        print(
            f"  [{r.claim_id}] {r.title} (score={r.score}, "
            f"fields={r.matched_fields})"
        )
