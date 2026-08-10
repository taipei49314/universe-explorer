# North Star v2 Architecture — Discovery · Cross-Domain · Reader Experience

> **Date:** 2026-08-10
> **Scope:** Local-first, constitution-gated, static dist/ output
> **Principle:** 自動化程度可以升，可回溯性不准降。

---

## 0. 北極星

> 讓知識**有管道地進來、有意義地連起來、直覺地被看見** — 同時每一條都能被任何人推翻。

三個方向，一個管線：

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                     CONSTITUTION (validator.py)                 │
  │            憲法法院 — 所有新 code 都過同一個法院                    │
  └─────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
  ╔══════════════╗    ╔══════════════╗    ╔══════════════╗
  ║  DISCOVERY   ║    ║  CROSS-DOMAIN║    ║    READER    ║
  ║  PIPELINE    ║    ║     MAP      ║    ║  EXPERIENCE  ║
  ║              ║    ║              ║    ║              ║
  ║ Source →     ║    ║ Shared src   ║    ║ Search       ║
  ║ Candidate →  ║    ║ Evidence gap ║    ║ Filter       ║
  ║ Pre-check →  ║    ║ Cross-link   ║    ║ Dual-axis Viz║
  ║ Review →     ║    ║ Conflict     ║    ║ Guided Read  ║
  ║ Human Gate   ║    ║   detect     ║    ║ Challenge    ║
  ╚══════════════╝    ╚══════════════╝    ╚══════════════╝
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               ▼
                        dist/ (static site)
