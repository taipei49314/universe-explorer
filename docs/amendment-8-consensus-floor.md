# 憲法修正案 #8 — 共識燈機械地板

> 修正案 #7 關閉「虛 PRIMARY → E1」。殘餘最短路徑：  
> 勾選 Established 的四條件（note=`I say so`）+ 任意過關的證據形狀  
> （例如單條假 `direct` 得 E2，或只有理論得 E4）→ 仍亮 🟢。  
> 共識軸仍由人判定；本條只加 **證據軸地板**，使人無法把燈號抬到高於  
> 已記錄證據機械允許的高度。

## 0. 修正條文

### 0.1 Established（🟢）

`status == Established` 時，`axes.derive(claim).strength` 必須是 **E1**  
（≥2 條 direct 掛在 ≥2 個可抓取 PRIMARY — 已含 amendment-7）。

| 規則 | 觸發 |
|------|------|
| `consensus_floor_established` | Established 但證據軸不是 E1 |

法理：入格條件含 `multiple_independent_replications`；E1 是機器可重算的同名要求。  
現庫 11 條 Established 量測皆為 E1（2026-08-11）。

### 0.2 Strong（🔵）

`status == Strong` 時，證據軸不得為 **E4**（純理論）或 **E5**（無證據）。  
允許 E1 / E2 / E3 — 保留 canonical 分岔（如 `hawking_radiation`：Strong × E3）。

| 規則 | 觸發 |
|------|------|
| `consensus_floor_strong` | Strong 且證據軸為 E4 或 E5 |

### 0.3 明確不關

- 不驗證 `status_reason.note` 內容真偽（仍可 `I say so`，但 **無 E1 就沒有 🟢**）。  
- 不禁止 Strong×E3 分岔。  
- 不自動升降燈號；只 **拒絕違憲組合**。  
- Competing / Frontier / Speculative 無本條地板。

## 1. 工程

- `validator.py`：在 evidence/source 檢查之後、`status_reason` 形狀檢查附近，呼叫 `axes.derive` 套用 0.1–0.2。  
- `LAWS` 登記兩規則；`constitution.md` 索引 + 法名；`engine_hashes` 重蓋。  
- 測試：`test_epistemic_adversary.py` 擴充；現庫 `build.py --check` 必須仍綠。

## 2. 驗收

1. Established + 僅 E2/E3/E4 → `consensus_floor_established`。  
2. Strong + 僅 theoretical → `consensus_floor_strong`。  
3. `hawking_radiation`（Strong×E3）仍 PASS。  
4. 全 topic constitution gate + `run_tests.py` 綠。
