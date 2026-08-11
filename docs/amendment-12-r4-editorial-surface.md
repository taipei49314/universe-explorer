# 修正案 #12 — Round-4 閉合：編輯 OS 公開面 + 防偽 + precheck 對齊

> 對齊 `docs/redteam-round4-after-a11.md` 的可修補項。  
> **不**宣稱關閉 C1 語義洞（真 DOI + 假 direct）；那仍需人審，且人審標記現在可見、難偽造。

## 0. 動機

#11 落地帳本定位與 `review_state`，但：

1. 公開 `claims.json` / UI **不顯示** review 標記（R4-1）  
2. `human_verified` + `verified_by="x"` 即可消佇列（R4-2）  
3. `CHALLENGED` 對讀者無可見後果（R4-5）  
4. discovery precheck 丟 `trace_refs`、不跑 provenance（R4-6）  
5. arXiv id 與 DOI 永不合併 → 可雙計 E1（R4-7）  
6. vacuous note 黑名單可繞（R4-9）  
7. 敘事拋光 C1 不提編輯狀態（R4-4）

## 1. 公開帳本（R4-1）

下列匯出/渲染必須含：

- `review_state` ∈ {unverified, human_verified, challenged}  
- `verified_by` / `verified_note` / `verified_at`  
- `trace_refs`（claims.json / app-data）

靜態 claim 卡與 `web/app.html` 面板顯示徽章：

| state | 徽章 |
|-------|------|
| unverified | ○ unverified |
| human_verified | ✓ human_verified (who) |
| challenged | ⚠ challenged |

## 2. 防偽（R4-2）

`review_state=human_verified` 時：

| 規則 | 法源 key |
|------|----------|
| `verified_by` 非空 | `verified_without_attribution`（#11） |
| `verified_by` 為 email / `@handle` / `github:handle` / 顯示名≥6，且不在 throwaway 黑名單 | `verified_by_invalid` |
| `verified_note` ≥12 字 | `verified_note_vacuous` |
| `verified_at` = `YYYY-MM-DD` | `verified_at_invalid` |

## 3. 敘事與挑戰可見（R4-4 / R4-5）

- `compose` **一律**附加編輯標記句（`condition:review_state` ref）  
- challenged / unverified 文案明確；不得只拋光共識燈  

## 4. Precheck = build 法院（R4-6）

- `_dict_to_claim` 保留 `trace_refs`、`review_state`、`competing_models`、`status_history`、verified\*  
- `validate_claim(..., check_provenance=True)`

## 5. 紙本身份合併（R4-7）

`paper_id_of`：掃描本地 `cache/arxiv/*.xml` 的 `<arxiv:doi>`，  
將 `arxiv:…` 與對應 `doi:…` **正規化到同一 canonical（prefer doi:）**。

## 6. Vacuous notes（R4-9）

擴充 `_VACUOUS_NOTES`（`because sources`、`supported by literature`、`yes it holds` 等）。

## 7. Strong × analog（R4-8）

編輯佇列對 **STRONG + 僅 analog** 且未 verified 使用更強 reason（false-analog risk）。  
不因未 verified 炸 build（#11 遷移策略保留）。

## 8. 驗收

1. `claims_json` / `app_data_json` 每則 claim 含 `review_state`  
2. `human_verified` + `verified_by="x"` → 違憲  
3. precheck 帶 `trace_refs` 的 candidate 不再假報 `trace_refs_missing`  
4. 有 DOI 對照的 arXiv+DOI 同一工作 → 同一 `paper_id`  
5. 敘事含 Editorial mark 句且 `check` 通過  
6. 全庫 tests 綠；`engine_hashes.json` 重蓋章  
