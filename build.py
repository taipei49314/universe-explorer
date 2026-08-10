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

    # D4: the dynamic frontends — static source files + a bilingual payload
    web = Path(__file__).parent / "web"
    for page in ("app.html", "universe.html"):
        (out_dir / page).write_text(
            (web / page).read_text(encoding="utf-8"), encoding="utf-8")
    (out_dir / "app-data.json").write_text(
        app_data_json(TOPICS), encoding="utf-8")

    # P-Pulse / P-Audit: changes + health surface pages
    from universe_explorer.surface import write_surface_pages
    write_surface_pages(out_dir, TOPICS)

    # D3: the public push channel — an Atom feed of change events.
    from universe_explorer.dataops.feed import build_feed
    (out_dir / "feed.xml").write_text(build_feed(), encoding="utf-8")

    # single-file Chinese edition (presentation overlay, same data)
    from dataops_artifact import build as build_single
    zh = ('<!doctype html>\n<meta charset="utf-8">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
          + build_single("zh"))
    (out_dir / "zh.html").write_text(zh, encoding="utf-8")

    # Phase 1: Discovery review dashboard
    from universe_explorer.discovery.review import generate_review_dashboard
    generate_review_dashboard(dist_dir=out_dir)

    # Phase 2: Cross-domain epistemic map + graph JSON
    from universe_explorer.crossdomain.graph_builder import build_cross_domain_graph
    from universe_explorer.crossdomain.render_map import render_epistemic_map
    import json
    graph = build_cross_domain_graph(TOPICS)
    render_epistemic_map(graph, dist_dir=out_dir)
    (out_dir / "epistemic-graph.json").write_text(
        json.dumps(graph.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8")

    # Phase 3: Reader experience pages
    from universe_explorer.reader.render_explore import render_explore_v2
    from universe_explorer.reader.challenge_form import generate_challenge_form
    from universe_explorer.reader.dual_axis_viz import generate_dual_axis_svg
    render_explore_v2(TOPICS, dist_dir=out_dir)
    generate_challenge_form(dist_dir=out_dir)
    (out_dir / "dual-axis.svg").write_text(
        generate_dual_axis_svg(TOPICS), encoding="utf-8")

    # Dashboard: central hub linking all pages
    from universe_explorer.reader.dashboard import render_dashboard
    render_dashboard(TOPICS, dist_dir=out_dir)

    # Stats: knowledge base statistics JSON
    from universe_explorer.reader.stats import compute_stats
    import json
    stats = compute_stats(TOPICS)
    (out_dir / "stats.json").write_text(
        json.dumps(stats.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8")

    # Health check validation gate
    from universe_explorer.reader.health_check import run_health_checks
    health_checks = run_health_checks(TOPICS)
    health_errors = sum(1 for c in health_checks if c.status == "error")
    if health_errors > 0:
        print(f"\nBuild blocked: {health_errors} health check error(s).")
        for c in health_checks:
            if c.status == "error":
                print(f"  ✗ {c.component}: {c.message}")
        return 1

    # Automation metrics
    from universe_explorer.reader.automation_metrics import compute_metrics
    metrics = compute_metrics()
    (out_dir / "automation-metrics.json").write_text(
        json.dumps(metrics.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8")

    # API documentation
    from universe_explorer.reader.api_docs import generate_api_docs
    generate_api_docs(dist_dir=out_dir)

    # Changelog
    from universe_explorer.reader.changelog import generate_changelog
    changelog = generate_changelog()
    (out_dir / "CHANGELOG.md").write_text(changelog, encoding="utf-8")

    # Sitemap
    from universe_explorer.reader.sitemap import generate_sitemap
    sitemap = generate_sitemap()
    (out_dir / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    print(f"\nRendered {len(TOPICS)} topic(s) + index + explore + claims.json "
          f"+ zh.html + discovery/crossdomain/reader/dashboard/stats pages -> {out_dir}")
    print(f"Health: all green. Automation: {metrics.automation_rate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
