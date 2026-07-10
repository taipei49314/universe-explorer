"""arXiv search -> pending candidates (P1 spec section 1, item 4).

A discovery inlet, never an ingestion path. Results are stored *verbatim* under
candidates/ and stay pending forever: there is deliberately NO code path that
writes a candidate into claim data. A human who wants to cite one must edit the
data file themselves — and the moment they do, the provenance rule ("cite it =>
fetch it") takes over mechanically.

Usage:
    python -m universe_explorer.dataops.arxiv_search "black hole information paradox"
"""

from __future__ import annotations

import datetime as dt
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "https://export.arxiv.org/api/query"
_ATOM = "{http://www.w3.org/2005/Atom}"
CANDIDATES_DIR = Path(__file__).parent.parent.parent / "candidates"
MAX_RESULTS = 10


def search(query: str) -> Path:
    endpoint = f"{API}?{urllib.parse.urlencode({'search_query': f'all:{query}', 'max_results': MAX_RESULTS, 'sortBy': 'relevance'})}"
    print(f"search <- {endpoint}")
    with urllib.request.urlopen(endpoint, timeout=30) as resp:
        raw = resp.read()

    root = ET.fromstring(raw.decode("utf-8"))
    items = []
    for entry in root.findall(f"{_ATOM}entry"):
        raw_id = entry.findtext(f"{_ATOM}id", default="")
        arxiv_id = re.sub(r"v\d+$", "", raw_id.rsplit("/abs/", 1)[-1])
        items.append({
            # verbatim copies of the API response fields — never rewritten:
            "arxiv_id": arxiv_id,
            "title": entry.findtext(f"{_ATOM}title", default="").strip(),
            "published": entry.findtext(f"{_ATOM}published", default="").strip(),
            "authors": [a.findtext(f"{_ATOM}name", default="").strip()
                        for a in entry.findall(f"{_ATOM}author")],
            "summary": entry.findtext(f"{_ATOM}summary", default="").strip(),
            "status": "pending",  # forever, unless a human cites it in the data file
        })

    CANDIDATES_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")[:50]
    out = CANDIDATES_DIR / f"{stamp}-{slug}.json"
    out.write_text(json.dumps({
        "query": query,
        "endpoint": endpoint,
        "retrieved_at": stamp,
        "note": "pending candidates only — citing one requires a human edit to "
                "the data file, which then falls under the cite=>fetch rule",
        "results": items,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    for it in items:
        print(f"  [{it['arxiv_id']}] {it['title'][:72]}")
    print(f"\n{len(items)} candidates -> {out} (all pending)")
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit('usage: python -m universe_explorer.dataops.arxiv_search "<query>"')
    search(" ".join(sys.argv[1:]))
