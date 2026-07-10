"""P1 Data-layer constitution: "cite it => you must have fetched it".

v0's validator polices the Evidence/Knowledge layers; this module polices the
Data layer. Any claim source that points at arXiv must resolve to a real fetch:
a verbatim local cache of the official API response, hash-checked against the
manifest, and re-parsed here to confirm it actually contains the cited id.

Deliberately mechanical and low-trust:

  * the manifest's own say-so is not enough — `provenance_id_mismatch` re-parses
    the cached XML itself, so a manifest pointing at the wrong file is caught;
  * a cache file edited after the fact fails `provenance_hash_mismatch`;
  * non-arXiv sources (textbooks, print journals, prize citations) are honestly
    exempt: they have no fetchable endpoint. The rule splits on "does an
    endpoint exist", never on convenience.

Kept separate from validator.py so the frozen v0 checks stay pure; build.py
gates on both.
"""

from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional

from .model import Topic
from .validator import Violation

# Matches "arXiv:1906.11238" and old-style "arXiv:hep-th/9306069".
ARXIV_REF_RE = re.compile(r"^arXiv:\s*([a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})$",
                          re.IGNORECASE)

# Amendment #6: DOI sources have an endpoint too (Crossref), so the honest
# exemption shrinks. Matches "doi:10.xxxx/anything".
DOI_REF_RE = re.compile(r"^doi:\s*(10\.\d{4,9}/\S+)$", re.IGNORECASE)

CACHE_DIR = Path(__file__).parent.parent / "cache" / "arxiv"
MANIFEST_PATH = CACHE_DIR / "manifest.json"

CROSSREF_CACHE_DIR = Path(__file__).parent.parent / "cache" / "crossref"
CROSSREF_MANIFEST_PATH = CROSSREF_CACHE_DIR / "manifest.json"

_ATOM = "{http://www.w3.org/2005/Atom}"


def arxiv_id_of(url_or_id: str) -> Optional[str]:
    """Return the bare arXiv id if this source reference is an arXiv one."""
    m = ARXIV_REF_RE.match(url_or_id.strip())
    return m.group(1) if m else None


def doi_of(url_or_id: str) -> Optional[str]:
    """Return the normalized (lowercase — DOIs are case-insensitive) DOI if
    this source reference is a DOI one."""
    m = DOI_REF_RE.match(url_or_id.strip())
    return m.group(1).lower() if m else None


def load_manifest(manifest_path: Path = MANIFEST_PATH) -> dict:
    if not manifest_path.exists():
        return {}
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cached_xml_contains_id(xml_path: Path, arxiv_id: str) -> bool:
    """Independent re-check: parse the cached Atom feed and confirm one of its
    entries really is the cited paper. Does not trust the manifest."""
    try:
        root = ET.fromstring(xml_path.read_text(encoding="utf-8"))
    except ET.ParseError:
        return False
    for entry in root.findall(f"{_ATOM}entry"):
        id_el = entry.find(f"{_ATOM}id")
        if id_el is None or not id_el.text:
            continue
        # entry id looks like http://arxiv.org/abs/1207.3123v2 — strip version.
        entry_id = id_el.text.rsplit("/abs/", 1)[-1]
        entry_id = re.sub(r"v\d+$", "", entry_id)
        if entry_id == arxiv_id:
            return True
    return False


def cached_json_contains_doi(json_path: Path, doi: str) -> bool:
    """Independent re-check for Crossref caches (Amendment #6): parse the
    cached response and confirm it really is the cited work. Does not trust
    the manifest."""
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False
    got = str(payload.get("message", {}).get("DOI", "")).lower()
    return got == doi.lower()


def _check_doi_sources(claim, violations: List[Violation],
                       crossref_manifest_path: Path) -> None:
    """Amendment #6: the same four rules as arXiv, for doi: sources."""
    manifest = load_manifest(crossref_manifest_path)
    cache_root = crossref_manifest_path.parent

    for src in claim.sources:
        doi = doi_of(src.url_or_id)
        if doi is None:
            continue  # not a DOI source

        rec = manifest.get(doi)
        if rec is None:
            violations.append(Violation(
                claim.id, "doi_source_unfetched",
                f"source {src.label!r} cites doi:{doi} but no fetch record "
                f"exists — cite it => fetch it first"))
            continue

        cache_file = cache_root / rec["cache_file"]
        if not cache_file.exists():
            violations.append(Violation(
                claim.id, "doi_cache_missing",
                f"manifest for doi:{doi} points at missing cache file "
                f"{rec['cache_file']!r}"))
            continue

        actual = sha256_of(cache_file)
        if actual != rec["sha256"]:
            violations.append(Violation(
                claim.id, "doi_hash_mismatch",
                f"cache for doi:{doi} was modified after fetch "
                f"(sha256 {actual[:12]}… != recorded {rec['sha256'][:12]}…)"))
            continue

        if not cached_json_contains_doi(cache_file, doi):
            violations.append(Violation(
                claim.id, "doi_id_mismatch",
                f"cached response for doi:{doi} does not actually contain "
                f"that work — manifest self-report rejected"))


def validate_provenance(
    topic: Topic,
    manifest_path: Path = MANIFEST_PATH,
    crossref_manifest_path: Path = CROSSREF_MANIFEST_PATH,
) -> List[Violation]:
    """P1 rules (arXiv) + Amendment #6 rules (DOI). Returns violations in the
    same shape as the v0 validator so build.py can gate on both lists at once."""
    violations: List[Violation] = []
    manifest = load_manifest(manifest_path)
    cache_root = manifest_path.parent

    for claim in topic.claims:
        _check_doi_sources(claim, violations, crossref_manifest_path)
        for src in claim.sources:
            arxiv_id = arxiv_id_of(src.url_or_id)
            if arxiv_id is None:
                continue  # not arXiv (DOI handled above; else honestly exempt)

            rec = manifest.get(arxiv_id)
            if rec is None:
                violations.append(Violation(
                    claim.id, "arxiv_source_unfetched",
                    f"source {src.label!r} cites arXiv:{arxiv_id} but no fetch "
                    f"record exists — cite it => fetch it first"))
                continue

            cache_file = cache_root / rec["cache_file"]
            if not cache_file.exists():
                violations.append(Violation(
                    claim.id, "provenance_cache_missing",
                    f"manifest for arXiv:{arxiv_id} points at missing cache "
                    f"file {rec['cache_file']!r}"))
                continue

            actual = sha256_of(cache_file)
            if actual != rec["sha256"]:
                violations.append(Violation(
                    claim.id, "provenance_hash_mismatch",
                    f"cache for arXiv:{arxiv_id} was modified after fetch "
                    f"(sha256 {actual[:12]}… != recorded {rec['sha256'][:12]}…)"))
                continue

            if not cached_xml_contains_id(cache_file, arxiv_id):
                violations.append(Violation(
                    claim.id, "provenance_id_mismatch",
                    f"cached response for arXiv:{arxiv_id} does not actually "
                    f"contain that paper — manifest self-report rejected"))

    return violations
