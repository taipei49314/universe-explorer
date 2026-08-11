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
    # stable anchor: anyone can share exactly one claim (D2)
    parts = [f'<article class="claim" id="c-{_esc(claim.id)}" '
             f'style="border-left-color:{color}">']
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
        f'<code class="cid">{_esc(claim.id)}</code>'
        f'<a class="permalink" href="#c-{_esc(claim.id)}" '
        f'title="permanent link to this claim">&para;</a>'
        f'<a class="challenge-link" title="argue this light is wrong — the '
        f'whole point is that verdicts can be overturned" '
        f'href="https://github.com/taipei49314/universe-explorer/issues/new'
        f'?template=challenge-a-verdict.yml&title=%5Bchallenge%5D%20'
        f'{_esc(claim.id)}">challenge</a>'
        f' <a class="challenge-link" href="app.html?c={_esc(claim.id)}">'
        f'open in map</a></div></div>'
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

    # sources — Data layer. Tier chip = mechanical classification (Amend. #3).
    from .validator import tier_of
    src_rows = []
    for s in claim.sources:
        tier = tier_of(s.kind) or "?"
        src_rows.append(
            f'<li><b>{_esc(s.label)}</b> '
            f'<span class="tier">{_esc(tier)}</span> &mdash; '
            f'{_esc(s.url_or_id)} '
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


def render_explore(topics: List[Topic], lang: str = "en") -> str:
    """D2: one compact page over every claim in every domain, filterable by
    light and evidence axis, text-searchable. Pure static + vanilla JS, zero
    external resources. Counts shown are counts of a visible list the reader
    can recount — constitutional. Order is fixed: bedrock first, ceiling last.

    lang="zh" renders the Chinese presentation overlay (falls back to the
    authored English wherever a translation is missing — visible degradation,
    never fabrication) and points cards at the zh single-page anchors."""
    zh = lang == "zh"
    if zh:
        from .data import translations_zh as ZH

    cards = []
    for t in topics:
        t_title = ZH.TOPIC_ZH[t.id]["title"] if zh else t.title
        for c in sorted(t.claims, key=lambda c: c.status.rank):
            d = derive(c)
            div = ('<span class="diverge">⚡</span>' if diverges(c) else "")
            title = (ZH.CLAIMS.get(c.id, {}).get("title", c.title)
                     if zh else c.title)
            href = (f'zh.html#c-{_esc(c.id)}' if zh
                    else f'{_esc(t.id)}.html#c-{_esc(c.id)}')
            search_text = " ".join([title, c.title, c.id, t_title, t.title])
            cards.append(
                f'<a class="ecard" href="{href}" '
                f'data-status="{c.status.name}" data-axis="{d.strength.short}" '
                f'data-text="{_esc(search_text.lower())}" '
                f'style="border-left-color:{_LIGHT_COLOR[c.status]}">'
                f'<span class="elight">{c.status.light}</span>'
                f'<span class="etitle">{_esc(title)}</span>'
                f'<span class="emeta">{_esc(t_title)} · '
                f'{_esc(d.strength.short)} {div}</span></a>'
            )
    status_chips = "".join(
        f'<button class="chip f" data-k="status" data-v="{s.name}">'
        f'{s.light} {_esc(ZH.STATUS_ZH[s.value] if zh else s.value)}</button>'
        for s in Status)
    axis_chips = "".join(
        f'<button class="chip f" data-k="axis" data-v="{a.short}">'
        f'{a.short}</button>' for a in EvidenceStrength)

    tpl = _EXPLORE_ZH if zh else _EXPLORE
    return tpl.format(
        status_chips=status_chips, axis_chips=axis_chips,
        cards="".join(cards), total=len(cards))


def claims_json(topics: List[Topic]) -> str:
    """D2: machine-readable export of everything recorded — the interface for
    third-party re-review. Only recorded fields and mechanical derivations;
    nothing invented at export time."""
    import json as _json
    from .validator import tier_of
    out = []
    for t in topics:
        for c in t.claims:
            d = derive(c)
            out.append({
                "topic": t.id,
                "id": c.id,
                "title": c.title,
                "status": c.status.name,
                "status_light": c.status.value,
                "evidence_axis": d.strength.short,
                "evidence_axis_name": d.strength.value,
                "axis_derivation": d.reasoning,
                "diverges": diverges(c),
                "status_reason": [
                    {"condition": ca.condition, "holds": ca.holds,
                     "note": ca.note} for ca in c.status_reason],
                "evidence": [
                    {"type": e.type, "description": e.description,
                     "source_ref": e.source_ref} for e in c.evidence],
                "competing_models": [
                    {"name": m.name, "supporting": m.supporting,
                     "opposing": m.opposing, "limitations": m.limitations}
                    for m in c.competing_models],
                "open_questions": list(c.open_questions),
                "sources": [
                    {"label": s.label, "url_or_id": s.url_or_id,
                     "kind": s.kind, "tier": tier_of(s.kind)}
                    for s in c.sources],
                "status_history": [
                    {"date": h.date, "from": h.from_status,
                     "to": h.to_status, "trigger": h.trigger}
                    for h in c.status_history],
            })
    return _json.dumps({
        "note": ("Universe Explorer open data. Only recorded fields and "
                 "mechanical derivations — no confidence numbers exist "
                 "anywhere in this system by constitution."),
        "claims": out,
    }, ensure_ascii=False, indent=1)


# Theme clusters for the expanded 宇宙 / 星球 / 地球 frontend (docs only + UI).
TOPIC_THEMES = {
    "cosmology": "cosmos",
    "dark_matter": "cosmos",
    "black_hole": "cosmos",
    "stars": "cosmos",
    "planets": "planets",
    "exoplanets": "planets",
    "ocean": "earth",
    "seismology": "earth",
    "polar": "earth",
}
THEME_META = {
    "cosmos": {"title": "Cosmos", "title_zh": "宇宙"},
    "planets": {"title": "Planets", "title_zh": "星球"},
    "earth": {"title": "Earth", "title_zh": "地球"},
}


def app_data_json(topics: List[Topic]) -> str:
    """D4: the bilingual payload for the dynamic frontend. Same constitution
    as claims.json — only recorded fields and mechanical derivations; the zh
    fields come from the presentation overlay and fall back to English."""
    import json as _json
    from .data import translations_zh as ZH
    from .data.translations_zh import ZH_LOC
    from .narrative import narrate
    from .validator import tier_of

    def _zc(cid):
        return ZH.CLAIMS.get(cid, {})

    topics_out = []
    claims_out = []
    for t in topics:
        tz = ZH.TOPIC_ZH.get(t.id, {})
        theme = TOPIC_THEMES.get(t.id, "cosmos")
        topics_out.append({
            "id": t.id, "title": t.title,
            "title_zh": tz.get("title", t.title),
            "summary": t.summary,
            "summary_zh": tz.get("summary", t.summary),
            "theme": theme,
            "theme_title": THEME_META[theme]["title"],
            "theme_title_zh": THEME_META[theme]["title_zh"],
            "n_claims": len(t.claims),
        })
        for c in t.claims:
            d = derive(c)
            z = _zc(c.id)
            ev_zh = z.get("evidence", [])
            cm_zh = z.get("competing", [])
            claims_out.append({
                "topic": t.id,
                "id": c.id,
                "title": c.title,
                "title_zh": z.get("title", c.title),
                "status": c.status.name,
                "status_light": c.status.light,
                "status_name": c.status.value,
                "status_name_zh": ZH.STATUS_ZH.get(c.status.value,
                                                   c.status.value),
                "status_rank": c.status.rank,
                "axis": d.strength.short,
                "axis_rank": list(EvidenceStrength).index(d.strength),
                "axis_name": d.strength.value,
                "axis_name_zh": ZH.AXIS_ZH.get(d.strength.short,
                                               d.strength.value),
                "axis_derivation": d.reasoning,
                "diverges": diverges(c),
                "status_reason": [{
                    "condition": ca.condition,
                    "condition_zh": ZH.CONDITION_ZH.get(ca.condition,
                                                        ca.condition),
                    "holds": ca.holds,
                    "note": ca.note,
                    "note_zh": z.get("reasons", {}).get(ca.condition, ca.note),
                } for ca in c.status_reason],
                "evidence": [{
                    "type": e.type,
                    "type_zh": ZH.EVIDENCE_TYPE_ZH.get(e.type, e.type),
                    "description": e.description,
                    "description_zh": (ev_zh[i] if i < len(ev_zh)
                                       else e.description),
                    "source_ref": e.source_ref,
                } for i, e in enumerate(c.evidence)],
                "competing": [{
                    "name": m.name,
                    "name_zh": (cm_zh[i].get("name", m.name)
                                if i < len(cm_zh) else m.name),
                    "supporting": m.supporting,
                    "supporting_zh": (cm_zh[i].get("for", m.supporting)
                                      if i < len(cm_zh) else m.supporting),
                    "opposing": m.opposing,
                    "opposing_zh": (cm_zh[i].get("against", m.opposing)
                                    if i < len(cm_zh) else m.opposing),
                    "limitations": m.limitations,
                    "limitations_zh": (cm_zh[i].get("limits", m.limitations)
                                       if i < len(cm_zh) else m.limitations),
                } for i, m in enumerate(c.competing_models)],
                "open_questions": list(c.open_questions),
                "open_questions_zh": (z.get("open_questions")
                                      or list(c.open_questions)),
                "sources": [{
                    "label": s.label, "url_or_id": s.url_or_id,
                    "kind": s.kind, "tier": tier_of(s.kind),
                } for s in c.sources],
                "narrative": [{"text": s.text, "refs": s.refs}
                              for s in narrate(c)],
                "narrative_zh": [{"text": s.text, "refs": s.refs}
                                 for s in narrate(c, ZH_LOC)],
                "history": [{"date": h.date, "from": h.from_status,
                             "to": h.to_status, "trigger": h.trigger}
                            for h in c.status_history],
                "permalink": f"{t.id}.html#c-{c.id}",
            })
    # Claim relations + mechanical inference paths (no confidence fields).
    from .relations import relations_payload
    from .canonicals import as_payload as canonicals_payload
    rel = relations_payload(topics)
    by = rel["by_claim"]
    for row in claims_out:
        block = by.get(row["id"], {})
        # attach lightweight related list; full paths under inferences
        row["related"] = block.get("related", [])
        row["inferences"] = block.get("inferences", [])
        row["n_related"] = block.get("n_related", 0)
        row["n_inferences"] = block.get("n_inferences", 0)
    return _json.dumps({
        "note": ("Universe Explorer app data. Only recorded fields and "
                 "mechanical derivations; zh fields are a presentation "
                 "overlay that falls back to English. Relations are authored "
                 "edges plus mechanical shared-source; inference paths are "
                 "listed routes — never confidence scores. "
                 "canonicals are three teaching anchors only."),
        "canonicals": canonicals_payload(),
        "relations": {
            "note": rel["note"],
            "kinds": rel["kinds"],
            "kind_labels": rel["kind_labels"],
            "n_links": rel["n_links"],
            "n_authored": rel["n_authored"],
            "n_mechanical": rel["n_mechanical"],
            "links": rel["links"],
            "reading_paths": rel["reading_paths"],
            "coverage": rel["coverage"],
        },
        "themes": [
            {"id": k, "title": v["title"], "title_zh": v["title_zh"]}
            for k, v in THEME_META.items()
        ],
        "topics": topics_out,
        "claims": claims_out,
    }, ensure_ascii=False)


def render_index(topics: List[Topic]) -> str:
    """The multi-topic landing page (P4). Each topic is a container with no
    light of its own; its claim lights are previewed so the knowledge shape is
    legible before you even open the topic. Grouped by 宇宙 / 星球 / 地球."""
    by_theme: dict = {k: [] for k in THEME_META}
    for t in topics:
        theme = TOPIC_THEMES.get(t.id, "cosmos")
        claims = sorted(t.claims, key=lambda c: c.status.rank)
        dots = "".join(
            f'<span class="dot" style="color:{_LIGHT_COLOR[c.status]}" '
            f'title="{_esc(c.title)}">{c.status.light}</span>'
            for c in claims
        )
        claim_rows = "".join(
            f'<a class="claim-row" href="{_esc(t.id)}.html#c-{_esc(c.id)}">'
            f'<span>{c.status.light}</span>'
            f'<b>{_esc(c.title)}</b>'
            f'<span class="cid">{_esc(c.id)}</span></a>'
            for c in claims
        )
        by_theme.setdefault(theme, []).append(
            f'<div class="topic-card" data-topic="{_esc(t.id)}">'
            f'<button type="button" class="topic-toggle" aria-expanded="false">'
            f'<span class="chev" aria-hidden="true">›</span>'
            f'<h2>{_esc(t.title)} '
            f'<span class="n">{len(t.claims)} claims</span></h2>'
            f'<div class="dots">{dots}</div></button>'
            f'<p>{_esc(t.summary)}</p>'
            f'<div class="claim-list" role="region">{claim_rows}'
            f'<a class="claim-row" href="{_esc(t.id)}.html" style="justify-content:center;'
            f'font-weight:500;color:var(--accent)">Open full domain page →</a>'
            f'</div></div>'
        )
    sections = []
    for tid, meta in THEME_META.items():
        cards = by_theme.get(tid) or []
        if not cards:
            continue
        sections.append(
            f'<section class="theme-block" id="theme-{_esc(tid)}">'
            f'<h2 class="theme-h">{_esc(meta["title"])} '
            f'<span class="theme-h-zh">{_esc(meta["title_zh"])}</span></h2>'
            f'<div class="theme-grid">{"".join(cards)}</div></section>'
        )
    total = sum(len(t.claims) for t in topics)
    lead = (
        f'<p class="lead">Cosmos · Planets · Earth — '
        f'{len(topics)} domains, <b>{total}</b> claims. '
        f'Lights belong to claims, never to topics. '
        f'<a href="app.html">Knowledge map</a> · '
        f'<a href="universe.html">Drift</a> · '
        f'<a href="zh.html">中文</a></p>'
    )
    return _INDEX.format(
        legend=_legend(),
        cards=lead + "".join(sections),
    )


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
  .permalink {{ opacity: .35; text-decoration: none; margin-left: 6px; }}
  .permalink:hover {{ opacity: .9; }}
  .challenge-link {{ font-size: .74em; opacity: .55; margin-left: 8px;
                    text-decoration: none; border: 1px solid currentColor;
                    border-radius: 999px; padding: 0 8px; }}
  .challenge-link:hover {{ opacity: 1; }}
  article:target {{ outline: 2px solid currentColor; outline-offset: 4px; }}
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
  .tier {{ font-size: .68em; font-weight: 700; letter-spacing: .05em;
          border: 1px solid currentColor; border-radius: 3px;
          padding: 0 5px; opacity: .75; }}
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


_EXPLORE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe Explorer — Explore</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.55 system-ui, sans-serif; max-width: 820px;
         margin: 0 auto; padding: 24px; }}
  .home {{ font-size: .85em; opacity: .7; text-decoration: none; }}
  h1 {{ margin: 8px 0 4px; }}
  .sub {{ opacity: .75; margin: 0 0 16px; }}
  .bar {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; }}
  .chip {{ border: 1px solid currentColor; background: transparent;
          color: inherit; border-radius: 999px; padding: 3px 12px;
          font-size: .82em; cursor: pointer; opacity: .65; }}
  .chip.on {{ opacity: 1; font-weight: 700;
             background: color-mix(in srgb, currentColor 12%, transparent); }}
  #q {{ width: 100%; box-sizing: border-box; font: inherit; padding: 8px 12px;
       border: 1px solid currentColor; border-radius: 8px;
       background: transparent; color: inherit; margin: 6px 0 4px; }}
  .count {{ font-size: .8em; opacity: .6; margin: 4px 0 12px; }}
  .ecard {{ display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap;
           text-decoration: none; color: inherit; border: 1px solid
           color-mix(in srgb, currentColor 25%, transparent);
           border-left: 5px solid; border-radius: 0 8px 8px 0;
           padding: 10px 14px; margin: 8px 0; }}
  .ecard:hover {{ background: color-mix(in srgb, currentColor 6%, transparent); }}
  .ecard.hide {{ display: none; }}
  .elight {{ font-size: 1.15em; }}
  .etitle {{ font-weight: 600; }}
  .emeta {{ font-size: .8em; opacity: .65; margin-left: auto; }}
  .diverge {{ opacity: 1; }}
  .foot {{ font-size: .8em; opacity: .6; margin-top: 24px; }}
  .chip:focus-visible, .ecard:focus-visible, #q:focus-visible {{
    outline: 2px solid currentColor; outline-offset: 2px; }}
