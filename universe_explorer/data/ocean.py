"""Ocean — the P4 cross-domain topic (spec docs/p4-spec.md).

The whole point of this file is what it does NOT touch: it is filled with the
exact same schema, taxonomy and controlled evidence vocabulary as black_hole.py,
and it flows through the identical engine (model / validator / axes / provenance
/ proposals / watch) with zero engine edits. Swap the Data layer, keep the mind.

Every source below was verified online before being written (title, journal,
year, DOI) — none from memory. Non-arXiv sources are honestly exempt from the P1
fetch rule (no machine-fetchable endpoint), same rule as the print/textbook
sources in the black-hole topic.

Expected lights:
  hydrothermal_vents_exist  -> 🟢 Established  (E1: two independent Alvin/RISE discoveries)
  amoc_weakening            -> 🟡 Competing    (first real competing_models — retires R4)
  ccz_biodiversity_unknown  -> 🟠 Frontier
  dark_oxygen_production    -> 🔴 Speculative   (reverse combo: single direct obs × low consensus)
"""

from __future__ import annotations

from ..model import (
    Claim,
    CompetingModel,
    ConditionAssessment,
    Evidence,
    Source,
    Status,
    StatusChange,
    Topic,
)

# --------------------------------------------------------------------------- #
# Claim 1 — hydrothermal vent ecosystems exist          🟢 Established         #
# --------------------------------------------------------------------------- #
hydrothermal_vents_exist = Claim(
    id="hydrothermal_vents_exist",
    title="Chemosynthetic hydrothermal vent ecosystems exist on the deep seafloor",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="Corliss1979",
            url_or_id="doi:10.1126/science.203.4385.1073",
            kind="peer-reviewed paper (Science 203, 1073-1083, 1979)",
        ),
        Source(
            label="Spiess1980",
            url_or_id="doi:10.1126/science.207.4438.1421",
            kind="peer-reviewed paper (Science 207, 1421-1433, 1980)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "The submersible Alvin directly observed warm-water vents on the "
                "Galápagos Rift surrounded by dense animal communities living off "
                "chemosynthesis by sulfur-oxidising bacteria rather than sunlight."
            ),
            source_ref="Corliss1979",
        ),
        Evidence(
            type="direct observation",
            description=(
                "An independent expedition (RISE) found high-temperature black-"
                "smoker vents at 21°N on the East Pacific Rise, with tube worms, "
                "clams and crabs like those at the Galápagos site — a second, "
                "separate confirmation."
            ),
            source_ref="Spiess1980",
        ),
    ],
    open_questions=[
        "The full extent and connectivity of vent fields along the global "
        "mid-ocean ridge system is still being mapped.",
        "How vent larvae disperse between isolated, ephemeral fields remains "
        "only partly understood.",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Two independent submersible expeditions (Alvin/Galápagos 1979, "
            "RISE/East Pacific Rise 1980) directly observed vent ecosystems; "
            "hundreds of fields have since been catalogued globally.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Chemosynthetic vent ecosystems are standard content in oceanography "
            "and marine-biology textbooks.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream theory disputes their existence; only details of "
            "distribution and ecology are debated.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Four decades of subsequent dives and global vent databases have "
            "only reinforced the finding.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — AMOC is weakening                            🟡 Competing          #
# --------------------------------------------------------------------------- #
amoc_weakening = Claim(
    id="amoc_weakening",
    title="The Atlantic Meridional Overturning Circulation is weakening",
    status=Status.COMPETING,
    sources=[
        Source(
            label="Caesar2018",
            url_or_id="doi:10.1038/s41586-018-0006-5",
            kind="peer-reviewed paper (Nature 556, 191-196, 2018)",
        ),
        Source(
            label="Worthington2021",
            url_or_id="doi:10.5194/os-17-285-2021",
            kind="peer-reviewed paper (Ocean Science 17, 285-299, 2021)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "A sea-surface-temperature 'fingerprint' (subpolar cooling, Gulf "
                "Stream warming) is read as evidence of an AMOC weakening of "
                "roughly 3 sverdrups (about 15%) since the mid-20th century."
            ),
            source_ref="Caesar2018",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "A 30-year reconstruction of AMOC strength finds no significant "
                "decline over its period, arguing the direct record is too short "
                "to establish an anthropogenic trend."
            ),
            source_ref="Worthington2021",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Long-term weakening (proxy-based)",
            supporting=(
                "SST fingerprints and paleo/proxy reconstructions indicate the "
                "AMOC is now near its weakest in centuries."
            ),
            opposing=(
                "Proxies are indirect; the direct measurement record is only ~2 "
                "decades long and does not by itself show a robust trend."
            ),
            limitations=(
                "Relies on converting temperature patterns into circulation "
                "strength, an inference with its own uncertainties."
            ),
        ),
        CompetingModel(
            name="No robust observed decline yet",
            supporting=(
                "Observation-based reconstructions over 1981-2016 show no "
                "significant AMOC decline."
            ),
            opposing=(
                "A record this short may simply be unable to resolve a slow "
                "forced trend against strong year-to-year variability."
            ),
            limitations=(
                "Cannot rule out a weakening that is real but not yet "
                "statistically detectable in the direct record."
            ),
        ),
    ],
    open_questions=[
        "Does the disagreement reflect a real physical dispute or mainly the "
        "different time periods and methods the two camps compare?",
        "How long must the direct (post-2004) observing array run before a "
        "forced trend can be separated from natural variability?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Two mainstream readings coexist: proxy-based long-term weakening "
            "versus observation-based reconstructions showing no robust decline.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "The direct observing array is too short to settle the trend, so "
            "neither camp has decisive evidence.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "A real, published disagreement between physical-oceanography groups, "
            "not a split asserted by the AI.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — most CCZ biodiversity is undescribed         🟠 Frontier          #
# --------------------------------------------------------------------------- #
ccz_biodiversity_unknown = Claim(
    id="ccz_biodiversity_unknown",
    title="Most animal biodiversity in the Clarion-Clipperton Zone is undescribed",
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Rabone2023",
            url_or_id="doi:10.1016/j.cub.2023.04.052",
            kind="peer-reviewed paper (Current Biology 33, 2383-2396, 2023)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "The first synthesis checklist of CCZ metazoan fauna records "
                "around 5,000 species, an estimated 88-92% of them new to "
                "science, based on collated specimen sampling across the region."
            ),
            source_ref="Rabone2023",
        ),
    ],
    open_questions=[
        "The true total species richness of the CCZ (estimates range widely) is "
        "not yet known.",
        "Vast areas of the zone have never been sampled at all.",
        "How quickly formal taxonomic description can keep pace with sampling "
        "before potential mining disturbance is unclear.",
    ],
    status_reason=[
        ConditionAssessment(
            "insufficient_sample", True,
            "Only a small, uneven fraction of the CCZ has been biologically "
            "sampled; the great majority of recorded species are unnamed.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Taxonomic outputs and databases for the region have grown quickly "
            "over the last decade, enabling this first synthesis.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — 'dark oxygen' production at the seafloor      🔴 Speculative       #
# --------------------------------------------------------------------------- #
dark_oxygen_production = Claim(
    id="dark_oxygen_production",
    title="Polymetallic nodules produce 'dark oxygen' on the abyssal seafloor",
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Sweetman2024",
            url_or_id="doi:10.1038/s41561-024-01480-8",
            kind="peer-reviewed paper (Nature Geoscience 17, 737-739, 2024)",
        ),
        Source(
            label="FrontiersCritique2025",
            url_or_id="doi:10.3389/fmars.2025.1721853",
            kind="peer-reviewed critique (Frontiers in Marine Science, 2025)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "In-situ benthic-chamber experiments on nodule-covered abyssal "
                "seafloor recorded oxygen rising over ~2 days, interpreted as "
                "oxygen production in the dark (proposed seawater electrolysis)."
            ),
            source_ref="Sweetman2024",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "A peer-reviewed critique argues the measurements are consistent "
                "with instrumental artefacts and that recorded voltages are too "
                "low to split water; several original authors have since walked "
                "back key claims and the journal added an editorial note."
            ),
            source_ref="FrontiersCritique2025",
        ),
    ],
    open_questions=[
        "Can the oxygen increase be independently reproduced with methods that "
        "rule out chamber and sensor artefacts?",
        "If real, what mechanism produces it, and does it occur at meaningful "
        "scale across the abyssal plains?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "Despite a single peer-reviewed observation, the claim is not "
            "accepted: multiple rebuttals, author walk-backs and an editorial "
            "note leave it contested rather than established.",
        ),
    ],
    status_history=[],
)


OCEAN = Topic(
    id="ocean",
    title="The deep ocean",
    summary=(
        "A second Data layer running through the identical engine — proof the "
        "epistemology is domain-agnostic. Same shape to read: a 🟢 bedrock "
        "(vents exist) under a 🔴 ceiling (dark oxygen), with a genuine 🟡 "
        "two-camp dispute (AMOC) in between."
    ),
    claims=[
        hydrothermal_vents_exist,
        amoc_weakening,
        ccz_biodiversity_unknown,
        dark_oxygen_production,
    ],
)
