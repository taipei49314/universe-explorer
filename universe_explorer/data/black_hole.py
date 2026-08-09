"""Black hole — cosmos theme (v0 seed, deepened).

Every field is hand-filled with real content and a real source. Where a source
is genuinely near-absent (hawking_radiation: strong theory, almost no direct
observation) the split is recorded honestly. Rather under-fill than invent.

Deepened map:
  🟢 event_horizon_exists
  🔵 hawking_radiation
  🔵 kerr_describes_astrophysical_bh
  🔵 smbh_common_in_galaxy_nuclei
  🟡 lower_mass_gap_compact_objects
  🟠 bbh_mergers_catalogued
  🟠 jets_extract_bh_spin
  🟠 information_paradox
  🔴 firewall
  🔴 horizonless_gw_echoes
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
# Claim 1 — the event horizon exists                     🟢 Established        #
# --------------------------------------------------------------------------- #
event_horizon_exists = Claim(
    id="event_horizon_exists",
    title="Astrophysical black holes with an event horizon exist",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="EHT2019-M87-I",
            url_or_id="arXiv:1906.11238",
            kind="collaboration result (peer-reviewed, ApJL 875 L1)",
        ),
        Source(
            label="EHT2022-SgrA-I",
            url_or_id="arXiv:2311.08680",
            kind="collaboration result (peer-reviewed, ApJL 930 L12)",
        ),
        Source(
            label="LIGO2016-GW150914",
            url_or_id="arXiv:1602.03837",
            kind="collaboration result (peer-reviewed, PRL 116 061102)",
        ),
        Source(
            label="Nobel2020",
            url_or_id="nobelprize.org/prizes/physics/2020",
            kind="prize citation (Genzel & Ghez, stellar orbits at Sgr A*)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "The Event Horizon Telescope resolved a ring of emission around "
                "M87* whose size matches the shadow of a ~6.5-billion-solar-mass "
                "black hole predicted by general relativity."
            ),
            source_ref="EHT2019-M87-I",
        ),
        Evidence(
            type="direct observation",
            description=(
                "A second, independent EHT target, Sgr A* at the centre of the "
                "Milky Way, shows a shadow consistent with a ~4-million-solar-mass "
                "black hole."
            ),
            source_ref="EHT2022-SgrA-I",
        ),
        Evidence(
            type="direct observation",
            description=(
                "LIGO detected gravitational waves from the merger of two compact "
                "objects; the ringdown waveform matches a Kerr black hole and rules "
                "out neutron-star or classical alternatives at that mass."
            ),
            source_ref="LIGO2016-GW150914",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Decades of tracking individual stellar orbits around Sgr A* pin a "
                "dark, compact mass into a volume no ordinary matter distribution "
                "can occupy — recognised by the 2020 Nobel Prize in Physics."
            ),
            source_ref="Nobel2020",
        ),
    ],
    open_questions=[
        "Whether the surface is a true general-relativistic horizon or an "
        "ultra-compact horizonless mimicker (e.g. a gravastar) is constrained "
        "but not logically closed by current resolution.",
        "The precise near-horizon plasma and magnetic-field structure feeding "
        "the observed emission is still being modelled.",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Three independent lines — horizon-scale imaging (EHT), "
            "gravitational waves (LIGO/Virgo) and stellar dynamics (Keck/VLT) — "
            "each confirm compact objects behaving as black holes.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Black holes are standard content in general-relativity and "
            "astrophysics textbooks.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream theory disputes their existence; horizonless "
            "mimickers are a minority research programme, not a rival consensus.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "No observation to date has refuted the black-hole interpretation; "
            "each new dataset has tightened it.",
        ),
    ],
    status_history=[
        StatusChange(
            date="2016-02-11",
            from_status="Strong Consensus",
            to_status="Established Consensus",
            trigger="First direct gravitational-wave detection (GW150914) added "
                    "a third independent confirmation line.",
        ),
    ],
)

# --------------------------------------------------------------------------- #
# Claim 2 — Hawking radiation                            🔵 Strong             #
# --------------------------------------------------------------------------- #
hawking_radiation = Claim(
    id="hawking_radiation",
    title="Black holes emit thermal Hawking radiation and slowly evaporate",
    status=Status.STRONG,
    sources=[
        Source(
            label="Hawking1975",
            url_or_id="Commun. Math. Phys. 43, 199 (1975)",
            kind="peer-reviewed paper (original derivation)",
        ),
        Source(
            label="Steinhauer2016",
            url_or_id="arXiv:1510.00621",
            kind="peer-reviewed paper (Nature Physics 12, 959; analog system)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical derivation",
            description=(
                "Applying quantum field theory to the curved spacetime of a black "
                "hole, Hawking derived a thermal flux at a temperature inversely "
                "proportional to the mass, implying gradual evaporation."
            ),
            source_ref="Hawking1975",
        ),
        Evidence(
            type="analog experiment",
            description=(
                "A sonic horizon in a Bose-Einstein condensate emitted correlated "
                "phonon pairs with a thermal spectrum — a laboratory analog of the "
                "effect, not the astrophysical process itself."
            ),
            source_ref="Steinhauer2016",
        ),
    ],
    open_questions=[
        "No direct astrophysical detection exists: for stellar-mass and larger "
        "black holes the predicted temperature is far below the cosmic "
        "microwave background, so they absorb more than they emit.",
        "Whether analog-gravity experiments faithfully reproduce the "
        "gravitational case, or only a mathematically similar phenomenon, is "
        "still debated.",
        "The end state of evaporation, where the semiclassical derivation breaks "
        "down, is unknown.",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "The derivation is a standard, widely taught result of quantum field "
            "theory in curved spacetime and is accepted across the field.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "A minority questions details (trans-Planckian problem, information "
            "content), but not the existence of the effect.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "The theoretical direction has been stable for five decades; new "
            "work refines the picture (e.g. greybody factors, end-state "
            "debates) without displacing it. Note: the gap between this strong "
            "consensus and the absence of direct observation is expressed "
            "structurally on the evidence axis (P1.5), no longer as a manual "
            "annotation here.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2b — binary mergers catalogued at scale           🟠 Frontier          #
#
# First claim inducted through the T4 drafting pipeline (drafts/
# bbh_mergers_are_common.json, 2026-07-10): local LLM drafted it, every court
# passed it mechanically, then a human verified faithfulness (venue confirmed
# Phys. Rev. X 13, 041039 (2023); evidence checked against the cached
# abstract; title rewritten from the paper name into a claim statement).
# --------------------------------------------------------------------------- #
bbh_mergers_catalogued = Claim(
    id="bbh_mergers_catalogued",
    title="Gravitational-wave astronomy has catalogued dozens of compact "
          "binary coalescences",
    status=Status.FRONTIER,
    sources=[
        Source(
            label="GWTC3-2023",
            url_or_id="arXiv:2111.03606",
            kind="collaboration result (peer-reviewed, Phys. Rev. X 13, "
                 "041039, 2023)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "The GWTC-3 catalog reports 35 compact-binary-coalescence "
                "candidates from the second half of the third observing run — "
                "including the first confident neutron-star–black-hole "
                "binaries — bringing the cumulative count of observed "
                "candidates to 90."
            ),
            source_ref="GWTC3-2023",
        ),
    ],
    open_questions=[
        "Can gravitational-wave data alone cleanly distinguish neutron stars "
        "from black holes among the lighter binary components?",
        "What do the observed merger populations imply about massive-star "
        "and binary evolution?",
        "How will the population statistics shift as detector sensitivity "
        "improves and further observing runs accumulate?",
    ],
    status_reason=[
        ConditionAssessment(
            "new_discovery", True,
            "Gravitational-wave astronomy is a newly opened observational "
            "channel; population-scale catalogues of mergers only began with "
            "the third observing run.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Each observing run multiplies the catalogue and produces a fast-"
            "growing body of population-analysis papers.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — the information paradox                      🟠 Frontier           #
# --------------------------------------------------------------------------- #
information_paradox = Claim(
    id="information_paradox",
    title="Whether information escapes an evaporating black hole",
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Hawking1976",
            url_or_id="Phys. Rev. D 14, 2460 (1976)",
            kind="peer-reviewed paper (states the paradox / information loss)",
        ),
        Source(
            label="Susskind1993",
            url_or_id="arXiv:hep-th/9306069",
            kind="peer-reviewed paper (black-hole complementarity)",
        ),
        Source(
            label="Penington2019",
            url_or_id="arXiv:1905.08255",
            kind="peer-reviewed paper (islands / Page curve)",
        ),
        Source(
            label="AMPPSSY2019",
            url_or_id="arXiv:1911.12333",
            kind="peer-reviewed paper (replica wormholes, unitary entropy)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "The original argument: purely thermal Hawking emission carries no "
                "information, so an initial pure state would evolve into a mixed "
                "one, violating unitarity of quantum mechanics."
            ),
            source_ref="Hawking1976",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Recent replica-wormhole / island computations reproduce a Page "
                "curve consistent with unitary evolution, implying information is "
                "preserved — but within specific toy models, not full quantum "
                "gravity."
            ),
            source_ref="AMPPSSY2019",
        ),
    ],
    open_questions=[
        "By what concrete physical mechanism, if any, does information leave the "
        "black-hole interior?",
        "Do the island / replica-wormhole results extend from toy models to "
        "realistic four-dimensional evaporating black holes?",
        "Is the resolution compatible with a smooth horizon, or does it force "
        "structure there (see the firewall claim)?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Since 2019 the replica-wormhole / island programme has produced a "
            "fast-growing body of papers reworking the problem.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "No settled resolution: the island results recover a unitary Page "
            "curve in toy models, but the concrete bulk mechanism for realistic "
            "black holes is not agreed upon.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "The regime that would decide it — near-Planckian evaporation — is "
            "beyond any conceivable observation, so it advances by theoretical "
            "consistency rather than measurement.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — the firewall                                 🔴 Speculative        #
# --------------------------------------------------------------------------- #
firewall = Claim(
    id="firewall",
    title="An infalling observer meets a high-energy 'firewall' at the horizon",
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="AMPS2013",
            url_or_id="arXiv:1207.3123",
            kind="peer-reviewed paper (JHEP 2013:062, states the firewall)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical derivation",
            description=(
                "Almheiri, Marolf, Polchinski and Sully argued that unitarity, "
                "locality and a smooth horizon cannot all hold; giving up "
                "smoothness yields a wall of high-energy quanta — a firewall — at "
                "the horizon."
            ),
            source_ref="AMPS2013",
        ),
    ],
    open_questions=[
        "Is the firewall a real feature or an artefact of assumptions later "
        "resolved by islands / complementarity?",
        "There is no conceivable near-term observation that could test it, since "
        "it lives at the horizon of a distant black hole.",
    ],
    status_reason=[
        ConditionAssessment(
            "no_observational_evidence", True,
            "There is no observational evidence for a firewall and no proposed "
            "way to observe one.",
        ),
        ConditionAssessment(
            "pure_theoretical_derivation", True,
            "It is a purely theoretical consequence drawn from a clash of "
            "assumptions, not a modelled prediction of any observed system.",
        ),
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "The field does not accept it as real; many regard the underlying "
            "tension as resolved by island / complementarity arguments.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5 — Kerr describes astrophysical BHs              🔵 Strong             #
# --------------------------------------------------------------------------- #
kerr_describes_astrophysical_bh = Claim(
    id="kerr_describes_astrophysical_bh",
    title=(
        "Astrophysical black holes are well described by the Kerr metric "
        "(mass and spin)"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="LIGO2016-GR-tests",
            url_or_id="arXiv:1602.03841",
            kind="collaboration result (peer-reviewed, PRL 116, 221101, 2016; "
                 "tests of GR with GW150914)",
        ),
        Source(
            label="EHT2019-M87-I-kerr",
            url_or_id="arXiv:1906.11238",
            kind="collaboration result (peer-reviewed, ApJL 875, L1; M87* "
                 "shadow size vs Kerr prediction)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "The GW150914 ringdown and inspiral–merger consistency tests "
                "agree with a Kerr remnant within the precision of the first "
                "detection, with no evidence for large deviations from GR."
            ),
            source_ref="LIGO2016-GR-tests",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The M87* ring diameter matches the photon-orbit / shadow scale "
                "expected for a Kerr black hole of the dynamically estimated "
                "mass, under standard emission assumptions."
            ),
            source_ref="EHT2019-M87-I-kerr",
        ),
    ],
    open_questions=[
        "How tightly can higher multipoles and non-Kerr metrics be constrained "
        "with next-generation GW detectors and multi-frequency EHT?",
        "Do accretion-flow systematics still allow mild horizonless mimickers "
        "at current resolution?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Kerr as the astrophysical black-hole spacetime is the default in "
            "GW data analysis and EHT modelling.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Parametrised non-Kerr metrics and exotic compact objects remain "
            "active minority programmes.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Each new ringdown and horizon-scale image has been consistent with "
            "Kerr within errors, refining bounds rather than displacing the "
            "framework.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 6 — SMBHs in galaxy nuclei                        🔵 Strong             #
# --------------------------------------------------------------------------- #
smbh_common_in_galaxy_nuclei = Claim(
    id="smbh_common_in_galaxy_nuclei",
    title=(
        "Supermassive black holes commonly inhabit the nuclei of massive "
        "galaxies"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="KormendyHo2013",
            url_or_id="arXiv:1304.7762",
            kind="peer-reviewed paper (ARA&A 51, 511, 2013; coevolution of "
                 "SMBHs and galaxies)",
        ),
        Source(
            label="EHT2022-SgrA-smbh",
            url_or_id="arXiv:2311.08680",
            kind="collaboration result (peer-reviewed, ApJL 930, L12; Sgr A* "
                 "shadow)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Decades of stellar and gas dynamical measurements find "
                "central dark masses of millions to billions of solar masses "
                "in nearby massive galaxies, correlating with bulge "
                "properties."
            ),
            source_ref="KormendyHo2013",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Horizon-scale imaging of Sgr A* confirms that the Milky Way's "
                "central dark mass is consistent with a four-million-solar-mass "
                "black hole, anchoring the local calibration of the SMBH "
                "picture."
            ),
            source_ref="EHT2022-SgrA-smbh",
        ),
    ],
    open_questions=[
        "How did the first seeds form and grow to billion-solar-mass quasars "
        "by z ~ 7?",
        "What is the occupation fraction in low-mass and dwarf galaxies?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Central SMBHs in massive galaxies are standard extragalactic "
            "astronomy.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Some nuclei may host nuclear star clusters without a dominant "
            "BH; that is a refinement of occupation, not a rejection of SMBHs "
            "in massive systems.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Dynamical samples, AGN demography and EHT targets continually "
            "reinforce the nuclear-SMBH paradigm.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 7 — lower mass gap                                🟡 Competing          #
# --------------------------------------------------------------------------- #
lower_mass_gap_compact_objects = Claim(
    id="lower_mass_gap_compact_objects",
    title=(
        "A lower mass gap between the heaviest neutron stars and the lightest "
        "stellar black holes is a real feature of nature versus a selection "
        "effect"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="GW190814",
            url_or_id="arXiv:2006.12611",
            kind="collaboration result (peer-reviewed, ApJL 896, L44, 2020; "
                 "2.6 Msun compact object in the mass-gap region)",
        ),
        Source(
            label="GWTC3-2023-gap",
            url_or_id="arXiv:2111.03606",
            kind="collaboration result (peer-reviewed, Phys. Rev. X 13, "
                 "041039, 2023; population context)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "GW190814's secondary has a mass ~2.6 Msun, sitting above "
                "canonical neutron-star maxima and below many stellar-BH "
                "masses, forcing the gap question into multi-messenger view."
            ),
            source_ref="GW190814",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Population analyses of GW catalogues and X-ray binaries "
                "debate whether the ~2–5 Msun region is underpopulated by "
                "physics (explosion engine / pair physics) or by detection "
                "and classification bias."
            ),
            source_ref="GWTC3-2023-gap",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Physical lower mass gap",
            supporting=(
                "Core-collapse engines and fallback models can suppress "
                "remnants in a window above the maximum NS mass."
            ),
            opposing=(
                "Events like GW190814 may fill or blur the window; the gap "
                "edges depend on uncertain NS EOS and explosion physics."
            ),
            limitations=(
                "Small-number statistics at the NS–BH boundary."
            ),
        ),
        CompetingModel(
            name="Selection / classification continuum",
            supporting=(
                "Detection thresholds, electromagnetic follow-up bias and "
                "ambiguous mass–spin degeneracies can mimic a gap."
            ),
            opposing=(
                "Some X-ray binary samples still show a dearth even after "
                "bias discussions."
            ),
            limitations=(
                "Heterogeneous electromagnetic and GW selection functions."
            ),
        ),
    ],
    open_questions=[
        "Is GW190814's secondary a heavy NS, a light BH, or something else?",
        "Will larger GW samples fill 2–5 Msun smoothly?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Physical-gap and selection-effect camps are both actively "
            "published in the GW and X-ray binary literature.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "Borderline-mass events and still-limited samples leave the "
            "gap's reality unsettled.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Reviews and catalogue papers document the split explicitly.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 8 — jets extract BH spin                          🟠 Frontier           #
# --------------------------------------------------------------------------- #
jets_extract_bh_spin = Claim(
    id="jets_extract_bh_spin",
    title=(
        "Powerful extragalactic jets are powered by extracting black-hole "
        "rotational energy (Blandford–Znajek–type processes)"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="BlandfordZnajek1977",
            url_or_id="doi:10.1093/mnras/179.3.433",
            kind="peer-reviewed paper (MNRAS 179, 433, 1977; electromagnetic "
                 "extraction of BH rotational energy)",
        ),
        Source(
            label="EHT2021-M87-pol",
            url_or_id="arXiv:2105.01169",
            kind="collaboration result (peer-reviewed, ApJL 910, L12/L13; "
                 "M87* polarised ring / magnetic structure)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "The Blandford–Znajek mechanism shows that ordered magnetic "
                "fields threading a spinning Kerr hole can extract rotational "
                "energy as a Poynting-flux dominated outflow."
            ),
            source_ref="BlandfordZnajek1977",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "EHT polarimetric images of M87* reveal a magnetised "
                "near-horizon flow organised in a way consistent with "
                "magnetically arrested disk / jet-launching models often "
                "paired with spin extraction."
            ),
            source_ref="EHT2021-M87-pol",
        ),
    ],
    open_questions=[
        "What fraction of jet power comes from BH spin versus the accretion "
        "disk (Blandford–Payne)?",
        "Can spin measurements from X-ray reflection and jet power be "
        "reconciled object by object?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "GRMHD jet-launching simulations and EHT polarimetry form a "
            "fast-moving programme.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Spin extraction is a leading framework; disk-wind power remains "
            "a live alternative or co-channel for many sources.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "Direct, clean spin–jet efficiency measurements are still sparse.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 9 — horizonless GW echoes                         🔴 Speculative        #
# --------------------------------------------------------------------------- #
horizonless_gw_echoes = Claim(
    id="horizonless_gw_echoes",
    title=(
        "Gravitational-wave echoes from reflective horizonless surfaces have "
        "been observationally established"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Abedi2017",
            url_or_id="arXiv:1612.00266",
            kind="peer-reviewed paper (echo searches in LIGO open data; "
                 "claims and methods contested)",
        ),
        Source(
            label="LIGO2016-GR-tests-echo",
            url_or_id="arXiv:1602.03841",
            kind="collaboration result (peer-reviewed; GR tests / ringdown "
                 "consistency — no established echo detection)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Some horizonless ultra-compact object models predict delayed "
                "repeating pulses (echoes) after the main ringdown if the "
                "would-be horizon is replaced by a partially reflecting "
                "surface."
            ),
            source_ref="Abedi2017",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "LIGO–Virgo analyses of merger ringdowns are consistent with "
                "standard Kerr damping within published tests; the community "
                "does not treat echo detections as established."
            ),
            source_ref="LIGO2016-GR-tests-echo",
        ),
    ],
    open_questions=[
        "Can future detectors set decisive upper limits that close popular "
        "echo parameter spaces?",
        "Are reported low-significance echo candidates reproducible under "
        "blind analyses?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "The field does not accept GW echoes as an established detection.",
        ),
        ConditionAssessment(
            "no_observational_evidence", True,
            "No community-accepted observational evidence establishes echoes; "
            "claimed signals remain contested or unreproduced at discovery "
            "significance.",
        ),
    ],
    status_history=[],
)


BLACK_HOLE = Topic(
    id="black_hole",
    title="Black holes",
    summary=(
        "Container topic (no light of its own). 🟢 horizon bedrock; 🔵 "
        "Hawking theory, Kerr description, nuclear SMBHs; 🟡 lower mass "
        "gap; 🟠 GW catalogues, spin-powered jets, information paradox; "
        "🔴 firewall + established GW echoes (not accepted)."
    ),
    claims=[
        event_horizon_exists,
        hawking_radiation,
        kerr_describes_astrophysical_bh,
        smbh_common_in_galaxy_nuclei,
        lower_mass_gap_compact_objects,
        bbh_mergers_catalogued,
        jets_extract_bh_spin,
        information_paradox,
        firewall,
        horizonless_gw_echoes,
    ],
)
