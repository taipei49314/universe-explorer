"""Multi-topic change watch — wiring, not engine.

The engine functions in watch.py (current_state / diff_events /
check_documented_transitions / emit_events) are already domain-agnostic; only
its CLI main() is hard-wired to the black-hole topic from the single-topic era.
Rather than amend the frozen engine for wiring, this module drives those same
functions over the whole topic registry and keeps one merged snapshot (claim
ids are globally unique).

Usage:
    python -m universe_explorer.dataops.watch_all            # diff + events
    python -m universe_explorer.dataops.watch_all --commit   # accept as baseline
"""

from __future__ import annotations

import datetime as dt
import json
from typing import Dict, List

from ..data.registry import TOPICS
from ..watch import (
    SNAPSHOT_PATH,
    check_documented_transitions,
    current_state,
    diff_events,
    emit_events,
    load_snapshot,
)


def merged_state() -> Dict[str, dict]:
    state: Dict[str, dict] = {}
    for topic in TOPICS:
        state.update(current_state(topic))
    return state


def commit_merged_snapshot() -> None:
    SNAPSHOT_PATH.parent.mkdir(exist_ok=True)
    SNAPSHOT_PATH.write_text(json.dumps({
        "committed_at": dt.datetime.now(dt.timezone.utc)
                          .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claims": merged_state(),
    }, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: List[str]) -> int:
    now = merged_state()
    snapshot = load_snapshot()

    if snapshot is None:
        if "--commit" in argv:
            commit_merged_snapshot()
            print(f"initial merged snapshot -> {SNAPSHOT_PATH}")
            return 0
        print("no snapshot yet — run with --commit to establish the baseline")
        return 0

    violations = []
    for topic in TOPICS:
        violations.extend(check_documented_transitions(topic, snapshot))
    for v in violations:
        print(f"VIOLATION {v}")

    events = diff_events(snapshot, now)
    if events:
        out = emit_events(events)
        print(f"{len(events)} change event(s) -> {out}")
        for e in events:
            print(f"  - {e['claim']}: {e['kind']}")
    else:
        print("stable: no changes against the committed snapshot (zero noise)")

    if "--commit" in argv:
        if violations:
            print("refusing to commit: document the transition in "
                  "status_history first")
            return 1
        commit_merged_snapshot()
        print(f"snapshot updated -> {SNAPSHOT_PATH}")

    return 1 if violations else 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
