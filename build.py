"""Entrypoint: validate every topic, gate, render.

Order matters and is enforced: the constitution checks run first, and pages are
only written if zero violations remain across ALL topics. A failing validator
blocks the build (non-zero exit) exactly as a failed status review blocks a claim.

Four gates apply, uniformly, to every registered topic:
  v0 — Evidence/Knowledge rules (no unsourced claims, no fake precision, ...)
  vocab — controlled evidence types (P1.5, inside the v0 validator)
  P1 — Data-layer provenance ("cite an arXiv source => you must have fetched it")
  P3 — no silent status changes vs the committed snapshot

P4: this file iterates the topic registry; the engine files are untouched.

    python build.py            # validate all topics + render dist/
    python build.py --check    # validate only
"""

from __future__ import annotations

import sys
from pathlib import Path

from universe_explorer.data.registry import TOPICS
from universe_explorer.provenance import validate_provenance
from universe_explorer.render import (
    app_data_json,
    claims_json,
    render_about,
    render_explore,
    render_index,
    render_topic,
)
from universe_explorer.validator import format_report, validate_topic
from universe_explorer.watch import check_documented_transitions, load_snapshot


def gate(topic) -> list:
    snapshot = load_snapshot()
    return (
        validate_topic(topic)                       # v0 constitution + vocab
        + validate_provenance(topic)                # P1 cite => fetch
        + check_documented_transitions(topic, snapshot)  # P3 no silent changes
    )


def main(argv) -> int:
    check_only = "--check" in argv
    total = 0
    for topic in TOPICS:
        violations = gate(topic)
        print(format_report(topic, violations))
        total += len(violations)
    if total:
        print(f"\nBuild blocked: {total} constitution violation(s) must be zero.")
        return 1
    if check_only:
        return 0

    out_dir = Path(__file__).parent / "dist"
    out_dir.mkdir(exist_ok=True)
    for topic in TOPICS:
        (out_dir / f"{topic.id}.html").write_text(
            render_topic(topic), encoding="utf-8")
    (out_dir / "index.html").write_text(render_index(TOPICS), encoding="utf-8")
    (out_dir / "explore.html").write_text(render_explore(TOPICS), encoding="utf-8")
    (out_dir / "explore-zh.html").write_text(
        render_explore(TOPICS, lang="zh"), encoding="utf-8")
    (out_dir / "claims.json").write_text(claims_json(TOPICS), encoding="utf-8")
    (out_dir / "about.html").write_text(render_about(), encoding="utf-8")
    (out_dir / "about-zh.html").write_text(render_about("zh"), encoding="utf-8")

    # D4: the dynamic frontend — a static source file + a bilingual data payload
    app_src = Path(__file__).parent / "web" / "app.html"
    (out_dir / "app.html").write_text(
        app_src.read_text(encoding="utf-8"), encoding="utf-8")
    (out_dir / "app-data.json").write_text(
        app_data_json(TOPICS), encoding="utf-8")

    # D3: the public push channel — an Atom feed of change events.
    from universe_explorer.dataops.feed import build_feed
    (out_dir / "feed.xml").write_text(build_feed(), encoding="utf-8")

    # single-file Chinese edition (presentation overlay, same data)
    from dataops_artifact import build as build_single
    zh = ('<!doctype html>\n<meta charset="utf-8">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
          + build_single("zh"))
    (out_dir / "zh.html").write_text(zh, encoding="utf-8")

    print(f"\nRendered {len(TOPICS)} topic(s) + index + explore + claims.json "
          f"+ zh.html -> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
