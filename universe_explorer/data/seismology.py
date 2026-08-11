"""Seismology — the fourth domain (topic picked by Claude, 2026-07-10).

Why this domain: nowhere is the gap between what the public wants to know
("when is the earthquake?") and what science honestly knows wider — and more
consequential. The knowledge shape here is the whole point of the system:
plate tectonics is bedrock; early warning genuinely buys seconds; how faults
repeat is a real two-camp dispute; operational forecasting is a frontier; and
electric-signal prediction is not accepted. People die over earthquake rumors;
a page that honestly separates these layers earns its keep.

Engineering note: this is the first domain whose provenance runs primarily
through the Crossref (Amendment #6) pipeline — none of these sources live on
arXiv. Every source was verified online (journal, volume, DOI) before writing.

Expected lights:
  plate_tectonics_drives_earthquakes -> 🟢 Established (E1)
  eew_gives_usable_warning           -> 🔵 Strong (E3 -> ⚡ axes diverge)
  characteristic_earthquake_model    -> 🟡 Competing
  oef_informs_civil_protection      -> 🟠 Frontier
  van_electric_precursors            -> 🔴 Speculative
"""

from __future__ import annotations

from ..model import (
    Claim,
    CompetingModel,
    ConditionAssessment,
    Evidence,
    Source,
    Status,
    Topic,
)

