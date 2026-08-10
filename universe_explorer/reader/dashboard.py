"""Dashboard — central hub linking all pages.

Generates dist/dashboard.html with:
  - Stats overview (claims, domains, edges, evidence, sources, questions)
  - Status distribution with bar chart
  - Evidence type breakdown
  - Quality metrics (divergent, competing, isolated)
  - Links to all pages (old + new)

Usage:
    python -m universe_explorer.reader.dashboard
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..axes import derive, diverges
from ..model import Status, Topic
from ..crossdomain.graph_builder import build_cross_domain_graph
from .stats import compute_stats

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def render_dashboard(topics: List[Topic], dist_dir: Path = _DIST_DIR) -> Path:
    """Generate dist/dashboard.html."""
    stats = compute_stats(topics)
    graph = build_cross_domain_graph(topics)
    edge_count = len(graph.edges)
    cross_domain = sum(1 for e in graph.edges if e.cross_domain)

    # Status bars.
    status_bars = ""
    colors = {
        "ESTABLISHED": "#2e7d32", "STRONG": "#1565c0",
        "COMPETING": "#f9a825", "FRONTIER": "#ef6c00", "SPECULATIVE": "#c62828",
    }
    lights = {
        "ESTABLISHED": "🟢", "STRONG": "🔵",
        "COMPETING": "🟡", "FRONTIER": "🟠", "SPECULATIVE": "🔴",
    }
    for name in ["ESTABLISHED", "STRONG", "COMPETING", "FRONTIER", "SPECULATIVE"]:
        count = stats.claims_by_status.get(name, 0)
        pct = (count / stats.total_claims * 100) if stats.total_claims else 0
        status_bars += (
            f'<div class="bar-row">'
            f'<span class="bar-label">{lights.get(name, "")} {name}</span>'
            f'<div class="bar-track"><div class="bar-fill" '
            f'style="width:{pct:.0f}%;background:{colors.get(name, "#888")}"></div></div>'
            f'<span class="bar-count">{count}</span>'
            f'</div>'
        )

    # Evidence type bars.
    ev_bars = ""
    ev_colors = {
        "direct observation": "#2e7d32",
        "indirect observation": "#1565c0",
        "analog experiment": "#f9a825",
        "theoretical derivation": "#ef6c00",
        "theoretical result": "#c62828",
    }
    max_ev = max(stats.evidence_by_type.values()) if stats.evidence_by_type else 1
    for etype, count in sorted(stats.evidence_by_type.items(),
                                key=lambda x: x[1], reverse=True):
        pct = (count / max_ev * 100) if max_ev else 0
        ev_bars += (
            f'<div class="bar-row">'
            f'<span class="bar-label">{etype}</span>'
            f'<div class="bar-track"><div class="bar-fill" '
            f'style="width:{pct:.0f}%;background:{ev_colors.get(etype, "#888")}"></div></div>'
            f'<span class="bar-count">{count}</span>'
            f'</div>'
        )

    # Quality metrics.
    quality_html = ""
    if stats.divergent_count > 0:
        quality_html += f'<div class="quality-item"><span class="q-num">{stats.divergent_count}</span> divergent claims (consensus ≠ evidence)</div>'
    if stats.competing_count > 0:
        quality_html += f'<div class="quality-item"><span class="q-num">{stats.competing_count}</span> competing models</div>'
    if stats.isolated_count > 0:
        quality_html += f'<div class="quality-item"><span class="q-num">{stats.isolated_count}</span> isolated claims (no edges)</div>'

    html_content = _DASHBOARD_TEMPLATE.format(
        total_claims=stats.total_claims,
        domains=stats.total_topics,
        edge_count=edge_count,
        cross_domain=cross_domain,
        divergent_count=stats.divergent_count,
        total_evidence=stats.total_evidence,
        total_sources=stats.total_sources,
        total_open_questions=stats.total_open_questions,
        status_bars=status_bars,
        ev_bars=ev_bars,
        quality_html=quality_html,
    )

    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = dist_dir / "dashboard.html"
    out_path.write_text(html_content, encoding="utf-8")
    print(f"[dashboard] {stats.total_claims} claims, {stats.total_topics} domains -> {out_path}")
    return out_path


_DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard — Universe Explorer</title>
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9;
    --muted: #8b949e; --accent: #58a6ff;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: system-ui, sans-serif;
         padding: 2rem; max-width: 900px; margin: 0 auto; }}
  h1 {{ font-size: 1.8rem; margin-bottom: .25rem; }}
  .subtitle {{ color: var(--muted); margin-bottom: 2rem; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 1rem; margin-bottom: 2rem; }}
  .stat-card {{ background: var(--card); border: 1px solid var(--border);
                border-radius: 8px; padding: 1rem; text-align: center; }}
  .stat-card .number {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}
  .stat-card .label {{ font-size: .8rem; color: var(--muted); }}
  .section {{ margin-bottom: 2rem; }}
  .section h2 {{ font-size: 1.2rem; margin-bottom: 1rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
           gap: .75rem; }}
  .link-card {{ background: var(--card); border: 1px solid var(--border);
                border-radius: 8px; padding: 1rem; text-decoration: none;
                color: var(--text); transition: border-color .15s; }}
  .link-card:hover {{ border-color: var(--accent); }}
  .link-card h3 {{ font-size: .95rem; margin-bottom: .25rem; color: var(--accent); }}
  .link-card p {{ font-size: .8rem; color: var(--muted); }}
  .bar-row {{ display: flex; align-items: center; gap: .5rem; margin-bottom: .4rem; }}
  .bar-label {{ width: 180px; font-size: .85rem; }}
  .bar-track {{ flex: 1; height: 8px; background: #21262d; border-radius: 4px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 4px; transition: width .3s; }}
  .bar-count {{ width: 30px; text-align: right; font-size: .85rem; color: var(--muted); }}
  .quality-item {{ padding: .4rem 0; font-size: .9rem; }}
  .q-num {{ font-weight: 700; color: var(--accent); margin-right: .25rem; }}
</style>
</head>
<body>
<h1>Universe Explorer</h1>
<p class="subtitle">Honestly separating what we know from what we don't.</p>

<div class="stats">
  <div class="stat-card"><div class="number">{total_claims}</div><div class="label">Claims</div></div>
  <div class="stat-card"><div class="number">{domains}</div><div class="label">Domains</div></div>
  <div class="stat-card"><div class="number">{edge_count}</div><div class="label">Relations</div></div>
  <div class="stat-card"><div class="number">{cross_domain}</div><div class="label">Cross-Domain</div></div>
  <div class="stat-card"><div class="number">{total_evidence}</div><div class="label">Evidence</div></div>
  <div class="stat-card"><div class="number">{total_sources}</div><div class="label">Sources</div></div>
  <div class="stat-card"><div class="number">{total_open_questions}</div><div class="label">Open Qs</div></div>
  <div class="stat-card"><div class="number">{divergent_count}</div><div class="label">Divergent</div></div>
</div>

<div class="section">
  <h2>Status Distribution</h2>
  {status_bars}
</div>

<div class="section">
  <h2>Evidence Types</h2>
  {ev_bars}
</div>

<div class="section">
  <h2>Quality Metrics</h2>
  {quality_html}
</div>

<div class="section">
  <h2>Explore</h2>
  <div class="grid">
    <a class="link-card" href="explore-v2.html">
      <h3>Explore v2</h3>
      <p>Search, filter, and browse all claims with dual-axis visualization.</p>
    </a>
    <a class="link-card" href="epistemic_map.html">
      <h3>Epistemic Map</h3>
      <p>Interactive cross-domain knowledge graph.</p>
    </a>
    <a class="link-card" href="app.html">
      <h3>Knowledge Map</h3>
      <p>Interactive map with ego graph, reading paths, and guides.</p>
    </a>
    <a class="link-card" href="universe.html">
      <h3>Universe</h3>
      <p>Constellation view of all domains.</p>
    </a>
  </div>
</div>

<div class="section">
  <h2>Discovery</h2>
  <div class="grid">
    <a class="link-card" href="review.html">
      <h3>Review Dashboard</h3>
      <p>Review candidate claims from Discovery Pipeline.</p>
    </a>
    <a class="link-card" href="challenge.html">
      <h3>Challenge a Verdict</h3>
      <p>Submit a challenge to any claim's status light.</p>
    </a>
  </div>
</div>

<div class="section">
  <h2>Data</h2>
  <div class="grid">
    <a class="link-card" href="claims.json">
      <h3>claims.json</h3>
      <p>Open data: all claims with evidence, status, and relations.</p>
    </a>
    <a class="link-card" href="epistemic-graph.json">
      <h3>epistemic-graph.json</h3>
      <p>Cross-domain knowledge graph in JSON.</p>
    </a>
    <a class="link-card" href="stats.json">
      <h3>stats.json</h3>
      <p>Knowledge base statistics and quality metrics.</p>
    </a>
    <a class="link-card" href="feed.xml">
      <h3>feed.xml</h3>
      <p>Atom feed of change events (restates, never interprets).</p>
    </a>
    <a class="link-card" href="dual-axis.svg">
      <h3>dual-axis.svg</h3>
      <p>Consensus × Evidence scatter plot.</p>
    </a>
  </div>
</div>

<div class="section">
  <h2>Reference</h2>
  <div class="grid">
    <a class="link-card" href="about.html">
      <h3>About</h3>
      <p>How to read, constitution, and support.</p>
    </a>
    <a class="link-card" href="health.html">
      <h3>Health</h3>
      <p>Inventory audit and source health.</p>
    </a>
    <a class="link-card" href="changes.html">
      <h3>Changes</h3>
      <p>Recent restated events.</p>
    </a>
    <a class="link-card" href="index.html">
      <h3>Index</h3>
      <p>Topic cards with expandable details.</p>
    </a>
  </div>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    from ..data.registry import TOPICS
    render_dashboard(TOPICS)
