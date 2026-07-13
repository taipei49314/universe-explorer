<!-- ai-control:begin -->
# AI 治理規則（必讀，優先於本檔其他內容）

本專案由 `.ai-control/` 治理：

1. 動手前先讀 `.ai-control/policies.md` 與 `.ai-control/project.yaml`。
2. 只能在被指派的 Task Packet 範圍內工作。在任務 worktree 裡，packet 副本是根目錄的 `TASK_PACKET.md`；找不到 packet 就先停下來向人類要一份。
3. 遵守 packet 的允許／禁止路徑。硬防線（secrets、政策檔、`git merge`、`git push --force`）由 hooks 強制執行，被擋下時不要嘗試繞過，回報即可。
4. 你不能：合併主線、發布、宣告任務完成。「完成」= 證據齊全 + 人類批准。
5. 既定決策在 `.ai-control/decisions/`。要翻案請新增一份狀態為 proposed 的 ADR，不要直接修改舊的。
6. 收工前（或額度快用完前）把進度、卡點、重要判斷的理由寫進 worktree 根目錄的 `HANDOFF.md`（證據收集時會自動歸檔）。
7. 完成的工作要 commit 到任務分支——uncommitted 的變更不會出現在證據 diff 裡。不要 commit `TASK_PACKET.md` 與 `HANDOFF.md`（已在 .gitignore）。
<!-- ai-control:end -->
