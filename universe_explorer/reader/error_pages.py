"""404 page generator — auto-generate 404.html.

Generates:
  - 404.html with links to main pages

Usage:
    python -m universe_explorer.reader.error_pages
"""

from __future__ import annotations

from pathlib import Path

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def generate_404() -> str:
    """Generate 404.html."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>404 — Universe Explorer</title>
<style>
  :root {
    --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9;
    --muted: #8b949e; --accent: #58a6ff;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: system-ui, sans-serif;
         display: flex; align-items: center; justify-content: center;
         min-height: 100vh; }
  .container { text-align: center; max-width: 500px; padding: 2rem; }
  h1 { font-size: 4rem; color: var(--accent); margin-bottom: .5rem; }
  p { color: var(--muted); margin-bottom: 2rem; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .links { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
  .links a { padding: .5rem 1rem; border: 1px solid var(--border);
             border-radius: 6px; transition: border-color .15s; }
  .links a:hover { border-color: var(--accent); }
</style>
</head>
<body>
<div class="container">
  <h1>404</h1>
  <p>This page doesn't exist. But there's plenty of knowledge that does.</p>
  <div class="links">
    <a href="dashboard.html">Dashboard</a>
    <a href="index.html">Index</a>
    <a href="explore-v2.html">Explore</a>
    <a href="epistemic_map.html">Map</a>
    <a href="about.html">About</a>
  </div>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    html = generate_404()
    _DIST_DIR.mkdir(parents=True, exist_ok=True)
    out = _DIST_DIR / "404.html"
    out.write_text(html, encoding="utf-8")
    print(f"404.html -> {out}")
