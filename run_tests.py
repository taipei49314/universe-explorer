"""One-command gate: all test suites + constitution build check + trust measure.

    python run_tests.py

Exit code 0 = everything green. This is the CI entrypoint.

Important: suites are executed via ``python -m pytest <file>`` so
class-based tests actually run. Bare ``python test_*.py`` that prints
nothing and exits 0 is treated as a **failure** (silent-suite blind spot).
"""

from __future__ import annotations

import re
import subprocess
import sys

SUITES = [
    "test_validator.py",    # v0 constitution + Amendment #1
    "test_provenance.py",   # P1 cite => fetch
    "test_axes.py",         # P1.5 evidence axis
    "test_proposals.py",    # P2 propose-never-decide + audit
    "test_watch.py",        # P3 no silent changes
    "test_p4.py",           # engine freeze + cross-domain
    "test_narrative.py",    # R6 + Amendment #2 localization
    "test_registry.py",     # every gate x every topic
    "test_push.py",         # P5 digest restates, never interprets
    "test_llm_narrative.py",  # B1 the court bites LLM output equally (offline)
    "test_tiers.py",          # C1/Amendment #3 source credibility tiers
    "test_llm_proposals.py",  # B2 the LLM drafter locked in its cell (offline)
    "test_explore.py",        # D2 anchors, explore page, claims.json export
    "test_crossref.py",       # C2/Amendment #6 DOI cite=>fetch rules bite
    "test_feed.py",           # D3 Atom feed restates, never interprets
    "test_health.py",         # T1 source health: report, never re-judge
    "test_claim_draft.py",    # T4 every court bites the drafting pipeline
    "test_constitution.py",   # V4-2 the doc and the code cannot drift
    "test_app.py",            # D4 dynamic frontend: data + self-containment
    "test_ui_expand.py",      # domain expand: measure first, then gate
    "test_trust_behavior.py", # trust surfaces: measure first, then trust
    "test_automation.py",     # automation metrics (must actually execute)
    "test_build_validation.py",  # dist shape + dynamic claim counts
    "test_relations.py",      # claim links + inference paths (no confidence)
    "test_transport.py",      # P5b webhook/SMTP transport (env-gated)
    "test_surface.py",        # P-Read/Shell/Pulse/Audit/Guide surface checks
    "test_challenge_ops.py",  # Trust Loop inventory (challenges/weeklies/candidates)
    "test_canonicals.py",     # v5 S3 three teaching anchors
    "test_inventory_docs.py", # README/milestones list-counts match registry
    "test_discovery.py",      # Discovery Pipeline: adapters, candidate builder
    "test_precheck.py",       # Discovery Pipeline: constitution precheck
    "test_crossdomain.py",    # Cross-domain: shared sources, conflicts, gaps
    "test_reader.py",         # Reader: search, filter, dual-axis, guided reading
    "test_integration.py",    # End-to-end integration tests
    "test_new_modules.py",    # Stats, export, diff, annotate, review, batch
    "test_links.py",          # link / reading-path integrity
    "test_content.py",        # every claim content/provenance/status shape
    "test_security.py",       # XSS / path / injection surface smoke
    "test_benchmarks.py",     # latency budgets (measure, then trust speed)
    "test_adversarial.py",    # adversarial: empty/unicode/cache edges
    "test_adversarial_2.py",  # adversarial: constitutional invariants
    "test_adversarial_3.py",  # adversarial: watch/discovery/cache/reviews
    "test_epistemic_adversary.py",  # amendment-7: red-team PoC must bite
    "test_editorial_openalex.py",  # amendment-11: ledger OS + OpenAlex
    "test_r4_closures.py",    # amendment-12: R4 editorial surface + anti-forgery
    "test_scene3d.py",        # 3D explore/reason scene view-model + path/neighbor nav
    "test_accessibility.py",  # a11y smoke: lang/title/viewport/labels (was disk-only)
]


_PASSED_RE = re.compile(r"(\d+)\s+passed")
_COLLECTED_RE = re.compile(r"collected\s+(\d+)\s+item")


def _run_suite(suite: str) -> tuple[int, str]:
    """Run one suite under pytest. Exit 1 if zero tests collected."""
    r = subprocess.run(
        [sys.executable, "-m", "pytest", suite, "-q", "--tb=line"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = ((r.stdout or "") + "\n" + (r.stderr or "")).strip()
    low = out.lower()
    # Blind spot: suite that collects nothing must not look green
    if "no tests ran" in low or re.search(r"collected 0 items", low):
        return 1, "FAIL collected 0 items (silent suite)"
    m = _PASSED_RE.search(out)
    n_pass = int(m.group(1)) if m else None
    if r.returncode == 0 and n_pass == 0:
        return 1, "FAIL 0 passed (silent suite)"
    if r.returncode == 0 and n_pass is None and "passed" not in low:
        # extremely quiet success with no summary — treat as blind spot
        return 1, "FAIL no pytest summary (silent suite)"
    tail = out.splitlines()[-1] if out.splitlines() else "(no output)"
    if r.returncode != 0:
        return r.returncode, tail
    return 0, tail if n_pass is None else f"{n_pass} passed"


def main() -> int:
    failed = []
    for suite in SUITES:
        code, tail = _run_suite(suite)
        mark = "ok " if code == 0 else "FAIL"
        print(f"  {mark} {suite:24} {tail}")
        if code != 0:
            failed.append(suite)
            # re-run verbose enough to see failures once
            r = subprocess.run(
                [sys.executable, "-m", "pytest", suite, "--tb=short", "-q"],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            print(r.stdout)
            print(r.stderr)

    r = subprocess.run(
        [sys.executable, "build.py", "--check"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    mark = "ok " if r.returncode == 0 else "FAIL"
    print(f"  {mark} build.py --check         (constitution gate, all topics)")
    if r.returncode != 0:
        failed.append("build.py --check")
        print(r.stdout)

    # Carry the trust measurer in the gate — measure before trusting green
    r = subprocess.run(
        [sys.executable, "-m", "universe_explorer.trust_behavior"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    meas_tail = (r.stdout or "").strip().splitlines()
    summary = next(
        (ln for ln in meas_tail if ln.startswith("pass:") or "all_ok" in ln),
        meas_tail[-1] if meas_tail else "(no measure output)",
    )
    mark = "ok " if r.returncode == 0 else "FAIL"
    print(f"  {mark} trust_behavior measure   {summary}")
    if r.returncode != 0:
        failed.append("trust_behavior")
        print(r.stdout)

    r = subprocess.run(
        [sys.executable, "-m", "universe_explorer.ui_expand"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    ui_lines = (r.stdout or "").strip().splitlines()
    ui_sum = next(
        (ln for ln in ui_lines if "fail" in ln.lower() or "pass" in ln.lower()
         or "all_ok" in ln.lower() or "measurements" in ln.lower()),
        ui_lines[-1] if ui_lines else "(no ui_expand output)",
    )
    mark = "ok " if r.returncode == 0 else "FAIL"
    print(f"  {mark} ui_expand measure        {ui_sum}")
    if r.returncode != 0:
        failed.append("ui_expand")
        print(r.stdout)

    if failed:
        print(f"\nFAILED: {failed}")
        return 1
    print("\nall suites + constitution gate + measures: green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
