"""Robots.txt generator — auto-generate robots.txt for search engines.

Generates:
  - robots.txt with sitemap reference

Usage:
    python -m universe_explorer.reader.robots
"""

from __future__ import annotations

from pathlib import Path

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def generate_robots(base_url: str = "https://taipei49314.github.io/universe-explorer") -> str:
    """Generate robots.txt."""
    return f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
"""


if __name__ == "__main__":
    robots = generate_robots()
    _DIST_DIR.mkdir(parents=True, exist_ok=True)
    out = _DIST_DIR / "robots.txt"
    out.write_text(robots, encoding="utf-8")
    print(f"robots.txt -> {out}")
