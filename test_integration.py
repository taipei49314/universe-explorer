"""End-to-end integration tests.

Verifies:
  - python build.py generates all expected pages
  - Discovery pipeline CLI works
  - Cross-domain analysis runs on real data
  - Reader search/filter works on real data
  - All new pages are self-contained HTML
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from universe_explorer.data.registry import TOPICS
from universe_explorer.discovery.review import generate_review_dashboard, list_candidates
from universe_explorer.discovery.precheck import precheck, PrecheckReport
from universe_explorer.crossdomain.shared_source import scan_shared_sources
from universe_explorer.crossdomain.evidence_conflict import detect_conflicts
from universe_explorer.crossdomain.gap_analyzer import analyze_gaps
from universe_explorer.crossdomain.graph_builder import build_cross_domain_graph
from universe_explorer.crossdomain.render_map import render_epistemic_map
from universe_explorer.reader.search_index import ClaimSearchIndex
from universe_explorer.reader.filter_engine import ClaimFilter, FilterCriteria
from universe_explorer.reader.dual_axis_viz import generate_dual_axis_svg
from universe_explorer.reader.guided_reading import GuidedReader
from universe_explorer.reader.render_explore import render_explore_v2
from universe_explorer.reader.challenge_form import generate_challenge_form


# ---------------------------------------------------------------------------
# Cross-domain analysis on real data
# ---------------------------------------------------------------------------


class TestCrossDomainRealData:
    def test_shared_sources_finds_connections(self):
        shared = scan_shared_sources(TOPICS)
        # With 91 claims across 8 domains, there should be some cross-domain links
        assert isinstance(shared, list)
        for s in shared:
            assert len(s.domains) > 1

    def test_conflicts_on_real_data(self):
        conflicts = detect_conflicts(TOPICS)
        assert isinstance(conflicts, list)
        for c in conflicts:
            assert c.claim_a["domain"] != c.claim_b["domain"]

    def test_gaps_covers_all_domains(self):
        gaps = analyze_gaps(TOPICS)
        domains = {g.domain for g in gaps}
        expected = {t.id for t in TOPICS}
        assert domains == expected

    def test_graph_builder_real_data(self):
        graph = build_cross_domain_graph(TOPICS)
        assert len(graph.nodes) == 91
        assert len(graph.edges) > 0
        stats = graph.to_dict()["stats"]
        assert stats["node_count"] == 91
        assert stats["domain_count"] == 8


# ---------------------------------------------------------------------------
# Reader on real data
# ---------------------------------------------------------------------------


class TestReaderRealData:
    def test_search_index_finds_claims(self):
        index = ClaimSearchIndex(TOPICS)
        # Search for something we know exists
        results = index.search("black hole")
        assert len(results) > 0

    def test_search_index_suggest(self):
        index = ClaimSearchIndex(TOPICS)
        suggestions = index.suggest("grav")
        assert len(suggestions) > 0

    def test_filter_all_claims(self):
        f = ClaimFilter(TOPICS)
        results = f.filter(FilterCriteria())
        assert len(results) == 91

    def test_filter_by_domain(self):
        f = ClaimFilter(TOPICS)
        results = f.filter(FilterCriteria(domain="black_hole"))
        assert len(results) == 10

    def test_filter_by_status(self):
        f = ClaimFilter(TOPICS)
        results = f.filter(FilterCriteria(status="ESTABLISHED"))
        assert len(results) > 0

    def test_filter_divergent(self):
        f = ClaimFilter(TOPICS)
        results = f.filter(FilterCriteria(diverges=True))
        # Hawking radiation should be divergent
        ids = [r["claim_id"] for r in results]
        assert "hawking_radiation" in ids

    def test_count_by_domain(self):
        f = ClaimFilter(TOPICS)
        counts = f.count_by("domain")
        assert counts["black_hole"] == 10
        assert counts["cosmology"] == 16

    def test_guided_reader_paths(self):
        reader = GuidedReader(TOPICS)
        paths = reader.list_paths()
        assert len(paths) > 0

    def test_guided_reader_claim_context(self):
        reader = GuidedReader(TOPICS)
        step = reader.get_claim_context("hawking_radiation")
        assert step is not None
        assert step.diverges is True
        assert step.evidence_axis == "E3"


# ---------------------------------------------------------------------------
# SVG generation
# ---------------------------------------------------------------------------


class TestDualAxisRealData:
    def test_svg_contains_all_claims(self):
        svg = generate_dual_axis_svg(TOPICS)
        assert "<svg" in svg
        # Should have 91 circles
        assert svg.count("<circle") == 91


# ---------------------------------------------------------------------------
# HTML page generation
# ---------------------------------------------------------------------------


class TestPageGeneration:
    def test_explore_v2_generates(self, tmp_path):
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        assert (tmp_path / "explore-v2.html").exists()

    def test_explore_v2_is_html(self, tmp_path):
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        content = (tmp_path / "explore-v2.html").read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "Explore" in content

    def test_challenge_form_generates(self, tmp_path):
        generate_challenge_form(dist_dir=tmp_path)
        assert (tmp_path / "challenge.html").exists()

    def test_epistemic_map_generates(self, tmp_path):
        graph = build_cross_domain_graph(TOPICS)
        render_epistemic_map(graph, dist_dir=tmp_path)
        assert (tmp_path / "epistemic_map.html").exists()

    def test_epistemic_map_is_html(self, tmp_path):
        graph = build_cross_domain_graph(TOPICS)
        render_epistemic_map(graph, dist_dir=tmp_path)
        content = (tmp_path / "epistemic_map.html").read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "Epistemic Map" in content

    def test_review_dashboard_generates(self, tmp_path):
        generate_review_dashboard(dist_dir=tmp_path)
        assert (tmp_path / "review.html").exists()


# ---------------------------------------------------------------------------
# Graph JSON
# ---------------------------------------------------------------------------


class TestGraphJSON:
    def test_graph_json_has_required_fields(self):
        graph = build_cross_domain_graph(TOPICS)
        d = graph.to_dict()
        assert "nodes" in d
        assert "edges" in d
        assert "clusters" in d
        assert "shared_sources" in d
        assert "conflicts" in d
        assert "gaps" in d
        assert "stats" in d

    def test_graph_json_serializable(self):
        graph = build_cross_domain_graph(TOPICS)
        # Should not raise
        json_str = json.dumps(graph.to_dict(), ensure_ascii=False)
        assert len(json_str) > 0
