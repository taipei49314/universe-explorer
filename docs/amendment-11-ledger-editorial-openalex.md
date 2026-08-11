# 修正案 #11 — 帳本定位、編輯 OS 標記、OpenAlex 適配

## 0. 產品定位（收窄承諾）

Universe Explorer **不是**「機器已分清科學真偽」。

它是：

> **可審計的科學主張帳本（auditable scientific claim ledger）**  
> + **憲法門禁的編輯作業系統（editorial OS）**  
> + **發現入口（含 OpenAlex）→ 人審入庫**

| 機器保證 | 機器不保證 |
|----------|------------|
| 來源可抓、燈↔軸地板、無靜默改燈、trace_refs | 句子是否被文獻語義支持（C1 殘餘） |
| 記錄形狀合法（record_ok） | 共識燈「政治正確」 |

## 1. 審閱標記（Claim 新欄位）

```text
review_state: unverified | human_verified | challenged
verified_by: str (optional, empty default)
verified_note: str (optional)
```

- 預設 `unverified`（現有 99 claims 無需改檔）。  
- **不**因 Established 未人審而違憲（避免一夜炸庫）；  
- 編輯佇列與匯出會 **暴露** 高燈未 verified 清單。

## 2. 編輯 OS

`universe_explorer/editorial.py`：

- `record_ok(claim)` → 憲法形狀是否過（不含網路）  
- `ledger_row(claim)` → 燈、軸、review_state、record_ok、缺口  
- `editorial_queue(topics)` → 待人審 / 被挑戰 / 形狀不過  

CLI：`python -m universe_explorer.editorial`

## 3. OpenAlex 適配

`discovery/adapters/openalex_adapter.py`：

- `search` → OpenAlex Works API（polite User-Agent）  
- 有 DOI → `source_ref=doi:…`（入庫後仍走 Crossref cite⇒fetch）  
- 無 DOI → `openalex:W…` + 本地 `cache/openalex/`  verbatim  
- **不判燈、不發明 confidence**

Pipeline：`--adapter openalex`

## 4. 驗收

1. README 首段為帳本 + 編輯 OS 定位。  
2. `review_state` 預設 unverified；非法值違憲。  
3. OpenAlex adapter 單元測試（離線 fixture）。  
4. editorial queue 可列高燈未 verified。  
5. 全庫 tests 綠；model 重蓋章。
