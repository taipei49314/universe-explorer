"""P5b transport acceptance. Run: python test_transport.py"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest import mock

from universe_explorer.dataops.transport import (
    deliver_digest,
    deliver_webhook,
    validate_digest_body,
)


CLEAN = (
    "UNIVERSE EXPLORER — change digest\n"
    "(mechanical restatement of recorded state changes; every line names "
    "its event file, which carries the derivation back to the evidence)\n\n"
    "== 2026-08-09T00:00:00Z  (fixture-events.json)\n"
    "  * firewall: status light moved — 'SPECULATIVE' -> 'FRONTIER'\n"
)


def test_validate_rejects_urgency_language():
    bad = CLEAN + "\nThis is a breakthrough! urgent action required.\n"
    problems = validate_digest_body(bad)
    assert any("banned" in p for p in problems)


def test_validate_accepts_clean_digest():
    assert validate_digest_body(CLEAN) == []


def test_not_configured_is_silent_ok():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("UE_")}
    with mock.patch.dict(os.environ, env, clear=True):
        r = deliver_digest(CLEAN, dry_run=False)
    assert r["ok"] is True
    assert r["status"] == "not_configured"
    assert r["configured"] is False
    assert r["channels"] == []


def test_webhook_dry_run_never_opens_socket():
    with mock.patch.dict(os.environ, {
        "UE_WEBHOOK_URL": "https://example.invalid/hook",
        "UE_TRANSPORT_DRY_RUN": "1",
    }, clear=False):
        with mock.patch("urllib.request.urlopen") as uo:
            r = deliver_digest(CLEAN, dry_run=True)
            uo.assert_not_called()
    assert r["ok"] is True
    assert r["configured"] is True
    assert r["channels"][0]["channel"] == "webhook"
    assert r["channels"][0]["status"] == "dry_run"


def test_webhook_posts_exact_body():
    captured = {}

    class Resp:
        status = 204
        def __enter__(self): return self
        def __exit__(self, *a): pass

    def fake_urlopen(req, timeout=20):
        captured["data"] = req.data
        captured["url"] = req.full_url
        captured["ctype"] = req.headers.get("Content-type") or req.headers.get(
            "Content-Type")
        return Resp()

    r = deliver_webhook(CLEAN, "https://example.invalid/hook", dry_run=False)
    # patch during call
    with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
        r = deliver_webhook(CLEAN, "https://example.invalid/hook", dry_run=False)
    assert r["ok"] is True
    assert captured["data"] == CLEAN.encode("utf-8")
    assert "text/plain" in (captured.get("ctype") or "")


def test_report_has_no_confidence_fields():
    r = deliver_digest(CLEAN, dry_run=True)
    blob = json.dumps(r)
    for banned in ("confidence", "probability", "certainty", "trust_score"):
        assert banned not in blob


def test_dirty_body_blocks_send():
    dirty = CLEAN + "\nbreakthrough announcement\n"
    with mock.patch.dict(os.environ, {
        "UE_WEBHOOK_URL": "https://example.invalid/hook",
    }, clear=False):
        r = deliver_digest(dirty, dry_run=True)
    assert r["ok"] is False
    assert r["body_problems"]


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
