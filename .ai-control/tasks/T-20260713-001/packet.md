---
id: T-20260713-001
title: V4-3 arXiv version monitoring (T1b)
status: draft
worker: claude-code
risk: medium
created: 2026-07-13
updated: 2026-07-13
time_cap_minutes: 90
base_branch: main
worktree: ""
test_command: "python run_tests.py"
requires_review: true
requires_human_approval: true
---

# 目標
週巡邏能偵測 arXiv 快取論文出了新版本（v2/v3…），並以事件進 feed／issue——
機械記錄「來源在動」，零詮釋。

# 背景
Roadmap V4-3（docs/roadmap-v4.md）。T1 目前只看 Crossref 的正式更正；
arXiv 修訂是另一種「來源在動」，系統目前無感（缺口 G6）。
與 Crossref 巡邏走同一 workflow。

# 範圍
## 做
- 週巡邏擴充：對每個 arXiv 快取比對 API 的最新版本號
- 出新版 → 事件（id、舊版、新版、日期）→ feed → issue
- 對應的測試（比照 test_watch.py / test_feed.py 的風格）

## 不做
- 不判斷「結論變了沒」——版本變化的重審永遠是人（誠實邊界，見 roadmap）
- 不動 Crossref 巡邏的既有行為
- 不新增付費或需金鑰的服務（免費優先已入憲；arXiv API 免金鑰）

# 允許修改的路徑
- universe_explorer/watch.py
- universe_explorer/dataops/
- test_watch.py、test_feed.py（新增案例；不得削弱既有斷言）
- run_tests.py（僅在需要註冊新測試檔時）

# 禁止修改的路徑
- engine_hashes.json、docs/constitution.md（憲法級，hooks 強制）
- universe_explorer/model.py、validator.py（動到就是修憲，先停下來提 ADR）
- .ai-control/（本任務 packet 除外）、.env 與任何 secrets

# 驗收條件
- [ ] 模擬「arXiv 出新版」的測試案例：事件被記錄，含 id、舊版號、新版號、日期
- [ ] 模擬「版本未變」：不產生事件（無誤報）
- [ ] 事件走既有 feed／issue workflow，與 Crossref 巡邏同構
- [ ] 事件內容零詮釋——只有機械事實，無任何「結論可能改變」類文字
- [ ] python run_tests.py 全綠（既有測試一個都不能紅），證據在 evidence/ 內

# 交接備註
（AI：收工前寫進 worktree 根目錄的 `HANDOFF.md`，evidence 收集時會自動歸檔到本任務的 evidence/ 內。
人類：審查後的裁決與備註可以直接寫在這裡。）
