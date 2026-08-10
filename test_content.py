"""Content validation tests — verify all claims have valid content.

Checks:
  - All claims have valid evidence
  - All sources are accessible
  - All relations are valid
  - All status reasons are complete
"""

from __future__ import annotations

import pytest

from universe_explorer.data.registry import TOPICS
from universe_explorer.model import Claim, Status
from universe_explorer.validator import validate_claim, validate_topic
from universe_explorer.provenance import validate_provenance
from universe_explorer.axes import derive, diverges, EvidenceStrength
from universe_explorer.relations import validate_links


class TestContentValidation:
    """All claims should have valid content."""

    def test_all_topics_pass_validator(self):
        """All topics should pass the constitution validator."""
        for topic in TOPICS:
            violations = validate_topic(topic)
            assert violations == [], \
                f"Topic {topic.id} has violations: {violations}"

    def test_all_topics_pass_provenance(self):
        """All topics should pass provenance checks."""
        for topic in TOPICS:
            violations = validate_provenance(topic)
            assert violations == [], \
                f"Topic {topic.id} has provenance violations: {violations}"

    def test_all_links_valid(self):
        """All relations should be valid."""
        violations = validate_links(TOPICS)
        assert violations == [], f"Link violations: {violations}"

    def test_all_claims_have_evidence(self):
        """All claims should have at least one evidence item."""
        for topic in TOPICS:
            for claim in topic.claims:
                assert len(claim.evidence) > 0, \
                    f"{claim.id} has no evidence"

    def test_all_claims_have_sources(self):
        """All claims should have at least one source."""
        for topic in TOPICS:
            for claim in topic.claims:
                assert len(claim.sources) > 0, \
                    f"{claim.id} has no sources"

    def test_all_claims_have_status_reason(self):
        """All claims should have status_reason."""
        for topic in TOPICS:
            for claim in topic.claims:
                assert len(claim.status_reason) > 0, \
                    f"{claim.id} has no status_reason"

    def test_all_evidence_have_source_ref(self):
        """All evidence items should have source_ref."""
        for topic in TOPICS:
            for claim in topic.claims:
                for ev in claim.evidence:
                    assert ev.source_ref, \
                        f"{claim.id}: evidence missing source_ref"

    def test_all_source_refs_resolve(self):
        """All source_ref should resolve to a source label."""
        for topic in TOPICS:
            for claim in topic.claims:
                source_labels = {s.label for s in claim.sources}
                for ev in claim.evidence:
                    assert ev.source_ref in source_labels, \
                        f"{claim.id}: source_ref {ev.source_ref} not found"

    def test_evidence_types_valid(self):
        """All evidence types should be in controlled vocabulary."""
        from universe_explorer.axes import EVIDENCE_TYPE_VOCAB
        for topic in TOPICS:
            for claim in topic.claims:
                for ev in claim.evidence:
                    assert ev.type in EVIDENCE_TYPE_VOCAB, \
                        f"{claim.id}: invalid evidence type {ev.type}"

    def test_source_kinds_classifiable(self):
        """All source kinds should be classifiable."""
        from universe_explorer.model import tier_of
        for topic in TOPICS:
            for claim in topic.claims:
                for src in claim.sources:
                    tier = tier_of(src.kind)
                    assert tier is not None, \
                        f"{claim.id}: unclassifiable source kind {src.kind}"


class TestContentCompleteness:
    """All claims should be complete."""

    def test_all_domains_covered(self):
        """All 8 domains should be covered."""
        domains = {t.id for t in TOPICS}
        expected = {"black_hole", "cosmology", "dark_matter", "stars",
                    "exoplanets", "planets", "ocean", "seismology"}
        assert domains == expected

    def test_total_claims_91(self):
        """Total claims should be 91."""
        total = sum(len(t.claims) for t in TOPICS)
        assert total == 91

    def test_all_statuses_represented(self):
        """All 5 statuses should be represented."""
        statuses = set()
        for topic in TOPICS:
            for claim in topic.claims:
                statuses.add(claim.status)
        assert len(statuses) == 5

    def test_all_evidence_axes_represented(self):
        """All evidence axes should be represented."""
        axes = set()
        for topic in TOPICS:
            for claim in topic.claims:
                d = derive(claim)
                axes.add(d.strength)
        assert len(axes) >= 3  # At least E1, E2, E3


class TestContentConsistency:
    """Content should be consistent."""

    def test_status_matches_reason(self):
        """Status should match status_reason conditions."""
        for topic in TOPICS:
            for claim in topic.claims:
                if claim.status_reason:
                    # At least one condition should be for the claimed status
                    from universe_explorer.model import STATUS_CONDITIONS
                    spec = STATUS_CONDITIONS.get(claim.status)
                    if spec:
                        allowed = set(spec["conditions"].keys())
                        for ca in claim.status_reason:
                            assert ca.condition in allowed, \
                                f"{claim.id}: condition {ca.condition} not in {claim.status.name}"

    def test_competing_has_models(self):
        """COMPETING status should have competing models."""
        for topic in TOPICS:
            for claim in topic.claims:
                if claim.status == Status.COMPETING:
                    assert len(claim.competing_models) >= 2, \
                        f"{claim.id}: COMPETING but < 2 models"

    def test_no_silent_status_changes(self):
        """Status changes should be documented."""
        for topic in TOPICS:
            for claim in topic.claims:
                if claim.status_history:
                    for change in claim.status_history:
                        assert change.from_status, f"{claim.id}: missing from_status"
                        assert change.to_status, f"{claim.id}: missing to_status"
