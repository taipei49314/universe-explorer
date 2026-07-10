"""Constitution checker (spec section 5).

Mechanical, not tasteful. It cannot tell whether a claim is *right*; it enforces
the hard red lines so that no record can quietly break the constitution:

  * evidence with no real source              -> error
  * a bare percentage / fabricated precision  -> error
  * open_questions replaced by a number       -> error
  * status_reason not mapping to the entry
    conditions of the claimed status          -> error

Write the checker first, fill the data second: that way the "no making things
up, no fake precision" rule is enforced by a machine from the very first record,
exactly as self-certification is not allowed for a human decision.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from .model import STATUS_CONDITIONS, Claim, Status, Topic

# Amendment #1 (docs/amendment-1-r7.md) splits "numbers" in two:
#
#   * declared confidence — vocabulary that states certainty as a number
#     ("共識度 73%", "confidence: 90"). Forbidden EVERYWHERE, evidence included:
#     even with a source attached, certainty may not be rewritten as a number.
#   * measured quantities — a bare % inside an evidence description. Allowed
#     there and only there, because every evidence line is already forced to
#     hang on a real source_ref (and, for arXiv, a verified fetch): the number
#     is a restatement of sourced content, not a declaration by the system.
#
# Everywhere else (title, open_questions, status_reason, competing_models) a
# bare % stays forbidden — editorial rule: quantities live in the Evidence
# layer, attached to sources.
_PERCENT_RE = re.compile(r"\d+(?:\.\d+)?\s*%|百分之")
_CONFIDENCE_RE = re.compile(
    r"(共識度|信心|置信|confidence|certainty|consensus)\s*[:：]?\s*"
    r"(約|around|about|~)?\s*\d",
    re.IGNORECASE,
)

# "Open Questions: 2" style numeric substitution for a list.
_COUNT_RE = re.compile(
    r"(open\s*questions?|open\s*problems?|未解|問題|疑問)\s*[:：]?\s*\d+",
    re.IGNORECASE,
)

# Amendment #3 (docs/amendment-3-source-tiers.md): source credibility tiers.
# The table itself lives in model.py since Amendment #4 (tiers are taxonomy);
# re-exported here so existing call sites keep working.
from .model import SOURCE_TIERS, tier_of  # noqa: F401  (re-export)

# Amendment #5 (docs/amendment-4-r8-tier-weighting.md, part 2): every rule
# must name its legal basis. A violation message cites the law that created
# the rule — "you broke the constitution" becomes "you broke THIS article".
# A rule missing from this registry is itself a test failure: no law, no rule.
LAWS = {
    # v0 constitution
    "invalid_status": "v0-constitution §2",
    "evidence_without_source": "v0-constitution §1/§4",
    "dangling_source_ref": "v0-constitution §4",
    "unsupported_claim": "v0-constitution §4",
    "no_fake_precision": "v0-constitution §3 (as amended by amendment-1)",
    "declared_confidence": "amendment-1",
    "no_numeric_open_questions": "v0-constitution §3",
    "empty_open_question": "v0-constitution §3",
    "numeric_open_question": "v0-constitution §3",
    "foreign_condition": "v0-constitution §3/§4",
    "unjustified_condition": "v0-constitution §4",
    "status_reason_incomplete": "v0-constitution §3",
    "condition_not_satisfied": "v0-constitution §3",
    "no_condition_satisfied": "v0-constitution §3",
    "competing_needs_models": "v0-constitution §2",
    "unexpected_competing_models": "v0-constitution §2",
    # P1.5 controlled vocabulary
    "invalid_evidence_type": "p1.5-spec §1",
    # Amendment #3 tiers
    "unclassifiable_source_kind": "amendment-3",
    # P1 data-layer provenance
    "arxiv_source_unfetched": "p1-spec §1 (cite => fetch)",
    "provenance_cache_missing": "p1-spec §1",
    "provenance_hash_mismatch": "p1-spec §1",
    "provenance_id_mismatch": "p1-spec §1",
    # P3 change constitution
    "undocumented_status_change": "p3-spec §0 (no silent changes)",
    # Amendment #6: DOI sources have an endpoint too (Crossref)
    "doi_source_unfetched": "amendment-6 (cite => fetch)",
    "doi_cache_missing": "amendment-6",
    "doi_hash_mismatch": "amendment-6",
    "doi_id_mismatch": "amendment-6",
}


@dataclass
class Violation:
    claim_id: str
    rule: str
    detail: str

    def __str__(self) -> str:
        law = LAWS.get(self.rule, "UNREGISTERED LAW")
        return f"[{self.claim_id}] {self.rule} (law: {law}): {self.detail}"


def _scan_text(fields: List[tuple]) -> List[tuple]:
    """Return (rule, label, offending_text) for every field tripping a text
    rule. Fields whose label starts with "evidence:" are sourced restatements:
    bare percentages are allowed there (Amendment #1), declared-confidence
    vocabulary is not."""
    hits = []
    for label, text in fields:
        if not text:
            continue
        if _CONFIDENCE_RE.search(text):
            hits.append(("declared_confidence", label, text))
        elif _PERCENT_RE.search(text) and not label.startswith("evidence:"):
            hits.append(("no_fake_precision", label, text))
        if _COUNT_RE.search(text):
            hits.append(("no_numeric_open_questions", label, text))
    return hits


def validate_claim(claim: Claim) -> List[Violation]:
    v: List[Violation] = []

    # --- status must be a real cell -------------------------------------
    if not isinstance(claim.status, Status):
        v.append(Violation(claim.id, "invalid_status",
                            f"status is not a Status enum: {claim.status!r}"))
        return v  # everything below depends on a real status

    spec = STATUS_CONDITIONS[claim.status]
    allowed = set(spec["conditions"])

    # --- evidence types must come from the controlled vocabulary --------
    # (P1.5: the evidence axis is derived mechanically from these types;
    #  free-text types would make that derivation sand.)
    from .axes import EVIDENCE_TYPE_VOCAB
    for ev in claim.evidence:
        if ev.type not in EVIDENCE_TYPE_VOCAB:
            v.append(Violation(
                claim.id, "invalid_evidence_type",
                f"evidence type {ev.type!r} is not in the controlled "
                f"vocabulary {sorted(EVIDENCE_TYPE_VOCAB)}"))

    # --- every source must classify into a credibility tier (Amend. #3) --
    for src in claim.sources:
        if tier_of(src.kind) is None:
            v.append(Violation(
                claim.id, "unclassifiable_source_kind",
                f"source {src.label!r} kind {src.kind!r} matches no "
                f"credibility tier {sorted(SOURCE_TIERS)}"))

    # --- every "known" claim must hang on a real source -----------------
    source_labels = {s.label for s in claim.sources}
    for ev in claim.evidence:
        if not (ev.source_ref and ev.source_ref.strip()):
            v.append(Violation(claim.id, "evidence_without_source",
                               f"evidence {ev.description!r} has empty source_ref"))
        elif ev.source_ref not in source_labels:
            v.append(Violation(
                claim.id, "dangling_source_ref",
                f"evidence source_ref {ev.source_ref!r} does not match any "
                f"source label on this claim"))
    if not claim.evidence:
        v.append(Violation(
            claim.id, "unsupported_claim",
            "a claim with no evidence must be demoted to AI Narrative and "
            "marked as unsupported"))

    # --- no fabricated precision, no numeric open_questions -------------
    text_fields = [("title", claim.title)]
    for ev in claim.evidence:
        text_fields.append((f"evidence:{ev.type}", ev.description))
    for cm in claim.competing_models:
        text_fields += [
            (f"competing:{cm.name}:supporting", cm.supporting),
            (f"competing:{cm.name}:opposing", cm.opposing),
            (f"competing:{cm.name}:limitations", cm.limitations),
        ]
    for i, oq in enumerate(claim.open_questions):
        text_fields.append((f"open_question[{i}]", oq))
    for ca in claim.status_reason:
        text_fields.append((f"status_reason:{ca.condition}", ca.note))
    for rule, label, text in _scan_text(text_fields):
        v.append(Violation(claim.id, rule, f"{label}: {text!r}"))

    # --- open_questions must be a real expandable list ------------------
    for i, oq in enumerate(claim.open_questions):
        if not isinstance(oq, str) or not oq.strip():
            v.append(Violation(claim.id, "empty_open_question",
                               f"open_questions[{i}] is empty"))
        elif oq.strip().isdigit():
            v.append(Violation(
                claim.id, "numeric_open_question",
                f"open_questions[{i}]={oq!r} is a number, not a question"))

    # --- status_reason must map onto the claimed status's conditions ----
    seen = {}
    for ca in claim.status_reason:
        if ca.condition not in allowed:
            v.append(Violation(
                claim.id, "foreign_condition",
                f"status_reason cites {ca.condition!r}, which is not an entry "
                f"condition of {claim.status.name}"))
            continue
        if not (ca.note and ca.note.strip()):
            v.append(Violation(
                claim.id, "unjustified_condition",
                f"condition {ca.condition!r} has no note (not traceable)"))
        seen[ca.condition] = ca.holds

    holding = {c for c, h in seen.items() if h}
    if spec["mode"] == "all":
        missing = allowed - set(seen)
        if missing:
            v.append(Violation(
                claim.id, "status_reason_incomplete",
                f"{claim.status.name} requires ALL conditions; missing: "
                f"{sorted(missing)}"))
        not_holding = {c for c, h in seen.items() if not h}
        if not_holding:
            v.append(Violation(
                claim.id, "condition_not_satisfied",
                f"{claim.status.name} requires ALL conditions to hold, but "
                f"these do not: {sorted(not_holding)}"))
    else:  # "any"
        if not holding:
            v.append(Violation(
                claim.id, "no_condition_satisfied",
                f"{claim.status.name} needs at least one holding condition; "
                f"none of {sorted(seen)} hold"))

    # --- competing_models is bound to the COMPETING light ---------------
    if claim.status == Status.COMPETING:
        if len(claim.competing_models) < 2:
            v.append(Violation(
                claim.id, "competing_needs_models",
                "status is Competing Models but fewer than two competing "
                "models are listed"))
    elif claim.competing_models:
        v.append(Violation(
            claim.id, "unexpected_competing_models",
            f"competing_models is only for status Competing, but status is "
            f"{claim.status.name}"))

    return v


def validate_topic(topic: Topic) -> List[Violation]:
    violations: List[Violation] = []
    for claim in topic.claims:
        violations.extend(validate_claim(claim))
    return violations


def format_report(topic: Topic, violations: List[Violation]) -> str:
    lines = [f"Constitution check: topic {topic.id!r} "
             f"({len(topic.claims)} claims)"]
    if not violations:
        lines.append("  PASS — zero violations.")
    else:
        lines.append(f"  FAIL — {len(violations)} violation(s):")
        for viol in violations:
            lines.append(f"    - {viol}")
    return "\n".join(lines)
