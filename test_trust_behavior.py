"""Trust-behavior measurer: gate + blind-spot probes.

Order of work (product rule):
  1. Build the measurer first.
  2. Only then trust behaviour — and only what the counts show.

Run: python test_trust_behavior.py
     python -m universe_explorer.trust_behavior
"""

from __future__ import annotations

import json
from pathlib import Path

from universe_explorer.model import (
    Claim, ConditionAssessment, Evidence, Source, Status, Topic,
)
from universe_explorer import trust_behavior as TB
from universe_explorer.axes import derive, diverges
from universe_explorer.data.registry import TOPICS


# ---------------------------------------------------------------------------
# 1. Live registry gate (measure first on real data)
# ---------------------------------------------------------------------------


def test_live_registry_all_ok():
    report = TB.measure(TOPICS)
    assert report["kind"] == "trust_behavior_measure"
    assert report["n_measurements"] >= 50
    if report["n_fail"]:
        fails = [m for m in report["measurements"] if not m["ok"]]
        preview = "\n".join(
            f"  {m['id']}: {m['expected']!r} vs {m['observed']!r}"
            for m in fails[:12]
        )
        raise AssertionError(f"{report['n_fail']} fail(s):\n{preview}")
    assert report["all_ok"] is True
    assert report["n_pass"] == report["n_measurements"]


def test_report_has_no_certainty_fields():
    report = TB.measure(TOPICS)
    banned = TB.BANNED_REPORT_KEYS

    def walk(x, path=""):
        if isinstance(x, dict):
            for k, v in x.items():
                assert k.lower() not in banned, (path, k)
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x[:200]):
                walk(v, f"{path}[{i}]")

    walk(report)


def test_report_counts_are_list_counts():
    report = TB.measure(TOPICS)
    assert report["n_pass"] + report["n_fail"] == report["n_measurements"]
    assert len(report["measurements"]) == report["n_measurements"]
    assert sum(1 for m in report["measurements"] if m["ok"]) == report["n_pass"]


def test_report_is_json_serializable():
    """Blind spot: Enum / Path leaking into expected/observed breaks --out."""
    report = TB.measure(TOPICS)
    raw = json.dumps(report, ensure_ascii=False)
    again = json.loads(raw)
    assert again["n_measurements"] == report["n_measurements"]
    assert again["all_ok"] == report["all_ok"]


def test_cli_exit_zero_on_live():
    assert TB.main([]) == 0


# ---------------------------------------------------------------------------
# 2. Blind spots — broken claims MUST fail the measurer
# ---------------------------------------------------------------------------


def _broken_topic_dangling_source() -> Topic:
    return Topic(
        id="t_blind",
        title="Blind",
        summary="probe",
        claims=[
            Claim(
                id="dangling_ev",
                title="Evidence points nowhere",
                status=Status.FRONTIER,
                sources=[Source(label="S1", url_or_id="arXiv:0000.00001",
                                kind="preprint")],
                evidence=[Evidence(
                    type="direct observation",
                    description="Something was seen.",
                    source_ref="MISSING_LABEL",
                )],
                status_reason=[ConditionAssessment(
                    "new_discovery", True, "probe",
                )],
            )
        ],
    )


def test_blind_dangling_source_fails_measurement():
    ms = TB.measure_claim(
        _broken_topic_dangling_source().claims[0], "t_blind")
    row = next(m for m in ms if m.id.endswith("evidence_sources_resolve"))
    assert row.ok is False
    assert "MISSING_LABEL" in row.observed


def test_blind_declared_confidence_text_fails():
    c = Claim(
        id="fake_conf",
        title="We are sure",
        status=Status.SPECULATIVE,
        sources=[Source(label="S1", url_or_id="x", kind="preprint")],
        evidence=[Evidence(
            type="theoretical derivation",
            description="Derivation only.",
            source_ref="S1",
        )],
        status_reason=[ConditionAssessment(
            "pure_theoretical_derivation", True,
            "confidence: 95 that this holds",  # banned pattern
        )],
    )
    ms = TB.measure_claim(c)
    row = next(m for m in ms if m.id.endswith("no_declared_confidence_text"))
    assert row.ok is False


def test_blind_empty_status_reason_fails():
    c = Claim(
        id="no_reason",
        title="Undocumented light",
        status=Status.STRONG,
        sources=[Source(label="S1", url_or_id="x", kind="peer-reviewed paper")],
        evidence=[Evidence(
            type="direct observation",
            description="Seen once.",
            source_ref="S1",
        )],
        status_reason=[],  # overturn path gone
    )
    ms = TB.measure_claim(c)
    row = next(m for m in ms if m.id.endswith("status_reason_nonempty"))
    assert row.ok is False


