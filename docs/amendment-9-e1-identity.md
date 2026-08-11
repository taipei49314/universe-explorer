# 憲法修正案 #9 — E1 按論文身份去重；preprint 不得偽升 PRIMARY

> Round-2 紅隊（`docs/redteam-round2-after-a7a8.md`）在 #7+#8 之後仍打穿：  
> (F) 同一 arXiv 兩個 label；(V) v1/v2 兩標籤；(kind) `preprint (peer-reviewed…)` → PRIMARY。  
> 本修正案關閉這三條**廉價假獨立 / 假分級**路徑。  
> **不關：** 兩篇**不同**真 DOI + 假 direct 文案（內容層，需人審）。

## 0. 修正條文

### 0.1 E1 獨立性 = distinct **paper identity**（`axes.py`）

在 amendment-7 的「可抓取 PRIMARY」之上：

- 對每條 direct 所掛來源，取正規化 **paper id**：  
  - arXiv → bare id（去 `vN`）  
  - DOI → lowercase DOI  
- E1 要求：direct ≥ 2 **且** 上述 paper id 的 **distinct 集合 ≥ 2**。

同一論文的兩種寫法（`arXiv:X` 與 `https://arxiv.org/abs/X`，或 `Xv1`/`Xv2`）只算 **一個** id。

### 0.2 preprint 字樣優先（`model.tier_of`）

若 `kind`（小寫）含 `"preprint"` → **一律 PREPRINT**，不再被後續 `peer-reviewed` 子字串洗成 PRIMARY。

已正式發表且 kind 只寫 `peer-reviewed paper`（不含 preprint 字樣）→ 仍為 PRIMARY。

### 0.3 明確不關

- 兩篇不同真論文 + 虛假 direct 描述 + 勾選 → 仍可能 🟢E1（內容層）。  
- Established note 必填 citation：另案（現庫 44 條 note 無 doi/arxiv 字串，改動面大）。

## 1. 工程

- `provenance.paper_id_of(url_or_id)`（或 axes 內呼叫 arxiv_id_of/doi_of）  
- `axes.derive` E1 計數改 paper id  
- `model.tier_of` preprint 優先  
- 引擎重蓋章；`test_epistemic_adversary` 擴 F/V/kind  
- 現庫量測：無 E1 claim 僅因雙 label 同一 id 而降級

## 2. 驗收

1. F/V PoC → 不得 E1；若 status=Established → `consensus_floor_established`。  
2. `tier_of("preprint (peer-reviewed later)") == "PREPRINT"`。  
3. 全庫 build/tests 綠。
