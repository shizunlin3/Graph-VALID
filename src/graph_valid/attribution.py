from __future__ import annotations

from math import isclose

from .constants import (
    ALPHA,
    MEFF_SNP,
    MEFF_SV,
    LOCAL_WINDOW_BP,
    LOW_TAG_R2,
    STRONG_TAG_R2,
    MIN_PAIRWISE_NONMISSING,
)
from .calibration import (
    bonferroni_support,
    bonferroni_adjusted,
    effective_test_support,
    effective_test_adjusted,
)
from .models import Evidence

def _state_from_single_support(snp: bool, sv: bool):
    if not snp and not sv:
        return "NULL"
    if snp and not sv:
        return "SNP_LED"
    if sv and not snp:
        return "SV_RETAINED"
    return None

def _compare(a: float, b: float, a_state: str, b_state: str):
    if isclose(float(a), float(b), rel_tol=0.0, abs_tol=0.0):
        return "UNRESOLVED"
    return a_state if a < b else b_state

def classify_b1(e: Evidence) -> str:
    snp = float(e.p_snp) <= ALPHA
    sv = float(e.p_sv) <= ALPHA
    one = _state_from_single_support(snp, sv)
    if one is not None:
        return one
    return _compare(float(e.p_snp), float(e.p_sv), "SNP_LED", "SV_RETAINED")

def classify_b2(e: Evidence) -> str:
    if e.n_snp is None or e.n_sv is None:
        raise ValueError("B2 requires n_snp and n_sv")
    snp = bonferroni_support(e.p_snp, e.n_snp)
    sv = bonferroni_support(e.p_sv, e.n_sv)
    one = _state_from_single_support(snp, sv)
    if one is not None:
        return one
    q_snp = bonferroni_adjusted(e.p_snp, e.n_snp)
    q_sv = bonferroni_adjusted(e.p_sv, e.n_sv)
    return _compare(q_snp, q_sv, "SNP_LED", "SV_RETAINED")

def _b3_support(e: Evidence):
    ms = MEFF_SNP if e.meff_snp is None else float(e.meff_snp)
    mv = MEFF_SV if e.meff_sv is None else float(e.meff_sv)
    snp = effective_test_support(e.p_snp, ms)
    sv = effective_test_support(e.p_sv, mv)
    return snp, sv, ms, mv

def classify_b3(e: Evidence) -> str:
    snp, sv, ms, mv = _b3_support(e)
    one = _state_from_single_support(snp, sv)
    if one is not None:
        return one
    q_snp = effective_test_adjusted(e.p_snp, ms)
    q_sv = effective_test_adjusted(e.p_sv, mv)
    return _compare(q_snp, q_sv, "SNP_LED", "SV_RETAINED")

def _b4_from_support(e: Evidence, snp: bool, sv: bool) -> str:
    one = _state_from_single_support(snp, sv)
    if one is not None:
        return one

    if e.same_chromosome is not True:
        return "UNRESOLVED"
    if e.distance_bp is None or int(e.distance_bp) > LOCAL_WINDOW_BP:
        return "UNRESOLVED"
    if e.r2 is None or e.n_pair is None or int(e.n_pair) < MIN_PAIRWISE_NONMISSING:
        return "UNRESOLVED"

    r2 = float(e.r2)
    if r2 >= STRONG_TAG_R2:
        return "CROSS_SOURCE_TAG_AMBIGUOUS"
    if r2 >= LOW_TAG_R2:
        return "UNRESOLVED"

    if e.conditional_p_snp is None or e.conditional_p_sv is None:
        return "UNRESOLVED"
    cs = float(e.conditional_p_snp) <= ALPHA
    cv = float(e.conditional_p_sv) <= ALPHA
    if cs and cv:
        return "MIXED"
    if cs:
        return "SNP_LED"
    if cv:
        return "SV_RETAINED"
    return "UNRESOLVED"

def classify_b4(e: Evidence) -> str:
    snp, sv, _, _ = _b3_support(e)
    return _b4_from_support(e, snp, sv)

def _lmm_compatible(state: str, e: Evidence) -> bool:
    if state == "UNRESOLVED":
        return True
    if e.lmm_support_snp is None or e.lmm_support_sv is None:
        return False
    s = bool(e.lmm_support_snp)
    v = bool(e.lmm_support_sv)
    if state == "NULL":
        return (not s) and (not v)
    if state == "SNP_LED":
        return s and (not v)
    if state == "SV_RETAINED":
        return v and (not s)
    if state == "MIXED":
        return s and v
    if state == "CROSS_SOURCE_TAG_AMBIGUOUS":
        return (
            e.same_chromosome is True
            and e.distance_bp is not None
            and int(e.distance_bp) <= LOCAL_WINDOW_BP
            and e.r2 is not None
            and float(e.r2) >= STRONG_TAG_R2
            and (s or v)
        )
    raise ValueError(f"unknown state: {state}")

def classify_b5(e: Evidence) -> str:
    b3_snp, b3_sv, _, _ = _b3_support(e)
    if e.empirical_p_snp is None or e.empirical_p_sv is None:
        raise ValueError("B5 requires empirical_p_snp and empirical_p_sv")

    snp = b3_snp and float(e.empirical_p_snp) <= ALPHA
    sv = b3_sv and float(e.empirical_p_sv) <= ALPHA
    state = _b4_from_support(e, snp, sv)

    if state == "UNRESOLVED":
        return "UNRESOLVED"
    return state if _lmm_compatible(state, e) else "UNRESOLVED"
