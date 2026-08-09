# Dark matter: what is established, what competes, and what remains open

**Manuscript skeleton — Introduction + Discussion only**  
Status: draft scaffold (2026-08-09); **Abstract + §8.3 near-final prose** · Claims: `universe_explorer/data/dark_matter.py` (18 claims)  
Companion artifacts: `dark-matter-paper-map.md` · `fig1-light-vs-evidence.svg` · open-questions & sources tables  

> **How to use this file**  
> - **Abstract** and **§8.3** below are written as near-submission English; edit for house style, not for substance, unless claims change.  
> - Other sections may still contain starter wording or `[FILL: …]`.  
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

## Abstract (near-final)

Dark matter is not one question. The phrase is used for an observed mass discrepancy under general relativity, for a cold non-baryonic ingredient in the standard cosmological model, and for a still-unidentified particle—layers that are often conflated in both pedagogy and public discussion. We present an epistemically stratified map of the problem as eighteen atomic claims. Each claim carries a consensus light fixed by explicit entry conditions and an evidence grade derived mechanically from recorded evidence types, not declared as a confidence score (Fig. 1).

On that map, the mass discrepancy under luminous matter alone is Established on multiple independent direct lines (`mass_discrepancy_observed`). The need for a cold non-baryonic component in ΛCDM is Strong Consensus, yet rests largely on indirect cosmological inference (`lcdm_includes_cold_dm`)—a structural divergence between consensus and directness. Three Competing nodes mark multi-year scientific camps rather than rhetorical binaries: particle dark-matter halos versus modified Newtonian dynamics (`particle_vs_modified_gravity`); dark-matter annihilation versus unresolved astrophysics for the Fermi Galactic Centre excess (`fermi_gc_excess_origin`); and new dark-sector physics versus survey systematics for the S8 structure-growth tension (`s8_structure_tension_dark_sector`). A broad Frontier layer records what remains open without pretending it is settled: the particle identity; the thermal WIMP freeze-out benchmark under laboratory and collider nulls; axion, self-interacting, and fuzzy/wave programmes; dwarf-spheroidal gamma-ray limits; merging-cluster bounds on the self-interaction cross section per unit mass; and the neutrino floor for direct detection. Speculative ceilings—most notably the claim that a ~7 keV sterile neutrino produces the 3.5 keV X-ray line and constitutes the dark matter, and that primordial black holes make up all of the dark matter—are retained only with that status light.

The map does not identify dark matter. It separates what observations establish from what models compete over, and from what searches constrain without yet detecting. Cosmological success is not particle identification; null results are knowledge, not emptiness; and live competitions should be argued on both sides until decisive evidence selects between them.

**Word count:** ~280 (trim 30–50 words for journals with a 200–250 limit by dropping the Speculative sentence or merging the Frontier list).

**Claim anchors (do not remove in editing):**  
`mass_discrepancy_observed` · `lcdm_includes_cold_dm` · `particle_vs_modified_gravity` · `fermi_gc_excess_origin` · `s8_structure_tension_dark_sector` · `dm_particle_identity` · thermal WIMP / axion / SIDM / fuzzy / dSph / cluster σ⁄m / neutrino floor / mono-jet cluster · `sterile_neutrino_7kev_line` · `pbh_all_dark_matter`

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

## 8.3 The three competitions that are not “noise” (near-final)

Citations in this section use **(Author Year)** form. Full bibliographic entries appear in **§8.3 References** below. Claim ids in backticks remain map anchors, not substitutes for the literature.

Not every disagreement in the dark-matter literature is a scientific competition in the sense used here. We reserve the Competing light for splits that (i) host at least two frameworks actively maintained in the peer-reviewed literature, (ii) still lack decisive evidence selecting between them, and (iii) are not artefacts of a single disputed analysis. Three nodes meet that bar. They are load-bearing: much of the Frontier layer is best read as an attempt to *live with*, *sharpen*, or *escape* one of these yellow tensions. Orange claims, by contrast, are where experiments primarily mint limits (Bertone & Tait, 2018). We discuss the three in turn without declaring winners.

