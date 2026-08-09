"""Dark matter — paper-grade domain map (review-article shape).

Same schema, taxonomy and controlled evidence vocabulary as every other topic.
Engine (model / validator / axes / provenance / proposals / watch) is untouched:
only the Data layer changes.

Discipline: the *mass discrepancy* is what observations establish; the
*particle identity* is what remains open. Do not promote particle dark matter
to Established merely because textbooks use the phrase "dark matter".

Paper outline and inclusion rules: docs/dark-matter-paper-map.md

Sections (lights belong to claims, not the topic):
  I   Phenomenology   🟢 mass discrepancy · 🔵 ΛCDM cold component
  II  Interpretation  🟡 particle vs MOND · 🟠 small-scale challenges
  III Microphysics    🟠 identity · thermal WIMP · axion · SIDM · fuzzy
                      🔴 sterile ν 7 keV · PBHs as all DM
  IV  Lab / collider  🟠 direct detection · mono-jet
  V   Astro signals   🟡 GC excess · S8/dark sector · 🟠 dSph γ limits
"""

from __future__ import annotations

from ..model import (
    Claim,
    CompetingModel,
    ConditionAssessment,
    Evidence,
    Source,
    Status,
    Topic,
)

# --------------------------------------------------------------------------- #
# Claim 1 — mass discrepancy is observed                 🟢 Established        #
# --------------------------------------------------------------------------- #
mass_discrepancy_observed = Claim(
    id="mass_discrepancy_observed",
    title=(
        "Under general relativity, luminous matter alone cannot account for "
        "observed galactic dynamics and cluster mass maps"
    ),
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="Rubin1980",
            url_or_id="doi:10.1086/158003",
            kind="peer-reviewed paper (ApJ 238, 471, 1980; extended rotation "
                 "curves of spiral galaxies)",
        ),
        Source(
            label="Clowe2006",
            url_or_id="arXiv:astro-ph/0608407",
            kind="peer-reviewed paper (ApJ 648, L109, 2006; Bullet Cluster "
                 "lensing vs X-ray gas)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Optical rotation curves of spiral galaxies remain flat at large "
                "radii, where the luminous disk alone under Newtonian/GR gravity "
                "would predict a Keplerian decline — a mass discrepancy "
                "replicated across many systems."
            ),
            source_ref="Rubin1980",
        ),
        Evidence(
            type="direct observation",
            description=(
                "In the Bullet Cluster, weak-lensing mass peaks are spatially "
                "offset from the X-ray-emitting baryonic gas stripped by the "
                "collision — an independent, non-kinematic demonstration that "
                "most gravitating mass does not track the hot gas."
            ),
            source_ref="Clowe2006",
        ),
    ],
    open_questions=[
        "How much of the galactic discrepancy can alternative gravity theories "
        "absorb without failing cluster and cosmological tests remains debated "
        "(see the competing-models claim).",
        "The detailed radial distribution of the non-luminous component in "
        "dwarfs and low-surface-brightness galaxies is still being refined.",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Kinematic mass discrepancies (rotation curves, velocity "
            "dispersions) and gravitational-lensing mass maps have been "
            "reproduced by many independent groups on many systems; the "
            "Bullet Cluster is one sharp cross-check between lensing and X-ray.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Galactic mass discrepancy and cluster dark-mass components are "
            "standard content in astrophysics and cosmology textbooks.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream programme denies the observational discrepancy under "
            "GR plus luminous matter alone; the live debate is interpretation "
            "(particle dark matter vs modified dynamics), not the data gap.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Subsequent surveys and lensing campaigns have enlarged and "
            "sharpened the discrepancy, not erased it.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — ΛCDM includes cold dark matter               🔵 Strong             #
# --------------------------------------------------------------------------- #
lcdm_includes_cold_dm = Claim(
    id="lcdm_includes_cold_dm",
    title=(
        "The standard cosmological model requires a dominant non-baryonic "
        "cold dark matter component"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="Planck2018-VI",
            url_or_id="arXiv:1807.06209",
            kind="collaboration result (peer-reviewed, A&A 641, A6, 2020; "
                 "cosmological parameters)",
        ),
        Source(
            label="BertoneTait2018",
            url_or_id="doi:10.1038/s41586-018-0542-z",
            kind="peer-reviewed paper (Nature 562, 51-56, 2018; review of "
                 "the dark-matter search landscape)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Planck CMB power spectra, combined with other cosmological "
                "probes, require a cold dark matter density parameter far above "
                "the baryon density fixed by big-bang nucleosynthesis and the "
                "acoustic-peak structure."
            ),
            source_ref="Planck2018-VI",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "A mainstream review synthesises the multi-probe case for "
                "non-baryonic dark matter (CMB, large-scale structure, "
                "clusters) while separating that case from the still-open "
                "particle-identity question."
            ),
            source_ref="BertoneTait2018",
        ),
    ],
    open_questions=[
        "Mild tensions (e.g. H0, S8) may refine parameters without removing "
        "the need for a cold dark component in the baseline model.",
        "Whether a small warm or self-interacting fraction is allowed is an "
        "active modelling question.",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "ΛCDM with cold dark matter is the baseline of major cosmological "
            "collaborations and textbooks; CMB and large-scale structure fit it.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Modified-gravity and warm/self-interacting variants exist as "
            "research programmes; they do not displace ΛCDM as the working "
            "cosmological standard.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Decades of improved CMB and survey data have tightened, not "
            "removed, the non-baryonic cold component. The evidence is "
            "cosmological inference (indirect); that sits on the evidence axis.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — particle DM vs modified dynamics             🟡 Competing          #
# --------------------------------------------------------------------------- #
particle_vs_modified_gravity = Claim(
    id="particle_vs_modified_gravity",
    title=(
        "Galactic dynamics are explained by particle dark-matter halos versus "
        "modified Newtonian dynamics"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Milgrom1983",
            url_or_id="doi:10.1086/161130",
            kind="peer-reviewed paper (ApJ 270, 365, 1983; MOND)",
        ),
        Source(
            label="Clowe2006b",
            url_or_id="arXiv:astro-ph/0608407",
            kind="peer-reviewed paper (ApJ 648, L109, 2006; cluster lensing "
                 "offset as challenge to pure modified gravity)",
        ),
        Source(
            label="BertoneTait2018b",
            url_or_id="doi:10.1038/s41586-018-0542-z",
            kind="peer-reviewed paper (Nature 562, 51-56, 2018)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical derivation",
            description=(
                "Modified Newtonian Dynamics (MOND) alters the force law at "
                "very low accelerations so that flat rotation curves emerge "
                "without particle halos, fitting many galactic scaling "
                "relations with few free parameters."
            ),
            source_ref="Milgrom1983",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The Bullet Cluster's separation between lensing mass and "
                "collisional gas is widely used as evidence that most mass is "
                "collisionless — a natural particle-dark-matter expectation and "
                "a hard test for gravity-only alternatives."
            ),
            source_ref="Clowe2006b",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Reviews of the search landscape treat particle dark matter as "
                "the leading interpretation of cosmological and cluster data "
                "while acknowledging that galactic phenomenology still fuels "
                "modified-dynamics research programmes."
            ),
            source_ref="BertoneTait2018b",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Particle dark-matter halos (ΛCDM paradigm)",
            supporting=(
                "CMB and large-scale structure require non-baryonic matter; "
                "cluster lensing offsets match collisionless mass; N-body "
                "halos form structure hierarchically."
            ),
            opposing=(
                "Small-scale issues (cores vs cusps, satellite abundances, "
                "diversity of rotation curves) remain actively debated."
            ),
            limitations=(
                "The particle itself is undetected; baryonic feedback is often "
                "invoked to reconcile simulations with galaxies."
            ),
        ),
        CompetingModel(
            name="Modified dynamics (MOND and relativistic extensions)",
            supporting=(
                "Many galactic scaling laws (e.g. baryonic Tully–Fisher) emerge "
                "naturally; fewer free parameters per galaxy than flexible "
                "halo fits."
            ),
            opposing=(
                "Clusters and cosmology remain difficult without additional "
                "unseen mass or fields; Bullet Cluster–class systems are a "
                "persistent challenge."
            ),
            limitations=(
                "Building a stable, cosmology-compatible relativistic theory "
                "that passes all tests is unfinished."
            ),
        ),
    ],
    open_questions=[
        "Can relativistic MOND-like theories meet CMB and cluster constraints "
        "without effectively reintroducing dark mass?",
        "How much of the small-scale CDM tension is baryonic physics versus "
        "new dark-sector physics?",
        "Which forthcoming surveys or laboratory searches would most cleanly "
        "discriminate the two programmes?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Particle CDM is the cosmological standard; MOND-like dynamics "
            "remains an active, peer-reviewed research programme for galactic "
            "scaling — both appear in the literature as live frameworks.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "No single observation has closed the debate for all scales: "
            "clusters favour collisionless mass, while some galactic "
            "regularities keep modified dynamics in play.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Published reviews, dedicated conferences and opposing papers "
            "document a real split — not an AI-invented dichotomy.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — particle identity unknown                    🟠 Frontier           #
# --------------------------------------------------------------------------- #
# (Paper §III.1 — umbrella: still no identification)
dm_particle_identity = Claim(
    id="dm_particle_identity",
    title="The particle identity of dark matter remains unknown",
    status=Status.FRONTIER,
    sources=[
        Source(
            label="BertoneTait2018c",
            url_or_id="doi:10.1038/s41586-018-0542-z",
            kind="peer-reviewed paper (Nature 562, 51-56, 2018)",
        ),
        Source(
            label="LZ2023",
            url_or_id="arXiv:2207.03764",
            kind="collaboration result (peer-reviewed, PRL 131, 041002, 2023; "
                 "LUX-ZEPLIN WIMP search)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "A major review frames the post-WIMP landscape: decades of "
                "direct, indirect and collider searches have not identified "
                "the dark-matter particle, while many well-motivated "
                "candidates remain viable."
            ),
            source_ref="BertoneTait2018c",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The LUX-ZEPLIN dual-phase xenon detector reports no "
                "significant WIMP-nucleon scattering excess, setting "
                "world-leading limits that exclude large regions of "
                "canonical weak-scale WIMP parameter space."
            ),
            source_ref="LZ2023",
        ),
    ],
    open_questions=[
        "Is dark matter a WIMP, axion/ALP, sterile neutrino, dark sector, or "
        "something not yet formulated?",
        "Do null direct-detection results push the field toward lighter or "
        "feebler interactions, or toward non-particle options?",
        "Which experimental channel is most likely to yield a positive "
        "identification in the next decade?",
    ],
    status_reason=[
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "There is consensus that something is missing from the baryonic "
            "budget, but no consensus on which particle (if any) it is.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Direct-detection, axion, and theory papers continue to accumulate "
            "rapidly as parameter space is reshaped by null results.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No laboratory or astrophysical channel has produced a confirmed "
            "particle detection that the field accepts as dark matter.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4a — thermal WIMP freeze-out benchmark           🟠 Frontier           #
# --------------------------------------------------------------------------- #
thermal_wimp_freezeout_benchmark = Claim(
    id="thermal_wimp_freezeout_benchmark",
    title=(
        "A thermal freeze-out WIMP with weak-scale mass and couplings remains "
        "a benchmark dark-matter target despite null searches"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Arcadi2018",
            url_or_id="arXiv:1703.07364",
            kind="peer-reviewed paper (Eur. Phys. J. C 78, 203, 2018; "
                 "waning of the WIMP review)",
        ),
        Source(
            label="BertoneTait2018e",
            url_or_id="doi:10.1038/s41586-018-0542-z",
            kind="peer-reviewed paper (Nature 562, 51-56, 2018)",
        ),
        Source(
            label="LZ2023b",
            url_or_id="arXiv:2207.03764",
            kind="collaboration result (peer-reviewed, PRL 131, 041002, 2023)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "A major review of the WIMP paradigm shows how thermal "
                "freeze-out at the weak scale naturally yields the observed "
                "relic density (the 'WIMP miracle'), while mapping how LHC and "
                "direct-detection nulls have eroded large parts of the "
                "simplest parameter space."
            ),
            source_ref="Arcadi2018",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Post-WIMP landscape reviews still treat thermal WIMPs as a "
                "central organising benchmark for comparing laboratory, "
                "collider and astrophysical searches even as attention "
                "broadens to axions and dark sectors."
            ),
            source_ref="BertoneTait2018e",
        ),
        Evidence(
            type="direct observation",
            description=(
                "World-leading xenon direct-detection limits (LZ) exclude "
                "large regions of canonical spin-independent WIMP-nucleon "
                "cross section near the weak scale without finding a signal."
            ),
            source_ref="LZ2023b",
        ),
    ],
    open_questions=[
        "Do compressed, co-annihilating or secluded WIMP models still offer "
        "thermal targets that evade current mono-jet and xenon bounds?",
        "At what point should the field demote thermal WIMPs from default "
        "benchmark to historical special case?",
        "How should relic-density priors be reported when combining "
        "collider and direct-detection likelihoods?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "WIMP simplified models, global fits and 'waning of the WIMP' "
            "reviews form a large, still-active literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "The community agrees the simplest WIMPs are pressured, not that "
            "thermal freeze-out is dead as a framework.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No confirmed WIMP detection exists; the benchmark is theoretical "
            "plus exclusion plots, not a positive particle ID.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4a2 — underground direct detection               🟠 Frontier           #
# --------------------------------------------------------------------------- #
direct_detection_wimp_searches = Claim(
    id="direct_detection_wimp_searches",
    title=(
        "Underground direct-detection experiments set leading limits on "
        "WIMP-nucleon scattering without a confirmed discovery"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Schumann2019",
            url_or_id="arXiv:1903.03026",
            kind="peer-reviewed paper (J. Phys. G 46, 103003, 2019; "
                 "direct-detection review)",
        ),
        Source(
            label="XENON1T2018",
            url_or_id="arXiv:1805.12562",
            kind="collaboration result (peer-reviewed, Phys. Rev. Lett. 121, "
                 "111302, 2018; XENON1T SI WIMP search)",
        ),
        Source(
            label="LZ2023c",
            url_or_id="arXiv:2207.03764",
            kind="collaboration result (peer-reviewed, PRL 131, 041002, 2023)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "A field review of direct detection summarises dual-phase "
                "xenon, cryogenic and other technologies that search for "
                "nuclear recoils from Galactic halo WIMPs, emphasising "
                "background control and the neutrino floor as the next "
                "sensitivity barrier."
            ),
            source_ref="Schumann2019",
        ),
        Evidence(
            type="direct observation",
            description=(
                "XENON1T reported a search for spin-independent "
                "WIMP-nucleon scattering with a tonne-scale liquid-xenon "
                "target, observing no significant excess and setting then "
                "world-leading upper limits."
            ),
            source_ref="XENON1T2018",
        ),
        Evidence(
            type="direct observation",
            description=(
                "LUX-ZEPLIN subsequently improved those limits with a larger "
                "exposure, again finding no WIMP signal in the canonical "
                "low-energy nuclear-recoil region of interest."
            ),
            source_ref="LZ2023c",
        ),
    ],
    open_questions=[
        "Will multi-tonne xenon/argon experiments hit the neutrino fog before "
        "a WIMP signal appears?",
        "How should annual-modulation claims (historically contested) be "
        "weighed against null rate experiments?",
        "Which low-mass and spin-dependent channels remain least constrained "
        "relative to collider mono-jet bounds?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Successive xenon/argon generations and directional/low-threshold "
            "R&D produce a continuous stream of limit and method papers.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "There is consensus on how to set limits, not on a discovery; "
            "modulation controversies remain outside the main null-result "
            "mainstream.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No underground experiment has a confirmed, widely accepted "
            "WIMP detection.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4b — small-scale CDM challenges                  🟠 Frontier           #
# --------------------------------------------------------------------------- #
small_scale_cdm_challenges = Claim(
    id="small_scale_cdm_challenges",
    title=(
        "Cold dark matter faces open small-scale challenges in galaxies "
        "and satellites"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="BullockBoylanKolchin2017",
            url_or_id="arXiv:1707.04256",
            kind="peer-reviewed paper (ARA&A 55, 343, 2017; small-scale "
                 "challenges review)",
        ),
        Source(
            label="TulinYu2018",
            url_or_id="arXiv:1705.02358",
            kind="peer-reviewed paper (Phys. Rep. 730, 1, 2018; dark-matter "
                 "self-interactions review)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "A major review catalogues persistent small-scale tensions "
                "between collisionless CDM simulations and observations — "
                "including cusp/core structure, missing satellites, and "
                "too-big-to-fail — while stressing that baryonic physics and "
                "survey incompleteness remain active confounders."
            ),
            source_ref="BullockBoylanKolchin2017",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Self-interacting dark matter is developed as one particle-"
                "physics response: velocity-dependent scattering can heat "
                "halos and help form cores, linking small-scale structure to "
                "microphysical cross sections without abandoning CDM on large "
                "scales."
            ),
            source_ref="TulinYu2018",
        ),
    ],
    open_questions=[
        "How much of each tension is baryonic feedback versus new dark-sector "
        "physics?",
        "Which combination of dwarfs, strong lensing and stellar streams most "
        "cleanly isolates the dark-matter microphysics?",
        "Do the tensions point to one common mechanism or several unrelated "
        "systematics?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Small-scale structure, hydrodynamical simulations and SIDM "
            "phenomenology form a fast-growing literature with dedicated "
            "reviews.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "There is no field-wide verdict that CDM is falsified on small "
            "scales, nor that baryons fully resolve every tension.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Satellite completeness, halo density profiles and feedback "
            "calibration are still incomplete for a decisive test.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4c — QCD axion / ALP as DM candidate             🟠 Frontier           #
# --------------------------------------------------------------------------- #
axion_dm_candidate = Claim(
    id="axion_dm_candidate",
    title=(
        "The QCD axion (or axion-like particle) is a viable dark-matter "
        "candidate under active laboratory search"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="BertoneTait2018d",
            url_or_id="doi:10.1038/s41586-018-0542-z",
            kind="peer-reviewed paper (Nature 562, 51-56, 2018)",
        ),
        Source(
            label="ADMX2018",
            url_or_id="arXiv:1804.05750",
            kind="collaboration result (peer-reviewed, PRL 120, 151301, 2018; "
                 "ADMX axion search)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Post-WIMP reviews keep the QCD axion and axion-like particles "
                "among the best-motivated non-WIMP candidates: they can be "
                "produced non-thermally in the early universe and match the "
                "observed dark-matter density in open parameter windows."
            ),
            source_ref="BertoneTait2018d",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The ADMX cavity experiment reports a resonant search for "
                "halo axions converting to photons in a magnetic field, "
                "excluding DFSZ-model axions over a band of microelectronvolt "
                "masses at high confidence — a null result that still "
                "demonstrates laboratory reach into cosmologically relevant "
                "axion parameter space."
            ),
            source_ref="ADMX2018",
        ),
    ],
    open_questions=[
        "Does the cosmological axion sit in a mass band current or near-term "
        "haloscopes can cover?",
        "How do ALP models without a QCD link change experimental priorities?",
        "Could axions be only a fraction of dark matter alongside other "
        "components?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Haloscope, helioscope and theory papers on axions/ALPs have "
            "expanded rapidly as WIMP space narrows.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Axions are a leading *candidate class*, not an established "
            "identification of dark matter.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No axion dark-matter signal has been confirmed; searches set "
            "limits and scan mass decades still largely unexplored.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4d — self-interacting DM for small scales        🟠 Frontier           #
# --------------------------------------------------------------------------- #
sidm_small_scales = Claim(
    id="sidm_small_scales",
    title=(
        "Velocity-dependent self-interacting dark matter can reconcile "
        "small-scale structure without spoiling large-scale success"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="TulinYu2018b",
            url_or_id="arXiv:1705.02358",
            kind="peer-reviewed paper (Phys. Rep. 730, 1, 2018)",
        ),
        Source(
            label="BullockBoylanKolchin2017b",
            url_or_id="arXiv:1707.04256",
            kind="peer-reviewed paper (ARA&A 55, 343, 2017)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Reviews of dark-matter self-interactions show that "
                "cross sections of order ~1 cm^2/g at dwarf velocities can "
                "thermalise inner halos and produce cores, while much smaller "
                "effective cross sections at cluster velocities remain "
                "compatible with merging-cluster constraints."
            ),
            source_ref="TulinYu2018b",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "The small-scale CDM challenge literature treats SIDM as one "
                "of the principal particle-physics alternatives to pure "
                "collisionless CDM plus baryons — still model-dependent and "
                "not uniquely selected by current data."
            ),
            source_ref="BullockBoylanKolchin2017b",
        ),
    ],
    open_questions=[
        "What velocity dependence is required simultaneously by dwarfs, "
        "LSBs and clusters?",
        "Can concrete microphysical models (light mediators, dark atoms) "
        "satisfy direct-detection and cosmological bounds?",
        "How does SIDM interact with baryonic feedback in modern "
        "hydrodynamical simulations?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "SIDM simulations, mediator models and cluster-constraint papers "
            "form a rapidly expanding subfield.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "SIDM is a serious research programme, not the default "
            "cosmological model; collisionless CDM plus baryons remains "
            "mainstream.",
        ),
        ConditionAssessment(
            "insufficient_sample", True,
            "Clean measurements of inner density profiles across a large, "
            "homogeneous galaxy sample are still limited.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4e — collider mono-jet / MET searches            🟠 Frontier           #
# --------------------------------------------------------------------------- #
monojet_collider_searches = Claim(
    id="monojet_collider_searches",
    title=(
        "LHC mono-jet and missing-transverse-momentum searches constrain "
        "dark-matter production without yet identifying a particle"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="LHCDMforum2015",
            url_or_id="arXiv:1507.00966",
            kind="peer-reviewed paper (Phys. Dark Univ. 2015; LHC Dark Matter "
                 "Working Group simplified-model recommendations)",
        ),
        Source(
            label="ATLASmonojet2021",
            url_or_id="arXiv:2102.10874",
            kind="collaboration result (peer-reviewed, Phys. Rev. D 103, "
                 "112006, 2021; ATLAS mono-jet + MET)",
        ),
        Source(
            label="CMSmonojet2021",
            url_or_id="arXiv:2107.13021",
            kind="collaboration result (peer-reviewed, JHEP 11 (2021) 153; "
                 "CMS jets + MET)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "The LHC Dark Matter Working Group defined simplified models "
                "and reporting standards so that mono-jet, mono-photon and "
                "related missing-energy searches can be compared to direct "
                "detection in a common mediator–DM parameter space — making "
                "colliders a laboratory channel parallel to underground "
                "detectors."
            ),
            source_ref="LHCDMforum2015",
        ),
        Evidence(
            type="direct observation",
            description=(
                "ATLAS searched 139 fb^-1 of 13 TeV proton–proton collisions "
                "for events with an energetic jet and large missing transverse "
                "momentum, finding no significant excess over Standard Model "
                "backgrounds and setting limits on invisible particle "
                "production."
            ),
            source_ref="ATLASmonojet2021",
        ),
        Evidence(
            type="direct observation",
            description=(
                "CMS performed a parallel jets-plus-missing-momentum search in "
                "the full Run-2 dataset, likewise observing no dark-matter "
                "signal and excluding large regions of simplified-model "
                "mediator and DM-mass space."
            ),
            source_ref="CMSmonojet2021",
        ),
    ],
    open_questions=[
        "Which mediator and coupling structures remain open after combining "
        "LHC mono-X limits with direct and indirect detection?",
        "Can HL-LHC or a future hadron collider reach thermal-relic WIMP "
        "benchmarks that current mono-jet searches miss?",
        "How should compressed spectra and long-lived dark-sector states be "
        "covered beyond classic mono-jet selections?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "ATLAS/CMS mono-X analyses, simplified-model recasts and "
            "HL-LHC projections form a large, continuously updated "
            "literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Colliders constrain production rates; they have not identified "
            "dark matter, and model dependence prevents a single closed "
            "verdict.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No excess attributed to dark matter has been established in "
            "mono-jet or related MET channels; only upper limits exist.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4f — fuzzy / wave (ultralight scalar) DM         🟠 Frontier           #
# --------------------------------------------------------------------------- #
fuzzy_wave_dark_matter = Claim(
    id="fuzzy_wave_dark_matter",
    title=(
        "Ultralight scalar 'fuzzy' dark matter with de Broglie-scale wave "
        "effects is a viable alternative to cold particle CDM on small scales"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="HuBarkanaGruzinov2000",
            url_or_id="arXiv:astro-ph/0003365",
            kind="peer-reviewed paper (Phys. Rev. Lett. 85, 1158, 2000; "
                 "fuzzy cold dark matter)",
        ),
        Source(
            label="Hui2017",
            url_or_id="arXiv:1610.08297",
            kind="peer-reviewed paper (Phys. Rev. D 95, 043541, 2017; "
                 "ultralight scalar DM review)",
        ),
        Source(
            label="Irsic2017",
            url_or_id="arXiv:1703.04683",
            kind="peer-reviewed paper (Phys. Rev. Lett. 119, 031302, 2017; "
                 "Lyman-α forest bounds on fuzzy DM)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Fuzzy cold dark matter proposes an ultralight boson whose "
                "de Broglie wavelength reaches kiloparsec scales in galactic "
                "halos, suppressing small-scale power and producing solitonic "
                "cores without invoking baryonic feedback alone."
            ),
            source_ref="HuBarkanaGruzinov2000",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "A comprehensive review of ultralight scalars as cosmological "
                "dark matter maps production mechanisms, Schrödinger–Poisson "
                "halo structure, and observational targets — establishing "
                "fuzzy/wave DM as a structured research programme rather than "
                "a single toy model."
            ),
            source_ref="Hui2017",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Lyman-α forest flux-power measurements are used to bound "
                "the ultralight boson mass from below: too-light fuzzy DM "
                "over-suppresses small-scale structure relative to the "
                "observed forest, squeezing the open mass window."
            ),
            source_ref="Irsic2017",
        ),
    ],
    open_questions=[
        "What mass window survives joint Lyman-α, dwarf-galaxy and black-hole "
        "superradiance constraints?",
        "Do solitonic cores and interference granules match observed dwarf "
        "and ultra-faint galaxy diversity better than CDM+baryons or SIDM?",
        "Is the QCD axion in the fuzzy regime, a distinct ALP, or neither "
        "required once feedback is fully modelled?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Wave-DM simulations, Lyman-α reanalyses and laboratory/axion "
            "connections produce a fast-growing literature since the 2010s.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Fuzzy DM is a serious alternative for small scales, not the "
            "default cosmological model; collisionless CDM remains mainstream.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No positive identification of an ultralight DM particle exists; "
            "constraints reshape the mass window without confirming it.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4g — dwarf spheroidal γ-ray limits               🟠 Frontier           #
# --------------------------------------------------------------------------- #
dwarf_spheroidal_indirect_limits = Claim(
    id="dwarf_spheroidal_indirect_limits",
    title=(
        "Fermi-LAT observations of dwarf spheroidal galaxies set strong "
        "limits on dark-matter annihilation without a confirmed signal"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Fermi dSph2015",
            url_or_id="arXiv:1503.02641",
            kind="collaboration result (peer-reviewed, Phys. Rev. Lett. 115, "
                 "231301, 2015; Fermi-LAT dSph joint analysis)",
        ),
        Source(
            label="Fermi dSph2017",
            url_or_id="arXiv:1611.03184",
            kind="collaboration result (peer-reviewed, ApJ 834, 110, 2017; "
                 "updated dSph search)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "A joint likelihood analysis of multiple Milky Way dwarf "
                "spheroidal galaxies with Fermi-LAT found no significant "
                "gamma-ray excess attributable to dark-matter annihilation "
                "and set limits intersecting thermal relic cross sections "
                "for masses of tens of GeV."
            ),
            source_ref="Fermi dSph2015",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "An updated Fermi-LAT dwarf-spheroidal search with more "
                "targets and refined J-factors again reported no globally "
                "significant annihilation signal, reinforcing dwarfs as a "
                "clean, if flux-limited, indirect-detection channel."
            ),
            source_ref="Fermi dSph2017",
        ),
    ],
    open_questions=[
        "How do J-factor systematics and newly discovered ultra-faints "
        "shift the combined limits?",
        "Can dwarfs rule out or support a dark-matter origin for the "
        "Galactic Centre excess at the same particle models?",
        "What CTA / wide-field survey synergy most improves sensitivity "
        "below current Fermi bounds?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Each Fermi catalog and each new ultra-faint dwarf spawns "
            "updated joint analyses and independent reanalyses.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Limits are widely used; a positive dwarf annihilation detection "
            "has not been established.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No confirmed DM annihilation signal in dSphs; constraints only.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4h — S8 / structure growth vs dark sector        🟡 Competing          #
# --------------------------------------------------------------------------- #
s8_structure_tension_dark_sector = Claim(
    id="s8_structure_tension_dark_sector",
    title=(
        "The S8 structure-growth tension is resolved by new dark-sector "
        "physics versus survey systematics within ΛCDM"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="DiValentino2021",
            url_or_id="arXiv:2008.11285",
            kind="peer-reviewed paper (Astropart. Phys. 131, 102604, 2021; "
                 "cosmic tension review)",
        ),
        Source(
            label="DESY3-2022",
            url_or_id="arXiv:2105.13549",
            kind="collaboration result (peer-reviewed, Phys. Rev. D 105, "
                 "023520, 2022; DES Y3 cosmological constraints)",
        ),
        Source(
            label="Planck2018-VIb",
            url_or_id="arXiv:1807.06209",
            kind="collaboration result (peer-reviewed, A&A 641, A6, 2020)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Reviews of cosmological tensions document a persistent "
                "mild-to-moderate discrepancy in the clustering amplitude "
                "S8 between primary CMB inferences and several weak-lensing "
                "/ galaxy-clustering surveys."
            ),
            source_ref="DiValentino2021",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Dark Energy Survey Year 3 3×2pt analyses prefer a lower S8 "
                "than Planck primary CMB when each is interpreted in flat "
                "ΛCDM, a result often cited as the observational core of "
                "the structure-growth tension."
            ),
            source_ref="DESY3-2022",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Planck 2018 baseline parameters fix a higher late-time "
                "clustering amplitude when extrapolated in ΛCDM, defining "
                "the CMB side of the comparison."
            ),
            source_ref="Planck2018-VIb",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="New dark-sector / late-time physics",
            supporting=(
                "Decaying, interacting or suppressed-growth dark-matter "
                "scenarios can lower S8 relative to primary CMB without "
                "abandoning early-universe successes in some fits."
            ),
            opposing=(
                "Many extensions reintroduce tensions elsewhere (CMB "
                "lensing, cluster counts, BAO) or require fine-tuned "
                "couplings."
            ),
            limitations=(
                "Model space is large; no single dark-sector fix is uniquely "
                "selected."
            ),
        ),
        CompetingModel(
            name="Systematics and ΛCDM consistency",
            supporting=(
                "Shear calibration, photo-z, intrinsic alignments and "
                "scale cuts can shift weak-lensing S8; some analyses find "
                "weaker tension under alternate pipelines."
            ),
            opposing=(
                "Multiple independent lensing teams report low S8, which "
                "is harder to dismiss as one experiment's flaw."
            ),
            limitations=(
                "Full end-to-end cross-survey consensus on residual "
                "systematics is still forming."
            ),
        ),
    ],
    open_questions=[
        "Will Euclid, LSST/Rubin and Roman reduce or sharpen the S8 offset?",
        "Which dark-sector models survive joint CMB + full-shape + lensing "
        "likelihoods?",
        "Is S8 the same physical tension as small-scale CDM challenges, or "
        "orthogonal?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Both dark-sector extensions and systematic / statistical "
            "reinterpretations of ΛCDM are actively published responses to "
            "S8.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "Tension significance depends on dataset combination; no "
            "decisive resolution exists.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Cosmology reviews and survey papers document a multi-year "
            "debate — not an AI-invented split.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4i — Fermi Galactic Centre excess                🟡 Competing          #
# --------------------------------------------------------------------------- #
fermi_gc_excess_origin = Claim(
    id="fermi_gc_excess_origin",
    title=(
        "The Fermi Galactic Centre gamma-ray excess is dark-matter "
        "annihilation versus unresolved astrophysical sources"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Daylan2016",
            url_or_id="arXiv:1402.6703",
            kind="peer-reviewed paper (Physics of the Dark Universe 12, 1, "
                 "2016; GC excess characterisation)",
        ),
        Source(
            label="LeaneSlatyer2019",
            url_or_id="arXiv:1904.08430",
            kind="peer-reviewed paper (PRL 123, 241101, 2019; challenges to "
                 "the pulsar-population interpretation)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Analyses of Fermi-LAT data find a roughly spherical GeV "
                "gamma-ray excess toward the Galactic Centre whose spectrum "
                "and morphology have been argued to match annihilating "
                "thermal WIMPs of tens of GeV."
            ),
            source_ref="Daylan2016",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Subsequent work shows that preferred non-Poissonian template "
                "fits to a faint millisecond-pulsar population can be "
                "pathological, reopening tension between the dark-matter and "
                "unresolved-source interpretations rather than closing the "
                "case for either."
            ),
            source_ref="LeaneSlatyer2019",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Dark-matter annihilation",
            supporting=(
                "Spectrum and approximate sphericity can match ~tens-of-GeV "
                "WIMP annihilation to Standard Model particles; the signal "
                "extends beyond the brightest stellar structures in some "
                "analyses."
            ),
            opposing=(
                "Required cross section and profile assumptions are "
                "model-dependent; other targets have not delivered a "
                "corroborating discovery."
            ),
            limitations=(
                "Galactic diffuse emission systematics dominate the "
                "uncertainty budget."
            ),
        ),
        CompetingModel(
            name="Unresolved astrophysical sources (e.g. MSPs)",
            supporting=(
                "A population of faint millisecond pulsars or other stellar "
                "remnants can produce a GeV excess with fewer new-physics "
                "assumptions."
            ),
            opposing=(
                "Claims that photon statistics uniquely prefer a point-source "
                "population have been challenged; the required population is "
                "not securely observed."
            ),
            limitations=(
                "Source-count and luminosity-function constraints remain "
                "incomplete in the inner Galaxy."
            ),
        ),
    ],
    open_questions=[
        "Can future gamma-ray, radio or stellar-remnant surveys break the "
        "degeneracy?",
        "Does the excess survive the most conservative Galactic diffuse "
        "models?",
        "If it is dark matter, why have dwarf-spheroidal searches not seen a "
        "clear counterpart?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Dark-matter annihilation and unresolved astrophysical sources "
            "are both actively published explanations for the same Fermi "
            "excess.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "No consensus analysis has eliminated either camp; systematics "
            "in the inner Galaxy remain large.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Competing papers and reviews document a multi-year split in the "
            "indirect-detection community — not an AI-asserted dichotomy.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5a — 7 keV sterile neutrino / 3.5 keV line       🔴 Speculative        #
# --------------------------------------------------------------------------- #
sterile_neutrino_7kev_line = Claim(
    id="sterile_neutrino_7kev_line",
    title=(
        "A ~7 keV sterile neutrino is the dark matter and produces the "
        "3.5 keV X-ray line"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Boyarsky2014",
            url_or_id="arXiv:1402.4119",
            kind="peer-reviewed paper (Phys. Rev. Lett. 113, 251301, 2014; "
                 "3.5 keV line in M31 and Perseus)",
        ),
        Source(
            label="Dessert2019",
            url_or_id="arXiv:1812.06976",
            kind="peer-reviewed paper (Science 367, 1465, 2020; blank-sky "
                 "challenge to the dark-matter line interpretation)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Stacked and individual X-ray spectra of galaxies and "
                "clusters were reported to show an unidentified emission "
                "feature near 3.5 keV, interpreted by some authors as the "
                "decay line of a ~7 keV sterile-neutrino dark-matter "
                "candidate."
            ),
            source_ref="Boyarsky2014",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "An independent blank-sky analysis argues that a dark-matter "
                "origin for the 3.5 keV feature is inconsistent with the "
                "non-observation of the line in deep fields where a Galactic "
                "halo sterile-neutrino signal should still appear — a direct "
                "challenge to the sterile-neutrino dark-matter claim."
            ),
            source_ref="Dessert2019",
        ),
    ],
    open_questions=[
        "Is the 3.5 keV feature astrophysical (e.g. charge exchange, "
        "potassium lines), instrumental, or a statistical artefact?",
        "Do XRISM and other high-resolution X-ray missions settle the "
        "line's existence and origin?",
        "If sterile neutrinos are dark matter, must they be only a fraction "
        "of the budget under current X-ray bounds?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "The 7 keV sterile-neutrino interpretation of the 3.5 keV line "
            "is not established consensus; multiple analyses dispute the "
            "line's existence or dark-matter origin.",
        ),
        ConditionAssessment(
            "philosophical_inference", False,
            "This is not a pure philosophy claim — it is an empirical X-ray "
            "controversy — so this entry condition does not carry the light.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4j — cluster bounds on DM self-interaction       🟠 Frontier           #
# --------------------------------------------------------------------------- #
cluster_sidm_cross_section_bounds = Claim(
    id="cluster_sidm_cross_section_bounds",
    title=(
        "Merging galaxy clusters bound the dark-matter self-interaction "
        "cross section per unit mass"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Harvey2015",
            url_or_id="arXiv:1503.07675",
            kind="peer-reviewed paper (Science 347, 1462, 2015; ensemble of "
                 "colliding clusters)",
        ),
        Source(
            label="Randall2008",
            url_or_id="arXiv:0704.0261",
            kind="peer-reviewed paper (ApJ 679, 1173, 2008; Bullet Cluster "
                 "self-interaction constraints)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "An ensemble analysis of colliding galaxy clusters measures "
                "the spatial offset between stars, gas and lensing mass to "
                "constrain the dark-matter self-interaction cross section "
                "per unit mass, finding consistency with collisionless "
                "behaviour within quoted uncertainties."
            ),
            source_ref="Harvey2015",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Bullet Cluster modelling places upper limits on σ/m from the "
                "survival and lack of drag of the dark-matter component "
                "relative to the collisional gas — a classic observational "
                "bound used by SIDM phenomenology."
            ),
            source_ref="Randall2008",
        ),
    ],
    open_questions=[
        "How much do merger geometry, projection and baryonic physics "
        "systematics loosen published σ/m limits?",
        "Can cluster bounds and dwarf-scale SIDM cores be satisfied by one "
        "velocity-dependent cross section?",
        "Will next-generation lensing surveys deliver a larger, cleaner "
        "merging-cluster sample?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Cluster merger constraints, hydro+N-body SIDM runs and ensemble "
            "lensing papers continue to refine σ/m limits.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "There is agreement that large constant σ/m is constrained, not "
            "a single settled number for all velocities.",
        ),
        ConditionAssessment(
            "insufficient_sample", True,
            "Clean, well-modelled major mergers remain few; ensemble analyses "
            "still grow.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4k — neutrino floor for direct detection         🟠 Frontier           #
# --------------------------------------------------------------------------- #
neutrino_floor_direct_detection = Claim(
    id="neutrino_floor_direct_detection",
    title=(
        "Coherent neutrino-nucleus scattering sets an irreducible background "
        "floor for WIMP direct detection"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Billard2014",
            url_or_id="arXiv:1307.5458",
            kind="peer-reviewed paper (Phys. Rev. D 89, 023524, 2014; "
                 "neutrino backgrounds / floor)",
        ),
        Source(
            label="Schumann2019b",
            url_or_id="arXiv:1903.03026",
            kind="peer-reviewed paper (J. Phys. G 46, 103003, 2019; "
                 "direct-detection review)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Calculations of solar, atmospheric and diffuse supernova "
                "neutrino coherent scattering on nuclei show a background "
                "that mimics WIMP recoils and defines a 'neutrino floor' "
                "(or fog) beyond which discovery claims require "
                "directional or spectral discrimination."
            ),
            source_ref="Billard2014",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Direct-detection reviews treat multi-tonne xenon/argon "
                "roadmaps as approaching this neutrino-limited regime and "
                "discuss technologies needed to work near or below it."
            ),
            source_ref="Schumann2019b",
        ),
    ],
    open_questions=[
        "Is the floor better described as a soft 'fog' with discovery "
        "potential remaining via statistics and directionality?",
        "Which target nuclei and energy windows hit the solar-neutrino "
        "component first?",
        "How should limit-setting experiments report sensitivity once "
        "exposures enter the neutrino-dominated region?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Neutrino-floor / fog calculations and next-generation detector "
            "design papers form a growing sub-literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "The existence of a neutrino background limit is accepted in "
            "outline; the precise discovery reach near it is still debated.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Experiments are approaching but have not fully mapped "
            "operations deep in the neutrino-dominated regime.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5 — primordial black holes as all DM             🔴 Speculative        #
# --------------------------------------------------------------------------- #
pbh_all_dark_matter = Claim(
    id="pbh_all_dark_matter",
    title="Primordial black holes constitute all of the dark matter",
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="CarrKuhnel2020",
            url_or_id="arXiv:2002.12778",
            kind="peer-reviewed paper (Annu. Rev. Nucl. Part. Sci. 70, 355, "
                 "2020; PBH constraints review)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "A comprehensive review of primordial black holes as dark-matter "
                "candidates shows that most mass windows are tightly constrained "
                "by microlensing, dynamics, accretion and gravitational waves; "
                "only limited windows remain, and 'all of DM is PBHs' is not "
                "the mainstream default."
            ),
            source_ref="CarrKuhnel2020",
        ),
    ],
    open_questions=[
        "Do any open mass windows still allow PBHs to be a substantial DM "
        "fraction without violating existing bounds?",
        "Can future gravitational-wave observatories settle or further "
        "squeeze those windows?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "Standard cosmology treats cold particle dark matter as the "
            "baseline; PBHs as *all* dark matter is a minority scenario under "
            "heavy observational pressure.",
        ),
        ConditionAssessment(
            "pure_theoretical_derivation", True,
            "The positive case is largely theoretical possibility plus "
            "constraint cartography, not a confirmed population that matches "
            "the full DM budget.",
        ),
    ],
    status_history=[],
)


