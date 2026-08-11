# Universe Explorer 紅隊攻擊報告

> **目標：** [taipei49314/universe-explorer](https://github.com/taipei49314/universe-explorer)  
> **定位：** 誠實區分已知與未知的科學知識系統（憲法門禁 + 雙軸 + 靜態站）  
> **方法：** 讀核心引擎 / 憲法 / 既有 `TESTING-BLIND-SPOTS.md` + **可執行 PoC**（本機 Python）  
> **日期：** 2026-08-11  
> **HEAD：** `main` @ `ac5d758`（含 user-path blind spots 修復）  
> **修訂：** 2026-08-11 — **Amendment #7** 關閉本報告 P0 最短路徑（見 `docs/amendment-7-endpoint-honesty.md`）。  
> 驗證：`python run_tests.py` 全綠；紅隊 PoC 現為 `primary_source_not_fetchable` + **非 E1**。

---

## 一句話

系統在 **「格式合法、可審計、可推翻」** 上很硬；  
在 **「內容真的對、燈號真的該亮」** 上，仍信任 **作者勾選共識燈**。  

**已關閉（#7）：** 用虛 PRIMARY + example.com 洗出 **E1**；arXiv HTTPS 跳過 fetch；空白 title / 重複 label。  
**已關閉（#8）：** 🟢 Established 無 E1；🔵 Strong 掛 E4/E5（純理論/無證據）。  
**仍開：** note 文案真偽（`I say so` 在 **有 E1 時**仍可過）；direct type 人標以湊 E1（需兩次可抓 PRIMARY）；敘事/圖邊語意。

---

## 攻擊者模型

| 角色 | 能力 | 目標 |
|------|------|------|
| **惡意/偷懶維護者** | 改 `data/*.py`、能過 CI | 把弱知識洗成強燈 / 高證據軸 |
| **有 PR 權的人** | 送 claim PR | 同上，審稿若只看「有過 gate」 |
| **外部挑戰者** | issue / challenge 模板 | 推翻錯誤燈（流程上有，證據壓力在人） |
| **讀者** | 靜態站 | 被 UI 的燈與 E1 誤導信任 |

憲法自承：機器 **排除** 違憲形狀，**核准永遠是人**。紅隊因此打 **「人 + 機械軸的縫」**。

---

## 系統實際守住什麼（先講綠隊）

| 守住 | 機制 |
|------|------|
| 無證據的「已知」 | `unsupported_claim` |
| 證據無 source / dangling ref | validator |
| 假信心百分比 / 數字化 open questions | 文字掃描 |
| 燈號條件欄位形狀 | `status_reason` 對 `STATUS_CONDITIONS` |
| arXiv / `doi:` **且寫成規範字串** 的 cite⇒fetch | provenance hash + 重解析 |
| 敘事句無 ref | narrative `check()` 整段 withhold |
| 提案不自動入庫 | discovery / drafts 邊界 |
| 引擎暗改 | `engine_hashes` + amendment 流程 |
| 使用者搜尋/中文/H0/challenge 契約 | 2026-08-11 已修一批（見 TESTING-BLIND-SPOTS） |

這些讓它 **不像** 一般 LLM 幻覺百科。  
問題在下一層：**合法通過 ≠ 認識論誠實**。

---

## 10 個可打穿點（按嚴重度）

### 1. 證據型別是作者標籤 → 可把理論洗成「direct」→ E1/E2

**嚴重度：Critical（認識論）**  
**狀態：E1 路徑已關（amendment-7）；direct 假標 → 最多 E2 仍開**

`axes.derive` 只看 `Evidence.type` 是否 ∈ 受控詞彙，**不看論文內容**。

```text
type="direct observation" + description 任意 + source_ref 合法
→ 計入 direct 計數
```

PoC（本機已跑）：兩個 `kind` 含 `peer-reviewed`、URL 為 `https://example.com/...`、type 全標 direct：

| 結果 | 值 |
|------|-----|
| `derive` | **E1_MULTIPLE_DIRECT** |
| `validate_claim` | **[] 零違規** |
| `diverges` | **False**（高共識 + 假 E1 對齊） |
| status | **ESTABLISHED**（四個 condition 全 `holds=True, note="I say so"`） |

**攻擊：** 把 speculative 理論寫成兩條「direct observation」+ 兩個 PRIMARY kind 字串 → 站上 **雙軸都最強**。

**緩解方向（難、但對品類致命）：**  
- evidence type 改 **由來源類型推導** 或需 machine-checkable 標註；或  
- E1 強制 arXiv/DOI **且** fetch 存在，禁止「無 endpoint 的 PRIMARY」進 E1；或  
- 高燈 + E1 必須 challenge / 第二人簽核欄位。

---

### 2. cite⇒fetch 只認 `arXiv:` / `doi:` 前綴 → URL 形狀整段豁免

**嚴重度：Critical（Data 層誠實豁免被擴大）**  
**狀態：已關（amendment-7）** — URL / 裸 DOI 正規化後進同一四規則。  
**修後：**

```text
arxiv_id_of("https://arxiv.org/abs/1906.11238")  →  1906.11238
arxiv_id_of("arXiv:1906.11238")                  →  1906.11238
```

**攻擊：** 來源寫成 https://arxiv.org/abs/…. 或裸 DOI `10.1038/...`（無 `doi:`）→ **不進 provenance 四規則**，同時 kind 可寫 `peer-reviewed` 餵 E1。

**緩解：** normalize URL → arXiv id / DOI；任何可解析 endpoint 都 cite⇒fetch。

---

### 3. 共識燈 = 勾選 + 非空 note（自證入格）

**嚴重度：Critical（產品核心承諾）**

`status_reason` 只檢查：

- condition key ∈ 該燈表格  
- `note` 非空白  
- mode=all 時全部 `holds=True`  

**不檢查：** 教科書是否真寫、是否真無競爭理論、note 是否可驗證。

`note="I say so"` / `note="because"` 對 Established **合法**（與 PoC 一致）。

**攻擊：** 任意 claim 升 🟢，只要編四段 note。  
**挑戰流程**存在，但 **gate 不擋**；公開站讀者先看到燈。

**緩解：**  
- note 必須含 checkable ref（doi/arxiv/頁碼）且可解析；或  
- Established/Strong 強制「至少 N 個 PRIMARY + fetch」機械前置（與共識軸分離的 hard floor）。

---

### 4. PRIMARY 靠 kind 子字串 → 標籤遊戲

**嚴重度：High**  
**已記錄：** TESTING-BLIND-SPOTS §1 `tier_of`

| kind | `tier_of` |
|------|-----------|
| `peer-reviewed paper` | PRIMARY |
| `collaboration result (peer-reviewed, …)` | PRIMARY |
| `peer reviewed`（空格） | **None → 違憲** |
| `journal article` | **None** |
| `preprint (arXiv)` | PREPRINT |
| `preprint later peer-reviewed` | **PRIMARY**（含 peer-reviewed） |

**攻擊 A：** 未審 preprint 寫進 kind 字串 `… peer-reviewed …` → 升 PRIMARY → 助 E1。  
**攻擊 B：** 合法期刊只寫 `journal article` → 建置失敗或被迫改字串（誤傷誠實作者）。

**緩解：** 結構化 `Source.tier` 枚舉（人填）+ 與 url 類型交叉檢查；子字串表降級為 hint。

---

### 5. 無 endpoint 來源完全豁免 fetch → 教科書/獎項可虛標

**嚴重度：High（設計誠實，但可濫用）**

provenance 對非 arXiv/doi **不檢查存在性**。  
`kind=textbook` / `prize citation` 可任意 label + url。

**攻擊：** 兩本假教科書 + 假 direct → 至少 E2；再配自證 Established。  
（E1 要 PRIMARY；textbook 是 SECONDARY → 假 E1 要用 peer-reviewed 字串，見 #1+#4。）

**緩解：** SECONDARY 也要可驗證識別符或「unverified secondary」顯示標記。

---

### 6. E1「獨立」= 不同 source **label**，非獨立實驗

**嚴重度：High**

```python
len(primary_direct_sources) >= 2  # set of source_ref labels
```

同一合作組兩篇 ApJL、或同一觀測兩次引用，只要兩個 label + 兩個 PRIMARY → **E1**。

**攻擊：** 單一線索拆成兩條 Evidence / 兩個 Source 標籤。

**緩解：** 獨立性需作者宣告 `independence_group` 或機構欄；或 E1 文案改為「≥2 PRIMARY records」而非「independent replications」。

---

### 7. 空白標題 / 重複 source label（gate 漏）

**嚴重度：Medium（資料品質）**  
**狀態：已關（amendment-7）** — `empty_title` / `duplicate_source_label`  
**修後：** `title="   "` → `empty_title`

**攻擊：** 垃圾 claim 仍進 dist；重複 label 時 dangling/唯一性語意混亂。

**緩解：** amendment：`title.strip()` 非空；source labels 唯一。

---

### 8. 共享來源圖 / 機械邊 ≠ 認識論連結

**嚴重度：Medium（UI 敘事）**

`shared_source` / `all_links` 可產生跨域邊與「188 edges」觀感。  
**攻擊：** 讀者以為領域已整合；實為引用重疊。  
README 有說明，但 **epistemic_map 視覺權重大**。

**緩解：** 邊預設灰標「shared citation only」；作者邊與機械邊強制分色（若尚未）。

---

### 9. 敘事層：refs 對 ≠ 句子忠於證據

**嚴重度：Medium（若開 LLM 敘事）**

`check()` 要求句句有可解析 ref + 開場公式；**不比對**句子是否扭曲 evidence 原文。

**攻擊：** LLM 或人寫「觀測已確認 X」掛上只支持「上限」的 source → 過法院、誤導讀者。

機械 `compose()` 較安全；**LLM 路徑**是主要風險面。

**緩解：** 敘事句限制為 evidence 子字串 / 模板槽；LLM 輸出 diff 必經人審 UI（流程已有草稿夾則強化不可跳過）。

---

### 10. 前端與流程殘餘（使用者信任）

| 項 | 嚴重度 | 說明 |
|----|--------|------|
| `?c=missing` 靜默 | Med | TESTING-BLIND-SPOTS U8 |
| health 文案路徑 | Low | U10 |
| 挑戰是人審 | 結構 | 惡意 PR 若合入，站上先錯後糾 |
| engine 凍結修洞慢 | 治理 | 已知洞長期 Open |
| Pages 靜態 | 部署 | 無「讀者回報已改燈」即時性 |

---

## 攻擊配方（惡意 PR 最短路徑）

```text
1. 新建 claim，status=ESTABLISHED
2. status_reason：四條件 holds=True，note 任意非空
3. sources：兩個 kind 含 "peer-reviewed"，url_or_id=https://example.com/a|b
   （不要用 arXiv: / doi: 前綴，避免 fetch）
4. evidence：兩條 type="direct observation"，source_ref 對上
5. python build.py --check  →  PASS
6. 雙軸顯示：🟢 + E1，diverges=false
```

**這條路徑不需要偽造 cache、不需要改引擎、不需要 LLM。**

---

## 與「誠實」承諾的對照

| 對外句子 | 紅隊讀法 |
|----------|----------|
| 誠實區分已知與未知 | **格式上**區分；**內容真值**靠編輯誠信 |
| 證據軸無人填寫 | 型別與來源 **kind 字串** 仍是人填 → 軸被上游污染 |
| cite ⇒ fetch | 僅規範 id 形狀；URL/假 PRIMARY 可逃 |
| 可被第三人推翻 | 對；但 **默認展示** 已賦權錯誤燈 |
| AI 不宣布事實 | 機械敘事尚可；LLM + 合法 ref 仍可 overlay |

**不是專案失敗**——是 **威脅模型應寫成：信任邊界在「有權合併 data 的人」**。

---

## 優先修復（建議）

| 優先 | 項 | 對應 |
|------|-----|------|
| P0 | URL/DOI 正規化進 cite⇒fetch | #2 |
| P0 | E1 禁止「無 fetch 的 PRIMARY」或禁止 example-like host | #1 #2 #5 |
| P0 | Established/Strong 機械地板（最低證據軸或 PRIMARY+fetch 數） | #3 |
| P1 | `tier_of` → 結構化 tier 或修 keyword 表 + 測試變體 | #4 |
| P1 | title 非空白、source label 唯一 | #7 |
| P1 | E1 文案/規則：label 數 ≠ 獨立複製 | #6 |
| P2 | 圖邊語意、缺失 deep-link、敘事槽位化 | #8 #9 #10 |
| 治理 | 修 validator/axes 走 amendment，不要無限拖 Open | engine_hashes |

---

## 量測建議（回歸）

在 `test_adversarial_*.py` 或新 `test_epistemic_adversary.py`：

1. **fail：** example.com + peer-reviewed kind + 雙 direct + Established 應 **不得** E1 或不通過 gate（選定政策後）  
2. **fail：** `https://arxiv.org/abs/...` 必須觸發 unfetched 或自動正規化後檢查  
3. **fail：** `title="   "`  
4. **fail：** 重複 source labels  
5. **document：** 兩 label 同合作組仍 E1 為已知限制（或關閉）

---

## 結論

| 問題 | 答案 |
|------|------|
| 能防 LLM 亂寫進庫？ | **能擋大半形狀與無來源**；擋不住「合法假證據」 |
| 能防惡意維護者洗燈？ | **基本上不能**（PoC 全綠） |
| 比一般科普站誠實？ | **是**——雙軸分岔、挑戰模板、fetch 對規範 id 仍強 |
| 頂級下一步？ | 把 **Data/Evidence 上游可偽造面** 收到與 validator 同級，而不是再加 UI |

> **Universe Explorer 的護欄守的是「記錄紀律」；攻擊面在「紀律允許的謊言」。**  
> 要升維，必須讓 **E1 / Established 無法僅靠 kind 字串與勾選** 達成。

---

## 附錄：本機 PoC 指令

```bash
cd universe-explorer
python -c "
from universe_explorer.model import *
from universe_explorer.validator import validate_claim
from universe_explorer.axes import derive, diverges
from universe_explorer.provenance import arxiv_id_of

c = Claim(
    id='poc', title='Fake established',
    status=Status.ESTABLISHED,
    sources=[
        Source('a', 'https://example.com/1', 'peer-reviewed paper'),
        Source('b', 'https://example.com/2', 'peer-reviewed paper'),
    ],
    evidence=[
        Evidence('direct observation', 'Invented 1', 'a'),
        Evidence('direct observation', 'Invented 2', 'b'),
    ],
    status_reason=[
        ConditionAssessment('multiple_independent_replications', True, 'I say so'),
        ConditionAssessment('accepted_in_mainstream_textbooks', True, 'I say so'),
        ConditionAssessment('no_mainstream_competing_theory', True, 'I say so'),
        ConditionAssessment('no_recent_major_refutation', True, 'I say so'),
    ],
)
print(derive(c).strength, validate_claim(c), diverges(c))
print('url bypass', arxiv_id_of('https://arxiv.org/abs/1906.11238'))
print('blank title', validate_claim(Claim(
    id='t', title='   ', status=Status.SPECULATIVE,
    sources=[Source('s','x','textbook')],
    evidence=[Evidence('theoretical derivation','d','s')],
    status_reason=[ConditionAssessment('pure_theoretical_derivation', True, 'n')],
)))
"
```

（SPECULATIVE 需符合 mode=any 的條件集合——以你本機 `STATUS_CONDITIONS` 為準；空白標題案例見正文用 STRONG 的 PoC。）
