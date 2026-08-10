"""DOI adapter — wraps the existing crossref_fetch module.

Same posture as the arXiv adapter: delegates to proven code.
  - fetch → dataops.crossref_fetch.fetch_dois (Crossref API, verbatim cache)
  - extract_evidence → reads cached JSON, structures one EvidenceItem

No search method yet (Crossref search is deferred to NASA/ESA adapters).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .base import EvidenceItem, FetchedRecord, RawResult, SourceAdapter

_CROSSREF_CACHE = Path(__file__).parent.parent.parent.parent / "cache" / "crossref"
_CROSSREF_MANIFEST = _CROSSREF_CACHE / "manifest.json"

API = "https://api.crossref.org/works/"


class DoiAdapter(SourceAdapter):
    """DOI source adapter. Wraps existing dataops.crossref_fetch."""

    @property
    def name(self) -> str:
        return "doi"

    @property
    def source_ref_prefix(self) -> str:
        return "doi:"

    def search(self, query: str, max_results: int = 10) -> List[RawResult]:
        """DOI search is not yet implemented (deferred to NASA/ESA adapters).
        Returns empty list — use arXiv adapter for discovery."""
        print("[doi] search not implemented — use arxiv adapter for discovery")
        return []

    def fetch(self, source_ref: str) -> FetchedRecord:
        """Fetch one DOI through the existing pipeline."""
        from ...dataops.crossref_fetch import fetch_dois

        doi = source_ref.replace("doi:", "").strip().lower()

        manifest = self._load_manifest()
        if doi not in manifest:
            failures = fetch_dois([doi])
            if failures:
                raise FileNotFoundError(
                    f"doi:{doi} could not be fetched — Crossref returned error")
            manifest = self._load_manifest()

        rec = manifest.get(doi)
        if rec is None:
            raise FileNotFoundError(
                f"doi:{doi} could not be fetched — no cache entry")

        return FetchedRecord(
            source_ref=source_ref,
            cache_path=str(_CROSSREF_CACHE / rec["cache_file"]),
            sha256=rec["sha256"],
            endpoint=rec["endpoint"],
            retrieved_at=rec["retrieved_at"],
            title=rec.get("title", ""),
            published=str(rec.get("issued", "")),
            raw_metadata={
                "container": rec.get("container", ""),
            },
        )

    def extract_evidence(self, record: FetchedRecord) -> List[EvidenceItem]:
        """Read cached JSON, extract title as one EvidenceItem."""
        cache_path = Path(record.cache_path)
        if not cache_path.exists():
            return []

        data = json.loads(cache_path.read_text(encoding="utf-8"))
        msg = data.get("message", {})
        title = (msg.get("title") or [""])[0]
        if not title:
            return []

        return [EvidenceItem(
            type="theoretical result",  # human refines
            description=title,
            source_ref=record.source_ref,
        )]

    def _load_manifest(self) -> dict:
        if _CROSSREF_MANIFEST.exists():
            return json.loads(_CROSSREF_MANIFEST.read_text(encoding="utf-8"))
        return {}
