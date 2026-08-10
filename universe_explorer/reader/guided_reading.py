"""Guided reading — navigate claims along reading paths.

Wraps the existing reading paths from relations.py into a guided
exploration experience with context at each step.

Usage:
    python -m universe_explorer.reader.guided_reading --path 0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ..axes import derive, diverges
from ..model import Claim, Topic
from ..relations import reading_paths, all_links


@dataclass
class ReadingStep:
    """One step in a guided reading path."""

    claim_id: str
    topic_id: str
    title: str
    status: str
    status_light: str
    evidence_axis: str
    diverges: bool
    summary: str           # first evidence description
    open_questions: List[str]
    related: List[dict]    # neighbor claims

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "topic_id": self.topic_id,
            "title": self.title,
            "status": self.status,
            "status_light": self.status_light,
            "evidence_axis": self.evidence_axis,
            "diverges": self.diverges,
            "summary": self.summary,
            "open_questions": self.open_questions,
            "related": self.related,
        }


class GuidedReader:
    """Navigate claims along reading paths."""

    def __init__(self, topics: List[Topic]):
        self._topics = topics
        self._claim_map: Dict[str, tuple] = {}
        for t in topics:
            for c in t.claims:
                self._claim_map[c.id] = (t.id, c)
        self._paths = reading_paths()
        self._links = all_links(topics)

    def list_paths(self) -> List[dict]:
        """List all available reading paths."""
        return [
            {"index": i, "id": p.id, "title": p.title,
             "claim_ids": list(p.steps)}
            for i, p in enumerate(self._paths)
        ]

    def get_path_steps(self, path_index: int) -> List[ReadingStep]:
        """Get all steps in a reading path."""
        if path_index < 0 or path_index >= len(self._paths):
            return []
        path = self._paths[path_index]
        steps = []
        for cid in path.steps:
            step = self._make_step(cid)
            if step:
                steps.append(step)
        return steps

    def get_claim_context(self, claim_id: str) -> Optional[ReadingStep]:
        """Get full context for a single claim."""
        return self._make_step(claim_id)

    def _make_step(self, claim_id: str) -> Optional[ReadingStep]:
        """Build a ReadingStep for a claim."""
        if claim_id not in self._claim_map:
            return None
        topic_id, claim = self._claim_map[claim_id]
        d = derive(claim)
        summary = claim.evidence[0].description if claim.evidence else ""

        # Find neighbors from links.
        related = []
        for link in self._links:
            other_id = None
            if link.source == claim_id:
                other_id = link.target
            elif link.target == claim_id:
                other_id = link.source
            if other_id and other_id in self._claim_map:
                _, other_claim = self._claim_map[other_id]
                related.append({
                    "claim_id": other_id,
                    "title": other_claim.title,
                    "status": other_claim.status.name,
                    "kind": link.kind,
                })

        return ReadingStep(
            claim_id=claim.id,
            topic_id=topic_id,
            title=claim.title,
            status=claim.status.name,
            status_light=claim.status.light,
            evidence_axis=d.strength.short,
            diverges=diverges(claim),
            summary=summary[:200],
            open_questions=claim.open_questions,
            related=related[:5],
        )


if __name__ == "__main__":
    import sys
    from ..data.registry import TOPICS

    reader = GuidedReader(TOPICS)
    if "--list" in sys.argv:
        for p in reader.list_paths():
            print(f"  [{p['index']}] {p['label']} ({len(p['claim_ids'])} claims)")
    elif "--path" in sys.argv:
        idx = int(sys.argv[sys.argv.index("--path") + 1])
        steps = reader.get_path_steps(idx)
        for s in steps:
            print(f"  {s.status_light} {s.title} ({s.evidence_axis})")
    elif "--claim" in sys.argv:
        cid = sys.argv[sys.argv.index("--claim") + 1]
        step = reader.get_claim_context(cid)
        if step:
            print(f"  {step.status_light} {step.title}")
            print(f"  {step.status} × {step.evidence_axis}")
            if step.open_questions:
                print(f"  Open: {step.open_questions}")
        else:
            print(f"  Claim {cid!r} not found")
