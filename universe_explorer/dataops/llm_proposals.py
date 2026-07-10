"""B2 — a local-LLM drafter locked inside one cell of the P2 governance.

The mechanical engine already split conditions into machine (derived from
evidence) and human (textbook acceptance, real camps, ...). The LLM's ONLY
power here is to draft assessments for `needs_human` conditions — hypotheses
for a human to verify against real sources. It cannot touch machine conditions,
cannot propose a light, and its drafts never enter claim data: they go to
audit/drafts.jsonl, physically separate from the human decision log, every
entry stamped UNVERIFIED.

Same failure posture as B1: model down, malformed output, any breach — the
draft is discarded and only the mechanical proposal remains.

Usage:
    python -m universe_explorer.dataops.llm_proposals <claim_id> <STATUS>
    python -m universe_explorer.dataops.llm_proposals --list
"""

from __future__ import annotations

import datetime as dt
import json
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List

from ..model import STATUS_CONDITIONS, Claim, Status
from ..proposals import AUDIT_DIR, propose

OLLAMA = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5vl:7b"
DRAFTS_LOG = AUDIT_DIR / "drafts.jsonl"


@dataclass
class ConditionDraft:
    condition: str
    suggested_holds: bool
    draft_note: str
    verified: str = "UNVERIFIED"  # constant by design


class DraftViolation(Exception):
    pass


def _human_conditions(claim: Claim, status: Status) -> List[str]:
    assessment = next(a for a in propose(claim).assessments
                      if a.status is status)
    if not assessment.compatible:
        raise DraftViolation(
            f"{status.name} is mechanically excluded for {claim.id} — "
            f"there is nothing for a human (or an LLM) to assess")
    return assessment.needs_human


def build_prompt(claim: Claim, status: Status) -> str:
    conditions = _human_conditions(claim, status)
    spec = STATUS_CONDITIONS[status]["conditions"]
    return (
        "You draft assessment suggestions for a human reviewer of scientific "
        "claims. You may ONLY address the listed human-judgement conditions. "
        "Your notes are hypotheses the human must verify against real "
        "sources — write them as checkable statements, never as verdicts.\n"
        f"CLAIM: {claim.title}\n"
        f"CANDIDATE STATUS: {status.value}\n"
        "CONDITIONS TO DRAFT (address each):\n"
        + "\n".join(f"- {c}: {spec[c]}" for c in conditions)
        + "\n\nRules:\n"
        "1. Only these condition keys, exactly as written.\n"
        "2. No percentages, no confidence-as-number phrasing.\n"
        "3. Each note names WHAT the human should check (which textbooks, "
        "which reviews, which communities).\n"
        'Answer ONLY a JSON array: '
        '[{"condition": "...", "suggested_holds": true, "draft_note": "..."}]\n'
    )


def call_model(prompt: str, model: str = DEFAULT_MODEL,
               timeout: int = 300) -> str:
    req = urllib.request.Request(
        f"{OLLAMA}/api/chat",
        data=json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 900},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())["message"]["content"]


def parse_and_gate(claim: Claim, status: Status, raw: str) -> List[ConditionDraft]:
    """The gate. Raises DraftViolation on any overreach."""
    from ..validator import _CONFIDENCE_RE, _PERCENT_RE  # same text law

    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if not m:
        raise DraftViolation("model output contains no JSON array")
    allowed = set(_human_conditions(claim, status))

    drafts: List[ConditionDraft] = []
    for it in json.loads(m.group(0)):
        cond = str(it.get("condition", ""))
        if cond not in allowed:
            raise DraftViolation(
                f"draft touches {cond!r} — not a human condition of "
                f"{status.name} for this claim (machine conditions and "
                f"foreign keys are out of the LLM's power)")
        note = str(it.get("draft_note", "")).strip()
        if not note:
            raise DraftViolation(f"empty draft note for {cond!r}")
        if _CONFIDENCE_RE.search(note) or _PERCENT_RE.search(note):
            raise DraftViolation(
                f"draft note for {cond!r} declares numeric confidence or a "
                f"bare percentage — same text law as everywhere")
        drafts.append(ConditionDraft(cond, bool(it.get("suggested_holds")),
                                     note))
    if not drafts:
        raise DraftViolation("no drafts produced")
    return drafts


def record_drafts(claim: Claim, status: Status,
                  drafts: List[ConditionDraft], model: str,
                  drafts_log: Path = DRAFTS_LOG) -> dict:
    """Append to the drafts log — physically separate from decisions.jsonl."""
    entry = {
        "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": "llm_condition_drafts",
        "verified": "UNVERIFIED",
        "claim": claim.id,
        "candidate_status": status.name,
        "model": model,
        "drafts": [{"condition": d.condition,
                    "suggested_holds": d.suggested_holds,
                    "draft_note": d.draft_note,
                    "verified": d.verified} for d in drafts],
    }
    drafts_log.parent.mkdir(exist_ok=True)
    with drafts_log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def draft(claim: Claim, status: Status,
          model: str = DEFAULT_MODEL) -> List[ConditionDraft]:
    """Full pipeline. Returns [] on any failure — the mechanical proposal is
    always the floor; drafts are only ever an optional layer on top."""
    try:
        raw = call_model(build_prompt(claim, status), model=model)
        drafts = parse_and_gate(claim, status, raw)
        record_drafts(claim, status, drafts, model)
        return drafts
    except Exception:
        return []


def main(argv: List[str]) -> int:
    from ..data.registry import TOPICS
    claims = {c.id: c for t in TOPICS for c in t.claims}

    if not argv or "--list" in argv:
        print("claims:", ", ".join(claims))
        print("statuses:", ", ".join(s.name for s in Status))
        return 0

    claim = claims[argv[0]]
    status = Status[argv[1]]

    from ..proposals import _print_proposal
    _print_proposal(propose(claim))

    drafts = draft(claim, status)
    if not drafts:
        print("\nno LLM drafts (model unavailable or draft rejected by the "
              "gate) — the mechanical proposal above stands alone")
        return 0

    print(f"\nUNVERIFIED drafts for {status.name} (recorded to {DRAFTS_LOG}; "
          f"a human must verify each against real sources):")
    for d in drafts:
        print(f"  ? {d.condition}: suggested holds={d.suggested_holds}")
        print(f"    {d.draft_note}")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
