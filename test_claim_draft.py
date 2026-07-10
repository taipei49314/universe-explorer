"""T4 acceptance: every court bites the drafting pipeline; nothing lands.
Offline — uses the already-cached GW150914 arXiv record. Run:
python test_claim_draft.py"""

from __future__ import annotations

import json
from pathlib import Path

from universe_explorer.dataops.claim_draft import (
    DraftRejected,
    assemble_and_gate,
    fetch_and_read_sources,
)

SOURCES = fetch_and_read_sources(["1602.03837"])  # cached; no network
LABEL = SOURCES[0]["label"]


def _raw(**kw) -> str:
    d = {
        "title": "Binary black hole mergers emit detectable gravitational waves",
        "suggested_status": "FRONTIER",
        "evidence": [{"type": "direct observation",
                      "description": "LIGO observed a transient gravitational-"
                                     "wave signal matching a binary black hole "
                                     "merger waveform.",
                      "source_ref": LABEL}],
        "human_condition_notes": {
            "new_discovery": {"holds": True,
                              "note": "Check whether this counts as a new "
                                      "observational channel."}},
        "open_questions": ["How common are such mergers?"],
    }
    d.update(kw)
    return json.dumps(d)


def test_good_draft_passes_every_court():
    draft = assemble_and_gate("bbh_mergers_detected", _raw(), SOURCES)
    assert draft["verified"] == "UNVERIFIED"
    assert draft["court_report"]["constitution"] == "zero violations"
    assert draft["court_report"]["evidence_axis"].startswith("E2")
    # machine conditions were filled from the derivation, never the LLM
    machine_notes = [r["note"] for r in draft["claim"]["status_reason"]
                     if r["note"].startswith("[machine]")]
    assert machine_notes


def test_status_outside_compatible_set_rejected():
    """One direct observation (E2) can never support ESTABLISHED. The defense
    is layered: the v0 constitution court (machine-filled
    multiple_independent_replications holds=False under all-mode) fires even
    before the compatible-set court would — either rejection is lawful."""
    raw = _raw(suggested_status="ESTABLISHED",
               human_condition_notes={
                   "accepted_in_mainstream_textbooks": {"holds": True, "note": "n"},
                   "no_mainstream_competing_theory": {"holds": True, "note": "n"},
                   "no_recent_major_refutation": {"holds": True, "note": "n"}})
    try:
        assemble_and_gate("x", raw, SOURCES)
        assert False
    except DraftRejected as e:
        assert ("OUTSIDE" in str(e)
                or "multiple_independent_replications" in str(e))


def test_percentage_in_condition_note_rejected():
    raw = _raw(human_condition_notes={
        "new_discovery": {"holds": True, "note": "About 90% of experts agree."}})
    try:
        assemble_and_gate("x", raw, SOURCES)
        assert False
    except DraftRejected as e:
        assert "constitution" in str(e)


def test_vocabulary_violation_rejected():
    raw = _raw(evidence=[{"type": "vibes", "description": "d",
                          "source_ref": LABEL}])
    try:
        assemble_and_gate("x", raw, SOURCES)
        assert False
    except DraftRejected as e:
        assert "invalid_evidence_type" in str(e)


def test_dangling_source_ref_rejected():
    raw = _raw(evidence=[{"type": "direct observation", "description": "d",
                          "source_ref": "NotASource"}])
    try:
        assemble_and_gate("x", raw, SOURCES)
        assert False
    except DraftRejected:
        pass


def test_data_files_untouched():
    data_dir = Path("universe_explorer/data")
    before = {p.name: p.read_bytes() for p in data_dir.glob("*.py")}
    assemble_and_gate("bbh_mergers_detected", _raw(), SOURCES)
    after = {p.name: p.read_bytes() for p in data_dir.glob("*.py")}
    assert before == after


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
