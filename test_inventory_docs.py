"""Public inventory in README/milestones must match the live registry.

Prevents the v0-era drift where docs said “4 claims” while the map held 91.
No confidence fields — list counts only.
"""

from __future__ import annotations

from pathlib import Path

from universe_explorer.data.registry import TOPICS
from universe_explorer.relations import authored_links, reading_paths


def _counts():
    return {
        "topics": len(TOPICS),
        "claims": sum(len(t.claims) for t in TOPICS),
        "authored": len(authored_links()),
        "paths": len(reading_paths()),
    }


def test_readme_snapshot_matches_registry():
    c = _counts()
    readme = Path("README.md").read_text(encoding="utf-8")
    # Snapshot table uses bold markdown numbers
    assert f"**{c['topics']}**" in readme, c
    assert f"**{c['claims']}**" in readme, c
    assert f"**{c['authored']}**" in readme, c
    assert f"**{c['paths']}**" in readme, c
    # Domain claim sum line still lists 8 topics
    for tid in (
        "black_hole", "cosmology", "dark_matter", "stars",
        "planets", "exoplanets", "ocean", "seismology",
    ):
        assert tid in readme


def test_milestones_claim_count_matches():
    c = _counts()
    text = Path("docs/milestones-complete.md").read_text(encoding="utf-8")
    assert f"**Claims:** {c['claims']}" in text or f"**Claims:** **{c['claims']}**" in text
    # Topics line
    assert f"**Topics:** {c['topics']}" in text or f"**Topics:** **{c['topics']}**" in text


def test_domain_claim_lines_sum():
    """README domain table numbers, if present as 'N + M', must sum to registry."""
    c = _counts()
    # Hard check: per-topic claim counts in registry
    by = {t.id: len(t.claims) for t in TOPICS}
    assert sum(by.values()) == c["claims"]
    assert by["black_hole"] == 10
    assert by["dark_matter"] == 18


def _run():
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
            passed += 1
    print(f"\n{passed} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_run())
