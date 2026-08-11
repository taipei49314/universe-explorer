# Universe Explorer — 測試盲點分析報告

> 以一般使用者角度完整操作一次後，系統性地識別出的測試盲點。
> 分析日期：2026-08-11  
> **修訂：2026-08-11** — 補上使用者路徑盲點；下列「已修復」項見 PR `fix/user-path-blind-spots`。

---

## 操作摘要

| 項目 | 結果 |
|------|------|
| Clone & Build | ✅ 8 topic、91 claim 通過憲法 gate |
| 本地瀏覽 | ✅ 主要頁面 200 |
| CLI 操作 | ✅ search / stats / filter / graph / paths / health |
| 測試套件 | ✅ `run_tests.py` 含 **43** suites（含 `test_accessibility.py`） |
| Trust Behavior | ✅ 499 pass / 0 fail |
| UI Expand | ✅ 契約 measure 通過 |

---

## 使用者路徑盲點（本輪主軸）

一般使用者最常做的四件事——**搜尋、中文、challenge、discover**——原先覆蓋最薄。

| # | 盲點 | 嚴重度 | 狀態 |
|---|------|--------|------|
| U1 | 搜尋不索引中文 overlay；整句 CJK 當單一 token | P0 | ✅ **已修** — CJK unigram/bigram + `translations_zh` |
| U2 | `H0` / `H₀` / 含數字短 token 被 `len>2` 丟掉 | P0 | ✅ **已修** — 含 digit 且 len≥2 保留；下標正規化 |
| U3 | `ΛCDM` vs `lcdm` 不互通 | P0 | ✅ **已修** — Greek→ASCII 正規化 |
| U4 | `discover` 網路 timeout 裸 traceback；假 topic 仍打網路 | P0 | ✅ **已修** — `DiscoveryError` + topic 先驗 |
| U5 | challenge 接受假 claim / 無 checkable ref；表單無 GitHub | P1 | ✅ **已修** — 契約 + template 連結 |
| U6 | `test_accessibility.py` 不在 `run_tests.py` gate | P1 | ✅ **已修** — 已納入 SUITES |
| U7 | filter `--status strong` 大小寫敏感 | P2 | ✅ **已修**（CLI 自動 `.upper()`） |
| U8 | deep-link `?c=missing` 靜默無提示 | P2 | ⬜ 未修（前端 JS；建議 Playwright） |
| U9 | README suite 數寫 30/320 過時 | P2 | ✅ **已修** — 改為 43 suites 誠實表述 |
| U10 | health「No candidates directory」語意（看 `structured/`） | P3 | ⬜ 未修（文案/路徑） |

### 驗證指令（修後）

```bash
python -m universe_explorer search "霍金"     # ≥1，含 hawking_radiation
python -m universe_explorer search "H0"       # ≥1，含 H0_tension_*
python -m universe_explorer search "lcdm"     # 與 ΛCDM 重疊
python -m universe_explorer discover q --topic nope   # error: unknown topic…  exit 1
python -m pytest test_reader.py test_discovery.py test_accessibility.py -q
```

---

## 引擎 / 資料層盲點（先前掃描，多數仍開著）

### 🔴 高風險

#### 1. `tier_of()` 漏接合法來源種類

**位置：** `universe_explorer/model.py`（`SOURCE_TIERS`）

**問題：** keyword 子字串比對漏掉 `"peer reviewed"`、`"journal article"` 等。  
**狀態：** ✅ **部分已修（amendment-7）** — 已加 `peer reviewed`、`journal article`；`conference paper` 仍可能未接。

---

#### 2. 空白標題通過驗證

**位置：** `universe_explorer/validator.py`

**問題：** `title="   "` 可過 gate。  
**狀態：** ✅ **已修（amendment-7）** — `empty_title`

---

#### 3. 重複 source labels 不被偵測

**位置：** `universe_explorer/validator.py`  
**狀態：** ✅ **已修（amendment-7）** — `duplicate_source_label`

---

#### 4. 無檔案鎖的並發寫入

**位置：** `watch.py` / `surface.py`  
**狀態：** ⬜ 未修

---

### 🟡 中風險

#### 5. 部分 claim 不在任何 authored reading path

**狀態：** ⬜ 未修（dynamic paths 有補，但 authored 未全覆蓋）

#### 6. `narrate()` 零 evidence 行為缺契約測試

**狀態：** ⬜ 未修

#### 7. `BANNED_KEYS` 多模組重複定義

**狀態：** ⬜ 未修

#### 8. `claims.json` / `app-data.json` 無 JSON Schema

**狀態：** ⬜ 未修

---

### 🟢 低風險

#### 9–13. challenge_ops 檔名猜測、空 feed、中文 explore 字串替換、`Status.rank` O(n)、engine_hashes 未在 CI 逐檔驗證

**狀態：** ⬜ 未修

---

## 建議優先修復順序（更新）

| 優先度 | 項目 | 狀態 |
|--------|------|------|
| P0 | U1–U4 搜尋 / discover 使用者路徑 | ✅ 本 PR |
| P0 | U5 challenge 契約 | ✅ 本 PR |
| P1 | U6 accessibility 入 gate | ✅ 本 PR |
| P1 | engine: empty title / dup labels / tier_of | ⬜ 需 amendment |
| P2 | deep-link not-found UI + Playwright | ⬜ |
| P2 | reading path 全覆蓋 | ⬜ |
| P3 | health candidates 路徑文案 | ⬜ |

---

## 測試覆蓋強度

**強：** 憲法 gate、axes、provenance、adversarial、trust_behavior、build 產物形狀。  
**本 PR 補強：** 中文/H0/lcdm 搜尋契約、discover 錯誤契約、challenge 拒絕假 claim、a11y suite 入 gate。  
**仍弱：** 真實瀏覽器互動（deep-link、panel）、Playwright 未進 main gate（見 `UI-TESTS-REPORT.md`）。

---

## 相關檔案（本 PR）

| 檔案 | 變更 |
|------|------|
| `universe_explorer/reader/search_index.py` | 中文 grams、短科學 token、Greek/下標、zh overlay、cache v3 |
| `universe_explorer/discovery/pipeline.py` | `DiscoveryError`、topic 先驗、網路錯誤包裝 |
| `universe_explorer/__main__.py` | discover 友善 error；filter status/axis upper |
| `universe_explorer/reader/challenge_form.py` | 契約 + GitHub template 連結 |
| `run_tests.py` | `test_accessibility.py` |
| `test_reader.py` / `test_discovery.py` / `test_accessibility.py` | 新契約測試 |
| `README.md` | suite 數與 challenge 描述誠實化 |
