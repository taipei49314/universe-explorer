"""Three product canonicals (v5 Trust Loop TL-4 / S3).

These are the stories the about page and tour teach. Not a ranking of
science — fixed teaching anchors. Measure before trusting the surface.

No confidence fields.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

# (canonical_id, claim_id, path_id, kind, en_title, zh_title)
# kind: dual_axis | competing | frontier_debate
CANONICALS: Tuple[Dict[str, str], ...] = (
    {
        "id": "c_hawking_dual_axis",
        "claim_id": "hawking_radiation",
        "path_id": "path_black_hole",
        "kind": "dual_axis",
        "title_en": "Hawking radiation — Strong light, thin direct evidence",
        "title_zh": "霍金輻射 —— 強共識燈 × 非直接證據",
        "map_href": "app.html?c=hawking_radiation",
        "path_href": "app.html?path=path_black_hole",
        "walkthrough": "docs/hawking-walkthrough.md",
        "challenge_record": "docs/challenges/2026-08-10-hawking-strong-re-review.md",
    },
    {
        "id": "c_h0_competing",
        "claim_id": "H0_tension_local_vs_cmb",
        "path_id": "path_h0",
        "kind": "competing",
        "title_en": "H0 tension — Competing poles, no winner path",
        "title_zh": "H0 張力 —— 競爭兩極，路徑沒有勝負",
        "map_href": "app.html?c=H0_tension_local_vs_cmb",
        "path_href": "app.html?path=path_h0",
        "walkthrough": "docs/paper/h0-discussion.md",
        "challenge_record": "",
    },
    {
        "id": "c_earth_prediction",
        "claim_id": "short_term_deterministic_prediction",
        "path_id": "path_seismology",
        "kind": "competing",
        "title_en": "Earthquake prediction debate — Competing vs forecasting",
        "title_zh": "地震預測辯論 —— 確定性預測 vs 預報",
        "map_href": "app.html?c=short_term_deterministic_prediction",
        "path_href": "app.html?path=path_seismology",
        "walkthrough": "docs/paper/seismology-discussion.md",
        "challenge_record": "",
    },
)

BANNED = frozenset({"confidence", "score", "probability", "certainty", "trust"})


def canonical_list() -> List[Dict[str, str]]:
    return [dict(c) for c in CANONICALS]


def canonical_claim_ids() -> Tuple[str, ...]:
    return tuple(c["claim_id"] for c in CANONICALS)


def canonical_path_ids() -> Tuple[str, ...]:
    return tuple(c["path_id"] for c in CANONICALS)


def as_payload() -> Dict[str, Any]:
    d = {
        "kind": "product_canonicals",
        "n": len(CANONICALS),
        "canonicals": canonical_list(),
        "note": (
            "Three teaching anchors only — not a ranking of truth. "
            "Recount the list yourself. No confidence field."
        ),
    }
    assert not (set(d) & BANNED)
    return d
