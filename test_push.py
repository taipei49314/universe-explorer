"""P5 (push) acceptance tests. Run: python test_push.py"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from universe_explorer.dataops.push import render_digest


def _event_file(tmp: Path, events: list) -> Path:
    f = tmp / "20260710T000000Z-events.json"
    f.write_text(json.dumps({"at": "20260710T000000Z", "events": events}),
                 encoding="utf-8")
    return f


def test_digest_restates_before_after():
    with tempfile.TemporaryDirectory() as d:
        f = _event_file(Path(d), [{
            "kind": "status_changed", "claim": "firewall",
            "before": "SPECULATIVE", "after": "FRONTIER",
            "derivation": ["rule E4: ..."],
        }])
        digest = render_digest([f])
        assert "firewall" in digest
        assert "'SPECULATIVE' -> 'FRONTIER'" in digest
        assert f.name in digest  # every line traces to its event file


def test_digest_has_no_interpretation():
    """The channel restates; it never editorialises."""
    with tempfile.TemporaryDirectory() as d:
        f = _event_file(Path(d), [{
            "kind": "evidence_axis_changed", "claim": "hawking_radiation",
            "before": "E3", "after": "E2", "derivation": [],
        }])
        digest = render_digest([f]).lower()
        for banned in ("breakthrough", "exciting", "finally", "proof",
                       "confirmed!", "revolution"):
            assert banned not in digest


def test_claim_added_line_carries_status_and_axis():
    with tempfile.TemporaryDirectory() as d:
        f = _event_file(Path(d), [{
            "kind": "claim_added", "claim": "planet_nine",
            "after": {"status": "COMPETING", "evidence_axis": "E3",
                      "evidence_items": 2, "sources": 2, "diverges": False},
            "derivation": [],
        }])
        digest = render_digest([f])
        assert "status COMPETING" in digest and "evidence axis E3" in digest


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
