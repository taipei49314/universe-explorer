"""Amendment #12 — Round-4 closures (editorial surface, anti-forgery, precheck, id merge)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from universe_explorer.axes import derive
from universe_explorer.discovery.precheck import _dict_to_claim, precheck
from universe_explorer.editorial import ledger_row
from universe_explorer.model import (
    STATUS_CONDITIONS,
    Claim,
    ConditionAssessment,
    Evidence,
    ReviewState,
    Source,
    Status,
)
from universe_explorer.narrative import check, compose
from universe_explorer.provenance import paper_id_of, reload_paper_aliases
from universe_explorer.render import app_data_json, claims_json, render_topic
from universe_explorer.validator import validate_claim


def _ca(cond: str, note: str = "well-documented multi-group confirmation note"):
    return ConditionAssessment(condition=cond, holds=True, note=note)


def _speculative() -> Claim:
    return Claim(
        id="poc_spec",
        title="speculative placeholder title",
        status=Status.SPECULATIVE,
        sources=[Source("s", "tb", "textbook")],
        evidence=[Evidence("theoretical derivation", "derivation note", "s")],
        status_reason=[
            ConditionAssessment("pure_theoretical_derivation", True, "pure theory only")
        ],
    )


def test_claims_json_exports_review_state():
    from universe_explorer.data.registry import TOPICS

    data = json.loads(claims_json(TOPICS))
    assert data["claims"], "export empty"
    for row in data["claims"]:
        assert "review_state" in row
        assert row["review_state"] in {
            "unverified", "human_verified", "challenged",
        }
        assert "verified_by" in row
        assert "verified_at" in row
        assert "trace_refs" in row
    # inventory defaults
    assert any(r["review_state"] == "unverified" for r in data["claims"])


def test_app_data_exports_review_state():
    from universe_explorer.data.registry import TOPICS

    data = json.loads(app_data_json(TOPICS))
    row = data["claims"][0]
    assert "review_state" in row
    assert "verified_by" in row


def test_static_html_shows_unverified_badge():
    from universe_explorer.data.black_hole import BLACK_HOLE

    html = render_topic(BLACK_HOLE)
    assert "unverified" in html or "○ unverified" in html
    assert "review-badge" in html


def test_throwaway_verified_by_blocked():
    c = _speculative()
    c.review_state = ReviewState.HUMAN_VERIFIED
    c.verified_by = "bot"
    c.verified_note = "checked sources against claim text"
    c.verified_at = "2026-08-11"
    assert "verified_by_invalid" in {v.rule for v in validate_claim(c)}


def test_human_verified_needs_note_and_date():
    c = _speculative()
    c.review_state = ReviewState.HUMAN_VERIFIED
    c.verified_by = "alice@example.com"
    c.verified_note = ""
    c.verified_at = ""
    rules = {v.rule for v in validate_claim(c)}
    assert "verified_note_vacuous" in rules
    assert "verified_at_invalid" in rules
    c.verified_note = "read both sources; titles match claim scope"
    c.verified_at = "2026-08-11"
    assert validate_claim(c) == []


def test_challenged_badge_in_html():
    from universe_explorer.data.black_hole import BLACK_HOLE
    import copy

    topic = copy.deepcopy(BLACK_HOLE)
    topic.claims[0].review_state = ReviewState.CHALLENGED
    html = render_topic(topic)
    assert "challenged" in html


def test_narrative_states_editorial_mark():
    c = _speculative()
    sents = compose(c)
    check(c, sents)
    assert any("Editorial mark" in s.text or "編輯標記" in s.text for s in sents)
    assert any("unverified" in s.text for s in sents)

    c.review_state = ReviewState.CHALLENGED
    sents = compose(c)
    check(c, sents)
    assert any("challenged" in s.text for s in sents)


def test_precheck_preserves_trace_refs():
    cand = {
        "id": "poc_pre_tr",
        "title": "draft with trace",
        "status": "FRONTIER",
        "status_reason": [
            {"condition": cond, "holds": True,
             "note": "adequate frontier justification text"}
            for cond in STATUS_CONDITIONS[Status.FRONTIER]["conditions"]
        ],
        "evidence": [
            {"type": "theoretical result", "description": "abstract note",
             "source_ref": "p1"},
        ],
        "sources": [
            {"label": "p1", "url_or_id": "arXiv:1906.11238",
             "kind": "preprint (arXiv)"},
        ],
        "open_questions": ["what next?"],
        "trace_refs": ["p1"],
        "review_state": "unverified",
    }
    claim = _dict_to_claim(cand)
    assert claim is not None
    assert claim.trace_refs == ["p1"]
    # With provenance on, precheck should not invent trace_refs_missing.
    report = precheck(cand)
    assert "trace_refs_missing" not in {v.rule for v in report.violations}


def test_precheck_runs_provenance():
    cand = {
        "id": "poc_unfetched",
        "title": "unfetched doi draft",
        "status": "FRONTIER",
        "status_reason": [
            {"condition": cond, "holds": True,
             "note": "adequate frontier justification text"}
            for cond in STATUS_CONDITIONS[Status.FRONTIER]["conditions"]
        ],
        "evidence": [
            {"type": "theoretical result", "description": "note",
             "source_ref": "p1"},
        ],
        "sources": [
            {"label": "p1", "url_or_id": "doi:10.9999/never-fetched-r4",
             "kind": "peer-reviewed paper"},
        ],
        "open_questions": ["?"],
    }
    report = precheck(cand)
    assert report.pass_constitution is False
    assert any(v.rule == "doi_source_unfetched" for v in report.violations)


def test_arxiv_doi_paper_id_merge_from_cache():
    reload_paper_aliases()
    # 0704.0261 declares DOI 10.1086/587859 in local Atom cache.
    a = paper_id_of("arXiv:0704.0261")
    d = paper_id_of("doi:10.1086/587859")
    assert a is not None and d is not None
    assert a == d == "doi:10.1086/587859"


def test_merged_ids_cannot_mint_e1_alone():
    """Same work via arxiv + doi must not count as two independent papers."""
    reload_paper_aliases()
    s1 = Source("a1", "arXiv:0704.0261", "peer-reviewed paper")
    s2 = Source("d1", "doi:10.1086/587859", "peer-reviewed paper")
    # Need both in provenance for full green; axis only needs fetchable shape.
    c = Claim(
        id="poc_merge_e1",
        title="identity merge blocks dual-count E1",
        status=Status.ESTABLISHED,
        status_reason=[
            _ca(x) for x in STATUS_CONDITIONS[Status.ESTABLISHED]["conditions"]
        ],
        evidence=[
            Evidence("direct observation", "obs A fabricated", "a1"),
            Evidence("direct observation", "obs B same work", "d1"),
        ],
        sources=[s1, s2],
        open_questions=["same paper?"],
        trace_refs=["a1", "d1"],
    )
    assert derive(c).strength.short != "E1"


def test_vacuous_note_r49_phrases_blocked():
    c = Claim(
        id="poc_vac",
        title="strong with weak note",
        status=Status.STRONG,
        sources=[Source("A", "arXiv:1906.11238", "peer-reviewed paper")],
        evidence=[Evidence("direct observation", "signal seen", "A")],
        status_reason=[
            ConditionAssessment("mainstream_model_support", True, "because sources"),
            ConditionAssessment("minor_alternatives_exist", True, "supported by literature"),
            ConditionAssessment("overall_direction_robust", True, "yes it holds"),
        ],
        trace_refs=["A"],
    )
    rules = {v.rule for v in validate_claim(c)}
    assert "status_reason_vacuous_note" in rules


def test_strong_analog_only_queue_reason():
    c = Claim(
        id="poc_analog_q",
        title="strong analog only unverified",
        status=Status.STRONG,
        sources=[Source("A", "doi:10.1126/science.203.4385.1073", "peer-reviewed paper")],
        evidence=[Evidence("analog experiment", "lab apparatus note long", "A")],
        status_reason=[
            _ca("mainstream_model_support"),
            _ca("minor_alternatives_exist"),
            _ca("overall_direction_robust"),
        ],
        open_questions=["?"],
        trace_refs=["A"],
    )
    row = ledger_row(c, "t")
    assert row.needs_human is True
    assert "analog" in row.reason.lower() or "false-analog" in row.reason.lower()
