# Roadmap v5 — Trust Loop（可被挑戰的公共知識台帳）

> **狀態：** 規劃已定；**S0–S3 已完成**（2026-08-10）。Q1 最低合格已滿足；Q2 待開。  
> **日期：** 2026-08-10  
> **前置：** v0–v4 引擎與產品表面已合閘；CI 含 pytest 全 suite +  
> `trust_behavior`（481）+ `ui_expand`（56）。  
> **北極星不變：** 誠實區分已知／未知；先量測，再信任；不給假答案、不造信心分。

---

## 0. 一句話

**V1 不是「更多 claim」或「Phase 4 功能山」。**  
V1 = **可被挑戰的公共知識台帳**：Measure first → 有人真的 overturn → 變更可重放 → 外人願意回訪。

| 上一階段做完了什麼 | 這一階段要補的洞 |
|--------------------|------------------|
| 憲章法院、雙軸、跨域、reader/discovery | 還沒有一次**公開成功的 overturn 事實** |
| challenge 模板、CONTRIBUTING、feed | 模板齊了，**運營閉環**未證明 |
| editorial-queue、candidates/ | 儀式寫了，**週節奏可量測**未成產品 |
| 91 claims · 8 paths · 96 authored edges | 故事仍像工具箱，缺 **3 條永遠講得清的 canonical** |

---

## 1. 現況盤點（可重算，非行銷）

```sh
python -m universe_explorer.relations --validate
python -m universe_explorer.trust_behavior
python run_tests.py
```

