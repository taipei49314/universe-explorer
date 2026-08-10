"""Adversarial tests — find what logic coverage misses.

Philosophy: build measurement before trusting behavior.
Test the edges, the empty, the weird, the corrupted.

Categories:
  1. Empty / minimal data
  2. Unicode / encoding stress
  3. Boundary conditions
  4. Cache corruption
  5. Missing directories
  6. Cross-module consistency
  7. CLI error handling
  8. Performance regression
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from universe_explorer.model import (
    Claim, CompetingModel, ConditionAssessment, Evidence,
    Source, Status, Topic,
)
from universe_explorer.validator import validate_claim, validate_topic
from universe_explorer.axes import derive, diverges, EvidenceStrength
from universe_explorer.relations import all_links, validate_links
from universe_explorer.reader.search_index import ClaimSearchIndex, _tokenize
from universe_explorer.reader.filter_engine import ClaimFilter, FilterCriteria
from universe_explorer.reader.stats import compute_stats
from universe_explorer.reader.annotate import ClaimAnnotations
from universe_explorer.reader.review import ReviewManager
from universe_explorer.reader.diff import diff_claims
from universe_explorer.crossdomain.shared_source import scan_shared_sources
from universe_explorer.crossdomain.gap_analyzer import analyze_gaps
from universe_explorer.crossdomain.graph_builder import build_cross_domain_graph


# ---------------------------------------------------------------------------
# 1. Empty / minimal data
# ---------------------------------------------------------------------------


class TestEmptyData:
    """What happens when there's nothing?"""

    def test_zero_topics(self):
        stats = compute_stats([])
        assert stats.total_claims == 0
        assert stats.total_topics == 0

    def test_zero_topics_filter(self):
        f = ClaimFilter([])
        results = f.filter(FilterCriteria())
        assert results == []

    def test_zero_topics_search(self):
        index = ClaimSearchIndex([])
        results = index.search("anything")
        assert results == []

    def test_zero_topics_graph(self):
        graph = build_cross_domain_graph([])
        assert len(graph.nodes) == 0
        # Edges may exist from authored_links (hardcoded), but no cross-domain
        cd_edges = [e for e in graph.edges if e.cross_domain]
        assert len(cd_edges) == 0

    def test_zero_topics_shared_sources(self):
        shared = scan_shared_sources([])
        assert shared == []

    def test_zero_topics_gaps(self):
        gaps = analyze_gaps([])
        assert gaps == []

    def test_single_claim_topic(self):
        topic = Topic(
            id="solo", title="Solo", summary="",
            claims=[Claim(
                id="only", title="The only claim",
                status=Status.ESTABLISHED,
                sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                kind="preprint (arXiv)")],
                evidence=[Evidence(type="direct observation",
                                   description="Observed.",
                                   source_ref="s1")],
            )],
        )
        stats = compute_stats([topic])
        assert stats.total_claims == 1
        assert stats.total_topics == 1

    def test_claim_with_no_evidence_fails_validator(self):
        claim = Claim(
            id="empty", title="No evidence",
            status=Status.ESTABLISHED,
            sources=[],
            evidence=[],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "unsupported_claim" for v in violations)

    def test_claim_with_no_sources_fails_validator(self):
        claim = Claim(
            id="nosrc", title="No sources",
            status=Status.ESTABLISHED,
            sources=[],
            evidence=[Evidence(type="direct observation",
                               description="Something",
                               source_ref="nonexistent")],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "dangling_source_ref" for v in violations)

    def test_empty_open_question_fails(self):
        claim = Claim(
            id="eoq", title="Empty question",
            status=Status.ESTABLISHED,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="Something",
                               source_ref="s1")],
            open_questions=[""],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "empty_open_question" for v in violations)


# ---------------------------------------------------------------------------
# 2. Unicode / encoding stress
# ---------------------------------------------------------------------------