</style>
</head>
<body>
<a class="home" href="index.html">&larr; all topics</a>
<h1>Explore</h1>
<p class="sub">Every claim across every domain. Filter by light or evidence
axis; the order never changes: bedrock first, ceiling last.
<a href="explore-zh.html">中文版 &rarr;</a></p>
<input id="q" type="search" placeholder="search title / id / topic&hellip;"
 aria-label="search claims">
<div class="bar" id="statusbar">{status_chips}</div>
<div class="bar" id="axisbar">{axis_chips}</div>
<div class="count"><span id="n">{total}</span> / {total} shown
 (a count of the visible list &mdash; recount it yourself)</div>
<main id="cards">
{cards}
</main>
<p class="foot">Open data: <a href="claims.json">claims.json</a> &mdash; every
recorded field, machine-readable, for third-party re-review.</p>
<script>
(function () {{
  var active = {{ status: new Set(), axis: new Set() }};
  var q = "";
  var cards = Array.prototype.slice.call(document.querySelectorAll(".ecard"));
  function apply() {{
    var n = 0;
    cards.forEach(function (c) {{
      var ok = true;
      if (active.status.size && !active.status.has(c.dataset.status)) ok = false;
      if (active.axis.size && !active.axis.has(c.dataset.axis)) ok = false;
      if (q && c.dataset.text.indexOf(q) === -1) ok = false;
      c.classList.toggle("hide", !ok);
      if (ok) n++;
    }});
    document.getElementById("n").textContent = n;
  }}
  document.querySelectorAll(".chip.f").forEach(function (b) {{
    b.addEventListener("click", function () {{
      var set = active[b.dataset.k];
      if (set.has(b.dataset.v)) {{ set.delete(b.dataset.v); b.classList.remove("on"); }}
      else {{ set.add(b.dataset.v); b.classList.add("on"); }}
      apply();
    }});
  }});
  document.getElementById("q").addEventListener("input", function (e) {{
    q = e.target.value.trim().toLowerCase(); apply();
  }});
}})();
</script>
</body>
</html>
"""


def render_about(lang: str = "en") -> str:
    """T3: the charter page — a stranger should understand the system in three
    minutes. Content is condensed from the frozen specs; it asserts nothing new."""
    return _ABOUT_ZH if lang == "zh" else _ABOUT


_ABOUT_BASE_CSS = """
  :root { color-scheme: light dark; }
  body { font: 16px/1.65 system-ui, sans-serif; max-width: 720px;
         margin: 0 auto; padding: 24px; }
  .home { font-size: .85em; opacity: .7; text-decoration: none; }
  h1 { margin: 10px 0 4px; }
  h2 { font-size: 1.15rem; margin: 26px 0 6px; }
  p, li { opacity: .92; }
  .lights td { padding: 3px 10px 3px 0; vertical-align: top; }
  code { font-family: ui-monospace, monospace; font-size: .88em; }
  .rule { border-left: 3px solid currentColor; padding: 2px 12px;
          opacity: .85; margin: 10px 0; }