```

---

## 1. 設計約束（不可違反）

| 約束 | 來源 | 實作 |
|------|------|------|
| 憲法零違反 | validator.py LAWS | 所有新模組通過同一法院 |
| AI 不自我認證 | 憲法 rule 2 | Discovery 的 LLM 只起草，不判定 |
| 無假精度 | 憲法 rule 3 | 新 UI 不顯示 %、分數、排名 |
| 引用必須 fetch | provenance.py | 新 source adapter 走同一 provenance 管線 |
| 燈號變更需記錄 | watch.py | 新 claim 進庫走 watch --commit |
| 純 Python stdlib | 現有慣例 | 新 core 模組零第三方；web 用 vanilla JS |
| 靜態 dist/ | render.py | 所有新頁面是靜態 HTML，不需 server |

---

## 2. Phase 1 — Discovery Pipeline（知識進來）

### 目標
從「手工搜尋 + 人工貼入」變成「結構化 intake → 預檢 → 人審 → 入庫」。

### 架構

```
Source Adapters          Candidate Store         Constitution Gate      Review Dashboard
─────────────────       ─────────────────       ──────────────────     ─────────────────
arxiv_adapter.py   ─┐                           precheck.py            review.html
doi_adapter.py     ─┼→ candidate_builder.py  →  (validator + axes  →   (互動式審查頁面
nasa_adapter.py    ─┤    生成結構化候選品          provenance 預檢)       accept / reject)
esa_adapter.py     ─┘    存入 candidates/                            ──→ data/*.py
                         含 evidence items                            ──→ events/
                         掛 source_ref                                ──→ watch --commit
```

### 新增模組

#### `universe_explorer/discovery/`
```
discovery/
  __init__.py
  adapters/                    # Source adapters（插件式）
    __init__.py
    base.py                    # SourceAdapter ABC
    arxiv_adapter.py           # 包裝現有 arxiv_search + arxiv_fetch
    doi_adapter.py             # 包裝現有 crossref_fetch
    nasa_adapter.py            # NASA ADS / PDS（新）
    esa_adapter.py             # ESA（新）
  candidate_builder.py         # Adapter 輸出 → 結構化候選 claim
  precheck.py                  # 候選品過 constitution 預檢
  review.py                    # 生成 review dashboard HTML
  pipeline.py                  # 端到端 orchestrator
```

#### `SourceAdapter` ABC（`adapters/base.py`）

```python
class SourceAdapter:
    """每個來源是插件，統一介面。"""
    name: str                    # "arxiv" | "doi" | "nasa" | "esa"
    def search(self, query: str, max_results: int = 10) -> List[RawResult]
    def fetch(self, source_ref: str) -> FetchedRecord    # 走 provenance 管線
    def extract_evidence(self, record: FetchedRecord) -> List[EvidenceItem]
```

#### `candidate_builder.py`

```python
def build_candidate(
    topic_id: str,
    claim_id: str,
    adapter: SourceAdapter,
    source_refs: List[str],
    human_context: str = "",     # 人類提供的背景（可選）
) -> CandidateClaim:
    """
    1. adapter.fetch() 每個 source_ref → FetchedRecord
    2. adapter.extract_evidence() → EvidenceItem list
    3. 組裝 CandidateClaim（含 evidence、sources、open_questions）
    4. 存入 candidates/<topic_id>/<claim_id>.json
    5. 不判定燈號 — 燈號是人類的事
    """
```

#### `precheck.py`

```python
def precheck(candidate: CandidateClaim) -> PrecheckReport:
    """
    在人類審查前，機械預檢：
    1. validator.validate_claim() — 憲法合規
    2. provenance.validate_provenance() — 引用可追溯
    3. axes.derive() — 證據軸自動推導
    4. proposals.propose() — 燈號建議（只排除，不核准）

    輸出 PrecheckReport：
    - violations: List[Violation]      # 必須修的
    - warnings: List[str]              # 建議注意的
    - suggested_evidence_axis: str     # E1-E5
    - compatible_statuses: Set[Status] # 可選燈號
    - excluded_statuses: Set[Status]   # 被排除的
    """
```

#### `review.py` → `dist/review.html`

```python
def generate_review_dashboard(candidates_dir: Path) -> str:
    """
    生成靜態 HTML review 頁面：
    - 候選品列表（按 topic 分組）
    - 每個候選品：來源、證據、預檢結果、建議燈號
    - Accept / Reject 按鈕（生成指令，非自動執行）
    - 憲法違規標紅，必須修才能 accept
    """
```

#### `pipeline.py` — 端到端 orchestrator

```python
def run_pipeline(
    query: str,
    topic_id: str,
    adapter_name: str = "arxiv",
    max_results: int = 10,
) -> PipelineReport:
    """
    完整流程：
    1. adapter.search(query) → RawResult list
    2. 對每個結果：build_candidate() → CandidateClaim
    3. 對每個候選品：precheck() → PrecheckReport
    4. generate_review_dashboard() → dist/review.html
    5. 輸出 PipelineReport（accepted / rejected / pending）

    人類下一步：
    - 打開 dist/review.html 審查
    - Accept 的候選品 → 編輯 data/*.py 加入正式 claim
    - python run_tests.py → python build.py
    """
```

### CLI 介面

```sh
# 搜尋 + 生成候選品 + 預檢 + 生成 review 頁面
python -m universe_explorer.discovery.pipeline "gravitational wave" --topic cosmology --adapter arxiv

# 只看預檢結果
python -m universe_explorer.discovery.precheck candidates/cosmology/gw_background.json

# 生成 review dashboard
python -m universe_explorer.discovery.review

# 列出所有待審候選品
python -m universe_explorer.discovery.review --list
```

### 與現有模組的整合

| 現有模組 | 整合方式 |
|----------|----------|
| `arxiv_search.py` | `arxiv_adapter.search()` 包裝它 |
| `arxiv_fetch.py` | `arxiv_adapter.fetch()` 包裝它 |
| `crossref_fetch.py` | `doi_adapter.fetch()` 包裝它 |
| `validator.py` | `precheck.py` 直接調用 |
| `provenance.py` | `precheck.py` 直接調用 |
| `axes.py` | `precheck.py` 直接調用 |
| `proposals.py` | `precheck.py` 直接調用 |
| `claim_draft.py` | 參考其 LLM 整合模式，但 Discovery 不強制用 LLM |
| `candidates/` | 候選品存儲位置，保持現有結構 |

---

## 3. Phase 2 — Cross-Domain Epistemic Map（知識連起來）

### 目標
從「每個 domain 是孤島」變成「跨域關聯可見、證據衝突可偵測、知識空白可標記」。

### 架構

```
Cross-Domain Detector        Domain Graph            Epistemic Map
─────────────────────       ──────────────          ──────────────
shared_source_scan.py  ─┐   graph_builder.py   →    epistemic_map.html
evidence_conflict.py   ─┼→  (跨域邊 + 共享證據       (互動式知識地圖)
gap_analyzer.py        ─┘   + 衝突 + 空白)          (力導向圖 + 篩選)
```

### 新增模組

#### `universe_explorer/crossdomain/`
```
crossdomain/
  __init__.py
  shared_source.py       # 掃描所有 claim 的 sources，找跨域共用
  evidence_conflict.py   # 同一 evidence 在不同 context 的解讀差異
  gap_analyzer.py        # 證據空白分析（哪個 domain 缺哪種證據）
  graph_builder.py       # 建構跨域知識圖
  render_map.py          # 生成 epistemic_map.html
```

#### `shared_source.py`

```python
def scan_shared_sources(topics: List[Topic]) -> List[SharedSource]:
    """
    掃描所有 claim 的 sources，找出跨域共用的 arXiv/DOI。

    輸出 SharedSource：
    - source_ref: str
    - claims: List[str]           # 引用它的 claim ids
    - domains: Set[str]           # 跨了哪些 domain
    - evidence_types: Dict[str, str]  # 每個 claim 怎麼用它

    這些自動生成為 shares_source edges，寫入 relations。
    """
```

#### `evidence_conflict.py`

```python
def detect_conflicts(topics: List[Topic]) -> List[EvidenceConflict]:
    """
    偵測同一證據在不同 claim 中的解讀差異。

    衝突條件：
    - 同一 source_ref 出現在不同 domain
    - 證據類型不同（一個當 direct，一個當 indirect）
    - 燈號差距 ≥ 2（一個 Established，一個 Frontier）

    輸出 EvidenceConflict（不含判斷，只記錄事實）：
    - source_ref
    - claim_a: {id, domain, evidence_type, status}
    - claim_b: {id, domain, evidence_type, status}
    - divergence_description: str
    """
```

#### `gap_analyzer.py`

```python
def analyze_gaps(topics: List[Topic]) -> List[EvidenceGap]:
    """
    分析每個 domain 的證據結構空白。

    分析維度：
    - 證據類型分布（direct / indirect / analog / theoretical）
    - 燈號 × 證據軸的 coverage matrix
    - open_questions 數量（人數，不打分）

    輸出 EvidenceGap：
    - domain: str
    - missing_evidence_types: Set[str]  # 完全沒有的證據類型
    - light_coverage: Dict[Status, int] # 各燈號的 claim 數
    - sparse_areas: List[str]           # claim < 2 的燈號
    """
```

#### `graph_builder.py`

```python
def build_cross_domain_graph(
    topics: List[Topic],
    shared_sources: List[SharedSource],
    conflicts: List[EvidenceConflict],
) -> DomainGraph:
    """
    建構跨域知識圖。

    節點：claim（含燈號、證據軸）
    邊：
    - 現有 authored edges（supports / requires / tensions / boundary）
    - 新增 cross_domain edges（shared_source / evidence_conflict）
    - 新增 gap edges（evidence_gap）

    輸出 DomainGraph：
    - nodes: List[GraphNode]
    - edges: List[GraphEdge]
    - clusters: Dict[str, List[str]]  # domain 分群
    """
```

#### `render_map.py` → `dist/epistemic_map.html`

```python
def render_epistemic_map(graph: DomainGraph) -> str:
    """
    生成互動式跨域知識地圖。

    視覺化：
    - 力導向圖（vanilla JS + Canvas，不用框架）
    - 節點：燈號顏色 + 大小 = evidence items 數
    - 邊：不同類型不同樣式（實線 = supports，虛線 = tensions，紅線 = conflict）
    - 篩選：按 domain、燈號、證據軸、邊類型
    - 點擊節點：展開 claim 詳情 + relations

    互動：
    - 搜尋 claim id / 關鍵詞
    - 高亮跨域路徑
    - 顯示證據衝突
    - 顯示證據空白
    """
```

### CLI 介面

```sh
# 掃描跨域共用來源
python -m universe_explorer.crossdomain.shared_source

# 偵測證據衝突
python -m universe_explorer.crossdomain.evidence_conflict

# 分析證據空白
python -m universe_explorer.crossdomain.gap_analyzer

# 生成跨域知識圖
python -m universe_explorer.crossdomain.graph_builder

# 生成 epistemic_map.html
python -m universe_explorer.crossdomain.render_map

# 全部一次跑
python -m universe_explorer.crossdomain.pipeline
```

### 與現有模組的整合

| 現有模組 | 整合方式 |
|----------|----------|
| `relations.py` | 新增 `cross_domain` 邊類型，復用現有的 LINK_KINDS |
| `axes.py` | gap_analyzer 用 derive() 分析證據結構 |
| `model.py` | 讀取所有 Topic/Claim 的 sources |
| `render.py` | 參考其靜態 HTML 生成模式 |
| `web/app.html` | epistemic_map.html 參考其互動模式 |

---

## 4. Phase 3 — Reader Experience（知識被看見）

### 目標
從「需要知道 claim id 才能查」變成「搜尋、篩選、引導式閱讀、雙軸張力一目了然」。

### 架構

```
Search Index          Filter Engine         Guided Reading        Challenge Form
─────────────        ──────────────        ───────────────       ──────────────
search_index.py  ─┐   filter_engine.py  →  guided_reading.py  →  challenge.html
(全文索引 +        ─┼→  (多維篩選)          (引導式閱讀路徑)       (站內挑戰表單)
 claim metadata)   │                       (雙軸張力視覺化)
                   └→ dist/explore-v2.html
                      (搜尋 + 篩選 + 列表)
```

### 新增模組

#### `universe_explorer/reader/`
```
reader/
  __init__.py
  search_index.py        # 全文搜尋索引（純 Python，不用外部搜尋引擎）
  filter_engine.py       # 多維篩選引擎
  guided_reading.py      # 引導式閱讀路徑
  dual_axis_viz.py       # 雙軸張力視覺化
  challenge_form.py      # 站內挑戰表單
  render_explore.py      # 生成 explore-v2.html
  render_claim_page.py   # 單一 claim 詳情頁
```

#### `search_index.py`

```python
class ClaimSearchIndex:
    """
    純 Python 全文搜尋索引。不用 Whoosh / Elasticsearch。

    索引欄位：
    - claim.id
    - claim.title
    - claim.open_questions（每個問題）
    - evidence items（description）
    - status_reason（condition descriptions）
    - competing_models
    - discussion（如果有）

    搜尋方式：
    - 關鍵詞匹配（tokenize + inverted index）
    - 布林運算（AND / OR / NOT）
    - 前綴匹配
    """

    def __init__(self, topics: List[Topic]): ...
    def search(self, query: str) -> List[SearchResult]: ...
    def suggest(self, prefix: str) -> List[str]: ...
```

#### `filter_engine.py`

```python
class ClaimFilter:
    """
    多維篩選，組合使用。

    篩選維度：
    - domain: str                    # topic id
    - status: Status                 # 燈號
    - evidence_axis: EvidenceStrength # E1-E5
    - diverges: bool                 # 雙軸分歧
    - has_open_questions: bool       # 有未解問題
    - has_competing_models: bool     # 有競爭模型
    - cross_domain: bool             # 有跨域關聯
    - evidence_type: str             # 證據類型
    """

    def filter(self, claims: List[Claim], **criteria) -> List[Claim]: ...
    def count_by(self, claims: List[Claim], dimension: str) -> Dict[str, int]: ...
```

#### `guided_reading.py`

```python
class GuidedReader:
    """
    引導式閱讀，基於現有的 7 條 reading paths。

    功能：
    - 沿 reading path 走，每步展開 claim + evidence + relations
    - 雙軸張力視覺化（divergent claims 高亮）
    - 跨域關聯提示
    - 未解問題計數（讓讀者自己數）
    """

    def get_path(self, path_id: str) -> ReadingPath: ...
    def next_step(self, current: str, path_id: str) -> Optional[Claim]: ...
    def get_context(self, claim_id: str) -> ClaimContext: ...
```

#### `dual_axis_viz.py`

```python
def generate_dual_axis_chart(topics: List[Topic]) -> str:
    """
    生成雙軸張力視覺化（純 SVG/Canvas）。

    視覺化：
    - X 軸 = 共識軸（Established → Speculative）
    - Y 軸 = 證據軸（E1 → E5）
    - 每個 claim 是一個點，位置 = (status_rank, evidence_rank)
    - divergent claims 用不同顏色/形狀標記
    - 點擊展開 claim 詳情

    這張圖讓讀者一眼看見：哪些 claim 共識強但證據弱（Hawking 輻射），
    哪些證據強但共識弱（新發現）。
    """
```

#### `challenge_form.py` → `dist/challenge.html`

```python
def generate_challenge_form(claim: Claim) -> str:
    """
    站內挑戰表單（取代 GitHub Issue）。

    表單欄位：
    - claim_id（自動填入）
    - challenge_type: "verdict" | "relation" | "source"
    - argument: str（必須引用 source_ref）
    - proposed_change: str（建議怎麼改）
    - evidence_refs: List[str]（支持挑戰的來源）

    提交後：
    - 生成 JSON 檔案存入 challenges/
    - 觸發 watch event
    - 可選：推送到 GitHub Issue（如果設定）
    """
```

#### `render_explore.py` → `dist/explore-v2.html`

```python
def render_explore_v2(topics: List[Topic], index: ClaimSearchIndex) -> str:
    """
    全新的探索頁面。

    功能：
    - 搜尋框（即時建議）
    - 左側篩選面板（domain、燈號、證據軸、divergence）
    - 右側結果列表（claim card + 雙軸 badge + 跨域標記）
    - 雙軸圖表（可互動）
    - 跨域知識地圖入口
    - 引導式閱讀入口
    """
```

### CLI 介面

```sh
# 建立搜尋索引
python -m universe_explorer.reader.search_index --build

# 搜尋
python -m universe_explorer.reader.search_index "gravitational wave"

# 篩選
python -m universe_explorer.reader.filter_engine --domain cosmology --status STRONG

# 生成 explore-v2.html
python -m universe_explorer.reader.render_explore

# 生成雙軸圖表
python -m universe_explorer.reader.dual_axis_viz

# 生成挑戰表單
python -m universe_explorer.reader.challenge_form --claim hawking_radiation
```

### 與現有模組的整合

| 現有模組 | 整合方式 |
|----------|----------|
| `render.py` | 參考其 HTML 生成模式；新頁面加入 dist/ |
| `model.py` | 讀取所有 Topic/Claim |
| `axes.py` | 雙軸視覺化用 derive() |
| `relations.py` | 引導式閱讀用 reading paths |
| `narrative.py` | claim 詳情頁顯示 narrative |
| `web/app.html` | 新頁面與現有頁面互相連結 |
| `build.py` | 新頁面加入 build 流程 |

---

## 5. Phase 整合 — 端到端流程

### 完整知識生命週期

```
                    ┌─────────────────────────────────────────┐
                    │            CONSTITUTION                  │
                    │  validator.py + provenance.py + axes.py  │
                    └─────────────────────────────────────────┘
                                      │
    ┌─────────────────────────────────┼─────────────────────────────────┐
    │                                 │                                 │
    ▼                                 ▼                                 ▼
╔═══════════════╗           ╔═══════════════╗           ╔═══════════════╗
║   DISCOVERY   ║           ║  CROSS-DOMAIN ║           ║    READER     ║
║   PIPELINE    ║           ║     MAP       ║           ║  EXPERIENCE   ║
╠═══════════════╣           ╠═══════════════╣           ╠═══════════════╣
║               ║           ║               ║           ║               ║
║ 1. Source     ║           ║ 1. Scan       ║           ║ 1. Index      ║
║    Adapter    ║           ║    shared     ║           ║    claims     ║
║    search()   ║           ║    sources    ║           ║               ║
║               ║           ║               ║           ║               ║
║ 2. Candidate  ║           ║ 2. Detect     ║           ║ 2. Search +   ║
║    Builder    ║           ║    evidence   ║           ║    Filter     ║
║               ║           ║    conflicts  ║           ║               ║
║ 3. Precheck   ║           ║               ║           ║ 3. Dual-axis  ║
║    (const.)   ║           ║ 3. Analyze    ║           ║    Viz        ║
║               ║           ║    gaps       ║           ║               ║
║ 4. Review     ║           ║               ║           ║ 4. Guided     ║
║    Dashboard  ║           ║ 4. Build      ║           ║    Reading    ║
║               ║           ║    graph      ║           ║               ║
║ 5. Human Gate ║           ║               ║           ║ 5. Challenge  ║
║    → data/*.py║           ║ 5. Render     ║           ║    Form       ║
║               ║           ║    map        ║           ║               ║
╚═══════════════╝           ╚═══════════════╝           ╚═══════════════╝
    │                                 │                         │
    └─────────────────────────────────┼─────────────────────────┘
                                      ▼
                              ┌───────────────┐
                              │   dist/       │
                              │   (static)    │
                              │               │
                              │ index.html    │
                              │ app.html      │
                              │ universe.html │
                              │ explore.html  │
                              │ review.html   │ ← NEW (Discovery)
                              │ epistemic.html│ ← NEW (Cross-Domain)
                              │ explore-v2.html│← NEW (Reader)
                              │ challenge.html│ ← NEW (Reader)
                              │ claims.json   │
                              │ feed.xml      │
                              └───────────────┘
```

### build.py 整合

```python
# 現有 build 流程 + 新增步驟
def build():
    # 現有
    validate_all_topics()
    render_all_pages()
    generate_claims_json()
    generate_feed()

    # 新增 Phase 1
    from .discovery.review import generate_review_dashboard
    generate_review_dashboard()

    # 新增 Phase 2
    from .crossdomain.render_map import render_epistemic_map
    render_epistemic_map()

    # 新增 Phase 3
    from .reader.render_explore import render_explore_v2
    render_explore_v2()
```

---

## 6. 測試策略

### 測試檔案對應

| Phase | 新測試檔案 | 覆蓋範圍 |
|-------|-----------|----------|
| Discovery | `test_discovery.py` | adapter 介面、candidate 結構、precheck 結果 |
| Discovery | `test_precheck.py` | 憲法預檢、證據軸推導、燈號排除 |
| Cross-Domain | `test_crossdomain.py` | 共用來源掃描、衝突偵測、空白分析 |
| Cross-Domain | `test_domain_graph.py` | 圖結構、邊類型、cluster |
| Reader | `test_search_index.py` | 索引建立、搜尋結果、建議 |
| Reader | `test_filter_engine.py` | 篩選邏輯、組合條件、計數 |
| Reader | `test_dual_axis.py` | 雙軸圖表數據、divergence 標記 |
| Reader | `test_challenge_form.py` | 表單生成、JSON 輸出、watch 整合 |
| 整合 | `test_integration.py` | 端到端流程、build 整合 |

### 測試原則

- 每個新模組都有獨立測試檔案
- 憲法測試（validator）對所有新 claim 一體適用
- 現有 181 個測試不能 break
- 新測試覆蓋 edge cases（空結果、無來源、跨域衝突）

---

## 7. 檔案結構總覽

```
universe_explorer/
  # 現有（不動）
  model.py
  validator.py
  axes.py
  provenance.py
  proposals.py
  watch.py
  narrative.py
  relations.py
  render.py
  surface.py
  ui_expand.py
  data/
  dataops/

  # 新增 Phase 1: Discovery Pipeline
  discovery/
    __init__.py
    adapters/
      __init__.py
      base.py
      arxiv_adapter.py
      doi_adapter.py
      nasa_adapter.py
      esa_adapter.py
    candidate_builder.py
    precheck.py
    review.py
    pipeline.py

  # 新增 Phase 2: Cross-Domain Map
  crossdomain/
    __init__.py
    shared_source.py
    evidence_conflict.py
    gap_analyzer.py
    graph_builder.py
    render_map.py
    pipeline.py

  # 新增 Phase 3: Reader Experience
  reader/
    __init__.py
    search_index.py
    filter_engine.py
    guided_reading.py
    dual_axis_viz.py
    challenge_form.py
    render_explore.py
    render_claim_page.py

# 新增測試
test_discovery.py
test_precheck.py
test_crossdomain.py
test_domain_graph.py
test_search_index.py
test_filter_engine.py
test_dual_axis.py
test_challenge_form.py
test_integration.py

# 新增 dist/ 頁面
dist/
  review.html          # Discovery review dashboard
  epistemic_map.html   # Cross-domain knowledge map
  explore-v2.html      # New explore page with search/filter
  challenge.html       # Challenge submission form

# 新增 docs
docs/
  north-star-v2-architecture.md  # 本文件
  discovery-pipeline-spec.md     # Phase 1 詳細規格
  crossdomain-spec.md            # Phase 2 詳細規格
  reader-experience-spec.md      # Phase 3 詳細規格
```

---

## 8. 實施順序

### Phase 1: Discovery Pipeline（優先）
**為什麼先做：** 解決「知識進來」的根本問題。沒有 intake pipeline，Phase 2 和 3 的內容是靜態的。

1. `discovery/adapters/base.py` — SourceAdapter ABC
2. `discovery/adapters/arxiv_adapter.py` — 包裝現有 arxiv_search + arxiv_fetch
3. `discovery/adapters/doi_adapter.py` — 包裝現有 crossref_fetch
4. `discovery/candidate_builder.py` — 候選品結構化
5. `discovery/precheck.py` — 憲法預檢
6. `discovery/review.py` — Review dashboard
7. `discovery/pipeline.py` — 端到端 orchestrator
8. `test_discovery.py` + `test_precheck.py`
9. CLI 介面

### Phase 2: Cross-Domain Map
**為什麼第二做：** 需要 Discovery 產生的候選品來豐富跨域關聯。

1. `crossdomain/shared_source.py`
2. `crossdomain/evidence_conflict.py`
3. `crossdomain/gap_analyzer.py`
4. `crossdomain/graph_builder.py`
5. `crossdomain/render_map.py`
6. `test_crossdomain.py` + `test_domain_graph.py`
7. CLI 介面

### Phase 3: Reader Experience
**為什麼最後做：** 需要 Phase 1 和 2 的內容來填充搜尋和地圖。

1. `reader/search_index.py`
2. `reader/filter_engine.py`
3. `reader/dual_axis_viz.py`
4. `reader/guided_reading.py`
5. `reader/challenge_form.py`
6. `reader/render_explore.py`
7. `test_search_index.py` + `test_filter_engine.py` + `test_dual_axis.py` + `test_challenge_form.py`
8. CLI 介面

### Phase 整合
1. `build.py` 整合新頁面生成
2. `test_integration.py` — 端到端測試
3. 現有 181 tests 回歸測試
4. `run_tests.py` 更新

---

## 9. 風險 & 緩解

| 風險 | 影響 | 緩解 |
|------|------|------|
| 新 code 違反憲法 | 系統誠信 | 所有新模組通過同一 validator；precheck 是第一道關卡 |
| Source adapter 依賴外部 API | 可用性 | 本地快取（復用 cache/）；離線模式降級到現有資料 |
| 搜尋索引效能 | 91 claims → 未來規模 | 純 Python inverted index；91 claims 毫秒級；未來可換 Whoosh |
| 跨域偵測誤報 | 品質 | 只記錄事實，不判斷；衝突標記需要人類確認 |
| 前端 JS 複雜度 | 維護 | 純 vanilla JS；不用框架；參考現有 app.html 模式 |
| Phase 之間依賴 | 進度 | 每個 Phase 可獨立運作；Phase 2/3 用現有資料就能跑 |

---

## 10. 成功標準

### Phase 1 完成
- [ ] Source adapter 介面 + arXiv / DOI adapter
- [ ] Candidate builder 生成結構化候選品
- [ ] Precheck 通過現有 validator + provenance + axes
- [ ] Review dashboard 顯示候選品 + 預檢結果
- [ ] CLI 端到端跑通：搜尋 → 候選品 → 預檢 → review.html
- [ ] 現有 181 tests 全數通過

### Phase 2 完成
- [ ] 共用來源掃描找出跨域關聯
- [ ] 證據衝突偵測標記差異
- [ ] 證據空白分析報告
- [ ] epistemic_map.html 互動式知識地圖
- [ ] 現有 181 tests 全數通過

### Phase 3 完成
- [ ] 全文搜尋 + 即時建議
- [ ] 多維篩選（domain、燈號、證據軸、divergence）
- [ ] 雙軸張力視覺化
- [ ] 引導式閱讀路徑
- [ ] 站內挑戰表單
- [ ] explore-v2.html 整合所有功能
- [ ] 現有 181 tests 全數通過

### 全案完成
- [ ] build.py 整合所有新頁面
- [ ] 端到端測試通過
- [ ] 知識生命週期完整：進 → 連 → 看 → 挑戰
- [ ] 憲法零違反

---

*自動化程度可以升，可回溯性不准降。*
