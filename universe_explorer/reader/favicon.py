"""Favicon generator — auto-generate favicon.svg.

Generates:
  - favicon.svg with universe theme

Usage:
    python -m universe_explorer.reader.favicon
"""

from __future__ import annotations

from pathlib import Path

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"


def generate_favicon() -> str:
    """Generate favicon.svg."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="14" fill="#0d1117" stroke="#58a6ff" stroke-width="2"/>
  <circle cx="16" cy="16" r="4" fill="#58a6ff"/>
  <circle cx="16" cy="16" r="8" fill="none" stroke="#58a6ff" stroke-width="1" opacity="0.5"/>
  <circle cx="16" cy="16" r="12" fill="none" stroke="#58a6ff" stroke-width="0.5" opacity="0.3"/>
</svg>
"""


if __name__ == "__main__":
    svg = generate_favicon()
    _DIST_DIR.mkdir(parents=True, exist_ok=True)
    out = _DIST_DIR / "favicon.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"favicon.svg -> {out}")
