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

# Bare arXiv ids (new-style 1906.11238 or old-style hep-th/9306069).
_ARXIV_ID = r"(?:[a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})"
# Matches "arXiv:1906.11238" and old-style "arXiv:hep-th/9306069".
ARXIV_REF_RE = re.compile(rf"^arXiv:\s*({_ARXIV_ID})(?:v\d+)?$", re.IGNORECASE)
# Amendment #7: URL shapes that are the same endpoint.
# Host may be arxiv.org or export.arxiv.org (same abs ids).
ARXIV_URL_RE = re.compile(
    rf"(?:https?://)?(?:export\.)?(?:www\.)?arxiv\.org/(?:abs|pdf|html)/({_ARXIV_ID})(?:v\d+)?(?:\.pdf)?/?(?:\?.*)?$",
    re.IGNORECASE,
)

# Amendment #6: DOI sources have an endpoint too (Crossref).
# Amendment #7: also doi.org URLs and bare 10.xxxx/... strings.
DOI_REF_RE = re.compile(r"^doi:\s*(10\.\d{4,9}/\S+)$", re.IGNORECASE)
DOI_URL_RE = re.compile(
    r"(?:https?://)?(?:dx\.)?doi\.org/(10\.\d{4,9}/\S+)$",
    re.IGNORECASE,
)
# Bare DOI: whole string is a DOI (no spaces). Trailing punctuation stripped.
BARE_DOI_RE = re.compile(r"^(10\.\d{4,9}/\S+)$", re.IGNORECASE)

CACHE_DIR = Path(__file__).parent.parent / "cache" / "arxiv"
MANIFEST_PATH = CACHE_DIR / "manifest.json"

CROSSREF_CACHE_DIR = Path(__file__).parent.parent / "cache" / "crossref"
CROSSREF_MANIFEST_PATH = CROSSREF_CACHE_DIR / "manifest.json"

_ATOM = "{http://www.w3.org/2005/Atom}"


def arxiv_id_of(url_or_id: str) -> Optional[str]:
    """Return the bare arXiv id if this source reference is an arXiv endpoint.

    Amendment #7: accepts ``arXiv:…`` and ``https://arxiv.org/abs|pdf|html/…``
    (with optional version suffix). Does not accept free-text mentions.
    """
    raw = (url_or_id or "").strip()
    if not raw:
        return None
    m = ARXIV_REF_RE.match(raw)
    if m:
        return m.group(1)
    m = ARXIV_URL_RE.match(raw.rstrip("/"))
    if m:
        return m.group(1)
    return None


def doi_of(url_or_id: str) -> Optional[str]:
    """Return the normalized (lowercase) DOI if this reference is a DOI endpoint.

    Amendment #7: ``doi:…``, ``https://doi.org/…``, ``dx.doi.org/…``, or a bare
    ``10.xxxx/…`` string. Bibliographic prose (``Nature 378, 355 (1995)``) is
    not a DOI and stays honestly exempt until rewritten.
    """
    raw = (url_or_id or "").strip().rstrip(").,;")
    if not raw:
        return None
    # Strip URL query/fragment so ``doi.org/10.x/y?locatt=…`` still parses.
    if "://" in raw or raw.lower().startswith("doi.org") or raw.lower().startswith("dx.doi.org"):
        raw = raw.split("?", 1)[0].split("#", 1)[0].rstrip("/")
    m = DOI_REF_RE.match(raw)
    if m:
        return m.group(1).lower()
    m = DOI_URL_RE.match(raw)
    if m:
        return m.group(1).lower()
    m = BARE_DOI_RE.match(raw)
    if m:
        return m.group(1).lower()
    return None


def is_fetchable_endpoint(url_or_id: str) -> bool:
    """True when cite⇒fetch applies (arXiv or DOI after Amendment #7 normalize)."""
    return arxiv_id_of(url_or_id) is not None or doi_of(url_or_id) is not None


_ARXIV_ATOM = "{http://www.w3.org/2005/Atom}"
_ARXIV_NS = "{http://arxiv.org/schemas/atom}"

# arxiv:id ↔ doi:id aliases learned from local arXiv Atom caches (amendment-12).
# Canonical form prefers doi:… when a DOI is known so preprint + journal of the
# same work cannot mint two independent E1 paper ids.
_paper_alias_map: Optional[dict] = None


def _build_paper_alias_map() -> dict:
    """Scan cache/arxiv/*.xml for <arxiv:doi> and map both forms to doi:…"""
    aliases: dict = {}
    if not CACHE_DIR.exists():
        return aliases
    for path in CACHE_DIR.glob("*.xml"):
        try:
            root = ET.fromstring(path.read_text(encoding="utf-8"))
        except (ET.ParseError, OSError, UnicodeDecodeError):
            continue
        for entry in root.findall(f"{_ARXIV_ATOM}entry"):
            id_el = entry.find(f"{_ARXIV_ATOM}id")
            doi_el = entry.find(f"{_ARXIV_NS}doi")
            if id_el is None or not id_el.text or doi_el is None or not doi_el.text:
                continue
            entry_id = id_el.text.rsplit("/abs/", 1)[-1]
            entry_id = re.sub(r"v\d+$", "", entry_id).lower()
            did = doi_of(f"doi:{doi_el.text.strip()}") or doi_of(doi_el.text.strip())
            if not entry_id or not did:
                continue
            canon = f"doi:{did}"
            aliases[f"arxiv:{entry_id}"] = canon
            aliases[canon] = canon
    return aliases


def reload_paper_aliases() -> None:
    """Drop the cached alias map (tests may call after writing fixtures)."""
    global _paper_alias_map
    _paper_alias_map = None


def paper_id_of(url_or_id: str) -> Optional[str]:
    """Normalized identity of a fetchable work (Amendment #9 / #12).

    Used so E1 counts *distinct papers*, not distinct source labels:
    ``arXiv:1906.11238`` and ``https://arxiv.org/abs/1906.11238v2`` share one id.
    Amendment #12: when the local arXiv cache records a DOI for that arXiv id,
    both ``arxiv:…`` and ``doi:…`` collapse to the same canonical ``doi:…``.
    Returns ``None`` when the reference is not a fetchable endpoint.
    """
    global _paper_alias_map
    raw: Optional[str] = None
    aid = arxiv_id_of(url_or_id)
    if aid is not None:
        raw = f"arxiv:{aid.lower()}"
    else:
        did = doi_of(url_or_id)
        if did is not None:
            raw = f"doi:{did}"
    if raw is None:
        return None
    if _paper_alias_map is None:
        _paper_alias_map = _build_paper_alias_map()
    return _paper_alias_map.get(raw, raw)


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
