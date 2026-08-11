"""Cosmology — universe-scale domain (complements dark_matter / black_hole).

Paper-grade map for theme 「宇宙」, with a deepened **H0 cluster**.
Same schema and courts as every other topic. Do not conflate expansion (🟢)
with particle dark matter (see dark_matter) or settle H0 by tone alone.

H0 cluster (read together):
  H0_tension_local_vs_cmb     🟡 umbrella competition (local ladder vs CMB+ΛCDM)
  shoes_local_H0_high         🔵 Cepheid–SN local programme (Strong pole; tension stays Competing)
  cmb_lcdm_implies_low_H0     🟠 early-universe inference under ΛCDM
  trgb_vs_cepheid_local_H0    🟡 calibrator split inside the local ladder
  early_dark_energy_H0_fix  🟠 proposed early-universe relief
  strong_lensing_time_delay_H0 🟠 geometric time-delay route
  standard_sirens_H0          🟠 GW multi-messenger route

Other claims:
  universe_is_expanding / cmb_hot_big_bang 🟢
  accelerated_expansion 🔵
  cosmic_inflation_early_universe 🟠  (umbrella)
  inflation_slow_roll_planck      🟠  Planck slow-roll preference
  primordial_tensors_undetected   🟠  B-mode / r upper limits
  inflation_vs_noninflation_alts  🟡  inflation vs bounce-class alternatives
  eternal_inflation_multiverse    🔴  speculative multiverse reading
  cyclic_or_bounce_replaces_bb    🔴
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
# Claim 1 — the universe is expanding                    🟢 Established        #
# --------------------------------------------------------------------------- #
universe_is_expanding = Claim(
    id="universe_is_expanding",
    trace_refs=['Hubble1929', 'Freedman2001'],
    title="The universe is expanding: distant galaxies recede with distance",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="Hubble1929",
            url_or_id="doi:10.1073/pnas.15.3.168",
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
    trace_refs=['PenziasWilson1965', 'Planck2018-I'],
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
    trace_refs=['Riess1998', 'Perlmutter1999'],
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
        "Do strong-lensing and standard-siren routes converge with either pole?",
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
# Claim 4a — SH0ES local ladder                          🔵 Strong             #
# Overturn: issue #5 accept FRONTIER→STRONG (v5-Q2 Sprint A). Tension stays
# on H0_tension_local_vs_cmb (COMPETING). Evidence axis remains E3 (indirect).
# --------------------------------------------------------------------------- #
shoes_local_H0_high = Claim(
    id="shoes_local_H0_high",
    trace_refs=['Riess2022b', 'Verde2019'],
    title=(
        "Cepheid-calibrated Type Ia supernova ladders measure a high local "
        "Hubble constant near 73 km s^-1 Mpc^-1"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="Riess2022b",
            url_or_id="arXiv:2112.04510",
            kind="peer-reviewed paper (ApJL 934, L7, 2022; SH0ES)",
        ),
        Source(
            label="Verde2019",
            url_or_id="arXiv:1907.10625",
            kind="peer-reviewed paper (Nat. Astron. 3, 891, 2019; H0 tension "
                 "review)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "The SH0ES programme builds a geometric anchor → Cepheid → "
                "SN Ia distance ladder and reports a local H0 substantially "
                "above the Planck ΛCDM inference, with detailed systematic "
                "error budgets."
            ),
            source_ref="Riess2022b",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Community reviews place Cepheid–SN local determinations "
                "among the highest-precision late-universe H0 routes and "
                "document their persistent offset from early-universe "
                "inferences."
            ),
            source_ref="Verde2019",
        ),
    ],
    open_questions=[
        "How much do metallicity, crowding and SN Ia host-mass steps still "
        "shift the SH0ES central value?",
        "Will JWST Cepheid photometry change the ladder zero-point?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "The Cepheid → Type Ia supernova distance ladder is a mainstream "
            "late-universe route to H0; the SH0ES programme reports a local "
            "value near 73 km s^-1 Mpc^-1 with a published systematic budget "
            "(Riess et al., ApJL 934, L7, 2022; arXiv:2112.04510).",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Alternate local calibrators (e.g. TRGB) and ongoing systematic "
            "reanalyses form a genuine minority/alternate track; they refine "
            "or cross-check the ladder rather than displace Cepheid–SN as a "
            "mainstream programme (context in Verde, Treu & Riess 2019; "
            "arXiv:1907.10625).",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "The multi-year direction of a high local H0 from Cepheid–SN "
            "ladders is stable; new evidence concentrates on zero-point and "
            "systematics (open_questions), not on abandoning the ladder "
            "method. Residual tension with CMB+ΛCDM is carried by the "
            "separate Competing claim H0_tension_local_vs_cmb — not by "
            "keeping this pole at Frontier.",
        ),
    ],
    status_history=[
        StatusChange(
            date="2026-08-11",
            from_status="Frontier Research",
            to_status="Strong Consensus",
            trigger=(
                "v5-Q2 Sprint A accept: issue "
                "https://github.com/taipei49314/universe-explorer/issues/5 — "
                "Frontier over-weighted literature motion and residual "
                "systematics; Strong triad holds for the local ladder "
                "determination. H0 tension remains Competing on "
                "H0_tension_local_vs_cmb. Evidence axis unchanged (E3)."
            ),
        ),
    ],
)

# --------------------------------------------------------------------------- #
# Claim 4b — CMB+ΛCDM low H0                             🟠 Frontier           #
# --------------------------------------------------------------------------- #
cmb_lcdm_implies_low_H0 = Claim(
    id="cmb_lcdm_implies_low_H0",
    title=(
        "Under flat ΛCDM, CMB acoustic-scale data imply a Hubble constant "
        "near 67–68 km s^-1 Mpc^-1"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Planck2018-VI-H0b",
            url_or_id="arXiv:1807.06209",
            kind="collaboration result (peer-reviewed, A&A 641, A6, 2020)",
        ),
        Source(
            label="Verde2019b",
            url_or_id="arXiv:1907.10625",
            kind="peer-reviewed paper (Nat. Astron. 3, 891, 2019)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Planck baseline fits within flat ΛCDM calibrate the sound "
                "horizon and infer H0 ≈ 67.4 km s^-1 Mpc^-1, tightly coupled "
                "to other early-universe parameters."
            ),
            source_ref="Planck2018-VI-H0b",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Reviews of the H0 tension treat the CMB+ΛCDM route as the "
                "standard early-universe pole against which late-universe "
                "ladders are compared."
            ),
            source_ref="Verde2019b",
        ),
    ],
    open_questions=[
        "How model-dependent is the low H0 once early dark energy or Neff "
        "extensions are allowed?",
        "Do ground-based CMB experiments confirm Planck's acoustic-scale "
        "H0 inference?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "CMB parameter papers and tension reviews continually update "
            "the early-universe H0 pole.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "The inference is standard *inside* ΛCDM; whether ΛCDM is the "
            "correct model for H0 is the open question.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "H0 is not measured directly from the CMB; it is model-inferred "
            "from the angular scale of the sound horizon.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4c — TRGB vs Cepheid local calibrators           🟡 Competing          #
# --------------------------------------------------------------------------- #
trgb_vs_cepheid_local_H0 = Claim(
    id="trgb_vs_cepheid_local_H0",
    title=(
        "Tip-of-the-red-giant-branch and Cepheid calibrations of the local "
        "distance ladder disagree on H0"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Freedman2019",
            url_or_id="arXiv:1907.05922",
            kind="peer-reviewed paper (ApJ 882, 34, 2019; CCHP TRGB H0)",
        ),
        Source(
            label="Riess2022c",
            url_or_id="arXiv:2112.04510",
            kind="peer-reviewed paper (ApJL 934, L7, 2022; SH0ES Cepheids)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "The Carnegie–Chicago Hubble Programme uses TRGB stars as "
                "an alternate Population II calibrator and reports a local "
                "H0 lower than SH0ES Cepheid results, reducing tension with "
                "Planck in some analyses."
            ),
            source_ref="Freedman2019",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "SH0ES Cepheid-based ladders continue to report higher local "
                "H0 with expanded samples and JWST-era cross-checks, "
                "sustaining a calibrator-level disagreement inside the "
                "late universe."
            ),
            source_ref="Riess2022c",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Cepheid ladder (SH0ES-like) is closer to truth",
            supporting=(
                "Large Cepheid–SN samples, multiple anchors and detailed "
                "systematic campaigns favour a high local H0."
            ),
            opposing=(
                "Crowding, metallicity and photometric zero-points remain "
                "contested systematics."
            ),
            limitations=(
                "Depends on understanding of massive-star photometry in "
                "crowded fields."
            ),
        ),
        CompetingModel(
            name="TRGB ladder (CCHP-like) is closer to truth",
            supporting=(
                "TRGB is a Population II standard candle less tied to young "
                "star-forming regions; some TRGB values sit nearer CMB+ΛCDM."
            ),
            opposing=(
                "TRGB tip measurement, extinction and sample selection have "
                "their own systematics; not all TRGB analyses agree."
            ),
            limitations=(
                "Smaller SN calibrator samples than the Cepheid route in "
                "some releases."
            ),
        ),
    ],
    open_questions=[
        "Will JWST resolve Cepheid crowding enough to end the split?",
        "Can masers, eclipsing binaries and TRGB be forced onto one "
        "zero-point?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Cepheid- and TRGB-led local H0 programmes are both actively "
            "published at high precision.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "No community consensus has selected a single local calibrator "
            "hierarchy.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "SH0ES vs CCHP and related exchanges document a real split in "
            "the distance-ladder community.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4d — early dark energy as H0 relief              🟠 Frontier           #
# --------------------------------------------------------------------------- #
early_dark_energy_H0_fix = Claim(
    id="early_dark_energy_H0_fix",
    title=(
        "An early dark-energy component before recombination can raise the "
        "CMB-inferred Hubble constant toward local values"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Poulin2019",
            url_or_id="arXiv:1811.04083",
            kind="peer-reviewed paper (Phys. Rev. Lett. 122, 221301, 2019; "
                 "early dark energy)",
        ),
        Source(
            label="Verde2019c",
            url_or_id="arXiv:1907.10625",
            kind="peer-reviewed paper (Nat. Astron. 3, 891, 2019)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Early dark energy (EDE) models inject extra energy density "
                "before recombination, shrinking the sound horizon so that "
                "CMB data accommodate a higher H0 while attempting to "
                "preserve acoustic-peak fits."
            ),
            source_ref="Poulin2019",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Tension reviews list EDE and related early-universe "
                "extensions among the leading *proposed* resolutions, while "
                "noting residual conflicts with large-scale structure or "
                "other datasets in many implementations."
            ),
            source_ref="Verde2019c",
        ),
    ],
    open_questions=[
        "Can EDE fit Planck+BAO+SNe without worsening S8 or other tensions?",
        "Is there a microphysical EDE candidate tied to particle physics?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "EDE and early-universe extension papers proliferated after the "
            "H0 tension intensified.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "EDE is a leading proposal, not an established resolution.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No unique EDE signature has been confirmed; constraints are "
            "from global fits, not direct detection of a new component.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4e — strong-lensing time-delay H0                🟠 Frontier           #
# --------------------------------------------------------------------------- #
strong_lensing_time_delay_H0 = Claim(
    id="strong_lensing_time_delay_H0",
    title=(
        "Time delays in strongly lensed quasars provide a geometric Hubble "
        "constant independent of the traditional distance ladder"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Wong2020",
            url_or_id="arXiv:1907.04869",
            kind="peer-reviewed paper (MNRAS 498, 1420, 2020; H0LiCOW)",
        ),
        Source(
            label="Verde2019d",
            url_or_id="arXiv:1907.10625",
            kind="peer-reviewed paper (Nat. Astron. 3, 891, 2019)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "The H0LiCOW collaboration combines lensed-quasar time delays "
                "with mass models of the lens galaxies to infer H0, reporting "
                "values that have often sat closer to local ladders than to "
                "Planck ΛCDM — with mass-modelling systematics under scrutiny."
            ),
            source_ref="Wong2020",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "H0 tension reviews treat time-delay strong lensing as a "
                "key one-step geometric method complementary to Cepheids "
                "and the CMB."
            ),
            source_ref="Verde2019d",
        ),
    ],
    open_questions=[
        "How much do lens mass-sheet degeneracies still shift H0?",
        "Will larger TDCOSMO samples pull toward the local or CMB pole?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "H0LiCOW/TDCOSMO and related lensing-H0 papers form an active "
            "subfield.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Time-delay H0 is competitive but systematics-limited; not a "
            "sole arbiter of the tension.",
        ),
        ConditionAssessment(
            "insufficient_sample", True,
            "The number of golden lenses with exquisite models remains "
            "modest.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4f — standard sirens                             🟠 Frontier           #
# --------------------------------------------------------------------------- #
standard_sirens_H0 = Claim(
    id="standard_sirens_H0",
    title=(
        "Gravitational-wave standard sirens can measure H0 without a "
        "classical distance ladder"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Abbott2017-H0",
            url_or_id="arXiv:1710.05835",
            kind="collaboration result (peer-reviewed, Nature 551, 85, 2017; "
                 "GW170817 H0)",
        ),
        Source(
            label="Verde2019e",
            url_or_id="arXiv:1907.10625",
            kind="peer-reviewed paper (Nat. Astron. 3, 891, 2019)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "The binary neutron-star merger GW170817 with an "
                "electromagnetic counterpart provided a luminosity distance "
                "from the gravitational-wave signal and a redshift from the "
                "host, yielding a first standard-siren H0 constraint."
            ),
            source_ref="Abbott2017-H0",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Reviews highlight standard sirens as a maturing third route "
                "to H0 whose error bars will shrink with the gravitational-wave "
                "event rate — still too wide to end the tension alone."
            ),
            source_ref="Verde2019e",
        ),
    ],
    open_questions=[
        "How many bright sirens are needed to match SH0ES or Planck "
        "precision?",
        "Can dark sirens with statistical host redshifts become competitive?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Post-GW170817 siren cosmology is a rapidly growing literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Sirens are established *as a method*; they have not yet "
            "delivered a tension-resolving H0.",
        ),
        ConditionAssessment(
            "insufficient_sample", True,
            "Bright siren events remain rare; current H0 posteriors are broad.",
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
# Claim 5a — Planck slow-roll preference                 🟠 Frontier           #
# --------------------------------------------------------------------------- #
inflation_slow_roll_planck = Claim(
    id="inflation_slow_roll_planck",
    title=(
        "CMB data prefer simple slow-roll inflationary potentials and "
        "constrain the scalar spectral index"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Planck2018-Xb",
            url_or_id="arXiv:1807.06211",
            kind="collaboration result (peer-reviewed, A&A 641, A10, 2020)",
        ),
        Source(
            label="Guth1981b",
            url_or_id="doi:10.1103/PhysRevD.23.347",
            kind="peer-reviewed paper (Phys. Rev. D 23, 347, 1981)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Planck analyses of primordial spectra report ns < 1 and "
                "tight limits on running and tensors, favouring plateau-like "
                "slow-roll models over many large-field alternatives."
            ),
            source_ref="Planck2018-Xb",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Slow-roll inflation supplies the dynamical framework in "
                "which a scalar field generates the observed nearly "
                "scale-invariant spectrum."
            ),
            source_ref="Guth1981b",
        ),
    ],
    open_questions=[
        "Which specific potential (if any) will survive next-generation "
        "CMB-S4 / LiteBIRD constraints?",
        "Is there detectable running of the spectral index?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Model-by-model Planck constraints and forecasts for future "
            "CMB missions form a large literature.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "A class of slow-roll models is preferred, not a unique inflaton.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "ns and upper limits on r do not identify a single microphysical "
            "model.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5b — primordial tensors undetected               🟠 Frontier           #
# --------------------------------------------------------------------------- #
primordial_tensors_undetected = Claim(
    id="primordial_tensors_undetected",
    title=(
        "Primordial gravitational-wave B-modes remain undetected, bounding "
        "the tensor-to-scalar ratio"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="BK2021",
            url_or_id="arXiv:2110.00483",
            kind="collaboration result (peer-reviewed; BICEP/Keck r limits)",
        ),
        Source(
            label="Planck2018-Xc",
            url_or_id="arXiv:1807.06211",
            kind="collaboration result (peer-reviewed, A&A 641, A10, 2020)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "BICEP/Keck degree-scale polarisation searches report no "
                "significant primordial B-mode excess after dust modelling, "
                "setting leading upper limits on the tensor-to-scalar ratio r."
            ),
            source_ref="BK2021",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Planck temperature and polarisation combinations similarly "
                "bound r and jointly constrain inflationary model space when "
                "combined with BICEP/Keck."
            ),
            source_ref="Planck2018-Xc",
        ),
    ],
    open_questions=[
        "Will the next generation of B-mode experiments detect r > 0?",
        "How low must r fall before large classes of high-scale inflation "
        "are excluded?",
    ],
    status_reason=[
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "B-mode experiments and foreground-cleaning methods are a major "
            "ongoing effort.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Upper limits are robust in outline; a positive primordial "
            "detection has not been established.",
        ),
        ConditionAssessment(
            "insufficient_observation", True,
            "No confirmed primordial B-mode signal; only limits on r.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5c — inflation vs non-inflation alternatives     🟡 Competing          #
# --------------------------------------------------------------------------- #
inflation_vs_noninflation_alts = Claim(
    id="inflation_vs_noninflation_alts",
    title=(
        "The early universe is described by inflation versus non-inflationary "
        "alternatives such as bounces"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Planck2018-Xd",
            url_or_id="arXiv:1807.06211",
            kind="collaboration result (peer-reviewed, A&A 641, A10, 2020)",
        ),
        Source(
            label="IjjasSteinhardt2018b",
            url_or_id="arXiv:1803.01961",
            kind="peer-reviewed paper (bounce / alternative early-universe "
                 "discussion)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "CMB constraints are routinely interpreted within "
                "inflationary slow-roll scenarios that fit ns and limit r, "
                "making inflation the working early-universe standard."
            ),
            source_ref="Planck2018-Xd",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Bouncing and related non-singular scenarios are developed "
                "as alternatives that aim to replace or precede the hot big "
                "bang without a quasi-de Sitter inflating phase."
            ),
            source_ref="IjjasSteinhardt2018b",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Inflationary hot big bang",
            supporting=(
                "Horizon/flatness motivation, near-scale-invariant spectrum, "
                "and detailed CMB fits under slow-roll."
            ),
            opposing=(
                "Inflation has an initial-conditions and multiverse debate; "
                "the inflaton is unidentified."
            ),
            limitations=(
                "Many viable potentials remain; tensors not yet seen."
            ),
        ),
        CompetingModel(
            name="Bounce / non-inflationary early universe",
            supporting=(
                "Seeks to avoid singular beginnings and can generate "
                "perturbations in some constructions."
            ),
            opposing=(
                "Must confront instability, anisotropy and detailed CMB "
                "success of inflation-based fits."
            ),
            limitations=(
                "No consensus bounce model matches the full precision dataset."
            ),
        ),
    ],
    open_questions=[
        "Which observable most cleanly separates inflation from bounce "
        "scenarios?",
        "Do primordial features or non-Gaussianity favour one camp?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Inflation is the default framework; bounce-class alternatives "
            "remain actively published theoretical programmes.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "CMB success under inflation is strong but not a logical "
            "elimination of all alternatives.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "Reviews and dedicated papers document inflation-versus-"
            "alternative debates over decades.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5d — eternal inflation / multiverse              🔴 Speculative        #
# --------------------------------------------------------------------------- #
eternal_inflation_multiverse = Claim(
    id="eternal_inflation_multiverse",
    title=(
        "Eternal inflation generates a multiverse of pocket universes as "
        "the correct reading of high-scale inflation"
    ),
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Guth1981c",
            url_or_id="doi:10.1103/PhysRevD.23.347",
            kind="peer-reviewed paper (Phys. Rev. D 23, 347, 1981; "
                 "inflation framework)",
        ),
        Source(
            label="Planck2018-Xe",
            url_or_id="arXiv:1807.06211",
            kind="collaboration result (peer-reviewed, A&A 641, A10, 2020; "
                 "data constrain models, not multiverse ontology)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "Some inflationary dynamics generically lead to eternal "
                "inflation and a multiverse of causally disconnected "
                "regions — a theoretical extrapolation beyond what CMB "
                "data can directly confirm."
            ),
            source_ref="Guth1981c",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Precision CMB constraints test inflationary *potentials* "
                "and spectra; they do not observationally establish a "
                "multiverse ontology."
            ),
            source_ref="Planck2018-Xe",
        ),
    ],
    open_questions=[
        "Is eternal inflation inevitable in viable high-scale models?",
        "Are there any empirical signatures of a multiverse?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "Multiverse readings of inflation are highly debated and not "
            "established empirical consensus.",
        ),
        ConditionAssessment(
            "philosophical_inference", True,
            "Much of the multiverse claim extrapolates beyond currently "
            "testable cosmology into interpretative territory.",
        ),
        ConditionAssessment(
            "pure_theoretical_derivation", True,
            "The positive case is theoretical dynamics, not a confirmed "
            "observation of other pocket universes.",
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
        "Universe-scale container (theme: 宇宙): deepened H0 cluster + "
        "inflation cluster. 🟢 expansion/CMB; 🔵 acceleration; 🟡 H0 + "
        "TRGB/Cepheid + inflation-vs-bounce; 🟠 ladders, EDE, lensing, "
        "sirens, slow-roll, tensors; 🔴 multiverse + bounce-as-replacement."
    ),
    claims=[
        universe_is_expanding,
        cmb_hot_big_bang,
        accelerated_expansion,
        H0_tension_local_vs_cmb,
        shoes_local_H0_high,
        cmb_lcdm_implies_low_H0,
        trgb_vs_cepheid_local_H0,
        early_dark_energy_H0_fix,
        strong_lensing_time_delay_H0,
        standard_sirens_H0,
        cosmic_inflation_early_universe,
        inflation_slow_roll_planck,
        primordial_tensors_undetected,
        inflation_vs_noninflation_alts,
        eternal_inflation_multiverse,
        cyclic_or_bounce_replaces_bb,
    ],
)
