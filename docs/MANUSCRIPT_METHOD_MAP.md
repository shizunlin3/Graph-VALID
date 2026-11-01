# Manuscript-to-code map

| Manuscript component | Public implementation |
|---|---|
| B1 raw minimum-P | `graph_valid.attribution.classify_b1` |
| B2 Bonferroni | `graph_valid.attribution.classify_b2` |
| B3 LD-aware effective tests | `graph_valid.attribution.classify_b3` |
| empirical P value | `graph_valid.calibration.empirical_p_value` |
| cross-source dosage r² | `graph_valid.statistics.squared_pearson_r2` |
| conditional joint regression | `graph_valid.statistics.conditional_ols_pvalues` |
| B4 tagging + conditional attribution | `graph_valid.attribution.classify_b4` |
| B5 empirical + LMM compatibility | `graph_valid.attribution.classify_b5` |
| macro-F1 | `graph_valid.scoring.macro_f1` |
| paired bootstrap | `graph_valid.scoring.paired_bootstrap_b5_vs_best_previous` |
