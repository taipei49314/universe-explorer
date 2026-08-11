"""3D explore/reason scene view-model (presentation only).

Pure functions map constitution-exported claim records into serializable
scene nodes, panel DTOs, reading-path step lists, and neighbor sets.

No confidence / score / probability / trust fields. No WebGL here — the
browser page loads scene3d.json and renders it.

Usage:
    python -m universe_explorer.reader.scene3d          # write dist/scene3d.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from ..data.registry import TOPICS
from ..render import TOPIC_THEMES, THEME_META, app_data_json

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"

# Presentation palette — aligned with CVD-safe status colors used in app.html
STATUS_COLOR = {
    "ESTABLISHED": "#2F7D46",
    "STRONG": "#2762A8",
    "COMPETING": "#A17C0A",
    "FRONTIER": "#C13E2A",
    "SPECULATIVE": "#93265E",
}

THEME_LAYER_Y = {
    "cosmos": 18.0,   # universe shell
    "planets": 0.0,   # mid
    "earth": -18.0,   # world / earth layer
}

BANNED_PAYLOAD_KEYS = frozenset({
    "confidence", "score", "probability", "certainty", "trust",
})


def build_app_data(topics=None) -> dict:
    """Load the same payload the browser uses (live registry → app_data_json)."""
    topics = topics if topics is not None else TOPICS
    return json.loads(app_data_json(topics))


def claims_to_scene_nodes(
    claims: Sequence[dict],
    topics: Sequence[dict],
) -> List[dict]:
    """Map export claim rows to 3D scene nodes with deterministic positions.

    Layout:
      - Y = theme layer (cosmos / planets / earth)
      - X = status_rank * scale + topic index offset
      - Z = axis_rank * scale + hash scatter (deterministic from claim id)
    """
    topic_theme = {t["id"]: t.get("theme") or TOPIC_THEMES.get(t["id"], "cosmos")
                   for t in topics}
    topic_index = {t["id"]: i for i, t in enumerate(topics)}
    # group claims by theme for radial packing within layer
    by_theme: Dict[str, List[dict]] = {k: [] for k in THEME_LAYER_Y}
    for c in claims:
        th = topic_theme.get(c.get("topic"), "cosmos")
        if th not in by_theme:
            th = "cosmos"
        by_theme[th].append(c)

    nodes: List[dict] = []
    for theme, group in by_theme.items():
        y0 = THEME_LAYER_Y.get(theme, 0.0)
        n = max(len(group), 1)
        for i, c in enumerate(group):
            status = c.get("status") or "FRONTIER"
            sr = int(c.get("status_rank") if c.get("status_rank") is not None
                     else 2)
            ar = int(c.get("axis_rank") if c.get("axis_rank") is not None else 2)
            tid = c.get("topic") or ""
            ti = topic_index.get(tid, 0)
            # ring placement within theme layer
            angle = (2.0 * math.pi * i) / n
            radius = 8.0 + 2.5 * ar + 0.4 * ti
            # slight vertical stack by status so lights separate
            y = y0 + (2 - sr) * 1.2
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            # deterministic micro-jitter from claim id (stable, no RNG)
            h = _stable_hash(c.get("id") or "")
            x += ((h % 100) / 100.0 - 0.5) * 0.8
            z += (((h // 100) % 100) / 100.0 - 0.5) * 0.8

            nodes.append({
                "id": c["id"],
                "topic": tid,
                "theme": theme,
                "title": c.get("title") or c["id"],
                "title_zh": c.get("title_zh") or c.get("title") or c["id"],
                "status": status,
                "status_light": c.get("status_light") or "",
                "status_name": c.get("status_name") or status,
                "axis": c.get("axis") or c.get("evidence_axis") or "E5",
                "axis_name": c.get("axis_name") or "",
                "diverges": bool(c.get("diverges")),
                "open_questions": list(c.get("open_questions") or []),
                "n_open_questions": len(c.get("open_questions") or []),
                "n_related": int(c.get("n_related") or 0),
                "permalink": c.get("permalink") or "",
                "color": STATUS_COLOR.get(status, "#888888"),
                "position": {
                    "x": round(x, 4),
                    "y": round(y, 4),
                    "z": round(z, 4),
                },
            })
    return nodes


def panel_from_claim(claim: dict) -> dict:
    """Detail panel DTO for explore/reason — no synthetic scores."""
    oq = list(claim.get("open_questions") or [])
    return {
        "id": claim.get("id"),
        "topic": claim.get("topic"),
        "title": claim.get("title"),
        "title_zh": claim.get("title_zh") or claim.get("title"),
        "what": claim.get("title"),  # the claim statement
        "status": claim.get("status"),
        "status_light": claim.get("status_light"),
        "status_name": claim.get("status_name"),
        "axis": claim.get("axis") or claim.get("evidence_axis"),
        "axis_name": claim.get("axis_name"),
        "diverges": bool(claim.get("diverges")),
        "open_questions": oq,
        "open_questions_empty": len(oq) == 0,
        "status_reason": claim.get("status_reason") or [],
        "related": claim.get("related") or [],
        "permalink": claim.get("permalink") or "",
    }


def path_step_ids(reading_paths: Sequence[dict], path_id: str) -> List[str]:
    """Ordered claim ids for a registered reading path."""
    for p in reading_paths:
        if p.get("id") == path_id:
            steps = p.get("steps") or []
            return [str(s) for s in steps]
    return []


def path_catalog(reading_paths: Sequence[dict]) -> List[dict]:
    """Lightweight path list for UI selectors."""
    out = []
    for p in reading_paths:
        out.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "title_zh": p.get("title_zh") or p.get("title"),
            "domain": p.get("domain"),
            "n_steps": p.get("n_steps") or len(p.get("steps") or []),
        })
    return out


def neighbor_ids(claim: dict) -> List[str]:
    """Authored/related neighbor claim ids from export related list."""
    related = claim.get("related") or []
    ids = []
    for r in related:
        if isinstance(r, dict) and r.get("id"):
            ids.append(str(r["id"]))
        elif isinstance(r, str):
            ids.append(r)
    return ids


def neighbor_ids_from_links(links: Sequence[dict], claim_id: str) -> List[str]:
    """Neighbors from relations.links when claim row is not pre-attached."""
    out: List[str] = []
    seen = set()
    for L in links:
        a, b = L.get("source") or L.get("from"), L.get("target") or L.get("to")
        # relations payload may use different keys
        if not a:
            a = L.get("a") or L.get("src")
        if not b:
            b = L.get("b") or L.get("dst")
        # app-data links shape: check common forms
        if a is None and "source_id" in L:
            a, b = L.get("source_id"), L.get("target_id")
        if a == claim_id and b and b not in seen:
            seen.add(b)
            out.append(str(b))
        elif b == claim_id and a and a not in seen:
            seen.add(a)
            out.append(str(a))
    return out


def build_scene_payload(app_data: Optional[dict] = None) -> dict:
    """Full scene3d.json payload from live (or provided) app-data."""
    data = app_data if app_data is not None else build_app_data()
    claims = data.get("claims") or []
    topics = data.get("topics") or []
    themes = data.get("themes") or [
        {"id": k, "title": v["title"], "title_zh": v["title_zh"]}
        for k, v in THEME_META.items()
    ]
    rel = data.get("relations") or {}
    reading_paths = rel.get("reading_paths") or []
    links = rel.get("links") or []

    nodes = claims_to_scene_nodes(claims, topics)
    by_id = {c["id"]: c for c in claims}

    # Attach neighbor lists on nodes for client navigation
    for node in nodes:
        c = by_id.get(node["id"], {})
        nids = neighbor_ids(c)
        if not nids and links:
            nids = neighbor_ids_from_links(links, node["id"])
        node["neighbors"] = nids

    edges = []
    for L in links:
        # normalize link endpoints from relations_payload shape
        a = L.get("source") or L.get("from") or L.get("a") or L.get("src")
        b = L.get("target") or L.get("to") or L.get("b") or L.get("dst")
        if a is None and "source_id" in L:
            a, b = L.get("source_id"), L.get("target_id")
        # relations_payload uses source/target as claim ids in "links" list items
        if a is None:
            # try authored form: source_id in nested
            a = L.get("source_claim") or L.get("s")
            b = L.get("target_claim") or L.get("t")
        if not a or not b:
            # last resort: common UE shape from relations_payload
            a = L.get("source")
            b = L.get("target")
        if a and b and a in by_id and b in by_id:
            edges.append({
                "source": a,
                "target": b,
                "kind": L.get("kind") or L.get("type") or "related",
                "origin": L.get("origin") or "authored",
            })

    # If link keys failed, build edges from related lists
    if not edges:
        for c in claims:
            for nid in neighbor_ids(c):
                if nid in by_id:
                    edges.append({
                        "source": c["id"],
                        "target": nid,
                        "kind": "related",
                        "origin": "authored",
                    })

    payload = {
        "note": (
            "Universe Explorer 3D scene. Explore/reason over registered claims "
            "only. No confidence, score, probability, certainty, or trust fields. "
            "cosmos = universe shell; earth = world/polar/ocean layer; "
            "planets = solar/exoplanet layer."
        ),
        "themes": themes,
        "topics": [
            {
                "id": t["id"],
                "title": t.get("title"),
                "title_zh": t.get("title_zh"),
                "theme": t.get("theme"),
                "n_claims": t.get("n_claims"),
            }
            for t in topics
        ],
        "nodes": nodes,
        "edges": edges,
        "paths": path_catalog(reading_paths),
        "path_steps": {
            p["id"]: path_step_ids(reading_paths, p["id"])
            for p in reading_paths
            if p.get("id")
        },
        "panels": {c["id"]: panel_from_claim(c) for c in claims},
        "n_nodes": len(nodes),
        "n_edges": len(edges),
        "n_paths": len(reading_paths),
    }
    _assert_no_banned(payload)
    return payload


def write_scene3d(dist_dir: Path = _DIST_DIR, topics=None) -> Path:
    """Write dist/scene3d.json from live registry."""
    dist_dir = Path(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    data = build_app_data(topics)
    payload = build_scene_payload(data)
    out = dist_dir / "scene3d.json"
    out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[scene3d] {payload['n_nodes']} nodes, {payload['n_edges']} edges, "
          f"{payload['n_paths']} paths -> {out}")
    return out


def _stable_hash(s: str) -> int:
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h


def _assert_no_banned(obj: Any, path: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in BANNED_PAYLOAD_KEYS:
                raise ValueError(f"banned key {k!r} at {path}")
            _assert_no_banned(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:2000]):
            _assert_no_banned(v, f"{path}[{i}]")


if __name__ == "__main__":
    write_scene3d()
