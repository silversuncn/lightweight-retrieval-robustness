# Lightweight Retrieval Robustness under Domain Shift

> **Lightweight Retrieval Robustness under Domain Shift**  
> Yaowen Sun

## Overview

This repository contains a sanitized reproduction bundle for an empirical
retrieval study on how lightweight retrieval methods behave across public
BEIR-style datasets under a fixed evaluation protocol. The bundle includes
processed result tables, paper figures, a lightweight verification script, and
tests for checking the reported row counts and headline values.

Repository URL: https://github.com/silversuncn/lightweight-retrieval-robustness

The formal matrix contains 3,000 query-level rows and 60 aggregate cells across
four datasets, three retrieval methods, and five query-bootstrap seeds. The tested
methods are BM25 lexical retrieval, an all-MiniLM-L6 dense bi-encoder, and a
BGE-small dense bi-encoder. The
primary reported metrics are nDCG@10, MRR@10, Recall@100, method-rank stability,
cross-domain regret, and cached latency/build-time context.

## Repository Structure

```text
.
├── README.md
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── data/
│   ├── README.md
│   ├── public_summary.json
│   ├── results.csv
│   ├── results_aggregated.csv
│   ├── dataset_summary.csv
│   ├── method_quality_table.csv
│   ├── regret_rank_stability.csv
│   ├── bootstrap_ci.csv
│   └── latency_cost_context.csv
├── figures/
│   ├── figure_quality_breakdown.png
│   ├── figure_regret_heatmap.png
│   ├── figure_bootstrap_distribution.png
│   └── figure_quality_cost_pareto.png
├── src/
│   └── verify_public_results.py
└── tests/
    └── test_public_results.py
```

## Experimental Setup

| Dimension | Values | Count |
| --- | --- | ---: |
| Datasets | `arguana`, `fiqa`, `nfcorpus`, `scifact` | 4 |
| Methods | `bm25`, `all_minilm_l6`, `bge_small_en_v15` | 3 |
| Query-bootstrap seeds | 23, 41, 67, 83, 127 | 5 |
| Query cap | 50 judged queries per dataset and seed | 1 |
| Retrieval depth | Top 100 | 1 |

Row-count check:

```text
4 datasets x 3 methods x 5 seeds x 50 queries = 3,000 query-level rows
4 datasets x 3 methods x 5 seeds = 60 aggregate cells
```

## Hardware & Environment

The reported matrix was produced with Python 3.11 and GPU dense-embedding
inference on CUDA. Dense retrieval uses transformer mean pooling for MiniLM and
BGE-small; timing columns are cached-ranking context rather than end-to-end
deployment benchmarks.

## Key Results

- BGE-small has the highest mean nDCG@10 on ArguAna, NFCorpus, and SciFact.
- MiniLM has the highest mean nDCG@10 on FiQA.
- The largest single observed nDCG regret is 0.1363 for BM25 on FiQA, and the
  maximum method-level regret range is 0.1086 under the tested protocol.
- The results support a bounded empirical conclusion about dataset-dependent
  retrieval robustness; they are not a state-of-the-art claim and do not propose
  a new retrieval model.

## Requirements

The included verification script uses only the Python standard library. The
`requirements.txt` file records the main packages used by the experiment
environment.

Verify the public tables:

```bash
python src/verify_public_results.py
```

Run the tests:

```bash
python -m unittest discover -s tests -q
```

## Citation

```bibtex
@article{sun2026lightweightretrievalrobustness,
  title = {Lightweight Retrieval Robustness under Domain Shift},
  author = {Sun, Yaowen},
  year = {2026}
}
```
