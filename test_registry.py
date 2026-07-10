"""Registry-wide acceptance: every gate, every topic, forever.

Any future domain added to the registry is automatically held to all of it.
Run: python test_registry.py"""

from __future__ import annotations

from universe_explorer.data.registry import TOPICS, get_topic
from universe_explorer.narrative import check as narrative_check, compose
from universe_explorer.proposals import propose
from universe_explorer.provenance import validate_provenance
from universe_explorer.validator import validate_topic


def test_all_topics_pass_constitution():
    for t in TOPICS:
        assert validate_topic(t) == [], t.id


def test_all_topics_pass_provenance():
    """Every arXiv-cited source in every domain has a verified fetch."""
    for t in TOPICS:
        assert validate_provenance(t) == [], t.id


def test_all_topics_show_light_diversity():
    """The knowledge-shape requirement holds per domain: at least three
    distinct lights, proving the light belongs to claims, not topics."""
    for t in TOPICS:
        assert len({c.status for c in t.claims}) >= 3, t.id


def test_all_claims_inside_proposal_compatible_set():
    for t in TOPICS:
        for c in t.claims:
            assert c.status in propose(c).compatible_statuses, c.id


def test_all_narratives_pass_their_gate():
    for t in TOPICS:
        for c in t.claims:
            narrative_check(c, compose(c))  # raises on breach


def test_registry_lookup():
    assert get_topic("exoplanets").id == "exoplanets"
    assert len(TOPICS) == 3


def _run():
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
            passed += 1
    print(f"\n{passed} tests passed.")


if __name__ == "__main__":
    _run()
