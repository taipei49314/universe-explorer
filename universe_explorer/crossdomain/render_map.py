"""Epistemic map renderer — generate interactive cross-domain knowledge map.

Generates dist/epistemic_map.html with:
  - Force-directed graph (vanilla JS + Canvas)
  - Nodes colored by status light, sized by evidence count
  - Edges styled by kind (solid=supports, dashed=tensions, red=conflict)
  - Domain clusters
  - Click to expand claim details
  - Filter by domain, status, evidence axis

Usage:
    python -m universe_explorer.crossdomain.render_map
"""

from __future__ import annotations

import html as _html
import json
from pathlib import Path

from .graph_builder import DomainGraph, build_cross_domain_graph

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def render_epistemic_map(
    graph: DomainGraph,
    dist_dir: Path = _DIST_DIR,
) -> Path:
    """Generate dist/epistemic_map.html."""
    graph_json = json.dumps(graph.to_dict(), ensure_ascii=False)
    stats = graph.to_dict()["stats"]

    html_content = _MAP_TEMPLATE.format(
        graph_json=graph_json,
        node_count=stats["node_count"],
        edge_count=stats["edge_count"],
        cross_domain_edges=stats["cross_domain_edges"],
        domain_count=stats["domain_count"],
    )

    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = dist_dir / "epistemic_map.html"
    out_path.write_text(html_content, encoding="utf-8")
    print(f"[map] {stats['node_count']} nodes, {stats['edge_count']} edges "
          f"({stats['cross_domain_edges']} cross-domain) -> {out_path}")
    return out_path


_MAP_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Epistemic Map — Universe Explorer</title>
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9;
    --muted: #8b949e; --accent: #58a6ff;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; }}
  .layout {{ display: flex; height: 100vh; }}
  .sidebar {{ width: 280px; background: var(--card); border-right: 1px solid var(--border);
              padding: 1rem; overflow-y: auto; }}
  .sidebar h2 {{ font-size: 1.1rem; margin-bottom: .75rem; }}
  .stat {{ font-size: .85rem; color: var(--muted); margin-bottom: .25rem; }}
  .filter-group {{ margin-bottom: 1rem; }}
  .filter-group label {{ display: block; font-size: .8rem; color: var(--muted);
                          margin-bottom: .25rem; }}
  .filter-group select {{ width: 100%; padding: .3rem; background: var(--bg);
                          color: var(--text); border: 1px solid var(--border); border-radius: 4px; }}
  .legend {{ margin-top: 1rem; }}
  .legend-item {{ display: flex; align-items: center; gap: .5rem; font-size: .8rem;
                  margin-bottom: .25rem; }}
  .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
  canvas {{ flex: 1; display: block; }}
  .tooltip {{ position: fixed; background: var(--card); border: 1px solid var(--border);
              border-radius: 6px; padding: .75rem; font-size: .85rem; max-width: 320px;
              pointer-events: none; z-index: 10; display: none; }}
  .tooltip h4 {{ margin-bottom: .25rem; }}
  .tooltip .meta {{ color: var(--muted); font-size: .8rem; }}
  nav {{ position: fixed; top: .5rem; left: .5rem; z-index: 20; }}
  nav a {{ color: var(--accent); text-decoration: none; margin-right: 1rem;
           font-size: .85rem; }}
  nav a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<nav>
  <a href="index.html">Index</a>
  <a href="app.html">Map</a>
  <a href="universe.html">Universe</a>
  <a href="explore.html">Explore</a>
  <a href="review.html">Review</a>
