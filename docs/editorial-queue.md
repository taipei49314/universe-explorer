# Editorial queue (P-Edit)

> Content grows by **human hours**, not claim-count KPIs.  
> This file is the living queue — update when the season or focus changes.

## This season (2026-Q3)

| Role | Domain | Goal |
|------|--------|------|
| **Primary** | `cosmology` (H0 cluster) | Keep Discussion honest; process challenges |
| **Secondary** | `seismology` | Prediction-vs-forecast narrative polish |

All other domains: bugfixes and challenges only unless a critical source update lands.

## Domain shape SLA (minimum honest map)

Each domain should either cover the five light layers or **explicitly note** a missing layer.

| Domain | 🟢 | 🔵 | 🟡 | 🟠 | 🔴 | Notes |
|--------|----|----|----|----|----|-------|
| black_hole | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| cosmology | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| dark_matter | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| stars | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| exoplanets | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| planets | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| ocean | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| seismology | ✓ | ✓ | ✓ | ✓ | ✓ | OK |
| polar | ✓ | ✓ | ✓ | ✓ | ✓ | 南北極 · 8 claims (2026-08-11) |

## Weekly ritual (suggested N = 3)

**Write-up location:** [`docs/weeklies/YYYY-Www.md`](weeklies/README.md) (required each ISO week).

1. Open `candidates/` — process up to **3** files (accept → claim draft path, or reject → `candidates/rejected/` with weekly note).  
2. Run `python -m universe_explorer.dataops.source_health` (or wait for Action).  
3. If events: `python -m universe_explorer.dataops.push` (+ `--deliver` if webhook set).  
4. If data changed: `python run_tests.py` · `python build.py` · commit.  
5. If nothing moved: record **legal silence** in that week's weekly file (not a fake commit).  
6. Check Trust Loop panel: `health.html#trust-loop` / `changes.html#overturn` (counts only).

## Challenge intake

| Label | Action |
|-------|--------|
| `challenge` | Human re-reads status_reason vs taxonomy |
| `relation` | Human re-reads edge kind + note |
| accepted | Edit `data/*.py`, `status_history` if light moves, fetch sources, tests, watch commit |

## Anti-goals

- No quarterly target of “+20 claims”.  
- No LLM batch write of claims into `data/`.  
- Sparse relations remain honest; do not densify to look complete.
