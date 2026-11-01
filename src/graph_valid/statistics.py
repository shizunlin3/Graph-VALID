from __future__ import annotations

import numpy as np
from scipy import stats

def squared_pearson_r2(x, y, min_pairs: int = 265):
    """Squared Pearson dosage correlation using pairwise non-missing samples."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape")
    mask = np.isfinite(x) & np.isfinite(y)
    n = int(mask.sum())
    if n < int(min_pairs):
        return None, n
    xv = x[mask]
    yv = y[mask]
    if np.std(xv) == 0 or np.std(yv) == 0:
        return None, n
    r = float(np.corrcoef(xv, yv)[0, 1])
    return r * r, n

def conditional_ols_pvalues(y, g_snp, g_sv, pcs=None):
    """
    Two-sided OLS t-test P values for SNP/InDel and SV coefficients in:
      y = intercept + PCs + beta_snp*g_snp + beta_sv*g_sv + error
    """
    y = np.asarray(y, dtype=float)
    g_snp = np.asarray(g_snp, dtype=float)
    g_sv = np.asarray(g_sv, dtype=float)
    if not (len(y) == len(g_snp) == len(g_sv)):
        raise ValueError("y, g_snp and g_sv must have equal length")

    cols = [np.ones(len(y), dtype=float)]
    if pcs is not None:
        pcs = np.asarray(pcs, dtype=float)
        if pcs.ndim == 1:
            pcs = pcs[:, None]
        if pcs.shape[0] != len(y):
            raise ValueError("pcs must have the same number of rows as y")
        cols.extend([pcs[:, j] for j in range(pcs.shape[1])])
    cols.extend([g_snp, g_sv])
    X = np.column_stack(cols)

    mask = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    y2 = y[mask]
    X2 = X[mask]
    if len(y2) <= X2.shape[1]:
        raise ValueError("insufficient complete observations for conditional OLS")

    beta, *_ = np.linalg.lstsq(X2, y2, rcond=None)
    resid = y2 - X2 @ beta
    dof = len(y2) - X2.shape[1]
    sigma2 = float((resid @ resid) / dof)
    xtx_inv = np.linalg.pinv(X2.T @ X2)
    se = np.sqrt(np.diag(xtx_inv) * sigma2)
    t = beta / se
    p = 2.0 * stats.t.sf(np.abs(t), df=dof)

    return {
        "p_snp": float(p[-2]),
        "p_sv": float(p[-1]),
        "beta_snp": float(beta[-2]),
        "beta_sv": float(beta[-1]),
        "n_complete": int(len(y2)),
    }