</nav>
<div class="layout">
  <div class="sidebar">
    <h2>Epistemic Map</h2>
    <div class="stat">Nodes: {node_count}</div>
    <div class="stat">Edges: {edge_count}</div>
    <div class="stat">Cross-domain: {cross_domain_edges}</div>
    <div class="stat">Domains: {domain_count}</div>
    <p class="stat" style="margin:.75rem 0;line-height:1.35;color:var(--muted)">
      <strong>Disclaimer:</strong> many edges are <em>shared citation</em> only —
      they do <em>not</em> mean the claims agree. Authored supports/tensions are
      distinct from mechanical co-citation (amendment-10 / C7).
    </p>

    <div class="filter-group">
      <label>Domain</label>
      <select id="filter-domain"><option value="">All</option></select>
    </div>
    <div class="filter-group">
      <label>Status</label>
      <select id="filter-status"><option value="">All</option></select>
    </div>
    <div class="filter-group">
      <label>Evidence Axis</label>
      <select id="filter-axis"><option value="">All</option></select>
    </div>

    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:#2e7d32"></div>Established</div>
      <div class="legend-item"><div class="legend-dot" style="background:#1565c0"></div>Strong</div>
      <div class="legend-item"><div class="legend-dot" style="background:#f9a825"></div>Competing</div>
      <div class="legend-item"><div class="legend-dot" style="background:#ef6c00"></div>Frontier</div>
      <div class="legend-item"><div class="legend-dot" style="background:#c62828"></div>Speculative</div>
    </div>
  </div>
  <canvas id="graph"></canvas>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
const DATA = {graph_json};
const STATUS_COLORS = {{
  ESTABLISHED: '#2e7d32', STRONG: '#1565c0', COMPETING: '#f9a825',
  FRONTIER: '#ef6c00', SPECULATIVE: '#c62828'
}};
const AXIS_SIZE = {{ E1: 14, E2: 12, E3: 10, E4: 8, E5: 6 }};

const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('tooltip');

let W, H;
function resize() {{
  W = canvas.width = canvas.offsetWidth;
  H = canvas.height = canvas.offsetHeight;
}}
resize();
window.addEventListener('resize', resize);

// Build nodes with physics state.
const nodes = DATA.nodes.map((n, i) => ({{
  ...n, x: W/2 + (Math.random()-.5)*400, y: H/2 + (Math.random()-.5)*400,
  vx: 0, vy: 0, visible: true,
  radius: AXIS_SIZE[n.evidence_axis] || 8,
  color: STATUS_COLORS[n.status] || '#888',
}}));

const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]));
const edges = DATA.edges.map(e => ({{
  ...e, visible: true,
  src: nodeMap[e.source], tgt: nodeMap[e.target],
}})).filter(e => e.src && e.tgt);

// Populate filters.
const domains = [...new Set(nodes.map(n => n.domain))].sort();
const statuses = [...new Set(nodes.map(n => n.status))].sort();
const axes = [...new Set(nodes.map(n => n.evidence_axis))].sort();
function addOpts(id, vals) {{
  const sel = document.getElementById(id);
  vals.forEach(v => {{ const o = document.createElement('option'); o.value = v; o.textContent = v; sel.appendChild(o); }});
}}
addOpts('filter-domain', domains);
addOpts('filter-status', statuses);
addOpts('filter-axis', axes);

function applyFilters() {{
  const fd = document.getElementById('filter-domain').value;
  const fs = document.getElementById('filter-status').value;
  const fa = document.getElementById('filter-axis').value;
  nodes.forEach(n => {{
    n.visible = (!fd || n.domain === fd) && (!fs || n.status === fs) && (!fa || n.evidence_axis === fa);
  }});
  edges.forEach(e => {{
    e.visible = e.src.visible && e.tgt.visible;
  }});
}}
document.getElementById('filter-domain').onchange = applyFilters;
document.getElementById('filter-status').onchange = applyFilters;
document.getElementById('filter-axis').onchange = applyFilters;

// Physics simulation.
let dragging = null, mouseX = 0, mouseY = 0;

