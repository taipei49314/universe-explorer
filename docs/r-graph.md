# R-Graph — relations as a first-class product surface

**Milestone status:** implemented (knowledge map).  
**Constitution:** edges and paths are **listed**; nothing is a confidence score.

## What shipped

| Surface | Behaviour |
|---------|-----------|
| **Ego graph** | Select a claim → polar neighbourhood of recorded neighbours; edge kinds colour-coded; click node opens claim |
| **Reading paths** | Authored sequences (H0, stars, black holes, dark matter, exoplanets, ocean, seismology, planets) — not rankings |
| **Panel** | Related list + inference paths + **challenge an edge** link |
| **Data** | `app-data.json` → `relations.reading_paths`, `relations.coverage` |
| **Challenge** | `.github/ISSUE_TEMPLATE/challenge-a-relation.yml` |
| **Measure** | `?measure=1` → `relation_nav` (surface=`rgraph`), `reading_path` |

## Coverage (sparse honesty)

`relations.coverage` reports:

- `n_with_authored_edge` / `n_claims`
- `n_isolated_authored`
- `authored_degree_hist` (0 / 1 / 2 / 3+)
- `n_reading_paths`

Isolation is **honest sparsity**, not a defect. Do not densify the graph to “look complete.”

```sh
python -m universe_explorer.relations --validate
python -m universe_explorer.relations --claim event_horizon_exists
python test_relations.py
```

## Edge colours (map graph)

| Kind | Style |
|------|--------|
| supports | green-ish |
| requires | blue-ish |
| specializes | accent |
| tensions | competing gold |
| boundary | speculative dash |
| shares_source | muted dash |

## Acceptance (milestone checklist)

1. [x] Ego graph on `app.html` for selected claim  
2. [x] ≥3 authored reading paths (actually 5)  
3. [x] Measure events for graph nav + path steps  
4. [x] Issue template for edge challenges  
5. [x] Coverage counts in data + UI line  
6. [x] Tests green; no confidence fields  

## Non-goals (still hold)

- No LLM auto-edges  
- No edge weights  
- No forced complete graph  
- Drift view keeps list-level relations (full ego SVG is map-first)  
