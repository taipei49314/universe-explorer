"""P1.5 acceptance tests: the evidence axis emerges, is traceable, and moves
only when the recorded evidence moves. Run: python test_axes.py"""

from __future__ import annotations

import copy

from universe_explorer.axes import (
    ANALOG,
    DIRECT,
    EvidenceStrength,
    THEORY_DERIVATION,
    derive,
    diverges,
)
from universe_explorer.data.black_hole import (
    BLACK_HOLE,
    event_horizon_exists,
    firewall,
    hawking_radiation,
    information_paradox,
)
from universe_explorer.model import Evidence, Source
from universe_explorer.validator import validate_claim


def test_expected_grades_on_real_data():
    assert derive(event_horizon_exists).strength is EvidenceStrength.E1_MULTIPLE_DIRECT
    assert derive(hawking_radiation).strength is EvidenceStrength.E3_INDIRECT_ANALOG
    assert derive(information_paradox).strength is EvidenceStrength.E4_THEORETICAL
    assert derive(firewall).strength is EvidenceStrength.E4_THEORETICAL


def test_divergence_is_structural():
    # Strong consensus x analog-only -> the axes point apart, mechanically.
    assert diverges(hawking_radiation)
    # Aligned claims carry no divergence flag.
    assert not diverges(event_horizon_exists)
    assert not diverges(information_paradox)
    assert not diverges(firewall)


def test_axis_moves_only_with_evidence():
    """Emergence, not declaration: record a (hypothetical) direct observation
    and the axis moves by itself — there is no field to set."""
    c = copy.deepcopy(hawking_radiation)
    assert derive(c).strength is EvidenceStrength.E3_INDIRECT_ANALOG
    c.sources.append(Source("HYPO", "arXiv:0000.00000", "peer-reviewed paper"))
    c.evidence.append(Evidence(DIRECT, "hypothetical direct detection", "HYPO"))
    assert derive(c).strength is EvidenceStrength.E2_SINGLE_DIRECT
    assert not diverges(c)  # divergence dissolves the moment evidence arrives


def test_e1_requires_distinct_sources():
    """Two direct observations from the SAME source stay E2 — independence is
    about sources, not about how many sentences were written."""
    c = copy.deepcopy(firewall)
    c.evidence = [
        Evidence(DIRECT, "obs a", "AMPS2013"),
        Evidence(DIRECT, "obs b", "AMPS2013"),
    ]
    assert derive(c).strength is EvidenceStrength.E2_SINGLE_DIRECT


def test_derivation_is_traceable():
    d = derive(hawking_radiation)
    assert any("rule E3" in r for r in d.reasoning)
    assert any("0 direct" in r for r in d.reasoning)


def test_vocab_rule_bites():
    c = copy.deepcopy(firewall)
    c.evidence[0].type = "vibes"
    rules = {v.rule for v in validate_claim(c)}
    assert "invalid_evidence_type" in rules


def test_real_data_vocab_clean():
    for claim in BLACK_HOLE.claims:
        rules = {v.rule for v in validate_claim(claim)}
        assert "invalid_evidence_type" not in rules, claim.id


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