"""

_ABOUT = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe Explorer — How to read this</title>
<style>{_ABOUT_BASE_CSS}</style>
</head>
<body>
<a class="home" href="app.html">&larr; knowledge map</a>
 · <a class="home" href="index.html">plain topics</a>
<h1 id="how-to-read">How to read this</h1>
<p>This site does not tell you answers. It tells you: what we know, how we
know it, what we still don't, and which hypotheses are competing. It was built
so that <b>every verdict can be checked — and overturned — by anyone</b>.
<a href="about-zh.html">中文版 &rarr;</a></p>
<p><a href="app.html">Open the map</a> · first visit shows a 60-second tour ·
or jump to the <a href="app.html?c=hawking_radiation">Hawking radiation example</a>.</p>
<p>Other surfaces (same data, different lenses):
<a href="dashboard.html">dashboard</a> ·
<a href="explore-v2.html">search &amp; filter</a> ·
<a href="epistemic_map.html">cross-domain map</a> ·
<a href="explore.html">browse all claims</a> ·
<a href="challenge.html">challenge a verdict</a> ·
<a href="health.html">inventory health</a> ·
<a href="stats.json">stats.json</a>.</p>

<h2 id="example">Canonical example: Hawking radiation</h2>
<p>Open <a href="app.html?c=hawking_radiation"><code>hawking_radiation</code></a>
on the map. The light is <b>Strong</b> (mainstream theory + analogue support),
but the evidence axis is weaker than the consensus — so the card may show
<b>⚡ axes diverge</b>. That is the product in one claim: high agreement does
not invent direct astrophysical detection. Count the open questions yourself.
Related edges (e.g. to the horizon or the information paradox) are
<i>recorded links</i>, not a score of who is right.
Full pipeline notes (data → axes → narrative → UI):
<a href="https://github.com/taipei49314/universe-explorer/blob/main/docs/hawking-walkthrough.md">hawking-walkthrough.md</a>.
Closed challenge (Trust Loop):
<a href="https://github.com/taipei49314/universe-explorer/issues/2">issue #2</a>
— Strong re-review, light unchanged.</p>

<h2 id="canonicals">Three stories to learn the product</h2>
<p class="note" style="opacity:.8;font-size:.9rem">Teaching anchors only —
not a ranking of science. Each opens a claim and a reading path.</p>
<ol>
<li><b>Dual axes (Cosmos)</b> —
  <a href="app.html?c=hawking_radiation"><code>hawking_radiation</code></a>
  · path <a href="app.html?path=path_black_hole"><code>path_black_hole</code></a>
  — Strong consensus × non-direct evidence (⚡ diverge).</li>
<li><b>Competing models (Cosmos)</b> —
  <a href="app.html?c=H0_tension_local_vs_cmb"><code>H0_tension_local_vs_cmb</code></a>
  · path <a href="app.html?path=path_h0"><code>path_h0</code></a>
  — yellow umbrella; poles and relief routes; <i>no path step is a winner</i>.</li>
<li><b>Competing models (Earth)</b> —
  <a href="app.html?c=short_term_deterministic_prediction"><code>short_term_deterministic_prediction</code></a>
  · path <a href="app.html?path=path_seismology"><code>path_seismology</code></a>
  — prediction vs forecasting; season secondary in the editorial queue.</li>
</ol>
<p>Machine list: <code>universe_explorer/canonicals.py</code> · inventory also on
<a href="health.html#trust-loop">health Trust Loop panel</a>.</p>

<h2>The five lights (they belong to claims, never to topics)</h2>
<table class="lights">
<tr><td>🟢</td><td><b>Established</b> — independently replicated, in the
textbooks, no mainstream rival, nothing recently overturned it.</td></tr>
<tr><td>🔵</td><td><b>Strong</b> — mainstream-supported; minority alternatives
exist; details may shift, direction won't.</td></tr>
<tr><td>🟡</td><td><b>Competing</b> — the field genuinely holds two or more
positions and no decisive evidence picks one.</td></tr>
<tr><td>🟠</td><td><b>Frontier</b> — new, under-sampled, fast-moving, no
consensus yet.</td></tr>
<tr><td>🔴</td><td><b>Speculative</b> — no observation, pure theory, or the
mainstream simply doesn't buy it.</td></tr>
</table>
<p>Each light has machine-checkable entry conditions; every claim card's
&ldquo;Why this light&rdquo; lists them one by one, so you can audit the verdict.</p>

<h2>The evidence axis (nobody fills it in)</h2>
<p>E1 (multiple independent direct observations, peer-reviewed sources only)
down to E4 (theory only). It is <i>derived by public rules</i> from the
recorded evidence — the only way to move it is to record new evidence. When a
strong consensus rests on non-direct evidence, the card shows
<b>⚡ axes diverge</b>: an honest tension, stated, not hidden.</p>

<h2>What this system refuses to do</h2>
<div class="rule">No confidence percentages. Ever. Certainty must emerge from
evidence you can open — it is never declared as a number.</div>
<div class="rule">No citation without a fetch: every arXiv/DOI source was
retrieved from the official API, stored verbatim, and hash-verified.
Unclassifiable sources are unconstitutional.</div>
<div class="rule">No silent changes: a status may move only with a recorded
date, origin and trigger — and sources are re-checked weekly for formally
deposited corrections and retractions.</div>
<div class="rule">Machines may exclude, only humans approve. AI drafts are
stamped UNVERIFIED and live outside the data.</div>

<h2>Overturn us</h2>
<p>Pick any claim, press <code>challenge</code> on its card, and argue against
its entry conditions with a checkable source. The full re-review path is in
<a href="https://github.com/taipei49314/universe-explorer/blob/main/CONTRIBUTING.md">CONTRIBUTING</a>;
every rule and its legal basis is consolidated in the
<a href="https://github.com/taipei49314/universe-explorer/blob/main/docs/constitution.md">constitution</a>;
the machine-readable data is <a href="claims.json">claims.json</a>; the
on-site form is <a href="challenge.html">challenge.html</a>; changes
stream to the <a href="feed.xml">Atom feed</a> and
<a href="changes.html">changes.html</a>. Audit inventory:
<a href="health.html">health.html</a>. Code is MIT; content is
CC BY 4.0 — challenging us requires no permission at all.</p>

<h2 id="support">How this stays alive</h2>
<p>This project does <b>not</b> sell “higher confidence lights.” If you support
it, you fund <i>editorial hours and infrastructure</i> — domain deepening,
source fetch, weekly health runs — never a paid verdict. See
<a href="https://github.com/taipei49314/universe-explorer">GitHub</a> for
issues and forks; domain forks may grow content while the engine stays the court.
Optional: star the repo, open careful challenges, or adopt the map in a course
with the constitution intact.</p>
</body>
</html>
"""

