# Dark matter: what is established, what competes, and what remains open

**Manuscript skeleton — Introduction + Discussion only**  
Status: draft scaffold (2026-08-09) · Claims source: `universe_explorer/data/dark_matter.py` (18 claims)  
Companion artifacts: `dark-matter-paper-map.md` · `fig1-light-vs-evidence.svg` · open-questions & sources tables  

> **How to use this file**  
> - Prose in normal text is *starter wording* (editable).  
> - `[FILL: …]` = author must write / verify.  
> - `` `claim_id` `` = must stay consistent with the knowledge map; do not upgrade a 🔴/🟠 claim to “known fact” in prose.  
> - No confidence percentages. Lights and evidence grades are structural, not rhetorical flourishes.

---

## Title options (pick one)

1. *Separating the mass discrepancy from the particle: an epistemically stratified map of dark matter*  
2. *What we know, what we debate, and what we have not found: dark matter across phenomenology, microphysics, and experiment*  
3. `[FILL: shorter journal-style title]`

**Running head:** Known / unknown structure of dark matter  

**Authors / affiliation / corresponding author:** `[FILL]`  

**Keywords:** dark matter; ΛCDM; direct detection; indirect detection; modified dynamics; axions; self-interacting dark matter; fuzzy dark matter; open science knowledge maps  

---

## Abstract (skeleton — write last)

**Background.** `[FILL: 1–2 sentences on mass discrepancy + cosmology.]`  

**Approach.** We organise the dark-matter problem as a set of **atomic claims**, each carrying (i) a consensus light fixed by explicit entry conditions and (ii) an **evidence grade** derived mechanically from recorded evidence types—not declared as a confidence score (Fig. 1).  

**Results (map, not discovery).**  
- 🟢 Established: mass discrepancy under GR + luminous matter alone (`mass_discrepancy_observed`, E1).  
- 🔵 Strong: non-baryonic cold component in the standard cosmology (`lcdm_includes_cold_dm`, E3; **axes diverge**).  
- 🟡 Competing: particle halos vs modified dynamics; GC excess origin; S8 vs systematics.  
- 🟠 Frontier: identity, WIMP benchmark, lab/collider nulls, small-scale programmes, axions, SIDM, fuzzy DM, dSph limits, cluster σ/m, neutrino floor.  
- 🔴 Speculative: 7 keV sterile-neutrino line claim; PBHs as *all* DM.  

**Conclusions.** `[FILL: one sentence — identity unknown; channels constrain without identifying; do not conflate cosmology success with particle ID.]`  

**Word budget:** abstract ≤ 200–250 words when filled.

---

# 1. Introduction

## 1.1 The problem is not a single question

Dark matter is often introduced as one mystery. In practice the literature mixes **several logically distinct questions**:

| # | Question | Map home |
|---|----------|----------|
| Q1 | Is there a mass/gravity discrepancy once luminous matter and GR are fixed? | §I phenomenology |
| Q2 | Does the standard cosmological model require a cold non-baryonic component? | §I cosmology |
| Q3 | Are galactic regularities better read as particle halos or modified dynamics? | §II interpretation |
| Q4 | What is the microphysical identity (if any)? | §III |
| Q5 | What do laboratory, collider, and astrophysical channels actually constrain? | §IV–V |

Conflating Q1–Q5 produces category errors: textbook language that “dark matter exists” can mean the **discrepancy** (often strongly supported) or a **particle species** (still unidentified). This paper keeps those layers separate.

**Claim anchors.** Q1 → `mass_discrepancy_observed` 🟢E1 · Q2 → `lcdm_includes_cold_dm` 🔵E3 · Q3 → `particle_vs_modified_gravity` 🟡 · Q4 → `dm_particle_identity` 🟠 · Q5 → lab/indirect cluster of 🟠/🟡 claims.

## 1.2 Why another review-shaped document?

Standard reviews already cover WIMPs, axions, SIDM, and searches in depth `[FILL: cite Bertone & Tait 2018; Arcadi et al.; PDG; Bullock & Boylan-Kolchin; Tulin & Yu; Hui et al.]`.  

What is still easy to lose—especially across communities—is the **epistemic shape** of the field:

