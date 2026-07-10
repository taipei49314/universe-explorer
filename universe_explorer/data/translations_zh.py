"""Chinese presentation overlay (view layer only).

This does NOT touch the frozen engine or the authored data. It maps each claim's
display text to a faithful Chinese rendering, keyed by claim id and field. What
stays in the original language on purpose: identifiers (DOIs, arXiv ids, source
labels, claim ids) and the mechanical evidence-axis derivation strings — those
are traceability anchors, not prose. Source_ref labels inside evidence stay as
labels; the DOI they resolve to is unchanged, so every claim still points at the
same real paper.

If a claim id is missing here, the renderer falls back to the English text — so
an untranslated field degrades visibly, never silently fabricates.
"""

from __future__ import annotations

from ..axes import Derivation
from ..model import Claim
from ..narrative import Localization

# --- chrome / UI labels ----------------------------------------------------
CHROME = {
    "site_title": "宇宙探索者",
    "tagline": "誠實區分我們「已知」與「未知」—— 三個領域,同一套引擎。",
    "charter": (
        "出處優先,AI 墊後。每個宣稱都掛在一筆已收錄、經核實的真實出處上。"
        "不宣告任何信心數字 —— 確定性從你能展開閱讀的證據中湧現。"
        "Topic 只是容器:燈號屬於每個 claim,不屬於 topic。"
    ),
    "footer": (
        "由宇宙探索者引擎的真實資料生成 —— 12 個宣稱、3 個領域,"
        "所有出處皆真實且經核實。燈號屬於 claim,永不屬於 topic。"
    ),
    "why_light": "為什麼是這個燈號",
    "evidence": "證據",
    "evidence_axis": "證據軸 —— 機械推導,非人工宣告",
    "competing": "競爭模型",
    "open_questions": "開放問題 —— 自己數",
    "ai_narrative": "AI 敘事 —— 整理自紀錄,絕不逾越",
    "sources": "出處",
    "status_history": "燈號遷移史",
    "axes_diverge": "雙軸分岔",
    "axes_diverge_title": "強共識卻建立在非直接證據上",
    "cm_for": "支持", "cm_against": "反對", "cm_limits": "侷限",
    "lang_switch": "English",
}

STATUS_ZH = {
    "Established Consensus": "已確立共識",
    "Strong Consensus": "強共識",
    "Competing Models": "競爭模型",
    "Frontier Research": "前沿研究",
    "Speculative": "推測性",
}

AXIS_ZH = {
    "E1": "多重獨立直接觀測",
    "E2": "單一直接觀測",
    "E3": "僅間接／類比",
    "E4": "僅理論",
    "E5": "無收錄證據",
}

EVIDENCE_TYPE_ZH = {
    "direct observation": "直接觀測",
    "indirect observation": "間接觀測",
    "analog experiment": "類比實驗",
    "theoretical derivation": "理論推導",
    "theoretical result": "理論結果",
}

CONDITION_ZH = {
    "multiple_independent_replications": "多個獨立團隊重複驗證",
    "accepted_in_mainstream_textbooks": "主流教科書接受",
    "no_mainstream_competing_theory": "無主流競爭理論",
    "no_recent_major_refutation": "近期無重大反證",
    "mainstream_model_support": "主流模型支持",
    "minor_alternatives_exist": "存在少數替代理論",
    "overall_direction_robust": "整體方向穩固",
    "two_or_more_mainstream_models": "至少兩個主流模型並存",
    "no_decisive_evidence_yet": "尚無決定性證據",
    "genuine_scientific_camps": "學界真有兩派",
    "new_discovery": "新發現",
    "insufficient_sample": "樣本不足",
    "insufficient_observation": "觀測不足",
    "rapidly_growing_literature": "文獻快速增長",
    "no_consensus_formed_yet": "尚未形成共識",
    "no_observational_evidence": "無觀測證據",
    "pure_theoretical_derivation": "純理論推導",
    "not_yet_peer_reviewed": "尚未同儕審查",
    "philosophical_inference": "哲學推論",
    "not_accepted_by_mainstream": "主流尚未接受",
}