| 量 | 來源（重算自己數） |
|----|-------------------|
| Topics | 8（registry） |
| Claims | 91 |
| Authored edges | 96 |
| Reading paths | 8（每 domain 至少一條） |
| trust_behavior | n_fail 必須為 0 才准談「可信」 |
| 公開 overturn 案例 | **≥1** — issue [#2](https://github.com/taipei49314/universe-explorer/issues/2)（reasoned **reject**；見 `docs/challenges/`） |

### 憲法紅線（v5 全程）

| ✅ 允許 | ❌ 禁止 |
|---------|---------|
| 人裁決挑戰；append-only 決策與 history | AI / 腳本自動改燈 |
| 計數、清單、合法沉默週報 | confidence / 排名 / trust score |
| candidate → draft → **人** accept | LLM 直寫 `data/*.py` 成事實 |
| 量測器擴列（expected vs observed） | 用 star、claim 數當 KPI |
| 加深 3 條 canonical 故事 | 為活躍假更新 status |
| 與 NormShift / tomorrowci **敘事接線** | 本季 monorepo 合併或搶主線 |

**繼續 defer（沿用 milestones）：** NASA/ESA 自動進 knowledge、T4b 多源 7B 當阻塞項。

---

## 2. 目標層級

| 層 | 目標 | 反目標 |
|----|------|--------|
| **Mission** | 判定可被第三人用可查來源推翻 | 成為「權威科普 AI」 |
| **Product V1** | 外人 60 秒懂、10 分鐘查、能開 challenge | 功能演示合集 |
| **System** | Trust Loop 可量測、可重放 | 只有 README 承諾 |
| **Phase** | 本文件 Q1–Q3 | 同時開三條 Nelson 專案主戰場 |

---

## 3. 三季結構

```
Q1 Trust Loop ──► Q2 Editorial OS ──► Q3 Public Product
   (證明可推翻)      (人決策可吞吐)       (值得回訪)
```

硬依賴：**Q2 不得在 Q1 零 overturn 案例下用 claim 增長宣告成功。**  
Q3 不得在 Q1 量測閘門變紅時上線「更炫 UI」當替代。

---

## 4. Q1 — Trust Loop（最高優先）

**時間盒：** 約 4–6 週（可壓成 3 個 sprint）。  
**完成一句話：** 系統上發生過至少一次**可公開覆核**的挑戰閉環，且週節奏可被量測。

### 4.1 工作包

| ID | 名稱 | 做什麼 | 完成定義（量測 / 可檢查） |
|----|------|--------|---------------------------|
| **TL-1** | 挑戰運營 | 自攻 2–3 條燈（或邀一人）；走 issue 模板 → 改 data 或有據 reject → tests → feed | ≥1 公開 closed `challenge` issue；接受則有 `status_history` 或證據增補；reject 則 issue 留下 condition 級理由 |
| **TL-2** | Challenge 儀表 | health / changes / about 露出「待審 · 已 overturn · 合法沉默」 | 新增 trust_behavior 量測列（見 §6）；頁面可點到 issue 或 feed |
| **TL-3** | 編輯週 SLA | `editorial-queue` + candidates **N≤3/週** 真跑；沒事寫 legal silence | 連續 4 週 log（`docs/unattended-log.md` 或 `docs/weeklies/`）：處理數 **或** 合法沉默（二者必居其一） |
| **TL-4** | Canonical 三故事 | 只打磨：**Hawking 雙軸分叉**、**H0 competing**、**Earth 一條**（建議 AMOC 或 seismology prediction debate） | about + tour + 各 1 條 reading path 可指認；`hawking_radiation` 量測仍 `diverges=true` |

### 4.2 Sprint 拆分（建議）

| Sprint | 長度 | 交付 |
|--------|------|------|
| **S0** | ✅ 2026-08-10 | 本文件合入；`measure_overturn_loop` TL 量測 ID；milestones v5 列 |
| **S1** | ✅ 2026-08-10 | **TL-1**：issue #2 `hawking_radiation` 公開閉環 — **reject** light change（條件級理由 + `docs/challenges/` 紀錄） |
| **S2** | ✅ 2026-08-10 | **TL-2** health/changes Trust Loop 面板 + **TL-3** `docs/weeklies/` 儀式（2026-W33；2 candidates reject-archive） |
| **S3** | ✅ 2026-08-10 | **TL-4** 三 canonical：Hawking / H0 / seismology prediction；about+tour+health+app-data；量測鎖 diverges |

### 4.3 Q1 合格線 / 優秀線

**最低合格：**

1. ≥1 公開挑戰閉環（接受 **或** 有據駁回，寫在 issue） — ✅ #2  
2. `run_tests.py` + trust_behavior + ui_expand 持續綠 — ✅ S0–S3 閘門  
3. 週 log：candidate 處理 **或** legal silence — ✅ 2026-W33（2 reject + 5 silence）  
4. 三 canonical 可在 about/tour 指認；Hawking 仍軸分叉 — ✅ S3  

（連續 4 週 weeklies 仍為 Q1 優秀運營目標；結構已落地。）

**優秀：**

5. 外部（非維護者）開過 challenge 或 PR  
6. feed/changes 出現真實變更事件（非空轉 commit）  
7. 第二條挑戰閉環  

---

## 5. Q2 — Editorial OS

**時間盒：** 約 4–6 週。  
**前提：** Q1 最低合格已滿足。  
**完成一句話：** 人仍決策，但 candidate→claim 與 provenance 值班**可計數、可回放**。

| ID | 名稱 | 做什麼 | 完成定義 |
|----|------|--------|----------|
| **EO-1** | Candidate→Draft 契約 | discovery / precheck / review 與 T4 draft 一條龍；accept 前永遠 UNVERIFIED | 計數：pending / accepted / rejected；accept 必過 cite⇒fetch + constitution |
| **EO-2** | Provenance 值班 | source_health + acknowledge 固定週儀式 | 無 silent light；digest 只 restatement（現有 P5/P5b 憲章） |
| **EO-3** | Discussion 深度 | 只加深 editorial primary/secondary（現：cosmology H0、seismology） | 每域 Author-Year 完整 + 至少一組 competing 寫清 |
| **EO-4** | 貢獻路徑實測 | CONTRIBUTING 10 分鐘流程用一次真實 PR 或外部 issue 跑通 | 步驟零跳號；記錄在 weeklies 或 challenge issue |

**Q2 不做：** 新 domain、claim 數目標、自動升燈。

---

## 6. Q3 — Public Product

**時間盒：** 約 4–6 週。  
**前提：** Q1 合格；Q2 至少 EO-1 + EO-2 綠。  
**完成一句話：** 陌生人值得 bookmark，而不是只在 demo 時打開。

| ID | 名稱 | 做什麼 | 完成定義 |
|----|------|--------|----------|
| **PP-1** | 單一 URL 故事 | Pages 首屏 = 三 canonical + dual-axis +「挑戰我們」 | `?measure=1` 可觀察 tour→claim→challenge 事件序列（既有 Measure 通道） |
| **PP-2** | 週報 / 合法沉默 | weekly Action：有事 digest、沒事 silence 公告 | 連續 12 週不中斷（允許 silence） |
| **PP-3** | Nelson stack 輕接線 | `nelson-stack` / profile：explorer = 知識狀態；NormShift = 標準 diff；tomorrowci = 未來 CI | **只敘事與連結**，不 monorepo |
| **PP-4** | 中英同 court（可選） | 三 canonical 中英 narrative 皆過同一 check | Amendment #2 協議；不降級憲章 |

**Q3 不做：** 3D 宇宙、人格辯論、confidence%、付費牆當信任替代。

---

## 7. 量測器契約（Measure first）

v5 **不發明 confidence**。所有「能不能進下一季」只看計數與布林閘。

### 7.1 既有閘門（不得拆除）

| 命令 | 意義 |
|------|------|
| `python run_tests.py` | pytest 全 suite；**0 collected = FAIL** |
| `python -m universe_explorer.trust_behavior` | 信任表面；n_fail 必須 0 |
| `python -m universe_explorer.ui_expand` | 展開 UX；全列 ok |
| `python build.py --check` | 全 topic 憲章 |

### 7.2 建議新增 trust_behavior 量測 ID（S0/S1 實作）

| Measurement id | surface | 通過條件 |
|----------------|---------|----------|
| `overturn.challenge_verdict_template` | contract | 模板檔存在（已有則保留） |
| `overturn.challenge_relation_template` | contract | 同上 |
| `overturn.contributing_mentions_challenge` | contract | CONTRIBUTING 含 challenge 路徑 |
| `overturn.feed_or_changes_surface` | surface | dist 有 feed.xml 與 changes.html（build 後） |
| `stress.hawking_diverges` | stress | 維持 True（回歸鎖） |
| `canonical.tour_mentions_axes` | ui | tour 文案否認 confidence %（已有類列可對齊） |

**運營量測（文件 / log，不進假分數）：**

| 計數 | 記錄處 | 規則 |
|------|--------|------|
| challenges_opened / closed | GitHub issues + weeklies | 只計數 |
| overturns_accepted | status_history + issue | 燈變必有 history |
| candidates_processed | editorial log | ≤3/週建議上限 |
| legal_silence_weeks | weeklies | 無變更時**必須**記一筆，禁止裝忙 |

### 7.3 反模式

- ❌ 用 `n_pass / n_measurements` 當「信任百分比」對外宣傳  
- ❌ 量測全綠但零挑戰，就宣稱 V1 完成  
- ❌ 為了 benchmark 變綠而放寬憲章  

---

## 8. 與既有文件的關係

| 文件 | 角色 |
|------|------|
| [`constitution.md`](constitution.md) | 法；v5 不修憲除非有 amendment |
| [`milestones-complete.md`](milestones-complete.md) | 已 ship 看板；v5 項目標 ✅ 時回寫 |
| [`product-remediation-7.md`](product-remediation-7.md) | P-Read…P-Sustain；v5 **TL/EO/PP** 吃剩餘運營洞 |
| [`editorial-queue.md`](editorial-queue.md) | 本季主修域；Q1–Q2 遵守 |
| [`trust-behavior-measure.md`](trust-behavior-measure.md) | 量測哲學與 CLI |
| [`hawking-walkthrough.md`](hawking-walkthrough.md) | Canonical #1 管線說明 |
| [`roadmap-v4.md`](roadmap-v4.md) | 授權 / 憲法彙編 / arXiv 版本；**已多完成**；未竟項不阻塞 v5 |
| [`unattended-log.md`](unattended-log.md) | 可作週 log 附錄；合法沉默可寫於此 |

### 與 Nelson 其他 repo（Q3 才接線）

| Repo | 在圖上的位置 |
|------|----------------|
| **universe-explorer** | 知識狀態本體（本 roadmap 主戰場） |
| **NormShift** | 標準文件 evidence-backed semantic diff |
| **tomorrowci** | 「最早何時會破」的時間軸證據 |
| **RepoPassport** | repo 場景可驗證護照 |

一季內 **只深耕 explorer 主線**；接線 = 連結與一句話定位，不是合併工程。

---

## 9. 明確不做（v5 範圍）

1. ❌ 新科學 domain（第 9 個 topic）  
2. ❌ Claim 數量 KPI（「衝到 150」）  
3. ❌ NASA/ESA 自動寫入 knowledge  
4. ❌ LLM 運行時宣布事實或自動升燈  
5. ❌ confidence / trust score / 排行榜  
6. ❌ 自動 merge challenge  
7. ❌ 3D / 軌道模擬當信任替代  
8. ❌ 付費解鎖「更可信」  
9. ❌ 為了活躍假 commit 改 status  

---

## 10. 風險與緩解

| 風險 | 緩解 |
|------|------|
| 自攻挑戰變成自嗨 | 條件鍵 + 可查來源；issue 永久可覆核 |
| 無人來挑戰 | Q1 允許維護者自攻；Q1 優秀線才要求外部 |
| 編輯倦怠 | N≤3 candidates；legal silence 合法 |
| 量測膨脹變儀式 | 新 ID 必須對應 overturn 或 canonical 回歸 |
| 與功能 PR 搶 main | 功能可合，但 **不得** 紅 trust_behavior / 拆 silent-suite 閘門 |

---

## 11. 定義「V1 發布」

同時滿足：

1. Q1 最低合格（§4.3）  
2. 公開 URL（Pages）可走完：讀 Hawking → 看 diverges → 開 challenge 模板  
3. `run_tests.py` 綠（含 measures）  
4. README / about 寫明：**完成里程碑 ≠ 發明信心**  

發版形式建議：GitHub Release 註記「Trust Loop V1」+ 連結第一個 overturn issue；**不**宣告科學結論已定。

---

## 12. 下一步（立刻可做）

1. **S0：** 合入本文件；`milestones-complete.md` 加 v5 列（In progress）；README Docs map 連結。  
2. **S1：** 選第一個 overturn 目標（建議 `hawking_radiation` 一條 Strong 條件，或 H0 一極）→ 開 `[challenge]` issue → 走完閉環。  
3. 全程：`python run_tests.py` 與 `python -m universe_explorer.trust_behavior` 必綠再推。

---

*Completing a roadmap item does not invent confidence.  
Every claim still hangs on sources; every digest still restates events; every edge and light remains challengeable.*
