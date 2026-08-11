# Universe Explorer — UI 測試報告

日期：2026-08-11（初稿）  
**修訂：2026-08-11** — 對齊 `main` 真實 gate；補使用者路徑契約；澄清 Playwright 狀態。  
Repo：[taipei49314/universe-explorer](https://github.com/taipei49314/universe-explorer)

---

## 總覽（`main` 現況）

| 類別 | 狀態 |
|------|------|
| Python gate (`python run_tests.py`) | **43** suites（含 `test_accessibility.py`）+ `build.py --check` + trust/ui measures |
| 靜態 UI 契約 | `test_app.py` / `test_ui_expand.py` / `test_surface.py` / `test_build_validation.py` 等（字串／DOM 契約，非瀏覽器） |
| Accessibility smoke | `test_accessibility.py`（lang / title / viewport / labels / challenge→GitHub）**已入 gate** |
| Playwright 瀏覽器 E2E | **未**在 `main` 的 `run_tests.py` 內（見下方「Playwright 分支備註」） |

```bash
python run_tests.py          # CI 入口：Python suites + constitution + measures
python -m pytest test_reader.py test_accessibility.py -q   # 本 PR 使用者路徑重點
```

---

## 本 PR 補強的「使用者路徑」UI/CLI 契約

這些不是完整瀏覽器 E2E，但是**一般人會踩到的入口**，已變成可回歸的 pytest：

| 契約 | 測試 |
|------|------|
| 中文搜尋（霍金／黑洞…） | `test_reader.py::TestSearchIndexLiveRegistry` |
| `H0` / `H₀` / `lcdm`↔`ΛCDM` | tokenize + live registry |
| discover 未知 topic / 網路錯誤 → 人話 + exit 1 | `test_discovery.py::TestDiscoveryPipelineErrors` |
| challenge 拒假 claim、拒無 ref；form 含 GitHub templates | `test_reader.py::TestChallengeForm` + a11y |
| challenge.html 可及性 + template 連結 | `test_accessibility.py` |

### 靜態頁面 smoke（本機 / live）

| 頁面 | 期望 |
|------|------|
| `index.html` / `app.html` / `explore-v2.html` | 200，可載入 |
| `app.html?c=hawking_radiation` | 靜態 200；JS 開啟 panel（E2E 仍建議 Playwright） |
| `challenge.html` | 含 `challenge-a-verdict.yml` 等 GitHub 連結 |
| `claims.json` | 91 claims；雙軸欄位齊 |

---

## `test_app.py` 靜態 UI 契約（既有）

針對 `web/app.html` + `app-data.json`（**原始碼字串**，非 headless 瀏覽器）：

### 結構 / 自包含
- `app-data.json` claim 數與 registry 一致；雙語欄位存在
- 無外部 script/link；唯一 `fetch("app-data.json")`
- 五色 status 色板 light+dark 齊全

### 互動契約（字串存在即過）
- domain expand：`openDomains` / `aria-expanded` / 中文提示
- deep-link 參數：`URLSearchParams` + `c` / `path`（**缺 claim 靜默** — 已知殘餘盲點 U8）
- tour / reduced-motion / color-scheme

### 認論
- divergent claims 落在標示 zone
- universe.html：size∝axis、moons=sources、UNCHARTED 誠實

---

## Accessibility smoke（`test_accessibility.py`）

| 檢查 | 頁面 |
|------|------|
| `lang=` | explore-v2 / dashboard / challenge |
| `<title>` | 同上 |
| viewport meta | explore-v2 / dashboard |
| headings | explore-v2 / dashboard |
| form labels | challenge |
| GitHub template links | challenge（本 PR 新增） |
| semantic / ARIA | explore-v2 |

**限制：** 非 axe-core、非鍵盤全路徑、非對比度量化。完整 a11y 仍需工具鏈。

---

## Playwright 分支備註（Desktop / 實驗）

以下描述**曾在本機實驗分支**出現（例如 Desktop clone 的 `agent/finalize-*`），**不是**目前 `main` gate 的一部分：

| 檔案 | 用途（實驗） |
|------|----------------|
| `playwright.config.js` | headless Chromium、本地 serve |
| `tests/ui-app.spec.js` | app.html 互動（panel、搜尋、中英、⚡） |
| `tests/ui-universe.spec.js` | universe.html HUD / panel |

若未來要合併進 `main`：

```bash
npm install -D @playwright/test serve
npx playwright install chromium
npx playwright test --reporter=line
```

並決定是否由 `run_tests.py` 呼叫（Windows 上 `npx` 需 `shell=True`）。

### 建議優先補的 Playwright 案例（殘餘盲點）

1. `?c=hawking_radiation` → panel 開啟且 diverges 可見  
2. `?c=__nope__` → **應**顯示 not-found（目前靜默）  
3. 搜尋框輸入後卡片數變化  
4. domain expand 後 list 可見  
5. challenge.html 假 claim_id → error 區塊  

---

## 架構決策

| 決策 | 理由 |
|------|------|
| 先修 Python 搜尋／CLI 契約 | 不依賴 Node；CI 已有 pytest |
| challenge 靜態站 + GitHub template | Pages 無法寫 `challenges/`；與 app 卡片同一套 issue 模板 |
| CJK unigram/bigram 而非 jieba | 零第三方依賴；與「stdlib engine」一致 |
| Playwright 暫不強制進 main | 避免 Windows greenlet / npm 成為 constitution gate 硬依賴 |

---

## 與 `TESTING-BLIND-SPOTS.md` 的分工

| 文件 | 焦點 |
|------|------|
| `TESTING-BLIND-SPOTS.md` | 盲點清單、嚴重度、修復狀態 |
| `UI-TESTS-REPORT.md`（本檔） | UI/入口測試實際覆蓋與缺口 |

兩者應一併閱讀；數字以 `python run_tests.py` 當次輸出為準（list-count only，無 confidence）。