TOPIC_ZH = {
    "black_hole": {
        "title": "黑洞",
        "summary": ("一個容器 topic,本身沒有燈號 —— 底下每個 claim 各自帶燈。"
                    "讀它的形狀:🟢 的地基(事件視界存在)撐著 🔴 的天花板(防火牆)。"),
    },
    "ocean": {
        "title": "深海",
        "summary": ("第二個 Data 層跑在完全相同的引擎上 —— 證明這套認識論與題材無關。"
                    "一樣的形狀:🟢 地基(熱泉存在)撐著 🔴 天花板(暗氧),"
                    "中間夾著一場真實的 🟡 兩派之爭(AMOC)。"),
    },
    "exoplanets": {
        "title": "系外行星",
        "summary": ("第三個領域跑在同一套引擎上 —— 而且這個再度壓測了 arXiv 的"
                    "「引用即抓取」管線。形狀依舊:🟢 地基(它們存在)撐著 🔴 天花板"
                    "(生物訊號),中間是一場真實的 🟡 兩派之爭(第九行星)。"),
    },
}

# --- per-claim content -----------------------------------------------------
# Structure: CLAIMS[claim_id] = {
#   "title": ..., "reasons": {condition: note_zh},
#   "evidence": [desc_zh, ...] (in the same order as the authored evidence list),
#   "open_questions": [...], "competing": [{name, for, against, limits}, ...] }
CLAIMS = {
    # ---- black hole -------------------------------------------------------
    "event_horizon_exists": {
        "title": "具事件視界的天體黑洞確實存在",
        "reasons": {
            "multiple_independent_replications":
                "三條獨立證據線 —— 視界尺度成像(EHT)、重力波(LIGO/Virgo)、"
                "恆星動力學(Keck/VLT)—— 各自確認了行為如黑洞的緻密天體。",
            "accepted_in_mainstream_textbooks":
                "黑洞是廣義相對論與天文物理教科書的標準內容。",
            "no_mainstream_competing_theory":
                "無主流理論質疑其存在;無視界的模仿者只是少數研究路線,非對抗性共識。",
            "no_recent_major_refutation":
                "至今無觀測推翻黑洞詮釋;每筆新資料都讓它更緊實。",
        },
        "evidence": [
            "事件視界望遠鏡解析出 M87* 周圍的環狀輻射,其大小符合廣義相對論預測的"
            "約 65 億太陽質量黑洞陰影。",
            "EHT 的第二個獨立目標 —— 銀河系中心的 Sgr A* —— 顯示的陰影符合一個"
            "約 400 萬太陽質量的黑洞。",
            "LIGO 偵測到兩個緻密天體併合的重力波;其鈴宕波形符合克爾黑洞,"
            "並在該質量下排除了中子星或古典替代方案。",
            "數十年追蹤 Sgr A* 周圍個別恆星軌道,把一個暗而緻密的質量鎖進"
            "一個任何普通物質分布都無法佔據的體積 —— 獲 2020 年諾貝爾物理獎肯定。",
        ],
        "open_questions": [
            "其表面是真正的廣義相對論視界,還是超緻密無視界模仿者(如重力星),"
            "目前受限但邏輯上未完全排除。",
            "餵養所觀測輻射的近視界電漿與磁場精細結構仍在建模中。",
        ],
    },
    "hawking_radiation": {
        "title": "黑洞放出熱的霍金輻射並緩慢蒸發",
        "reasons": {
            "mainstream_model_support":
                "此推導是彎曲時空量子場論的標準、廣泛教授的結果,全領域接受。",
            "minor_alternatives_exist":
                "少數人質疑細節(跨普朗克問題、資訊內容),但不質疑效應的存在。",
            "overall_direction_robust":
                "理論方向五十年來穩定,新研究只精修圖像(如灰體因子、末態爭論)"
                "而未動搖它。註記:強共識與缺乏直接觀測之間的落差,已在證據軸(P1.5)"
                "結構化表達,不再是這裡的手動註記。",
        },
        "evidence": [
            "將量子場論應用於黑洞的彎曲時空,霍金推導出一股溫度與質量成反比的"
            "熱通量,意味著逐漸蒸發。",
            "玻色–愛因斯坦凝聚體中的聲學視界放出具熱譜的關聯聲子對 —— "
            "這是該效應的實驗室類比,而非天文過程本身。",
        ],
        "open_questions": [
            "無直接天文偵測:對恆星質量以上的黑洞,預測溫度遠低於宇宙微波背景,"
            "故它們吸收多於放出。",
            "類比重力實驗是忠實重現了重力情形,還是只是數學相似的現象,仍有爭論。",
            "蒸發的末態(半古典推導在此失效)是未知的。",
        ],
    },
    "bbh_mergers_catalogued": {
        "title": "重力波天文學已編錄數十起緻密雙星併合",
        "reasons": {
            "new_discovery":
                "重力波天文學是新開啟的觀測管道;族群規模的併合目錄自第三次"
                "觀測run才開始。",
            "rapidly_growing_literature":
                "每次觀測 run 都倍增目錄,並產出快速增長的族群分析文獻。",
        },
        "evidence": [
            "GWTC-3 目錄回報第三次觀測 run 後半段的 35 個緻密雙星併合候選 —— "
            "包括首批確信的中子星–黑洞雙星 —— 使觀測候選累計達 90 個。",
        ],
        "open_questions": [
            "僅憑重力波資料,能否在較輕的雙星成員中乾淨區分中子星與黑洞?",
            "觀測到的併合族群對大質量恆星與雙星演化意味著什麼?",
            "隨偵測器靈敏度提升與觀測累積,族群統計會如何變動?",
        ],
    },
    "information_paradox": {
        "title": "資訊是否逃出蒸發中的黑洞",
        "reasons": {
            "rapidly_growing_literature":
                "自 2019 年起,複本蟲洞／島嶼綱領產出了快速增長的一批論文,重做此問題。",
            "no_consensus_formed_yet":
                "尚無定論:島嶼結果在玩具模型中還原出么正的佩吉曲線,但對真實黑洞的"
                "具體體機制尚無共識。",
            "insufficient_observation":
                "能決定此事的區域 —— 近普朗克尺度蒸發 —— 超出任何可想像的觀測,"
                "故它靠理論自洽而非測量推進。",
        },
        "evidence": [
            "原始論證:純熱的霍金輻射不帶資訊,故初始純態將演化為混合態,"
            "違反量子力學的么正性。",
            "近期複本蟲洞／島嶼計算還原出符合么正演化的佩吉曲線,意味資訊被保留 —— "
            "但這是在特定玩具模型中,非完整量子重力。",
        ],
        "open_questions": [
            "若資訊真能離開黑洞內部,是透過什麼具體物理機制?",
            "島嶼／複本蟲洞的結果能否從玩具模型推廣到真實的四維蒸發黑洞?",
            "此解答是否相容於光滑視界,還是會逼出視界上的結構(見防火牆 claim)?",
        ],
    },
    "firewall": {
        "title": "墜入者在視界遭遇高能「防火牆」",
        "reasons": {
            "no_observational_evidence":
                "沒有防火牆的觀測證據,也沒有觀測它的方法。",
            "pure_theoretical_derivation":
                "它是從一組假設衝突推導出的純理論後果,而非任何被觀測系統的建模預測。",
            "not_accepted_by_mainstream":
                "領域不接受它為真;許多人認為其底層張力已被島嶼／互補性論證解決。",
        },
        "evidence": [
            "Almheiri、Marolf、Polchinski 與 Sully 論證:么正性、局域性與光滑視界"
            "三者不可兼得;放棄光滑性就得到視界上一堵高能量子之牆 —— 即防火牆。",
        ],
        "open_questions": [
            "防火牆是真實特徵,還是後來被島嶼／互補性解決的假設所產生的假象?",
            "由於它位於遙遠黑洞的視界,沒有任何可想像的近期觀測能檢驗它。",
        ],
    },
    # ---- ocean ------------------------------------------------------------
    "hydrothermal_vents_exist": {
        "title": "深海海床上存在化學合成的熱泉生態系",
        "reasons": {
            "multiple_independent_replications":
                "兩支獨立的潛水器探勘(1979 Alvin/加拉巴哥、1980 RISE/東太平洋隆起)"
                "直接觀測到熱泉生態系;此後全球已編錄數百個熱泉區。",
            "accepted_in_mainstream_textbooks":
                "化學合成熱泉生態系是海洋學與海洋生物學教科書的標準內容。",
            "no_mainstream_competing_theory":
                "無主流理論質疑其存在;僅分布與生態的細節有爭論。",
            "no_recent_major_refutation":
                "四十年來後續的下潛與全球熱泉資料庫只增強了此發現。",
        },
        "evidence": [
            "潛水器 Alvin 在加拉巴哥裂谷直接觀測到溫水噴口,周圍是靠硫氧化細菌"
            "化學合成(而非陽光)維生的密集動物群落。",
            "一支獨立探勘隊(RISE)在東太平洋隆起 21°N 發現高溫黑煙囪熱泉,"
            "帶有管蟲、蛤與蟹,與加拉巴哥的類似 —— 這是第二次獨立確認。",
        ],
        "open_questions": [
            "沿全球中洋脊系統的熱泉區範圍與連通性仍在測繪中。",
            "熱泉幼體如何在孤立、短命的熱泉區之間擴散,仍只部分理解。",
        ],
    },
    "ocean_heat_uptake": {
        "title": "海洋吸收了人為過剩熱量的絕大部分",
        "reasons": {
            "mainstream_model_support":
                "「海洋主導熱吸收」是 Argo 時代觀測與歷次國際評估的一致結果。",
            "minor_alternatives_exist":
                "爭論停留在精確分配與 Argo 之前年代的量值,而非海洋的主導角色。",
            "overall_direction_robust":
                "獨立觀測系統(現場量測、衛星測高、大氣層頂輻射)指向同一方向;"
                "新資料精修數字,不動方向。",
        },
        "evidence": [
            "三十多個研究團隊對現場海溫量測(Argo 浮標與歷史剖面)的綜合分析發現,"
            "1971–2018 年間地球系統累積的熱量約 89% 儲存在海洋。",
        ],
        "open_questions": [
            "Argo 時代之前(2005 年前)的覆蓋稀疏,使早期年代的誤差棒偏寬。",
            "2000 公尺以下的深海採樣仍然不足。",
            "跨獨立觀測系統收支閉合地球能量失衡,仍是進行中的工作。",
        ],
    },
    "amoc_weakening": {
        "title": "大西洋經向翻轉環流(AMOC)正在減弱",
        "reasons": {
            "two_or_more_mainstream_models":
                "兩種主流解讀並存:代理重建的長期減弱,對上觀測重建的無顯著下降。",
            "no_decisive_evidence_yet":
                "直接觀測陣列太短,不足以確立趨勢,故兩派皆無決定性證據。",
            "genuine_scientific_camps":
                "這是物理海洋學團隊之間真實、已發表的分歧,非 AI 宣稱的兩派。",
        },
        "evidence": [
            "一個海表溫度「指紋」(副極區冷卻、灣流增暖)被解讀為 AMOC 自 20 世紀中期"
            "以來減弱約 3 Sv(約 15%)的證據。",
            "一份 30 年的 AMOC 強度重建在其期間內未發現顯著下降,主張直接紀錄太短,"
            "不足以確立人為趨勢。",
        ],
        "competing": [
            {"name": "長期減弱(代理為本)",
             "for": "海表溫度指紋與古氣候／代理重建顯示 AMOC 現處於數世紀來最弱。",
             "against": "代理是間接的;直接測量紀錄僅約二十年,本身無法顯示穩健趨勢。",
             "limits": "依賴把溫度型態換算成環流強度,這個推論本身有其不確定性。"},
            {"name": "尚無穩健的觀測下降",
             "for": "基於觀測的重建在 1981–2016 年間未顯示顯著的 AMOC 下降。",
             "against": "如此短的紀錄,或許根本無法在強烈年際變率中解析出緩慢的受迫趨勢。",
             "limits": "無法排除一個真實、但尚未在直接紀錄中達統計顯著的減弱。"},
        ],
        "open_questions": [
            "這場分歧反映的是真實的物理爭議,還是主要來自兩派比較的時段與方法不同?",
            "直接(2004 年後)觀測陣列要運作多久,才能把受迫趨勢從自然變率中分離出來?",
        ],
    },
    "ccz_biodiversity_unknown": {
        "title": "克拉里昂–克利珀頓區(CCZ)的動物多樣性多數尚未描述",
        "reasons": {
            "insufficient_sample":
                "CCZ 只有一小部分、且不均勻地被生物採樣過;所記錄的物種絕大多數未命名。",
            "rapidly_growing_literature":
                "過去十年該區的分類產出與資料庫快速增長,才促成這第一份綜合清單。",
        },
        "evidence": [
            "CCZ 後生動物相的第一份綜合清單記錄了約 5,000 個物種,據估其中 88–92% "
            "為科學上的新種,基於彙整全區的標本採樣。",
        ],
        "open_questions": [
            "CCZ 的真實總物種豐富度(估計值範圍很廣)尚屬未知。",
            "該區廣大範圍從未被採樣過。",
            "在潛在採礦擾動之前,正式分類描述能否跟上採樣速度,尚不清楚。",
        ],
    },
    "dark_oxygen_production": {
        "title": "多金屬結核在深淵海床產生「暗氧」",
        "reasons": {
            "not_accepted_by_mainstream":
                "儘管有單一篇同儕審查觀測,此宣稱並未被接受:多篇反駁、作者收回部分主張、"
                "以及期刊加註編輯說明,使它處於爭議而非確立狀態。",
        },
        "evidence": [
            "在覆有結核的深淵海床上的原位底棲艙實驗,記錄到氧氣在約兩天內上升,"
            "被詮釋為黑暗中的產氧(提出海水電解為機制)。",
            "一篇同儕審查的批評論證,這些測量與儀器假象一致,且所記錄的電壓過低不足以"
            "電解水;多位原作者此後收回關鍵主張,期刊也加註編輯說明。",
        ],
        "open_questions": [
            "在排除底棲艙與感測器假象的方法下,氧氣上升能否被獨立重現?",
            "若屬真實,是什麼機制產生它,且它是否在深淵平原上以有意義的規模發生?",
        ],
    },
    # ---- exoplanets -------------------------------------------------------
    "exoplanets_exist": {
        "title": "繞其他恆星運行的行星確實存在",
        "reasons": {
            "multiple_independent_replications":
                "兩種獨立方法(徑向速度、凌日)確認了同一類行星;此後多項巡天與儀器"
                "已發現數千顆行星。",
            "accepted_in_mainstream_textbooks":
                "系外行星是天文學教科書的標準內容,1995 年的發現更獲 2019 年諾貝爾物理獎。",
            "no_mainstream_competing_theory":
                "無主流替代方案能解釋徑向速度、凌日與直接成像的綜合證據。",
            "no_recent_major_refutation":
                "後續每一項巡天都擴大、而非動搖了這個行星族群。",
        },
        "evidence": [
            "對飛馬座 51 的徑向速度測量揭示一顆繞行週期 4.2 天的木星質量伴星 —— "
            "這是繞類太陽恆星發現的第一顆系外行星。",
            "對 HD 209458 的測光,捕捉到行星在徑向速度所預測的準確時刻橫越其恆星 —— "
            "這是一種完全獨立的偵測方法,確認了行星詮釋。",
        ],
        "open_questions": [
            "已知族群的代表性,受限於偏向大型、近距行星的偵測偏差。",
            "真正地球類比體的出現率仍在確定中。",
        ],
    },
    "proxima_b_exists": {
        "title": "最近的恆星比鄰星,擁有一顆溫帶地球質量行星",
        "reasons": {
            "multiple_independent_replications":
                "兩套獨立儀器與團隊(2016 HARPS/UVES 觀測戰役;2020 ESPRESSO,"
                "其後再獲後續 ESPRESSO 分析確認)偵測到同一行星訊號。",
            "accepted_in_mainstream_textbooks":
                "比鄰星 b 作為已知最近的系外行星,是當代天文教材與系外行星"
                "參考書的標準內容。",
            "no_mainstream_competing_theory":
                "早期的恆星活動假象疑慮已被獨立的 ESPRESSO 資料檢驗並排除;"
                "行星詮釋已無主流替代方案。",
            "no_recent_major_refutation":
                "後續的徑向速度觀測只讓偵測更加銳利。",
        },
        "evidence": [
            "徑向速度監測揭示一顆最小質量約 1.3 地球質量的行星,"
            "以 11.2 天的溫帶軌道繞行比鄰星。",
            "獨立且精度更高的 ESPRESSO 光譜儀在 2019 年的全新資料中"
            "重新偵測到同一 11.2 天訊號,確認行星並精修其最小質量。",
        ],
        "open_questions": [
            "在 M 型矮星宿主的閃焰環境下,行星是否保有大氣仍屬未知。",
            "其真實質量(而非最小質量)取決於未測得的軌道傾角。",
            "受潮汐影響的溫帶行星,其表面條件是否容許液態水仍屬開放。",
        ],
    },
    "planets_are_common": {
        "title": "在銀河系恆星周圍,行星是常態而非例外",
        "reasons": {
            "mainstream_model_support":
                "獨立的巡天方法(微重力透鏡、凌日統計、徑向速度巡天)收斂於行星的普遍性。",
            "minor_alternatives_exist":
                "方法學上對完備性修正與精確出現率仍有爭論,但不涉及普遍性本身。",
            "overall_direction_robust":
                "每一次擴大的巡天都提高、而非降低了行星豐度的推論。註記:證據的統計"
                "(間接)性質已在證據軸上結構化表達。",
        },
        "evidence": [
            "對六年微重力透鏡巡天資料的統計分析得出:銀河系恆星平均擁有一顆或更多"
            "受束縛行星 —— 行星是常態,而非例外。",
        ],
        "open_questions": [
            "適居帶內真正地球類比體的出現率,仍是統計中約束最弱的部分。",
            "出現率如何隨恆星類型、金屬豐度與銀河環境變化,仍在測繪中。",
        ],
    },
    "planet_nine": {
        "title": "有一顆第九顆巨行星形塑了遙遠古柏帶天體的軌道",
        "reasons": {
            "two_or_more_mainstream_models":
                "兩種主流解讀並存:一顆真實的遙遠行星,對上以巡天偏差解釋此群聚。",
            "no_decisive_evidence_yet":
                "尚無直接偵測,也尚無無偏的全天樣本可在兩者間裁決。",
            "genuine_scientific_camps":
                "這是動力學建模團隊與巡天團隊之間真實、已發表的爭議,非 AI 宣稱。",
        },
        "evidence": [
            "遙遠的古柏帶天體顯示出軌道角的群聚,動力學建模將其歸因於一顆位於"
            "遙遠偏心軌道上、尚未見到的巨行星。",
            "獨立的 OSSOS 巡天發現其偵測結果與均勻(非群聚)分布一致,並證明了"
            "產生群聚訊號的那些巡天存在強烈的指向偏差。",
        ],
        "competing": [
            {"name": "第九行星存在",
             "for": "所觀測到的遙遠海王星外天體軌道群聚,可由一顆遙遠的、"
                    "超級地球至海王星質量的行星在動力學上重現。",
             "against": "多年定向搜尋仍無直接偵測;群聚可能是巡天假象。",
             "limits": "隨遙遠天體樣本增長,預測的軌道與質量不斷被修正。"},
            {"name": "群聚是觀測偏差",
             "for": "一項特性明確的獨立巡天(OSSOS)在建模其偏差後,與均勻軌道角一致。",
             "against": "對綜合巡天做偏差校正後,仍有難以完全排除的殘餘群聚。",
             "limits": "個別巡天覆蓋天區有限,削弱其確認或排除群聚的能力。"},
        ],
        "open_questions": [
            "寬視場巡天(如 Rubin/LSST)會偵測到這顆行星,還是以無偏樣本殺掉群聚訊號?",
            "替代的動力學解釋(自重力盤、原初黑洞)能否在觀測上被區分?",
        ],
    },
    "trappist1b_bare_rock": {
        "title": "TRAPPIST-1 b 缺乏實質的大氣層",
        "reasons": {
            "new_discovery":
                "JWST 才剛讓地球大小系外行星的熱輻射變得可測。",
            "insufficient_sample":
                "結論建立在單一行星、單一波段的少數幾次掩星上。",
            "rapidly_growing_literature":
                "針對 TRAPPIST-1 系統的 JWST 後續觀測正快速產出論文。",
        },
        "evidence": [
            "JWST 在 15 微米測量了該行星的日側熱輻射;其高亮溫符合來自裸露日側的"
            "再輻射,且無可偵測的 CO2 大氣。",
        ],
        "open_questions": [
            "單一波段測光無法排除每一種薄大氣情境。",
            "TRAPPIST-1 系統中更外側的其他行星是否保有大氣,仍屬未定。",
            "M 型矮星活動如何剝離或保存次生大氣,是活躍的建模前沿。",
        ],
    },
    "k2_18b_biosignature": {
        "title": "K2-18 b 的大氣帶有生物訊號(DMS)",
        "reasons": {
            "not_accepted_by_mainstream":
                "DMS 的跡象顯著度低、被重分析質疑,且無生命的替代模型也能擬合資料;"
                "領域視此生物訊號解讀為尚未確立。",
        },
        "evidence": [
            "JWST 穿透光譜在富氫大氣中偵測到甲烷與二氧化碳,並帶有一個微弱、低顯著度的"
            "二甲基硫(DMS,被提議為生物標記)跡象 —— 作者自己也標明其需要驗證。",
            "光化學與氣候建模顯示,同一光譜也能由一顆無適居表面、富氣體的迷你海王星擬合,"
            "完全不需要生物圈。",
        ],
        "open_questions": [
            "更深的 JWST 觀測能否在有意義的顯著度上確認或排除 DMS?",
            "這顆行星是海洋世界(Hycean)還是富氣體的迷你海王星?",
            "考慮到已提出的非生物產生途徑,DMS 究竟是不是可靠的生物訊號?",
        ],
    },
}


