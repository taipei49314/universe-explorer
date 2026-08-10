"""P-Pulse / P-Audit surface pages. Run: python test_surface.py"""

from __future__ import annotations

import json
from pathlib import Path

from universe_explorer.data.registry import TOPICS
from universe_explorer.surface import (
    health_payload,
    render_changes_html,
    render_health_html,
    sample_claims,
    write_surface_pages,
)


def test_health_payload_counts():
    p = health_payload(TOPICS)
    assert p["n_claims"] == sum(len(t.claims) for t in TOPICS)
    assert p["n_topics"] == len(TOPICS)
    assert len(p["audit_sample"]) == 3
    assert "confidence" not in json.dumps(p)


def test_sample_stable_for_day():
    a = [c["id"] for c in sample_claims(TOPICS, day="2026-08-09")]
    b = [c["id"] for c in sample_claims(TOPICS, day="2026-08-09")]
    assert a == b
    c = [c["id"] for c in sample_claims(TOPICS, day="2026-08-10")]
    # different day may differ; at least same length
    assert len(c) == 3


def test_health_html_has_nav():
    html = render_health_html(health_payload(TOPICS))
    assert "health.json" in html and "challenge" in html.lower()
    # Phase 1–3 + dashboard/stats stay one hop from the audit page
    for href in (
        "explore-v2.html",
        "epistemic_map.html",
        "challenge.html",
        "dashboard.html",
        "stats.json",
    ):
        assert href in html, href


def test_changes_html_renders():
    html = render_changes_html()
    assert "Changes" in html and "feed.xml" in html


def test_write_surface_pages(tmp_path: Path = None):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        write_surface_pages(out, TOPICS)
        assert (out / "health.json").is_file()
        assert (out / "health.html").is_file()
        assert (out / "changes.html").is_file()
        data = json.loads((out / "health.json").read_text(encoding="utf-8"))
        assert data["n_claims"] >= 1


def test_app_html_product_surface():
    app = Path("web/app.html").read_text(encoding="utf-8")
    for needle in (
        "topnav", "tour", "applyDeepLink", "compare-section",
        "qchips", "pathguide", "panelAdvanced", "tour_step",
        "deep_link_open", "relDisclaimer",
    ):
        assert needle in app, needle


def test_reading_paths_have_guides():
    from universe_explorer.relations import reading_paths
    with_guide = [p for p in reading_paths() if p.guide]
    assert len(with_guide) >= 5


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