1. **Consensus strength** and **evidence directness** are not the same axis.  
   Example: ΛCDM’s cold component is mainstream (`lcdm_includes_cold_dm` 🔵) yet sits on **indirect** cosmological inference (E3)—a documented **divergence** (Fig. 1).  
2. **Null results** (direct detection, mono-jet, dSph γ-rays) are scientific knowledge, not “absence of science.”  
3. **Competing models** are only listed where the literature hosts multi-year camps, not rhetorical binaries.  
4. **Speculative** claims (e.g. all-DM PBHs; 7 keV line as sterile-neutrino DM) must remain labelled as such even when they generate high citation traffic.

**Contribution of this work.** We present a **claim-level map** of the dark-matter problem in which each thesis sentence is tied to verified sources and dual axes (consensus light × evidence grade). The map is implemented as open, test-gated data (`dark_matter` domain); this manuscript supplies the narrative Intro/Discussion that a review reader expects around that map.

`[FILL: 1 paragraph on audience — particle physics / cosmology / cross-disciplinary.]`

## 1.3 Scope and non-goals

**In scope.**

- Observational mass discrepancy and cosmological cold component.  
- Macroscopic interpretation (particle vs modified dynamics; small-scale challenges).  
- Leading microphysical programmes: thermal WIMP benchmark, axions/ALPs, SIDM, fuzzy/wave DM.  
- Laboratory and collider channels: direct detection, neutrino floor, mono-jet/MET.  
- Astrophysical signals and tensions: dSph limits, GC excess, S8.  
- Explicitly speculative corners: 3.5 keV / 7 keV sterile neutrino; PBHs as *all* DM.

**Out of scope (deliberate).**

- Exhaustive model zoo or every simplified-model operator.  
- New statistical reanalysis of public datasets.  
- Declaring a “most promising” experiment or particle.  
- Continuous confidence scores or ranking of theories by hype.

`[FILL: ethics / data availability — point to GitHub claim files + arXiv/DOI cache policy.]`

## 1.4 Reading guide and figure

**Fig. 1** places each claim in the plane of **evidence grade** (E1–E5, derived from recorded evidence types) versus **consensus light** (Established → Speculative).  

How to read Fig. 1:

- **Bottom-left / E1+🟢:** bedrock phenomenology with multiple independent direct lines.  
- **High consensus + weak evidence (divergence):** treat carefully—strong belief, less direct contact.  
- **🟡 band:** live scientific splits; prose must present both camps.  
- **Upper 🔴:** not mainstream conclusions; useful as boundaries of speculation.

Section order of the paper follows the map outline (§I–V in `dark-matter-paper-map.md`). Body sections (Results / claim-by-claim) may be expanded from the data layer later; **this skeleton prioritises Introduction and Discussion.**

## 1.5 Roadmap of the manuscript

- **§2 Methods (optional short):** claim schema, dual axes, provenance rule (cite ⇒ fetch). `[FILL or move to Supplementary]`  
- **§3–7 Results:** one subsection per map block (I–V), each ending with open questions.  
- **§8 Discussion:** synthesis (below).  
- **§9 Conclusions:** five sentences max.  
- **Data availability / Code:** link to domain data and export tables.

---

# 8. Discussion

> Numbered as §8 assuming Results occupy §3–7. Renumber freely.

## 8.1 The knowledge shape in one paragraph

The map’s shape is not accidental. A **narrow green/blue base** (discrepancy + cosmological cold component) supports a **wide orange frontier** (identity and search programmes) under a **thin red ceiling** (claims that assert a specific exotic identification without field acceptance). Three **yellow** nodes mark durable camps: particle vs MOND-like dynamics; GC excess origin; S8 dark-sector vs systematics. That geometry—few bedrock facts, many constrained unknowns—is the honest status of the field as of the claim freeze date `[FILL: freeze date / Planck+DES+LZ generation]`.

## 8.2 Do not promote cosmology into particle physics

`lcdm_includes_cold_dm` is **Strong** and **E3**. Success of ΛCDM on CMB and large-scale structure is real knowledge, but it does **not** identify a particle, does **not** by itself refute every modified-dynamics programme at galactic scales, and does **not** license treating WIMP or axion parameter points as established.  

