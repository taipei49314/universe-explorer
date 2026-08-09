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
    "tagline": "誠實區分我們「已知」與「未知」—— 跨領域,同一套引擎。",
    "charter": (
        "出處優先,AI 墊後。每個宣稱都掛在一筆已收錄、經核實的真實出處上。"
        "不宣告任何信心數字 —— 確定性從你能展開閱讀的證據中湧現。"
        "Topic 只是容器:燈號屬於每個 claim,不屬於 topic。"
    ),
    "footer": (
        "由宇宙探索者引擎的真實資料生成 —— 所有出處皆真實且經核實。"
        "燈號屬於 claim,永不屬於 topic。"
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
    "seismology": {
        "title": "地震",
        "summary": ("「什麼時候會地震?」—— 大眾最想問的問題,正是科學誠實所知"
                    "與大眾期待落差最大、也最致命的領域。形狀:🟢 地基(板塊"
                    "造成地震)、🔵 真實能力(預警爭取秒數)、🟡 真實爭議(斷層"
                    "如何重複)、🟠 前沿(營運式預報)、🔴 天花板(電訊號前兆)。"
                    "第一個 provenance 主要走 Crossref DOI 管線的領域。"),
    },
    "exoplanets": {
        "title": "系外行星",
        "summary": ("第三個領域跑在同一套引擎上 —— 而且這個再度壓測了 arXiv 的"
                    "「引用即抓取」管線。形狀依舊:🟢 地基(它們存在)撐著 🔴 天花板"
                    "(生物訊號),中間是一場真實的 🟡 兩派之爭(第九行星)。"),
    },
    "dark_matter": {
        "title": "暗物質",
        "summary": ("論文級地圖(見 docs/dark-matter-paper-map.md)。僅容器、無 topic 燈。"
                    "I 🟢 質量缺失 · 🔵 ΛCDM;II 🟡 粒子 vs MOND · 🟠 小尺度;"
                    "III–IV 🟠 WIMP/直接偵測/微中子地板/mono-jet/軸子/SIDM/"
                    "星系團 σ⁄m/fuzzy/dSph · 🔴 惰性微中子與 PBH;"
                    "V 🟡 銀心過剩與 S8。身份仍開放。"),
    },
    "cosmology": {
        "title": "宇宙學",
        "summary": ("主題「宇宙」:H0 叢集 + 暴脹叢集。🟢 膨脹/CMB;🔵 加速;"
                    "🟡 H0、TRGB/造父、暴脹 vs 反彈;🟠 階梯/EDE/透鏡/汽笛/"
                    "慢滾/張量;🔴 多重宇宙與反彈取代。"),
    },
    "planets": {
        "title": "行星",
        "summary": ("主題「星球」+ 加深海洋世界叢集。🟢 年齡;🔵 成月;"
                    "🟡 晚期重轟擊;🟠 總覽/木衛二/土衛二/土衛六/羽流有機物;"
                    "🔴 冰衛星現存生命與今日火星表面適居(主流不接受)。"),
    },
    "stars": {
        "title": "恆星",
        "summary": ("恆星物理(宇宙主題)。🟢 聚變驅動;🔵 核合成與緻密殘骸;"
                    "🟡 紅超巨星問題;🟠 太陽發電機;🔴 本地常規觀測到 Pop III"
                    "(主流不接受)。"),
    },
}

