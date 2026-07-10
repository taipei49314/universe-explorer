"""arXiv fetcher — a courier, not a judge (P1 spec section 1).

It cannot decide whether a paper counts as evidence; it only moves bytes:
the official API response is stored *verbatim* (the sha256 in the manifest is
the proof no rewriting happened), together with where and when it was fetched.
There is no generation step anywhere in this pipeline.

Usage:
    python -m universe_explorer.dataops.arxiv_fetch          # fetch all cited ids
    python -m universe_explorer.dataops.arxiv_fetch 1207.3123 ...   # specific ids

Respects arXiv's courtesy rate limit (3 s between requests).
"""

from __future__ import annotations

import datetime as dt
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List

from ..provenance import (
    ARXIV_REF_RE,
    CACHE_DIR,
    MANIFEST_PATH,
    arxiv_id_of,
    sha256_of,
)

API = "https://export.arxiv.org/api/query"
_ATOM = "{http://www.w3.org/2005/Atom}"
RATE_LIMIT_S = 3.0


def cited_arxiv_ids() -> List[str]:
    """Every arXiv id cited anywhere in any registered topic."""
    from ..data.registry import TOPICS
    ids = []
    for topic in TOPICS:
        for claim in topic.claims:
            for src in claim.sources:
                a = arxiv_id_of(src.url_or_id)
                if a and a not in ids:
                    ids.append(a)
    return ids


def _safe_name(arxiv_id: str) -> str:
    return arxiv_id.replace("/", "_") + ".xml"


def _entry_meta(xml_text: str) -> Dict[str, str]:
    """Copy title/published/authors out of the response verbatim — for human
    eyeballing in the manifest, never rewritten."""
    root = ET.fromstring(xml_text)
    entry = root.find(f"{_ATOM}entry")
    if entry is None:
        return {}
    title = entry.findtext(f"{_ATOM}title", default="").strip()
    published = entry.findtext(f"{_ATOM}published", default="").strip()
    authors = [
        a.findtext(f"{_ATOM}name", default="").strip()
        for a in entry.findall(f"{_ATOM}author")
    ]
    return {"title": title, "published": published, "authors": authors}


def fetch_ids(ids: List[str]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for i, arxiv_id in enumerate(ids):
        if i:
            time.sleep(RATE_LIMIT_S)
        endpoint = f"{API}?{urllib.parse.urlencode({'id_list': arxiv_id, 'max_results': 1})}"
        print(f"fetch {arxiv_id} <- {endpoint}")
        with urllib.request.urlopen(endpoint, timeout=30) as resp:
            raw = resp.read()

        cache_file = CACHE_DIR / _safe_name(arxiv_id)
        cache_file.write_bytes(raw)  # verbatim, byte for byte

        meta = _entry_meta(raw.decode("utf-8"))
        if not meta.get("title"):
            print(f"  !! response for {arxiv_id} has no entry — NOT recording")
            cache_file.unlink()
            continue

        manifest[arxiv_id] = {
            "endpoint": endpoint,
            "retrieved_at": dt.datetime.now(dt.timezone.utc)
                              .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "cache_file": cache_file.name,
            "sha256": sha256_of(cache_file),
            # verbatim copies for human verification, never rewritten:
            "title": meta["title"],
            "published": meta["published"],
            "authors": meta["authors"],
        }
        print(f"  ok  {meta['title'][:70]}")

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nmanifest -> {MANIFEST_PATH} ({len(manifest)} records)")


if __name__ == "__main__":
    import sys
    ids = sys.argv[1:] or cited_arxiv_ids()
    fetch_ids(ids)
