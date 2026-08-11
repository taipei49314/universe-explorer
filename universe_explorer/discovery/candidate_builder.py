"""Candidate builder — turn adapter results into structured candidate claims.

The builder does NOT assign a status light. It assembles the skeleton:
  - Sources (from adapter fetch)
  - Evidence items (from adapter extract_evidence)
  - Open questions (empty — humans fill these)

The candidate is written to candidates/<topic_id>/<claim_id>.json
with a constitution precheck report attached.

Usage:
    python -m universe_explorer.discovery.candidate_builder \
        --topic cosmology --claim new_claim_id arXiv:2311.08680
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Dict, List, Optional

from .adapters.base import EvidenceItem, FetchedRecord, SourceAdapter

CANDIDATES_DIR = Path(__file__).parent.parent.parent / "candidates" / "structured"


def build_candidate(
    topic_id: str,
    claim_id: str,
    adapter: SourceAdapter,
    source_refs: List[str],
    title: str = "",
    human_context: str = "",
) -> dict:
    """Build a structured candidate claim from source refs.

    Steps:
      1. adapter.fetch() each source_ref → FetchedRecord
      2. adapter.extract_evidence() each record → EvidenceItem list
      3. Assemble candidate dict (no status — that's for humans)
      4. Write to candidates/structured/<topic_id>/<claim_id>.json

    Returns the candidate dict.
    """
    sources = []
    evidence_items = []
    fetch_errors = []

    for ref in source_refs:
        try:
            record = adapter.fetch(ref)
        except (FileNotFoundError, Exception) as exc:
            fetch_errors.append({"source_ref": ref, "error": str(exc)})
            continue

        # Source entry (matches model.Source shape).
        sources.append({
            "label": _make_label(ref),
            "url_or_id": ref,
            "kind": _infer_kind(record),
        })

        # Evidence items from this source.
        items = adapter.extract_evidence(record)
        for item in items:
            evidence_items.append({
                "type": item.type,
                "description": item.description,
                "source_ref": _make_label(ref),
            })

    # Assemble candidate (matches model.Claim shape, minus status).
    candidate = {
        "id": claim_id,
        "topic_id": topic_id,
        "title": title or f"[DRAFT] {claim_id}",
        "status": None,  # human decides
        "status_reason": [],  # human fills after choosing status
        "evidence": evidence_items,
        "competing_models": [],
        "open_questions": [],
        "sources": sources,
        "status_history": [],
        # Discovery metadata (not part of model.Claim).
        "_discovery": {
            "adapter": adapter.name,
            "built_at": dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"),
            "source_refs": source_refs,
            "fetch_errors": fetch_errors,
            "human_context": human_context,
        },
    }

    # Write to disk.
    out_dir = CANDIDATES_DIR / topic_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{claim_id}.json"
    out_path.write_text(
        json.dumps(candidate, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[candidate] {len(sources)} sources, {len(evidence_items)} evidence "
          f"items -> {out_path}")
    if fetch_errors:
        print(f"[candidate] {len(fetch_errors)} fetch error(s): "
              f"{[e['source_ref'] for e in fetch_errors]}")
    return candidate


def load_candidate(topic_id: str, claim_id: str) -> Optional[dict]:
    """Load a structured candidate from disk."""
    path = CANDIDATES_DIR / topic_id / f"{claim_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_candidates(topic_id: Optional[str] = None) -> List[dict]:
    """List all structured candidates, optionally filtered by topic."""
    if not CANDIDATES_DIR.exists():
        return []
    results = []
    dirs = [CANDIDATES_DIR / topic_id] if topic_id else CANDIDATES_DIR.iterdir()
    for d in dirs:
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.json")):
            results.append(json.loads(f.read_text(encoding="utf-8")))
    return results


def _make_label(source_ref: str) -> str:
    """Turn a source_ref into a Source.label.
    e.g. 'arXiv:2311.08680' → 'arXiv-2311-08680'
         'doi:10.1038/xyz' → 'doi-10-1038-xyz'"""
    return (source_ref
            .replace(":", "-")
            .replace("/", "-")
            .replace(".", "-"))


def _infer_kind(record: FetchedRecord) -> str:
    """Infer source kind from the adapter name and record metadata."""
    if "arXiv" in record.source_ref:
        return "preprint (arXiv)"
    if record.source_ref.lower().startswith("doi:"):
        container = record.raw_metadata.get("container", "")
        if container:
            return f"peer-reviewed paper ({container})"
        return "peer-reviewed paper"
    if record.source_ref.lower().startswith("openalex:"):
        # No DOI path — treat as external archive until a human upgrades the kind.
        return "dataset (OpenAlex work record)"
    return "external source"
