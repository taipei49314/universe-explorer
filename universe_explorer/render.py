"""Minimal static-HTML renderer (spec section 5, last bullet).

Deliberately plain. The point is not visual polish but that the *shape of
knowledge* is visible at a glance: which parts are bedrock, which are still
being felt out. Claims are laid out bedrock-first (Established) to ceiling
(Speculative). Everything below the headline light is collapsed into <details>
so the reader expands the evidence and counts the open questions themselves —
no numbers are pre-counted for them.

No AI narrative is generated in v0: the page shows only recorded, sourced
structure. That keeps the page inside the constitution (AI may not declare
facts) without needing a narrative layer yet.
"""

from __future__ import annotations

import html
from typing import List

from .axes import EvidenceStrength, derive, diverges
from .model import Claim, Status, Topic
from .narrative import narrate

_LIGHT_COLOR = {
    Status.ESTABLISHED: "#2e7d32",
    Status.STRONG: "#1565c0",
    Status.COMPETING: "#f9a825",
    Status.FRONTIER: "#ef6c00",
    Status.SPECULATIVE: "#c62828",
}


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _legend() -> str:
    items = []
    for st in Status:
        items.append(
            f'<span class="chip" style="border-color:{_LIGHT_COLOR[st]}">'
            f'{st.light} {_esc(st.value)}</span>'
        )
    return '<div class="legend">' + " ".join(items) + "</div>"


def _claim_html(claim: Claim) -> str:
    color = _LIGHT_COLOR[claim.status]
    derivation = derive(claim)
    parts = [f'<article class="claim" style="border-left-color:{color}">']
    diverge_badge = (
        '<span class="diverge" title="high consensus resting on non-direct '
        'evidence — the two axes point apart">⚡ axes diverge</span>'
        if diverges(claim) else ""
    )
    parts.append(
        f'<div class="claim-head">'
        f'<span class="light">{claim.status.light}</span>'
        f'<div><h3>{_esc(claim.title)}</h3>'
        f'<span class="status" style="color:{color}">{_esc(claim.status.value)}'
        f'</span> <span class="axis-badge">'
        f'{_esc(derivation.strength.short)} · '
        f'{_esc(derivation.strength.value)}</span> {diverge_badge}'
        f'<code class="cid">{_esc(claim.id)}</code></div></div>'
    )

    # evidence axis — derived, never declared; the derivation is expandable so
    # a third party can recompute it from the public rules and overturn it.
    deriv_rows = "".join(f"<li>{_esc(r)}</li>" for r in derivation.reasoning)
    parts.append(
        '<details><summary>Evidence axis (derived from the recorded evidence '
        '&mdash; nobody fills this in)</summary>'
        f'<ul class="derivation">{deriv_rows}</ul></details>'
    )

    # status_reason — the traceable justification, condition by condition.
    reason_rows = []
    for ca in claim.status_reason:
        mark = "✓" if ca.holds else "✗"
        reason_rows.append(
            f'<li><span class="cond">{mark} {_esc(ca.condition)}</span>'
            f'<span class="note">{_esc(ca.note)}</span></li>'
        )
    parts.append(
        '<details open><summary>Why this light '
        '(status_reason &mdash; check it against the taxonomy)</summary>'
        f'<ul class="reasons">{"".join(reason_rows)}</ul></details>'
    )

    # evidence — Evidence layer, each with its source ref.
    ev_rows = []
    for ev in claim.evidence:
        ev_rows.append(
            f'<li><span class="etype">{_esc(ev.type)}</span>'
            f'{_esc(ev.description)} '
            f'<span class="ref">[{_esc(ev.source_ref)}]</span></li>'
        )
    parts.append(
        f'<details><summary>Evidence ({_word(len(ev_rows), "item")})'
        f'</summary><ul class="evidence">{"".join(ev_rows)}</ul></details>'
    )

    # competing models — only when the light is Competing.
    if claim.competing_models:
        cm_rows = []
        for cm in claim.competing_models:
            cm_rows.append(
                f'<li><b>{_esc(cm.name)}</b>'
                f'<div class="cm-grid">'
                f'<span>for</span><span>{_esc(cm.supporting)}</span>'
                f'<span>against</span><span>{_esc(cm.opposing)}</span>'
                f'<span>limits</span><span>{_esc(cm.limitations)}</span>'
                f'</div></li>'
            )
        parts.append(
            '<details><summary>Competing models</summary>'
            f'<ul class="competing">{"".join(cm_rows)}</ul></details>'
        )

    # open questions — an expandable list; never a number.
    if claim.open_questions:
        oq_rows = "".join(f"<li>{_esc(q)}</li>" for q in claim.open_questions)
        parts.append(
            '<details><summary>Open questions '
            '(expand and count them yourself)</summary>'
            f'<ul class="open">{oq_rows}</ul></details>'
        )

    # AI narrative — the bottom layer: organised from records, never beyond
    # them; each sentence shows the refs it hangs on. Withheld entirely if the
    # narrative gate rejects it.
    sentences = narrate(claim)
    if sentences:
        n_rows = "".join(
            f'<li>{_esc(s.text)} <span class="ref">'
            f'[{_esc(", ".join(s.refs))}]</span></li>'
            for s in sentences
        )
        parts.append(
            '<details><summary>AI narrative &mdash; organised from recorded '
            'evidence, never beyond it (every sentence carries its refs)'
            f'</summary><ul class="narrative">{n_rows}</ul></details>'
        )

    # sources — Data layer.
    src_rows = []
    for s in claim.sources:
        src_rows.append(
            f'<li><b>{_esc(s.label)}</b> &mdash; {_esc(s.url_or_id)} '
            f'<span class="kind">({_esc(s.kind)})</span></li>'
        )
    parts.append(
        f'<details><summary>Sources ({_word(len(src_rows), "source")})'
        f'</summary><ul class="sources">{"".join(src_rows)}</ul></details>'
    )

    # status history — kept for the future push trigger.
    if claim.status_history:
        hist = "".join(
            f'<li>{_esc(h.date)}: {_esc(h.from_status)} &rarr; '
            f'{_esc(h.to_status)} &mdash; {_esc(h.trigger)}</li>'
            for h in claim.status_history
        )
        parts.append(
            '<details><summary>Status history</summary>'
            f'<ul class="history">{hist}</ul></details>'
        )

    parts.append("</article>")
    return "".join(parts)


