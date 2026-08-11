# 憲法修正案 #10 — Round-3 Critical 閉合包

> 對 `docs/redteam-round3-10-critical.md` 的 C1–C10 **逐條機械閉合**（能閉的閉；不能閉的寫清殘餘）。

## 0. 條文對照

| Crit | 規則 / 措施 | 法源 ID |
|------|-------------|---------|
| C9/C3/C10 部分 | `direct` / `analog` 只能掛 **PRIMARY + fetchable** 來源 | `evidence_type_requires_primary_fetchable` |
| C4 | `validate_topic` / 預設 `validate_claim(..., check_provenance=True)` 合併 provenance | 既有 arxiv/doi 規則 |
| C5 | COMPETING 需 ≥2 個 distinct `paper_id` | `competing_needs_distinct_papers` |
| C6 | ESTABLISHED/STRONG 的 holds note 禁止**空洞套話**（I say so / because / n / x…） | `status_reason_vacuous_note` |
| C6b | ESTABLISHED/STRONG 必須有 `trace_refs`：非空、⊆ source labels；Established ≥2 | `trace_refs_missing` / `trace_refs_unknown` / `trace_refs_insufficient` |
| C8 | FRONTIER 至少 1 個 fetchable endpoint 來源 | `frontier_needs_fetchable_source` |
| C7 | 圖邊：機械 shared-source 強制 `kind=shared_source` + 渲染 disclaimer | render/graph |
| C2 | 敘事：`check` 在 claim 有 vacuous trace 時…（由 C6 擋）；compose 開頭加「records only」不變 | narrative 既有 + C6 |
| C1 | **殘餘：** 兩不同真 paper + 假 direct 文案 — 機器不讀論文。C6b+trace_refs 抬高勾選成本，**不宣稱語義關閉** | 見 §3 |
| C10 | 根因：type 仍人填；C9 限制 direct/analog 只能掛可抓 PRIMARY，**抬成本** | 連動 |

## 1. Claim 新欄位

```python
trace_refs: List[str] = field(default_factory=list)
```

- 意義：共識燈所**錨定**的 source labels（人顯式點名，不是 note 裡隱含）。  
- ESTABLISHED：≥2 個、皆為 claim.sources 的 label。  
- STRONG：≥1 個。  
- 其他燈：可空。

## 2. 空洞 note

`holds=True` 且 note strip 後（小寫）∈  
`{"i say so", "because", "n", "x", "yes", "y", "ok", "true", "holds", "todo", "...", "tbd"}`  
或長度 < 12 → `status_reason_vacuous_note`（僅 ESTABLISHED/STRONG）。

## 3. 明確不關（C1 核心）

兩篇**不同**真 PRIMARY + 任意長 direct 描述 + 合法 trace_refs + 非空洞 note  
仍可 🟢E1。關閉需人審/引用片段，**不在本修正案**。

## 4. 驗收

1. Round-3 PoC H/H2 若 note=`I say so` → 擋；若改長 note 無 trace_refs → 擋。  
2. Nobel 當 direct → 擋。  
3. Competing 單 paper → 擋。  
4. Frontier 無 fetchable → 擋。  
5. 全庫 tests 綠；圖 disclaimer 存在。
