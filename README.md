# Universe Explorer — v0 (black hole)

A knowledge-exploration system that honestly separates **what humanity knows**
from **what it does not**. v0 proves the epistemology on one real topic —
*black holes* — end to end, from sourced evidence to a plain web page.

It does not tell you the answer. It tells you: what we know, how we know it,
what we still don't, and which competing hypotheses exist.

## The constitution (hard red lines, enforced by code)

1. **Reference first, AI last.** `Data → Evidence → Knowledge → AI Narrative`,
   one-directional. AI sits at the bottom; no source, no upper-layer claim.
2. **AI does not declare facts**, it only organises recorded evidence. (v0 emits
   no AI narrative at all — only sourced structure — so it stays trivially inside
   this line.)
3. **No fake precision.** No confidence percentages, no numeric `open_questions`
   counts. Certainty must *emerge* from the evidence, never be declared.
4. **Every "known" claim hangs on a real source.** No source → demoted.

The **status light belongs to the Claim, not the Topic.** A topic is a container
with no light; claims under it can differ.

## Layout

```
universe_explorer/
  model.py            # frozen schema + the 5-cell taxonomy as machine-checkable conditions
  validator.py        # the constitution checker (mechanical)
  data/black_hole.py  # 4 hand-filled claims, real content, real sources
  render.py           # plain static-HTML renderer
build.py              # validate -> gate -> render (dist/index.html)
test_validator.py     # proves the validator actually catches violations
```

## Run

```sh
python test_validator.py     # v0: 12 tests — real data clean + every rule bites
python test_provenance.py    # P1: 8 tests — data-layer provenance rules bite
python test_axes.py          # P1.5: 7 tests — evidence axis emerges, never declared
python test_proposals.py     # P2: 8 tests — propose, never decide; audit trail
python test_watch.py         # P3: 7 tests — no silent light changes; events trace back
python test_p4.py            # P4: 8 tests — engine byte-frozen; ocean passes every gate
python test_narrative.py     # R6: 7 tests — every narrative sentence carries resolvable refs
python test_registry.py      # all gates x all topics, automatically for future domains
python test_push.py          # P5: 3 tests — digests restate, never interpret
                             # (test_validator includes Amendment #1: sourced % vs declared confidence)
python build.py              # both constitutions gate, then render dist/index.html
python build.py --check      # validate only
```

## P1 — Data-layer provenance (built on 2026-07-10)

Rule: **cite an arXiv source => you must actually have fetched it.**

```sh
python -m universe_explorer.dataops.arxiv_fetch      # fetch every cited arXiv id
python -m universe_explorer.dataops.arxiv_search "black hole islands"   # discovery inlet
```

- `cache/arxiv/` holds the official API responses **verbatim** (sha256-proven,
  no rewriting anywhere in the pipeline — there is no AI step at all).
- `cache/arxiv/manifest.json` records endpoint URL, UTC time, hash, and the
  verbatim title/authors for human eyeballing.
- The validator re-parses the cached XML itself (`provenance_id_mismatch`), so
  a manifest's self-report is not trusted.
- `candidates/` is a discovery inlet only: results stay pending forever; no code
  path writes a candidate into claim data. A human must edit the data file —
  and then the cite=>fetch rule takes over mechanically.
- Non-arXiv sources (textbooks, print journals, prize citations) are honestly
  exempt: no fetchable endpoint. The rule splits on "does an endpoint exist".

See [docs/p1-spec.md](docs/p1-spec.md) for the acceptance lines (defined before
the code was written) and [docs/design-framework.md](docs/design-framework.md)
for the whole-project frame.

## P1.5 — Two axes (built on 2026-07-10)

The consensus axis (five-cell light, human-judged, traceable) is now paired
with an **evidence axis that nobody fills in**: it is derived by public rules
(`axes.py`) over the recorded evidence items. The only way to move a claim on
it is to record new evidence — which the v0 constitution and the P1 cite=>fetch
rule police. `hawking_radiation` now shows its long-recorded tension
structurally: **Strong Consensus × E3 indirect/analog only → ⚡ axes diverge.**
Spec: [docs/p1.5-spec.md](docs/p1.5-spec.md).

## P2 — Semi-automatic status proposals (built on 2026-07-10)

`python -m universe_explorer.proposals` — a mechanical engine that **proposes,
never decides**: it marks which lights are compatible with the recorded
evidence, may *exclude* a light on a hard contradiction (never approve one),
answers "cannot judge — needs a human" for every human-only condition (textbook
acceptance, real scientific camps...), and writes nothing into claim data.
Human decisions over proposals go to an append-only audit log
(`audit/decisions.jsonl`) via `--decide <claim> accept|reject <name> <reason>`.
Spec: [docs/p2-spec.md](docs/p2-spec.md).

## P3 — Change detection (built on 2026-07-10)

`python -m universe_explorer.watch` — diffs the current knowledge state against
the committed snapshot (`snapshot/state.json`); differences become event files
(`events/*.json`, the trigger interface for future push channels) carrying
before/after values and the mechanical derivation, no interpretation. New
constitution rule, build-blocking: **lights may change, never silently** — a
status change without a matching `status_history` entry is
`undocumented_status_change`. Snapshot updates only on explicit `--commit`.
Spec: [docs/p3-spec.md](docs/p3-spec.md).

## P4 — Cross-domain: same engine, new domain (built on 2026-07-10)

