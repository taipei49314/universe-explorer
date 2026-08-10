"""Explore v2 renderer — search + filter + dual-axis + guided reading.

Generates dist/explore-v2.html with all reader features integrated.

Usage:
    python -m universe_explorer.reader.render_explore
"""

from __future__ import annotations

import html as _html
import json
from pathlib import Path
from typing import List

from ..axes import derive, diverges
from ..model import Status, Topic
from .search_index import ClaimSearchIndex
from .filter_engine import ClaimFilter

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def render_explore_v2(topics: List[Topic], dist_dir: Path = _DIST_DIR) -> Path:
    """Generate dist/explore-v2.html."""
    index = ClaimSearchIndex(topics)
    filt = ClaimFilter(topics)

    # Build claims data for the frontend.
    claims = []
    for t in topics:
        for c in t.claims:
            d = derive(c)
            claims.append({
                "id": c.id,
                "topic_id": t.id,
                "title": c.title,
                "status": c.status.name,
                "status_light": c.status.light,
                "evidence_axis": d.strength.short,
                "diverges": diverges(c),
                "evidence_count": len(c.evidence),
                "open_question_count": len(c.open_questions),
                "has_competing": len(c.competing_models) > 0,
                "evidence_types": list({ev.type for ev in c.evidence}),
            })

    claims_json = json.dumps(claims, ensure_ascii=False)
    domains = json.dumps(filt.available_domains())
    statuses = json.dumps(filt.available_statuses())
    axes = json.dumps(filt.available_axes())

    html_content = _EXPLORE_TEMPLATE.format(
        claims_json=claims_json,
        domains=domains,
        statuses=statuses,
        axes=axes,
        total=len(claims),
    )

    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = dist_dir / "explore-v2.html"
    out_path.write_text(html_content, encoding="utf-8")
    print(f"[explore-v2] {len(claims)} claims -> {out_path}")
    return out_path


def _esc(s: str) -> str:
    return _html.escape(str(s), quote=True)


