# UI domain-expand measure

> **Measure first. Trust only what the counts show.**  
> Expand behaviour is not declared correct; it is *measured*.

## What is measured

| Surface | Behaviour | Observable |
|---------|-----------|------------|
| `app.html` | Domain accordion | open/closed per domain; chip auto-open; claim list count |
| `universe.html` | Constellation expand | `expandId` toggle; nav / label path |
| index (`render.py`) | Topic cards | toggle + `?open=` deep-link |
| `app-data.json` | Inventory | focus domain exists; `title_zh`; claim count |

Each row in the report is a **measurement**: `expected` vs `observed` + boolean `ok`.  
There is **no** `confidence`, `score`, `probability`, `certainty`, or `trust` field.

`n_pass` / `n_fail` / `n_measurements` are **counts of the measurement list** — recount them yourself.

## Offline gate (CI)

```sh
python -m universe_explorer.ui_expand              # text report
python -m universe_explorer.ui_expand --json        # JSON
python -m universe_explorer.ui_expand --out health/ui-expand.json
python test_ui_expand.py
python run_tests.py                                 # includes test_ui_expand
```

Exit code **0** only when `n_fail == 0`.

## Runtime channel (opt-in)

In the browser, enable the measure log:

- URL: `app.html?measure=1` or `universe.html?measure=1`
- or `localStorage.setItem("ue_measure", "1")`

Then, after clicks:

```js
window.__UE_MEASURE__.snapshot()   // list of {t, event, ...}
window.__UE_MEASURE__.count("domain_expand")
window.__UE_MEASURE__.n()          // total events recorded
```

Events:

- `domain_expand` — app domain head toggle (`id`, `open`, `n_claims`, …)
- `domain_chip` — topic chip selection
- `cluster_expand` — drift constellation expand/collapse

The channel is **silent unless opt-in**. It never invents a confidence number.

## Stars (恆星) focus

Default `--focus stars`. A green report means: contracts present, state machine
scenarios pass for that domain, and inventory matches the engine export.
It does **not** mean a human has watched the animation — only that every
*recorded* measurement in this suite passed.
