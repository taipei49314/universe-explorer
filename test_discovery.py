"""Tests for the discovery pipeline.

Covers:
  - SourceAdapter ABC contract
  - ArxivAdapter / DoiAdapter structure
  - CandidateBuilder output shape
  - Pipeline report structure
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from universe_explorer.discovery.adapters.base import (
    EvidenceItem,
    FetchedRecord,
    RawResult,
    SourceAdapter,
)
from universe_explorer.discovery.adapters.arxiv_adapter import ArxivAdapter
from universe_explorer.discovery.adapters.doi_adapter import DoiAdapter
from universe_explorer.discovery.adapters.nasa_adapter import NasaAdapter
from universe_explorer.discovery.candidate_builder import (
    build_candidate,
    list_candidates,
    load_candidate,
    _make_label,
    _infer_kind,
)


# ---------------------------------------------------------------------------
# Adapter ABC contract
# ---------------------------------------------------------------------------


class TestAdapterABC:
    def test_arxiv_adapter_implements_interface(self):
        adapter = ArxivAdapter()
        assert adapter.name == "arxiv"
        assert adapter.source_ref_prefix == "arXiv:"
        assert hasattr(adapter, "search")
        assert hasattr(adapter, "fetch")
        assert hasattr(adapter, "extract_evidence")

    def test_doi_adapter_implements_interface(self):
        adapter = DoiAdapter()
        assert adapter.name == "doi"
        assert adapter.source_ref_prefix == "doi:"
        assert hasattr(adapter, "search")
        assert hasattr(adapter, "fetch")
        assert hasattr(adapter, "extract_evidence")

    def test_can_handle_arxiv(self):
        adapter = ArxivAdapter()
        assert adapter.can_handle("arXiv:2311.08680")
        assert not adapter.can_handle("doi:10.1038/xyz")

    def test_can_handle_doi(self):
        adapter = DoiAdapter()
        assert adapter.can_handle("doi:10.1038/xyz")
        assert not adapter.can_handle("arXiv:2311.08680")

    def test_nasa_adapter_implements_interface(self):
        adapter = NasaAdapter()
        assert adapter.name == "nasa"
        assert adapter.source_ref_prefix == "ADS:"
        assert hasattr(adapter, "search")
        assert hasattr(adapter, "fetch")
        assert hasattr(adapter, "extract_evidence")

    def test_can_handle_nasa(self):
        adapter = NasaAdapter()
        assert adapter.can_handle("ADS:2023ApJ...950L..20S")
        assert not adapter.can_handle("arXiv:2311.08680")


# ---------------------------------------------------------------------------
# RawResult / FetchedRecord / EvidenceItem data classes
# ---------------------------------------------------------------------------


class TestDataClasses:
    def test_raw_result_fields(self):
        r = RawResult(
            source_ref="arXiv:2311.08680",
            title="Test Paper",
            published="2023-11-15",
            authors=["Alice", "Bob"],
            summary="An abstract.",
        )
        assert r.source_ref == "arXiv:2311.08680"
        assert r.title == "Test Paper"
        assert len(r.authors) == 2

    def test_fetched_record_fields(self):
        r = FetchedRecord(
            source_ref="arXiv:2311.08680",
            cache_path="/tmp/cache.xml",
            sha256="abc123",
            endpoint="https://arxiv.org/api/query",
            retrieved_at="2023-11-15T00:00:00Z",
        )
        assert r.sha256 == "abc123"

    def test_evidence_item_fields(self):
        e = EvidenceItem(
            type="direct observation",
            description="We observed X.",
            source_ref="arXiv:2311.08680",
        )
        assert e.type == "direct observation"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_make_label_arxiv(self):
        assert _make_label("arXiv:2311.08680") == "arXiv-2311-08680"

    def test_make_label_doi(self):
        assert _make_label("doi:10.1038/nphys1234") == "doi-10-1038-nphys1234"

    def test_infer_kind_arxiv(self):
        record = FetchedRecord(
            source_ref="arXiv:2311.08680",
            cache_path="", sha256="", endpoint="", retrieved_at="",
        )
        assert _infer_kind(record) == "preprint (arXiv)"

    def test_infer_kind_doi_with_container(self):
        record = FetchedRecord(
            source_ref="doi:10.1038/xyz",
            cache_path="", sha256="", endpoint="", retrieved_at="",
            raw_metadata={"container": "Nature Physics"},
        )
        assert "Nature Physics" in _infer_kind(record)


# ---------------------------------------------------------------------------
# CandidateBuilder (with mocked adapter)
# ---------------------------------------------------------------------------


def _mock_adapter() -> SourceAdapter:
    """Create a mock adapter that returns predictable results."""
    adapter = MagicMock(spec=SourceAdapter)
    adapter.name = "mock"
    adapter.source_ref_prefix = "arXiv:"

    record = FetchedRecord(
        source_ref="arXiv:2311.08680",
        cache_path="/tmp/mock.xml",
        sha256="mockhash",
        endpoint="https://arxiv.org/api/query",
        retrieved_at="2023-01-01T00:00:00Z",
        title="Mock Paper",
        authors=["Mock Author"],
    )
    adapter.fetch.return_value = record
    adapter.extract_evidence.return_value = [
        EvidenceItem(
            type="theoretical result",
            description="Mock evidence description.",
            source_ref="arXiv-2311-08680",
        )
    ]
    return adapter


class TestCandidateBuilder:
    def test_build_candidate_structure(self, tmp_path):
        import universe_explorer.discovery.candidate_builder as cb
        old_dir = cb.CANDIDATES_DIR
        cb.CANDIDATES_DIR = tmp_path / "candidates"
        try:
            adapter = _mock_adapter()
            candidate = build_candidate(
                topic_id="test_topic",
                claim_id="test_claim",
                adapter=adapter,
                source_refs=["arXiv:2311.08680"],
                title="Test Claim",
            )
            assert candidate["id"] == "test_claim"
            assert candidate["topic_id"] == "test_topic"
            assert candidate["title"] == "Test Claim"
            assert candidate["status"] is None  # human decides
            assert len(candidate["sources"]) == 1
            assert len(candidate["evidence"]) == 1
            assert "_discovery" in candidate
            assert candidate["_discovery"]["adapter"] == "mock"
        finally:
            cb.CANDIDATES_DIR = old_dir

    def test_build_candidate_writes_to_disk(self, tmp_path):
        import universe_explorer.discovery.candidate_builder as cb
        old_dir = cb.CANDIDATES_DIR
        cb.CANDIDATES_DIR = tmp_path / "candidates"
        try:
            adapter = _mock_adapter()
            build_candidate(
                topic_id="t1", claim_id="c1",
                adapter=adapter, source_refs=["arXiv:2311.08680"],
            )
            path = tmp_path / "candidates" / "t1" / "c1.json"
            assert path.exists()
            data = json.loads(path.read_text(encoding="utf-8"))
            assert data["id"] == "c1"
        finally:
            cb.CANDIDATES_DIR = old_dir

    def test_build_candidate_handles_fetch_error(self, tmp_path):
        import universe_explorer.discovery.candidate_builder as cb
        old_dir = cb.CANDIDATES_DIR
        cb.CANDIDATES_DIR = tmp_path / "candidates"
        try:
            adapter = _mock_adapter()
            adapter.fetch.side_effect = FileNotFoundError("not found")
            candidate = build_candidate(
                topic_id="t1", claim_id="c1",
                adapter=adapter, source_refs=["arXiv:9999.99999"],
            )
            assert len(candidate["sources"]) == 0
            assert len(candidate["_discovery"]["fetch_errors"]) == 1
        finally:
            cb.CANDIDATES_DIR = old_dir

    def test_load_candidate(self, tmp_path):
        import universe_explorer.discovery.candidate_builder as cb
        old_dir = cb.CANDIDATES_DIR
        cb.CANDIDATES_DIR = tmp_path / "candidates"
        try:
            adapter = _mock_adapter()
            build_candidate(
                topic_id="t1", claim_id="c1",
                adapter=adapter, source_refs=["arXiv:2311.08680"],
            )
            loaded = load_candidate("t1", "c1")
            assert loaded is not None
            assert loaded["id"] == "c1"
            assert load_candidate("t1", "nonexistent") is None
        finally:
            cb.CANDIDATES_DIR = old_dir

    def test_list_candidates(self, tmp_path):
        import universe_explorer.discovery.candidate_builder as cb
        old_dir = cb.CANDIDATES_DIR
        cb.CANDIDATES_DIR = tmp_path / "candidates"
        try:
            adapter = _mock_adapter()
            build_candidate(topic_id="t1", claim_id="c1",
                            adapter=adapter, source_refs=["arXiv:2311.08680"])
            build_candidate(topic_id="t1", claim_id="c2",
                            adapter=adapter, source_refs=["arXiv:2311.08680"])
            all_c = list_candidates()
            assert len(all_c) == 2
            t1_c = list_candidates("t1")
            assert len(t1_c) == 2
        finally:
            cb.CANDIDATES_DIR = old_dir


# ---------------------------------------------------------------------------
# ArxivAdapter.search (mocked HTTP)
# ---------------------------------------------------------------------------


class TestArxivAdapterSearch:
    def test_search_returns_raw_results(self):
        """Test with a mocked HTTP response."""
        adapter = ArxivAdapter()
        mock_xml = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2311.08680v1</id>
    <title>Test Paper Title</title>
    <published>2023-11-15T00:00:00Z</published>
    <author><name>Alice</name></author>
    <summary>A test abstract.</summary>
  </entry>
</feed>"""

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_resp = MagicMock()
            mock_resp.read.return_value = mock_xml.encode("utf-8")
            mock_resp.__enter__ = lambda s: s
            mock_resp.__exit__ = MagicMock(return_value=False)
            mock_urlopen.return_value = mock_resp

            results = adapter.search("test query", max_results=1)
            assert len(results) == 1
            assert results[0].source_ref == "arXiv:2311.08680"
            assert results[0].title == "Test Paper Title"

