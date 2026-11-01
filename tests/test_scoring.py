from graph_valid.scoring import macro_f1, abstention_rate, paired_bootstrap_b5_vs_best_previous

def test_macro_f1_perfect():
    truth = ["NULL","SNP_LED","SV_RETAINED","CROSS_SOURCE_TAG_AMBIGUOUS","MIXED"]
    assert macro_f1(truth, truth) == 1.0

def test_unresolved_is_error_not_truth_class():
    truth = ["NULL","SNP_LED","SV_RETAINED","CROSS_SOURCE_TAG_AMBIGUOUS","MIXED"]
    pred = ["UNRESOLVED"] * 5
    assert macro_f1(truth, pred) == 0.0
    assert abstention_rate(pred) == 1.0

def test_bootstrap_deterministic():
    truth = ["NULL","SNP_LED","SV_RETAINED","CROSS_SOURCE_TAG_AMBIGUOUS","MIXED"] * 20
    good = truth[:]
    weak = ["UNRESOLVED"] * len(truth)
    preds = {"B1": weak, "B2": weak, "B3": weak, "B4": weak, "B5": good}
    a = paired_bootstrap_b5_vs_best_previous(truth, preds, n_boot=100, seed=11)
    b = paired_bootstrap_b5_vs_best_previous(truth, preds, n_boot=100, seed=11)
    assert a == b
    assert a["global_superiority"] is True
