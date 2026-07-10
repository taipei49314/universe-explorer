"""Black hole — the single v0 topic (spec sections 2 and 5).

Every field below is hand-filled with real content and a real source. Where a
source is genuinely near-absent (hawking_radiation has strong theory but almost
no direct observation) the split is recorded honestly in status_reason rather
than papered over. Rather under-fill than invent.

Expected lights (used to stress the "light belongs to the claim" pivot):
  event_horizon_exists  -> 🟢 Established
  hawking_radiation     -> 🔵 Strong   (theory strong, direct evidence ~ zero)
  information_paradox   -> 🟠 Frontier
  firewall              -> 🔴 Speculative
"""

from __future__ import annotations

from ..model import (
    Claim,
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


BLACK_HOLE = Topic(
    id="black_hole",
    title="Black holes",
    summary=(
        "A container topic. It carries no status light of its own — each claim "
        "below carries its own. Read the shape: a 🟢 bedrock (the horizon exists) "
        "under a 🔴 ceiling (the firewall)."
    ),
    claims=[
        event_horizon_exists,
        hawking_radiation,
        information_paradox,
        firewall,
    ],
)
