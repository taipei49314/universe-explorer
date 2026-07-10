"""V4-2 acceptance: the consolidated constitution and the code cannot drift.
Run: python test_constitution.py"""

from __future__ import annotations

from pathlib import Path

from universe_explorer.validator import LAWS

DOC = Path("docs/constitution.md").read_text(encoding="utf-8")


def test_every_law_appears_in_the_constitution():
    """Every rule registered in LAWS must be named in constitution.md."""
    missing = [rule for rule in LAWS if f"`{rule}`" not in DOC]
    assert not missing, f"rules missing from the constitution doc: {missing}"


def test_every_amendment_is_indexed():
    # all six amendments have a row in the index table
    for n in range(1, 7):
        assert f"| {n} |" in DOC, f"amendment #{n} missing from the index"
    # every referenced amendment file really exists (amendment #5 lives in
    # the amendment-4 file, second part — by design)
    for fname in ("amendment-1-r7.md", "amendment-2-narrative-i18n.md",
                  "amendment-3-source-tiers.md",
                  "amendment-4-r8-tier-weighting.md",
                  "amendment-6-c2-doi-provenance.md"):
        assert fname in DOC, fname
        assert Path("docs", fname).exists(), fname


def test_licenses_exist_and_are_referenced():
    assert Path("LICENSE").exists()
    assert Path("LICENSE-CONTENT.md").exists()
    assert "MIT" in DOC and "CC BY 4.0" in DOC


def test_constitution_declares_no_verdicts():
    """The consolidated doc is normative, not evidentiary: it must not smuggle
    in claim verdicts or sources of its own."""
    assert "doi:" not in DOC.lower()
    assert "arXiv:" not in DOC


def _run():
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
            passed += 1
    print(f"\n{passed} tests passed.")


if __name__ == "__main__":
    _run()
