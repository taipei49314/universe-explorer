"""Sitemap generator — auto-generate sitemap.xml for search engines.

Generates:
  - sitemap.xml with all public pages
  - Last modified dates from file system

Usage:
    python -m universe_explorer.reader.sitemap
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
_DIST_DIR = _ROOT / "dist"

# Public pages to include in sitemap.
PUBLIC_PAGES = [
    "index.html",
    "app.html",
    "universe.html",
    "explore3d.html",
    "explore.html",
    "explore-v2.html",
    "epistemic_map.html",
    "dashboard.html",
    "about.html",
    "health.html",
    "changes.html",
    "challenge.html",
    "review.html",
    "api-docs.html",
]


def generate_sitemap(base_url: str = "https://taipei49314.github.io/universe-explorer") -> str:
    """Generate sitemap.xml."""
    entries = []
    for page in PUBLIC_PAGES:
        path = _DIST_DIR / page
        if path.exists():
            mtime = datetime.fromtimestamp(
                path.stat().st_mtime, tz=timezone.utc
            ).strftime("%Y-%m-%d")
            url = f"{base_url}/{page}"
            entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{mtime}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>"""


if __name__ == "__main__":
    sitemap = generate_sitemap()
    _DIST_DIR.mkdir(parents=True, exist_ok=True)
    out = _DIST_DIR / "sitemap.xml"
    out.write_text(sitemap, encoding="utf-8")
    print(f"sitemap.xml -> {out}")
