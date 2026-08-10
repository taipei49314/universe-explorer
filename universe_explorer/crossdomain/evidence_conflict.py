"""Evidence conflict detector — same evidence, different interpretation.

When the same source_ref appears in claims from different domains with
different evidence types or wildly different status lights, that's a
structural tension worth surfacing. The detector records facts only —
no judgement about which interpretation is "right".

Usage:
    python -m universe_explorer.crossdomain.evidence_conflict
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from ..axes import derive, diverges
from ..model import Claim, Status, Topic
from ..provenance import arxiv_id_of, doi_of


@dataclass
class EvidenceConflict:
    """A factual tension: same source, different treatment across domains."""

    source_ref: str
    normalized_id: str
    claim_a: dict      # {id, domain, evidence_type, status, status_rank}
    claim_b: dict
    description: str

    def to_dict(self) -> dict:
        return {
            "source_ref": self.source_ref,
            "normalized_id": self.normalized_id,
            "claim_a": self.claim_a,
            "claim_b": self.claim_b,
            "description": self.description,
        }


def detect_conflicts(topics: List[Topic]) -> List[EvidenceConflict]:
    """Find evidence items that point to the same source across domains
    but carry different evidence types or sit under very different lights.

    Conflict conditions (mechanical, not opinionated):
      1. Same normalized source in different domains
      2. AND (different evidence types OR status rank gap >= 2)
    """
    # Build: normalized_id → list of (claim, topic, evidence_item)
    source_index = {}
    for topic in topics:
        for claim in topic.claims:
            for ev in claim.evidence:
                nid = _find_nid(ev.source_ref, claim)
                if nid is None:
                    continue
                if nid not in source_index:
                    source_index[nid] = []
                source_index[nid].append((claim, topic, ev))

    conflicts = []
    seen_pairs = set()

    for nid, entries in source_index.items():
        # Group by domain.
        by_domain = {}
        for claim, topic, ev in entries:
            by_domain.setdefault(topic.id, []).append((claim, topic, ev))

        if len(by_domain) < 2:
            continue

        # Compare across domains.
        domains = sorted(by_domain.keys())
        for i, da in enumerate(domains):
            for db in domains[i + 1:]:
                for claim_a, topic_a, ev_a in by_domain[da]:
                    for claim_b, topic_b, ev_b in by_domain[db]:
                        pair = tuple(sorted([claim_a.id, claim_b.id]))
                        if pair in seen_pairs:
                            continue
                        seen_pairs.add(pair)

                        # Check conflict conditions.
                        type_differs = ev_a.type != ev_b.type
                        rank_gap = abs(claim_a.status.rank - claim_b.status.rank)
                        status_differs = rank_gap >= 2

                        if type_differs or status_differs:
                            desc = _describe_conflict(
                                claim_a, claim_b, ev_a, ev_b,
                                type_differs, status_differs, rank_gap)
                            conflicts.append(EvidenceConflict(
                                source_ref=_find_original_ref(
                                    ev_a.source_ref, claim_a),
                                normalized_id=nid,
                                claim_a={
                                    "id": claim_a.id,
                                    "domain": da,
                                    "evidence_type": ev_a.type,
                                    "status": claim_a.status.name,
                                    "status_rank": claim_a.status.rank,
                                },
                                claim_b={
                                    "id": claim_b.id,
                                    "domain": db,
                                    "evidence_type": ev_b.type,
                                    "status": claim_b.status.name,
                                    "status_rank": claim_b.status.rank,
                                },
                                description=desc,
                            ))

    return conflicts


def _find_nid(source_ref: str, claim: Claim) -> str | None:
    """Resolve a source_ref label to a normalized id via the claim's sources."""
    for src in claim.sources:
        if src.label == source_ref:
            arxiv = arxiv_id_of(src.url_or_id)
            if arxiv:
                return f"arXiv:{arxiv}"
            doi = doi_of(src.url_or_id)
            if doi:
                return f"doi:{doi}"
            return None
    return None


def _find_original_ref(source_ref: str, claim: Claim) -> str:
    """Get the original url_or_id for a source_ref label."""
    for src in claim.sources:
        if src.label == source_ref:
            return src.url_or_id
    return source_ref


def _describe_conflict(
    claim_a: Claim, claim_b: Claim,
    ev_a, ev_b,
    type_differs: bool, status_differs: bool, rank_gap: int,
) -> str:
    """Build a human-readable description of the conflict."""
    parts = []
    if type_differs:
        parts.append(f"evidence type differs: {ev_a.type} vs {ev_b.type}")
    if status_differs:
        parts.append(f"status gap: {claim_a.status.value} (rank {claim_a.status.rank}) "
                     f"vs {claim_b.status.value} (rank {claim_b.status.rank}), "
                     f"gap={rank_gap}")
    return "; ".join(parts)


def format_conflicts_report(conflicts: List[EvidenceConflict]) -> str:
    """Human-readable report."""
    if not conflicts:
        return "No cross-domain evidence conflicts detected."
    lines = [f"Evidence conflicts: {len(conflicts)}"]
    for c in conflicts:
        lines.append(f"  [{c.normalized_id}]")
        lines.append(f"    {c.claim_a['id']} ({c.claim_a['domain']}) "
                     f"— {c.claim_a['evidence_type']}, {c.claim_a['status']}")
        lines.append(f"    {c.claim_b['id']} ({c.claim_b['domain']}) "
                     f"— {c.claim_b['evidence_type']}, {c.claim_b['status']}")
        lines.append(f"    → {c.description}")
    return "\n".join(lines)


if __name__ == "__main__":
    from ..data.registry import TOPICS
    conflicts = detect_conflicts(TOPICS)
    print(format_conflicts_report(conflicts))
