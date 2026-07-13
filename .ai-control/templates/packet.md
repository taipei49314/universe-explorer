---
id: {{ID}}
title: {{TITLE}}
status: draft
worker: {{WORKER}}
risk: {{RISK}}
created: {{DATE}}
updated: {{DATE}}
time_cap_minutes: {{TIMECAP}}
base_branch: {{BASE}}
worktree: ""
test_command: ""
requires_review: true
requires_human_approval: true
---

# 目標
（一句話：做完之後世界有什麼不同）

# 背景
（為什麼要做。相關決策：.ai-control/decisions/ADR-XXXX）

# 範圍
## 做
-

## 不做
-

# 允許修改的路徑
- src/

# 禁止修改的路徑
- .ai-control/（本任務的 packet.md、notes.md 除外）
- .env 與任何 secrets

# 驗收條件
- [ ]
- [ ] test_command 執行通過，證據在 evidence/ 內

# 交接備註
（AI：收工前寫進 worktree 根目錄的 `HANDOFF.md`，evidence 收集時會自動歸檔到本任務的 evidence/ 內。
人類：審查後的裁決與備註可以直接寫在這裡。）
