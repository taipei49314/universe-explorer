# 產品七點修正總規劃（Product Remediation Plan）

> **狀態：** 規劃已定，待分批實作。  
> **北極星不變：** 誠實區分已知／未知；不給假答案、不造信心分。  
> **來源：** 產品體檢七點壞處 → 可執行修正；與 `docs/milestones-complete.md`（引擎里程碑）互補——那邊是「法院與地圖建成」，這邊是「人怎麼用、怎麼信、怎麼活」。

---

## 0. 總覽

| # | 問題（體檢） | 修正代號 | 本質 | 主要槓桿 |
|---|--------------|----------|------|----------|
| 1 | 認知成本太高 | **P-Read** | 產品／文案／UX | 60 秒讀法 |
| 2 | 內容不均＋人手瓶頸 | **P-Edit** | 編輯制度 | 域 SLA＋季主修 |
| 3 | 關聯只是索引 | **P-Guide** | 導讀結構 | 路徑解說＋對照 |
| 4 | 前端分裂 | **P-Shell** | 資訊架構 | 單主殼 |
| 5 | 無人用／無節奏 | **P-Pulse** | 運維節奏 | 週巡＋變更頁 |
| 6 | 無永續路徑 | **P-Sustain** | 策略／輕基建 | 贊助／採納 |
| 7 | 外人難信 | **P-Audit** | 可覆核性 | 健康儀表板 |

### 憲法紅線（七點共通）

| ✅ 允許 | ❌ 禁止 |
|---------|---------|
| 引導、折疊進階、導航統一 | AI 宣布「誰對」 |
| 計數、清單、靜默週報 | confidence / 排名勝負 |
| 人工路徑解說、人工主修域 | 自動改燈、自動長邊填滿 |
| 抽查與挑戰 | 「已獲認證」自我蓋章 |

### 依賴圖（實作順序的硬約束）

```
P-Read (①) ──┬──► P-Shell (④) ──► P-Guide (③)
              │         │
              │         └──► P-Pulse (⑤) ──► P-Audit (⑦)
              │
              └──► P-Edit (②) 全程並行（制度）
                          │
P-Sustain (⑥) ◄──────────┴── 策略並行，幾乎不挡工程
```

- **① 不先做，④ 的導航文案會沒有共同語言。**  
- **④ 不穩，③ 的圖／對照會散落在三個入口。**  
- **⑤ 沒節奏，⑦ 的「最近覆核」是空的。**  
- **②、⑥ 不堵工程，但決定一年後是否還有人養內容。**

### 建議時程（約一季，可壓縮）

| 階段 | 週次 | 交付 | 代號 |
|------|------|------|------|
| **S0** | 0 | 本文件入庫；凍結「本季主修域」決定 | — |
| **S1** | 1–2 | 首屏導覽 + about 範例 claim + 簡表面板 | P-Read |
| **S2** | 2–3 | 主殼導航、`?c=` 深鏈、Drift 降級標籤 | P-Shell |
| **S3** | 3–4 | Actions 週巡 + changes 頁 + webhook 真接（可 dry-run） | P-Pulse |
| **S4** | 5–6 | 健康／覆核儀表板 + 邊挑戰全覆蓋 + DOI 粗檢警告 | P-Audit |
| **S5** | 7–8 | 路徑解說 + 雙 claim 對照卡 | P-Guide |
| **Sx** | 全程 | 編輯 SLA、候選佇列、CONTRIBUTING | P-Edit |
| **Sy** | 全程 | Sponsors／課程話術、公開工時 | P-Sustain |

**一季成功（可數，非信心分）：**

1. 新訪客能完成導覽或讀完 canonical example（質性抽問即可）。  
2. 單一主 URL 完成：選域 → 展開 → 關聯 → 詳情。  
3. 連續 4 週有 digest **或** 公開「本週靜默」。  
4. 健康頁可抽 3 則 claim 完成覆核路徑。  
5. 至少 1 條 reading path 有人工解說段落。  
6. 本季主修域有 Discussion 更新或 challenge 落地。  
7. （可選）出現第一次外部 challenge 或課程／贊助意向。

