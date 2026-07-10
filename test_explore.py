"""D2 acceptance tests. Run: python test_explore.py"""

from __future__ import annotations

import json

from universe_explorer.data.registry import TOPICS
from universe_explorer.axes import derive
from universe_explorer.render import claims_json, render_explore, render_topic

ALL_CLAIMS = [(t, c) for t in TOPICS for c in t.claims]


def test_every_claim_has_a_stable_anchor():
    for t in TOPICS:
        html = render_topic(t)
        for c in t.claims:
            assert f'id="c-{c.id}"' in html, c.id
            assert f'href="#c-{c.id}"' in html  # visible permalink


def test_explore_lists_every_claim_with_filter_data():
    html = render_explore(TOPICS)
    for t, c in ALL_CLAIMS:
        assert f'{t.id}.html#c-{c.id}' in html, c.id
        assert f'data-status="{c.status.name}"' in html
    # filter chips for all five lights and all five axis grades
    for name in ("ESTABLISHED", "STRONG", "COMPETING", "FRONTIER", "SPECULATIVE"):
        assert f'data-v="{name}"' in html
    for grade in ("E1", "E2", "E3", "E4", "E5"):
        assert f'data-v="{grade}"' in html


def test_explore_is_self_contained():
    """Zero external resources: no http(s) URLs in src/href except local pages."""
    html = render_explore(TOPICS)
    assert "http://" not in html and "https://" not in html
    assert "<script src" not in html  # JS is inline vanilla


def test_claims_json_complete_and_consistent():
    data = json.loads(claims_json(TOPICS))
    claims = {c["id"]: c for c in data["claims"]}
    assert len(claims) == len(ALL_CLAIMS)
    for t, c in ALL_CLAIMS:
        j = claims[c.id]
        assert j["topic"] == t.id
        assert j["status"] == c.status.name
        assert j["evidence_axis"] == derive(c).strength.short
        assert len(j["evidence"]) == len(c.evidence)
        assert len(j["sources"]) == len(c.sources)
        for s in j["sources"]:
            assert s["tier"] is not None  # Amendment #3 holds in the export
        assert isinstance(j["open_questions"], list)  # a list, never a number


def test_claims_json_invents_nothing():
    """No confidence-like numeric fields exist anywhere in the export."""
    data = json.loads(claims_json(TOPICS))
    banned_keys = {"confidence", "score", "probability", "certainty"}
    def walk(x):
        if isinstance(x, dict):
            assert not (set(x) & banned_keys), set(x) & banned_keys
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(data)


# --- T2/T3: challenge channel + charter page ---------------------------------

def test_every_claim_card_has_a_challenge_link():
    for t in TOPICS:
        html = render_topic(t)
        for c in t.claims:
            assert (f'template=challenge-a-verdict.yml&title=%5Bchallenge%5D'
                    f'%20{c.id}' in html), c.id


def test_about_pages_carry_the_charter():
    from universe_explorer.render import render_about
    en, zh = render_about(), render_about("zh")
    for needle in ("No confidence percentages", "axes diverge",
                   "claims.json", "challenge"):
        assert needle in en, needle
    for needle in ("信心百分比", "雙軸分岔", "claims.json", "推翻"):
        assert needle in zh, needle
    # the charter page asserts nothing new: no DOIs, no claim verdicts
    assert "doi:" not in en.lower().replace("challenge-a-verdict", "")


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
