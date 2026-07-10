"""Generate the single-file Artifact page for claude.ai hosting.

Reads the real topic registry (same data, same derivations) and emits one
self-contained HTML body — no doctype/html/head/body wrapper, all CSS inline,
token-level theming for light/dark. Run:

    python dataops_artifact.py <output_path> [en|zh]

The Chinese build is a *view overlay* (data/translations_zh.py): it never
touches the engine or authored data, keeps every identifier (DOI, arXiv id,
source label, claim id) in the original, and falls back to English on any
missing translation — so a gap degrades visibly, never fabricates.
"""

from __future__ import annotations

import html
import sys

from universe_explorer.axes import derive, diverges
from universe_explorer.data import translations_zh as ZH
from universe_explorer.data.registry import TOPICS
from universe_explorer.model import Status
from universe_explorer.narrative import narrate

E = lambda s: html.escape(str(s), quote=True)

LANG = "en"  # set by build()


def zh_active() -> bool:
    return LANG == "zh"

ST_TOKEN = {
    Status.ESTABLISHED: "est",
    Status.STRONG: "strong",
    Status.COMPETING: "comp",
    Status.FRONTIER: "front",
    Status.SPECULATIVE: "spec",
}

CSS = """
:root {
  --bg: #F4F6F3; --panel: #FDFDFB; --ink: #1B2320; --muted: #5A665F;
  --line: #D5DCD6; --accent: #2E6E5E; --mono-bg: #EBEFEA;
  --st-est: #2F7D46; --st-strong: #2762A8; --st-comp: #A67C0F;
  --st-front: #B85C1E; --st-spec: #A83232;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #131917; --panel: #1A211E; --ink: #D7DED9; --muted: #8FA097;
    --line: #2C3630; --accent: #6FB5A3; --mono-bg: #222B26;
    --st-est: #62BE7C; --st-strong: #6FA8E8; --st-comp: #D9B04A;
    --st-front: #E08A50; --st-spec: #E07070;
  }
}
:root[data-theme="dark"] {
  --bg: #131917; --panel: #1A211E; --ink: #D7DED9; --muted: #8FA097;
  --line: #2C3630; --accent: #6FB5A3; --mono-bg: #222B26;
  --st-est: #62BE7C; --st-strong: #6FA8E8; --st-comp: #D9B04A;
  --st-front: #E08A50; --st-spec: #E07070;
}
:root[data-theme="light"] {
  --bg: #F4F6F3; --panel: #FDFDFB; --ink: #1B2320; --muted: #5A665F;
  --line: #D5DCD6; --accent: #2E6E5E; --mono-bg: #EBEFEA;
  --st-est: #2F7D46; --st-strong: #2762A8; --st-comp: #A67C0F;
  --st-front: #B85C1E; --st-spec: #A83232;
}
body { background: var(--bg); color: var(--ink);
  font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
  margin: 0; padding: 0 20px 80px; }
.wrap { max-width: 780px; margin: 0 auto; }
h1, h2, h3 { font-family: Georgia, "Times New Roman", "Songti SC",
  "Noto Serif CJK TC", "Source Han Serif TC", serif;
  font-weight: 500; text-wrap: balance; }
h1 { font-size: 2rem; margin: 40px 0 6px; }
h2 { font-size: 1.5rem; margin: 0 0 4px; }
h3 { font-size: 1.08rem; margin: 0 0 2px; }
.sub { color: var(--muted); margin: 0 0 18px; }
.charter { border: 1px solid var(--line); border-left: 3px solid var(--accent);
  background: var(--panel); padding: 12px 16px; border-radius: 4px;
  font-size: .88rem; color: var(--muted); margin: 20px 0; }
nav { display: flex; flex-wrap: wrap; gap: 10px; margin: 22px 0 8px; }
nav a { text-decoration: none; color: var(--ink); font-size: .85rem;
  border: 1px solid var(--line); background: var(--panel);
  border-radius: 999px; padding: 5px 14px; }
nav a:hover { border-color: var(--accent); }
nav a .lights { letter-spacing: 2px; margin-left: 6px; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 12px 0 36px;
  font-size: .78rem; color: var(--muted); text-transform: uppercase;
  letter-spacing: .06em; }
.legend b { font-weight: 600; }
section.topic { margin: 52px 0 0; }
.topic-head { border-bottom: 1px solid var(--line); padding-bottom: 12px;
  margin-bottom: 6px; }
.topic-head p { color: var(--muted); font-size: .92rem; margin: 6px 0 0; }
article { background: var(--panel); border: 1px solid var(--line);
  border-left: 4px solid var(--stc); border-radius: 4px;
  padding: 14px 18px 10px; margin: 18px 0; }
.head { display: flex; gap: 12px; align-items: baseline; flex-wrap: wrap; }
.dot { width: 12px; height: 12px; border-radius: 50%; background: var(--stc);
  display: inline-block; flex: none; transform: translateY(1px); }
.meta { display: flex; gap: 8px; flex-wrap: wrap; align-items: center;
  margin: 4px 0 10px; }
.status { color: var(--stc); font-weight: 600; font-size: .82rem;
  text-transform: uppercase; letter-spacing: .05em; }
.badge, .cid { font-family: ui-monospace, "Cascadia Mono", Consolas, monospace;
  font-size: .74rem; background: var(--mono-bg); border-radius: 3px;
  padding: 2px 7px; color: var(--muted); }
.diverge { font-size: .74rem; font-weight: 700; color: var(--st-comp);
  border: 1px solid var(--st-comp); border-radius: 3px; padding: 1px 7px; }
details { border-top: 1px dashed var(--line); }
summary { cursor: pointer; font-size: .82rem; font-weight: 600;
  color: var(--muted); padding: 8px 0; text-transform: uppercase;
  letter-spacing: .05em; list-style-position: inside; }
summary:hover { color: var(--accent); }
summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
details ul { margin: 0 0 12px; padding-left: 20px; display: grid; gap: 8px;
  font-size: .92rem; }
.k { font-family: ui-monospace, Consolas, monospace; font-size: .78rem;
  color: var(--accent); }
.note { color: var(--muted); }
.ref { font-family: ui-monospace, Consolas, monospace; font-size: .74rem;
  color: var(--muted); }
.cmname { font-weight: 600; }
.cmrow { display: grid; grid-template-columns: 64px 1fr; gap: 2px 10px;
  font-size: .88rem; margin-top: 4px; }
.cmrow span:nth-child(odd) { color: var(--muted); font-size: .72rem;
  text-transform: uppercase; letter-spacing: .05em; padding-top: 2px; }
footer { margin-top: 60px; font-size: .8rem; color: var(--muted);
  border-top: 1px solid var(--line); padding-top: 14px; }
@media (prefers-reduced-motion: no-preference) {
  details[open] ul { animation: fade .18s ease; }
  @keyframes fade { from { opacity: 0 } to { opacity: 1 } }
}
"""


