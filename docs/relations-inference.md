# Claim relations & inference

> **Edges are recorded. Paths are listed. Nothing is a confidence score.**

## Why this exists

The map already shows *what* each claim says. Relations show **how claims sit next to each other** — supports, presuppositions, specialisations, tensions, and honest domain boundaries — so a reader can follow structure without an AI inventing a verdict.

## Edge kinds (discrete)

| Kind | Meaning |
|------|---------|
| `supports` | A strengthens the reading of B |
| `requires` | A is an epistemic presupposition of B |
| `specializes` | A is a pole / sub-claim under umbrella B |
| `tensions` | A and B sit in structured tension |
| `boundary` | Cross-domain adjacency (map honesty) |
| `shares_source` | **Mechanical:** same arXiv/DOI key |
| `co_topic` | Reserved mechanical same-topic (weak) |

No continuous weights. No `confidence` / `score` / `probability` / `trust`.

## Origins

1. **Authored** — human notes in `universe_explorer/relations.py` (`_AUTHORED`).
2. **Mechanical** — shared normalised source keys; only added when no authored edge already connects the pair.

AI may not write edges into the graph.

## Inference

For claim C, the engine:

1. Lists **direct neighbours** (outbound + inbound with inverse labels).
2. Lists **paths of depth ≤ 2** over *authored* edges (undirected walk for reachability; kinds recorded as traversed).
3. Attaches titles/lights for display only.

An inference path is a **route you can recount**, not a proof and not a ranking.

```sh
python -m universe_explorer.relations --validate
python -m universe_explorer.relations --claim H0_tension_local_vs_cmb
python -m universe_explorer.relations --claim stars_powered_by_fusion
python test_relations.py
```

## Frontend

- `app-data.json` → each claim has `related`, `inferences`, `n_related`, `n_inferences`.
- Top-level `relations` block: kinds, labels, full `links` list, counts,
  **`reading_paths`**, **`coverage`**.
- Knowledge map: **R-Graph** ego neighbourhood SVG + reading-path chips
  (see `docs/r-graph.md`).
- Knowledge map + Drift panels: **Related claims** and **Inference paths**; click navigates to the neighbour claim.
- Opt-in measure: `relation_nav` / `reading_path` events when `?measure=1`.
- Challenge an edge: GitHub template `challenge-a-relation.yml`.

## Growing the graph

Add a tuple to `_AUTHORED`:

```python
("source_claim_id", "target_claim_id", "kind", "one-line note"),
```

Then:

```sh
python -m universe_explorer.relations --validate
python run_tests.py
```

Prefer sparse, high-signal edges over a dense hairball. Every note must be something a third party can challenge.
