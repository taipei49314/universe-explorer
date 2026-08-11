"""OpenAlex adapter — discovery courier (amendment-11).

Search uses the OpenAlex Works API. When a work has a DOI, the source_ref is
``doi:…`` so cite⇒fetch stays on Crossref (same court as the rest of the
ledger). Works without a DOI use ``openalex:W…`` and a local verbatim cache
under ``cache/openalex/``.

The adapter never assigns status lights or confidence.
Polite pool: User-Agent includes a contact mailto.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

from .base import EvidenceItem, FetchedRecord, RawResult, SourceAdapter

API = "https://api.openalex.org"
CONTACT = "taipei840428@gmail.com"
UA = f"UniverseExplorer/0.1 (mailto:{CONTACT}; +https://github.com/taipei49314/universe-explorer)"
RATE_LIMIT_S = 0.1

_CACHE_DIR = Path(__file__).parent.parent.parent.parent / "cache" / "openalex"
_MANIFEST_PATH = _CACHE_DIR / "manifest.json"

_W_ID_RE = re.compile(r"(?:openalex:)?(?:https?://openalex\.org/)?(W\d+)$", re.I)


def _request(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def _abstract_from_inverted(index: Optional[dict]) -> str:
    if not index:
        return ""
    # inverted index: token -> [positions]
    positions: Dict[int, str] = {}
    for token, locs in index.items():
        for loc in locs:
            positions[int(loc)] = token
    if not positions:
        return ""
    return " ".join(positions[i] for i in sorted(positions))


def _doi_from_work(work: dict) -> Optional[str]:
    raw = (work.get("doi") or "").strip()
    if not raw:
        return None
    # OpenAlex returns https://doi.org/10.xxxx/...
    if "doi.org/" in raw:
        raw = raw.split("doi.org/", 1)[-1]
    raw = raw.replace("https://", "").replace("http://", "")
    if raw.lower().startswith("doi:"):
        raw = raw[4:]
    raw = raw.strip().lower()
    return raw if raw.startswith("10.") else None


def _openalex_w_id(work: dict) -> str:
    oid = work.get("id") or ""
    m = re.search(r"(W\d+)", oid)
    return m.group(1) if m else oid.rsplit("/", 1)[-1]


def _authors(work: dict) -> List[str]:
    out = []
    for a in work.get("authorships") or []:
        name = (a.get("author") or {}).get("display_name") or ""
        if name:
            out.append(name)
    return out


class OpenAlexAdapter(SourceAdapter):
    """OpenAlex Works search + fetch. DOI paths prefer Crossref provenance."""

    @property
    def name(self) -> str:
        return "openalex"

    @property
    def source_ref_prefix(self) -> str:
        # Primary discovery refs may be doi: or openalex:
        return "openalex:"

    def can_handle(self, source_ref: str) -> bool:
        return source_ref.startswith("openalex:") or source_ref.startswith("doi:")

    def search(self, query: str, max_results: int = 10) -> List[RawResult]:
        params = {
            "search": query,
            "per_page": str(min(max(max_results, 1), 50)),
        }
        endpoint = f"{API}/works?{urllib.parse.urlencode(params)}"
        print(f"[openalex] search <- {endpoint}")
        raw = _request(endpoint)
        payload = json.loads(raw.decode("utf-8"))
        results: List[RawResult] = []
        for work in payload.get("results") or []:
            doi = _doi_from_work(work)
            w_id = _openalex_w_id(work)
            if doi:
                ref = f"doi:{doi}"
            else:
                ref = f"openalex:{w_id}"
            abstract = _abstract_from_inverted(work.get("abstract_inverted_index"))
            results.append(
                RawResult(
                    source_ref=ref,
                    title=(work.get("title") or work.get("display_name") or "").strip(),
                    published=(work.get("publication_date") or "")[:10],
                    authors=_authors(work),
                    summary=abstract[:2000],
                    extra={
                        "openalex_id": w_id,
                        "cited_by_count": str(work.get("cited_by_count") or 0),
                        "type": str(work.get("type") or ""),
                    },
                )
            )
        print(f"[openalex] {len(results)} results")
        return results

    def fetch(self, source_ref: str) -> FetchedRecord:
        # DOI: hand off to Crossref path so cite⇒fetch stays unified.
        if source_ref.startswith("doi:"):
            from .doi_adapter import DoiAdapter

            return DoiAdapter().fetch(source_ref)

        m = _W_ID_RE.match(source_ref.strip())
        if not m:
            raise FileNotFoundError(f"unrecognised OpenAlex ref: {source_ref!r}")
        w_id = m.group(1)
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        manifest = {}
        if _MANIFEST_PATH.exists():
            manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))

        if w_id not in manifest:
            endpoint = f"{API}/works/{w_id}"
            print(f"[openalex] fetch <- {endpoint}")
            time.sleep(RATE_LIMIT_S)
            raw = _request(endpoint)
            cache_file = f"{w_id}.json"
            path = _CACHE_DIR / cache_file
            path.write_bytes(raw)
            work = json.loads(raw.decode("utf-8"))
            manifest[w_id] = {
                "endpoint": endpoint,
                "retrieved_at": dt.datetime.now(dt.timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "cache_file": cache_file,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "title": (work.get("title") or work.get("display_name") or ""),
                "doi": _doi_from_work(work) or "",
            }
            _MANIFEST_PATH.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        rec = manifest[w_id]
        return FetchedRecord(
            source_ref=f"openalex:{w_id}",
            cache_path=str(_CACHE_DIR / rec["cache_file"]),
            sha256=rec["sha256"],
            endpoint=rec["endpoint"],
            retrieved_at=rec["retrieved_at"],
            title=rec.get("title", ""),
            authors=[],
            published="",
            raw_metadata={"doi": rec.get("doi", ""), "openalex_id": w_id},
        )

    def extract_evidence(self, record: FetchedRecord) -> List[EvidenceItem]:
        path = Path(record.cache_path)
        if not path.exists():
            # DOI path may have been filled via Crossref — use title only.
            if record.title:
                return [
                    EvidenceItem(
                        type="theoretical result",
                        description=record.title,
                        source_ref=_make_label(record.source_ref),
                    )
                ]
            return []

        # OpenAlex work JSON
        if path.suffix == ".json" and "openalex" in str(path).replace("\\", "/"):
            try:
                work = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return []
            title = (work.get("title") or work.get("display_name") or "").strip()
            abstract = _abstract_from_inverted(work.get("abstract_inverted_index"))
            text = f"{title}. {abstract}".strip() if abstract else title
            if not text:
                return []
            return [
                EvidenceItem(
                    type="theoretical result",
                    description=text[:4000],
                    source_ref=_make_label(record.source_ref),
                )
            ]

        # Crossref JSON (doi hand-off)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            msg = payload.get("message", payload)
            title = " ".join(msg.get("title") or [])
            abstract = msg.get("abstract") or ""
            # strip simple JATS tags if present
            abstract = re.sub(r"<[^>]+>", " ", abstract)
            text = f"{title}. {abstract}".strip() if abstract else title
            if not text:
                return []
            return [
                EvidenceItem(
                    type="theoretical result",
                    description=text[:4000],
                    source_ref=_make_label(record.source_ref),
                )
            ]
        except (json.JSONDecodeError, OSError):
            return []


def _make_label(source_ref: str) -> str:
    return (
        source_ref.replace(":", "-")
        .replace("/", "-")
        .replace(".", "-")
    )
