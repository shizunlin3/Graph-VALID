import numpy as np
from graph_valid.statistics import squared_pearson_r2, conditional_ols_pvalues

def test_r2():
    x = np.arange(300, dtype=float)
    y = 2*x + 5
    r2, n = squared_pearson_r2(x, y)
    assert n == 300
    assert abs(r2 - 1.0) < 1e-12

def test_conditional_ols_identifies_both():
    rng = np.random.default_rng(7)
    n = 400
    a = rng.normal(size=n)
    b = rng.normal(size=n)
    y = 0.8*a + 0.7*b + rng.normal(scale=0.8, size=n)
    res = conditional_ols_pvalues(y, a, b)
    assert res["p_snp"] < 0.05
    assert res["p_sv"] < 0.05
