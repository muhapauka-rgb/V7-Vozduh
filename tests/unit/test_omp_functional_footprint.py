from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CPS = ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_footprint", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpFunctionalFootprintTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text()

    def test_current_repository_has_no_real_reconciliation_caller(self):
        result = self.lib.python_function_call_sites(ROOT, "program_execution_reconciliation")
        self.assertEqual(result["real_caller_count"], 0)
        self.assertGreaterEqual(result["test_caller_count"], 3)

    def test_test_calls_are_not_real_consumers(self):
        result = self.lib.python_function_call_sites(ROOT, "program_execution_reconciliation")
        self.assertTrue(all(item["class"] == "TEST_ONLY" for item in result["test_callers"]))

    def test_current_cps_footprint_passes(self):
        self.assertEqual(self.lib.omp_functional_footprint_consistency(self.cps, root=ROOT)["final_verdict"], "PASS")

    def test_false_complete_consumed_claim_fails(self):
        altered = self.cps.replace("`IMPLEMENTED_MANUALLY_CALLABLE`", "`COMPLETE_CONSUMED`", 1)
        result = self.lib.omp_functional_footprint_consistency(altered, root=ROOT)
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("false_automation_completion_without_real_caller", result["errors"])

    def test_false_real_automation_claim_fails(self):
        altered = self.cps.replace("`CODEX_ASSISTED`", "`REAL_ENGINEERING_AUTOMATION`", 1)
        result = self.lib.omp_functional_footprint_consistency(altered, root=ROOT)
        self.assertEqual(result["final_verdict"], "NO-GO")

    def test_active_source_caller_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            (root / "tests").mkdir()
            (root / "tools/entry.py").write_text("program_execution_reconciliation({})\n")
            (root / "tests/test_entry.py").write_text("program_execution_reconciliation({})\n")
            result = self.lib.python_function_call_sites(root, "program_execution_reconciliation")
            self.assertEqual(result["real_caller_count"], 1)
            self.assertEqual(result["test_caller_count"], 1)

    def test_scanner_is_deterministic(self):
        first = self.lib.python_function_call_sites(ROOT, "program_execution_reconciliation")
        second = self.lib.python_function_call_sites(ROOT, "program_execution_reconciliation")
        self.assertEqual(first, second)

    def test_syntax_error_does_not_create_false_caller(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            (root / "tools/broken.py").write_text("program_execution_reconciliation(\n")
            result = self.lib.python_function_call_sites(root, "program_execution_reconciliation")
            self.assertEqual(result["real_caller_count"], 0)


if __name__ == "__main__":
    unittest.main()
