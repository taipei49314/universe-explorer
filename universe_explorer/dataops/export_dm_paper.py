"""Export paper-facing tables + Fig.1 for the dark_matter domain.

Stdlib only (no matplotlib). Writes:

  docs/paper/dark-matter-open-questions.md
  docs/paper/dark-matter-sources.md
  docs/paper/dark-matter-claims-summary.md
  docs/paper/fig1-light-vs-evidence.svg

Usage:
  python -m universe_explorer.dataops.export_dm_paper
"""

from __future__ import annotations

import html
from pathlib import Path

from ..axes import derive, diverges
from ..data.dark_matter import DARK_MATTER

OUT = Path(__file__).resolve().parents[2] / "docs" / "paper"

STATUS_ORDER = [
    "Established Consensus",
    "Strong Consensus",
    "Competing Models",
    "Frontier Research",
    "Speculative",
]

E_ORDER = ["E1", "E2", "E3", "E4", "E5"]

LIGHT_COLOR = {
    "🟢": "#1a7f37",
    "🔵": "#0969da",
    "🟡": "#9a6700",
    "🟠": "#bc4c00",
    "🔴": "#cf222e",
}


def _rows():
    rows = []
    for c in DARK_MATTER.claims:
        d = derive(c)
        rows.append({
            "id": c.id,
            "title": c.title,
            "light": c.status.light,
            "status": c.status.value,
            "status_rank": c.status.rank,
            "E": d.strength.short,
            "E_label": d.strength.value,
            "n_src": len(c.sources),
            "n_ev": len(c.evidence),
            "n_oq": len(c.open_questions),
            "diverges": diverges(c),
            "claim": c,
            "derivation": d,
        })
    return rows


