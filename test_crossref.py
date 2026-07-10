"""C2 / Amendment #6 acceptance tests. All failure cases use forged fixtures
in temp dirs — the real cache is never touched. Run: python test_crossref.py"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from universe_explorer.data.registry import TOPICS
from universe_explorer.model import (
    Claim, ConditionAssessment, Evidence, Source, Status, Topic,
)
from universe_explorer.provenance import (
    CROSSREF_MANIFEST_PATH,
    doi_of,
    validate_provenance,
)

FAKE_DOI = "10.9999/fixture.123"
GOOD_JSON = json.dumps({"message": {"DOI": FAKE_DOI, "title": ["fixture"]}})
WRONG_JSON = json.dumps({"message": {"DOI": "10.9999/other.456"}})


def _topic_citing(ref: str) -> Topic:
    claim = Claim(
        id="fixture_claim", title="t", status=Status.SPECULATIVE,
        sources=[Source("SRC", ref, "peer-reviewed paper")],
        evidence=[Evidence("theoretical derivation", "d", "SRC")],
        status_reason=[ConditionAssessment("no_observational_evidence", True, "n")],
    )
    return Topic(id="fixture", title="t", summary="s", claims=[claim])


def _stage(json_text, manifest_sha=None, write_cache=True):
    tmp = Path(tempfile.mkdtemp())
    cache_file = tmp / "fake.json"
    if write_cache:
        cache_file.write_text(json_text, encoding="utf-8")
        sha = hashlib.sha256(cache_file.read_bytes()).hexdigest()
    else:
        sha = "0" * 64
    (tmp / "manifest.json").write_text(json.dumps({FAKE_DOI: {
        "endpoint": "https://example.invalid", "retrieved_at": "2026-07-10",
        "cache_file": "fake.json", "sha256": manifest_sha or sha,
    }}), encoding="utf-8")
    return tmp / "manifest.json"


def _rules(topic, cross_mpath) -> set:
    # point the arXiv manifest at an empty temp path so only DOI rules fire
    empty = Path(tempfile.mkdtemp()) / "manifest.json"
    return {v.rule for v in validate_provenance(topic, empty, cross_mpath)}


def test_real_data_passes():
    for t in TOPICS:
        assert [v for v in validate_provenance(t)
                if v.rule.startswith("doi_")] == [], t.id


def test_cite_without_fetch():
    topic = _topic_citing("doi:10.9999/never.fetched")
    assert "doi_source_unfetched" in _rules(topic, _stage(GOOD_JSON))


def test_cache_file_missing():
    topic = _topic_citing(f"doi:{FAKE_DOI}")
    assert "doi_cache_missing" in _rules(topic, _stage(GOOD_JSON, write_cache=False))


def test_cache_tampered_hash_mismatch():
    topic = _topic_citing(f"doi:{FAKE_DOI}")
    assert "doi_hash_mismatch" in _rules(topic, _stage(GOOD_JSON, manifest_sha="a" * 64))


def test_manifest_points_at_wrong_work():
    topic = _topic_citing(f"doi:{FAKE_DOI}")
    assert "doi_id_mismatch" in _rules(topic, _stage(WRONG_JSON))


def test_doi_case_insensitive():
    assert doi_of("doi:10.1038/S41586-018-0006-5") == "10.1038/s41586-018-0006-5"
    assert doi_of("arXiv:1601.05438") is None
    assert doi_of("Nature 378, 355-359 (1995)") is None


def test_non_doi_sources_still_exempt():
    topic = _topic_citing("Commun. Math. Phys. 43, 199 (1975)")
    assert _rules(topic, _stage(GOOD_JSON)) == set()


def test_real_manifest_covers_all_cited_dois():
    manifest = json.loads(CROSSREF_MANIFEST_PATH.read_text(encoding="utf-8"))
    cited = {doi_of(s.url_or_id) for t in TOPICS for c in t.claims
             for s in c.sources if doi_of(s.url_or_id)}
    assert cited <= set(manifest), cited - set(manifest)


def _run():
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
            passed += 1
    print(f"\n{passed} tests passed.")


if __name__ == "__main__":
    _run()
