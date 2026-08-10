"""Tests for the reader experience module.

Covers:
  - ClaimSearchIndex (tokenize, search, suggest)
  - ClaimFilter (filter, count_by)
  - Dual-axis SVG generation
  - GuidedReader (paths, steps)
  - Challenge form
"""

from __future__ import annotations

import pytest

from universe_explorer.reader.search_index import (
    ClaimSearchIndex,
    SearchResult,
    _tokenize,
)
from universe_explorer.reader.filter_engine import (
    ClaimFilter,
    FilterCriteria,
)
from universe_explorer.reader.dual_axis_viz import (
    generate_dual_axis_svg,
    _axis_rank,
)
from universe_explorer.reader.guided_reading import (
    GuidedReader,
    ReadingStep,
)
from universe_explorer.reader.challenge_form import submit_challenge
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


def _sample_topics() -> list:
    src1 = Source(label="s1", url_or_id="arXiv:1111.11111",
                  kind="preprint (arXiv)")
    src2 = Source(label="s2", url_or_id="arXiv:2222.22222",
                  kind="preprint (arXiv)")
    claim1 = Claim(
        id="c1", title="Gravitational waves from binary mergers",
        status=Status.ESTABLISHED,
        sources=[src1],
        evidence=[Evidence(type="direct observation",
                           description="LIGO detected gravitational waves",
                           source_ref="s1")],
        open_questions=["What is the mass distribution?"],
    )
    claim2 = Claim(
        id="c2", title="Dark matter candidates",
        status=Status.COMPETING,
        sources=[src2],
        evidence=[Evidence(type="theoretical result",
                           description="WIMP model predicts detection rates",
                           source_ref="s2")],
        competing_models=[],
        open_questions=[],
    )
    return [
        Topic(id="cosmology", title="Cosmology", summary="",
              claims=[claim1]),
        Topic(id="dark_matter", title="Dark Matter", summary="",
              claims=[claim2]),
    ]


# ---------------------------------------------------------------------------
# _tokenize
# ---------------------------------------------------------------------------


class TestTokenize:
    def test_basic(self):
        tokens = _tokenize("Gravitational waves from binary mergers")
        assert "gravitational" in tokens
        assert "waves" in tokens
        assert "binary" in tokens

    def test_empty(self):
        assert _tokenize("") == []

    def test_alphanumeric(self):
        tokens = _tokenize("test-123 abc")
        assert "test" in tokens
        assert "123" in tokens


# ---------------------------------------------------------------------------
# ClaimSearchIndex
# ---------------------------------------------------------------------------


class TestSearchIndex:
    def test_search_by_title(self):
        index = ClaimSearchIndex(_sample_topics())
        results = index.search("gravitational")
        assert len(results) >= 1
        assert results[0].claim_id == "c1"

    def test_search_by_evidence(self):
        index = ClaimSearchIndex(_sample_topics())
        results = index.search("LIGO")
        assert len(results) >= 1

    def test_search_no_match(self):
        index = ClaimSearchIndex(_sample_topics())
        results = index.search("nonexistent")
        assert len(results) == 0

    def test_suggest(self):
        index = ClaimSearchIndex(_sample_topics())
        suggestions = index.suggest("grav")
        assert any("gravitational" in s for s in suggestions)

    def test_result_to_dict(self):
        index = ClaimSearchIndex(_sample_topics())
        results = index.search("waves")
        if results:
            d = results[0].to_dict()
            assert "claim_id" in d
            assert "score" in d


# ---------------------------------------------------------------------------
# ClaimFilter
# ---------------------------------------------------------------------------


class TestFilter:
    def test_filter_all(self):
        f = ClaimFilter(_sample_topics())
        results = f.filter(FilterCriteria())
        assert len(results) == 2

    def test_filter_by_domain(self):
        f = ClaimFilter(_sample_topics())
        results = f.filter(FilterCriteria(domain="cosmology"))
        assert len(results) == 1
        assert results[0]["claim_id"] == "c1"

    def test_filter_by_status(self):
        f = ClaimFilter(_sample_topics())
        results = f.filter(FilterCriteria(status="ESTABLISHED"))
        assert len(results) == 1

    def test_filter_by_axis(self):
        f = ClaimFilter(_sample_topics())
        # E1 requires multiple independent direct — our fixture has only one
        results_e2 = f.filter(FilterCriteria(evidence_axis="E2"))
        assert len(results_e2) >= 1

    def test_count_by_domain(self):
        f = ClaimFilter(_sample_topics())
        counts = f.count_by("domain")
        assert counts.get("cosmology") == 1
        assert counts.get("dark_matter") == 1

    def test_count_by_status(self):
        f = ClaimFilter(_sample_topics())
        counts = f.count_by("status")
        assert counts.get("ESTABLISHED") == 1
        assert counts.get("COMPETING") == 1


