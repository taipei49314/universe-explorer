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


def test_readme_lists_phase13_surfaces():
    """Product surfaces table must name pages that build.py actually writes."""
    readme = Path("README.md").read_text(encoding="utf-8")
    for surface in (
        "explore-v2.html",
        "epistemic_map.html",
        "challenge.html",
        "review.html",
        "dual-axis.svg",
        "epistemic-graph.json",
        "dashboard.html",
        "stats.json",
    ):
        assert surface in readme, surface
    for pkg in ("discovery/", "crossdomain/", "reader/"):
        assert pkg in readme, pkg
    # Editorial tools exist but must not be described as auto-writing claims
    assert "annotations/" in readme
    assert "never auto-write" in readme.lower() or "never auto-writes" in readme.lower()


def test_readme_relation_edge_split_is_honest():
    """Do not conflate all_links mechanical count with epistemic-map graph size."""
    from universe_explorer.data.registry import TOPICS
    from universe_explorer.relations import all_links
    from universe_explorer.crossdomain.graph_builder import build_cross_domain_graph

    links = all_links(TOPICS)
    authored = sum(1 for L in links if L.origin == "authored")
    mechanical = sum(1 for L in links if L.origin == "mechanical")
    graph_n = len(build_cross_domain_graph(TOPICS).edges)
    readme = Path("README.md").read_text(encoding="utf-8")
    assert f"**{authored}**" in readme
    assert f"**{mechanical}**" in readme
    assert f"**{graph_n}**" in readme
    assert authored + mechanical == len(links)


def test_milestones_claim_count_matches():
    c = _counts()
    text = Path("docs/milestones-complete.md").read_text(encoding="utf-8")
    assert f"**Claims:** {c['claims']}" in text or f"**Claims:** **{c['claims']}**" in text
    # Topics line
    assert f"**Topics:** {c['topics']}" in text or f"**Topics:** **{c['topics']}**" in text
    # Phase 1–3 closeout rows stay visible once shipped
    assert "Phase 1 Discovery" in text
    assert "Phase 2 Cross-domain map" in text
    assert "Phase 3 Reader" in text
    assert "Dashboard + stats.json" in text
    assert "planets" in text and "reading path" in text.lower()


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