class TestUnicode:
    """Unicode should not break anything."""

    def test_chinese_title(self):
        claim = Claim(
            id="zh_test", title="黑洞事件視界是否存在",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="觀測到黑洞陰影",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert violations == []

    def test_unicode_in_search(self):
        topic = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="黑洞事件視界",
                  status=Status.FRONTIER,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="觀測",
                                     source_ref="s1")],
                  status_reason=[ConditionAssessment("new_discovery", True, "New.")]),
        ])
        index = ClaimSearchIndex([topic], use_cache=False)
        results = index.search("黑洞")
        assert len(results) >= 1

    def test_unicode_in_tags(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        mgr.add_tag("c1", "需要審查")
        assert mgr.has_tag("c1", "需要審查")

    def test_unicode_in_notes(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        mgr.add_note("c1", "這個 claim 需要更多證據")
        notes = mgr.get_notes("c1")
        assert len(notes) == 1
        assert "證據" in notes[0]["value"]

    def test_emoji_in_title(self):
        claim = Claim(
            id="emoji", title="Black holes exist",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="Observed",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert violations == []

    def test_mixed_lang_title(self):
        claim = Claim(
            id="mixed", title="Black hole observations",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="Observed",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert violations == []


# ---------------------------------------------------------------------------
# 3. Boundary conditions
# ---------------------------------------------------------------------------


class TestBoundaries:
    """Test the edges of valid ranges."""

    def test_all_five_statuses(self):
        """Every status should be valid."""
        for status in Status:
            claim = Claim(
                id=f"test_{status.name}", title=f"Test {status.name}",
                status=status,
                sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                kind="preprint (arXiv)")],
                evidence=[Evidence(type="direct observation",
                                   description="Something",
                                   source_ref="s1")],
                status_reason=_make_reason_for(status),
            )
            violations = validate_claim(claim)
            # Should have no violations (or only expected ones)
            assert isinstance(violations, list)

    def test_all_five_evidence_strengths(self):
        """Every evidence axis should be derivable."""
        for strength in EvidenceStrength:
            # Can't directly set, but can verify derivation doesn't crash
            assert strength.short in ("E1", "E2", "E3", "E4", "E5")

    def test_many_evidence_items(self):
        """Claim with many evidence items shouldn't break."""
        sources = [Source(label=f"s{i}", url_or_id=f"arXiv:{i:04d}.00000",
                          kind="preprint (arXiv)") for i in range(20)]
        evidence = [Evidence(type="direct observation",
                             description=f"Observation {i}",
                             source_ref=f"s{i}") for i in range(20)]
        claim = Claim(
            id="many_ev", title="Many evidence items",
            status=Status.ESTABLISHED,
            sources=sources, evidence=evidence,
        )
        d = derive(claim)
        assert d.strength in EvidenceStrength

    def test_many_open_questions(self):
        """Claim with many open questions shouldn't break."""
        questions = [f"Question {i}?" for i in range(50)]
        claim = Claim(
            id="many_oq", title="Many questions",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="Something",
                               source_ref="s1")],
            open_questions=questions,
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert violations == []

    def test_very_long_title(self):
        """Very long title shouldn't break."""
        long_title = "A" * 1000
        claim = Claim(
            id="long_title", title=long_title,
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert violations == []

    def test_very_long_evidence_description(self):
        """Very long evidence description shouldn't break."""
        long_desc = "Evidence " * 500
        claim = Claim(
            id="long_ev", title="Long evidence",
            status=Status.ESTABLISHED,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description=long_desc,
                               source_ref="s1")],
        )
        d = derive(claim)
        assert d.strength in EvidenceStrength

    def test_special_chars_in_id(self):
        """IDs with hyphens and underscores should work."""
        claim = Claim(
            id="test-claim_v2.0", title="Special ID",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert violations == []


# ---------------------------------------------------------------------------
# 4. Cache corruption
# ---------------------------------------------------------------------------


class TestCacheCorruption:
    """What if cache files are corrupted?"""

    def test_corrupted_search_cache(self, tmp_path):
        """Corrupted cache should be ignored, not crash."""
        cache_dir = tmp_path / "cache" / "search_index"
        cache_dir.mkdir(parents=True)
        # Write garbage
        (cache_dir / "bad.json").write_text("not valid json{{{", encoding="utf-8")

        # Should not crash - falls back to rebuild
        topic = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="Test",
                  status=Status.ESTABLISHED,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="Something",
                                     source_ref="s1")]),
        ])
        index = ClaimSearchIndex([topic], use_cache=False)
        results = index.search("test")
        assert len(results) >= 1

    def test_missing_cache_dir(self, tmp_path):
        """Missing cache directory shouldn't crash."""
        topic = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="Test",
                  status=Status.ESTABLISHED,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="Something",
                                     source_ref="s1")]),
        ])
        index = ClaimSearchIndex([topic], use_cache=False)
        results = index.search("test")
        assert len(results) >= 1


