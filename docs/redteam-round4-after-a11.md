# Universe Explorer 紅隊 Round 4 — 出路 1+2+4 之後

> **前提：** Amendment **#7–#11** 已落地；`run_tests.py` 全綠（含 `test_editorial_openalex` 8）  
> **方法：** 可執行 PoC（2026-08-11），攻擊面 = 收窄承諾後仍破壞「帳本 + 編輯 OS + OpenAlex 發現」  
> **不做：** 再寫策略文；本檔只報洞與證據

---

## 一句話

**形狀法院仍然很硬；語義法院仍然不存在。**  
#11 把產品話術改成「帳本 + 人審標記」，但 **人審標記沒有進公開面**，  
而且 **`human_verified` 用任意字串就能消佇列** —— 編輯 OS 目前是 **離線 CLI，不是讀者看得到的第二軸**。

```text
機器保證（仍成立）     機器不保證（仍成立）      #11 新增表面
─────────────────     ──────────────────      ──────────────
fetch / 地板 / 去重     句子是否被文獻支持(C1)    review_state 欄位
trace_refs 形狀         type 是否說謊             editorial queue CLI
OpenAlex 不判燈         期刊品質                 ⚠ 未進 dist/UI
```

---

## 回歸：仍然關死（本輪複驗）

| 攻擊 | 結果 |
|------|------|
| `example.com` 假 PRIMARY | `primary_source_not_fetchable` |
| 同一 arXiv 雙 label / v1+v2 → E1 | 紙 id 去重 → 非 E1 → floor |
| preprint 字串洗 PRIMARY | tier = PREPRINT |
| Strong 純理論 E4/E5 | `consensus_floor_strong` |
| `openalex:W…` 扮 PRIMARY | `primary_source_not_fetchable` |
| `openalex:` + `direct` | `evidence_type_requires_primary_fetchable` |
| Competing 僅兩個 OpenAlex | `competing_needs_distinct_papers` |
| evidence 裡 `confidence: 99` | `declared_confidence` |
| 空白 title / 雙 label | 擋 |
| 全庫 `validate_topic` | 0 violations；build 綠 |

OpenAlex 適配器本身 **不發明燈、DOI 回落 Crossref** —— 作為 courier 的設計是對的。

---

## Round-4 戰果（依嚴重度）

嚴重度以 **#11 自己的承諾** 為準（帳本可審計、編輯 OS 可見、發現不越權），  
不再用「機器必須知真偽」當尺（那條已正式放棄）。

---

### R4-1. 公開面零 `review_state` — 編輯 OS 對讀者隱形

**嚴重度：Critical（#11 產品承諾缺口）**

| 表面 | `review_state` / `human_verified` |
|------|-----------------------------------|
| `dist/claims.json` | **0** |
| `dist/app-data.json` | **0** |
| `web/` · `dist/*.html` | **0** |
| `ClaimFilter` 匯出列 | 無此欄 |
| CLI `editorial` | 有（46 項佇列） |

**PoC：** 庫內 **11 個 ESTABLISHED** 全部 `unverified`，站上仍只顯示 🟢。  
讀者無法區分「形狀合法」與「有人簽核過語義」。

**含義：** 出路 2 的核心交付若只在 CLI，則公開帳本仍是 **單軸共識燈**。  
收窄承諾寫了 Review 層，**渲染/匯出沒接線**。

---

### R4-2. `human_verified` + 任意 `verified_by` → 佇列蒸發

**嚴重度：Critical（編輯 OS 可偽造）**

```text
review_state=HUMAN_VERIFIED, verified_by="attacker"   → validate []
verified_by="x"                                       → validate []
ledger_row.needs_human                                → False
```

無：身份綁定、簽章、append-only 審核事件、時間戳強制、與 challenge 的對立狀態機。  
攻擊者（或草率 PR）可在 data 檔一行把 30 個高燈全部「審完」。

`verified_without_attribution` 只擋 **空字串**，不擋垃圾字串。

---

### R4-3. C1 殘餘 — 真 DOI/arXiv + 假 `direct` → 🟢E1 + `record_ok`

**嚴重度：High（已知結構洞；#11 明文不保證語義）**  
**但在 R4-1 成立時升級：** 讀者以為帳本「已審計」，實際只審計了形狀。

**PoC（已跑）：** 兩個已 cache DOI + 捏造 direct 文案 + ESTABLISHED 全條件 note ≥12 字：

| 檢查 | 結果 |
|------|------|
| `validate_claim(..., check_provenance=True)` | `[]` |
| `derive` | **E1** |
| `record_ok` | **True** |
| `ledger_row.needs_human` | True（僅因 unverified） |
| 若再標 `human_verified` + `verified_by=x` | needs_human **False**，全綠 |

這是「最完整綠路徑」：形狀 + fetch + 地板 + 編輯標記全可對齊，**語義仍可全假**。

---

### R4-4. 敘事層仍為 C1 拋光

**嚴重度：High（產品誤導，非法院洞）**