_ABOUT_ZH = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>宇宙探索者 — 這個網站怎麼讀</title>
<style>{_ABOUT_BASE_CSS}</style>
</head>
<body>
<a class="home" href="app.html">&larr; 知識地圖</a>
 · <a class="home" href="zh.html">中文總覽</a>
<h1 id="how-to-read">這個網站怎麼讀</h1>
<p>這個網站不告訴你答案。它告訴你:我們知道什麼、怎麼知道的、還不知道什麼、
有哪些假說在競爭。它被造出來,就是為了讓<b>任何人都能查核 —— 並推翻 ——
任何一個判定</b>。<a href="about.html">English &rarr;</a></p>
<p><a href="app.html">打開地圖</a> · 首次造訪有約 60 秒導覽 ·
或直接看範例 <a href="app.html?c=hawking_radiation">霍金輻射</a>。</p>
<p>其他介面（同一套資料、不同切面）:
<a href="dashboard.html">總覽儀表板</a> ·
<a href="explore-v2.html">搜尋與篩選</a> ·
<a href="epistemic_map.html">跨領域地圖</a> ·
<a href="explore-zh.html">瀏覽全部宣稱</a> ·
<a href="challenge.html">挑戰判定</a> ·
<a href="health.html">盤點健康</a> ·
<a href="stats.json">stats.json</a>。</p>