A second topic — **the deep ocean** — runs through the identical engine with
**zero edits to the six engine files** (`model`, `validator`, `axes`,
`provenance`, `proposals`, `watch`), verified byte-for-byte against
`engine_hashes.json`. Only the Data layer changed: `data/ocean.py` +
`data/registry.py`, plus build/render wiring. Every source was verified online
before being written (Corliss 1979, Spiess 1980, Caesar 2018, Worthington 2021,
Rabone 2023, Sweetman 2024, Frontiers 2025) — none from memory. The AMOC claim
finally exercises `competing_models` on a real two-camp dispute (retiring
tension R4), and dark-oxygen production shows the reverse combo — a single
direct observation (E2) under a 🔴 Speculative light. `python build.py` now
renders an index over both topics. Spec: [docs/p4-spec.md](docs/p4-spec.md).

Note: P4 surfaced tension **R7** — resolved by **Amendment #1**
([docs/amendment-1-r7.md](docs/amendment-1-r7.md)): evidence descriptions
(which are forced to hang on real sources) may carry measured percentages;
declared-confidence vocabulary stays banned everywhere, evidence included.

## R6 — AI Narrative layer (built on 2026-07-10)

The fourth layer, finally filled in — under the constitution's terms. Every
narrative sentence must carry refs resolving to the claim's sources or
status_reason conditions; the mandated opening is "Based on the evidence
recorded here"; percentages only as verbatim quotes of evidence descriptions;
if the gate rejects anything, the whole narrative is withheld (rather absent
than overreaching). Composer and checker are separate: today's composer is a
mechanical assembler; a future LLM composer must pass the **same** `check()`.
Spec: [docs/r6-narrative-spec.md](docs/r6-narrative-spec.md).

## Third domain — Exoplanets (built on 2026-07-10)

`data/exoplanets.py`: 🟢 they exist (RV + transit, independent) / 🟡 Planet
Nine (clustering real vs survey bias — a second real `competing_models`) /
🟠 TRAPPIST-1 b bare rock (JWST era just opening) / 🔴 K2-18 b biosignature
(observation exists, mainstream unconvinced). Six new arXiv sources verified
online and fetched through the P1 pipeline (manifest now 14 records).
`test_registry.py` holds every current and future domain to every gate.

## Amendment #2 — Narrative localization (2026-07-10)

Language is a presentation property; the gate is a structural property.
`narrative.py` gained a `Localization` seam — sentence templates + evidence-text
access per language — and `check()` now takes the localization too, so a Chinese
(or any) narrative passes the **same court**: per-sentence refs, the localized
constitutional opening (「根據目前收錄的證據」), percentages only as verbatim
quotes of the localized evidence text. The Chinese localization lives in the
data layer (`data/translations_zh.py`); the engine knows the protocol, never a
language. Default calls behave exactly as before. This is the fourth
"swap the smart part, never the court" seam (P2 proposer, R6 composer, R6
narrative-checker, now language). Spec:
[docs/amendment-2-narrative-i18n.md](docs/amendment-2-narrative-i18n.md).

The bilingual artifact generator is [dataops_artifact.py](dataops_artifact.py)
(`python dataops_artifact.py out.html [en|zh]`).

## P5 (partial) — Push channel (built on 2026-07-10)

`python -m universe_explorer.dataops.watch_all` watches all topics (wiring over
the frozen engine); `python -m universe_explorer.dataops.push` turns event
files into digests in `outbox/` — restating before/after values, never
interpreting, each line naming the event file that traces back to the
derivation. No events => silence. Real transport (SMTP/webhook) and NASA/ESA
adapters are deliberately not wired: sending is deployment, digesting is model.

To view the page: `python -m http.server 8731 --directory universe-explorer/dist`
then open <http://localhost:8731>.

## The four claims (they carry three... four different lights)

| Claim | Light | Status |
|---|---|---|
| `event_horizon_exists` | 🟢 | Established Consensus |
| `hawking_radiation` | 🔵 | Strong Consensus |
| `information_paradox` | 🟠 | Frontier Research |
| `firewall` | 🔴 | Speculative |

`hawking_radiation` is the deliberate stress case: theoretical consensus is very
strong while direct astrophysical evidence is essentially zero. That split is
**recorded in `status_reason`, not forced onto one light** — the frozen spec
leaves axis-splitting (consensus strength vs evidence strength) to a later
version.

## v0 acceptance (spec §6) — result

1. **Zero constitution violations** — `build.py` reports PASS on all 4 claims.
2. **Light divergence holds** — 4 distinct lights across 4 claims, proving the
   light belongs to the claim, not the topic.
3. **Traceability holds** — each `status_reason` is a condition-by-condition
   list a third party can check against §3 and overturn; `test_validator.py`
   shows the checker fails a claim whose reasons don't cover its status.
4. **Knowledge shape is visible** — the page reads bedrock-first: a 🟢 base
   (the horizon exists) under a 🔴 ceiling (the firewall), not one averaged blob.

> v0 passing = the epistemology stands up on one real topic. It does **not** mean
> the system is complete or shippable — real automated ingestion (NASA/ESA/arXiv)
> is v1 and is intentionally not built here.

## Deliberately NOT in v0

No live API ingestion, no 3D/orbit simulation, no daily push (the
`status_history` field is kept as its future trigger), no persona debate, no
ocean topic, no automatic light classification. v0 proves *traceable human
judgement* as the foundation; automated classification is v1.