### 8.3.1 Particle dark-matter halos versus modified dynamics

Claim: `particle_vs_modified_gravity` (Competing).

At galactic scales, two reading frames remain in simultaneous use. In the first, flat rotation curves and related scaling relations are explained by extended, largely collisionless particle dark-matter halos embedded in the ΛCDM paradigm. That frame inherits large-scale support from the cosmological need for non-baryonic cold matter (`lcdm_includes_cold_dm`; Planck Collaboration, 2020; Bertone & Tait, 2018) and from merging-cluster configurations in which lensing mass remains spatially offset from collisional baryonic gas—behaviour natural for a collisionless mass component and a persistent challenge for gravity-only alternatives (Clowe et al., 2006). Hierarchical structure formation in N-body simulations further organises the particle-halo picture into a predictive, if baryon-dependent, programme (Bullock & Boylan-Kolchin, 2017).

In the second frame, the force law itself is modified at very low accelerations so that flat rotation curves and several galactic regularities—classically including the baryonic Tully–Fisher relation—emerge with few free parameters per system, without assigning each galaxy a flexible halo (Milgrom, 1983). The appeal of this programme is empirical thrift at galaxy scales, not denial of the mass discrepancy under Newtonian gravity with luminous matter alone. The cost is well advertised by its critics: clusters and cosmology are difficult without reintroducing unseen mass or additional fields, and stable, cosmology-compatible relativistic completions that pass the full suite of tests remain unfinished work (Bertone & Tait, 2018; Clowe et al., 2006).

Neither side is a straw man. Particle CDM is the working standard of precision cosmology; MOND-like dynamics remains an active, peer-reviewed research programme for galactic phenomenology (Milgrom, 1983; Bertone & Tait, 2018). No single observation has closed the debate *at all scales*. The honest cross-links on our map are therefore not rhetorical. Small-scale challenges to collisionless CDM in dwarfs and satellites (`small_scale_cdm_challenges`; Bullock & Boylan-Kolchin, 2017) keep open the question of how much tension is baryonic feedback versus new dark-sector physics—an invitation to particle-side elaborations such as velocity-dependent self-interactions (`sidm_small_scales`; Tulin & Yu, 2018), which must still face merging-cluster bounds on the cross section per unit mass (`cluster_sidm_cross_section_bounds`; Randall et al., 2008; Harvey et al., 2015). Fuzzy or wave dark matter (`fuzzy_wave_dark_matter`; Hu et al., 2000; Hui et al., 2017) offers a different microphysical route to cores and suppressed small-scale power, under Lyman-α mass floors (Iršič et al., 2017). On the gravity side, the decisive tests remain whether relativistic completions can meet CMB and cluster constraints without effectively smuggling dark mass back in. Laboratory and collider nulls constrain couplings (Bertone & Tait, 2018); they do not, by themselves, adjudicate this macroscopic split.

**What would move this light.** A relativistic modified-dynamics framework that simultaneously satisfies CMB, clusters, and galactic scaling—or a clean, widely accepted failure thereof—would collapse the competition. Absent that, both camps remain scientific, and prose that “settles” the issue by tone alone is out of scope for this map.

### 8.3.2 The Fermi Galactic Centre excess: annihilation versus unresolved sources

Claim: `fermi_gc_excess_origin` (Competing).

Analyses of Fermi-LAT data have long reported a roughly spherical GeV gamma-ray excess toward the Galactic Centre whose spectrum and morphology can be argued to match annihilating thermal WIMPs of tens of GeV (Daylan et al., 2016). That reading would be of first importance if confirmed: it would be a positive, if still model-dependent, *signal* in a field dominated by limits. The opposing camp attributes the same excess to unresolved astrophysical sources—most prominently a faint population of millisecond pulsars or related stellar remnants—without new particle physics. The dispute is not whether an excess relative to some diffuse models has been discussed; it is whether the residual is dark matter, stars, or an artefact of Galactic emission systematics.