<h2 id="example">標準範例:霍金輻射</h2>
<p>在地圖打開 <a href="app.html?c=hawking_radiation"><code>hawking_radiation</code></a>。
燈號是<strong>強共識</strong>(主流理論 + 類比實驗),但證據軸可能弱於共識 —
卡片可能出現 <b>⚡ 雙軸分岔</b>。這就是產品的一句話:高共識不捏造直接天文偵測。
開放問題請自己數。關聯邊(例如連到視界或資訊悖論)是<i>已記錄的連結</i>,不是勝負分數。
完整管線說明(data → axes → narrative → UI):
<a href="https://github.com/taipei49314/universe-explorer/blob/main/docs/hawking-walkthrough.md">hawking-walkthrough.md</a>。
Trust Loop 已關閉挑戰:
<a href="https://github.com/taipei49314/universe-explorer/issues/2">issue #2</a>
— Strong 覆核,燈號未改。</p>

<h2 id="canonicals">三則故事,學會這個產品</h2>
<p style="opacity:.8;font-size:.9rem">僅教學錨點 —— 不是科學排名。每一則連到宣稱與閱讀路徑。</p>
<ol>
<li><b>雙軸(宇宙)</b> —
  <a href="app.html?c=hawking_radiation"><code>hawking_radiation</code></a>
  · 路徑 <a href="app.html?path=path_black_hole"><code>path_black_hole</code></a>
  — 強共識 × 非直接證據(⚡ 分岔)。</li>