對 R4-3 claim：`compose` + `check` → **PASS**。  
開場句：「Based on the evidence recorded here … 🟢 Established」+ 複述假 evidence。

敘事法院只查 refs 形狀，不查真偽 —— 與 #11 一致，但 **會放大 R4-1 的隱形問題**。

---

### R4-5. `CHALLENGED` 不降燈、不擋 build

**嚴重度：High（編輯狀態無齒）**

```text
status=ESTABLISHED + review_state=CHALLENGED
  → validate_claim []（形狀過）
  → editorial queue 列出
  → build / 公開 🟢 不變
```

挑戰狀態是 **佇列標籤**，不是共識軸或顯示軸。  
世界開放挑戰（憲法第四章）在資料模型有洞口，在 **讀者路徑沒有後果**。

---

### R4-6. Discovery precheck ≠ build 法院

**嚴重度：High（整合/運維）**

`discovery/precheck._dict_to_claim` **丟棄**：

- `trace_refs`
- `review_state` / `verified_by`
- `status_history` / `competing_models`（部分）

**PoC：** candidate 明明帶 `trace_refs`，precheck 報 `trace_refs_missing`。  
且 `validate_claim` **預設 `check_provenance=False`**，未 fetch 的 DOI 在 dress rehearsal 與 build 行為不一致。

編輯若信 precheck PASS/FAIL，會得到 **錯的 rehearsal**（對高燈永遠缺 trace；對低燈可能假 PASS）。

---

### R4-7. 紙本身份空間分裂 — arXiv id 與 DOI 永不合併

**嚴重度：Medium–High（E1 雙計）**

```text
paper_id_of("arXiv:1906.11238")     → arxiv:1906.11238
paper_id_of("doi:10.1038/…")      → doi:10.1038/…
```

同一工作的 preprint + 正式刊若都當 PRIMARY + direct，**兩個 id → E1**。  
#9 關了「雙 label 同 arXiv」，**沒關「arxiv↔doi 交叉身份」**。

**PoC：** 任一已 cache arXiv + 任一已 cache DOI + 兩條假 direct → `validate` 全綠、`axis=E1`  
（本輪用不同論文示範 id 空間；同文雙入口在邏輯上同構）。

---

### R4-8. 假 analog → Strong + 可 diverges（C3 殘餘）

**嚴重度：Medium–High**

一個已 fetch PRIMARY + `analog experiment` 捏造 + Strong 條件：

| 結果 | 值 |
|------|-----|
| rules | `[]` |
| axis | E3 |
| `diverges` | 依燈×軸規則可 True |

分岔 UI 可被 **偽審慎** 利用。

---

### R4-9. Vacuous note 黑名單可繞

**嚴重度：Medium**

`I say so` / `holds` / 過短 note 會咬；下列 **通過**（≥12 字且不在集合）：

| note | 結果 |
|------|------|
| `because sources` | **[]** |
| `supported by literature` | **[]** |
| `yes it holds` | **[]** |

高燈「可追溯 justification」仍是 **長度 + 弱黑名單**，不是可核對引用。

---

### R4-10. OpenAlex 路徑：安全邊界清楚，污染面在下游人

**嚴重度：Medium（發現層）**

| 行為 | 評估 |
|------|------|
| 有 DOI → `doi:` + Crossref | 正確 |
| 無 DOI → `openalex:` + 本地 cache | 正確 |
| 不判燈 | 正確 |
| `openalex:` 當 PRIMARY / Frontier / Competing 雙源 | **法院擋** |
| abstract inverted index → evidence 全文 | 可灌奇文；`declared_confidence` 若抄進 description 會擋 |
| 期刊質量 / 掠奪刊 | **零檢查**（DOI 形狀即可） |
| candidate `kind` 推成 dataset | 誠實；人若手改 kind 為 peer-reviewed 且 url 仍 openalex → PRIMARY 被擋 |

**真正風險：** 編輯把 OpenAlex abstract **手改成 `direct observation` 並換上兩個真 DOI** —— 回到 R4-3。  
適配器不是洞；**人填 type 才是根**（舊 C10）。

---

### R4-11. 軸仍由人填 `Evidence.type` 決定（C10 根因）

**嚴重度：High（結構，#11 未動）**

`derive` 只讀 type / tier / paper_id。  
「證據軸機械湧現」= **對人填欄位做純函數**，不是對 PDF 語義。

出路 1 已承認；若 README/UI 仍寫「Nobody fills it in」而無「type 是編輯主張」，仍屬文案風險。

---

### R4-12. 編輯佇列不進 build gate（by design，仍有產品代價）

**嚴重度：Medium（運維誠實）**

A11 明文：高燈未 verified **不違憲**（避免一夜炸庫）。  
結果：

```text
editorial queue ≈ 46（高燈未審 ~30 + competing 等）
validate_topic / build     = 全綠
```

這是正確的 **遷移策略**；若長期不消化佇列，公開站 = **永久「形狀已審、語義未審」庫**，且因 R4-1 讀者看不出。

---

## 嚴重度總表（#11 承諾尺）

