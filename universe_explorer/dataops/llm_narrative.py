"""B1 — a local-LLM composer behind the unchanged narrative court.

First live use of the "swap the smart part, never the court" seam: a local
Ollama model drafts narrative sentences, and every sentence faces the exact
same `narrative.check()` as the mechanical composer. On ANY failure — server
down, malformed output, one unconstitutional sentence — the whole draft is
discarded and the mechanical composer takes over. The system can never become
less traceable by adding an LLM; the worst case is exactly what existed before.

The prompt feeds ONLY the claim's recorded fields plus the list of legal refs:
the model cannot cite anything the claim does not already record — the same
constitution the narrative layer itself lives under.

Local only (Ollama at localhost:11434): claim data never leaves the machine.

Usage:
    python -m universe_explorer.dataops.llm_narrative <claim_id> [--zh]
    python -m universe_explorer.dataops.llm_narrative --list
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import List, Optional

from ..model import Claim
from ..narrative import (
    ENGLISH,
    Localization,
    NarrativeSentence,
    NarrativeViolation,
    check,
    compose,
)

OLLAMA = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5vl:7b"


def _legal_refs(claim: Claim) -> List[str]:
    refs = [s.label for s in claim.sources]
    refs += [f"condition:{ca.condition}" for ca in claim.status_reason]
    return refs


def build_prompt(claim: Claim, loc: Localization = ENGLISH) -> str:
    """Only recorded fields + legal refs. Nothing else exists for the model."""
    record = {
        "title": loc.claim_title(claim),
        "status": f"{claim.status.light} {loc.status_name(claim)}",
        "evidence": [
            {"type": loc.evidence_type(claim, i),
             "description": loc.evidence_text(claim, i),
             "source_ref": claim.evidence[i].source_ref}
            for i in range(len(claim.evidence))
        ],
        "status_conditions": [
            {"condition": ca.condition, "holds": ca.holds}
            for ca in claim.status_reason
        ],
        "open_questions": claim.open_questions,
    }
    return (
        "You organise recorded scientific evidence. You never state facts on "
        "your own authority — you only restate what the record below contains.\n"
        f"RECORD:\n{json.dumps(record, ensure_ascii=False, indent=1)}\n\n"
        f"LEGAL REFS (each sentence must cite at least one, exactly as "
        f"written): {json.dumps(_legal_refs(claim), ensure_ascii=False)}\n\n"
        "Write 3-6 sentences summarising the record. Rules:\n"
        f"1. Sentence 1 MUST start exactly with: {loc.opening}\n"
        "2. Every sentence must carry a refs array of legal refs it restates.\n"
        "3. Never invent numbers. A percentage may appear ONLY inside a "
        "verbatim quote of an evidence description.\n"
        "4. Never use confidence-as-number phrasing (e.g. 'confidence: 90').\n"
        'Answer with ONLY a JSON array: [{"text": "...", "refs": ["..."]}]\n'
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


def parse_and_gate(claim: Claim, raw: str,
                   loc: Localization = ENGLISH) -> List[NarrativeSentence]:
    """Parse the model's draft and put it before the SAME court.
    Raises NarrativeViolation / ValueError on any breach."""
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if not m:
        raise ValueError("model output contains no JSON array")
    items = json.loads(m.group(0))
    sentences = [NarrativeSentence(text=str(it["text"]),
                                   refs=[str(r) for r in it.get("refs", [])])
                 for it in items]
    check(claim, sentences, loc)  # the unchanged court
    return sentences


def narrate_llm(claim: Claim, loc: Localization = ENGLISH,
                model: str = DEFAULT_MODEL) -> tuple:
    """Returns (sentences, origin) where origin is 'llm' or 'mechanical'.
    Any failure anywhere -> mechanical fallback, never an error."""
    try:
        raw = call_model(build_prompt(claim, loc), model=model)
        return parse_and_gate(claim, raw, loc), "llm"
    except Exception:
        return compose(claim, loc), "mechanical"


def main(argv: List[str]) -> int:
    from ..data.registry import TOPICS

    claims = {c.id: c for t in TOPICS for c in t.claims}
    if not argv or "--list" in argv:
        print("claims:", ", ".join(claims))
        return 0

    loc: Localization = ENGLISH
    if "--zh" in argv:
        from ..data.translations_zh import ZH_LOC
        loc = ZH_LOC
        argv = [a for a in argv if a != "--zh"]

    claim = claims[argv[0]]
    sentences, origin = narrate_llm(claim, loc)
    print(f"[{origin}] narrative for {claim.id} "
          f"({'passed the court' if origin == 'llm' else 'LLM draft rejected or model unavailable — mechanical fallback'}):\n")
    for s in sentences:
        print(f"  {s.text}")
        print(f"    refs: {s.refs}")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
