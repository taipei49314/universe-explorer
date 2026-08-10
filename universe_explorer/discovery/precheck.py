"""Constitution precheck — run every gate on a candidate BEFORE human review.

The precheck is a dress rehearsal: the same validator, provenance, axes,
and proposals that run on real claims run here too. The human sees the
report and decides whether to accept, fix, or reject.

Precheck does NOT approve — it only reports. The human is the gate.

Usage:
    python -m universe_explorer.discovery.precheck candidates/structured/cosmology/new_claim.json
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from ..axes import EvidenceStrength, derive, diverges
from ..model import (
    STATUS_CONDITIONS,
    Claim,
    ConditionAssessment,
    Evidence,
    Source,
    Status,
    Topic,
)
from ..proposals import MACHINE_CONDITIONS, propose as _propose
from ..provenance import validate_provenance
from ..validator import Violation, validate_claim


@dataclass
class PrecheckReport:
    """The full constitution precheck result."""

    claim_id: str
    violations: List[Violation] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    evidence_axis: Optional[str] = None          # E1-E5
    evidence_axis_derivation: List[str] = field(default_factory=list)
    diverges: bool = False
    compatible_statuses: Set[str] = field(default_factory=set)
    excluded_statuses: Set[str] = field(default_factory=set)
    proposal_signals: List[dict] = field(default_factory=list)
    pass_constitution: bool = False

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "pass_constitution": self.pass_constitution,
            "violations": [
                {"rule": v.rule, "detail": v.detail, "law": v.rule}
                for v in self.violations
            ],
            "warnings": self.warnings,
            "evidence_axis": self.evidence_axis,
            "evidence_axis_derivation": self.evidence_axis_derivation,
            "diverges": self.diverges,
            "compatible_statuses": sorted(self.compatible_statuses),
            "excluded_statuses": sorted(self.excluded_statuses),
            "proposal_signals": self.proposal_signals,
        }


def precheck(candidate: dict) -> PrecheckReport:
    """Run the full constitution gate on a structured candidate.

    Steps:
      1. Convert candidate dict → model objects
      2. validate_claim() — constitution compliance
      3. derive() — evidence axis (mechanical)
      4. propose() — status proposal (exclude only)
      5. Build report

    Returns PrecheckReport with all findings.
    """
    claim_id = candidate.get("id", "unknown")
    report = PrecheckReport(claim_id=claim_id)

    # 1. Convert to model objects.
    claim = _dict_to_claim(candidate)
    if claim is None:
        report.violations.append(Violation(
            claim_id, "invalid_candidate",
            "Could not convert candidate to Claim — missing required fields"))
        return report

    # 2. Constitution check (same validator as real claims).
    report.violations = validate_claim(claim)
    report.pass_constitution = len(report.violations) == 0

    # 3. Evidence axis (mechanical derivation).
    try:
        derivation = derive(claim)
        report.evidence_axis = derivation.strength.short
        report.evidence_axis_derivation = derivation.reasoning
        report.diverges = diverges(claim)
    except Exception as exc:
        report.warnings.append(f"Evidence axis derivation failed: {exc}")

    # 4. Status proposal (exclude only, never approve).
    try:
        proposal = _propose(claim)
        report.compatible_statuses = {
            s.name for s in proposal.compatible_statuses
        }
        report.excluded_statuses = {
            s.name for s in proposal.excluded_statuses
        }
        for sa in proposal.assessments:
            for sig in sa.signals:
                report.proposal_signals.append({
                    "condition": sig.condition,
                    "kind": sig.kind,
                    "holds": sig.holds,
                    "rationale": sig.rationale,
                })
    except Exception as exc:
        report.warnings.append(f"Status proposal failed: {exc}")

    # 5. Extra warnings for common issues.
    if not candidate.get("title") or candidate["title"].startswith("[DRAFT]"):
        report.warnings.append("Title is a placeholder — human should provide "
                               "a real claim statement")
    if not candidate.get("open_questions"):
        report.warnings.append("No open questions listed — consider what the "
                               "evidence leaves unresolved")

    return report


def _dict_to_claim(candidate: dict) -> Optional[Claim]:
    """Convert a candidate JSON dict to a Claim object.
    Returns None if required fields are missing."""
    try:
        status_val = candidate.get("status")
        status = Status[status_val] if status_val else Status.FRONTIER

        sources = [
            Source(label=s["label"], url_or_id=s["url_or_id"], kind=s["kind"])
            for s in candidate.get("sources", [])
        ]
        evidence = [
            Evidence(type=e["type"], description=e["description"],
                     source_ref=e["source_ref"])
            for e in candidate.get("evidence", [])
        ]
        status_reason = [
            ConditionAssessment(
                condition=ca["condition"], holds=ca["holds"], note=ca["note"])
            for ca in candidate.get("status_reason", [])
        ]
        return Claim(
            id=candidate["id"],
            title=candidate.get("title", ""),
            status=status,
            status_reason=status_reason,
            evidence=evidence,
            open_questions=candidate.get("open_questions", []),
            sources=sources,
        )
    except (KeyError, TypeError):
        return None


def format_precheck_report(report: PrecheckReport) -> str:
    """Human-readable precheck report."""
    lines = [
        f"Precheck: {report.claim_id}",
        f"  Constitution: {'PASS' if report.pass_constitution else 'FAIL'}",
    ]
    if report.violations:
        lines.append(f"  Violations ({len(report.violations)}):")
        for v in report.violations:
            lines.append(f"    - {v}")
    if report.warnings:
        lines.append(f"  Warnings ({len(report.warnings)}):")
        for w in report.warnings:
            lines.append(f"    - {w}")
    if report.evidence_axis:
        lines.append(f"  Evidence axis: {report.evidence_axis}")
    if report.diverges:
        lines.append("  Divergence: YES — consensus and evidence axes point apart")
    if report.compatible_statuses:
        lines.append(f"  Compatible statuses: {sorted(report.compatible_statuses)}")
    if report.excluded_statuses:
        lines.append(f"  Excluded statuses: {sorted(report.excluded_statuses)}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit(
            "usage: python -m universe_explorer.discovery.precheck "
            "<candidate.json>")
    path = Path(sys.argv[1])
    if not path.exists():
        raise SystemExit(f"not found: {path}")
    candidate = json.loads(path.read_text(encoding="utf-8"))
    report = precheck(candidate)
    print(format_precheck_report(report))
