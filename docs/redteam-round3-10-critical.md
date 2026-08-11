# Universe Explorer 紅隊 Round 3 — 10 Critical

> **前提：** Amendment **#7 + #8 + #9** 已落地（`run_tests.py` 全綠）  
> **方法：** 可執行 PoC（2026-08-11）  
> **目標：** 在「形狀門禁已抬高」之後，找出仍能破壞產品承諾的 **10 個 Critical**

---

## Round-3 一句話

**廉價假路徑（example.com、雙 label、preprint 洗 PRIMARY、無 E1 掛 🟢）已死。**  
**Critical 戰線移到：真 endpoint + 假語義，以及「法院只審形、不審義」。**

---

## 已確認仍關閉（回歸）

| 攻擊 | 結果 |
|------|------|
| example.com 假 PRIMARY | BLOCK |
| 同一 arXiv 兩 label / v1+v2 | BLOCK（E2 → floor） |
| preprint 升 PRIMARY | PREPRINT |
| Strong 純理論 | BLOCK |
| 空白 title | BLOCK |

---

## 10 Critical

嚴重度以 **產品承諾（誠實區分已知/未知）** 為準，不是 CVSS 遠端 RCE。

---

### C1. 真論文 + 假 direct 文案 → 🟢 + E1 全綠

**嚴重度：Critical**  
**PoC：** 兩個已 cache 的 PRIMARY（例如 `arXiv:1906.11238` + `arXiv:2311.08680`，或兩個真 DOI），`type=direct observation`，描述任意捏造，`status_reason` 全 `holds` + `I say so`。

| 檢查 | 結果 |
|------|------|
| `validate_claim` | `[]` |
| `validate_provenance` | `[]` |
| `derive` | **E1** |
| status | **ESTABLISHED** |

**含義：** cite⇒fetch 只證明「DOI/arXiv 存在」，不證明「支持本 claim」。  
**這是 #7–#9 之後最完整的綠路徑。**

---

### C2. 敘事法院對 C1 放行（機械 compose + check）

**嚴重度：Critical**  
**PoC：** 對 C1 的 claim 跑 `compose` + `check` → **不 raise**。

敘事句 refs 合法、開場公式合法，會把假 evidence **整理成合法旁白**，讀者更像「系統已審」。

---

### C3. Strong × 假 analog → 合法 🔵 且可標 diverges

**嚴重度：Critical**  
**PoC：** 一篇真 DOI + `type=analog experiment` + 捏造 lab 描述 + Strong 三條件勾選。

| 結果 | 值 |
|------|-----|
| rules | `[]` |
| axis | **E3** |
| diverges | **True**（若共識高） |

**含義：** 分岔 UI 本意是誠實（如 hawking）；攻擊者可 **偽造分岔** 顯得「審慎」，實為假 analog。  
比 C1 略「便宜」（只需一個 fetchable 源）。

---

### C4. claim 層與 build 層分裂 — 未 fetch 也可「長得像 E1+🟢」

**嚴重度：Critical（整合/API）**  
**PoC：** 兩 `arXiv:0000.*` 未 fetch：

- `validate_claim` → `[]`，`derive` → **E1**  
- `validate_provenance` → `arxiv_source_unfetched`

若任何 UI/CLI/草稿路徑 **只跑 validator 不跑 provenance**，會展示假通過。  
完整 `build.py` 會擋；**信任邊界取決於呼叫方**。

---

### C5. Competing 燈 = 兩個假 camp 名稱即可

**嚴重度：Critical（認識論展示）**  
**PoC：** Competing + 兩個 `CompetingModel("CampA"/"CampB")` + 三條件 `holds` + 一句 indirect。

`validate_claim` → **[]**。  
系統會展示「領域分裂」，但 camp 可完全虛構。  
（與 Established 不同：不需 E1，門檻更低。）

---

### C6. 共識 note 自證在「有 E1 形」時完全合法

**嚴重度：Critical（與入格條件敘事衝突）**  
條件名為 `multiple_independent_replications` 等，但 **note 可為 `I say so`**。  
#8 只要求軸到 E1，**不要求 note 可核對**。

讀者以為每條 condition 有追溯；實為勾選+任意字串。

---

### C7. 圖 / 共享來源膨脹認識論連結

**嚴重度：Critical（產品誤導）**  
量測（當前庫）：`shared groups ≈ 2`，graph **~188 edges**，**~8 cross-domain**。

共享引用 ≠ 主張一致。  
README 有說明，但 **epistemic_map 視覺權重** 仍可讓人以為跨域已「連成一張知識網」。  
攻擊：灌引用重疊的弱 claim → 圖更「豐富」、信任感上升。

---

### C8. Frontier / Speculative 灌水稀釋「未知」的信號

**嚴重度：Critical（若規模被當可信度）**  
Frontier + 理論 + 任意 note「new discovery」；Speculative + textbook：**故意易過**。

若站上以 claim **數量** 或主題覆蓋示強，攻擊者可灌水拉高 inventory，  
稀釋真正 Established 的信噪比。  
憲法不擋——但是 **產品度量可被刷**。

