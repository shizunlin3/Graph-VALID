from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Evidence:
    """Evidence required for one Graph-VALID decision."""

    p_snp: float
    p_sv: float
    n_snp: Optional[float] = None
    n_sv: Optional[float] = None
    meff_snp: Optional[float] = None
    meff_sv: Optional[float] = None

    same_chromosome: Optional[bool] = None
    distance_bp: Optional[int] = None
    r2: Optional[float] = None
    n_pair: Optional[int] = None
    conditional_p_snp: Optional[float] = None
    conditional_p_sv: Optional[float] = None

    empirical_p_snp: Optional[float] = None
    empirical_p_sv: Optional[float] = None
    lmm_support_snp: Optional[bool] = None
    lmm_support_sv: Optional[bool] = None
