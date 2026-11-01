# Graph-VALID

**Graph-VALID** is a calibrated source-attribution framework for interpreting graph-pangenome-associated genetic gains when SNP/InDel and structural-variant (SV) spaces are unequal and correlated.

The software implements the source-attribution decision procedure described in the RECOMB 2027 manuscript:

> **Graph-VALID: Calibrating the sources of graph-pangenome-associated genetic gains**

Graph-VALID does **not** infer molecular causality. It maps statistical evidence to one of six source-support states:

- `NULL`
- `SNP_LED`
- `SV_RETAINED`
- `CROSS_SOURCE_TAG_AMBIGUOUS`
- `MIXED`
- `UNRESOLVED`

## Method overview

Five cumulative analysis layers are exposed:

- **B1** — raw source-wise minimum-\(P\) comparison.
- **B2** — source-specific Bonferroni calibration.
- **B3** — source-specific LD-aware effective-test calibration.
- **B4** — B3 plus cross-source tagging and conditional attribution.
- **B5** — B4-type attribution after source-specific empirical-null confirmation, followed by state-specific kinship-aware compatibility assessment.

The benchmark values used in the manuscript are:

- \(M_{\mathrm{eff,SNP/InDel}} = 229,793.8037987769\)
- \(M_{\mathrm{eff,SV}} = 13,112.067729427283\)
- SNP/InDel threshold = \(2.1758637166641537\times 10^{-7}\)
- SV threshold = \(3.813281095840094\times 10^{-6}\)
- local comparison window = 1 Mb
- low tagging = \(r^2 < 0.20\)
- strong tagging = \(r^2 \ge 0.80\)
- minimum pairwise non-missing samples = 265

## Install

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

For tests:

```bash
python -m pip install -e ".[test]"
pytest -q
```

## Quick example

```bash
python scripts/run_example.py
```

## Evidence-table CLI

```bash
graph-valid attribute \
  --input examples/example_evidence.tsv \
  --output predictions.tsv \
  --layer B4
```

The evidence-table schema is described in `docs/INPUT_SCHEMA.md`.

## Benchmark scoring

A table containing one truth column and one prediction column per analysis layer can be scored with:

```bash
graph-valid score \
  --input benchmark_predictions.tsv \
  --truth-column truth \
  --layers B1 B2 B3 B4 B5 \
  --bootstrap 10000 \
  --output benchmark_summary.json
```

`UNRESOLVED` is an abstention output, not a sixth truth class. For macro-F1 it counts as an incorrect prediction for the corresponding generating class.

### Canonical paired-bootstrap configuration

- RNG: `PCG64DXSM`
- fixed canonical seed: `282049723644848642`
- resamples: `10,000`
- quantiles: linear interpolation

Exact manuscript-CI reproduction requires the original benchmark replicate-plan row order before integer-index bootstrap resampling. The source-attribution predictions and point metrics are invariant to row order; the deterministic bootstrap stream is not.

## Reproducibility boundary

This release contains the portable source-attribution and benchmark-scoring implementation. It intentionally contains no machine-specific paths, credentials, internal execution-stage identifiers, or unpublished raw genotype data.

Full reproduction of the manuscript's 332-accession benchmark additionally requires the analysis-ready genotype/phenotype assets described in the manuscript and Supplementary Materials. Those assets are not bundled in this repository. The original tomato graph-pangenome resources are described by Zhou et al. (Nature 2022;606:527–534).

The selected-lead common-\(K\) LMM itself was run in the study analysis workflow; this portable package consumes its source-support indicators for the final B5 compatibility decision. This avoids silently substituting a different LMM implementation.

## Validation

Run:

```bash
python scripts/validate_release.py
```

The validator performs:

1. Python syntax compilation.
2. Unit tests.
3. Deterministic example execution.
4. Absolute local-path audit.
5. Basic secret-pattern audit.
6. Manuscript constant checks.

The portable implementation has been validated against hash-verified canonical benchmark outputs: all 500 B1-B5 predictions, intermediate B5 source-support states, classwise metrics, headline macro-F1 values, state counts, and the paired-bootstrap confidence interval were reproduced within numerical tolerance.

## License

No software license is included in this candidate package. The authors should select and add an explicit license before public release.

## Citation

Citation metadata are provided in `CITATION.cff`.