Conversely, laboratory nulls (`direct_detection_wimp_searches`, `monojet_collider_searches`, `dwarf_spheroidal_indirect_limits`) do not falsify the **mass discrepancy**. They falsify or constrain **classes of couplings and masses**. Discussion language should track that scope.

**Discussion takeaway A.** *Cosmological cold DM ≠ identified particle ≠ dead modified dynamics.*

## 8.3 The three competitions that are not “noise”

### 8.3.1 Particle dark matter vs modified dynamics  
(`particle_vs_modified_gravity` 🟡)

Clusters and cosmology (including offset lensing mass in merging systems) pressure pure gravity-only explanations; galactic scaling laws keep MOND-like programmes alive. Prose must not pick a winner. Cross-links: small-scale CDM challenges (`small_scale_cdm_challenges`); cluster σ/m (`cluster_sidm_cross_section_bounds`); SIDM as a particle-side response (`sidm_small_scales`).

**Open (select 2–3 for the printed table):**  
- Relativistic completions of MOND vs CMB/cluster data.  
- How much small-scale tension is baryonic feedback vs new dark physics.  
- `[FILL: one observational programme you will emphasise]`

### 8.3.2 Galactic Centre excess  
(`fermi_gc_excess_origin` 🟡)

DM annihilation versus unresolved astrophysics (e.g. MSPs) remains open after years of template and statistical work. Cross-link: dSph joint limits (`dwarf_spheroidal_indirect_limits`) as a cleaner but fainter channel that has not delivered a corroborating discovery.

### 8.3.3 S8 / structure growth  
(`s8_structure_tension_dark_sector` 🟡)

Late-time lensing/clustering preferences for lower S8 relative to primary CMB may reflect systematics **or** dark-sector extensions. Not the same claim as galactic small-scale challenges, though both sit in “structure” language—Discussion should keep them **orthogonal until proven linked**.

**Discussion takeaway B.** *Yellow nodes are the load-bearing debates; orange nodes are where experiments mint limits.*

## 8.4 Microphysics: a portfolio, not a single horse

### Thermal WIMP  
Still the **benchmark** (`thermal_wimp_freezeout_benchmark` 🟠) after the “waning of the WIMP”: nulls reshape the simple parameter space without deleting freeze-out as an organising idea. Direct detection approaches a neutrino floor/fog (`neutrino_floor_direct_detection`); colliders map production via mono-jet/MET (`monojet_collider_searches`, E1 nulls).

### Axions / ALPs  
Motivated non-WIMP target under active laboratory search (`axion_dm_candidate`). Distinguish **candidate class** from **identification**.

### SIDM and fuzzy / wave DM  
Both answer small-scale structure without abandoning large-scale CDM success, under different microphysics (`sidm_small_scales`, `fuzzy_wave_dark_matter`). Cluster σ/m bounds and Lyman-α mass floors are **constraint engines**, not discovery engines.

### Speculative ceiling  
- `sterile_neutrino_7kev_line` 🔴: claim + counter-claim both recorded; mainstream non-acceptance is the light.  
- `pbh_all_dark_matter` 🔴: constrained windows; not the default budget.

**Discussion takeaway C.** *Frontier thickness means the field is active, not that all candidates are equally likely—likelihood is not what our lights encode.*

## 8.5 What would move a light? (decision-relevant)

Discussion should state **mechanisms of light migration**, not predictions of winners:

| If this happens… | Candidate claim movement (illustrative) |
|------------------|----------------------------------------|
| Confirmed multi-channel particle detection with consistent rates | `dm_particle_identity` / relevant candidate 🟠→ stronger; others demoted |
| Decisive GC analysis + dSph corroboration or refutation | `fermi_gc_excess_origin` 🟡 resolves toward one camp |
| Survey consensus removes or locks S8 offset | `s8_structure_tension_dark_sector` 🟡 narrows |
| Relativistic modified dynamics passes CMB+clusters **or** fails cleanly | `particle_vs_modified_gravity` 🟡 shifts |
| Line confirmed by high-res X-ray + halo-consistent non-observation elsewhere | sterile-neutrino claim stays 🔴 or dies |

`[FILL: 1 paragraph on XRISM / Euclid–Rubin–Roman / HL-LHC / multi-tonne xenon generation—descriptive, not promotional.]`

## 8.6 Limitations of this map

