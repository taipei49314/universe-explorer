"""Claim relations + inference acceptance. Run: python test_relations.py"""

from __future__ import annotations

import json

from universe_explorer.data.registry import TOPICS
from universe_explorer.relations import (
    BANNED_KEYS,
    authored_links,
    claim_index,
    format_claim_report,
    infer_paths,
    neighbors,
    relations_payload,
    validate_links,
)
from universe_explorer.render import app_data_json


def test_authored_graph_validates():
    assert validate_links(TOPICS) == []
    assert len(authored_links()) >= 40


def test_payload_has_no_certainty_fields():
    payload = relations_payload(TOPICS)

    def walk(x, path=""):
        if isinstance(x, dict):
            for k, v in x.items():
                assert k.lower() not in BANNED_KEYS, (path, k)
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x[:30]):
                walk(v, f"{path}[{i}]")

    walk(payload)


def test_payload_counts_are_list_counts():
    payload = relations_payload(TOPICS)
    assert payload["n_links"] == len(payload["links"])
    assert payload["n_authored"] + payload["n_mechanical"] == payload["n_links"]
    assert payload["n_authored"] == len(authored_links())


def test_h0_umbrella_has_specializations():
    payload = relations_payload(TOPICS)
    rel = payload["by_claim"]["H0_tension_local_vs_cmb"]["related"]
    kinds_to = {(r["kind"], r["id"]) for r in rel if r["direction"] == "out"}
    # specializes edges stored as out from umbrella
    targets = {r["id"] for r in rel if r["kind"] == "specializes"}
    assert "shoes_local_H0_high" in targets or any(
        r["id"] == "shoes_local_H0_high" for r in rel
    )
    assert any(r["id"] == "cmb_lcdm_implies_low_H0" for r in rel)


def test_inference_paths_are_transparent_lists():
    links = authored_links()
    paths = infer_paths("stars_powered_by_fusion", links, max_depth=2)
    assert paths
    for p in paths:
        assert "path" in p and "kinds" in p and "depth" in p
        assert p["depth"] == len(p["path"]) - 1
        assert "confidence" not in p and "score" not in p


def test_neighbors_bidirectional():
    links = authored_links()
    # A supports B ⇒ B lists inbound supported_by A
    out = neighbors("event_horizon_exists", links)
    assert any(r["id"] == "kerr_describes_astrophysical_bh" for r in out)
    back = neighbors("kerr_describes_astrophysical_bh", links)
    assert any(
        r["id"] == "event_horizon_exists" and r["direction"] == "in"
        for r in back
    )


def test_app_data_embeds_related():
    data = json.loads(app_data_json(TOPICS))
    assert "relations" in data
    assert data["relations"]["n_authored"] >= 40
    c = next(x for x in data["claims"] if x["id"] == "event_horizon_exists")
    assert "related" in c and "inferences" in c
    assert c["n_related"] == len(c["related"])
    assert c["n_inferences"] == len(c["inferences"])
    # at least one authored relation
    assert c["n_related"] >= 1


def test_every_claim_has_relation_block():
    payload = relations_payload(TOPICS)
    idx = claim_index(TOPICS)
    assert set(payload["by_claim"]) == set(idx)


def test_cli_report_runs():
    text = format_claim_report("H0_tension_local_vs_cmb", TOPICS)
    assert "H0_tension_local_vs_cmb" in text
    assert "related:" in text


def test_boundary_cross_domain():
    """Stars PISN gap boundaries black_hole lower mass gap — distinct nodes."""
    links = authored_links()
    n = neighbors("pair_instability_bh_mass_gap", links)
    assert any(r["id"] == "lower_mass_gap_compact_objects" for r in n)


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
