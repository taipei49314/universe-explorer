"""Challenge form — submit challenges from the web UI.

Generates a static HTML form for submitting challenges to claims.
Replaces the GitHub Issue template workflow with a local-first approach.

Usage:
    python -m universe_explorer.reader.challenge_form --claim hawking_radiation
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Optional

from ..model import Claim, Topic

_DIST_DIR = Path(__file__).parent.parent.parent / "dist"
_CHALLENGES_DIR = Path(__file__).parent.parent.parent / "challenges"


def generate_challenge_form(dist_dir: Path = _DIST_DIR) -> Path:
    """Generate dist/challenge.html — a standalone challenge submission form."""
    html_content = _CHALLENGE_TEMPLATE
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
) -> dict:
    """Save a challenge to disk. Returns the challenge dict."""
    _CHALLENGES_DIR.mkdir(parents=True, exist_ok=True)
    challenge = {
        "claim_id": claim_id,
        "type": challenge_type,
        "argument": argument,
        "proposed_change": proposed_change,
        "evidence_refs": evidence_refs or [],
        "submitted_at": dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "status": "pending",
    }
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = _CHALLENGES_DIR / f"{stamp}-{claim_id}.json"
    out_path.write_text(
        json.dumps(challenge, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[challenge] {challenge_type} for {claim_id} -> {out_path}")
    return challenge


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
  .result.error { background: #ffebee; display: block; }
  nav { margin-bottom: 1.5rem; }
  nav a { margin-right: 1rem; color: var(--accent); text-decoration: none; }
</style>
</head>
<body>
<nav>
  <a href="index.html">Index</a>
  <a href="app.html">Map</a>
  <a href="explore.html">Explore</a>
</nav>
<h1>Challenge a Verdict</h1>
<p class="intro">
  The whole point of this system is that verdicts can be overturned.
  Read the claim's <code>status_reason</code> against the entry conditions,
  recompute the evidence axis, and make your argument with a checkable source.
</p>

<form id="challenge-form">
  <div class="form-group">
    <label>Claim ID <span class="req">*</span></label>
    <input name="claim_id" required placeholder="e.g. hawking_radiation">
    <div class="help">Find it in claims.json or on the claim card.</div>
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
    <label>Evidence References</label>
    <input name="evidence_refs"
      placeholder="arXiv IDs or DOIs, comma-separated">
    <div class="help">Sources that support your challenge.</div>
  </div>

  <button type="submit">Submit Challenge</button>
</form>

<div class="result" id="result"></div>

<script>
document.getElementById('challenge-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const fd = new FormData(this);
  const data = {
    claim_id: fd.get('claim_id'),
    type: fd.get('type'),
    argument: fd.get('argument'),
    proposed_change: fd.get('proposed_change'),
    evidence_refs: fd.get('evidence_refs').split(',').map(s => s.trim()).filter(Boolean),
  };
  // Display as JSON (local-first: no server to POST to).
  const result = document.getElementById('result');
  result.className = 'result success';
  result.style.display = 'block';
  result.innerHTML = '<strong>Challenge recorded:</strong><pre>' +
    JSON.stringify(data, null, 2) + '</pre>' +
    '<div style="margin-top:.5rem;font-size:.85rem;color:#616161">' +
    'Copy this JSON and save it to challenges/ or submit as a GitHub Issue.</div>';
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    generate_challenge_form()
