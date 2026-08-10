"""Review dashboard — generate a static HTML page for candidate review.

The dashboard shows every structured candidate with its precheck report.
Humans review, then accept (edit data/*.py) or reject.

Usage:
    python -m universe_explorer.discovery.review
    python -m universe_explorer.discovery.review --list
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import List, Optional

from .candidate_builder import CANDIDATES_DIR, list_candidates
from .precheck import PrecheckReport, precheck

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def generate_review_dashboard(
    candidates_dir: Path = CANDIDATES_DIR,
    dist_dir: Path = _DIST_DIR,
) -> Path:
    """Generate dist/review.html from all structured candidates."""
    candidates = list_candidates()
    cards = []
    pass_count = 0
    fail_count = 0

    for c in candidates:
        report = precheck(c)
        if report.pass_constitution:
            pass_count += 1
        else:
            fail_count += 1
        cards.append(_render_candidate_card(c, report))

    html_content = _REVIEW_TEMPLATE.format(
        total=len(candidates),
        pass_count=pass_count,
        fail_count=fail_count,
        cards="\n".join(cards),
    )

    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = dist_dir / "review.html"
    out_path.write_text(html_content, encoding="utf-8")
    print(f"[review] {len(candidates)} candidates ({pass_count} pass, "
          f"{fail_count} fail) -> {out_path}")
    return out_path


def list_pending() -> List[dict]:
    """List candidates that haven't been accepted/rejected yet."""
    return [c for c in list_candidates()
            if c.get("status") is None]


def _render_candidate_card(candidate: dict, report: PrecheckReport) -> str:
    """Render one candidate as an HTML card."""
    cid = _esc(candidate.get("id", "unknown"))
    topic = _esc(candidate.get("topic_id", "unknown"))
    title = _esc(candidate.get("title", "[untitled]"))
    status_class = "pass" if report.pass_constitution else "fail"

    # Evidence items.
    evidence_html = ""
    for ev in candidate.get("evidence", []):
        evidence_html += (
            f'<div class="evidence-item">'
            f'<span class="ev-type">{_esc(ev.get("type", ""))}</span> '
            f'<span class="ev-source">{_esc(ev.get("source_ref", ""))}</span>'
            f'<p>{_esc(ev.get("description", "")[:300])}</p>'
            f'</div>'
        )

    # Violations.
    violations_html = ""
    for v in report.violations:
        violations_html += (
            f'<div class="violation">'
            f'<code>{_esc(v.rule)}</code>: {_esc(v.detail[:200])}'
            f'</div>'
        )

    # Warnings.
    warnings_html = ""
    for w in report.warnings:
        warnings_html += f'<div class="warning">{_esc(w)}</div>'

    # Compatible statuses.
    compat = ", ".join(sorted(report.compatible_statuses)) or "—"
    excluded = ", ".join(sorted(report.excluded_statuses)) or "—"

    return _CARD_TEMPLATE.format(
        cid=cid,
        topic=topic,
        title=title,
        status_class=status_class,
        constitution="PASS" if report.pass_constitution else "FAIL",
        evidence_axis=_esc(report.evidence_axis or "—"),
        diverge="YES" if report.diverges else "no",
        compat=_esc(compat),
        excluded=_esc(excluded),
        evidence_html=evidence_html,
        violations_html=violations_html,
        warnings_html=warnings_html,
        source_count=len(candidate.get("sources", [])),
        evidence_count=len(candidate.get("evidence", [])),
    )


def _esc(text: str) -> str:
    return html.escape(str(text), quote=True)


# ── Templates ──────────────────────────────────────────────────────────────

