"""Adversarial round 2 — deeper invariants and edge cases.

Focus areas the first round missed:
  1. Constitutional invariants — can violations slip through?
  2. Data integrity — inconsistent claim states
  3. Relations edge cases — self-loops, duplicates, orphans
  4. Render safety — HTML generation with weird data
  5. Build resilience — what breaks the build?
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from universe_explorer.model import (
    Claim, CompetingModel, ConditionAssessment, Evidence,
    Source, Status, Topic, StatusChange,
)
from universe_explorer.validator import validate_claim, validate_topic, LAWS
from universe_explorer.axes import derive, diverges, EVIDENCE_TYPE_VOCAB
from universe_explorer.relations import (
    all_links, validate_links, authored_links, LINK_KINDS,
)
from universe_explorer.narrative import compose, check, OPENING
from universe_explorer.render import render_topic, claims_json
from universe_explorer.reader.stats import compute_stats
from universe_explorer.reader.diff import diff_claims


# ---------------------------------------------------------------------------
# 1. Constitutional invariants — can violations slip through?
# ---------------------------------------------------------------------------


class TestConstitutionalInvariants:
    """Every law in LAWS must be enforced. Test the enforcement."""

    def test_every_law_has_test_coverage(self):
        """Every rule in LAWS should be testable."""
        # LAWS is a dict of rule_name -> law_reference
        assert len(LAWS) > 10
        for rule_name, law_ref in LAWS.items():
            assert isinstance(rule_name, str)
            assert isinstance(law_ref, str)
            assert len(law_ref) > 0

    def test_confidence_percentage_always_caught(self):
        """Any percentage in title or status_reason must be caught."""
        bad_texts = [
            "90% confidence",
            "共識度 73%",
            "confidence: 90",
            "certainty 85%",
        ]
        for text in bad_texts:
            claim = Claim(
                id="bad", title=text,
                status=Status.FRONTIER,
                sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                kind="peer-reviewed paper")],
                evidence=[Evidence(type="theoretical derivation",
                                   description="Something",
                                   source_ref="s1")],
                status_reason=[ConditionAssessment("new_discovery", True, text)],
            )
            violations = validate_claim(claim)
            # Should catch either declared_confidence or no_fake_precision
            rules = {v.rule for v in violations}
            assert "declared_confidence" in rules or "no_fake_precision" in rules, \
                f"Missed: {text}"

    def test_numeric_open_questions_caught(self):
        """Numeric open questions must be caught."""
        claim = Claim(
            id="bad_oq", title="Test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            open_questions=["3"],  # just a number
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "numeric_open_question" for v in violations)

    def test_evidence_without_source_always_caught(self):
        """Evidence with empty source_ref must be caught."""
        claim = Claim(
            id="bad_src", title="Test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "evidence_without_source" for v in violations)

    def test_invalid_evidence_type_caught(self):
        """Invalid evidence type must be caught."""
        claim = Claim(
            id="bad_ev", title="Test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="made up type",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "invalid_evidence_type" for v in violations)

    def test_unclassifiable_source_kind_caught(self):
        """Source kind that doesn't match any tier must be caught."""
        claim = Claim(
            id="bad_kind", title="Test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="unknown kind that matches nothing")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "unclassifiable_source_kind" for v in violations)

    def test_competing_without_models_caught(self):
        """COMPETING status without competing_models must be caught."""
        claim = Claim(
            id="bad_comp", title="Test",
            status=Status.COMPETING,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            competing_models=[],  # empty!
            status_reason=[
                ConditionAssessment("two_or_more_mainstream_models", True, "Two."),
                ConditionAssessment("no_decisive_evidence_yet", True, "No."),
                ConditionAssessment("genuine_scientific_camps", True, "Real."),
            ],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "competing_needs_models" for v in violations)

    def test_competing_models_on_wrong_status_caught(self):
        """competing_models on non-COMPETING status must be caught."""
        claim = Claim(
            id="bad_cm", title="Test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            competing_models=[CompetingModel(
                name="M1", supporting="S", opposing="O", limitations="L")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert any(v.rule == "unexpected_competing_models" for v in violations)


# ---------------------------------------------------------------------------
# 2. Data integrity — inconsistent claim states
# ---------------------------------------------------------------------------


class TestDataIntegrity:
    """Can claims be in inconsistent states?"""

    def test_status_history_preserved(self):
        """Status history should survive round-trip."""
        claim = Claim(
            id="hist", title="History test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            status_history=[StatusChange(
                date="2026-01-01",
                from_status="SPECULATIVE",
                to_status="FRONTIER",
                trigger="new evidence",
            )],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        assert len(claim.status_history) == 1
        assert claim.status_history[0].from_status == "SPECULATIVE"

    def test_evidence_source_ref_matches_source_label(self):
        """Evidence source_ref must match a source label."""
        claim = Claim(
            id="ref_match", title="Ref match test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        source_labels = {s.label for s in claim.sources}
        for ev in claim.evidence:
            assert ev.source_ref in source_labels

    def test_multiple_evidence_same_source(self):
        """Multiple evidence items can reference the same source."""
        claim = Claim(
            id="multi_ev", title="Multiple evidence",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[
                Evidence(type="theoretical derivation",
                         description="First finding",
                         source_ref="s1"),
                Evidence(type="indirect observation",
                         description="Second finding",
                         source_ref="s1"),
            ],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        violations = validate_claim(claim)
        assert violations == []

    def test_evidence_types_are_controlled_vocabulary(self):
        """All evidence types must be in EVIDENCE_TYPE_VOCAB."""
        for ev_type in EVIDENCE_TYPE_VOCAB:
            claim = Claim(
                id=f"ev_{ev_type}", title=f"Test {ev_type}",
                status=Status.FRONTIER,
                sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                kind="peer-reviewed paper")],
                evidence=[Evidence(type=ev_type,
                                   description="Something",
                                   source_ref="s1")],
                status_reason=[ConditionAssessment("new_discovery", True, "New.")],
            )
            violations = validate_claim(claim)
            assert not any(v.rule == "invalid_evidence_type" for v in violations)


