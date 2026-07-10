# 憲法修正案 #6 — DOI 來源納入 cite ⇒ fetch(C2)

> P1 的誠實豁免寫得很清楚:「規則按有沒有 endpoint 劃分,不按方便劃分。」
> Crossref API(免金鑰、帶 email 進 polite pool)讓所有 DOI 來源**有了 endpoint** ——
> 豁免範圍因此誠實縮小。這不是新原則,是舊原則在新事實下的必然結果。

## 0. 修正條文

任何 `url_or_id` 以 `doi:` 開頭的來源,適用與 arXiv 同構的四條規則:

| 規則 | 內容 | 法源 |
|---|---|---|
| `doi_source_unfetched` | 引用了 DOI 卻沒有抓取記錄 | amendment-6 |
| `doi_cache_missing` | manifest 指到的快取檔不存在 | amendment-6 |
| `doi_hash_mismatch` | 快取檔與記錄的 sha256 不符(被改過) | amendment-6 |
| `doi_id_mismatch` | 快取內容的 DOI 與宣稱不符(重新解析,不信任 manifest 自我宣稱) | amendment-6 |

豁免範圍(誠實列舉):教科書、獎項引文、**無 DOI 的**紙本期刊條目。
它們仍然沒有可機器抓取的 endpoint。若日後為它們補上 DOI,即自動落入本條管轄。

## 1. 工程

- `provenance.py`(引擎,重新蓋章):DOI 正則 + Crossref 快取/清單路徑 +
  四規則檢查;arXiv 邏輯一字不動。DOI 比對不分大小寫(DOI 規範如此)。
- `dataops/crossref_fetch.py`(搬運工):`GET api.crossref.org/works/<doi>`,
  回應**逐位元**存檔;manifest 記 endpoint、UTC、sha256、逐字 title/期刊/年份
  供人眼核對。禮貌池:User-Agent 帶聯絡 email;請求間隔 1 秒。
- LAWS 登記四條新規則;修正案 #5 的「法不可無源」測試同步擴充。

## 2. 本修正案的自我試煉(誠實預告)

現有 7 個 DOI 來源中,多數已在 P4 網路核實,但 Rabone2023 與 FrontiersCritique2025
的 **DOI 字串本身**是從頁面路徑推得、未逐字核實過。C2 上線的第一次抓取
就是對它們的審判 —— 若解析失敗,修 data(而非放寬規則),並記錄在案。

## 3. 驗收

1. 全部 `doi:` 來源有真實抓取記錄,可回溯到 Crossref endpoint(線上實跑)。
2. 四規則咬人由偽造測試證明(不碰真快取)。
3. 非 DOI 來源豁免照舊(測試)。
4. 全部套件照過;引擎重新蓋章;CI 綠。
