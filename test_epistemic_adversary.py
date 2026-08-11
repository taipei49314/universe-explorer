"""Amendments #7–#10 — red-team PoCs must bite.

Cheap paths to a green Established + E1 without real science must fail.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from universe_explorer.axes import EvidenceStrength, derive
from universe_explorer.model import (
    Claim,
    CompetingModel,
    ConditionAssessment,
    Evidence,
    Source,
    Status,
    Topic,
)
from universe_explorer.provenance import (
    arxiv_id_of,
    doi_of,
    is_fetchable_endpoint,
    validate_provenance,
)
from universe_explorer.validator import validate_claim


def _vc(claim: Claim, **kwargs):
    """Shape + #10 rules; provenance only when requested."""
    return validate_claim(claim, check_provenance=kwargs.pop("check_provenance", False), **kwargs)


def _established_reasons(note: str = "Substantial justification for the condition."):
    return [
        ConditionAssessment("multiple_independent_replications", True, note),
        ConditionAssessment("accepted_in_mainstream_textbooks", True, note),
        ConditionAssessment("no_mainstream_competing_theory", True, note),
        ConditionAssessment("no_recent_major_refutation", True, note),
    ]


def _strong_reasons(note: str = "Substantial justification for the condition."):
    return [
        ConditionAssessment("mainstream_model_support", True, note),
        ConditionAssessment("minor_alternatives_exist", True, note),
        ConditionAssessment("overall_direction_robust", True, note),
    ]


def test_redteam_example_com_cannot_be_e1():
    """Two fake peer-reviewed hosts + dual direct must not yield E1."""
    claim = Claim(
        id="poc_fake_e1",
        title="Fake established",
        status=Status.ESTABLISHED,
        sources=[
            Source("a", "https://example.com/paper1", "peer-reviewed paper"),
            Source("b", "https://example.com/paper2", "peer-reviewed paper"),
        ],
        evidence=[
            Evidence("direct observation", "Invented 1", "a"),
            Evidence("direct observation", "Invented 2", "b"),
        ],
        status_reason=_established_reasons(),
    )
    # PRIMARY without fetchable endpoint is unconstitutional (amendment-7).
    rules = {v.rule for v in _vc(claim)}
    assert "primary_source_not_fetchable" in rules
    # Even if someone forced the axis alone, E1 must refuse non-fetchable PRIMARY.
    assert derive(claim).strength is not EvidenceStrength.E1_MULTIPLE_DIRECT
    assert derive(claim).strength is EvidenceStrength.E2_SINGLE_DIRECT


def test_arxiv_https_url_requires_fetch():
    """https://arxiv.org/abs/… is the same endpoint as arXiv:… (amendment-7)."""
    assert arxiv_id_of("https://arxiv.org/abs/1906.11238") == "1906.11238"
    assert arxiv_id_of("http://arxiv.org/pdf/1906.11238v2.pdf") == "1906.11238"
    assert arxiv_id_of("arXiv:1906.11238") == "1906.11238"

    claim = Claim(
        id="poc_url_arxiv",
        title="Needs fetch",
        status=Status.SPECULATIVE,
        sources=[
            Source(
                "S",
                "https://arxiv.org/abs/0000.99999",
                "peer-reviewed paper",
            ),
        ],
        evidence=[Evidence("theoretical derivation", "d", "S")],
        status_reason=[
            ConditionAssessment("no_observational_evidence", True, "n"),
        ],
    )
    topic = Topic(id="t", title="t", summary="s", claims=[claim])
    # Empty temp manifest — never fetched.
    tmp = Path(tempfile.mkdtemp())
    mpath = tmp / "manifest.json"
    mpath.write_text("{}", encoding="utf-8")
    rules = {v.rule for v in validate_provenance(topic, mpath)}
    assert "arxiv_source_unfetched" in rules


def test_doi_url_and_bare_doi_normalize():
    assert doi_of("doi:10.1038/378355a0") == "10.1038/378355a0"
    assert doi_of("https://doi.org/10.1038/378355a0") == "10.1038/378355a0"
    assert doi_of("10.1038/378355a0") == "10.1038/378355a0"
    assert is_fetchable_endpoint("https://dx.doi.org/10.1073/pnas.15.3.168")


def test_empty_title_rejected():
    claim = Claim(
        id="poc_blank",
        title="   ",
        status=Status.SPECULATIVE,
        sources=[Source("s", "doi:10.1038/378355a0", "peer-reviewed paper")],
        evidence=[Evidence("theoretical derivation", "d", "s")],
        status_reason=[
            ConditionAssessment("pure_theoretical_derivation", True, "n"),
        ],
    )
    assert "empty_title" in {v.rule for v in _vc(claim)}


