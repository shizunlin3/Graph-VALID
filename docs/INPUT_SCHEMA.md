# Evidence-table schema

Graph-VALID separates **evidence construction** from **source-state attribution**.

The `attribute` command consumes a tab-delimited table with one row per trait or benchmark replicate.

## Required for all layers

| Column | Meaning |
|---|---|
| `p_snp` | minimum SNP/InDel source-wise association P value |
| `p_sv` | minimum SV source-wise association P value |

## Additional B2 columns

- `n_snp`
- `n_sv`

## Optional B3 override columns

If omitted, the manuscript benchmark constants are used:

- `meff_snp`
- `meff_sv`

## Additional B4 columns when both sources pass B3

- `same_chromosome`
- `distance_bp`
- `r2`
- `n_pair`
- `conditional_p_snp`
- `conditional_p_sv`

Conditional P values are required only for local low-tagging pairs.

## Additional B5 columns

- `empirical_p_snp`
- `empirical_p_sv`
- `lmm_support_snp`
- `lmm_support_sv`

The LMM support columns are boolean indicators derived from the selected-lead common-\(K\) analysis used by the study. The portable package does not substitute a different LMM implementation.
