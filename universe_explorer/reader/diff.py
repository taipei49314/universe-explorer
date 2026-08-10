"""Claim diff — compare claims and track changes over time.

Compares two claims field by field, highlighting:
  - Status changes
  - Evidence additions/removals
  - Source changes
  - Open question changes
  - Competing model changes

Usage:
    python -m universe_explorer.reader.diff <claim_id1> <claim_id2>
    python -m universe_explorer.reader.diff --snapshot <claim_id>
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from ..model import Claim, Topic

_SNAPSHOT_DIR = Path(__file__).parent.parent.parent / "snapshot" / "claims"


@dataclass
class ClaimDiff:
    """Difference between two claims."""

    claim_id: str
    changes: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "changes": self.changes,
            "has_changes": len(self.changes) > 0,
        }

    def format(self) -> str:
        """Human-readable diff."""
        if not self.changes:
            return f"No changes for {self.claim_id}."
        lines = [f"Changes for {self.claim_id}:"]
        for change in self.changes:
            lines.append(f"  {change['field']}: {change['description']}")
        return "\n".join(lines)


def diff_claims(claim_a: Claim, claim_b: Claim) -> ClaimDiff:
    """Compare two claims and return differences."""
    changes = []

    # Status change.
    if claim_a.status != claim_b.status:
        changes.append({
            "field": "status",
            "description": f"{claim_a.status.name} → {claim_b.status.name}",
            "old": claim_a.status.name,
            "new": claim_b.status.name,
        })

    # Title change.
    if claim_a.title != claim_b.title:
        changes.append({
            "field": "title",
            "description": f"Changed from '{claim_a.title[:50]}' to '{claim_b.title[:50]}'",
            "old": claim_a.title,
            "new": claim_b.title,
        })

    # Evidence changes.
    ev_a = {ev.source_ref: ev for ev in claim_a.evidence}
    ev_b = {ev.source_ref: ev for ev in claim_b.evidence}
    added_ev = set(ev_b.keys()) - set(ev_a.keys())
    removed_ev = set(ev_a.keys()) - set(ev_b.keys())
    for ref in sorted(added_ev):
        changes.append({
            "field": "evidence",
            "description": f"Added evidence from {ref}",
            "type": "added",
            "source_ref": ref,
        })
    for ref in sorted(removed_ev):
        changes.append({
            "field": "evidence",
            "description": f"Removed evidence from {ref}",
            "type": "removed",
            "source_ref": ref,
        })

    # Source changes.
    src_a = {s.label: s for s in claim_a.sources}
    src_b = {s.label: s for s in claim_b.sources}
    added_src = set(src_b.keys()) - set(src_a.keys())
    removed_src = set(src_a.keys()) - set(src_b.keys())
    for label in sorted(added_src):
        changes.append({
            "field": "sources",
            "description": f"Added source {label}",
            "type": "added",
            "label": label,
        })
    for label in sorted(removed_src):
        changes.append({
            "field": "sources",
            "description": f"Removed source {label}",
            "type": "removed",
            "label": label,
        })

    # Open questions changes.
    oq_a = set(claim_a.open_questions)
    oq_b = set(claim_b.open_questions)
    added_oq = oq_b - oq_a
    removed_oq = oq_a - oq_b
    for q in sorted(added_oq):
        changes.append({
            "field": "open_questions",
            "description": f"Added question: {q[:60]}",
            "type": "added",
        })
    for q in sorted(removed_oq):
        changes.append({
            "field": "open_questions",
            "description": f"Removed question: {q[:60]}",
            "type": "removed",
        })

    # Status reason changes.
    sr_a = {(ca.condition, ca.holds, ca.note) for ca in claim_a.status_reason}
    sr_b = {(ca.condition, ca.holds, ca.note) for ca in claim_b.status_reason}
    if sr_a != sr_b:
        changes.append({
            "field": "status_reason",
            "description": "Status reason conditions changed",
            "old_count": len(sr_a),
            "new_count": len(sr_b),
        })

    # Competing models changes.
    cm_a = {cm.name: cm for cm in claim_a.competing_models}
    cm_b = {cm.name: cm for cm in claim_b.competing_models}
    added_cm = set(cm_b.keys()) - set(cm_a.keys())
    removed_cm = set(cm_a.keys()) - set(cm_b.keys())
    for name in sorted(added_cm):
        changes.append({
            "field": "competing_models",
            "description": f"Added competing model: {name}",
            "type": "added",
        })
    for name in sorted(removed_cm):
        changes.append({
            "field": "competing_models",
            "description": f"Removed competing model: {name}",
            "type": "removed",
        })

    return ClaimDiff(claim_id=claim_a.id, changes=changes)


def save_snapshot(claim: Claim):
    """Save a claim snapshot for later comparison."""
    _SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "id": claim.id,
        "title": claim.title,
        "status": claim.status.name,
        "evidence_count": len(claim.evidence),
        "source_count": len(claim.sources),
        "open_question_count": len(claim.open_questions),
        "competing_model_count": len(claim.competing_models),
    }
    out_path = _SNAPSHOT_DIR / f"{claim.id}.json"
    out_path.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_snapshot(claim_id: str) -> Optional[dict]:
    """Load a claim snapshot."""
    path = _SNAPSHOT_DIR / f"{claim_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def format_diff_report(diff: ClaimDiff) -> str:
    """Human-readable diff report."""
    return diff.format()


if __name__ == "__main__":
    import sys
    from ..data.registry import TOPICS

    if "--snapshot" in sys.argv:
        # Save snapshots for all claims.
        idx = sys.argv.index("--snapshot")
        if idx + 1 < len(sys.argv):
            claim_id = sys.argv[idx + 1]
            for t in TOPICS:
                for c in t.claims:
                    if c.id == claim_id:
                        save_snapshot(c)
                        print(f"Saved snapshot for {claim_id}")
                        break
        else:
            for t in TOPICS:
                for c in t.claims:
                    save_snapshot(c)
            print(f"Saved snapshots for all claims")
    elif len(sys.argv) >= 3:
        # Compare two claims.
        id_a, id_b = sys.argv[1], sys.argv[2]
        claim_a = claim_b = None
        for t in TOPICS:
            for c in t.claims:
                if c.id == id_a:
                    claim_a = c
                if c.id == id_b:
                    claim_b = c
        if claim_a and claim_b:
            diff = diff_claims(claim_a, claim_b)
            print(format_diff_report(diff))
        else:
            print(f"Claim not found: {id_a if not claim_a else id_b}")
    else:
        print("usage:")
        print("  python -m universe_explorer.reader.diff <claim_id1> <claim_id2>")
        print("  python -m universe_explorer.reader.diff --snapshot [claim_id]")
        print("  python -m universe_explorer.reader.diff --tag <tag>")
        print("  python -m universe_explorer.reader.diff --label <label>")