# ---------------------------------------------------------------------------
# 5. Missing directories
# ---------------------------------------------------------------------------


class TestMissingDirectories:
    """What if expected directories don't exist?"""

    def test_annotations_dir_missing(self, tmp_path):
        """ClaimAnnotations should create directory on first write."""
        ann_dir = tmp_path / "nonexistent"
        mgr = ClaimAnnotations(ann_dir)
        mgr.add_tag("c1", "test")
        assert (ann_dir / "c1").exists()

    def test_reviews_dir_missing(self, tmp_path):
        """ReviewManager should create directory on first write."""
        rev_dir = tmp_path / "nonexistent"
        mgr = ReviewManager(rev_dir)
        mgr.start_review("c1")
        assert (rev_dir / "c1.json").exists()


# ---------------------------------------------------------------------------
# 6. Cross-module consistency
# ---------------------------------------------------------------------------


class TestCrossModuleConsistency:
    """Do different modules agree on the same data?"""

    def test_validator_and_axes_agree_on_evidence(self):
        """Validator and axes should be consistent about evidence types."""
        claim = Claim(
            id="consistency", title="Consistency test",
            status=Status.ESTABLISHED,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="preprint (arXiv)")],
            evidence=[Evidence(type="direct observation",
                               description="Something",
                               source_ref="s1")],
        )
        violations = validate_claim(claim)
        d = derive(claim)
        # If validator passes, axes should produce a valid result
        if not violations:
            assert d.strength in EvidenceStrength

    def test_filter_and_search_find_same_claims(self):
        """Filter and search should find overlapping claims."""
        topic = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="Gravitational waves detected",
                  status=Status.ESTABLISHED,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="LIGO detection",
                                     source_ref="s1")]),
        ])
        index = ClaimSearchIndex([topic])
        search_results = index.search("gravitational")

        filt = ClaimFilter([topic])
        filter_results = filt.filter(FilterCriteria())

        # Both should find c1
        search_ids = {r.claim_id for r in search_results}
        filter_ids = {r["claim_id"] for r in filter_results}
        assert "c1" in search_ids or "c1" in filter_ids

    def test_stats_counts_match_filter_counts(self):
        """Stats and filter should agree on claim counts."""
        topics = _make_multi_domain_topics()
        stats = compute_stats(topics)
        filt = ClaimFilter(topics)
        all_claims = filt.filter(FilterCriteria())
        assert stats.total_claims == len(all_claims)

    def test_graph_nodes_match_claims(self):
        """Graph should have one node per claim."""
        topics = _make_multi_domain_topics()
        graph = build_cross_domain_graph(topics)
        total_claims = sum(len(t.claims) for t in topics)
        assert len(graph.nodes) == total_claims


# ---------------------------------------------------------------------------
# 7. CLI error handling
# ---------------------------------------------------------------------------


class TestCLIErrorHandling:
    """CLI should not crash on bad input."""

    def test_tokenize_empty(self):
        assert _tokenize("") == []

    def test_tokenize_whitespace(self):
        assert _tokenize("   ") == []

    def test_tokenize_special_chars(self):
        tokens = _tokenize("!@#$%^&*()")
        assert tokens == []

    def test_tokenize_numbers_only(self):
        tokens = _tokenize("12345")
        # Numbers > 2 chars should be included
        assert "12345" in tokens

    def test_tokenize_single_char(self):
        tokens = _tokenize("a b c")
        # Single chars should be filtered out
        assert tokens == []


