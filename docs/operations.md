# 操作手冊 — 日常維運循環

> 目的:讓任何人(包括未來的你)能照做完整的資料維運循環,不需要讀完所有 spec。

## 一鍵驗證

```sh
python run_tests.py          # 全部套件 + 憲法擋關,一個 exit code
```

## 產品表面頁(build 產出)

| 頁 | 用途 |
|----|------|
| `app.html` | 主殼:地圖 · 展開 · R-Graph · 導覽 · 對照 |
| `app.html?c=<id>` | 深鏈開宣稱 |
| `app.html?path=path_h0` | 打開閱讀路徑 |
| `app.html?tour=1` | 強制 60 秒導覽 |
| `changes.html` | 最近 digest / 事件(機械轉述) |
| `health.html` | 覆核清單 + 當日抽 3 則 |
| `about.html#how-to-read` | 讀法 + 霍金輻射範例 |
| `about.html#support` | 如何支持(不賣燈號) |

## 週節奏(P-Pulse)

- GitHub Action: `.github/workflows/weekly.yml`(週一 UTC 或手動)
- 本機:`python -m universe_explorer.dataops.source_health` → `push` → `build.py`
- 可選 secrets:`UE_WEBHOOK_URL` 等(見 transport)
- 編輯佇列:`docs/editorial-queue.md`

## 新增 / 修改一個 claim 的完整循環

1. **編輯資料**:`universe_explorer/data/<topic>.py`
   - 出處必須真實且先核實(標題/期刊/年份/DOI)。寧可少填,不編。
   - 改燈號必須同時補一筆 `status_history`(date/from/to/trigger),否則 P3 擋 build。
2. **抓取新 arXiv 來源**(若引用了):
   ```sh
   python -m universe_explorer.dataops.arxiv_fetch <arxiv_id> ...
   ```
   引用而未抓取 → validator 違憲(cite ⇒ fetch)。
3. **中文 overlay**(可選):`universe_explorer/data/translations_zh.py` 補對應翻譯;
   缺了會退回英文,不會壞。
4. **驗證**:`python run_tests.py`
5. **確認變化並提交快照**:
   ```sh
   python -m universe_explorer.dataops.watch_all           # 看 diff/事件
   python -m universe_explorer.dataops.watch_all --commit  # 接受為新基線
   ```
6. **產出 digest**(可選):`python -m universe_explorer.dataops.push`  
   可選傳輸(P5b):設定 `UE_WEBHOOK_URL` 或 SMTP 環境變數後  
   `python -m universe_explorer.dataops.push --deliver`  
   (或 `--deliver --dry-run`)。未設定則只寫 `outbox/`。
7. **重建頁面**:`python build.py` → dist/
8. **git commit**。修改引擎七檔 = 修憲:先寫 `docs/amendment-N-*.md`,
   重新蓋章 `engine_hashes.json`,commit message 註明修正案編號。

## 用 LLM 起草新 claim(T4,可選)

```sh
python -m universe_explorer.dataops.claim_draft <topic_id> <claim_id> <arxiv_id> ... [--status FRONTIER]
```

來源由你選、燈號可由你定(`--status`);本地模型只起草。草稿在你看到之前
已過完**全部**法院(憲法/詞彙/cite⇒fetch/證據軸/相容集/敘事),寫入 `drafts/`
帶 UNVERIFIED 章。你要做的是機器做不到的那件事:**核對內容忠於來源**,
然後自己把 Python 寫進 data/(屆時全部把關再跑一次)。

## 發現新來源

```sh
python -m universe_explorer.dataops.arxiv_search "<query>"   # -> candidates/(永遠 pending)
```

要引用:人工寫進 data 檔(然後第 2 步的 cite⇒fetch 自動接管)。

## 發佈

- **claude.ai artifact**(私人):`python dataops_artifact.py out.html [en|zh]` 後由 Claude 重新發佈同一 URL。
- **GitHub Pages**(公開):push 到 main,Actions 會跑 run_tests + build 並部署 —— **憲法在 CI 裡,違憲的資料上不了線**。

## 目錄地圖

| 路徑 | 是什麼 | 進 git? |
|---|---|---|
| `universe_explorer/*.py` | 引擎七檔(雜湊凍結) | ✓ |
| `universe_explorer/data/` | 領域資料 + 註冊表 + 中文 overlay | ✓ |
| `universe_explorer/dataops/` | 接線:fetch/search/watch_all/push | ✓ |
| `cache/arxiv/` | 逐字快取 + manifest(validator 驗雜湊) | ✓(是紀錄) |
| `snapshot/` | 知識狀態基線 | ✓ |
| `events/` `audit/` `outbox/` `candidates/` | 歷史紀錄 | ✓ |
| `dist/` | 產出頁面 | ✗(可重建) |
