"""Health check — verify integrity of all system components.

Checks:
  - Constitution: all claims pass validator
  - Provenance: all sources are fetchable and verified
  - Relations: all edges reference valid claims
  - Annotations: all annotation files are valid JSON
  - Reviews: all review files are valid JSON
  - Cache: search index cache is consistent
  - Discovery: all candidates are valid JSON
  - Cross-domain: graph is consistent

Usage:
    python -m universe_explorer.reader.health
    python -m universe_explorer.reader.health --verbose
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from ..model import Topic
from ..validator import validate_topic
from ..provenance import validate_provenance
from ..relations import all_links, validate_links

_ROOT = Path(__file__).parent.parent.parent
_ANNOTATIONS_DIR = _ROOT / "annotations"
_REVIEWS_DIR = _ROOT / "reviews"
_CACHE_DIR = _ROOT / "cache" / "search_index"
_CANDIDATES_DIR = _ROOT / "candidates" / "structured"


@dataclass
class HealthCheck:
    """Result of a health check."""

    component: str
    status: str           # "ok", "warning", "error"
    message: str
    details: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "component": self.component,
            "status": self.status,
            "message": self.message,
            "details": self.details,
        }


def run_health_checks(topics: List[Topic], verbose: bool = False) -> List[HealthCheck]:
    """Run all health checks."""
    checks = []
    checks.extend(_check_constitution(topics))
    checks.extend(_check_provenance(topics))
    checks.extend(_check_relations(topics))
    checks.extend(_check_annotations())
    checks.extend(_check_reviews())
    checks.extend(_check_cache())
    checks.extend(_check_candidates())
    return checks


def _check_constitution(topics: List[Topic]) -> List[HealthCheck]:
    """Check that all claims pass the constitution."""
    violations = []
    for topic in topics:
        topic_violations = validate_topic(topic)
        violations.extend(topic_violations)

    if violations:
        return [HealthCheck(
            component="constitution",
            status="error",
            message=f"{len(violations)} constitution violation(s)",
            details=[str(v) for v in violations[:10]],
        )]
    return [HealthCheck(
        component="constitution",
        status="ok",
        message=f"All {sum(len(t.claims) for t in topics)} claims pass",
    )]


def _check_provenance(topics: List[Topic]) -> List[HealthCheck]:
    """Check that all sources are fetchable and verified."""
    violations = []
    for topic in topics:
        topic_violations = validate_provenance(topic)
        violations.extend(topic_violations)

    if violations:
        return [HealthCheck(
            component="provenance",
            status="error",
            message=f"{len(violations)} provenance violation(s)",
            details=[str(v) for v in violations[:10]],
        )]
    return [HealthCheck(
        component="provenance",
        status="ok",
        message="All sources verified",
    )]


def _check_relations(topics: List[Topic]) -> List[HealthCheck]:
    """Check that all edges reference valid claims."""
    violations = validate_links(topics)

    if violations:
        return [HealthCheck(
            component="relations",
            status="warning",
            message=f"{len(violations)} relation issue(s)",
            details=violations[:10],
        )]
    return [HealthCheck(
        component="relations",
        status="ok",
        message="All edges valid",
    )]


def _check_annotations() -> List[HealthCheck]:
    """Check that all annotation files are valid JSON."""
    if not _ANNOTATIONS_DIR.exists():
        return [HealthCheck(
            component="annotations",
            status="ok",
            message="No annotations directory",
        )]

    errors = []
    total = 0
    for claim_dir in _ANNOTATIONS_DIR.iterdir():
        if not claim_dir.is_dir():
            continue
        for f in claim_dir.glob("*.json"):
            total += 1
            try:
                json.loads(f.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(f"{f.name}: {e}")

    if errors:
        return [HealthCheck(
            component="annotations",
            status="error",
            message=f"{len(errors)} invalid annotation file(s)",
            details=errors[:10],
        )]
    return [HealthCheck(
        component="annotations",
        status="ok",
        message=f"{total} annotation file(s) valid",
    )]


def _check_reviews() -> List[HealthCheck]:
    """Check that all review files are valid JSON."""
    if not _REVIEWS_DIR.exists():
        return [HealthCheck(
            component="reviews",
            status="ok",
            message="No reviews directory",
        )]

    errors = []
    total = 0
    for f in _REVIEWS_DIR.glob("*.json"):
        total += 1
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            required = {"claim_id", "status", "items"}
            missing = required - set(data.keys())
            if missing:
                errors.append(f"{f.name}: missing fields {missing}")
        except Exception as e:
            errors.append(f"{f.name}: {e}")

    if errors:
        return [HealthCheck(
            component="reviews",
            status="error",
            message=f"{len(errors)} invalid review file(s)",
            details=errors[:10],
        )]
    return [HealthCheck(
        component="reviews",
        status="ok",
        message=f"{total} review file(s) valid",
    )]


def _check_cache() -> List[HealthCheck]:
    """Check that search index cache is consistent."""
    if not _CACHE_DIR.exists():
        return [HealthCheck(
            component="cache",
            status="ok",
            message="No cache directory",
        )]

    errors = []
    total = 0
    for f in _CACHE_DIR.glob("*.json"):
        total += 1
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if "index" not in data:
                errors.append(f"{f.name}: missing 'index' key")
        except Exception as e:
            errors.append(f"{f.name}: {e}")

    if errors:
        return [HealthCheck(
            component="cache",
            status="warning",
            message=f"{len(errors)} invalid cache file(s)",
            details=errors[:10],
        )]
    return [HealthCheck(
        component="cache",
        status="ok",
        message=f"{total} cache file(s) valid",
    )]


def _check_candidates() -> List[HealthCheck]:
    """Check that all candidate files are valid JSON."""
    if not _CANDIDATES_DIR.exists():
        return [HealthCheck(
            component="candidates",
            status="ok",
            message="No candidates directory",
        )]

    errors = []
    total = 0
    for topic_dir in _CANDIDATES_DIR.iterdir():
        if not topic_dir.is_dir():
            continue
        for f in topic_dir.glob("*.json"):
            total += 1
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                required = {"id", "sources", "evidence"}
                missing = required - set(data.keys())
                if missing:
                    errors.append(f"{f.name}: missing fields {missing}")
            except Exception as e:
                errors.append(f"{f.name}: {e}")

    if errors:
        return [HealthCheck(
            component="candidates",
            status="error",
            message=f"{len(errors)} invalid candidate file(s)",
            details=errors[:10],
        )]
    return [HealthCheck(
        component="candidates",
        status="ok",
        message=f"{total} candidate file(s) valid",
    )]


def format_health_report(checks: List[HealthCheck]) -> str:
    """Human-readable health report."""
    lines = ["Health Check Report", "=" * 40]

    ok_count = sum(1 for c in checks if c.status == "ok")
    warn_count = sum(1 for c in checks if c.status == "warning")
    error_count = sum(1 for c in checks if c.status == "error")

    lines.append(f"OK: {ok_count}  Warning: {warn_count}  Error: {error_count}")
    lines.append("")

    for check in checks:
        icon = {"ok": "✓", "warning": "⚠", "error": "✗"}[check.status]
        lines.append(f"  {icon} {check.component}: {check.message}")
        if check.details:
            for detail in check.details[:5]:
                lines.append(f"    - {detail}")

    if error_count > 0:
        lines.append("")
        lines.append("RESULT: FAIL — errors must be fixed before build.")
    elif warn_count > 0:
        lines.append("")
        lines.append("RESULT: PASS with warnings.")
    else:
        lines.append("")
        lines.append("RESULT: ALL GREEN.")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    from ..data.registry import TOPICS

    parser = argparse.ArgumentParser(description="Health check")
    parser.add_argument("--verbose", action="store_true", help="Show all details")
    args = parser.parse_args()

    checks = run_health_checks(TOPICS, verbose=args.verbose)
    print(format_health_report(checks))