<li><b>競爭模型(宇宙)</b> —
  <a href="app.html?c=H0_tension_local_vs_cmb"><code>H0_tension_local_vs_cmb</code></a>
  · 路徑 <a href="app.html?path=path_h0"><code>path_h0</code></a>
  — 黃燈傘形;兩極與緩解路徑;<i>路徑步驟沒有勝負</i>。</li>
<li><b>競爭模型(地球)</b> —
  <a href="app.html?c=short_term_deterministic_prediction"><code>short_term_deterministic_prediction</code></a>
  · 路徑 <a href="app.html?path=path_seismology"><code>path_seismology</code></a>
  — 確定性預測 vs 預報;本季 editorial 次要域。</li>
</ol>
<p>機器清單:<code>universe_explorer/canonicals.py</code> · 亦見
<a href="health.html#trust-loop">health Trust Loop 面板</a>。</p>

<h2>五格燈號(屬於 claim,永不屬於 topic)</h2>
<table class="lights">
<tr><td>🟢</td><td><b>已確立</b> —— 多團隊獨立驗證、寫進教科書、無主流競爭理論、近期無反證。</td></tr>
<tr><td>🔵</td><td><b>強共識</b> —— 主流支持;有少數替代理論;細節會修,方向不動。</td></tr>
<tr><td>🟡</td><td><b>競爭模型</b> —— 學界真的有兩派以上,且無決定性證據。</td></tr>
<tr><td>🟠</td><td><b>前沿研究</b> —— 新、樣本不足、變動快、尚無共識。</td></tr>
<tr><td>🔴</td><td><b>推測性</b> —— 無觀測、純理論,或主流就是不買帳。</td></tr>
</table>
<p>每格燈號都有機器可查的入格條件;每張卡片的「為什麼是這個燈號」逐條列出,
供你稽核。</p>

<h2>證據軸(沒有人填它)</h2>
<p>從 E1(多重獨立直接觀測,僅計同儕審查來源)到 E4(僅理論)。它由公開規則
從已收錄證據<i>機械推導</i> —— 想動它,唯一的路是收錄新證據。當強共識建立在
非直接證據上,卡片會顯示 <b>⚡ 雙軸分岔</b>:張力誠實攤開,不藏。</p>

<h2>這個系統拒絕做的事</h2>
<div class="rule">永不出現信心百分比。確定性必須從你能展開的證據湧現,
不得被宣告成一個數字。</div>
<div class="rule">引用即必須抓過原文:每個 arXiv/DOI 來源都從官方 API 取回、
逐字保存、雜湊驗證。無法分級的來源即違憲。</div>
<div class="rule">不准無聲地變:燈號要動,必須留下日期、來歷與觸發原因 ——
且來源每週自動回查正式存繳的更正與撤稿。</div>
<div class="rule">機器只能排除,核准永遠是人。AI 草稿蓋 UNVERIFIED 章,
住在資料之外。</div>

