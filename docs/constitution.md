# Universe Explorer 憲法彙編(Consolidated Constitution)

> 單一權威文件。規範原文散見 v0 Kickoff Spec、各階段 spec 與修正案 #1–#6;
> 本彙編收斂全貌,供挑戰者與維護者查閱。**與程式碼的一致性由測試強制**:
> 本文件列出的規則集必須等於 `validator.LAWS` 登記表,漂移即測試失敗。

---

## 前言

本系統是**可審計的科學主張帳本**與**編輯作業系統**,不是「機器已分清真偽」。
它陳列:記錄了什麼、掛了哪些可抓來源、共識燈與證據軸、是否經人審
(`review_state`) —— 且每一個**記錄層**判定都可被推翻。語義是否支持 claim
仍需人類與挑戰流程(修正案 #11)。

## 第一章 架構(v0 §1)

```
Data → Evidence → Knowledge → AI Narrative(依賴單向不可逆,AI 墊底)
```

- 燈號屬於 **Claim**,永不屬於 Topic(容器無燈)。
- AI 不宣布事實,只整理已收錄證據;確定性從證據湧現,不得宣告為數字。

## 第二章 判定體系

**共識軸(五格,人工判定、逐條可回溯)**:Established / Strong / Competing /
Frontier / Speculative,各有入格條件(`model.STATUS_CONDITIONS`);
mode=all 須全部成立,mode=any 一條即可。

**證據軸(E1–E5,機械湧現,無人填寫)**:由公開規則自已收錄證據推導
(`axes.derive`);E1 需 ≥2 條直接觀測掛 ≥2 個不同 **PRIMARY** 出處(修正案 #4)。
強共識 × 非直接證據 → **⚡ 分岔**,機械標記。

**來源分級(修正案 #3)**:PRIMARY / SECONDARY / PREPRINT / DATASET,
離散類別、禁數字分數,不可分類即違憲。

## 第三章 規則總表(法源即 `validator.LAWS`;違憲訊息自動引法)

### v0 憲法(Evidence/Knowledge 層)
- `invalid_status` — 燈號必須是五格之一
- `evidence_without_source` — 證據必須掛 source_ref
- `dangling_source_ref` — source_ref 必須解析到本 claim 的 Source
- `unsupported_claim` — 無證據的宣稱降級,不得佯裝已知
- `no_fake_precision` — 證據欄以外禁裸 %(修正案 #1 修訂範圍)
- `declared_confidence` — 宣告式信心語彙(共識度/confidence+數字)全域禁,含證據欄(修正案 #1)
- `no_numeric_open_questions` / `empty_open_question` / `numeric_open_question` — 開放問題是可展開清單,永不是數字
- `foreign_condition` / `unjustified_condition` — status_reason 只准引用該燈號的條件,且必須附理由
- `status_reason_incomplete` / `condition_not_satisfied` / `no_condition_satisfied` — 入格條件依 mode 全查
- `competing_needs_models` / `unexpected_competing_models` — competing_models 僅屬 Competing 燈
- `invalid_evidence_type` — 證據型別限受控詞彙(P1.5)
- `unclassifiable_source_kind` — 來源必須可分級(修正案 #3)

### Data 層:cite ⇒ fetch(P1;修正案 #6 擴至 DOI)
- `arxiv_source_unfetched` / `provenance_cache_missing` / `provenance_hash_mismatch` / `provenance_id_mismatch`
- `doi_source_unfetched` / `doi_cache_missing` / `doi_hash_mismatch` / `doi_id_mismatch`
- 快取為官方 API 回應逐位元保存;validator 重新解析內容,不信 manifest 自我宣稱。
- 誠實豁免:無 endpoint 的來源(教科書、獎項引文、無 DOI 紙本)。
- Amendment #7: arXiv/DOI **URL 與裸 DOI** 亦為 endpoint;`primary_source_not_fetchable` — PRIMARY 必須可抓取;E1 僅計可抓取 PRIMARY;`empty_title` / `duplicate_source_label` 記錄衛生。
- Amendment #8: 共識燈機械地板 — `consensus_floor_established`（🟢 必須 E1）;`consensus_floor_strong`（🔵 禁止 E4/E5；允許 Strong×E3 分岔）。
- Amendment #9: E1 依**正規化論文 id**（arXiv bare / DOI）去重，不依 source label；`kind` 含 `preprint` 一律 PREPRINT，不得被 `peer-reviewed` 子字串洗成 PRIMARY。
- Amendment #10: Critical 閉合 — `evidence_type_requires_primary_fetchable`；`validate_claim`/`validate_topic` 含 provenance；`competing_needs_distinct_papers`；`status_reason_vacuous_note`；`trace_refs_missing` / `trace_refs_unknown` / `trace_refs_insufficient`；`frontier_needs_fetchable_source`；`title_hidden_controls`；圖 shared-citation disclaimer。
- Amendment #11: 帳本+編輯 OS — `invalid_review_state` / `verified_without_attribution`；`review_state`∈{unverified,human_verified,challenged}；OpenAlex 為 discovery 適配器(有 DOI 則回落 Crossref fetch)。
- Amendment #12: 編輯 OS 公開面與防偽 — `verified_by_invalid` / `verified_note_vacuous` / `verified_at_invalid`；`claims.json`/`app-data`/卡片必出 `review_state`；敘事必述編輯標記；precheck 對齊 build（含 provenance 與 `trace_refs`）；arXiv↔DOI 紙 id 合併；vacuous note 黑名單擴充。

### 變化憲法(P3)
- `undocumented_status_change` — 燈號可以變,不准無聲地變(status_history 強制)。
- 來源同理:週巡邏回查正式存繳的更正/撤稿(T1);發現只報告,人重審。

## 第四章 治理

- **機器只能排除,核准永遠是人**(P2)。提案不落地;決定進 append-only 稽核。
- **LLM 的一切輸出過同一法院**:敘事逐句掛 refs、憲法開場句式(B1);
  條件草稿限 human 條件、UNVERIFIED 章、獨立日誌(B2);claim 草稿過全部
  法院後仍只進 drafts/,由人核對忠實性後手寫入庫(T4)。
- **推送只轉述**:digest/feed 逐行回指事件檔與推導,零詮釋(P5/D3)。
- **挑戰對世界開放**:issue 模板 + CONTRIBUTING;裁決永遠是人。

## 第五章 修憲程序(慣例成文)

1. 先立條文:`docs/amendment-N-*.md`(動機、修正內容、驗收)。
2. 修改引擎(七檔:model/validator/axes/provenance/proposals/watch/narrative)。
3. 新舊規則都要有測試證明會咬人;既有測試不得刪。
4. 重新蓋章 `engine_hashes.json`(凍結測試防的是**未經修正案的暗改**)。
5. commit 註明修正案編號。新規則必須登記 `LAWS`(法不可無源,測試強制)。

## 附:修正案索引

| # | 內容 | 檔案 |
|---|---|---|
| 1 | 實測 % 與宣告信心的區分 | amendment-1-r7.md |
| 2 | 敘事層在地化(同院多語) | amendment-2-narrative-i18n.md |
| 3 | 來源可信度分級 | amendment-3-source-tiers.md |
| 4 | 分級進證據軸(E1 需 PRIMARY) | amendment-4-r8-tier-weighting.md |
| 5 | 違憲報告標註法源 | amendment-4-r8-tier-weighting.md(第二部) |
| 6 | DOI 納入 cite⇒fetch | amendment-6-c2-doi-provenance.md |
| 7 | Endpoint 正規化、E1 需可抓取 PRIMARY、PRIMARY 必須可抓、空白 title / 重複 label | amendment-7-endpoint-honesty.md |
| 8 | 共識燈機械地板（Established→E1；Strong 禁 E4/E5） | amendment-8-consensus-floor.md |
| 9 | E1 paper-id 去重；preprint 不偽升 PRIMARY | amendment-9-e1-identity.md |
| 10 | Round-3 Critical 閉合包（direct 限 PRIMARY、trace_refs、vacuous note、Competing/Frontier 地板、claim+provenance） | amendment-10-critical-closures.md |
| 11 | 帳本定位、`review_state` 編輯 OS、OpenAlex 適配 | amendment-11-ledger-editorial-openalex.md |
| 12 | Round-4 閉合：編輯 OS 公開面、verified 防偽、precheck 對齊、arxiv↔doi id | amendment-12-r4-editorial-surface.md |

授權:程式碼 MIT;內容 CC BY 4.0(LICENSE / LICENSE-CONTENT.md)。