def _ct(claim_id):
    return ZH.CLAIMS.get(claim_id, {}) if zh_active() else {}


def _L(key, en):
    return ZH.CHROME[key] if zh_active() else en


def light_dots(topic) -> str:
    return "".join(
        f'<span style="color:var(--st-{ST_TOKEN[c.status]})">&#9679;</span>'
        for c in sorted(topic.claims, key=lambda c: c.status.rank))


def claim_html(c) -> str:
    tok = ST_TOKEN[c.status]
    d = derive(c)
    t = _ct(c.id)
    parts = [f'<article id="c-{E(c.id)}" style="--stc:var(--st-{tok})">']
    title = t.get("title", c.title)
    parts.append(f'<div class="head"><span class="dot"></span><h3>{E(title)}</h3></div>')

    status_txt = ZH.STATUS_ZH[c.status.value] if zh_active() else c.status.value
    axis_txt = ZH.AXIS_ZH[d.strength.short] if zh_active() else d.strength.value
    div_badge = (f'<span class="diverge" title="{E(_L("axes_diverge_title", "high consensus resting on non-direct evidence"))}">'
                 f'{E(_L("axes_diverge", "axes diverge"))}</span>' if diverges(c) else "")
    parts.append(
        f'<div class="meta"><span class="status">{E(status_txt)}</span>'
        f'<span class="badge">{E(d.strength.short)} &middot; {E(axis_txt)}</span>'
        f'{div_badge}<span class="cid">{E(c.id)}</span></div>')

    reasons_zh = t.get("reasons", {})
    rows = ""
    for ca in c.status_reason:
        cond = ZH.CONDITION_ZH[ca.condition] if zh_active() else ca.condition
        note = reasons_zh.get(ca.condition, ca.note)
        rows += (f'<li><span class="k">{"&#10003;" if ca.holds else "&#10007;"} '
                 f'{E(cond)}</span><br><span class="note">{E(note)}</span></li>')
    parts.append(f'<details open><summary>{E(_L("why_light", "Why this light"))}</summary><ul>{rows}</ul></details>')

    ev_zh = t.get("evidence", [])
    rows = ""
    for i, ev in enumerate(c.evidence):
        etype = ZH.EVIDENCE_TYPE_ZH[ev.type] if zh_active() else ev.type
        desc = ev_zh[i] if i < len(ev_zh) else ev.description
        rows += (f'<li><span class="k">{E(etype)}</span> {E(desc)} '
                 f'<span class="ref">[{E(ev.source_ref)}]</span></li>')
    parts.append(f'<details><summary>{E(_L("evidence", "Evidence"))}</summary><ul>{rows}</ul></details>')

    rows = "".join(f'<li>{E(r)}</li>' for r in d.reasoning)
    parts.append(f'<details><summary>{E(_L("evidence_axis", "Evidence axis &mdash; derived, not declared"))}'
                 f'</summary><ul>{rows}</ul></details>')

    if c.competing_models:
        cm_zh = t.get("competing", [])
        rows = ""
        for i, cm in enumerate(c.competing_models):
            z = cm_zh[i] if i < len(cm_zh) else {}
            rows += (
                f'<li><span class="cmname">{E(z.get("name", cm.name))}</span>'
                f'<div class="cmrow">'
                f'<span>{E(_L("cm_for", "for"))}</span><span>{E(z.get("for", cm.supporting))}</span>'
                f'<span>{E(_L("cm_against", "against"))}</span><span>{E(z.get("against", cm.opposing))}</span>'
                f'<span>{E(_L("cm_limits", "limits"))}</span><span>{E(z.get("limits", cm.limitations))}</span>'
                f'</div></li>')
        parts.append(f'<details><summary>{E(_L("competing", "Competing models"))}</summary><ul>{rows}</ul></details>')

    if c.open_questions:
        oq_zh = t.get("open_questions", [])
        qs = oq_zh if (zh_active() and oq_zh) else c.open_questions
        rows = "".join(f'<li>{E(q)}</li>' for q in qs)
        parts.append(f'<details><summary>{E(_L("open_questions", "Open questions &mdash; count them yourself"))}'
                     f'</summary><ul>{rows}</ul></details>')

    # AI narrative — Amendment #2: the zh narrative is composed through the
    # engine's Localization seam and passes the SAME check() court.
    loc = ZH.ZH_LOC if zh_active() else None
    sentences = narrate(c, loc) if loc else narrate(c)
    if sentences:
        rows = "".join(
            f'<li>{E(s.text)} <span class="ref">[{E(", ".join(s.refs))}]</span></li>'
            for s in sentences)
        parts.append(f'<details><summary>{E(_L("ai_narrative", "AI narrative &mdash; organised from records, never beyond them"))}'
                     f'</summary><ul>{rows}</ul></details>')

    rows = "".join(
        f'<li><span class="cmname">{E(s.label)}</span> &mdash; {E(s.url_or_id)} '
        f'<span class="note">({E(s.kind)})</span></li>' for s in c.sources)
    parts.append(f'<details><summary>{E(_L("sources", "Sources"))}</summary><ul>{rows}</ul></details>')

    if c.status_history:
        rows = "".join(
            f'<li>{E(h.date)}: {E(h.from_status)} &rarr; {E(h.to_status)} '
            f'&mdash; {E(h.trigger)}</li>' for h in c.status_history)
        parts.append(f'<details><summary>{E(_L("status_history", "Status history"))}</summary><ul>{rows}</ul></details>')

    parts.append("</article>")
    return "".join(parts)