_CARD_TEMPLATE = """
<div class="candidate-card {status_class}" id="c-{cid}">
  <div class="card-header">
    <div>
      <h3>{title}</h3>
      <code>{cid}</code> · <span class="topic">{topic}</span>
    </div>
    <span class="badge {status_class}">{constitution}</span>
  </div>
  <div class="card-body">
    <div class="meta-row">
      <span>Sources: {source_count}</span>
      <span>Evidence: {evidence_count}</span>
      <span>Axis: {evidence_axis}</span>
      <span>Diverge: {diverge}</span>
    </div>
    <div class="status-row">
      <span>Compatible: {compat}</span>
      <span>Excluded: {excluded}</span>
    </div>
    <details>
      <summary>Evidence items</summary>
      {evidence_html}
    </details>
    {violations_html}
    {warnings_html}
  </div>
</div>
"""

_REVIEW_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Discovery Review — Universe Explorer</title>
<style>
  :root {{
    --pass: #2e7d32; --fail: #c62828; --warn: #f9a825;
    --bg: #fafafa; --card: #fff; --border: #e0e0e0;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: system-ui, sans-serif; background: var(--bg);
         color: #212121; padding: 2rem; max-width: 960px; margin: 0 auto; }}
  h1 {{ margin-bottom: .5rem; }}
  .summary {{ margin-bottom: 1.5rem; color: #616161; }}
  .summary .pass {{ color: var(--pass); font-weight: 600; }}
  .summary .fail {{ color: var(--fail); font-weight: 600; }}
  .candidate-card {{ background: var(--card); border: 1px solid var(--border);
                     border-radius: 8px; margin-bottom: 1rem; overflow: hidden; }}
  .candidate-card.pass {{ border-left: 4px solid var(--pass); }}
  .candidate-card.fail {{ border-left: 4px solid var(--fail); }}
  .card-header {{ display: flex; justify-content: space-between; align-items: center;
                  padding: 1rem; border-bottom: 1px solid var(--border); }}
  .card-header h3 {{ font-size: 1rem; }}
  .card-header code {{ font-size: .85rem; color: #757575; }}
  .topic {{ color: #1565c0; font-size: .85rem; }}
  .badge {{ padding: .25rem .75rem; border-radius: 4px; font-weight: 600;
            font-size: .85rem; color: #fff; }}
  .badge.pass {{ background: var(--pass); }}
  .badge.fail {{ background: var(--fail); }}
  .card-body {{ padding: 1rem; }}
  .meta-row, .status-row {{ display: flex; gap: 1.5rem; margin-bottom: .75rem;
                             font-size: .9rem; color: #424242; }}
  .evidence-item {{ padding: .5rem 0; border-bottom: 1px solid #f5f5f5;
                    font-size: .85rem; }}
  .ev-type {{ background: #e3f2fd; padding: .1rem .4rem; border-radius: 3px;
              font-size: .8rem; }}
  .ev-source {{ color: #757575; font-size: .8rem; }}
  .violation {{ background: #ffebee; padding: .5rem; border-radius: 4px;
                margin: .25rem 0; font-size: .85rem; }}
  .violation code {{ color: var(--fail); }}
  .warning {{ background: #fff8e1; padding: .5rem; border-radius: 4px;
              margin: .25rem 0; font-size: .85rem; }}
  details {{ margin: .5rem 0; }}
  summary {{ cursor: pointer; font-weight: 500; }}
  .empty {{ text-align: center; color: #9e9e9e; padding: 3rem; }}
  nav {{ margin-bottom: 1.5rem; }}
  nav a {{ margin-right: 1rem; color: #1565c0; text-decoration: none; }}
  nav a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<nav>
  <a href="index.html">Index</a>
  <a href="app.html">Map</a>
  <a href="universe.html">Universe</a>
  <a href="explore.html">Explore</a>
</nav>
<h1>Discovery Review</h1>
<p class="summary">
  {total} candidate(s): <span class="pass">{pass_count} pass</span> ·
  <span class="fail">{fail_count} fail</span>
</p>
{cards}
</body>
</html>
"""


if __name__ == "__main__":
    import sys
    if "--list" in sys.argv:
        for c in list_pending():
            print(f"  {c['id']} ({c.get('topic_id', '?')})")
        if not list_pending():
            print("  (none)")
    else:
        generate_review_dashboard()
