"""One-command gate: all test suites + the constitution build check.

    python run_tests.py

Exit code 0 = everything green. This is the CI entrypoint.
"""

from __future__ import annotations

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
]


def main() -> int:
    failed = []
    for suite in SUITES:
        r = subprocess.run([sys.executable, suite], capture_output=True, text=True)
        tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        mark = "ok " if r.returncode == 0 else "FAIL"
        print(f"  {mark} {suite:22} {tail}")
        if r.returncode != 0:
            failed.append(suite)
            print(r.stdout)
            print(r.stderr)

    r = subprocess.run([sys.executable, "build.py", "--check"],
                       capture_output=True, text=True)
    mark = "ok " if r.returncode == 0 else "FAIL"
    print(f"  {mark} build.py --check       (constitution gate, all topics)")
    if r.returncode != 0:
        failed.append("build.py --check")
        print(r.stdout)

    if failed:
        print(f"\nFAILED: {failed}")
        return 1
    print("\nall suites + constitution gate: green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
