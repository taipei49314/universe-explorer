# Dark Matter — paper-grade research map

> Domain data: `universe_explorer/data/dark_matter.py`  
> Goal: a **review-article-shaped** knowledge map under Universe Explorer’s
> constitution — not a simulation code, not an AI summary of Wikipedia.

## 0. What “paper grade” means here

| Criterion | Rule |
|-----------|------|
| **Claim = thesis sentence** | One falsifiable or field-debated statement, not a topic label |
| **Sources first** | Every evidence line hangs on a fetch-verified arXiv/DOI primary or review |
| **Light ≠ hype** | Established only for *observations under GR*; candidates stay Frontier/Speculative |
| **Axes honest** | Strong consensus can sit on E3 (indirect cosmology); discovery claims need direct lines |
| **Camps only when real** | `competing_models` only for documented multi-year splits |
| **Open questions countable** | Reader can open them; no “confidence %” |
| **Cross-layer** | Lab (direct/collider/axion), sky (indirect/X-ray), and theory (WIMP/SIDM/fuzzy) all appear |

Non-goals:

- ❌ Declare which particle is dark matter  
- ❌ Forecast experimental winners  
- ❌ Stack every preprint — prefer **spine reviews + decisive measurements**

## 1. Paper outline ↔ claims

### I. Phenomenology (what must be explained)

| § | Claim id | Light | Role |
|---|----------|-------|------|
| I.1 | `mass_discrepancy_observed` | 🟢 | Mass gap under GR + luminous matter |
| I.2 | `lcdm_includes_cold_dm` | 🔵 | Cosmological cold non-baryonic component |

### II. Macroscopic interpretation

| § | Claim id | Light | Role |
|---|----------|-------|------|
| II.1 | `particle_vs_modified_gravity` | 🟡 | Halos vs MOND-like dynamics |
| II.2 | `small_scale_cdm_challenges` | 🟠 | Cusp/core, satellites, TBTF |

### III. Microphysics programmes

| § | Claim id | Light | Role |
|---|----------|-------|------|
| III.1 | `dm_particle_identity` | 🟠 | Identity still unknown |
| III.2 | `thermal_wimp_freezeout_benchmark` | 🟠 | Freeze-out / “WIMP miracle” as benchmark |
| III.3 | `axion_dm_candidate` | 🟠 | QCD axion / ALP |
| III.4 | `sidm_small_scales` | 🟠 | Self-interactions |
| III.5 | `fuzzy_wave_dark_matter` | 🟠 | Ultralight wave DM |
| III.6 | `sterile_neutrino_7kev_line` | 🔴 | 7 keV + 3.5 keV line claim |
| III.7 | `pbh_all_dark_matter` | 🔴 | PBHs as *all* DM |

### IV. Laboratory & collider channels

| § | Claim id | Light | Role |
|---|----------|-------|------|
| IV.1 | `direct_detection_wimp_searches` | 🟠 | Underground nuclear recoils |
| IV.2 | `neutrino_floor_direct_detection` | 🟠 | Irreducible ν coherent scattering floor |
| IV.3 | `monojet_collider_searches` | 🟠 | LHC mono-jet / MET |
| IV.4 | (axion lab) | — | Covered under `axion_dm_candidate` (ADMX) |
| IV.5 | `cluster_sidm_cross_section_bounds` | 🟠 | Merging-cluster σ/m bounds |

### V. Astrophysical / multi-messenger signals

| § | Claim id | Light | Role |
|---|----------|-------|------|
| V.1 | `fermi_gc_excess_origin` | 🟡 | GC GeV excess |
| V.2 | `dwarf_spheroidal_indirect_limits` | 🟠 | dSph γ-ray joint limits |
| V.3 | `s8_structure_tension_dark_sector` | 🟡 | S8 / growth tension vs new DM |

## 2. Citation spine (minimum reviews a paper-level map must touch)

1. Bertone & Tait 2018 — search landscape (`doi:10.1038/s41586-018-0542-z`)  
2. Planck 2018 VI — parameters (`arXiv:1807.06209`)  
3. Bullock & Boylan-Kolchin 2017 — small scales (`arXiv:1707.04256`)  
4. Tulin & Yu 2018 — SIDM (`arXiv:1705.02358`)  
5. Hui et al. 2017 — ultralight scalars (`arXiv:1610.08297`)  
6. LHC DM WG simplified models (`arXiv:1507.00966`)  
7. Direct-detection nulls — LZ / XENON class  
8. Fermi dSph / GC literature for indirect  

## 3. Depth rules when editing claims

1. Prefer **two independent experimental lines** for any 🟢 claim.  
2. For 🟠 candidate claims, always pair **motivation + null/constraint**.  
3. For 🔴 claims, include at least one **opposing** peer-reviewed source in `evidence` when the claim asserts a discovery.  
4. Never upgrade identity to Established because textbooks say “dark matter particle”.  
5. New claim → fetch arXiv/DOI → `run_tests.py` → `watch_all --commit` → rebuild.

## 4. Paper-ready checklist (human gate)

- [x] Outline §I–V each has ≥1 claim  
- [x] Every claim has real, fetched sources  
- [x] Lights span ≥3 colours; at least one 🟡 with `competing_models`  
- [x] ZH overlay covers all claim ids  
- [x] `python run_tests.py` green  
- [x] Topic summary reads like a structured abstract  

When all boxes hold, this domain is **map-complete for a review-shaped paper**; writing the prose paper is a separate human/authorship step outside the engine.

**Status (2026-08-09):** map-complete at **18 claims** (incl. cluster σ/m + neutrino floor).

Paper artifacts (auto-exported):

| Artifact | Path |
|----------|------|
| Claims summary | `docs/paper/dark-matter-claims-summary.md` |
| Open questions table | `docs/paper/dark-matter-open-questions.md` |
| Sources table | `docs/paper/dark-matter-sources.md` |
| Fig.1 light × evidence | `docs/paper/fig1-light-vs-evidence.svg` |

Regenerate: `python -m universe_explorer.dataops.export_dm_paper`