<h2>來推翻我們</h2>
<p>挑任何一個 claim,按卡片上的 <code>challenge</code>,拿可查證的來源逐條
攻擊它的入格條件。完整覆核路徑在
<a href="https://github.com/taipei49314/universe-explorer/blob/main/CONTRIBUTING.md">CONTRIBUTING</a>;
全部規則與法源彙編於
<a href="https://github.com/taipei49314/universe-explorer/blob/main/docs/constitution.md">憲法</a>;
機器可讀資料在 <a href="claims.json">claims.json</a>;站內表單在
<a href="challenge.html">challenge.html</a>;所有變化流向
<a href="feed.xml">Atom feed</a> 與 <a href="changes.html">changes.html</a>。
覆核清單:<a href="health.html">health.html</a>。程式碼 MIT、內容 CC BY 4.0 ——
挑戰我們,完全不需要任何人的許可。</p>

<h2 id="support">這專案如何活著</h2>
<p>這裡<b>不賣</b>「更高信心的燈號」。若你支持,買的是<i>編輯工時與基礎設施</i>
—— 加深領域、抓取出處、每週健康巡檢 —— 永遠不是付費判決。見
<a href="https://github.com/taipei49314/universe-explorer">GitHub</a>
的 issue 與 fork;分域 fork 可養內容,上游養法院。可選:star、開謹慎的挑戰、
或在課程採用此地圖並保留憲法。</p>
</body>
</html>
"""


# Chinese explore page: same template, translated chrome. Derived by literal
# replacement so the two can never drift structurally.
_EXPLORE_ZH = (
    _EXPLORE
    .replace('<html lang="en">', '<html lang="zh-Hant">')
    .replace("<title>Universe Explorer &mdash; Explore</title>",
             "<title>宇宙探索者 — 探索</title>")
    .replace("<title>Universe Explorer — Explore</title>",
             "<title>宇宙探索者 — 探索</title>")
    .replace('<a class="home" href="index.html">&larr; all topics</a>',
             '<a class="home" href="zh.html">&larr; 中文總覽</a>')
    .replace("<h1>Explore</h1>", "<h1>探索</h1>")
    .replace("Every claim across every domain. Filter by light or evidence\n"
             "axis; the order never changes: bedrock first, ceiling last.\n"
             '<a href="explore-zh.html">中文版 &rarr;</a>',
             "跨領域的全部宣稱。可依燈號或證據軸篩選;排序永遠不變:地基在前、"
             '天花板在後。<a href="explore.html">English &rarr;</a>')
    .replace('placeholder="search title / id / topic&hellip;"',
             'placeholder="搜尋標題 / id / 領域…"')
    .replace("aria-label=\"search claims\"", 'aria-label="搜尋宣稱"')
    .replace("shown\n (a count of the visible list &mdash; recount it yourself)",
             "顯示中\n(這是可見清單的計數 —— 請自行重數)")
    .replace("Open data: <a href=\"claims.json\">claims.json</a> &mdash; every\n"
             "recorded field, machine-readable, for third-party re-review.",
             '開放資料:<a href="claims.json">claims.json</a> —— 全部已收錄欄位,'
             "機器可讀,供第三方覆核。")
)


_INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe Explorer</title>
<style>
  :root {{ color-scheme: light dark;
    --bg: #F5F5F7; --ink: #1D1D1F; --muted: #6E6E73; --accent: #0071E3;
    --card: rgba(255,255,255,.72); --line: rgba(0,0,0,.08);
    --ease: cubic-bezier(.16,1,.3,1); }}
  @media (prefers-color-scheme: dark) {{ :root {{
    --bg: #000; --ink: #F5F5F7; --muted: #98989D; --accent: #0A84FF;
    --card: rgba(28,28,30,.78); --line: rgba(255,255,255,.1); }} }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font: 17px/1.47 -apple-system, BlinkMacSystemFont,
         "SF Pro Text", "Segoe UI", "PingFang TC", sans-serif;
         background: var(--bg); color: var(--ink);
         -webkit-font-smoothing: antialiased; letter-spacing: -.01em; }}
  body::before {{ content: ""; position: fixed; inset: 0; pointer-events: none;
    background: radial-gradient(ellipse 80% 50% at 30% -5%,
      color-mix(in srgb, var(--accent) 14%, transparent), transparent 55%); }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ opacity: .8; }}
  .wrap {{ max-width: 980px; margin: 0 auto; padding: 0 24px 80px;
           position: relative; z-index: 1; }}
  .hero {{ padding: 72px 0 28px; text-align: center; }}
  .hero h1 {{ font: 600 3.2rem/1.05 -apple-system, BlinkMacSystemFont,
             "SF Pro Display", Georgia, "Songti SC", serif;
             letter-spacing: -.035em; margin: 0 0 14px; }}
  .hero .tag {{ color: var(--muted); font-size: 1.2rem; max-width: 28em;
               margin: 0 auto 28px; line-height: 1.4; }}
  .cta {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;
         margin-bottom: 18px; }}
  .cta a {{ display: inline-flex; align-items: center; gap: 6px;
           border-radius: 980px; padding: 12px 22px; font-size: .95rem;
           font-weight: 500; transition: transform .25s var(--ease),
           opacity .2s; }}
  .cta a:hover {{ transform: scale(1.04); opacity: 1; }}
  .cta .primary {{ background: var(--accent); color: #fff; }}
  .cta .ghost {{ border: 1px solid var(--line); color: var(--ink);
               background: var(--card);
               backdrop-filter: blur(16px); }}
  .banner {{ font-size: .88rem; color: var(--muted); text-align: center;
            margin: 8px auto 36px; max-width: 36em; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
            margin: 0 0 40px; }}
  .chip {{ border: 1px solid var(--line); border-radius: 980px;
          padding: 4px 12px; font-size: .8rem; background: var(--card);
          backdrop-filter: blur(12px); }}
  .lead {{ color: var(--muted); margin: 0 0 8px; font-size: .95rem;
          text-align: center; }}
  .theme-block {{ margin: 48px 0; }}
  .theme-h {{ font: 600 1.5rem/1.15 -apple-system, BlinkMacSystemFont,
             "SF Pro Display", Georgia, serif; margin: 0 0 18px;
             letter-spacing: -.02em; text-align: center; }}
  .theme-h-zh {{ font-size: .75em; opacity: .55; margin-left: 8px;
                font-weight: 500; }}
  .theme-grid {{ display: grid; gap: 14px;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
  .topic-card {{ display: block; border: 1px solid var(--line); border-radius: 20px;
                padding: 0; margin: 0; background: var(--card);
                backdrop-filter: blur(18px); overflow: hidden;
                box-shadow: 0 4px 24px rgba(0,0,0,.04);
                transition: transform .35s var(--ease),
                  box-shadow .35s var(--ease), border-color .2s; }}
  .topic-card:hover {{ box-shadow: 0 16px 40px rgba(0,0,0,.1);
    border-color: color-mix(in srgb, var(--accent) 35%, var(--line)); }}
  .topic-card.open {{ border-color: color-mix(in srgb, var(--accent) 45%, var(--line)); }}
  .topic-toggle {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;
                  width: 100%; text-align: left; border: 0; background: transparent;
                  color: inherit; font: inherit; padding: 22px 22px 18px; cursor: pointer; }}
  .topic-toggle .chev {{ width: 26px; height: 26px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    background: color-mix(in srgb, var(--ink) 6%, transparent); margin-right: 4px;
    transition: transform .3s var(--ease); font-size: .9rem; color: var(--muted); }}
  .topic-card.open .chev {{ transform: rotate(90deg); background: var(--accent); color: #fff; }}
  .topic-card h2 {{ margin: 0 0 8px; font-size: 1.2rem; letter-spacing: -.015em; flex: 1; }}
  .topic-card .n {{ font-size: .7em; font-weight: 500; opacity: .5;
                   font-family: ui-monospace, monospace; }}
  .dots {{ font-size: 1.25em; letter-spacing: 2px; margin-bottom: 10px; width: 100%;
           padding-left: 34px; }}
  .topic-card > p {{ margin: 0; opacity: .72; font-size: .9rem; line-height: 1.45;
                    padding: 0 22px 14px 56px; }}
  .claim-list {{ max-height: 0; opacity: 0; overflow: hidden; padding: 0 14px;
    transition: max-height .45s var(--ease), opacity .3s, padding .3s; }}
  .topic-card.open .claim-list {{ max-height: 2400px; opacity: 1; padding: 0 14px 16px; }}
  .claim-row {{ display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap;
    text-decoration: none; color: inherit; border: 1px solid var(--line);
    border-radius: 12px; padding: 10px 14px; margin: 6px 0;
    background: color-mix(in srgb, var(--bg) 40%, transparent);
    transition: background .2s, transform .2s var(--ease); }}
  .claim-row:hover {{ background: color-mix(in srgb, var(--accent) 8%, transparent);
    transform: translateX(3px); }}
  .claim-row b {{ font-weight: 600; font-size: .92rem; }}
  .claim-row .cid {{ font-size: .7rem; opacity: .45; font-family: ui-monospace, monospace; }}
  @media (max-width: 640px) {{
    .hero h1 {{ font-size: 2.2rem; }}
    .hero {{ padding-top: 40px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .topic-card, .cta a {{ transition: none; }}
  }}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Universe Explorer</h1>
  <p class="tag">Honestly separating what we know from what we don't.
  Cosmos · Planets · Earth &mdash; lights belong to claims, never topics.</p>
  <div class="cta">
    <a class="primary" href="universe.html">Drift the universe</a>
    <a class="ghost" href="app.html">Knowledge map</a>
    <a class="ghost" href="dashboard.html">Dashboard</a>
    <a class="ghost" href="explore-v2.html">Search &amp; filter</a>
    <a class="ghost" href="epistemic_map.html">Cross-domain map</a>
    <a class="ghost" href="explore.html">Explore claims</a>
    <a class="ghost" href="zh.html">中文</a>
  </div>
  <p class="banner">Reference first, AI last. Certainty emerges from evidence
  you can open &mdash; never from a declared number.
  <a href="about.html">How to read this</a> ·
  <a href="challenge.html">Challenge</a> ·
  <a href="feed.xml">Feed</a></p>
  {legend}
</header>
<main>
{cards}
</main>
</div>
<script>
document.querySelectorAll(".topic-toggle").forEach(btn => {{
  btn.addEventListener("click", () => {{
    const card = btn.closest(".topic-card");
    const open = !card.classList.contains("open");
    card.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }});
}});
// deep-link ?open=stars or #stars
(function () {{
  const q = new URLSearchParams(location.search).get("open");
  const hash = (location.hash || "").replace(/^#/, "");
  const id = q || hash;
  if (!id) return;
  const card = document.querySelector('.topic-card[data-topic="' + CSS.escape(id) + '"]');
  if (!card) return;
  card.classList.add("open");
  const btn = card.querySelector(".topic-toggle");
  if (btn) btn.setAttribute("aria-expanded", "true");
  card.scrollIntoView({{ behavior: "smooth", block: "center" }});
}})();
</script>
</body>
</html>
"""
