"""Proof the P1 Data-layer rules actually bite (P1 spec section 4.2).

All failure cases are staged inside a temp directory with fabricated fixtures —
the real cache is never touched or modified. Run: python test_provenance.py
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from universe_explorer.data.black_hole import BLACK_HOLE
from universe_explorer.model import Claim, ConditionAssessment, Evidence, Source, Status, Topic
from universe_explorer.provenance import (
    MANIFEST_PATH,
    arxiv_id_of,
    validate_provenance,
)

FAKE_ID = "1234.56789"

FAKE_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<feed xmlns="http://www.w3.org/2005/Atom">'
    '<entry><id>http://arxiv.org/abs/1234.56789v1</id>'
    '<title>fixture</title></entry></feed>'
)

WRONG_XML = FAKE_XML.replace("1234.56789", "9999.00000")


def _topic_citing(arxiv_ref: str) -> Topic:
    claim = Claim(
        id="fixture_claim", title="t", status=Status.SPECULATIVE,
        sources=[Source("SRC", arxiv_ref, "peer-reviewed paper")],
        evidence=[Evidence("theoretical derivation", "d", "SRC")],
        status_reason=[ConditionAssessment("no_observational_evidence", True, "n")],
    )
    return Topic(id="fixture", title="t", summary="s", claims=[claim])


def _stage(xml_text, manifest_sha=None, write_cache=True):
    """Build a temp cache dir + manifest; return its manifest path."""
    tmp = Path(tempfile.mkdtemp())
    cache_file = tmp / "fake.xml"
    if write_cache:
        cache_file.write_text(xml_text, encoding="utf-8")
        sha = hashlib.sha256(cache_file.read_bytes()).hexdigest()
    else:
        sha = "0" * 64
    manifest = {FAKE_ID: {
        "endpoint": "https://example.invalid/api",
        "retrieved_at": "2026-07-10T00:00:00Z",
        "cache_file": "fake.xml",
        "sha256": manifest_sha or sha,
    }}
    mpath = tmp / "manifest.json"
    mpath.write_text(json.dumps(manifest), encoding="utf-8")
    return mpath


def _rules(topic, mpath) -> set:
    return {v.rule for v in validate_provenance(topic, mpath)}


def test_real_data_passes():
    assert validate_provenance(BLACK_HOLE) == [], (
        "all cited arXiv sources must have verified provenance")


def test_cite_without_fetch():
    topic = _topic_citing("arXiv:0000.99999")  # never fetched
    mpath = _stage(FAKE_XML)
    assert "arxiv_source_unfetched" in _rules(topic, mpath)


def test_cache_file_missing():
    topic = _topic_citing(f"arXiv:{FAKE_ID}")
    mpath = _stage(FAKE_XML, write_cache=False)
    assert "provenance_cache_missing" in _rules(topic, mpath)


def test_cache_tampered_hash_mismatch():
    topic = _topic_citing(f"arXiv:{FAKE_ID}")
    mpath = _stage(FAKE_XML, manifest_sha="a" * 64)  # recorded hash差
    assert "provenance_hash_mismatch" in _rules(topic, mpath)


def test_manifest_points_at_wrong_content():
    # hash matches (manifest honestly records the wrong file's hash), but the
    # cached XML does not contain the cited paper -> independent re-parse catches it.
    topic = _topic_citing(f"arXiv:{FAKE_ID}")
    mpath = _stage(WRONG_XML)
    assert "provenance_id_mismatch" in _rules(topic, mpath)


def test_non_arxiv_sources_exempt():
    topic = _topic_citing("Commun. Math. Phys. 43, 199 (1975)")
    mpath = _stage(FAKE_XML)
    assert _rules(topic, mpath) == set(), "no endpoint => honestly exempt"


def test_old_style_id_recognised():
    assert arxiv_id_of("arXiv:hep-th/9306069") == "hep-th/9306069"
    assert arxiv_id_of("arXiv:1906.11238") == "1906.11238"
    assert arxiv_id_of("nobelprize.org/prizes/physics/2020") is None


def test_real_manifest_exists_for_all_cited():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cited = set()
    for c in BLACK_HOLE.claims:
        for s in c.sources:
            a = arxiv_id_of(s.url_or_id)
            if a:
                cited.add(a)
    assert cited <= set(manifest), f"missing fetch records: {cited - set(manifest)}"


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