# ---------------------------------------------------------------------------
# _axis_rank
# ---------------------------------------------------------------------------


class TestAxisRank:
    def test_ranks(self):
        assert _axis_rank("E1") == 0
        assert _axis_rank("E2") == 1
        assert _axis_rank("E5") == 4

    def test_unknown(self):
        assert _axis_rank("??") == 2  # default


# ---------------------------------------------------------------------------
# generate_dual_axis_svg
# ---------------------------------------------------------------------------


class TestDualAxisViz:
    def test_generates_svg(self):
        svg = generate_dual_axis_svg(_sample_topics())
        assert "<svg" in svg
        assert "</svg>" in svg
        assert "circle" in svg

    def test_contains_claim_ids(self):
        svg = generate_dual_axis_svg(_sample_topics())
        assert "c1" in svg
        assert "c2" in svg


# ---------------------------------------------------------------------------
# GuidedReader
# ---------------------------------------------------------------------------


class TestGuidedReader:
    def test_list_paths(self):
        reader = GuidedReader(_sample_topics())
        paths = reader.list_paths()
        assert isinstance(paths, list)

    def test_get_claim_context(self):
        reader = GuidedReader(_sample_topics())
        step = reader.get_claim_context("c1")
        assert step is not None
        assert step.claim_id == "c1"
        assert step.status == "ESTABLISHED"

    def test_get_claim_context_missing(self):
        reader = GuidedReader(_sample_topics())
        assert reader.get_claim_context("nonexistent") is None

    def test_step_to_dict(self):
        reader = GuidedReader(_sample_topics())
        step = reader.get_claim_context("c1")
        d = step.to_dict()
        assert "claim_id" in d
        assert "evidence_axis" in d


# ---------------------------------------------------------------------------
# submit_challenge
# ---------------------------------------------------------------------------


class TestChallengeForm:
    def test_submit_challenge(self, tmp_path):
        import universe_explorer.reader.challenge_form as cf
        old_dir = cf._CHALLENGES_DIR
        cf._CHALLENGES_DIR = tmp_path / "challenges"
        try:
            challenge = submit_challenge(
                claim_id="hawking_radiation",
                challenge_type="verdict",
                argument="The evidence is analog only, not direct.",
            )
            assert challenge["claim_id"] == "hawking_radiation"
            assert challenge["status"] == "pending"
            assert len(list((tmp_path / "challenges").glob("*.json"))) == 1
        finally:
            cf._CHALLENGES_DIR = old_dir


# ---------------------------------------------------------------------------
# Dynamic reading paths
# ---------------------------------------------------------------------------


from universe_explorer.reader.dynamic_paths import (
    DynamicPath,
    generate_dynamic_paths,
    _divergence_paths,
    _evidence_chain_paths,
    _frontier_trail_paths,
)


class TestDynamicPaths:
    def test_generates_paths(self):
        paths = generate_dynamic_paths(_sample_topics())
        assert isinstance(paths, list)

    def test_divergence_paths(self):
        paths = _divergence_paths(_sample_topics())
        assert isinstance(paths, list)

    def test_evidence_chain_paths(self):
        paths = _evidence_chain_paths(_sample_topics())
        assert isinstance(paths, list)

    def test_frontier_trail_paths(self):
        paths = _frontier_trail_paths(_sample_topics())
        assert isinstance(paths, list)

    def test_dynamic_path_to_dict(self):
        p = DynamicPath(
            id="test", title="Test", description="A test path",
            claim_ids=["c1", "c2"], kind="divergence",
        )
        d = p.to_dict()
        assert d["id"] == "test"
        assert len(d["claim_ids"]) == 2
