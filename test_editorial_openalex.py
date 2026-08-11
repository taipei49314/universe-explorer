"""Amendment #11 — ledger editorial OS + OpenAlex adapter (offline)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from universe_explorer.discovery.adapters.openalex_adapter import (
    OpenAlexAdapter,
    _abstract_from_inverted,
    _doi_from_work,
)
from universe_explorer.discovery.pipeline import ADAPTERS
from universe_explorer.editorial import editorial_queue, ledger_row, record_ok
from universe_explorer.model import (
    Claim,
    ConditionAssessment,
    Evidence,
    ReviewState,
    Source,
    Status,
)
from universe_explorer.validator import validate_claim


def test_openalex_registered():
    assert "openalex" in ADAPTERS
    assert ADAPTERS["openalex"].name == "openalex"


def test_abstract_inverted_index():
    idx = {"Hello": [0], "world": [1]}
    assert _abstract_from_inverted(idx) == "Hello world"


def test_doi_from_work():
    assert _doi_from_work({"doi": "https://doi.org/10.1038/378355a0"}) == "10.1038/378355a0"
    assert _doi_from_work({"doi": None}) is None


def test_openalex_search_maps_doi_refs():
    fixture = {
        "results": [
            {
                "id": "https://openalex.org/W123",
                "doi": "https://doi.org/10.1038/378355a0",
                "title": "A Jupiter-mass companion",
                "publication_date": "1995-11-23",
                "authorships": [{"author": {"display_name": "Mayor"}}],
                "abstract_inverted_index": {"Planet": [0]},
                "cited_by_count": 10,
                "type": "journal-article",
            },
            {
                "id": "https://openalex.org/W999",
                "doi": None,
                "title": "No DOI work",
                "publication_date": "2020-01-01",
                "authorships": [],
                "abstract_inverted_index": {},
            },
        ]
    }
    raw = json.dumps(fixture).encode("utf-8")

    with patch(
        "universe_explorer.discovery.adapters.openalex_adapter._request",
        return_value=raw,
    ):
        hits = OpenAlexAdapter().search("exoplanet", max_results=5)

    assert hits[0].source_ref == "doi:10.1038/378355a0"
    assert hits[0].title.startswith("A Jupiter-mass")
    assert hits[1].source_ref == "openalex:W999"


def test_review_state_default_unverified():
    c = Claim(
        id="x",
        title="t",
        status=Status.SPECULATIVE,
        sources=[Source("s", "tb", "textbook")],
        evidence=[Evidence("theoretical derivation", "d", "s")],
        status_reason=[ConditionAssessment("pure_theoretical_derivation", True, "n")],
    )
    assert c.review_state is ReviewState.UNVERIFIED
    assert validate_claim(c) == []


def test_human_verified_requires_attribution():
    c = Claim(
        id="x",
        title="t",
        status=Status.SPECULATIVE,
        sources=[Source("s", "tb", "textbook")],
        evidence=[Evidence("theoretical derivation", "d", "s")],
        status_reason=[ConditionAssessment("pure_theoretical_derivation", True, "n")],
        review_state=ReviewState.HUMAN_VERIFIED,
        verified_by="",
    )
    assert "verified_without_attribution" in {v.rule for v in validate_claim(c)}
    c.verified_by = "editor@example.com"
    c.verified_note = "checked sources against claim text"
    c.verified_at = "2026-08-11"
    assert validate_claim(c) == []


def test_human_verified_rejects_throwaway_identity():
    c = Claim(
        id="x",
        title="t",
        status=Status.SPECULATIVE,
        sources=[Source("s", "tb", "textbook")],
        evidence=[Evidence("theoretical derivation", "d", "s")],
        status_reason=[ConditionAssessment("pure_theoretical_derivation", True, "n")],
        review_state=ReviewState.HUMAN_VERIFIED,
        verified_by="x",
        verified_note="checked sources against claim text",
        verified_at="2026-08-11",
    )
    rules = {v.rule for v in validate_claim(c)}
    assert "verified_by_invalid" in rules
    c.verified_by = "attacker"
    assert "verified_by_invalid" in {v.rule for v in validate_claim(c)}
    c.verified_by = "taipei49314@example.com"
    assert validate_claim(c) == []


def test_editorial_queue_flags_unverified_high_lights():
    from universe_explorer.data.black_hole import event_horizon_exists
    from universe_explorer.model import Topic

    # Real corpus claim: Established + default unverified → needs human.
    row = ledger_row(event_horizon_exists, "black_hole")
    assert row.record_ok is True
    assert row.review_state == "unverified"
    assert row.needs_human is True

    q = editorial_queue([Topic("black_hole", "BH", "", [event_horizon_exists])])
    assert any(r.claim_id == "event_horizon_exists" for r in q)


def test_record_ok_false_on_vacuous_strong():
    c = Claim(
        id="bad",
        title="t",
        status=Status.STRONG,
        sources=[Source("A", "doi:10.1038/378355a0", "peer-reviewed paper")],
        evidence=[Evidence("analog experiment", "lab note long enough", "A")],
        status_reason=[
            ConditionAssessment("mainstream_model_support", True, "I say so"),
            ConditionAssessment("minor_alternatives_exist", True, "I say so"),
            ConditionAssessment("overall_direction_robust", True, "I say so"),
        ],
        trace_refs=["A"],
    )
    assert record_ok(c) is False
