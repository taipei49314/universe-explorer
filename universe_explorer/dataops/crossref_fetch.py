"""Crossref DOI fetcher — a courier, not a judge (Amendment #6 / C2).

Same posture as the arXiv courier: the official API response is stored
verbatim (sha256 in the manifest proves no rewriting), together with where and
when it was fetched. No key needed; the polite pool just wants a contact in
the User-Agent. One-second spacing between requests.

Usage:
    python -m universe_explorer.dataops.crossref_fetch          # all cited DOIs
    python -m universe_explorer.dataops.crossref_fetch 10.1038/... ...
"""

from __future__ import annotations

import datetime as dt
import json
import time
import urllib.request
from typing import List

from ..provenance import (
    CROSSREF_CACHE_DIR,
    CROSSREF_MANIFEST_PATH,
    doi_of,
    sha256_of,
)

API = "https://api.crossref.org/works/"
CONTACT = "taipei840428@gmail.com"
UA = f"UniverseExplorer/0.1 (mailto:{CONTACT})"
RATE_LIMIT_S = 1.0


def cited_dois() -> List[str]:
    """Every DOI cited anywhere in any registered topic."""
    from ..data.registry import TOPICS
    dois = []
    for topic in TOPICS:
        for claim in topic.claims:
            for src in claim.sources:
                d = doi_of(src.url_or_id)
                if d and d not in dois:
                    dois.append(d)
    return dois


def _safe_name(doi: str) -> str:
    return doi.replace("/", "_").replace(".", "-") + ".json"


def fetch_dois(dois: List[str]) -> int:
    CROSSREF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    if CROSSREF_MANIFEST_PATH.exists():
        manifest = json.loads(
            CROSSREF_MANIFEST_PATH.read_text(encoding="utf-8"))

    failures = 0
    for i, doi in enumerate(dois):
        if i:
            time.sleep(RATE_LIMIT_S)
        endpoint = API + urllib.request.quote(doi, safe="")
        print(f"fetch {doi} <- {endpoint}")
        req = urllib.request.Request(endpoint, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
        except Exception as exc:  # 404 = the DOI does not resolve: real signal
            print(f"  !! FAILED: {exc} — NOT recording (fix the data, not the rule)")
            failures += 1
            continue

        cache_file = CROSSREF_CACHE_DIR / _safe_name(doi)
        cache_file.write_bytes(raw)  # verbatim, byte for byte

        msg = json.loads(raw).get("message", {})
        title = (msg.get("title") or [""])[0]
        manifest[doi] = {
            "endpoint": endpoint,
            "retrieved_at": dt.datetime.now(dt.timezone.utc)
                              .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "cache_file": cache_file.name,
            "sha256": sha256_of(cache_file),
            # verbatim copies for human eyeballing, never rewritten:
            "title": title,
            "container": (msg.get("container-title") or [""])[0],
            "issued": msg.get("issued", {}).get("date-parts", [[None]])[0][0],
        }
        print(f"  ok  {title[:70]}")

    CROSSREF_MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nmanifest -> {CROSSREF_MANIFEST_PATH} ({len(manifest)} records, "
          f"{failures} failure(s))")
    return failures


if __name__ == "__main__":
    import sys
    dois = sys.argv[1:] or cited_dois()
    raise SystemExit(1 if fetch_dois(dois) else 0)
