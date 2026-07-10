"""P2 — mechanical status proposals: propose, never decide.

Governance iron rules (P2 spec section 0):

  * A proposal is not a decision. This module never writes claim data; its only
    outputs are stdout and an append-only audit log.
  * Every entry condition is honestly classified: `machine` conditions are
    judged from the recorded evidence (each item source-verified by P1);
    `human` conditions (textbook acceptance, whether the field really has two
    camps, peer-review state) are answered "cannot judge — needs a human" and
    NEVER guessed.
  * Machine signals may EXCLUDE a status (a hard contradiction with recorded
    evidence) but can never approve one. Which light to give stays a human call.

If a future version swaps in an LLM proposer, this gate structure stays put —
only the proposer changes.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .axes import EvidenceStrength, derive
from .model import STATUS_CONDITIONS, Claim, Status

AUDIT_DIR = Path(__file__).parent.parent / "audit"
AUDIT_LOG = AUDIT_DIR / "decisions.jsonl"

# ---------------------------------------------------------------------------
# The machine/human split. A condition is `machine` only when the recorded
# evidence can genuinely answer it; everything else is human, full stop.
# ---------------------------------------------------------------------------

MACHINE_CONDITIONS = {
    # ESTABLISHED: replication is readable off the evidence axis.
    "multiple_independent_replications",
    # SPECULATIVE: both are readable off the recorded evidence types.
    "no_observational_evidence",
    "pure_theoretical_derivation",
    # FRONTIER: "observation still insufficient" ≈ no direct observation recorded.
    "insufficient_observation",
}

# Everything else in STATUS_CONDITIONS is human-only.


@dataclass
class ConditionSignal:
    condition: str
    kind: str                    # "machine" | "human"
    holds: Optional[bool]        # None => cannot judge (always None for human)
    rationale: str               # traceable: cites evidence records / rules


@dataclass
class StatusAssessment:
    status: Status
    compatible: bool             # False only on a hard machine contradiction
    signals: List[ConditionSignal]
    needs_human: List[str]


@dataclass
class Proposal:
    claim_id: str
    current_status: str
    evidence_axis: str
    assessments: List[StatusAssessment] = field(default_factory=list)

    @property
    def compatible_statuses(self) -> List[Status]:
        return [a.status for a in self.assessments if a.compatible]

    @property
    def excluded_statuses(self) -> List[Status]:
        return [a.status for a in self.assessments if not a.compatible]


def _judge_machine(condition: str, claim: Claim) -> ConditionSignal:
    d = derive(claim)
    grade = d.strength
    ev_summary = d.reasoning[0]  # "recorded evidence: N direct (...), ..."

    if condition == "multiple_independent_replications":
        holds = grade is EvidenceStrength.E1_MULTIPLE_DIRECT
        why = (f"evidence axis is {grade.short} ({grade.value}); {ev_summary}")
        return ConditionSignal(condition, "machine", holds, why)

    if condition == "no_observational_evidence":
        holds = grade in (EvidenceStrength.E4_THEORETICAL,
                          EvidenceStrength.E5_NONE)
        return ConditionSignal(condition, "machine", holds,
                               f"evidence axis {grade.short}; {ev_summary}")

    if condition == "pure_theoretical_derivation":
        holds = grade is EvidenceStrength.E4_THEORETICAL
        return ConditionSignal(condition, "machine", holds,
                               f"evidence axis {grade.short}; {ev_summary}")

    if condition == "insufficient_observation":
        holds = grade in (EvidenceStrength.E3_INDIRECT_ANALOG,
                          EvidenceStrength.E4_THEORETICAL,
                          EvidenceStrength.E5_NONE)
        return ConditionSignal(condition, "machine", holds,
                               f"no direct observation recorded "
                               f"({grade.short}); {ev_summary}")

    raise ValueError(f"no machine judge for {condition}")


def assess(claim: Claim, status: Status) -> StatusAssessment:
    spec = STATUS_CONDITIONS[status]
    signals: List[ConditionSignal] = []
    needs_human: List[str] = []

    for cond in spec["conditions"]:
        if cond in MACHINE_CONDITIONS:
            signals.append(_judge_machine(cond, claim))
        else:
            signals.append(ConditionSignal(
                cond, "human", None,
                "cannot judge mechanically — needs a human (never guessed)"))
            needs_human.append(cond)

    # Exclusion logic. Machine may exclude, never approve:
    #   mode "all": one machine condition judged False => status impossible.
    #   mode "any": every condition machine-judged and all False => impossible;
    #               if any human condition remains unjudged, stay compatible.
    machine = [s for s in signals if s.kind == "machine"]
    if spec["mode"] == "all":
        compatible = all(s.holds is not False for s in machine)
    else:
        if len(machine) == len(signals):
            compatible = any(s.holds for s in machine)
        else:
            compatible = True

    return StatusAssessment(status, compatible, signals, needs_human)


def propose(claim: Claim) -> Proposal:
    p = Proposal(
        claim_id=claim.id,
        current_status=claim.status.name,
        evidence_axis=derive(claim).strength.short,
    )
    for status in Status:
        p.assessments.append(assess(claim, status))
    return p


# ---------------------------------------------------------------------------
# Audit log: append-only record of human decisions over proposals.
# ---------------------------------------------------------------------------

def record_decision(
    proposal: Proposal,
    decision: str,          # "accept" | "reject"
    decided_by: str,
    note: str,
    audit_log: Path = AUDIT_LOG,
) -> dict:
    if decision not in ("accept", "reject"):
        raise ValueError("decision must be 'accept' or 'reject'")
    if not (decided_by and decided_by.strip()):
        raise ValueError("a decision must name its human decider")
    if not (note and note.strip()):
        raise ValueError("a decision must carry a reason (traceability)")

    entry = {
        "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claim": proposal.claim_id,
        "proposal_snapshot": {
            "current_status": proposal.current_status,
            "evidence_axis": proposal.evidence_axis,
            "compatible": [s.name for s in proposal.compatible_statuses],
            "excluded": [s.name for s in proposal.excluded_statuses],
        },
        "decision": decision,
        "decided_by": decided_by,
        "note": note,
    }
    audit_log.parent.mkdir(exist_ok=True)
    with audit_log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_proposal(p: Proposal) -> None:
    print(f"\n== {p.claim_id}  (current: {p.current_status}, "
          f"evidence axis: {p.evidence_axis})")
    ok = ", ".join(s.name for s in p.compatible_statuses)
    ex = ", ".join(s.name for s in p.excluded_statuses) or "(none)"
    print(f"   compatible : {ok}")
    print(f"   excluded   : {ex}")
    consistent = p.current_status in {s.name for s in p.compatible_statuses}
    print(f"   consistency: current human status is "
          f"{'INSIDE' if consistent else '** OUTSIDE **'} the compatible set")
    for a in p.assessments:
        if not a.compatible:
            for s in a.signals:
                if s.kind == "machine" and s.holds is False:
                    print(f"     - {a.status.name} excluded: {s.condition} "
                          f"fails ({s.rationale})")
    human_needed = sorted({c for a in p.assessments if a.compatible
                           for c in a.needs_human})
    print(f"   needs human: {', '.join(human_needed)}")


def main(argv: List[str]) -> int:
    from .data.black_hole import BLACK_HOLE

    if "--decide" in argv:
        i = argv.index("--decide")
        claim_id, decision, decided_by = argv[i + 1], argv[i + 2], argv[i + 3]
        note = " ".join(argv[i + 4:]) or ""
        claim = next(c for c in BLACK_HOLE.claims if c.id == claim_id)
        entry = record_decision(propose(claim), decision, decided_by, note)
        print(f"audit entry appended -> {AUDIT_LOG}")
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        return 0

    for claim in BLACK_HOLE.claims:
        _print_proposal(propose(claim))
    print("\nA proposal is not a decision: nothing above was written anywhere.")
    print("To record a human decision:  python -m universe_explorer.proposals "
          "--decide <claim_id> accept|reject <your-name> <reason...>")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
