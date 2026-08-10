"""Trust-behavior measurer.

Philosophy (same as ui_expand):
  Measure first. Trust only what the counts show.
  Behaviours users would otherwise *trust* are reduced to observables —
  expected vs observed + boolean ok. No confidence / score / trust fields.

What counts as a "trust behaviour" here
---------------------------------------
Anything a reader might accept as authority without re-checking:

  • dual-axis export honesty (diverges / evidence grade match the engine)
  • every evidence item hangs on a resolvable source
  • status lights carry overturnable status_reason (entry conditions)
  • public JSON never invents banned certainty vocabulary
  • challenge surfaces exist (overturn is a product path, not a slogan)
  • UI contracts: tour denies confidence %, diverge / challenge copy present
  • canonical stress case (hawking_radiation) still shows axis split
  • every domain has an authored reading path (navigation, not ranking)

CLI::

    python -m universe_explorer.trust_behavior
    python -m universe_explorer.trust_behavior --json
    python -m universe_explorer.trust_behavior --out health/trust-behavior.json

Exit 0 only when n_fail == 0.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence

from .axes import derive, diverges
from .model import Claim, Status, Topic
from .relations import reading_paths, validate_links
from .validator import validate_claim

ROOT = Path(__file__).resolve().parent.parent
WEB_APP = ROOT / "web" / "app.html"
WEB_UNI = ROOT / "web" / "universe.html"
ISSUE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
DIST = ROOT / "dist"

BANNED_REPORT_KEYS = frozenset({
    "confidence", "score", "probability", "certainty", "trust",
})

# Keys that must not appear as JSON *field names* in public exports.
BANNED_PAYLOAD_KEYS = frozenset({
    "confidence", "score", "probability", "certainty", "trust",
    "trust_score", "confidence_score", "p_value",
})

# Controlled substring bans in free text of *exports* (case-insensitive).
# Deliberately narrow — measured %, "confidence interval" in evidence
# descriptions may be scientific language; we ban *declared* confidence.
BANNED_TEXT_PATTERNS = (
    re.compile(r"\bconfidence\s*[:=]\s*\d", re.I),
    re.compile(r"\btrust\s*score\b", re.I),
    re.compile(r"\bcertainty\s*[:=]\s*\d", re.I),
)


@dataclass(frozen=True)
class Measurement:
    """One observable. ``ok`` is a gate, not a confidence."""

    id: str
    surface: str   # claim | export | surface | contract | inventory | stress
    kind: str      # dual_axis | provenance | overturn | constitution | ui | path
    expected: Any
    observed: Any
    ok: bool
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        d = {
            "id": self.id,
            "surface": self.surface,
            "kind": self.kind,
            "expected": _jsonable(self.expected),
            "observed": _jsonable(self.observed),
            "ok": self.ok,
            "note": self.note,
        }
        assert not (set(d) & BANNED_REPORT_KEYS)
        return d


def _jsonable(x: Any) -> Any:
    """Reports must serialize; enums / paths become strings (no interpretation)."""
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, Status):
        return x.name
    if isinstance(x, Path):
        return str(x)
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if hasattr(x, "name") and not isinstance(x, type):
        try:
            return x.name  # Enum-like
        except Exception:
            pass
    return str(x)


def _m(mid: str, surface: str, kind: str, expected: Any, observed: Any,
       note: str = "") -> Measurement:
    return Measurement(
        id=mid,
        surface=surface,
        kind=kind,
        expected=expected,
        observed=observed,
        ok=(expected == observed),
        note=note,
    )


def _m_bool(mid: str, surface: str, kind: str, ok: bool,
            expected: Any, observed: Any, note: str = "") -> Measurement:
    return Measurement(
        id=mid, surface=surface, kind=kind,
        expected=expected, observed=observed, ok=ok, note=note,
    )


# ---------------------------------------------------------------------------
# Claim-level trust behaviours (pure engine — no browser)
# ---------------------------------------------------------------------------

def measure_claim(claim: Claim, topic_id: str = "") -> List[Measurement]:
    """Observables for one claim a reader might trust."""
    ms: List[Measurement] = []
    prefix = f"{topic_id + ':' if topic_id else ''}{claim.id}"

    # 1. Evidence hangs on resolvable sources
    labels = {s.label for s in claim.sources}
    dangling = [e.source_ref for e in claim.evidence if e.source_ref not in labels]
    ms.append(_m_bool(
        f"{prefix}.evidence_sources_resolve",
        "claim", "provenance",
        ok=len(dangling) == 0,
        expected=[],
        observed=dangling,
        note="every evidence.source_ref must resolve to a Source.label",
    ))

    # 2. Validator (constitution court)
    viol = validate_claim(claim)
    ms.append(_m_bool(
        f"{prefix}.constitution_pass",
        "claim", "constitution",
        ok=(len(viol) == 0),
        expected=0,
        observed=len(viol),
        note="; ".join(f"{v.rule}:{v.detail}" for v in viol[:4]) if viol else "",
    ))

    # 3. Dual-axis: diverges is mechanical, not opinion
    d = derive(claim)
    div = diverges(claim)
    high = claim.status in (Status.ESTABLISHED, Status.STRONG)
    weak_ev = d.strength.name.startswith("E3") or d.strength.name.startswith("E4") or d.strength.name.startswith("E5")
    expected_div = high and weak_ev
    ms.append(_m(
        f"{prefix}.diverges_matches_rule",
        "claim", "dual_axis",
        expected_div, div,
        note=f"status={claim.status.name} axis={d.strength.short}",
    ))

    # 4. status_reason present for non-empty judgement
    #    (FRONTIER/SPECULATIVE mode=any still need at least one holding reason in live data)
    ms.append(_m_bool(
        f"{prefix}.status_reason_nonempty",
        "claim", "overturn",
        ok=len(claim.status_reason) > 0,
        expected="≥1 status_reason line",
        observed=len(claim.status_reason),
        note="overturn path needs entry conditions",
    ))

    # 5. No banned certainty vocabulary in free-text notes / descriptions
    blobs = [claim.title]
    for e in claim.evidence:
        blobs.append(e.description)
    for ca in claim.status_reason:
        blobs.append(ca.note)
    for oq in claim.open_questions:
        blobs.append(oq)
    joined = "\n".join(blobs)
    hits = [p.pattern for p in BANNED_TEXT_PATTERNS if p.search(joined)]
    ms.append(_m_bool(
        f"{prefix}.no_declared_confidence_text",
        "claim", "constitution",
        ok=len(hits) == 0,
        expected=[],
        observed=hits,
        note="declared confidence / trust score language",
    ))

    return ms


def measure_topics(topics: Sequence[Topic]) -> List[Measurement]:
    ms: List[Measurement] = []
    for t in topics:
        for c in t.claims:
            ms.extend(measure_claim(c, t.id))
    return ms


# ---------------------------------------------------------------------------
# Inventory / graph trust behaviours
# ---------------------------------------------------------------------------

def measure_inventory(topics: Sequence[Topic]) -> List[Measurement]:
    ms: List[Measurement] = []
    n_topics = len(topics)
    n_claims = sum(len(t.claims) for t in topics)
    ms.append(_m_bool(
        "inventory.nonempty",
        "inventory", "path",
        ok=(n_topics > 0 and n_claims > 0),
        expected="topics>0 and claims>0",
        observed={"n_topics": n_topics, "n_claims": n_claims},
    ))

    # Every domain has ≥1 authored reading path that touches it
    paths = reading_paths()
    claim_to_topic = {c.id: t.id for t in topics for c in t.claims}
    domains_with_path = set()
    for rp in paths:
        for step in rp.steps:
            if step in claim_to_topic:
                domains_with_path.add(claim_to_topic[step])
    topic_ids = {t.id for t in topics}
    missing_paths = sorted(topic_ids - domains_with_path)
    ms.append(_m_bool(
        "inventory.every_domain_has_reading_path",
        "inventory", "path",
        ok=len(missing_paths) == 0,
        expected=[],
        observed=missing_paths,
        note="navigation path, not a ranking",
    ))

    # Authored graph validates
    link_bad = validate_links(topics)
    ms.append(_m_bool(
        "inventory.authored_links_valid",
        "inventory", "path",
        ok=len(link_bad) == 0,
        expected=0,
        observed=len(link_bad),
        note="; ".join(link_bad[:3]) if link_bad else "",
    ))

    # Dual-axis stress inventory: at least one diverging claim exists
    n_div = sum(1 for t in topics for c in t.claims if diverges(c))
    ms.append(_m_bool(
        "inventory.has_divergence_stress_case",
        "inventory", "dual_axis",
        ok=n_div >= 1,
        expected="≥1 diverging claim",
        observed=n_div,
        note="system must show axis split somewhere, not hide it",
    ))
    return ms


def measure_stress_hawking(topics: Sequence[Topic]) -> List[Measurement]:
    """Canonical dual-axis stress case the about page teaches."""
    ms: List[Measurement] = []
    claim = None
    for t in topics:
        for c in t.claims:
            if c.id == "hawking_radiation":
                claim = c
                break
    ms.append(_m_bool(
        "stress.hawking_present",
        "stress", "dual_axis",
        ok=claim is not None,
        expected="hawking_radiation in registry",
        observed=claim is not None,
    ))
    if claim is None:
        return ms
    ms.append(_m(
        "stress.hawking_status_strong",
        "stress", "dual_axis",
        Status.STRONG, claim.status,
        note="canonical about example",
    ))
    ms.append(_m(
        "stress.hawking_diverges",
        "stress", "dual_axis",
        True, diverges(claim),
        note="Strong × non-direct evidence",
    ))
    axis = derive(claim)
    ms.append(_m_bool(
        "stress.hawking_axis_not_direct",
        "stress", "dual_axis",
        ok=axis.strength.short in ("E3", "E4", "E5"),
        expected="E3|E4|E5",
        observed=axis.strength.short,
    ))
    return ms


# ---------------------------------------------------------------------------
# Surface contracts (static files — no browser)
# ---------------------------------------------------------------------------

def measure_ui_contracts() -> List[Measurement]:
    ms: List[Measurement] = []
    app = WEB_APP.read_text(encoding="utf-8") if WEB_APP.is_file() else ""
    uni = WEB_UNI.read_text(encoding="utf-8") if WEB_UNI.is_file() else ""

    contracts = [
        ("ui.app_exists", WEB_APP.is_file(), "web/app.html present"),
        ("ui.app_tour",
         "showTour" in app and "id=\"tour\"" in app,
         "60s tour surface"),
        ("ui.app_no_confidence_tour",
         "no confidence" in app.lower() or "Two axes, no confidence" in app,
         "tour denies confidence %"),
        ("ui.app_diverge_copy", "diverge" in app.lower(), "axes diverge copy"),
        ("ui.app_challenge_copy", "challenge" in app.lower(), "challenge CTA"),
        ("ui.app_measure_channel",
         "__UE_MEASURE__" in app or "ue_measure" in app or "Measure.rec" in app,
         "opt-in measure log"),
        ("ui.app_deeplink_c",
         "applyDeepLink" in app or "deep_link" in app or "?c=" in app,
         "claim deep-link"),
        ("ui.universe_exists", WEB_UNI.is_file(), "web/universe.html present"),
    ]
    for mid, ok, note in contracts:
        ms.append(_m_bool(
            mid, "contract", "ui", ok=ok,
            expected=True, observed=ok, note=note,
        ))

    # Challenge issue templates — overturn path is real
    # (legacy ids kept; v5 Trust Loop ids live in measure_overturn_loop)
    for name, mid in (
        ("challenge-a-verdict.yml", "ui.challenge_verdict_template"),
        ("challenge-a-relation.yml", "ui.challenge_relation_template"),
    ):
        p = ISSUE_DIR / name
        ms.append(_m_bool(
            mid, "contract", "overturn",
            ok=p.is_file(),
            expected=str(p.name),
            observed=p.is_file(),
            note="GitHub overturn inlet",
        ))
    return ms


def measure_overturn_loop() -> List[Measurement]:
    """v5 Trust Loop (S0): surfaces that make overturn a product path, not a slogan.

    Measurement ids match docs/roadmap-v5-trust-loop.md §7.2.
    """
    ms: List[Measurement] = []
    contributing = ROOT / "CONTRIBUTING.md"
    contrib_text = (
        contributing.read_text(encoding="utf-8") if contributing.is_file() else ""
    )
    app = WEB_APP.read_text(encoding="utf-8") if WEB_APP.is_file() else ""

    verdict_tpl = ISSUE_DIR / "challenge-a-verdict.yml"
    relation_tpl = ISSUE_DIR / "challenge-a-relation.yml"
    ms.append(_m_bool(
        "overturn.challenge_verdict_template",
        "contract", "overturn",
        ok=verdict_tpl.is_file(),
        expected="challenge-a-verdict.yml",
        observed=verdict_tpl.is_file(),
        note="v5 TL: verdict overturn inlet",
    ))
    ms.append(_m_bool(
        "overturn.challenge_relation_template",
        "contract", "overturn",
        ok=relation_tpl.is_file(),
        expected="challenge-a-relation.yml",
        observed=relation_tpl.is_file(),
        note="v5 TL: edge overturn inlet",
    ))
    ms.append(_m_bool(
        "overturn.contributing_mentions_challenge",
        "contract", "overturn",
        ok=("challenge" in contrib_text.lower()
            and "status_reason" in contrib_text),
        expected="CONTRIBUTING documents challenge + status_reason path",
        observed={
            "exists": contributing.is_file(),
            "has_challenge": "challenge" in contrib_text.lower(),
            "has_status_reason": "status_reason" in contrib_text,
        },
        note="10-minute re-review path",
    ))

    # feed / changes: source of truth is build outputs when dist present;
    # otherwise require the *generators* so the path is real pre-build.
    feed_dist = DIST / "feed.xml"
    changes_dist = DIST / "changes.html"
    feed_src_ok = (ROOT / "universe_explorer" / "dataops" / "feed.py").is_file()
    surface_src_ok = (ROOT / "universe_explorer" / "surface.py").is_file()
    if feed_dist.is_file() and changes_dist.is_file():
        feed_ok, obs = True, "dist/feed.xml + dist/changes.html"
    else:
        feed_ok = feed_src_ok and surface_src_ok
        obs = {
            "dist_feed": feed_dist.is_file(),
            "dist_changes": changes_dist.is_file(),
            "feed_module": feed_src_ok,
            "surface_module": surface_src_ok,
        }
    ms.append(_m_bool(
        "overturn.feed_or_changes_surface",
        "surface", "overturn",
        ok=feed_ok,
        expected="feed + changes publish path",
        observed=obs,
        note="challenge outcomes must be able to surface as restated events",
    ))

    # Canonical tour: axes without confidence % (about + app tour copy)
    tour_ok = (
        "no confidence" in app.lower()
        or "Two axes, no confidence" in app
        or "two axes" in app.lower()
    )
    ms.append(_m_bool(
        "canonical.tour_mentions_axes",
        "contract", "ui",
        ok=tour_ok,
        expected="tour teaches dual axes / denies confidence %",
        observed=tour_ok,
        note="v5 TL-4 / PP-1 entry story",
    ))

    # Public record that at least one challenge closed loop exists (ops, not vanity)
    challenges_dir = ROOT / "docs" / "challenges"
    challenge_records = (
        list(challenges_dir.glob("*.md")) if challenges_dir.is_dir() else []
    )
    # Exclude a pure README placeholder if we add one later
    challenge_records = [
        p for p in challenge_records
        if p.name.lower() not in ("readme.md", "template.md")
    ]
    ms.append(_m_bool(
        "overturn.public_record_exists",
        "inventory", "overturn",
        ok=len(challenge_records) >= 1,
        expected="≥1 docs/challenges/*.md record",
        observed=[p.name for p in challenge_records],
        note="v5 Q1: at least one documented closed loop (accept or reasoned reject)",
    ))
    return ms


def measure_dist_exports(topics: Sequence[Topic]) -> List[Measurement]:
    """If dist/ exists, check public JSON honesty against the live engine."""
    ms: List[Measurement] = []
    claims_path = DIST / "claims.json"
    if not claims_path.is_file():
        ms.append(_m_bool(
            "export.claims_json_skipped",
            "export", "constitution",
            ok=True,
            expected="optional when dist missing",
            observed="skipped",
            note="run build.py to enable export checks",
        ))
        return ms

    data = json.loads(claims_path.read_text(encoding="utf-8"))
    # banned keys walk
    banned_hits: List[str] = []

    def walk(x: Any, path: str = "") -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str) and k.lower() in BANNED_PAYLOAD_KEYS:
                    banned_hits.append(f"{path}.{k}")
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x[:500]):
                walk(v, f"{path}[{i}]")

    walk(data)
    ms.append(_m_bool(
        "export.claims_json_no_banned_keys",
        "export", "constitution",
        ok=len(banned_hits) == 0,
        expected=[],
        observed=banned_hits[:10],
    ))

    # note field should deny confidence numbers
    note = data.get("note") or ""
    ms.append(_m_bool(
        "export.claims_json_note_denies_confidence",
        "export", "constitution",
        ok=("confidence" in note.lower() and "no" in note.lower())
           or "no confidence" in note.lower()
           or "Only recorded" in note,
        expected="note denies confidence / only recorded fields",
        observed=note[:120],
    ))

    by_id = {c.id: c for t in topics for c in t.claims}
    export_claims = data.get("claims") or []
    # dual-axis parity for every exported claim
    mismatch = []
    for row in export_claims:
        cid = row.get("id")
        eng = by_id.get(cid)
        if eng is None:
            mismatch.append(f"unknown:{cid}")
            continue
        if bool(row.get("diverges")) != diverges(eng):
            mismatch.append(f"diverges:{cid}")
        exp_axis = derive(eng).strength.short
        got = (row.get("evidence_axis") or row.get("evidence_axis_name") or "")
        # accept E3 or full name
        if exp_axis not in str(got) and str(got) not in exp_axis:
            # evidence_axis field is often "E3"
            if row.get("evidence_axis") != exp_axis:
                mismatch.append(f"axis:{cid}:{got}!={exp_axis}")
    ms.append(_m_bool(
        "export.dual_axis_parity",
        "export", "dual_axis",
        ok=len(mismatch) == 0,
        expected=0,
        observed=mismatch[:12],
        note="export must restate engine, never reinterpret",
    ))

    # every engine claim appears in export
    export_ids = {r.get("id") for r in export_claims}
    missing = sorted(set(by_id) - export_ids)
    ms.append(_m_bool(
        "export.complete_claim_set",
        "export", "constitution",
        ok=len(missing) == 0,
        expected=[],
        observed=missing[:12],
    ))

    # Automation inventory: every expected build output exists (when dist present)
    try:
        from .reader.automation_metrics import EXPECTED_OUTPUTS
        absent = [n for n, _ in EXPECTED_OUTPUTS if not (DIST / n).is_file()]
    except Exception as e:  # pragma: no cover
        absent = [f"import_error:{e}"]
    ms.append(_m_bool(
        "export.automation_outputs_present",
        "export", "constitution",
        ok=len(absent) == 0,
        expected=[],
        observed=absent[:15],
        note="dist/ must match EXPECTED_OUTPUTS (measure before trusting ship)",
    ))

    auto_path = DIST / "automation-metrics.json"
    if auto_path.is_file():
        auto = json.loads(auto_path.read_text(encoding="utf-8"))
        ms.append(_m_bool(
            "export.automation_metrics_zero_missing",
            "export", "constitution",
            ok=auto.get("missing_outputs") == 0,
            expected=0,
            observed=auto.get("missing_outputs"),
        ))
        auto_hits: List[str] = []
        walk(auto)  # reuse banned-key walker → writes banned_hits; re-walk clean
        # dedicated walk for automation payload
        def walk_auto(x: Any, path: str = "") -> None:
            if isinstance(x, dict):
                for k, v in x.items():
                    if isinstance(k, str) and k.lower() in BANNED_PAYLOAD_KEYS:
                        auto_hits.append(f"{path}.{k}")
                    walk_auto(v, f"{path}.{k}")
            elif isinstance(x, list):
                for i, v in enumerate(x[:200]):
                    walk_auto(v, f"{path}[{i}]")
        walk_auto(auto)
        ms.append(_m_bool(
            "export.automation_metrics_no_banned_keys",
            "export", "constitution",
            ok=len(auto_hits) == 0,
            expected=[],
            observed=auto_hits[:10],
        ))
    else:
        ms.append(_m_bool(
            "export.automation_metrics_present",
            "export", "constitution",
            ok=False,
            expected="automation-metrics.json",
            observed=False,
            note="build.py should emit this",
        ))

    # stats.json claim count parity
    stats_path = DIST / "stats.json"
    if stats_path.is_file():
        stats = json.loads(stats_path.read_text(encoding="utf-8"))
        n_engine = len(by_id)
        n_stats = None
        if isinstance(stats.get("counts"), dict):
            n_stats = stats["counts"].get("claims") or stats["counts"].get("n_claims")
        n_stats = n_stats or stats.get("total_claims") or stats.get("n_claims")
        ms.append(_m(
            "export.stats_claim_count",
            "export", "constitution",
            n_engine, n_stats,
            note="stats.json must recount the registry",
        ))
    return ms


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def measure(
    topics: Optional[Sequence[Topic]] = None,
    *,
    include_dist: bool = True,
) -> dict[str, Any]:
    if topics is None:
        from .data.registry import TOPICS
        topics = TOPICS

    measurements: List[Measurement] = []
    measurements.extend(measure_topics(topics))
    measurements.extend(measure_inventory(topics))
    measurements.extend(measure_stress_hawking(topics))
    measurements.extend(measure_ui_contracts())
    measurements.extend(measure_overturn_loop())
    if include_dist:
        measurements.extend(measure_dist_exports(topics))

    rows = [m.as_dict() for m in measurements]
    n = len(rows)
    n_pass = sum(1 for r in rows if r["ok"])
    n_fail = n - n_pass
    report = {
        "kind": "trust_behavior_measure",
        "n_measurements": n,
        "n_pass": n_pass,
        "n_fail": n_fail,
        "all_ok": n_fail == 0,
        "n_topics": len(topics),
        "n_claims": sum(len(t.claims) for t in topics),
        "note": (
            "Measure first; trust only what the counts show. "
            "n_pass/n_fail are list counts — recount them yourself. "
            "No confidence field exists in this report."
        ),
        "measurements": rows,
    }
    assert not (set(report) & BANNED_REPORT_KEYS)
    return report


def format_report(report: dict[str, Any]) -> str:
    lines = [
        "Trust-behavior measure",
        "=" * 40,
        f"measurements: {report['n_measurements']}",
        f"pass: {report['n_pass']}  fail: {report['n_fail']}",
        f"all_ok: {report['all_ok']}",
        f"topics/claims: {report['n_topics']}/{report['n_claims']}",
        "",
    ]
    fails = [m for m in report["measurements"] if not m["ok"]]
    if fails:
        lines.append(f"FAILURES ({len(fails)}):")
        for m in fails[:40]:
            lines.append(
                f"  ✗ {m['id']}  expected={m['expected']!r} "
                f"observed={m['observed']!r}  ({m['note']})"
            )
        if len(fails) > 40:
            lines.append(f"  … {len(fails) - 40} more")
    else:
        lines.append("All measurements passed.")
    lines.append("")
    lines.append(report["note"])
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    as_json = "--json" in argv
    out_path = None
    if "--out" in argv:
        i = argv.index("--out")
        out_path = Path(argv[i + 1])
    report = measure()
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"wrote {out_path}", file=sys.stderr)
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_report(report))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
