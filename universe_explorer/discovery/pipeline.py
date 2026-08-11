"""Discovery pipeline — end-to-end orchestrator.

Runs the full discovery flow:
  1. Source adapter search → RawResult list
  2. Candidate builder → structured candidate per result
  3. Constitution precheck → PrecheckReport per candidate
  4. Review dashboard → dist/review.html

Usage:
    # Full pipeline: search → candidates → precheck → review.html
    python -m universe_explorer.discovery.pipeline "gravitational wave" --topic cosmology

    # With adapter selection
    python -m universe_explorer.discovery.pipeline "dark energy" --topic cosmology --adapter arxiv

    # Limit results
    python -m universe_explorer.discovery.pipeline "exoplanet" --topic exoplanets --max 5
"""

from __future__ import annotations

import json
import socket
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Set

from .adapters.arxiv_adapter import ArxivAdapter
from .adapters.base import SourceAdapter
from .adapters.doi_adapter import DoiAdapter
from .adapters.nasa_adapter import NasaAdapter
from .candidate_builder import build_candidate, list_candidates
from .precheck import PrecheckReport, format_precheck_report, precheck
from .review import generate_review_dashboard

# Registry of available adapters.
ADAPTERS: Dict[str, SourceAdapter] = {
    "arxiv": ArxivAdapter(),
    "doi": DoiAdapter(),
    "nasa": NasaAdapter(),
}


class DiscoveryError(Exception):
    """User-facing discovery failure (bad args or network). Not a traceback path."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def get_adapter(name: str) -> SourceAdapter:
    if name not in ADAPTERS:
        raise DiscoveryError(
            f"unknown adapter: {name!r} (available: {sorted(ADAPTERS)})"
        )
    return ADAPTERS[name]


def _known_topic_ids() -> Set[str]:
    try:
        from ..data.registry import TOPICS
        return {t.id for t in TOPICS}
    except Exception:
        return set()


def run_pipeline(
    query: str,
    topic_id: str,
    adapter_name: str = "arxiv",
    max_results: int = 10,
    claim_id_prefix: str = "",
) -> dict:
    """Run the full discovery pipeline.

    Returns a report dict with:
      - query, topic_id, adapter
      - results: list of {candidate, precheck}
      - review_path: path to generated review.html

    Raises:
        DiscoveryError: unknown topic/adapter, or network/search failure.
            Callers (CLI) should print ``e.message`` and exit 1 — never dump
            a raw stack to a casual user for expected failures.
    """
    # Validate topic before any network call.
    known = _known_topic_ids()
    if known and topic_id not in known:
        raise DiscoveryError(
            f"unknown topic: {topic_id!r} (available: {sorted(known)})"
        )

    adapter = get_adapter(adapter_name)
    print(f"[pipeline] query={query!r} topic={topic_id} adapter={adapter_name}")

    # 1. Search (network failures become DiscoveryError, not traceback).
    try:
        raw_results = adapter.search(query, max_results=max_results)
    except DiscoveryError:
        raise
    except (urllib.error.URLError, socket.timeout, TimeoutError, OSError) as e:
        raise DiscoveryError(
            f"discovery search failed ({adapter_name}): {e}. "
            "Check network access to the source API, or retry later. "
            "No candidates were written."
        ) from e
    except Exception as e:
        raise DiscoveryError(
            f"discovery search failed ({adapter_name}): {type(e).__name__}: {e}. "
            "No candidates were written."
        ) from e

    if not raw_results:
        print("[pipeline] no results — nothing to do")
        return {
            "query": query, "topic_id": topic_id, "adapter": adapter_name,
            "results": [], "review_path": None,
        }

    # 2. Build candidates + precheck.
    items = []
    for i, result in enumerate(raw_results):
        cid = claim_id_prefix or _make_claim_id(result.title, topic_id, i)
        print(f"\n[pipeline] --- candidate {i+1}/{len(raw_results)}: {cid} ---")

        candidate = build_candidate(
            topic_id=topic_id,
            claim_id=cid,
            adapter=adapter,
            source_refs=[result.source_ref],
            title=result.title,
        )

        report = precheck(candidate)
        print(format_precheck_report(report))

        items.append({
            "candidate": candidate,
            "precheck": report.to_dict(),
        })

    # 3. Generate review dashboard.
    review_path = generate_review_dashboard()

    pipeline_report = {
        "query": query,
        "topic_id": topic_id,
        "adapter": adapter_name,
        "results": items,
        "review_path": str(review_path),
    }

    # Write report to disk.
    report_dir = Path(__file__).parent.parent.parent / "candidates"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"pipeline-{topic_id}.json"
    report_path.write_text(
        json.dumps(pipeline_report, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"\n[pipeline] report -> {report_path}")
    print(f"[pipeline] review -> {review_path}")

    return pipeline_report


def _make_claim_id(title: str, topic_id: str, index: int) -> str:
    """Generate a claim id from title. Keeps it short and slug-like."""
    import re
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:40]
    return f"{topic_id}_{slug}_{index}"


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Discovery pipeline: search → candidates → precheck → review")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--topic", required=True, help="Target topic id")
    parser.add_argument("--adapter", default="arxiv",
                        help="Source adapter (default: arxiv)")
    parser.add_argument("--max", type=int, default=10,
                        help="Max results (default: 10)")
    parser.add_argument("--prefix", default="",
                        help="Claim id prefix (auto-generated if empty)")
    args = parser.parse_args()

    try:
        run_pipeline(
            query=args.query,
            topic_id=args.topic,
            adapter_name=args.adapter,
            max_results=args.max,
            claim_id_prefix=args.prefix,
        )
    except DiscoveryError as e:
        print(f"error: {e.message}", file=sys.stderr)
        raise SystemExit(1)