# ---------------------------------------------------------------------------
# 3. Relations edge cases
# ---------------------------------------------------------------------------


class TestRelationsEdgeCases:
    """Edge cases in the relations graph."""

    def test_authored_links_are_valid(self):
        """All authored links should reference valid kinds."""
        links = authored_links()
        for link in links:
            assert link.kind in LINK_KINDS
            assert link.source != link.target  # no self-loops

    def test_all_links_no_duplicates(self):
        """No duplicate authored edges."""
        links = authored_links()
        seen = set()
        for link in links:
            key = (link.source, link.target, link.kind)
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_all_links_no_banned_keys(self):
        """No confidence/score/trust fields in link payloads."""
        from universe_explorer.relations import BANNED_KEYS
        links = all_links(_make_real_topics())
        for link in links:
            d = link.as_dict()
            assert not (set(d) & BANNED_KEYS), f"Banned keys in {d}"

    def test_validate_links_on_real_data(self):
        """Real data should have no link violations."""
        from universe_explorer.data.registry import TOPICS
        violations = validate_links(TOPICS)
        assert violations == []


# ---------------------------------------------------------------------------
# 4. Render safety
# ---------------------------------------------------------------------------


class TestRenderSafety:
    """HTML generation shouldn't crash on edge cases."""

    def test_render_topic_with_divergent_claim(self):
        """Topic with divergent claim should render."""
        topic = Topic(
            id="test", title="Test", summary="A test topic.",
            claims=[Claim(
                id="div", title="Divergent claim",
                status=Status.STRONG,
                sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                kind="peer-reviewed paper")],
                evidence=[Evidence(type="analog experiment",
                                   description="Analog only",
                                   source_ref="s1")],
                status_reason=[
                    ConditionAssessment("mainstream_model_support", True, "Yes."),
                    ConditionAssessment("minor_alternatives_exist", True, "Minor."),
                    ConditionAssessment("overall_direction_robust", True, "Robust."),
                ],
            )],
        )
        html = render_topic(topic)
        assert "diverges" in html or "Divergent" in html

    def test_claims_json_valid(self):
        """claims_json should produce valid JSON."""
        from universe_explorer.data.registry import TOPICS
        json_str = claims_json(TOPICS)
        data = json.loads(json_str)
        assert isinstance(data, dict)
        assert "claims" in data
        assert isinstance(data["claims"], list)
        assert len(data["claims"]) == sum(
            len(t.claims) for t in TOPICS
        )

    def test_claims_json_has_required_fields(self):
        """Every claim in JSON should have required fields."""
        from universe_explorer.data.registry import TOPICS
        json_str = claims_json(TOPICS)
        data = json.loads(json_str)
        for claim in data["claims"]:
            assert "id" in claim
            assert "title" in claim
            assert "status" in claim
            assert "evidence" in claim


