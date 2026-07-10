"""D3 — the push channel goes public: an Atom feed of change events.

No credentials, no mail server, no webhook endpoint: the feed is a static file
on the site and ANY feed reader can subscribe. The digest constitution applies
unchanged — every entry is a mechanical restatement of recorded state changes
(before/after values), never an interpretation, and each entry names the event
file that carries the derivation back to the evidence.

build.py calls build_feed() and writes dist/feed.xml.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import List

from ..watch import EVENTS_DIR
from .push import _KIND_TEXT

SITE = "https://taipei49314.github.io/universe-explorer/"


def _entry_lines(events: List[dict]) -> List[str]:
    lines = []
    for e in events:
        kind = _KIND_TEXT.get(e["kind"], e["kind"])
        if e["kind"] == "claim_added":
            a = e["after"]
            lines.append(f"{e['claim']}: {kind} — status {a['status']}, "
                         f"evidence axis {a['evidence_axis']}")
        elif "before" in e and "after" in e:
            lines.append(f"{e['claim']}: {kind} — "
                         f"{e['before']!r} -> {e['after']!r}")
        else:
            lines.append(f"{e['claim']}: {kind}")
    return lines


def build_feed(events_dir: Path = EVENTS_DIR, site: str = SITE) -> str:
    files = sorted(events_dir.glob("*-events.json")) if events_dir.exists() else []
    entries = []
    latest = "1970-01-01T00:00:00Z"

    for ef in reversed(files):  # newest first
        payload = json.loads(ef.read_text(encoding="utf-8"))
        stamp = payload["at"]  # e.g. 20260710T092422Z
        iso = (f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}"
               f"T{stamp[9:11]}:{stamp[11:13]}:{stamp[13:15]}Z")
        latest = max(latest, iso)
        lines = _entry_lines(payload["events"])
        body = html.escape("\n".join("* " + l for l in lines))
        n = len(payload["events"])
        entries.append(
            f"<entry>"
            f"<title>{n} recorded change{'s' if n != 1 else ''} "
            f"({html.escape(iso)})</title>"
            f"<id>{site}feed#{html.escape(ef.stem)}</id>"
            f"<updated>{iso}</updated>"
            f"<link href=\"{site}explore.html\"/>"
            f"<content type=\"text\">mechanical restatement of recorded "
            f"state changes (event file: {html.escape(ef.name)}; the file "
            f"carries the derivation back to the evidence)\n{body}</content>"
            f"</entry>")

    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        f"<title>Universe Explorer — change feed</title>\n"
        f"<subtitle>Knowledge may move, never silently. Every entry restates "
        f"recorded state changes; nothing here interprets.</subtitle>\n"
        f"<id>{site}feed.xml</id>\n"
        f"<link href=\"{site}feed.xml\" rel=\"self\"/>\n"
        f"<link href=\"{site}\"/>\n"
        f"<updated>{latest}</updated>\n"
        f"<author><name>Universe Explorer engine</name></author>\n"
        + "\n".join(entries) + "\n</feed>\n")
