"""Stars — stellar physics domain (cosmos theme).

Complements black_hole (endpoints) and cosmology (large-scale). Same courts.

Expected lights:
  stars_powered_by_fusion                 -> 🟢 Established
  stellar_nucleosynthesis_makes_elements  -> 🔵 Strong
  core_collapse_forms_ns_bh               -> 🔵 Strong
  red_supergiant_problem                  -> 🟡 Competing
  solar_dynamo_cycle                      -> 🟠 Frontier
  pop_iii_already_routinely_observed      -> 🔴 Speculative
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
                 "dynamo models of the solar cycle)",
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
            source_ref="Charbonneau2010",
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


STARS = Topic(
    id="stars",
    title="Stars",
    summary=(
        "Stellar physics container (cosmos theme). 🟢 fusion bedrock; 🔵 "
        "nucleosynthesis + compact remnants; 🟡 red-supergiant problem; "
        "🟠 solar dynamo; 🔴 routine local Pop III (not accepted)."
    ),
    claims=[
        stars_powered_by_fusion,
        stellar_nucleosynthesis_makes_elements,
        core_collapse_forms_ns_bh,
        red_supergiant_problem,
        solar_dynamo_cycle,
        pop_iii_already_routinely_observed,
    ],
)
