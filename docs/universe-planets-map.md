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

## Cosmology claim map (incl. deepened H0 cluster)

| Light | Claim id | Role |
|:-----:|----------|------|
| 🟢 | `universe_is_expanding` | Expansion bedrock |
| 🟢 | `cmb_hot_big_bang` | Hot big bang / CMB |
| 🔵 | `accelerated_expansion` | Late-time acceleration |
| 🟡 | `H0_tension_local_vs_cmb` | **Umbrella** local vs CMB+ΛCDM |
| 🟠 | `shoes_local_H0_high` | Cepheid–SN (SH0ES) high local H0 |
| 🟠 | `cmb_lcdm_implies_low_H0` | Planck ΛCDM low H0 pole |
| 🟡 | `trgb_vs_cepheid_local_H0` | **Local calibrator split** |
| 🟠 | `early_dark_energy_H0_fix` | Proposed early-universe fix |
| 🟠 | `strong_lensing_time_delay_H0` | Geometric H0LiCOW/TDCOSMO |
| 🟠 | `standard_sirens_H0` | GW170817-style sirens |
| 🟠 | `cosmic_inflation_early_universe` | Inflation umbrella |
| 🟠 | `inflation_slow_roll_planck` | Planck slow-roll preference |
| 🟠 | `primordial_tensors_undetected` | B-mode / r upper limits |
| 🟡 | `inflation_vs_noninflation_alts` | Inflation vs bounce-class alts |
| 🔴 | `eternal_inflation_multiverse` | Multiverse reading |
| 🔴 | `cyclic_or_bounce_replaces_bb` | Bounce as replacement |

**H0 reading order:** umbrella 🟡 → two poles (SH0ES / CMB+ΛCDM) → local split (TRGB vs Cepheid) → relief routes (EDE, lensing, sirens).

**Boundary with dark_matter:** cosmology owns expansion / CMB / H0 / inflation; dark_matter owns mass discrepancy, particle candidates, and lab channels. Cross-link H0 ↔ S8 in prose only.

## Planets claim map (incl. ocean-worlds cluster)

| Light | Claim id |
|:-----:|----------|
| 🟢 | `solar_system_age` |
| 🔵 | `moon_giant_impact` |
| 🟡 | `late_heavy_bombardment` |
| 🟠 | `ocean_worlds_icy_moons` (umbrella) |
| 🟠 | `europa_induced_field_ocean` |
| 🟠 | `enceladus_plume_global_ocean` |
| 🟠 | `titan_subsurface_ocean` |
| 🟠 | `enceladus_plume_organics` |
| 🔴 | `ocean_world_life_today` |
| 🔴 | `mars_sustained_surface_habitability_now` |

**Boundary with exoplanets:** `planets` = solar system + formation chronology; `exoplanets` = other stars (existence, Planet Nine, JWST atmospheres, biosignature claims).

**Discussion prose (near-final English, Author Year):**

| Topic | Path |
|-------|------|
| H0 tension | `docs/paper/h0-discussion.md` |
| Ocean worlds | `docs/paper/ocean-worlds-discussion.md` |
| Cosmic inflation | `docs/paper/inflation-discussion.md` |

## Paper / narrative hooks

- Extended abstract can open with Q-set: *How does the universe evolve? What is most of the matter? What are planets, here and elsewhere?*
- Fig.1-style exports can be re-run per domain; umbrella Fig optional later.
- Chinese site chrome already says 跨領域; topic titles in `translations_zh.py`.

## Maintenance

1. Edit `universe_explorer/data/cosmology.py` or `planets.py`  
2. Fetch arXiv/DOI → `run_tests.py`  
3. `watch_all --commit` · `build.py`  
4. Keep lights honest: do not promote inflation or present-day Mars habitability.
