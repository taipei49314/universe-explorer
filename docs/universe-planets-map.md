# Theme expansion — 宇宙 (universe) · 星球 (planets)

Umbrella map for the expanded research theme beyond dark matter alone.  
Engine: same constitution; each domain is still a `Topic` of atomic claims.

## Domain clusters

| Theme | Domain id | Role | Seed scale |
|-------|-----------|------|------------|
| **宇宙** | `cosmology` | Expansion, CMB, acceleration, H0, inflation | 6 claims |
| **宇宙** | `dark_matter` | Mass discrepancy → particle searches | 18 claims (paper-grade) |
| **宇宙** | `black_hole` | Compact objects / horizons | 5 claims |
| **星球** | `planets` | Solar system age, Moon, bombardment, ocean worlds | 5 claims |
| **星球** | `exoplanets` | Planets around other stars | 7 claims |
| **地球** | `ocean` / `seismology` | Earth systems (unchanged) | 5+5 |

```
                    ┌─ cosmology ──────────── 宇宙 large-scale
  宇宙 Cosmos ──────┼─ dark_matter ────────── matter budget / identity
                    └─ black_hole ─────────── strong gravity endpoints

  星球 Planets ─────┬─ planets ────────────── our system + formation
                    └─ exoplanets ─────────── other stars

  地球 Earth ───────┬─ ocean
                    └─ seismology
```

## Cosmology claim map (new)

| Light | Claim id |
|:-----:|----------|
| 🟢 | `universe_is_expanding` |
| 🟢 | `cmb_hot_big_bang` |
| 🔵 | `accelerated_expansion` |
| 🟡 | `H0_tension_local_vs_cmb` |
| 🟠 | `cosmic_inflation_early_universe` |
| 🔴 | `cyclic_or_bounce_replaces_bb` |

**Boundary with dark_matter:** cosmology owns expansion / CMB / H0 / inflation; dark_matter owns mass discrepancy, particle candidates, and lab channels. Cross-link H0 ↔ S8 in prose only.

## Planets claim map (new)

| Light | Claim id |
|:-----:|----------|
| 🟢 | `solar_system_age` |
| 🔵 | `moon_giant_impact` |
| 🟡 | `late_heavy_bombardment` |
| 🟠 | `ocean_worlds_icy_moons` |
| 🔴 | `mars_sustained_surface_habitability_now` |

**Boundary with exoplanets:** `planets` = solar system + formation chronology; `exoplanets` = other stars (existence, Planet Nine, JWST atmospheres, biosignature claims).

## Paper / narrative hooks

- Extended abstract can open with Q-set: *How does the universe evolve? What is most of the matter? What are planets, here and elsewhere?*
- Fig.1-style exports can be re-run per domain; umbrella Fig optional later.
- Chinese site chrome already says 跨領域; topic titles in `translations_zh.py`.

## Maintenance

1. Edit `universe_explorer/data/cosmology.py` or `planets.py`  
2. Fetch arXiv/DOI → `run_tests.py`  
3. `watch_all --commit` · `build.py`  
4. Keep lights honest: do not promote inflation or present-day Mars habitability.
