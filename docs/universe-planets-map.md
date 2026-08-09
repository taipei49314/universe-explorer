# Theme expansion — 宇宙 (universe) · 星球 (planets)

Umbrella map for the expanded research theme beyond dark matter alone.  
Engine: same constitution; each domain is still a `Topic` of atomic claims.

## Domain clusters

| Theme | Domain id | Role | Seed scale |
|-------|-----------|------|------------|
| **宇宙** | `cosmology` | Expansion, CMB, H0, inflation | 16 claims |
| **宇宙** | `dark_matter` | Mass discrepancy → particle searches | 18 claims |
| **宇宙** | `black_hole` | Horizons → Kerr → populations → ceilings | 10 claims |
| **宇宙** | `stars` | Fusion → solar interior → death channels | 12 claims |
| **星球** | `planets` | Solar system + ocean worlds | 10 claims |
| **星球** | `exoplanets` | Other stars; radius valley; JWST | 9 claims |
| **地球** | `ocean` / `seismology` | Earth systems (deepened) | 8+8 |

```
                    ┌─ cosmology ──────────── large-scale / H0 / inflation
  宇宙 Cosmos ──────┼─ dark_matter ────────── matter budget / identity
                    ├─ black_hole ─────────── horizons / Kerr / GW / ceilings (deepened)
                    └─ stars ──────────────── stellar physics (deepened)

  星球 Planets ─────┬─ planets ────────────── solar system + ocean worlds
                    └─ exoplanets ─────────── other stars + atmospheres

  地球 Earth ───────┬─ ocean
                    └─ seismology
```

## Black hole claim map (deepened)

| Light | Claim id | Role |
|:-----:|----------|------|
| 🟢 | `event_horizon_exists` | Horizon bedrock (EHT + GW + Sgr A*) |
| 🔵 | `hawking_radiation` | Thermal evaporation (theory + analogue) |
| 🔵 | `kerr_describes_astrophysical_bh` | Kerr mass+spin working spacetime |
| 🔵 | `smbh_common_in_galaxy_nuclei` | Nuclear SMBHs in massive galaxies |
| 🟡 | `lower_mass_gap_compact_objects` | NS–BH lower mass gap debate |
| 🟠 | `bbh_mergers_catalogued` | GW catalogue population science |
| 🟠 | `jets_extract_bh_spin` | Blandford–Znajek–type jet power |
| 🟠 | `information_paradox` | Unitary evaporation / islands |
| 🔴 | `firewall` | Horizon firewall (not accepted) |
| 🔴 | `horizonless_gw_echoes` | Established GW echoes (not accepted) |

**Discussion:** `docs/paper/black-hole-discussion.md`.  
**Boundary:** upper (PISN) mass gap → `stars`; PBH-as-all-DM → `dark_matter`.

## Stars claim map (deepened)

| Light | Claim id | Role |
|:-----:|----------|------|
| 🟢 | `stars_powered_by_fusion` | Fusion bedrock (solar ν) |
| 🔵 | `stellar_nucleosynthesis_makes_elements` | Elements beyond He |
| 🔵 | `core_collapse_forms_ns_bh` | NS/BH remnants |
| 🔵 | `helioseismology_constrains_solar_interior` | Seismic solar interior |
| 🔵 | `white_dwarfs_electron_degenerate` | WD degeneracy support |
| 🔵 | `imf_approximately_universal` | Local IMF default |
| 🟡 | `red_supergiant_problem` | Missing high-mass RSG SN progenitors |
| 🟡 | `sn_ia_progenitor_channels` | SD vs DD for Type Ia |
| 🟠 | `solar_dynamo_cycle` | 11-yr dynamo detail |
| 🟠 | `cno_cycle_solar_neutrinos_detected` | Borexino CNO ν |
| 🟠 | `pair_instability_bh_mass_gap` | PISN BH mass gap |
| 🔴 | `pop_iii_already_routinely_observed` | Local Pop III (not accepted) |

**Reading order:** fusion 🟢 → Strong shelf (nucleosynthesis / remnants / helioseismology / WD / IMF) → yellow death-channel debates (RSG, SN Ia) → orange programmes (dynamo, CNO, PISN gap) → red ceiling.

**Discussion prose:** `docs/paper/stars-discussion.md`.

**Boundaries:** horizons → `black_hole`; \(H_0\) / CMB → `cosmology`; other stars’ planets → `exoplanets`.

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

## Exoplanets claim map

| Light | Claim id | Role |
|:-----:|----------|------|
| 🟢 | `exoplanets_exist` | Existence bedrock (RV + transit) |
| 🟢 | `proxima_b_exists` | Nearest-star temperate planet |
| 🔵 | `planets_are_common` | Demographic abundance |
| 🟡 | `planet_nine` | Distant giant vs survey bias |
| 🟡 | `radius_valley_mechanism` | Photoevaporation vs core-powered |
| 🟠 | `trappist1b_bare_rock` | JWST TRAPPIST-1 b airless |
| 🟠 | `trappist1_inner_planets_airless` | Inner pair atmospheres |
| 🟠 | `jwst_exoplanet_atmospheres` | Transmission spectroscopy era |
| 🔴 | `k2_18b_biosignature` | DMS-as-life (not accepted) |

**Discussion:** `docs/paper/exoplanets-discussion.md`.

**Discussion prose (near-final English, Author Year):**

| Topic | Path |
|-------|------|
| H0 tension | `docs/paper/h0-discussion.md` |
| Ocean worlds | `docs/paper/ocean-worlds-discussion.md` |
| Cosmic inflation | `docs/paper/inflation-discussion.md` |
| Stars (deepened) | `docs/paper/stars-discussion.md` |
| Black holes (deepened) | `docs/paper/black-hole-discussion.md` |
| Exoplanets | `docs/paper/exoplanets-discussion.md` |
| Deep ocean | `docs/paper/ocean-discussion.md` |
| Earthquakes | `docs/paper/seismology-discussion.md` |

## Paper / narrative hooks

- Extended abstract can open with Q-set: *How does the universe evolve? What is most of the matter? What are planets, here and elsewhere?*
- Fig.1-style exports can be re-run per domain; umbrella Fig optional later.
- Chinese site chrome already says 跨領域; topic titles in `translations_zh.py`.

## Maintenance

1. Edit `universe_explorer/data/cosmology.py` or `planets.py`  
2. Fetch arXiv/DOI → `run_tests.py`  
3. `watch_all --commit` · `build.py`  
4. Keep lights honest: do not promote inflation or present-day Mars habitability.
