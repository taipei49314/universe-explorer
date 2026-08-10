"""Export module — export claims, search results, and stats in various formats.

Supports JSON, CSV, and Markdown output.

Usage:
    python -m universe_explorer.reader.export --format json
    python -m universe_explorer.reader.export --format csv --domain cosmology
    python -m universe_explorer.reader.export --format markdown --status ESTABLISHED
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Dict, List, Optional

from ..axes import derive, diverges
from ..model import Status, Topic
from .filter_engine import ClaimFilter, FilterCriteria
from .stats import compute_stats

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def export_claims(
    topics: List[Topic],
    fmt: str = "json",
    criteria: Optional[FilterCriteria] = None,
) -> str:
    """Export claims in the specified format.

    Args:
        topics: List of topics to export.
        fmt: Output format ("json", "csv", "markdown").
        criteria: Optional filter criteria.

    Returns:
        Formatted string output.
    """
    filt = ClaimFilter(topics)
    claims = filt.filter(criteria or FilterCriteria())

    if fmt == "json":
        return _export_json(claims)
    elif fmt == "csv":
        return _export_csv(claims)
    elif fmt == "markdown":
        return _export_markdown(claims)
    else:
        raise ValueError(f"Unknown format: {fmt!r}. Use json, csv, or markdown.")


def export_stats(topics: List[Topic], fmt: str = "json") -> str:
    """Export knowledge base statistics.

    Args:
        topics: List of topics.
        fmt: Output format ("json" or "markdown").

    Returns:
        Formatted string output.
    """
    stats = compute_stats(topics)

    if fmt == "json":
        return json.dumps(stats.to_dict(), indent=2, ensure_ascii=False)
    elif fmt == "markdown":
        return _stats_markdown(stats)
    else:
        raise ValueError(f"Unknown format: {fmt!r}. Use json or markdown.")


def _export_json(claims: List[dict]) -> str:
    """Export claims as JSON."""
    return json.dumps(claims, indent=2, ensure_ascii=False)


def _export_csv(claims: List[dict]) -> str:
    """Export claims as CSV."""
    if not claims:
        return ""

    output = io.StringIO()
    fieldnames = [
        "claim_id", "topic_id", "title", "status", "evidence_axis",
        "diverges", "evidence_count", "open_question_count", "has_competing",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for claim in claims:
        writer.writerow(claim)

    return output.getvalue()


def _export_markdown(claims: List[dict]) -> str:
    """Export claims as Markdown table."""
    if not claims:
        return "*No claims match the filter.*\n"

    lines = [
        "| Status | Claim | Domain | Axis | Divergent | Evidence | Open Qs |",
        "|--------|-------|--------|------|-----------|----------|---------|",
    ]

    for c in claims:
        diverge = "⚡" if c["diverges"] else ""
        lines.append(
            f"| {c['status_light']} {c['status']} "
            f"| {c['title'][:50]} "
            f"| {c['topic_id']} "
            f"| {c['evidence_axis']} "
            f"| {diverge} "
            f"| {c['evidence_count']} "
            f"| {c['open_question_count']} |"
        )

    lines.append("")
    lines.append(f"*{len(claims)} claims exported.*")
    return "\n".join(lines)


def _stats_markdown(stats) -> str:
    """Export stats as Markdown."""
    lines = [
        "# Knowledge Base Statistics",
        "",
        f"- **Topics:** {stats.total_topics}",
        f"- **Claims:** {stats.total_claims}",
        f"- **Evidence items:** {stats.total_evidence}",
        f"- **Sources:** {stats.total_sources}",
        f"- **Open questions:** {stats.total_open_questions}",
        "",
        "## Claims by Domain",
        "",
        "| Domain | Claims |",
        "|--------|--------|",
    ]
    for d, c in sorted(stats.claims_by_domain.items()):
        lines.append(f"| {d} | {c} |")

    lines.extend([
        "",
        "## Claims by Status",
        "",
        "| Status | Count |",
        "|--------|-------|",
    ])
    for s, c in sorted(stats.claims_by_status.items()):
        lines.append(f"| {s} | {c} |")

    lines.extend([
        "",
        "## Quality Metrics",
        "",
        f"- **Divergent claims:** {stats.divergent_count}",
        f"- **Competing models:** {stats.competing_count}",
        f"- **Isolated claims:** {stats.isolated_count}",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    from ..data.registry import TOPICS

    parser = argparse.ArgumentParser(description="Export claims")
    parser.add_argument("--format", default="json", choices=["json", "csv", "markdown"])
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--axis", help="Filter by evidence axis")
    parser.add_argument("--stats", action="store_true", help="Export stats instead of claims")
    args = parser.parse_args()

    if args.stats:
        print(export_stats(TOPICS, args.format))
    else:
        criteria = FilterCriteria(
            domain=args.domain,
            status=args.status,
            evidence_axis=args.axis,
        )
        print(export_claims(TOPICS, args.format, criteria))
