"""Unified CLI entry point for Universe Explorer.

Usage:
    python -m universe_explorer <command> [args...]

Commands:
    build           Validate + render site to dist/
    build --check   Validate only
    search <query>  Full-text search over claims
    filter [opts]   Filter claims by domain/status/axis
    stats           Show knowledge base statistics
    paths           List all reading paths
    discover <q>    Run discovery pipeline
    graph           Build cross-domain graph
    health          Run health checks on all components
    help            Show this help

Examples:
    python -m universe_explorer build
    python -m universe_explorer search "black hole"
    python -m universe_explorer filter --domain cosmology --status STRONG
    python -m universe_explorer stats
    python -m universe_explorer discover "gravitational wave" --topic cosmology
    python -m universe_explorer health
"""

from __future__ import annotations

import sys


def main(argv: list = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] in ("help", "--help", "-h"):
        print(__doc__)
        return 0

    cmd = argv[0]
    args = argv[1:]

    if cmd == "build":
        from build import main as build_main
        return build_main(args)

    if cmd == "search":
        if not args:
            print("usage: python -m universe_explorer search <query>")
            return 1
        from .data.registry import TOPICS
        from .reader.search_index import ClaimSearchIndex
        index = ClaimSearchIndex(TOPICS)
        results = index.search(" ".join(args))
        print(f"Search: {' '.join(args)!r} — {len(results)} result(s)")
        for r in results[:20]:
            print(f"  [{r.claim_id}] {r.title} (score={r.score})")
        return 0

    if cmd == "filter":
        from .data.registry import TOPICS
        from .reader.filter_engine import ClaimFilter, FilterCriteria
        import argparse
        p = argparse.ArgumentParser(description="Filter claims")
        p.add_argument("--domain", help="Topic id")
        p.add_argument("--status", help="Status name")
        p.add_argument("--axis", help="Evidence axis (E1-E5)")
        p.add_argument("--diverges", type=lambda x: x.lower() == "true")
        p.add_argument("--tag", help="Filter by annotation tag")
        p.add_argument("--label", help="Filter by annotation label")
        p.add_argument("--has-notes", type=lambda x: x.lower() == "true")
        opts = p.parse_args(args)
        f = ClaimFilter(TOPICS)
        criteria = FilterCriteria(
            domain=opts.domain, status=opts.status,
            evidence_axis=opts.axis, diverges=opts.diverges,
            tag=opts.tag, label=opts.label, has_notes=opts.has_notes,
        )
        results = f.filter(criteria)
        print(f"Filter: {len(results)} claims")
        for r in results[:20]:
            print(f"  {r['status_light']} [{r['claim_id']}] {r['title']} ({r['evidence_axis']})")
        return 0

    if cmd == "stats":
        from .data.registry import TOPICS
        from .reader.stats import compute_stats, format_stats_report
        stats = compute_stats(TOPICS)
        print(format_stats_report(stats))
        return 0

    if cmd == "paths":
        from .data.registry import TOPICS
        from .reader.guided_reading import GuidedReader
        reader = GuidedReader(TOPICS)
        paths = reader.list_paths()
        print(f"Reading paths: {len(paths)}")
        for p in paths:
            src = p.get('source', 'authored')
            kind = p.get('kind', '')
            label = f" [{kind}]" if kind else ""
            print(f"  [{p['index']}] {p['title']} ({len(p['claim_ids'])} claims) [{src}]{label}")
        return 0

    if cmd == "discover":
        from .discovery.pipeline import run_pipeline
        import argparse
        p = argparse.ArgumentParser(description="Discovery pipeline")
        p.add_argument("query", help="Search query")
        p.add_argument("--topic", required=True, help="Target topic id")
        p.add_argument("--adapter", default="arxiv")
        p.add_argument("--max", type=int, default=10)
        opts = p.parse_args(args)
        run_pipeline(opts.query, opts.topic, opts.adapter, opts.max)
        return 0

    if cmd == "graph":
        from .data.registry import TOPICS
        from .crossdomain.graph_builder import build_cross_domain_graph, format_graph_report
        graph = build_cross_domain_graph(TOPICS)
        print(format_graph_report(graph))
        return 0

    if cmd == "health":
        from .data.registry import TOPICS
        from .reader.health_check import run_health_checks, format_health_report
        checks = run_health_checks(TOPICS, verbose="--verbose" in args)
        print(format_health_report(checks))
        errors = sum(1 for c in checks if c.status == "error")
        return 1 if errors > 0 else 0

    print(f"Unknown command: {cmd!r}. Run 'python -m universe_explorer help' for usage.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
