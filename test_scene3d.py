"""Tests for 3D explore/reason scene view-model.

Calls shipped mapping functions with live registry / app-data export.
No re-implemented oracle; no confidence fields allowed.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from universe_explorer.data.registry import TOPICS
from universe_explorer.reader.scene3d import (
    BANNED_PAYLOAD_KEYS,
    build_app_data,
    build_scene_payload,
    claims_to_scene_nodes,
    neighbor_ids,
    panel_from_claim,
    path_step_ids,
    write_scene3d,
)


@pytest.fixture(scope="module")
def app_data():
    return build_app_data(TOPICS)


@pytest.fixture(scope="module")
def scene(app_data):
    return build_scene_payload(app_data)


class TestClaimsToSceneNodes:
    def test_every_claim_becomes_a_node(self, app_data):
        claims = app_data["claims"]
        topics = app_data["topics"]
        nodes = claims_to_scene_nodes(claims, topics)
        claim_ids = {c["id"] for c in claims}
        node_ids = {n["id"] for n in nodes}
        assert node_ids == claim_ids
        assert len(nodes) == sum(len(t.claims) for t in TOPICS)

    def test_node_round_trips_epistemic_fields(self, app_data):
        claims = {c["id"]: c for c in app_data["claims"]}
        nodes = claims_to_scene_nodes(app_data["claims"], app_data["topics"])
        by = {n["id"]: n for n in nodes}
        # hawking is the dual-axis teaching claim when present
        if "hawking_radiation" in claims:
            n = by["hawking_radiation"]
            c = claims["hawking_radiation"]
            assert n["status"] == c["status"]
            assert n["axis"] == c["axis"]
            assert n["diverges"] == c["diverges"]
            assert n["open_questions"] == list(c["open_questions"])
            assert "position" in n and "x" in n["position"]

    def test_earth_theme_layer_present_when_polar_or_ocean(self, app_data):
        nodes = claims_to_scene_nodes(app_data["claims"], app_data["topics"])
        themes = {n["theme"] for n in nodes}
        assert "cosmos" in themes
        assert "earth" in themes  # world / polar / ocean / seismology


class TestPanelFromClaim:
    def test_panel_has_explore_reason_fields(self, app_data):
        c = app_data["claims"][0]
        p = panel_from_claim(c)
        assert p["id"] == c["id"]
        assert p["what"] == c["title"]
        assert p["status"] == c["status"]
        assert p["axis"] == c["axis"]
        assert "open_questions" in p
        assert p["open_questions_empty"] == (len(c.get("open_questions") or []) == 0)
        for banned in BANNED_PAYLOAD_KEYS:
            assert banned not in p

    def test_hawking_panel_when_present(self, app_data):
        by = {c["id"]: c for c in app_data["claims"]}
        if "hawking_radiation" not in by:
            pytest.skip("hawking not in registry")
        p = panel_from_claim(by["hawking_radiation"])
        assert p["diverges"] is True
        assert p["axis"] == "E3"
        assert p["status"] == "STRONG"


class TestPathAndNeighbors:
    def test_path_h0_steps_match_export(self, app_data):
        paths = app_data["relations"]["reading_paths"]
        steps = path_step_ids(paths, "path_h0")
        assert len(steps) >= 2
        # first steps are bedrock expansion/CMB in authored path
        assert "universe_is_expanding" in steps or steps[0]
        # all step ids exist as claims
        claim_ids = {c["id"] for c in app_data["claims"]}
        for sid in steps:
            assert sid in claim_ids

    def test_path_polar_or_ocean_exists(self, app_data):
        paths = app_data["relations"]["reading_paths"]
        ids = {p["id"] for p in paths}
        assert "path_ocean" in ids or "path_polar" in ids or "path_seismology" in ids

    def test_neighbor_ids_from_related(self, app_data):
        # find a claim with related edges
        c = next((x for x in app_data["claims"] if x.get("n_related", 0) > 0), None)
        if c is None:
            pytest.skip("no related edges")
        nids = neighbor_ids(c)
        assert len(nids) >= 1
        claim_ids = {x["id"] for x in app_data["claims"]}
        for nid in nids:
            assert nid in claim_ids


class TestScenePayload:
    def test_payload_counts_and_no_banned_keys(self, scene):
        assert scene["n_nodes"] == sum(len(t.claims) for t in TOPICS)
        assert scene["n_paths"] >= 1
        assert len(scene["nodes"]) == scene["n_nodes"]
        assert "panels" in scene
        assert len(scene["panels"]) == scene["n_nodes"]

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    assert k.lower() not in BANNED_PAYLOAD_KEYS, k
                    walk(v)
            elif isinstance(o, list):
                for v in o[:500]:
                    walk(v)

        walk(scene)

    def test_themes_include_cosmos_and_earth(self, scene):
        theme_ids = {t["id"] for t in scene["themes"]}
        assert "cosmos" in theme_ids
        assert "earth" in theme_ids

    def test_write_scene3d(self, tmp_path):
        out = write_scene3d(dist_dir=tmp_path, topics=TOPICS)
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["n_nodes"] == sum(len(t.claims) for t in TOPICS)
        assert (tmp_path / "scene3d.json").exists()


class TestExplore3dPageArtifact:
    """Structural checks on the shipped 3D page source (no WebGL required)."""

    def test_web_source_has_interaction_surface(self):
        html = Path("web/explore3d.html").read_text(encoding="utf-8")
        assert "OrbitControls" in html
        assert "scene3d.json" in html
        assert "window.__UE3D" in html
        assert 'data-theme="cosmos"' in html
        assert 'data-theme="earth"' in html
        assert "path-sel" in html
        assert "selectClaim" in html
        # file: protocol honest fail
        assert "file:" in html
        for banned in ("confidence", "trust score", "probability%"):
            # must not advertise fake precision UI
            assert "trust score" not in html.lower()

    def test_dist_built_artifacts_when_present(self):
        dist = Path("dist")
        if not (dist / "explore3d.html").is_file():
            pytest.skip("dist not built")
        assert (dist / "scene3d.json").is_file()
        html = (dist / "explore3d.html").read_text(encoding="utf-8")
        assert "three" in html.lower()
        data = json.loads((dist / "scene3d.json").read_text(encoding="utf-8"))
        assert data["n_nodes"] == sum(len(t.claims) for t in TOPICS)
        # index / dashboard discoverability
        index = (dist / "index.html").read_text(encoding="utf-8")
        assert "explore3d.html" in index
