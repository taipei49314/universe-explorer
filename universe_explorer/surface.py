"""Product surface pages: health (P-Audit) + changes (P-Pulse).

Mechanical inventories only — counts, ids, file names. No confidence.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, List, Sequence

from .challenge_ops import trust_loop_inventory
from .data.registry import TOPICS
from .model import Status, Topic
from .relations import relations_payload
from .watch import EVENTS_DIR

ROOT = Path(__file__).resolve().parent.parent
OUTBOX = ROOT / "outbox"
BANNED = frozenset({"confidence", "score", "probability", "certainty", "trust"})


def _esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def sample_claims(topics: Sequence[Topic], *, n: int = 3, day: str | None = None) -> List[dict]:
    """Deterministic daily sample for public audit (not random trust)."""
    day = day or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    all_c = [(t.id, c) for t in topics for c in t.claims]
    if not all_c:
        return []
    # stable shuffle via hash
    ranked = sorted(
        all_c,
        key=lambda tc: hashlib.sha256(f"{day}:{tc[1].id}".encode()).hexdigest(),
    )
    out = []
    for tid, c in ranked[:n]:
        out.append({
            "id": c.id,
            "topic": tid,
            "title": c.title,
            "status": c.status.name,
            "status_light": c.status.light,
            "n_sources": len(c.sources),
            "source_labels": [s.label for s in c.sources[:6]],
            "permalink": f"{tid}.html#c-{c.id}",
            "map_link": f"app.html?c={c.id}",
        })
    return out


def health_payload(topics: Sequence[Topic] | None = None) -> dict:
    topics = list(topics if topics is not None else TOPICS)
    rel = relations_payload(topics)
    cov = rel["coverage"]
    by_topic = {}
    for t in topics:
        lights = {
            st.name: sum(1 for c in t.claims if c.status == st)
            for st in Status
        }
        by_topic[t.id] = {
            "n_claims": len(t.claims),
            "lights": {k: v for k, v in lights.items() if v},
        }

    payload = {
        "kind": "site_health",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_topics": len(topics),
        "n_claims": sum(len(t.claims) for t in topics),
        "n_authored_links": rel["n_authored"],
        "n_mechanical_links": rel["n_mechanical"],
        "n_reading_paths": len(rel["reading_paths"]),
        "coverage": cov,
        "by_topic": by_topic,
        "audit_sample": sample_claims(topics, n=3),
        "trust_loop": trust_loop_inventory(),
        "note": (
            "Mechanical inventory for third-party audit. "
            "Counts are list counts — recount them yourself. "
            "Challenge lights and edges on GitHub. "
            "trust_loop panel: closed records + weeklies + candidate counts "
            "(no confidence)."
        ),
        "links": {
            "map": "app.html",
            "constitution": "https://github.com/taipei49314/universe-explorer/blob/main/docs/constitution.md",
            "claims_json": "claims.json",
            "feed": "feed.xml",
            "challenge_verdict": (
                "https://github.com/taipei49314/universe-explorer/issues/new"
                "?template=challenge-a-verdict.yml"
            ),
            "challenge_edge": (
                "https://github.com/taipei49314/universe-explorer/issues/new"
                "?template=challenge-a-relation.yml"
            ),
            "challenge_records": (
                "https://github.com/taipei49314/universe-explorer/tree/main/docs/challenges"
            ),
            "weeklies": (
                "https://github.com/taipei49314/universe-explorer/tree/main/docs/weeklies"
            ),
        },
    }
    assert not (set(payload) & BANNED)
    return payload


def _render_trust_loop_section(tl: dict, links: dict) -> str:
    """TL-2: pending is GitHub; closed records + weeklies + candidates are local counts."""
    recs = tl.get("challenge_records") or []
    if recs:
        rows = "".join(
            f"<tr><td><code>{_esc(r.get('claim_id', ''))}</code></td>"
            f"<td>{_esc(r.get('verdict', ''))}</td>"
            f"<td>{_esc(r.get('issue', ''))}</td>"
            f"<td><code>{_esc(r.get('file', ''))}</code></td>"
            f"<td>{_esc(r.get('date', ''))}</td></tr>"
            for r in recs
        )
        table = (
            "<table><tr><th>Claim</th><th>Verdict</th><th>Issue</th>"
            f"<th>Record</th><th>Date</th></tr>{rows}</table>"
        )
    else:
        table = (
            "<p><b>No closed challenge records yet.</b> "
            "Open a challenge, then write <code>docs/challenges/*.md</code>.</p>"
        )
    cands = tl.get("candidates") or {}
    latest_w = tl.get("latest_weekly") or "—"
    gh = _esc(tl.get("github_challenge_label") or links.get("challenge_verdict", "#"))
    rec_link = _esc(links.get("challenge_records", "#"))
    week_link = _esc(links.get("weeklies", "#"))
    return f"""
