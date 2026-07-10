# Universe Explorer 憲法彙編(Consolidated Constitution)

> 單一權威文件。規範原文散見 v0 Kickoff Spec、各階段 spec 與修正案 #1–#6;
> 本彙編收斂全貌,供挑戰者與維護者查閱。**與程式碼的一致性由測試強制**:
> 本文件列出的規則集必須等於 `validator.LAWS` 登記表,漂移即測試失敗。

---

## 前言

本系統誠實區分人類的已知與未知。它不宣布答案;它陳列:我們知道什麼、
怎麼知道的、還不知道什麼、有哪些競爭假說 —— 且每一個判定都可被任何人
以可查證的論證推翻。

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

授權:程式碼 MIT;內容 CC BY 4.0(LICENSE / LICENSE-CONTENT.md)。