---

## 1. P-Read — 認知成本（體檢點 1）

### 問題
燈／軸／分岔／入格條件同時砸來；第一印象像論文後台。

### 目標
**60 秒**建立共同語言：綠＝什麼、紅＝什麼、系統不給信心分、關聯不是判決。

### 工作包

| ID | 工作 | 產出 |
|----|------|------|
| R1 | 首次造訪導覽 overlay（4 步） | `app.html`；`localStorage ue_tour_done`；`?tour=0` 強制重看 |
| R2 | 步驟文案中英 | I18N 鍵，不新增認識論詞彙 |
| R3 | Canonical example | about 固定以 `hawking_radiation`（或選定一則）示範：燈 vs 軸分岔 |
| R4 | 面板「簡表／進階」 | 預設：標題、燈、摘要式 why、關聯、OQ；進階：入格條件全文、E 軸推導、敘事 |
| R5 | 地圖一角常駐「怎麼讀」 | 鏈到 about 錨點 `#how-to-read` |

### 驗收
- [ ] 不認識專案者看完導覽能口述：燈屬 claim、無信心分、紅≠「假」而是「未接受／推測層」。  
- [ ] `prefers-reduced-motion` 下導覽無強制動畫。  
- [ ] 測試：導覽字串存在、about 含 example claim id。

### 刻意不做
簡化五格為三格；用進度條表示「確定性」。

---

## 2. P-Edit — 內容與人手（體檢點 2）

### 問題
域深度不均；擴張速度 = 作者帶寬；禁止用 AI 衝 claim 數。

### 目標
**可預期的編輯節奏**與**域級最低形狀**，讓「薄」是明示不是疏忽。

### 工作包

| ID | 工作 | 產出 |
|----|------|------|
| E1 | 域 SLA 表 | 每域：目標形狀（建議至少覆蓋 🟢🔵🟡🟠🔴 或註明「本域無 X」） |
| E2 | 本季主修域 | 公開寫在 `docs/editorial-queue.md`（每季改一次） |
| E3 | 候選佇列紀律 | 每週處理 N 則 `candidates/`（建議 N=3）；通過才入 data |
| E4 | Challenge 落地清單 | issue label → 必改 data + history + watch commit |
| E5 | CONTRIBUTING 加硬步驟 | 核實出處 → fetch → 譯 → test → watch |
| E6 | （可選）域健康報告腳本 | 印出每域燈號計數、缺層警告（機械計數） |

### 驗收
- [ ] `editorial-queue.md` 存在且含本季主修域。  
- [ ] 連續兩週有候選處理或明示「本週佇列空／靜默」。  
- [ ] 新 claim 不經 fetch／test 無法進 main（既有閘門維持）。

### 刻意不做
季度 KPI = claim 總數；LLM 批量產 claim。

### 與工程關係
**幾乎不挡 S1–S5**；但 S0 就要選定主修域，避免一邊做 UX 一邊無目的加 claim。

---

## 3. P-Guide — 關聯增值（體檢點 3）

### 問題
R-Graph 誠實但是索引；使用者期待「讀完有結論感」容易失望。

### 目標
在**不判決**的前提下，讓路徑與張力**可讀完**。

### 工作包

| ID | 工作 | 產出 |
|----|------|------|
| G1 | Reading path 解說 | 每 path 3–5 句人工 `guide` / `guide_zh`（relations 資料） |
| G2 | 邊點擊 | 圖上點 edge → 顯示 kind + note（非新判決） |
| G3 | 雙 claim 對照 | UI：選 A/B → 並排燈、軸、分岔、是否有邊、permalink |
| G4 | 問題入口 | 3–5 個「我關心…」芯片 → 對應 path（H0／地震預測／深海開採…） |
| G5 | 面板文案 | 關聯區固定句：「下列是記錄的邊，不是勝負。」 |

