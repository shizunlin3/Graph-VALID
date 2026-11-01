from graph_valid.models import Evidence
from graph_valid.attribution import classify_b1, classify_b2, classify_b3, classify_b4, classify_b5

def test_b1_states():
    assert classify_b1(Evidence(0.9, 0.8)) == "NULL"
    assert classify_b1(Evidence(0.01, 0.8)) == "SNP_LED"
    assert classify_b1(Evidence(0.8, 0.01)) == "SV_RETAINED"

def test_b2_uses_adjusted_evidence_when_both_pass():
    e = Evidence(p_snp=1e-8, p_sv=2e-6, n_snp=1_000_000, n_sv=10_000)
    assert classify_b2(e) == "SNP_LED"

def test_b2_exact_adjusted_tie_is_unresolved():
    e = Evidence(p_snp=1e-8, p_sv=1e-6, n_snp=1_000_000, n_sv=10_000)
    assert classify_b2(e) == "UNRESOLVED"

def test_b4_strong_tagging():
    e = Evidence(
        p_snp=1e-10, p_sv=1e-8,
        same_chromosome=True, distance_bp=100_000,
        r2=0.90, n_pair=300,
    )
    assert classify_b4(e) == "CROSS_SOURCE_TAG_AMBIGUOUS"

def test_b4_intermediate_is_unresolved():
    e = Evidence(
        p_snp=1e-10, p_sv=1e-8,
        same_chromosome=True, distance_bp=100_000,
        r2=0.50, n_pair=300,
    )
    assert classify_b4(e) == "UNRESOLVED"

def test_b4_low_tag_conditional_mixed():
    e = Evidence(
        p_snp=1e-10, p_sv=1e-8,
        same_chromosome=True, distance_bp=100_000,
        r2=0.05, n_pair=300,
        conditional_p_snp=0.01, conditional_p_sv=0.02,
    )
    assert classify_b4(e) == "MIXED"

def test_b5_incompatible_lmm_abstains():
    e = Evidence(
        p_snp=1e-10, p_sv=1e-8,
        same_chromosome=True, distance_bp=100_000,
        r2=0.05, n_pair=300,
        conditional_p_snp=0.01, conditional_p_sv=0.2,
        empirical_p_snp=0.01, empirical_p_sv=0.01,
        lmm_support_snp=False, lmm_support_sv=True,
    )
    assert classify_b5(e) == "UNRESOLVED"

def test_b5_tag_ambiguity_requires_at_least_one_lmm_source():
    base = dict(
        p_snp=1e-10, p_sv=1e-8,
        same_chromosome=True, distance_bp=100_000,
        r2=0.90, n_pair=300,
        empirical_p_snp=0.01, empirical_p_sv=0.01,
    )
    assert classify_b5(Evidence(**base, lmm_support_snp=True, lmm_support_sv=False)) == "CROSS_SOURCE_TAG_AMBIGUOUS"
    assert classify_b5(Evidence(**base, lmm_support_snp=False, lmm_support_sv=False)) == "UNRESOLVED"