Subsequent statistical work has not closed the case. Preferred non-Poissonian template fits that once appeared to favour a point-source population have been argued to be pathological, reopening tension between the two interpretations rather than awarding victory to either (Leane & Slatyer, 2019). The uncertainty budget is dominated by the Galactic diffuse foreground. Required annihilation cross sections and density profiles are model-dependent, and other targets have not delivered a corroborating discovery. In particular, joint Fermi-LAT analyses of dwarf spheroidal galaxies—cleaner targets with lower astrophysical backgrounds—set strong limits on annihilation without a confirmed signal (`dwarf_spheroidal_indirect_limits`; Fermi-LAT Collaboration, 2015; Fermi-LAT Collaboration & DES Collaboration, 2017). That null does not logically refute every GC dark-matter model, but it raises the bar: a particle explanation of the Centre should eventually face the dwarf channel under consistent microphysics.

**What would move this light.** Decisive control of diffuse systematics, a securely observed stellar-remnant population that accounts for the residual, or a multi-target dark-matter pattern (Centre plus dwarfs or other systems) under one particle model would select a camp. Until then, the GC excess remains a Competing node, not a discovery claim and not a dismissed curiosity.

### 8.3.3 The S8 structure-growth tension: dark sector versus systematics

Claim: `s8_structure_tension_dark_sector` (Competing).

A mild-to-moderate discrepancy in the clustering amplitude \(S_8\) between primary CMB inferences and several weak-lensing and galaxy-clustering surveys has become a standing feature of the cosmological conversation (Di Valentino et al., 2021). On one side, Planck baseline parameters, extrapolated in flat ΛCDM, fix a higher late-time clustering amplitude (Planck Collaboration, 2020). On the other, analyses such as Dark Energy Survey Year 3 \(3\times2\)pt results prefer a lower \(S_8\) when interpreted in the same model family (DES Collaboration, 2022). Reviews of cosmological tensions document the persistence of this offset across combinations, while emphasising that its formal significance depends on dataset choice and pipeline (Di Valentino et al., 2021).

Two responses are actively published. The first explores new dark-sector or late-time physics—decaying, interacting, or growth-suppressing dark matter among other extensions—that can lower \(S_8\) relative to the primary CMB without immediately abandoning early-universe successes (Di Valentino et al., 2021). The limitation is familiar: many extensions reintroduce tension elsewhere (CMB lensing, cluster counts, BAO) or require fine-tuned couplings, and no single dark-sector fix is uniquely selected. The second response keeps ΛCDM and attributes the offset to residual systematics—shear calibration, photometric redshifts, intrinsic alignments, scale cuts—or to statistical variation across analyses. Alternate pipelines sometimes weaken the tension; yet multiple independent lensing teams reporting low \(S_8\) makes a single-experiment flaw an incomplete dismissal (DES Collaboration, 2022; Di Valentino et al., 2021). End-to-end cross-survey consensus on residual systematics is still forming.

This competition is **not** the same claim as galactic small-scale CDM challenges (`small_scale_cdm_challenges`; Bullock & Boylan-Kolchin, 2017), even though both are discussed under the loose heading of “structure.” One concerns the growth amplitude on cosmological weak-lensing scales relative to the CMB; the other concerns the internal structure and satellite populations of galaxies relative to collisionless simulations. They may eventually share a microphysical cause; they may not. Our map treats them as orthogonal until joint evidence forces a link. Forthcoming wide surveys (Euclid, LSST/Rubin, Roman) will either reduce the \(S_8\) offset, sharpen it, or relocate it—any of which moves the light more honestly than premature dark-sector marketing or premature denial.

**What would move this light.** Survey-level consensus that removes the offset inside ΛCDM, or a dark-sector model that survives joint CMB, full-shape clustering, and lensing likelihoods without collateral damage, would narrow the competition. Present data do not yet deliver either verdict.

### 8.3.4 Synthesis

