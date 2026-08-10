"""Shared source scanner — find sources cited across multiple domains.

Scans every claim's sources. When the same arXiv id or DOI appears in
claims from different topics, that's a cross-domain connection — mechanical,
not invented.

Usage:
    python -m universe_explorer.crossdomain.shared_source
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set

from ..model import Topic
from ..provenance import arxiv_id_of, doi_of


@dataclass
class SharedSource:
    """A source cited by claims in multiple domains."""

    source_ref: str              # the raw url_or_id
    normalized_id: str           # arXiv id or DOI
    claims: List[dict] = field(default_factory=list)  # {id, domain, evidence_types}
    domains: Set[str] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            "source_ref": self.source_ref,
            "normalized_id": self.normalized_id,
            "claims": self.claims,
            "domains": sorted(self.domains),
            "domain_count": len(self.domains),
        }


def scan_shared_sources(topics: List[Topic]) -> List[SharedSource]:
    """Find all sources cited across multiple domains.

    Returns a list of SharedSource, one per cross-domain source.
    """
    # Build index: normalized_id → list of (claim_id, domain, evidence_types)
    index: Dict[str, List[dict]] = {}
    ref_map: Dict[str, str] = {}  # normalized_id → original source_ref

    for topic in topics:
        for claim in topic.claims:
            for src in claim.sources:
                nid = _normalize(src.url_or_id)
                if nid is None:
                    continue
                if nid not in index:
                    index[nid] = []
                    ref_map[nid] = src.url_or_id
                ev_types = [ev.type for ev in claim.evidence
                            if ev.source_ref == src.label]
                index[nid].append({
                    "claim_id": claim.id,
                    "domain": topic.id,
                    "evidence_types": ev_types,
                })

    # Filter to cross-domain only.
    shared = []
    for nid, entries in sorted(index.items()):
        domains = {e["domain"] for e in entries}
        if len(domains) > 1:
            shared.append(SharedSource(
                source_ref=ref_map[nid],
                normalized_id=nid,
                claims=entries,
                domains=domains,
            ))

    return shared


def _normalize(url_or_id: str) -> str | None:
    """Normalize a source reference to a canonical id."""
    arxiv = arxiv_id_of(url_or_id)
    if arxiv:
        return f"arXiv:{arxiv}"
    doi = doi_of(url_or_id)
    if doi:
        return f"doi:{doi}"
    return None  # non-fetchable sources (textbooks, prizes) — honest exemption


def format_shared_sources_report(sources: List[SharedSource]) -> str:
    """Human-readable report."""
    if not sources:
        return "No cross-domain shared sources found."
    lines = [f"Cross-domain shared sources: {len(sources)}"]
    for s in sources:
        lines.append(f"  {s.normalized_id} ({len(s.domains)} domains: "
                     f"{', '.join(sorted(s.domains))})")
        for c in s.claims:
            lines.append(f"    - {c['claim_id']} ({c['domain']})")
    return "\n".join(lines)


if __name__ == "__main__":
    from ..data.registry import TOPICS
    sources = scan_shared_sources(TOPICS)
    print(format_shared_sources_report(sources))
