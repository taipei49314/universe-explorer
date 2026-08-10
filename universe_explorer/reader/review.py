"""Claim review workflow — structured review process for claims.

Provides a checklist-based review workflow:
  - Predefined review checklists for different claim types
  - Review status tracking (pending, in-progress, approved, rejected)
  - Review comments and decisions
  - Audit trail for all review actions

Usage:
    python -m universe_explorer.reader.review --start <claim_id>
    python -m universe_explorer.reader.review --check <claim_id> --item sources
    python -m universe_explorer.reader.review --approve <claim_id> --note "Looks good"
    python -m universe_explorer.reader.review --status <claim_id>
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from ..model import Claim, Topic

_REVIEWS_DIR = Path(__file__).parent.parent.parent / "reviews"

# Predefined review checklists.
CHECKLISTS = {
    "default": [
        {"id": "sources", "label": "Sources are valid and accessible", "required": True},
        {"id": "evidence", "label": "Evidence items are properly sourced", "required": True},
        {"id": "status", "label": "Status light is justified by evidence", "required": True},
        {"id": "precision", "label": "No fake precision or confidence scores", "required": True},
        {"id": "questions", "label": "Open questions are meaningful", "required": False},
        {"id": "competing", "label": "Competing models are properly documented", "required": False},
    ],
    "new_claim": [
        {"id": "sources", "label": "All sources are fetched and verified", "required": True},
        {"id": "evidence", "label": "Evidence items match source content", "required": True},
        {"id": "status", "label": "Status is within compatible set", "required": True},
        {"id": "precision", "label": "No invented numbers or percentages", "required": True},
        {"id": "title", "label": "Title is a claim statement, not paper name", "required": True},
        {"id": "questions", "label": "Open questions reflect source gaps", "required": False},
    ],
    "status_change": [
        {"id": "reason", "label": "Status reason covers all conditions", "required": True},
        {"id": "history", "label": "Status history entry added", "required": True},
        {"id": "evidence", "label": "New evidence supports the change", "required": True},
        {"id": "watch", "label": "Watch event documented", "required": True},
    ],
}


@dataclass
class ReviewItem:
    """One item in a review checklist."""

    id: str
    label: str
    required: bool
    checked: bool = False
    comment: str = ""


@dataclass
class Review:
    """A review session for a claim."""

    claim_id: str
    checklist_type: str = "default"
    status: str = "pending"   # pending, in-progress, approved, rejected
    items: List[ReviewItem] = field(default_factory=list)
    comments: List[dict] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""

    def __post_init__(self):
        if not self.started_at:
            self.started_at = dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
        if not self.items:
            checklist = CHECKLISTS.get(self.checklist_type, CHECKLISTS["default"])
            self.items = [ReviewItem(**item) for item in checklist]

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "checklist_type": self.checklist_type,
            "status": self.status,
            "items": [
                {"id": i.id, "label": i.label, "required": i.required,
                 "checked": i.checked, "comment": i.comment}
                for i in self.items
            ],
            "comments": self.comments,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }

    @property
    def progress(self) -> float:
        """Review progress as a percentage."""
        if not self.items:
            return 0.0
        checked = sum(1 for i in self.items if i.checked)
        return checked / len(self.items) * 100

    @property
    def required_complete(self) -> bool:
        """Check if all required items are checked."""
        return all(i.checked for i in self.items if i.required)

    @property
    def can_approve(self) -> bool:
        """Check if the review can be approved."""
        return self.required_complete and self.status in ("pending", "in-progress")


class ReviewManager:
    """Manage claim reviews."""

    def __init__(self, reviews_dir: Path = _REVIEWS_DIR):
        self._dir = reviews_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def start_review(self, claim_id: str, checklist_type: str = "default") -> Review:
        """Start a new review for a claim."""
        review = Review(
            claim_id=claim_id,
            checklist_type=checklist_type,
            status="in-progress",
        )
        self._save(review)
        return review

    def get_review(self, claim_id: str) -> Optional[Review]:
        """Get the current review for a claim."""
        review_file = self._dir / f"{claim_id}.json"
        if not review_file.exists():
            return None
        try:
            data = json.loads(review_file.read_text(encoding="utf-8"))
            items = [ReviewItem(**i) for i in data.get("items", [])]
            return Review(
                claim_id=data["claim_id"],
                checklist_type=data.get("checklist_type", "default"),
                status=data.get("status", "pending"),
                items=items,
                comments=data.get("comments", []),
                started_at=data.get("started_at", ""),
                completed_at=data.get("completed_at", ""),
            )
        except Exception:
            return None

    def check_item(self, claim_id: str, item_id: str, comment: str = "") -> bool:
        """Check a review item."""
        review = self.get_review(claim_id)
        if not review:
            return False

        for item in review.items:
            if item.id == item_id:
                item.checked = True
                if comment:
                    item.comment = comment
                break
        else:
            return False

        self._save(review)
        return True

    def uncheck_item(self, claim_id: str, item_id: str) -> bool:
        """Uncheck a review item."""
        review = self.get_review(claim_id)
        if not review:
            return False

        for item in review.items:
            if item.id == item_id:
                item.checked = False
                break
        else:
            return False

        self._save(review)
        return True

    def add_comment(self, claim_id: str, comment: str, author: str = "editor") -> bool:
        """Add a comment to a review."""
        review = self.get_review(claim_id)
        if not review:
            return False

        review.comments.append({
            "text": comment,
            "author": author,
            "timestamp": dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"),
        })
        self._save(review)
        return True

    def approve(self, claim_id: str, note: str = "") -> bool:
        """Approve a review."""
        review = self.get_review(claim_id)
        if not review or not review.can_approve:
            return False

        review.status = "approved"
        review.completed_at = dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        if note:
            review.comments.append({
                "text": f"Approved: {note}",
                "author": "editor",
                "timestamp": review.completed_at,
            })
        self._save(review)
        return True

    def reject(self, claim_id: str, reason: str = "") -> bool:
        """Reject a review."""
        review = self.get_review(claim_id)
        if not review:
            return False

        review.status = "rejected"
        review.completed_at = dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        if reason:
            review.comments.append({
                "text": f"Rejected: {reason}",
                "author": "editor",
                "timestamp": review.completed_at,
            })
        self._save(review)
        return True

    def list_reviews(self, status: Optional[str] = None) -> List[dict]:
        """List all reviews, optionally filtered by status."""
        reviews = []
        for f in self._dir.glob("*.json"):
            review = self.get_review(f.stem)
            if review and (status is None or review.status == status):
                reviews.append({
                    "claim_id": review.claim_id,
                    "status": review.status,
                    "progress": review.progress,
                    "checklist_type": review.checklist_type,
                })
        return reviews

    def _save(self, review: Review):
        """Save a review to disk."""
        out_path = self._dir / f"{review.claim_id}.json"
        out_path.write_text(
            json.dumps(review.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def format_review(review: Review) -> str:
    """Human-readable review report."""
    if not review:
        return "No review found."

    lines = [
        f"Review: {review.claim_id}",
        f"Status: {review.status}",
        f"Checklist: {review.checklist_type}",
        f"Progress: {review.progress:.0f}%",
        "",
        "Checklist:",
    ]

    for item in review.items:
        check = "✓" if item.checked else "○"
        req = " *" if item.required else ""
        lines.append(f"  {check} {item.label}{req}")
        if item.comment:
            lines.append(f"    └─ {item.comment}")

    if review.comments:
        lines.append("")
        lines.append("Comments:")
        for comment in review.comments:
            lines.append(f"  [{comment['timestamp']}] {comment['text']}")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Claim review workflow")
    parser.add_argument("claim_id", help="Claim id")
    parser.add_argument("--start", action="store_true", help="Start a review")
    parser.add_argument("--check", help="Check a review item")
    parser.add_argument("--uncheck", help="Uncheck a review item")
    parser.add_argument("--comment", help="Add a comment")
    parser.add_argument("--approve", action="store_true", help="Approve the review")
    parser.add_argument("--reject", action="store_true", help="Reject the review")
    parser.add_argument("--status", action="store_true", help="Show review status")
    parser.add_argument("--list", action="store_true", help="List all reviews")
    parser.add_argument("--note", default="", help="Note for approve/reject")
    parser.add_argument("--checklist", default="default", help="Checklist type")
    parser.add_argument("--tag", help="Filter by annotation tag")
    parser.add_argument("--label", help="Filter by annotation label")
    parser.add_argument("--has-notes", type=lambda x: x.lower() == "true",
                        help="Filter by whether claim has notes")
    args = parser.parse_args()

    manager = ReviewManager()

    if args.list:
        reviews = manager.list_reviews()
        if args.tag:
            from .annotate import ClaimAnnotations
            annotations = ClaimAnnotations()
            reviews = [r for r in reviews
                       if annotations.has_tag(r["claim_id"], args.tag)]
        if args.label:
            from .annotate import ClaimAnnotations
            annotations = ClaimAnnotations()
            reviews = [r for r in reviews
                       if args.label in annotations.get_labels(r["claim_id"])]
        if args.has_notes is not None:
            from .annotate import ClaimAnnotations
            annotations = ClaimAnnotations()
            if args.has_notes:
                reviews = [r for r in reviews
                           if annotations.get_notes(r["claim_id"])]
            else:
                reviews = [r for r in reviews
                           if not annotations.get_notes(r["claim_id"])]
        print(f"Reviews: {len(reviews)}")
        for r in reviews:
            print(f"  {r['claim_id']}: {r['status']} ({r['progress']:.0f}%)")
    elif args.start:
        review = manager.start_review(args.claim_id, args.checklist)
        print(f"Started review for {args.claim_id}")
        print(format_review(review))
    elif args.check:
        if manager.check_item(args.claim_id, args.check, args.note):
            print(f"Checked '{args.check}' for {args.claim_id}")
        else:
            print(f"Failed to check '{args.check}' for {args.claim_id}")
    elif args.uncheck:
        if manager.uncheck_item(args.claim_id, args.uncheck):
            print(f"Unchecked '{args.uncheck}' for {args.claim_id}")
        else:
            print(f"Failed to uncheck '{args.uncheck}' for {args.claim_id}")
    elif args.comment:
        if manager.add_comment(args.claim_id, args.comment):
            print(f"Added comment to {args.claim_id}")
        else:
            print(f"Failed to add comment to {args.claim_id}")
    elif args.approve:
        if manager.approve(args.claim_id, args.note):
            print(f"Approved review for {args.claim_id}")
        else:
            print(f"Cannot approve review for {args.claim_id}")
    elif args.reject:
        if manager.reject(args.claim_id, args.note):
            print(f"Rejected review for {args.claim_id}")
        else:
            print(f"Failed to reject review for {args.claim_id}")
    else:
        review = manager.get_review(args.claim_id)
        if review:
            print(format_review(review))
        else:
            print(f"No review found for {args.claim_id}")