def test_duplicate_source_label_rejected():
    claim = Claim(
        id="poc_dup",
        title="Dup labels",
        status=Status.SPECULATIVE,
        sources=[
            Source("s", "doi:10.1038/378355a0", "peer-reviewed paper"),
            Source("s", "doi:10.1038/nature10684", "peer-reviewed paper"),
        ],
        evidence=[Evidence("theoretical derivation", "d", "s")],
        status_reason=[
            ConditionAssessment("pure_theoretical_derivation", True, "n"),
        ],
    )
    assert "duplicate_source_label" in {v.rule for v in _vc(claim)}


def test_established_without_e1_rejected():
    """Amendment #8: checkbox Established cannot sit on E2/E3/E4."""
    claim = Claim(
        id="poc_floor_est",
        title="Only one direct line",
        status=Status.ESTABLISHED,
        sources=[
            Source("A", "arXiv:1111.11111", "peer-reviewed paper"),
        ],
        evidence=[
            Evidence("direct observation", "single line", "A"),
        ],
        status_reason=_established_reasons(),
    )
    assert derive(claim).strength is EvidenceStrength.E2_SINGLE_DIRECT
    assert "consensus_floor_established" in {v.rule for v in _vc(claim)}


def test_strong_on_theory_only_rejected():
    """Amendment #8: Strong may not rest on E4 theoretical-only."""
    claim = Claim(
        id="poc_floor_strong",
        title="Theory costume as strong",
        status=Status.STRONG,
        sources=[
            Source("A", "arXiv:1111.11111", "peer-reviewed paper"),
        ],
        evidence=[
            Evidence("theoretical derivation", "on paper only", "A"),
        ],
        status_reason=_strong_reasons(),
        trace_refs=["A"],
    )
    assert derive(claim).strength is EvidenceStrength.E4_THEORETICAL
    assert "consensus_floor_strong" in {v.rule for v in _vc(claim)}


def test_strong_times_e3_divergence_still_legal():
    """hawking-style Strong × analog-only remains constitutional."""
    from universe_explorer.data.black_hole import hawking_radiation
    assert derive(hawking_radiation).strength is EvidenceStrength.E3_INDIRECT_ANALOG
    assert _vc(hawking_radiation) == []


def test_e1_rejects_same_paper_two_labels():
    """Amendment #9: one arXiv under two labels is not two independent directs."""
    claim = Claim(
        id="poc_same_paper",
        title="Duplicate labels",
        status=Status.ESTABLISHED,
        sources=[
            Source("a", "arXiv:1906.11238", "peer-reviewed paper"),
            Source("b", "https://arxiv.org/abs/1906.11238", "peer-reviewed paper"),
        ],
        evidence=[
            Evidence("direct observation", "o1", "a"),
            Evidence("direct observation", "o2", "b"),
        ],
        status_reason=_established_reasons(),
        trace_refs=["a", "b"],
    )
    assert derive(claim).strength is EvidenceStrength.E2_SINGLE_DIRECT
    assert "consensus_floor_established" in {v.rule for v in _vc(claim)}


def test_e1_rejects_version_twins():
    """v1/v2 of the same arXiv id collapse to one paper identity."""
    claim = Claim(
        id="poc_vtwins",
        title="Version twins",
        status=Status.ESTABLISHED,
        sources=[
            Source("a", "arXiv:1906.11238v1", "peer-reviewed paper"),
            Source("b", "arXiv:1906.11238v2", "peer-reviewed paper"),
        ],
        evidence=[
            Evidence("direct observation", "o1", "a"),
            Evidence("direct observation", "o2", "b"),
        ],
        status_reason=_established_reasons(),
        trace_refs=["a", "b"],
    )
    assert derive(claim).strength is EvidenceStrength.E2_SINGLE_DIRECT


def test_preprint_kind_not_promoted_to_primary():
    from universe_explorer.model import tier_of

    assert tier_of("preprint (peer-reviewed later)") == "PREPRINT"
    assert tier_of("peer-reviewed paper") == "PRIMARY"


def test_e1_requires_two_fetchable_primary_with_staged_cache():
    """Two direct + two PRIMARY arXiv with real cache shape can still be E1."""
    fake_id_a, fake_id_b = "1111.11111", "2222.22222"
    xml_a = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        f'<entry><id>http://arxiv.org/abs/{fake_id_a}v1</id>'
        "<title>a</title></entry></feed>"
    )
    xml_b = xml_a.replace(fake_id_a, fake_id_b)
    tmp = Path(tempfile.mkdtemp())
    for fid, body in ((fake_id_a, xml_a), (fake_id_b, xml_b)):
        (tmp / f"{fid}.xml").write_text(body, encoding="utf-8")
    manifest = {
        fake_id_a: {
            "cache_file": f"{fake_id_a}.xml",
            "sha256": hashlib.sha256(xml_a.encode()).hexdigest(),
        },
        fake_id_b: {
            "cache_file": f"{fake_id_b}.xml",
            "sha256": hashlib.sha256(xml_b.encode()).hexdigest(),
        },
    }
    mpath = tmp / "manifest.json"
    mpath.write_text(json.dumps(manifest), encoding="utf-8")

    claim = Claim(
        id="poc_real_e1_shape",
        title="Two fetchable directs",
        status=Status.STRONG,
        sources=[
            Source("A", f"https://arxiv.org/abs/{fake_id_a}", "peer-reviewed paper"),
            Source("B", f"arXiv:{fake_id_b}", "peer-reviewed paper"),
        ],
        evidence=[
            Evidence("direct observation", "obs a", "A"),
            Evidence("direct observation", "obs b", "B"),
        ],
        status_reason=_strong_reasons(),
        trace_refs=["A", "B"],
    )
    assert derive(claim).strength is EvidenceStrength.E1_MULTIPLE_DIRECT
    topic = Topic(id="t", title="t", summary="s", claims=[claim])
    assert validate_provenance(topic, mpath) == []
    assert _vc(claim) == []
    assert _vc(claim, check_provenance=True, manifest_path=mpath) == []


