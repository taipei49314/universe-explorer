"""T4 — the claim drafting pipeline: every court in the system, then a human.

A local LLM drafts a NEW claim skeleton from human-chosen, verbatim-fetched
arXiv sources. Before any human reviews it, the draft must clear every
existing gate: the v0 constitution, the controlled evidence vocabulary,
cite=>fetch provenance, the derived evidence axis, the P2 compatible set
(the suggested light must sit inside it — machine-condition notes are filled
from the derivation, never by the LLM), and the narrative court. Only a draft
that passes them all is written to drafts/ (physically separate from data/),
stamped UNVERIFIED, with the full court report attached.

The human's remaining job is the one machines cannot do: verify the content
is FAITHFUL to the sources — legality was already guaranteed mechanically.
The human then writes the Python into data/ themselves, where every gate runs
again.

Usage:
    python -m universe_explorer.dataops.claim_draft <topic_id> <new_claim_id> \
        <arxiv_id> [<arxiv_id> ...]
"""

from __future__ import annotations

import datetime as dt
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List

from ..axes import EVIDENCE_TYPE_VOCAB, derive
from ..model import (
    STATUS_CONDITIONS,
    Claim,
    ConditionAssessment,
    Evidence,
    Source,
    Status,
    Topic,
)
from ..narrative import check as narrative_check, compose
from ..proposals import MACHINE_CONDITIONS, propose
from ..provenance import CACHE_DIR, MANIFEST_PATH, validate_provenance
from ..validator import validate_claim

OLLAMA = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5vl:7b"
DRAFTS_DIR = Path(__file__).parent.parent.parent / "drafts"
_ATOM = "{http://www.w3.org/2005/Atom}"


class DraftRejected(Exception):
    pass


# --------------------------------------------------------------------------- #
# 1. sources: human-chosen ids, fetched through the existing pipeline          #
# --------------------------------------------------------------------------- #

def fetch_and_read_sources(arxiv_ids: List[str]) -> List[Dict[str, str]]:
    """Ensure every id is fetched (cite=>fetch), then read title + abstract
    verbatim from the local cache — the only text the LLM will ever see."""
    from .arxiv_fetch import fetch_ids

    manifest = (json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
                if MANIFEST_PATH.exists() else {})
    missing = [a for a in arxiv_ids if a not in manifest]
    if missing:
        fetch_ids(missing)
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    out = []
    for a in arxiv_ids:
        rec = manifest.get(a)
        if rec is None:
            raise DraftRejected(f"arXiv:{a} could not be fetched — no source, "
                                f"no draft")
        xml_path = CACHE_DIR / rec["cache_file"]
        root = ET.fromstring(xml_path.read_text(encoding="utf-8"))
        entry = root.find(f"{_ATOM}entry")
        out.append({
            "arxiv_id": a,
            "label": "arXiv-" + a.replace("/", "-").replace(".", "-"),
            "title": entry.findtext(f"{_ATOM}title", default="").strip(),
            "abstract": entry.findtext(f"{_ATOM}summary", default="").strip(),
        })
    return out


# --------------------------------------------------------------------------- #
# 2. the drafting prompt: verbatim metadata only                               #
# --------------------------------------------------------------------------- #

def build_prompt(claim_id: str, sources: List[Dict[str, str]],
                 target_status: str = "") -> str:
    src_block = json.dumps(
        [{"label": s["label"], "title": s["title"], "abstract": s["abstract"]}
         for s in sources], ensure_ascii=False, indent=1)
    human_conds = {
        st.name: [c for c in spec["conditions"] if c not in MACHINE_CONDITIONS]
        for st, spec in STATUS_CONDITIONS.items()
    }
    return (
        "You draft a scientific-claim skeleton for HUMAN review. You may only "
        "restate what the fetched records below contain — nothing else exists.\n"
        f"FETCHED SOURCES (verbatim official metadata):\n{src_block}\n\n"
        f"CLAIM ID: {claim_id}\n"
        f"EVIDENCE TYPES (controlled vocabulary): {sorted(EVIDENCE_TYPE_VOCAB)}\n"
        f"STATUSES and their HUMAN-judgement conditions you may draft notes "
        f"for: {json.dumps(human_conds)}\n\n"
        "Rules:\n"
        "1. One evidence item per source, description restating its abstract; "
        "source_ref must equal the source's label exactly.\n"
        "2. No invented numbers; a percentage only if it appears verbatim in "
        "the abstract you are restating.\n"
        + ("3. suggested_status MUST be exactly "
           f"{target_status!r} (chosen by the human operator). Draft a note "
           "for EVERY human condition listed above for that status — the "
           "note may honestly say a condition does NOT hold (holds: false); "
           "missing a note gets the whole draft rejected. (Notes will be "
           "stamped UNVERIFIED.)\n"
           if target_status else
           "3. suggested_status: pick the most defensible status NAME "
           "(ESTABLISHED/STRONG/COMPETING/FRONTIER/SPECULATIVE). Then draft a "
           "note for EVERY human condition listed above for that status — "
           "missing even one gets the whole draft rejected. (Notes will be "
           "stamped UNVERIFIED.)\n")
        + "4. open_questions: questions the abstracts themselves leave open.\n"
        'Answer ONLY JSON: {"title": "...", "suggested_status": "...", '
        '"evidence": [{"type": "...", "description": "...", "source_ref": '
        '"..."}], "human_condition_notes": {"<condition>": {"holds": true, '
        '"note": "..."}}, "open_questions": ["..."]}\n'
    )


