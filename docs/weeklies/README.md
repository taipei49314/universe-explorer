# Editorial weeklies (Trust Loop TL-3)

> **Measure the week. Do not invent busyness.**  
> Each ISO week: process **≤3** `candidates/` items **or** record **legal silence**.

## File naming

```
docs/weeklies/YYYY-Www.md
```

Example: `2026-W33.md` for the week containing 2026-08-10.

## Required sections

1. **UTC range** — week start/end (Mon–Sun ISO)  
2. **Challenges** — opened / closed / none (link issues + `docs/challenges/` if closed)  
3. **Candidates** — processed ≤3 (accept path or reject→`candidates/rejected/`) **or** legal silence  
4. **Gates** — `run_tests.py` + trust_behavior result (green / fail)  
5. **Honesty** — no confidence numbers; no claim-count KPIs  

## Legal silence

If no candidate moved **and** no light moved, write that explicitly:

> Legal silence this week: no candidate accept/reject; no status light migration.

Silence is **valid**. Fake commits that only touch noise to look active are not.

## Anti-goals

- No “we shipped 12 claims this week” targets  
- No LLM batch accept of candidates  
- No silent light changes (P3)
