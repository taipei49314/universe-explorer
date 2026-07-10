"""T1 — source health check: sources move too, and never silently.

A cited paper is not a fixed star: it can be corrected, receive an editorial
expression of concern, or be retracted. Crossref models every such act as a
NEW work whose `update-to` points at the original DOI — so the reverse query
`/works?filter=updates:<doi>` mechanically surfaces everything that has
happened to a source since we cited it.

This module ONLY reports (governance line in roadmap-v3: the health check
feeds humans, it never re-judges a claim):

  * findings are mechanical records — updating DOI, update type, date, title —
    zero interpretation;
  * NEW findings (vs health/acknowledged.json) are emitted as event files, so
    they flow through the existing digest + Atom feed pipeline to subscribers;
  * exit code 1 on new findings, so scheduled CI can open an issue for the
    humans who must re-judge.

Acknowledging a finding (after reviewing it and, if needed, updating the claim
and its status_history) means adding its updating-DOI to acknowledged.json —
an explicit, versioned human act, like every other confirmation here.

Usage:
    python -m universe_explorer.dataops.source_health          # check + report
    python -m universe_explorer.dataops.source_health --quiet  # exit code only
"""

from __future__ import annotations

import datetime as dt
import json
import time
import urllib.request
from pathlib import Path
from typing import Dict, List

import re
import xml.etree.ElementTree as ET

from ..provenance import CACHE_DIR, CROSSREF_MANIFEST_PATH, MANIFEST_PATH
from ..watch import emit_events

API = "https://api.crossref.org/works"
ARXIV_API = "https://export.arxiv.org/api/query"
CONTACT = "taipei840428@gmail.com"
UA = f"UniverseExplorer/0.1 (mailto:{CONTACT})"
RATE_LIMIT_S = 1.0

HEALTH_DIR = Path(__file__).parent.parent.parent / "health"
ACK_PATH = HEALTH_DIR / "acknowledged.json"

_ATOM = "{http://www.w3.org/2005/Atom}"
_VER_RE = re.compile(r"v(\d+)$")


def _entry_version(xml_text: str) -> int:
    """Version number from an arXiv Atom entry id (…/abs/1234.5678v3 -> 3)."""
    root = ET.fromstring(xml_text)
    entry = root.find(f"{_ATOM}entry")
    if entry is None:
        return 0
    m = _VER_RE.search((entry.findtext(f"{_ATOM}id") or "").strip())
    return int(m.group(1)) if m else 0


