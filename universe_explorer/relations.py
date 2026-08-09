"""Claim-to-claim relations and mechanical inference.

Epistemic rules (hard):
  • Links are either *authored* (human note, discrete kind) or *mechanical*
    (shared sources, co-topic). AI does not invent edges.
  • No confidence / score / probability / trust fields anywhere.
  • Inference = transparent path listing over recorded edges — not a verdict.

Kinds (discrete taxonomy):
  supports     — A strengthens the reading of B
  requires     — A is an epistemic presupposition of B's framing
  specializes  — A is a pole / sub-claim under umbrella B
  tensions     — A and B sit in structured tension
  boundary     — cross-domain adjacency (honest map boundary)
  shares_source — mechanical: same arXiv id or DOI
  co_topic     — mechanical: same topic container (weak; listed separately)

CLI::

    python -m universe_explorer.relations --claim stars_powered_by_fusion
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .model import Claim, Topic

# Discrete kinds only — never a continuum.
LINK_KINDS = frozenset({
    "supports",
    "requires",
    "specializes",
    "tensions",
    "boundary",
    "shares_source",
    "co_topic",
})

# Human-facing labels (en / zh). Presentation only.
KIND_LABELS = {
    "supports": {"en": "supports", "zh": "支持閱讀"},
    "requires": {"en": "requires", "zh": "預設前提"},
    "specializes": {"en": "specializes", "zh": "具體化"},
    "tensions": {"en": "tensions with", "zh": "結構張力"},
    "boundary": {"en": "boundary with", "zh": "領域邊界"},
    "shares_source": {"en": "shares source", "zh": "共用出處"},
    "co_topic": {"en": "same domain", "zh": "同領域"},
}

# Reverse reading for inbound edges (display only).
KIND_INVERSE = {
    "supports": "supported_by",
    "requires": "required_by",
    "specializes": "generalizes",
    "tensions": "tensions",
    "boundary": "boundary",
    "shares_source": "shares_source",
    "co_topic": "co_topic",
}

KIND_INVERSE_LABELS = {
    "supported_by": {"en": "supported by", "zh": "被支持於"},
    "required_by": {"en": "presupposed by", "zh": "被作為前提"},
    "generalizes": {"en": "generalizes", "zh": "概括"},
    "tensions": KIND_LABELS["tensions"],
    "boundary": KIND_LABELS["boundary"],
    "shares_source": KIND_LABELS["shares_source"],
    "co_topic": KIND_LABELS["co_topic"],
}

BANNED_KEYS = frozenset({
    "confidence", "score", "probability", "certainty", "trust",
})


@dataclass(frozen=True)
class ClaimLink:
    """One directed edge. ``origin`` is authored | mechanical."""

    source: str
    target: str
    kind: str
    note: str
    origin: str = "authored"  # authored | mechanical

    def as_dict(self) -> dict:
        d = {
            "source": self.source,
            "target": self.target,
            "kind": self.kind,
            "note": self.note,
            "origin": self.origin,
        }
        assert self.kind in LINK_KINDS, self.kind
        assert self.origin in ("authored", "mechanical")
        assert not (set(d) & BANNED_KEYS)
        return d


# ---------------------------------------------------------------------------
# Authored graph (human). Grow carefully; never invent edges in code gen.
# Tuple: (source, target, kind, note)
# ---------------------------------------------------------------------------

_AUTHORED: Tuple[Tuple[str, str, str, str], ...] = (
    # --- cosmology H0 cluster ---
    ("universe_is_expanding", "shoes_local_H0_high", "requires",
     "Local H0 ladders presuppose cosmic expansion."),
    ("universe_is_expanding", "cmb_lcdm_implies_low_H0", "requires",
     "CMB+ΛCDM H0 is a late-time expansion rate in an expanding cosmos."),
    ("cmb_hot_big_bang", "cmb_lcdm_implies_low_H0", "requires",
     "Sound-horizon H0 inference sits on the hot-big-bang CMB framework."),
    ("H0_tension_local_vs_cmb", "shoes_local_H0_high", "specializes",
     "SH0ES high local pole under the tension umbrella."),
    ("H0_tension_local_vs_cmb", "cmb_lcdm_implies_low_H0", "specializes",
     "Planck ΛCDM low pole under the tension umbrella."),
    ("H0_tension_local_vs_cmb", "trgb_vs_cepheid_local_H0", "specializes",
     "Local calibrator split is a second yellow node under H0."),
    ("shoes_local_H0_high", "trgb_vs_cepheid_local_H0", "tensions",
     "Cepheid vs TRGB calibrators disagree inside the local universe."),
    ("shoes_local_H0_high", "cmb_lcdm_implies_low_H0", "tensions",
     "High local vs low early poles under standard assumptions."),
    ("early_dark_energy_H0_fix", "H0_tension_local_vs_cmb", "supports",
     "EDE is proposed as an early-universe relief for the tension."),
    ("strong_lensing_time_delay_H0", "H0_tension_local_vs_cmb", "supports",
     "Geometric H0 route that can arbitrate without the same ladder."),
    ("standard_sirens_H0", "H0_tension_local_vs_cmb", "supports",
     "GW sirens are a third-route H0 programme."),
    ("accelerated_expansion", "universe_is_expanding", "requires",
     "Late-time acceleration is a property of an expanding universe."),
    ("cosmic_inflation_early_universe", "cmb_hot_big_bang", "supports",
     "Inflation is framed as early physics feeding the hot big bang."),
    ("inflation_slow_roll_planck", "cosmic_inflation_early_universe", "specializes",
     "Planck slow-roll preference under the inflation umbrella."),
    ("primordial_tensors_undetected", "cosmic_inflation_early_universe", "specializes",
     "Tensor bounds constrain inflationary energy scale."),
    ("inflation_vs_noninflation_alts", "cosmic_inflation_early_universe", "tensions",
     "Bounce-class alternatives vs inflation as early framework."),
    ("eternal_inflation_multiverse", "cosmic_inflation_early_universe", "specializes",
     "Multiverse reading sits above plain inflation — Speculative ceiling."),
    ("cyclic_or_bounce_replaces_bb", "cmb_hot_big_bang", "tensions",
     "Replacement thesis vs hot-big-bang bedrock."),

    # --- dark matter spine ---
    ("mass_discrepancy_observed", "lcdm_includes_cold_dm", "supports",
     "Observed discrepancy motivates a cold dark component in ΛCDM."),
    ("lcdm_includes_cold_dm", "dm_particle_identity", "requires",
     "Particle-identity programmes assume a CDM-like component exists."),
    ("particle_vs_modified_gravity", "mass_discrepancy_observed", "requires",
     "Both camps accept a discrepancy; they split on the cause."),
    ("particle_vs_modified_gravity", "dm_particle_identity", "tensions",
     "Particle vs modified-gravity camps structure the identity debate."),
    ("thermal_wimp_freezeout_benchmark", "dm_particle_identity", "specializes",
     "WIMP freeze-out is one identity benchmark."),
    ("direct_detection_wimp_searches", "thermal_wimp_freezeout_benchmark", "supports",
     "Direct detection targets the WIMP window."),
    ("neutrino_floor_direct_detection", "direct_detection_wimp_searches", "supports",
     "Neutrino floor bounds how far WIMP searches can push."),
    ("axion_dm_candidate", "dm_particle_identity", "specializes",
     "Axions are an alternate identity programme."),
    ("fuzzy_wave_dark_matter", "small_scale_cdm_challenges", "supports",
     "Ultralight wave DM is proposed partly for small-scale issues."),
    ("sidm_small_scales", "small_scale_cdm_challenges", "supports",
     "Self-interacting DM targets small-scale CDM tensions."),
    ("fermi_gc_excess_origin", "dm_particle_identity", "tensions",
     "GC excess may be DM or stellar remnants — not settled identity."),
    ("sterile_neutrino_7kev_line", "dm_particle_identity", "specializes",
     "7 keV sterile-neutrino line is a contested identity claim."),
    ("pbh_all_dark_matter", "dm_particle_identity", "tensions",
     "PBH-as-all-DM competes with particle identity programmes."),
    ("H0_tension_local_vs_cmb", "s8_structure_tension_dark_sector", "boundary",
     "H0 and S8 tensions are distinct; both can involve dark-sector extensions."),

    # --- black holes ---
    ("event_horizon_exists", "kerr_describes_astrophysical_bh", "supports",
     "Horizon-scale objects are modelled as Kerr in the working spacetime."),
    ("event_horizon_exists", "hawking_radiation", "requires",
     "Hawking radiation is defined for black-hole horizons."),
    ("kerr_describes_astrophysical_bh", "jets_extract_bh_spin", "requires",
     "Blandford–Znajek-type extraction assumes a spinning Kerr hole."),
    ("event_horizon_exists", "smbh_common_in_galaxy_nuclei", "supports",
     "Nuclear SMBHs are the population reading of horizon-class objects."),
    ("bbh_mergers_catalogued", "kerr_describes_astrophysical_bh", "supports",
     "Catalogue ringdowns test Kerr remnants at population scale."),
    ("bbh_mergers_catalogued", "lower_mass_gap_compact_objects", "supports",
     "GW mass spectra feed the lower-mass-gap debate."),
    ("information_paradox", "hawking_radiation", "requires",
     "The paradox is about information in evaporating (Hawking) holes."),
    ("firewall", "information_paradox", "specializes",
     "Firewall is one proposed price of unitary evaporation."),
    ("horizonless_gw_echoes", "event_horizon_exists", "tensions",
     "Echo claims probe horizonless alternatives to the horizon bedrock."),
    ("horizonless_gw_echoes", "kerr_describes_astrophysical_bh", "tensions",
     "Reflective ECO models deviate from pure Kerr horizons."),

    # --- stars ---
    ("stars_powered_by_fusion", "helioseismology_constrains_solar_interior",
     "supports",
     "Fusion-powered structure is what helioseismology maps in bulk."),
    ("stars_powered_by_fusion", "cno_cycle_solar_neutrinos_detected",
     "requires",
     "CNO neutrinos are a fusion-cycle channel in the solar core."),
    ("stars_powered_by_fusion", "stellar_nucleosynthesis_makes_elements",
     "supports",
     "Nucleosynthesis pathways sit on stellar energy generation."),
    ("stellar_nucleosynthesis_makes_elements", "core_collapse_forms_ns_bh",
     "supports",
     "Explosive sites include core-collapse endpoints."),
    ("core_collapse_forms_ns_bh", "red_supergiant_problem", "requires",
     "The RSG problem is about which massive stars explode to remnants."),
    ("core_collapse_forms_ns_bh", "pair_instability_bh_mass_gap", "supports",
     "PISN gap is a prediction about which remnants form at high mass."),
    ("white_dwarfs_electron_degenerate", "sn_ia_progenitor_channels",
     "requires",
     "Type Ia channels are channels for exploding white dwarfs."),
    ("imf_approximately_universal", "core_collapse_forms_ns_bh", "supports",
     "The high-mass IMF sets the rate of core-collapse endpoints."),
    ("solar_dynamo_cycle", "helioseismology_constrains_solar_interior",
     "supports",
     "Dynamo models are constrained by seismic interior structure."),
    ("pop_iii_already_routinely_observed", "stellar_nucleosynthesis_makes_elements",
     "tensions",
     "Local Pop III would rewrite how early metals seed — not accepted."),

    # --- stars ↔ black_hole / cosmology boundaries ---
    ("core_collapse_forms_ns_bh", "event_horizon_exists", "boundary",
     "Stellar death produces some of the objects the BH domain images."),
    ("pair_instability_bh_mass_gap", "lower_mass_gap_compact_objects",
     "boundary",
     "Upper (PISN) vs lower (NS–BH) mass gaps are distinct yellow/orange nodes."),
    ("pair_instability_bh_mass_gap", "bbh_mergers_catalogued", "supports",
     "GW mass spectra are the empirical arena for the PISN gap."),
    ("sn_ia_progenitor_channels", "shoes_local_H0_high", "boundary",
     "Cosmology uses Ia ladders; stellar domain owns progenitor engineering."),

    # --- planets / exoplanets / ocean ---
    ("solar_system_age", "moon_giant_impact", "supports",
     "Chronology frames when the giant impact could occur."),
    ("ocean_worlds_icy_moons", "europa_induced_field_ocean", "specializes",
     "Europa is a pole under the icy-moon ocean umbrella."),
    ("ocean_worlds_icy_moons", "enceladus_plume_global_ocean", "specializes",
     "Enceladus plume + libration under the ocean-worlds umbrella."),
    ("ocean_worlds_icy_moons", "titan_subsurface_ocean", "specializes",
     "Titan subsurface ocean under the umbrella."),
    ("enceladus_plume_organics", "enceladus_plume_global_ocean", "supports",
     "Organics are measured in the plume of an ocean-bearing moon."),
    ("ocean_world_life_today", "ocean_worlds_icy_moons", "requires",
     "Life-today claims presuppose oceans exist."),
    ("ocean_world_life_today", "enceladus_plume_organics", "supports",
     "Organics are necessary but not sufficient for life claims."),
    ("exoplanets_exist", "planets_are_common", "supports",
     "Existence is the floor under demographic commonality."),
    ("exoplanets_exist", "proxima_b_exists", "supports",
     "Proxima b is a specific existence claim under the class."),
    ("planets_are_common", "radius_valley_mechanism", "supports",
     "The valley is a feature of a large exoplanet population."),
    ("radius_valley_mechanism", "trappist1b_bare_rock", "supports",
     "Atmospheric loss mechanisms inform bare-rock interpretations."),
    ("jwst_exoplanet_atmospheres", "trappist1b_bare_rock", "supports",
     "JWST spectroscopy is the measurement channel for TRAPPIST atmospheres."),
    ("jwst_exoplanet_atmospheres", "k2_18b_biosignature", "supports",
     "Biosignature claims ride on atmospheric spectroscopy."),
    ("k2_18b_biosignature", "jwst_exoplanet_atmospheres", "specializes",
     "K2-18 b is a contested reading of JWST-era atmosphere data."),
    ("planet_nine", "exoplanets_exist", "boundary",
     "Planet Nine is a solar-system oddity housed near exoplanet claims."),
    ("ocean_worlds_icy_moons", "exoplanets_exist", "boundary",
     "Solar-system oceans vs planets around other stars — different domains."),

    # --- earth ---
    ("plate_tectonics_drives_earthquakes", "eew_gives_usable_warning",
     "supports",
     "EEW sits on tectonic earthquake generation."),
    ("plate_tectonics_drives_earthquakes", "characteristic_earthquake_model",
     "requires",
     "Characteristic-earthquake debates presuppose tectonic quakes."),
    ("plate_tectonics_drives_earthquakes", "induced_seismicity_human_activities",
     "supports",
     "Induced events are still elastic failure on faults — often plate-loaded."),
    ("plate_tectonics_drives_earthquakes", "short_term_deterministic_prediction",
     "requires",
     "Prediction/forecasting debates presuppose tectonic earthquake generation."),
    ("short_term_deterministic_prediction", "oef_informs_civil_protection",
     "tensions",
     "OEF is probabilistic forecasting; deterministic prediction is the rival ask."),
    ("short_term_deterministic_prediction", "van_electric_precursors",
     "specializes",
     "VAN is a concrete prediction-claim under the short-term prediction debate."),
    ("eew_gives_usable_warning", "oef_informs_civil_protection", "boundary",
     "Seconds of EEW vs days–weeks of forecast probabilities — different tools."),
    ("slow_slip_and_ets_observed", "plate_tectonics_drives_earthquakes",
     "supports",
     "ETS is observed deformation on subduction plate interfaces."),
    ("hydrothermal_vents_exist", "ocean_heat_uptake", "boundary",
     "Vents and heat uptake are different ocean-science cuts."),
    ("ocean_heat_uptake", "ocean_acidification_anthropogenic", "supports",
     "Both are primary ocean responses to anthropogenic CO2 / heat forcing."),
    ("ocean_acidification_anthropogenic", "hydrothermal_vents_exist", "boundary",
     "Acidification is surface-carbon chemistry; vents are chemosynthetic oases."),
    ("ccz_biodiversity_unknown", "deep_sea_mining_impacts_uncertain",
     "supports",
     "Undescribed CCZ diversity is why mining impacts stay hard to quantify."),
    ("microplastics_reach_deep_ocean", "hydrothermal_vents_exist", "boundary",
     "Deep plastics are a contamination layer; vents are ecosystems."),
    ("dark_oxygen_production", "hydrothermal_vents_exist", "boundary",
     "Dark-oxygen claim is abyssal nodules — not vent chemistry consensus."),
    ("amoc_weakening", "ocean_heat_uptake", "supports",
     "AMOC debates sit inside a warming, heat-absorbing ocean."),
)


def authored_links() -> List[ClaimLink]:
    return [
        ClaimLink(s, t, k, n, origin="authored")
        for s, t, k, n in _AUTHORED
    ]


# ---------------------------------------------------------------------------
# Authored reading paths (ordered claim ids). Not rankings — sequences.
# Each step should already be connected by some authored edge when possible;
# disconnected steps are allowed if the note explains the map jump.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReadingPath:
    id: str
    title: str
    title_zh: str
    domain: str          # primary topic id
    steps: Tuple[str, ...]
    note: str
    note_zh: str
    guide: str = ""      # P-Guide: short authored walkthrough (not a verdict)
    guide_zh: str = ""

    def as_dict(self) -> dict:
        d = {
            "id": self.id,
            "title": self.title,
            "title_zh": self.title_zh,
            "domain": self.domain,
            "steps": list(self.steps),
            "n_steps": len(self.steps),
            "note": self.note,
            "note_zh": self.note_zh,
            "guide": self.guide,
            "guide_zh": self.guide_zh,
        }
        assert not (set(d) & BANNED_KEYS)
        return d


_READING_PATHS: Tuple[ReadingPath, ...] = (
    ReadingPath(
        id="path_h0",
        title="H0 tension — poles and relief routes",
        title_zh="H0 張力 —— 兩極與緩解路徑",
        domain="cosmology",
        steps=(
            "universe_is_expanding",
            "cmb_hot_big_bang",
            "H0_tension_local_vs_cmb",
            "shoes_local_H0_high",
            "cmb_lcdm_implies_low_H0",
            "trgb_vs_cepheid_local_H0",
            "early_dark_energy_H0_fix",
            "strong_lensing_time_delay_H0",
            "standard_sirens_H0",
        ),
        note=(
            "Bedrock expansion/CMB → umbrella → local and early poles → "
            "local calibrator split → three Frontier relief routes."
        ),
        note_zh=(
            "擴張/CMB 地基 → 傘形宣稱 → 本地與早期兩極 → 本地校準分裂 → "
            "三條前沿緩解路徑。"
        ),
        guide=(
            "Start from expansion and the CMB (what is Established). "
            "The yellow umbrella is the disagreement under standard assumptions — "
            "not a claim that cosmology is broken. Then read the two poles, the "
            "local calibrator split, and three Frontier routes that might arbitrate. "
            "No path step is a winner."
        ),
        guide_zh=(
            "先從擴張與 CMB(已確立)讀起。黃燈傘形是在標準假設下的不一致 — "
            "不是「宇宙學壞了」。再讀兩極、本地校準分裂、三條可能仲裁的前沿路徑。"
            "路徑上沒有勝負。"
        ),
    ),
    ReadingPath(
        id="path_stars",
        title="Stars — fusion floor to death channels",
        title_zh="恆星 —— 聚變地基到死亡通道",
        domain="stars",
        steps=(
            "stars_powered_by_fusion",
            "helioseismology_constrains_solar_interior",
            "cno_cycle_solar_neutrinos_detected",
            "stellar_nucleosynthesis_makes_elements",
            "core_collapse_forms_ns_bh",
            "white_dwarfs_electron_degenerate",
            "red_supergiant_problem",
            "sn_ia_progenitor_channels",
            "pair_instability_bh_mass_gap",
            "pop_iii_already_routinely_observed",
        ),
        note=(
            "Fusion and solar interior → nucleosynthesis and remnants → "
            "yellow death-channel debates → PISN gap → red Pop III ceiling."
        ),
        note_zh=(
            "聚變與太陽內部 → 核合成與殘骸 → 黃燈死亡通道 → PISN 間隙 → "
            "紅燈 Pop III 天花板。"
        ),
        guide=(
            "Fusion is the floor. Solar interior and CNO neutrinos deepen the "
            "laboratory. Nucleosynthesis and remnants are Strong. Yellow nodes "
            "are open engineering of death channels. The red ceiling forbids "
            "routine local Pop III — absence of acceptance, not a joke claim."
        ),
        guide_zh=(
            "聚變是地板。太陽內部與 CNO 微中子加深實驗室。核合成與殘骸是強共識。"
            "黃燈是死亡通道的開放工程問題。紅燈天花板禁止「本地常規 Pop III」—"
            "是主流不接受，不是玩笑宣稱。"
        ),
    ),
    ReadingPath(
        id="path_black_hole",
        title="Black holes — horizon to ceilings",
        title_zh="黑洞 —— 視界到天花板",
        domain="black_hole",
        steps=(
            "event_horizon_exists",
            "kerr_describes_astrophysical_bh",
            "smbh_common_in_galaxy_nuclei",
            "hawking_radiation",
            "lower_mass_gap_compact_objects",
            "bbh_mergers_catalogued",
            "jets_extract_bh_spin",
            "information_paradox",
            "firewall",
            "horizonless_gw_echoes",
        ),
        note=(
            "Horizon bedrock → Kerr/SMBH shelf → lower mass gap → "
            "catalogues and jets → information → firewall and echo ceilings."
        ),
        note_zh=(
            "視界地基 → 克爾/SMBH 平台 → 低質量間隙 → 目錄與噴流 → "
            "資訊悖論 → 防火牆與回聲天花板。"
        ),
        guide=(
            "Horizons exist (Established). Kerr and nuclear SMBHs are the Strong "
            "working picture. The lower mass gap is Competing. Catalogues, jets and "
            "the information paradox are Frontier programmes. Firewall and "
            "established GW echoes stay Speculative ceilings."
        ),
        guide_zh=(
            "視界存在(已確立)。克爾與星系核 SMBH 是強共識工作圖像。低質量間隙是 Competing。"
            "目錄、噴流與資訊悖論是前沿。防火牆與「回聲已確立」停在推測天花板。"
        ),
    ),
    ReadingPath(
        id="path_dark_matter",
        title="Dark matter — discrepancy to identity ceiling",
        title_zh="暗物質 —— 差異到身份天花板",
        domain="dark_matter",
        steps=(
            "mass_discrepancy_observed",
            "lcdm_includes_cold_dm",
            "particle_vs_modified_gravity",
            "dm_particle_identity",
            "thermal_wimp_freezeout_benchmark",
            "direct_detection_wimp_searches",
            "axion_dm_candidate",
            "fermi_gc_excess_origin",
            "sterile_neutrino_7kev_line",
            "pbh_all_dark_matter",
        ),
        note=(
            "Discrepancy floor → CDM → particle vs modified gravity → "
            "identity programmes → contested and speculative ceilings."
        ),
        note_zh=(
            "差異地基 → CDM → 粒子 vs 修正重力 → 身份綱領 → "
            "爭議與推測天花板。"
        ),
        guide=(
            "Mass discrepancy is the floor. CDM is Strong scaffolding. Particle vs "
            "modified gravity is the structural yellow split. Identity programmes "
            "(WIMP, axion, …) are specialisations. Red ceilings mark claims the "
            "mainstream does not accept as discovery."
        ),
        guide_zh=(
            "質量差異是地板。CDM 是強鷹架。粒子 vs 修正重力是結構性黃燈分裂。"
            "身份綱領(WIMP、軸子…)是具體化。紅燈天花板標記主流不接受為發現的宣稱。"
        ),
    ),
    ReadingPath(
        id="path_exoplanets",
        title="Exoplanets — existence to biosignature ceiling",
        title_zh="系外行星 —— 存在到生物訊號天花板",
        domain="exoplanets",
        steps=(
            "exoplanets_exist",
            "proxima_b_exists",
            "planets_are_common",
            "planet_nine",
            "radius_valley_mechanism",
            "jwst_exoplanet_atmospheres",
            "trappist1b_bare_rock",
            "k2_18b_biosignature",
        ),
        note=(
            "Existence and commonality → yellow debates → JWST atmospheres → "
            "biosignature red ceiling."
        ),
        note_zh=(
            "存在與常見性 → 黃燈辯論 → JWST 大氣 → 生物訊號紅燈天花板。"
        ),
        guide=(
            "Existence is Established; commonality is Strong demography. Planet Nine "
            "and the radius-valley mechanism are Competing debates. JWST atmospheres "
            "are Frontier measurement. Biosignature-as-life stays Speculative."
        ),
        guide_zh=(
            "存在是已確立；常見性是強共識人口統計。Planet Nine 與半徑谷機制是 Competing。"
            "JWST 大氣是前沿測量。生物訊號-as-生命停在推測。"
        ),
    ),
    ReadingPath(
        id="path_ocean",
        title="Deep ocean — vents to dark-oxygen ceiling",
        title_zh="深海 —— 熱泉到暗氧天花板",
        domain="ocean",
        steps=(
            "hydrothermal_vents_exist",
            "ocean_heat_uptake",
            "ocean_acidification_anthropogenic",
            "amoc_weakening",
            "ccz_biodiversity_unknown",
            "microplastics_reach_deep_ocean",
            "deep_sea_mining_impacts_uncertain",
            "dark_oxygen_production",
        ),
        note=(
            "Vent bedrock → heat and acidification → AMOC debate → "
            "CCZ/mining/plastics frontier → dark oxygen ceiling."
        ),
        note_zh=(
            "熱泉地基 → 熱與酸化 → AMOC 辯論 → CCZ/採礦/塑膠前沿 → 暗氧天花板。"
        ),
        guide=(
            "Vents are Established ecology. Heat uptake and acidification are Strong "
            "bulk responses. AMOC is Competing. CCZ biodiversity, plastics and mining "
            "impacts are Frontier. Dark oxygen is a Speculative ceiling after critique."
        ),
        guide_zh=(
            "熱泉是已確立生態。熱吸收與酸化是強共識總量回應。AMOC 是 Competing。"
            "CCZ 生物多樣性、塑膠與採礦影響是前沿。暗氧在批評後停在推測天花板。"
        ),
    ),
    ReadingPath(
        id="path_seismology",
        title="Earthquakes — plates to prediction ceiling",
        title_zh="地震 —— 板塊到預測天花板",
        domain="seismology",
        steps=(
            "plate_tectonics_drives_earthquakes",
            "eew_gives_usable_warning",
            "induced_seismicity_human_activities",
            "characteristic_earthquake_model",
            "short_term_deterministic_prediction",
            "oef_informs_civil_protection",
            "slow_slip_and_ets_observed",
            "van_electric_precursors",
        ),
        note=(
            "Plate bedrock → EEW and induced seismicity → yellow "
            "characteristic/prediction debates → OEF and ETS → VAN ceiling."
        ),
        note_zh=(
            "板塊地基 → EEW 與誘發地震 → 黃燈特徵/預測辯論 → OEF 與 ETS → VAN 天花板。"
        ),
        guide=(
            "Plates cause earthquakes (Established). EEW and induced seismicity are "
            "Strong capabilities/facts. Characteristic quakes and deterministic "
            "prediction vs forecasting are Competing. OEF and ETS are Frontier. "
            "VAN electric precursors remain Speculative."
        ),
        guide_zh=(
            "板塊造成地震(已確立)。EEW 與誘發地震是強能力/事實。特徵地震與確定性預測"
            "vs 預報是 Competing。OEF 與 ETS 是前沿。VAN 電前兆停在推測。"
        ),
    ),
)


def reading_paths() -> List[ReadingPath]:
    return list(_READING_PATHS)


def validate_reading_paths(topics: Sequence[Topic]) -> List[str]:
    idx = claim_index(topics)
    bad: List[str] = []
    seen_ids: Set[str] = set()
    for rp in reading_paths():
        if rp.id in seen_ids:
            bad.append(f"duplicate_path_id {rp.id}")
        seen_ids.add(rp.id)
        if len(rp.steps) < 2:
            bad.append(f"path_too_short {rp.id}")
        for s in rp.steps:
            if s not in idx:
                bad.append(f"path_missing_claim {rp.id}:{s}")
        if len(set(rp.steps)) != len(rp.steps):
            bad.append(f"path_duplicate_step {rp.id}")
    return bad


def coverage_stats(
    topics: Sequence[Topic],
    links: Optional[Sequence[ClaimLink]] = None,
) -> dict:
    """Sparse-honesty inventory: how many claims have any related edge."""
    idx = claim_index(topics)
    links = list(links if links is not None else all_links(topics))
    touched: Set[str] = set()
    authored_touched: Set[str] = set()
    for L in links:
        touched.add(L.source)
        touched.add(L.target)
        if L.origin == "authored":
            authored_touched.add(L.source)
            authored_touched.add(L.target)
    n = len(idx)
    n_any = sum(1 for c in idx if c in touched)
    n_auth = sum(1 for c in idx if c in authored_touched)
    # degree histogram (authored undirected)
    deg: Dict[str, int] = {c: 0 for c in idx}
    for L in links:
        if L.origin != "authored":
            continue
        if L.source in deg:
            deg[L.source] += 1
        if L.target in deg:
            deg[L.target] += 1
    # string keys only — JSON-stable and walk-safe (no int dict keys)
    hist = {"0": 0, "1": 0, "2": 0, "3+": 0}
    for d in deg.values():
        if d == 0:
            hist["0"] += 1
        elif d == 1:
            hist["1"] += 1
        elif d == 2:
            hist["2"] += 1
        else:
            hist["3+"] += 1
    stats = {
        "n_claims": n,
        "n_with_any_edge": n_any,
        "n_with_authored_edge": n_auth,
        "n_isolated": n - n_any,
        "n_isolated_authored": n - n_auth,
        "authored_degree_hist": hist,
        "n_reading_paths": len(reading_paths()),
        "note": (
            "Isolation is honest sparsity, not a defect. "
            "Counts are list counts — recount them yourself."
        ),
    }
    assert not (set(stats) & BANNED_KEYS)
    return stats


def graph_neighborhood(
    claim_id: str,
    topics: Sequence[Topic],
    *,
    authored_only: bool = False,
) -> dict:
    """Layout-ready ego network for one claim (center + 1-hop neighbors).

    Positions are deterministic polar layout — no physics, no scores.
    """
    import math
    idx = claim_index(topics)
    if claim_id not in idx:
        return {"center": None, "nodes": [], "edges": []}
    links = all_links(topics)
    if authored_only:
        links = [L for L in links if L.origin == "authored"]
    rel = enrich_related(neighbors(claim_id, links), idx)
    # unique neighbor ids preserving order
    seen: Set[str] = set()
    neigh_ids: List[str] = []
    for r in rel:
        if r["id"] not in seen:
            seen.add(r["id"])
            neigh_ids.append(r["id"])
    # cap fan-out for readability
    neigh_ids = neigh_ids[:16]
    nodes = []
    t0, c0 = idx[claim_id]
    nodes.append({
        "id": claim_id,
        "title": c0.title,
        "status_light": c0.status.light,
        "status": c0.status.name,
        "topic": t0.id,
        "role": "center",
        "x": 0.0,
        "y": 0.0,
        "permalink": f"{t0.id}.html#c-{claim_id}",
    })
    n = max(len(neigh_ids), 1)
    for i, nid in enumerate(neigh_ids):
        t, c = idx[nid]
        ang = (2 * math.pi * i / n) - math.pi / 2
        r = 1.0
        nodes.append({
            "id": nid,
            "title": c.title,
            "status_light": c.status.light,
            "status": c.status.name,
            "topic": t.id,
            "role": "neighbor",
            "x": round(r * math.cos(ang), 4),
            "y": round(r * math.sin(ang), 4),
            "permalink": f"{t.id}.html#c-{nid}",
        })
    # edges between center and neighbors only (ego graph)
    edges = []
    for L in links:
        pair = {L.source, L.target}
        if claim_id not in pair:
            continue
        other = L.target if L.source == claim_id else L.source
        if other not in seen and other != claim_id:
            continue
        if other not in neigh_ids and other != claim_id:
            continue
        if other == claim_id:
            continue
        edges.append({
            "source": L.source,
            "target": L.target,
            "kind": L.kind,
            "kind_label_en": KIND_LABELS[L.kind]["en"],
            "kind_label_zh": KIND_LABELS[L.kind]["zh"],
            "note": L.note,
            "origin": L.origin,
        })
    g = {
        "center": claim_id,
        "nodes": nodes,
        "edges": edges,
        "n_nodes": len(nodes),
        "n_edges": len(edges),
    }
    assert not (set(g) & BANNED_KEYS)
    return g


def _norm_source_key(url_or_id: str) -> str:
    s = (url_or_id or "").strip().lower()
    for pref in ("arxiv:", "doi:", "https://doi.org/", "http://doi.org/",
                 "https://arxiv.org/abs/", "http://arxiv.org/abs/"):
        if s.startswith(pref):
            s = s[len(pref):]
    return s.rstrip("/")


def mechanical_shared_source_links(
    topics: Sequence[Topic],
    *,
    min_tier_primary: bool = False,
) -> List[ClaimLink]:
    """Undirected shared-source edges, emitted once as source < target id."""
    from .model import tier_of

    # claim_id -> set of normalized source keys
    keys: Dict[str, Set[str]] = {}
    for t in topics:
        for c in t.claims:
            ks: Set[str] = set()
            for s in c.sources:
                if min_tier_primary and tier_of(s.kind) != "PRIMARY":
                    continue
                k = _norm_source_key(s.url_or_id)
                if k and len(k) > 4:
                    ks.add(k)
            keys[c.id] = ks

    # inverted index
    inv: Dict[str, List[str]] = {}
    for cid, ks in keys.items():
        for k in ks:
            inv.setdefault(k, []).append(cid)

    out: List[ClaimLink] = []
    seen: Set[Tuple[str, str]] = set()
    for k, cids in inv.items():
        cids = sorted(set(cids))
        if len(cids) < 2:
            continue
        # cap fan-out per source to avoid complete bipartite blow-up
        for i, a in enumerate(cids):
            for b in cids[i + 1: i + 1 + 8]:
                pair = (a, b)
                if pair in seen:
                    continue
                seen.add(pair)
                out.append(ClaimLink(
                    a, b, "shares_source",
                    f"Both cite source key {k[:48]}",
                    origin="mechanical",
                ))
    return out


def all_links(
    topics: Sequence[Topic],
    *,
    include_mechanical: bool = True,
) -> List[ClaimLink]:
    links = list(authored_links())
    if include_mechanical:
        links.extend(mechanical_shared_source_links(topics))
    return links


def claim_index(topics: Sequence[Topic]) -> Dict[str, Tuple[Topic, Claim]]:
    idx: Dict[str, Tuple[Topic, Claim]] = {}
    for t in topics:
        for c in t.claims:
            idx[c.id] = (t, c)
    return idx


def validate_links(
    topics: Sequence[Topic],
    links: Optional[Sequence[ClaimLink]] = None,
) -> List[str]:
    """Return human-readable violation strings (empty = clean)."""
    idx = claim_index(topics)
    links = list(links if links is not None else authored_links())
    bad: List[str] = []
    for L in links:
        if L.kind not in LINK_KINDS:
            bad.append(f"unknown_kind {L.kind} on {L.source}->{L.target}")
        if L.source not in idx:
            bad.append(f"missing_source {L.source}")
        if L.target not in idx:
            bad.append(f"missing_target {L.target}")
        if L.source == L.target:
            bad.append(f"self_loop {L.source}")
        if not (L.note or "").strip():
            bad.append(f"empty_note {L.source}->{L.target}")
    # duplicate authored edges
    seen: Set[Tuple[str, str, str]] = set()
    for L in links:
        if L.origin != "authored":
            continue
        key = (L.source, L.target, L.kind)
        if key in seen:
            bad.append(f"duplicate_authored {key}")
        seen.add(key)
    return bad


def neighbors(
    claim_id: str,
    links: Sequence[ClaimLink],
    *,
    kinds: Optional[Set[str]] = None,
) -> List[dict]:
    """Direct related rows (outbound + inbound)."""
    rows: List[dict] = []
    for L in links:
        if kinds and L.kind not in kinds:
            continue
        if L.source == claim_id:
            rows.append({
                "id": L.target,
                "kind": L.kind,
                "kind_label_en": KIND_LABELS[L.kind]["en"],
                "kind_label_zh": KIND_LABELS[L.kind]["zh"],
                "direction": "out",
                "note": L.note,
                "origin": L.origin,
            })
        elif L.target == claim_id:
            inv = KIND_INVERSE[L.kind]
            lab = KIND_INVERSE_LABELS[inv]
            rows.append({
                "id": L.source,
                "kind": inv,
                "kind_label_en": lab["en"],
                "kind_label_zh": lab["zh"],
                "direction": "in",
                "note": L.note,
                "origin": L.origin,
            })
    return rows


def infer_paths(
    claim_id: str,
    links: Sequence[ClaimLink],
    *,
    max_depth: int = 2,
    max_paths: int = 12,
    authored_only: bool = True,
) -> List[dict]:
    """List short paths starting at claim_id. Transparent listing only.

    A path is recorded as ordered claim ids + edge kinds. No strength score.
    """
    # adjacency: node -> list of (neighbor, kind, note, origin)
    adj: Dict[str, List[Tuple[str, str, str, str]]] = {}
    for L in links:
        if authored_only and L.origin != "authored":
            continue
        # treat as undirected for path discovery so inbound is reachable
        adj.setdefault(L.source, []).append(
            (L.target, L.kind, L.note, L.origin))
        adj.setdefault(L.target, []).append(
            (L.source, KIND_INVERSE[L.kind], L.note, L.origin))

    paths: List[dict] = []
    # BFS of paths
    queue: List[Tuple[List[str], List[str]]] = [([claim_id], [])]
    seen_end: Set[Tuple[str, ...]] = set()
    while queue and len(paths) < max_paths:
        nodes, kinds = queue.pop(0)
        if len(nodes) - 1 >= max_depth:
            continue
        last = nodes[-1]
        for nxt, kind, note, origin in adj.get(last, []):
            if nxt in nodes:
                continue
            n_nodes = nodes + [nxt]
            n_kinds = kinds + [kind]
            key = tuple(n_nodes)
            if key in seen_end:
                continue
            seen_end.add(key)
            if len(n_nodes) >= 2:
                paths.append({
                    "path": n_nodes,
                    "kinds": n_kinds,
                    "depth": len(n_nodes) - 1,
                    "via": n_nodes[1:-1],
                    "end": n_nodes[-1],
                    "origin": "path",
                    "note": (
                        f"path length {len(n_nodes) - 1}"
                        + (f" via {' → '.join(n_nodes[1:-1])}"
                           if len(n_nodes) > 2 else "")
                    ),
                })
            if len(n_nodes) - 1 < max_depth:
                queue.append((n_nodes, n_kinds))
    return paths


def enrich_related(
    rows: List[dict],
    idx: Dict[str, Tuple[Topic, Claim]],
) -> List[dict]:
    out = []
    for r in rows:
        meta = idx.get(r["id"])
        if not meta:
            continue
        t, c = meta
        item = dict(r)
        item["title"] = c.title
        item["status"] = c.status.name
        item["status_light"] = c.status.light
        item["topic"] = t.id
        item["permalink"] = f"{t.id}.html#c-{c.id}"
        assert not (set(item) & BANNED_KEYS)
        out.append(item)
    return out


def relations_payload(topics: Sequence[Topic]) -> dict:
    """Build the JSON-serialisable relations block for app-data."""
    idx = claim_index(topics)
    authored = authored_links()
    mechanical = mechanical_shared_source_links(topics)
    # Prefer authored; add mechanical only when no authored edge exists
    # between the pair (either direction).
    authored_pairs = {
        frozenset((L.source, L.target)) for L in authored
    }
    mech_filtered = [
        L for L in mechanical
        if frozenset((L.source, L.target)) not in authored_pairs
    ]
    links = authored + mech_filtered
    violations = validate_links(topics, authored)
    if violations:
        raise ValueError("relation graph invalid: " + "; ".join(violations[:8]))

    per_claim: Dict[str, dict] = {}
    for cid in idx:
        rel = enrich_related(neighbors(cid, links), idx)
        # depth-2 paths ending at other claims (skip trivial length-1 dupes
        # already in related — keep paths with depth>=2 primarily, plus
        # length-1 authored for inference list if useful)
        paths = infer_paths(cid, authored, max_depth=2, max_paths=16)
        # keep only paths that reach a known claim and depth>=1
        paths = [p for p in paths if p["end"] in idx]
        # attach end titles
        for p in paths:
            end = idx[p["end"]][1]
            p["end_title"] = end.title
            p["end_light"] = end.status.light
            p["end_topic"] = idx[p["end"]][0].id
        per_claim[cid] = {
            "related": rel,
            "inferences": paths,
            "n_related": len(rel),
            "n_inferences": len(paths),
        }

    path_bad = validate_reading_paths(topics)
    if path_bad:
        raise ValueError("reading paths invalid: " + "; ".join(path_bad[:8]))

    paths_out = []
    for rp in reading_paths():
        d = rp.as_dict()
        # attach lights/titles for each step (presentation only)
        step_meta = []
        for sid in rp.steps:
            t, c = idx[sid]
            step_meta.append({
                "id": sid,
                "title": c.title,
                "status_light": c.status.light,
                "status": c.status.name,
                "topic": t.id,
                "permalink": f"{t.id}.html#c-{sid}",
            })
        d["step_meta"] = step_meta
        paths_out.append(d)

    cov = coverage_stats(topics, links)

    payload = {
        "note": (
            "Claim relations: authored edges + mechanical shared-source. "
            "Inference paths and reading paths are listed routes — "
            "not confidence."
        ),
        "kinds": sorted(LINK_KINDS),
        "kind_labels": KIND_LABELS,
        "links": [L.as_dict() for L in links],
        "n_links": len(links),
        "n_authored": len(authored),
        "n_mechanical": len(mech_filtered),
        "by_claim": per_claim,
        "reading_paths": paths_out,
        "coverage": cov,
    }
    assert not (set(payload) & BANNED_KEYS)
    return payload


def format_claim_report(claim_id: str, topics: Sequence[Topic]) -> str:
    idx = claim_index(topics)
    if claim_id not in idx:
        return f"unknown claim: {claim_id}"
    payload = relations_payload(topics)
    block = payload["by_claim"][claim_id]
    t, c = idx[claim_id]
    lines = [
        f"{c.status.light} {claim_id}  ({t.id})",
        c.title,
        f"related: {block['n_related']}   inference paths: {block['n_inferences']}",
        "",
        "— related —",
    ]
    for r in block["related"]:
        lines.append(
            f"  [{r['origin']}] {r['direction']} {r['kind_label_en']:16} "
            f"{r['status_light']} {r['id']}"
        )
        lines.append(f"      {r['note']}")
    lines.append("")
    lines.append("— inference paths (depth ≤ 2) —")
    for p in block["inferences"][:12]:
        chain = " → ".join(p["path"])
        lines.append(f"  {chain}")
        lines.append(f"      kinds={p['kinds']}  {p['note']}")
    lines.append("")
    lines.append(
        "Counts are counts of listed edges/paths — not a confidence score."
    )
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse
    import json
    from .data.registry import TOPICS

    p = argparse.ArgumentParser(description="Claim relations / inference")
    p.add_argument("--claim", help="print related + paths for one claim id")
    p.add_argument("--json", action="store_true")
    p.add_argument("--validate", action="store_true",
                   help="validate authored graph only")
    args = p.parse_args(argv)

    if args.validate:
        bad = validate_links(TOPICS) + validate_reading_paths(TOPICS)
        if bad:
            print("FAIL")
            for b in bad:
                print(" ", b)
            return 1
        cov = coverage_stats(TOPICS)
        print(f"OK  {len(authored_links())} authored links, "
              f"{len(claim_index(TOPICS))} claims, "
              f"{len(reading_paths())} reading paths")
        print(f"    with authored edge: {cov['n_with_authored_edge']}/"
              f"{cov['n_claims']}  isolated(authored): "
              f"{cov['n_isolated_authored']}")
        return 0

    if args.claim:
        if args.json:
            payload = relations_payload(TOPICS)
            print(json.dumps(payload["by_claim"].get(args.claim, {}),
                             ensure_ascii=False, indent=2))
        else:
            print(format_claim_report(args.claim, TOPICS))
        return 0

    payload = relations_payload(TOPICS)
    if args.json:
        print(json.dumps({
            k: payload[k] for k in (
                "note", "kinds", "n_links", "n_authored", "n_mechanical")
        }, ensure_ascii=False, indent=2))
    else:
        print(f"links: {payload['n_links']} "
              f"(authored {payload['n_authored']} + "
              f"mechanical {payload['n_mechanical']})")
        print(f"claims with relations block: {len(payload['by_claim'])}")
        print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
