import runpy
import unittest

from tools import v7_sync_lib


class TruthPathClassificationTest(unittest.TestCase):
    def test_uppercase_evidence_dirs_are_docs_only_for_deploy_guard(self):
        for path in (
            "docs/reports/evidence/EXEC1_EVIDENCE/autoswitch_plan_summary.json",
            "docs/reports/evidence/SNAP1_CLOSE_EVIDENCE/truth_final_summary.json",
            "tests/unit/test_truth_path_classification.py",
        ):
            self.assertTrue(v7_sync_lib.is_docs_only_change(path))

    def test_uppercase_evidence_dirs_are_documentation_only_for_dirty_status(self):
        truth = runpy.run_path("tools/v7-truth-check")
        dirty_path_category = truth["dirty_path_category"]
        for path in (
            "docs/reports/evidence/EXEC1_EVIDENCE/autoswitch_plan_summary.json",
            "docs/reports/evidence/SNAP1_CLOSE_EVIDENCE/truth_final_summary.json",
        ):
            self.assertEqual(dirty_path_category(path), "documentation_only")


if __name__ == "__main__":
    unittest.main()
