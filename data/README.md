# Data Files

This directory contains processed retrieval-evaluation outputs used by the
public verification script.

| File | Description |
| --- | --- |
| `public_summary.json` | Sanitized machine-readable summary of the public candidate. |
| `results.csv` | Query-level metric rows. |
| `results_aggregated.csv` | Aggregate metric cells by dataset, method, and seed. |
| `dataset_summary.csv` | Dataset-level query/corpus/qrels context. |
| `method_quality_table.csv` | Mean quality and cached timing values used in the manuscript. |
| `regret_rank_stability.csv` | Dataset-wise rank and regret summary. |
| `bootstrap_ci.csv` | Paired bootstrap confidence intervals and adjusted p-values. |
| `latency_cost_context.csv` | Cached latency and build-time context. |

The CSV files contain derived metrics and identifiers, not raw document text.
