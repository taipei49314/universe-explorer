# End-to-end: `hawking_radiation`

Canonical **dual-axis stress case**. Not a verdict tour — a trace of how one
claim moves through the constitution.

## 1. Data layer

File: `universe_explorer/data/black_hole.py` → claim `hawking_radiation`

| Field | Value |
|-------|--------|
| Title | Black holes emit thermal Hawking radiation and slowly evaporate |
| Status light | **Strong Consensus** (🔵) |
| Sources | `Hawking1975` (Commun. Math. Phys. 43, 199) · `Steinhauer2016` (arXiv:1510.00621) |
| Evidence | theoretical derivation → Hawking1975 · analog experiment → Steinhauer2016 |
| `status_reason` | all three Strong conditions hold (mainstream support, minor alternatives, overall direction robust) |
| Open questions | 3 recorded strings (no numeric “score”) |

## 2. Constitution gate

```sh
python -c "from universe_explorer.data.black_hole import hawking_radiation as c; from universe_explorer.validator import validate_claim; print(validate_claim(c) or 'PASS')"
```

Expected: empty violation list. Every evidence item has a resolving `source_ref`;
reasons map onto `STATUS_CONDITIONS[STRONG]` (mode `all`).

## 3. Evidence axis (derived, never declared)

```sh
python -c "from universe_explorer.data.black_hole import hawking_radiation as c; from universe_explorer.axes import derive, diverges; d=derive(c); print(d.strength, diverges(c)); print(d.reasoning)"
```

| Output | Meaning |
|--------|---------|
| **E3** | indirect / analog only |
| **diverges = True** | high consensus resting on non-direct evidence |

Rule path: 0 direct observations → analog present → E3. Certainty is not a % field.

## 4. Narrative (bottom layer)

```sh
python -c "from universe_explorer.data.black_hole import hawking_radiation as c; from universe_explorer.narrative import narrate; 
[print(s.refs, s.text[:120]) for s in narrate(c)]"
```

Mechanical composer emits ~6 sentences: constitutional opening, each evidence
line, axis grade, **divergence note**, open-questions prompt. Every sentence
carries resolvable refs. `check()` rejects confidence vocabulary and orphan %.

## 5. Relations

Authored edges that touch this claim (non-exhaustive of the whole graph):

| Source | Target | Kind |
|--------|--------|------|
| `event_horizon_exists` | `hawking_radiation` | requires |
| `information_paradox` | `hawking_radiation` | requires |

Reading path: `path_black_hole` includes `hawking_radiation` mid-sequence
(horizon → … → Hawking → … → firewall ceiling).

## 6. UI / open data

| Surface | How |
|---------|-----|
| Map | `app.html?c=hawking_radiation` |
| Static topic | `black_hole.html#c-hawking_radiation` |
| Open JSON | `claims.json` → id `hawking_radiation` (`evidence_axis: E3`, `diverges: true`) |
| About | P-Read canonical example of axis split |

```sh
python build.py
python -m http.server 8731 --directory dist
# open http://localhost:8731/app.html?c=hawking_radiation
```

## 7. Challenge path

If the Strong light is wrong: open
[Challenge a verdict](../.github/ISSUE_TEMPLATE/challenge-a-verdict.yml)
naming a condition key under Strong (`mainstream_model_support`,
`minor_alternatives_exist`, `overall_direction_robust`) with a checkable source.
See [CONTRIBUTING.md](../CONTRIBUTING.md).

---

*This walkthrough invents no confidence. It only restates recorded fields and
mechanical derivations.*
