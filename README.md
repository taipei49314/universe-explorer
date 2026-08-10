# Universe Explorer

**Honestly separating what we know from what we don't.**  
誠實區分已知與未知的科學知識系統。

Live site: <https://taipei49314.github.io/universe-explorer/>  
Open data: [`claims.json`](https://taipei49314.github.io/universe-explorer/claims.json) · Atom feed: [`feed.xml`](https://taipei49314.github.io/universe-explorer/feed.xml)

It does **not** tell you “the answer.” It shows, claim by claim:

- **what** is claimed  
- **how** we know it (sources + evidence)  
- **which light** it carries, and **why** (entry conditions, overturnable)  
- **how strong the evidence is** as a separate, mechanical axis  
- **what is still open** (questions you can count yourself)

---

## Snapshot (measured, not marketed)

| Measure | Value |
|---------|-------|
| Topics | **8** |
| Claims | **91** |
| Themes | Cosmos · Planets · Earth |
| Authored relation edges | **96** (+ **67** mechanical shared-source via `all_links`; epistemic map may add detector edges → **171** graph edges / **8** cross-domain flags) |
| Reading paths | **8** (one authored path per registered domain) |
| Engine | Constitution-gated Python · static `dist/` site |
| AI at runtime | **None required** (narrative is a gated bottom layer) |
| CI test modules | **30** suites in `run_tests.py` (**320** `test_*` functions) |

### Domains

| Theme | Topics | Claims |
|-------|--------|--------|
| **Cosmos** | `black_hole`, `cosmology`, `dark_matter`, `stars` | 10 + 16 + 18 + 12 |
| **Planets** | `planets`, `exoplanets` | 10 + 9 |
| **Earth** | `ocean`, `seismology` | 8 + 8 |

*Counts are inventory from the topic registry. Re-measure after data edits with `python build.py --check`.*

---

## The constitution (enforced by code)

Hard red lines live in `universe_explorer/validator.py` (`LAWS`) and related gates — not only in prose.

1. **Reference first, AI last.**  
   `Data → Evidence → Knowledge → AI Narrative` (one-way). No source → no upper-layer claim.
2. **AI does not declare facts.**  
   It may only organise recorded evidence. Narrative sentences must carry resolvable refs; on failure the whole narrative is **withheld** (rather absent than overreaching).
3. **No fake precision.**  
   No confidence percentages, no numeric “open questions” counts as a score. Certainty must **emerge** from evidence.
4. **Every “known” hangs on a real source.**  
   Cite arXiv/DOI ⇒ must have **fetched** and hash-verified the record (P1 / Amendment #6).
5. **Lights never change silently.**  
   Status moves need `status_history` + watch events (P3).

The **status light belongs to the Claim, not the Topic.** A topic is a container; claims under it can disagree.

Human overview: [`docs/constitution.md`](docs/constitution.md) · design frame: [`docs/design-framework.md`](docs/design-framework.md)

---

## Dual axes (the point of the system)

Two axes sit on every claim. They are **not** averaged into one trust score.

| Axis | Who sets it | What it is |
|------|-------------|------------|
| **Consensus** (five-cell light) | Human, with traceable `status_reason` | Established · Strong · Competing · Frontier · Speculative |
| **Evidence** (E1–E5) | **Nobody fills it in** — derived by public rules in `axes.py` | E1 multiple independent **PRIMARY** direct · … · E5 none |

Entry conditions for each light are frozen in `model.STATUS_CONDITIONS` (mode `all` or `any`). A third party can recompute and overturn.

### Canonical stress case: `hawking_radiation`

| Field | Value |
|-------|--------|
| Light | **Strong Consensus** (🔵) |
| Evidence axis | **E3** — indirect / analog only |
| `diverges` | **true** — axes point apart |

Strong theory + analog lab work; **no direct astrophysical detection**. That split is structural, not a footnote.  
Deep-link: `app.html?c=hawking_radiation`

---

## Layout (where things live)

```
universe_explorer/
  model.py          # frozen schema + five-cell taxonomy
  validator.py      # constitution court
  axes.py           # evidence axis (derived, never declared)
  provenance.py     # cite ⇒ fetch (arXiv / DOI)
  proposals.py      # propose, never decide
  watch.py          # no silent light changes
  narrative.py      # compose + check (same court for any composer)
  relations.py      # edges + reading paths (no confidence)
  render.py         # static pages
  surface.py        # changes / health surfaces
  discovery/        # search → candidates → precheck → review.html (never auto-writes claims)
  crossdomain/      # shared-source graph → epistemic_map.html
  reader/           # explore-v2, challenge, dual-axis, dashboard, stats/export;
                    # editorial: annotate, review workflow, batch, diff, dynamic_paths
  data/             # hand-authored topics (the only place knowledge grows)
  dataops/          # fetch, push, health, transport
build.py            # gate ALL topics → write dist/
run_tests.py        # every suite + build --check
web/                # app.html, universe.html (shipped into dist/)
docs/               # specs, amendments, editorial queue
cache/              # verbatim API responses + hashes
candidates/         # discovery inlet only (never auto-writes claims)
annotations/        # editorial tags/notes (outside claim data; never auto-writes lights)
reviews/            # claim review checklist state (outside claim data)
```

Engine files are hash-frozen (`engine_hashes.json`). Changing them requires a numbered amendment under `docs/amendment-*.md`.

---

## Run (local)

Requires **Python 3.9+**. No third-party packages for the core gate.

```sh
git clone https://github.com/taipei49314/universe-explorer.git
cd universe-explorer

# One command: all test suites + constitution gate on every topic
python run_tests.py

# Validate only
python build.py --check

# Validate + render site → dist/
python build.py

# Browse
python -m http.server 8731 --directory dist
# open http://localhost:8731/          (index)
#      http://localhost:8731/app.html?c=hawking_radiation
#      http://localhost:8731/explore-v2.html
#      http://localhost:8731/epistemic_map.html
#      http://localhost:8731/universe.html
```

### Unified CLI

```sh
python -m universe_explorer build           # validate + render site
python -m universe_explorer build --check   # validate only
python -m universe_explorer search "query"  # full-text search
python -m universe_explorer filter --domain cosmology --status STRONG
python -m universe_explorer stats           # knowledge base statistics
python -m universe_explorer paths           # list all reading paths
python -m universe_explorer discover "q" --topic cosmology --adapter arxiv
python -m universe_explorer graph           # cross-domain graph report
python -m universe_explorer health          # integrity check all components
```

### Useful modules

```sh
python -m universe_explorer.dataops.arxiv_fetch     # fetch cited arXiv ids
python -m universe_explorer.dataops.arxiv_search "…"  # discovery → candidates/ only
python -m universe_explorer.discovery.pipeline "…"  # search → candidates → precheck → review.html
python -m universe_explorer.discovery.review        # regenerate dist/review.html
python -m universe_explorer.crossdomain.render_map  # regenerate dist/epistemic_map.html
python -m universe_explorer.reader.dashboard        # regenerate dist/dashboard.html
python -m universe_explorer.reader.stats            # structural inventory report
python -m universe_explorer.reader.export           # JSON/CSV/Markdown export (filtered)
python -m universe_explorer.reader.annotate         # tags/notes/labels → annotations/
python -m universe_explorer.reader.review           # checklist review workflow
python -m universe_explorer.reader.batch            # bulk export / tag / review-start / stats
python -m universe_explorer.reader.diff             # compare two claims field-by-field
python -m universe_explorer.reader.health_check     # integrity check all components
python -m universe_explorer.trust_behavior          # measure trust surfaces before trusting them
python -m universe_explorer.ui_expand               # measure domain-expand UX contracts
python -m universe_explorer.proposals               # mechanical status proposals
python -m universe_explorer.watch                   # diff vs snapshot/state.json
python -m universe_explorer.dataops.push            # events → outbox digests (restatement only)
python -m universe_explorer.dataops.push --deliver  # optional webhook/SMTP (env-gated)
python -m universe_explorer.dataops.source_health
```

CI: `.github/workflows/` — Pages deploy, source health, weekly pulse.

---

## Challenge a verdict (how to overturn us)

Core promise: **anyone with a checkable argument can overturn a light.**

1. Open [`claims.json`](https://taipei49314.github.io/universe-explorer/claims.json) or a claim card on the site.
2. Read `status_reason` against `STATUS_CONDITIONS` in `universe_explorer/model.py`.
3. Recompute the evidence axis with `axes.py` rules (or read `evidence_axis` + `axis_derivation` in the JSON).
4. Open a challenge with a checkable source:
   - On-site form: [`challenge.html`](https://taipei49314.github.io/universe-explorer/challenge.html) (static; routes into GitHub issue templates)  
   - **[Challenge a verdict](.github/ISSUE_TEMPLATE/challenge-a-verdict.yml)** — wrong light / wrong condition / misread source  
   - **[Challenge a relation](.github/ISSUE_TEMPLATE/challenge-a-relation.yml)** — wrong or missing edge  
   - **[Report a source problem](.github/ISSUE_TEMPLATE/report-a-source-problem.yml)** — fetch / hash / mis-cite  

A challenge **without a checkable source** (DOI / arXiv / journal) is itself an unsupported claim.

Successful challenges: data file edited → cite⇒fetch → `status_history` if light moves → `python run_tests.py` → feed / changes surface.  
Full path: [`CONTRIBUTING.md`](CONTRIBUTING.md) · editorial focus: [`docs/editorial-queue.md`](docs/editorial-queue.md)

---

## Product surfaces

| Surface | What |
|---------|------|
| `dist/dashboard.html` | Central hub — stats, status distribution, links to all pages |
| `dist/stats.json` | Machine-readable inventory (counts only; no confidence scores) |
| `dist/index.html` | Topic cards, expand, deep-link `?open=` |
| `dist/app.html` | Interactive map / Drift / ego graph / guides (`?c=` · `?path=`) |
| `dist/universe.html` | Constellation view |
| `dist/explore.html` (+ `-zh`) | Browse / export-oriented |
| `dist/explore-v2.html` | Search + filter + dual-axis reader (Phase 3) |
| `dist/epistemic_map.html` · `epistemic-graph.json` | Cross-domain graph (Phase 2; shared sources + authored edges + detectors) |
| `dist/challenge.html` | Standalone challenge form (links into GitHub issue templates) |
| `dist/dual-axis.svg` | Snapshot of consensus vs evidence across claims |
| `dist/review.html` | Discovery candidate review dashboard (editorial; never auto-writes claims) |
| `dist/zh.html` | Single-file Chinese edition |
| `dist/changes.html` | Recent restated events (P-Pulse) |
| `dist/health.html` · `health.json` | Inventory audit (P-Audit) |
| `dist/about.html` (+ `-zh`) | How to read · constitution · support |
| `dist/feed.xml` | Atom of change events (restates, never interprets) |

---

## What this is not

- Not a chatbot and not an LLM knowledge base  
- Not live NASA/ESA ingestion into claims (adapters deferred until a real inlet exists)  
- Not automatic light classification that replaces human status decisions  
- Not confidence scores, rankings, or “trust percentages”  
- Not auto-writing claim lights from annotations, review checklists, or batch tools

Knowledge grows by **human editorial hours** under the constitution — not by claim-count KPIs.

---

## License

- **Code:** MIT — [`LICENSE`](LICENSE)  
- **Content** (claim text, narratives, translations): CC BY — [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md)

---

## Docs map

| Doc | Role |
|-----|------|
| [`docs/constitution.md`](docs/constitution.md) | Consolidated laws |
| [`docs/design-framework.md`](docs/design-framework.md) | North star + roadmap history |
| [`docs/milestones-complete.md`](docs/milestones-complete.md) | Closeout board (P5b, R-Graph, …) |
| [`docs/product-remediation-7.md`](docs/product-remediation-7.md) | P-Read … P-Sustain |
| [`docs/amendment-*.md`](docs/) | Numbered constitution changes |
| [`docs/editorial-queue.md`](docs/editorial-queue.md) | What editors work on this season |
| [`docs/hawking-walkthrough.md`](docs/hawking-walkthrough.md) | Dual-axis stress case, data → UI |
| [`docs/trust-behavior-measure.md`](docs/trust-behavior-measure.md) | Measure first; trust only counted rows |
| [`docs/ui-expand-measure.md`](docs/ui-expand-measure.md) | Domain-expand measure gate |
| [`docs/north-star-v2-architecture.md`](docs/north-star-v2-architecture.md) | Discovery · cross-domain map · reader (Phase 1–3) |

---

*Completing a roadmap item does not invent confidence. Every claim still hangs on sources; every digest still restates events; every edge remains challengeable.*
