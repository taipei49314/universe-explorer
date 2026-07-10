"""B1 acceptance: the court bites LLM output exactly as hard.
No live model needed — drafts are forged. Run: python test_llm_narrative.py"""

from __future__ import annotations

import json

from universe_explorer.data.black_hole import hawking_radiation as HR
from universe_explorer.dataops.llm_narrative import (
    build_prompt,
    narrate_llm,
    parse_and_gate,
)
from universe_explorer.narrative import OPENING, NarrativeViolation


def _draft(sentences) -> str:
    return json.dumps(sentences)


def test_good_llm_draft_passes():
    raw = _draft([
        {"text": f"{OPENING}, this claim carries the light "
                 f"\U0001F535 Strong Consensus.",
         "refs": ["Hawking1975", "condition:mainstream_model_support"]},
        {"text": "The recorded theoretical derivation hangs on Hawking's "
                 "1975 calculation.", "refs": ["Hawking1975"]},
    ])
    sentences = parse_and_gate(HR, raw)
    assert len(sentences) == 2


def test_unreferenced_llm_sentence_killed():
    raw = _draft([
        {"text": f"{OPENING}, summary.", "refs": ["Hawking1975"]},
        {"text": "Black holes certainly evaporate.", "refs": []},
    ])
    try:
        parse_and_gate(HR, raw)
        assert False
    except NarrativeViolation:
        pass


def test_invented_ref_killed():
    raw = _draft([{"text": f"{OPENING}, summary.", "refs": ["MadeUp2049"]}])
    try:
        parse_and_gate(HR, raw)
        assert False
    except NarrativeViolation:
        pass


def test_invented_percentage_killed():
    raw = _draft([
        {"text": f"{OPENING}, summary.", "refs": ["Hawking1975"]},
        {"text": "About 30% of physicists doubt this.", "refs": ["Hawking1975"]},
    ])
    try:
        parse_and_gate(HR, raw)
        assert False
    except NarrativeViolation:
        pass


def test_garbage_output_raises():
    try:
        parse_and_gate(HR, "sorry, I cannot help with that")
        assert False
    except ValueError:
        pass


def test_fallback_is_always_safe():
    """With an unreachable model, narrate_llm returns the mechanical
    narrative — never an error, never silence."""
    sentences, origin = narrate_llm(HR, model="no-such-model:0b")
    # origin may be 'mechanical' (server down / model missing) or, if a live
    # local model actually answered lawfully, 'llm' — both are legal outcomes.
    assert sentences and all(s.refs for s in sentences)


def test_prompt_contains_only_recorded_fields():
    p = build_prompt(HR)
    assert "Hawking1975" in p and "Steinhauer2016" in p
    assert OPENING in p
    # the prompt must not leak other claims' sources
    assert "AMPS2013" not in p and "EHT2019-M87-I" not in p


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
