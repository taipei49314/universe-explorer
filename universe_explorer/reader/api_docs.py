"""API documentation generator — auto-generate docs from code.

Generates:
  - Module listing with descriptions
  - CLI command reference
  - Data model reference
  - Test coverage summary

Usage:
    python -m universe_explorer.reader.api_docs
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..data.registry import TOPICS

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def generate_api_docs(dist_dir: Path = _DIST_DIR) -> Path:
    """Generate API documentation."""
    modules = _get_modules()
    cli_commands = _get_cli_commands()
    data_model = _get_data_model()

    content = _TEMPLATE.format(
        modules=_format_modules(modules),
        cli_commands=_format_cli(cli_commands),
        data_model=_format_data_model(data_model),
        total_claims=sum(len(t.claims) for t in TOPICS),
        total_topics=len(TOPICS),
    )

    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = dist_dir / "api-docs.html"
    out_path.write_text(content, encoding="utf-8")
    print(f"[api-docs] {len(modules)} modules, {len(cli_commands)} commands -> {out_path}")
    return out_path


def _get_modules() -> list:
    """Get all modules with descriptions."""
    return [
        {"name": "discovery", "desc": "Discovery Pipeline — automated intake with constitution gate",
         "submodules": ["adapters", "candidate_builder", "precheck", "review", "pipeline"]},
        {"name": "crossdomain", "desc": "Cross-Domain Map — find connections between isolated domains",
         "submodules": ["shared_source", "evidence_conflict", "gap_analyzer", "graph_builder", "render_map"]},
        {"name": "reader", "desc": "Reader Experience — search, filter, explore, challenge",
         "submodules": ["search_index", "filter_engine", "dual_axis_viz", "guided_reading",
                        "challenge_form", "render_explore", "dashboard", "stats",
                        "export", "annotate", "review", "diff", "dynamic_paths",
                        "automation_metrics", "api_docs"]},
        {"name": "model", "desc": "Frozen data model — Claim, Topic, Status, Evidence, Source"},
        {"name": "validator", "desc": "Constitution court — enforce hard red lines"},
        {"name": "axes", "desc": "Evidence axis — derived, never declared"},
        {"name": "provenance", "desc": "Cite ⇒ fetch — arXiv/DOI verification"},
        {"name": "proposals", "desc": "Status proposals — propose, never decide"},
        {"name": "watch", "desc": "Change detection — no silent light changes"},
        {"name": "narrative", "desc": "AI Narrative — compose + check"},
        {"name": "relations", "desc": "Claim relations — edges + reading paths"},
        {"name": "render", "desc": "Static HTML renderer"},
        {"name": "surface", "desc": "Changes + health surfaces"},
    ]


def _get_cli_commands() -> list:
    """Get CLI commands."""
    return [
        {"cmd": "build", "desc": "Validate + render site to dist/"},
        {"cmd": "build --check", "desc": "Validate only"},
        {"cmd": "search <query>", "desc": "Full-text search over claims"},
        {"cmd": "filter [opts]", "desc": "Multi-dimensional filter"},
        {"cmd": "stats", "desc": "Knowledge base statistics"},
        {"cmd": "paths", "desc": "List all reading paths"},
        {"cmd": "discover <q>", "desc": "Run discovery pipeline"},
        {"cmd": "graph", "desc": "Cross-domain graph report"},
        {"cmd": "health", "desc": "Integrity check all components"},
    ]


def _get_data_model() -> dict:
    """Get data model reference."""
    return {
        "Claim": ["id", "title", "status", "status_reason", "evidence",
                   "competing_models", "open_questions", "sources", "status_history"],
        "Topic": ["id", "title", "summary", "claims"],
        "Status": ["ESTABLISHED", "STRONG", "COMPETING", "FRONTIER", "SPECULATIVE"],
        "Evidence": ["type", "description", "source_ref"],
        "Source": ["label", "url_or_id", "kind"],
    }


def _format_modules(modules: list) -> str:
    lines = []
    for m in modules:
        subs = ", ".join(m.get("submodules", []))
        lines.append(f'<tr><td><strong>{m["name"]}</strong></td>'
                     f'<td>{m["desc"]}</td>'
                     f'<td>{subs}</td></tr>')
    return "\n".join(lines)


def _format_cli(commands: list) -> str:
    lines = []
    for c in commands:
        lines.append(f'<tr><td><code>{c["cmd"]}</code></td>'
                     f'<td>{c["desc"]}</td></tr>')
    return "\n".join(lines)


def _format_data_model(model: dict) -> str:
    lines = []
    for name, fields in model.items():
        fs = ", ".join(f'<code>{f}</code>' for f in fields)
        lines.append(f'<tr><td><strong>{name}</strong></td><td>{fs}</td></tr>')
    return "\n".join(lines)


_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>API Docs — Universe Explorer</title>
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9;
    --muted: #8b949e; --accent: #58a6ff;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: system-ui, sans-serif;
         padding: 2rem; max-width: 900px; margin: 0 auto; }}
  h1 {{ font-size: 1.8rem; margin-bottom: .5rem; }}
  h2 {{ font-size: 1.2rem; margin: 2rem 0 1rem; color: var(--accent); }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 2rem; }}
  th, td {{ text-align: left; padding: .5rem; border-bottom: 1px solid var(--border); }}
  th {{ color: var(--muted); font-size: .85rem; }}
  code {{ background: var(--card); padding: .15rem .4rem; border-radius: 3px; font-size: .9rem; }}
  nav {{ margin-bottom: 1.5rem; }}
  nav a {{ color: var(--accent); text-decoration: none; margin-right: 1rem; }}
  .stat {{ color: var(--muted); font-size: .9rem; margin-bottom: .5rem; }}
</style>
</head>
<body>
<nav>
  <a href="dashboard.html">Dashboard</a>
  <a href="index.html">Index</a>
  <a href="app.html">Map</a>
</nav>
<h1>API Documentation</h1>
<p class="stat">{total_topics} topics · {total_claims} claims · Constitution-gated</p>

<h2>Modules</h2>
<table>
<tr><th>Module</th><th>Description</th><th>Submodules</th></tr>
{modules}
</table>

<h2>CLI Commands</h2>
<table>
<tr><th>Command</th><th>Description</th></tr>
{cli_commands}
</table>

<h2>Data Model</h2>
<table>
<tr><th>Type</th><th>Fields</th></tr>
{data_model}
</table>
</body>
</html>
"""


if __name__ == "__main__":
    generate_api_docs()