# --------------------------------------------------------------------------- #
# Claim 1 — plate tectonics drives earthquakes            🟢 Established       #
# --------------------------------------------------------------------------- #
plate_tectonics_drives_earthquakes = Claim(
    id="plate_tectonics_drives_earthquakes",
    trace_refs=['VineMatthews1963', 'DeMets2010'],
    title="Moving tectonic plates cause the world's earthquakes",
    status=Status.ESTABLISHED,
    sources=[
        Source(
            label="VineMatthews1963",
            url_or_id="doi:10.1038/199947a0",
            kind="peer-reviewed paper (Nature 199, 947-949, 1963)",
        ),
        Source(
            label="DeMets2010",
            url_or_id="doi:10.1111/j.1365-246X.2009.04491.x",
            kind="peer-reviewed paper (Geophys. J. Int. 181, 1-80, 2010)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Measured magnetic stripes on the seafloor, symmetric about "
                "mid-ocean ridges and matching geomagnetic reversals, recorded "
                "new crust forming as plates spread apart."
            ),
            source_ref="VineMatthews1963",
        ),
        Evidence(
            type="direct observation",
            description=(
                "The MORVEL synthesis measures the current motions of 25 "
                "plates covering nearly the whole Earth surface from spreading "
                "rates, fault azimuths and GPS velocities — earthquake belts "
                "trace the measured plate boundaries."
            ),
            source_ref="DeMets2010",
        ),
    ],
    open_questions=[
        "How strain partitions across diffuse plate-boundary zones and "
        "continental interiors is still being mapped.",
        "What controls the depth limits of seismic rupture on individual "
        "faults remains an active question.",
    ],
    status_reason=[
        ConditionAssessment(
            "multiple_independent_replications", True,
            "Seafloor magnetics, global seismicity, paleomagnetism and modern "
            "space geodesy independently measure the same plate motions.",
        ),
        ConditionAssessment(
            "accepted_in_mainstream_textbooks", True,
            "Plate tectonics is the organizing framework of every modern "
            "earth-science textbook.",
        ),
        ConditionAssessment(
            "no_mainstream_competing_theory", True,
            "No mainstream alternative explains the joint pattern of "
            "seismicity, magnetics and geodesy.",
        ),
        ConditionAssessment(
            "no_recent_major_refutation", True,
            "Six decades of ever-denser measurement have only sharpened the "
            "picture.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 2 — early warning buys seconds                    🔵 Strong            #
# --------------------------------------------------------------------------- #
eew_gives_usable_warning = Claim(
    id="eew_gives_usable_warning",
    trace_refs=['AllenMelgar2019'],
    title="Earthquake early warning systems provide seconds to tens of "
          "seconds of usable warning",
    status=Status.STRONG,
    sources=[
        Source(
            label="AllenMelgar2019",
            url_or_id="doi:10.1146/annurev-earth-053018-060457",
            kind="peer-reviewed paper (Annu. Rev. Earth Planet. Sci. 47, "
                 "361-388, 2019)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "A synthesis of deployed systems (Japan, Mexico, the US West "
                "Coast and others) documents that detecting P-waves near the "
                "source yields seconds to tens of seconds of warning before "
                "strong shaking arrives at more distant sites."
            ),
            source_ref="AllenMelgar2019",
        ),
    ],
    open_questions=[
        "Alert accuracy for the very largest ruptures, whose magnitude grows "
        "while the alert is already out, is still improving.",
        "The blind zone near the epicenter — where shaking arrives before "
        "any alert — is physically irreducible; how to communicate this is "
        "an open design problem.",
        "How much protective action alerts actually trigger in practice is "
        "under active study.",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Early warning is deployed at national scale in several countries "
            "and endorsed by their seismological agencies.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Real debates persist about magnitude saturation, alert "
            "thresholds and cost-benefit — details, not the capability.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Every deployed system and simulation study points the same way: "
            "the physics of P-versus-S wave speed reliably buys time. The "
            "indirect (synthesis) character of the recorded evidence is "
            "expressed structurally on the evidence axis.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 3 — characteristic earthquakes                    🟡 Competing         #
# --------------------------------------------------------------------------- #
characteristic_earthquake_model = Claim(
    id="characteristic_earthquake_model",
    title="Individual faults repeat characteristic, quasi-periodic large "
          "earthquakes",
    status=Status.COMPETING,
    sources=[
        Source(
            label="SchwartzCoppersmith1984",
            url_or_id="doi:10.1029/JB089iB07p05681",
            kind="peer-reviewed paper (J. Geophys. Res. 89, 5681-5698, 1984)",
        ),
        Source(
            label="KaganJackson1991",
            url_or_id="doi:10.1029/91JB02210",
            kind="peer-reviewed paper (J. Geophys. Res. 96, 21419-21431, 1991)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Paleoseismic trenching on the Wasatch and San Andreas fault "
                "zones was read as showing individual fault segments tending "
                "to repeat essentially the same 'characteristic' earthquake."
            ),
            source_ref="SchwartzCoppersmith1984",
        ),
        Evidence(
            type="indirect observation",
            description=(
                "Statistical testing of the seismic-gap forecasts built on "
                "that picture found the observed earthquake record fit a "
                "clustered, non-quasi-periodic model better than the gap "
                "model's predictions."
            ),
            source_ref="KaganJackson1991",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Characteristic / seismic-gap model",
            supporting=(
                "Paleoseismic records on some faults show similar-size "
                "ruptures recurring; hazard maps long relied on segment-based "
                "recurrence."
            ),
            opposing=(
                "Formal statistical tests of gap-based forecasts against "
                "subsequent earthquakes performed poorly."
            ),
            limitations=(
                "Paleoseismic records are short and dating uncertainties are "
                "large, so 'quasi-periodic' is hard to establish per fault."
            ),
        ),
        CompetingModel(
            name="Clustered / statistical seismicity",
            supporting=(
                "Earthquake catalogs are well described by clustering "
                "statistics; several 'overdue' gaps stayed quiet while "
                "'recently ruptured' zones broke again."
            ),
            opposing=(
                "Purely statistical models struggle with faults where "
                "trenching does show repeated similar ruptures."
            ),
            limitations=(
                "Catalog spans are short relative to recurrence times, "
                "limiting the power of every statistical test."
            ),
        ),
    ],
    open_questions=[
        "Do longer paleoseismic and geodetic records converge on periodic, "
        "clustered, or mixed recurrence?",
        "Can physics-based rupture simulators discriminate between the two "
        "pictures where data cannot yet?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Characteristic/segment-based recurrence and clustered "
            "statistical seismicity are both live, published frameworks that "
            "hazard models still draw on.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "Records are short relative to recurrence intervals, so neither "
            "side commands a decisive test.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "A decades-long, published dispute (comment-and-reply exchanges "
            "included) between paleoseismology-oriented and statistics-"
            "oriented groups — not a split asserted by the AI.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 4 — operational earthquake forecasting            🟠 Frontier          #
# --------------------------------------------------------------------------- #
oef_informs_civil_protection = Claim(
    id="oef_informs_civil_protection",
    title="Operational earthquake forecasting can usefully inform civil "
          "protection",
    status=Status.FRONTIER,
    sources=[
        Source(
            label="Jordan2011",
            url_or_id="doi:10.4401/ag-5350",
            kind="peer-reviewed paper (Annals of Geophysics 54, 315-391, "
                 "2011; ICEF report after L'Aquila)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "The post-L'Aquila international commission reviewed global "
                "forecasting experiments and concluded that probabilistic "
                "short-term forecasts carry real, if low-probability, skill — "
                "and issued the first guidelines for using them operationally."
            ),
            source_ref="Jordan2011",
        ),
    ],
    open_questions=[
        "How should authorities act on forecasts whose absolute "
        "probabilities remain small even when elevated many-fold?",
        "Do aftershock-statistics models capture the situations that matter "
        "most, or only the easy ones?",
        "How is forecast skill best communicated without triggering the "
        "very rumors it should displace?",
    ],
    status_reason=[
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Which models to operationalize, and how authorities should "
            "respond, remains unsettled across agencies.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Forecast experiments (CSEP and successors) and national OEF "
            "systems are producing a fast-growing evaluation literature.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 5 — VAN electric precursors                       🔴 Speculative       #
# --------------------------------------------------------------------------- #
van_electric_precursors = Claim(
    id="van_electric_precursors",
    title="Seismic electric signals (the VAN method) predict imminent "
          "earthquakes",
    status=Status.SPECULATIVE,
    sources=[
        Source(
            label="Varotsos1984",
            url_or_id="doi:10.1016/0040-1951(84)90059-3",
            kind="peer-reviewed paper (Tectonophysics 110, 73-98, 1984)",
        ),
        Source(
            label="Geller1997",
            url_or_id="doi:10.1126/science.275.5306.1616",
            kind="peer-reviewed critique (Science 275, 1616-1617, 1997)",
        ),
    ],
    evidence=[
        Evidence(
            type="indirect observation",
            description=(
                "Telluric electric-field stations in Greece were reported to "
                "record 'seismic electric signals' preceding earthquakes, "
                "with claimed successful predictions of epicenter and "
                "magnitude."
            ),
            source_ref="Varotsos1984",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "A prominent mainstream rebuttal argued that earthquakes are "
                "inherently unpredictable — small ruptures cascade into large "
                "ones depending on unmeasurably fine conditions — and that "
                "claimed precursor successes, VAN included, do not survive "
                "statistical scrutiny."
            ),
            source_ref="Geller1997",
        ),
    ],
    open_questions=[
        "Is there any physical mechanism by which pre-rupture stress could "
        "generate detectable electric signals at the claimed distances?",
        "Can any precursor claim be validated under prospective, "
        "pre-registered testing rather than retrospective selection?",
    ],
    status_reason=[
        ConditionAssessment(
            "not_accepted_by_mainstream", True,
            "Despite decades of publications, the mainstream assessment is "
            "that VAN's claimed successes do not survive statistical "
            "scrutiny; no seismological agency uses electric signals for "
            "prediction.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 6 — induced seismicity                           🔵 Strong             #
# --------------------------------------------------------------------------- #
induced_seismicity_human_activities = Claim(
    id="induced_seismicity_human_activities",
    trace_refs=['Ellsworth2013', 'Keranen2014'],
    title=(
        "Human activities (especially fluid injection) can induce earthquakes"
    ),
    status=Status.STRONG,
    sources=[
        Source(
            label="Ellsworth2013",
            url_or_id="doi:10.1126/science.1225942",
            kind="peer-reviewed paper (Science 341, 1225942, 2013; injection-"
                 "induced earthquakes)",
        ),
        Source(
            label="Keranen2014",
            url_or_id="doi:10.1126/science.1255802",
            kind="peer-reviewed paper (Science 345, 448, 2014; Oklahoma "
                 "wastewater injection)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Spatial and temporal correlations between high-rate wastewater "
                "injection and earthquake rate increases establish a causal "
                "link in well-studied regions."
            ),
            source_ref="Ellsworth2013",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Detailed studies in the central United States link specific "
                "injection wells and volumes to elevated seismicity, including "
                "damaging events."
            ),
            source_ref="Keranen2014",
        ),
    ],
    open_questions=[
        "What pore-pressure thresholds best predict induced sequences?",
        "How should regulation balance energy operations with seismic risk?",
    ],
    status_reason=[
        ConditionAssessment(
            "mainstream_model_support", True,
            "Induced seismicity from fluid injection is standard applied "
            "seismology.",
        ),
        ConditionAssessment(
            "minor_alternatives_exist", True,
            "Some events remain ambiguous between induced and natural; the "
            "class of injection-induced quakes is not in doubt.",
        ),
        ConditionAssessment(
            "overall_direction_robust", True,
            "Additional basins and mechanisms (geothermal, fracking, reservoir "
            "impoundment) keep confirming the phenomenon.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 7 — short-term prediction vs forecasting         🟡 Competing          #
# --------------------------------------------------------------------------- #
short_term_deterministic_prediction = Claim(
    id="short_term_deterministic_prediction",
    title=(
        "Deterministic short-term earthquake prediction is achievable with "
        "current science versus fundamentally limited to probabilistic "
        "forecasting"
    ),
    status=Status.COMPETING,
    sources=[
        Source(
            label="Geller1997",
            url_or_id="doi:10.1126/science.275.5306.1616",
            kind="peer-reviewed paper (Science 275, 1616, 1997; earthquakes "
                 "cannot be predicted)",
        ),
        Source(
            label="Jordan2011",
            url_or_id="doi:10.4401/ag-5350",
            kind="peer-reviewed paper (Ann. Geophys.; operational earthquake "
                 "forecasting principles)",
        ),
    ],
    evidence=[
        Evidence(
            type="theoretical result",
            description=(
                "A long-standing mainstream assessment holds that reliable "
                "deterministic short-term prediction of large earthquakes is "
                "not supported by physics or statistics of fault systems."
            ),
            source_ref="Geller1997",
        ),
        Evidence(
            type="theoretical result",
            description=(
                "Operational earthquake forecasting frameworks instead offer "
                "time-dependent probabilities for civil protection, explicitly "
                "distinguished from deterministic prediction."
            ),
            source_ref="Jordan2011",
        ),
    ],
    competing_models=[
        CompetingModel(
            name="Prediction is not achievable (forecasting only)",
            supporting=(
                "Chaotic loading, limited precursor reproducibility and failed "
                "prospective tests support probabilistic forecasts only."
            ),
            opposing=(
                "Some researchers still pursue multi-parameter precursor "
                "systems aiming at short-term alerts."
            ),
            limitations=(
                "Public demand for 'when' messages pressures agencies beyond "
                "what physics delivers."
            ),
        ),
        CompetingModel(
            name="Useful short-term prediction may still emerge",
            supporting=(
                "Improved dense networks, AI pattern searches and multi-sensor "
                "precursors are argued to reopen the question."
            ),
            opposing=(
                "Prospective, pre-registered successes at operational skill "
                "remain lacking for large events."
            ),
            limitations=(
                "Retrospective selection and publication bias are chronic."
            ),
        ),
    ],
    open_questions=[
        "Can any precursor claim survive prospective, pre-registered tests?",
        "How should agencies communicate forecast probabilities without "
        "implying false prediction skill?",
    ],
    status_reason=[
        ConditionAssessment(
            "two_or_more_mainstream_models", True,
            "Forecasting-only orthodoxy and continued prediction-research "
            "programmes both appear in the peer-reviewed literature.",
        ),
        ConditionAssessment(
            "no_decisive_evidence_yet", True,
            "No consensus operational short-term predictor has been "
            "demonstrated.",
        ),
        ConditionAssessment(
            "genuine_scientific_camps", True,
            "The prediction vs forecasting split is a multi-decade debate, "
            "not a rhetorical invention.",
        ),
    ],
    status_history=[],
)

# --------------------------------------------------------------------------- #
# Claim 8 — slow slip / ETS                              🟠 Frontier           #
# --------------------------------------------------------------------------- #
slow_slip_and_ets_observed = Claim(
    id="slow_slip_and_ets_observed",
    title=(
        "Slow-slip events and episodic tremor and slip are observed on some "
        "subduction zones"
    ),
    status=Status.FRONTIER,
    sources=[
        Source(
            label="RogersDragert2003",
            url_or_id="doi:10.1126/science.1084783",
            kind="peer-reviewed paper (Science 300, 1942, 2003; episodic "
                 "tremor and slip)",
        ),
        Source(
            label="Obara2002",
            url_or_id="doi:10.1126/science.1070378",
            kind="peer-reviewed paper (Science 296, 1679, 2002; nonvolcanic "
                 "deep tremor)",
        ),
    ],
    evidence=[
        Evidence(
            type="direct observation",
            description=(
                "Geodetic and seismic records in Cascadia document repeating "
                "slow-slip episodes accompanied by tremor (ETS)."
            ),
            source_ref="RogersDragert2003",
        ),
        Evidence(
            type="direct observation",
            description=(
                "Deep nonvolcanic tremor discovered in southwest Japan opened "
                "the observational class of slow deformation phenomena."
            ),
            source_ref="Obara2002",
        ),
    ],
    open_questions=[
        "How do slow-slip cycles relate to the timing of great megathrust "
        "earthquakes?",
        "What physical conditions select slow vs fast rupture?",
    ],
    status_reason=[
        ConditionAssessment(
            "new_discovery", True,
            "Slow slip and ETS were established observationally this century.",
        ),
        ConditionAssessment(
            "rapidly_growing_literature", True,
            "Global catalogues of slow earthquakes continue to expand.",
        ),
        ConditionAssessment(
            "no_consensus_formed_yet", True,
            "Links to great-earthquake timing remain an open research "
            "programme.",
        ),
    ],
    status_history=[],
)


SEISMOLOGY = Topic(
    id="seismology",
    title="Earthquakes",
    summary=(
        "Earthquakes domain: 🟢 plates; 🔵 EEW + induced seismicity; 🟡 "
        "characteristic quakes + prediction-vs-forecast; 🟠 OEF + slow slip; "
        "🔴 VAN electric precursors (not accepted)."
    ),
    claims=[
        plate_tectonics_drives_earthquakes,
        eew_gives_usable_warning,
        induced_seismicity_human_activities,
        characteristic_earthquake_model,
        short_term_deterministic_prediction,
        oef_informs_civil_protection,
        slow_slip_and_ets_observed,
        van_electric_precursors,
    ],
)
