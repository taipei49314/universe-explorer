"""NASA ADS adapter — search astrophysics literature.

Wraps the NASA ADS (Astrophysics Data System) API.
Requires API key: export ADS_API_KEY="your_key"
Free tier: 5000 requests/day.

Search endpoint: https://api.adsabs.harvard.edu/v1/search/query
Returns bibcode, title, abstract, authors, pub year.

Usage:
    python -m universe_explorer.discovery.adapters.nasa_adapter "gravitational wave"
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List

from .base import EvidenceItem, FetchedRecord, RawResult, SourceAdapter

ADS_API = "https://api.adsabs.harvard.edu/v1"
ADS_CACHE = Path(__file__).parent.parent.parent.parent / "cache" / "nasa_ads"
ADS_MANIFEST = ADS_CACHE / "manifest.json"


class NasaAdapter(SourceAdapter):
    """NASA ADS source adapter."""

    @property
    def name(self) -> str:
        return "nasa"

    @property
    def source_ref_prefix(self) -> str:
        return "ADS:"

    def search(self, query: str, max_results: int = 10) -> List[RawResult]:
        """Search NASA ADS. Requires ADS_API_KEY env var."""
        api_key = os.environ.get("ADS_API_KEY", "")
        if not api_key:
            print("[nasa] ADS_API_KEY not set — skipping search")
            return []

        params = urllib.parse.urlencode({
            "q": query,
            "fl": "bibcode,title,abstract,author,pub_year,doctype",
            "rows": max_results,
            "sort": "relevance desc",
        })
        endpoint = f"{ADS_API}/search/query?{params}"
        print(f"[nasa] search <- {endpoint}")

        req = urllib.request.Request(
            endpoint,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            print(f"[nasa] search failed: {exc}")
            return []

        results = []
        for doc in data.get("response", {}).get("docs", []):
            bibcode = doc.get("bibcode", "")
            title = (doc.get("title") or [""])[0]
            abstract = doc.get("abstract", "")
            authors = doc.get("author", [])
            year = str(doc.get("pub_year", ""))
            results.append(RawResult(
                source_ref=f"ADS:{bibcode}",
                title=title,
                published=year,
                authors=authors[:10],  # ADS returns full author list
                summary=abstract,
                extra={"doctype": doc.get("doctype", ""), "bibcode": bibcode},
            ))
        print(f"[nasa] {len(results)} results")
        return results

    def fetch(self, source_ref: str) -> FetchedRecord:
        """Fetch a NASA ADS record by bibcode.
        Uses cached data if available."""
        bibcode = source_ref.replace("ADS:", "").strip()
        manifest = self._load_manifest()

        if bibcode not in manifest:
            # Fetch from API
            api_key = os.environ.get("ADS_API_KEY", "")
            if not api_key:
                raise FileNotFoundError(
                    f"ADS:{bibcode} not cached and ADS_API_KEY not set")

            endpoint = f"{ADS_API}/search/query?q=bibcode:{bibcode}&fl=bibcode,title,abstract,author,pub_year"
            req = urllib.request.Request(
                endpoint,
                headers={"Authorization": f"Bearer {api_key}"},
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception as exc:
                raise FileNotFoundError(f"ADS:{bibcode} fetch failed: {exc}")

            docs = data.get("response", {}).get("docs", [])
            if not docs:
                raise FileNotFoundError(f"ADS:{bibcode} not found")

            doc = docs[0]
            ADS_CACHE.mkdir(parents=True, exist_ok=True)
            cache_file = ADS_CACHE / f"{bibcode}.json"
            cache_file.write_text(
                json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")

            manifest[bibcode] = {
                "endpoint": endpoint,
                "cache_file": cache_file.name,
                "title": (doc.get("title") or [""])[0],
                "bibcode": bibcode,
            }
            ADS_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            ADS_MANIFEST.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False),
                encoding="utf-8")

        rec = manifest[bibcode]
        cache_path = ADS_CACHE / rec["cache_file"]

        return FetchedRecord(
            source_ref=source_ref,
            cache_path=str(cache_path),
            sha256="",  # ADS doesn't provide content hashing
            endpoint=rec.get("endpoint", ""),
            retrieved_at="",
            title=rec.get("title", ""),
            raw_metadata={"bibcode": bibcode},
        )

    def extract_evidence(self, record: FetchedRecord) -> List[EvidenceItem]:
        """Read cached JSON, extract title + abstract."""
        cache_path = Path(record.cache_path)
        if not cache_path.exists():
            return []

        data = json.loads(cache_path.read_text(encoding="utf-8"))
        title = (data.get("title") or [""])[0]
        abstract = data.get("abstract", "")
        if not abstract:
            return []

        description = f"{title}. {abstract}" if title else abstract
        return [EvidenceItem(
            type="theoretical result",  # human refines
            description=description[:2000],
            source_ref=record.source_ref,
        )]

    def _load_manifest(self) -> dict:
        if ADS_MANIFEST.exists():
            return json.loads(ADS_MANIFEST.read_text(encoding="utf-8"))
        return {}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit('usage: python -m universe_explorer.discovery.adapters.nasa_adapter "query"')
    adapter = NasaAdapter()
    results = adapter.search(" ".join(sys.argv[1:]))
    for r in results:
        print(f"  [{r.source_ref}] {r.title[:70]}")
