"""Tests for stats, export, diff, annotate, review, batch modules."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from universe_explorer.model import (
    Claim, CompetingModel, ConditionAssessment, Evidence,
    Source, Status, Topic,
)
from universe_explorer.reader.stats import compute_stats, format_stats_report
from universe_explorer.reader.export import export_claims, export_stats
from universe_explorer.reader.filter_engine import FilterCriteria
from universe_explorer.reader.diff import diff_claims, ClaimDiff
from universe_explorer.reader.annotate import ClaimAnnotations, Annotation
from universe_explorer.reader.review import ReviewManager, Review, CHECKLISTS
from universe_explorer.reader.batch import batch_summary


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_topics():
    src1 = Source(label="s1", url_or_id="arXiv:1111.11111",
                  kind="preprint (arXiv)")
    src2 = Source(label="s2", url_or_id="arXiv:2222.22222",
                  kind="peer-reviewed paper")
    c1 = Claim(
        id="c1", title="Gravitational waves detected",
        status=Status.ESTABLISHED,
        sources=[src1],
        evidence=[Evidence(type="direct observation",
                           description="LIGO detection",
                           source_ref="s1")],
        open_questions=["Mass distribution?"],
    )
    c2 = Claim(
        id="c2", title="Dark matter candidates",
        status=Status.COMPETING,
        sources=[src2],
        evidence=[Evidence(type="theoretical result",
                           description="WIMP model",
                           source_ref="s2")],
        competing_models=[
            CompetingModel(name="WIMP", supporting="detection rates",
                           opposing="no signal", limitations="mass range"),
            CompetingModel(name="Axion", supporting="theoretical motivation",
                           opposing="no detection", limitations="coupling"),
        ],
        open_questions=[],
    )
    return [
        Topic(id="cosmology", title="Cosmology", summary="", claims=[c1]),
        Topic(id="dark_matter", title="Dark Matter", summary="", claims=[c2]),
    ]


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_compute_stats(self):
        stats = compute_stats(_make_topics())
        assert stats.total_topics == 2
        assert stats.total_claims == 2
        assert stats.total_evidence == 2
        assert stats.total_sources == 2

    def test_claims_by_domain(self):
        stats = compute_stats(_make_topics())
        assert stats.claims_by_domain["cosmology"] == 1
        assert stats.claims_by_domain["dark_matter"] == 1

    def test_claims_by_status(self):
        stats = compute_stats(_make_topics())
        assert stats.claims_by_status["ESTABLISHED"] == 1
        assert stats.claims_by_status["COMPETING"] == 1

    def test_competing_count(self):
        stats = compute_stats(_make_topics())
        assert stats.competing_count == 1

    def test_to_dict(self):
        stats = compute_stats(_make_topics())
        d = stats.to_dict()
        assert "counts" in d
        assert "distribution" in d
        assert "quality" in d

    def test_format_report(self):
        stats = compute_stats(_make_topics())
        report = format_stats_report(stats)
        assert "Claims: 2" in report


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


class TestExport:
    def test_export_json(self):
        output = export_claims(_make_topics(), "json")
        data = json.loads(output)
        assert len(data) == 2

    def test_export_csv(self):
        output = export_claims(_make_topics(), "csv")
        lines = output.strip().split("\n")
        assert len(lines) == 3  # header + 2 rows

    def test_export_markdown(self):
        output = export_claims(_make_topics(), "markdown")
        assert "| Status |" in output
        assert "2 claims exported" in output

    def test_export_with_filter(self):
        output = export_claims(
            _make_topics(), "json",
            FilterCriteria(domain="cosmology"),
        )
        data = json.loads(output)
        assert len(data) == 1

    def test_export_stats_json(self):
        output = export_stats(_make_topics(), "json")
        data = json.loads(output)
        assert "counts" in data

    def test_export_stats_markdown(self):
        output = export_stats(_make_topics(), "markdown")
        assert "# Knowledge Base Statistics" in output


# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------


class TestDiff:
    def test_no_changes(self):
        topics = _make_topics()
        claim = topics[0].claims[0]
        diff = diff_claims(claim, claim)
        assert len(diff.changes) == 0

    def test_status_change(self):
        topics = _make_topics()
        c1 = topics[0].claims[0]
        c2 = Claim(
            id="c1", title="Gravitational waves detected",
            status=Status.STRONG,
            sources=c1.sources,
            evidence=c1.evidence,
        )
        diff = diff_claims(c1, c2)
        assert any(ch["field"] == "status" for ch in diff.changes)

    def test_evidence_change(self):
        topics = _make_topics()
        c1 = topics[0].claims[0]
        c2 = Claim(
            id="c1", title="Gravitational waves detected",
            status=Status.ESTABLISHED,
            sources=c1.sources,
            evidence=c1.evidence + [
                Evidence(type="direct observation",
                         description="New detection",
                         source_ref="s2"),
            ],
        )
        diff = diff_claims(c1, c2)
        assert any(ch["field"] == "evidence" for ch in diff.changes)

    def test_diff_format(self):
        topics = _make_topics()
        c1 = topics[0].claims[0]
        diff = diff_claims(c1, c1)
        assert "No changes" in diff.format()

    def test_diff_to_dict(self):
        topics = _make_topics()
        c1 = topics[0].claims[0]
        diff = diff_claims(c1, c1)
        d = diff.to_dict()
        assert "claim_id" in d
        assert d["has_changes"] is False


# ---------------------------------------------------------------------------
# Annotate
# ---------------------------------------------------------------------------


class TestAnnotate:
    def test_add_tag(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        ann = mgr.add_tag("c1", "needs-review")
        assert ann.kind == "tag"
        assert ann.value == "needs-review"

    def test_get_tags(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        mgr.add_tag("c1", "tag1")
        mgr.add_tag("c1", "tag2")
        tags = mgr.get_tags("c1")
        assert "tag1" in tags
        assert "tag2" in tags

    def test_has_tag(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        mgr.add_tag("c1", "important")
        assert mgr.has_tag("c1", "important")
        assert not mgr.has_tag("c1", "other")

    def test_remove_tag(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        mgr.add_tag("c1", "temp")
        assert mgr.remove_tag("c1", "temp")
        assert not mgr.has_tag("c1", "temp")

    def test_add_note(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        ann = mgr.add_note("c1", "Review this claim")
        assert ann.kind == "note"
        notes = mgr.get_notes("c1")
        assert len(notes) == 1

    def test_add_label(self, tmp_path):
        mgr = ClaimAnnotations(tmp_path / "ann")
        mgr.add_label("c1", "high-priority")
        labels = mgr.get_labels("c1")
        assert "high-priority" in labels


# ---------------------------------------------------------------------------
# Review
# ---------------------------------------------------------------------------


class TestReview:
    def test_start_review(self, tmp_path):
        mgr = ReviewManager(tmp_path / "reviews")
        review = mgr.start_review("c1")
        assert review.status == "in-progress"
        assert len(review.items) > 0

    def test_check_item(self, tmp_path):
        mgr = ReviewManager(tmp_path / "reviews")
        mgr.start_review("c1")
        assert mgr.check_item("c1", "sources")
        review = mgr.get_review("c1")
        sources_item = [i for i in review.items if i.id == "sources"][0]
        assert sources_item.checked

    def test_approve_requires_all_required(self, tmp_path):
        mgr = ReviewManager(tmp_path / "reviews")
        mgr.start_review("c1")
        # Can't approve yet — required items not checked.
        assert not mgr.approve("c1")
        # Check all required items.
        for item in mgr.get_review("c1").items:
            if item.required:
                mgr.check_item("c1", item.id)
        assert mgr.approve("c1")
        assert mgr.get_review("c1").status == "approved"

    def test_reject(self, tmp_path):
        mgr = ReviewManager(tmp_path / "reviews")
        mgr.start_review("c1")
        assert mgr.reject("c1", "Missing sources")
        assert mgr.get_review("c1").status == "rejected"

    def test_checklist_types(self):
        assert "default" in CHECKLISTS
        assert "new_claim" in CHECKLISTS
        assert "status_change" in CHECKLISTS


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------


class TestBatch:
    def test_batch_summary(self):
        summary = batch_summary(_make_topics())
        assert summary["claims"] == 2
        assert summary["domains"] == 2
        assert "annotations" in summary
        assert "reviews" in summary
