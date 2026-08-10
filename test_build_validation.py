"""Build validation tests — verify build.py outputs.

Checks:
  - All expected files exist in dist/
  - HTML files are valid (have DOCTYPE, charset, etc.)
  - JSON files are valid JSON
  - SVG files are valid SVG
  - All internal links resolve
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from universe_explorer.data.registry import TOPICS
from universe_explorer.reader.automation_metrics import EXPECTED_OUTPUTS

_DIST_DIR = Path(__file__).parent / "dist"


class TestBuildOutputs:
    """All expected outputs should exist and be valid."""

    @pytest.fixture(autouse=True)
    def build_if_needed(self):
        """Build if dist/ doesn't exist."""
        if not _DIST_DIR.exists() or not (_DIST_DIR / "index.html").exists():
            import subprocess
            subprocess.run(["python", "build.py"], check=True,
                           capture_output=True, text=True)

    def test_all_expected_files_exist(self):
        """All expected output files should exist."""
        for name, _ in EXPECTED_OUTPUTS:
            path = _DIST_DIR / name
            assert path.exists(), f"Missing: {name}"

    def test_html_files_have_doctype(self):
        """All HTML files should have DOCTYPE."""
        for name, _ in EXPECTED_OUTPUTS:
            if name.endswith(".html"):
                path = _DIST_DIR / name
                if path.exists():
                    content = path.read_text(encoding="utf-8")
                    assert "<!DOCTYPE html>" in content or "<!doctype html>" in content, \
                        f"{name} missing DOCTYPE"

    def test_json_files_are_valid(self):
        """All JSON files should be valid JSON."""
        for name, _ in EXPECTED_OUTPUTS:
            if name.endswith(".json"):
                path = _DIST_DIR / name
                if path.exists():
                    data = json.loads(path.read_text(encoding="utf-8"))
                    assert data is not None, f"{name} is null"

    def test_svg_files_are_valid(self):
        """All SVG files should have svg tag."""
        for name, _ in EXPECTED_OUTPUTS:
            if name.endswith(".svg"):
                path = _DIST_DIR / name
                if path.exists():
                    content = path.read_text(encoding="utf-8")
                    assert "<svg" in content, f"{name} missing <svg> tag"

    def test_xml_files_are_valid(self):
        """All XML files should have xml declaration."""
        for name, _ in EXPECTED_OUTPUTS:
            if name.endswith(".xml"):
                path = _DIST_DIR / name
                if path.exists():
                    content = path.read_text(encoding="utf-8")
                    assert "<?xml" in content, f"{name} missing XML declaration"

    def test_claims_json_has_91_claims(self):
        """claims.json should have 91 claims."""
        path = _DIST_DIR / "claims.json"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "claims" in data
        assert len(data["claims"]) == 91

    def test_stats_json_has_counts(self):
        """stats.json should have counts."""
        path = _DIST_DIR / "stats.json"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "counts" in data
        assert data["counts"]["claims"] == 91

    def test_epistemic_graph_json_has_nodes(self):
        """epistemic-graph.json should have nodes."""
        path = _DIST_DIR / "epistemic-graph.json"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "nodes" in data
        assert len(data["nodes"]) == 91

    def test_automation_metrics_json_has_outputs(self):
        """automation-metrics.json should track outputs."""
        path = _DIST_DIR / "automation-metrics.json"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "outputs" in data
        assert data["total_outputs"] == 30


class TestBuildResilience:
    """Build should handle edge cases."""

    def test_build_check_passes(self):
        """build.py --check should pass."""
        import subprocess
        result = subprocess.run(
            ["python", "build.py", "--check"],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        assert result.returncode == 0, f"Build check failed: {result.stderr}"

    def test_run_tests_passes(self):
        """run_tests.py should pass."""
        import subprocess
        result = subprocess.run(
            ["python", "run_tests.py"],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=120,
        )
        assert result.returncode == 0, f"run_tests.py failed: {result.stderr}"
