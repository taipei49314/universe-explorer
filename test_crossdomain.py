"""Tests for the cross-domain epistemic map.

Covers:
  - Shared source scanner
  - Evidence conflict detector
  - Gap analyzer
  - Graph builder
"""

from __future__ import annotations

import pytest

from universe_explorer.crossdomain.shared_source import (
    SharedSource,
    scan_shared_sources,
    _normalize,
)
from universe_explorer.crossdomain.evidence_conflict import (
    EvidenceConflict,
    detect_conflicts,
    _find_nid,
)
from universe_explorer.crossdomain.gap_analyzer import (
    DomainGap,
    analyze_gaps,
    _ALL_EVIDENCE_TYPES,
)
from universe_explorer.crossdomain.graph_builder import (
    DomainGraph,
    GraphNode,
    GraphEdge,
    build_cross_domain_graph,
)
from universe_explorer.model import (
    Claim,
    Evidence,
    Source,
    Status,
    Topic,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_topic(topic_id: str, claims: list) -> Topic:
    return Topic(id=topic_id, title=topic_id, summary="", claims=claims)


def _make_claim(claim_id: str, status: Status, sources: list,
                evidence: list) -> Claim:
    return Claim(
        id=claim_id,
        title=f"Claim {claim_id}",
        status=status,
        sources=sources,
        evidence=evidence,
        status_reason=[],
        open_questions=[],
    )


def _sample_topics() -> list:
    """Two topics sharing one source."""
    shared_src = Source(
        label="arXiv-2311-08680",
        url_or_id="arXiv:2311.08680",
        kind="preprint (arXiv)",
    )
    topic_a = _make_topic("cosmology", [
        _make_claim("claim_a1", Status.STRONG, [shared_src], [
            Evidence(type="direct observation", description="Observed X",
                     source_ref="arXiv-2311-08680"),
        ]),
    ])
    topic_b = _make_topic("black_hole", [
        _make_claim("claim_b1", Status.FRONTIER, [shared_src], [
            Evidence(type="theoretical result", description="Derived Y",
                     source_ref="arXiv-2311-08680"),
        ]),
    ])
    return [topic_a, topic_b]


def _single_domain_topics() -> list:
    """One topic, no cross-domain."""
    src = Source(label="s1", url_or_id="arXiv:1111.11111",
                 kind="preprint (arXiv)")
    topic = _make_topic("stars", [
        _make_claim("c1", Status.ESTABLISHED, [src], [
            Evidence(type="direct observation", description="D",
                     source_ref="s1"),
        ]),
        _make_claim("c2", Status.STRONG, [src], [
            Evidence(type="direct observation", description="D2",
                     source_ref="s1"),
        ]),
    ])
    return [topic]


# ---------------------------------------------------------------------------
# _normalize
# ---------------------------------------------------------------------------


class TestNormalize:
    def test_arxiv(self):
        assert _normalize("arXiv:2311.08680") == "arXiv:2311.08680"

    def test_doi(self):
        assert _normalize("doi:10.1038/nphys1234") == "doi:10.1038/nphys1234"

    def test_non_fetchable(self):
        assert _normalize("nobelprize.org/prizes/physics/2020") is None


# ---------------------------------------------------------------------------
# scan_shared_sources
# ---------------------------------------------------------------------------


class TestSharedSources:
    def test_finds_cross_domain(self):
        shared = scan_shared_sources(_sample_topics())
        assert len(shared) == 1
        assert shared[0].normalized_id == "arXiv:2311.08680"
        assert len(shared[0].domains) == 2

    def test_no_cross_domain(self):
        shared = scan_shared_sources(_single_domain_topics())
        assert len(shared) == 0

    def test_to_dict(self):
        shared = scan_shared_sources(_sample_topics())
        d = shared[0].to_dict()
        assert "source_ref" in d
        assert "domain_count" in d


# ---------------------------------------------------------------------------
# detect_conflicts
# ---------------------------------------------------------------------------


class TestConflicts:
    def test_detects_type_difference(self):
        conflicts = detect_conflicts(_sample_topics())
        assert len(conflicts) >= 1
        c = conflicts[0]
        assert c.claim_a["evidence_type"] != c.claim_b["evidence_type"]

    def test_no_conflict_single_domain(self):
        conflicts = detect_conflicts(_single_domain_topics())
        assert len(conflicts) == 0

    def test_to_dict(self):
        conflicts = detect_conflicts(_sample_topics())
        if conflicts:
            d = conflicts[0].to_dict()
            assert "claim_a" in d
            assert "claim_b" in d


# ---------------------------------------------------------------------------
# analyze_gaps
# ---------------------------------------------------------------------------


class TestGapAnalyzer:
    def test_analyzes_single_domain(self):
        gaps = analyze_gaps(_single_domain_topics())
        assert len(gaps) == 1
        g = gaps[0]
        assert g.domain == "stars"
        assert g.total_claims == 2

    def test_missing_evidence_types(self):
        gaps = analyze_gaps(_single_domain_topics())
        g = gaps[0]
        # Only "direct observation" present, others missing.
        assert "direct observation" not in g.missing_evidence_types
        assert "analog experiment" in g.missing_evidence_types

    def test_light_counts(self):
        gaps = analyze_gaps(_single_domain_topics())
        g = gaps[0]
        assert g.light_counts.get("ESTABLISHED") == 1
        assert g.light_counts.get("STRONG") == 1

    def test_to_dict(self):
        gaps = analyze_gaps(_single_domain_topics())
        d = gaps[0].to_dict()
        assert "domain" in d
        assert "missing_evidence_types" in d


# ---------------------------------------------------------------------------
# build_cross_domain_graph
# ---------------------------------------------------------------------------


class TestGraphBuilder:
    def test_builds_graph(self):
        graph = build_cross_domain_graph(_sample_topics())
        assert len(graph.nodes) == 2
        assert len(graph.edges) >= 1  # at least the cross-domain shared edge

    def test_clusters(self):
        graph = build_cross_domain_graph(_sample_topics())
        assert "cosmology" in graph.clusters
        assert "black_hole" in graph.clusters

    def test_cross_domain_edge(self):
        graph = build_cross_domain_graph(_sample_topics())
        cd_edges = [e for e in graph.edges if e.cross_domain]
        assert len(cd_edges) >= 1

    def test_to_dict(self):
        graph = build_cross_domain_graph(_sample_topics())
        d = graph.to_dict()
        assert "nodes" in d
        assert "edges" in d
        assert "stats" in d
        assert d["stats"]["node_count"] == 2

    def test_single_domain_no_cross_edges(self):
        graph = build_cross_domain_graph(_single_domain_topics())
        cd_edges = [e for e in graph.edges if e.cross_domain]
        assert len(cd_edges) == 0


# ---------------------------------------------------------------------------
# GraphNode / GraphEdge data classes
# ---------------------------------------------------------------------------


class TestDataClasses:
    def test_graph_node(self):
        n = GraphNode(
            id="c1", title="Test", domain="d1",
            status="STRONG", status_rank=1,
            evidence_axis="E2", diverges=False,
            evidence_count=3, open_question_count=2,
        )
        d = n.to_dict()
        assert d["id"] == "c1"
        assert d["diverges"] is False

    def test_graph_edge(self):
        e = GraphEdge(
            source="c1", target="c2", kind="supports",
            origin="authored", note="test",
        )
        d = e.to_dict()
        assert d["cross_domain"] is False
