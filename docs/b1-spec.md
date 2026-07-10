# B1 Spec — 本地 LLM 組稿器(第一個接上接縫的 LLM)

> 決策(Nelson,2026-07-10):LLM 用**本地模型**(Ollama),不接雲端 API ——
> claim 資料不出機器。這是四個「聰明可換、法院不換」接縫的第一次實戰。

## 0. 鐵律(全部沿用,零新規)

- LLM 產的每句敘事**過同一個 `narrative.check()`**:逐句 refs、憲法開場句式、
  % 逐字引用、宣告信心殺。法院一字不動。
- **失敗即退回**:模型沒開、輸出格式壞、任何一句違憲 → 整段退回機械組稿器。
  系統永遠不會因為 LLM 而更不可回溯,最壞情況 = 沒有 LLM 之前的樣子。
- Prompt 只餵 claim 已收錄的欄位 + 合法 refs 清單 —— LLM 拿不到收錄以外的資訊,
  跟 AI Narrative 層「只能整理已收錄證據」的憲法同構。

## 1. 實作

- `dataops/llm_narrative.py`(接線,不動引擎):
  - `call_model(prompt)` 與 `parse_and_gate(claim, raw, loc)` 分離(可測性)。
  - 模型輸出 JSON `[{"text": ..., "refs": [...]}]`;解析後跑 check()。
  - CLI:`python -m universe_explorer.dataops.llm_narrative <claim_id> [--zh]`
- 測試(`test_llm_narrative.py`)不依賴模型:偽造好/壞輸出,證明法院咬 LLM 一樣痛。

## 2. 驗收

1. 離線安全:Ollama 沒開時,narrate 路徑照常(機械版),測試全綠。
2. 法院平等:偽造的 LLM 違憲輸出(無 refs / 錯開場 / 假 %)被殺並退回(測試)。
3. 活體驗證:對至少一個真實 claim 跑通本地模型,產出通過 check() 的敘事,
   或誠實記錄它過不了(7B 模型過不了法院也是有效結果 —— 證明法院在工作)。
