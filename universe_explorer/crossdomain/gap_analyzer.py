"""Evidence gap analyzer — find structural holes in domain coverage.

For each domain, analyzes:
  - Evidence type distribution (direct / indirect / analog / theoretical)
  - Light × evidence axis coverage matrix
  - Which light layers have fewer than 2 claims (sparse areas)

Records facts only — no interpretation of what "should" be there.

Usage:
    python -m universe_explorer.crossdomain.gap_analyzer
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set

from ..axes import EvidenceStrength, derive
from ..model import Status, Topic


@dataclass
class DomainGap:
    """Structural evidence gaps for one domain."""

    domain: str
    total_claims: int
    evidence_type_counts: Dict[str, int]       # type → count
    light_counts: Dict[str, int]               # Status.name → count
    axis_counts: Dict[str, int]                # E1-E5 → count
    missing_evidence_types: Set[str]           # types with 0 claims
    sparse_lights: List[str]                   # lights with < 2 claims
    coverage_matrix: Dict[str, Dict[str, int]] # light → axis → count

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "total_claims": self.total_claims,
            "evidence_type_counts": self.evidence_type_counts,
            "light_counts": self.light_counts,
            "axis_counts": self.axis_counts,
            "missing_evidence_types": sorted(self.missing_evidence_types),
            "sparse_lights": self.sparse_lights,
            "coverage_matrix": self.coverage_matrix,
        }


# The full controlled vocabulary (from axes.py).
_ALL_EVIDENCE_TYPES = {
    "direct observation",
    "indirect observation",
    "analog experiment",
    "theoretical derivation",
    "theoretical result",
}


def analyze_gaps(topics: List[Topic]) -> List[DomainGap]:
    """Analyze evidence structure for each domain."""
    gaps = []
    for topic in topics:
        gaps.append(_analyze_one(topic))
    return gaps


def _analyze_one(topic: Topic) -> DomainGap:
    """Analyze a single domain."""
    ev_type_counts: Dict[str, int] = {}
    light_counts: Dict[str, int] = {}
    axis_counts: Dict[str, int] = {}
    coverage: Dict[str, Dict[str, int]] = {}

    for claim in topic.claims:
        # Light distribution.
        light_name = claim.status.name
        light_counts[light_name] = light_counts.get(light_name, 0) + 1

        # Evidence type distribution (per evidence item).
        for ev in claim.evidence:
            ev_type_counts[ev.type] = ev_type_counts.get(ev.type, 0) + 1

        # Evidence axis distribution.
        try:
            d = derive(claim)
            axis = d.strength.short
            axis_counts[axis] = axis_counts.get(axis, 0) + 1

            # Coverage matrix: light × axis.
            if light_name not in coverage:
                coverage[light_name] = {}
            coverage[light_name][axis] = coverage[light_name].get(axis, 0) + 1
        except Exception:
            pass

    # Missing evidence types.
    present_types = set(ev_type_counts.keys())
    missing = _ALL_EVIDENCE_TYPES - present_types

    # Sparse lights (< 2 claims).
    sparse = [name for name, count in light_counts.items() if count < 2]

    return DomainGap(
        domain=topic.id,
        total_claims=len(topic.claims),
        evidence_type_counts=ev_type_counts,
        light_counts=light_counts,
        axis_counts=axis_counts,
        missing_evidence_types=missing,
        sparse_lights=sorted(sparse),
        coverage_matrix=coverage,
    )


def format_gaps_report(gaps: List[DomainGap]) -> str:
    """Human-readable report."""
    if not gaps:
        return "No domains to analyze."
    lines = ["Evidence gap analysis:"]
    for g in gaps:
        lines.append(f"\n  [{g.domain}] {g.total_claims} claims")
        lines.append(f"    Evidence types: {g.evidence_type_counts}")
        if g.missing_evidence_types:
            lines.append(f"    Missing types: {sorted(g.missing_evidence_types)}")
        lines.append(f"    Lights: {g.light_counts}")
        if g.sparse_lights:
            lines.append(f"    Sparse lights (< 2 claims): {g.sparse_lights}")
        lines.append(f"    Axis: {g.axis_counts}")
    return "\n".join(lines)


if __name__ == "__main__":
    from ..data.registry import TOPICS
    gaps = analyze_gaps(TOPICS)
    print(format_gaps_report(gaps))
