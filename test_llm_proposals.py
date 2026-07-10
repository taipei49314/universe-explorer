"""B2 acceptance: the LLM drafter is locked in its cell.
No live model needed. Run: python test_llm_proposals.py"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from universe_explorer.data.black_hole import hawking_radiation as HR
from universe_explorer.dataops.llm_proposals import (
    DraftViolation,
    build_prompt,
    parse_and_gate,
    record_drafts,
)
from universe_explorer.model import Status


def _raw(items) -> str:
    return json.dumps(items)


def test_good_draft_passes():
    raw = _raw([{"condition": "mainstream_model_support",
                 "suggested_holds": True,
                 "draft_note": "Check standard QFT-in-curved-spacetime "
                               "textbooks (Birrell & Davies; Wald) for the "
                               "derivation's acceptance."}])
    drafts = parse_and_gate(HR, Status.STRONG, raw)
    assert drafts[0].verified == "UNVERIFIED"


def test_machine_condition_is_out_of_power():
    """multiple_independent_replications is machine-judged — an LLM draft
    touching it must be rejected."""
    raw = _raw([{"condition": "multiple_independent_replications",
                 "suggested_holds": True, "draft_note": "looks replicated"}])
    try:
        parse_and_gate(HR, Status.ESTABLISHED, raw)
        assert False
    except DraftViolation:
        pass


def test_foreign_condition_rejected():
    raw = _raw([{"condition": "sounds_cool", "suggested_holds": True,
                 "draft_note": "note"}])
    try:
        parse_and_gate(HR, Status.STRONG, raw)
        assert False
    except DraftViolation:
        pass


def test_excluded_status_has_nothing_to_draft():
    """ESTABLISHED is mechanically excluded for hawking (E3 evidence) — the
    LLM cannot be asked to draft for an impossible light."""
    try:
        build_prompt(HR, Status.ESTABLISHED)
        assert False
    except DraftViolation:
        pass


def test_numeric_confidence_in_draft_rejected():
    raw = _raw([{"condition": "mainstream_model_support",
                 "suggested_holds": True,
                 "draft_note": "Consensus: 90 out of 100 hold this."}])
    try:
        parse_and_gate(HR, Status.STRONG, raw)
        assert False
    except DraftViolation:
        pass


def test_drafts_log_is_separate_and_stamped():
    drafts = parse_and_gate(HR, Status.STRONG, _raw([
        {"condition": "minor_alternatives_exist", "suggested_holds": True,
         "draft_note": "Survey review articles on trans-Planckian critiques."}]))
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "drafts.jsonl"
        entry = record_drafts(HR, Status.STRONG, drafts, "test-model", log)
        assert entry["verified"] == "UNVERIFIED"
        assert log.name != "decisions.jsonl"  # physical separation
        line = json.loads(log.read_text(encoding="utf-8"))
        assert all(d["verified"] == "UNVERIFIED" for d in line["drafts"])


def test_prompt_offers_only_human_conditions():
    p = build_prompt(HR, Status.STRONG)
    assert "mainstream_model_support" in p
    assert "multiple_independent_replications" not in p  # machine, other status


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
