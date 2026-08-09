"""UI domain-expand measurer acceptance.

Run: python test_ui_expand.py
     python -m universe_explorer.ui_expand

Trust does not precede measurement. The gate is: every counted measurement
passes. There is no confidence field.
"""

from __future__ import annotations

import json
from pathlib import Path

from universe_explorer import ui_expand as U


def test_measure_all_ok_for_stars():
    report = U.measure(focus="stars")
    assert report["kind"] == "ui_expand_measure"
    assert report["focus"] == "stars"
    assert report["n_measurements"] >= 20
    assert report["n_pass"] == report["n_measurements"]
    assert report["n_fail"] == 0
    assert report["all_ok"] is True


def test_report_invents_no_certainty_fields():
    report = U.measure(focus="stars")
    banned = U.BANNED_REPORT_KEYS

    def walk(x, path=""):
        if isinstance(x, dict):
            for k, v in x.items():
                assert k.lower() not in banned, (path, k)
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")

    walk(report)


def test_report_counts_are_list_counts():
    """n_pass + n_fail == n_measurements — recount them yourself."""
    report = U.measure(focus="stars")
    assert report["n_pass"] + report["n_fail"] == report["n_measurements"]
    assert len(report["measurements"]) == report["n_measurements"]
    assert sum(1 for m in report["measurements"] if m["ok"]) == report["n_pass"]


def test_app_state_machine_toggle_independence():
    st = U.AppExpandState()
    assert U.app_click_domain_head(st, "stars") is True
    assert st.is_open("stars") is True
    assert st.is_open("cosmology") is False
    assert U.app_click_domain_head(st, "stars") is False
    assert st.is_open("stars") is False


def test_chip_forces_open_and_filters_view():
    data = U.load_app_data()
    topic_ids = [t["id"] for t in data["topics"]]
    theme_of = {t["id"]: t.get("theme") or "cosmos" for t in data["topics"]}
    claims_by = {}
    for c in data["claims"]:
        claims_by.setdefault(c["topic"], []).append(c["id"])
    st = U.AppExpandState()
    U.app_select_topic_chip(st, "stars")
    view = U.app_topics_in_view(topic_ids, claims_by, topic=st.topic, theme_of=theme_of)
    U.app_auto_expand(st, view)
    assert view == ["stars"]
    assert st.is_open("stars")
    assert len(claims_by["stars"]) == 6


def test_universe_cluster_toggle():
    st = U.UniExpandState()
    assert U.uni_expand_cluster(st, "stars") == "stars"
    assert U.uni_expand_cluster(st, "stars") is None
    U.uni_expand_cluster(st, "stars")
    assert U.uni_expand_cluster(st, "dark_matter") == "dark_matter"


def test_index_deeplink_and_toggle():
    st = U.IndexExpandState()
    U.index_deeplink(st, "stars")
    assert st.is_open("stars")
    assert U.index_toggle(st, "stars") is False
    assert not st.is_open("stars")


def test_contracts_require_measure_hooks():
    """Runtime channel is opt-in, but the wiring must be present to measure."""
    app = Path("web/app.html").read_text(encoding="utf-8")
    uni = Path("web/universe.html").read_text(encoding="utf-8")
    assert "__UE_MEASURE__" in app and "domain_expand" in app
    assert "__UE_MEASURE__" in uni and "cluster_expand" in uni
    assert "Measure.rec" in app and "Measure.rec" in uni


def test_cli_exit_zero_when_green():
    assert U.main(["--focus", "stars"]) == 0


def test_json_report_roundtrip_shape():
    report = U.measure(focus="stars")
    blob = json.dumps(report)
    again = json.loads(blob)
    assert again["n_fail"] == 0
    assert again["measurements"][0]["id"]


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
