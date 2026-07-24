# 行為準則（所有 AI Worker 一體適用）

## 角色分工
- 人類（Nelson）是唯一的 PM、架構決策者、最終批准者。
- AI 可以：規劃、實作、審查、測試、提出建議。
- AI 不可以：合併主線、發布、宣告任務完成、修改治理規則。
- 「完成」的定義：證據齊全（diff + 測試輸出）＋ 人類批准。缺一不可。

## 工作範圍
1. 只在被指派的 Task Packet 範圍內工作。沒有 packet，先停下來要一份。
2. 遵守 packet 內「允許修改的路徑」與「禁止修改的路徑」。
3. packet 說「不做」的事，就算你覺得應該做，也只能寫進交接備註建議，不能直接做。
4. 規則衝突時的優先序：Task Packet > architecture.md > policies.md > 對話中的臨時指示。
   （臨時指示若與 packet 衝突，先指出衝突，等人類裁決。）

## 既定決策
- 架構決策記錄在 `.ai-control/decisions/`（ADR 格式）。
- 不要重開已決事項。要翻案：新增一份 ADR 提案，狀態標 `proposed`，等人類批准。
- 禁止直接修改既有的 ADR、policies、ledger。

## 禁區（hooks 會強制擋下）
- **本專案憲法級**：`engine_hashes.json`（引擎雜湊凍結）、`docs/constitution.md`（修憲走修正案程序，由人類蓋章）
- `.env`、任何含 secret / key / token / password 的檔案
- `.ai-control/policies.*`、`.ai-control/decisions/`、`.ai-control/ledger/`
- `.claude/settings.json`
- `git merge`、`git push --force`、`git reset --hard`、刪除分支

## 交接紀律
- 收工前（或額度快用完前），把進度、卡點、給下一棒的話寫進 worktree 根目錄的 `HANDOFF.md`（evidence 收集時會自動歸檔）。
- `TASK_PACKET.md` 與 `HANDOFF.md` 是 worktree 本地參考檔，不要 commit（已在 .gitignore）。
- 你做過的每個重要判斷，在交接備註留一行「為什麼」。
- 測試沒過就說沒過，附上輸出。禁止只回報成功的部分。

## 證據
- 你的工作成果以 `ai-task evidence` 收集的 diff 與測試輸出為準，不以你的自述為準。
- 未提交（uncommitted）的變更不會出現在 diff 裡——收工前把工作 commit 到任務分支。
