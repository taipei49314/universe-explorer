# Roadmap v5-Q2 — Editorial OS（人決策可吞吐的知識台帳）

> **狀態：** 規劃已定；**Sprint A 開工**（2026-08-11）。  
> **日期：** 2026-08-11  
> **前置：** v5-Q1 Trust Loop S0–S3 已合閘（見 [`roadmap-v5-trust-loop.md`](roadmap-v5-trust-loop.md)）；  
> 使用者路徑硬化（中文搜尋 / H0 token / discover 錯誤 / challenge 契約 / a11y gate）見 PR 軌跡。  
> **北極星不變：** 誠實區分已知／未知；先量測，再信任；不給假答案、不造信心分。

---

## 0. 一句話

**Q2 不是「更多 claim」或「Phase 4 功能山」。**  
Q2 = **Editorial OS**：挑戰與 candidate **進得來**，人裁決 **出得去**，每週 **可沉默、可重算**。

| Q1 已證明 | Q2 要補的洞 |
|-----------|-------------|
| ≥1 公開挑戰閉環（#2 **reject** light） | 仍缺穩定的 **accept** 閉環（燈動或證據實質增補 + `status_history` / 紀錄） |
| Trust Loop 面板、weeklies 結構、三 canonical | 佇列可計數，但 **Inbox → Decision → Feed** 未成 OS |
| challenge 模板 + 表單契約 | 編輯 SLA（N≤3、legal silence）要連續可覆核 |
| 91 claims · 雙軸 · discovery | 外人 10 分鐘能跟做；維護者 30 分鐘能結案 |

硬依賴（沿用 v5）：**不得**在零 accept／零運營 log 下用 claim 增長宣告 Q2 成功。

---

## 1. 現況盤點（可重算）

```sh
python run_tests.py
python -m universe_explorer.trust_behavior
python -m universe_explorer.ui_expand
python -m universe_explorer health
```