1. **Claim selection bias.** Spine reviews and decisive measurements preferred; some active subfields (e.g. detailed EFT operator bases, certain ultralight black-hole superradiance windows) are under-represented.  
2. **Evidence vocabulary is coarse.** E1–E5 is discrete by design; it does not replace experiment-specific likelihoods.  
3. **Status lights are human-authored** under explicit conditions; third parties can overturn them by attacking `status_reason`, not by vibes.  
4. **Freeze date.** Literature after `[FILL]` is not automatically ingested.  
5. **No Bayesian global fit.** We do not combine channels into a posterior over “what DM is.”

## 8.7 Relation to open knowledge infrastructure

`[FILL optional:]` This Discussion is paired with a public, test-gated knowledge base: provenance (cite ⇒ fetch), dual-axis rendering, and export tables for open questions and sources. The scientific content is the claims; the infrastructure is an audit surface so that upgrades of lights leave a trail.

---

# 9. Conclusions (skeleton)

1. Under GR, the **mass discrepancy** is Established on multiple independent direct lines (`mass_discrepancy_observed`).  
2. Standard cosmology’s need for a **cold non-baryonic component** is Strong, but largely **indirect** (`lcdm_includes_cold_dm`)—do not confuse with particle ID.  
3. **Identity remains Frontier** (`dm_particle_identity`); thermal WIMPs remain a benchmark under pressure; axions, SIDM, and fuzzy DM are structured programmes, not discoveries.  
4. Laboratory and collider channels deliver **limits without identification**; neutrino floor defines the next direct-detection regime.  
5. Three live **Competing** nodes (particle vs modified dynamics; GC excess; S8) and two **Speculative** ceilings (7 keV line claim; all-DM PBHs) mark where rhetoric most often outruns evidence.

`[FILL: funding, acknowledgements, conflict of interest, author contributions.]`

---

## Appendix A — Claim → section crosswalk

| Section | Claim ids |
|---------|-----------|
| Intro Q1–Q5 | `mass_discrepancy_observed`, `lcdm_includes_cold_dm`, `particle_vs_modified_gravity`, `dm_particle_identity`, (+ lab cluster) |
| Discussion 8.2 | `lcdm_includes_cold_dm`, direct/mono-jet/dSph |
| Discussion 8.3 | `particle_vs_modified_gravity`, `fermi_gc_excess_origin`, `s8_structure_tension_dark_sector` |
| Discussion 8.4 | thermal WIMP, axion, SIDM, fuzzy, sterile ν, PBH + detection claims |
| Discussion 8.5 | light-migration table (all) |

## Appendix B — Suggested figure/table list for full paper

| Item | File / source |
|------|----------------|
| Fig. 1 Light × evidence | `docs/paper/fig1-light-vs-evidence.svg` |
| Table 1 Claims summary | `dark-matter-claims-summary.md` |
| Table 2 Open questions (subset) | `dark-matter-open-questions.md` (curate ≤15 rows for print) |
| Table 3 Source spine | `dark-matter-sources.md` (unique ids) |
| Fig. 2 (optional) | Schematic Q1–Q5 flowchart `[FILL]` |
| Fig. 3 (optional) | Channel sketch: direct / collider / indirect / X-ray `[FILL]` |

## Appendix C — Author checklist before submission

- [ ] No sentence upgrades 🔴/🟠 identity claims to Established.  
- [ ] Divergence of `lcdm_includes_cold_dm` mentioned once in Intro and once in Discussion.  
- [ ] Each 🟡 has both camps in prose.  
- [ ] Abstract written last; matches claim lights.  
- [ ] All `[FILL]` removed or resolved.  
- [ ] Freeze date and software/data links present.  
- [ ] Re-run `python -m universe_explorer.dataops.export_dm_paper` if claims changed.  
- [ ] `python run_tests.py` green on the claim freeze commit.

---

## Next writing sprints (optional order)

1. Fill Abstract + §1.2 audience paragraph (30–45 min).  
2. Expand §8.3 three competitions with 2–3 spine citations each (half day).  
3. Curate print Table 2 open questions down to ≤15 (1–2 h).  
4. Draft full Results body from claims (multi-day; can be semi-automated from narrative engine).  
5. Human pass for tone (no hype, no false balance on 🟢).