### 驗收
- [ ] ≥3 條 path 有 guide 文案。  
- [ ] 對照卡不出現 score／winner。  
- [ ] 測試：guide 欄位無 banned keys；path validate 仍過。

### 依賴
**S2（P-Shell）之後**做，避免導讀入口散落。

### 刻意不做
「系統推論本地 H0 更可能」；自動依共現權重排序邊。

---

## 4. P-Shell — 前端統一（體檢點 4）

### 問題
app / universe / 陽春 topic 三套心智。

### 目標
**一個主產品殼**；其餘降級為模式或底線。

### 工作包

| ID | 工作 | 產出 |
|----|------|------|
| H1 | 全域導航列 | 地圖 · 漂流 · 怎麼讀 · Feed · 中英（app 為準） |
| H2 | 深鏈 | `app.html?c=<claim_id>` 開面板 + 聚焦 R-Graph；`?path=` 開閱讀路徑 |
| H3 | Drift 標籤 | 標題區註明「沉浸模式／同一資料」；關聯行為對齊 |
| H4 | 陽春頁 | 保留；每頁頂部「在知識地圖中打開」鏈回 `app.html?c=` |
| H5 | 共用片段策略 | 短期：重複可接受；中期：建置時從 `web/partials/` 注入 nav（可選） |
| H6 | 行動版 panel | 全寬、安全區、關閉鈕可點 |

### 驗收
- [ ] 新使用者只ブックマーク `app.html` 可完成主路徑。  
- [ ] `?c=event_horizon_exists` 直達。  
- [ ] 測試：app 含 nav 與 query parse。

### 依賴
**S1 導覽文案就緒後**接導航，避免空殼。

### 刻意不做
上 React/Vue；刪除陽春 permalink 頁。

---

## 5. P-Pulse — 節奏與分發（體檢點 5）

### 問題
Digest／webhook 有了，沒有讀者節奏。

### 目標
**合法、可預期的週期輸出**（無事件則公開靜默）。

### 工作包

| ID | 工作 | 產出 |
|----|------|------|
| U1 | GitHub Action 週排程 | watch（若適用）+ source_health + push；artifact 保留 digest |
| U2 | `changes.html`（或 dist 生成） | 最近 N 份 digest 轉述列表；無則「本週知識狀態無新事件」 |
| U3 | Webhook 實接文件 | operations：Discord/Slack incoming webhook 一步步 |
| U4 | Feed 入口強化 | 導航與 about 明示「訂閱 feed = 訂閱機械變更」 |
| U5 | （可選）月報 | 人工 10 行 + 連 commit；放 `docs/monthlies/` |

### 驗收
- [ ] 連續 4 週 CI 有成功 run（或 skip 原因清楚）。  
- [ ] 站上可打開最近變更。  
- [ ] digest 正文仍過 transport 憲法檢查。

### 依賴
P5b 已完成；**不依赖**新科學內容。

### 刻意不做
「突破性發現」推播；強制每日郵件。

---

## 6. P-Sustain — 永續（體檢點 6）

### 問題
免費＋憲法 → 無編輯團隊資金。

### 目標
**不靠賣假確定性**的存活路徑。

### 工作包

| ID | 工作 | 產出 |
|----|------|------|
| S1 | README／about「如何支持」 | Sponsors 或捐助說明；寫明贊助買的是工時不是燈號 |
| S2 | 公開工時卡 | 「主修一域估時」表（編輯用） |
| S3 | 採納話術 | 一頁：課程／新聞室／博物館怎麼用（可挑戰底圖） |
| S4 | Fork 邀請 | 分域 fork 養 content；上游養法院——寫清邊界 |
| S5 | 紅線 | 若未來收費：只代管巡檢／工作坊，**不賣更準燈號** |

### 驗收
- [ ] 公開頁存在支持／採納說明。  
- [ ] 12 個月內至少觸及：贊助 or 課程試用 or 外部 fork（質性目標）。

### 刻意不做
付費 API「答案更正確」；廣告聯盟綁知識判決。