def call_model(prompt: str, model: str = DEFAULT_MODEL,
               timeout: int = 300) -> str:
    req = urllib.request.Request(
        f"{OLLAMA}/api/chat",
        data=json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 1400},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())["message"]["content"]


# --------------------------------------------------------------------------- #
# 3. every court in the system                                                 #
# --------------------------------------------------------------------------- #

def parse_json_object(raw: str) -> Dict:
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise DraftRejected("model output contains no JSON object")
    return json.loads(m.group(0))


def normalize_notes(d: Dict) -> None:
    """Models sometimes return human_condition_notes as a list of
    {condition, holds, note} — normalize to the dict form in place."""
    notes = d.get("human_condition_notes")
    if isinstance(notes, list):
        d["human_condition_notes"] = {
            str(n.get("condition")): {"holds": n.get("holds"),
                                      "note": n.get("note", "")}
            for n in notes if isinstance(n, dict)}


def missing_human_conditions(d: Dict) -> List[str]:
    """For an all-mode suggested status: which human conditions lack notes."""
    try:
        status = Status[str(d.get("suggested_status", ""))]
    except KeyError:
        return []
    spec = STATUS_CONDITIONS[status]
    if spec["mode"] != "all":
        return []
    notes = d.get("human_condition_notes", {})
    return [c for c in spec["conditions"]
            if c not in MACHINE_CONDITIONS and c not in notes]


def assemble_and_gate(claim_id: str, raw: str,
                      sources: List[Dict[str, str]]) -> Dict:
    """Parse the model's draft, assemble a real Claim, and run EVERY gate.
    Raises DraftRejected on the first breach. Returns the draft + court report."""
    d = parse_json_object(raw)

    try:
        status = Status[str(d.get("suggested_status", ""))]
    except KeyError:
        raise DraftRejected(
            f"suggested_status {d.get('suggested_status')!r} is not a status")

    claim = Claim(
        id=claim_id,
        title=str(d.get("title", "")).strip(),
        status=status,
        sources=[Source(s["label"], f"arXiv:{s['arxiv_id']}",
                        "peer-reviewed paper (arXiv record; venue to be "
                        "confirmed by human review)")
                 for s in sources],
        evidence=[Evidence(str(e.get("type", "")), str(e.get("description", "")),
                           str(e.get("source_ref", "")))
                  for e in d.get("evidence", [])],
        open_questions=[str(q) for q in d.get("open_questions", [])],
    )

    # status_reason: machine conditions filled FROM THE DERIVATION (never the
    # LLM); human conditions from the LLM, stamped UNVERIFIED.
    derivation = derive(claim)
    spec = STATUS_CONDITIONS[status]
    notes = d.get("human_condition_notes", {})
    for cond in spec["conditions"]:
        if cond in MACHINE_CONDITIONS:
            from ..proposals import _judge_machine
            sig = _judge_machine(cond, claim)
            claim.status_reason.append(ConditionAssessment(
                cond, bool(sig.holds), f"[machine] {sig.rationale}"))
        else:
            n = notes.get(cond)
            if n is None:
                if spec["mode"] == "all":
                    raise DraftRejected(
                        f"{status.name} requires ALL conditions; the draft "
                        f"has no note for human condition {cond!r}")
                continue
            claim.status_reason.append(ConditionAssessment(
                cond, bool(n.get("holds")),
                f"UNVERIFIED (LLM draft): {str(n.get('note', '')).strip()}"))

    # Court 1: the v0 constitution + vocabulary + tiers
    violations = validate_claim(claim)
    if violations:
        raise DraftRejected("constitution: " + "; ".join(map(str, violations)))

    # Court 2: cite=>fetch provenance (wrap in a throwaway topic)
    prov = validate_provenance(Topic("draft", "draft", "draft", [claim]))
    if prov:
        raise DraftRejected("provenance: " + "; ".join(map(str, prov)))

    # Court 3: the suggested light must sit inside the mechanical compatible set
    proposal = propose(claim)
    if status not in proposal.compatible_statuses:
        raise DraftRejected(
            f"suggested status {status.name} is OUTSIDE the mechanically "
            f"compatible set "
            f"{[s.name for s in proposal.compatible_statuses]}")

    # Court 4: the narrative court
    narrative_check(claim, compose(claim))

    return {
        "verified": "UNVERIFIED",
        "drafted_at": dt.datetime.now(dt.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claim": {
            "id": claim.id, "title": claim.title, "status": status.name,
            "status_reason": [{"condition": c.condition, "holds": c.holds,
                               "note": c.note} for c in claim.status_reason],
            "evidence": [{"type": e.type, "description": e.description,
                          "source_ref": e.source_ref} for e in claim.evidence],
            "open_questions": claim.open_questions,
            "sources": [{"label": s.label, "url_or_id": s.url_or_id,
                         "kind": s.kind} for s in claim.sources],
        },
        "court_report": {
            "constitution": "zero violations",
            "provenance": "all sources fetched and verified",
            "evidence_axis": f"{derivation.strength.short} "
                             f"({derivation.strength.value})",
            "axis_derivation": derivation.reasoning,
            "compatible_statuses": [s.name for s in proposal.compatible_statuses],
            "narrative_court": "passed",
        },
        "human_todo": [
            "verify every evidence description is FAITHFUL to its source",
            "verify the venue/peer-review state of each source (kind field)",
            "verify UNVERIFIED condition notes against real references",
            "then write the claim into data/<topic>.py yourself — all gates "
            "run again there",
        ],
    }


