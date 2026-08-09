"""P5b — optional transport for digests (webhook / SMTP).

Constitution:
  * The body sent is exactly the digest text from push.render_digest —
    restatement only, no urgency language injected by the transport layer.
  * No credentials are hardcoded. All endpoints come from environment variables.
  * If nothing is configured, transport is a no-op success with reason
    ``not_configured`` (silence is legal).
  * Dry-run never opens a network socket.

Environment:

  UE_WEBHOOK_URL          POST raw text/plain digest body
  UE_SMTP_HOST            SMTP hostname
  UE_SMTP_PORT            default 587
  UE_SMTP_USER / UE_SMTP_PASS
  UE_SMTP_FROM / UE_SMTP_TO
  UE_TRANSPORT_DRY_RUN=1  force dry-run even if URLs set

Usage (usually via push)::

    python -m universe_explorer.dataops.push --deliver
    python -m universe_explorer.dataops.transport --file outbox/....txt --dry-run
"""

from __future__ import annotations

import json
import os
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Dict, List, Optional

BANNED_BODY_WORDS = (
    "breakthrough", "urgent", "must act", "confidence%",
    "game-changer", "settled science",
)


def _env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


def validate_digest_body(text: str) -> List[str]:
    """Mechanical checks: digest must remain restatement-only."""
    bad: List[str] = []
    low = text.lower()
    for w in BANNED_BODY_WORDS:
        if w in low:
            bad.append(f"banned_phrase:{w}")
    if "confidence" in low and "%" in text:
        bad.append("banned_confidence_percent")
    if not text.strip():
        bad.append("empty_body")
    return bad


def deliver_webhook(
    body: str,
    url: str,
    *,
    dry_run: bool = False,
    timeout: float = 20.0,
) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "channel": "webhook",
        "url_host": urllib.request.urlparse(url).netloc,
        "bytes": len(body.encode("utf-8")),
        "dry_run": dry_run,
        "ok": False,
        "status": None,
        "error": None,
    }
    # never log full URL with secrets in query — host only
    if dry_run:
        result["ok"] = True
        result["status"] = "dry_run"
        return result
    req = urllib.request.Request(
        url,
        data=body.encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "User-Agent": "UniverseExplorer-transport/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result["status"] = getattr(resp, "status", 200)
            result["ok"] = 200 <= int(result["status"]) < 300
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["error"] = f"HTTPError {e.code}"
        result["ok"] = False
    except Exception as e:  # network errors — report, don't interpret science
        result["error"] = type(e).__name__
        result["ok"] = False
    return result


def deliver_smtp(
    body: str,
    *,
    host: str,
    port: int,
    user: str,
    password: str,
    mail_from: str,
    mail_to: str,
    subject: str = "Universe Explorer — change digest",
    dry_run: bool = False,
) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "channel": "smtp",
        "host": host,
        "port": port,
        "to": mail_to,
        "bytes": len(body.encode("utf-8")),
        "dry_run": dry_run,
        "ok": False,
        "error": None,
    }
    if dry_run:
        result["ok"] = True
        result["status"] = "dry_run"
        return result
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.ehlo()
            try:
                smtp.starttls()
                smtp.ehlo()
            except smtplib.SMTPException:
                pass  # some servers already TLS; mechanical try
            if user:
                smtp.login(user, password)
            smtp.send_message(msg)
        result["ok"] = True
        result["status"] = "sent"
    except Exception as e:
        result["error"] = type(e).__name__
        result["ok"] = False
    return result


def deliver_digest(
    body: str,
    *,
    dry_run: Optional[bool] = None,
) -> Dict[str, Any]:
    """Send digest on every configured channel. Returns a mechanical report."""
    if dry_run is None:
        dry_run = _env("UE_TRANSPORT_DRY_RUN") in ("1", "true", "yes")

    problems = validate_digest_body(body)
    report: Dict[str, Any] = {
        "kind": "transport_report",
        "ok": False,
        "configured": False,
        "dry_run": dry_run,
        "body_bytes": len(body.encode("utf-8")),
        "body_problems": problems,
        "channels": [],
    }
    if problems:
        report["error"] = "body_failed_constitution_check"
        return report

    webhook = _env("UE_WEBHOOK_URL")
    smtp_host = _env("UE_SMTP_HOST")

    if not webhook and not smtp_host:
        report["ok"] = True
        report["status"] = "not_configured"
        report["note"] = (
            "No UE_WEBHOOK_URL or UE_SMTP_HOST — transport silent "
            "(outbox files remain the interface)."
        )
        return report

    report["configured"] = True
    channels: List[Dict[str, Any]] = []

    if webhook:
        channels.append(deliver_webhook(body, webhook, dry_run=dry_run))

    if smtp_host:
        channels.append(deliver_smtp(
            body,
            host=smtp_host,
            port=int(_env("UE_SMTP_PORT", "587") or "587"),
            user=_env("UE_SMTP_USER"),
            password=_env("UE_SMTP_PASS"),
            mail_from=_env("UE_SMTP_FROM") or _env("UE_SMTP_USER"),
            mail_to=_env("UE_SMTP_TO"),
            dry_run=dry_run,
        ))

    report["channels"] = channels
    report["ok"] = all(c.get("ok") for c in channels)
    return report


def main(argv: Optional[List[str]] = None) -> int:
    import argparse
    p = argparse.ArgumentParser(description="Deliver a digest file (P5b)")
    p.add_argument("--file", type=Path, required=True, help="path to digest .txt")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    body = args.file.read_text(encoding="utf-8")
    report = deliver_digest(body, dry_run=args.dry_run or None)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"configured={report.get('configured')} ok={report.get('ok')} "
              f"status={report.get('status') or report.get('error')}")
        for c in report.get("channels") or []:
            print(f"  {c.get('channel')}: ok={c.get('ok')} "
                  f"status={c.get('status')} err={c.get('error')}")
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
