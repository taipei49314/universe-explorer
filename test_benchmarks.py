"""Performance benchmarks — track performance over time.

Measures:
  - Search latency (91 claims)
  - Filter latency (91 claims)
  - Stats computation latency
  - Graph build latency
  - Validation latency
  - Build latency

Usage:
    python test_benchmarks.py --benchmark
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from universe_explorer.data.registry import TOPICS
from universe_explorer.validator import validate_topic
from universe_explorer.reader.search_index import ClaimSearchIndex
from universe_explorer.reader.filter_engine import ClaimFilter, FilterCriteria
from universe_explorer.reader.stats import compute_stats
from universe_explorer.crossdomain.graph_builder import build_cross_domain_graph


# Performance limits (milliseconds).
LIMITS = {
    "search_10x": 100,      # 10 searches in < 100ms
    "filter_10x": 50,       # 10 filters in < 50ms
    "stats_10x": 100,       # 10 stats in < 100ms
    "graph_1x": 1000,       # 1 graph build in < 1000ms
    "validate_all_1x": 1000, # 1 full validation in < 1000ms
}


class TestPerformanceBenchmarks:
    """Performance benchmarks with hard limits."""

    def test_search_latency(self):
        """Search should be fast."""
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        start = time.time()
        for _ in range(10):
            index.search("black hole")
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < LIMITS["search_10x"], \
            f"Search too slow: {elapsed_ms:.1f}ms (limit: {LIMITS['search_10x']}ms)"

    def test_filter_latency(self):
        """Filter should be fast."""
        filt = ClaimFilter(TOPICS)
        start = time.time()
        for _ in range(10):
            filt.filter(FilterCriteria())
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < LIMITS["filter_10x"], \
            f"Filter too slow: {elapsed_ms:.1f}ms (limit: {LIMITS['filter_10x']}ms)"

    def test_stats_latency(self):
        """Stats computation should be fast."""
        start = time.time()
        for _ in range(10):
            compute_stats(TOPICS)
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < LIMITS["stats_10x"], \
            f"Stats too slow: {elapsed_ms:.1f}ms (limit: {LIMITS['stats_10x']}ms)"

    def test_graph_build_latency(self):
        """Graph build should be fast."""
        start = time.time()
        build_cross_domain_graph(TOPICS)
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < LIMITS["graph_1x"], \
            f"Graph build too slow: {elapsed_ms:.1f}ms (limit: {LIMITS['graph_1x']}ms)"

    def test_validation_latency(self):
        """Validation should be fast."""
        start = time.time()
        for topic in TOPICS:
            validate_topic(topic)
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < LIMITS["validate_all_1x"], \
            f"Validation too slow: {elapsed_ms:.1f}ms (limit: {LIMITS['validate_all_1x']}ms)"


class TestBenchmarkReport:
    """Generate benchmark report."""

    def test_benchmark_report(self):
        """Generate benchmark report for reference."""
        report = {}

        # Search benchmark.
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        start = time.time()
        for _ in range(10):
            index.search("black hole")
        report["search_10x_ms"] = round((time.time() - start) * 1000, 1)

        # Filter benchmark.
        filt = ClaimFilter(TOPICS)
        start = time.time()
        for _ in range(10):
            filt.filter(FilterCriteria())
        report["filter_10x_ms"] = round((time.time() - start) * 1000, 1)

        # Stats benchmark.
        start = time.time()
        for _ in range(10):
            compute_stats(TOPICS)
        report["stats_10x_ms"] = round((time.time() - start) * 1000, 1)

        # Graph benchmark.
        start = time.time()
        build_cross_domain_graph(TOPICS)
        report["graph_1x_ms"] = round((time.time() - start) * 1000, 1)

        # Validation benchmark.
        start = time.time()
        for topic in TOPICS:
            validate_topic(topic)
        report["validate_all_1x_ms"] = round((time.time() - start) * 1000, 1)

        # Write report.
        bench_dir = Path(__file__).parent / "benchmarks"
        bench_dir.mkdir(exist_ok=True)
        out = bench_dir / "latest.json"
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")

        # All should be within limits.
        assert report["search_10x_ms"] < LIMITS["search_10x"]
        assert report["filter_10x_ms"] < LIMITS["filter_10x"]
        assert report["stats_10x_ms"] < LIMITS["stats_10x"]
        assert report["graph_1x_ms"] < LIMITS["graph_1x"]
        assert report["validate_all_1x_ms"] < LIMITS["validate_all_1x"]
