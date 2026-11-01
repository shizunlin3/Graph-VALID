import json
from pathlib import Path
from graph_valid.constants import B3_THRESHOLD_SNP, B3_THRESHOLD_SV

def test_frozen_summary_counts_and_headline_values():
    p = Path(__file__).parent / "fixtures" / "frozen_manuscript_summary.json"
    x = json.loads(p.read_text())
    assert x["headline_macro_f1"]["B4"] == 0.35531271332661607
    assert x["headline_macro_f1"]["B5"] == 0.3358046552591913
    assert x["paired_bootstrap_ci95"] == [-0.04695832892520332, 0.006105670734807242]
    assert x["global_superiority"] is False
    assert sum(x["B4_prediction_counts"].values()) == 500
    assert sum(x["B5_prediction_counts"].values()) == 500
    assert x["B5_prediction_counts"]["UNRESOLVED"] == 108
    assert x["B5_abstention"] == 0.216
    assert x["B5_coverage"] == 0.784
    assert abs(B3_THRESHOLD_SNP - 2.1758637166641537e-07) < 1e-20
    assert abs(B3_THRESHOLD_SV - 3.813281095840094e-06) < 1e-20