def build(lang: str = "en") -> str:
    global LANG
    LANG = lang
    zh = zh_active()

    site = _L("site_title", "Universe Explorer")
    wrap_lang = ' lang="zh-Hant"' if zh else ""
    out = [f"<title>{E(site)}</title>", f"<style>{CSS}</style>",
           f'<div class="wrap"{wrap_lang}>']
    out.append(f'<h1>{E(site)}</h1>')
    out.append(f'<p class="sub">{_L("tagline", "Honestly separating what we know from what we don&rsquo;t &mdash; three domains, one engine.")}</p>')
    out.append(f'<div class="charter">{_L("charter", "Reference first, AI last. Every claim hangs on a recorded, verified source. No confidence numbers are declared &mdash; certainty emerges from evidence you can open and read. A topic is only a container: each claim carries its own status light.")}</div>')

    out.append("<nav>")
    for t in TOPICS:
        ttitle = ZH.TOPIC_ZH[t.id]["title"] if zh else t.title
        out.append(f'<a href="#{E(t.id)}">{E(ttitle)}'
                   f'<span class="lights">{light_dots(t)}</span></a>')
    out.append("</nav>")

    legend = " ".join(
        f'<span><b style="color:var(--st-{ST_TOKEN[s]})">&#9679;</b> '
        f'{E(ZH.STATUS_ZH[s.value] if zh else s.value)}</span>'
        for s in Status)
    out.append(f'<div class="legend">{legend}</div>')

    for t in TOPICS:
        ttitle = ZH.TOPIC_ZH[t.id]["title"] if zh else t.title
        tsum = ZH.TOPIC_ZH[t.id]["summary"] if zh else t.summary
        out.append(f'<section class="topic" id="{E(t.id)}">')
        out.append(f'<div class="topic-head"><h2>{E(ttitle)}</h2>'
                   f'<p>{E(tsum)}</p></div>')
        for c in sorted(t.claims, key=lambda c: c.status.rank):
            out.append(claim_html(c))
        out.append("</section>")

    out.append(f'<footer>{_L("footer", "Generated from the live data of the Universe Explorer engine &mdash; 12 claims, 3 domains, all sources real and verified. Lights belong to claims, never to topics.")}</footer>')
    out.append("</div>")
    return "\n".join(out)


if __name__ == "__main__":
    dest = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "en"
    with open(dest, "w", encoding="utf-8") as f:
        f.write(build(lang))
    print(f"artifact page ({lang}) -> {dest}")
