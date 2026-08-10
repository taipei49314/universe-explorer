"""Stars — stellar physics domain (cosmos theme).

Complements black_hole (endpoints) and cosmology (large-scale). Same courts.

Deepened map (solar interior · remnants · birth/death channels):

  🟢 stars_powered_by_fusion
  🔵 stellar_nucleosynthesis_makes_elements
  🔵 core_collapse_forms_ns_bh
  🔵 helioseismology_constrains_solar_interior
  🔵 white_dwarfs_electron_degenerate
  🔵 imf_approximately_universal
  🟡 red_supergiant_problem
  🟡 sn_ia_progenitor_channels
  🟠 solar_dynamo_cycle
  🟠 cno_cycle_solar_neutrinos_detected
  🟠 pair_instability_bh_mass_gap
  🔴 pop_iii_already_routinely_observed
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
# Claim 1 — fusion powers stars                          🟢 Established        #
# --------------------------------------------------------------------------- #
stars_powered_by_fusion = Claim(
    id="stars_powered_by_fusion",
    title="Main-sequence stars are powered by nuclear fusion in their cores",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="SNO2002",
            url_or_id="arXiv:nucl-ex/0204008",
            kind="collaboration result (peer-reviewed, PRL 89, 011301, 2002; "
                 "SNO solar neutrinos)",
        ),
        Source(
            label="SuperK2001",
            url_or_id="arXiv:hep-ex/0103032",
            kind="collaboration result (peer-reviewed, ApJ 539, 558, 2000; "
                 "Super-Kamiokande solar neutrinos)",
        ),
        Source(
            label="Bethe1939",
            url_or_id="doi:10.1103/PhysRev.55.434",
            kind="peer-reviewed paper (Phys. Rev. 55, 434, 1939; fusion "
                 "chains)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "The Sudbury Neutrino Observatory measures solar electron "
                "neutrinos via charged-current and neutral-current channels, "
                "confirming the flux expected from core hydrogen fusion."
            ),
            source_ref="SNO2002",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Super-Kamiokande detects a large sample of solar neutrinos "
                "scattering on electrons, independently confirming a nuclear "
                "fusion origin for the solar luminosity."
            ),
            source_ref="SuperK2001",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Bethe's nuclear reaction chains (pp and CNO) provide the "
                "theoretical energy budget of main-sequence stars via "
                "hydrogen fusion to helium."
            ),
            source_ref="Bethe1939",
        ),
    ],
    open_questions=[
        "How do convection and magnetic fields couple to fusion-driven "
        "structure in low-mass stars?",
        "What are the precise rates of key rare reactions at stellar "
        "energies?",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Independent solar-neutrino experiments (SNO, Super-Kamiokande) "
            "and nuclear theory converge on fusion-powered main sequences.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Fusion-powered stars are standard content in every modern "
            "astrophysics textbook.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream theory replaces core fusion for main-sequence "
            "energy generation.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Neutrino and helioseismic data have strengthened, not "
            "overturned, the fusion picture.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — nucleosynthesis                              🔵 Strong             #
# --------------------------------------------------------------------------- #
stellar_nucleosynthesis_makes_elements = Claim(
    id="stellar_nucleosynthesis_makes_elements",
    title=(
        "Most chemical elements heavier than helium are made in stars and "
        "stellar explosions"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="B2FH1957",
            url_or_id="doi:10.1103/RevModPhys.29.547",
            kind="peer-reviewed paper (Rev. Mod. Phys. 29, 547, 1957; B2FH)",
        ),
        Source(
            label="Abbott2017-kilonova",
            url_or_id="arXiv:1710.05841",
            kind="collaboration result (peer-reviewed, ApJL 848, L12, 2017; "
                 "GW170817 kilonova)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "The B2FH framework maps stellar burning stages and explosive "
                "nucleosynthesis pathways that build the elements beyond "
                "helium observed in the cosmos."
            ),
            source_ref="B2FH1957",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The GW170817 kilonova spectrum and light curve match "
                "r-process nucleosynthesis in a neutron-star merger, "
                "confirming a stellar-endpoint site for heavy elements."
            ),
            source_ref="Abbott2017-kilonova",
        ),
    ],
    open_questions=[
        "What fraction of r-process elements come from mergers versus "
        "rare supernovae?",
        "How do the first Population III stars seed early metals?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Stellar and explosive nucleosynthesis is the standard account "
            "of elemental abundances.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Relative site contributions (AGB, CCSN, mergers) are debated; "
            "the stellar origin itself is not.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Multi-messenger astronomy has expanded confirmed sites without "
            "displacing the stellar nucleosynthesis paradigm.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — core-collapse endpoints                      🔵 Strong             #
# --------------------------------------------------------------------------- #
core_collapse_forms_ns_bh = Claim(
    id="core_collapse_forms_ns_bh",
    title=(
        "Core-collapse supernovae leave behind neutron stars or black holes"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="BaadeZwicky1934",
            url_or_id="doi:10.1073/pnas.20.5.254",
            kind="peer-reviewed paper (PNAS 20, 254, 1934; supernovae / "
                 "neutron stars)",
        ),
        Source(
            label="LIGO2016-GW150914b",
            url_or_id="arXiv:1602.03837",
            kind="collaboration result (peer-reviewed, PRL 116, 061102, 2016; "
                 "BBH merger)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Core collapse of massive stars was proposed to power "
                "supernovae and form ultra-dense neutron-star remnants."
            ),
            source_ref="BaadeZwicky1934",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Gravitational-wave detections of binary black hole and "
                "neutron-star mergers, together with Galactic pulsars and "
                "SN remnants, confirm compact remnants of stellar death."
            ),
            source_ref="LIGO2016-GW150914b",
        ),
    ],
    open_questions=[
        "Where is the mass threshold between neutron-star and black-hole "
        "remnants?",
        "How often do failed supernovae collapse quietly to black holes?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Compact remnants from massive-star death are standard "
            "astrophysics.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Details of explosion engines and mass gaps are active research, "
            "not alternatives to remnant formation itself.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Pulsars, X-ray binaries and GW catalogues continually reinforce "
            "the remnant picture.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — red supergiant problem                       🟡 Competing          #
# --------------------------------------------------------------------------- #
red_supergiant_problem = Claim(
    id="red_supergiant_problem",
    title=(
        "The missing high-mass red-supergiant supernova progenitors is a "
        "real physical effect versus an observational bias"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Smartt2009",
            url_or_id="arXiv:0809.0403",
            kind="peer-reviewed paper (ARA&A 47, 63, 2009; SN progenitors)",
        ),
        Source(
            label="DaviesBeasor2020",
            url_or_id="arXiv:2001.06020",
            kind="peer-reviewed paper (MNRAS; upper luminosity boundary / "
                 "RSG problem)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Archival imaging of Type IIP supernova sites finds red "
                "supergiant progenitors up to a mass ceiling well below the "
                "expected upper RSG mass — the classic 'red supergiant "
                "problem'."
            ),
            source_ref="Smartt2009",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Reanalyses of bolometric corrections and sample biases argue "
                "the apparent mass cutoff can be reduced or removed, "
                "challenging a purely physical disappearance of high-mass "
                "RSG explosions."
            ),
            source_ref="DaviesBeasor2020",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Physical cutoff (failed SN / direct collapse)",
            supporting=(
                "Most massive RSGs may collapse with weak or failed "
                "optical supernovae, explaining a missing high-mass "
                "progenitor bin."
            ),
            opposing=(
                "Direct-collapse rates and luminosity calibrations remain "
                "uncertain."
            ),
            limitations=(
                "Small progenitor sample sizes."
            ),
        ),
        CompetingModel(
            name="Observational / calibration bias",
            supporting=(
                "Updated bolometric corrections and dust treatment can raise "
                "inferred progenitor masses and ease the discrepancy."
            ),
            opposing=(
                "Even revised samples may not fully populate the highest "
                "mass bins expected from stellar models."
            ),
            limitations=(
                "Depends on pre-explosion photometry quality."
            ),
        ),
    ],
    open_questions=[
        "Will larger transient surveys find luminous RSG progenitors above "
        "the disputed ceiling?",
        "Can neutrino or GW signatures of failed supernovae be detected?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Physical failed-SN explanations and calibration-bias "
            "explanations are both actively published.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "Progenitor samples remain small; the cutoff significance is "
            "contested.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "A multi-year literature debate documents the split.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5 — solar dynamo / cycle                         🟠 Frontier           #
# --------------------------------------------------------------------------- #
solar_dynamo_cycle = Claim(
    id="solar_dynamo_cycle",
    title=(
        "The Sun's 11-year activity cycle is generated by an interior "
        "magnetic dynamo"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Charbonneau2010",
            url_or_id="doi:10.12942/lrsp-2010-3",
            kind="peer-reviewed paper (Living Rev. Sol. Phys. 7, 3, 2010; "
                 "dynamo models of the solar cycle; superseded by "
                 "10.1007/s41116-020-00025-6)",
        ),
        Source(
            label="Charbonneau2020",
            url_or_id="doi:10.1007/s41116-020-00025-6",
            kind="peer-reviewed paper (Living Rev. Sol. Phys. 2020; "
                 "publisher new_version of Charbonneau2010 dynamo review)",
        ),
        Source(
            label="Hathaway2015",
            url_or_id="arXiv:1502.07020",
            kind="peer-reviewed paper (Living Rev. Sol. Phys.; solar cycle)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Mean-field and flux-transport dynamo models generate "
                "oscillatory large-scale fields that reverse polarity each "
                "cycle, providing the leading framework for the solar cycle."
            ),
            source_ref="Charbonneau2020",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Sunspot records, magnetograms and helioseismic constraints "
                "map the cyclic emergence and migration of magnetic flux "
                "over centuries of observation."
            ),
            source_ref="Hathaway2015",
        ),
    ],
    open_questions=[
        "What sets cycle amplitude and the Maunder-type minima?",
        "Can dynamos predict the next cycle peak with useful skill?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Solar dynamo theory and cycle forecasting remain highly active.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "A dynamo origin is widely accepted in outline; the detailed "
            "engine is not uniquely settled.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "The deep tachocline and interior field are only indirectly "
            "constrained.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 6 — first stars never formed                     🔴 Speculative        #
# --------------------------------------------------------------------------- #
# Better speculative: Population III already detected as claim that's false
pop_iii_already_routinely_observed = Claim(
    id="pop_iii_already_routinely_observed",
    title=(
        "Metal-free Population III stars are routinely observed in the "
        "local universe"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="BrommLarson2004",
            url_or_id="arXiv:astro-ph/0311019",
            kind="peer-reviewed paper (ARA&A 42, 79, 2004; first stars "
                 "review)",
        ),
        Source(
            label="B2FH1957b",
            url_or_id="doi:10.1103/RevModPhys.29.547",
            kind="peer-reviewed paper (Rev. Mod. Phys. 29, 547, 1957)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Theory places true metal-free Population III stars in the "
                "early universe; they are not expected as a routine local "
                "stellar population."
            ),
            source_ref="BrommLarson2004",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Galactic chemical evolution and nucleosynthesis frameworks "
                "treat surviving local stars as metal-enriched descendants, "
                "not pristine Pop III members."
            ),
            source_ref="B2FH1957b",
        ),
    ],
    open_questions=[
        "Can JWST isolate individual Pop III stellar signatures at high "
        "redshift?",
        "Do any ultra metal-poor local stars retain a pure Pop III imprint?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "The field does not accept routine local observation of "
            "metal-free Pop III stars.",
        ),
        ConditionAssessment(
            "no_observational_evidence", True,
            "Recorded evidence points to early-universe formation, not a "
            "local routine Pop III census.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 7 — helioseismology                              🔵 Strong             #
# --------------------------------------------------------------------------- #
helioseismology_constrains_solar_interior = Claim(
    id="helioseismology_constrains_solar_interior",
    title=(
        "Helioseismology tightly constrains the Sun's interior structure "
        "and validates standard solar models in bulk"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="ChristensenDalsgaard2002",
            url_or_id="arXiv:astro-ph/0207403",
            kind="peer-reviewed paper (Rev. Mod. Phys. 74, 1073, 2002; "
                 "helioseismology review)",
        ),
        Source(
            label="Bahcall2001",
            url_or_id="arXiv:astro-ph/0010346",
            kind="peer-reviewed paper (ApJ; solar models, neutrinos, "
                 "helioseismology)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Global p-mode frequencies invert to sound-speed and density "
                "profiles throughout most of the solar interior, providing "
                "a seismic map of the convective zone and radiative core."
            ),
            source_ref="ChristensenDalsgaard2002",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Standard solar models matched to helioseismic constraints "
                "reproduce the observed acoustic structure and inform the "
                "neutrino flux predictions later confirmed experimentally."
            ),
            source_ref="Bahcall2001",
        ),
    ],
    open_questions=[
        "How should revised solar abundances be reconciled with the "
        "seismic sound-speed profile (the solar abundance problem)?",
        "What is the detailed structure of the tachocline?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Helioseismic inversion as a probe of solar structure is "
            "standard solar physics.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Abundance mixtures and near-surface modelling details remain "
            "debated; the bulk seismic success is not.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Decades of BiSON/GONG/SOHO/SDO data have refined, not "
            "overturned, the seismic interior picture.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 8 — white dwarfs                                 🔵 Strong             #
# --------------------------------------------------------------------------- #
white_dwarfs_electron_degenerate = Claim(
    id="white_dwarfs_electron_degenerate",
    title=(
        "White dwarfs are supported against gravity by electron degeneracy "
        "pressure"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="Chandrasekhar1931",
            url_or_id="doi:10.1086/143324",
            kind="peer-reviewed paper (ApJ 74, 81, 1931; highly collapsed "
                 "configurations / mass limit)",
        ),
        Source(
            label="B2FH1957c",
            url_or_id="doi:10.1103/RevModPhys.29.547",
            kind="peer-reviewed paper (Rev. Mod. Phys. 29, 547, 1957; "
                 "stellar endpoints context)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Electron-degenerate configurations yield a finite maximum "
                "white-dwarf mass (the Chandrasekhar limit) set by quantum "
                "statistics and general relativity corrections."
            ),
            source_ref="Chandrasekhar1931",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Observed white-dwarf mass distributions and cooling "
                "sequences align with degenerate-electron support as the "
                "endpoint of low- and intermediate-mass stellar evolution."
            ),
            source_ref="B2FH1957c",
        ),
    ],
    open_questions=[
        "What is the precise empirical Chandrasekhar mass for exploding "
        "white dwarfs in Type Ia events?",
        "How do crystallization and core composition affect cooling ages?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Degenerate white dwarfs are textbook stellar endpoints.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Composition, rotation and magnetic corrections refine masses; "
            "they do not replace degeneracy support.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Gaia white-dwarf sequences and binary mass measurements "
            "continually reinforce the degenerate picture.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 9 — IMF                                          🔵 Strong             #
# --------------------------------------------------------------------------- #
imf_approximately_universal = Claim(
    id="imf_approximately_universal",
    title=(
        "The stellar initial mass function is approximately universal in "
        "present-day star-forming regions"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="Bastian2010",
            url_or_id="arXiv:1001.2965",
            kind="peer-reviewed paper (ARA&A 48, 339, 2010; universal IMF "
                 "review)",
        ),
        Source(
            label="Kroupa2001",
            url_or_id="arXiv:astro-ph/0009005",
            kind="peer-reviewed paper (MNRAS 322, 231, 2001; multi-part "
                 "power-law IMF)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Resolved stellar populations in the local field, open "
                "clusters and nearby galaxies yield similar high-mass "
                "slopes near the Salpeter value over a wide range of "
                "environments."
            ),
            source_ref="Bastian2010",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "A multi-part power-law (or similar) IMF fits local star "
                "counts from brown-dwarf to O-star masses with only modest "
                "environment-to-environment scatter in the present-day "
                "disc."
            ),
            source_ref="Kroupa2001",
        ),
    ],
    open_questions=[
        "Is the IMF top-heavy in extreme starbursts or at very low "
        "metallicity?",
        "How does the substellar mass function connect to the stellar IMF?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "An approximately universal local IMF is the default assumption "
            "in galactic chemical evolution and population synthesis.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Top-heavy or bottom-light IMFs are proposed for extreme "
            "environments; they are refinements of universality, not a "
            "replacement of the IMF concept.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Decades of star-count and cluster work leave the local IMF "
            "shape stable even as extremes are debated.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 10 — SN Ia progenitors                           🟡 Competing          #
# --------------------------------------------------------------------------- #
sn_ia_progenitor_channels = Claim(
    id="sn_ia_progenitor_channels",
    title=(
        "Type Ia supernovae arise primarily via the single-degenerate "
        "versus double-degenerate channel"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Maoz2014",
            url_or_id="arXiv:1312.0628",
            kind="peer-reviewed paper (ARA&A 52, 107, 2014; SN Ia "
                 "progenitor clues)",
        ),
        Source(
            label="B2FH1957d",
            url_or_id="doi:10.1103/RevModPhys.29.547",
            kind="peer-reviewed paper (Rev. Mod. Phys. 29, 547, 1957; "
                 "explosive nucleosynthesis context)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Delay-time distributions, companion searches, radio/X-ray "
                "limits and pre-explosion constraints leave both "
                "single-degenerate (WD + non-degenerate donor) and "
                "double-degenerate (WD + WD) channels viable at population "
                "level."
            ),
            source_ref="Maoz2014",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Explosive carbon burning in a near-Chandrasekhar or "
                "sub-Chandrasekhar white dwarf reproduces the hallmark "
                "intermediate-mass-element and iron-group yields of Type Ia "
                "events in outline."
            ),
            source_ref="B2FH1957d",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Single-degenerate (WD + non-degenerate companion)",
            supporting=(
                "Accretion toward the Chandrasekhar mass provides a natural "
                "explosion trigger; some systems show possible companion "
                "signatures."
            ),
            opposing=(
                "Stringent non-detections of companions and circumstellar "
                "material in many events challenge a universal SD channel."
            ),
            limitations=(
                "Retention efficiency and steady burning regimes are "
                "uncertain."
            ),
        ),
        CompetingModel(
            name="Double-degenerate (WD + WD merger / collision)",
            supporting=(
                "Delay-time distributions and the absence of surviving "
                "companions favour WD+WD pathways in a large fraction of "
                "events."
            ),
            opposing=(
                "Which mergers ignite as normal SNe Ia versus collapse or "
                "fail remains model-dependent."
            ),
            limitations=(
                "Merger hydrodynamics and viewing-angle diversity are hard "
                "to constrain event-by-event."
            ),
        ),
    ],
    open_questions=[
        "What fraction of normal SNe Ia come from each channel?",
        "Do sub-Chandrasekhar double detonations dominate some subclasses?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Single- and double-degenerate families are both extensively "
            "developed in the peer-reviewed literature.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "No single observation has eliminated either channel for the "
            "normal SN Ia population.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Reviews document a multi-decade camp structure, not a "
            "rhetorical split.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 11 — CNO solar neutrinos                         🟠 Frontier           #
# --------------------------------------------------------------------------- #
cno_cycle_solar_neutrinos_detected = Claim(
    id="cno_cycle_solar_neutrinos_detected",
    title=(
        "Neutrinos from the solar CNO cycle have been experimentally "
        "detected"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Borexino2020-CNO",
            url_or_id="arXiv:2006.15115",
            kind="collaboration result (peer-reviewed, Nature 2020; first "
                 "CNO solar-neutrino evidence)",
        ),
        Source(
            label="Borexino2023-CNO",
            url_or_id="arXiv:2307.14636",
            kind="collaboration result (peer-reviewed; Borexino final CNO "
                 "results with CID method)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Borexino reports the first experimental evidence of solar "
                "neutrinos produced in the carbon–nitrogen–oxygen fusion "
                "cycle, using an ultra-radio-pure liquid scintillator."
            ),
            source_ref="Borexino2020-CNO",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Subsequent Borexino analyses incorporating correlated "
                "integrated directionality strengthen the CNO neutrino "
                "measurement and reduce background systematics."
            ),
            source_ref="Borexino2023-CNO",
        ),
    ],
    open_questions=[
        "How precisely can CNO neutrinos constrain the solar core "
        "metallicity?",
        "Will next-generation scintillator experiments turn CNO into a "
        "precision metallicity probe?",
    ],
    status_reason=[
        ConditionAssessment(
            "new_discovery", True,
            "First detection of CNO-cycle solar neutrinos is a recent "
            "experimental milestone.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "The community accepts the detection in outline; its use as a "
            "decisive metallicity arbiter is still developing.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Event statistics and residual backgrounds still limit "
            "precision relative to pp-chain neutrino measurements.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 12 — pair-instability mass gap                   🟠 Frontier           #
# --------------------------------------------------------------------------- #
pair_instability_bh_mass_gap = Claim(
    id="pair_instability_bh_mass_gap",
    title=(
        "Pair-instability supernovae carve a gap in the stellar black-hole "
        "mass spectrum near ~50–120 solar masses"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Farmer2019",
            url_or_id="arXiv:1910.12874",
            kind="peer-reviewed paper (ApJ; lower edge of the PISN black "
                 "hole mass gap)",
        ),
        Source(
            label="Woosley2017",
            url_or_id="arXiv:1608.08939",
            kind="peer-reviewed paper (ApJ; pulsational pair instability "
                 "and massive star deaths)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Electron–positron pair production in very massive stellar "
                "cores triggers pulsational or complete pair-instability "
                "supernovae that are predicted to leave a gap in remnant "
                "black-hole masses."
            ),
            source_ref="Woosley2017",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Modern stellar models map the lower edge of the predicted "
                "gap as a function of nuclear rates and wind physics, "
                "providing targets for gravitational-wave mass spectra."
            ),
            source_ref="Farmer2019",
        ),
    ],
    open_questions=[
        "Do current LIGO–Virgo–KAGRA catalogues show a clean high-mass "
        "gap, or is it blurred by hierarchical mergers?",
        "How sensitive is the gap edge to the 12C(α,γ)16O rate?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "PISN mass-gap predictions and GW mass-spectrum tests form a "
            "fast-moving literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "The theoretical gap is widely discussed; its empirical "
            "sharpness in observed BH masses is not settled.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "GW samples at the highest stellar BH masses remain limited.",
        ),
    ],
    status_history=[],
)


STARS = Topic(
    id="stars",
    title="Stars",
    summary=(
        "Stellar physics container (cosmos theme). 🟢 fusion; 🔵 "
        "nucleosynthesis, remnants, helioseismology, white dwarfs, IMF; "
        "🟡 RSG problem + SN Ia channels; 🟠 dynamo, CNO neutrinos, "
        "PISN mass gap; 🔴 routine local Pop III (not accepted)."
    ),
    claims=[
        stars_powered_by_fusion,
        stellar_nucleosynthesis_makes_elements,
        core_collapse_forms_ns_bh,
        helioseismology_constrains_solar_interior,
        white_dwarfs_electron_degenerate,
        imf_approximately_universal,
        red_supergiant_problem,
        sn_ia_progenitor_channels,
        solar_dynamo_cycle,
        cno_cycle_solar_neutrinos_detected,
        pair_instability_bh_mass_gap,
        pop_iii_already_routinely_observed,
    ],
)
