# Discussion — Exoplanets: existence, populations, atmospheres, and a red ceiling

**Domain anchors:** `exoplanets` (9 claims).  
**Companion:** `docs/universe-planets-map.md` · data in `universe_explorer/data/exoplanets.py`.  
**Citation style:** (Author Year). **Boundaries:** solar-system chronology and icy-moon oceans → `planets`; stellar physics → `stars`.

---

## 1. Framing: a green floor under an orange atmosphere era

Exoplanets are no longer a discovery speciality in the sense of “do they exist?” They are a **population and atmosphere** speciality. Our map records that shift as a light shape: two Established existence claims, one Strong demographic claim, two Competing nodes (Planet Nine; radius-valley mechanism), three Frontier JWST-era atmosphere claims, and one Speculative biosignature ceiling.

We refuse confidence percentages. Occurrence rates, scale heights and feature detections are quantities you open in the sources—not scores we invent.

## 2. Existence is Established; commonality is Strong

Planets orbiting other stars are Established because independent methods converge on the same class of objects (`exoplanets_exist`; Mayor & Queloz, 1995; Charbonneau et al., 2000). Radial velocity found 51 Peg b; the transit of HD 209458 b confirmed a planetary interpretation with a second technique. Thousands of subsequent detections enlarged the population without refuting it (Mayor & Queloz, 1995; Charbonneau et al., 2000).

The nearest star hosts a temperate Earth-mass planet (`proxima_b_exists`; Anglada-Escudé et al., 2016; Suárez Mascareño et al., 2020). Independent spectrographs recover the same 11.2-day signal. That does **not** establish habitability, surface water or an atmosphere—only the planet’s dynamical existence.

Planets as the rule rather than the exception around Milky Way stars is Strong (`planets_are_common`; Cassan et al., 2012). Microlensing statistics imply order-unity planets per star on average. The light is not Established because the claim is demographic and method-dependent: true Earth analogues in habitable zones remain the least pinned part of the census (Cassan et al., 2012). Completeness debates refine numbers; they do not restore a “planets are rare” textbook picture.

## 3. Two yellow nodes

**Planet Nine.** Clustering of distant trans-Neptunian object angles can be read as the dynamical signature of an unseen giant planet (`planet_nine`; Batygin & Brown, 2016). Independent survey work has argued that pointing biases can produce apparent clustering without a planet (Shankman et al., 2017). Both camps publish; neither has a community knockout. Note the domain honesty: Planet Nine is a *solar-system* dynamical claim housed here because it is “a planet we have not imaged,” not because it is an exoplanet. If the map ever splits solar-system oddities out of `exoplanets`, this node moves with them.

**Radius valley.** The observed dearth of planets near ~1.5–2.0 Earth radii is Competing as to *mechanism* (`radius_valley_mechanism`; Owen & Wu, 2017; related core-powered mass-loss literature). Photoevaporation and core-powered mass loss both carve a valley in published models; present demographics have not uniquely selected one channel. The valley’s *existence* as a feature of the radius distribution is much more secure than the engineering that cuts it.

## 4. Orange: TRAPPIST-1 and JWST atmospheres

JWST-era thermal and transmission work on TRAPPIST-1 b (and the broader inner pair) reports little evidence for thick atmospheres, favouring bare-rock or tenuous-air interpretations for the innermost worlds (`trappist1b_bare_rock`, `trappist1_inner_planets_airless`; JWST TRAPPIST programmes). These claims are Frontier: new instruments, small samples, model-dependent retrievals. They are not a general theorem that all M-dwarf terrestrials are airless.

More broadly, JWST transmission spectroscopy measures molecular features in exoplanet atmospheres (`jwst_exoplanet_atmospheres`). That is Frontier capability science: real spectra, rapidly growing literature, no settled “standard atmospheric inventory” for any large demographic bin. Scale-height, cloud and stellar-contamination systematics are the honest open questions—not whether the telescope collects photons.

## 5. Red ceiling: biosignatures

A claimed biosignature (e.g. DMS) in the atmosphere of K2-18 b is Speculative as a life detection (`k2_18b_biosignature`). Spectral features may be discussed; mainstream acceptance of a biological origin has not followed. Abiotic pathways and data-reduction debates keep the claim below the Frontier “new measurement” shelf and in the Speculative “not accepted as life” ceiling. Moving this light would require a community-accepted detection protocol that rules out abiotic explanations—not better press language.

## 6. Reading order and boundaries

**Order:** existence + Proxima b 🟢 → commonality 🔵 → Planet Nine + radius valley 🟡 → TRAPPIST/JWST atmospheres 🟠 → biosignature 🔴.

| Question | Domain |
|----------|--------|
| Solar-system age, Moon, icy-moon oceans | `planets` |
| Stellar hosts, IMF, mass loss | `stars` |
| Planets around other stars, atmospheres, biosignature claims | **`exoplanets`** |

---

## References

**Anglada-Escudé, G., et al.** (2016). A terrestrial planet candidate in a temperate orbit around Proxima Centauri. *Nature*, *536*, 437–440. arXiv:1609.03449

**Batygin, K., & Brown, M. E.** (2016). Evidence for a distant giant planet in the Solar System. *Astronomical Journal*, *151*, 22. arXiv:1601.05438

**Cassan, A., et al.** (2012). One or more bound planets per Milky Way star from microlensing observations. *Nature*, *481*, 167–169. https://doi.org/10.1038/nature10684

**Charbonneau, D., Brown, T. M., Latham, D. W., & Mayor, M.** (2000). Detection of planetary transits across a Sun-like star. *Astrophysical Journal Letters*, *529*, L45–L48. arXiv:astro-ph/9911436

**Mayor, M., & Queloz, D.** (1995). A Jupiter-mass companion to a solar-type star. *Nature*, *378*, 355–359.

**Owen, J. E., & Wu, Y.** (2017). The evaporation valley in the Kepler planets. arXiv related radius-valley / photoevaporation literature (see claim sources in `exoplanets.py`).

**Shankman, C., et al.** (2017). OSSOS. VI. Striking biases in the detection of large semimajor axis trans-Neptunian objects. *Astronomical Journal*. arXiv:1706.04175

**Suárez Mascareño, A., et al.** (2020). Revisiting Proxima with ESPRESSO. *Astronomy & Astrophysics*, *639*, A77. arXiv:2005.12114

*(TRAPPIST-1 / JWST atmosphere and K2-18 b source labels: open the claim records in `exoplanets.py` for the exact arXiv/DOI ids used by the engine.)*