def _word(n: int, noun: str) -> str:
    # A label such as "3 items" is a count of a *visible list the reader can
    # recount*, not a fabricated confidence number — allowed by the constitution.
    return f'{n} {noun}{"" if n == 1 else "s"}'


def render_topic(topic: Topic) -> str:
    claims = sorted(topic.claims, key=lambda c: c.status.rank)
    body = "".join(_claim_html(c) for c in claims)
    return _PAGE.format(
        title=_esc(topic.title),
        summary=_esc(topic.summary),
        nav='<a class="home" href="index.html">&larr; all topics</a>',
        legend=_legend(),
        body=body,
    )


def render_index(topics: List[Topic]) -> str:
    """The multi-topic landing page (P4). Each topic is a container with no
    light of its own; its claim lights are previewed so the knowledge shape is
    legible before you even open the topic."""
    cards = []
    for t in topics:
        claims = sorted(t.claims, key=lambda c: c.status.rank)
        dots = "".join(
            f'<span class="dot" style="color:{_LIGHT_COLOR[c.status]}" '
            f'title="{_esc(c.title)}">{c.status.light}</span>'
            for c in claims
        )
        cards.append(
            f'<a class="topic-card" href="{_esc(t.id)}.html">'
            f'<h2>{_esc(t.title)}</h2>'
            f'<div class="dots">{dots}</div>'
            f'<p>{_esc(t.summary)}</p></a>'
        )
    return _INDEX.format(legend=_legend(), cards="".join(cards))


