"""UI domain-expand measurer.

Certainty about expand behaviour must *emerge* from counted measurements,
never from a declared "it works". This module:

1. Mirrors the accordion / cluster state machines used by the frontend
   (pure Python — no browser, no trust of runtime claims).
2. Probes source contracts in ``web/app.html``, ``web/universe.html``,
   and the index template in ``render.py``.
3. Emits a report of measurements only: each row is an observable
   (scenario step or contract needle) with pass/fail. No confidence
   field exists anywhere.

CLI::

    python -m universe_explorer.ui_expand
    python -m universe_explorer.ui_expand --json

Exit 0 only when every measurement passes.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parent.parent
APP_HTML = ROOT / "web" / "app.html"
UNI_HTML = ROOT / "web" / "universe.html"
RENDER_PY = ROOT / "universe_explorer" / "render.py"

# ---------------------------------------------------------------------------
# Measurement record (mechanical; no interpretation fields)
# ---------------------------------------------------------------------------

BANNED_REPORT_KEYS = frozenset({
    "confidence", "score", "probability", "certainty", "trust",
})


@dataclass(frozen=True)
class Measurement:
    """One observable. ``ok`` is a boolean gate, not a confidence."""
    id: str
    surface: str          # app | universe | index | data | scenario
    kind: str             # contract | scenario_step | inventory
    expected: Any
    observed: Any
    ok: bool
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        d = {
            "id": self.id,
            "surface": self.surface,
            "kind": self.kind,
            "expected": self.expected,
            "observed": self.observed,
            "ok": self.ok,
            "note": self.note,
        }
        assert not (set(d) & BANNED_REPORT_KEYS)
        return d


# ---------------------------------------------------------------------------
# Pure state machines (mirror JS in app.html / universe.html)
# ---------------------------------------------------------------------------

@dataclass
class AppExpandState:
    """Mirrors ``state`` fields that govern domain expand in app.html."""
    topic: str = ""
    theme: str = ""
    open_domains: dict[str, bool] = field(default_factory=dict)

    def is_open(self, domain_id: str) -> bool:
        return bool(self.open_domains.get(domain_id))


def app_auto_expand(state: AppExpandState, topics_in_view: list[str]) -> None:
    """Mirror renderCards auto-expand rules."""
    if state.topic:
        state.open_domains[state.topic] = True
    if len(topics_in_view) == 1:
        state.open_domains[topics_in_view[0]] = True


def app_click_domain_head(state: AppExpandState, domain_id: str) -> bool:
    """Mirror domain-head click. Returns the new open flag."""
    will_open = not state.is_open(domain_id)
    state.open_domains[domain_id] = will_open
    return will_open


def app_select_topic_chip(state: AppExpandState, domain_id: str) -> None:
    """Mirror topic chip click: filter + force open when non-empty."""
    state.topic = domain_id
    if domain_id:
        state.open_domains[domain_id] = True


def app_topics_in_view(
    all_topic_ids: list[str],
    claims_by_topic: dict[str, list[str]],
    *,
    topic: str = "",
    theme_of: dict[str, str] | None = None,
    theme: str = "",
) -> list[str]:
    """Mirror which domain blocks appear (topic/theme filter + non-empty)."""
    theme_of = theme_of or {}
    out: list[str] = []
    for tid in all_topic_ids:
        if theme and theme_of.get(tid) != theme:
            continue
        if topic and tid != topic:
            continue
        if claims_by_topic.get(tid):
            out.append(tid)
    return out


@dataclass
class UniExpandState:
    expand_id: str | None = None


def uni_expand_cluster(state: UniExpandState, domain_id: str) -> str | None:
    """Mirror expandCluster: toggle expandId."""
    state.expand_id = None if state.expand_id == domain_id else domain_id
    return state.expand_id


@dataclass
class IndexExpandState:
    open_topics: set[str] = field(default_factory=set)

    def is_open(self, topic_id: str) -> bool:
        return topic_id in self.open_topics


def index_toggle(state: IndexExpandState, topic_id: str) -> bool:
    if topic_id in state.open_topics:
        state.open_topics.discard(topic_id)
        return False
    state.open_topics.add(topic_id)
    return True


def index_deeplink(state: IndexExpandState, topic_id: str) -> None:
    state.open_topics.add(topic_id)


# ---------------------------------------------------------------------------
# Contract probes (source text must contain the wiring)
# ---------------------------------------------------------------------------

APP_CONTRACTS: list[tuple[str, str]] = [
    ("app.openDomains_state", "openDomains"),
    ("app.domain_block_css", ".domain-block"),
    ("app.domain_head_control", "domain-head"),
    ("app.toggle_open_class", 'classList.toggle("open"'),
    ("app.chip_auto_expand", "state.openDomains[id] = true"),
    ("app.auto_expand_selected_topic", "if (state.topic) state.openDomains[state.topic] = true"),
    ("app.auto_expand_single", "if (topics.length === 1) state.openDomains[topics[0].id] = true"),
    ("app.aria_expanded", "aria-expanded"),
    ("app.zh_hint", "點領域即可展開底下的宣稱"),
    ("app.zh_claims_word", "則宣稱"),
    ("app.measure_hook", "__UE_MEASURE__"),
    ("app.measure_rec_expand", "domain_expand"),
]

UNI_CONTRACTS: list[tuple[str, str]] = [
    ("uni.expand_cluster_fn", "function expandCluster"),
    ("uni.expand_id_state", "expandId"),
    ("uni.label_click", "expandCluster(c.id)"),
    ("uni.nav_click", "expandCluster(b.dataset.a.slice(2))"),
    ("uni.stars_layout", "stars:[-80,200]"),
    ("uni.measure_hook", "__UE_MEASURE__"),
    ("uni.measure_rec_expand", "cluster_expand"),
]

INDEX_CONTRACTS: list[tuple[str, str]] = [
    ("index.topic_toggle", "topic-toggle"),
    ("index.open_css", ".topic-card.open"),
    ("index.deeplink_open", 'get("open")'),
    ("index.toggle_open", 'classList.toggle("open"'),
    ("index.claim_list", "claim-list"),
    ("index.data_topic_attr", 'data-topic="'),
]


def probe_contracts(text: str, surface: str,
                    pairs: Iterable[tuple[str, str]]) -> list[Measurement]:
    out: list[Measurement] = []
    for mid, needle in pairs:
        present = needle in text
        out.append(Measurement(
            id=mid,
            surface=surface,
            kind="contract",
            expected=f"contains {needle!r}",
            observed=present,
            ok=present,
            note="source contract",
        ))
    return out


# ---------------------------------------------------------------------------
# Scenario runner
# ---------------------------------------------------------------------------

def _m(scenario: str, step: str, expected: Any, observed: Any,
       note: str = "") -> Measurement:
    return Measurement(
        id=f"{scenario}.{step}",
        surface="scenario",
        kind="scenario_step",
        expected=expected,
        observed=observed,
        ok=expected == observed,
        note=note,
    )


def run_app_scenarios(
    topic_ids: list[str],
    claims_by_topic: dict[str, list[str]],
    theme_of: dict[str, str],
    focus: str = "stars",
) -> list[Measurement]:
    ms: list[Measurement] = []
    n_focus = len(claims_by_topic.get(focus, []))

    # S1: default all-domains view — focus collapsed
    st = AppExpandState()
    view = app_topics_in_view(topic_ids, claims_by_topic, theme_of=theme_of)
    app_auto_expand(st, view)
    ms.append(_m("app_default", "focus_closed", False, st.is_open(focus),
                 "all domains: not auto-opened"))
    ms.append(_m("app_default", "view_has_focus", True, focus in view,
                 "focus domain is listed"))
    ms.append(_m("app_default", "view_count_gt1", True, len(view) > 1,
                 "multi-domain view"))

    # S2: click domain head → open
    opened = app_click_domain_head(st, focus)
    ms.append(_m("app_click_open", "returns_true", True, opened))
    ms.append(_m("app_click_open", "is_open", True, st.is_open(focus)))
    # independence: another domain still closed
    other = next((t for t in view if t != focus), None)
    if other:
        ms.append(_m("app_click_open", "other_still_closed", False,
                     st.is_open(other), f"other={other}"))

    # S3: click again → collapse
    closed = app_click_domain_head(st, focus)
    ms.append(_m("app_click_close", "returns_false", False, closed))
    ms.append(_m("app_click_close", "is_closed", False, st.is_open(focus)))

    # S4: topic chip selects + auto-opens
    st2 = AppExpandState()
    app_select_topic_chip(st2, focus)
    view2 = app_topics_in_view(topic_ids, claims_by_topic, topic=st2.topic,
                              theme_of=theme_of)
    app_auto_expand(st2, view2)
    ms.append(_m("app_chip", "topic_set", focus, st2.topic))
    ms.append(_m("app_chip", "is_open", True, st2.is_open(focus)))
    ms.append(_m("app_chip", "single_in_view", True, view2 == [focus]))
    ms.append(_m("app_chip", "claim_count", n_focus,
                 len(claims_by_topic[focus]),
                 "claims under focus domain"))

    # S5: clearing chip keeps prior open_domains entry (JS does not wipe)
    st2.topic = ""
    view3 = app_topics_in_view(topic_ids, claims_by_topic, theme_of=theme_of)
    app_auto_expand(st2, view3)
    ms.append(_m("app_chip_clear", "focus_stays_open", True, st2.is_open(focus),
                 "openDomains persists after All"))

    # S6: single-domain theme filter auto-opens only when length==1
    # (if cosmos has multiple topics, no force-open of all)
    st3 = AppExpandState(theme="cosmos")
    view_c = app_topics_in_view(
        topic_ids, claims_by_topic, theme="cosmos", theme_of=theme_of)
    app_auto_expand(st3, view_c)
    if len(view_c) == 1:
        ms.append(_m("app_theme", "single_auto_open", True,
                     st3.is_open(view_c[0])))
    else:
        ms.append(_m("app_theme", "multi_no_mass_open", False,
                     any(st3.is_open(t) for t in view_c),
                     f"cosmos domains in view: {len(view_c)}"))

    return ms


def run_uni_scenarios(focus: str = "stars") -> list[Measurement]:
    ms: list[Measurement] = []
    st = UniExpandState()
    ms.append(_m("uni_default", "expand_id_null", None, st.expand_id))

    r1 = uni_expand_cluster(st, focus)
    ms.append(_m("uni_expand", "id_set", focus, r1))
    ms.append(_m("uni_expand", "state", focus, st.expand_id))

    r2 = uni_expand_cluster(st, focus)
    ms.append(_m("uni_collapse", "id_cleared", None, r2))
    ms.append(_m("uni_collapse", "state", None, st.expand_id))

    uni_expand_cluster(st, focus)
    uni_expand_cluster(st, "cosmology")
    ms.append(_m("uni_switch", "to_other", "cosmology", st.expand_id,
                 "expand other replaces focus"))
    return ms


def run_index_scenarios(focus: str = "stars") -> list[Measurement]:
    ms: list[Measurement] = []
    st = IndexExpandState()
    ms.append(_m("index_default", "closed", False, st.is_open(focus)))

    o1 = index_toggle(st, focus)
    ms.append(_m("index_toggle_open", "returns_true", True, o1))
    ms.append(_m("index_toggle_open", "is_open", True, st.is_open(focus)))

    o2 = index_toggle(st, focus)
    ms.append(_m("index_toggle_close", "returns_false", False, o2))
    ms.append(_m("index_toggle_close", "is_closed", False, st.is_open(focus)))

    st2 = IndexExpandState()
    index_deeplink(st2, focus)
    ms.append(_m("index_deeplink", "opens", True, st2.is_open(focus)))
    return ms


# ---------------------------------------------------------------------------
# Inventory measurements from app-data
# ---------------------------------------------------------------------------

def run_inventory(data: dict[str, Any], focus: str = "stars") -> list[Measurement]:
    ms: list[Measurement] = []
    topics = {t["id"]: t for t in data.get("topics", [])}
    claims = data.get("claims", [])
    by_topic: dict[str, list[str]] = {}
    for c in claims:
        by_topic.setdefault(c["topic"], []).append(c["id"])

    ms.append(Measurement(
        id="data.focus_topic_present",
        surface="data",
        kind="inventory",
        expected=True,
        observed=focus in topics,
        ok=focus in topics,
        note=f"topic id {focus}",
    ))
    if focus not in topics:
        return ms

    t = topics[focus]
    n = len(by_topic.get(focus, []))
    ms.append(Measurement(
        id="data.focus_title_zh",
        surface="data",
        kind="inventory",
        expected="恆星",
        observed=t.get("title_zh"),
        ok=t.get("title_zh") == "恆星",
    ))
    ms.append(Measurement(
        id="data.focus_n_claims_field",
        surface="data",
        kind="inventory",
        expected=n,
        observed=t.get("n_claims"),
        ok=t.get("n_claims") == n,
        note="n_claims must equal counted claims",
    ))
    ms.append(Measurement(
        id="data.focus_claim_count_positive",
        surface="data",
        kind="inventory",
        expected=True,
        observed=n >= 1,
        ok=n >= 1,
        note=f"n={n}",
    ))
    # ban confidence-like keys in payload
    def walk(x: Any, path: str = "") -> list[str]:
        bad: list[str] = []
        if isinstance(x, dict):
            for k, v in x.items():
                if k.lower() in BANNED_REPORT_KEYS:
                    bad.append(f"{path}.{k}" if path else k)
                bad.extend(walk(v, f"{path}.{k}" if path else k))
        elif isinstance(x, list):
            for i, v in enumerate(x[:50]):
                bad.extend(walk(v, f"{path}[{i}]"))
        return bad

    banned_hits = walk(data)
    ms.append(Measurement(
        id="data.no_banned_certainty_keys",
        surface="data",
        kind="inventory",
        expected=[],
        observed=banned_hits,
        ok=not banned_hits,
        note="confidence/score/probability/certainty/trust forbidden",
    ))
    return ms


# ---------------------------------------------------------------------------
# Full measure pipeline
# ---------------------------------------------------------------------------

def load_app_data() -> dict[str, Any]:
    """Prefer live engine export; fall back to dist if present."""
    try:
        from universe_explorer.data.registry import TOPICS
        from universe_explorer.render import app_data_json
        return json.loads(app_data_json(TOPICS))
    except Exception:
        p = ROOT / "dist" / "app-data.json"
        return json.loads(p.read_text(encoding="utf-8"))


def measure(focus: str = "stars") -> dict[str, Any]:
    """Run every probe. Returns a report dict with only mechanical fields."""
    data = load_app_data()
    claims_by_topic: dict[str, list[str]] = {}
    theme_of: dict[str, str] = {}
    topic_ids: list[str] = []
    for t in data.get("topics", []):
        topic_ids.append(t["id"])
        theme_of[t["id"]] = t.get("theme") or "cosmos"
    for c in data.get("claims", []):
        claims_by_topic.setdefault(c["topic"], []).append(c["id"])

    measurements: list[Measurement] = []
    measurements.extend(run_inventory(data, focus=focus))
    measurements.extend(run_app_scenarios(
        topic_ids, claims_by_topic, theme_of, focus=focus))
    measurements.extend(run_uni_scenarios(focus=focus))
    measurements.extend(run_index_scenarios(focus=focus))

    app_text = APP_HTML.read_text(encoding="utf-8") if APP_HTML.exists() else ""
    uni_text = UNI_HTML.read_text(encoding="utf-8") if UNI_HTML.exists() else ""
    # index contracts live in render.py template (source of truth)
    render_text = RENDER_PY.read_text(encoding="utf-8") if RENDER_PY.exists() else ""

    measurements.extend(probe_contracts(app_text, "app", APP_CONTRACTS))
    measurements.extend(probe_contracts(uni_text, "universe", UNI_CONTRACTS))
    measurements.extend(probe_contracts(render_text, "index", INDEX_CONTRACTS))

    rows = [m.as_dict() for m in measurements]
    n_pass = sum(1 for m in measurements if m.ok)
    n_fail = sum(1 for m in measurements if not m.ok)
    report = {
        "kind": "ui_expand_measure",
        "focus": focus,
        "n_measurements": len(measurements),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "all_ok": n_fail == 0,
        "measurements": rows,
    }
    # constitution: report itself invents no certainty numbers
    assert not (set(report) & BANNED_REPORT_KEYS)
    return report


def format_text_report(report: dict[str, Any]) -> str:
    lines = [
        f"ui_expand_measure  focus={report['focus']}",
        f"measurements: {report['n_pass']}/{report['n_measurements']} pass"
        f"  fail={report['n_fail']}",
        "",
    ]
    for m in report["measurements"]:
        mark = "OK  " if m["ok"] else "FAIL"
        lines.append(
            f"  {mark} [{m['surface']}/{m['kind']}] {m['id']}"
            f"  expected={m['expected']!r} observed={m['observed']!r}"
            + (f"  ({m['note']})" if m.get("note") else "")
        )
    lines.append("")
    lines.append("all_ok" if report["all_ok"] else "HAS_FAILURES")
    lines.append(
        "Note: pass counts are counts of measurements — not a confidence score."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(description="Measure domain-expand UI behaviour")
    p.add_argument("--focus", default="stars", help="domain id to centre on")
    p.add_argument("--json", action="store_true", help="emit JSON report")
    p.add_argument("--out", type=Path, default=None,
                   help="optional path to write JSON report")
    args = p.parse_args(argv)

    report = measure(focus=args.focus)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_text_report(report))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
