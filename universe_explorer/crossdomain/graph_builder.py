"""Cross-domain graph builder — assemble the epistemic knowledge graph.

Combines:
  - Existing authored relations (from relations.py)
  - Cross-domain shared sources (from shared_source.py)
  - Evidence conflicts (from evidence_conflict.py)
  - Evidence gaps (from gap_analyzer.py)

Output: a graph structure (nodes + edges + clusters) suitable for
rendering into an interactive map.

Usage:
    python -m universe_explorer.crossdomain.graph_builder
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from ..axes import derive, diverges
from ..model import Status, Topic
from ..relations import all_links, ClaimLink
from .evidence_conflict import EvidenceConflict, detect_conflicts
from .gap_analyzer import DomainGap, analyze_gaps
from .shared_source import SharedSource, scan_shared_sources


@dataclass
class GraphNode:
    """One claim in the knowledge graph."""

    id: str
    title: str
    domain: str
    status: str               # Status.name
    status_rank: int
    evidence_axis: str        # E1-E5
    diverges: bool
    evidence_count: int
    open_question_count: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "domain": self.domain,
            "status": self.status,
            "status_rank": self.status_rank,
            "evidence_axis": self.evidence_axis,
            "diverges": self.diverges,
            "evidence_count": self.evidence_count,
            "open_question_count": self.open_question_count,
        }


@dataclass
class GraphEdge:
    """One edge in the knowledge graph."""

    source: str        # claim id
    target: str        # claim id
    kind: str          # from LINK_KINDS or "cross_domain_shared" / "evidence_conflict"
    origin: str        # "authored" | "mechanical" | "cross_domain"
    note: str = ""
    cross_domain: bool = False

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "kind": self.kind,
            "origin": self.origin,
            "note": self.note,
            "cross_domain": self.cross_domain,
        }


@dataclass
class DomainGraph:
    """The complete cross-domain knowledge graph."""

    nodes: List[GraphNode]
    edges: List[GraphEdge]
    clusters: Dict[str, List[str]]  # domain → claim ids
    shared_sources: List[dict]
    conflicts: List[dict]
    gaps: List[dict]

    def to_dict(self) -> dict:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "clusters": self.clusters,
            "shared_sources": self.shared_sources,
            "conflicts": self.conflicts,
            "gaps": self.gaps,
            "stats": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "cross_domain_edges": sum(1 for e in self.edges if e.cross_domain),
                "domain_count": len(self.clusters),
            },
        }


def build_cross_domain_graph(topics: List[Topic]) -> DomainGraph:
    """Build the complete epistemic knowledge graph."""
    nodes = []
    clusters = {}
    node_ids = set()

    # 1. Build nodes from all claims.
    for topic in topics:
        clusters[topic.id] = []
        for claim in topic.claims:
            d = derive(claim)
            node = GraphNode(
                id=claim.id,
                title=claim.title,
                domain=topic.id,
                status=claim.status.name,
                status_rank=claim.status.rank,
                evidence_axis=d.strength.short,
                diverges=diverges(claim),
                evidence_count=len(claim.evidence),
                open_question_count=len(claim.open_questions),
            )
            nodes.append(node)
            clusters[topic.id].append(claim.id)
            node_ids.add(claim.id)

    # 2. Build edges from authored relations.
    edges = []
    existing_edges = all_links(topics)
    for link in existing_edges:
        edges.append(GraphEdge(
            source=link.source,
            target=link.target,
            kind=link.kind,
            origin=link.origin,
            note=link.note,
            cross_domain=False,
        ))

    # 3. Add cross-domain shared source edges.
    shared = scan_shared_sources(topics)
    for s in shared:
        claim_ids = [c["claim_id"] for c in s.claims]
        for i, ca in enumerate(claim_ids):
            for cb in claim_ids[i + 1:]:
                if ca in node_ids and cb in node_ids:
                    edges.append(GraphEdge(
                        source=ca,
                        target=cb,
                        kind="cross_domain_shared",
                        origin="cross_domain",
                        note=f"shared source: {s.normalized_id}",
                        cross_domain=True,
                    ))

    # 4. Add evidence conflict edges.
    conflicts = detect_conflicts(topics)
    for c in conflicts:
        if c.claim_a["id"] in node_ids and c.claim_b["id"] in node_ids:
            edges.append(GraphEdge(
                source=c.claim_a["id"],
                target=c.claim_b["id"],
                kind="evidence_conflict",
                origin="cross_domain",
                note=c.description,
                cross_domain=True,
            ))

    # 5. Compute gaps.
    gaps = analyze_gaps(topics)

    return DomainGraph(
        nodes=nodes,
        edges=edges,
        clusters=clusters,
        shared_sources=[s.to_dict() for s in shared],
        conflicts=[c.to_dict() for c in conflicts],
        gaps=[g.to_dict() for g in gaps],
    )


def format_graph_report(graph: DomainGraph) -> str:
    """Human-readable summary."""
    stats = graph.to_dict()["stats"]
    lines = [
        f"Cross-domain graph:",
        f"  Nodes: {stats['node_count']}",
        f"  Edges: {stats['edge_count']} "
        f"({stats['cross_domain_edges']} cross-domain)",
        f"  Domains: {stats['domain_count']}",
        f"  Shared sources: {len(graph.shared_sources)}",
        f"  Conflicts: {len(graph.conflicts)}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    from ..data.registry import TOPICS

    parser = argparse.ArgumentParser(description="Cross-domain graph")
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

    graph = build_cross_domain_graph(TOPICS)

    if args.tag or args.label or args.has_notes is not None or args.has_competing is not None or args.has_open_questions is not None or args.diverges is not None:
        from ..reader.annotate import ClaimAnnotations
        annotations = ClaimAnnotations()
        filtered_ids = set()
        for claim_dir in (Path(__file__).parent.parent.parent / "annotations").iterdir():
            if not claim_dir.is_dir():
                continue
            claim_id = claim_dir.name
            if args.tag and annotations.has_tag(claim_id, args.tag):
                filtered_ids.add(claim_id)
            if args.label and args.label in annotations.get_labels(claim_id):
                filtered_ids.add(claim_id)
            if args.has_notes is not None:
                has = bool(annotations.get_notes(claim_id))
                if has == args.has_notes:
                    filtered_ids.add(claim_id)
        # For has_competing and has_open_questions, we need to check claim data
        if args.has_competing is not None or args.has_open_questions is not None:
            claim_map = {c.id: c for t in TOPICS for c in t.claims}
            for node in graph.nodes:
                if node.id in claim_map:
                    if args.has_competing is not None:
                        has = bool(claim_map[node.id].competing_models)
                        if has == args.has_competing:
                            filtered_ids.add(node.id)
                    if args.has_open_questions is not None:
                        has = bool(claim_map[node.id].open_questions)
                        if has == args.has_open_questions:
                            filtered_ids.add(node.id)
        # For diverges, we need to check claim data
        if args.diverges is not None:
            from ..axes import diverges as _diverges
            claim_map = {c.id: c for t in TOPICS for c in t.claims}
            for node in graph.nodes:
                if node.id in claim_map:
                    has = _diverges(claim_map[node.id])
                    if has == args.diverges:
                        filtered_ids.add(node.id)
        graph.nodes = [n for n in graph.nodes if n.id in filtered_ids]
        graph.edges = [e for e in graph.edges
                       if e.source in filtered_ids and e.target in filtered_ids]

    print(format_graph_report(graph))
    # Write graph JSON to dist/.
    dist = Path(__file__).parent.parent.parent / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / "epistemic-graph.json"
    out.write_text(json.dumps(graph.to_dict(), indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"  Graph JSON -> {out}")
