"""Link validation tests — verify all internal links resolve.

Checks:
  - All <a href="..."> links in HTML files resolve to existing files
  - All <img src="..."> links resolve
  - All <link href="..."> links resolve (CSS)
  - All <script src="..."> links resolve
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_DIST_DIR = Path(__file__).parent / "dist"


class TestInternalLinks:
    """All internal links should resolve."""

    @pytest.fixture(autouse=True)
    def ensure_dist(self):
        if not _DIST_DIR.exists():
            pytest.skip("dist/ not found")

    def _get_internal_links(self, html_content: str) -> list:
        """Extract internal links from HTML content."""
        links = []
        # Match href="..." and src="..."
        for match in re.finditer(r'(?:href|src)="([^"]*)"', html_content):
            url = match.group(1)
            # Skip external links, anchors, javascript, mailto
            if (url.startswith("http") or url.startswith("#") or
                url.startswith("javascript:") or url.startswith("mailto:") or
                "${" in url):
                continue
            # Remove query strings and anchors
            clean = url.split("?")[0].split("#")[0]
            if clean:
                links.append(clean)
        return links

    def test_index_html_links_resolve(self):
        """All links in index.html should resolve."""
        path = _DIST_DIR / "index.html"
        if not path.exists():
            pytest.skip("index.html not found")
        content = path.read_text(encoding="utf-8")
        links = self._get_internal_links(content)
        for link in links:
            target = _DIST_DIR / link
            assert target.exists(), f"Broken link in index.html: {link}"

    def test_app_html_links_resolve(self):
        """All links in app.html should resolve."""
        path = _DIST_DIR / "app.html"
        if not path.exists():
            pytest.skip("app.html not found")
        content = path.read_text(encoding="utf-8")
        links = self._get_internal_links(content)
        for link in links:
            target = _DIST_DIR / link
            assert target.exists(), f"Broken link in app.html: {link}"

    def test_dashboard_links_resolve(self):
        """All links in dashboard.html should resolve."""
        path = _DIST_DIR / "dashboard.html"
        if not path.exists():
            pytest.skip("dashboard.html not found")
        content = path.read_text(encoding="utf-8")
        links = self._get_internal_links(content)
        for link in links:
            target = _DIST_DIR / link
            assert target.exists(), f"Broken link in dashboard.html: {link}"

    def test_explore_v2_links_resolve(self):
        """All links in explore-v2.html should resolve."""
        path = _DIST_DIR / "explore-v2.html"
        if not path.exists():
            pytest.skip("explore-v2.html not found")
        content = path.read_text(encoding="utf-8")
        links = self._get_internal_links(content)
        for link in links:
            target = _DIST_DIR / link
            assert target.exists(), f"Broken link in explore-v2.html: {link}"

    def test_epistemic_map_links_resolve(self):
        """All links in epistemic_map.html should resolve."""
        path = _DIST_DIR / "epistemic_map.html"
        if not path.exists():
            pytest.skip("epistemic_map.html not found")
        content = path.read_text(encoding="utf-8")
        links = self._get_internal_links(content)
        for link in links:
            target = _DIST_DIR / link
            assert target.exists(), f"Broken link in epistemic_map.html: {link}"

    def test_review_links_resolve(self):
        """All links in review.html should resolve."""
        path = _DIST_DIR / "review.html"
        if not path.exists():
            pytest.skip("review.html not found")
        content = path.read_text(encoding="utf-8")
        links = self._get_internal_links(content)
        for link in links:
            target = _DIST_DIR / link
            assert target.exists(), f"Broken link in review.html: {link}"

    def test_about_links_resolve(self):
        """All links in about.html should resolve."""
        path = _DIST_DIR / "about.html"
        if not path.exists():
            pytest.skip("about.html not found")
        content = path.read_text(encoding="utf-8")
        links = self._get_internal_links(content)
        for link in links:
            target = _DIST_DIR / link
            assert target.exists(), f"Broken link in about.html: {link}"
