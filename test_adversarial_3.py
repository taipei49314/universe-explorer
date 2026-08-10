"""Adversarial round 3 — watch, discovery pipeline, cache invalidation.

Focus areas:
  1. Watch/events — change detection correctness
  2. Discovery pipeline — end-to-end with mocked adapter
  3. Search index cache — invalidation and consistency
  4. Annotation persistence — survives round-trips
  5. Review workflow — full lifecycle
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from universe_explorer.model import (
    Claim, Evidence, Source, Status, Topic, ConditionAssessment,
)
from universe_explorer.watch import (
    current_state, diff_events, emit_events, SNAPSHOT_PATH,
)
from universe_explorer.discovery.adapters.base import (
    RawResult, FetchedRecord, EvidenceItem, SourceAdapter,
)
from universe_explorer.discovery.candidate_builder import build_candidate
from universe_explorer.discovery.precheck import precheck
from universe_explorer.reader.search_index import ClaimSearchIndex
from universe_explorer.reader.annotate import ClaimAnnotations
from universe_explorer.reader.review import ReviewManager


# ---------------------------------------------------------------------------
# 1. Watch/events — change detection
# ---------------------------------------------------------------------------


class TestWatchEvents:
    """Change detection should be correct."""

    def test_current_state_captures_claim_state(self):
        """current_state should capture all claim fields."""
        topic = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="Test",
                  status=Status.FRONTIER,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="Something",
                                     source_ref="s1")],
                  status_reason=[ConditionAssessment("new_discovery", True, "New.")]),
        ])
        state = current_state(topic)
        assert "c1" in state
        assert state["c1"]["status"] == "FRONTIER"
        assert "evidence_axis" in state["c1"]

    def test_diff_detects_status_change(self):
        """Diff should detect status changes."""
        snapshot = {"c1": {"status": "FRONTIER", "evidence_axis": "E2",
                           "evidence_items": 1, "sources": 1,
                           "diverges": False, "derivation": []}}
        now = {"c1": {"status": "STRONG", "evidence_axis": "E2",
                      "evidence_items": 1, "sources": 1,
                      "diverges": False, "derivation": []}}
        events = diff_events(snapshot, now)
        assert len(events) == 1
        assert events[0]["kind"] == "status_changed"

    def test_diff_detects_evidence_change(self):
        """Diff should detect evidence changes."""
        snapshot = {"c1": {"status": "FRONTIER", "evidence_axis": "E2",
                           "evidence_items": 1, "sources": 1,
                           "diverges": False, "derivation": []}}
        now = {"c1": {"status": "FRONTIER", "evidence_axis": "E1",
                      "evidence_items": 2, "sources": 2,
                      "diverges": False, "derivation": []}}
        events = diff_events(snapshot, now)
        assert len(events) >= 1

    def test_diff_no_change_no_events(self):
        """No change should produce no events."""
        state = {"c1": {"status": "FRONTIER", "evidence_axis": "E2",
                        "evidence_items": 1, "sources": 1,
                        "diverges": False, "derivation": []}}
        events = diff_events(state, state)
        assert len(events) == 0


# ---------------------------------------------------------------------------
# 2. Discovery pipeline — mocked adapter
# ---------------------------------------------------------------------------


class TestDiscoveryPipeline:
    """Discovery pipeline with mocked adapter."""

    def _mock_adapter(self) -> SourceAdapter:
        adapter = MagicMock(spec=SourceAdapter)
        adapter.name = "mock"
        adapter.source_ref_prefix = "arXiv:"
        adapter.can_handle.return_value = True

        record = FetchedRecord(
            source_ref="arXiv:2311.08680",
            cache_path="/tmp/mock.xml",
            sha256="mockhash",
            endpoint="https://arxiv.org/api/query",
            retrieved_at="2023-01-01T00:00:00Z",
            title="Mock Paper",
            authors=["Mock Author"],
        )
        adapter.fetch.return_value = record
        adapter.extract_evidence.return_value = [
            EvidenceItem(
                type="theoretical result",
                description="Mock evidence description.",
                source_ref="arXiv-2311-08680",
            )
        ]
        return adapter

    def test_build_candidate_structure(self, tmp_path):
        """Candidate should have correct structure."""
        import universe_explorer.discovery.candidate_builder as cb
        old_dir = cb.CANDIDATES_DIR
        cb.CANDIDATES_DIR = tmp_path / "candidates"
        try:
            adapter = self._mock_adapter()
            candidate = build_candidate(
                topic_id="t", claim_id="c1",
                adapter=adapter, source_refs=["arXiv:2311.08680"],
                title="Test Claim",
            )
            assert candidate["id"] == "c1"
            assert candidate["topic_id"] == "t"
            assert candidate["status"] is None
            assert len(candidate["sources"]) == 1
            assert len(candidate["evidence"]) == 1
            assert "_discovery" in candidate
        finally:
            cb.CANDIDATES_DIR = old_dir

    def test_precheck_catches_violations(self):
        """Precheck should catch constitution violations."""
        candidate = {
            "id": "bad", "topic_id": "t", "title": "Bad claim",
            "status": None, "status_reason": [],
            "evidence": [{"type": "direct observation",
                          "description": "Something",
                          "source_ref": "nonexistent"}],
            "sources": [], "open_questions": [],
        }
        report = precheck(candidate)
        assert not report.pass_constitution
        assert len(report.violations) > 0

    def test_precheck_passes_valid_candidate(self):
        """Precheck should pass valid candidate."""
        candidate = {
            "id": "good", "topic_id": "t", "title": "Good claim",
            "status": "FRONTIER", "status_reason": [
                {"condition": "new_discovery", "holds": True, "note": "New."}
            ],
            "evidence": [{"type": "direct observation",
                          "description": "Something",
                          "source_ref": "s1"}],
            "sources": [{"label": "s1", "url_or_id": "arXiv:0000.00000",
                         "kind": "preprint (arXiv)"}],
            "open_questions": [],
        }
        report = precheck(candidate)
        assert report.pass_constitution


# ---------------------------------------------------------------------------
# 3. Search index cache — invalidation
# ---------------------------------------------------------------------------


class TestSearchIndexCache:
    """Cache invalidation should work correctly."""

    def test_cache_key_changes_with_claims(self):
        """Cache key should change when claims change."""
        topic1 = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="Claim 1",
                  status=Status.FRONTIER,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="Something",
                                     source_ref="s1")]),
        ])
        topic2 = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="Claim 1",
                  status=Status.FRONTIER,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="Something",
                                     source_ref="s1")]),
            Claim(id="c2", title="Claim 2",
                  status=Status.FRONTIER,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="Something",
                                     source_ref="s1")]),
        ])
        index1 = ClaimSearchIndex([topic1], use_cache=False)
        index2 = ClaimSearchIndex([topic2], use_cache=False)
        # Different claims should produce different cache keys
        key1 = index1._cache_key([topic1])
        key2 = index2._cache_key([topic2])
        assert key1 != key2

    def test_fresh_index_has_results(self):
        """Fresh index should have results."""
        topic = Topic(id="t", title="T", summary="", claims=[
            Claim(id="c1", title="Gravitational waves",
                  status=Status.FRONTIER,
                  sources=[Source(label="s1", url_or_id="arXiv:0000.00000",
                                  kind="preprint (arXiv)")],
                  evidence=[Evidence(type="direct observation",
                                     description="LIGO detection",
                                     source_ref="s1")]),
        ])
        index = ClaimSearchIndex([topic], use_cache=False)
        results = index.search("gravitational")
        assert len(results) >= 1


# ---------------------------------------------------------------------------
# 4. Annotation persistence
# ---------------------------------------------------------------------------


class TestAnnotationPersistence:
    """Annotations should survive round-trips."""

    def test_tags_persist(self, tmp_path):
        """Tags should persist across manager instances."""
        dir_path = tmp_path / "ann"
        mgr1 = ClaimAnnotations(dir_path)
        mgr1.add_tag("c1", "needs-review")
        mgr1.add_tag("c1", "high-priority")

        mgr2 = ClaimAnnotations(dir_path)
        tags = mgr2.get_tags("c1")
        assert "needs-review" in tags
        assert "high-priority" in tags

    def test_notes_persist(self, tmp_path):
        """Notes should persist across manager instances."""
        dir_path = tmp_path / "ann"
        mgr1 = ClaimAnnotations(dir_path)
        mgr1.add_note("c1", "This needs more evidence.")

        mgr2 = ClaimAnnotations(dir_path)
        notes = mgr2.get_notes("c1")
        assert len(notes) == 1
        assert "evidence" in notes[0]["value"]

    def test_labels_persist(self, tmp_path):
        """Labels should persist across manager instances."""
        dir_path = tmp_path / "ann"
        mgr1 = ClaimAnnotations(dir_path)
        mgr1.add_label("c1", "high-priority")

        mgr2 = ClaimAnnotations(dir_path)
        labels = mgr2.get_labels("c1")
        assert "high-priority" in labels

    def test_remove_tag_persists(self, tmp_path):
        """Tag removal should persist."""
        dir_path = tmp_path / "ann"
        mgr1 = ClaimAnnotations(dir_path)
        mgr1.add_tag("c1", "temp")
        mgr1.remove_tag("c1", "temp")

        mgr2 = ClaimAnnotations(dir_path)
        assert not mgr2.has_tag("c1", "temp")


# ---------------------------------------------------------------------------
# 5. Review workflow — full lifecycle
# ---------------------------------------------------------------------------


class TestReviewLifecycle:
    """Full review lifecycle should work."""

    def test_full_lifecycle(self, tmp_path):
        """Start → check → approve should work."""
        mgr = ReviewManager(tmp_path / "reviews")

        # Start review.
        review = mgr.start_review("c1")
        assert review.status == "in-progress"

        # Check all required items.
        for item in review.items:
            if item.required:
                mgr.check_item("c1", item.id, f"Checked {item.label}")

        # Add comment.
        mgr.add_comment("c1", "Looks good overall.")

        # Approve.
        assert mgr.approve("c1", "Approved after review")
        review = mgr.get_review("c1")
        assert review.status == "approved"
        assert review.completed_at != ""

    def test_reject_lifecycle(self, tmp_path):
        """Start → reject should work."""
        mgr = ReviewManager(tmp_path / "reviews")

        # Start review.
        review = mgr.start_review("c1")
        assert review.status == "in-progress"

        # Reject.
        assert mgr.reject("c1", "Missing sources")
        review = mgr.get_review("c1")
        assert review.status == "rejected"

    def test_multiple_reviews_independent(self, tmp_path):
        """Multiple reviews should be independent."""
        mgr = ReviewManager(tmp_path / "reviews")

        mgr.start_review("c1")
        mgr.start_review("c2")
        mgr.check_item("c1", "sources")

        review1 = mgr.get_review("c1")
        review2 = mgr.get_review("c2")

        # c1 should have sources checked, c2 should not.
        sources1 = [i for i in review1.items if i.id == "sources"][0]
        sources2 = [i for i in review2.items if i.id == "sources"][0]
        assert sources1.checked
        assert not sources2.checked
