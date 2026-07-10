# P1 Spec — 真實抓取(Data 層自動化)

> 定位:Roadmap P1。v0 證明了認識論站得住;P1 證明 **Data 層可以自動、可回溯地長出來**。
> 與 v0 相同的紀律:先定驗收線、先寫把關程式,再讓資料流進來。
> 上位文件:v0 Kickoff Spec(憲法)、design-framework.md(五支柱)。本文件不得違反兩者。

---

## 0. 一句話定位

**「引用即必須抓過原文」**:任何 claim 引用的 arXiv 來源,必須真的從 arXiv 官方 API 抓取過、
逐字快取在本地、且可用雜湊值驗證未被竄改 —— 否則 validator 判違憲,build 被擋下。

## 1. P1 範圍(明確劃線)

### 做

1. **arXiv 抓取器**:對 v0 已引用的每個 arXiv id,打官方 API(`export.arxiv.org/api/query`),
   把原始 Atom XML **逐字**存進 `cache/arxiv/`,不做任何改寫。
2. **Provenance manifest**(`cache/arxiv/manifest.json`):每筆記錄
   `endpoint`(完整請求 URL)、`retrieved_at`(UTC)、`cache_file`、`sha256`、
   `title / published / authors`(從回應逐字抄錄,供人眼核對)。
3. **Validator 擴充**(Data 層憲法):
   - `arxiv_source_unfetched` —— 引用了 arXiv 來源但沒抓過原文 → 違憲。
   - `provenance_cache_missing` —— manifest 指到的快取檔不存在 → 違憲。
   - `provenance_hash_mismatch` —— 快取檔與記錄的 sha256 不符(被改過)→ 違憲。
   - `provenance_id_mismatch` —— 快取檔內容不包含宣稱的 arXiv id
     (validator **自己重新解析 XML** 核對,不信任 manifest 自我宣稱)→ 違憲。
4. **候選來源搜尋 CLI**(發現新資料的入口,不是自動入庫):
   `search` 指令查 arXiv、把結果**逐字**存成 pending candidates。
   candidates 永遠不會自動進入 claim —— 人要引用,就得自己寫進 data 檔,
   而寫進去的瞬間就落入第 3 條的「引用即必須抓過原文」把關。

### 不做(越界即違規)

- ❌ 不做 NASA / ESA / ADS(需要金鑰與不同資料模型,留 P1+)。
- ❌ 不做 AI 摘要、AI 改寫、AI 判燈 —— **P1 管線裡沒有任何生成步驟**,抓取只搬運不改寫。
- ❌ 不動 §2 凍結 schema:provenance 屬於 **Data 層**(manifest),不塞進 Claim/Source 資料類。
- ❌ 不做自動把 candidate 塞進 claim(那是 self-certification 的自動化版本)。
- ❌ 不做雙軸燈號(那是 P1.5)。

## 2. 架構位置(對齊四層)

```
Data Layer      ← P1 蓋這層:fetcher + cache + manifest(可回溯到原始 endpoint)
Evidence Layer  ← 不變:evidence 仍由人寫、掛 source_ref
Knowledge Layer ← 不變:人工判燈 + status_reason
AI Narrative    ← 仍然空(刻意)
```

非 arXiv 來源(教科書、期刊紙本、Nobel 官網)誠實豁免:它們沒有可機器抓取的 endpoint,
manifest 不強制;但 arXiv 來源一律強制。**規則按「有沒有 endpoint」劃分,不按方便劃分。**

## 3. 治理:誰是把關者

- 抓取器是**搬運工**,不是判定者:它不能決定「這篇算不算證據」。
- 人仍然是唯一能把來源寫進 claim 的角色(P2 之前不變)。
- validator 是憲法法院:人引用了沒抓過的來源、或快取被竄改,**機械擋下,不看情面**。
- 這延續 v0 的反 self-certification 原則:P1 把「你說你讀過」升級成「系統證明你抓過」。

## 4. P1 驗收(先於實作定義;全部成立才算 PASS)

1. **全量可回溯**:v0 引用的全部 arXiv 來源(8 個 id,含舊式 `hep-th/9306069`)
   都有真實抓取記錄:原始 endpoint URL + UTC 時間 + 本地逐字快取 + sha256。
2. **把關真的會咬人**:測試證明 —— 刪掉快取檔、竄改快取內容、引用沒抓過的 id、
   manifest 指錯內容,四種情況 validator 各報對應違憲。**用假資料測,不竄改真快取。**
3. **憲法零違反不退步**:v0 全部檢查照跑照過;P1 檢查疊加其上,build 一次擋兩層。
4. **無 AI 生成**:管線中不存在任何改寫/摘要步驟;快取內容與 API 回應逐位元一致(sha256 即證明)。
5. **候選閘成立**:search 產出的 candidates 停在 pending 區;不存在任何程式路徑能把
   candidate 自動寫入 claim 資料。

> P1 通過 = Data 層能自動、誠實地長出來。不代表 Evidence 自動化(那是 P1 之後)、
> 不代表判燈自動化(P2)。別讓「P1 通過」蓋到還沒做的層。

## 5. 開工順序(同 v0 紀律:先把關、後資料)

1. 寫 validator 的 provenance 規則(先讓法院開門)。
2. 寫 fetcher + manifest(搬運工)。
3. 對 v0 的 8 個 arXiv id 跑真實抓取。
4. build.py 把 provenance 檢查納入擋關。
5. 寫「把關會咬人」的測試(驗收 §4.2)。
6. 搜尋 CLI + pending candidates。
7. 跑 §4 全部驗收。
