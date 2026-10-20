"""Contract checks for saved reports; use REPORT_DIR=examples for baseline evidence."""
import json
import math
import os
from pathlib import Path
import unittest

class ReportContract(unittest.TestCase):
    def test_sample_metrics(self):
        rows = json.loads((Path(os.environ.get("REPORT_DIR", "reports")) / "metrics.json").read_text())
        values = {(r["instance"], r["name"]): r["value"] for r in rows}
        self.assertEqual(values[("*", "Size")], 4.0)
        self.assertEqual(values[("customer_id", "Uniqueness")], 0.5)
        self.assertTrue(math.isclose(values[("age", "Mean")], 170/3))

    def test_intentional_failures(self):
        rows = json.loads((Path(os.environ.get("REPORT_DIR", "reports")) / "verification.json").read_text())
        self.assertEqual(len(rows), 4)
        for prefix, status in [("CompletenessConstraint", "Success"), ("UniquenessConstraint", "Failure"), ("MinimumConstraint", "Failure"), ("MaximumConstraint", "Failure")]:
            matches = [r for r in rows if r["constraint"].startswith(prefix)]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["constraint_status"], status)

if __name__ == "__main__":
    unittest.main()
