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

from .model import (  # Topic: provenance wrap
    STATUS_CONDITIONS,
    Claim,
    ReviewState,
    Status,
    Topic,
)

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
    # Amendment #7: endpoint honesty + record hygiene
    "primary_source_not_fetchable": "amendment-7",
    "empty_title": "amendment-7",
    "duplicate_source_label": "amendment-7",
    # Amendment #8: consensus light may not float above the evidence axis
    "consensus_floor_established": "amendment-8",
    "consensus_floor_strong": "amendment-8",
    # Amendment #10: round-3 critical closures
    "evidence_type_requires_primary_fetchable": "amendment-10",
    "competing_needs_distinct_papers": "amendment-10",
    "status_reason_vacuous_note": "amendment-10",
    "trace_refs_missing": "amendment-10",
    "trace_refs_unknown": "amendment-10",
    "trace_refs_insufficient": "amendment-10",
    "frontier_needs_fetchable_source": "amendment-10",
    "title_hidden_controls": "amendment-10",
    # Amendment #11: editorial review markers
    "invalid_review_state": "amendment-11",
    "verified_without_attribution": "amendment-11",
    # Amendment #12: anti-forgery + review surface honesty
    "verified_by_invalid": "amendment-12",
    "verified_note_vacuous": "amendment-12",
    "verified_at_invalid": "amendment-12",
}

# Vacuous consensus notes (amendment-10 / C6; expanded amendment-12 / R4-9).
_VACUOUS_NOTES = frozenset({
    "i say so", "because", "n", "x", "yes", "y", "ok", "true", "holds",
    "todo", "...", "tbd", "tba", "fixme", "placeholder", "none", "na", "n/a",
    "because sources", "supported by literature", "yes it holds",
    "see paper", "see above", "as above", "well known", "known fact",
    "obviously", "clearly true", "it holds", "holds true",
    "literature supports", "per literature", "standard result",
    "see sources", "see the paper", "per sources", "as stated",
    "confirmed", "validated", "lgtm", "looks good", "seems fine",
})

# Amendment #12: human_verified cannot be stamped with a throwaway identity.
_VERIFIED_BY_BLOCKLIST = frozenset({
    "x", "bot", "attacker", "admin", "test", "todo", "tbd", "none", "na", "n/a",
    "me", "user", "editor", "human", "yes", "ok", "lgtm", "foo", "bar", "asdf",
    "anonymous", "anon", "system", "ci", "github", "root", "null", "undefined",
    "someone", "reviewer", "maintainer", "owner", "aaa", "abc", "xxx",
})
_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
_GITHUB_HANDLE_RE = re.compile(
    r"^(?:github:|@)([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)$"
)
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _valid_verified_by(raw: str) -> bool:
    """True when verified_by looks like a real editor identity (amendment-12)."""
    s = (raw or "").strip()
    if len(s) < 4:
        return False
    low = s.lower()
    if low in _VERIFIED_BY_BLOCKLIST:
        return False
    if _EMAIL_RE.match(s):
        # Bare throwaway tokens as *local* part only (editor@… is a real pattern).
        local = s.split("@", 1)[0].lower()
        if local in {
            "bot", "test", "admin", "attacker", "none", "null", "fake",
            "noreply", "no-reply", "root", "ci", "system",
        }:
            return False
        return True
    gh = _GITHUB_HANDLE_RE.match(s)
    if gh:
        return gh.group(1).lower() not in _VERIFIED_BY_BLOCKLIST
    # Bare display name: need a letter (or CJK), length ≥ 6, not blocklisted.
    if not re.search(r"[A-Za-z\u4e00-\u9fff]", s):
        return False
    if len(s) < 6:
        return False
    return low not in _VERIFIED_BY_BLOCKLIST

# Zero-width / bidi / BOM — title cosmetics that break search/dedup (C8-adjacent).
_HIDDEN_TITLE_CHARS = frozenset(
    [0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0x00AD, 0xFEFF]
    + list(range(0x202A, 0x2030))
    + list(range(0x2066, 0x206A))
)


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


