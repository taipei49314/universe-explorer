"""P1.5 — the evidence axis: derived, never declared.

The consensus axis (the five-cell status light) stays human-judged with a
traceable status_reason. This module adds the second axis, and its judging
mechanism is deliberately different: *nobody* fills it in. It is computed by
public rules over the recorded evidence items (each of which hangs on a real,
fetch-verified source). The only way to move a claim on this axis is to record
new evidence — and new evidence is itself policed by the v0 constitution and
the P1 cite=>fetch rule.

That makes constitution rule 3 literal: certainty *emerges* from the content of
the evidence fields; it is not declared by an AI or a human.

Divergence (e.g. hawking_radiation: Strong consensus x analog-only evidence) is
likewise a mechanical juxtaposition of two traceable facts, not an opinion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

from .model import Claim, Status, tier_of

# Evidence.type controlled vocabulary. Without this, mechanical derivation
# would be built on free-text sand. Validator enforces membership.
DIRECT = "direct observation"
INDIRECT = "indirect observation"
ANALOG = "analog experiment"
THEORY_DERIVATION = "theoretical derivation"
THEORY_RESULT = "theoretical result"

EVIDENCE_TYPE_VOCAB = {
    DIRECT, INDIRECT, ANALOG, THEORY_DERIVATION, THEORY_RESULT,
}


class EvidenceStrength(Enum):
    """Discrete cells only — a continuous score would be fake precision with
    extra steps."""

    E1_MULTIPLE_DIRECT = "multiple independent direct observations"
    E2_SINGLE_DIRECT = "direct observation (single line)"
    E3_INDIRECT_ANALOG = "indirect / analog only"
    E4_THEORETICAL = "theoretical only"
    E5_NONE = "no recorded evidence"

    @property
    def short(self) -> str:
        return self.name.split("_")[0]  # "E1" ... "E5"


@dataclass
class Derivation:
    """The traceable output: the grade plus the rule-by-rule reasoning a third
    party can recompute from the public rules and overturn."""

    strength: EvidenceStrength
    reasoning: List[str]


def derive(claim: Claim) -> Derivation:
    """Apply the public rules (P1.5 spec section 1, E1 as amended by
    Amendment #4), strongest cell first."""
    reasons: List[str] = []

    direct = [e for e in claim.evidence if e.type == DIRECT]
    indirect_analog = [e for e in claim.evidence if e.type in (INDIRECT, ANALOG)]
    theoretical = [e for e in claim.evidence
                   if e.type in (THEORY_DERIVATION, THEORY_RESULT)]

    # Amendment #4: independence-of-replication is a claim about the reviewed
    # record — only PRIMARY-tier sources can establish E1.
    # Amendment #7: those PRIMARY sources must also be *fetchable* endpoints
    # (arXiv or DOI after normalization). A kind string containing
    # "peer-reviewed" with https://example.com is not E1.
    # Amendment #9: independence is counted by *paper identity* (normalized
    # arXiv id / DOI), not by source label — so one paper under two labels
    # (or v1/v2) cannot mint E1.
    from .provenance import is_fetchable_endpoint, paper_id_of

    source_by_label = {s.label: s for s in claim.sources}
    tier_by_label = {s.label: tier_of(s.kind) for s in claim.sources}
    direct_sources = {e.source_ref for e in direct}
    primary_direct_sources = {
        ref for ref in direct_sources
        if tier_by_label.get(ref) == "PRIMARY"
    }
    fetchable_primary_direct = {
        ref for ref in primary_direct_sources
        if (src := source_by_label.get(ref)) is not None
        and is_fetchable_endpoint(src.url_or_id)
    }
    independent_paper_ids = {
        paper_id_of(source_by_label[ref].url_or_id)
        for ref in fetchable_primary_direct
        if paper_id_of(source_by_label[ref].url_or_id) is not None
    }
    reasons.append(
        f"recorded evidence: {len(direct)} direct "
        f"(distinct sources: {len(direct_sources)}, "
        f"of which PRIMARY: {len(primary_direct_sources)}, "
        f"fetchable PRIMARY labels: {len(fetchable_primary_direct)}, "
        f"distinct paper ids: {len(independent_paper_ids)}), "
        f"{len(indirect_analog)} indirect/analog, {len(theoretical)} theoretical")

    if len(direct) >= 2 and len(independent_paper_ids) >= 2:
        reasons.append(
            "rule E1 (amendment-4/7/9): at least two direct observations "
            "hanging on distinct *papers* (normalized arXiv/DOI) that are "
            "PRIMARY and fetchable -> multiple independent direct")
        return Derivation(EvidenceStrength.E1_MULTIPLE_DIRECT, reasons)

    if direct:
        reasons.append(
            "rule E2: direct observation exists but not from two distinct "
            "fetchable PRIMARY *papers* -> single direct line")
        return Derivation(EvidenceStrength.E2_SINGLE_DIRECT, reasons)

    if indirect_analog:
        reasons.append(
            "rule E3: no direct observation; indirect or analog evidence "
            "exists -> indirect/analog only")
        return Derivation(EvidenceStrength.E3_INDIRECT_ANALOG, reasons)

    if theoretical:
        reasons.append(
            "rule E4: only theoretical derivations/results are recorded "
            "-> theoretical only")
        return Derivation(EvidenceStrength.E4_THEORETICAL, reasons)

    reasons.append("rule E5: no evidence recorded (unconstitutional on its own)")
    return Derivation(EvidenceStrength.E5_NONE, reasons)


# --- divergence: a mechanical juxtaposition, not an opinion -----------------

_HIGH_CONSENSUS = {Status.ESTABLISHED, Status.STRONG}
_WEAK_EVIDENCE = {
    EvidenceStrength.E3_INDIRECT_ANALOG,
    EvidenceStrength.E4_THEORETICAL,
    EvidenceStrength.E5_NONE,
}


def diverges(claim: Claim) -> bool:
    """High consensus resting on non-direct evidence — the axes point apart."""
    return claim.status in _HIGH_CONSENSUS and derive(claim).strength in _WEAK_EVIDENCE
