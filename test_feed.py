"""D3 (feed) acceptance tests. Run: python test_feed.py"""

from __future__ import annotations

import json
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from universe_explorer.dataops.feed import build_feed

_A = "{http://www.w3.org/2005/Atom}"


def _events_dir(payloads) -> Path:
    tmp = Path(tempfile.mkdtemp())
    for i, p in enumerate(payloads):
        (tmp / f"2026071{i}T00000{i}Z-events.json").write_text(
            json.dumps(p), encoding="utf-8")
    return tmp


def test_feed_is_valid_atom_with_one_entry_per_event_file():
    d = _events_dir([
        {"at": "20260710T000000Z", "events": [
            {"kind": "status_changed", "claim": "firewall",
             "before": "SPECULATIVE", "after": "FRONTIER"}]},
        {"at": "20260711T000001Z", "events": [
            {"kind": "claim_added", "claim": "x",
             "after": {"status": "STRONG", "evidence_axis": "E2"}}]},
    ])
    root = ET.fromstring(build_feed(d))
    entries = root.findall(f"{_A}entry")
    assert len(entries) == 2
    texts = [e.findtext(f"{_A}content") for e in entries]
    assert any("firewall" in t and "'SPECULATIVE' -> 'FRONTIER'" in t
               for t in texts)
    # every entry names its event file (traceability back to the derivation)
    assert all("-events.json" in t for t in texts)


def test_feed_restates_never_interprets():
    d = _events_dir([{"at": "20260710T000000Z", "events": [
        {"kind": "evidence_axis_changed", "claim": "c",
         "before": "E3", "after": "E2"}]}])
    feed = build_feed(d).lower()
    for banned in ("breakthrough", "exciting", "finally", "revolution",
                   "amazing"):
        assert banned not in feed


def test_empty_events_dir_gives_valid_empty_feed():
    tmp = Path(tempfile.mkdtemp())
    root = ET.fromstring(build_feed(tmp))
    assert root.findall(f"{_A}entry") == []


def test_real_feed_builds_and_parses():
    root = ET.fromstring(build_feed())
    assert root.findtext(f"{_A}title").startswith("Universe Explorer")


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
