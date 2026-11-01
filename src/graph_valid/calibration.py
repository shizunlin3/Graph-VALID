from __future__ import annotations

import numpy as np

from .constants import ALPHA

def bonferroni_support(p_value: float, n_tests: float, alpha: float = ALPHA) -> bool:
    if n_tests is None or n_tests <= 0:
        raise ValueError("n_tests must be positive")
    return float(p_value) <= alpha / float(n_tests)

def bonferroni_adjusted(p_value: float, n_tests: float) -> float:
    if n_tests is None or n_tests <= 0:
        raise ValueError("n_tests must be positive")
    return min(1.0, float(p_value) * float(n_tests))

def effective_test_support(p_value: float, meff: float, alpha: float = ALPHA) -> bool:
    if meff is None or meff <= 0:
        raise ValueError("meff must be positive")
    return float(p_value) <= alpha / float(meff)

def effective_test_adjusted(p_value: float, meff: float) -> float:
    if meff is None or meff <= 0:
        raise ValueError("meff must be positive")
    return min(1.0, float(p_value) * float(meff))

def empirical_p_value(observed_min_p: float, null_min_p) -> float:
    """(1 + count(null <= observed)) / (B + 1)."""
    null = np.asarray(null_min_p, dtype=float)
    if null.ndim != 1 or len(null) == 0:
        raise ValueError("null_min_p must be a non-empty one-dimensional array")
    return float((1 + np.sum(null <= float(observed_min_p))) / (len(null) + 1))
