"""arXiv adapter — wraps the existing arxiv_search and arxiv_fetch modules.

Delegates to the proven pipeline:
  - search → dataops.arxiv_search.search (verbatim API results)
  - fetch  → dataops.arxiv_fetch.fetch_ids (cite ⇒ fetch, verbatim cache)
  - extract_evidence → reads cached XML, structures one EvidenceItem per entry

No new fetch logic; this adapter is a thin re-skin of existing code.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from .base import EvidenceItem, FetchedRecord, RawResult, SourceAdapter

_ATOM = "{http://www.w3.org/2005/Atom}"

# Re-use the same cache locations as the existing modules.
_CACHE_DIR = Path(__file__).parent.parent.parent.parent / "cache" / "arxiv"
_MANIFEST_PATH = _CACHE_DIR / "manifest.json"


class ArxivAdapter(SourceAdapter):
    """arXiv source adapter. Wraps existing dataops modules."""

    @property
    def name(self) -> str:
        return "arxiv"

    @property
    def source_ref_prefix(self) -> str:
        return "arXiv:"

    def search(self, query: str, max_results: int = 10) -> List[RawResult]:
        """Delegate to dataops.arxiv_search, re-parse into RawResult."""
        import urllib.parse
        import urllib.request

        api = "https://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "max_results": str(max_results),
            "sortBy": "relevance",
        }
        endpoint = f"{api}?{urllib.parse.urlencode(params)}"
        print(f"[arxiv] search <- {endpoint}")
        with urllib.request.urlopen(endpoint, timeout=30) as resp:
            raw = resp.read()

        root = ET.fromstring(raw.decode("utf-8"))
        results = []
        for entry in root.findall(f"{_ATOM}entry"):
            raw_id = entry.findtext(f"{_ATOM}id", default="")
            arxiv_id = re.sub(r"v\d+$", "", raw_id.rsplit("/abs/", 1)[-1])
            results.append(RawResult(
                source_ref=f"arXiv:{arxiv_id}",
                title=entry.findtext(f"{_ATOM}title", default="").strip(),
                published=entry.findtext(f"{_ATOM}published", default="").strip(),
                authors=[
                    a.findtext(f"{_ATOM}name", default="").strip()
                    for a in entry.findall(f"{_ATOM}author")
                ],
                summary=entry.findtext(f"{_ATOM}summary", default="").strip(),
            ))
        print(f"[arxiv] {len(results)} results")
        return results

    def fetch(self, source_ref: str) -> FetchedRecord:
        """Fetch one arXiv id through the existing pipeline.
        Uses dataops.arxiv_fetch for the actual HTTP + cache."""
        from ...dataops.arxiv_fetch import fetch_ids

        arxiv_id = source_ref.replace("arXiv:", "").strip()

        # Ensure fetched (cite ⇒ fetch).
        manifest = self._load_manifest()
        if arxiv_id not in manifest:
            fetch_ids([arxiv_id])
            manifest = self._load_manifest()

        rec = manifest.get(arxiv_id)
        if rec is None:
            raise FileNotFoundError(
                f"arXiv:{arxiv_id} could not be fetched — no cache entry")

        return FetchedRecord(
            source_ref=source_ref,
            cache_path=str(_CACHE_DIR / rec["cache_file"]),
            sha256=rec["sha256"],
            endpoint=rec["endpoint"],
            retrieved_at=rec["retrieved_at"],
            title=rec.get("title", ""),
            authors=rec.get("authors", []),
            published=rec.get("published", ""),
        )

    def extract_evidence(self, record: FetchedRecord) -> List[EvidenceItem]:
        """Read cached XML, extract title + abstract as one EvidenceItem."""
        xml_path = Path(record.cache_path)
        if not xml_path.exists():
            return []

        root = ET.fromstring(xml_path.read_text(encoding="utf-8"))
        entry = root.find(f"{_ATOM}entry")
        if entry is None:
            return []

        title = entry.findtext(f"{_ATOM}title", default="").strip()
        abstract = entry.findtext(f"{_ATOM}summary", default="").strip()
        if not abstract:
            return []

        # Evidence type is a judgement call the adapter does NOT make.
        # Default to "theoretical result"; the human or precheck will refine.
        description = f"{title}. {abstract}" if title else abstract
        return [EvidenceItem(
            type="theoretical result",
            description=description[:2000],  # reasonable bound
            source_ref=record.source_ref,
        )]

    def _load_manifest(self) -> dict:
        if _MANIFEST_PATH.exists():
            return json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
        return {}
