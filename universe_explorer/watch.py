"""P3 — change detection: knowledge may move, but never silently.

The snapshot records what the knowledge state looked like when a human last
committed it. On every run this module re-derives the current state, diffs the
two, and:

  * emits event files (events/*.json) for every difference — the trigger
    interface for future push channels. Events carry before/after values and
    the mechanical derivation, never interpretation;
  * enforces the P3 constitution rule: a claim whose status differs from the
    snapshot MUST have a status_history entry documenting that transition
    (`undocumented_status_change` blocks the build otherwise). Lights may
    change; they may not change silently;
  * only updates the snapshot on an explicit --commit — detection is the
    machine's job, confirmation is a human's.

Usage:
    python -m universe_explorer.watch            # diff + emit events
    python -m universe_explorer.watch --commit   # accept current state as baseline
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Dict, List, Optional

from .axes import derive, diverges
from .model import Topic
from .validator import Violation

SNAPSHOT_PATH = Path(__file__).parent.parent / "snapshot" / "state.json"
EVENTS_DIR = Path(__file__).parent.parent / "events"


def current_state(topic: Topic) -> Dict[str, dict]:
    state = {}
    for c in topic.claims:
        d = derive(c)
        state[c.id] = {
            "status": c.status.name,
            "evidence_axis": d.strength.short,
            "evidence_items": len(c.evidence),
            "sources": len(c.sources),
            "diverges": diverges(c),
            # the mechanical derivation, so an event can point back at it:
            "derivation": d.reasoning,
        }
    return state


def load_snapshot(path: Path = SNAPSHOT_PATH) -> Optional[Dict[str, dict]]:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))["claims"]


def diff_events(snapshot: Dict[str, dict], now: Dict[str, dict]) -> List[dict]:
    """Mechanical diff -> event dicts. No interpretation, only before/after."""
    events: List[dict] = []
    watched = ("status", "evidence_axis", "evidence_items", "sources", "diverges")

    for cid, cur in now.items():
        old = snapshot.get(cid)
        if old is None:
            events.append({
                "kind": "claim_added", "claim": cid,
                "after": {k: cur[k] for k in watched},
                "derivation": cur["derivation"],
            })
            continue
        for key in watched:
            if old.get(key) != cur[key]:
                events.append({
                    "kind": f"{key}_changed", "claim": cid,
                    "before": old.get(key), "after": cur[key],
                    "derivation": cur["derivation"],
                })
    for cid in snapshot:
        if cid not in now:
            events.append({"kind": "claim_removed", "claim": cid,
                           "before": {k: snapshot[cid].get(k) for k in watched}})
    return events


def check_documented_transitions(
    topic: Topic, snapshot: Optional[Dict[str, dict]],
) -> List[Violation]:
    """P3 constitution: a light may change only with a documented transition."""
    if snapshot is None:
        return []
    violations = []
    for c in topic.claims:
        old = snapshot.get(c.id)
        if old is None or old["status"] == c.status.name:
            continue
        documented = any(
            h.to_status in (c.status.name, c.status.value)
            for h in c.status_history
        )
        if not documented:
            violations.append(Violation(
                c.id, "undocumented_status_change",
                f"status moved {old['status']} -> {c.status.name} but no "
                f"status_history entry documents this transition — lights may "
                f"change, never silently"))
    return violations


def emit_events(events: List[dict], events_dir: Path = EVENTS_DIR) -> Optional[Path]:
    if not events:
        return None
    events_dir.mkdir(exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = events_dir / f"{stamp}-events.json"
    out.write_text(json.dumps({
        "at": stamp,
        "note": "mechanical diff against the committed snapshot; the trigger "
                "interface for future push channels",
        "events": events,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def commit_snapshot(topic: Topic, path: Path = SNAPSHOT_PATH) -> None:
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({
        "committed_at": dt.datetime.now(dt.timezone.utc)
                          .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claims": current_state(topic),
    }, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: List[str]) -> int:
    from .data.black_hole import BLACK_HOLE

    now = current_state(BLACK_HOLE)
    snapshot = load_snapshot()

    if snapshot is None:
        if "--commit" in argv:
            commit_snapshot(BLACK_HOLE)
            print(f"initial snapshot committed -> {SNAPSHOT_PATH}")
            return 0
        print("no snapshot yet — run with --commit to establish the baseline")
        return 0

    violations = check_documented_transitions(BLACK_HOLE, snapshot)
    for v in violations:
        print(f"VIOLATION {v}")

    events = diff_events(snapshot, now)
    if events:
        out = emit_events(events)
        print(f"{len(events)} change event(s) -> {out}")
        for e in events:
            print(f"  - {e['claim']}: {e['kind']} "
                  f"{e.get('before')!r} -> {e.get('after')!r}")
    else:
        print("stable: no changes against the committed snapshot (zero noise)")

    if "--commit" in argv:
        if violations:
            print("refusing to commit: document the transition in "
                  "status_history first")
            return 1
        commit_snapshot(BLACK_HOLE)
        print(f"snapshot updated -> {SNAPSHOT_PATH}")

    return 1 if violations else 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
