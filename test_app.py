"""D4 acceptance tests. Run: python test_app.py"""

from __future__ import annotations

import json
import re
from pathlib import Path

from universe_explorer.axes import EvidenceStrength, derive, diverges
from universe_explorer.data.registry import TOPICS
from universe_explorer.render import app_data_json

DATA = json.loads(app_data_json(TOPICS))
APP = Path("web/app.html").read_text(encoding="utf-8")
UNI = Path("web/universe.html").read_text(encoding="utf-8")


def test_app_data_complete_and_consistent():
    all_claims = [(t, c) for t in TOPICS for c in t.claims]
    by_id = {c["id"]: c for c in DATA["claims"]}
    assert len(by_id) == len(all_claims)
    assert {t["id"] for t in DATA["topics"]} == {t.id for t in TOPICS}
    for t, c in all_claims:
        j = by_id[c.id]
        assert j["status"] == c.status.name
        assert j["axis"] == derive(c).strength.short
        assert j["diverges"] == diverges(c)
        assert j["axis_rank"] == list(EvidenceStrength).index(derive(c).strength)
        assert j["permalink"] == f"{t.id}.html#c-{c.id}"
        # bilingual fields exist (fallback == English is legal, absence is not)
        for f in ("title_zh", "status_name_zh", "axis_name_zh",
                  "open_questions_zh"):
            assert f in j, (c.id, f)
        for sr in j["status_reason"]:
            assert sr["note_zh"]
        for s in j["sources"]:
            assert s["tier"] is not None


def test_app_data_invents_nothing():
    banned = {"confidence", "score", "probability", "certainty"}
    def walk(x):
        if isinstance(x, dict):
            assert not (set(x) & banned), set(x) & banned
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(DATA)


def test_app_html_self_contained():
    """No external RESOURCES: no remote scripts/styles/imports/fetches.
    Outbound <a href> links (github challenge) are navigation, not resources."""
    assert "<script src" not in APP
    assert "<link " not in APP
    assert "@import" not in APP
    assert "url(http" not in APP
    fetches = re.findall(r'fetch\("([^"]+)"\)', APP)
    assert fetches == ["app-data.json"]


def test_app_html_has_the_required_surfaces():
    for needle in ('id="map"', 'id="panel"', 'id="langbtn"', 'id="cards"',
                   "prefers-reduced-motion", "prefers-color-scheme",
                   'role="button"', "tabindex"):
        assert needle in APP, needle
    # both validated palettes present (light + dark), all five status slots
    for hexv in ("#2F7D46", "#2762A8", "#A17C0A", "#C13E2A", "#93265E",
                 "#3E9E5C", "#4C89CC", "#A99312", "#D0512F", "#C04E96"):
        assert hexv in APP, hexv


def test_divergent_claims_land_in_the_marked_zone():
    """The shaded corner is x(status_rank) in {0,1} × y(axis_rank) in {2,3,4};
    every mechanically divergent claim must land inside it."""
    for c in DATA["claims"]:
        if c["diverges"]:
            assert c["status_rank"] <= 1 and c["axis_rank"] >= 2, c["id"]


def test_universe_self_contained_and_epistemic():
    """The drift view: same self-containment law, and its visuals must encode
    epistemics — every status has a distinct body form, size follows the
    evidence axis, divergence pulses."""
    assert "<script src" not in UNI and "<link " not in UNI
    assert "@import" not in UNI and "url(http" not in UNI
    fetches = re.findall(r'fetch\("([^"]+)"\)', UNI)
    assert fetches == ["app-data.json"]
    for needle in ("ESTABLISHED", "STRONG", "COMPETING", "FRONTIER",
                   "SPECULATIVE", "axis_rank", "diverges",
                   "prefers-reduced-motion", "binary", "nebula"):
        assert needle in UNI, needle
    # size = evidence strength: the layout derives size from axis_rank
    assert "size:24 - k.axis_rank" in UNI


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
