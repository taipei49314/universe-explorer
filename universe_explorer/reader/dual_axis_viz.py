"""Dual-axis visualization — consensus × evidence scatter plot.

Generates an SVG chart showing every claim's position on two axes:
  X = Consensus (Established → Speculative)
  Y = Evidence (E1 multiple direct → E5 none)

Divergent claims (where axes point apart) are highlighted.

Usage:
    python -m universe_explorer.reader.dual_axis_viz
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from ..axes import derive, diverges
from ..model import Status, Topic

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def generate_dual_axis_svg(topics: List[Topic]) -> str:
    """Generate SVG scatter plot of consensus × evidence."""
    points = []
    for topic in topics:
        for claim in topic.claims:
            d = derive(claim)
            points.append({
                "id": claim.id,
                "title": claim.title,
                "domain": topic.id,
                "x": claim.status.rank,         # 0=Established, 4=Speculative
                "y": _axis_rank(d.strength.short),  # 0=E1, 4=E5
                "diverges": diverges(claim),
                "status": claim.status.name,
                "axis": d.strength.short,
            })

    return _render_svg(points)


def _axis_rank(axis_short: str) -> int:
    """E1→0, E2→1, E3→2, E4→3, E5→4."""
    return {"E1": 0, "E2": 1, "E3": 2, "E4": 3, "E5": 4}.get(axis_short, 2)


def _render_svg(points: list) -> str:
    """Render points as an SVG scatter plot."""
    W, H = 600, 400
    PAD = 60
    PW = W - PAD * 2
    PH = H - PAD * 2

    status_colors = {
        "ESTABLISHED": "#2e7d32", "STRONG": "#1565c0",
        "COMPETING": "#f9a825", "FRONTIER": "#ef6c00", "SPECULATIVE": "#c62828",
    }
    status_labels = ["Established", "Strong", "Competing", "Frontier", "Speculative"]
    axis_labels = ["E1", "E2", "E3", "E4", "E5"]

    circles = []
    for p in points:
        cx = PAD + (p["x"] / 4) * PW
        cy = PAD + (p["y"] / 4) * PH
        color = status_colors.get(p["status"], "#888")
        r = 6
        stroke = ' stroke="#f9a825" stroke-width="2"' if p["diverges"] else ""
        circles.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" '
            f'fill="{color}"{stroke} opacity="0.8">'
            f'<title>{_esc(p["id"])}: {_esc(p["title"])}\n'
            f'{p["status"]} × {p["axis"]}'
            f'{" (diverges)" if p["diverges"] else ""}</title>'
            f'</circle>'
        )

    # Axes.
    x_labels_svg = []
    for i, label in enumerate(status_labels):
        x = PAD + (i / 4) * PW
        x_labels_svg.append(
            f'<text x="{x:.1f}" y="{H - 10}" text-anchor="middle" '
            f'font-size="10" fill="#c9d1d9">{label}</text>'
        )

    y_labels_svg = []
    for i, label in enumerate(axis_labels):
        y = PAD + (i / 4) * PH
        y_labels_svg.append(
            f'<text x="{PAD - 10}" y="{y:.1f}" text-anchor="end" '
            f'dominant-baseline="middle" font-size="10" fill="#c9d1d9">'
            f'{label}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"
     style="background:#0d1117;max-width:100%">
  <text x="{W/2}" y="20" text-anchor="middle" font-size="14" fill="#c9d1d9">
    Consensus × Evidence (divergent claims highlighted)
  </text>
  <line x1="{PAD}" y1="{PAD}" x2="{PAD}" y2="{H-PAD}" stroke="#30363d" stroke-width="1"/>
  <line x1="{PAD}" y1="{H-PAD}" x2="{W-PAD}" y2="{H-PAD}" stroke="#30363d" stroke-width="1"/>
  {"".join(x_labels_svg)}
  {"".join(y_labels_svg)}
  {"".join(circles)}
</svg>'''


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


if __name__ == "__main__":
    from ..data.registry import TOPICS
    svg = generate_dual_axis_svg(TOPICS)
    out = _DIST_DIR / "dual-axis.svg"
    _DIST_DIR.mkdir(exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"[dual-axis] SVG -> {out}")
