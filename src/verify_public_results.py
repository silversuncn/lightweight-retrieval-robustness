#!/usr/bin/env python3
"""Verify public result tables for the retrieval robustness bundle."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


EXPECTED_DATASETS = {"arguana", "fiqa", "nfcorpus", "scifact"}
EXPECTED_METHODS = {"all_minilm_l6", "bm25"}
EXPECTED_SEEDS = {23, 41, 67, 83, 127}
EXPECTED_HEADLINES = {
    ("arguana", "all_minilm_l6"): 0.3635,
    ("arguana", "bm25"): 0.3318,
    ("fiqa", "all_minilm_l6"): 0.3808,
    ("fiqa", "bm25"): 0.2444,
    ("nfcorpus", "all_minilm_l6"): 0.2603,
    ("nfcorpus", "bm25"): 0.2599,
    ("scifact", "all_minilm_l6"): 0.6504,
    ("scifact", "bm25"): 0.6814,
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def rounded(value: str | float, digits: int = 4) -> float:
    return round(float(value), digits)


def assert_close(name: str, observed: float, expected: float, tolerance: float = 0.0001) -> None:
    if not math.isclose(observed, expected, rel_tol=0.0, abs_tol=tolerance):
        raise AssertionError(f"{name}: observed {observed}, expected {expected}")


def build_report() -> dict[str, object]:
    summary = json.loads((DATA / "public_summary.json").read_text(encoding="utf-8"))
    query_rows = read_csv("results.csv")
    aggregate_rows = read_csv("results_aggregated.csv")
    dataset_rows = read_csv("dataset_summary.csv")
    quality_rows = read_csv("method_quality_table.csv")
    bootstrap_rows = read_csv("bootstrap_ci.csv")
    regret_rows = read_csv("regret_rank_stability.csv")
    latency_rows = read_csv("latency_cost_context.csv")

    if len(query_rows) != 2000:
        raise AssertionError(f"query rows: observed {len(query_rows)}, expected 2000")
    if len(aggregate_rows) != 40:
        raise AssertionError(f"aggregate rows: observed {len(aggregate_rows)}, expected 40")
    if len(dataset_rows) != 4:
        raise AssertionError(f"dataset rows: observed {len(dataset_rows)}, expected 4")
    if len(quality_rows) != 8:
        raise AssertionError(f"quality rows: observed {len(quality_rows)}, expected 8")
    if len(bootstrap_rows) != 12:
        raise AssertionError(f"bootstrap rows: observed {len(bootstrap_rows)}, expected 12")
    if len(regret_rows) != 8:
        raise AssertionError(f"regret rows: observed {len(regret_rows)}, expected 8")
    if len(latency_rows) != 8:
        raise AssertionError(f"latency rows: observed {len(latency_rows)}, expected 8")

    datasets = {row["dataset"] for row in aggregate_rows}
    methods = {row["method"] for row in aggregate_rows}
    seeds = {int(row["seed"]) for row in aggregate_rows}
    query_caps = {int(row["query_cap"]) for row in aggregate_rows}

    if datasets != EXPECTED_DATASETS:
        raise AssertionError(f"datasets: observed {sorted(datasets)}")
    if methods != EXPECTED_METHODS:
        raise AssertionError(f"methods: observed {sorted(methods)}")
    if seeds != EXPECTED_SEEDS:
        raise AssertionError(f"seeds: observed {sorted(seeds)}")
    if query_caps != {50}:
        raise AssertionError(f"query caps: observed {sorted(query_caps)}")

    quality = {(row["dataset"], row["method"]): row for row in quality_rows}
    for key, expected in EXPECTED_HEADLINES.items():
        observed = rounded(quality[key]["ndcg@10"])
        assert_close(f"{key} nDCG@10", observed, expected)

    regret_by_method: dict[str, list[float]] = {}
    for row in regret_rows:
        regret_by_method.setdefault(row["method"], []).append(float(row["regret_ndcg@10"]))
    max_regret_range = max(max(values) - min(values) for values in regret_by_method.values())
    assert_close("maximum regret range", round(max_regret_range, 4), 0.1363)

    if {int(row["n_pairs"]) for row in bootstrap_rows} != {250}:
        raise AssertionError("all bootstrap rows must have 250 query-seed pairs")

    return {
        "status": "PASS",
        "title": summary["title"],
        "row_counts": {
            "query_level_rows": len(query_rows),
            "aggregate_rows": len(aggregate_rows),
            "dataset_rows": len(dataset_rows),
            "quality_rows": len(quality_rows),
            "bootstrap_rows": len(bootstrap_rows),
            "regret_rows": len(regret_rows),
            "latency_rows": len(latency_rows)
        },
        "datasets": sorted(datasets),
        "methods": sorted(methods),
        "seeds": sorted(seeds),
        "maximum_regret_range": round(max_regret_range, 4)
    }


def main() -> None:
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
