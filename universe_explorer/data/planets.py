"""Planets — solar-system and formation domain (complements exoplanets).

Theme 「星球」: bodies in our system and how planets form, without replacing
the exoplanets topic (other stars). Same schema and courts.

Ocean-worlds cluster (deepened):
  ocean_worlds_icy_moons              🟠 umbrella inventory
  europa_induced_field_ocean          🟠 Europa conducting layer
  enceladus_plume_global_ocean        🟠 plume + libration
  titan_subsurface_ocean              🟠 Titan interior ocean
  enceladus_plume_organics            🟠 complex organics in plume
  ocean_world_life_today              🔴 Speculative present biosphere claim

Other:
  solar_system_age 🟢 · moon_giant_impact 🔵 · late_heavy_bombardment 🟡
  mars_sustained_surface_habitability_now 🔴
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
# Claim 4a — Europa induced-field ocean                  🟠 Frontier           #
# --------------------------------------------------------------------------- #
europa_induced_field_ocean = Claim(
    id="europa_induced_field_ocean",
    title=(
        "Europa hosts a global subsurface saline ocean inferred from "
        "induced magnetic fields"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Kivelson2000b",
            url_or_id="doi:10.1126/science.289.5483.1340",
            kind="peer-reviewed paper (Science 289, 1340, 2000)",
        ),
        Source(
            label="Khurana1998",
            url_or_id="doi:10.1038/27394",
            kind="peer-reviewed paper (Nature 395, 777, 1998; induced "
                 "fields as ocean evidence)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Galileo magnetometer measurements show time-varying induced "
                "fields at Europa consistent with a global conducting shell, "
                "interpreted as a saline liquid-water ocean beneath the ice."
            ),
            source_ref="Kivelson2000b",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Earlier Galileo flybys already indicated an inductive "
                "response requiring a near-surface conducting layer on "
                "Europa-scale geometry."
            ),
            source_ref="Khurana1998",
        ),
    ],
    open_questions=[
        "What are the ocean's salinity, thickness and ice-shell thickness?",
        "Does the ocean contact rock, enabling hydrothermal chemistry?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Europa Clipper and JUICE drive continuous geophysical and "
            "astrophysical follow-up literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "A subsurface ocean is the leading interpretation; detailed "
            "properties remain model-dependent.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No in-situ ocean sample; evidence is magnetic and remote-sensing.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4b — Enceladus plume + global ocean              🟠 Frontier           #
# --------------------------------------------------------------------------- #
enceladus_plume_global_ocean = Claim(
    id="enceladus_plume_global_ocean",
    title=(
        "Enceladus vents water-rich plumes from a global subsurface ocean"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Porco2006",
            url_or_id="doi:10.1126/science.1123013",
            kind="peer-reviewed paper (Science 311, 1393, 2006; plume "
                 "discovery)",
        ),
        Source(
            label="Thomas2016b",
            url_or_id="doi:10.1016/j.icarus.2015.08.037",
            kind="peer-reviewed paper (Icarus 264, 37, 2016; libration)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Cassini imaged and sampled water-rich jets erupting from "
                "Enceladus's south-polar terrain, establishing active "
                "venting to space."
            ),
            source_ref="Porco2006",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Measured physical libration requires a decoupled ice shell "
                "over a global liquid layer, linking the plume source region "
                "to a moon-wide ocean rather than only a local sea."
            ),
            source_ref="Thomas2016b",
        ),
    ],
    open_questions=[
        "How continuous is ocean–rock interaction under the south pole?",
        "What fraction of plume material is fresh ocean spray versus ice "
        "regolith?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Cassini legacy analyses and Enceladus mission concepts sustain "
            "a large literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Global ocean plus plume is the leading picture; detailed "
            "plumbing remains debated.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No landed or returned ocean sample; plume chemistry is the "
            "proxy.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4c — Titan subsurface ocean                      🟠 Frontier           #
# --------------------------------------------------------------------------- #
titan_subsurface_ocean = Claim(
    id="titan_subsurface_ocean",
    title=(
        "Titan harbours a deep subsurface water ocean beneath its ice shell"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Iess2012",
            url_or_id="doi:10.1126/science.1219631",
            kind="peer-reviewed paper (Science 337, 457, 2012; Titan "
                 "gravity / interior)",
        ),
        Source(
            label="Durante2019",
            url_or_id="doi:10.1016/j.icarus.2019.03.003",
            kind="peer-reviewed paper (Icarus 326, 123, 2019; Titan "
                 "gravity field after Cassini)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Cassini gravity measurements of Titan's tidal response "
                "imply a decoupled shell over a high-density fluid layer, "
                "interpreted as a subsurface water ocean."
            ),
            source_ref="Iess2012",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Post-Cassini gravity-field solutions refine Titan's "
                "interior structure and remain consistent with a deep "
                "global ocean under the ice shell."
            ),
            source_ref="Durante2019",
        ),
    ],
    open_questions=[
        "What is the ocean's depth, salinity and contact with silicates?",
        "How do surface organics couple to any deep aqueous chemistry?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Dragonfly-era Titan science keeps interior-ocean models active.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "A subsurface ocean is widely favoured; thickness and composition "
            "remain uncertain.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Inference is geophysical; no direct ocean access.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4d — Enceladus plume organics                    🟠 Frontier           #
# --------------------------------------------------------------------------- #
enceladus_plume_organics = Claim(
    id="enceladus_plume_organics",
    title=(
        "Enceladus's plume contains complex organic molecules sourced from "
        "an interior water environment"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Postberg2018",
            url_or_id="doi:10.1038/s41586-018-0246-4",
            kind="peer-reviewed paper (Nature 558, 564, 2018; macromolecular "
                 "organics)",
        ),
        Source(
            label="Porco2006b",
            url_or_id="doi:10.1126/science.1123013",
            kind="peer-reviewed paper (Science 311, 1393, 2006)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Cassini Cosmic Dust Analyzer mass spectra of ice grains in "
                "the Enceladus plume show macromolecular organic material "
                "consistent with a complex organic reservoir in contact with "
                "liquid water."
            ),
            source_ref="Postberg2018",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The plume itself is an observed, ongoing ejection of "
                "water-rich material from the south-polar fractures, "
                "providing the sampled grains."
            ),
            source_ref="Porco2006b",
        ),
    ],
    open_questions=[
        "Are the organics hydrothermal, primordial, or both?",
        "Do they include unambiguous biosignatures, or only abiotic "
        "complexity?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Plume chemistry papers remain a high-output Enceladus topic.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Complex organics are reported; biological interpretation is "
            "not established.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Grain spectra are not a returned ocean sample; pathways remain "
            "model-dependent.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4e — life in ocean worlds today                  🔴 Speculative        #
# --------------------------------------------------------------------------- #
ocean_world_life_today = Claim(
    id="ocean_world_life_today",
    title=(
        "Extant life is present today in at least one icy-moon subsurface "
        "ocean"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Postberg2018b",
            url_or_id="doi:10.1038/s41586-018-0246-4",
            kind="peer-reviewed paper (Nature 558, 564, 2018; organics — "
                 "not a life detection)",
        ),
        Source(
            label="Kivelson2000c",
            url_or_id="doi:10.1126/science.289.5483.1340",
            kind="peer-reviewed paper (Science 289, 1340, 2000; ocean "
                 "inference)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Complex organics in Enceladus plume grains demonstrate "
                "interesting chemistry in an ocean-world environment but "
                "do not constitute a detection of living organisms."
            ),
            source_ref="Postberg2018b",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Geophysical evidence for subsurface oceans establishes "
                "habitability *potential*, not the presence of life."
            ),
            source_ref="Kivelson2000c",
        ),
    ],
    open_questions=[
        "What measurement would count as a decisive biosignature in a plume "
        "or ice shell?",
        "How should abiotic organic complexity be ruled out?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "No icy-moon extant-life detection is accepted by the field; "
            "organics and oceans motivate searches only.",
        ),
        ConditionAssessment(
            "no_observational_evidence", True,
            "Recorded evidence supports oceans and organics, not organisms.",
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
        "Planet-scale container (theme: 星球). 🟢 age; 🔵 Moon impact; "
        "🟡 late heavy bombardment; 🟠 ocean-worlds cluster (umbrella, "
        "Europa, Enceladus, Titan, plume organics); 🔴 extant ocean life "
        "and present Mars surface habitability (not accepted)."
    ),
    claims=[
        solar_system_age,
        moon_giant_impact,
        late_heavy_bombardment,
        ocean_worlds_icy_moons,
        europa_induced_field_ocean,
        enceladus_plume_global_ocean,
        titan_subsurface_ocean,
        enceladus_plume_organics,
        ocean_world_life_today,
        mars_sustained_surface_habitability_now,
    ],
)
