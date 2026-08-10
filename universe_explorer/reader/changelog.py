"""Changelog generator — auto-generate changelog from git commits.

Generates:
  - CHANGELOG.md with recent commits
  - Categorized by type (feat, fix, test, docs, etc.)

Usage:
    python -m universe_explorer.reader.changelog
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

_ROOT = Path(__file__).parent.parent.parent


def generate_changelog(limit: int = 50) -> str:
    """Generate changelog from recent git commits."""
    commits = _get_recent_commits(limit)
    categorized = _categorize_commits(commits)
    return _format_changelog(categorized)


def _get_recent_commits(limit: int) -> List[dict]:
    """Get recent git commits."""
    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{limit}", "--format=%H|%s|%ai"],
            capture_output=True, text=True, cwd=_ROOT,
            encoding="utf-8", errors="replace",
        )
        commits = []
        for line in result.stdout.strip().split("\n"):
            if "|" in line:
                parts = line.split("|", 2)
                if len(parts) >= 3:
                    commits.append({
                        "hash": parts[0][:8],
                        "message": parts[1],
                        "date": parts[2][:10],
                    })
        return commits
    except Exception:
        return []


def _categorize_commits(commits: List[dict]) -> dict:
    """Categorize commits by type."""
    categories = {
        "feat": [],      # New features
        "fix": [],       # Bug fixes
        "test": [],      # Tests
        "docs": [],      # Documentation
        "refactor": [],  # Refactoring
        "other": [],     # Other
    }

    for commit in commits:
        msg = commit["message"].lower()
        if any(k in msg for k in ["add", "new", "feat", "implement"]):
            categories["feat"].append(commit)
        elif any(k in msg for k in ["fix", "bug", "patch"]):
            categories["fix"].append(commit)
        elif any(k in msg for k in ["test", "spec"]):
            categories["test"].append(commit)
        elif any(k in msg for k in ["doc", "readme", "update readme"]):
            categories["docs"].append(commit)
        elif any(k in msg for k in ["refactor", "clean", "rename"]):
            categories["refactor"].append(commit)
        else:
            categories["other"].append(commit)

    return categories


def _format_changelog(categorized: dict) -> str:
    """Format categorized commits as markdown."""
    lines = ["# Changelog", ""]

    labels = {
        "feat": "Features",
        "fix": "Bug Fixes",
        "test": "Tests",
        "docs": "Documentation",
        "refactor": "Refactoring",
        "other": "Other Changes",
    }

    for category, label in labels.items():
        commits = categorized.get(category, [])
        if commits:
            lines.append(f"## {label}")
            lines.append("")
            for commit in commits[:10]:  # Limit per category
                lines.append(f"- {commit['message']} (`{commit['hash']}`)")
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    changelog = generate_changelog()
    print(changelog)

    # Write to dist/.
    _DIST_DIR = _ROOT / "dist"
    _DIST_DIR.mkdir(exist_ok=True)
    out = _DIST_DIR / "CHANGELOG.md"
    out.write_text(changelog, encoding="utf-8")
    print(f"\nCHANGELOG.md -> {out}")