_EXPLORE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Explore — Universe Explorer</title>
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9;
    --muted: #8b949e; --accent: #58a6ff; --pass: #2e7d32; --fail: #c62828;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; }}
  .layout {{ display: flex; height: 100vh; }}
  .sidebar {{ width: 260px; background: var(--card); border-right: 1px solid var(--border);
              padding: 1rem; overflow-y: auto; }}
  .sidebar h2 {{ font-size: 1.1rem; margin-bottom: .75rem; }}
  .filter-group {{ margin-bottom: 1rem; }}
  .filter-group label {{ display: block; font-size: .8rem; color: var(--muted);
                          margin-bottom: .25rem; }}
  .filter-group select, .filter-group input {{
    width: 100%; padding: .35rem; background: var(--bg); color: var(--text);
    border: 1px solid var(--border); border-radius: 4px; font-size: .9rem;
  }}
  .count {{ font-size: .85rem; color: var(--muted); margin-bottom: 1rem; }}
  .main {{ flex: 1; overflow-y: auto; padding: 1.5rem; }}
  .search-bar {{ margin-bottom: 1.5rem; }}
  .search-bar input {{ width: 100%; padding: .6rem; background: var(--card);
                        color: var(--text); border: 1px solid var(--border);
                        border-radius: 6px; font-size: 1rem; }}
  .claim-card {{ background: var(--card); border: 1px solid var(--border);
                 border-radius: 8px; padding: 1rem; margin-bottom: .75rem;
                 cursor: pointer; transition: border-color .15s; }}
  .claim-card:hover {{ border-color: var(--accent); }}
  .claim-card .header {{ display: flex; justify-content: space-between;
                          align-items: flex-start; }}
  .claim-card h3 {{ font-size: .95rem; margin-bottom: .25rem; }}
  .claim-card .meta {{ font-size: .8rem; color: var(--muted); display: flex;
                        gap: 1rem; flex-wrap: wrap; }}
  .badge {{ display: inline-block; padding: .15rem .5rem; border-radius: 3px;
            font-size: .75rem; font-weight: 600; color: #fff; }}
  .badge.E1 {{ background: #2e7d32; }}
  .badge.E2 {{ background: #1565c0; }}
  .badge.E3 {{ background: #f9a825; color: #212121; }}
  .badge.E4 {{ background: #ef6c00; }}
  .badge.E5 {{ background: #c62828; }}
  .diverge-tag {{ background: #f9a82533; color: #f9a825; padding: .1rem .4rem;
                   border-radius: 3px; font-size: .75rem; }}
  .status-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%;
                 margin-right: .25rem; vertical-align: middle; }}
  .detail-panel {{ position: fixed; right: 0; top: 0; width: 400px; height: 100vh;
                    background: var(--card); border-left: 1px solid var(--border);
                    padding: 1.5rem; overflow-y: auto; transform: translateX(100%);
                    transition: transform .2s; z-index: 10; }}
  .detail-panel.open {{ transform: translateX(0); }}
  .detail-panel .close {{ cursor: pointer; color: var(--muted); float: right;
                           font-size: 1.2rem; }}
  .detail-panel h2 {{ font-size: 1.1rem; margin-bottom: .5rem; }}
  .detail-panel .section {{ margin-bottom: 1rem; }}
  .detail-panel .section h4 {{ font-size: .85rem; color: var(--muted);
                                 margin-bottom: .25rem; }}
  nav {{ padding: .75rem 1.5rem; border-bottom: 1px solid var(--border); }}
  nav a {{ color: var(--accent); text-decoration: none; margin-right: 1rem;
           font-size: .85rem; }}
  nav a:hover {{ text-decoration: underline; }}
  .legend {{ display: flex; gap: .75rem; flex-wrap: wrap; margin-bottom: 1rem; }}
  .legend-item {{ display: flex; align-items: center; gap: .3rem; font-size: .75rem;
                   color: var(--muted); }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
</style>
</head>
<body>
<nav>
  <a href="index.html">Index</a>
  <a href="app.html">Map</a>
  <a href="universe.html">Universe</a>
  <a href="epistemic_map.html">Epistemic Map</a>
  <a href="review.html">Review</a>
</nav>
<div class="layout">
  <div class="sidebar">
    <h2>Explore</h2>
    <div class="count" id="count">{total} claims</div>

    <div class="filter-group">
      <label>Domain</label>
      <select id="f-domain"><option value="">All</option></select>
    </div>
    <div class="filter-group">
      <label>Status</label>
      <select id="f-status"><option value="">All</option></select>
    </div>
    <div class="filter-group">
      <label>Evidence Axis</label>
      <select id="f-axis"><option value="">All</option></select>
    </div>
    <div class="filter-group">
      <label>Divergence</label>
      <select id="f-diverge">
        <option value="">All</option>
        <option value="true">Divergent only</option>
        <option value="false">Aligned only</option>
      </select>
    </div>

    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:#2e7d32"></div>🟢 Est.</div>
      <div class="legend-item"><div class="legend-dot" style="background:#1565c0"></div>🔵 Strong</div>
      <div class="legend-item"><div class="legend-dot" style="background:#f9a825"></div>🟡 Comp.</div>
      <div class="legend-item"><div class="legend-dot" style="background:#ef6c00"></div>🟠 Front.</div>
      <div class="legend-item"><div class="legend-dot" style="background:#c62828"></div>🔴 Spec.</div>
    </div>
  </div>

  <div class="main">
    <div class="search-bar">
      <input id="search" placeholder="Search claims... (title, evidence, questions)">
    </div>
    <div id="results"></div>
  </div>
</div>

<div class="detail-panel" id="detail">
  <span class="close" onclick="closeDetail()">&times;</span>
  <div id="detail-content"></div>
</div>

<script>
const CLAIMS = {claims_json};
const DOMAINS = {domains};
const STATUSES = {statuses};
const AXES = {axes};

const STATUS_COLORS = {{
  ESTABLISHED: '#2e7d32', STRONG: '#1565c0', COMPETING: '#f9a825',
  FRONTIER: '#ef6c00', SPECULATIVE: '#c62828'
}};

// Populate filters.
function addOpts(id, vals) {{
  const sel = document.getElementById(id);
  vals.forEach(v => {{ const o = document.createElement('option'); o.value = v; o.textContent = v; sel.appendChild(o); }});
}}
addOpts('f-domain', DOMAINS);
addOpts('f-status', STATUSES);
addOpts('f-axis', AXES);

function getFiltered() {{
  const fd = document.getElementById('f-domain').value;
  const fs = document.getElementById('f-status').value;
  const fa = document.getElementById('f-axis').value;
  const fdiv = document.getElementById('f-diverge').value;
  const q = document.getElementById('search').value.toLowerCase().trim();

  return CLAIMS.filter(c => {{
    if (fd && c.topic_id !== fd) return false;
    if (fs && c.status !== fs) return false;
    if (fa && c.evidence_axis !== fa) return false;
    if (fdiv === 'true' && !c.diverges) return false;
    if (fdiv === 'false' && c.diverges) return false;
    if (q && !c.title.toLowerCase().includes(q) && !c.id.includes(q)) return false;
    return true;
  }});
}}

function render() {{
  const filtered = getFiltered();
  document.getElementById('count').textContent = filtered.length + ' claims';
  const html = filtered.map(c => `
    <div class="claim-card" onclick="showDetail('${{c.id}}')">
      <div class="header">
        <h3>${{c.title}}</h3>
        <span class="badge ${{c.evidence_axis}}">${{c.evidence_axis}}</span>
      </div>
      <div class="meta">
        <span><span class="status-dot" style="background:${{STATUS_COLORS[c.status]}}"></span>${{c.status_light}} ${{c.status}}</span>
        <span>${{c.topic_id}}</span>
        <span>Evidence: ${{c.evidence_count}}</span>
        <span>Open Qs: ${{c.open_question_count}}</span>
        ${{c.diverges ? '<span class="diverge-tag">axes diverge</span>' : ''}}
      </div>
    </div>
  `).join('');
  document.getElementById('results').innerHTML = html || '<div style="color:var(--muted);padding:2rem">No claims match.</div>';
}}

function showDetail(id) {{
  const c = CLAIMS.find(x => x.id === id);
  if (!c) return;
  document.getElementById('detail-content').innerHTML = `
    <h2>${{c.title}}</h2>
    <div class="section">
      <div><strong>${{c.status_light}} ${{c.status}}</strong> · ${{c.evidence_axis}}</div>
      <div style="margin-top:.25rem"><code>${{c.id}}</code></div>
      ${{c.diverges ? '<div style="color:#f9a825;margin-top:.25rem">⚡ Axes diverge</div>' : ''}}
    </div>
    <div class="section">
      <h4>Domain</h4>
      <div>${{c.topic_id}}</div>
    </div>
    <div class="section">
      <h4>Evidence</h4>
      <div>${{c.evidence_count}} item(s)</div>
      <div style="font-size:.85rem;color:var(--muted)">Types: ${{c.evidence_types.join(', ')}}</div>
    </div>
    <div class="section">
      <h4>Open Questions</h4>
      <div>${{c.open_question_count}}</div>
    </div>
    <div class="section">
      <a href="app.html?c=${{c.id}}" style="color:var(--accent)">Open in map</a>
      · <a href="challenge.html" style="color:var(--accent)">Challenge</a>
    </div>
  `;
  document.getElementById('detail').classList.add('open');
}}

function closeDetail() {{
  document.getElementById('detail').classList.remove('open');
}}

// Event listeners.
document.getElementById('f-domain').onchange = render;
document.getElementById('f-status').onchange = render;
document.getElementById('f-axis').onchange = render;
document.getElementById('f-diverge').onchange = render;
document.getElementById('search').oninput = render;

render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    from ..data.registry import TOPICS
    render_explore_v2(TOPICS)
