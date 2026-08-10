"""SourceAdapter ABC — the contract every source must honour.

A source adapter does three things:
  1. search(query) → RawResult list (discovery)
  2. fetch(source_ref) → FetchedRecord (cite ⇒ fetch, verbatim cache)
  3. extract_evidence(record) → EvidenceItem list (structure the raw bytes)

The adapter is a courier, not a judge: it moves bytes and structures them.
It never assigns status lights, evidence strength, or confidence.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class RawResult:
    """One search hit, verbatim from the API. No rewriting."""

    source_ref: str          # e.g. "arXiv:2311.08680" or "doi:10.1038/..."
    title: str
    published: str           # ISO date or empty
    authors: List[str] = field(default_factory=list)
    summary: str = ""        # abstract / description
    extra: Dict[str, str] = field(default_factory=dict)  # source-specific fields


@dataclass(frozen=True)
class FetchedRecord:
    """Verbatim cached bytes + metadata. Provenance-proof."""

    source_ref: str
    cache_path: str          # local file holding the verbatim response
    sha256: str
    endpoint: str            # the URL that was fetched
    retrieved_at: str        # ISO timestamp
    title: str = ""
    authors: List[str] = field(default_factory=list)
    published: str = ""
    raw_metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceItem:
    """One structured evidence item, ready to become a model.Evidence.

    The adapter extracts these from the fetched record. The pipeline
    turns them into Evidence objects with the correct source_ref.
    """

    type: str               # must be in EVIDENCE_TYPE_VOCAB
    description: str         # restates the record; no invented numbers
    source_ref: str          # matches the Source.label


class SourceAdapter(ABC):
    """Plugin interface. Subclass and implement all three methods."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier: 'arxiv', 'doi', 'nasa', 'esa'."""

    @property
    @abstractmethod
    def source_ref_prefix(self) -> str:
        """Prefix for source_ref: 'arXiv:', 'doi:', etc."""

    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> List[RawResult]:
        """Search the source. Returns verbatim results, no rewriting."""

    @abstractmethod
    def fetch(self, source_ref: str) -> FetchedRecord:
        """Fetch and cache one record. Respects rate limits.
        Raises FileNotFoundError if the source_ref is unresolvable."""

    @abstractmethod
    def extract_evidence(self, record: FetchedRecord) -> List[EvidenceItem]:
        """Turn a fetched record into structured evidence items.
        Returns one item per 'finding' the record contains."""

    def can_handle(self, source_ref: str) -> bool:
        """Check if this adapter handles a given source_ref."""
        return source_ref.startswith(self.source_ref_prefix)
