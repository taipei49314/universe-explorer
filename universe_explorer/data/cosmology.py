"""Cosmology — universe-scale domain (complements dark_matter / black_hole).

Paper-grade seed map for the expanded theme 「宇宙」. Same schema and courts
as every other topic. Do not conflate expansion (🟢) with particle dark matter
(see dark_matter domain) or with the still-open nature of dark energy.

Expected lights:
  universe_is_expanding              -> 🟢 Established
  cmb_hot_big_bang                   -> 🟢 Established
  accelerated_expansion              -> 🔵 Strong
  H0_tension_local_vs_cmb            -> 🟡 Competing
  cosmic_inflation_early_universe    -> 🟠 Frontier
  cyclic_or_bounce_replaces_bb       -> 🔴 Speculative
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
# Claim 1 — the universe is expanding                    🟢 Established        #
# --------------------------------------------------------------------------- #
universe_is_expanding = Claim(
    id="universe_is_expanding",
    title="The universe is expanding: distant galaxies recede with distance",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="Hubble1929",
            url_or_id="Proc. Natl. Acad. Sci. 15, 168 (1929)",
            kind="peer-reviewed paper (original distance–velocity relation)",
        ),
        Source(
            label="Freedman2001",
            url_or_id="arXiv:astro-ph/0012376",
            kind="peer-reviewed paper (ApJ 553, 47, 2001; HST Key Project)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Extragalactic nebulae show recession velocities that increase "
                "with distance, establishing a linear velocity–distance "
                "relation later identified with cosmic expansion."
            ),
            source_ref="Hubble1929",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The Hubble Space Telescope Key Project measured Cepheid "
                "distances to galaxies hosting secondary distance indicators, "
                "confirming cosmic expansion and calibrating the modern "
                "Hubble diagram."
            ),
            source_ref="Freedman2001",
        ),
    ],
    open_questions=[
        "What is the precise present-day expansion rate H0 once all "
        "systematics are controlled (see the H0-tension claim)?",
        "How does expansion couple to structure growth on the largest scales?",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Velocity–distance relations have been repeated with many "
            "distance ladders and redshift surveys over a century.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Cosmic expansion is standard content in every modern cosmology "
            "and astronomy textbook.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream theory denies expansion of the metric; debates "
            "concern rate, dark energy, and early-universe physics.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Subsequent surveys have only refined the expansion history.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — CMB / hot big bang                           🟢 Established        #
# --------------------------------------------------------------------------- #
cmb_hot_big_bang = Claim(
    id="cmb_hot_big_bang",
    title=(
        "The cosmic microwave background is relic radiation from a hot, "
        "dense early universe"
    ),
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="PenziasWilson1965",
            url_or_id="doi:10.1086/148307",
            kind="peer-reviewed paper (ApJ 142, 419, 1965; CMB discovery)",
        ),
        Source(
            label="Planck2018-I",
            url_or_id="arXiv:1807.06205",
            kind="collaboration result (peer-reviewed, A&A 641, A1, 2020; "
                 "Planck overview)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "A highly isotropic microwave excess antenna temperature was "
                "measured and identified as cosmic background radiation, "
                "not terrestrial or Galactic noise."
            ),
            source_ref="PenziasWilson1965",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Full-sky satellite maps (culminating in Planck) measure a "
                "blackbody spectrum and acoustic-peak structure in the CMB "
                "anisotropies, matching a hot big-bang plus recombination "
                "history to high precision."
            ),
            source_ref="Planck2018-I",
        ),
    ],
    open_questions=[
        "What physics set the initial fluctuations imprinted on the CMB?",
        "Are there residual anomalies (e.g. large-angle alignments) beyond "
        "ΛCDM expectations?",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Ground, balloon and multiple satellite generations confirm the "
            "CMB spectrum and anisotropy pattern.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "CMB as big-bang relic is core textbook cosmology.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream alternative explains the blackbody CMB plus "
            "acoustic peaks without a hot dense early phase.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Each generation of experiments has sharpened, not overturned, "
            "the hot-big-bang reading.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — accelerated expansion                        🔵 Strong             #
# --------------------------------------------------------------------------- #
accelerated_expansion = Claim(
    id="accelerated_expansion",
    title="The expansion of the universe is accelerating",
    status=Status.STRONG,
    sources=[
        Source(
            label="Riess1998",
            url_or_id="arXiv:astro-ph/9805201",
            kind="peer-reviewed paper (AJ 116, 1009, 1998; SN Ia)",
        ),
        Source(
            label="Perlmutter1999",
            url_or_id="arXiv:astro-ph/9812133",
            kind="peer-reviewed paper (ApJ 517, 565, 1999; SN Ia)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "High-redshift Type Ia supernovae are fainter than expected "
                "in a decelerating matter-only universe, implying accelerated "
                "expansion when combined with local calibrators."
            ),
            source_ref="Riess1998",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "An independent supernova cosmology project reached the same "
                "conclusion with a distinct high-z sample, establishing "
                "acceleration as a multi-team result."
            ),
            source_ref="Perlmutter1999",
        ),
    ],
    open_questions=[
        "Is acceleration driven by a cosmological constant, a dynamical "
        "dark-energy field, or modified gravity on large scales?",
        "Do supernova, BAO and CMB datasets remain fully consistent on "
        "the expansion history?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Accelerated expansion is the standard interpretation of SN Ia, "
            "BAO and CMB combinations in ΛCDM.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Modified-gravity and void alternatives exist but are minority "
            "programmes relative to dark energy / Λ.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Subsequent surveys have reinforced acceleration; debate shifted "
            "to the microphysical nature of dark energy, not the kinematic "
            "result. Evidence is cosmological inference (indirect).",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — H0 tension                                   🟡 Competing          #
# --------------------------------------------------------------------------- #
H0_tension_local_vs_cmb = Claim(
    id="H0_tension_local_vs_cmb",
    title=(
        "The Hubble constant from the local distance ladder disagrees with "
        "the value inferred from the CMB under ΛCDM"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Riess2022",
            url_or_id="arXiv:2112.04510",
            kind="peer-reviewed paper (ApJL 934, L7, 2022; SH0ES H0)",
        ),
        Source(
            label="Planck2018-VI-H0",
            url_or_id="arXiv:1807.06209",
            kind="collaboration result (peer-reviewed, A&A 641, A6, 2020)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Cepheid-calibrated Type Ia supernova ladders (SH0ES) measure "
                "a local H0 systematically higher than the Planck ΛCDM "
                "inference from the CMB acoustic scale."
            ),
            source_ref="Riess2022",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Planck 2018 baseline parameters imply a lower H0 when "
                "the sound horizon is calibrated within flat ΛCDM, defining "
                "the early-universe side of the tension."
            ),
            source_ref="Planck2018-VI-H0",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="New early- or late-universe physics",
            supporting=(
                "Extensions (e.g. early dark energy, extra relativistic "
                "species, evolving dark energy) can raise the CMB-inferred "
                "H0 or alter the late expansion history in some fits."
            ),
            opposing=(
                "Many extensions reintroduce tensions with BAO, CMB lensing "
                "or large-scale structure, or require fine-tuning."
            ),
            limitations=(
                "No single extension is uniquely selected by all datasets."
            ),
        ),
        CompetingModel(
            name="Unrecognised systematics in one or both ladders",
            supporting=(
                "Distance-ladder rungs (Cepheids, supernova standardisation) "
                "and CMB foreground/model assumptions can shift H0; some "
                "independent ladders report intermediate values."
            ),
            opposing=(
                "Multiple local analyses remain high while CMB+ΛCDM remains "
                "low, which is hard to dismiss as one team's error."
            ),
            limitations=(
                "Full cross-method consensus on residual systematics is "
                "still forming."
            ),
        ),
    ],
    open_questions=[
        "Will JWST Cepheid/TRGB work remove or harden the local H0 value?",
        "Which early-universe extensions survive joint BAO+CMB+SNe fits?",
        "Is the H0 tension physically linked to the S8 tension, or separate?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Both new-physics and systematics interpretations are actively "
            "published responses to the H0 offset.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "Significance depends on dataset combination; no consensus "
            "resolution exists.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Cosmology reviews and collaboration papers document a multi-year "
            "split — not an AI-invented dichotomy.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5 — cosmic inflation                             🟠 Frontier           #
# --------------------------------------------------------------------------- #
cosmic_inflation_early_universe = Claim(
    id="cosmic_inflation_early_universe",
    title=(
        "A quasi-exponential inflationary phase preceded the hot big bang "
        "and seeded cosmic structure"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Guth1981",
            url_or_id="doi:10.1103/PhysRevD.23.347",
            kind="peer-reviewed paper (Phys. Rev. D 23, 347, 1981)",
        ),
        Source(
            label="Planck2018-X",
            url_or_id="arXiv:1807.06211",
            kind="collaboration result (peer-reviewed, A&A 641, A10, 2020; "
                 "inflation constraints)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Inflationary models propose a brief accelerated expansion "
                "that solves horizon and flatness problems and generates "
                "nearly scale-invariant primordial fluctuations."
            ),
            source_ref="Guth1981",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Planck constraints on the scalar spectral index and "
                "tensor-to-scalar ratio favour simple slow-roll scenarios "
                "while excluding large regions of inflationary model space — "
                "supportive but not a unique identification of the inflaton."
            ),
            source_ref="Planck2018-X",
        ),
    ],
    open_questions=[
        "What field(s) drove inflation, and at what energy scale?",
        "Will primordial B-modes be detected, and at what r?",
        "Are bounce or other non-inflationary early-universe models viable?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Inflation model-building and CMB/large-scale-structure "
            "constraints form a vast, still-growing literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Inflation is the leading early-universe framework, but not a "
            "single established microphysical theory.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No direct detection of the inflaton or primordial gravitational "
            "waves has identified a unique model.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 6 — cyclic / bounce replaces big bang            🔴 Speculative        #
# --------------------------------------------------------------------------- #
cyclic_or_bounce_replaces_bb = Claim(
    id="cyclic_or_bounce_replaces_bb",
    title=(
        "A cyclic or bouncing cosmology replaces the hot big-bang singularity "
        "as the correct early-universe description"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="IjjasSteinhardt2018",
            url_or_id="arXiv:1803.01961",
            kind="peer-reviewed paper (Class. Quantum Grav. / review-level "
                 "bounce discussion; arXiv:1803.01961)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Bouncing and cyclic scenarios aim to replace or complement "
                "the singular hot big bang with a prior contracting phase, "
                "remaining active theoretical programmes without decisive "
                "observational selection over inflation plus hot big bang."
            ),
            source_ref="IjjasSteinhardt2018",
        ),
    ],
    open_questions=[
        "Do bounce models produce distinguishable CMB or GW signatures?",
        "Can they satisfy singularity and instability constraints?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "Hot big bang plus inflation remains the working standard; "
            "bounce/cyclic models are minority theoretical programmes.",
        ),
        ConditionAssessment(
            "pure_theoretical_derivation", True,
            "Positive case is theoretical construction, not a confirmed "
            "replacement of the hot-big-bang empirical core.",
        ),
    ],
    status_history=[],
)


COSMOLOGY = Topic(
    id="cosmology",
    title="Cosmology",
    summary=(
        "Universe-scale container (theme: 宇宙). No topic light. Shape: "
        "🟢 expansion + CMB bedrock; 🔵 accelerated expansion; 🟡 H0 tension; "
        "🟠 inflation; 🔴 bounce/cyclic alternatives. Complements dark_matter "
        "without duplicating particle identity claims."
    ),
    claims=[
        universe_is_expanding,
        cmb_hot_big_bang,
        accelerated_expansion,
        H0_tension_local_vs_cmb,
        cosmic_inflation_early_universe,
        cyclic_or_bounce_replaces_bb,
    ],
)