def write_claims_summary(rows) -> Path:
    path = OUT / "dark-matter-claims-summary.md"
    lines = [
        "# Dark matter — claims summary (auto-exported)",
        "",
        f"Topic: **{DARK_MATTER.title}** · {len(rows)} claims · "
        "source: `universe_explorer/data/dark_matter.py`",
        "",
        "Map rules: `docs/dark-matter-paper-map.md` · "
        "Fig.1: `docs/paper/fig1-light-vs-evidence.svg`",
        "",
        "| # | Light | Claim id | E | Sources | Diverges? |",
        "|--:|:-----:|----------|:-:|--------:|:---------:|",
    ]
    for i, r in enumerate(rows, 1):
        div = "yes" if r["diverges"] else ""
        lines.append(
            f"| {i} | {r['light']} | `{r['id']}` | {r['E']} | "
            f"{r['n_src']} | {div} |"
        )
    lines += [
        "",
        "## Titles",
        "",
    ]
    for r in rows:
        lines.append(f"- {r['light']} **`{r['id']}`** — {r['title']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_open_questions(rows) -> Path:
    path = OUT / "dark-matter-open-questions.md"
    lines = [
        "# Dark matter — open questions table (auto-exported)",
        "",
        "For Methods / Discussion tables. Questions are **authored** on each "
        "claim; this file only aggregates them. Count them yourself — no "
        "confidence percentages.",
        "",
        "| Claim id | Light | E | Open question |",
        "|----------|:-----:|:-:|---------------|",
    ]
    for r in rows:
        for oq in r["claim"].open_questions:
            q = oq.replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| `{r['id']}` | {r['light']} | {r['E']} | {q} |"
            )
    lines += [
        "",
        f"_Total open-question rows: "
        f"{sum(r['n_oq'] for r in rows)} across {len(rows)} claims._",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_sources(rows) -> Path:
    path = OUT / "dark-matter-sources.md"
    lines = [
        "# Dark matter — sources table (auto-exported)",
        "",
        "Every row hangs on a claim. arXiv/DOI rows are cite⇒fetch verified "
        "by the provenance court when present in cache.",
        "",
        "| Claim id | Light | Source label | url_or_id | kind |",
        "|----------|:-----:|--------------|-----------|------|",
    ]
    seen = set()
    n = 0
    for r in rows:
        for s in r["claim"].sources:
            kind = s.kind.replace("|", "\\|")
            lines.append(
                f"| `{r['id']}` | {r['light']} | `{s.label}` | "
                f"`{s.url_or_id}` | {kind} |"
            )
            seen.add(s.url_or_id)
            n += 1
    lines += [
        "",
        f"_Citation instances: {n} · unique url_or_id: {len(seen)}._",
        "",
        "## Unique identifiers",
        "",
    ]
    for u in sorted(seen):
        lines.append(f"- `{u}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_fig1_svg(rows) -> Path:
    """Consensus rank (y) vs evidence grade (x) — paper Fig.1."""
    path = OUT / "fig1-light-vs-evidence.svg"
    W, H = 920, 640
    ml, mr, mt, mb = 110, 40, 50, 90
    plot_w = W - ml - mr
    plot_h = H - mt - mb

    def x_of(e: str) -> float:
        i = E_ORDER.index(e)
        return ml + (i + 0.5) / len(E_ORDER) * plot_w

    def y_of(rank: int) -> float:
        # rank 0 Established at bottom (bedrock), 4 Speculative at top
        return mt + plot_h - (rank + 0.5) / 5 * plot_h

    # jitter stacks for overlapping cells
    cell_counts: dict[tuple[str, int], int] = {}
    cell_index: dict[str, int] = {}
    for r in rows:
        key = (r["E"], r["status_rank"])
        cell_index[r["id"]] = cell_counts.get(key, 0)
        cell_counts[key] = cell_counts.get(key, 0) + 1

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="460" y="28" text-anchor="middle" font-family="Segoe UI,'
        ' Helvetica, Arial, sans-serif" font-size="16" font-weight="600" '
        'fill="#1f2328">Fig. 1 — Dark matter claims: consensus light vs '
        "evidence axis</text>",
        f'<rect x="{ml}" y="{mt}" width="{plot_w}" height="{plot_h}" '
        'fill="#f6f8fa" stroke="#d0d7de"/>',
    ]

    # grid + axis labels
    for i, e in enumerate(E_ORDER):
        x = ml + (i + 0.5) / len(E_ORDER) * plot_w
        parts.append(
            f'<line x1="{x}" y1="{mt}" x2="{x}" y2="{mt + plot_h}" '
            'stroke="#eaeef2"/>'
        )
        parts.append(
            f'<text x="{x}" y="{mt + plot_h + 28}" text-anchor="middle" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif" '
            f'font-size="13" fill="#1f2328">{e}</text>'
        )
    for rank, name in enumerate(STATUS_ORDER):
        y = y_of(rank)
        parts.append(
            f'<line x1="{ml}" y1="{y}" x2="{ml + plot_w}" y2="{y}" '
            'stroke="#eaeef2"/>'
        )
        short = name.replace(" Consensus", "").replace(" Research", "").replace(
            " Models", "")
        parts.append(
            f'<text x="{ml - 12}" y="{y + 4}" text-anchor="end" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif" '
            f'font-size="12" fill="#1f2328">{html.escape(short)}</text>'
        )

    parts.append(
        f'<text x="{ml + plot_w / 2}" y="{H - 28}" text-anchor="middle" '
        'font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" '
        'fill="#656d76">Evidence axis (derived, never declared) →</text>'
    )
    parts.append(
        f'<text x="24" y="{mt + plot_h / 2}" text-anchor="middle" '
        'font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" '
        'fill="#656d76" transform="rotate(-90 24 '
        f'{mt + plot_h / 2})">← Consensus light (human + status_reason)</text>'
    )

    # points
    for r in rows:
        key = (r["E"], r["status_rank"])
        n = cell_counts[key]
        k = cell_index[r["id"]]
        dx = (k - (n - 1) / 2) * 14
        x = x_of(r["E"]) + dx
        y = y_of(r["status_rank"])
        color = LIGHT_COLOR.get(r["light"], "#57606a")
        title = html.escape(f"{r['id']}: {r['title']}")
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{color}" '
            f'stroke="#ffffff" stroke-width="1.5">'
            f"<title>{title}</title></circle>"
        )
        # short id label under point for print
        label = r["id"]
        if len(label) > 18:
            label = label[:16] + "…"
        parts.append(
            f'<text x="{x:.1f}" y="{y + 18:.1f}" text-anchor="middle" '
            f'font-family="Consolas, Menlo, monospace" font-size="8" '
            f'fill="#57606a">{html.escape(label)}</text>'
        )

    # legend note
    parts.append(
        f'<text x="{ml}" y="{H - 12}" font-family="Segoe UI, Helvetica, '
        'Arial, sans-serif" font-size="11" fill="#656d76">'
        "Bedrock (Established) at bottom · ceiling (Speculative) at top · "
        "divergence = high consensus + weak evidence (e.g. ΛCDM on E3)"
        "</text>"
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = _rows()
    paths = [
        write_claims_summary(rows),
        write_open_questions(rows),
        write_sources(rows),
        write_fig1_svg(rows),
    ]
    print(f"Exported {len(rows)} claims:")
    for p in paths:
        print(f"  -> {p}")


if __name__ == "__main__":
    main()
