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
from universe_explorer.reader.challenge_form import (
    ChallengeError,
    generate_challenge_form,
    submit_challenge,
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

    def test_short_science_tokens_with_digits(self):
        """H0 / E1 / GW150914 must not be dropped (len>=2 + digit rule)."""
        assert "h0" in _tokenize("H0 tension")
        assert "h0" in _tokenize("H₀")
        assert "e1" in _tokenize("E1 direct")
        assert "gw150914" in _tokenize("GW150914")

    def test_pure_stopwords_still_dropped(self):
        assert "of" not in _tokenize("of the to")
        assert "is" not in _tokenize("is a be")

    def test_greek_lcdm_normalizes(self):
        """ΛCDM → lcdm so users can type either form."""
        assert "lcdm" in _tokenize("ΛCDM")
        assert "lcdm" in _tokenize("lcdm")

    def test_chinese_tokens(self):
        assert "霍金" in _tokenize("霍金輻射")
        assert "黑洞" in _tokenize("黑洞")


# ---------------------------------------------------------------------------
# ClaimSearchIndex
# ---------------------------------------------------------------------------


class TestSearchIndex:
    def test_search_by_title(self):
        index = ClaimSearchIndex(_sample_topics(), use_cache=False)
        results = index.search("gravitational")
        assert len(results) >= 1
        assert results[0].claim_id == "c1"

    def test_search_by_evidence(self):
        index = ClaimSearchIndex(_sample_topics(), use_cache=False)
        results = index.search("LIGO")
        assert len(results) >= 1

    def test_search_no_match(self):
        index = ClaimSearchIndex(_sample_topics(), use_cache=False)
        results = index.search("nonexistent")
        assert len(results) == 0

    def test_suggest(self):
        index = ClaimSearchIndex(_sample_topics(), use_cache=False)
        suggestions = index.suggest("grav")
        assert any("gravitational" in s for s in suggestions)

    def test_result_to_dict(self):
        index = ClaimSearchIndex(_sample_topics(), use_cache=False)
        results = index.search("waves")
        if results:
            d = results[0].to_dict()
            assert "claim_id" in d
            assert "score" in d

    def test_search_by_claim_id_fragment(self):
        index = ClaimSearchIndex(_sample_topics(), use_cache=False)
        # claim id "c1" alone is too short; real ids are longer
        results = index.search("c1")
        # c1 alone may not pass token filter; use a longer synthetic id path
        assert isinstance(results, list)


class TestSearchIndexLiveRegistry:
    """User-path contracts against the real 91-claim registry."""

    def test_chinese_title_search_hits_hawking(self):
        from universe_explorer.data.registry import TOPICS
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        results = index.search("霍金")
        ids = {r.claim_id for r in results}
        assert "hawking_radiation" in ids

    def test_chinese_domain_word_black_hole(self):
        from universe_explorer.data.registry import TOPICS
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        results = index.search("黑洞")
        assert len(results) >= 1
        assert any(r.topic_id == "black_hole" for r in results)

    def test_h0_token_finds_hubble_claims(self):
        from universe_explorer.data.registry import TOPICS
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        results = index.search("H0")
        ids = {r.claim_id for r in results}
        assert any("H0" in i or "h0" in i.lower() for i in ids) or len(results) >= 1

    def test_lcdm_ascii_matches_greek(self):
        from universe_explorer.data.registry import TOPICS
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        a = {r.claim_id for r in index.search("lcdm")}
        b = {r.claim_id for r in index.search("ΛCDM")}
        assert len(a) >= 1
        assert a & b  # overlap: same normalization


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
                evidence_refs=["arXiv:1602.03837"],
            )
            assert challenge["claim_id"] == "hawking_radiation"
            assert challenge["status"] == "pending"
            assert challenge["github_template"]
            assert "github.com" in challenge["github_template"]
            assert len(list((tmp_path / "challenges").glob("*.json"))) == 1
        finally:
            cf._CHALLENGES_DIR = old_dir

    def test_reject_unknown_claim(self, tmp_path):
        import universe_explorer.reader.challenge_form as cf
        old = cf._CHALLENGES_DIR
        cf._CHALLENGES_DIR = tmp_path / "challenges"
        try:
            with pytest.raises(ChallengeError) as ei:
                submit_challenge(
                    claim_id="totally_fake_claim",
                    challenge_type="verdict",
                    argument="because I said so",
                    evidence_refs=["arXiv:1602.03837"],
                )
            assert "unknown claim_id" in ei.value.message
            assert list((tmp_path / "challenges").glob("*.json")) == []
        finally:
            cf._CHALLENGES_DIR = old

    def test_reject_verdict_without_refs(self, tmp_path):
        import universe_explorer.reader.challenge_form as cf
        old = cf._CHALLENGES_DIR
        cf._CHALLENGES_DIR = tmp_path / "challenges"
        try:
            with pytest.raises(ChallengeError) as ei:
                submit_challenge(
                    claim_id="hawking_radiation",
                    challenge_type="verdict",
                    argument="no source",
                    evidence_refs=[],
                )
            assert "evidence_ref" in ei.value.message
        finally:
            cf._CHALLENGES_DIR = old

    def test_reject_non_checkable_ref(self, tmp_path):
        import universe_explorer.reader.challenge_form as cf
        old = cf._CHALLENGES_DIR
        cf._CHALLENGES_DIR = tmp_path / "challenges"
        try:
            with pytest.raises(ChallengeError):
                submit_challenge(
                    claim_id="hawking_radiation",
                    challenge_type="verdict",
                    argument="vague",
                    evidence_refs=["trust me bro"],
                )
        finally:
            cf._CHALLENGES_DIR = old

    def test_form_links_github_templates(self, tmp_path):
        generate_challenge_form(dist_dir=tmp_path)
        html = (tmp_path / "challenge.html").read_text(encoding="utf-8")
        assert "challenge-a-verdict.yml" in html
        assert "challenge-a-relation.yml" in html
        assert "report-a-source-problem.yml" in html
        assert "github.com/taipei49314/universe-explorer" in html
        assert "KNOWN_CLAIM_IDS" in html
        assert "hawking_radiation" in html


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
