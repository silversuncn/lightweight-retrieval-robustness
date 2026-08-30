import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from verify_public_results import build_report


class PublicResultsTest(unittest.TestCase):
    def test_public_counts_and_best_methods(self):
        report = build_report()
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["row_counts"]["query_level_rows"], 8031)
        self.assertEqual(report["row_counts"]["model_dataset_combinations"], 12)
        self.assertEqual(set(report["best_methods"].values()), {"bge_small_en_v15"})

    def test_only_current_figures_are_present(self):
        report = build_report()
        self.assertEqual(
            report["figures"],
            [
                "fig1_quality_bars_v2.png",
                "fig2_regret_heatmap_v2.png",
                "fig3_bootstrap_distributions_v2.png",
            ],
        )


if __name__ == "__main__":
    unittest.main()
