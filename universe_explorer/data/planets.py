"""Planets — solar-system and formation domain (complements exoplanets).

Theme 「星球」: bodies in our system and how planets form, without replacing
the exoplanets topic (other stars). Same schema and courts.

Expected lights:
  solar_system_age                 -> 🟢 Established
  moon_giant_impact                -> 🔵 Strong
  late_heavy_bombardment           -> 🟡 Competing
  ocean_worlds_icy_moons           -> 🟠 Frontier
  mars_sustained_surface_habitability_now -> 🔴 Speculative
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
# Claim 1 — solar system age                             🟢 Established        #
# --------------------------------------------------------------------------- #
solar_system_age = Claim(
    id="solar_system_age",
    title=(
        "The solar system formed about 4.56 billion years ago from a "
        "collapsing molecular cloud"
    ),
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="Amelin2002",
            url_or_id="doi:10.1126/science.1073950",
            kind="peer-reviewed paper (Science 297, 1678, 2002; CAI ages)",
        ),
        Source(
            label="Connelly2012",
            url_or_id="doi:10.1126/science.1226919",
            kind="peer-reviewed paper (Science 338, 651, 2012; Pb-Pb "
                 "chronology)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Lead-isotope ages of calcium–aluminium-rich inclusions "
                "(CAIs) in meteorites date the oldest solar-system solids "
                "to approximately 4.567 Ga."
            ),
            source_ref="Amelin2002",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Refined Pb–Pb chronometry of CAIs and chondrules confirms "
                "a brief formation interval for the earliest solids, "
                "anchoring solar-system age in radiometric data."
            ),
            source_ref="Connelly2012",
        ),
    ],
    open_questions=[
        "How quickly did giant planets grow after CAI formation?",
        "What was the birth environment (cluster vs isolated cloud)?",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Multiple laboratories and isotopic systems date early "
            "solar-system materials to ~4.56 Ga.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "A ~4.5–4.6 Ga solar-system age is standard in planetary science.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream chronology displaces CAI-based ages for system "
            "formation.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Refinements sharpen absolute ages without overturning the Ga "
            "scale.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — Moon giant impact                            🔵 Strong             #
# --------------------------------------------------------------------------- #
moon_giant_impact = Claim(
    id="moon_giant_impact",
    title=(
        "The Moon formed from a giant impact of a Mars-sized body with the "
        "early Earth"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="CanupAsphaug2001",
            url_or_id="doi:10.1038/35089010",
            kind="peer-reviewed paper (Nature 412, 708, 2001)",
        ),
        Source(
            label="Canup2012",
            url_or_id="doi:10.1126/science.1226073",
            kind="peer-reviewed paper (Science 338, 1052, 2012; "
                 "isotopic issues / variants)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Hydrodynamic simulations show that a giant impact can place "
                "iron-depleted, silicate-rich material into Earth orbit, "
                "matching the Moon's low iron core fraction and orbital "
                "angular momentum."
            ),
            source_ref="CanupAsphaug2001",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Earth–Moon isotopic similarities and dynamical constraints "
                "motivate impact variants (including high-angular-momentum "
                "scenarios) while keeping giant impact as the leading "
                "formation framework."
            ),
            source_ref="Canup2012",
        ),
    ],
    open_questions=[
        "Which impact geometry best matches isotopic near-identity of Earth "
        "and Moon?",
        "What was the fate of the impactor's core?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Giant impact is the standard lunar-origin model in planetary "
            "science.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Capture and co-formation variants exist but are minority "
            "relative to impact.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Debate refines impact parameters and isotopic mixing, not the "
            "broad impact framework.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — late heavy bombardment                       🟡 Competing          #
# --------------------------------------------------------------------------- #
late_heavy_bombardment = Claim(
    id="late_heavy_bombardment",
    title=(
        "A brief cataclysmic late heavy bombardment spiked impact rates "
        "across the inner solar system ~3.9 Ga ago"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Tera1974",
            url_or_id="doi:10.1016/0012-821x(74)90059-4",
            kind="peer-reviewed paper (Earth Planet. Sci. Lett. 22, 1, 1974; "
                 "lunar cataclysm hypothesis)",
        ),
        Source(
            label="BoehnkeHarrison2016",
            url_or_id="doi:10.1073/pnas.1611535113",
            kind="peer-reviewed paper (PNAS 113, 10802, 2016; challenges "
                 "to the cataclysm)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Clustering of lunar impact-melt ages near ~3.9 Ga was "
                "interpreted as a solar-system-wide cataclysm — the classic "
                "late heavy bombardment."
            ),
            source_ref="Tera1974",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Reanalyses argue that sampling bias and reset ages can "
                "produce an apparent age spike without a true system-wide "
                "cataclysm, favouring a smoother decline in bombardment."
            ),
            source_ref="BoehnkeHarrison2016",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Cataclysmic late heavy bombardment",
            supporting=(
                "Lunar melt-rock age clusters and basin chronology have long "
                "been read as a spike in impacts near 3.9 Ga."
            ),
            opposing=(
                "Sample collections may over-represent a few events; "
                "dynamical triggers remain debated."
            ),
            limitations=(
                "Apollo sampling is geographically limited."
            ),
        ),
        CompetingModel(
            name="Declining bombardment without a sharp cataclysm",
            supporting=(
                "Statistical reassessments of age data allow continuous "
                "decline; some dynamical models do not require a late spike."
            ),
            opposing=(
                "Some basin and meteorite records still prefer a late "
                "uptick in certain reconstructions."
            ),
            limitations=(
                "Absolute calibration of early impact flux remains uncertain."
            ),
        ),
    ],
    open_questions=[
        "Can Artemis-era samples break the sampling-bias degeneracy?",
        "Do asteroid-belt and terrestrial records require the same flux "
        "history as the Moon?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Cataclysm and continuous-decline readings are both actively "
            "published in planetary chronology.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "Limited lunar sampling prevents a unique flux history.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Decades of published debate document a real split.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — ocean worlds                                 🟠 Frontier           #
# --------------------------------------------------------------------------- #
ocean_worlds_icy_moons = Claim(
    id="ocean_worlds_icy_moons",
    title=(
        "Several icy moons host subsurface liquid-water oceans today"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Kivelson2000",
            url_or_id="doi:10.1126/science.289.5483.1340",
            kind="peer-reviewed paper (Science 289, 1340, 2000; Europa "
                 "induced field)",
        ),
        Source(
            label="Thomas2016",
            url_or_id="doi:10.1016/j.icarus.2015.08.037",
            kind="peer-reviewed paper (Icarus 264, 37, 2016; Enceladus "
                 "libration / ocean)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Galileo magnetometer data at Europa show an induced magnetic "
                "field consistent with a global conducting layer, interpreted "
                "as a saline subsurface ocean."
            ),
            source_ref="Kivelson2000",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Cassini measurements of Enceladus's physical libration "
                "require a decoupled ice shell over a global liquid layer, "
                "supporting a subsurface ocean feeding the south-polar plume."
            ),
            source_ref="Thomas2016",
        ),
    ],
    open_questions=[
        "Which moons have oceans that contact rock long enough for "
        "interesting chemistry?",
        "Can future missions detect unambiguous biosignatures in plumes "
        "or ice?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Europa Clipper, JUICE and Enceladus mission studies drive a "
            "fast-growing ocean-world literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Strong cases exist for several moons, but ocean properties and "
            "the full inventory remain under active refinement.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No in-situ sampling of a confirmed subsurface ocean has been "
            "returned; evidence is geophysical and remote.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5 — Mars habitable now                           🔴 Speculative        #
# --------------------------------------------------------------------------- #
mars_sustained_surface_habitability_now = Claim(
    id="mars_sustained_surface_habitability_now",
    title=(
        "Mars presently sustains surface conditions suitable for widespread "
        "Earth-like life"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Wordsworth2016",
            url_or_id="arXiv:1606.02813",
            kind="peer-reviewed paper (ARA&A 54, 2016; climate of early Mars)",
        ),
        Source(
            label="Grotzinger2014",
            url_or_id="doi:10.1126/science.1242777",
            kind="peer-reviewed paper (Science 343, 1242777, 2014; Gale "
                 "crater habitability *past*)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Climate and atmospheric studies emphasise that present-day "
                "Mars is cold, thin-atmosphered, and oxidising at the "
                "surface — a harsh environment for widespread Earth-like "
                "surface life, even while early Mars may have been wetter."
            ),
            source_ref="Wordsworth2016",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Curiosity's results at Gale crater support past aqueous "
                "environments that could have been habitable — evidence about "
                "ancient Mars, not a demonstration of present global surface "
                "habitability."
            ),
            source_ref="Grotzinger2014",
        ),
    ],
    open_questions=[
        "Do protected subsurface niches host life today?",
        "How should past habitability be separated from present biosignature "
        "searches in mission design?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "Planetary science does not accept present-day Mars as widely "
            "surface-habitable in the Earth-like sense; interest focuses on "
            "past habitability and subsurface niches.",
        ),
        ConditionAssessment(
            "no_observational_evidence", True,
            "No confirmed evidence supports widespread present surface "
            "habitability; recorded evidence points to past environments "
            "and a harsh present surface.",
        ),
    ],
    status_history=[],
)


PLANETS = Topic(
    id="planets",
    title="Planets",
    summary=(
        "Planet-scale container (theme: 星球) for the solar system and "
        "formation — complements exoplanets (other stars). Shape: 🟢 age "
        "bedrock; 🔵 Moon giant impact; 🟡 late heavy bombardment; 🟠 ocean "
        "worlds; 🔴 present Mars surface habitability (not accepted)."
    ),
    claims=[
        solar_system_age,
        moon_giant_impact,
        late_heavy_bombardment,
        ocean_worlds_icy_moons,
        mars_sustained_surface_habitability_now,
    ],
)
