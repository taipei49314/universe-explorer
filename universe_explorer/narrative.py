"""R6 — the AI Narrative layer: organise, never proclaim.

The last of the four layers, deliberately left empty until the three below it
were proven. Constitution rule 2 made mechanical:

  * every sentence must carry refs resolving to this claim's sources or
    status_reason conditions — a sentence with no refs is unconstitutional
    and kills the whole narrative for that claim (rather absent than overreaching);
  * the opening formula ("Based on the evidence recorded here" / its localized
    constitutional equivalent) is mandated phrasing, not style;
  * composer and checker are separate on purpose: today's composer is a
    mechanical assembler; a future LLM composer must pass the *same* check().

Amendment #2 (docs/amendment-2-narrative-i18n.md): language is a presentation
property; the gate is a structural property. A Localization seam lets any
language's narrative through the SAME court — the engine knows the protocol,
never any particular language. Chinese (or any) localizations live in the data
layer. Calls without a localization behave exactly as before the amendment.

The narrative layer only reads from the layers above it and never writes back.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .axes import Derivation, derive, diverges
from .model import Claim

OPENING = "Based on the evidence recorded here"


@dataclass
class NarrativeSentence:
    text: str
    refs: List[str]  # source labels and/or "condition:<key>" markers


class Localization:
    """The seam. Sentence templates + evidence-text access for one language.
    Subclass and override; identifiers (refs, claim ids, E1-E5 codes) are
    never localized — they are traceability anchors, not prose."""

    opening = OPENING

    # -- text accessors (what counts as "the recorded text" in this language)
    def claim_title(self, claim: Claim) -> str:
        return claim.title

    def evidence_text(self, claim: Claim, i: int) -> str:
        return claim.evidence[i].description

    def evidence_type(self, claim: Claim, i: int) -> str:
        return claim.evidence[i].type

    def status_name(self, claim: Claim) -> str:
        return claim.status.value

    def axis_name(self, d: Derivation) -> str:
        return d.strength.value

    def competing_name(self, claim: Claim, i: int) -> str:
        return claim.competing_models[i].name

    # -- sentence templates
    def s_opening(self, claim: Claim) -> str:
        return (f"{self.opening}, the claim “{self.claim_title(claim)}” "
                f"currently carries the light {claim.status.light} "
                f"{self.status_name(claim)}.")

    def s_evidence(self, claim: Claim, i: int) -> str:
        return (f"Recorded as {self.evidence_type(claim, i)}: "
                f"{self.evidence_text(claim, i)}")

    def s_axis(self, claim: Claim, d: Derivation) -> str:
        return (f"Mechanically derived from these records, the evidence axis "
                f"stands at {d.strength.short} ({self.axis_name(d)}).")

    def s_diverge(self, claim: Claim) -> str:
        return ("Note: the consensus light and the evidence axis point apart "
                "here — strong community consensus resting on non-direct "
                "evidence.")

    def s_competing(self, claim: Claim) -> str:
        names = " versus ".join(
            self.competing_name(claim, i)
            for i in range(len(claim.competing_models)))
        return f"The recorded competing models are: {names}."

    def s_open_questions(self, claim: Claim) -> str:
        return ("Open questions remain recorded on this claim; expand the "
                "list below and count them yourself.")


ENGLISH = Localization()


def compose(claim: Claim, loc: Localization = ENGLISH) -> List[NarrativeSentence]:
    """Mechanical assembly. Every sentence is built FROM a recorded field and
    carries that field's provenance. Nothing here knows anything the claim
    does not already record."""
    out: List[NarrativeSentence] = []

    ev_refs = sorted({e.source_ref for e in claim.evidence})
    cond_refs = [f"condition:{ca.condition}" for ca in claim.status_reason]

    out.append(NarrativeSentence(loc.s_opening(claim), refs=ev_refs + cond_refs))

    for i, ev in enumerate(claim.evidence):
        out.append(NarrativeSentence(loc.s_evidence(claim, i),
                                     refs=[ev.source_ref]))

    d = derive(claim)
    out.append(NarrativeSentence(loc.s_axis(claim, d), refs=ev_refs))

    if diverges(claim):
        out.append(NarrativeSentence(loc.s_diverge(claim),
                                     refs=ev_refs + cond_refs))

    if claim.competing_models:
        out.append(NarrativeSentence(loc.s_competing(claim), refs=ev_refs))

    if claim.open_questions:
        out.append(NarrativeSentence(loc.s_open_questions(claim), refs=ev_refs))

    return out


class NarrativeViolation(Exception):
    pass


def check(claim: Claim, sentences: List[NarrativeSentence],
          loc: Localization = ENGLISH) -> None:
    """Independent gate. Does not trust compose() — a future LLM composer (in
    any language) runs through exactly this. Raises on the first breach."""
    from .validator import _CONFIDENCE_RE, _PERCENT_RE  # same law, same court

    if not sentences:
        raise NarrativeViolation(f"{claim.id}: empty narrative")
    if not sentences[0].text.startswith(loc.opening):
        raise NarrativeViolation(
            f"{claim.id}: narrative must open with the constitutional formula "
            f"{loc.opening!r}")

    valid_refs = {s.label for s in claim.sources}
    valid_refs |= {f"condition:{ca.condition}" for ca in claim.status_reason}
    evidence_texts = [loc.evidence_text(claim, i)
                      for i in range(len(claim.evidence))]

    for i, s in enumerate(sentences):
        if not s.refs:
            raise NarrativeViolation(
                f"{claim.id}: sentence {i} carries no refs — an unreferenced "
                f"sentence is a proclamation, not an organisation")
        for r in s.refs:
            if r not in valid_refs:
                raise NarrativeViolation(
                    f"{claim.id}: sentence {i} ref {r!r} does not resolve to a "
                    f"source or status_reason condition of this claim")
        if _CONFIDENCE_RE.search(s.text):
            raise NarrativeViolation(
                f"{claim.id}: sentence {i} declares confidence as a number")
        if _PERCENT_RE.search(s.text):
            # A % is only allowed if the sentence quotes a recorded evidence
            # description (in this localization) verbatim.
            if not any(txt in s.text for txt in evidence_texts):
                raise NarrativeViolation(
                    f"{claim.id}: sentence {i} contains a percentage that is "
                    f"not a verbatim quote of a recorded evidence description")


def narrate(claim: Claim, loc: Localization = ENGLISH) -> List[NarrativeSentence]:
    """Compose then gate. On any violation the narrative is withheld entirely —
    rather absent than overreaching. The build never fails over a narrative."""
    sentences = compose(claim, loc)
    try:
        check(claim, sentences, loc)
    except NarrativeViolation:
        return []
    return sentences
