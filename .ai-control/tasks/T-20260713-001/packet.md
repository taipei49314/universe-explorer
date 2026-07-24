---
id: T-20260713-001
title: V4-3 arXiv version monitoring (T1b)
status: approved
worker: claude-code
risk: medium
created: 2026-07-13
updated: 2026-07-13
time_cap_minutes: 90
base_branch: main
worktree: "C:\Users\1\Desktop\universe-explorer.worktrees\T-20260713-001"
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

## 修訂紀錄（2026-07-13，worker 開工後盤點，PM 代理修訂）
- 發現 V4-3 核心已於 commit e8b30e5 實作（source_health.py 的
  arxiv_version_findings()），roadmap 未標註完成 → 原「實作」範圍作廢。
- 但本 packet 的驗收條件有兩條未被既有測試滿足：核心版本比對邏輯無離線測試、
  「版本未變 → 零誤報」完全未覆蓋（邏輯與網路 I/O 綁死，不可測）。
- 範圍縮小為：抽出純比對函數 + 補齊離線測試。
- 原允許路徑誤含 watch.py——它在 engine_hashes.json 凍結名單內，已移除。

# 範圍
## 做
- 把 arxiv_version_findings() 的純比對邏輯抽成可離線測試的函數（行為不變）
- 補測試：出新版 → finding 含 id、舊版、新版；版本未變 → 零誤報；
  版本無法解析（0）→ 保持沉默不猜測；schema 零詮釋

## 不做
- 不重新實作 V4-3（已存在，不重造）
- 不判斷「結論變了沒」——版本變化的重審永遠是人（誠實邊界，見 roadmap）
- 不動 Crossref 巡邏的既有行為、不削弱任何既有斷言
- 不碰凍結引擎（engine_hashes.json 名單，含 watch.py）

# 允許修改的路徑
- universe_explorer/dataops/source_health.py（非凍結，V4-3 所在地）
- test_health.py（V4-3 測試區；新增案例，不得削弱既有斷言）

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