# --- narrative localization (Amendment #2) ----------------------------------
# Lives in the data layer on purpose: the engine knows only the Localization
# protocol, never a language. Refs / claim ids / E-codes stay untranslated —
# they are traceability anchors. Missing per-claim translations fall back to
# the authored English (visible degradation, never fabrication).

class ZhLocalization(Localization):
    """繁體中文敘事在地化。過同一個 check() 法院。"""

    opening = "根據目前收錄的證據"

    def claim_title(self, claim: Claim) -> str:
        return CLAIMS.get(claim.id, {}).get("title", claim.title)

    def evidence_text(self, claim: Claim, i: int) -> str:
        ev = CLAIMS.get(claim.id, {}).get("evidence", [])
        return ev[i] if i < len(ev) else claim.evidence[i].description

    def evidence_type(self, claim: Claim, i: int) -> str:
        return EVIDENCE_TYPE_ZH.get(claim.evidence[i].type,
                                    claim.evidence[i].type)

    def status_name(self, claim: Claim) -> str:
        return STATUS_ZH.get(claim.status.value, claim.status.value)

    def axis_name(self, d: Derivation) -> str:
        return AXIS_ZH.get(d.strength.short, d.strength.value)

    def competing_name(self, claim: Claim, i: int) -> str:
        cms = CLAIMS.get(claim.id, {}).get("competing", [])
        if i < len(cms):
            return cms[i].get("name", claim.competing_models[i].name)
        return claim.competing_models[i].name

    def s_opening(self, claim: Claim) -> str:
        return (f"{self.opening},宣稱「{self.claim_title(claim)}」"
                f"目前的燈號為 {claim.status.light} {self.status_name(claim)}。")

    def s_evidence(self, claim: Claim, i: int) -> str:
        return (f"收錄為{self.evidence_type(claim, i)}:"
                f"{self.evidence_text(claim, i)}")

    def s_axis(self, claim: Claim, d: Derivation) -> str:
        return (f"由這些紀錄機械推導,證據軸落在 {d.strength.short}"
                f"({self.axis_name(d)})。")

    def s_diverge(self, claim: Claim) -> str:
        return ("註記:此處共識燈號與證據軸方向分岔 —— "
                "強社群共識建立在非直接證據之上。")

    def s_competing(self, claim: Claim) -> str:
        names = " 對上 ".join(
            self.competing_name(claim, i)
            for i in range(len(claim.competing_models)))
        return f"已收錄的競爭模型為:{names}。"

    def s_open_questions(self, claim: Claim) -> str:
        return "此宣稱仍記錄有開放問題;請展開下方清單、自行清點。"


ZH_LOC = ZhLocalization()