<h2 id="trust-loop">Trust Loop (overturn panel)</h2>
<p class="note">{_esc(tl.get("note", ""))}</p>
<ul>
  <li>Closed challenge records: <b>{tl.get("n_challenge_records", 0)}</b>
      (reject: <b>{tl.get("n_verdict_reject", 0)}</b>
      · accept: <b>{tl.get("n_verdict_accept", 0)}</b>)</li>
  <li>Open / labeled challenges: see
      <a href="{gh}">GitHub label <code>challenge</code></a>
      (live issue tracker — not a local score)</li>
  <li>Weeklies: <b>{tl.get("n_weeklies", 0)}</b>
      · latest: <code>{_esc(str(latest_w))}</code>
      · <a href="{week_link}">docs/weeklies/</a></li>
  <li>Candidates pending: <b>{cands.get("n_pending", 0)}</b>
      · rejected archive: <b>{cands.get("n_rejected_archived", 0)}</b>
      (process ≤3/week or legal silence)</li>
  <li>Records dir:
      <a href="{rec_link}">docs/challenges/</a></li>
</ul>
{table}
"""


def render_health_html(payload: dict) -> str:
    sample_rows = "".join(
        f"<tr><td>{_esc(s['status_light'])} <code>{_esc(s['id'])}</code></td>"
        f"<td>{_esc(s['title'][:80])}</td>"
        f"<td>{s['n_sources']} sources</td>"
        f"<td><a href=\"{_esc(s['map_link'])}\">map</a> · "
        f"<a href=\"{_esc(s['permalink'])}\">page</a></td></tr>"
        for s in payload.get("audit_sample") or []
    )
    topic_rows = "".join(
        f"<tr><td><code>{_esc(tid)}</code></td><td>{b['n_claims']}</td>"
        f"<td>{_esc(json.dumps(b.get('lights') or {}, ensure_ascii=False))}</td></tr>"
        for tid, b in (payload.get("by_topic") or {}).items()
    )
    cov = payload.get("coverage") or {}
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe Explorer — Site health</title>
<style>
body {{ font: 15px/1.55 system-ui, sans-serif; max-width: 820px; margin: 0 auto; padding: 24px; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: .92rem; }}
td, th {{ border-bottom: 1px solid #ddd; padding: 6px 8px; text-align: left; vertical-align: top; }}
code {{ font-size: .85em; }}
.nav a {{ margin-right: 12px; }}
.note {{ opacity: .75; font-size: .88rem; }}
h1 {{ margin-bottom: 4px; }}
</style>
</head>
<body>
<p class="nav">
  <a href="app.html">Map</a>
  <a href="dashboard.html">Dashboard</a>
  <a href="explore-v2.html">Search</a>
  <a href="epistemic_map.html">Cross-domain</a>
  <a href="challenge.html">Challenge</a>
  <a href="changes.html">Changes</a>
  <a href="about.html">How to read</a>
  <a href="feed.xml">Feed</a>
  <a href="stats.json">stats.json</a>
  <a href="health.json">health.json</a>
</p>
<h1>Site health</h1>
<p class="note">{_esc(payload.get("note", ""))}</p>
<p>Generated (UTC): <code>{_esc(payload.get("generated_at", ""))}</code></p>
<ul>
  <li>Topics: <b>{payload.get("n_topics")}</b></li>
  <li>Claims: <b>{payload.get("n_claims")}</b></li>
  <li>Authored edges: <b>{payload.get("n_authored_links")}</b>
      · mechanical: <b>{payload.get("n_mechanical_links")}</b></li>
  <li>Reading paths: <b>{payload.get("n_reading_paths")}</b></li>
  <li>Claims with authored edge: <b>{cov.get("n_with_authored_edge")}</b>
      / {cov.get("n_claims")}
      · isolated (authored): <b>{cov.get("n_isolated_authored")}</b></li>
</ul>
{_render_trust_loop_section(payload.get("trust_loop") or {}, payload.get("links") or {})}
<h2>Today's audit sample (3 claims)</h2>
<p class="note">Deterministic sample for the UTC date — recount sources yourself.</p>
<table>
<tr><th>Claim</th><th>Title</th><th>Sources</th><th>Open</th></tr>
{sample_rows}
</table>
<h2>By domain</h2>
<table>
<tr><th>Topic</th><th>n</th><th>Lights present</th></tr>
{topic_rows}
</table>
<h2>Challenge</h2>
<ul>
  <li><a href="{_esc(payload["links"]["challenge_verdict"])}">Challenge a verdict</a></li>
  <li><a href="{_esc(payload["links"]["challenge_edge"])}">Challenge a relation edge</a></li>
  <li><a href="{_esc(payload["links"]["constitution"])}">Constitution</a></li>
</ul>
</body>
</html>
"""


def list_recent_digests(limit: int = 12) -> List[dict]:
    if not OUTBOX.exists():
        return []
    files = sorted(OUTBOX.glob("*-digest.txt"), reverse=True)[:limit]
    rows = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        rows.append({
            "name": f.name,
            "bytes": f.stat().st_size,
            "preview": "\n".join(lines[:12]),
        })
    return rows


