"""Exoplanets — the third domain (docs/third-domain note in p4-spec lineage).

Second cross-domain stress test. Unlike the ocean topic, most sources here ARE
on arXiv — so this domain also re-exercises the P1 cite=>fetch pipeline on
fresh ids. Every source verified online before writing (journal, volume, arXiv
id); Mayor & Queloz 1995 predates arXiv posting for Nature and is honestly
exempt like the print sources elsewhere.

Expected lights:
  exoplanets_exist            -> 🟢 Established (E1: RV + transit, independent)
  planet_nine                 -> 🟡 Competing   (clustering real vs survey bias)
  trappist1b_bare_rock        -> 🟠 Frontier    (JWST era just opening)
  k2_18b_biosignature         -> 🔴 Speculative (observation exists, mainstream unconvinced)
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
# Claim 1 — exoplanets exist                              🟢 Established       #
# --------------------------------------------------------------------------- #
exoplanets_exist = Claim(
    id="exoplanets_exist",
    title="Planets orbiting other stars exist",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="MayorQueloz1995",
            url_or_id="Nature 378, 355-359 (1995)",
            kind="peer-reviewed paper (51 Peg b radial-velocity discovery; "
                 "2019 Nobel Prize in Physics)",
        ),
        Source(
            label="Charbonneau2000",
            url_or_id="arXiv:astro-ph/9911436",
            kind="peer-reviewed paper (ApJ 529, L45; first transit, HD 209458 b)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Radial-velocity measurements of 51 Pegasi revealed a Jupiter-"
                "mass companion in a 4.2-day orbit — the first exoplanet found "
                "around a Sun-like star."
            ),
            source_ref="MayorQueloz1995",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Photometry of HD 209458 caught the planet crossing its star at "
                "exactly the times predicted by radial velocity — an entirely "
                "independent detection method confirming the planet "
                "interpretation."
            ),
            source_ref="Charbonneau2000",
        ),
    ],
    open_questions=[
        "How representative the known population is remains limited by "
        "detection biases toward large, close-in planets.",
        "Occurrence rates of true Earth analogues are still being pinned down.",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Two independent methods (radial velocity, transits) confirmed the "
            "same planet class; thousands of planets have since been found by "
            "multiple surveys and instruments.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Exoplanets are standard content in astronomy textbooks and the "
            "1995 discovery earned the 2019 Nobel Prize in Physics.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream alternative explains the combined radial-velocity, "
            "transit and direct-imaging evidence.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Every subsequent survey has enlarged, never undermined, the "
            "population.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 1c — Proxima b exists                             🟢 Established       #
# (T5 cycle: sources chosen and web-verified by human; T4 LLM drafting was
#  lawfully rejected on the multi-source case — see t4-spec §1.5 — so this
#  one was authored manually on the fetched, verified sources.)
# --------------------------------------------------------------------------- #
proxima_b_exists = Claim(
    id="proxima_b_exists",
    title="The nearest star, Proxima Centauri, hosts a temperate "
          "Earth-mass planet",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="AngladaEscude2016",
            url_or_id="arXiv:1609.03449",
            kind="peer-reviewed paper (Nature 536, 437-440, 2016)",
        ),
        Source(
            label="SuarezMascareno2020",
            url_or_id="arXiv:2005.12114",
            kind="peer-reviewed paper (A&A 639, A77, 2020; independent "
                 "ESPRESSO confirmation)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Radial-velocity monitoring revealed a minimum-mass ~1.3 "
                "Earth-mass planet in an 11.2-day temperate orbit around "
                "Proxima Centauri."
            ),
            source_ref="AngladaEscude2016",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The independent, higher-precision ESPRESSO spectrograph "
                "re-detected the same 11.2-day signal in fresh 2019 data, "
                "confirming the planet and refining its minimum mass."
            ),
            source_ref="SuarezMascareno2020",
        ),
    ],
    open_questions=[
        "Whether the planet retains an atmosphere under its M-dwarf host's "
        "flaring is unknown.",
        "Its true (not minimum) mass depends on the unmeasured orbital "
        "inclination.",
        "Whether conditions on a tidally influenced temperate planet permit "
        "surface liquid water is open.",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Two independent instruments and teams (HARPS/UVES campaign 2016; "
            "ESPRESSO 2020, further re-confirmed in later ESPRESSO analyses) "
            "detect the same planetary signal.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Proxima b is standard content in current astronomy teaching "
            "materials and exoplanet references as the nearest known "
            "exoplanet.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "The early stellar-activity-artifact concern was tested and "
            "rejected by the independent ESPRESSO data; no mainstream "
            "alternative to the planet interpretation remains.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Subsequent radial-velocity campaigns have only sharpened the "
            "detection.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 1b — planets are the rule                         🔵 Strong            #
# --------------------------------------------------------------------------- #
planets_are_common = Claim(
    id="planets_are_common",
    title="Planets are the rule rather than the exception around Milky Way stars",
    status=Status.STRONG,
    sources=[
        Source(
            label="Cassan2012",
            url_or_id="doi:10.1038/nature10684",
            kind="peer-reviewed paper (Nature 481, 167-169, 2012)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "A statistical analysis of six years of microlensing survey "
                "data concludes that Milky Way stars host on average one or "
                "more bound planets, making planets the rule rather than the "
                "exception."
            ),
            source_ref="Cassan2012",
        ),
    ],
    open_questions=[
        "Occurrence rates for true Earth analogues in habitable zones remain "
        "the least constrained part of the statistics.",
        "How occurrence varies with stellar type, metallicity and Galactic "
        "environment is still being mapped.",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Independent survey methods (microlensing, transit statistics, "
            "radial-velocity surveys) converge on planetary abundance.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Methodological debates persist over completeness corrections and "
            "exact occurrence numbers, not over abundance itself.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Every enlarged survey has raised, never lowered, the inferred "
            "abundance of planets. Note: the statistical (indirect) character "
            "of the evidence is expressed structurally on the evidence axis.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — Planet Nine                                   🟡 Competing         #
# --------------------------------------------------------------------------- #
planet_nine = Claim(
    id="planet_nine",
    title="A ninth giant planet shapes distant Kuiper-belt orbits",
    status=Status.COMPETING,
    sources=[
        Source(
            label="BatyginBrown2016",
            url_or_id="arXiv:1601.05438",
            kind="peer-reviewed paper (AJ 151, 22, 2016)",
        ),
        Source(
            label="Shankman2017",
            url_or_id="arXiv:1706.04175",
            kind="peer-reviewed paper (AJ, OSSOS VI, 2017)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Distant Kuiper-belt objects show clustering of orbital angles "
                "that dynamical modelling attributes to an unseen giant planet "
                "on a distant eccentric orbit."
            ),
            source_ref="BatyginBrown2016",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "The independent OSSOS survey found its detections consistent "
                "with a uniform (unclustered) distribution and demonstrated "
                "strong pointing biases in the surveys behind the clustering "
                "signal."
            ),
            source_ref="Shankman2017",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Planet Nine exists",
            supporting=(
                "Observed orbital clustering of distant trans-Neptunian objects "
                "is dynamically reproduced by a distant super-Earth-to-Neptune-"
                "mass planet."
            ),
            opposing=(
                "No direct detection despite years of targeted searches; the "
                "clustering may be a survey artefact."
            ),
            limitations=(
                "Predicted orbit and mass keep being revised as the sample of "
                "distant objects grows."
            ),
        ),
        CompetingModel(
            name="Clustering is observational bias",
            supporting=(
                "A well-characterised independent survey (OSSOS) is consistent "
                "with uniform orbital angles once its biases are modelled."
            ),
            opposing=(
                "Bias-corrected analyses of the combined surveys still find "
                "residual clustering that is hard to dismiss entirely."
            ),
            limitations=(
                "Individual surveys cover limited sky, weakening their power to "
                "confirm or exclude the clustering."
            ),
        ),
    ],
    open_questions=[
        "Will wide-field surveys (e.g. Rubin/LSST) either detect the planet or "
        "kill the clustering signal with an unbiased sample?",
        "Can alternative dynamical explanations (self-gravitating disk, "
        "primordial black hole) be distinguished observationally?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Two mainstream readings coexist: a real distant planet versus "
            "survey-bias explanations of the clustering.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "No direct detection and no unbiased all-sky sample yet exists to "
            "decide between them.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "A real published dispute between dynamical-modelling and survey "
            "groups, not a split asserted by the AI.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — TRAPPIST-1 b is a bare rock                   🟠 Frontier          #
# --------------------------------------------------------------------------- #
trappist1b_bare_rock = Claim(
    id="trappist1b_bare_rock",
    title="TRAPPIST-1 b lacks a substantial atmosphere",
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Greene2023",
            url_or_id="arXiv:2303.14849",
            kind="peer-reviewed paper (Nature 618, 39-42, 2023)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "JWST measured the planet's dayside thermal emission at 15 "
                "microns; the high brightness temperature is consistent with "
                "re-radiation from a bare dayside and no detectable CO2 "
                "atmosphere."
            ),
            source_ref="Greene2023",
        ),
    ],
    open_questions=[
        "Single-band photometry cannot exclude every thin-atmosphere scenario.",
        "Whether the other TRAPPIST-1 planets, further out, retain atmospheres "
        "is still open.",
        "How M-dwarf activity strips or preserves secondary atmospheres is an "
        "active modelling front.",
    ],
    status_reason=[
        ConditionAssessment(
            "new_discovery", True,
            "JWST has only just made thermal emission from Earth-sized "
            "exoplanets measurable at all.",
        ),
        ConditionAssessment(
            "insufficient_sample", True,
            "Conclusions rest on a handful of eclipses of one planet in one "
            "band.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Follow-up JWST programmes on the TRAPPIST-1 system are producing "
            "papers at a fast clip.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3b — TRAPPIST-1's inner pair lack thick atmospheres  🟠 Frontier       #
# (Second claim through the T4 pipeline — first via the V4-4 stepwise path.
#  Human review corrected: evidence-2 type (MIRI secondary-eclipse thermal
#  emission is a direct observation, same technique as evidence 1 -> E1),
#  title de-overclaimed ("thick" added), venues confirmed: Greene 2023
#  Nature 618, 39; Zieba 2023 Nature 620, 746.)
# --------------------------------------------------------------------------- #
trappist1_inner_pair_airless = Claim(
    id="trappist1_inner_planets_airless",
    title="TRAPPIST-1's two innermost planets lack thick atmospheres",
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Greene2023b",
            url_or_id="arXiv:2303.14849",
            kind="peer-reviewed paper (Nature 618, 39-42, 2023; planet b)",
        ),
        Source(
            label="Zieba2023",
            url_or_id="arXiv:2306.10150",
            kind="peer-reviewed paper (Nature 620, 746-749, 2023; planet c)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "JWST/MIRI secondary-eclipse photometry of TRAPPIST-1 b at 15 "
                "microns detected the planet's dayside thermal emission at "
                "high confidence, consistent with little or no atmosphere "
                "redistributing heat and no detectable CO2 absorption."
            ),
            source_ref="Greene2023b",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The same technique applied to TRAPPIST-1 c measured a dayside "
                "brightness temperature of about 380 K — hot enough to "
                "disfavour a thick, CO2-rich atmosphere on that planet too."
            ),
            source_ref="Zieba2023",
        ),
    ],
    open_questions=[
        "Thin or exotic atmospheres are not fully excluded by single-band "
        "photometry.",
        "Whether the cooler outer planets (d through h) retain atmospheres is "
        "the system's open frontier.",
        "What do two airless inner rocky planets imply for volatile delivery "
        "and escape around active M dwarfs?",
    ],
    status_reason=[
        ConditionAssessment(
            "new_discovery", True,
            "Thermal-emission measurements of Earth-sized temperate-zone "
            "planets only became possible with JWST; these are the first two "
            "such results in this system.",
        ),
        ConditionAssessment(
            "insufficient_sample", True,
            "Each conclusion rests on a handful of eclipses in a single "
            "photometric band per planet.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "JWST programmes on TRAPPIST-1 continue to produce follow-up "
            "papers at a fast clip.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — a biosignature on K2-18 b                     🔴 Speculative       #
# --------------------------------------------------------------------------- #
k2_18b_biosignature = Claim(
    id="k2_18b_biosignature",
    title="K2-18 b's atmosphere carries a biosignature (DMS)",
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Madhusudhan2023",
            url_or_id="arXiv:2309.05566",
            kind="peer-reviewed paper (ApJL 956, L13, 2023)",
        ),
        Source(
            label="Wogan2024",
            url_or_id="arXiv:2401.11082",
            kind="peer-reviewed paper (ApJL 963, L7, 2024)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "JWST transmission spectroscopy detected methane and carbon "
                "dioxide in a hydrogen-rich atmosphere, with a tentative, low-"
                "significance hint of dimethyl sulfide — a proposed biomarker — "
                "that the authors themselves flag as requiring validation."
            ),
            source_ref="Madhusudhan2023",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Photochemical and climate modelling shows the same spectrum is "
                "matched by a lifeless gas-rich mini-Neptune with no habitable "
                "surface, needing no biosphere at all."
            ),
            source_ref="Wogan2024",
        ),
    ],
    open_questions=[
        "Can deeper JWST observations confirm or exclude DMS at meaningful "
        "significance?",
        "Is the planet a Hycean ocean world or a gas-rich mini-Neptune?",
        "Is DMS even a reliable biosignature, given proposed abiotic "
        "production routes?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "The DMS hint is low-significance, contested by re-analyses, and "
            "alternative lifeless models fit the data; the field treats the "
            "biosignature reading as unestablished.",
        ),
    ],
    status_history=[],
)


EXOPLANETS = Topic(
    id="exoplanets",
    title="Exoplanets",
    summary=(
        "Third domain through the identical engine — and this one re-exercises "
        "the arXiv cite=>fetch pipeline on fresh sources. The shape again: a 🟢 "
        "bedrock (they exist) under a 🔴 ceiling (a biosignature), with a real "
        "🟡 two-camp dispute (Planet Nine) in between."
    ),
    claims=[
        exoplanets_exist,
        proxima_b_exists,
        planets_are_common,
        planet_nine,
        trappist1b_bare_rock,
        trappist1_inner_pair_airless,
        k2_18b_biosignature,
    ],
)