| ID | 標題 | 攻擊成本 | #11 後 |
|----|------|----------|--------|
| **R4-1** | 公開面無 review_state | 0（現況） | **開 · Critical** |
| **R4-2** | fake human_verified | 改一字串 | **開 · Critical** |
| **R4-3** | C1 真源假 direct | 2 fetchable | **開 · High**（語義殘餘） |
| **R4-4** | 敘事拋光 C1 | 同左 | **開 · High** |
| **R4-5** | CHALLENGED 無顯示後果 | 改 enum | **開 · High** |
| **R4-6** | precheck 丟欄位 / 無 provenance | 用 discovery | **開 · High** |
| **R4-7** | arxiv↔doi 身份分裂 | 2 endpoint | **開 · Med-High** |
| **R4-8** | 假 analog Strong | 1 fetchable | **開 · Med-High** |
| **R4-9** | 弱 vacuous note | 低 | **開 · Medium** |
| **R4-10** | OpenAlex 下游人填 | 編輯 | **邊界 OK / 下游開** |
| **R4-11** | type 決定軸 | 結構 | **開 · High 根因** |
| **R4-12** | queue 不閘 build | by design | **Med 產品債** |

---

## 與 Round 3 對照

| R3 | #10/#11 後 |
|----|------------|
| C1 真源假 direct | **仍開**（語義） |
| C2 敘事 | **仍開** |
| C3 假 analog | **仍開** |
| C4 claim 略 provenance | build 已合；**precheck 仍裂**（R4-6） |
| C5 假 Competing camps | 部分關（需 2 paper id）；camp 名仍可假 |
| C6 note 自證 | 部分關（黑名單）；R4-9 繞過 |
| C7 圖邊 | 未本輪重測；disclaimer 仍在 |
| C8 低燈灌水 | by design 寬 |
| C9 SECONDARY direct | **#10 關**（`evidence_type_requires_primary_fetchable`） |
| C10 type 決軸 | **仍開** |
| — | **新：** R4-1/2/5 編輯 OS 表面與偽造 |

---

## 建議修補順序（只排序，不開 STRATEGY 文）

1. **P0 可見性：** `claims.json` / app-data / 卡片 UI 輸出 `review_state`（+ 高燈未 verified 徽章）。沒這步，#11 對公眾是假的。  
2. **P0 不可偽造的 verified：** `verified_by` 最低要求（非空 + 最小長度/格式）+ **append-only 審核事件**（誰/何時/哪個 claim）；理想：與 git author 或 challenge issue 連結。  
3. **P1 precheck 對齊 build：** `_dict_to_claim` 帶 `trace_refs`；`check_provenance=True`（或報告分兩欄 shape vs fetch）。  
4. **P1 CHALLENGED 顯示：** 燈旁挑戰標、或 feed/API 強制欄位。  
5. **P2 身份：** OpenAlex/Crossref 回傳的 DOI↔arXiv 對照寫入 `paper_id` 合併（降 R4-7）。  
6. **P2+ 語義：** 仍不要假裝機器能關 C1；用「未 verified 不可稱 ledger-complete」產品規則消化 R4-3。

---

## 本輪結論

| 層 | 狀態 |
|----|------|
| 形狀法院（#7–#10） | **硬**，回歸綠 |
| OpenAlex courier（#11） | **邊界正確**，不越權 |
| 編輯 OS（#11） | **半成品**：模型+CLI 有，**公開帳本與防偽沒有** |
| 語義 / C1 | **永開**（已寫進憲法前言）；在 R4-1/2 未修前，讀者會 **誤讀為已人審** |

**最優攻擊組合（一條 PR）：**  
假 direct × 兩真 DOI（C1）→ 標 `human_verified`/`verified_by=bot`（R4-2）→ build 綠 → 公開 🟢 且無 unverified 徽章（R4-1）。

這不是「系統又爛掉」，而是：**#11 把謊話成本從「騙法院」挪到「騙編輯標記 + 讀者」——而標記目前幾乎不設防、讀者目前看不到。**

---

## 閉合狀態（Amendment #12 後）

| ID | 狀態 | 修法 |
|----|------|------|
| R4-1 | **關** | claims.json / app-data / 靜態卡 / app.html 徽章 |
| R4-2 | **關** | verified_by 格式 + note≥12 + verified_at ISO |
| R4-3 | **殘餘** | 語義洞；公開面現標 ○ unverified，偽造 verified 被擋 |
| R4-4 | **關（敘事誠實）** | compose 必述 Editorial mark |
| R4-5 | **關（可見）** | ⚠ challenged 徽章 + 敘事句（仍不炸 build） |
| R4-6 | **關** | precheck 保留欄位 + `check_provenance=True` |
| R4-7 | **關（有 cache DOI 時）** | arXiv Atom `<arxiv:doi>` → 合併 paper_id |
| R4-8 | **緩** | 佇列 reason 強化；不炸 build |
| R4-9 | **關** | vacuous note 黑名單擴充 |
| R4-10–12 | 邊界/by design | 見修正案 #12 |

法源：`docs/amendment-12-r4-editorial-surface.md`