---

### C9. SECONDARY（獎項等）可標 `direct observation` 進入證據軸

**嚴重度：Critical（軸污染）**  
**PoC：** `prize citation` + `type=direct observation` → tier SECONDARY，**axis E2** 可過 Strong（再配其他證據或單 E2/E3 規則）。

獎項頁不是觀測數據；標成 direct **合法**。  
E1 仍要求 PRIMARY，但 **E2/E3 故事與 UI 文案** 可被污染。

---

### C10. 雙軸「機械湧現」被上游人填欄位完全決定

**嚴重度：Critical（承諾層）**  
對外：`Evidence axis — Nobody fills it in — derived`。

實作：`derive` 只讀人填的 `Evidence.type` + `Source.kind` + `url_or_id`。  
**人填 type=direct 即改變軸**；機器不驗證 type 是否名副其實。

#7–#9 限制了 **誰能當 PRIMARY / 幾個 paper id**；  
**沒有限制 type 是否說謊。**  
這是整條「確定性從證據湧現」承諾的根洞。

---

## 嚴重度總表

| ID | 標題 | 攻擊成本 | #7–9 後 |
|----|------|----------|---------|
| **C1** | 真論文 + 假 direct → 🟢E1 | 需 2 個已 fetch PRIMARY | **開** |
| **C2** | 敘事對 C1 背書 | 同 C1 | **開** |
| **C3** | 假 analog → 🔵 + diverges | 1 個 fetchable | **開** |
| **C4** | claim 層略過 provenance | 呼叫面錯誤 | **開** |
| **C5** | 假 Competing camps | 極低 | **開** |
| **C6** | note 自證 | 極低（有 E1 時） | **開** |
| **C7** | 圖邊誤導 | 編輯/灌水 | **開** |
| **C8** | 低燈灌水 | 極低 | **開**（by design 寬） |
| **C9** | SECONDARY 當 direct | 低 | **開** |
| **C10** | 軸由 type 字串決定 | 結構 | **開**（根因） |

---

## 與前幾輪關係

```text
Round1: 便宜假 PRIMARY / URL 豁免 / 無地板
   ↓ #7 #8 #9
Round2: 雙 label、preprint 洗分級、內容假
   ↓ #9 關雙 label / preprint
Round3: 內容假 + 敘事背書 + 分岔偽造 + 圖/灌水/type 根因
```

**進步真實；Critical 沒消失，只是變貴、變「像真的」。**

---

## 建議修復優先（若繼續）

| 順位 | 對策 | 擋 |
|------|------|-----|
| P0 | `direct`/`analog` **僅允許**掛在 PRIMARY+fetchable（禁 prize/textbook 當 direct） | C9 部分、抬 C3 成本 |
| P0 | 入庫路徑 **強制** `validate_claim+provenance` 單一 API | C4 |
| P1 | Established 每條 holds note 須含 paper id 或「unverified」標記 | C6 |
| P1 | 圖預設隱藏機械 shared-source 邊 / 強標 disclaimer | C7 |
| P2 | Competing 需 ≥2 個 **不同 paper id** 的來源 | C5 |
| 永不單靠機器 | C1/C2/C10 語義 — 人審、挑戰、抽樣重讀 | 內容層 |

---

## 結論

在 #7–#9 之後再攻擊一次：

- **能擋：** 無 endpoint、假獨立 label、無 E1 掛 🟢、純理論 🔵。  
- **不能擋：** **有真文獻身份、無真語義對齊** 的記錄。  

**10 個 Critical 的共同根：法院審「形狀與身份」，不審「句子是否被文獻支持」。**  
這對「誠實區分已知與未知」產品是 **結構上限**；要再升維必須加 **人審工作流強制** 或 **引用片段/頁碼級約束**，而不是再加一層 type 枚舉。

---

## Amendment #10 閉合狀態（同日落地）

| ID | #10 狀態 |
|----|----------|
| C1 | **部分** — vacuous note / 缺 `trace_refs` 擋便宜勾選；**兩真 paper + 長 note + trace_refs + 假 direct 文案仍開**（內容層） |
| C2 | **部分** — 敘事仍只審 ref；C1 形過則敘事過 |
| C3 | **關（抬成本）** — analog/direct 僅 PRIMARY+fetchable；假 prize analog 擋 |
| C4 | **關** — `validate_topic` / build 一律含 provenance |
| C5 | **關** — Competing 需 ≥2 distinct paper ids |
| C6 | **關** — vacuous note 擋；`trace_refs` 強制錨點 |
| C7 | **關（展示）** — epistemic_map disclaimer |
| C8 | **關（部分）** — Frontier 需 fetchable source；Speculative 仍寬 |
| C9 | **關** — SECONDARY 不得掛 direct/analog |
| C10 | **部分** — type 仍人填，但 direct/analog 入口收窄 |

`run_tests.py` 全綠。詳見 `docs/amendment-10-critical-closures.md`。
