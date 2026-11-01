from __future__ import annotations

import math
import pandas as pd
from .models import Evidence

def _optional(row, name, cast=None):
    if name not in row.index or pd.isna(row[name]) or row[name] == "":
        return None
    return cast(row[name]) if cast else row[name]

def row_to_evidence(row):
    return Evidence(
        p_snp=float(row["p_snp"]),
        p_sv=float(row["p_sv"]),
        n_snp=_optional(row, "n_snp", float),
        n_sv=_optional(row, "n_sv", float),
        meff_snp=_optional(row, "meff_snp", float),
        meff_sv=_optional(row, "meff_sv", float),
        same_chromosome=_optional(row, "same_chromosome", lambda x: str(x).lower() in {"1","true","yes"}),
        distance_bp=_optional(row, "distance_bp", int),
        r2=_optional(row, "r2", float),
        n_pair=_optional(row, "n_pair", int),
        conditional_p_snp=_optional(row, "conditional_p_snp", float),
        conditional_p_sv=_optional(row, "conditional_p_sv", float),
        empirical_p_snp=_optional(row, "empirical_p_snp", float),
        empirical_p_sv=_optional(row, "empirical_p_sv", float),
        lmm_support_snp=_optional(row, "lmm_support_snp", lambda x: str(x).lower() in {"1","true","yes"}),
        lmm_support_sv=_optional(row, "lmm_support_sv", lambda x: str(x).lower() in {"1","true","yes"}),
    )
