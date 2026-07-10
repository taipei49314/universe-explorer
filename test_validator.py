"""Proof that the validator actually catches violations (spec section 6.3).

A validator that never fails is worthless: it must be able to overturn a bad
record. Each case below deliberately breaks one constitution rule and asserts
the matching violation is raised. Run with:  python test_validator.py
"""

from __future__ import annotations

import copy

from universe_explorer.data.black_hole import BLACK_HOLE, firewall
from universe_explorer.model import (
    Claim,
    ConditionAssessment,
    Evidence,
    Source,
    Status,
)
from universe_explorer.validator import validate_claim, validate_topic


def _rules(claim) -> set:
    return {v.rule for v in validate_claim(claim)}


def test_real_data_passes():
    assert validate_topic(BLACK_HOLE) == [], "shipped data must be clean"


def test_evidence_without_source():
    c = copy.deepcopy(firewall)
    c.evidence[0].source_ref = ""
    assert "evidence_without_source" in _rules(c)


def test_dangling_source_ref():
    c = copy.deepcopy(firewall)
    c.evidence[0].source_ref = "does-not-exist"
    assert "dangling_source_ref" in _rules(c)


def test_bare_percentage_is_rejected():
    c = copy.deepcopy(firewall)
    c.open_questions.append("Consensus is about 73% against it.")
    assert "no_fake_precision" in _rules(c)


def test_amendment1_sourced_percentage_in_evidence_allowed():
    """Amendment #1: a measured % inside an evidence description (which is
    forced to hang on a real source) is a restatement, not a declaration."""
    c = copy.deepcopy(firewall)
    c.evidence[0].description += " The cited paper reports a 15% effect."
    rules = _rules(c)
    assert "no_fake_precision" not in rules
    assert "declared_confidence" not in rules


def test_amendment1_declared_confidence_caught_even_in_evidence():
    """Even with a source attached, certainty must not be rewritten as a
    number — the confidence vocabulary is banned everywhere."""
    c = copy.deepcopy(firewall)
    c.evidence[0].description += " Confidence: 73."
    assert "declared_confidence" in _rules(c)


def test_amendment1_percent_outside_evidence_still_banned():
    c = copy.deepcopy(firewall)
    c.status_reason[0].note += " roughly 40% of theorists agree"
    assert "no_fake_precision" in _rules(c)


def test_numeric_open_question_count():
    c = copy.deepcopy(firewall)
    c.evidence[0].description += " Open questions: 2 remain."
    assert "no_numeric_open_questions" in _rules(c)


def test_open_question_that_is_just_a_number():
    c = copy.deepcopy(firewall)
    c.open_questions.append("3")
    assert "numeric_open_question" in _rules(c)


def test_status_reason_incomplete():
    # Established requires ALL four conditions; drop one.
    c = copy.deepcopy(BLACK_HOLE.claims[0])
    c.status_reason = c.status_reason[:-1]
    assert "status_reason_incomplete" in _rules(c)


def test_foreign_condition():
    c = copy.deepcopy(firewall)
    c.status_reason.append(
        ConditionAssessment("multiple_independent_replications", True, "nope")
    )
    assert "foreign_condition" in _rules(c)


def test_condition_not_satisfied_for_all_mode():
    c = copy.deepcopy(BLACK_HOLE.claims[0])  # Established, mode "all"
    c.status_reason[0].holds = False
    assert "condition_not_satisfied" in _rules(c)


def test_competing_without_models():
    c = Claim(
        id="x", title="t", status=Status.COMPETING,
        sources=[Source("s", "id", "k")],
        evidence=[Evidence("t", "d", "s")],
        status_reason=[
            ConditionAssessment("two_or_more_mainstream_models", True, "n"),
            ConditionAssessment("no_decisive_evidence_yet", True, "n"),
            ConditionAssessment("genuine_scientific_camps", True, "n"),
        ],
    )
    assert "competing_needs_models" in _rules(c)


def test_competing_models_on_wrong_status():
    from universe_explorer.model import CompetingModel
    c = copy.deepcopy(firewall)  # Speculative
    c.competing_models = [CompetingModel("a", "s", "o", "l")]
    assert "unexpected_competing_models" in _rules(c)


def test_unsupported_claim_has_no_evidence():
    c = copy.deepcopy(firewall)
    c.evidence = []
    assert "unsupported_claim" in _rules(c)


def _run():
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
            passed += 1
    print(f"\n{passed} tests passed.")


if __name__ == "__main__":
    _run()