# --- per-claim content -----------------------------------------------------
# Structure: CLAIMS[claim_id] = {
#   "title": ..., "reasons": {condition: note_zh},
#   "evidence": [desc_zh, ...] (in the same order as the authored evidence list),
#   "open_questions": [...], "competing": [{name, for, against, limits}, ...] }
CLAIMS = {
    # ---- seismology ---------------------------------------------------------
    "plate_tectonics_drives_earthquakes": {
        "title": "移動的板塊造成了世界上的地震",
        "reasons": {
            "multiple_independent_replications":
                "海底磁條、全球地震帶、古地磁與現代太空大地測量,各自獨立測得同一套板塊運動。",
            "accepted_in_mainstream_textbooks":
                "板塊構造是每一本現代地球科學教科書的組織框架。",
            "no_mainstream_competing_theory":
                "沒有主流替代方案能同時解釋地震分布、磁條與大地測量的聯合圖像。",
            "no_recent_major_refutation":
                "六十年來愈趨綿密的測量只讓圖像更銳利。",
        },
        "evidence": [
            "海床上測得的磁條,對稱於中洋脊並對應地磁反轉,記錄了板塊分離時新地殼的生成。",
            "MORVEL 綜合分析以擴張速率、斷層方位角與 GPS 速度,測得覆蓋幾乎整個地表的 25 個板塊的現今運動 —— 地震帶正沿著測得的板塊邊界分布。",
        ],
        "open_questions": [
            "應變如何在瀰散型板塊邊界帶與大陸內部分配,仍在測繪中。",
            "是什麼控制個別斷層地震破裂的深度極限,仍是活躍問題。",
        ],
    },
    "eew_gives_usable_warning": {
        "title": "地震預警系統能提供數秒至數十秒的可用警報",
        "reasons": {
            "mainstream_model_support":
                "預警已在數個國家以全國尺度部署,並獲各國地震機構背書。",
            "minor_alternatives_exist":
                "規模飽和、警報門檻與成本效益仍有真實爭論 —— 是細節,不是能力本身。",
            "overall_direction_robust":
                "每個已部署系統與模擬研究都指向同一方向:P 波與 S 波速差的物理"
                "可靠地換來時間。所錄證據的間接(綜述)性質已在證據軸上結構化表達。",
        },
        "evidence": [
            "對已部署系統(日本、墨西哥、美國西岸等)的綜合分析記錄:在震源附近偵測 P 波,能讓較遠的地點在強震動抵達前獲得數秒至數十秒的警報。",
        ],
        "open_questions": [
            "對最大型破裂(警報發出時規模仍在成長)的警報精度仍在改進。",
            "震央附近的盲區 —— 震動比任何警報先到 —— 是物理上不可消除的;如何溝通它是開放的設計問題。",
            "警報實際觸發多少保護行動,仍在研究中。",
        ],
    },
    "characteristic_earthquake_model": {
        "title": "個別斷層會重複「特徵型」準週期大地震",
        "reasons": {
            "two_or_more_mainstream_models":
                "特徵型/分段復發與叢集式統計地震學,是災害模型至今都在引用的兩套活框架。",
            "no_decisive_evidence_yet":
                "紀錄長度遠短於復發間隔,任一方都沒有決定性檢驗。",
            "genuine_scientific_camps":
                "古地震學派與統計學派之間數十年、含正式評論與回覆的已發表爭論 —— 非 AI 宣稱的兩派。",
        },
        "evidence": [
            "Wasatch 與聖安德魯斯斷層帶的古地震溝槽開挖,被解讀為個別斷層段傾向重複幾乎同樣大小的「特徵地震」。",
            "對建立在該圖像上的地震空區預測做統計檢驗,發現實際地震紀錄更符合叢集、非準週期的模型。",
        ],
        "competing": [
            {"name": "特徵型/地震空區模型",
             "for": "部分斷層的古地震紀錄顯示相近規模的破裂重複發生;災害圖長期依賴分段復發。",
             "against": "以空區為本的預測與其後地震的正式統計檢驗表現不佳。",
             "limits": "古地震紀錄短、定年不確定性大,「準週期」很難對單一斷層確立。"},
            {"name": "叢集式/統計地震學",
             "for": "地震目錄可被叢集統計良好描述;數個「逾期」空區持續安靜,而「剛破裂」區域再次破裂。",
             "against": "純統計模型難以解釋溝槽開挖確實顯示重複相似破裂的那些斷層。",
             "limits": "目錄時長相對復發時間太短,限制了所有統計檢驗的效力。"},
        ],
        "open_questions": [
            "更長的古地震與大地測量紀錄,會收斂到週期、叢集,還是混合式復發?",
            "物理式破裂模擬器能否在資料尚不能分辨處分辨兩種圖像?",
        ],
    },
    "oef_informs_civil_protection": {
        "title": "營運式地震預報能有效輔助民防決策",
        "reasons": {
            "no_consensus_formed_yet":
                "該把哪些模型營運化、當局該如何回應,各機構間仍未底定。",
            "rapidly_growing_literature":
                "預報實驗(CSEP 及其後繼)與各國營運系統正產出快速增長的評估文獻。",
        },
        "evidence": [
            "拉奎拉地震後的國際委員會審視全球預報實驗,結論是:機率式短期預報具有真實的 —— 儘管機率很低的 —— 技能,並發布了首份營運使用準則。",
        ],
        "open_questions": [
            "當預報的絕對機率即使放大數倍仍然很小,當局應如何行動?",
            "餘震統計模型抓住的是最重要的情境,還是只有容易的情境?",
            "如何傳達預報技能,而不觸發它本應取代的謠言?",
        ],
    },
    "van_electric_precursors": {
        "title": "地震電訊號(VAN 方法)能預測即將發生的地震",
        "reasons": {
            "not_accepted_by_mainstream":
                "儘管發表數十年,主流評估是 VAN 宣稱的成功案例經不起統計檢驗;沒有任何地震機構使用電訊號做預測。",
        },
        "evidence": [
            "希臘的大地電場測站被報告記錄到地震前的「地震電訊號」,並宣稱成功預測過震央與規模。",
            "一篇著名的主流反駁論證:地震本質上不可預測 —— 小破裂是否串聯成大地震取決於無法測量的細微條件 —— 且包括 VAN 在內的前兆成功宣稱都經不起統計檢驗。",
        ],
        "open_questions": [
            "是否存在任何物理機制,能讓破裂前的應力在宣稱的距離上產生可偵測的電訊號?",
            "任何前兆宣稱能否在前瞻性、預先登記的檢驗下(而非事後挑選)被驗證?",
        ],
    },
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
    "trappist1_inner_planets_airless": {
        "title": "TRAPPIST-1 最內側的兩顆行星缺乏厚大氣",
        "reasons": {
            "new_discovery":
                "對地球大小溫帶行星的熱輻射測量,直到 JWST 才成為可能;"
                "這是該系統最早的兩筆此類結果。",
            "insufficient_sample":
                "每顆行星的結論都建立在單一測光波段的少數幾次掩星上。",
            "rapidly_growing_literature":
                "針對 TRAPPIST-1 的 JWST 計畫持續快速產出後續論文。",
        },
        "evidence": [
            "JWST/MIRI 在 15 微米對 TRAPPIST-1 b 的次掩星測光,以高置信度"
            "偵測到行星日側熱輻射,符合幾乎無大氣重新分配熱量、"
            "且無可偵測 CO2 吸收的情形。",
            "同一技術應用於 TRAPPIST-1 c,測得約 380 K 的日側亮溫 —— "
            "足夠熱,使該行星也不利於擁有厚的富 CO2 大氣。",
        ],
        "open_questions": [
            "單一波段測光無法完全排除稀薄或特殊組成的大氣。",
            "較冷的外側行星(d 至 h)是否保有大氣,是該系統的開放前沿。",
            "兩顆無大氣的內側岩石行星,對活躍 M 矮星周圍的揮發物輸送與"
            "逃逸意味著什麼?",
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
    # ---- dark matter --------------------------------------------------------
    # ---- stars --------------------------------------------------------------
    "stars_powered_by_fusion": {
        "title": "主序星由核心核融合驅動",
        "reasons": {
            "multiple_independent_replications":
                "核理論、恆星結構、日震與微中子實驗在主序聚變上收斂。",
            "accepted_in_mainstream_textbooks":
                "聚變驅動的恆星是每本現代天文物理教科書的標準內容。",
            "no_mainstream_competing_theory":
                "沒有主流理論取代主序星的核心聚變產能。",
            "no_recent_major_refutation":
                "微中子與日震資料強化、而非推翻聚變圖像。",
        },
        "evidence": [
            "薩德伯里微中子觀測站(SNO)以帶電流與中性流通道測量太陽電子微中子,"
            "確認核心氫融合預期的通量。",
            "超級神岡偵測到大量太陽微中子在電子上的散射,獨立確認太陽光度的核融合起源。",
            "Bethe 的核反應鏈(pp 與 CNO)提供主序星經氫融合為氦的理論能量預算。",
        ],
        "open_questions": [
            "低質量恆星中對流與磁場如何與聚變驅動的結構耦合?",
            "恆星能量下關鍵稀有反應的精確速率為何?",
        ],
    },
    "stellar_nucleosynthesis_makes_elements": {
        "title": "大多數比氦重的化學元素在恆星與恆星爆炸中生成",
        "reasons": {
            "mainstream_model_support":
                "恆星與爆炸核合成是元素豐度的標準敘事。",
            "minor_alternatives_exist":
                "各產生源(AGB、CCSN、併合)相對貢獻有辯論;恆星起源本身沒有。",
            "overall_direction_robust":
                "多信使天文擴大了確認的產生源,未取代恆星核合成典範。",
        },
        "evidence": [
            "B2FH 框架描繪恆星燃燒階段與爆炸核合成途徑,建造觀測到的氦以外元素。",
            "GW170817 千新星光譜與光變曲線符合中子星併合中的 r-過程,確認重元素的恆星終點產生源。",
        ],
        "open_questions": [
            "r-過程元素有多少來自併合、多少來自罕見超新星?",
            "第一代 Population III 恆星如何播下早期金屬?",
        ],
    },
    "core_collapse_forms_ns_bh": {
        "title": "核心塌縮超新星留下中子星或黑洞",
        "reasons": {
            "mainstream_model_support":
                "大質量恆星死亡形成緻密殘骸是標準天文物理。",
            "minor_alternatives_exist":
                "爆炸引擎與質量間隙細節是活躍研究,不是殘骸形成本身的替代。",
            "overall_direction_robust":
                "脈衝星、X 射線雙星與重力波目錄持續強化殘骸圖像。",
        },
        "evidence": [
            "大質量恆星核心塌縮被提出為超新星供能並形成超緻密中子星殘骸。",
            "雙黑洞與中子星併合的重力波偵測,連同銀河脈衝星與超新星殘骸,"
            "確認恆星死亡的緻密殘骸。",
        ],
        "open_questions": [
            "中子星與黑洞殘骸的質量門檻在哪?",
            "失敗超新星安靜塌縮成黑洞有多常見?",
        ],
    },
    "red_supergiant_problem": {
        "title": "缺失高質量紅超巨星超新星前身星,是真實物理效應還是觀測偏差",
        "reasons": {
            "two_or_more_mainstream_models":
                "失敗超新星物理解釋與校準偏差解釋都活躍發表。",
            "no_decisive_evidence_yet":
                "前身星樣本仍小;截止顯著度有爭議。",
            "genuine_scientific_camps":
                "多年文獻辯論記錄了分裂。",
        },
        "evidence": [
            "IIP 型超新星位置的檔案成像找到紅超巨星前身星,質量上限遠低於預期最大 RSG 質量"
            "—— 經典「紅超巨星問題」。",
            "對熱校正與樣本偏差的再分析主張表觀質量截止可降低或消失,"
            "挑戰高質量 RSG 爆炸純物理消失的說法。",
        ],
        "competing": [
            {"name": "物理截止(失敗超新星/直接塌縮)",
             "for": "最重 RSG 可能以微弱或失敗光學超新星塌縮,解釋缺失的高質量前身星箱。",
             "against": "直接塌縮率與光度校準仍不確定。",
             "limits": "前身星樣本小。"},
            {"name": "觀測/校準偏差",
             "for": "更新的熱校正與塵埃處理可提高推論前身星質量並緩和差異。",
             "against": "即使修訂樣本也可能未完全填滿恆星模型預期的最高質量箱。",
             "limits": "依賴爆炸前測光品質。"},
        ],
        "open_questions": [
            "更大暫現源巡天會否找到超過爭議天花板的亮 RSG 前身星?",
            "失敗超新星的微中子或重力波印記能否被偵測?",
        ],
    },
    "solar_dynamo_cycle": {
        "title": "太陽約 11 年的活動週期由內部磁發電機產生",
        "reasons": {
            "rapidly_growing_literature":
                "太陽發電機理論與週期預報仍高度活躍。",
            "no_consensus_formed_yet":
                "發電機起源大綱被廣泛接受;細節引擎尚未唯一底定。",
            "insufficient_observation":
                "深層差旋層與內部磁場僅被間接約束。",
        },
        "evidence": [
            "平均場與通量輸運發電機模型產生每週期反轉極性的振盪大尺度場,"
            "為太陽週期提供領先框架。",
            "黑子紀錄、磁圖與日震約束描繪數世紀觀測中磁通量的週期浮現與遷移。",
        ],
        "open_questions": [
            "什麼決定週期振幅與蒙得型極小期?",
            "發電機能否以有用技巧預報下一週期峰值?",
        ],
    },
    "pop_iii_already_routinely_observed": {
        "title": "無金屬的 Population III 恆星在本地宇宙被常規觀測到",
        "reasons": {
            "not_accepted_by_mainstream":
                "領域不接受本地常規觀測到無金屬 Pop III 恆星。",
            "no_observational_evidence":
                "已錄證據指向早期宇宙形成,而非本地常規 Pop III 普查。",
        },
        "evidence": [
            "理論把真正無金屬的 Population III 恆星放在早期宇宙;"
            "它們不被預期為常規本地恆星族群。",
            "銀河化學演化與核合成框架把存活的本地恆星視為富金屬後代,而非原始 Pop III。",
        ],
        "open_questions": [
            "JWST 能否在高紅移分離個別 Pop III 恆星印記?",
            "是否有極貧金屬本地恆星保留純 Pop III 印記?",
        ],
    },
    # ---- exoplanets expansions ----------------------------------------------
    "radius_valley_mechanism": {
        "title": "系外行星半徑谷由光致蒸發還是核心供能質量損失刻出",
        "reasons": {
            "two_or_more_mainstream_models":
                "光致蒸發與核心供能質量損失都是半徑谷的領先已發表解釋。",
            "no_decisive_evidence_yet":
                "目前人口統計尚未唯一選定一種機制。",
            "genuine_scientific_camps":
                "活躍文獻比較並結合這兩條通道。",
        },
        "evidence": [
            "Kepler 出現率研究在約 1.5–2.0 地球半徑之間發現行星赤字 —— 半徑谷 ——"
            "分開超級地球與次海王星。",
            "核心供能質量損失模型用行星形成後自身冷卻光度剝離包層,"
            "可在不需僅靠高能恆星輻照的情況下重現山谷。",
            "由宿主星 XUV 輻照驅動的光致蒸發模型也可刻出半徑谷,位置依賴恆星類型與軌道週期。",
        ],
        "competing": [
            {"name": "光致蒸發",
             "for": "XUV 驅動流體動力學逃逸自然在觀測半徑附近為近距行星開出缺口。",
             "against": "山谷人口統計相對恆星年齡與類型,可能不在所有樣本唯一匹配純光致蒸發。",
             "limits": "依賴不確定的早期恆星 XUV 歷史。"},
            {"name": "核心供能質量損失",
             "for": "由核心冷卻熱驅動的包層損失可產生類似山谷,對恆星活動依賴較弱。",
             "against": "仍須匹配跨巡天的週期與恆星質量斜率細節。",
             "limits": "形成途徑與包層組成仍簡併。"},
        ],
        "open_questions": [
            "有年齡定年的星團是否顯示如光致蒸發預期演化的山谷?",
            "大氣金屬豐度能否打破簡併?",
        ],
    },
    "jwst_exoplanet_atmospheres": {
        "title": "JWST 穿透光譜測量系外行星大氣中的分子豐度",
        "reasons": {
            "new_discovery":
                "JWST 開啟了系外行星光譜學的新精密體制。",
            "rapidly_growing_literature":
                "早期釋放與 GO 計畫正高節奏產出大氣論文。",
            "insufficient_sample":
                "詳細分子清單相對已知人口仍只覆蓋有限行星集。",
        },
        "evidence": [
            "JWST NIRSpec/PRISM 對熱土星 WASP-39b 的穿透光譜顯示清晰二氧化碳吸收,"
            "以高置信度示範系外行星大氣中的分子偵測。",
            "JWST 對 TRAPPIST-1 類地行星的熱發射測光,把大氣表徵延伸到類地體制,"
            "儘管波長覆蓋仍稀疏。",
        ],
        "open_questions": [
            "富金屬與貧金屬熱巨行星大氣有多常見?",
            "JWST 能否穩健偵測 M 矮星周圍溫和岩石行星的大氣?",
        ],
    },
    # ---- cosmology (宇宙) ---------------------------------------------------
    "universe_is_expanding": {
        "title": "宇宙正在膨脹:遙遠星系隨距離退行",
        "reasons": {
            "multiple_independent_replications":
                "速度–距離關係已由多種距離階梯與紅移巡天重複一個世紀。",
            "accepted_in_mainstream_textbooks":
                "宇宙膨脹是每本現代宇宙學與天文學教科書的標準內容。",
            "no_mainstream_competing_theory":
                "沒有主流理論否認度規膨脹;辯論在於速率、暗能量與早期宇宙物理。",
            "no_recent_major_refutation":
                "後續巡天只精煉膨脹史,沒有推翻膨脹本身。",
        },
        "evidence": [
            "河外星雲的退行速度隨距離增加,確立線性速度–距離關係,後被認定為宇宙膨脹。",
            "哈伯太空望遠鏡關鍵計畫測量造父變星距離並校準現代哈伯圖,確認宇宙膨脹。",
        ],
        "open_questions": [
            "在系統誤差全控下,今日精確膨脹率 H0 是多少(見 H0 張力 claim)?",
            "膨脹如何與最大尺度上的結構成長耦合?",
        ],
    },
    "cmb_hot_big_bang": {
        "title": "宇宙微波背景是熱、緻密早期宇宙的遺蹟輻射",
        "reasons": {
            "multiple_independent_replications":
                "地面、氣球與多代衛星確認 CMB 光譜與各向異性圖樣。",
            "accepted_in_mainstream_textbooks":
                "CMB 作為大爆炸遺蹟是教科書宇宙學核心。",
            "no_mainstream_competing_theory":
                "沒有主流替代能在無熱緻密早期的情況下解釋黑體 CMB 加聲學峰。",
            "no_recent_major_refutation":
                "每一代實驗只讓熱大爆炸讀法更銳,沒有推翻。",
        },
        "evidence": [
            "測得高度各向同性的微波過剩天線溫度,並鑑定為宇宙背景輻射,非地表或銀河雜訊。",
            "全天衛星圖(至 Planck)測量黑體譜與 CMB 各向異性的聲學峰結構,"
            "高精度符合熱大爆炸加復合歷史。",
        ],
        "open_questions": [
            "什麼物理設定了印在 CMB 上的初始起伏?",
            "是否存在超出 ΛCDM 預期的殘餘異常(如大角度對齊)?",
        ],
    },
    "accelerated_expansion": {
        "title": "宇宙的膨脹正在加速",
        "reasons": {
            "mainstream_model_support":
                "加速膨脹是 SN Ia、BAO 與 CMB 組合在 ΛCDM 下的標準詮釋。",
            "minor_alternatives_exist":
                "修正重力與空洞替代存在,但相對暗能量/Λ 是少數綱領。",
            "overall_direction_robust":
                "後續巡天強化加速;辯論轉向暗能量微物理,而非運動學結果。"
                "證據屬宇宙學推論(間接)。",
        },
        "evidence": [
            "高紅移 Ia 型超新星比僅物質減速宇宙所預期更暗,與本地校準結合意味著加速膨脹。",
            "獨立的超新星宇宙學計畫以不同高 z 樣本得到同一結論,確立加速為多團隊結果。",
        ],
        "open_questions": [
            "加速由宇宙常數、動態暗能量場,還是大尺度修正重力驅動?",
            "超新星、BAO 與 CMB 在膨脹史上是否完全一致?",
        ],
    },
    "H0_tension_local_vs_cmb": {
        "title": "本地距離階梯測得的哈伯常數,與在 ΛCDM 下由 CMB 推論的值不一致",
        "reasons": {
            "two_or_more_mainstream_models":
                "新物理與系統誤差兩種詮釋都是對 H0 偏移活躍發表的回應。",
            "no_decisive_evidence_yet":
                "顯著度依賴資料組合;尚無共識裁定。",
            "genuine_scientific_camps":
                "宇宙學綜述與合作論文記錄多年分裂 —— 非 AI 發明的兩派。",
        },
        "evidence": [
            "以造父變星校準的 Ia 型超新星階梯(SH0ES)測得的本地 H0,"
            "系統性高於 Planck 在 ΛCDM 下由 CMB 聲學尺度推論的值。",
            "Planck 2018 基線參數在平坦 ΛCDM 內校準聲速視界時暗示較低 H0,"
            "定義了張力的早期宇宙一側。",
        ],
        "competing": [
            {"name": "新的早期或晚期宇宙物理",
             "for": "擴展(如早期暗能量、額外相對論物種、演化暗能量)在某些擬合中"
                    "可提高 CMB 推論的 H0 或改變晚期膨脹史。",
             "against": "許多擴展在 BAO、CMB 透鏡或大尺度結構再引入張力,或需微調。",
             "limits": "沒有單一擴展被全部資料唯一選定。"},
            {"name": "一側或兩側階梯未識別的系統誤差",
             "for": "距離階梯各階(造父、超新星標準化)與 CMB 前景/模型假設可移動 H0;"
                    "某些獨立階梯報告中間值。",
             "against": "多個本地分析仍偏高而 CMB+ΛCDM 仍偏低,難歸咎單一團隊錯誤。",
             "limits": "殘餘系統誤差的跨方法共識仍在形成。"},
        ],
        "open_questions": [
            "JWST 造父/TRGB 工作會消除還是加固本地 H0?",
            "哪些早期宇宙擴展能在聯合 BAO+CMB+SNe 擬合下存活?",
            "H0 張力與 S8 張力在物理上相連,還是分開?",
            "強透鏡與標準汽笛路線會收斂到哪一極?",
        ],
    },
    "shoes_local_H0_high": {
        "title": "以造父變星校準的 Ia 型超新星階梯測得偏高的本地哈伯常數(約 73 km s^-1 Mpc^-1)",
        "reasons": {
            "rapidly_growing_literature":
                "SH0ES 更新、JWST 造父論文與系統誤差再分析形成快速文獻。",
            "no_consensus_formed_yet":
                "本地高 H0 結果被高度引用,但尚未被普遍接受為無殘餘系統誤差。",
            "insufficient_observation":
                "獨立幾何錨與替代校準器仍限制單一封閉的本地值。",
        },
        "evidence": [
            "SH0ES 計畫建立幾何錨 → 造父 → SN Ia 距離階梯,報告本地 H0 明顯高於"
            "Planck ΛCDM 推論,並附詳細系統誤差預算。",
            "社群綜述把造父–SN 本地測定列為最高精度晚期宇宙 H0 路線之一,"
            "並記錄其與早期宇宙推論的持續偏移。",
        ],
        "open_questions": [
            "金屬豐度、擁擠與 SN Ia 宿主質量階仍會使 SH0ES 中心值移動多少?",
            "JWST 造父測光會否改變階梯零點?",
        ],
    },
    "cmb_lcdm_implies_low_H0": {
        "title": "在平坦 ΛCDM 下,CMB 聲學尺度資料暗示哈伯常數約 67–68 km s^-1 Mpc^-1",
        "reasons": {
            "rapidly_growing_literature":
                "CMB 參數論文與張力綜述持續更新早期宇宙 H0 一極。",
            "no_consensus_formed_yet":
                "此推論在 ΛCDM *內部*是標準;ΛCDM 是否為 H0 的正確模型仍是開放問題。",
            "insufficient_observation":
                "H0 並非由 CMB 直接測量;而是從聲速視界角尺度模型推論。",
        },
        "evidence": [
            "Planck 在平坦 ΛCDM 下的基線擬合校準聲速視界並推論 H0 ≈ 67.4,"
            "與其他早期宇宙參數緊密耦合。",
            "H0 張力綜述把 CMB+ΛCDM 路線視為與晚期宇宙階梯比較的標準早期宇宙極。",
        ],
        "open_questions": [
            "一旦允許早期暗能量或 Neff 擴展,低 H0 的模型依賴有多大?",
            "地基 CMB 實驗是否確認 Planck 的聲學尺度 H0 推論?",
        ],
    },
    "trgb_vs_cepheid_local_H0": {
        "title": "紅巨星支頂端(TRGB)與造父變星對本地距離階梯的校準在 H0 上不一致",
        "reasons": {
            "two_or_more_mainstream_models":
                "造父主導與 TRGB 主導的本地 H0 計畫都以高精度活躍發表。",
            "no_decisive_evidence_yet":
                "社群尚未共識選定單一本地校準器層級。",
            "genuine_scientific_camps":
                "SH0ES 與 CCHP 及相關交鋒記錄了距離階梯社群的真實分裂。",
        },
        "evidence": [
            "Carnegie–Chicago Hubble 計畫以 TRGB 作為替代的第二星族校準器,"
            "報告的本地 H0 低於 SH0ES 造父結果,在某些分析中減輕與 Planck 的張力。",
            "SH0ES 造父階梯持續以擴大樣本與 JWST 時代交叉檢驗報告較高本地 H0,"
            "維持晚期宇宙內部的校準器層級分歧。",
        ],
        "competing": [
            {"name": "造父階梯(SH0ES 類)更接近真相",
             "for": "大樣本造父–SN、多重錨與詳細系統誤差戰役支持高本地 H0。",
             "against": "擁擠、金屬豐度與測光零點仍是有爭議的系統誤差。",
             "limits": "依賴對擁擠場中大質量恆星測光的理解。"},
            {"name": "TRGB 階梯(CCHP 類)更接近真相",
             "for": "TRGB 是較不綁定年輕恆星形成區的第二星族標準燭;"
                    "部分 TRGB 值較靠近 CMB+ΛCDM。",
             "against": "TRGB 尖端測量、消光與樣本選擇自有系統誤差;並非所有 TRGB 分析一致。",
             "limits": "某些版本的 SN 校準器樣本小於造父路線。"},
        ],
        "open_questions": [
            "JWST 能否把造父擁擠解決到足以結束分裂?",
            "能否把 Megamaser、食雙星與 TRGB 逼到同一零點?",
        ],
    },
    "early_dark_energy_H0_fix": {
        "title": "復合前的早期暗能量成分可把 CMB 推論的哈伯常數提高到接近本地值",
        "reasons": {
            "rapidly_growing_literature":
                "H0 張力加劇後,EDE 與早期宇宙擴展論文大量湧現。",
            "no_consensus_formed_yet":
                "EDE 是領先提案,不是已確立的解決方案。",
            "insufficient_observation":
                "尚無確認的獨特 EDE 印記;約束來自全域擬合,非直接偵測新成分。",
        },
        "evidence": [
            "早期暗能量(EDE)模型在復合前注入額外能量密度,縮小聲速視界,"
            "使 CMB 資料在試圖保持聲學峰擬合的同時容納較高 H0。",
            "張力綜述把 EDE 及相關早期宇宙擴展列為領先的*提議*解決方案,"
            "同時指出許多實現仍與大尺度結構或其他資料集衝突。",
        ],
        "open_questions": [
            "EDE 能否擬合 Planck+BAO+SNe 而不惡化 S8 或其他張力?",
            "是否存在連結粒子物理的微觀 EDE 候選?",
        ],
    },
    "strong_lensing_time_delay_H0": {
        "title": "強透鏡類星體的時間延遲提供不依賴傳統距離階梯的幾何哈伯常數",
        "reasons": {
            "rapidly_growing_literature":
                "H0LiCOW/TDCOSMO 及相關透鏡 H0 論文形成活躍子領域。",
            "no_consensus_formed_yet":
                "時間延遲 H0 具競爭力但受系統誤差限制;尚非張力的唯一仲裁。",
            "insufficient_sample":
                "具精緻模型的黃金透鏡數量仍然不多。",
        },
        "evidence": [
            "H0LiCOW 合作結合透鏡類星體時間延遲與透鏡星系質量模型推論 H0,"
            "報告值常較靠近本地階梯而非 Planck ΛCDM —— 質量模型系統誤差仍在審視。",
            "H0 張力綜述把時間延遲強透鏡視為互補造父與 CMB 的關鍵一步幾何方法。",
        ],
        "open_questions": [
            "透鏡 mass-sheet 簡併仍使 H0 移動多少?",
            "更大的 TDCOSMO 樣本會拉向本地極還是 CMB 極?",
        ],
    },
    "standard_sirens_H0": {
        "title": "重力波標準汽笛可不靠經典距離階梯測量 H0",
        "reasons": {
            "rapidly_growing_literature":
                "GW170817 之後的汽笛宇宙學是快速增長的文獻。",
            "no_consensus_formed_yet":
                "汽笛作為*方法*已確立;尚未給出能裁定張力的 H0。",
            "insufficient_sample":
                "亮汽笛事件仍稀少;目前 H0 後驗仍寬。",
        },
        "evidence": [
            "雙中子星併合 GW170817 加上電磁對應體,以重力波訊號給出光度距離、"
            "以宿主給出紅移,得到首個標準汽笛 H0 約束。",
            "綜述強調標準汽笛是成熟中的第三條 H0 路線,誤差會隨重力波事件率縮小 ——"
            "目前仍太寬,無法單獨結束張力。",
        ],
        "open_questions": [
            "需要多少亮汽笛才能匹配 SH0ES 或 Planck 精度?",
            "帶統計宿主紅移的暗汽笛能否具競爭力?",
        ],
    },
    "cosmic_inflation_early_universe": {
        "title": "熱大爆炸之前存在準指數暴脹階段,並播下宇宙結構的種子",
        "reasons": {
            "rapidly_growing_literature":
                "暴脹模型建構與 CMB/大尺度結構約束形成仍在增長的龐大文獻。",
            "no_consensus_formed_yet":
                "暴脹是領先的早期宇宙框架,但不是單一已確立的微物理理論。",
            "insufficient_observation":
                "尚無直接偵測到通膨子或原初重力波以唯一鑑定模型。",
        },
        "evidence": [
            "暴脹模型提出短暫加速膨脹,解決視界與平坦性問題,並產生近乎尺度不變的原初起伏。",
            "Planck 對標量譜指數與張量–標量比的約束偏好簡單慢滾情境,"
            "同時排除大片暴脹模型空間 —— 支持性的,但非通膨子的唯一鑑定。",
        ],
        "open_questions": [
            "什麼場驅動暴脹,能量尺度為何?",
            "會否偵測到原初 B 模,張量比 r 多大?",
            "反彈或其他非暴脹早期宇宙模型是否可行?",
        ],
    },
    "inflation_slow_roll_planck": {
        "title": "CMB 資料偏好簡單慢滾暴脹勢,並約束標量譜指數",
        "reasons": {
            "rapidly_growing_literature":
                "逐模型 Planck 約束與未來 CMB 任務預估形成大量文獻。",
            "no_consensus_formed_yet":
                "偏好一類慢滾模型,而非唯一通膨子。",
            "insufficient_observation":
                "ns 與 r 上限無法鑑定單一微物理模型。",
        },
        "evidence": [
            "Planck 對原初譜的分析報告 ns < 1,並緊緊限制跑動與張量,"
            "相對許多大場模型更偏好平台型慢滾。",
            "慢滾暴脹提供標量場產生近尺度不變譜的動力學框架。",
        ],
        "open_questions": [
            "哪個具體勢(若有)能在下一代 CMB-S4/LiteBIRD 約束下存活?",
            "譜指數跑動是否可偵測?",
        ],
    },
    "primordial_tensors_undetected": {
        "title": "原初重力波 B 模仍未偵測到,並限制張量–標量比",
        "reasons": {
            "rapidly_growing_literature":
                "B 模實驗與前景清理方法是主要持續努力。",
            "no_consensus_formed_yet":
                "上限大綱穩健;尚未確立正向原初偵測。",
            "insufficient_observation":
                "無確認的原初 B 模訊號;只有 r 的上限。",
        },
        "evidence": [
            "BICEP/Keck 度尺度偏振搜尋在塵埃建模後未報告顯著原初 B 模過剩,"
            "給出張量–標量比 r 的領先上限。",
            "Planck 溫度與偏振組合同樣限制 r,並在與 BICEP/Keck 聯合時約束暴脹模型空間。",
        ],
        "open_questions": [
            "下一代 B 模實驗會否偵測到 r > 0?",
            "r 須多低才排除大類高尺度暴脹?",
        ],
    },
    "inflation_vs_noninflation_alts": {
        "title": "早期宇宙由暴脹描述,還是由反彈等非暴脹替代描述",
        "reasons": {
            "two_or_more_mainstream_models":
                "暴脹是預設框架;反彈類替代仍是活躍發表的理論綱領。",
            "no_decisive_evidence_yet":
                "暴脹下的 CMB 成功很強,但不是對所有替代的邏輯消除。",
            "genuine_scientific_camps":
                "綜述與專文記錄數十年暴脹 vs 替代的辯論。",
        },
        "evidence": [
            "CMB 約束通常在擬合 ns 並限制 r 的慢滾暴脹情境下詮釋,使暴脹成為工作標準。",
            "反彈及相關非奇異情境被發展為替代,旨在不以準 de Sitter 暴脹相取代或先於熱大爆炸。",
        ],
        "competing": [
            {"name": "暴脹熱大爆炸",
             "for": "視界/平坦性動機、近尺度不變譜、慢滾下詳細 CMB 擬合。",
             "against": "暴脹有初始條件與多重宇宙辯論;通膨子未鑑定。",
             "limits": "許多可行勢仍在;張量尚未見到。"},
            {"name": "反彈/非暴脹早期宇宙",
             "for": "試圖避免奇異開端,並在某些建構中產生擾動。",
             "against": "須面對不穩定性、各向異性與暴脹擬合的詳細 CMB 成功。",
             "limits": "沒有共識反彈模型匹配全部精密資料集。"},
        ],
        "open_questions": [
            "哪個可觀測量最乾淨區分暴脹與反彈?",
            "原初特徵或非高斯性是否偏好一派?",
        ],
    },
    "eternal_inflation_multiverse": {
        "title": "永恆暴脹產生口袋宇宙的多重宇宙,是高尺度暴脹的正確讀法",
        "reasons": {
            "not_accepted_by_mainstream":
                "對暴脹的多重宇宙讀法高度爭議,非已確立的經驗共識。",
            "philosophical_inference":
                "多重宇宙宣稱多半外推到目前可檢驗宇宙學之外的詮釋領域。",
            "pure_theoretical_derivation":
                "正面論述是理論動力學,非對其他口袋宇宙的確認觀測。",
        },
        "evidence": [
            "某些暴脹動力學一般性地導致永恆暴脹與因果斷開區域的多重宇宙 ——"
            "這是超出 CMB 資料能直接確認的理論外推。",
            "精密 CMB 約束檢驗暴脹*勢*與譜;它們並不觀測上確立多重宇宙本體論。",
        ],
        "open_questions": [
            "在可行高尺度模型中永恆暴脹是否不可避免?",
            "多重宇宙是否有任何經驗印記?",
        ],
    },
    "cyclic_or_bounce_replaces_bb": {
        "title": "循環或反彈宇宙學取代熱大爆炸奇點,成為正確的早期宇宙描述",
        "reasons": {
            "not_accepted_by_mainstream":
                "熱大爆炸加暴脹仍是工作標準;反彈/循環是少數理論綱領。",
            "pure_theoretical_derivation":
                "正面論述是理論建構,不是已確認取代熱大爆炸經驗核心。",
        },
        "evidence": [
            "反彈與循環情境試圖以先前收縮相取代或補充奇異熱大爆炸,"
            "仍是活躍理論綱領,尚未有決定性觀測相對於暴脹加熱大爆炸做出選擇。",
        ],
        "open_questions": [
            "反彈模型是否產生可區分的 CMB 或重力波印記?",
            "它們能否滿足奇點與不穩定性約束?",
        ],
    },
    # ---- planets (星球) -----------------------------------------------------
    "solar_system_age": {
        "title": "太陽系約在 45.6 億年前由塌縮的分子雲形成",
        "reasons": {
            "multiple_independent_replications":
                "多實驗室與多同位素系統將早期太陽系物質定年在 ~4.56 Ga。",
            "accepted_in_mainstream_textbooks":
                "~4.5–4.6 Ga 太陽系年齡是行星科學標準內容。",
            "no_mainstream_competing_theory":
                "沒有主流年表取代以 CAI 為錨的系統形成年齡。",
            "no_recent_major_refutation":
                "精煉只銳化絕對年齡,不推翻 Ga 量級。",
        },
        "evidence": [
            "隕石中富鈣鋁包裹體(CAI)的鉛同位素年齡,將最古老太陽系固體定在約 4.567 Ga。",
            "CAI 與球粒的精煉 Pb–Pb 年代學確認最早固體的短暫形成區間,以放射定年錨定太陽系年齡。",
        ],
        "open_questions": [
            "巨行星在 CAI 形成後多快成長?",
            "誕生環境是星團還是孤立雲?",
        ],
    },
    "moon_giant_impact": {
        "title": "月球由類火星天體與早期地球的巨大撞擊形成",
        "reasons": {
            "mainstream_model_support":
                "大碰撞是行星科學中月球起源的標準模型。",
            "minor_alternatives_exist":
                "捕獲與共形成變體存在,但相對撞擊是少數。",
            "overall_direction_robust":
                "辯論精煉撞擊參數與同位素混合,而非廣義撞擊框架。",
        },
        "evidence": [
            "流體動力模擬顯示大碰撞可把貧鐵、富矽酸鹽物質送入地球軌道,"
            "符合月球低鐵核比例與軌道角動量。",
            "地–月同位素相似性與動力學約束推動撞擊變體(含高角動量情境),"
            "同時保持大碰撞為領先形成框架。",
        ],
        "open_questions": [
            "哪種撞擊幾何最符合地月同位素近乎同一?",
            "撞擊者的核結局如何?",
        ],
    },
    "late_heavy_bombardment": {
        "title": "約 39 億年前內太陽系曾出現短暫災難性的晚期重轟擊、衝擊率驟升",
        "reasons": {
            "two_or_more_mainstream_models":
                "災變與連續下降兩種讀法都在行星年表中活躍發表。",
            "no_decisive_evidence_yet":
                "有限的月球取樣使通量史無法唯一確定。",
            "genuine_scientific_camps":
                "數十年已發表辯論記錄了真實分裂。",
        },
        "evidence": [
            "月球撞擊熔岩年齡在 ~3.9 Ga 附近的叢集,曾被解讀為全太陽系尺度的災變 —— 經典晚期重轟擊。",
            "再分析主張取樣偏差與重置年齡可在無真實全系統災變下產生表觀年齡尖峰,"
            "偏向轟擊更平滑的下降。",
        ],
        "competing": [
            {"name": "災變性晚期重轟擊",
             "for": "月球熔岩年齡叢集與盆地年表長期被讀作 ~3.9 Ga 附近的衝擊尖峰。",
             "against": "樣品可能過度代表少數事件;動力學觸發仍有爭議。",
             "limits": "阿波羅取樣地理有限。"},
            {"name": "無尖銳災變的下降式轟擊",
             "for": "年齡資料的統計重評估允許連續下降;某些動力學模型不需要晚期尖峰。",
             "against": "某些盆地與隕石紀錄在特定重建中仍偏好晚期上揚。",
             "limits": "早期衝擊通量的絕對校準仍不確定。"},
        ],
        "open_questions": [
            "Artemis 時代樣品能否打破取樣偏差簡併?",
            "小行星帶與地球紀錄是否要求與月球相同的通量史?",
        ],
    },
    "ocean_worlds_icy_moons": {
        "title": "若干冰衛星今日擁有地下液態水海洋",
        "reasons": {
            "rapidly_growing_literature":
                "Europa Clipper、JUICE 與恩克拉多斯任務研究推動快速增長的海洋世界文獻。",
            "no_consensus_formed_yet":
                "數顆衛星有強有力證據,但海洋性質與完整清單仍在精煉。",
            "insufficient_observation":
                "尚無已確認地下海洋的原位取樣送回;證據是地球物理與遙測。",
        },
        "evidence": [
            "伽利略號在木衛二的磁力計資料顯示感應磁場,符合全球導電層,"
            "被解讀為含鹽地下海洋。",
            "卡西尼對土衛二物理天平動的測量要求冰殼與全球液層解耦,"
            "支持餵養南極羽流的地下海洋。",
        ],
        "open_questions": [
            "哪些衛星的海洋與岩石接觸足夠久以產生有趣化學?",
            "未來任務能否在羽流或冰中偵測 unambiguously 的生物訊號?",
        ],
    },
    "europa_induced_field_ocean": {
        "title": "木衛二擁有由感應磁場推論的全球含鹽地下海洋",
        "reasons": {
            "rapidly_growing_literature":
                "Europa Clipper 與 JUICE 持續推動地球物理與行星科學文獻。",
            "no_consensus_formed_yet":
                "地下海洋是領先詮釋;細節性質仍依賴模型。",
            "insufficient_observation":
                "無原位海洋樣品;證據是磁場與遙測。",
        },
        "evidence": [
            "伽利略磁力計在木衛二測得時變感應場,符合全球導電殼,"
            "解讀為冰下含鹽液態水海洋。",
            "更早的飛掠已顯示需要近表面導電層的感應響應。",
        ],
        "open_questions": [
            "海洋鹽度、厚度與冰殼厚度為何?",
            "海洋是否接觸岩石以允許熱液化學?",
        ],
    },
    "enceladus_plume_global_ocean": {
        "title": "土衛二從全球地下海洋噴出水富集羽流",
        "reasons": {
            "rapidly_growing_literature":
                "卡西尼遺產分析與任務構想維持大量文獻。",
            "no_consensus_formed_yet":
                "全球海洋加羽流是領先圖像;細節管路仍有辯論。",
            "insufficient_observation":
                "無登陸或送回的海洋樣品;羽流化學是代理。",
        },
        "evidence": [
            "卡西尼成像並取樣土衛二南極地形噴出的水富集噴流,確立向太空的活躍噴發。",
            "測得的物理天平動要求冰殼與全球液層解耦,把羽流源區連到整月海洋而非僅局部海。",
        ],
        "open_questions": [
            "南極下海洋–岩石交互有多連續?",
            "羽流物質有多少是新鮮海洋噴霧、多少是冰風化層?",
        ],
    },
    "titan_subsurface_ocean": {
        "title": "土衛六冰殼下擁有深層地下水海洋",
        "reasons": {
            "rapidly_growing_literature":
                "Dragonfly 時代的土衛六科學使內部海洋模型保持活躍。",
            "no_consensus_formed_yet":
                "地下海洋被廣泛偏好;厚度與組成仍不確定。",
            "insufficient_observation":
                "推論是地球物理;無直接海洋通道。",
        },
        "evidence": [
            "卡西尼對土衛六潮汐響應的重力測量暗示解耦殼層與高密度流體層,"
            "解讀為地下海洋。",
            "完整卡西尼資料集的更新重力場解精煉內部結構,並與冰殼下全球深海一致。",
        ],
        "open_questions": [
            "海洋深度、鹽度與矽酸鹽接觸如何?",
            "表面有機物如何耦合到任何深層水化學?",
        ],
    },
    "enceladus_plume_organics": {
        "title": "土衛二羽流含來自內部水環境的複雜有機分子",
        "reasons": {
            "rapidly_growing_literature":
                "羽流化學論文仍是高產量土衛二主題。",
            "no_consensus_formed_yet":
                "已報告複雜有機物;生物學詮釋尚未確立。",
            "insufficient_observation":
                "冰粒譜不是送回的海洋樣品;途徑仍依賴模型。",
        },
        "evidence": [
            "卡西尼宇宙塵分析器對羽流冰粒的質譜顯示大分子有機物,"
            "符合與液態水接觸的複雜有機庫。",
            "羽流本身是觀測到的、持續從南極裂縫噴出的水富集物質,提供被取樣的冰粒。",
        ],
        "open_questions": [
            "有機物是熱液、原初,還是兩者皆有?",
            "是否包含 unambiguous 生物訊號,或僅有非生物複雜性?",
        ],
    },
    "ocean_world_life_today": {
        "title": "至少一個冰衛星地下海洋中今日存在現存生命",
        "reasons": {
            "not_accepted_by_mainstream":
                "領域不接受任何冰衛星現存生命偵測;有機物與海洋僅動機搜尋。",
            "no_observational_evidence":
                "已錄證據支持海洋與有機物,不支持生物體。",
        },
        "evidence": [
            "土衛二羽流冰粒中的複雜有機物展示海洋世界環境中的有趣化學,"
            "但不構成對活體生物的偵測。",
            "地下海洋的地球物理證據確立適居*潛力*,而非生命存在。",
        ],
        "open_questions": [
            "羽流或冰殼中什麼測量可算決定性生物訊號?",
            "如何排除非生物有機複雜性?",
        ],
    },
    "mars_sustained_surface_habitability_now": {
        "title": "火星目前維持適合廣泛類地生命的表面條件",
        "reasons": {
            "not_accepted_by_mainstream":
                "行星科學不接受今日火星在類地意義上廣為表面適居;"
                "興趣在過去適居與地下生態位。",
            "no_observational_evidence":
                "沒有確認證據支持廣泛的現今表面適居;已錄證據指向過去環境與嚴苛現今表面。",
        },
        "evidence": [
            "氣候與大氣研究強調今日火星寒冷、大氣稀薄、表面氧化 ——"
            "對廣泛類地表面生命嚴苛,即使早期火星可能更濕。",
            "好奇號在蓋爾隕石坑的結果支持過去可適居的水環境 ——"
            "關乎古代火星,不是現今全球表面適居的證明。",
        ],
        "open_questions": [
            "受保護的地下生態位今日是否承載生命?",
            "任務設計應如何把過去適居與現今生物訊號搜尋分開?",
        ],
    },
    "mass_discrepancy_observed": {
        "title": "在廣義相對論下,僅憑可見物質無法解釋觀測到的星系動力學與星系團質量圖",
        "reasons": {
            "multiple_independent_replications":
                "運動學質量缺失(旋轉曲線、速度彌散)與重力透鏡質量圖,已由多個獨立團隊"
                "在多個系統上重複;子彈星系團是透鏡與 X 射線的尖銳交叉檢驗。",
            "accepted_in_mainstream_textbooks":
                "星系質量缺失與星系團暗質量成分是天文物理與宇宙學教科書的標準內容。",
            "no_mainstream_competing_theory":
                "沒有主流綱領否認「在 GR 加可見物質下存在觀測落差」;真正的辯論是詮釋"
                "(粒子暗物質 vs 修正動力學),不是資料缺口本身。",
            "no_recent_major_refutation":
                "後續巡天與透鏡觀測只讓落差更大、更清楚,沒有抹除它。",
        },
        "evidence": [
            "螺旋星系的光學旋轉曲線在大半徑仍大致平坦;若只有發光盤,在牛頓/GR 重力下"
            "應呈克卜勒式下降 —— 此質量缺失已在多系統重複。",
            "子彈星系團中,弱透鏡質量峰與碰撞剝離的 X 射線重子氣體在空間上錯開 ——"
            "這是一條獨立於運動學的證據:多數致密質量並不跟著熱氣體走。",
        ],
        "open_questions": [
            "替代重力理論能吸收多少星系尺度落差、同時又不在星系團與宇宙學測試上失敗,"
            "仍是開放辯論(見競爭模型 claim)。",
            "矮星系與低表面亮度星系中非發光成分的詳細徑向分布仍在精煉。",
        ],
    },
    "lcdm_includes_cold_dm": {
        "title": "標準宇宙學模型需要一個佔優的非重子冷暗物質成分",
        "reasons": {
            "mainstream_model_support":
                "含冷暗物質的 ΛCDM 是主要宇宙學合作與教科書的基線;CMB 與大尺度結構"
                "都與之吻合。",
            "minor_alternatives_exist":
                "修正重力與溫/自作用變體是研究路線,尚未取代 ΛCDM 作為工作標準。",
            "overall_direction_robust":
                "數十年改進的 CMB 與巡天資料只收緊、從未取消非重子冷成分。"
                "證據屬宇宙學推論(間接),已在證據軸上結構化表達。",
        },
        "evidence": [
            "Planck CMB 功率譜結合其他宇宙學探針,要求冷暗物質密度參數遠高於由"
            "大爆炸核合成與聲學峰結構固定的重子密度。",
            "主流綜述綜合了非重子暗物質的多探針證據(CMB、大尺度結構、星系團),"
            "並把該證據與仍開放的粒子身份問題分開。",
        ],
        "open_questions": [
            "輕微張力(如 H0、S8)可能精煉參數,但不必然取消基線模型中的冷暗成分。",
            "是否允許一小部分溫暗物質或自作用暗物質,是活躍的建模問題。",
        ],
    },
    "particle_vs_modified_gravity": {
        "title": "星系動力學由粒子暗物質暈解釋,還是由修正牛頓動力學解釋",
        "reasons": {
            "two_or_more_mainstream_models":
                "粒子 CDM 是宇宙學標準;MOND 類動力學對星系標度律仍是活躍、經同儕審查的"
                "研究綱領 —— 兩者都作為活框架出現在文獻中。",
            "no_decisive_evidence_yet":
                "沒有單一觀測在所有尺度上關閉辯論:星系團傾向無碰撞質量,"
                "而某些星系規律仍讓修正動力學有空間。",
            "genuine_scientific_camps":
                "已發表綜述、專題會議與對立論文記錄了真實分裂 —— 非 AI 發明的兩派。",
        },
        "evidence": [
            "修正牛頓動力學(MOND)在極低加速度下改寫力定律,使平坦旋轉曲線無需粒子暈"
            "即可出現,並以少數自由參數擬合許多星系標度關係。",
            "子彈星系團中透鏡質量與碰撞氣體的分離,被廣泛用作「多數質量無碰撞」的證據"
            "—— 符合粒子暗物質預期,也是純修正重力方案的嚴峻考驗。",
            "搜尋現況綜述把粒子暗物質視為宇宙學與星系團資料的領先詮釋,同時承認星系"
            "現象學仍支撐修正動力學研究路線。",
        ],
        "competing": [
            {"name": "粒子暗物質暈(ΛCDM 典範)",
             "for": "CMB 與大尺度結構需要非重子物質;星系團透鏡錯位符合無碰撞質量;"
                    "N-body 暈階層式形成結構。",
             "against": "小尺度問題(核 vs 尖點、衛星豐度、旋轉曲線多樣性)仍在激烈辯論。",
             "limits": "粒子本身未被偵測;常訴諸重子回饋以調和模擬與星系。"},
            {"name": "修正動力學(MOND 及其相對論推廣)",
             "for": "許多星系標度律(如重子 Tully–Fisher)自然出現;每星系自由參數少於"
                    "彈性暈擬合。",
             "against": "星系團與宇宙學在不加額外不可見質量或場時仍然困難;"
                        "子彈星系團類系統是持續挑戰。",
             "limits": "建立穩定、與宇宙學相容且通過全部測試的相對論理論尚未完成。"},
        ],
        "open_questions": [
            "相對論 MOND 類理論能否在不實質重引入暗質量的情況下滿足 CMB 與星系團約束?",
            "小尺度 CDM 張力有多少是重子物理、多少是新暗部門物理?",
            "哪些即將到來的巡天或實驗室搜尋最能乾淨區分兩條綱領?",
        ],
    },
    "dm_particle_identity": {
        "title": "暗物質的粒子身份仍然未知",
        "reasons": {
            "no_consensus_formed_yet":
                "學界共識是重子預算缺了東西,但對「是哪一種粒子(若有的話)」沒有共識。",
            "rapidly_growing_literature":
                "直接偵測、軸子與理論論文隨零結果重塑參數空間而快速累積。",
            "insufficient_observation":
                "沒有任何實驗室或天文通道產出被領域接受為暗物質的確認粒子偵測。",
        },
        "evidence": [
            "一篇重要綜述勾勒後 WIMP 時代:數十年直接、間接與對撞機搜尋尚未鑑定"
            "暗物質粒子,同時許多動機充分的候選仍然成立。",
            "LUX-ZEPLIN 雙相氙探測器未報告顯著的 WIMP–核子散射過剩,給出領先上限,"
            "排除大片經典弱尺度 WIMP 參數空間。",
        ],
        "open_questions": [
            "暗物質是 WIMP、軸子/ALP、惰性微中子、暗部門,還是尚未寫出的東西?",
            "直接偵測零結果是把領域推向更輕/更弱相互作用,還是推向非粒子選項?",
            "未來十年哪一條實驗通道最可能給出正向鑑定?",
        ],
    },
    "pbh_all_dark_matter": {
        "title": "原初黑洞構成全部暗物質",
        "reasons": {
            "not_accepted_by_mainstream":
                "標準宇宙學以冷粒子暗物質為基線;「全部暗物質都是原初黑洞」是少數情境,"
                "且受觀測強烈擠壓。",
            "pure_theoretical_derivation":
                "正面論述主要是理論可能性加上約束地圖,而非已確認、能對上全部 DM 預算的"
                "族群。",
        },
        "evidence": [
            "一篇全面綜述顯示:多數原初黑洞質量窗口已被微重力透鏡、動力學、吸積與"
            "重力波緊緊約束;僅剩有限窗口,且「全部 DM 都是 PBH」不是主流預設。",
        ],
        "open_questions": [
            "是否仍有開放質量窗口允許 PBH 佔可觀 DM 比例而不違反既有界限?",
            "未來重力波觀測能否裁定或進一步擠壓那些窗口?",
        ],
    },
    "small_scale_cdm_challenges": {
        "title": "冷暗物質在星系與衛星尺度上面對未解的小尺度挑戰",
        "reasons": {
            "rapidly_growing_literature":
                "小尺度結構、流體動力模擬與 SIDM 現象學形成快速增長、有專題綜述的文獻。",
            "no_consensus_formed_yet":
                "領域沒有共識認定 CDM 在小尺度已被證偽,也沒有共識認定重子物理已完全解決所有張力。",
            "insufficient_observation":
                "衛星完備性、暈密度剖面與回饋校正,對決定性檢驗仍不足。",
        },
        "evidence": [
            "一篇重要綜述整理無碰撞 CDM 模擬與觀測之間持續的小尺度張力 ——"
            "包括尖點/核結構、缺失衛星、too-big-to-fail —— 並強調重子物理與巡天不完備仍是活躍混淆因素。",
            "自作用暗物質被發展為一種粒子物理回應:速度相依散射可加熱暈並幫助形成核,"
            "把小尺度結構連到微觀截面,同時不必放棄大尺度上的 CDM 成功。",
        ],
        "open_questions": [
            "各張力有多少來自重子回饋、多少來自新暗部門物理?",
            "矮星系、強透鏡與恆星流的哪種組合最能乾淨隔離暗物質微物理?",
            "這些張力指向單一共同機制,還是多個不相關系統誤差?",
        ],
    },
    "axion_dm_candidate": {
        "title": "QCD 軸子(或類軸子粒子)是仍在實驗室積極搜尋的可行暗物質候選",
        "reasons": {
            "rapidly_growing_literature":
                "隨著 WIMP 空間收窄,軸子/ALP 的諧振腔、日冕儀與理論論文快速擴張。",
            "no_consensus_formed_yet":
                "軸子是領先的*候選類別*,不是已確立的暗物質鑑定。",
            "insufficient_observation":
                "尚無確認的軸子暗物質訊號;搜尋給出上限,多數質量量級仍未掃完。",
        },
        "evidence": [
            "後 WIMP 綜述把 QCD 軸子與類軸子粒子列為最佳動機的非 WIMP 候選之一:"
            "它們可在早期宇宙非熱產生,並在開放參數窗口對上觀測到的暗物質密度。",
            "ADMX 腔體實驗報告在磁場中把暈軸子轉成光子的共振搜尋,在高置信度下"
            "排除一段微電子伏特質量帶的 DFSZ 模型軸子 —— 零結果,但仍顯示實驗室"
            "已觸及宇宙學相關的軸子參數空間。",
        ],
        "open_questions": [
            "宇宙學軸子是否落在當前或近期 haloscope 能覆蓋的質量帶?",
            "沒有 QCD 連結的 ALP 模型如何改變實驗優先序?",
            "軸子是否可能只是暗物質的一部分,與其他成分並存?",
        ],
    },
    "sidm_small_scales": {
        "title": "速度相依的自作用暗物質可在不破壞大尺度成功的情況下調和小尺度結構",
        "reasons": {
            "rapidly_growing_literature":
                "SIDM 模擬、媒介子模型與星系團約束論文形成快速擴張的子領域。",
            "no_consensus_formed_yet":
                "SIDM 是嚴肅研究綱領,不是預設宇宙學模型;無碰撞 CDM 加重子仍是主流。",
            "insufficient_sample":
                "跨大樣本、同質星系的內層密度剖面乾淨測量仍然有限。",
        },
        "evidence": [
            "暗物質自作用綜述顯示:矮星系速度下約 ~1 cm^2/g 量級的截面可使內暈熱化並形成核,"
            "而星系團速度下小得多的有效截面仍可與合併星系團約束相容。",
            "小尺度 CDM 挑戰文獻把 SIDM 視為「純無碰撞 CDM 加重子」之外的主要粒子物理替代之一"
            "—— 仍依賴模型,且未被現有資料唯一選定。",
        ],
        "open_questions": [
            "矮星系、LSB 與星系團同時要求什麼樣的速度相依性?",
            "具體微觀模型(輕媒介子、暗原子)能否同時滿足直接偵測與宇宙學界限?",
            "在現代流體動力模擬中,SIDM 如何與重子回饋交互?",
        ],
    },
    "fermi_gc_excess_origin": {
        "title": "Fermi 銀心伽馬射線過剩是暗物質湮滅,還是未解析的天體物理源",
        "reasons": {
            "two_or_more_mainstream_models":
                "暗物質湮滅與未解析天體物理源,都是對同一 Fermi 過剩活躍發表的解釋。",
            "no_decisive_evidence_yet":
                "沒有共識分析排除任一派;銀心系統誤差仍然很大。",
            "genuine_scientific_camps":
                "對立論文與綜述記錄了間接偵測社群多年的分裂 —— 非 AI 宣稱的兩派。",
        },
        "evidence": [
            "對 Fermi-LAT 資料的分析在銀心方向找到大致球對稱的 GeV 伽馬射線過剩,"
            "其光譜與型態曾被論證符合數十 GeV 熱 WIMP 的湮滅。",
            "後續工作顯示,偏好暗弱毫秒脈衝星族群的非泊松模板擬合可能有病態,"
            "使暗物質與未解析源兩種詮釋之間的張力重新打開,而非為任一方結案。",
        ],
        "competing": [
            {"name": "暗物質湮滅",
             "for": "光譜與近似球對稱可匹配 ~數十 GeV WIMP 湮滅到標準模型粒子;"
                    "某些分析中訊號延伸超出最亮的恆星結構。",
             "against": "所需截面與剖面假設依賴模型;其他靶標尚未給出相互印證的發現。",
             "limits": "銀河瀰漫發射系統誤差主導不確定度預算。"},
            {"name": "未解析天體物理源(如毫秒脈衝星)",
             "for": "暗弱毫秒脈衝星或其他恆星殘骸族群能以較少新物理假設產生 GeV 過剩。",
             "against": "「光子統計唯一偏好點源族群」的宣稱受到挑戰;所需族群尚未被穩固觀測。",
             "limits": "內銀河的源計數與光度函數約束仍不完整。"},
        ],
        "open_questions": [
            "未來伽馬射線、電波或恆星殘骸巡天能否打破簡併?",
            "在最保守的銀河瀰漫模型下,過剩是否仍然存在?",
            "若是暗物質,為何矮球狀星系搜尋未見清楚對應?",
        ],
    },
    "monojet_collider_searches": {
        "title": "LHC 的 mono-jet 與大橫向缺失動量搜尋約束暗物質產生,但尚未鑑定出粒子",
        "reasons": {
            "rapidly_growing_literature":
                "ATLAS/CMS mono-X 分析、簡化模型 recast 與 HL-LHC 預估形成持續更新的龐大文獻。",
            "no_consensus_formed_yet":
                "對撞機約束產生率;尚未鑑定暗物質,且模型依賴使無法給出單一結案。",
            "insufficient_observation":
                "mono-jet 及相關 MET 通道尚無被確立為暗物質的過剩;只有上限。",
        },
        "evidence": [
            "LHC 暗物質工作小組定義了簡化模型與報告標準,使 mono-jet、mono-photon 等"
            "缺失能量搜尋能與直接偵測在共同的媒介子–DM 參數空間比較 ——"
            "讓對撞機成為與地下探測器並列的實驗室通道。",
            "ATLAS 以 139 fb^-1 的 13 TeV 質子–質子碰撞搜尋高能噴注加大橫向缺失動量事件,"
            "未見相對標準模型背景的顯著過剩,並對不可見粒子產生給出上限。",
            "CMS 在完整 Run-2 資料集做了平行的噴注加缺失動量搜尋,同樣未觀測到暗物質訊號,"
            "並排除大片簡化模型媒介子與 DM 質量空間。",
        ],
        "open_questions": [
            "把 LHC mono-X 上限與直接、間接偵測合併後,哪些媒介子與耦合結構仍開放?",
            "HL-LHC 或未來強子對撞機能否觸及當前 mono-jet 搜尋漏掉的熱遺蹟 WIMP 基準點?",
            "壓縮譜與長壽命暗部門態,如何在經典 mono-jet 選取之外被覆蓋?",
        ],
    },
    "cluster_sidm_cross_section_bounds": {
        "title": "合併星系團約束暗物質自作用截面單位質量",
        "reasons": {
            "rapidly_growing_literature":
                "星系團合併約束、流體+N-body SIDM 模擬與集成透鏡論文持續精煉 σ/m 上限。",
            "no_consensus_formed_yet":
                "大體同意過大的常數 σ/m 受約束,但不是所有速度下單一已定數字。",
            "insufficient_sample":
                "乾淨、建模良好的主合併仍然很少;集成分析仍在成長。",
        },
        "evidence": [
            "對碰撞星系團集成的分析,以恆星、氣體與透鏡質量的空間錯位約束暗物質自作用"
            "截面單位質量,在給定不確定度內與無碰撞行為一致。",
            "子彈星系團建模從暗物質成分相對碰撞氣體的存活與缺乏拖曳給出 σ/m 上限 ——"
            "這是 SIDM 現象學常用的經典觀測界限。",
        ],
        "open_questions": [
            "合併幾何、投影與重子物理系統誤差會使已發表的 σ/m 界限放鬆多少?",
            "星系團界限與矮星系尺度 SIDM 核能否由同一速度相依截面同時滿足?",
            "下一代透鏡巡天能否提供更大、更乾淨的合併星系團樣本?",
        ],
    },
    "neutrino_floor_direct_detection": {
        "title": "相干微中子–核散射為 WIMP 直接偵測設定不可約本底地板",
        "reasons": {
            "rapidly_growing_literature":
                "微中子地板/霧計算與下一代探測器設計論文形成成長中的子文獻。",
            "no_consensus_formed_yet":
                "存在微中子本底極限的大綱被接受;接近它時的精確發現能力仍有辯論。",
            "insufficient_observation":
                "實驗正在接近、但尚未完整映射深處於微中子主導區的運作。",
        },
        "evidence": [
            "太陽、大氣與瀰漫超新星微中子在核上的相干散射計算顯示,此本底可模仿 WIMP 反衝,"
            "並定義「微中子地板」(或霧);超越之後的發現宣稱需要定向或光譜判別。",
            "直接偵測綜述把多噸氙/氬路線圖視為逼近此微中子受限區間,"
            "並討論在其附近或之下運作所需的技術。",
        ],
        "open_questions": [
            "地板是否更宜描述為仍可藉統計與定向性保有發現潛力的軟「霧」?",
            "哪些靶核與能量窗口會最先撞上太陽微中子成分?",
            "當曝光進入微中子主導區時,給上限的實驗應如何報告靈敏度?",
        ],
    },
    "thermal_wimp_freezeout_benchmark": {
        "title": "具弱尺度質量與耦合的熱凍結 WIMP,儘管搜尋零結果,仍是暗物質基準靶標",
        "reasons": {
            "rapidly_growing_literature":
                "WIMP 簡化模型、全域擬合與「WIMP 式微」綜述仍構成龐大活躍文獻。",
            "no_consensus_formed_yet":
                "社群同意最簡單 WIMP 受壓,但不同意熱凍結作為框架已死。",
            "insufficient_observation":
                "尚無確認的 WIMP 偵測;基準是理論加上排除圖,不是正向粒子鑑定。",
        },
        "evidence": [
            "一篇 WIMP 典範的重要綜述說明弱尺度熱凍結如何自然給出觀測遺蹟密度"
            "(「WIMP 奇蹟」),並繪出 LHC 與直接偵測零結果如何侵蝕最簡單參數空間的大片區域。",
            "後 WIMP 景觀綜述仍把熱 WIMP 當作比較實驗室、對撞機與天文搜尋的中心組織基準,"
            "即使注意力已擴及軸子與暗部門。",
            "世界領先的氙直接偵測上限(LZ)在弱尺度附近排除大片經典自旋無關 WIMP–核子截面,"
            "且未發現訊號。",
        ],
        "open_questions": [
            "壓縮、共湮滅或隔離 WIMP 模型是否仍提供能避開當前 mono-jet 與氙界限的熱靶標?",
            "領域在哪一點應把熱 WIMP 從預設基準降為歷史特例?",
            "合併對撞機與直接偵測似然時,遺蹟密度先驗應如何報告?",
        ],
    },
    "direct_detection_wimp_searches": {
        "title": "地下直接偵測實驗對 WIMP–核子散射給出領先上限,但尚無確認發現",
        "reasons": {
            "rapidly_growing_literature":
                "連續數代氙/氬實驗與定向/低閾值 R&D 持續產出上限與方法論文。",
            "no_consensus_formed_yet":
                "對如何給上限有共識,對發現沒有;調制爭議仍在主流零結果之外。",
            "insufficient_observation":
                "尚無地下實驗給出被廣泛接受的確認 WIMP 偵測。",
        },
        "evidence": [
            "直接偵測領域綜述總結雙相氙、低溫等技術如何搜尋銀暈 WIMP 的核反衝,"
            "並強調本底控制與微中子地板作為下一靈敏度屏障。",
            "XENON1T 以噸級液氙靶報告自旋無關 WIMP–核子散射搜尋,未見顯著過剩,"
            "並給出當時世界領先上限。",
            "LUX-ZEPLIN 隨後以更大曝光改進這些上限,在經典低能核反衝興趣區同樣未見 WIMP 訊號。",
        ],
        "open_questions": [
            "多噸氙/氬實驗會在出現 WIMP 訊號前撞上微中子霧嗎?",
            "歷史上有爭議的年調制宣稱,應如何對照零計數率實驗來權衡?",
            "哪些低質量與自旋相依通道相對對撞機 mono-jet 界限仍最鬆?",
        ],
    },
    "dwarf_spheroidal_indirect_limits": {
        "title": "Fermi-LAT 對矮球狀星系的觀測對暗物質湮滅給出強上限,但尚無確認訊號",
        "reasons": {
            "rapidly_growing_literature":
                "每個 Fermi 目錄與每顆新發現的超暗弱矮星系都會催生更新的聯合分析與獨立再分析。",
            "no_consensus_formed_yet":
                "上限被廣泛使用;尚未確立正向的矮星系湮滅偵測。",
            "insufficient_observation":
                "dSph 中尚無確認的 DM 湮滅訊號;只有約束。",
        },
        "evidence": [
            "Fermi-LAT 對多個銀河矮球狀星系的聯合似然分析未發現可歸因於暗物質湮滅的顯著"
            "伽馬射線過剩,並在數十 GeV 質量處給出與熱遺蹟截面相交的上限。",
            "更新的 Fermi-LAT 矮球狀搜尋納入更多靶標與精煉 J 因子,再次未報告全域顯著湮滅訊號,"
            "強化矮星系作為乾淨、但流量有限的間接偵測通道。",
        ],
        "open_questions": [
            "J 因子系統誤差與新發現的超暗弱天體如何移動聯合上限?",
            "矮星系能否在同一粒子模型下排除或支持銀心過剩的暗物質起源?",
            "CTA 與廣域巡天的哪種協同最能改進目前 Fermi 界限以下的靈敏度?",
        ],
    },
    "s8_structure_tension_dark_sector": {
        "title": "S8 結構成長張力由新暗部門物理解決,還是由 ΛCDM 內的巡天系統誤差解決",
        "reasons": {
            "two_or_more_mainstream_models":
                "暗部門擴展與對 ΛCDM 的系統/統計再詮釋,都是對 S8 活躍發表的回應。",
            "no_decisive_evidence_yet":
                "張力顯著度依賴資料組合;尚無決定性裁定。",
            "genuine_scientific_camps":
                "宇宙學綜述與巡天論文記錄了多年辯論 —— 非 AI 發明的分裂。",
        },
        "evidence": [
            "宇宙學張力綜述記錄:主 CMB 推論與若干弱透鏡/星系成團巡天之間,"
            "在成團振幅 S8 上存在持續的輕度至中度不一致。",
            "Dark Energy Survey Year 3 的 3×2pt 分析在平坦 ΛCDM 下偏好低於 Planck 主 CMB 的 S8,"
            "常被引用為結構成長張力的觀測核心。",
            "Planck 2018 基線參數在 ΛCDM 外推下固定較高的晚期成團振幅,定義了比較的 CMB 一側。",
        ],
        "competing": [
            {"name": "新暗部門/晚期物理",
             "for": "衰變、相互作用或壓制成長的暗物質情境,在某些擬合中可相對主 CMB 降低 S8,"
                    "而不放棄早期宇宙成功。",
             "against": "許多擴展在別處再引入張力(CMB 透鏡、星系團計數、BAO)或需要微調耦合。",
             "limits": "模型空間很大;沒有單一暗部門修正被唯一選定。"},
            {"name": "系統誤差與 ΛCDM 一致性",
             "for": "剪切校正、photo-z、內稟對齊與尺度切割可移動弱透鏡 S8;"
                    "某些分析在替代管線下張力較弱。",
             "against": "多個獨立透鏡團隊報告低 S8,較難歸咎於單一實驗缺陷。",
             "limits": "跨巡天對殘餘系統誤差的端到端共識仍在形成。"},
        ],
        "open_questions": [
            "Euclid、LSST/Rubin 與 Roman 會減弱還是加深 S8 偏移?",
            "哪些暗部門模型能在聯合 CMB + full-shape + 透鏡似然下存活?",
            "S8 與小尺度 CDM 挑戰是同一物理張力,還是正交的?",
        ],
    },
    "fuzzy_wave_dark_matter": {
        "title": "具 de Broglie 尺度波動效應的超輕標量「Fuzzy」暗物質,是小尺度上冷粒子 CDM 的可行替代",
        "reasons": {
            "rapidly_growing_literature":
                "自 2010 年代起,wave-DM 模擬、Lyman-α 再分析與實驗室/軸子連結形成快速增長的文獻。",
            "no_consensus_formed_yet":
                "Fuzzy DM 是小尺度上的嚴肅替代,不是預設宇宙學模型;無碰撞 CDM 仍是主流。",
            "insufficient_observation":
                "尚無超輕 DM 粒子的正向鑑定;約束重塑質量窗口,但未確認它。",
        },
        "evidence": [
            "Fuzzy 冷暗物質提出一種超輕玻色子,其 de Broglie 波長在星系暈中可達千秒差距尺度,"
            "抑制小尺度功率並形成孤子核,而不必單靠重子回饋。",
            "一篇超輕標量宇宙學暗物質綜述梳理了產生機制、Schrödinger–Poisson 暈結構與觀測靶標 ——"
            "把 fuzzy/wave DM 立為有結構的研究綱領,而非單一玩具模型。",
            "Lyman-α 森林流量功率測量被用來從下方約束超輕玻色子質量:過輕的 fuzzy DM"
            "相對觀測森林過度壓制小尺度結構,擠壓開放質量窗口。",
        ],
        "open_questions": [
            "在聯合 Lyman-α、矮星系與黑洞超輻射約束後,還剩什麼質量窗口?",
            "孤子核與干涉顆粒是否比 CDM+重子或 SIDM 更符合矮星系與超暗弱星系的多樣性?",
            "QCD 軸子是否落在 fuzzy 區間、是另一種 ALP,還是在回饋完全建模後兩者皆非必要?",
        ],
    },
    "sterile_neutrino_7kev_line": {
        "title": "約 7 keV 的惰性微中子是暗物質,並產生 3.5 keV X 射線發射線",
        "reasons": {
            "not_accepted_by_mainstream":
                "把 3.5 keV 線解讀為 7 keV 惰性微中子並非已確立共識;多項分析質疑該線的存在或暗物質起源。",
            "philosophical_inference":
                "這不是純哲學宣稱,而是經驗性的 X 射線爭議 —— 此條件不承載燈號。",
        },
        "evidence": [
            "星系與星系團的堆疊及個別 X 射線光譜曾被報告在約 3.5 keV 出現未識別發射特徵,"
            "部分作者將其解讀為約 7 keV 惰性微中子暗物質候選的衰變線。",
            "一項獨立 blank-sky 分析主張:若 3.5 keV 特徵來自暗物質,則在應仍可見銀暈"
            "惰性微中子訊號的深空場中未見到該線,與暗物質起源不一致 ——"
            "直接挑戰惰性微中子暗物質宣稱。",
        ],
        "open_questions": [
            "3.5 keV 特徵是天體物理(如電荷交換、鉀線)、儀器效應,還是統計假象?",
            "XRISM 等其他高解析 X 射線任務能否裁定該線的存在與起源?",
            "若惰性微中子是暗物質,在現有 X 射線界限下是否只能佔預算的一部分?",
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
