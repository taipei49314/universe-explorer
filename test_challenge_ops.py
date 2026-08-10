"""Trust Loop ops inventory tests. Run: python -m pytest test_challenge_ops.py -q"""

from __future__ import annotations

import json

from universe_explorer.challenge_ops import (
    candidate_counts,
    list_challenge_records,
    list_weeklies,
    trust_loop_inventory,
)


def test_at_least_one_challenge_record():
    recs = list_challenge_records()
    assert len(recs) >= 1
    hawking = [r for r in recs if r.claim_id == "hawking_radiation"]
    assert hawking
    assert hawking[0].verdict == "reject"
    assert "2" in hawking[0].issue


def test_at_least_one_weekly():
    weeks = list_weeklies()
    assert len(weeks) >= 1
    assert any(w["file"].startswith("2026-W") for w in weeks)


def test_inventory_no_banned_keys():
    inv = trust_loop_inventory()
    raw = json.dumps(inv)

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                assert k.lower() not in {
                    "confidence", "score", "probability", "certainty", "trust",
                }, k
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(inv)
    assert "n_challenge_records" in inv
    assert inv["n_challenge_records"] == len(inv["challenge_records"])


def test_candidate_counts_are_non_negative():
    c = candidate_counts()
    assert c["n_pending"] >= 0
    assert c["n_rejected_archived"] >= 0
    # S2 archived two files
    assert c["n_rejected_archived"] >= 2
