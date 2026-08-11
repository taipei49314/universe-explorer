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
    trace_refs=['Corliss1979', 'Spiess1980'],
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
# Claim 1b — the ocean absorbs most excess heat           🔵 Strong            #
# --------------------------------------------------------------------------- #
ocean_heat_uptake = Claim(
    id="ocean_heat_uptake",
    trace_refs=['vonSchuckmann2020'],
    title="The ocean absorbs the vast majority of anthropogenic excess heat",
    status=Status.STRONG,
    sources=[
        Source(
            label="vonSchuckmann2020",
            url_or_id="doi:10.5194/essd-12-2013-2020",
            kind="peer-reviewed paper (Earth Syst. Sci. Data 12, 2013-2041, "
                 "2020; multi-team synthesis)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "A synthesis of in-situ ocean temperature measurements (Argo "
                "floats and historical profiles) by more than thirty research "
                "groups finds that about 89% of the heat accumulated in the "
                "Earth system over 1971-2018 is stored in the ocean."
            ),
            source_ref="vonSchuckmann2020",
        ),
    ],
    open_questions=[
        "Coverage before the Argo era (pre-2005) is sparse, widening error "
        "bars on the earlier decades.",
        "The deep ocean below 2000 m is still poorly sampled.",
        "Closing the Earth energy imbalance budget across independent "
        "observing systems remains an active effort.",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Ocean-dominated heat uptake is the consistent result of Argo-era "
            "observations and successive international assessments.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Debate persists over the exact partitioning and pre-Argo "
            "magnitudes, not over the ocean's dominant role.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Independent observing systems (in-situ, satellite altimetry, "
            "top-of-atmosphere radiation) point the same way; new data refine "
            "the numbers without moving the direction.",
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

# --------------------------------------------------------------------------- #
# Claim 6 — ocean acidification                          🔵 Strong             #
# --------------------------------------------------------------------------- #
ocean_acidification_anthropogenic = Claim(
    id="ocean_acidification_anthropogenic",
    trace_refs=['Doney2009', 'IPCCAR6WGI'],
    title=(
        "Anthropogenic CO2 uptake is acidifying the surface ocean"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="Doney2009",
            url_or_id="doi:10.1146/annurev.marine.010908.163834",
            kind="peer-reviewed paper (Annu. Rev. Mar. Sci. 1, 169, 2009; "
                 "ocean acidification)",
        ),
        Source(
            label="IPCCAR6WGI",
            url_or_id="doi:10.1017/9781009157896",
            kind="peer-reviewed paper (IPCC AR6 WGI; ocean carbon and "
                 "acidification assessment)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Time series of surface ocean pH and carbonate chemistry show "
                "declining pH concurrent with rising atmospheric CO2."
            ),
            source_ref="Doney2009",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Global assessments attribute the multi-decadal acidification "
                "trend primarily to anthropogenic carbon uptake by the ocean."
            ),
            source_ref="IPCCAR6WGI",
        ),
    ],
    open_questions=[
        "How will regional upwelling and biology modulate coastal acidification "
        "extremes?",
        "What are organism- and ecosystem-level thresholds across taxa?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Anthropogenic ocean acidification is standard marine chemistry "
            "and IPCC assessment content.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Natural variability modulates the signal regionally; it does not "
            "replace the anthropogenic driver of the long-term trend.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Longer records and denser observing networks have strengthened "
            "the trend detection.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 7 — microplastics deep ocean                     🟠 Frontier           #
# --------------------------------------------------------------------------- #
microplastics_reach_deep_ocean = Claim(
    id="microplastics_reach_deep_ocean",
    title=(
        "Microplastic particles are widespread in the deep ocean and trenches"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Woodall2014",
            url_or_id="doi:10.1098/rsos.140317",
            kind="peer-reviewed paper (R. Soc. Open Sci. 1, 140317, 2014; "
                 "deep-sea microplastics)",
        ),
        Source(
            label="Peng2018",
            url_or_id="doi:10.7185/geochemlet.1829",
            kind="peer-reviewed paper (Geochem. Persp. Lett. 9, 1, 2018; "
                 "hadal microplastics)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Sediment cores and deep-sea samples contain microplastic "
                "fibres and fragments far below the sunlit surface ocean."
            ),
            source_ref="Woodall2014",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Hadal trench samples show plastic debris and microplastics "
                "in some of the deepest marine environments sampled."
            ),
            source_ref="Peng2018",
        ),
    ],
    open_questions=[
        "What fraction of surface plastic production reaches the abyss?",
        "How do deep-sea food webs interact with microplastic loads?",
    ],
    status_reason=[
        ConditionAssessment(
            "new_discovery", True,
            "Deep-ocean and hadal microplastic detections are a recent "
            "observational frontier.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Sampling papers across basins and trenches are accumulating "
            "quickly.",
        ),
        ConditionAssessment(
            "insufficient_sample", True,
            "Global deep coverage remains sparse relative to the ocean volume.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 8 — deep-sea mining impacts                      🟠 Frontier           #
# --------------------------------------------------------------------------- #
deep_sea_mining_impacts_uncertain = Claim(
    id="deep_sea_mining_impacts_uncertain",
    title=(
        "Commercial deep-sea mining would cause large, long-lived ecological "
        "impacts that cannot yet be fully quantified"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Miller2018",
            url_or_id="doi:10.3389/fmars.2017.00418",
            kind="peer-reviewed paper (Front. Mar. Sci.; deep-sea mining "
                 "impacts review)",
        ),
        Source(
            label="Niner2018",
            url_or_id="doi:10.3389/fmars.2018.00053",
            kind="peer-reviewed paper (Front. Mar. Sci. 5, 53, 2018; "
                 "deep-sea mining and no net loss of biodiversity; "
                 "corrigendum 10.3389/fmars.2018.00195)",
        ),
        Source(
            label="Niner2018corrigendum",
            url_or_id="doi:10.3389/fmars.2018.00195",
            kind="peer-reviewed corrigendum (Front. Mar. Sci. 2018; "
                 "publisher update to Niner2018; does not reverse the "
                 "no-net-loss impossibility claim)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Reviews of trial mining and analogous disturbances document "
                "sediment plumes, habitat removal and slow recovery of abyssal "
                "communities."
            ),
            source_ref="Miller2018",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Analyses of 'no net loss' biodiversity goals for deep-sea "
                "mining conclude that residual impacts cannot be fully "
                "offset with present knowledge and tools."
            ),
            source_ref="Niner2018",
        ),
    ],
    open_questions=[
        "What plume and noise footprints scale to commercial operations?",
        "Can protected-area designs offset nodule-field losses?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Mining-impact and baseline biodiversity papers are expanding "
            "ahead of possible commercial start.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No full commercial-scale mining time series exists to calibrate "
            "long-term recovery.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Policy and science still negotiate how large and lasting impacts "
            "will be under real operations.",
        ),
    ],
    status_history=[],
)


OCEAN = Topic(
    id="ocean",
    title="The deep ocean",
    summary=(
        "Earth-systems ocean container. 🟢 vents; 🔵 heat uptake + "
        "acidification; 🟡 AMOC; 🟠 CCZ biodiversity, microplastics, mining "
        "impacts; 🔴 dark oxygen (not accepted)."
    ),
    claims=[
        hydrothermal_vents_exist,
        ocean_heat_uptake,
        ocean_acidification_anthropogenic,
        amoc_weakening,
        ccz_biodiversity_unknown,
        microplastics_reach_deep_ocean,
        deep_sea_mining_impacts_uncertain,
        dark_oxygen_production,
    ],
)
