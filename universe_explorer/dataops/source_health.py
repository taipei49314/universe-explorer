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

from ..provenance import CROSSREF_MANIFEST_PATH
from ..watch import emit_events

API = "https://api.crossref.org/works"
CONTACT = "taipei840428@gmail.com"
UA = f"UniverseExplorer/0.1 (mailto:{CONTACT})"
RATE_LIMIT_S = 1.0

HEALTH_DIR = Path(__file__).parent.parent.parent / "health"
ACK_PATH = HEALTH_DIR / "acknowledged.json"


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