def test_a10_prize_cannot_carry_direct():
    claim = Claim(
        id="poc_prize_direct",
        title="Prize as direct",
        status=Status.SPECULATIVE,
        sources=[Source("n", "nobelprize.org/x", "prize citation (x)")],
        evidence=[Evidence("direct observation", "orbits", "n")],
        status_reason=[ConditionAssessment("philosophical_inference", True, "n")],
    )
    assert "evidence_type_requires_primary_fetchable" in {v.rule for v in _vc(claim)}


def test_a10_vacuous_note_blocked_on_strong():
    claim = Claim(
        id="poc_vacuous",
        title="Vacuous",
        status=Status.STRONG,
        sources=[Source("A", "doi:10.1038/378355a0", "peer-reviewed paper")],
        evidence=[Evidence("analog experiment", "lab work recorded", "A")],
        status_reason=_strong_reasons(note="I say so"),
        trace_refs=["A"],
    )
    assert "status_reason_vacuous_note" in {v.rule for v in _vc(claim)}


def test_a10_trace_refs_required_for_established():
    claim = Claim(
        id="poc_no_trace",
        title="No anchors",
        status=Status.ESTABLISHED,
        sources=[
            Source("A", "doi:10.1038/378355a0", "peer-reviewed paper"),
            Source("B", "doi:10.1073/pnas.15.3.168", "peer-reviewed paper"),
        ],
        evidence=[
            Evidence("direct observation", "obs a long enough", "A"),
            Evidence("direct observation", "obs b long enough", "B"),
        ],
        status_reason=_established_reasons(),
        # no trace_refs
    )
    assert "trace_refs_missing" in {v.rule for v in _vc(claim)}


def test_a10_competing_needs_two_papers():
    claim = Claim(
        id="poc_one_paper_camps",
        title="One paper two camps",
        status=Status.COMPETING,
        sources=[Source("A", "arXiv:1111.11111", "peer-reviewed paper")],
        evidence=[Evidence("indirect observation", "weak", "A")],
        competing_models=[
            CompetingModel("CampA", "s", "o", "l"),
            CompetingModel("CampB", "s", "o", "l"),
        ],
        status_reason=[
            ConditionAssessment("two_or_more_mainstream_models", True, "two camps named"),
            ConditionAssessment("no_decisive_evidence_yet", True, "still open"),
            ConditionAssessment("genuine_scientific_camps", True, "real split"),
        ],
    )
    assert "competing_needs_distinct_papers" in {v.rule for v in _vc(claim)}


def test_a10_frontier_needs_fetchable():
    claim = Claim(
        id="poc_frontier_tb",
        title="Frontier on textbook",
        status=Status.FRONTIER,
        sources=[Source("T", "Some Textbook", "textbook")],
        evidence=[Evidence("theoretical derivation", "idea", "T")],
        status_reason=[ConditionAssessment("new_discovery", True, "brand new idea")],
    )
    assert "frontier_needs_fetchable_source" in {v.rule for v in _vc(claim)}


def test_a10_hidden_title_controls():
    claim = Claim(
        id="poc_zw",
        title="Fake\u200bClaim",
        status=Status.SPECULATIVE,
        sources=[Source("T", "tb", "textbook")],
        evidence=[Evidence("theoretical derivation", "d", "T")],
        status_reason=[ConditionAssessment("pure_theoretical_derivation", True, "n")],
    )
    assert "title_hidden_controls" in {v.rule for v in _vc(claim)}


def test_a10_claim_default_includes_provenance():
    """C4: unfetched arXiv is visible on validate_claim when provenance on."""
    claim = Claim(
        id="poc_unfetched",
        title="Needs fetch",
        status=Status.SPECULATIVE,
        sources=[Source("S", "arXiv:0000.99999", "peer-reviewed paper")],
        evidence=[Evidence("theoretical derivation", "d", "S")],
        status_reason=[ConditionAssessment("no_observational_evidence", True, "none yet")],
    )
    rules = {v.rule for v in _vc(claim, check_provenance=True)}
    assert "arxiv_source_unfetched" in rules
