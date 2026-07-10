"""P4 acceptance: same engine, new domain. Run: python test_p4.py"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from universe_explorer.axes import EvidenceStrength, derive, diverges
from universe_explorer.data.ocean import OCEAN, amoc_weakening
from universe_explorer.data.registry import TOPICS, get_topic
from universe_explorer.model import Status
from universe_explorer.proposals import propose
from universe_explorer.provenance import validate_provenance
from universe_explorer.validator import validate_topic
from universe_explorer.watch import current_state, diff_events

ENGINE = ["model.py", "validator.py", "axes.py", "provenance.py",
          "proposals.py", "watch.py", "narrative.py"]


def test_engine_files_unchanged():
    """P4 acceptance 1: the six engine files are byte-identical to the frozen
    pre-P4 baseline. Editing any one of them fails here."""
    base = Path("universe_explorer")
    frozen = json.loads(Path("engine_hashes.json").read_text(encoding="utf-8"))
    for f in ENGINE:
        got = hashlib.sha256((base / f).read_bytes()).hexdigest()
        assert got == frozen[f], f"engine file {f} changed — P4 broke zero-change"


def test_ocean_passes_every_gate():
    """P4 acceptance 4: all v0/vocab/P1 gates apply cleanly to the new domain."""
    assert validate_topic(OCEAN) == []
    assert validate_provenance(OCEAN) == []  # non-arxiv sources -> exempt, clean


def test_ocean_light_diversity():
    lights = {c.status for c in OCEAN.claims}
    assert len(lights) == 5, "the ocean topic now spans the full spectrum"
    assert Status.COMPETING in lights


def test_competing_models_populated_for_real():
    """P4 acceptance 5 (retires R4): a real two-camp dispute exercises the
    competing_models field end to end."""
    assert amoc_weakening.status is Status.COMPETING
    assert len(amoc_weakening.competing_models) == 2
    for cm in amoc_weakening.competing_models:
        assert cm.supporting and cm.opposing and cm.limitations


def test_evidence_axis_reverse_combo():
    """Dark oxygen: single direct observation (E2) under a Speculative light —
    the reverse of the black-hole cases, derived not declared."""
    dark = get_topic("ocean").claims[-1]
    assert dark.status is Status.SPECULATIVE
    assert derive(dark).strength is EvidenceStrength.E2_SINGLE_DIRECT
    assert not diverges(dark)  # low consensus, so no divergence flag
    vents = OCEAN.claims[0]
    assert derive(vents).strength is EvidenceStrength.E1_MULTIPLE_DIRECT


def test_proposal_engine_runs_on_ocean_unchanged():
    """The P2 engine judges ocean claims with zero edits; human status sits
    inside the compatible set for every claim."""
    for c in OCEAN.claims:
        p = propose(c)
        assert c.status in p.compatible_statuses, c.id


def test_change_pipeline_is_domain_agnostic():
    """P4 acceptance 6: the P3 diff pipeline produces claim_added events for the
    new topic against an empty baseline — proving it too is domain-agnostic."""
    events = diff_events({}, current_state(OCEAN))
    added = {e["claim"] for e in events if e["kind"] == "claim_added"}
    assert added == {c.id for c in OCEAN.claims}


def test_registry_has_both_domains():
    ids = {t.id for t in TOPICS}
    assert {"black_hole", "ocean"} <= ids


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
