"""P3 acceptance tests. All change scenarios are staged on deep copies —
the real snapshot and data are never modified. Run: python test_watch.py"""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from universe_explorer.data.black_hole import BLACK_HOLE
from universe_explorer.model import Evidence, Source, Status, StatusChange, Topic
from universe_explorer.watch import (
    check_documented_transitions,
    current_state,
    diff_events,
    emit_events,
)


def _fw(topic):
    return next(c for c in topic.claims if c.id == "firewall")


def _snap() -> dict:
    return current_state(BLACK_HOLE)


def test_stable_means_zero_noise():
    snap = _snap()
    assert diff_events(snap, snap) == []
    assert check_documented_transitions(BLACK_HOLE, snap) == []


def test_diff_is_idempotent():
    snap = _snap()
    topic = copy.deepcopy(BLACK_HOLE)
    _fw(topic).status = Status.FRONTIER
    now = current_state(topic)
    first = diff_events(snap, now)
    second = diff_events(snap, now)
    assert first == second and first  # same result twice, and non-empty


def test_silent_status_change_is_caught():
    snap = _snap()
    topic = copy.deepcopy(BLACK_HOLE)
    _fw(topic).status = Status.FRONTIER  # firewall promoted, no history
    v = check_documented_transitions(topic, snap)
    assert [x.rule for x in v] == ["undocumented_status_change"]
    assert v[0].claim_id == "firewall"


def test_documented_status_change_passes():
    snap = _snap()
    topic = copy.deepcopy(BLACK_HOLE)
    c = _fw(topic)
    c.status = Status.FRONTIER
    c.status_history.append(StatusChange(
        date="2026-07-10", from_status="Speculative",
        to_status="Frontier Research",
        trigger="hypothetical: first observational proposal peer-reviewed"))
    assert check_documented_transitions(topic, snap) == []


def test_evidence_change_produces_traceable_event():
    """New evidence moves the derived axis -> an event with before/after and
    the mechanical derivation, no interpretation."""
    snap = _snap()
    topic = copy.deepcopy(BLACK_HOLE)
    hawking = topic.claims[1]
    hawking.sources.append(Source("HYPO", "Nature (hypothetical)", "paper"))
    hawking.evidence.append(
        Evidence("direct observation", "hypothetical detection", "HYPO"))
    events = diff_events(snap, current_state(topic))
    kinds = {(e["claim"], e["kind"]) for e in events}
    assert ("hawking_radiation", "evidence_axis_changed") in kinds
    assert ("hawking_radiation", "diverges_changed") in kinds
    ax = next(e for e in events if e["kind"] == "evidence_axis_changed")
    assert ax["before"] == "E3" and ax["after"] == "E2"
    assert any("rule E2" in r for r in ax["derivation"])  # points back at rules


def test_events_written_as_files():
    snap = _snap()
    topic = copy.deepcopy(BLACK_HOLE)
    topic.claims[0].open_questions.append("does not affect watched keys")
    _fw(topic).status = Status.FRONTIER
    events = diff_events(snap, current_state(topic))
    with tempfile.TemporaryDirectory() as tmp:
        out = emit_events(events, Path(tmp))
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["events"] and data["events"][0]["claim"] == "firewall"


def test_no_events_no_file():
    with tempfile.TemporaryDirectory() as tmp:
        assert emit_events([], Path(tmp)) is None
        assert not list(Path(tmp).iterdir())


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