| 量 | 來源（自己重算） |
|----|------------------|
| Topics / Claims | 8 / 91（registry） |
| Authored edges / reading paths | 96 / 8 authored（+ dynamic paths 於 CLI） |
| 公開 overturn 案例 | **1** — issue [#2](https://github.com/taipei49314/universe-explorer/issues/2) **reject** |
| 公開 **accept** 案例 | **0** ← Q2 Sprint A 主缺口 |
| trust_behavior | n_fail 必須 0 |
| Editorial primary / secondary | cosmology (H0) / seismology（[`editorial-queue.md`](editorial-queue.md)） |

### 憲法紅線（Q2 全程）

| ✅ 允許 | ❌ 禁止 |
|---------|---------|
| 人裁決；append-only `status_history` + 決策紀錄 | AI / 腳本自動改燈 |
| 計數、清單、合法沉默週報 | confidence / 排名 / trust score |
| candidate → draft → **人** accept | LLM 直寫 `data/*.py` 成事實 |
| 量測器擴列（expected vs observed） | 用 star、claim 數當 KPI |
| 加深 primary/secondary Discussion | 新 domain、claim 衝量 |
| 薄工程服務 OS（Inbox、deep-link） | monorepo / NASA 自動 inlet |

**繼續 defer：** NASA/ESA 自動寫 knowledge、T4b 多源 7B 阻塞項、3D 宇宙、runtime LLM 宣布事實。

---

## 2. 目標層級

| 層 | 目標 | 反目標 |
|----|------|--------|
| **Mission** | 判定可被第三人用可查來源推翻；**接受也算成功** | 永遠只 reject 裝安全 |
| **Product** | Inbox 5 分鐘答「幾件待審」；結案 30 分鐘內可重放 | 功能演示合集 |
| **System** | candidate / challenge / weekly 同一套計數契約 | 只有 README 儀式 |
| **Phase** | 本文件 EO-* 工作包 + Sprint A–C | 同時開三條 Nelson 主戰場 |

---

## 3. 三季位置（不變）

```
Q1 Trust Loop ✅  ──►  Q2 Editorial OS (本文件)  ──►  Q3 Public Product
   證明可推翻              人決策可吞吐                   值得回訪
```

Q1 摘要：S0 量測 → S1 首閉環 reject → S2 面板+weeklies → S3 三 canonical。  
Q3 前提：Q2 至少 **EO-1 + EO-2 綠**，且 **≥1 accept 閉環**（見 §4.3）。

---

## 4. 工作包（EO-*）

| ID | 名稱 | 做什麼 | 完成定義（量測 / 可檢查） |
|----|------|--------|---------------------------|
| **EO-1** | Candidate→Draft 契約 | discovery / precheck / review 與 draft 一條龍；accept 前永遠不寫燈 | 計數 pending / accepted / rejected；accept 必過 cite⇒fetch + constitution；路徑寫在 weeklies |
| **EO-2** | Provenance 值班 | `source_health` + 必要 acknowledge 的週儀式 | 無 silent light；digest 只 restatement（P5/P5b） |
| **EO-3** | Discussion 深度 | 只加深 primary/secondary：cosmology H0、seismology | 每域 Author-Year 完整；至少一組 competing 寫清；不開新 domain |
| **EO-4** | 貢獻路徑實測 | CONTRIBUTING + challenge 表單用一次真實閉環跑通 | 步驟零跳號；issue + `docs/challenges/` 永久可覆核 |
| **EO-5** | Inbox 可見性 | 統一：GitHub `challenge` issues + `candidates/` + 可選 `challenges/*.json` | health 或 docs 清單可答「待審 N」；只計數 |
| **EO-6** | Accept 閉環 | 至少一次**接受**（燈動 **或** 證據實質增補且紀錄為 accept） | 燈動 ⇒ `status_history` + watch/feed；純證據 accept 也要 decision record |

**Q2 不做：** 新 domain、claim 數目標、自動升燈、第三套 explore UI 當主線。

---

## 5. Sprint 表

**時間盒：** 約 4–6 週（可壓成 3 sprint）。

| Sprint | 長度 | 焦點 | 交付 | 主要 EO |
|--------|------|------|------|---------|
| **A** | ~1–2 週 | **Overturn 事實密度** | 設計並執行下一條自攻；目標 **accept**；issue + `docs/challenges/` | EO-4, EO-6 |
| **B** | ~2 週 | **Editorial OS 本體** | Inbox 計數、candidate→draft 契約可跑、週 SLA 連續 | EO-1, EO-2, EO-5 |
| **C** | ~1–2 週 | **深度 + 公開預備** | H0/seismology Discussion；三 canonical 導覽可跟做；Q3 入口清單 | EO-3, EO-4 |

### 5.1 Sprint A — 開工細節

見 **§8 Sprint A 設計包**（目標 claim、攻擊論點、接受條件、反模式）。

| 檢查項 | 狀態 |
|--------|------|
| 目標 claim 選定 | ✅ `shoes_local_H0_high`（主）；備援見 §8.4 |
| 攻擊類型 | verdict：`FRONTIER` → `STRONG`（**accept**） |
| GitHub issue 已開 | ✅ [#5](https://github.com/taipei49314/universe-explorer/issues/5) |
| data 編輯 + `status_history` | ✅ `cosmology.py` + zh overlay |
| `run_tests.py` 綠 | ✅ trust_behavior 499/499 after rebuild |
| `docs/challenges/YYYY-MM-DD-shoes-….md` | ✅ `2026-08-11-shoes-local-H0-frontier-to-strong.md` |

### 5.2 Sprint B — 預告

1. EO-5：`health` / Trust Loop 或 `docs/editorial-inbox.md` 列出待審計數。  
2. EO-1：從 1 個 candidate 走完 reject **或** draft→人 accept（仍 N≤3/週）。  
3. EO-2：一次 `source_health` 寫入 weekly。  
4. 薄工程（可選，不挡 OS）：deep-link `?c=missing` not-found；engine amendment（empty title / dup labels）另開。

### 5.3 Sprint C — 預告

1. EO-3：`docs/paper/h0-discussion.md` / seismology discussion 補 Author-Year 與 competing 對讀。  
2. 第二條挑戰（可外部）或 legal silence 週。  
3. Q3  readiness checklist（PP-1 URL 故事需要的連結是否齊）。

---

## 6. 量測器契約（Measure first）

Q2 **不發明 confidence**。進下一季只看計數與布林閘。

### 6.1 既有閘門（不得拆除）

| 命令 | 意義 |
|------|------|
| `python run_tests.py` | 全 suite；**0 collected = FAIL** |
| `python -m universe_explorer.trust_behavior` | n_fail 必須 0 |
| `python -m universe_explorer.ui_expand` | 全列 ok |
| `python build.py --check` | 全 topic 憲章 |

### 6.2 Q1 已落地的 overturn 量測（保留）

| Measurement id | 通過條件 |
|----------------|----------|
| `overturn.*` 模板 / CONTRIBUTING / feed·changes | 見 v5-Q1 §7.2 |
| `stress.hawking_diverges` | 維持 `true` |
| `overturn.public_record_exists` | `docs/challenges/` ≥1 |

### 6.3 Q2 建議新增量測 ID（Sprint B 實作，S0 可先 stub）

| Measurement id | surface | 通過條件 |
|----------------|---------|----------|
| `editorial.inbox_doc_or_health` | surface | 存在可讀的待審入口（health 錨點 **或** `docs/editorial-inbox.md`） |
| `editorial.accept_record_exists` | contract | `docs/challenges/` 中 ≥1 件 verdict=**accept**（燈動或證據 accept） |
| `editorial.weekly_current_iso_week` | ops | 當週 ISO week 檔存在 **或** 合法沉默句（實作時選可機器查的一種） |
| `stress.shoes_status_matches_history` | stress | 若燈曾動，末筆 `status_history` 與現狀一致 |

**運營量測（文件 / log，不進假分數）：**

| 計數 | 記錄處 | 規則 |
|------|--------|------|
| challenges_opened / closed | GitHub + weeklies | 只計數 |
| overturns_accepted | status_history + `docs/challenges/` | 燈變必有 history |
| overturns_rejected | `docs/challenges/` | condition 級理由 |
| candidates_processed | weeklies | ≤3/週建議上限 |
| legal_silence_weeks | weeklies | 無變更時**必須**記一筆 |

### 6.4 反模式

- ❌ 用 n_pass/n_measurements 當「信任百分比」  
- ❌ 量測全綠但零 accept，就宣稱 Q2 完成  
- ❌ 為了 accept 強行改燈、跳過 STATUS_CONDITIONS  
- ❌ 為了活躍假 commit 改 status  

---

## 7. 合格線 / 優秀線

### 7.1 Q2 最低合格

1. **≥1 公開 accept 閉環**（本季；可與 Q1 reject 並存）  
2. `run_tests.py` + trust_behavior + ui_expand 持續綠  
3. 連續 **4** 週 weeklies：candidate 處理 **或** legal silence  
4. EO-1 可演示：至少 1 條 candidate 有 accept/reject 紀錄  
5. EO-5：任意時刻可答「待審 N」（計數 only）  

### 7.2 Q2 優秀

6. 外部（非維護者）開過 challenge 或 PR  
7. ≥2 accept **或** 1 accept + 1 新 reject（condition 級）  
8. Inbox 與 feed/changes 在同一次結案中可互相點到  

### 7.3 進入 Q3 的硬閘

- Q2 §7.1 全滿  
- Hawking `diverges=true` 仍鎖  
- 無 silent light 變更  

---

## 8. Sprint A 設計包 — 下一條自攻 / **接受** 目標

### 8.1 為什麼不是再打 Hawking

| | issue #2 `hawking_radiation` | Sprint A 新目標 |
|--|------------------------------|-----------------|
| 結果 | **Reject** light change | 規劃 **Accept** |
| 教學 | 雙軸不可壓成一軸 | 燈號可 overturn，條件可寫清 |
| Q2 缺口 | 已有 reject 範例 | 缺 accept 範例 |

再 reject 一次同型攻擊會增加「閉環次數」但不補 **accept 事實**。

### 8.2 主目標 claim

| Field | Value |
|-------|--------|
| **claim_id** | `shoes_local_H0_high` |
| **Topic** | `cosmology`（editorial **primary**） |
| **現況燈** | 🟠 `FRONTIER` |
| **Evidence axis** | E3（indirect；距離階梯） |
| **`diverges`** | false |
| **Canonical 關係** | H0 故事的 **local 極**；張力本體是 `H0_tension_local_vs_cmb`（COMPETING） |
| **Deep-link** | `app.html?c=shoes_local_H0_high` |
| **Path** | `app.html?path=path_h0` |
| **攻擊類型** | **verdict** |
| **建議新燈** | 🔵 `STRONG` |
| **規劃裁決** | **Accept**（若條件覆核成立） |

### 8.3 攻擊論點（自攻草稿 — 可貼進 issue）

**命題：**  
將 `shoes_local_H0_high` 標為 FRONTIER，把「測量綱領是否仍在快速演化」與「local 高 H0 測定的主流方向是否穩」混在同一格燈裡。  
在 STATUS_CONDITIONS 下，更貼切的是 **STRONG**（mode=all）：

| STRONG condition | 自攻主張 holds | 可查依據（起點） |
|------------------|----------------|------------------|
| `mainstream_model_support` | True | Cepheid→SN Ia 階梯為晚期宇宙 H0 主流路線之一；Riess et al. SH0ES 系列（如 arXiv:2112.04510） |
| `minor_alternatives_exist` | True | TRGB、系統差辯論、宿主質量步等 — 少數替代／修正，不否定階梯本體 |
| `overall_direction_robust` | True | 多年 local 高 H0 方向穩定；新證據多在系統差與零點，而非「階梯無效」 |

**FRONTIER 現有 status_reason 的問題（攻擊面）：**

| FRONTIER condition（現標 True） | 攻擊 |
|--------------------------------|------|
| `no_consensus_formed_yet` | 過寬：社群爭議的是 **與 CMB+ΛCDM 的張力** 與殘餘系統差，不是「有沒有一個高度發展的 local 測定綱領」 |
| `rapidly_growing_literature` | 文獻仍多，但 **mode=any 的 FRONTIER** 不應單獨壓過已滿足的 STRONG 三條件（燈號屬 claim，張力應落在 `H0_tension_local_vs_cmb`） |
| `insufficient_observation` | 仍可寫進 open_questions；不足以降到「方向不穩」 |

**明確不攻擊：**

- 不宣稱張力已解決  
- 不把 `H0_tension_local_vs_cmb` 從 COMPETING 拉走  
- 不發明信心 %；不改 evidence axis 規則（階梯仍是 indirect → E3 合理）  
- 不把 CMB 極一併暗改（備援見 §8.4）

### 8.4 接受時的資料契約（執行 checklist）

若裁決 **Accept**：

1. `status`: `FRONTIER` → `STRONG`  
2. `status_reason`: 改為 STRONG 三條件的 `ConditionAssessment`（holds + 可查 note）  
3. `status_history`: append 一筆（from/to、日期、理由、issue 連結）  
4. 可選：增補 1 筆 PRIMARY 出處（cite⇒fetch）；**非必須**若既有源已夠  
5. `open_questions` 保留系統差 / JWST 零點 — 誠實未關  
6. `python run_tests.py` + `build.py`  
7. `docs/challenges/YYYY-MM-DD-shoes-local-H0-frontier-to-strong.md`  
8. weeklies：記 1 accept；candidates 本週可 legal silence  

若覆核後 **不能** 誠實 satisfiy STRONG（例如認為系統差仍否定 overall_direction_robust）：

- **Reject** 並寫 condition 級理由（仍算閉環，但 **不** 滿足 EO-6 accept 計數）  
- 改打備援 claim，不硬改燈  

### 8.5 備援目標（主目標卡住時）

| 優先 | claim_id | 規劃 | 何時改用 |
|------|----------|------|----------|
| B1 | `cmb_lcdm_implies_low_H0` | FRONTIER→STRONG（early 極對稱論證） | 與 shoes 同時審可成「雙極 Strong + 張力 Competing」套餐；或 shoes 被拒後 |
| B2 | `oef_informs_civil_protection` | **source/evidence accept**：補 CSEP/國家 OEF 源；燈可維持 FRONTIER | 想先練 cite⇒fetch 與 seismology secondary |
| B3 | `standard_sirens_H0` | 維持 FRONTIER；證據包增補 dark/bright siren 文獻 | 只要證據 accept、不改燈時 |

**不建議本 sprint 自攻：**  
`hawking_radiation`（剛 reject）、`accelerated_expansion`（諾獎級 STRONG，易變成表演）、`dark_oxygen_production`（爭議新結果，accept 風險高且非 primary）。

### 8.6 教化學習（接受後產品句）

> Local 階梯測定可以是 **Strong**；CMB+ΛCDM 推論可以是 **Strong**；  
> **Competing** 留給張力本身（`H0_tension_local_vs_cmb`）。  
> 燈號在 claim 上，不在「H0 這個話題」上。

這與 v5-S3 H0 canonical 一致，並補上「可 overturn 極點燈號」的實彈。

### 8.7 Sprint A 執行順序（下一步人工）

```text
1. 開 GitHub issue（challenge-a-verdict），貼 §8.3 表
2. 覆核 Riess2022b / Verde2019 與 STATUS_CONDITIONS
3. 人裁決 accept 或 reject（寫進 issue）
4. accept → 改 cosmology.py + history + tests + challenge 紀錄
5. weekly 記一筆；更新本文件 §5.1 檢查項 ✅
```

---

## 9. 與既有文件的關係

| 文件 | 角色 |
|------|------|
| [`roadmap-v5-trust-loop.md`](roadmap-v5-trust-loop.md) | Q1 全文 + Q2/Q3 摘要；**本文件展開 Q2** |
| [`constitution.md`](constitution.md) | 法；改燈必合 STATUS_CONDITIONS + P3 history |
| [`editorial-queue.md`](editorial-queue.md) | primary=H0 cosmology；secondary=seismology |
| [`milestones-complete.md`](milestones-complete.md) | Q2 項完成時回寫 |
| [`docs/challenges/`](challenges/) | 閉環永久紀錄（reject #2；accept 待寫） |
| [`TESTING-BLIND-SPOTS.md`](../TESTING-BLIND-SPOTS.md) | 工程盲點；Q2 只抽服務 OS 的薄項 |
| [`hawking-walkthrough.md`](hawking-walkthrough.md) | Canonical #1；勿在 Q2 重打成 accept 假勝利 |

---

## 10. 明確不做（Q2 範圍）

1. ❌ 第 9 個科學 domain  
2. ❌ Claim 數量 KPI  
3. ❌ NASA/ESA 自動寫入 knowledge  
4. ❌ LLM 運行時宣布事實或自動升燈  
5. ❌ confidence / trust score / 排行榜  
6. ❌ 自動 merge challenge  
7. ❌ 為活躍假改 status  
8. ❌ 用 Playwright / 新 UI 替代 accept 事實  
9. ❌ monorepo 合併 NormShift / tomorrowci（Q3 才敘事接線）  

---

## 11. 風險與緩解

| 風險 | 緩解 |
|------|------|
| 強行 accept 傷害憲章 | §8.4 允許改 reject；備援 B1–B3 |
| 自嗨自攻 | 條件鍵 + arXiv/DOI；issue 永久可覆核 |
| 與功能 PR 搶 main | 功能可合，不得紅 trust_behavior / silent-suite |
| 編輯倦怠 | N≤3；legal silence 合法 |
| 只改 shoes、忘了張力 claim | 產品句 §8.6；不碰 COMPETING 本體除非另開 issue |

---

## 12. 定義「Q2 完成 / 可進 Q3」

同時滿足：

1. §7.1 最低合格  
2. 公開 URL 可走：讀 H0 path → 看 shoes（新燈若已 accept）→ challenge 路徑  
3. `run_tests.py` 綠  
4. README / about / weeklies **不**宣稱科學張力已解決  

發版註記建議：「Editorial OS / first accepted overturn」+ 連結 accept issue；**不**宣告 H0 已決。

---

## 13. 變更日誌

| 日期 | 變更 |
|------|------|
| 2026-08-11 | 初版：EO-1…6、Sprint A–C、量測列、Sprint A 目標 `shoes_local_H0_high` |
