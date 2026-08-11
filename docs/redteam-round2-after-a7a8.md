# Universe Explorer 紅隊 Round 2（Amendment #7+#8 之後）

> **日期：** 2026-08-11  
> **前提：** #7 endpoint/E1/PRIMARY/title/label；#8 Established→E1、Strong 禁 E4/E5  
> **方法：** 可執行 PoC（`tmp_redteam2.py` 一輪；結果如下）

---

## 一句話

**#7+#8 擋住了「便宜假 PRIMARY / 無 E1 掛 🟢 / 純理論掛 🔵」。**  
**仍開的核心洞：E1 只數「標籤與型別」，不讀論文——兩篇真 DOI + 假 direct 文案 + 勾選 = 全綠 🟢E1。**

---

## 已確認關閉（本輪重打）

| 攻擊 | 結果 |
|------|------|
| example.com + peer-reviewed + 雙 direct + Established | **BLOCK** `primary_source_not_fetchable` + `consensus_floor_established` |
| Established + 單條 direct（E2） | **BLOCK** `consensus_floor_established` |
| Strong + 純理論（E4） | **BLOCK** `consensus_floor_strong` |
| 空白 title | **BLOCK** `empty_title` |
| status_reason 外來 condition / 信心數字 / Competing 單模型 | **BLOCK**（舊規則仍咬） |
| 兩 arXiv 未 fetch 的「假 E1」 | claim 層過 E1，**build 層** `arxiv_source_unfetched` |

Strong×E3（hawking 形）**仍合法**。

---

## 仍開 — 10 個可打穿 / 殘餘

### 1. Critical — 內容虛假、形式為真（E1+🟢）

```text
兩個真的、已 fetch 的 PRIMARY（doi: 或 arXiv:）
+ type=direct observation（描述可全假）
+ status_reason 全 holds + note="I say so"
→ validate_claim=[] + validate_provenance=[] + derive=E1 + Established
```

**PoC H/K：** 用庫內已有 `doi:10.1038/378355a0` 與 `doi:10.1073/pnas.15.3.168`，描述寫 invented → **全 PASS**。

機器不讀論文；**cite⇒fetch 只證明「這 DOI 存在」**，不證明「觀測支持本 claim」。

---

### 2. Critical — 同一論文拆成兩個 PRIMARY 標籤（假獨立）

| 變體 | 結果 |
|------|------|
| `arXiv:1906.11238` + `https://arxiv.org/abs/1906.11238` 兩個 label | **E1 + Established PASS**（PoC F） |
| `arXiv:1906.11238v1` + `v2`（正規化同一 bare id） | **E1 + Established PASS**（PoC V） |

E1 的「獨立」= **distinct source labels**，不是 distinct paper id。  
**一次觀測 × 兩個 label = 假多重複製。**

---

### 3. High — `preprint (peer-reviewed…)` 子字串升 PRIMARY

```text
tier_of("preprint (peer-reviewed later)") → PRIMARY
```

因 `SOURCE_TIERS` 先掃 PRIMARY 的 `peer-reviewed`。  
未審稿 preprint 可被字串洗成 PRIMARY（再配 fetch 真 arXiv 進 E1）。

---

### 4. High — 共識 note 仍可自證

Established 在 **有真 E1 形** 時，note 仍可全是 `I say so`（本輪 PoC H）。  
#8 只卡軸，**不卡理由內容**。

---

### 5. Medium — 低燈垃圾庫

Frontier / Speculative + 理論 + 教科書：**故意易過**（產品允許「未知」）。  
攻擊不是洗 🟢，而是 **灌水 / 稀釋站**。

---

### 6. Medium — zero-width 標題

`Fake\u200bClaim` **PASS**（非空白 strip 仍非空）。  
可混淆搜尋 / 去重。

---

### 7. Medium — `conference paper` 仍 unclassifiable

誠實會議論文可能被擋；攻擊面小，誤傷面有。

---

### 8. Medium — evidence 內 % 合法

`measured 42% effect` in evidence：**PASS**（amendment-1 設計）。  
若 description 胡扯百分比仍過。

---

### 9. Low — claim 層 vs build 層

未 fetch 的雙 arXiv：validator 給 E1 形，**build 擋**。  
若有人只跑 `validate_claim` 不當 build，會誤以為可入庫。

---

### 10. 結構殘餘（未變）

- 共享引用圖 ≠ 認識論連結  
- 敘事有 ref ≠ 忠於證據  
- 人審 / challenge 才是內容防線  

---

## 攻擊成本曲線（#7/#8 前後）

| 路徑 | 改前 | 改後 |
|------|------|------|
| example.com 假 PRIMARY | 🟢E1 | **死** |
| 勾 Established 無 E1 | 🟢 | **死** |
| Strong 純理論 | 🔵 | **死** |
| 兩真 DOI + 假 direct 文案 | 🟢E1 | **仍活**（成本：需真實 DOI 在 cache） |
| 同一 arXiv 兩 label | 🟢E1 | **仍活**（成本極低） |

---

## 建議下一刀（若繼續修）

| 優先 | 修法 | 擋 |
|------|------|-----|
| P0 | E1 按 **正規化 paper id**（arXiv bare / DOI）去重，不按 label | F, V |
| P0 | PRIMARY kind 若含 `preprint` 且未另標 published → 不得 PRIMARY | #3 |
| P1 | Established 的每條 `holds` note 須含 checkable ref（doi/arxiv） | note 自證 |
| P2 | 標題禁 zero-width / 控制字元 | #6 |
| 永不關 | 論文語義是否支持 claim | 人審 / 外部挑戰 |

---

## 結論

第二輪攻擊證明：**形狀門禁已到「需要真 endpoint + 真 E1 形」**；  
**最便宜仍開的洞是「同一論文雙標籤」與「真論文 + 假 direct 文案」。**

這不是 #7/#8 失敗，而是 **信任邊界上移到「fetch 存在 ≠ 證據支持本 claim」**。

---

## 後續修補（Amendment #9，同日）

| Round-2 OPEN | #9 狀態 |
|--------------|---------|
| F 同一 arXiv 兩 label | **已關** — E1 按 `paper_id_of` 去重 |
| V v1/v2 假獨立 | **已關** |
| preprint 子字串升 PRIMARY | **已關** — `tier_of` 見 preprint 即 PREPRINT |
| H 兩真 DOI + 假 direct 文案 | **仍開**（內容層；見 amendment-9 §0.3） |