def arxiv_version_findings() -> List[dict]:
    """V4-3: cached arXiv papers get revised (v2, v3, ...) and that must not
    happen silently either. Compare the version cached at fetch time with the
    live API's latest — ONE batched request for every cached id. Mechanical
    records only: detecting that a version changed is the machine's job;
    whether the conclusions changed is a human's."""
    if not MANIFEST_PATH.exists():
        return []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    ids = sorted(manifest)
    if not ids:
        return []

    cached_versions = {}
    for a in ids:
        xml_path = CACHE_DIR / manifest[a]["cache_file"]
        cached_versions[a] = _entry_version(
            xml_path.read_text(encoding="utf-8"))

    url = (f"{ARXIV_API}?id_list="
           f"{','.join(urllib.request.quote(a, safe='') for a in ids)}"
           f"&max_results={len(ids)}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read().decode("utf-8"))

    current = {}
    for entry in root.findall(f"{_ATOM}entry"):
        raw_id = (entry.findtext(f"{_ATOM}id") or "").rsplit("/abs/", 1)[-1]
        m = _VER_RE.search(raw_id)
        bare = _VER_RE.sub("", raw_id)
        if m:
            current[bare] = int(m.group(1))

    findings = []
    for a in ids:
        cur = current.get(a, 0)
        if cur and cached_versions.get(a, 0) and cur > cached_versions[a]:
            findings.append({
                "source_doi": f"arXiv:{a}",
                # ack key, same mechanism as Crossref updates:
                "updating_doi": f"arXiv:{a}v{cur}",
                "update_types": ["new_arxiv_version"],
                "title": (f"cached v{cached_versions[a]} -> latest v{cur}"),
                "issued": [None],
            })
    return findings


def _updates_for(doi: str) -> List[dict]:
    """Reverse lookup: every Crossref work that declares itself an update
    (correction / erratum / retraction / concern...) to this DOI."""
    url = (f"{API}?filter=updates:{urllib.request.quote(doi, safe='')}"
           f"&rows=10&select=DOI,title,type,update-to,issued")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        items = json.loads(resp.read())["message"]["items"]

    findings = []
    for it in items:
        update_types = sorted({
            u.get("type", "unknown") for u in it.get("update-to", [])
            if u.get("DOI", "").lower() == doi.lower()
        }) or ["unknown"]
        findings.append({
            # mechanical record, zero interpretation:
            "source_doi": doi,
            "updating_doi": it.get("DOI", ""),
            "update_types": update_types,
            "title": (it.get("title") or [""])[0],
            "issued": (it.get("issued", {}).get("date-parts", [[None]])[0]),
        })
    return findings


def _load_acknowledged(ack_path: Path = ACK_PATH) -> set:
    if ack_path.exists():
        return set(json.loads(ack_path.read_text(encoding="utf-8")))
    return set()


def new_findings(findings: List[dict], acknowledged: set) -> List[dict]:
    """A finding is NEW until a human explicitly acknowledges its updating DOI
    (a versioned act in health/acknowledged.json, like every confirmation)."""
    return [f for f in findings
            if f["updating_doi"] and f["updating_doi"] not in acknowledged]


def check(quiet: bool = False) -> int:
    manifest = json.loads(CROSSREF_MANIFEST_PATH.read_text(encoding="utf-8"))
    acknowledged = _load_acknowledged()

    all_findings: List[dict] = []
    for i, doi in enumerate(sorted(manifest)):
        if i:
            time.sleep(RATE_LIMIT_S)
        found = _updates_for(doi)
        if not quiet:
            mark = f"{len(found)} update record(s)" if found else "clean"
            print(f"  {doi}: {mark}")
        all_findings.extend(found)

    # V4-3: arXiv revision watch (one batched request for every cached id)
    arxiv_found = arxiv_version_findings()
    if not quiet:
        n_arxiv = (len(json.loads(MANIFEST_PATH.read_text(encoding="utf-8")))
                   if MANIFEST_PATH.exists() else 0)
        print(f"  arXiv versions: {n_arxiv} cached id(s), "
              f"{len(arxiv_found)} revised")
        for f in arxiv_found:
            print(f"    {f['source_doi']}: {f['title']}")
    all_findings.extend(arxiv_found)

    HEALTH_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report = {
        "at": stamp,
        "note": ("mechanical Crossref reverse lookup (filter=updates:DOI); "
                 "the health check reports, humans re-judge"),
        "checked": len(manifest),
        "findings": all_findings,
    }
    (HEALTH_DIR / f"{stamp}-health.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    new = new_findings(all_findings, acknowledged)
    if new:
        events = [{
            "kind": "source_update_found",
            "claim": "(source-level)",
            "source_doi": f["source_doi"],
            "updating_doi": f["updating_doi"],
            "update_types": f["update_types"],
            "title": f["title"],
        } for f in new]
        out = emit_events(events)
        if not quiet:
            print(f"\n{len(new)} NEW finding(s) -> {out}")
            for f in new:
                print(f"  ! {f['source_doi']} has update "
                      f"[{', '.join(f['update_types'])}] "
                      f"-> {f['updating_doi']} : {f['title'][:60]}")
            print("\nhumans must re-judge the citing claims; acknowledge by "
                  f"adding the updating DOI to {ACK_PATH}")
        return 1

    if not quiet:
        print(f"\nall {len(manifest)} cited DOIs healthy "
              f"(or findings already acknowledged)")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(check(quiet="--quiet" in sys.argv))
