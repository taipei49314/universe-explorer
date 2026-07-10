# R6 Spec — AI Narrative 層(四層架構的最後一層)

> 定位:回填四層架構刻意留空的最上層。R6 風險:「AI 越權宣布事實」。
> 處置:跟 P2 同一招 —— **先蓋把關,再談聰明**。本版的組稿器是機械的;
> 未來換 LLM 組稿器時,把關(逐句回溯檢查)原地不動。

---

## 0. 憲法約束(v0 第 2 條的機械落地)

1. **AI 不宣布事實,只整理已收錄證據。** 敘事的每一句都必須攜帶 refs
   (指向該 claim 的 source label 或 status_reason 條件),**無 refs 的句子 = 違憲**。
2. **開場句式強制**:敘事必須以「根據目前收錄的證據」(Based on the evidence
   recorded here)開頭 —— 不是風格偏好,是憲法句式。
3. **敘事永遠是最底層**:它從 Knowledge/Evidence 層讀,絕不寫回任何上層;
   敘事檢查失敗 → 該 claim 的敘事整段不呈現(寧缺勿越權),build 不擋
   (敘事是加值,不是資格)。
4. 文字內容過 validator 同一套掃描(宣告信心語彙禁、非證據欄裸 % 禁 ——
   敘事句引用實測數字時必須逐字引自證據描述)。

## 1. 實作

- `narrative.py`(引擎檔,入基準雜湊):
  - `NarrativeSentence {text, refs: [...]}`
  - `compose(claim)`:機械組稿 —— 從 status/status_reason/evidence/open_questions
    組出句子,每句自動攜帶其來源 refs。
  - `check(claim, sentences)`:逐句驗證 refs 可解析 + 文字合憲。組稿器與檢查器
    **分開**,未來 LLM 組稿也走同一個 check。
- render:敘事區塊顯示於 claim 卡片,每句後面跟著它的 refs;
  區塊標題明示「AI narrative — organised from recorded evidence, never beyond it」。

## 2. 驗收

1. 逐句可回溯:兩個領域全部 claim 的敘事,每句 refs 都解析到真實 source/條件(測試)。
2. 越權句被殺:塞一句無 refs 的句子 → check 抓到(測試)。
3. 檢查器獨立:check() 不信任 compose(),偽造的壞敘事一樣抓(測試)。
4. 全部既有把關照過。