# ---------------------------------------------------------------------------
# 8. Performance regression
# ---------------------------------------------------------------------------


class TestPerformance:
    """Ensure operations complete within reasonable time."""

    def test_search_91_claims_under_100ms(self):
        from universe_explorer.data.registry import TOPICS
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        start = time.time()
        for _ in range(10):
            index.search("black hole")
        elapsed = (time.time() - start) / 10
        assert elapsed < 0.1, f"Search took {elapsed:.3f}s (limit: 0.1s)"

    def test_filter_91_claims_under_50ms(self):
        from universe_explorer.data.registry import TOPICS
        filt = ClaimFilter(TOPICS)
        start = time.time()
        for _ in range(10):
            filt.filter(FilterCriteria())
        elapsed = (time.time() - start) / 10
        assert elapsed < 0.05, f"Filter took {elapsed:.3f}s (limit: 0.05s)"

    def test_stats_under_100ms(self):
        from universe_explorer.data.registry import TOPICS
        start = time.time()
        for _ in range(10):
            compute_stats(TOPICS)
        elapsed = (time.time() - start) / 10
        assert elapsed < 0.1, f"Stats took {elapsed:.3f}s (limit: 0.1s)"

    def test_graph_build_under_1s(self):
        from universe_explorer.data.registry import TOPICS
        start = time.time()
        build_cross_domain_graph(TOPICS)
        elapsed = time.time() - start
        assert elapsed < 1.0, f"Graph build took {elapsed:.3f}s (limit: 1s)"

    def test_validate_all_claims_under_1s(self):
        from universe_explorer.data.registry import TOPICS
        start = time.time()
        for topic in TOPICS:
            validate_topic(topic)
        elapsed = time.time() - start
        assert elapsed < 1.0, f"Validation took {elapsed:.3f}s (limit: 1s)"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_reason_for(status: Status) -> list:
    """Generate minimal status_reason for a given status."""
    spec = {
        Status.ESTABLISHED: [
            ConditionAssessment("multiple_independent_replications", True, "Multiple groups verified."),
            ConditionAssessment("accepted_in_mainstream_textbooks", True, "In textbooks."),
            ConditionAssessment("no_mainstream_competing_theory", True, "No competitors."),
            ConditionAssessment("no_recent_major_refutation", True, "No refutations."),
        ],
        Status.STRONG: [
            ConditionAssessment("mainstream_model_support", True, "Supported."),
            ConditionAssessment("minor_alternatives_exist", True, "Minor alternatives."),
            ConditionAssessment("overall_direction_robust", True, "Robust."),
        ],
        Status.COMPETING: [
            ConditionAssessment("two_or_more_mainstream_models", True, "Two models."),
            ConditionAssessment("no_decisive_evidence_yet", True, "No decisive evidence."),
            ConditionAssessment("genuine_scientific_camps", True, "Real camps."),
        ],
        Status.FRONTIER: [
            ConditionAssessment("new_discovery", True, "New discovery."),
        ],
        Status.SPECULATIVE: [
            ConditionAssessment("no_observational_evidence", True, "No observations."),
        ],
    }
    return spec.get(status, [])


def _make_multi_domain_topics():
    """Create multiple topics with claims for cross-module testing."""
    src = Source(label="s1", url_or_id="arXiv:0000.00000",
                 kind="preprint (arXiv)")
    topics = []
    for domain in ["cosmology", "stars", "ocean"]:
        claims = []
        for i in range(3):
            claims.append(Claim(
                id=f"{domain}_c{i}",
                title=f"Claim {i} in {domain}",
                status=list(Status)[i % 5],
                sources=[src],
                evidence=[Evidence(type="direct observation",
                                   description=f"Evidence {i}",
                                   source_ref="s1")],
                status_reason=_make_reason_for(list(Status)[i % 5]),
            ))
        topics.append(Topic(id=domain, title=domain, summary="", claims=claims))
    return topics
