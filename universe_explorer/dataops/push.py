"""P5 (partial) — the push channel: events -> human-readable digest.

Turns the mechanical event files that watch emits into a digest a subscriber
could receive. Constitution applies all the way down the pipe:

  * a digest line only restates its event — before/after values and the claim
    it belongs to. No interpretation, no urgency language, no "breakthrough!";
  * every digest line names the event file it came from, which itself carries
    the mechanical derivation — the push is traceable back to evidence;
  * no events => no digest. The channel is silent when knowledge is stable.

Channels: the default writes digests to outbox/ (files ARE the interface — an
email/webhook sender later just picks them up). Real transport (SMTP, webhook
POST) is deliberately not wired here: sending is deployment, digesting is model.

Usage:
    python -m universe_explorer.dataops.push          # digest all new events
    python -m universe_explorer.dataops.push --all    # re-digest everything
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import List

from ..watch import EVENTS_DIR

OUTBOX_DIR = Path(__file__).parent.parent.parent / "outbox"
STATE_FILE = OUTBOX_DIR / ".digested.json"

_KIND_TEXT = {
    "claim_added": "new claim recorded",
    "claim_removed": "claim removed",
    "status_changed": "status light moved",
    "evidence_axis_changed": "evidence axis moved",
    "evidence_items_changed": "evidence count changed",
    "sources_changed": "source count changed",
    "diverges_changed": "axis divergence changed",
}


def _digested() -> set:
    if STATE_FILE.exists():
        return set(json.loads(STATE_FILE.read_text(encoding="utf-8")))
    return set()


def _mark_digested(names: List[str]) -> None:
    OUTBOX_DIR.mkdir(exist_ok=True)
    done = _digested() | set(names)
    STATE_FILE.write_text(json.dumps(sorted(done)), encoding="utf-8")


def render_digest(event_files: List[Path]) -> str:
    """Restate events, never interpret them."""
    lines = [
        "UNIVERSE EXPLORER — change digest",
        "(mechanical restatement of recorded state changes; every line names "
        "its event file, which carries the derivation back to the evidence)",
        "",
    ]
    for ef in event_files:
        payload = json.loads(ef.read_text(encoding="utf-8"))
        lines.append(f"== {payload['at']}  ({ef.name})")
        for e in payload["events"]:
            kind = _KIND_TEXT.get(e["kind"], e["kind"])
            if e["kind"] == "claim_added":
                after = e["after"]
                lines.append(
                    f"  * {e['claim']}: {kind} — status {after['status']}, "
                    f"evidence axis {after['evidence_axis']}")
            elif "before" in e and "after" in e:
                lines.append(
                    f"  * {e['claim']}: {kind} — "
                    f"{e['before']!r} -> {e['after']!r}")
            else:
                lines.append(f"  * {e['claim']}: {kind}")
        lines.append("")
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    if not EVENTS_DIR.exists():
        print("no events directory — nothing to digest")
        return 0

    all_events = sorted(EVENTS_DIR.glob("*-events.json"))
    todo = (all_events if "--all" in argv
            else [f for f in all_events if f.name not in _digested()])
    if not todo:
        print("no new events — the channel stays silent (zero noise)")
        return 0

    digest = render_digest(todo)
    OUTBOX_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUTBOX_DIR / f"{stamp}-digest.txt"
    out.write_text(digest, encoding="utf-8")
    _mark_digested([f.name for f in todo])
    print(f"digest of {len(todo)} event file(s) -> {out}")
    print()
    print(digest)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
