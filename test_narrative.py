"""R6 acceptance tests. Run: python test_narrative.py"""

from __future__ import annotations

import copy

from universe_explorer.data.registry import TOPICS
from universe_explorer.data.black_hole import hawking_radiation
from universe_explorer.narrative import (
    OPENING,
    NarrativeSentence,
    NarrativeViolation,
    check,
    compose,
    narrate,
)


def test_every_sentence_traceable_across_all_topics():
    """R6 acceptance 1: for every claim in every registered topic, every
    narrative sentence resolves its refs — check() raises on nothing."""
    for topic in TOPICS:
        for claim in topic.claims:
            sentences = compose(claim)
            check(claim, sentences)  # raises on breach
            assert sentences[0].text.startswith(OPENING)
            assert all(s.refs for s in sentences)


def test_unreferenced_sentence_is_killed():
    """R6 acceptance 2: a sentence with no refs is a proclamation."""
    c = hawking_radiation
    bad = compose(c) + [NarrativeSentence("Black holes definitely evaporate.", [])]
    try:
        check(c, bad)
        assert False, "unreferenced sentence must be rejected"
    except NarrativeViolation:
        pass


def test_checker_does_not_trust_composer():
    """R6 acceptance 3: hand-forged narratives face the same court."""
    c = hawking_radiation
    forged = [NarrativeSentence(
        f"{OPENING}, everything is settled.", ["NoSuchSource2049"])]
    try:
        check(c, forged)
        assert False, "dangling ref must be rejected"
    except NarrativeViolation:
        pass


def test_declared_confidence_in_narrative_rejected():
    c = hawking_radiation
    bad = compose(c)
    bad.append(NarrativeSentence(
        f"Community consensus: 92 out of 100.", [c.sources[0].label]))
    try:
        check(c, bad)
        assert False, "declared confidence must be rejected"
    except NarrativeViolation:
        pass


def test_percentage_only_as_verbatim_quote():
    c = hawking_radiation
    bad = compose(c)
    bad.append(NarrativeSentence(
        "Roughly 15% of the radiation escapes.", [c.sources[0].label]))
    try:
        check(c, bad)
        assert False, "non-quoted percentage must be rejected"
    except NarrativeViolation:
        pass


def test_missing_opening_formula_rejected():
    c = hawking_radiation
    s = compose(c)
    s[0] = NarrativeSentence("Here is what we know for sure.", s[0].refs)
    try:
        check(c, s)
        assert False, "missing constitutional opening must be rejected"
    except NarrativeViolation:
        pass


def test_narrate_withholds_rather_than_overreaches():
    """A claim whose narrative cannot pass the gate gets NO narrative — the
    build never renders an overreaching one."""
    c = copy.deepcopy(hawking_radiation)
    c.sources = []          # break ref resolution on purpose
    c.status_reason = []
    assert narrate(c) == []


# --- Amendment #2: localization through the same court ----------------------

def test_amendment2_default_calls_unchanged():
    """Regression: calls without a localization behave exactly as before."""
    s = compose(hawking_radiation)
    assert s[0].text.startswith("Based on the evidence recorded here")
    assert "Recorded as analog experiment" in s[2].text


def test_amendment2_zh_narrative_passes_same_court():
    from universe_explorer.data.translations_zh import ZH_LOC
    for topic in TOPICS:
        for claim in topic.claims:
            sentences = compose(claim, ZH_LOC)
            check(claim, sentences, ZH_LOC)  # raises on breach
            assert sentences[0].text.startswith("根據目前收錄的證據")
            assert all(s.refs for s in sentences)


def test_amendment2_zh_percent_is_verbatim_quote():
    """The AMOC zh evidence contains 15% — its narrative sentence passes only
    because it quotes the zh description verbatim."""
    from universe_explorer.data.translations_zh import ZH_LOC
    from universe_explorer.data.ocean import amoc_weakening
    sentences = compose(amoc_weakening, ZH_LOC)
    check(amoc_weakening, sentences, ZH_LOC)
    assert any("15%" in s.text for s in sentences)


def test_amendment2_forged_zh_narrative_rejected():
    from universe_explorer.data.translations_zh import ZH_LOC
    c = hawking_radiation
    # wrong opening formula
    bad = compose(c, ZH_LOC)
    bad[0] = NarrativeSentence("我們可以確定:" + bad[0].text, bad[0].refs)
    try:
        check(c, bad, ZH_LOC)
        assert False, "wrong zh opening must be rejected"
    except NarrativeViolation:
        pass
    # non-verbatim percentage
    bad = compose(c, ZH_LOC)
    bad.append(NarrativeSentence("大約 40% 的輻射逃逸。", [c.sources[0].label]))
    try:
        check(c, bad, ZH_LOC)
        assert False, "non-quoted zh percentage must be rejected"
    except NarrativeViolation:
        pass


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
