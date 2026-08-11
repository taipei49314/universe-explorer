"""Editorial OS — the human gate next to the constitution court (amendment-11).

The ledger layer is orthogonal to consensus lights:

  * record_ok     — mechanical constitution (shape, floors, fetch when checked)
  * review_state  — human_verified | challenged | unverified
  * queue         — what an editor should open next

Usage:
    python -m universe_explorer.editorial
    python -m universe_explorer.editorial --json
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import List, Optional

from .axes import derive
from .model import Claim, ReviewState, Status, Topic
from .validator import validate_claim


@dataclass
class LedgerRow:
    """One claim as the editorial OS sees it."""

    claim_id: str
    topic_id: str
    title: str
    status: str
    evidence_axis: str
    review_state: str
    record_ok: bool
    violation_rules: List[str] = field(default_factory=list)
    verified_by: str = ""
    needs_human: bool = False
    reason: str = ""


def record_ok(claim: Claim, *, check_provenance: bool = False) -> bool:
    """True when the claim passes the shape court (optionally with fetch)."""
    return not validate_claim(claim, check_provenance=check_provenance)


def ledger_row(claim: Claim, topic_id: str = "") -> LedgerRow:
    """Build one editorial row."""
    violations = validate_claim(claim, check_provenance=False)
    rules = sorted({v.rule for v in violations})
    ok = not rules
    axis = derive(claim).strength.short if claim.evidence else "E5"
    rs = getattr(claim, "review_state", ReviewState.UNVERIFIED)
    if not isinstance(rs, ReviewState):
        rs = ReviewState.UNVERIFIED

    needs = False
    reason = ""
    # Amendment #12 / R4-8: Strong on analog-only is the cheap false-analog path.
    only_analog = bool(claim.evidence) and all(
        e.type == "analog experiment" for e in claim.evidence
    )
    if not ok:
        needs, reason = True, "constitution violations: " + ", ".join(rules)
    elif rs is ReviewState.CHALLENGED:
        needs, reason = True, "open challenge — human adjudication required"
    elif rs is ReviewState.UNVERIFIED and claim.status in (
        Status.ESTABLISHED,
        Status.STRONG,
    ):
        if claim.status is Status.STRONG and only_analog:
            needs, reason = True, (
                "strong × analog-only without human_verified "
                "(false-analog risk — R4-8)"
            )
        else:
            needs, reason = True, "high light without human_verified mark"
    elif rs is ReviewState.UNVERIFIED and claim.status is Status.COMPETING:
        needs, reason = True, "competing models — prefer human review"
    elif (
        rs is ReviewState.HUMAN_VERIFIED
        and claim.status is Status.STRONG
        and only_analog
    ):
        # Still list once in --all; queue only if we want re-check — skip queue.
        pass

    return LedgerRow(
        claim_id=claim.id,
        topic_id=topic_id,
        title=claim.title,
        status=claim.status.name,
        evidence_axis=axis,
        review_state=rs.value,
        record_ok=ok,
        violation_rules=rules,
        verified_by=getattr(claim, "verified_by", "") or "",
        needs_human=needs,
        reason=reason,
    )


def editorial_queue(topics: List[Topic]) -> List[LedgerRow]:
    """Claims an editor should look at first (needs_human only)."""
    rows = []
    for t in topics:
        for c in t.claims:
            row = ledger_row(c, t.id)
            if row.needs_human:
                rows.append(row)
    # Constitution failures first, then challenges, then unverified high lights.
    def sort_key(r: LedgerRow):
        if not r.record_ok:
            return (0, r.claim_id)
        if r.review_state == ReviewState.CHALLENGED.value:
            return (1, r.claim_id)
        return (2, r.claim_id)

    return sorted(rows, key=sort_key)


def format_queue(rows: List[LedgerRow]) -> str:
    if not rows:
        return "editorial queue: empty (nothing needs human right now)."
    lines = [f"editorial queue: {len(rows)} item(s)", ""]
    for r in rows:
        flag = "FAIL" if not r.record_ok else r.review_state
        lines.append(
            f"  [{flag}] {r.topic_id}/{r.claim_id}  "
            f"{r.status}/{r.evidence_axis}  — {r.reason}"
        )
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    from .data.registry import TOPICS

    p = argparse.ArgumentParser(description="Editorial OS queue (amendment-11)")
    p.add_argument("--json", action="store_true", help="machine-readable rows")
    p.add_argument(
        "--all",
        action="store_true",
        help="list every claim ledger row, not only needs_human",
    )
    args = p.parse_args(argv)

    if args.all:
        rows = [ledger_row(c, t.id) for t in TOPICS for c in t.claims]
    else:
        rows = editorial_queue(TOPICS)

    if args.json:
        print(json.dumps([asdict(r) for r in rows], indent=2, ensure_ascii=False))
    else:
        print(format_queue(rows))
        high = sum(
            1
            for t in TOPICS
            for c in t.claims
            if c.status in (Status.ESTABLISHED, Status.STRONG)
            and getattr(c, "review_state", ReviewState.UNVERIFIED)
            is ReviewState.UNVERIFIED
        )
        print()
        print(
            f"inventory: high-light claims still unverified = {high} "
            f"(expected under amendment-11 default; mark human_verified when reviewed)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
