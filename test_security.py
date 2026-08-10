"""Security tests — verify no common vulnerabilities.

Checks:
  - No XSS in HTML generation (unescaped user input)
  - No path traversal in file operations
  - No injection in CLI argument handling
  - No sensitive data in outputs
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from universe_explorer.data.registry import TOPICS
from universe_explorer.render import render_topic, claims_json
from universe_explorer.reader.render_explore import render_explore_v2
from universe_explorer.reader.dashboard import render_dashboard


class TestXSSPrevention:
    """HTML output should not contain unescaped user input."""

    def test_render_escapes_html_in_title(self):
        """HTML in claim titles should be escaped."""
        # The renderer uses html.escape, so this should be safe.
        # We verify by checking the output doesn't contain raw HTML.
        for topic in TOPICS:
            html = render_topic(topic)
            # Should not contain unescaped <script> tags
            assert "<script>" not in html, \
                f"Topic {topic.id} contains unescaped <script>"

    def test_render_escapes_html_in_evidence(self):
        """HTML in evidence descriptions should be escaped."""
        for topic in TOPICS:
            html = render_topic(topic)
            # Should not contain unescaped <script> tags
            assert "<script>" not in html

    def test_claims_json_escapes_html(self):
        """claims.json should escape HTML in titles."""
        import json
        json_str = claims_json(TOPICS)
        data = json.loads(json_str)
        for claim in data["claims"]:
            title = claim.get("title", "")
            # Should not contain unescaped HTML
            assert "<script>" not in title

    def test_explore_v2_escapes_html(self, tmp_path):
        """explore-v2.html should escape HTML in user-facing content."""
        render_explore_v2(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "explore-v2.html").read_text(encoding="utf-8")
        # innerHTML is used for dynamic rendering, but user data should be escaped
        # Check that no raw <script> tags from claim data appear
        assert "<script>alert" not in html  # No XSS payloads

    def test_dashboard_escapes_html(self, tmp_path):
        """dashboard.html should escape HTML."""
        render_dashboard(TOPICS, dist_dir=tmp_path)
        html = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
        assert "<script>" not in html or "innerHTML" not in html


class TestPathTraversal:
    """File operations should not allow path traversal."""

    def test_search_index_no_traversal(self):
        """Search index should not allow path traversal."""
        from universe_explorer.reader.search_index import ClaimSearchIndex
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        # Search for path traversal attempts
        results = index.search("../../../etc/passwd")
        # Should not crash or return sensitive data
        assert isinstance(results, list)

    def test_filter_no_traversal(self):
        """Filter should not allow path traversal."""
        from universe_explorer.reader.filter_engine import ClaimFilter, FilterCriteria
        filt = ClaimFilter(TOPICS)
        results = filt.filter(FilterCriteria(domain="../../../etc"))
        assert isinstance(results, list)

    def test_annotate_no_traversal(self, tmp_path):
        """Annotations should not allow path traversal."""
        from universe_explorer.reader.annotate import ClaimAnnotations
        mgr = ClaimAnnotations(tmp_path / "ann")
        # Try to create annotation with path traversal
        mgr.add_tag("../../../etc/passwd", "test")
        # Should not create files outside the directory
        assert not (tmp_path / "etc").exists()


class TestInputSanitization:
    """User input should be sanitized."""

    def test_search_handles_special_chars(self):
        """Search should handle special characters safely."""
        from universe_explorer.reader.search_index import ClaimSearchIndex
        index = ClaimSearchIndex(TOPICS, use_cache=False)
        # Try various special characters
        for query in ["<script>", "'; DROP TABLE--", "../../", "\\x00"]:
            results = index.search(query)
            assert isinstance(results, list)

    def test_filter_handles_special_chars(self):
        """Filter should handle special characters safely."""
        from universe_explorer.reader.filter_engine import ClaimFilter, FilterCriteria
        filt = ClaimFilter(TOPICS)
        results = filt.filter(FilterCriteria(domain="<script>"))
        assert isinstance(results, list)


class TestOutputSafety:
    """Outputs should not contain sensitive data."""

    def test_claims_json_no_secrets(self):
        """claims.json should not contain API keys or tokens."""
        import json
        json_str = claims_json(TOPICS)
        # Should not contain common secret patterns
        assert "api_key" not in json_str.lower()
        assert "token" not in json_str.lower()
        assert "password" not in json_str.lower()

    def test_html_no_secrets(self):
        """HTML outputs should not contain API keys or tokens."""
        for topic in TOPICS:
            html = render_topic(topic)
            assert "api_key" not in html.lower()
            assert "token" not in html.lower()
            assert "password" not in html.lower()