def list_recent_events(limit: int = 8) -> List[dict]:
    if not EVENTS_DIR.exists():
        return []
    files = sorted(EVENTS_DIR.glob("*-events.json"), reverse=True)[:limit]
    rows = []
    for f in files:
        try:
            payload = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        rows.append({
            "name": f.name,
            "at": payload.get("at", ""),
            "n_events": len(payload.get("events") or []),
            "kinds": sorted({e.get("kind", "?") for e in (payload.get("events") or [])}),
        })
    return rows


def render_changes_html() -> str:
    digests = list_recent_digests()
    events = list_recent_events()
    tl = trust_loop_inventory()
    if digests:
        d_html = "".join(
            f"<section><h3><code>{_esc(d['name'])}</code> "
            f"({d['bytes']} bytes)</h3>"
            f"<pre>{_esc(d['preview'])}</pre></section>"
            for d in digests
        )
    else:
        d_html = (
            "<p><b>No digests in outbox yet.</b> "
            "That is legal silence — run "
            "<code>python -m universe_explorer.dataops.push</code> after events, "
            "or wait for the weekly workflow.</p>"
        )
    if events:
        e_html = "<ul>" + "".join(
            f"<li><code>{_esc(e['name'])}</code> — {_esc(e.get('at', ''))} — "
            f"{e['n_events']} event(s): {_esc(', '.join(e.get('kinds') or []))}</li>"
            for e in events
        ) + "</ul>"
    else:
        e_html = "<p>No event files found.</p>"

    # TL-2/TL-3: overturn + weekly ritual surface (counts only)
    recs = tl.get("challenge_records") or []
    if recs:
        ch_html = "<ul>" + "".join(
            f"<li><code>{_esc(r['claim_id'])}</code> — "
            f"<b>{_esc(r['verdict'])}</b> {_esc(r.get('issue', ''))} "
            f"(<code>{_esc(r['file'])}</code>)</li>"
            for r in recs
        ) + "</ul>"
    else:
        ch_html = (
            "<p>No closed challenge records. "
            "A quiet channel here is not a trust score — "
            "open a challenge or keep legal silence in weeklies.</p>"
        )
    weeks = tl.get("weeklies") or []
    if weeks:
        w_html = "<ul>" + "".join(
            f"<li><code>{_esc(w['file'])}</code>"
            f"{' · legal silence' if w.get('legal_silence') else ''}"
            f"{' · mentions challenge' if w.get('mentions_challenge') else ''}"
            f"</li>"
            for w in weeks
        ) + "</ul>"
    else:
        w_html = (
            "<p><b>No weeklies yet.</b> "
            "Write <code>docs/weeklies/YYYY-Www.md</code> — "
            "either work done (≤3 candidates) or <b>legal silence</b>.</p>"
        )
    cands = tl.get("candidates") or {}

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe Explorer — Changes</title>
<style>
body {{ font: 15px/1.55 system-ui, sans-serif; max-width: 820px; margin: 0 auto; padding: 24px; }}
pre {{ background: #f4f4f5; padding: 12px; overflow: auto; font-size: .78rem;
  border-radius: 8px; white-space: pre-wrap; }}
@media (prefers-color-scheme: dark) {{
  pre {{ background: #1c1c1e; }}
}}
.nav a {{ margin-right: 12px; }}
.note {{ opacity: .75; font-size: .88rem; }}
</style>
</head>
<body>
<p class="nav">
  <a href="app.html">Map</a>
  <a href="health.html">Health</a>
  <a href="health.html#trust-loop">Trust Loop</a>
  <a href="about.html">How to read</a>
  <a href="feed.xml">Atom feed</a>
  <a href="challenge.html">Challenge</a>
</p>
<h1>Changes</h1>
<p class="note">Mechanical restatement of recorded state changes. Digests do not
interpret science. If nothing changed, the channel stays silent — that is a feature
(<b>legal silence</b>), not a confidence score.</p>

<h2 id="overturn">Closed challenges (overturn ledger)</h2>
<p class="note">Permanent records under <code>docs/challenges/</code>.
Open issues: <a href="{_esc(tl.get('github_challenge_label', '#'))}">label challenge</a>.</p>
{ch_html}

<h2 id="weeklies">Editorial weeklies</h2>
<p class="note">Ritual: process ≤3 candidates <b>or</b> record legal silence.
Latest: <code>{_esc(str(tl.get('latest_weekly') or '—'))}</code>.
Pending candidates: <b>{cands.get('n_pending', 0)}</b>.</p>
{w_html}

<h2>Recent digests</h2>
{d_html}
<h2>Recent event files</h2>
{e_html}
<p class="note">Subscribe: <a href="feed.xml">feed.xml</a>. Optional webhook:
see <code>docs/operations.md</code> (UE_WEBHOOK_URL).</p>
</body>
</html>
"""


def write_surface_pages(out_dir: Path, topics: Sequence[Topic] | None = None) -> None:
    topics = list(topics if topics is not None else TOPICS)
    health = health_payload(topics)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "health.json").write_text(
        json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "health.html").write_text(render_health_html(health), encoding="utf-8")
    (out_dir / "changes.html").write_text(render_changes_html(), encoding="utf-8")
