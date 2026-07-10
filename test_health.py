"""T1 acceptance tests (offline — the live mechanism was verified against the
formally retracted Wakefield 1998 record). Run: python test_health.py"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from universe_explorer.dataops.source_health import (
    _load_acknowledged,
    new_findings,
)

F1 = {"source_doi": "10.1/a", "updating_doi": "10.1/a-retraction",
      "update_types": ["retraction"], "title": "Retraction notice",
      "issued": [2026]}
F2 = {"source_doi": "10.1/b", "updating_doi": "10.1/b-corr",
      "update_types": ["correction"], "title": "Correction", "issued": [2025]}


def test_unacknowledged_findings_are_new():
    assert new_findings([F1, F2], set()) == [F1, F2]


def test_acknowledged_findings_go_quiet():
    """Acknowledging is an explicit human act; after it, the channel is silent
    for that record — but ONLY that record."""
    acked = {"10.1/a-retraction"}
    assert new_findings([F1, F2], acked) == [F2]


def test_finding_without_updating_doi_never_fires():
    ghost = dict(F1, updating_doi="")
    assert new_findings([ghost], set()) == []


def test_acknowledged_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "acknowledged.json"
        assert _load_acknowledged(p) == set()
        p.write_text(json.dumps(["10.1/a-retraction"]), encoding="utf-8")
        assert _load_acknowledged(p) == {"10.1/a-retraction"}


def test_findings_carry_zero_interpretation():
    """Mechanical records only: the finding schema has no judgment fields."""
    allowed = {"source_doi", "updating_doi", "update_types", "title", "issued"}
    assert set(F1) <= allowed


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
