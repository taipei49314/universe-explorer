"""Claim annotations — tags and notes for editorial workflow.

Adds lightweight metadata to claims without modifying the constitution:
  - Tags: categorize claims (e.g., "needs-review", "high-priority", "contested")
  - Notes: editorial comments and observations
  - Labels: status indicators for workflow management

Annotations are stored separately from claims (in annotations/) and
never affect the constitution, validator, or evidence axis.

Usage:
    python -m universe_explorer.reader.annotate --tag needs-review <claim_id>
    python -m universe_explorer.reader.annotate --note "Review this claim" <claim_id>
    python -m universe_explorer.reader.annotate --list <claim_id>
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from ..model import Claim, Topic

_ANNOTATIONS_DIR = Path(__file__).parent.parent.parent / "annotations"


@dataclass
class Annotation:
    """One annotation on a claim."""

    claim_id: str
    kind: str           # "tag", "note", "label"
    value: str
    author: str = "editor"
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "kind": self.kind,
            "value": self.value,
            "author": self.author,
            "timestamp": self.timestamp,
        }


class ClaimAnnotations:
    """Manage annotations for claims."""

    def __init__(self, annotations_dir: Path = _ANNOTATIONS_DIR):
        self._dir = annotations_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def add_tag(self, claim_id: str, tag: str, author: str = "editor") -> Annotation:
        """Add a tag to a claim."""
        annotation = Annotation(
            claim_id=claim_id,
            kind="tag",
            value=tag.lower().strip(),
            author=author,
        )
        self._save(annotation)
        return annotation

    def add_note(self, claim_id: str, note: str, author: str = "editor") -> Annotation:
        """Add a note to a claim."""
        annotation = Annotation(
            claim_id=claim_id,
            kind="note",
            value=note.strip(),
            author=author,
        )
        self._save(annotation)
        return annotation

    def add_label(self, claim_id: str, label: str, author: str = "editor") -> Annotation:
        """Add a label to a claim (workflow status indicator)."""
        annotation = Annotation(
            claim_id=claim_id,
            kind="label",
            value=label.lower().strip(),
            author=author,
        )
        self._save(annotation)
        return annotation

    def get_annotations(self, claim_id: str) -> List[Annotation]:
        """Get all annotations for a claim."""
        claim_dir = self._dir / claim_id
        if not claim_dir.exists():
            return []

        annotations = []
        for f in sorted(claim_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                annotations.append(Annotation(**data))
            except Exception:
                continue
        return annotations

    def get_tags(self, claim_id: str) -> List[str]:
        """Get all tags for a claim."""
        return [a.value for a in self.get_annotations(claim_id)
                if a.kind == "tag"]

    def get_notes(self, claim_id: str) -> List[dict]:
        """Get all notes for a claim."""
        return [{"value": a.value, "author": a.author, "timestamp": a.timestamp}
                for a in self.get_annotations(claim_id) if a.kind == "note"]

    def get_labels(self, claim_id: str) -> List[str]:
        """Get all labels for a claim."""
        return [a.value for a in self.get_annotations(claim_id)
                if a.kind == "label"]

    def has_tag(self, claim_id: str, tag: str) -> bool:
        """Check if a claim has a specific tag."""
        return tag.lower().strip() in self.get_tags(claim_id)

    def remove_tag(self, claim_id: str, tag: str) -> bool:
        """Remove a tag from a claim."""
        tag = tag.lower().strip()
        claim_dir = self._dir / claim_id
        if not claim_dir.exists():
            return False

        removed = False
        for f in claim_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if data.get("kind") == "tag" and data.get("value") == tag:
                    f.unlink()
                    removed = True
            except Exception:
                continue
        return removed

    def list_all_tags(self) -> Dict[str, List[str]]:
        """List all tags across all claims."""
        result = {}
        for claim_dir in self._dir.iterdir():
            if claim_dir.is_dir():
                tags = self.get_tags(claim_dir.name)
                if tags:
                    result[claim_dir.name] = tags
        return result

    def _save(self, annotation: Annotation):
        """Save an annotation to disk."""
        claim_dir = self._dir / annotation.claim_id
        claim_dir.mkdir(parents=True, exist_ok=True)

        # Use timestamp + value hash for uniqueness.
        import hashlib
        stamp = annotation.timestamp.replace(":", "").replace("-", "")
        val_hash = hashlib.md5(annotation.value.encode()).hexdigest()[:8]
        out_path = claim_dir / f"{stamp}_{val_hash}_{annotation.kind}.json"
        out_path.write_text(
            json.dumps(annotation.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def format_annotations(claim_id: str, annotations: List[Annotation]) -> str:
    """Human-readable annotations report."""
    if not annotations:
        return f"No annotations for {claim_id}."

    lines = [f"Annotations for {claim_id}:"]
    tags = [a.value for a in annotations if a.kind == "tag"]
    notes = [a for a in annotations if a.kind == "note"]
    labels = [a.value for a in annotations if a.kind == "label"]

    if tags:
        lines.append(f"  Tags: {', '.join(tags)}")
    if labels:
        lines.append(f"  Labels: {', '.join(labels)}")
    if notes:
        lines.append(f"  Notes ({len(notes)}):")
        for note in notes:
            lines.append(f"    [{note.timestamp}] {note.value}")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Claim annotations")
    parser.add_argument("claim_id", help="Claim id")
    parser.add_argument("--tag", help="Add a tag")
    parser.add_argument("--note", help="Add a note")
    parser.add_argument("--label", help="Add a label")
    parser.add_argument("--list", action="store_true", help="List annotations")
    parser.add_argument("--remove-tag", help="Remove a tag")
    parser.add_argument("--has-notes", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has notes")
    parser.add_argument("--has-competing", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has competing models")
    parser.add_argument("--has-open-questions", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has open questions")
    parser.add_argument("--diverges", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim diverges")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--claim-status", help="Filter by claim status")
    args = parser.parse_args()

    annotations = ClaimAnnotations()

    if args.tag:
        annotations.add_tag(args.claim_id, args.tag)
        print(f"Added tag '{args.tag}' to {args.claim_id}")
    if args.note:
        annotations.add_note(args.claim_id, args.note)
        print(f"Added note to {args.claim_id}")
    if args.label:
        annotations.add_label(args.claim_id, args.label)
        print(f"Added label '{args.label}' to {args.claim_id}")
    if args.remove_tag:
        removed = annotations.remove_tag(args.claim_id, args.remove_tag)
        if removed:
            print(f"Removed tag '{args.remove_tag}' from {args.claim_id}")
        else:
            print(f"Tag '{args.remove_tag}' not found on {args.claim_id}")
    if args.list or not any([args.tag, args.note, args.label, args.remove_tag]):
        anns = annotations.get_annotations(args.claim_id)
        print(format_annotations(args.claim_id, anns))
