"""Dynamic reading path generator — auto-generate paths from graph structure.

Extends the 7 authored reading paths with algorithmically generated ones:
  - Divergence paths: claims where consensus and evidence diverge
  - Cross-domain bridges: paths that traverse domain boundaries
  - Evidence chains: from strongest to weakest evidence
  - Frontier trails: from established to speculative

These supplement (never replace) the authored paths in relations.py.

Usage:
    python -m universe_explorer.reader.dynamic_paths
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set

from ..axes import derive, diverges, EvidenceStrength
from ..model import Claim, Status, Topic
from ..relations import all_links, ClaimLink


@dataclass
class DynamicPath:
    """A dynamically generated reading path."""

    id: str
    title: str
    description: str
    claim_ids: List[str]
    kind: str  # "divergence" | "cross_domain" | "evidence_chain" | "frontier_trail"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "claim_ids": self.claim_ids,
            "kind": self.kind,
        }


def generate_dynamic_paths(topics: List[Topic]) -> List[DynamicPath]:
    """Generate all dynamic reading paths."""
    paths = []
    paths.extend(_divergence_paths(topics))
    paths.extend(_cross_domain_paths(topics))
    paths.extend(_evidence_chain_paths(topics))
    paths.extend(_frontier_trail_paths(topics))
    return paths


def _divergence_paths(topics: List[Topic]) -> List[DynamicPath]:
    """Paths through claims where consensus and evidence diverge."""
    divergent = []
    for t in topics:
        for c in t.claims:
            if diverges(c):
                divergent.append(c)

    if len(divergent) < 2:
        return []

    # Sort by status rank (strongest consensus first).
    divergent.sort(key=lambda c: c.status.rank)
    return [DynamicPath(
        id="divergence_tour",
        title="Divergence Tour",
        description="Claims where consensus and evidence point apart — "
                    "the structural tensions in our knowledge.",
        claim_ids=[c.id for c in divergent],
        kind="divergence",
    )]


def _cross_domain_paths(topics: List[Topic]) -> List[DynamicPath]:
    """Paths that traverse domain boundaries via shared sources."""
    links = all_links(topics)
    claim_map: Dict[str, tuple] = {}
    for t in topics:
        for c in t.claims:
            claim_map[c.id] = (t.id, c)

    # Find cross-domain edges.
    cross_edges = []
    for link in links:
        if link.source in claim_map and link.target in claim_map:
            src_domain = claim_map[link.source][0]
            tgt_domain = claim_map[link.target][0]
            if src_domain != tgt_domain:
                cross_edges.append(link)

    if not cross_edges:
        return []

    # Build a path by following cross-domain edges.
    visited: Set[str] = set()
    path_claims = []
    for edge in cross_edges:
        if edge.source not in visited:
            path_claims.append(edge.source)
            visited.add(edge.source)
        if edge.target not in visited:
            path_claims.append(edge.target)
            visited.add(edge.target)

    if len(path_claims) < 2:
        return []

    return [DynamicPath(
        id="cross_domain_bridges",
        title="Cross-Domain Bridges",
        description="Claims connected across domain boundaries — "
                    "where different fields share evidence.",
        claim_ids=path_claims[:15],  # cap at 15 for readability
        kind="cross_domain",
    )]


def _evidence_chain_paths(topics: List[Topic]) -> List[DynamicPath]:
    """Paths from strongest to weakest evidence within each domain."""
    paths = []
    for topic in topics:
        claims_by_axis = {}
        for c in topic.claims:
            d = derive(c)
            claims_by_axis.setdefault(d.strength, []).append(c)

        # Build path: E1 → E2 → E3 → E4 → E5.
        chain = []
        for strength in EvidenceStrength:
            claims = claims_by_axis.get(strength, [])
            claims.sort(key=lambda c: c.status.rank)
            chain.extend(claims)

        if len(chain) >= 3:
            paths.append(DynamicPath(
                id=f"evidence_chain_{topic.id}",
                title=f"Evidence Chain: {topic.title}",
                description=f"From strongest to weakest evidence in {topic.title} — "
                            f"see how evidence strength varies within one domain.",
                claim_ids=[c.id for c in chain],
                kind="evidence_chain",
            ))
    return paths


def _frontier_trail_paths(topics: List[Topic]) -> List[DynamicPath]:
    """Paths from Established to Speculative within each domain."""
    paths = []
    for topic in topics:
        by_status = {}
        for c in topic.claims:
            by_status.setdefault(c.status, []).append(c)

        # Build path: Established → Strong → Competing → Frontier → Speculative.
        trail = []
        for status in Status:
            claims = by_status.get(status, [])
            claims.sort(key=lambda c: len(c.evidence), reverse=True)
            trail.extend(claims)

        if len(trail) >= 3:
            paths.append(DynamicPath(
                id=f"frontier_trail_{topic.id}",
                title=f"Frontier Trail: {topic.title}",
                description=f"From bedrock to ceiling in {topic.title} — "
                            f"see the full spectrum of scientific certainty.",
                claim_ids=[c.id for c in trail],
                kind="frontier_trail",
            ))
    return paths


def format_paths_report(paths: List[DynamicPath]) -> str:
    """Human-readable report."""
    if not paths:
        return "No dynamic paths generated."
    lines = [f"Dynamic reading paths: {len(paths)}"]
    for p in paths:
        lines.append(f"  [{p.kind}] {p.title} ({len(p.claim_ids)} claims)")
        lines.append(f"    {p.description}")
    return "\n".join(lines)


if __name__ == "__main__":
    from ..data.registry import TOPICS
    paths = generate_dynamic_paths(TOPICS)
    print(format_paths_report(paths))
