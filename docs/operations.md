# 操作手冊 — 日常維運循環

> 目的:讓任何人(包括未來的你)能照做完整的資料維運循環,不需要讀完所有 spec。

## 一鍵驗證

```sh
python run_tests.py          # 9 個套件 + 憲法擋關,一個 exit code
```

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
7. **重建頁面**:`python build.py` → dist/
8. **git commit**。修改引擎七檔 = 修憲:先寫 `docs/amendment-N-*.md`,
   重新蓋章 `engine_hashes.json`,commit message 註明修正案編號。

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
