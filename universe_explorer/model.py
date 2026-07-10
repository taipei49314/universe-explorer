"""Frozen v0 data model (spec section 2 and 3).

Design pivot that must not be reverted: the *status light belongs to the Claim,
not to the Topic*. A Topic is only a container and has no light of its own; two
claims under the same topic can carry different lights.

The five-cell Scientific Status Taxonomy (section 3) is encoded here as machine
checkable entry conditions so that a human status decision is never mere
self-certification: `status_reason` must map, condition by condition, onto the
entry conditions of the claimed status, and any third party can use this table
to overturn a decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Status(Enum):
    """The five cells. Ordered from bedrock (Established) to ceiling
    (Speculative) so the UI can lay knowledge out as a shape."""

    ESTABLISHED = "Established Consensus"
    STRONG = "Strong Consensus"
    COMPETING = "Competing Models"
    FRONTIER = "Frontier Research"
    SPECULATIVE = "Speculative"

    @property
    def light(self) -> str:
        return {
            Status.ESTABLISHED: "🟢",
            Status.STRONG: "🔵",
            Status.COMPETING: "🟡",
            Status.FRONTIER: "🟠",
            Status.SPECULATIVE: "🔴",
        }[self]

    @property
    def rank(self) -> int:
        """Bedrock = 0 ... ceiling = 4. Used only for display ordering."""
        return list(Status).index(self)


# Entry conditions per status (section 3), frozen.
#
#   mode "all" -> every listed condition must hold (holds=True) for the light.
#   mode "any" -> at least one listed condition holding is enough.
#
# `status_reason` on a claim is a list of ConditionAssessment; the validator
# checks it against exactly this table. Condition keys used in a claim must come
# from the claimed status's set (no foreign keys, no invented conditions).
STATUS_CONDITIONS = {
    Status.ESTABLISHED: {
        "mode": "all",
        "conditions": {
            "multiple_independent_replications":
                "Repeatedly verified by several independent research groups.",
            "accepted_in_mainstream_textbooks":
                "Accepted in mainstream textbooks.",
            "no_mainstream_competing_theory":
                "No mainstream competing theory.",
            "no_recent_major_refutation":
                "No recent major refuting evidence.",
        },
    },
    Status.STRONG: {
        "mode": "all",
        "conditions": {
            "mainstream_model_support":
                "Supported by the mainstream model.",
            "minor_alternatives_exist":
                "A minority of alternative theories exist.",
            "overall_direction_robust":
                "New evidence may refine details, but the overall direction "
                "is highly stable.",
        },
    },
    Status.COMPETING: {
        "mode": "all",
        "conditions": {
            "two_or_more_mainstream_models":
                "At least two mainstream models coexist.",
            "no_decisive_evidence_yet":
                "No decisive evidence currently selects between them.",
            "genuine_scientific_camps":
                "The split is a real division in the field, not one asserted "
                "by the AI.",
        },
    },
    Status.FRONTIER: {
        "mode": "any",
        "conditions": {
            "new_discovery": "A new discovery.",
            "insufficient_sample": "Sample size still insufficient.",
            "insufficient_observation": "Observation still insufficient.",
            "rapidly_growing_literature": "Papers are accumulating fast.",
            "no_consensus_formed_yet": "No consensus has formed yet.",
        },
    },
    Status.SPECULATIVE: {
        "mode": "any",
        "conditions": {
            "no_observational_evidence": "No observational evidence.",
            "pure_theoretical_derivation": "Pure theoretical derivation.",
            "not_yet_peer_reviewed": "Not yet peer reviewed.",
            "philosophical_inference": "A philosophical inference.",
            "not_accepted_by_mainstream":
                "Not yet accepted by the mainstream field.",
        },
    },
}


@dataclass
class ConditionAssessment:
    """One line of `status_reason`: which entry condition, whether it holds,
    and the traceable justification. `holds` + `note` are what a reviewer uses
    to overturn a light."""

    condition: str
    holds: bool
    note: str


@dataclass
class Source:
    """Data Layer. The raw thing an evidence item points back to."""

    label: str
    url_or_id: str
    kind: str  # e.g. "peer-reviewed paper", "collaboration result", "textbook"


@dataclass
class Evidence:
    """Evidence Layer. Every item must carry a real source_ref that resolves to
    a Source.label on the same claim."""

    type: str  # e.g. "direct observation", "theoretical derivation", "analog experiment"
    description: str
    source_ref: str


@dataclass
class CompetingModel:
    """Only populated when status == COMPETING."""

    name: str
    supporting: str
    opposing: str
    limitations: str


@dataclass
class StatusChange:
    """A recorded light migration. v0 does not act on these, but the field is
    kept because it is the trigger basis for future push notifications."""

    date: str
    from_status: str
    to_status: str
    trigger: str


@dataclass
class Claim:
    """The smallest unit. The status light lives here."""

    id: str
    title: str
    status: Status
    status_reason: List[ConditionAssessment] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    competing_models: List[CompetingModel] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)
    sources: List[Source] = field(default_factory=list)
    status_history: List[StatusChange] = field(default_factory=list)


@dataclass
class Topic:
    """A container. It has NO status light of its own."""

    id: str
    title: str
    summary: str
    claims: List[Claim] = field(default_factory=list)
