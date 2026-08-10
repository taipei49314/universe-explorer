"""Trust Loop ops inventory — challenges, weeklies, candidates.

Mechanical list counts only. No confidence / ranking.
Used by surface pages (health/changes) and trust_behavior measures.

v5 S2: TL-2 instrument panel + TL-3 weekly ritual data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
CHALLENGES_DIR = ROOT / "docs" / "challenges"
WEEKLIES_DIR = ROOT / "docs" / "weeklies"
CANDIDATES_DIR = ROOT / "candidates"
CANDIDATES_REJECTED = CANDIDATES_DIR / "rejected"

BANNED = frozenset({"confidence", "score", "probability", "certainty", "trust"})

_SKIP_NAMES = frozenset({"readme.md", "template.md", ".gitkeep"})


@dataclass(frozen=True)
class ChallengeRecord:
    file: str
    claim_id: str
    verdict: str  # reject | accept | unknown
    issue: str
    date: str

    def as_dict(self) -> dict:
        d = {
            "file": self.file,
            "claim_id": self.claim_id,
            "verdict": self.verdict,
            "issue": self.issue,
            "date": self.date,
        }
        assert not (set(d) & BANNED)
        return d


def _table_field(text: str, key: str) -> str:
    """Pull a value from a simple markdown table row ``| **Key** | value |``."""
    # bold key
    m = re.search(
        rf"\|\s*\*\*{re.escape(key)}\*\*\s*\|\s*(.+?)\s*\|",
        text,
        re.I,
    )
    if m:
        return m.group(1).strip()
    m = re.search(rf"\|\s*{re.escape(key)}\s*\|\s*(.+?)\s*\|", text, re.I)
    if m:
        return m.group(1).strip()
    return ""


def _verdict_token(raw: str) -> str:
    low = raw.lower()
    if "reject" in low:
        return "reject"
    if "accept" in low:
        return "accept"
    return "unknown"


def _claim_from_text(text: str, fallback_name: str) -> str:
    m = re.search(r"`([a-z0-9_]+)`", text)
    if m:
        return m.group(1)
    m = re.search(r"claim[:\s]+`?([a-z0-9_]+)`?", text, re.I)
    if m:
        return m.group(1)
    # filename often contains claim id
    stem = Path(fallback_name).stem
    parts = stem.split("-")
    for p in parts:
        if p in ("hawking",) or "_" in p:
            pass
    if "hawking" in stem:
        return "hawking_radiation"
    return stem


def list_challenge_records() -> List[ChallengeRecord]:
    if not CHALLENGES_DIR.is_dir():
        return []
    out: List[ChallengeRecord] = []
    for path in sorted(CHALLENGES_DIR.glob("*.md")):
        if path.name.lower() in _SKIP_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        claim = _table_field(text, "Claim").strip("`") or _claim_from_text(text, path.name)
        verdict_raw = _table_field(text, "Verdict")
        issue = _table_field(text, "Issue")
        date = _table_field(text, "Date")
        # issue may be a markdown link
        im = re.search(r"issues/(\d+)", issue) or re.search(r"issues/(\d+)", text)
        issue_ref = f"#{im.group(1)}" if im else (issue[:80] if issue else "")
        out.append(ChallengeRecord(
            file=path.name,
            claim_id=claim or "unknown",
            verdict=_verdict_token(verdict_raw or text[:500]),
            issue=issue_ref,
            date=date or path.stem[:10],
        ))
    return out


def list_weeklies() -> List[dict]:
    if not WEEKLIES_DIR.is_dir():
        return []
    rows = []
    for path in sorted(WEEKLIES_DIR.glob("*.md"), reverse=True):
        if path.name.lower() in _SKIP_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        silence = "legal silence" in text.lower() or "合法沉默" in text
        rows.append({
            "file": path.name,
            "bytes": path.stat().st_size,
            "legal_silence": silence,
            "mentions_challenge": "challenge" in text.lower() or "overturn" in text.lower(),
        })
    return rows


def candidate_counts() -> dict:
    pending = 0
    rejected = 0
    if CANDIDATES_DIR.is_dir():
        pending = sum(
            1 for p in CANDIDATES_DIR.glob("*.json")
            if p.is_file()
        )
    if CANDIDATES_REJECTED.is_dir():
        rejected = sum(1 for p in CANDIDATES_REJECTED.glob("*.json") if p.is_file())
    d = {
        "n_pending": pending,
        "n_rejected_archived": rejected,
        "note": (
            "candidates/ is discovery-only; nothing auto-writes claims. "
            "Weekly ritual: process ≤3 or record legal silence."
        ),
    }
    assert not (set(d) & BANNED)
    return d


def trust_loop_inventory() -> Dict[str, Any]:
    """Panel numbers for health.json — list counts only."""
    from .canonicals import as_payload as canonicals_payload

    records = list_challenge_records()
    weeklies = list_weeklies()
    cands = candidate_counts()
    n_reject = sum(1 for r in records if r.verdict == "reject")
    n_accept = sum(1 for r in records if r.verdict == "accept")
    can = canonicals_payload()
    inv = {
        "kind": "trust_loop_inventory",
        "n_challenge_records": len(records),
        "n_verdict_reject": n_reject,
        "n_verdict_accept": n_accept,
        "n_verdict_unknown": len(records) - n_reject - n_accept,
        "challenge_records": [r.as_dict() for r in records],
        "n_weeklies": len(weeklies),
        "latest_weekly": weeklies[0]["file"] if weeklies else None,
        "weeklies": weeklies[:8],
        "candidates": cands,
        "canonicals": can,
        "github_challenge_label": (
            "https://github.com/taipei49314/universe-explorer/issues"
            "?q=label%3Achallenge"
        ),
        "challenge_records_dir": "docs/challenges/",
        "weeklies_dir": "docs/weeklies/",
        "note": (
            "Pending open issues are on GitHub (label challenge) — "
            "not invented here. Legal silence weeks are recorded under "
            "docs/weeklies/. Three product canonicals are teaching anchors "
            "only. No banned-key fields exist."
        ),
    }
    assert not (set(inv) & BANNED)
    return inv
