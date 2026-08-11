"""Challenge form — submit challenges from the web UI.

Generates a static HTML form for submitting challenges to claims.
Local-first JSON draft + explicit links into GitHub issue templates
(same templates as app.html claim cards).

Usage:
    python -m universe_explorer.reader.challenge_form --claim hawking_radiation
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set

from ..model import Claim, Topic

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"
_CHALLENGES_DIR = Path(__file__).parent.parent.parent / "challenges"

VALID_TYPES = frozenset({"verdict", "relation", "source"})

# GitHub issue templates (same targets as web/app.html claim cards).
_GH_BASE = "https://github.com/taipei49314/universe-explorer/issues/new"
_GH_TEMPLATES = {
    "verdict": f"{_GH_BASE}?template=challenge-a-verdict.yml",
    "relation": f"{_GH_BASE}?template=challenge-a-relation.yml",
    "source": f"{_GH_BASE}?template=report-a-source-problem.yml",
}


class ChallengeError(ValueError):
    """Contract violation for a challenge submission."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def _known_claim_ids(topics: Optional[Sequence[Topic]] = None) -> Set[str]:
    if topics is None:
        from ..data.registry import TOPICS
        topics = TOPICS
    return {c.id for t in topics for c in t.claims}


def generate_challenge_form(
    dist_dir: Path = _DIST_DIR,
    topics: Optional[Sequence[Topic]] = None,
) -> Path:
    """Generate dist/challenge.html — form + GitHub template routes."""
    known = sorted(_known_claim_ids(topics))
    known_js = json.dumps(known, ensure_ascii=False)
    html_content = _CHALLENGE_TEMPLATE.replace(
        "__KNOWN_CLAIM_IDS__", known_js
    )
    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = dist_dir / "challenge.html"
    out_path.write_text(html_content, encoding="utf-8")
    print(f"[challenge] form -> {out_path}")
    return out_path


