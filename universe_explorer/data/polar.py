"""Polar regions (Arctic + Antarctic) — Earth-systems domain.

Same schema and courts as every other topic. Lights belong to claims, not to
"the poles" as a container. Cross-domain adjacency to ocean (heat / AMOC) is
authored in relations.py as boundary edges.

Expected lights (domain shape SLA — all five cells present):
  ice_cores_record_paleoclimate     -> 🟢 Established
  arctic_sea_ice_multidecade_decline -> 🔵 Strong
  greenland_ice_sheet_losing_mass   -> 🔵 Strong
  antarctic_ice_sheet_losing_mass   -> 🟡 Competing
  marine_ice_sheet_instability      -> 🟠 Frontier
  permafrost_carbon_feedback        -> 🟠 Frontier
  antarctic_sea_ice_recent_lows     -> 🟠 Frontier
  arctic_ice_free_summer_imminent   -> 🔴 Speculative
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
# Claim 1 — ice cores record paleoclimate               🟢 Established         #
# --------------------------------------------------------------------------- #
ice_cores_record_paleoclimate = Claim(
    id="ice_cores_record_paleoclimate",
    title=(
        "Polar ice cores preserve a multi-proxy record of past climate and "
        "atmospheric composition"
    ),
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="Jouzel2007",
            url_or_id="doi:10.1126/science.1141038",
            kind="peer-reviewed paper (Science 317, 793-796, 2007; EPICA Dome C)",
        ),
        Source(
            label="Petit1999",
            url_or_id="doi:10.1038/20859",
            kind="peer-reviewed paper (Nature 399, 429-436, 1999; Vostok)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "EPICA Dome C ice-core isotopic and gas records reconstruct "
                "Antarctic climate and atmospheric CO2 over eight glacial "
                "cycles, measured in the ice itself."
            ),
            source_ref="Jouzel2007",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The Vostok ice core independently recovered a multi-cycle "
                "record of temperature proxies and greenhouse gases from a "
                "separate East Antarctic site."
            ),
            source_ref="Petit1999",
        ),
    ],
    open_questions=[
        "How far back can continuous Antarctic cores be pushed beyond ~800 ka?",
        "How best to reconcile bipolar seesaw timing between Greenland and "
        "Antarctic cores?",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Independent deep cores (Vostok, EPICA Dome C, and others) recover "
            "consistent glacial–interglacial patterns in isotopes and gases.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Ice-core paleoclimate is standard content in climate and "
            "Quaternary science textbooks.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream theory denies that polar ice preserves layered "
            "climate and gas records; debates concern interpretation details.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Subsequent cores and reanalyses have refined, not overturned, "
            "the ice-core archive.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — Arctic sea-ice multi-decade decline          🔵 Strong             #
# --------------------------------------------------------------------------- #
arctic_sea_ice_multidecade_decline = Claim(
    id="arctic_sea_ice_multidecade_decline",
    title=(
        "Arctic sea-ice extent has declined multi-decadally in the satellite era"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="Stroeve2012",
            url_or_id="doi:10.1007/s10584-011-0101-1",
            kind="peer-reviewed paper (Climatic Change 110, 1005-1027, 2012)",
        ),
        Source(
            label="IPCC-AR6-WGI-Ch9",
            url_or_id="doi:10.1017/9781009157896.011",
            kind="peer-reviewed assessment (IPCC AR6 WGI Chapter 9, 2021)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Satellite passive-microwave records show a multi-decade "
                "decline in Arctic sea-ice extent and volume indicators, with "
                "especially large late-summer losses."
            ),
            source_ref="Stroeve2012",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "IPCC AR6 assesses observed Arctic sea-ice decline as a robust "
                "feature of the recent climate, with human influence as a "
                "dominant driver of the multi-decade trend."
            ),
            source_ref="IPCC-AR6-WGI-Ch9",
        ),
    ],
    open_questions=[
        "How will seasonal ice-free thresholds be defined operationally "
        "(area vs duration vs region)?",
        "What is the relative role of ocean heat vs atmosphere in specific "
        "recent extreme years?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Satellite records and climate-assessment syntheses treat "
            "multi-decade Arctic sea-ice decline as established observational "
            "fact under mainstream climate science.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Minority discussions of natural variability and reanalysis "
            "details refine attribution and year-to-year noise; they do not "
            "displace the multi-decade decline itself.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "The long-term satellite-era direction is robust across products; "
            "new evidence revises rates and extremes more than the sign of "
            "the multi-decade trend.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — Greenland ice sheet mass loss                🔵 Strong             #
# --------------------------------------------------------------------------- #
greenland_ice_sheet_losing_mass = Claim(
    id="greenland_ice_sheet_losing_mass",
    title=(
        "The Greenland Ice Sheet has been losing mass in the satellite era"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="IMBIE2019",
            url_or_id="doi:10.1038/s41586-019-1855-2",
            kind="peer-reviewed paper (Nature 579, 233-239, 2020; IMBIE team)",
        ),
        Source(
            label="IPCC-AR6-WGI-Ch9b",
            url_or_id="doi:10.1017/9781009157896.011",
            kind="peer-reviewed assessment (IPCC AR6 WGI Chapter 9, 2021)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "IMBIE reconciles altimetry, gravimetry and input–output "
                "methods and reports sustained Greenland Ice Sheet mass loss "
                "over the satellite era."
            ),
            source_ref="IMBIE2019",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "IPCC AR6 assesses Greenland mass loss as a major contributor "
                "to observed sea-level rise, consistent with multi-method "
                "mass-budget studies."
            ),
            source_ref="IPCC-AR6-WGI-Ch9b",
        ),
    ],
    open_questions=[
        "How will surface melt vs dynamic discharge partition under higher "
        "warming pathways?",
        "What is the committed long-term sea-level contribution on century "
        "to millennial scales?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Multi-method mass-budget assessments (IMBIE and successors) and "
            "IPCC AR6 treat satellite-era Greenland mass loss as robust.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Method differences (altimetry vs GRACE vs input–output) produce "
            "spread in rates; they do not reverse the sign of multi-decade "
            "loss in mainstream syntheses.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "The direction of satellite-era mass loss is stable across "
            "independent techniques; debate focuses on acceleration timing "
            "and future partitioning.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — Antarctic ice sheet mass balance             🟡 Competing          #
# --------------------------------------------------------------------------- #
antarctic_ice_sheet_losing_mass = Claim(
    id="antarctic_ice_sheet_losing_mass",
    title=(
        "The Antarctic Ice Sheet as a whole is losing mass, or East Antarctic "
        "gains still offset West Antarctic losses"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="IMBIE2018",
            url_or_id="doi:10.1038/s41586-018-0179-y",
            kind="peer-reviewed paper (Nature 558, 219-222, 2018; IMBIE Antarctica)",
        ),
        Source(
            label="Shepherd2019",
            url_or_id="doi:10.1038/s41586-019-1855-2",
            kind="peer-reviewed paper (Nature 579, 233-239, 2020; IMBIE update)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "IMBIE Antarctica syntheses report net mass loss dominated by "
                "West Antarctica and the Antarctic Peninsula, with East "
                "Antarctic sectors showing smaller or regionally mixed signals."
            ),
            source_ref="IMBIE2018",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Updated multi-method reconciliations continue to refine the "
                "partition between sectors; the field still argues over how "
                "large East Antarctic accumulation offsets are relative to "
                "WAIS/Peninsula losses in particular intervals."
            ),
            source_ref="Shepherd2019",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Net Antarctic mass loss (WAIS/Peninsula-dominated)",
            supporting=(
                "Multi-mission IMBIE-style reconciliations find continent-scale "
                "net loss driven by West Antarctica and the Peninsula."
            ),
            opposing=(
                "East Antarctic accumulation and reanalysis choices can reduce "
                "or reverse inferred net loss in some time windows."
            ),
            limitations=(
                "Sector-level error bars remain large; method choice still "
                "moves the total."
            ),
        ),
        CompetingModel(
            name="East Antarctic gains can offset western losses (interval-dependent)",
            supporting=(
                "Some altimetry and input–output intervals show strong East "
                "Antarctic mass gain episodes."
            ),
            opposing=(
                "Later multi-method assessments emphasize that western dynamic "
                "losses dominate the multi-decade budget."
            ),
            limitations=(
                "Offsetting is time-window sensitive; not a claim of long-term "
                "stability under high warming."
            ),
        ),
    ],
    open_questions=[
        "What is the best multi-decade East Antarctic mass trend after "
        "reconciliation of snowfall reanalyses?",
        "How should sector-level uncertainties be communicated for sea-level "
        "projections?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Net-loss and interval-dependent offset narratives both appear in "
            "mainstream mass-budget literature, especially around East "
            "Antarctic accumulation.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "Method and reanalysis choices still move the continent-scale "
            "total enough that a single closed bookkeeping is contested for "
            "some periods.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "The split is a real mass-budget debate over partition and "
            "offsets, not an AI-invented controversy.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5 — marine ice-sheet instability                 🟠 Frontier           #
# --------------------------------------------------------------------------- #
marine_ice_sheet_instability = Claim(
    id="marine_ice_sheet_instability",
    title=(
        "Marine ice-sheet instability is already underway in key West "
        "Antarctic sectors (e.g. Thwaites)"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Joughin2014",
            url_or_id="doi:10.1126/science.1249055",
            kind="peer-reviewed paper (Science 344, 735-738, 2014)",
        ),
        Source(
            label="Rignot2014",
            url_or_id="doi:10.1002/2014GL060140",
            kind="peer-reviewed paper (Geophys. Res. Lett. 41, 3502-3509, 2014)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Ice-sheet model experiments forced by observed thinning and "
                "retreat argue that parts of the Amundsen Sea sector are "
                "already in unstable retreat configurations."
            ),
            source_ref="Joughin2014",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Satellite and airborne observations document rapid grounding-"
                "line retreat and dynamic thinning in Thwaites and neighboring "
                "glaciers."
            ),
            source_ref="Rignot2014",
        ),
    ],
    open_questions=[
        "Which sectors have already passed irreversible thresholds vs remain "
        "stabilizable by bed topography?",
        "How much can ice-shelf buttressing and melt variability slow or "
        "modulate MISI-like retreat?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Thwaites and Amundsen Sea sector papers form a fast-growing "
            "observational and modelling literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Whether MISI is already 'underway' as a continent-scale "
            "commitment remains contested even where rapid retreat is "
            "observed.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Longer time series and better bed/ocean constraints are still "
            "needed to close irreversible-threshold claims.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 6 — permafrost carbon feedback                   🟠 Frontier           #
# --------------------------------------------------------------------------- #
permafrost_carbon_feedback = Claim(
    id="permafrost_carbon_feedback",
    title=(
        "Thawing permafrost will release a large net greenhouse-gas feedback "
        "this century"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Schuur2015",
            url_or_id="doi:10.1038/nature14338",
            kind="peer-reviewed paper (Nature 520, 171-179, 2015)",
        ),
        Source(
            label="Natali2021",
            url_or_id="doi:10.1073/pnas.2100163118",
            kind="peer-reviewed paper (PNAS 118, e2100163118, 2021)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Reviews of the permafrost carbon pool and thaw processes "
                "argue for a substantial century-scale carbon–climate "
                "feedback, with large uncertainty in magnitude and timing."
            ),
            source_ref="Schuur2015",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Observational and modelling assessments of winter and "
                "shoulder-season respiration highlight under-accounted CO2 "
                "losses from northern permafrost regions."
            ),
            source_ref="Natali2021",
        ),
    ],
    open_questions=[
        "What is the net CO2 vs CH4 partition under different thaw pathways?",
        "How much of the pool is vulnerable on policy-relevant timescales "
        "vs multi-century commitment?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Permafrost carbon and winter flux papers are expanding quickly.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Sparse winter and interior-Arctic flux networks leave large "
            "regional gaps.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Magnitude, timing and greenhouse-gas mix of the feedback remain "
            "unsettled across models and observational upscaling.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 7 — Antarctic sea-ice recent lows                🟠 Frontier           #
# --------------------------------------------------------------------------- #
antarctic_sea_ice_recent_lows = Claim(
    id="antarctic_sea_ice_recent_lows",
    title=(
        "Recent Antarctic sea-ice lows mark a regime shift rather than "
        "interannual noise"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Parkinson2019",
            url_or_id="doi:10.1073/pnas.1906556116",
            kind="peer-reviewed paper (PNAS 116, 14414-14423, 2019)",
        ),
        Source(
            label="IPCC-AR6-WGI-Ch9c",
            url_or_id="doi:10.1017/9781009157896.011",
            kind="peer-reviewed assessment (IPCC AR6 WGI Chapter 9, 2021)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Satellite records document large year-to-year Antarctic "
                "sea-ice variability, including multi-year high and low "
                "episodes that differ in character from the Arctic's "
                "smoother multi-decade decline."
            ),
            source_ref="Parkinson2019",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Assessment literature treats Antarctic sea-ice trends as "
                "regionally complex and less linear than Arctic decline, with "
                "open questions about recent extremes vs long-term regime "
                "change."
            ),
            source_ref="IPCC-AR6-WGI-Ch9c",
        ),
    ],
    open_questions=[
        "Are post-2016 Antarctic sea-ice extremes a new baseline or a tail "
        "of natural variability?",
        "How do ocean heat, winds and ice-shelf freshwater fluxes combine in "
        "recent lows?",
    ],
    status_reason=[
        ConditionAssessment(
            "new_discovery", True,
            "Recent extreme Antarctic sea-ice lows are a new observational "
            "focus relative to the longer Arctic decline literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Whether recent lows constitute a lasting regime shift remains "
            "debated.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "The satellite era is still short relative to multi-decadal "
            "Southern Ocean modes.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 8 — near-term ice-free Arctic certainty          🔴 Speculative        #
# --------------------------------------------------------------------------- #
arctic_ice_free_summer_imminent = Claim(
    id="arctic_ice_free_summer_imminent",
    title=(
        "A reliably ice-free Arctic summer is effectively certain within a "
        "few years under present conditions"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="NotzStroeve2016",
            url_or_id="doi:10.1126/science.aag2345",
            kind="peer-reviewed paper (Science 354, 747-750, 2016)",
        ),
        Source(
            label="IPCC-AR6-WGI-Ch9d",
            url_or_id="doi:10.1017/9781009157896.011",
            kind="peer-reviewed assessment (IPCC AR6 WGI Chapter 9, 2021)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Process-based and observationally constrained analyses link "
                "cumulative CO2 to September Arctic sea-ice loss, supporting "
                "projections of ice-free summers under continued warming — "
                "with substantial timing uncertainty."
            ),
            source_ref="NotzStroeve2016",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Assessment literature projects ice-free Arctic summers as "
                "likely later this century under high emissions, but does not "
                "treat 'effectively certain within a few years' as a closed "
                "result."
            ),
            source_ref="IPCC-AR6-WGI-Ch9d",
        ),
    ],
    open_questions=[
        "Which definition of ice-free (threshold area, duration) is policy-"
        "relevant?",
        "How much internal variability can still delay or advance the first "
        "ice-free September?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "Mainstream assessments project ice-free Arctic summers under "
            "continued warming but reject overstated near-term certainty "
            "as a settled forecast.",
        ),
        ConditionAssessment(
            "philosophical_inference", True,
            "Collapsing multi-decadal projection envelopes into 'effectively "
            "certain within a few years' is an over-reading beyond the "
            "recorded evidence grade.",
        ),
    ],
    status_history=[],
)


POLAR = Topic(
    id="polar",
    title="Polar regions",
    summary=(
        "Arctic and Antarctic container — no topic light. 🟢 ice-core archive; "
        "🔵 Arctic sea ice + Greenland mass loss; 🟡 Antarctic mass-budget "
        "partition; 🟠 MISI/Thwaites, permafrost carbon, Antarctic sea-ice "
        "extremes; 🔴 overstated near-term ice-free certainty."
    ),
    claims=[
        ice_cores_record_paleoclimate,
        arctic_sea_ice_multidecade_decline,
        greenland_ice_sheet_losing_mass,
        antarctic_ice_sheet_losing_mass,
        marine_ice_sheet_instability,
        permafrost_carbon_feedback,
        antarctic_sea_ice_recent_lows,
        arctic_ice_free_summer_imminent,
    ],
)