The three yellow nodes fail different kinds of impatience. Particle-versus-MOND impatience wants a single sentence for “what gravity does in galaxies.” GC-excess impatience wants a discovery press release or a burial. S8 impatience wants either a new dark sector or an assurance that systematics will vanish. The map’s job is narrower: to keep both camps legible, to cross-link the Frontier programmes that try to relieve each tension, and to refuse false closure. **Yellow nodes are the load-bearing debates; orange nodes are where experiments mint limits; green and blue nodes are what those debates are not allowed to erase.**

### 8.3 References

Bibliographic entries for inline citations in §8.3. Identifiers match the claim data layer (arXiv/DOI) where applicable. Collaboration papers are listed under the collaboration name used in the text.

**Bertone, G., & Tait, T. M. P.** (2018). A new era in the search for dark matter. *Nature*, *562*, 51–56. https://doi.org/10.1038/s41586-018-0542-z · claim sources: `BertoneTait2018*`

**Bullock, J. S., & Boylan-Kolchin, M.** (2017). Small-scale challenges to the ΛCDM paradigm. *Annual Review of Astronomy and Astrophysics*, *55*, 343–387. arXiv:1707.04256 · claim: `small_scale_cdm_challenges`

**Clowe, D., Bradač, M., Gonzalez, A. H., Markevitch, M., Randall, S. W., Jones, C., & Zaritsky, D.** (2006). A direct empirical proof of the existence of dark matter. *The Astrophysical Journal Letters*, *648*, L109–L113. arXiv:astro-ph/0608407 · claims: `mass_discrepancy_observed`, `particle_vs_modified_gravity`

**Daylan, T., Finkbeiner, D. P., Hooper, D., Linden, T., Portillo, S. K. N., Rodd, N. L., & Slatyer, T. R.** (2016). The characterization of the gamma-ray signal from the central Milky Way: A compelling case for annihilating dark matter. *Physics of the Dark Universe*, *12*, 1–23. arXiv:1402.6703 · claim: `fermi_gc_excess_origin`

**DES Collaboration** (Abbott, T. M. C., et al.). (2022). Dark Energy Survey Year 3 results: Cosmological constraints from galaxy clustering and weak lensing. *Physical Review D*, *105*, 023520. arXiv:2105.13549 · claim: `s8_structure_tension_dark_sector`

**Di Valentino, E., et al.** (2021). Cosmology intertwined III: \(f\sigma_8\) and \(S_8\). *Astroparticle Physics*, *131*, 102604. arXiv:2008.11285 · claim: `s8_structure_tension_dark_sector`

**Fermi-LAT Collaboration** (Ackermann, M., et al.). (2015). Searching for dark matter annihilation from Milky Way dwarf spheroidal galaxies with six years of Fermi Large Area Telescope data. *Physical Review Letters*, *115*, 231301. arXiv:1503.02641 · claim: `dwarf_spheroidal_indirect_limits`

**Fermi-LAT Collaboration & DES Collaboration** (Albert, A., et al.). (2017). Searching for dark matter annihilation in recently discovered Milky Way satellites with Fermi-LAT. *The Astrophysical Journal*, *834*, 110. arXiv:1611.03184 · claim: `dwarf_spheroidal_indirect_limits`

**Harvey, D., Massey, R., Kitching, T., Taylor, A., & Tittley, E.** (2015). The nongravitational interactions of dark matter in colliding galaxy clusters. *Science*, *347*, 1462–1465. arXiv:1503.07675 · claim: `cluster_sidm_cross_section_bounds`

**Hu, W., Barkana, R., & Gruzinov, A.** (2000). Fuzzy cold dark matter: The wave properties of ultralight particles. *Physical Review Letters*, *85*, 1158–1161. arXiv:astro-ph/0003365 · claim: `fuzzy_wave_dark_matter`

**Hui, L., Ostriker, J. P., Tremaine, S., & Witten, E.** (2017). Ultralight scalars as cosmological dark matter. *Physical Review D*, *95*, 043541. arXiv:1610.08297 · claim: `fuzzy_wave_dark_matter`

