"""C1 / Amendment #3 acceptance tests. Run: python test_tiers.py"""

from __future__ import annotations

import copy

from universe_explorer.data.registry import TOPICS
from universe_explorer.data.black_hole import firewall
from universe_explorer.validator import (
    SOURCE_TIERS,
    tier_of,
    validate_claim,
)


def test_every_current_source_classifies():
    for topic in TOPICS:
        for claim in topic.claims:
            for src in claim.sources:
                assert tier_of(src.kind) is not None, (claim.id, src.label)


def test_keyword_sets_are_disjoint():
    """No kind can legally match two tiers — classification is unambiguous."""
    all_kw = [w for kws in SOURCE_TIERS.values() for w in kws]
    assert len(all_kw) == len(set(all_kw))
    for tier, kws in SOURCE_TIERS.items():
        for w in kws:
            matches = [t for t, k2 in SOURCE_TIERS.items()
                       if any(x in w or w in x for x in k2)]
            assert matches == [tier], (w, matches)


def test_expected_tiers_on_real_data():
    from universe_explorer.data.black_hole import event_horizon_exists
    kinds = {s.label: tier_of(s.kind) for s in event_horizon_exists.sources}
    assert kinds["EHT2019-M87-I"] == "PRIMARY"
    assert kinds["Nobel2020"] == "SECONDARY"


def test_unclassifiable_kind_is_unconstitutional():
    c = copy.deepcopy(firewall)
    c.sources[0].kind = "a blog post I liked"
    rules = {v.rule for v in validate_claim(c)}
    assert "unclassifiable_source_kind" in rules


def test_no_numeric_scores_anywhere():
    """Tiers are discrete categories; the table must contain no numbers."""
    for tier in SOURCE_TIERS:
        assert not any(ch.isdigit() for ch in tier)


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
