"""Build validation — measure dist/ before trusting a ship.

Hard rule: this file must run under ``python test_build_validation.py``
(used by run_tests.py). Pytest class collections that print nothing and
exit 0 are a blind spot — they were fixed here.

Counts are list counts from the live registry / EXPECTED_OUTPUTS —
never frozen vanity numbers.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from universe_explorer.data.registry import TOPICS
from universe_explorer.reader.automation_metrics import EXPECTED_OUTPUTS

_DIST = Path(__file__).resolve().parent / "dist"
_ROOT = Path(__file__).resolve().parent


def _n_claims() -> int:
    return sum(len(t.claims) for t in TOPICS)


def _ensure_dist() -> None:
    if not (_DIST / "index.html").is_file() or not (_DIST / "claims.json").is_file():
        r = subprocess.run(
            [sys.executable, str(_ROOT / "build.py")],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        assert r.returncode == 0, f"build.py failed:\n{r.stdout}\n{r.stderr}"


def test_all_expected_files_exist():
    _ensure_dist()
    missing = [name for name, _ in EXPECTED_OUTPUTS if not (_DIST / name).is_file()]
    assert missing == [], f"missing dist outputs: {missing}"


def test_html_files_have_doctype():
    _ensure_dist()
    bad = []
    for name, _ in EXPECTED_OUTPUTS:
        if not name.endswith(".html"):
            continue
        path = _DIST / name
        if not path.is_file():
            bad.append(f"{name}:absent")
            continue
        text = path.read_text(encoding="utf-8")
        if "<!DOCTYPE html>" not in text and "<!doctype html>" not in text:
            bad.append(name)
    assert bad == [], f"HTML missing DOCTYPE: {bad}"


def test_json_files_are_valid():
    _ensure_dist()
    bad = []
    for name, _ in EXPECTED_OUTPUTS:
        if not name.endswith(".json"):
            continue
        path = _DIST / name
        if not path.is_file():
            bad.append(f"{name}:absent")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            bad.append(f"{name}:{e}")
            continue
        if data is None:
            bad.append(f"{name}:null")
    assert bad == [], f"bad JSON: {bad}"


def test_svg_and_xml_shape():
    _ensure_dist()
    bad = []
    for name, _ in EXPECTED_OUTPUTS:
        path = _DIST / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if name.endswith(".svg") and "<svg" not in text:
            bad.append(name)
        if name.endswith(".xml") and "<?xml" not in text:
            bad.append(name)
    assert bad == [], f"bad SVG/XML: {bad}"


def test_claims_json_count_matches_registry():
    _ensure_dist()
    data = json.loads((_DIST / "claims.json").read_text(encoding="utf-8"))
    assert len(data["claims"]) == _n_claims()


def test_stats_json_count_matches_registry():
    _ensure_dist()
    data = json.loads((_DIST / "stats.json").read_text(encoding="utf-8"))
    n = _n_claims()
    # accept either nested counts or top-level fields
    if "counts" in data and isinstance(data["counts"], dict):
        assert data["counts"].get("claims") == n or data["counts"].get("n_claims") == n
    else:
        assert data.get("total_claims") == n or data.get("n_claims") == n


def test_epistemic_graph_node_count_matches_registry():
    _ensure_dist()
    data = json.loads((_DIST / "epistemic-graph.json").read_text(encoding="utf-8"))
    assert len(data["nodes"]) == _n_claims()


def test_automation_metrics_json_tracks_expected():
    _ensure_dist()
    path = _DIST / "automation-metrics.json"
    assert path.is_file(), "run build.py to emit automation-metrics.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["total_outputs"] == len(EXPECTED_OUTPUTS)
    assert data["missing_outputs"] == 0
    assert len(data["outputs"]) == len(EXPECTED_OUTPUTS)
    # no certainty vocabulary
    raw = json.dumps(data).lower()
    for banned in ("confidence", "trust_score", "probability"):
        assert banned not in raw or banned in (data.get("note") or "").lower()


def test_build_check_passes():
    r = subprocess.run(
        [sys.executable, str(_ROOT / "build.py"), "--check"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    assert r.returncode == 0, r.stdout + r.stderr


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
