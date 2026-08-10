"""Automation metrics — measure the measurement tools.

Must run under bare ``python test_automation.py`` (run_tests.py entry).
"""

from __future__ import annotations

import json

from universe_explorer.reader.automation_metrics import (
    AutomationMetrics,
    OutputMetric,
    compute_metrics,
    format_metrics_report,
    EXPECTED_OUTPUTS,
)


def test_compute_metrics_returns_valid():
    metrics = compute_metrics()
    assert isinstance(metrics, AutomationMetrics)
    assert metrics.total_outputs == len(EXPECTED_OUTPUTS)
    assert metrics.automated_outputs > 0


def test_all_expected_outputs_tracked():
    metrics = compute_metrics()
    tracked = {o.name for o in metrics.outputs}
    for name, _ in EXPECTED_OUTPUTS:
        assert name in tracked, f"Missing: {name}"


def test_automation_rate_string():
    metrics = compute_metrics()
    assert metrics.automation_rate == (
        f"{metrics.automated_outputs}/{metrics.total_outputs}"
    )


def test_health_status_is_known_token():
    metrics = compute_metrics()
    assert metrics.health_status in ("ok", "error", "unknown")


def test_to_dict_json_serializable():
    metrics = compute_metrics()
    raw = json.dumps(metrics.to_dict())
    assert len(raw) > 10


def test_format_report_contains_stats():
    report = format_metrics_report(compute_metrics())
    assert "Automation Metrics" in report
    assert "Total outputs" in report


def test_after_build_all_outputs_exist():
    """If dist was built, missing_outputs must be 0."""
    metrics = compute_metrics()
    existing = [o for o in metrics.outputs if o.exists]
    # Soft when dist absent; hard when majority present
    if len(existing) >= len(EXPECTED_OUTPUTS) // 2:
        assert metrics.missing_outputs == 0, [
            o.name for o in metrics.outputs if not o.exists
        ]


def test_automation_rate_high():
    metrics = compute_metrics()
    rate = metrics.automated_outputs / metrics.total_outputs
    assert rate >= 0.9, f"Automation rate too low: {rate:.1%}"


def test_output_metric_roundtrip():
    metric = OutputMetric(
        name="test.html", path="/tmp/test.html",
        exists=True, size_bytes=100, automated=True,
    )
    d = metric.to_dict()
    assert d["name"] == "test.html" and d["exists"] is True and d["automated"] is True


def test_no_banned_keys_in_metrics_payload():
    d = compute_metrics().to_dict()
    banned = {"confidence", "score", "probability", "certainty", "trust"}

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                assert k.lower() not in banned, k
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(d)


def _run() -> int:
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
