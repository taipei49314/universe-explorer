# Contributing — how to overturn us / 如何推翻我們

This system's core promise is that **every verdict can be overturned by anyone
with a checkable argument**. This document is the path.

本系統的核心承諾:**任何人拿著可查證的論證,都能推翻任何判定。** 本文件就是那條路。

## The 10-minute re-review / 十分鐘覆核流程

1. Open [claims.json](https://taipei49314.github.io/universe-explorer/claims.json)
   (or any claim card on the [site](https://taipei49314.github.io/universe-explorer/)).
2. Pick a claim. Its `status_reason` lists, condition by condition, why it
   carries its light. The conditions come from the frozen five-cell taxonomy
   (`universe_explorer/model.py`, `STATUS_CONDITIONS`) — statuses with mode
   `all` need every condition to hold; mode `any` needs one.
3. Check each condition against the recorded evidence and your own sources.
   Also check the evidence axis: it is derived by public rules
   (`universe_explorer/axes.py`) — recompute it yourself.
4. Found a failure? Open a
   [Challenge issue](../../issues/new?template=challenge-a-verdict.yml).
   Name the condition key. Attach a checkable source (DOI / arXiv id) —
   a challenge without a source is itself an unsupported claim.

## What happens to a successful challenge / 挑戰成立之後

The claim's data file is edited (new evidence recorded through cite⇒fetch,
status moved **with** a `status_history` entry — lights never change silently),
the constitution gate re-runs in CI, and the change flows into the
[Atom feed](https://taipei49314.github.io/universe-explorer/feed.xml).
Your issue is the permanent record of the overturn.

## Ground rules (the constitution, in brief)

- Every "known" hangs on a real, fetched, hash-verified source.
- No confidence numbers — certainty emerges from evidence, never gets declared.
- The status light belongs to the claim, never the topic.
- Machines may exclude, only humans approve; AI drafts are stamped UNVERIFIED.
- Engine files are hash-frozen; changing them requires a numbered amendment
  (`docs/amendment-*.md`).

Run everything locally: `python run_tests.py` (all suites + the gate).
