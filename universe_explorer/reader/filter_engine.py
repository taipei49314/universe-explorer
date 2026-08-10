"""Multi-dimensional filter engine for claims.

Filters can be combined arbitrarily:
  - domain (topic id)
  - status (Status enum)
  - evidence_axis (E1-E5)
  - diverges (bool)
  - has_open_questions (bool)
  - has_competing_models (bool)
  - evidence_type (str)
  - tag (str) — filter by annotation tag

Usage:
    python -m universe_explorer.reader.filter_engine --domain cosmology --status STRONG
    python -m universe_explorer.reader.filter_engine --tag needs-review
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from ..axes import EvidenceStrength, derive, diverges
from ..model import Claim, Status, Topic


@dataclass
class FilterCriteria:
    """Combine any subset of filters. None means "don't filter on this"."""

    domain: Optional[str] = None
    status: Optional[str] = None           # Status.name
    evidence_axis: Optional[str] = None    # E1-E5
    diverges: Optional[bool] = None
    has_open_questions: Optional[bool] = None
    has_competing_models: Optional[bool] = None
    evidence_type: Optional[str] = None
    tag: Optional[str] = None              # filter by annotation tag
    label: Optional[str] = None            # filter by annotation label
    has_notes: Optional[bool] = None       # filter by whether claim has notes


class ClaimFilter:
    """Filter claims across topics."""

    def __init__(self, topics: List[Topic]):
        self._topics = topics
        self._all_claims: List[tuple] = []  # (topic_id, Claim)
        for t in topics:
            for c in t.claims:
                self._all_claims.append((t.id, c))

    def filter(self, criteria: FilterCriteria) -> List[dict]:
        """Apply filters, return matching claims as dicts."""
        results = []
        for topic_id, claim in self._all_claims:
            if not _matches(claim, topic_id, criteria):
                continue
            d = derive(claim)
            results.append({
                "claim_id": claim.id,
                "topic_id": topic_id,
                "title": claim.title,
                "status": claim.status.name,
                "status_light": claim.status.light,
                "evidence_axis": d.strength.short,
                "diverges": diverges(claim),
                "evidence_count": len(claim.evidence),
                "open_question_count": len(claim.open_questions),
                "has_competing": len(claim.competing_models) > 0,
            })
        return results

    def count_by(self, dimension: str) -> Dict[str, int]:
        """Count claims by a dimension (for filter UI)."""
        counts: Dict[str, int] = {}
        for topic_id, claim in self._all_claims:
            key = _dimension_key(claim, topic_id, dimension)
            if key is not None:
                counts[key] = counts.get(key, 0) + 1
        return counts

    def available_domains(self) -> List[str]:
        return sorted({t.id for t in self._topics})

    def available_statuses(self) -> List[str]:
        return sorted({c.status.name for t in self._topics for c in t.claims})

    def available_axes(self) -> List[str]:
        return sorted({derive(c).strength.short
                       for t in self._topics for c in t.claims})


def _matches(claim: Claim, topic_id: str, c: FilterCriteria) -> bool:
    """Check if a claim matches all specified criteria."""
    if c.domain and topic_id != c.domain:
        return False
    if c.status and claim.status.name != c.status:
        return False
    if c.evidence_axis:
        d = derive(claim)
        if d.strength.short != c.evidence_axis:
            return False
    if c.diverges is not None:
        if diverges(claim) != c.diverges:
            return False
    if c.has_open_questions is not None:
        has = len(claim.open_questions) > 0
        if has != c.has_open_questions:
            return False
    if c.has_competing_models is not None:
        has = len(claim.competing_models) > 0
        if has != c.has_competing_models:
            return False
    if c.evidence_type:
        types = {ev.type for ev in claim.evidence}
        if c.evidence_type not in types:
            return False
    if c.tag:
        from .annotate import ClaimAnnotations
        annotations = ClaimAnnotations()
        if not annotations.has_tag(claim.id, c.tag):
            return False
    if c.label:
        from .annotate import ClaimAnnotations
        annotations = ClaimAnnotations()
        labels = annotations.get_labels(claim.id)
        if c.label not in labels:
            return False
    if c.has_notes is not None:
        from .annotate import ClaimAnnotations
        annotations = ClaimAnnotations()
        notes = annotations.get_notes(claim.id)
        has = len(notes) > 0
        if has != c.has_notes:
            return False
    return True


def _dimension_key(claim: Claim, topic_id: str, dimension: str) -> Optional[str]:
    """Extract a grouping key for count_by."""
    if dimension == "domain":
        return topic_id
    if dimension == "status":
        return claim.status.name
    if dimension == "evidence_axis":
        return derive(claim).strength.short
    if dimension == "diverges":
        return str(diverges(claim))
    if dimension == "evidence_type":
        return ", ".join(sorted({ev.type for ev in claim.evidence}))
    return None


if __name__ == "__main__":
    import argparse
    from ..data.registry import TOPICS

    parser = argparse.ArgumentParser(description="Filter claims")
    parser.add_argument("--domain", help="Topic id")
    parser.add_argument("--status", help="Status name")
    parser.add_argument("--axis", help="Evidence axis (E1-E5)")
    parser.add_argument("--diverges", type=lambda x: x.lower() == "true",
                        help="Only divergent claims")
    parser.add_argument("--tag", help="Filter by annotation tag")
    parser.add_argument("--label", help="Filter by annotation label")
    parser.add_argument("--has-notes", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has notes")
    parser.add_argument("--has-competing", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has competing models")
    args = parser.parse_args()

    f = ClaimFilter(TOPICS)
    criteria = FilterCriteria(
        domain=args.domain,
        status=args.status,
        evidence_axis=args.axis,
        diverges=args.diverges,
        tag=args.tag,
        label=args.label,
        has_notes=args.has_notes,
        has_competing_models=args.has_competing,
    )
    results = f.filter(criteria)
    print(f"Filter: {len(results)} claims")
    for r in results:
        print(f"  {r['status_light']} [{r['claim_id']}] {r['title']} "
              f"({r['evidence_axis']})")
