"""Tests for automation metrics — measure the measurement tools.

Verifies:
  - Metrics computation is correct
  - All expected outputs are tracked
  - Health status integration works
  - Automation rate calculation is correct
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from universe_explorer.reader.automation_metrics import (
    AutomationMetrics,
    OutputMetric,
    compute_metrics,
    format_metrics_report,
    EXPECTED_OUTPUTS,
)


class TestAutomationMetrics:
    """Automation metrics should be correct."""

    def test_compute_metrics_returns_valid(self):
        """compute_metrics should return valid metrics."""
        metrics = compute_metrics()
        assert isinstance(metrics, AutomationMetrics)
        assert metrics.total_outputs > 0
        assert metrics.automated_outputs > 0

    def test_all_expected_outputs_tracked(self):
        """All expected outputs should be tracked."""
        metrics = compute_metrics()
        tracked_names = {o.name for o in metrics.outputs}
        for name, _ in EXPECTED_OUTPUTS:
            assert name in tracked_names, f"Missing: {name}"

    def test_automation_rate_calculation(self):
        """Automation rate should be correct."""
        metrics = compute_metrics()
        assert metrics.automation_rate == f"{metrics.automated_outputs}/{metrics.total_outputs}"

    def test_health_status_is_string(self):
        """Health status should be a string."""
        metrics = compute_metrics()
        assert isinstance(metrics.health_status, str)
        assert metrics.health_status in ("ok", "error", "unknown")

    def test_outputs_have_required_fields(self):
        """All outputs should have required fields."""
        metrics = compute_metrics()
        for output in metrics.outputs:
            assert hasattr(output, "name")
            assert hasattr(output, "exists")
            assert hasattr(output, "automated")

    def test_to_dict_serializable(self):
        """to_dict should produce serializable output."""
        metrics = compute_metrics()
        d = metrics.to_dict()
        json_str = json.dumps(d)
        assert len(json_str) > 0

    def test_format_report_contains_stats(self):
        """Report should contain statistics."""
        metrics = compute_metrics()
        report = format_metrics_report(metrics)
        assert "Automation Metrics" in report
        assert "Total outputs" in report
        assert "Automated" in report

    def test_existing_outputs_detected(self):
        """Existing outputs should be detected."""
        metrics = compute_metrics()
        # At least some outputs should exist (from previous build)
        existing = [o for o in metrics.outputs if o.exists]
        assert len(existing) > 0

    def test_automation_rate_high(self):
        """Automation rate should be high (most outputs automated)."""
        metrics = compute_metrics()
        rate = metrics.automated_outputs / metrics.total_outputs
        assert rate >= 0.9, f"Automation rate too low: {rate:.1%}"


class TestOutputMetric:
    """OutputMetric should work correctly."""

    def test_output_metric_creation(self):
        """OutputMetric should be creatable."""
        metric = OutputMetric(
            name="test.html",
            path="/tmp/test.html",
            exists=True,
            size_bytes=100,
            automated=True,
        )
        assert metric.name == "test.html"
        assert metric.exists is True

    def test_output_metric_to_dict(self):
        """to_dict should produce valid dict."""
        metric = OutputMetric(
            name="test.html",
            path="/tmp/test.html",
            exists=True,
            size_bytes=100,
            automated=True,
        )
        d = metric.to_dict()
        assert "name" in d
        assert "exists" in d
        assert "automated" in d
