"""P2 acceptance tests. Run: python test_proposals.py"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from universe_explorer.data.black_hole import BLACK_HOLE, hawking_radiation
from universe_explorer.model import STATUS_CONDITIONS, Status
from universe_explorer.proposals import (
    MACHINE_CONDITIONS,
    propose,
    record_decision,
)


def test_current_statuses_all_inside_compatible_set():
    """Consistency (P2 acceptance 3): every human-judged light must sit inside
    the engine's compatible set — a mismatch means data or engine is wrong."""
    for claim in BLACK_HOLE.claims:
        p = propose(claim)
        names = {s.name for s in p.compatible_statuses}
        assert claim.status.name in names, claim.id


def test_engine_actually_excludes():
    """Not a rubber stamp: at least one real claim has an excluded status."""
    excluded_somewhere = [c.id for c in BLACK_HOLE.claims
                          if propose(c).excluded_statuses]
    assert excluded_somewhere, "engine excluded nothing — it approves everything"
    # hawking specifically: E3 evidence makes ESTABLISHED mechanically impossible.
    p = propose(hawking_radiation)
    assert Status.ESTABLISHED in p.excluded_statuses


def test_human_conditions_are_never_guessed():
    """Iron rule 2: every non-machine condition must come back holds=None."""
    for claim in BLACK_HOLE.claims:
        for a in propose(claim).assessments:
            for s in a.signals:
                if s.kind == "human":
                    assert s.holds is None, (claim.id, s.condition)
                else:
                    assert s.condition in MACHINE_CONDITIONS


def test_machine_signals_are_traceable():
    """P2 acceptance 1: machine rationale cites the derived evidence summary."""
    for a in propose(hawking_radiation).assessments:
        for s in a.signals:
            if s.kind == "machine":
                assert "recorded evidence:" in s.rationale, s.condition


def test_every_condition_is_classified():
    """The machine/human split must cover the whole taxonomy — no orphans."""
    all_conditions = {c for spec in STATUS_CONDITIONS.values()
                      for c in spec["conditions"]}
    assert MACHINE_CONDITIONS <= all_conditions


def test_audit_log_append_only_and_complete():
    p = propose(hawking_radiation)
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "decisions.jsonl"
        record_decision(p, "reject", "tester", "engine set looks right", log)
        record_decision(p, "accept", "tester", "confirmed against taxonomy", log)
        lines = log.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2  # appended, not overwritten
        entry = json.loads(lines[1])
        assert entry["decided_by"] == "tester"
        assert entry["proposal_snapshot"]["excluded"] == ["ESTABLISHED"]


def test_decision_requires_decider_and_reason():
    p = propose(hawking_radiation)
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "d.jsonl"
        for bad in (("accept", "", "reason"), ("accept", "who", ""),
                    ("maybe", "who", "reason")):
            try:
                record_decision(p, *bad, audit_log=log)
                assert False, f"should have refused {bad}"
            except ValueError:
                pass
        assert not log.exists()  # nothing was written on refusal


def test_proposals_never_touch_claim_data():
    """Iron rule 1: proposing must not modify the data module's file."""
    data_file = Path("universe_explorer/data/black_hole.py")
    before = data_file.read_bytes()
    for claim in BLACK_HOLE.claims:
        propose(claim)
    assert data_file.read_bytes() == before


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
