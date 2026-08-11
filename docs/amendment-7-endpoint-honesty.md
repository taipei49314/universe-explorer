# 憲法修正案 #7 — Endpoint 誠實、E1 不可虛標、記錄最低衛生

> 紅隊 2026-08-11（`docs/redteam-universe-explorer-2026-08-11.md`）證明：  
> 兩個 `kind` 含 `peer-reviewed`、URL 為 `https://example.com/...`、evidence type 標  
> `direct observation`、status_reason 勾選 `I say so`，可同時得到 **🟢 Established + E1**  
> 且 `validate_claim` 零違規。另：`https://arxiv.org/abs/...` 不觸發 cite⇒fetch。  
> 本修正案關閉這條「合法假證據」最短路徑，不宣稱解決「人勾選共識燈」的全部問題。

## 0. 修正條文

### 0.1 cite ⇒ fetch 的 endpoint 識別（`provenance.py`）

下列 **任一** 寫法視為有 endpoint，適用既有 arXiv / DOI 四規則：

| 形狀 | 正規化結果 |
|------|------------|
| `arXiv:1906.11238` | arXiv id（既有） |
| `https://arxiv.org/abs/1906.11238`（http/https、`pdf/`、`html/`、可帶 `vN`） | 同上 |
| `doi:10.xxxx/...` | DOI 小寫（既有） |
| `https://doi.org/10.xxxx/...`、`dx.doi.org/...` | 同上 |
| 裸 `10.xxxx/...`（整段像 DOI） | 同上 |

**誠實豁免不變：** 教科書、獎項引文、**無法解析出 arXiv id / DOI** 的紙本條目。  
把紙本 PRIMARY 升格時，應改寫為 `doi:`（或 arXiv）並 fetch —— 見 0.3 與 data 同步。

### 0.2 證據軸 E1（`axes.py`）

E1 條件收緊為：

- ≥2 條 `direct observation`，且  
- 所掛來源中，**可解析 endpoint（arXiv 或 DOI）且 `tier_of` = PRIMARY** 的 **distinct source labels ≥ 2**。

僅有 `peer-reviewed` 字串、無可抓取 id 的來源，**不得**計入 E1 的 PRIMARY 集合。  
（E2 仍可由單條 direct 達成，含歷史紙本；E1 的「多重獨立」必須可機器核對出處。）

### 0.3 PRIMARY 必須可抓取（`validator.py`）

`tier_of(kind) == PRIMARY` 的來源，其 `url_or_id` 必須解析出 arXiv id 或 DOI。  
否則 `primary_source_not_fetchable`。  
法理：PRIMARY 宣稱「已審主文獻」卻無可核對 endpoint，等於把分級變成字串化妝。

### 0.4 記錄衛生（`validator.py`）

| 規則 | 內容 |
|------|------|
| `empty_title` | `title.strip()` 為空 |
| `duplicate_source_label` | 同一 claim 上 source label 重複 |

### 0.5 分級關鍵字（`model.py`，小修）

`SOURCE_TIERS` PRIMARY 增加：`peer reviewed`（空格）、`journal article`。  
（避免誠實作者被 `unclassifiable` 誤傷；E1 仍受 0.2 約束。）

## 1. 工程

- 引擎：`provenance.py`、`axes.py`、`validator.py`、`model.py` → 重新蓋章 `engine_hashes.json`。  
- Data：四個紙本 PRIMARY 改寫 `doi:` 並 `crossref_fetch` 入庫。  
- LAWS 登記新規則；`test_validator` 法源集擴充。  
- 新測試：`test_epistemic_adversary.py`（紅隊 PoC 必須咬人）。

## 2. 明確不關（殘餘）

- 共識燈仍可由人勾選；本修正案不驗證 note 內容真偽。  
- `direct` type 仍可由人標在理論上 → 最多 E2（若來源可抓），**不再**單靠虛 PRIMARY 得 E1。  
- 敘事句與 ref 一致性、共享引用圖語意：後續修正案。

## 3. 驗收

1. 紅隊 PoC（example.com + peer-reviewed + 雙 direct + Established）→ **不得** E1；PRIMARY 無 endpoint → gate 失敗。  
2. `https://arxiv.org/abs/...` 未 fetch → `arxiv_source_unfetched`。  
3. 空白 title、重複 label → 對應違規。  
4. 全庫 `build.py --check` / `run_tests.py` 綠；引擎哈希與修正案一致。
