"""Product canonicals (v5 S3). Run: python -m pytest test_canonicals.py -q"""

from __future__ import annotations

from universe_explorer.canonicals import (
    CANONICALS,
    as_payload,
    canonical_claim_ids,
    canonical_path_ids,
)
from universe_explorer.data.registry import TOPICS
from universe_explorer.axes import diverges
from universe_explorer.relations import reading_paths
from universe_explorer.render import render_about, app_data_json
import json


def test_exactly_three_canonicals():
    assert len(CANONICALS) == 3
    assert as_payload()["n"] == 3


def test_claims_and_paths_exist():
    ids = {c.id for t in TOPICS for c in t.claims}
    paths = {p.id for p in reading_paths()}
    for cid in canonical_claim_ids():
        assert cid in ids, cid
    for pid in canonical_path_ids():
        assert pid in paths, pid


def test_hawking_diverges():
    h = next(c for t in TOPICS for c in t.claims if c.id == "hawking_radiation")
    assert diverges(h) is True


def test_about_and_app_data():
    en = render_about("en")
    zh = render_about("zh")
    assert 'id="canonicals"' in en and 'id="canonicals"' in zh
    for cid in canonical_claim_ids():
        assert cid in en and cid in zh
    data = json.loads(app_data_json(TOPICS))
    assert data["canonicals"]["n"] == 3
    assert "confidence" not in json.dumps(data["canonicals"]).split("note")[0]
