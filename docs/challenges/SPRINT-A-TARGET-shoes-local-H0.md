# Sprint A target — `shoes_local_H0_high` (design pack)

| Field | Value |
|-------|--------|
| **Status** | 🟡 **Designed — not yet filed / not yet closed** |
| **Roadmap** | [`docs/roadmap-v5-q2-editorial-os.md`](../roadmap-v5-q2-editorial-os.md) §8 |
| **Sprint** | v5-Q2 Sprint A |
| **Goal** | First **accept** overturn (Q1 #2 was reject-only) |
| **Claim** | `shoes_local_H0_high` |
| **Attack** | Verdict: FRONTIER → STRONG |
| **Planned verdict** | **Accept** (if conditions hold on re-read) |
| **Issue** | ⬜ not opened yet |
| **Closed record** | ⬜ after decision → `docs/challenges/YYYY-MM-DD-shoes-….md` |

---

## Why this claim

1. **Editorial primary** — cosmology / H0 cluster ([`editorial-queue.md`](../editorial-queue.md)).  
2. **Canonical adjacency** — teaches the H0 story without re-fighting Hawking dual-axis.  
3. **Honest accept path** — light can move under STATUS_CONDITIONS without claiming the tension is solved.  
4. **Product sentence after accept:**  
   *Local ladder measurement can be Strong; CMB+ΛCDM inference can be Strong; Competing stays on `H0_tension_local_vs_cmb`.*

---

## Current inventory (re-measure yourself)

```sh
python -m universe_explorer search "H0"
# or open app.html?c=shoes_local_H0_high
```

| Field | As of design date |
|-------|-------------------|
| status | FRONTIER |
| evidence_axis | E3 |
| diverges | false |
| sources | Riess2022b (arXiv:2112.04510), Verde2019 (arXiv:1907.10625) |
| status_history | empty |

---

## Attack (paste into GitHub challenge template)

### Summary

`shoes_local_H0_high` is labeled **Frontier**, but the claim is about a **mature late-universe distance-ladder determination** of a high local H0 (~73). Frontier conditions (mode=any) over-weight “literature still moves” and under-weight the Strong triad: mainstream method support, minority alternatives, robust overall direction. The **tension** with early-universe inference already has its own Competing claim (`H0_tension_local_vs_cmb`); that should not force the local pole to stay Frontier.

### Proposed change

- **From:** FRONTIER  
- **To:** STRONG  
- **Not proposed:** resolving H0 tension; changing evidence axis rules; demoting Competing tension claim.

### Condition table (STRONG, mode=all)

| condition | holds? | Note + checkable source |
|-----------|--------|-------------------------|
| `mainstream_model_support` | yes | Cepheid–SN Ia ladder is a mainstream late-universe H0 route; SH0ES ApJL 934, L7 (arXiv:2112.04510) |
| `minor_alternatives_exist` | yes | TRGB and systematic reanalyses exist as minority/alternate calibrators and critiques; they refine, not replace, the ladder programme |
| `overall_direction_robust` | yes | Multi-year local high-H0 direction is stable; new work focuses on zero-point and systematics (see Verde et al. Nat. Astron. review arXiv:1907.10625) |

### Evidence refs (checkable)

- arXiv:2112.04510  
- arXiv:1907.10625  

---

## Accept checklist (executor)

- [ ] Issue opened with template `challenge-a-verdict.yml`  
- [ ] Human re-read of `status_reason` vs `STATUS_CONDITIONS`  
- [ ] If accept: edit `universe_explorer/data/cosmology.py`  
- [ ] `status_history` append (from FRONTIER → STRONG, issue URL, date)  
- [ ] `status_reason` rewritten for Strong triad  
- [ ] `python run_tests.py` green  
- [ ] Closed markdown under `docs/challenges/`  
- [ ] Weekly log: 1 accept  
- [ ] Update roadmap §5.1 checkboxes  

## Reject off-ramp

If `overall_direction_robust` cannot be honestly marked true (e.g. executor judges residual systematics as direction-breaking):

- Close as **reject** with condition-level notes  
- Switch to backup B1 `cmb_lcdm_implies_low_H0` or B2 `oef_informs_civil_protection` (source accept)  
- Do **not** force the light  

---

## Honesty note

Accepting Strong on a **pole measurement claim** is not a claim that cosmology has converged on H0. The Competing light on `H0_tension_local_vs_cmb` remains the tension container. No confidence field is introduced.