**Iršič, V., Viel, M., Haehnelt, M. G., Bolton, J. S., & Becker, G. D.** (2017). First constraints on fuzzy dark matter from Lyman-α forest data and hydrodynamical simulations. *Physical Review Letters*, *119*, 031302. arXiv:1703.04683 · claim: `fuzzy_wave_dark_matter`

**Leane, R. K., & Slatyer, T. R.** (2019). Dark matter strikes back at the Galactic Center. *Physical Review Letters*, *123*, 241101. arXiv:1904.08430 · claim: `fermi_gc_excess_origin`

**Milgrom, M.** (1983). A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis. *The Astrophysical Journal*, *270*, 365–370. https://doi.org/10.1086/161130 · claim: `particle_vs_modified_gravity`

**Planck Collaboration** (Aghanim, N., et al.). (2020). Planck 2018 results. VI. Cosmological parameters. *Astronomy & Astrophysics*, *641*, A6. arXiv:1807.06209 · claims: `lcdm_includes_cold_dm`, `s8_structure_tension_dark_sector`

**Randall, S. W., Markevitch, M., Clowe, D., Gonzalez, A. H., & Bradač, M.** (2008). Constraints on the self-interaction cross-section of dark matter from numerical simulations of the merging galaxy cluster 1E 0657−56. *The Astrophysical Journal*, *679*, 1173–1180. arXiv:0704.0261 · claim: `cluster_sidm_cross_section_bounds`

**Tulin, S., & Yu, H.-B.** (2018). Dark matter self-interactions and small scale structure. *Physics Reports*, *730*, 1–57. arXiv:1705.02358 · claims: `sidm_small_scales`, `small_scale_cdm_challenges`

| Inline key | Full entry |
|------------|------------|
| (Bertone & Tait, 2018) | Bertone & Tait (2018) |
| (Bullock & Boylan-Kolchin, 2017) | Bullock & Boylan-Kolchin (2017) |
| (Clowe et al., 2006) | Clowe et al. (2006) |
| (Daylan et al., 2016) | Daylan et al. (2016) |
| (DES Collaboration, 2022) | DES Collaboration (2022) |
| (Di Valentino et al., 2021) | Di Valentino et al. (2021) |
| (Fermi-LAT Collaboration, 2015) | Fermi-LAT Collaboration (2015) |
| (Fermi-LAT Collaboration & DES Collaboration, 2017) | Fermi-LAT Collaboration & DES Collaboration (2017) |
| (Harvey et al., 2015) | Harvey et al. (2015) |
| (Hu et al., 2000) | Hu et al. (2000) |
| (Hui et al., 2017) | Hui et al. (2017) |
| (Iršič et al., 2017) | Iršič et al. (2017) |
| (Leane & Slatyer, 2019) | Leane & Slatyer (2019) |
| (Milgrom, 1983) | Milgrom (1983) |
| (Planck Collaboration, 2020) | Planck Collaboration (2020) |
| (Randall et al., 2008) | Randall et al. (2008) |
| (Tulin & Yu, 2018) | Tulin & Yu (2018) |

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
- [x] Each 🟡 has both camps in prose (§8.3).  
- [x] Abstract near-final; matches claim lights (trim if journal word cap requires).  
- [x] §8.3 three competitions in near-final prose; both camps each.  
- [ ] Remaining `[FILL]` outside Abstract/§8.3 removed or resolved.  
- [ ] Freeze date and software/data links present.  
- [ ] Re-run `python -m universe_explorer.dataops.export_dm_paper` if claims changed.  
- [ ] `python run_tests.py` green on the claim freeze commit.

---

## Next writing sprints (optional order)

1. ~~Abstract + §8.3~~ **done (near-final).**  
2. Curate print Table 2 open questions down to ≤15 (1–2 h).  
3. Fill §1.2 audience paragraph + §8.5 survey generation paragraph.  
4. Draft full Results body from claims (multi-day; can be semi-automated from narrative engine).  
5. Human pass for tone (no hype, no false balance on 🟢); journal word-count trim of Abstract if needed.
