# Reproducibility

The portable Graph-VALID implementation was validated against hash-verified canonical benchmark outputs.

## Exact validation summary

- 500 benchmark replicate identifiers matched exactly.
- B1-B5 row-wise prediction mismatches: 0.
- B5 intermediate source-support mismatches: 0.
- Classwise metric field mismatches: 0.

Reproduced macro-F1 values:

| Layer | Macro-F1 |
|---|---:|
| B1 | 0.18548752834467122 |
| B2 | 0.23100878363003030 |
| B3 | 0.29013104666678585 |
| B4 | 0.35531271332661607 |
| B5 | 0.33580465525919130 |

Reproduced B5-minus-B4 point difference: `-0.019508058067424783`.

Canonical paired bootstrap:
- RNG: `PCG64DXSM`
- fixed canonical seed: `282049723644848642`
- resamples: `10,000`
- quantile method: linear
- reproduced 95% CI: `[-0.04695832892520332, 0.006105670734807242]`
- global superiority: `false`

Exact CI reproduction requires the historical benchmark replicate-plan row order. Row order does not alter source-attribution predictions or point metrics.

The repository does not redistribute unpublished genotype matrices or other local analysis assets. The selected-lead common-kinship LMM was executed in the study workflow; this portable package consumes the resulting source-support indicators and does not substitute another mixed-model implementation.

Graph-VALID reports statistical source-support states, not causal-source assignments.