def test_blind_diverges_rule_is_mechanical():
    """Strong + analog-only must report diverges=True (the hawking shape)."""
    c = Claim(
        id="strong_analog",
        title="Strong on analog only",
        status=Status.STRONG,
        sources=[
            Source(label="T", url_or_id="x", kind="peer-reviewed paper"),
            Source(label="A", url_or_id="y", kind="peer-reviewed paper"),
        ],
        evidence=[
            Evidence(type="theoretical derivation",
                     description="Derived on paper.", source_ref="T"),
            Evidence(type="analog experiment",
                     description="Lab analog only.", source_ref="A"),
        ],
        status_reason=[
            ConditionAssessment("mainstream_model_support", True, "taught"),
            ConditionAssessment("minor_alternatives_exist", True, "few"),
            ConditionAssessment("overall_direction_robust", True, "stable"),
        ],
    )
    assert diverges(c) is True
    assert derive(c).strength.short == "E3"
    ms = TB.measure_claim(c)
    row = next(m for m in ms if m.id.endswith("diverges_matches_rule"))
    assert row.ok is True
    assert row.observed is True


def test_blind_missing_domain_path_fails_inventory():
    solo = Topic(
        id="orphan_domain",
        title="Orphan",
        summary="",
        claims=[Claim(
            id="orphan_claim_xyz",
            title="Alone",
            status=Status.FRONTIER,
            sources=[Source(label="S1", url_or_id="x", kind="preprint")],
            evidence=[Evidence(
                type="indirect observation",
                description="Hint.",
                source_ref="S1",
            )],
            status_reason=[ConditionAssessment(
                "insufficient_observation", True, "probe",
            )],
        )],
    )
    # Only this topic — no reading path can touch it (paths use real claim ids)
    ms = TB.measure_inventory([solo])
    row = next(m for m in ms if m.id == "inventory.every_domain_has_reading_path")
    assert row.ok is False
    assert "orphan_domain" in row.observed


def test_blind_export_axis_mismatch_detected(tmp_path, monkeypatch):
    """If dist/claims.json lies about diverges, measurer must fail."""
    # Build a minimal lying export from a real diverging claim
    from universe_explorer.data.black_hole import hawking_radiation as h
    assert diverges(h) is True
    fake = {
        "note": "Only recorded fields — no confidence numbers exist anywhere.",
        "claims": [{
            "topic": "black_hole",
            "id": "hawking_radiation",
            "title": h.title,
            "status": "STRONG",
            "evidence_axis": "E1",  # lie
            "diverges": False,      # lie
        }],
    }
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "claims.json").write_text(
        json.dumps(fake), encoding="utf-8")
    monkeypatch.setattr(TB, "DIST", dist)
    # topics with only hawking is enough for parity check of that id
    from universe_explorer.data.registry import TOPICS as LIVE
    ms = TB.measure_dist_exports(LIVE)
    row = next(m for m in ms if m.id == "export.dual_axis_parity")
    assert row.ok is False


def test_blind_ui_contract_fails_if_app_gutted(tmp_path, monkeypatch):
    empty = tmp_path / "app.html"
    empty.write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(TB, "WEB_APP", empty)
    monkeypatch.setattr(TB, "WEB_UNI", empty)
    ms = TB.measure_ui_contracts()
    failed = [m.id for m in ms if not m.ok]
    assert "ui.app_tour" in failed
    assert "ui.app_challenge_copy" in failed


# ---------------------------------------------------------------------------
# 3. Stress case still present on live data
# ---------------------------------------------------------------------------


def test_hawking_stress_measurements_pass():
    ms = TB.measure_stress_hawking(TOPICS)
    assert all(m.ok for m in ms), [m for m in ms if not m.ok]


def test_measure_claim_count_scales_with_registry():
    """Blind spot: silent claim drops would shrink measurement coverage."""
    report = TB.measure(TOPICS, include_dist=False)
    n_claims = sum(len(t.claims) for t in TOPICS)
    # each claim contributes ≥4 claim-surface rows
    claim_rows = [m for m in report["measurements"]
                  if m["surface"] == "claim"]
    assert len(claim_rows) >= n_claims * 4


def _run():
    passed = 0
    # simple runner without pytest for run_tests.py compatibility
    import inspect
    g = globals()
    for name, fn in sorted(g.items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        sig = inspect.signature(fn)
        if sig.parameters:
            # skip pytest-style tests in bare runner — handled below with hacks
            if "tmp_path" in sig.parameters or "monkeypatch" in sig.parameters:
                continue
        fn()
        print(f"  ok  {name}")
        passed += 1

    # pytest-style tests with manual fixtures
    import tempfile
    from pathlib import Path as P

    class MP:
        def __init__(self):
            self._orig = {}

        def setattr(self, obj, name, value):
            self._orig[(obj, name)] = getattr(obj, name)
            setattr(obj, name, value)

        def undo(self):
            for (obj, name), v in self._orig.items():
                setattr(obj, name, v)

    with tempfile.TemporaryDirectory() as d:
        mp = MP()
        try:
            test_blind_export_axis_mismatch_detected(P(d), mp)
            print("  ok  test_blind_export_axis_mismatch_detected")
            passed += 1
        finally:
            mp.undo()

    with tempfile.TemporaryDirectory() as d:
        mp = MP()
        try:
            test_blind_ui_contract_fails_if_app_gutted(P(d), mp)
            print("  ok  test_blind_ui_contract_fails_if_app_gutted")
            passed += 1
        finally:
            mp.undo()

    print(f"\n{passed} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_run())