_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe Explorer — {title}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.55 system-ui, sans-serif; max-width: 820px;
         margin: 0 auto; padding: 24px; }}
  header p {{ opacity: .8; }}
  .banner {{ font-size: .85em; opacity: .7; border: 1px dashed currentColor;
            padding: 8px 12px; border-radius: 6px; margin: 12px 0; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px; }}
  .chip {{ border: 1px solid; border-radius: 999px; padding: 2px 10px;
          font-size: .82em; }}
  .claim {{ border-left: 6px solid; padding: 4px 16px 8px; margin: 18px 0;
           background: color-mix(in srgb, currentColor 4%, transparent);
           border-radius: 0 8px 8px 0; }}
  .claim-head {{ display: flex; gap: 12px; align-items: flex-start; }}
  .light {{ font-size: 1.6em; line-height: 1; }}
  .claim h3 {{ margin: 2px 0 2px; }}
  .status {{ font-weight: 600; font-size: .9em; }}
  .axis-badge {{ font-size: .78em; border: 1px solid currentColor; opacity: .8;
                border-radius: 999px; padding: 1px 8px; margin-left: 6px; }}
  .diverge {{ font-size: .78em; font-weight: 700; border-radius: 999px;
             padding: 1px 8px; margin-left: 6px;
             background: color-mix(in srgb, currentColor 12%, transparent); }}
  .cid {{ opacity: .6; font-size: .82em; margin-left: 6px; }}
  details {{ margin: 8px 0; }}
  summary {{ cursor: pointer; font-weight: 600; font-size: .9em; }}
  ul {{ margin: 6px 0; padding-left: 18px; }}
  li {{ margin: 6px 0; }}
  .reasons .cond {{ display: block; font-weight: 600; }}
  .reasons .note {{ display: block; opacity: .82; font-size: .92em; }}
  .etype {{ display: inline-block; font-size: .72em; text-transform: uppercase;
           letter-spacing: .04em; opacity: .7; border: 1px solid currentColor;
           border-radius: 4px; padding: 0 5px; margin-right: 6px; }}
  .ref {{ font-size: .82em; opacity: .7; }}
  .kind {{ opacity: .65; font-size: .85em; }}
  .cm-grid {{ display: grid; grid-template-columns: auto 1fr; gap: 2px 10px;
             margin: 4px 0 0; font-size: .92em; }}
  .cm-grid span:nth-child(odd) {{ opacity: .6; text-transform: uppercase;
             font-size: .8em; }}
  code {{ font-family: ui-monospace, monospace; }}
  .home {{ font-size: .85em; opacity: .7; text-decoration: none; }}
</style>
</head>
<body>
<header>
  {nav}
  <h1>{title}</h1>
  <p>{summary}</p>
  <div class="banner">Reference first, AI last. Every claim below hangs on a
  recorded source; no confidence numbers are declared &mdash; certainty emerges
  from the evidence you can open and read.</div>
  {legend}
</header>
<main>
{body}
</main>
</body>
</html>
"""


_INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe Explorer</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.55 system-ui, sans-serif; max-width: 820px;
         margin: 0 auto; padding: 24px; }}
  header p {{ opacity: .8; }}
  .banner {{ font-size: .85em; opacity: .7; border: 1px dashed currentColor;
            padding: 8px 12px; border-radius: 6px; margin: 12px 0; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px; }}
  .chip {{ border: 1px solid; border-radius: 999px; padding: 2px 10px;
          font-size: .82em; }}
  .topic-card {{ display: block; text-decoration: none; color: inherit;
                border: 1px solid currentColor; border-radius: 10px;
                padding: 12px 18px; margin: 14px 0;
                background: color-mix(in srgb, currentColor 4%, transparent); }}
  .topic-card:hover {{ background: color-mix(in srgb, currentColor 9%, transparent); }}
  .topic-card h2 {{ margin: 0 0 4px; }}
  .dots {{ font-size: 1.3em; letter-spacing: 3px; margin-bottom: 4px; }}
  .topic-card p {{ margin: 0; opacity: .8; font-size: .92em; }}
</style>
</head>
<body>
<header>
  <h1>Universe Explorer</h1>
  <p>Honestly separating what we know from what we don't. A topic is only a
  container &mdash; it has no status light of its own; each claim inside carries
  its own. Same engine, any domain.</p>
  <div class="banner">Reference first, AI last. Certainty emerges from evidence
  you can open and read &mdash; never from a declared number.</div>
  {legend}
</header>
<main>
{cards}
</main>
</body>
</html>
"""