DARK_MATTER = Topic(
    id="dark_matter",
    title="Dark matter",
    summary=(
        "Paper-grade map (see docs/dark-matter-paper-map.md). Container only "
        "— no topic light. I 🟢 mass discrepancy · 🔵 ΛCDM cold DM; "
        "II 🟡 particle vs MOND · 🟠 small scales; III–IV 🟠 WIMP/direct/"
        "mono-jet/axion/SIDM/fuzzy/dSph/cluster σ⁄m/neutrino floor · "
        "🔴 sterile ν & PBH; V 🟡 GC excess & S8. Identity remains open."
    ),
    claims=[
        mass_discrepancy_observed,
        lcdm_includes_cold_dm,
        particle_vs_modified_gravity,
        dm_particle_identity,
        thermal_wimp_freezeout_benchmark,
        direct_detection_wimp_searches,
        neutrino_floor_direct_detection,
        small_scale_cdm_challenges,
        axion_dm_candidate,
        sidm_small_scales,
        cluster_sidm_cross_section_bounds,
        monojet_collider_searches,
        fuzzy_wave_dark_matter,
        dwarf_spheroidal_indirect_limits,
        fermi_gc_excess_origin,
        s8_structure_tension_dark_sector,
        sterile_neutrino_7kev_line,
        pbh_all_dark_matter,
    ],
)
