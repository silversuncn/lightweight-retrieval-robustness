#!/usr/bin/env python3
"""Verify the public result tables for the retrieval robustness bundle."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"

EXPECTED_TITLE = "Lightweight Retrieval Robustness across Heterogeneous Tasks"
EXPECTED_AUTHORS = ["Yaowen Sun", "Hai Du", "Qian Zhang"]
EXPECTED_DATASETS = ["arguana", "fiqa", "nfcorpus", "scifact"]
EXPECTED_METHODS = ["bm25", "all_minilm_l6", "bge_small_en_v15"]
EXPECTED_QUERY_COUNTS = {
    "arguana": 1406,
    "fiqa": 648,
    "nfcorpus": 323,
    "scifact": 300,
}
EXPECTED_NDCG = {
    ("arguana", "bm25"): 0.34078699269741264,
    ("arguana", "all_minilm_l6"): 0.36983417349799114,
    ("arguana", "bge_small_en_v15"): 0.4332670933862082,
    ("fiqa", "bm25"): 0.23719561294834587,
    ("fiqa", "all_minilm_l6"): 0.36867136984071597,
    ("fiqa", "bge_small_en_v15"): 0.39126178824863234,
    ("nfcorpus", "bm25"): 0.3073218775425817,
    ("nfcorpus", "all_minilm_l6"): 0.31672230320930983,
    ("nfcorpus", "bge_small_en_v15"): 0.3454137274739744,
    ("scifact", "bm25"): 0.662213025368359,
    ("scifact", "all_minilm_l6"): 0.6450816521455774,
    ("scifact", "bge_small_en_v15"): 0.7005040179184695,
}
EXPECTED_FIGURES = {
    "fig1_quality_bars_v2.png",
    "fig2_regret_heatmap_v2.png",
    "fig3_bootstrap_distributions_v2.png",
}
DISALLOWED_COLUMN_FRAGMENTS = ("stage", "top1", "score", "seconds", "cap")


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def assert_equal(label: str, observed: object, expected: object) -> None:
    if observed != expected:
        raise AssertionError(f"{label}: observed {observed!r}, expected {expected!r}")


def assert_close(label: str, observed: float, expected: float) -> None:
    if not math.isclose(observed, expected, rel_tol=0.0, abs_tol=1e-12):
        raise AssertionError(f"{label}: observed {observed!r}, expected {expected!r}")


def assert_public_columns(name: str, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise AssertionError(f"{name}: no rows")
    for column in rows[0]:
        lowered = column.lower()
        if any(fragment in lowered for fragment in DISALLOWED_COLUMN_FRAGMENTS):
            raise AssertionError(f"{name}: disallowed public column {column!r}")


def build_report() -> dict[str, object]:
    summary = json.loads((DATA / "public_summary.json").read_text(encoding="utf-8"))
    query_rows = read_csv("results.csv")
    aggregate_rows = read_csv("results_aggregated.csv")
    dataset_rows = read_csv("dataset_summary.csv")
    regret_rows = read_csv("regret_rank_stability.csv")
    pairwise_rows = read_csv("pairwise_statistics.csv")

    for name, rows in (
        ("results.csv", query_rows),
        ("results_aggregated.csv", aggregate_rows),
        ("dataset_summary.csv", dataset_rows),
        ("regret_rank_stability.csv", regret_rows),
        ("pairwise_statistics.csv", pairwise_rows),
    ):
        assert_public_columns(name, rows)

    assert_equal("title", summary["title"], EXPECTED_TITLE)
    assert_equal("authors", summary["authors"], EXPECTED_AUTHORS)
    assert_equal("query rows", len(query_rows), 8031)
    assert_equal("aggregate rows", len(aggregate_rows), 12)
    assert_equal("dataset rows", len(dataset_rows), 4)
    assert_equal("regret rows", len(regret_rows), 12)
    assert_equal("pairwise statistic rows", len(pairwise_rows), 36)
    assert_equal("summary query rows", summary["row_counts"]["query_level_rows"], 8031)
    assert_equal("summary combinations", summary["row_counts"]["model_dataset_combinations"], 12)
    assert_equal("summary runtime table flag", summary["runtime_measurements_in_public_tables"], False)
    assert_equal("summary BGE-small ordering", summary["bge_small_leads_all_datasets"], True)

    datasets = sorted({row["dataset"] for row in aggregate_rows})
    methods = sorted({row["method"] for row in aggregate_rows})
    assert_equal("datasets", datasets, sorted(EXPECTED_DATASETS))
    assert_equal("methods", methods, sorted(EXPECTED_METHODS))

    query_counts: dict[tuple[str, str], int] = {}
    for row in query_rows:
        key = (row["dataset"], row["method"])
        query_counts[key] = query_counts.get(key, 0) + 1
    for dataset in EXPECTED_DATASETS:
        for method in EXPECTED_METHODS:
            assert_equal(f"{dataset} {method} query count", query_counts[(dataset, method)], EXPECTED_QUERY_COUNTS[dataset])

    ndcg_by_dataset: dict[str, dict[str, float]] = {}
    for row in aggregate_rows:
        dataset = row["dataset"]
        method = row["method"]
        observed = float(row["ndcg@10"])
        assert_close(f"{dataset} {method} nDCG@10", observed, EXPECTED_NDCG[(dataset, method)])
        ndcg_by_dataset.setdefault(dataset, {})[method] = observed
        assert_equal(f"{dataset} {method} eligible flag", row["full_eligible_query_set"], "True")
        assert_equal(f"{dataset} {method} eligible query count", int(row["n_queries"]), EXPECTED_QUERY_COUNTS[dataset])

    best_methods = {
        dataset: max(method_scores.items(), key=lambda item: item[1])[0]
        for dataset, method_scores in ndcg_by_dataset.items()
    }
    assert_equal("best methods", best_methods, {dataset: "bge_small_en_v15" for dataset in EXPECTED_DATASETS})

    bge_rank_rows = [
        row for row in regret_rows
        if row["method"] == "bge_small_en_v15" and row["method_rank"] == "1" and row["regret_ndcg@10"] == "0.0"
    ]
    assert_equal("BGE-small rank-one rows", len(bge_rank_rows), 4)

    actual_figures = {path.name for path in FIGURES.iterdir() if path.is_file()}
    assert_equal("figures", actual_figures, EXPECTED_FIGURES)

    return {
        "result": "PASS",
        "title": summary["title"],
        "row_counts": {
            "query_level_rows": len(query_rows),
            "model_dataset_combinations": len(aggregate_rows),
            "pairwise_statistics": len(pairwise_rows),
        },
        "best_methods": best_methods,
        "figures": sorted(actual_figures),
    }


def main() -> None:
    print(json.dumps(build_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
