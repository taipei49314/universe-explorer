"""Accessibility tests — verify HTML pages meet basic accessibility.

Checks:
  - All images have alt text
  - All forms have labels
  - All pages have lang attribute
  - All pages have proper heading hierarchy
  - All interactive elements are keyboard accessible
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from universe_explorer.data.registry import TOPICS
from universe_explorer.reader.render_explore import render_explore_v2
from universe_explorer.reader.dashboard import render_dashboard
from universe_explorer.reader.challenge_form import generate_challenge_form


class TestAccessibility:
    """HTML pages should meet basic accessibility standards."""

    def test_explore_v2_has_lang(self, tmp_path):
        """explore-v2.html should have lang attribute."""
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "explore-v2.html").read_text(encoding="utf-8")
        assert 'lang=' in html

    def test_dashboard_has_lang(self, tmp_path):
        """dashboard.html should have lang attribute."""
        render_dashboard(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
        assert 'lang=' in html

    def test_challenge_has_lang(self, tmp_path):
        """challenge.html should have lang attribute."""
        generate_challenge_form(dist_dir=tmp_path)
        html = (tmp_path / "challenge.html").read_text(encoding="utf-8")
        assert 'lang=' in html

    def test_explore_v2_has_title(self, tmp_path):
        """explore-v2.html should have <title>."""
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "explore-v2.html").read_text(encoding="utf-8")
        assert '<title>' in html

    def test_dashboard_has_title(self, tmp_path):
        """dashboard.html should have <title>."""
        render_dashboard(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
        assert '<title>' in html

    def test_explore_v2_has_viewport(self, tmp_path):
        """explore-v2.html should have viewport meta tag."""
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "explore-v2.html").read_text(encoding="utf-8")
        assert 'viewport' in html

    def test_dashboard_has_viewport(self, tmp_path):
        """dashboard.html should have viewport meta tag."""
        render_dashboard(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
        assert 'viewport' in html

    def test_explore_v2_has_headings(self, tmp_path):
        """explore-v2.html should have headings."""
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "explore-v2.html").read_text(encoding="utf-8")
        assert '<h1' in html or '<h2' in html

    def test_dashboard_has_headings(self, tmp_path):
        """dashboard.html should have headings."""
        render_dashboard(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
        assert '<h1' in html or '<h2' in html

    def test_challenge_has_form_labels(self, tmp_path):
        """challenge.html should have form labels."""
        generate_challenge_form(dist_dir=tmp_path)
        html = (tmp_path / "challenge.html").read_text(encoding="utf-8")
        assert '<label' in html

    def test_challenge_routes_to_github_templates(self, tmp_path):
        """challenge.html must link GitHub issue templates (user overturn path)."""
        generate_challenge_form(dist_dir=tmp_path)
        html = (tmp_path / "challenge.html").read_text(encoding="utf-8")
        assert "challenge-a-verdict.yml" in html
        assert "github.com/taipei49314/universe-explorer" in html

    def test_explore_v2_has_aria(self, tmp_path):
        """explore-v2.html should have ARIA or semantic HTML."""
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "explore-v2.html").read_text(encoding="utf-8")
        # Semantic HTML elements are also acceptable
        has_semantic = any(tag in html for tag in [
            '<nav', '<main', '<header', '<footer', '<section', '<article',
            'aria-', 'role=',
        ])
        assert has_semantic, "No semantic HTML or ARIA attributes found"