def main(argv: List[str]) -> int:
    target_status = ""
    if "--status" in argv:
        i = argv.index("--status")
        target_status = Status[argv[i + 1]].name  # validate the name
        argv = argv[:i] + argv[i + 2:]
    if len(argv) < 3:
        print("usage: python -m universe_explorer.dataops.claim_draft "
              "<topic_id> <new_claim_id> <arxiv_id> [...] "
              "[--status FRONTIER]")
        return 2
    topic_id, claim_id, ids = argv[0], argv[1], argv[2:]

    sources = fetch_and_read_sources(ids)
    try:
        raw = call_model(build_prompt(claim_id, sources, target_status))
        # completion loop (engineering, not law): a small model often misses a
        # human-condition note; ask ONCE for exactly the missing ones, merge,
        # then face the unchanged courts.
        d = parse_json_object(raw)
        normalize_notes(d)
        for _round in range(3):
            missing = missing_human_conditions(d)
            if not missing:
                break
            spec = STATUS_CONDITIONS[Status[d["suggested_status"]]]["conditions"]
            follow = (
                f"Your draft suggested {d['suggested_status']} but is missing "
                f"notes for these human conditions:\n"
                + "\n".join(f"- {c}: {spec[c]}" for c in missing)
                + '\nAnswer ONLY JSON: {"human_condition_notes": '
                  '{"' + missing[0] + '": {"holds": true, "note": "..."}}} '
                  "covering exactly these conditions (use the exact keys). "
                  "No percentages, no confidence-as-number phrasing."
            )
            extra = parse_json_object(call_model(follow))
            normalize_notes(extra)
            d.setdefault("human_condition_notes", {}).update(
                extra.get("human_condition_notes", {}))
        draft = assemble_and_gate(claim_id, json.dumps(d), sources)
    except DraftRejected as exc:
        print(f"DRAFT REJECTED (nothing written): {exc}")
        return 1
    except Exception as exc:
        print(f"model unavailable or malformed output ({exc}) — no draft")
        return 1

    draft["topic"] = topic_id
    DRAFTS_DIR.mkdir(exist_ok=True)
    out = DRAFTS_DIR / f"{claim_id}.json"
    out.write_text(json.dumps(draft, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"draft passed every court -> {out}")
    print(json.dumps(draft["court_report"], indent=2, ensure_ascii=False))
    print("\nUNVERIFIED: a human must now verify faithfulness to the sources "
          "and write the claim into data/ themselves.")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