# --- discovery pipeline error contracts ---
from unittest.mock import MagicMock, patch
import pytest
from universe_explorer.discovery.pipeline import (
    DiscoveryError,
    get_adapter,
    run_pipeline,
)


class TestDiscoveryPipelineErrors:
    def test_unknown_adapter(self):
        with pytest.raises(DiscoveryError) as ei:
            get_adapter("not_a_real_adapter")
        assert "unknown adapter" in ei.value.message

    def test_unknown_topic_fails_before_network(self):
        with pytest.raises(DiscoveryError) as ei:
            run_pipeline("anything", topic_id="nope_not_a_topic")
        assert "unknown topic" in ei.value.message

    def test_network_timeout_becomes_discovery_error(self):
        import socket
        mock_adapter = MagicMock()
        mock_adapter.search.side_effect = socket.timeout("timed out")
        with patch.dict(
            "universe_explorer.discovery.pipeline.ADAPTERS",
            {"mock": mock_adapter},
        ):
            with pytest.raises(DiscoveryError) as ei:
                run_pipeline("q", topic_id="cosmology", adapter_name="mock")
        assert "failed" in ei.value.message.lower()
        assert "No candidates were written" in ei.value.message

    def test_cli_discover_unknown_topic_exit_1(self):
        from universe_explorer.__main__ import main
        code = main(["discover", "q", "--topic", "definitely_missing_topic_xyz"])
        assert code == 1
