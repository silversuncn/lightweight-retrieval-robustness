# Lightweight Retrieval Robustness across Heterogeneous Tasks

> **Lightweight Retrieval Robustness across Heterogeneous Tasks**  
> Yaowen Sun; Hai Du; Qian Zhang

## Overview

This repository contains a public derived-result verification bundle for an
empirical retrieval evaluation across heterogeneous BEIR-style tasks. It
includes processed aggregate tables, paper-referenced figures, and lightweight
verification scripts, matching the paper's Data and Code Availability
statement.

This bundle verifies derived metrics and identifiers. It is not an end-to-end
retrieval reproduction pipeline: it does not redistribute raw dataset text and
does not include scripts for data acquisition, model inference, training,
retrieval reruns, or regeneration of the paper's tables and figures from raw
corpora.

The evaluation contains 8,031 query-level rows from four datasets and three
retrieval methods, forming 12 model-dataset combinations. Runtime measurements are not part of the contribution or the public result tables.

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── checksums_sha256.txt
├── data/
│   ├── README.md
│   ├── public_summary.json
│   ├── results.csv
│   ├── results_aggregated.csv
│   ├── dataset_summary.csv
│   ├── regret_rank_stability.csv
│   └── pairwise_statistics.csv
├── figures/
│   ├── fig1_quality_bars_v2.png
│   ├── fig2_regret_heatmap_v2.png
│   └── fig3_bootstrap_distributions_v2.png
├── src/
│   └── verify_public_results.py
└── tests/
    └── test_public_results.py
```

## Experimental Setup

The public tables are derived from the complete eligible query set for each
dataset. The query-level table has one row per dataset, method, and eligible
query, with columns for nDCG@10, MRR@10, and Recall@100. The aggregate table has
12 rows, one for each model-dataset combination.

| Dataset | Eligible queries |
| --- | ---: |
| ArguAna | 1,406 |
| FiQA | 648 |
| NFCorpus | 323 |
| SciFact | 300 |

| Dimension | Values | Count |
| --- | --- | ---: |
| Datasets | ArguAna, FiQA, NFCorpus, SciFact | 4 |
| Retrieval methods | BM25, all-MiniLM-L6, BGE-small | 3 |
| Evaluation unit | Eligible judged query | 8,031 rows |
| Aggregate cells | Dataset x method | 12 |

## Figures

The bundle includes only the three figures referenced by the current paper:

| File | Content |
| --- | --- |
| `figures/fig1_quality_bars_v2.png` | Mean retrieval quality by dataset and method. |
| `figures/fig2_regret_heatmap_v2.png` | Dataset-wise nDCG regret relative to the best method. |
| `figures/fig3_bootstrap_distributions_v2.png` | Query-level paired uncertainty distributions. |

## Verification

The verification script uses only the Python standard library:

```bash
python src/verify_public_results.py
```

The test suite checks the same public counts and headline ordering:

```bash
python -m unittest discover -s tests -q
```

## Hardware & Environment

The recorded v2 environment used Linux under WSL2 with Python `3.11.15`.
The package snapshot records PyTorch `2.11.0+cu128`, Transformers `5.4.0`,
NumPy `2.4.4`, SciPy `1.17.1`, Matplotlib `3.10.8`, Pandas `3.0.1`, and
Requests `2.33.1`. The public verification script is CPU-only and reads the
bundled CSV/JSON files.

## Key Results

BGE-small has the highest mean nDCG@10 on all four datasets.

| Dataset | BM25 | all-MiniLM-L6 | BGE-small | Best |
| --- | ---: | ---: | ---: | --- |
| ArguAna | 0.3408 | 0.3698 | 0.4333 | BGE-small |
| FiQA | 0.2372 | 0.3687 | 0.3913 | BGE-small |
| NFCorpus | 0.3073 | 0.3167 | 0.3454 | BGE-small |
| SciFact | 0.6622 | 0.6451 | 0.7005 | BGE-small |

These results support a bounded empirical conclusion about the tested public
datasets and methods only. The artifact does not introduce a new retrieval
model and does not make a state-of-the-art claim.

## Requirements

The bundled verifier and tests use only the Python standard library. No
third-party package is required for the included public verification checks.

## License

The code and derived public tables in this bundle are provided under the MIT
License in `LICENSE`.

## Citation

Title: Lightweight Retrieval Robustness across Heterogeneous Tasks

Authors: Yaowen Sun; Hai Du; Qian Zhang

Year: 2026
