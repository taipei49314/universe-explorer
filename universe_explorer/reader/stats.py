"""Knowledge base statistics — structural insights for editors.

Generates a statistics report covering:
  - Coverage: claims per domain, per status, per evidence axis
  - Quality: divergent claims, open questions, competing models
  - Relations: edge density, cross-domain connections, isolated claims
  - Trends: evidence type distribution, source tier breakdown

Usage:
    python -m universe_explorer.reader.stats
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set

from ..axes import EvidenceStrength, derive, diverges
from ..model import Status, Topic
from ..relations import all_links

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


@dataclass
class KnowledgeStats:
    """Comprehensive statistics about the knowledge base."""

    # Counts
    total_topics: int = 0
    total_claims: int = 0
    total_evidence: int = 0
    total_sources: int = 0
    total_open_questions: int = 0

    # Distribution
    claims_by_domain: Dict[str, int] = field(default_factory=dict)
    claims_by_status: Dict[str, int] = field(default_factory=dict)
    claims_by_axis: Dict[str, int] = field(default_factory=dict)
    evidence_by_type: Dict[str, int] = field(default_factory=dict)
    sources_by_tier: Dict[str, int] = field(default_factory=dict)

    # Quality
    divergent_count: int = 0
    divergent_ids: List[str] = field(default_factory=list)
    competing_count: int = 0
    isolated_count: int = 0
    isolated_ids: List[str] = field(default_factory=list)

    # Relations
    total_edges: int = 0
    authored_edges: int = 0
    mechanical_edges: int = 0
    cross_domain_edges: int = 0
    avg_edges_per_claim: float = 0.0

    # Coverage gaps
    sparse_domains: List[str] = field(default_factory=list)
    empty_status_layers: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "counts": {
                "topics": self.total_topics,
                "claims": self.total_claims,
                "evidence": self.total_evidence,
                "sources": self.total_sources,
                "open_questions": self.total_open_questions,
            },
            "distribution": {
                "by_domain": self.claims_by_domain,
                "by_status": self.claims_by_status,
                "by_axis": self.claims_by_axis,
                "evidence_types": self.evidence_by_type,
                "source_tiers": self.sources_by_tier,
            },
            "quality": {
                "divergent": self.divergent_count,
                "divergent_ids": self.divergent_ids,
                "competing": self.competing_count,
                "isolated": self.isolated_count,
                "isolated_ids": self.isolated_ids,
            },
            "relations": {
                "total_edges": self.total_edges,
                "authored": self.authored_edges,
                "mechanical": self.mechanical_edges,
                "cross_domain": self.cross_domain_edges,
                "avg_per_claim": round(self.avg_edges_per_claim, 2),
            },
            "gaps": {
                "sparse_domains": self.sparse_domains,
                "empty_status_layers": self.empty_status_layers,
            },
        }


def compute_stats(topics: List[Topic]) -> KnowledgeStats:
    """Compute comprehensive statistics."""
    stats = KnowledgeStats()
    stats.total_topics = len(topics)

    # Track which claims have edges.
    claims_with_edges: Set[str] = set()
    domain_status_coverage: Dict[str, Set[str]] = defaultdict(set)

    for topic in topics:
        stats.claims_by_domain[topic.id] = len(topic.claims)

        for claim in topic.claims:
            stats.total_claims += 1
            stats.total_evidence += len(claim.evidence)
            stats.total_sources += len(claim.sources)
            stats.total_open_questions += len(claim.open_questions)

            # Status distribution.
            status_name = claim.status.name
            stats.claims_by_status[status_name] = \
                stats.claims_by_status.get(status_name, 0) + 1
            domain_status_coverage[topic.id].add(status_name)

            # Evidence axis.
            try:
                d = derive(claim)
                axis = d.strength.short
                stats.claims_by_axis[axis] = \
                    stats.claims_by_axis.get(axis, 0) + 1
            except Exception:
                pass

            # Evidence types.
            for ev in claim.evidence:
                stats.evidence_by_type[ev.type] = \
                    stats.evidence_by_type.get(ev.type, 0) + 1

            # Source tiers.
            from ..model import tier_of
            for src in claim.sources:
                tier = tier_of(src.kind) or "UNCLASSIFIED"
                stats.sources_by_tier[tier] = \
                    stats.sources_by_tier.get(tier, 0) + 1

            # Divergent claims.
            if diverges(claim):
                stats.divergent_count += 1
                stats.divergent_ids.append(claim.id)

            # Competing models.
            if claim.competing_models:
                stats.competing_count += 1

    # Relations.
    links = all_links(topics)
    stats.total_edges = len(links)
    for link in links:
        claims_with_edges.add(link.source)
        claims_with_edges.add(link.target)
        if link.origin == "authored":
            stats.authored_edges += 1
        else:
            stats.mechanical_edges += 1

    # Cross-domain edges.
    claim_domain = {}
    for t in topics:
        for c in t.claims:
            claim_domain[c.id] = t.id
    for link in links:
        src_domain = claim_domain.get(link.source)
        tgt_domain = claim_domain.get(link.target)
        if src_domain and tgt_domain and src_domain != tgt_domain:
            stats.cross_domain_edges += 1

    # Average edges per claim.
    if stats.total_claims > 0:
        stats.avg_edges_per_claim = stats.total_edges * 2 / stats.total_claims

    # Isolated claims (no edges).
    all_claim_ids = {c.id for t in topics for c in t.claims}
    isolated = all_claim_ids - claims_with_edges
    stats.isolated_count = len(isolated)
    stats.isolated_ids = sorted(isolated)

    # Sparse domains (< 8 claims).
    stats.sparse_domains = sorted(
        d for d, count in stats.claims_by_domain.items() if count < 8)

    # Empty status layers per domain.
    all_statuses = {s.name for s in Status}
    for domain, covered in domain_status_coverage.items():
        missing = all_statuses - covered
        if missing:
            stats.empty_status_layers[domain] = sorted(missing)

    return stats


def format_stats_report(stats: KnowledgeStats) -> str:
    """Human-readable report."""
    lines = [
        "Knowledge Base Statistics",
        "=" * 40,
        f"Topics: {stats.total_topics}",
        f"Claims: {stats.total_claims}",
        f"Evidence items: {stats.total_evidence}",
        f"Sources: {stats.total_sources}",
        f"Open questions: {stats.total_open_questions}",
        "",
        "Claims by domain:",
    ]
    for d, c in sorted(stats.claims_by_domain.items()):
        lines.append(f"  {d}: {c}")

    lines.append("")
    lines.append("Claims by status:")
    for s, c in sorted(stats.claims_by_status.items()):
        lines.append(f"  {s}: {c}")

    lines.append("")
    lines.append("Claims by evidence axis:")
    for a, c in sorted(stats.claims_by_axis.items()):
        lines.append(f"  {a}: {c}")

    lines.append("")
    lines.append(f"Divergent claims: {stats.divergent_count}")
    lines.append(f"Competing models: {stats.competing_count}")
    lines.append(f"Isolated claims: {stats.isolated_count}")

    lines.append("")
    lines.append(f"Total edges: {stats.total_edges}")
    lines.append(f"  Authored: {stats.authored_edges}")
    lines.append(f"  Mechanical: {stats.mechanical_edges}")
    lines.append(f"  Cross-domain: {stats.cross_domain_edges}")
    lines.append(f"  Avg per claim: {stats.avg_edges_per_claim:.1f}")

    if stats.sparse_domains:
        lines.append("")
        lines.append(f"Sparse domains (< 8 claims): {stats.sparse_domains}")

    if stats.empty_status_layers:
        lines.append("")
        lines.append("Missing status layers:")
        for d, missing in sorted(stats.empty_status_layers.items()):
            lines.append(f"  {d}: {', '.join(missing)}")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    from ..data.registry import TOPICS

    parser = argparse.ArgumentParser(description="Knowledge base statistics")
    parser.add_argument("--tag", help="Filter by annotation tag")
    parser.add_argument("--label", help="Filter by annotation label")
    parser.add_argument("--has-notes", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has notes")
    parser.add_argument("--has-competing", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has competing models")
    parser.add_argument("--has-open-questions", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has open questions")
    parser.add_argument("--diverges", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim diverges")
    args = parser.parse_args()

    stats = compute_stats(TOPICS)
    print(format_stats_report(stats))

    # Write JSON to dist/.
    _DIST_DIR.mkdir(exist_ok=True)
    out = _DIST_DIR / "stats.json"
    out.write_text(json.dumps(stats.to_dict(), indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nstats.json -> {out}")