def validate_claim(
    claim: Claim,
    *,
    check_provenance: bool = False,
    manifest_path=None,
    crossref_manifest_path=None,
) -> List[Violation]:
    """Constitution check for one claim (shape / axes / floors).

    Amendment #10 / C4: cite⇒fetch is enforced on the **topic** court
    (``validate_topic`` / ``build.py``), which always runs provenance once.
    Pass ``check_provenance=True`` to also pin fetch rules on a single claim
    (e.g. unit tests and draft previews).
    """
    v: List[Violation] = []

    # --- status must be a real cell -------------------------------------
    if not isinstance(claim.status, Status):
        v.append(Violation(claim.id, "invalid_status",
                            f"status is not a Status enum: {claim.status!r}"))
        return v  # everything below depends on a real status

    spec = STATUS_CONDITIONS[claim.status]
    allowed = set(spec["conditions"])

    # --- Amendment #7: title must be real text --------------------------
    if not (claim.title and claim.title.strip()):
        v.append(Violation(
            claim.id, "empty_title",
            "claim title is empty or whitespace-only"))
    # Amendment #10 / zero-width & bidi controls in titles
    elif any(ord(ch) in _HIDDEN_TITLE_CHARS for ch in claim.title):
        v.append(Violation(
            claim.id, "title_hidden_controls",
            "claim title contains hidden/control characters "
            "(zero-width, bidi, or BOM)"))

    # --- Amendment #11/#12: editorial review_state + anti-forgery ----------
    rs = getattr(claim, "review_state", ReviewState.UNVERIFIED)
    if not isinstance(rs, ReviewState):
        v.append(Violation(
            claim.id, "invalid_review_state",
            f"review_state must be a ReviewState enum, got {rs!r}"))
    elif rs is ReviewState.HUMAN_VERIFIED:
        who = (getattr(claim, "verified_by", None) or "").strip()
        note = (getattr(claim, "verified_note", None) or "").strip()
        when = (getattr(claim, "verified_at", None) or "").strip()
        if not who:
            v.append(Violation(
                claim.id, "verified_without_attribution",
                "review_state is human_verified but verified_by is empty"))
        elif not _valid_verified_by(who):
            v.append(Violation(
                claim.id, "verified_by_invalid",
                f"verified_by {who!r} is not a usable editor identity "
                f"(use email, @github-handle, github:handle, or a real "
                f"display name ≥6 chars — not a throwaway token)"))
        if len(note) < 12:
            v.append(Violation(
                claim.id, "verified_note_vacuous",
                "human_verified requires verified_note ≥12 characters "
                "describing what was checked"))
        if not _ISO_DATE_RE.match(when):
            v.append(Violation(
                claim.id, "verified_at_invalid",
                "human_verified requires verified_at as ISO date YYYY-MM-DD"))

    # --- evidence types must come from the controlled vocabulary --------
    # (P1.5: the evidence axis is derived mechanically from these types;
    #  free-text types would make that derivation sand.)
    from .axes import ANALOG, DIRECT, EVIDENCE_TYPE_VOCAB
    from .provenance import is_fetchable_endpoint, paper_id_of
    for ev in claim.evidence:
        if ev.type not in EVIDENCE_TYPE_VOCAB:
            v.append(Violation(
                claim.id, "invalid_evidence_type",
                f"evidence type {ev.type!r} is not in the controlled "
                f"vocabulary {sorted(EVIDENCE_TYPE_VOCAB)}"))

    # --- every source must classify into a credibility tier (Amend. #3) --
    # Amendment #7: PRIMARY must carry a fetchable endpoint (arXiv or DOI).
    seen_labels: set[str] = set()
    source_by_label: dict = {}
    for src in claim.sources:
        if src.label in seen_labels:
            v.append(Violation(
                claim.id, "duplicate_source_label",
                f"source label {src.label!r} appears more than once on this claim"))
        seen_labels.add(src.label)
        source_by_label[src.label] = src
        tier = tier_of(src.kind)
        if tier is None:
            v.append(Violation(
                claim.id, "unclassifiable_source_kind",
                f"source {src.label!r} kind {src.kind!r} matches no "
                f"credibility tier {sorted(SOURCE_TIERS)}"))
        elif tier == "PRIMARY" and not is_fetchable_endpoint(src.url_or_id):
            v.append(Violation(
                claim.id, "primary_source_not_fetchable",
                f"source {src.label!r} is PRIMARY but url_or_id "
                f"{src.url_or_id!r} is not a fetchable arXiv or DOI endpoint "
                f"(amendment-7: PRIMARY is not a kind-string costume)"))

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
        # Amendment #10 / C3,C9: direct & analog only on PRIMARY+fetchable.
        elif ev.type in (DIRECT, ANALOG):
            src = source_by_label.get(ev.source_ref)
            if src is not None:
                if tier_of(src.kind) != "PRIMARY" or not is_fetchable_endpoint(
                    src.url_or_id
                ):
                    v.append(Violation(
                        claim.id, "evidence_type_requires_primary_fetchable",
                        f"{ev.type!r} on source {ev.source_ref!r} requires a "
                        f"PRIMARY fetchable (arXiv/DOI) source — not "
                        f"{src.kind!r} / {src.url_or_id!r}"))
    if not claim.evidence:
        v.append(Violation(
            claim.id, "unsupported_claim",
            "a claim with no evidence must be demoted to AI Narrative and "
            "marked as unsupported"))

    # --- Amendment #10 / C5: Competing needs two distinct papers ----------
    if claim.status is Status.COMPETING:
        paper_ids = {
            paper_id_of(s.url_or_id)
            for s in claim.sources
            if paper_id_of(s.url_or_id) is not None
        }
        if len(paper_ids) < 2:
            v.append(Violation(
                claim.id, "competing_needs_distinct_papers",
                "status is Competing Models but fewer than two distinct "
                "fetchable papers (arXiv/DOI ids) are cited — camp names alone "
                "are not enough (amendment-10)"))

    # --- Amendment #10 / C8: Frontier needs a fetchable endpoint ----------
    if claim.status is Status.FRONTIER:
        if not any(is_fetchable_endpoint(s.url_or_id) for s in claim.sources):
            v.append(Violation(
                claim.id, "frontier_needs_fetchable_source",
                "status is Frontier Research but no source has a fetchable "
                "arXiv/DOI endpoint (amendment-10)"))

    # --- Amendment #10 / C6: high-light notes and explicit trace_refs -------
    if claim.status in (Status.ESTABLISHED, Status.STRONG):
        for ca in claim.status_reason:
            if not ca.holds:
                continue
            note = (ca.note or "").strip()
            if len(note) < 12 or note.lower() in _VACUOUS_NOTES:
                v.append(Violation(
                    claim.id, "status_reason_vacuous_note",
                    f"condition {ca.condition!r} has a vacuous note {note!r} "
                    f"— high lights require a non-trivial justification "
                    f"(amendment-10)"))
        refs = list(getattr(claim, "trace_refs", None) or [])
        if not refs:
            v.append(Violation(
                claim.id, "trace_refs_missing",
                f"{claim.status.name} requires trace_refs (explicit source "
                f"labels the light is anchored on; amendment-10)"))
        else:
            unknown = [r for r in refs if r not in source_labels]
            if unknown:
                v.append(Violation(
                    claim.id, "trace_refs_unknown",
                    f"trace_refs not on this claim's sources: {unknown}"))
            need = 2 if claim.status is Status.ESTABLISHED else 1
            if len(set(refs)) < need:
                v.append(Violation(
                    claim.id, "trace_refs_insufficient",
                    f"{claim.status.name} needs ≥{need} distinct trace_refs, "
                    f"got {sorted(set(refs))}"))

    # --- Amendment #8: consensus light may not float above the evidence axis
    # Established requires E1 (mechanical twin of multiple independent directs).
    # Strong forbids pure theory / empty evidence (E4/E5); E3 divergence stays legal.
    from .axes import EvidenceStrength, derive
    if claim.evidence:
        axis = derive(claim).strength
        if claim.status is Status.ESTABLISHED and axis is not EvidenceStrength.E1_MULTIPLE_DIRECT:
            v.append(Violation(
                claim.id, "consensus_floor_established",
                f"status is Established but evidence axis is {axis.short} "
                f"({axis.value}); amendment-8 requires E1 (two direct "
                f"observations on distinct fetchable PRIMARY sources)"))
        if claim.status is Status.STRONG and axis in (
            EvidenceStrength.E4_THEORETICAL,
            EvidenceStrength.E5_NONE,
        ):
            v.append(Violation(
                claim.id, "consensus_floor_strong",
                f"status is Strong but evidence axis is {axis.short} "
                f"({axis.value}); amendment-8 forbids E4/E5 under Strong "
                f"(E1–E3 allowed, including Strong×E3 divergence)"))

    # --- Amendment #10 / C4: cite⇒fetch is part of the default court --------
    if check_provenance:
        from .provenance import (
            CROSSREF_MANIFEST_PATH,
            MANIFEST_PATH,
            validate_provenance,
        )
        topic = Topic(
            id=f"_claim_{claim.id}",
            title="",
            summary="",
            claims=[claim],
        )
        v.extend(
            validate_provenance(
                topic,
                manifest_path if manifest_path is not None else MANIFEST_PATH,
                crossref_manifest_path
                if crossref_manifest_path is not None
                else CROSSREF_MANIFEST_PATH,
            )
        )

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
    """Full court for a topic: shape rules + cite⇒fetch (amendment-10 / C4)."""
    violations: List[Violation] = []
    for claim in topic.claims:
        # Shape first without per-claim provenance to avoid N× manifest reloads;
        # one topic-level provenance pass covers all sources.
        violations.extend(validate_claim(claim, check_provenance=False))
    from .provenance import validate_provenance
    violations.extend(validate_provenance(topic))
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
