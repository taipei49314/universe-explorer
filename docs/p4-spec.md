# P4 Spec — 跨領域(Ocean Explorer)

> 定位:Roadmap P4,「引擎 vs demo」的終極測試。
> 命題:換掉 Data 層的題材,同一套認識論引擎長出第二個領域,**核心引擎零改動**。

---

## 0. 「核心引擎零改動」的精確定義

零改動範圍(動一行即 P4 FAIL):
`model.py`(schema + 五格條件)、`validator.py`(憲法規則)、`axes.py`(證據軸推導)、
`provenance.py`(P1 規則)、`proposals.py`(提案邏輯)、`watch.py`(diff/擋關邏輯)。

允許改動範圍(誠實列舉,不偷渡):
- `data/`:新增海洋題材資料檔 + 一個 topics 註冊表(資料層本來就是要換的)。
- 入口與呈現:`build.py` / `render.py` / 各 CLI 的 `main()` 從單一 topic 改為
  走註冊表(這是接線,不是引擎)。

## 1. 出處紀律(本版最重要的憲法應用)

- 海洋科學來源多不在 arXiv(Science/Nature 紙本、Ocean Science 等)——
  **每一筆出處在寫入前必須上網核實**(標題、作者、期刊、年份、DOI)。寧可少填,不編。
- 非 arXiv 來源沿用 P1 的誠實豁免(無可抓取 endpoint);
  海洋資料庫的自動抓取 adapter 是 P4 之後的工程,本版不做。

## 2. 海洋題材的 claim 規劃(壓測目標)

| Claim | 預期燈號 | 壓測什麼 |
|---|---|---|
| 熱泉生態系存在 | 🟢 Established | 地基:多重獨立直接觀測(E1) |
| AMOC 減弱中 | 🟡 Competing | **首次用真實資料跑通 competing_models 欄位**(銷 R4):代理重建 vs 直接觀測兩派 |
| CCZ 深海生物多樣性大多未描述 | 🟠 Frontier | 樣本不足 + 文獻快速增長 |
| 深海「暗氧」產生 | 🔴 Speculative | 有觀測但主流未接受 —— 壓測「單線觀測 × 低共識」的反向組合 |

四格四種燈號 + 一個 Competing,知識形狀完整。

## 3. P4 驗收(先於實作)

1. **核心引擎零改動**:§0 列的六個檔案 diff 為零(以檔案雜湊驗證)。
2. **出處全數核實**:每筆 source 有真實可查的出處(DOI/期刊卷期),核實過程留記錄。
3. **兩個 topic 並存**:index 頁列出兩個領域;各自的知識形狀一眼可見。
4. **全部既有把關照跑**:v0 憲法 + 受控詞彙 + P1 + P3 對兩個 topic 一體適用,零違憲。
5. **R4 銷案**:competing_models 以真實學界分歧(AMOC)跑通,含兩派的支持/反對/侷限。
6. **P3 事件實證**:新增 topic 對 watch 產生 claim_added 事件後 commit —— 用真實變化
   驗證變化偵測管線。
