# Roadmap v2 — 核心已證明之後的路(2026-07-10 規劃)

> 前情:P0–P4b 全通、修正案 #1/#2、R6 敘事層、P5 部分(digest)。
> 認識論、四層架構、治理三者已完整且自我防衛;四個「聰明可換、法院不換」接縫就位。
> 本文件規劃下一階段,依「先根基、再能力、後規模」排序。

---

## 現況盤點

**已解張力**:R1(雙軸)、R4(Competing 實證)、R6(敘事越權)、R7(實測 % 誤殺)
**未解張力**:R2(判燈的 LLM 提案)、R3(來源可信度分級)、R5(validator 規則版本化)
**誠實缺口**(盤點時發現,登記在案):
- **G1:專案不在 git 裡。** 凍結/修正案制度目前靠 engine_hashes.json 一份檔案;
  沒有歷史、沒有回滾、修正案沒有 commit 可指。這是全案最大的工程風險。
- G2:9 個測試套件靠手工迴圈跑,無一鍵入口。
- G3:snapshot/events/outbox/audit 的重生成流程只存在於我腦中與 README 片段。

---

## Track A — 工程根基(最先做:便宜、防災、半天內)

| 項目 | 內容 | 驗收 |
|---|---|---|
| A1 git 化 | `git init` + 初始 commit;`.gitignore`(cache/events/outbox/dist 視情況);**修正案制度落地為 git 慣例**:修憲 = 一個帶 amendment 文件的 commit | 歷史可查;engine_hashes.json 降級為 belt-and-suspenders |
| A2 一鍵測試 | `run_tests.py`:跑 9 套件 + build --check,一個 exit code | CI-ready;README 一行指令 |
| A3 操作手冊 | `docs/operations.md`:改資料 → fetch → 測試 → watch --commit → push → artifact 重發的完整循環 | 第三者能照做 |

## Track B — 啟用 LLM 接縫(R2,B 路線;**需要你拍板 API key/費用**)

四個接縫本來就是為此而建。啟用順序由風險低至高:

| 項目 | 內容 | 把關(已存在,不動) |
|---|---|---|
| B1 LLM 組稿器 | Claude API 產生更自然的敘事,取代機械組稿 | `narrative.check()`:逐句 refs、開場句式、% 逐字 —— 不過就整段不呈現 |
| B2 LLM 提案器 | Claude API 讀證據草擬 status_reason 供人審 | `proposals` 治理:提案不落地、人拍板、append-only 稽核 |
| B3 翻譯生成 | LLM 起草新 claim 的中文 overlay,人校對後入庫 | 缺翻譯退回英文;識別碼不翻 |

設計約束:**offline-safe** —— 無 API key 時自動退回機械版,測試不依賴網路。

## Track C — 資料層擴張

| 項目 | 內容 | 驗收 |
|---|---|---|
| C1 R3 來源分級 | Source.kind 升級為受控詞彙(peer-reviewed / preprint / dataset / prize / textbook / critique),validator 檢查;證據軸推導可考慮 preprint 降權(需修正案) | 分級可回溯、不產生新的假精度 |
| C2 NASA/ESA/ADS adapter | 第二個 Data 層抓取器(需 API key 註冊) | 與 arXiv 同級的 provenance |
| C3 加深領域 | 每領域 4 claim → 8-10 claim;或第四領域 | 出處紀律照舊 |

## Track D — 產品化(讓別人也能用)

| 項目 | 內容 | 驗收 |
|---|---|---|
| D1 公開部署 | dist/ 是純靜態 → GitHub Pages / Cloudflare Pages 免費上線(依賴 A1) | 任何人可訪問,不需 claude.ai 帳號 |
| D2 探索 UX | 燈號篩選、跨領域搜尋、單 claim 永久連結 | 前端仍陽春優先,結構清楚 |
| D3 真實推送 | outbox → email/webhook 傳輸;訂閱單一 claim | digest 憲法照管 |

## Track E — 治理深化(遠期)

- E1 R5:validator 規則版本化(修正案編號寫進違憲報告)
- E2 條件觸發的自動燈號遷移提案(P3 事件 → P2 提案自動生成,**人仍拍板**)

---

## 推薦順序(我的判斷)

```
A(根基,先做)──► B1(LLM 敘事,最低風險驗證接縫)──► D1(上線)
                └─► C1(來源分級)──► B2(LLM 提案)──► C2/C3/D2/D3 按需
```

理由:
1. **A 必須最先** —— 沒有 git,後面每一步的「修正案制度」都是沙上建塔。
2. **B1 先於 B2**:敘事的失敗模式是「整段不呈現」(無害);提案的失敗模式牽涉判燈治理(重)。用 B1 驗證 LLM 接縫的工程,再上 B2。
3. **D1 很便宜**:dist/ 已是純靜態,git 化之後上 Pages 幾乎零工程。
4. B 整條依賴你決定:是否接 Claude API(key、費用、資料出境到 API 的考量)。
   不接的話,B 全跳過,系統照樣完整 —— 機械版本來就合憲。