---

## 7. P-Audit — 外部信任（體檢點 7）

### 問題
內部法院嚴，外人仍難快速覆核。

### 目標
**第三者 15 分鐘抽查路徑**。

### 工作包

| ID | 工作 | 產出 |
|----|------|------|
| A1 | `health.html` 或 build 產物 | 最後 build 時間、claim 數、域計數、孤立 claim 數、relations coverage |
| A2 | 隨機三則 | 每次 build 固定 seed 或日期 seed 抽 3 claim：id、sources、cache 是否存在 |
| A3 | 邊挑戰入口 | 面板每條 related 旁「挑戰此邊」深鏈 template |
| A4 | DOI／arXiv 標題粗檢 | fetch 後 title tokens vs claim 關鍵詞；**只警告**不改燈 |
| A5 | status_history 露出 | 面板歷史區強化；連 GitHub blame（可選） |
| A6 | 測試 | 健康 payload 無 banned keys；抽樣邏輯可單測 |

### 驗收
- [ ] 陌生人按健康頁 → 一則 claim → sources → challenge 走通。  
- [ ] 錯誤 DOI 類問題有機會在粗檢被標黃（不自動靜默失敗整庫除非 cite 缺失）。

### 依賴
**P-Pulse 之後**「最近巡檢時間」才有意義；可與 S4 重疊。

### 刻意不做
「本站已 peer-reviewed」徽章；自動因粗檢降燈。

---

## 8. 跨切面：量測與測試

| 項目 | 做法 |
|------|------|
| 導覽 | `?measure=1` → `tour_step` 事件（可選） |
| 深鏈 | 既有 `relation_nav`；加 `deep_link_open` |
| 測試閘 | 每階段對應 `test_app` / `test_relations` / 新 `test_health_page` 等 |
| 文件 | 本檔 + 各階段結束改狀態表（下方） |

### 狀態表（實作時勾選）

| 代號 | 狀態 | 完成 commit |
|------|------|-------------|
| P-Read | ✅ shipping | product surface sprint |
| P-Shell | ✅ shipping | topnav + `?c=` / `?path=` |
| P-Pulse | ✅ shipping | changes.html + weekly.yml |
| P-Audit | ✅ shipping | health.html / health.json |
| P-Guide | ✅ shipping | path guides + compare + qchips |
| P-Edit | ✅ shipping | docs/editorial-queue.md |
| P-Sustain | ✅ shipping | about#support |

---

## 9. 資源假設

| 角色 | 投入 |
|------|------|
| 實作者（工程） | S1–S5 約 0.5–1 人季（視並行） |
| 編輯（科學） | 每週固定塊：候選 3 + 主修域 1 塊；不可被 UX sprint 吃掉 |
| 運維 | Action secrets：`UE_WEBHOOK_URL` 可選 |

若只有一人：嚴格順序 **Read → Shell → Pulse → Audit → Guide**，Edit/Sustain 用文件先落地再慢慢執行。

---

## 10. 第一個實作指令（規劃凍結後）

建議開幹指令（擇一）：

1. **`實作 P-Read + P-Shell`** — 最快改變體感（原 ①+④）。  
2. **`實作 P-Pulse + P-Audit`** — 最快建立外部信任與節奏。  
3. **`實作 S0：editorial-queue + 本季主修域`** — 零 UI，先鎖內容紀律。

預設推薦：**1 然後 2**，與依賴圖一致。

---

## 11. 成功時產品會長成什麼

- **對路人：** 知道怎麼讀，不必先懂法院。  
- **對覆核者：** 15 分鐘能挑戰燈或邊。  
- **對訂戶：** 有變更才吵，沒變更說靜默。  
- **對作者：** 主修域清晰，不靠 claim 計數自欺。  
- **對憲法：** 仍然不宣布答案。

這七點修完，產品從「嚴謹的知識作業系統」更接近「**可被公眾使用的誠實知識介面**」——仍然不是百科全書，也不該變成。