def submit_challenge(
    claim_id: str,
    challenge_type: str,     # "verdict" | "relation" | "source"
    argument: str,
    proposed_change: str = "",
    evidence_refs: list = None,
    topics: Optional[Sequence[Topic]] = None,
    require_known_claim: bool = True,
) -> dict:
    """Validate and save a challenge to disk. Returns the challenge dict.

    Contract:
      - claim_id must be non-empty; when require_known_claim, must exist
      - type must be verdict | relation | source
      - argument required
      - verdict/source challenges need at least one checkable evidence_ref
        (arXiv id or DOI-like token). A challenge without a checkable source
        is itself an unsupported claim.
    """
    claim_id = (claim_id or "").strip()
    if not claim_id:
        raise ChallengeError("claim_id is required")

    challenge_type = (challenge_type or "").strip().lower()
    if challenge_type not in VALID_TYPES:
        raise ChallengeError(
            f"invalid type: {challenge_type!r} "
            f"(expected one of {sorted(VALID_TYPES)})"
        )

    argument = (argument or "").strip()
    if not argument:
        raise ChallengeError("argument is required")

    if require_known_claim:
        known = _known_claim_ids(topics)
        if claim_id not in known:
            raise ChallengeError(
                f"unknown claim_id: {claim_id!r} "
                "(use an id from claims.json / app-data.json)"
            )

    refs = [
        r.strip() for r in (evidence_refs or [])
        if isinstance(r, str) and r.strip()
    ]
    if challenge_type in ("verdict", "source") and not refs:
        raise ChallengeError(
            f"{challenge_type} challenge requires at least one evidence_ref "
            "(arXiv id or DOI). A challenge without a checkable source is "
            "itself an unsupported claim."
        )
    for ref in refs:
        if not _looks_checkable(ref):
            raise ChallengeError(
                f"evidence_ref {ref!r} does not look like arXiv/DOI/checkable "
                "source (examples: 1602.03837, 10.1038/nature…, arXiv:1602.03837)"
            )

    _CHALLENGES_DIR.mkdir(parents=True, exist_ok=True)
    challenge = {
        "claim_id": claim_id,
        "type": challenge_type,
        "argument": argument,
        "proposed_change": (proposed_change or "").strip(),
        "evidence_refs": refs,
        "submitted_at": dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "status": "pending",
        "github_template": _GH_TEMPLATES.get(challenge_type, _GH_BASE),
    }
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Sanitize filename: claim ids are [a-z0-9_]; reject path segments.
    safe_id = re.sub(r"[^a-zA-Z0-9_-]+", "_", claim_id)[:80]
    out_path = _CHALLENGES_DIR / f"{stamp}-{safe_id}.json"
    out_path.write_text(
        json.dumps(challenge, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[challenge] {challenge_type} for {claim_id} -> {out_path}")
    return challenge


def _looks_checkable(ref: str) -> bool:
    """Loose check: arXiv id, DOI, or labeled source with either."""
    s = ref.strip()
    if not s or len(s) < 5:
        return False
    low = s.lower()
    if "arxiv" in low:
        return True
    # bare arXiv: YYMM.NNNNN or older archive/NNNNNNN
    if re.search(r"\b\d{4}\.\d{4,5}(v\d+)?\b", s):
        return True
    if re.search(r"\b(astro-ph|hep-th|gr-qc|cond-mat)/\d{7}\b", low):
        return True
    # DOI
    if re.search(r"\b10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+\b", s):
        return True
    if low.startswith("doi:"):
        return True
    return False


_CHALLENGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Challenge a Verdict — Universe Explorer</title>
<style>
  :root {
    --bg: #fafafa; --card: #fff; --border: #e0e0e0; --text: #212121;
    --muted: #757575; --accent: #1565c0; --error: #c62828;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: system-ui, sans-serif; background: var(--bg);
         color: var(--text); padding: 2rem; max-width: 640px; margin: 0 auto; }
  h1 { margin-bottom: .5rem; font-size: 1.5rem; }
  p.intro { color: var(--muted); margin-bottom: 1.5rem; font-size: .95rem; }
  .form-group { margin-bottom: 1rem; }
  label { display: block; font-weight: 500; margin-bottom: .25rem; }
  label .req { color: var(--error); }
  input, textarea, select {
    width: 100%; padding: .5rem; border: 1px solid var(--border);
    border-radius: 4px; font-size: .95rem; font-family: inherit;
  }
  textarea { min-height: 120px; resize: vertical; }
  .help { font-size: .8rem; color: var(--muted); margin-top: .25rem; }
  button { background: var(--accent); color: #fff; border: none; padding: .6rem 1.5rem;
           border-radius: 4px; font-size: 1rem; cursor: pointer; }
  button:hover { opacity: .9; }
  .result { margin-top: 1rem; padding: 1rem; border-radius: 4px; display: none; }
  .result.success { background: #e8f5e9; display: block; }
  .result.error { background: #ffebee; display: block; color: #b71c1c; }
  nav { margin-bottom: 1.5rem; }
  nav a { margin-right: 1rem; color: var(--accent); text-decoration: none; }
  .gh-links { margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid var(--border); }
  .gh-links a { display: inline-block; margin: .25rem .75rem .25rem 0; color: var(--accent); }
</style>
</head>
<body>
<nav>
  <a href="index.html">Index</a>
  <a href="app.html">Map</a>
  <a href="explore.html">Explore</a>
  <a href="claims.json">claims.json</a>
</nav>
<h1>Challenge a Verdict</h1>
<p class="intro">
  The whole point of this system is that verdicts can be overturned.
  Read the claim's <code>status_reason</code> against the entry conditions,
  recompute the evidence axis, and make your argument with a <strong>checkable</strong>
  source (arXiv / DOI). This static form prepares a JSON draft and routes you into
  the matching GitHub issue template — same templates as claim cards on the map.
</p>

<form id="challenge-form">
  <div class="form-group">
    <label>Claim ID <span class="req">*</span></label>
    <input name="claim_id" required placeholder="e.g. hawking_radiation" autocomplete="off">
    <div class="help">Must match an id in claims.json (validated in-browser against the shipped list).</div>
  </div>

  <div class="form-group">
    <label>Challenge Type <span class="req">*</span></label>
    <select name="type" required>
      <option value="verdict">Verdict — wrong light or wrong condition</option>
      <option value="relation">Relation — wrong or missing edge</option>
      <option value="source">Source — fetch / hash / mis-cite problem</option>
    </select>
  </div>

  <div class="form-group">
    <label>Argument <span class="req">*</span></label>
    <textarea name="argument" required
      placeholder="Cite the entry conditions from model.py STATUS_CONDITIONS and explain why the current light is wrong. Reference specific evidence items."></textarea>
    <div class="help">A challenge without a checkable source is itself an unsupported claim.</div>
  </div>

  <div class="form-group">
    <label>Proposed Change</label>
    <textarea name="proposed_change"
      placeholder="What should change? e.g. 'Move to COMPETING because...'"></textarea>
  </div>

  <div class="form-group">
    <label>Evidence References <span class="req" id="refs-req">*</span></label>
    <input name="evidence_refs"
      placeholder="arXiv IDs or DOIs, comma-separated (e.g. 1602.03837, 10.1038/…)">
    <div class="help">Required for verdict and source challenges. Optional for relation-only edges.</div>
  </div>

  <button type="submit">Prepare challenge</button>
</form>

<div class="result" id="result"></div>

<div class="gh-links">
  <strong>Or open a GitHub issue template directly:</strong><br>
  <a id="gh-verdict" href="https://github.com/taipei49314/universe-explorer/issues/new?template=challenge-a-verdict.yml">Challenge a verdict</a>
  <a id="gh-relation" href="https://github.com/taipei49314/universe-explorer/issues/new?template=challenge-a-relation.yml">Challenge a relation</a>
  <a id="gh-source" href="https://github.com/taipei49314/universe-explorer/issues/new?template=report-a-source-problem.yml">Report a source problem</a>
</div>

<script>
const KNOWN_CLAIM_IDS = new Set(__KNOWN_CLAIM_IDS__);
const GH = {
  verdict: "https://github.com/taipei49314/universe-explorer/issues/new?template=challenge-a-verdict.yml",
  relation: "https://github.com/taipei49314/universe-explorer/issues/new?template=challenge-a-relation.yml",
  source: "https://github.com/taipei49314/universe-explorer/issues/new?template=report-a-source-problem.yml",
};

function looksCheckable(ref) {
  const s = (ref || "").trim();
  if (s.length < 5) return false;
  const low = s.toLowerCase();
  if (low.includes("arxiv")) return true;
  if (/\\b\\d{4}\\.\\d{4,5}(v\\d+)?\\b/.test(s)) return true;
  if (/\\b10\\.\\d{4,9}\\/[-._;()/:a-zA-Z0-9]+/.test(s)) return true;
  if (low.startsWith("doi:")) return true;
  return false;
}

document.getElementById('challenge-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const fd = new FormData(this);
  const claim_id = (fd.get('claim_id') || '').trim();
  const type = (fd.get('type') || '').trim();
  const argument = (fd.get('argument') || '').trim();
  const proposed_change = (fd.get('proposed_change') || '').trim();
  const evidence_refs = (fd.get('evidence_refs') || '')
    .split(',').map(s => s.trim()).filter(Boolean);

  const result = document.getElementById('result');
  function fail(msg) {
    result.className = 'result error';
    result.style.display = 'block';
    result.textContent = msg;
  }

  if (!claim_id) return fail('claim_id is required');
  if (KNOWN_CLAIM_IDS.size && !KNOWN_CLAIM_IDS.has(claim_id)) {
    return fail('Unknown claim_id: ' + claim_id + ' (must match claims.json)');
  }
  if (!argument) return fail('argument is required');
  if ((type === 'verdict' || type === 'source') && evidence_refs.length === 0) {
    return fail(type + ' challenge requires at least one checkable evidence_ref (arXiv/DOI).');
  }
  for (const ref of evidence_refs) {
    if (!looksCheckable(ref)) {
      return fail('evidence_ref does not look checkable: ' + ref);
    }
  }

  const data = {
    claim_id, type, argument, proposed_change, evidence_refs,
    status: 'pending',
  };
  const title = encodeURIComponent('[challenge] ' + claim_id);
  const body = encodeURIComponent(
    '## Challenge draft (from challenge.html)\\n\\n```json\\n' +
    JSON.stringify(data, null, 2) + '\\n```\\n'
  );
  const ghUrl = (GH[type] || GH.verdict) + '&title=' + title + '&body=' + body;

  result.className = 'result success';
  result.style.display = 'block';
  result.innerHTML = '<strong>Challenge draft ready:</strong><pre>' +
    JSON.stringify(data, null, 2) + '</pre>' +
    '<div style="margin-top:.75rem">' +
    '<a href="' + ghUrl + '" target="_blank" rel="noopener">Open GitHub issue template with this draft →</a>' +
    '</div>' +
    '<div style="margin-top:.5rem;font-size:.85rem;color:#616161">' +
    'Static site cannot write challenges/ for you. Prefer the GitHub route, ' +
    'or save the JSON locally under challenges/ if you are a maintainer.</div>';
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    generate_challenge_form()
