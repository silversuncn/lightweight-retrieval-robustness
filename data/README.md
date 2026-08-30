# Data Files

This directory contains sanitized retrieval-evaluation outputs used by the
public verification script.

| File | Description |
| --- | --- |
| `public_summary.json` | Machine-readable summary of title, authors, counts, methods, and headline ordering. |
| `results.csv` | Query-level nDCG@10, MRR@10, and Recall@100 values. |
| `results_aggregated.csv` | Mean metrics for the 12 model-dataset combinations. |
| `dataset_summary.csv` | Public dataset query, corpus, and qrels counts. |
| `regret_rank_stability.csv` | Dataset-wise nDCG rank and regret values. |
| `pairwise_statistics.csv` | Query-level paired confidence intervals and adjusted p-values. |

The CSV files omit local paths, document text, raw embeddings, top-hit document
identifiers, ranking scores, and runtime columns.