canvas.addEventListener('mousedown', e => {{
  const r = canvas.getBoundingClientRect();
  const mx = e.clientX - r.left, my = e.clientY - r.top;
  for (const n of nodes) {{
    if (!n.visible) continue;
    if (Math.hypot(n.x - mx, n.y - my) < n.radius + 4) {{ dragging = n; break; }}
  }}
}});
canvas.addEventListener('mousemove', e => {{
  const r = canvas.getBoundingClientRect();
  mouseX = e.clientX - r.left; mouseY = e.clientY - r.top;
  if (dragging) {{ dragging.x = mouseX; dragging.y = mouseY; dragging.vx = 0; dragging.vy = 0; }}
  // Tooltip.
  let hit = null;
  for (const n of nodes) {{
    if (!n.visible) continue;
    if (Math.hypot(n.x - mouseX, n.y - mouseY) < n.radius + 4) {{ hit = n; break; }}
  }}
  if (hit) {{
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 12) + 'px';
    tooltip.style.top = (e.clientY + 12) + 'px';
    tooltip.innerHTML = `<h4>${{hit.title}}</h4>`
      + `<div class="meta">${{hit.domain}} · ${{hit.status}} · ${{hit.evidence_axis}}</div>`
      + `<div>Evidence: ${{hit.evidence_count}} · Open Qs: ${{hit.open_question_count}}</div>`
      + (hit.diverges ? '<div style="color:#f9a825">Axes diverge</div>' : '');
  }} else {{
    tooltip.style.display = 'none';
  }}
}});
canvas.addEventListener('mouseup', () => {{ dragging = null; }});

function tick() {{
  const alpha = 0.3;
  // Repulsion.
  for (let i = 0; i < nodes.length; i++) {{
    for (let j = i+1; j < nodes.length; j++) {{
      const a = nodes[i], b = nodes[j];
      if (!a.visible || !b.visible) continue;
      let dx = a.x - b.x, dy = a.y - b.y;
      let d = Math.hypot(dx, dy) || 1;
      if (d < 200) {{
        const f = 800 / (d * d);
        a.vx += dx/d * f; a.vy += dy/d * f;
        b.vx -= dx/d * f; b.vy -= dy/d * f;
      }}
    }}
  }}
  // Attraction along edges.
  for (const e of edges) {{
    if (!e.visible) continue;
    const a = e.src, b = e.tgt;
    let dx = b.x - a.x, dy = b.y - a.y;
    let d = Math.hypot(dx, dy) || 1;
    const ideal = e.cross_domain ? 300 : 120;
    const f = (d - ideal) * 0.005;
    a.vx += dx/d * f; a.vy += dy/d * f;
    b.vx -= dx/d * f; b.vy -= dy/d * f;
  }}
  // Center gravity.
  for (const n of nodes) {{
    if (!n.visible) continue;
    n.vx += (W/2 - n.x) * 0.001;
    n.vy += (H/2 - n.y) * 0.001;
  }}
  // Apply velocity.
  for (const n of nodes) {{
    if (n === dragging || !n.visible) continue;
    n.vx *= 0.85; n.vy *= 0.85;
    n.x += n.vx; n.y += n.vy;
    n.x = Math.max(n.radius, Math.min(W - n.radius, n.x));
    n.y = Math.max(n.radius, Math.min(H - n.radius, n.y));
  }}
}}

function draw() {{
  ctx.clearRect(0, 0, W, H);
  // Edges.
  for (const e of edges) {{
    if (!e.visible) continue;
    ctx.beginPath();
    ctx.moveTo(e.src.x, e.src.y);
    ctx.lineTo(e.tgt.x, e.tgt.y);
    if (e.kind === 'evidence_conflict') {{
      ctx.strokeStyle = '#c6282888'; ctx.lineWidth = 2;
      ctx.setLineDash([]);
    }} else if (e.cross_domain) {{
      ctx.strokeStyle = '#58a6ff44'; ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
    }} else if (e.kind === 'tensions') {{
      ctx.strokeStyle = '#f9a82566'; ctx.lineWidth = 1.5;
      ctx.setLineDash([6, 3]);
    }} else {{
      ctx.strokeStyle = '#30363d88'; ctx.lineWidth = 1;
      ctx.setLineDash([]);
    }}
    ctx.stroke();
    ctx.setLineDash([]);
  }}
  // Nodes.
  for (const n of nodes) {{
    if (!n.visible) continue;
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
    ctx.fillStyle = n.color;
    ctx.fill();
    if (n.diverges) {{
      ctx.strokeStyle = '#f9a825';
      ctx.lineWidth = 2;
      ctx.stroke();
    }}
  }}
}}

function loop() {{
  tick();
  draw();
  requestAnimationFrame(loop);
}}
loop();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    from ..data.registry import TOPICS
    graph = build_cross_domain_graph(TOPICS)
    render_epistemic_map(graph)
