from __future__ import annotations

import numpy as np
from .constants import TRUTH_STATES, BOOTSTRAP_SEED

def _f1_for_class(y_true, y_pred, cls):
    tp = sum(t == cls and p == cls for t, p in zip(y_true, y_pred))
    fp = sum(t != cls and p == cls for t, p in zip(y_true, y_pred))
    fn = sum(t == cls and p != cls for t, p in zip(y_true, y_pred))
    denom = 2 * tp + fp + fn
    return 0.0 if denom == 0 else (2.0 * tp) / denom

def macro_f1(y_true, y_pred, classes=TRUTH_STATES):
    y_true = list(y_true)
    y_pred = list(y_pred)
    if len(y_true) != len(y_pred):
        raise ValueError("truth and prediction lengths differ")
    return float(np.mean([_f1_for_class(y_true, y_pred, c) for c in classes]))

def abstention_rate(y_pred):
    y_pred = list(y_pred)
    return float(sum(p == "UNRESOLVED" for p in y_pred) / len(y_pred))

def paired_bootstrap_b5_vs_best_previous(
    y_true,
    predictions_by_layer,
    n_boot=10000,
    seed=BOOTSTRAP_SEED,
):
    required = ["B1", "B2", "B3", "B4", "B5"]
    missing = [k for k in required if k not in predictions_by_layer]
    if missing:
        raise ValueError(f"missing layers: {missing}")

    y_true = np.asarray(list(y_true), dtype=object)
    pred = {k: np.asarray(list(predictions_by_layer[k]), dtype=object) for k in required}
    n = len(y_true)
    if any(len(v) != n for v in pred.values()):
        raise ValueError("prediction lengths differ")

    point = {k: macro_f1(y_true, pred[k]) for k in required}
    point_delta = point["B5"] - max(point[k] for k in ["B1", "B2", "B3", "B4"])

    rng = np.random.Generator(np.random.PCG64DXSM(seed))
    deltas = np.empty(int(n_boot), dtype=float)
    for b in range(int(n_boot)):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        scores = {k: macro_f1(yt, pred[k][idx]) for k in required}
        deltas[b] = scores["B5"] - max(scores[k] for k in ["B1", "B2", "B3", "B4"])

    lo, hi = np.quantile(deltas, [0.025, 0.975])
    return {
        "point_macro_f1": point,
        "point_delta_b5_vs_best_previous": float(point_delta),
        "bootstrap_ci95": [float(lo), float(hi)],
        "global_superiority": bool(lo > 0.0),
        "n_boot": int(n_boot),
        "seed": int(seed),
    }
