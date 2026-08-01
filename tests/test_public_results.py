import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from verify_public_results import build_report


class PublicResultsTest(unittest.TestCase):
    def test_public_results_pass(self):
        report = build_report()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["row_counts"]["query_level_rows"], 3000)
        self.assertEqual(report["row_counts"]["aggregate_rows"], 60)
        self.assertEqual(report["maximum_regret_range"], 0.1086)


if __name__ == "__main__":
    unittest.main()
