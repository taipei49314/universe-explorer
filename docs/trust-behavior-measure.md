# Trust-behavior measure

> **Measure first. Trust only what the counts show.**  
> Behaviours a reader might accept as authority are reduced to observables —
> `expected` vs `observed` + boolean `ok`.  
> There is **no** `confidence`, `score`, `probability`, `certainty`, or `trust` field.

## Why this exists

`ui_expand` measures *expand UX*. This module measures *epistemic trust surfaces*:

| Surface people might trust | What we measure |
|----------------------------|-----------------|
| Dual-axis lights / E-grades | Engine recomputation matches; diverges is mechanical |
| Sources behind a claim | Every `evidence.source_ref` resolves |
| Status light | Constitution validator + non-empty `status_reason` |
| Public JSON | No banned certainty keys; export parity with engine |
| Overturn path | Challenge templates + UI copy present |
| Tour / map | Denies confidence %; diverge + challenge copy |
| Canonical example | `hawking_radiation` still Strong × non-direct (diverges) |
| Reading paths | Every domain has an authored path |

## Offline gate

```sh
python -m universe_explorer.trust_behavior
python -m universe_explorer.trust_behavior --json
python -m universe_explorer.trust_behavior --out health/trust-behavior.json
python test_trust_behavior.py
python run_tests.py   # pytest every suite + trust_behavior + ui_expand measures
```

Exit code **0** only when `n_fail == 0`.

`run_tests.py` runs suites under **pytest** (class-based tests must actually
execute). A suite that collects **0 items** is a failure — bare
`python test_foo.py` exiting 0 with no tests is the silent-suite blind spot.

`n_pass` / `n_fail` / `n_measurements` are **counts of the measurement list** —
recount them yourself.

## v5 Trust Loop rows (S0)

| id | Pass when |
|----|-----------|
| `overturn.challenge_verdict_template` | `.github/ISSUE_TEMPLATE/challenge-a-verdict.yml` exists |
| `overturn.challenge_relation_template` | relation challenge template exists |
| `overturn.contributing_mentions_challenge` | CONTRIBUTING documents challenge + `status_reason` |
| `overturn.feed_or_changes_surface` | dist feed/changes **or** generator modules present |
| `canonical.tour_mentions_axes` | app tour teaches dual axes / denies confidence % |
| `overturn.public_record_exists` | ≥1 `docs/challenges/*.md` closed-loop record |

First public record: [`docs/challenges/2026-08-10-hawking-strong-re-review.md`](challenges/2026-08-10-hawking-strong-re-review.md) (issue #2).

## Blind-spot tests

`test_trust_behavior.py` deliberately injects broken shapes:

- dangling `source_ref`
- declared `confidence: N` prose
- empty `status_reason`
- domain with no reading path
- lying `dist/claims.json` axis / diverges fields
- gutted `app.html` contracts

Each must make the measurer **fail**. A green live report without red
synthetic probes would be a blind spot.

## Order of work

1. **Measurer** (`trust_behavior.py`) — this file’s subject  
2. **Then** trust behaviour — only rows with `ok: true`  
3. Never declare “users can trust X” without a measurement id that covers X
