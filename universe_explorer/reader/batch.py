"""Batch operations — perform bulk actions on claims.

Supports:
  - Bulk export (JSON, CSV, Markdown)
  - Bulk annotation (tags, notes)
  - Bulk review start
  - Bulk statistics generation

Usage:
    python -m universe_explorer.reader.batch --export --format json
    python -m universe_explorer.reader.batch --tag needs-review --domain cosmology
    python -m universe_explorer.reader.batch --review --checklist new_claim
    python -m universe_explorer.reader.batch --stats --format markdown
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from ..model import Topic
from .annotate import ClaimAnnotations
from .export import export_claims, export_stats
from .filter_engine import ClaimFilter, FilterCriteria
from .review import ReviewManager
from .stats import compute_stats

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def batch_export(
    topics: List[Topic],
    fmt: str = "json",
    criteria: Optional[FilterCriteria] = None,
    output_dir: Optional[Path] = None,
) -> Path:
    """Export claims to a file."""
    if output_dir is None:
        output_dir = _DIST_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    content = export_claims(topics, fmt, criteria)
    ext = {"json": "json", "csv": "csv", "markdown": "md"}[fmt]
    out_path = output_dir / f"export.{ext}"
    out_path.write_text(content, encoding="utf-8")
    print(f"[batch] Exported to {out_path}")
    return out_path


def batch_tag(
    topics: List[Topic],
    tag: str,
    criteria: Optional[FilterCriteria] = None,
) -> int:
    """Add a tag to all claims matching criteria."""
    filt = ClaimFilter(topics)
    claims = filt.filter(criteria or FilterCriteria())
    annotations = ClaimAnnotations()

    count = 0
    for claim in claims:
        annotations.add_tag(claim["claim_id"], tag)
        count += 1

    print(f"[batch] Tagged {count} claims with '{tag}'")
    return count


def batch_review(
    topics: List[Topic],
    checklist_type: str = "default",
    criteria: Optional[FilterCriteria] = None,
) -> int:
    """Start reviews for all claims matching criteria."""
    filt = ClaimFilter(topics)
    claims = filt.filter(criteria or FilterCriteria())
    manager = ReviewManager()

    count = 0
    for claim in claims:
        manager.start_review(claim["claim_id"], checklist_type)
        count += 1

    print(f"[batch] Started {count} reviews with checklist '{checklist_type}'")
    return count


def batch_stats(
    topics: List[Topic],
    fmt: str = "json",
    output_dir: Optional[Path] = None,
) -> Path:
    """Generate statistics to a file."""
    if output_dir is None:
        output_dir = _DIST_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    content = export_stats(topics, fmt)
    ext = {"json": "json", "markdown": "md"}[fmt]
    out_path = output_dir / f"stats.{ext}"
    out_path.write_text(content, encoding="utf-8")
    print(f"[batch] Stats exported to {out_path}")
    return out_path


def batch_summary(topics: List[Topic]) -> dict:
    """Generate a summary of all batch operations."""
    stats = compute_stats(topics)
    annotations = ClaimAnnotations()
    manager = ReviewManager()

    # Count annotations.
    all_tags = annotations.list_all_tags()
    total_tags = sum(len(tags) for tags in all_tags.values())

    # Count reviews.
    reviews = manager.list_reviews()
    approved = sum(1 for r in reviews if r["status"] == "approved")
    rejected = sum(1 for r in reviews if r["status"] == "rejected")
    in_progress = sum(1 for r in reviews if r["status"] == "in-progress")

    return {
        "claims": stats.total_claims,
        "domains": stats.total_topics,
        "evidence": stats.total_evidence,
        "sources": stats.total_sources,
        "annotations": {
            "total_tags": total_tags,
            "claims_with_tags": len(all_tags),
        },
        "reviews": {
            "total": len(reviews),
            "approved": approved,
            "rejected": rejected,
            "in_progress": in_progress,
        },
    }


if __name__ == "__main__":
    import argparse
    from ..data.registry import TOPICS

    parser = argparse.ArgumentParser(description="Batch operations")
    parser.add_argument("--export", action="store_true", help="Export claims")
    parser.add_argument("--format", default="json", choices=["json", "csv", "markdown"])
    parser.add_argument("--tag", help="Add tag to filtered claims")
    parser.add_argument("--review", action="store_true", help="Start reviews")
    parser.add_argument("--checklist", default="default", help="Review checklist type")
    parser.add_argument("--stats", action="store_true", help="Export statistics")
    parser.add_argument("--summary", action="store_true", help="Show summary")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--axis", help="Filter by evidence axis")
    parser.add_argument("--filter-tag", help="Filter by annotation tag")
    parser.add_argument("--filter-label", help="Filter by annotation label")
    parser.add_argument("--filter-has-notes", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has notes")
    args = parser.parse_args()

    criteria = FilterCriteria(
        domain=args.domain,
        status=args.status,
        evidence_axis=args.axis,
        tag=args.filter_tag,
        label=args.filter_label,
        has_notes=args.filter_has_notes,
    )

    if args.export:
        batch_export(TOPICS, args.format, criteria)
    elif args.tag:
        batch_tag(TOPICS, args.tag, criteria)
    elif args.review:
        batch_review(TOPICS, args.checklist, criteria)
    elif args.stats:
        batch_stats(TOPICS, args.format)
    elif args.summary:
        summary = batch_summary(TOPICS)
        print(json.dumps(summary, indent=2))
    else:
        parser.print_help()