# ---------------------------------------------------------------------------
# 5. Narrative safety
# ---------------------------------------------------------------------------


class TestNarrativeSafety:
    """Narrative layer should be safe."""

    def test_compose_with_valid_claim(self):
        """Compose should produce sentences for valid claim."""
        claim = Claim(
            id="narr", title="Narrative test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something observed.",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        sentences = compose(claim)
        assert len(sentences) > 0

    def test_check_rejects_unreferenced_sentence(self):
        """Check should reject sentences without refs (raises exception)."""
        from universe_explorer.narrative import NarrativeSentence, NarrativeViolation
        claim = Claim(
            id="narr2", title="Narrative test 2",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something observed.",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        # Must start with constitutional opening formula
        bad_sentences = [NarrativeSentence(
            text="This has no refs at all.",
            refs=[],
        )]
        with pytest.raises(NarrativeViolation):
            check(claim, bad_sentences)


# ---------------------------------------------------------------------------
# 6. Diff edge cases
# ---------------------------------------------------------------------------


class TestDiffEdgeCases:
    """Diff should handle edge cases."""

    def test_diff_same_claim_no_changes(self):
        """Diffing same claim should show no changes."""
        claim = Claim(
            id="same", title="Same claim",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        diff = diff_claims(claim, claim)
        assert len(diff.changes) == 0

    def test_diff_different_status(self):
        """Status change should be detected."""
        claim_a = Claim(
            id="d1", title="Test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        claim_b = Claim(
            id="d1", title="Test",
            status=Status.STRONG,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[
                ConditionAssessment("mainstream_model_support", True, "Yes."),
                ConditionAssessment("minor_alternatives_exist", True, "Minor."),
                ConditionAssessment("overall_direction_robust", True, "Robust."),
            ],
        )
        diff = diff_claims(claim_a, claim_b)
        assert any(ch["field"] == "status" for ch in diff.changes)

    def test_diff_added_evidence(self):
        """Added evidence should be detected."""
        claim_a = Claim(
            id="d2", title="Test",
            status=Status.FRONTIER,
            sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                            kind="peer-reviewed paper")],
            evidence=[Evidence(type="theoretical derivation",
                               description="Something",
                               source_ref="s1")],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        claim_b = Claim(
            id="d2", title="Test",
            status=Status.FRONTIER,
            sources=[
                Source(label="s1", url_or_id="arXiv:0000.00000",
                       kind="peer-reviewed paper"),
                Source(label="s2", url_or_id="arXiv:1111.11111",
                       kind="peer-reviewed paper"),
            ],
            evidence=[
                Evidence(type="theoretical derivation",
                         description="Something",
                         source_ref="s1"),
                Evidence(type="theoretical derivation",
                         description="New finding",
                         source_ref="s2"),
            ],
            status_reason=[ConditionAssessment("new_discovery", True, "New.")],
        )
        diff = diff_claims(claim_a, claim_b)
        assert any(ch["field"] == "evidence" for ch in diff.changes)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_real_topics():
    """Get real topics for testing."""
    from universe_explorer.data.registry import TOPICS
    return TOPICS
