import importlib.machinery
import importlib.util
from pathlib import Path
import unittest


def load_admin_api():
    path = Path(__file__).resolve().parents[2] / "admin" / "v7-admin-api"
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_omp_document_index_test", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class OmpDocumentIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_api = load_admin_api()

    def test_document_index_contains_core_operator_files(self):
        response = self.admin_api.omp_dashboard_response()
        index = response.get("document_index") or {}
        paths = {entry.get("path") for entry in index.get("entries", [])}

        self.assertIn("docs/programs/OPERATIONAL_MATURITY_PROGRAM.md", paths)
        self.assertIn("docs/programs/V7_CURRENT_PROGRAM_STATE.md", paths)
        self.assertIn("docs/reference/SYSTEM_MAP.md", paths)
        self.assertIn("docs/reference/V7_CANONICAL_REFERENCE.md", paths)
        self.assertEqual(index.get("source"), "docs/reference/V7_OPERATOR_FILE_MEMO.md")

    def test_live_dashboard_uses_authoritative_section_zero(self):
        response = self.admin_api.omp_dashboard_response()
        operator = response["operator_view"]
        self.assertEqual(operator["current_program"], "FUTURE_SCALE_SCENARIO_ENGINEERING")
        self.assertEqual(operator["current_step"], "STANDARD_CONTINUE_OMP")
        self.assertEqual(operator["next_step"], "CONTINUE_OMP")
        self.assertEqual(operator["next_scenario"], "NONE")
        self.assertEqual(operator["current_stop"], "BOUNDED_INVOCATION_BUDGET_REACHED")
        self.assertEqual(operator["external_input_required"], "FALSE")
        self.assertEqual(operator["omp_continuation_required"], "TRUE")

    def test_historical_dashboard_cannot_override_live_dashboard(self):
        response = self.admin_api.omp_dashboard_response()
        rendered = repr({
            "executive": response["executive_view"],
            "operator": response["operator_view"],
            "engineering": response["engineering_view"],
        })
        self.assertNotIn("ACTIONABLE_BACKLOG_COMPLETE", rendered)
        self.assertNotIn("wait for explicit operator-approved scope", rendered)
        self.assertNotIn("B2 -> B3", rendered)
        self.assertEqual(response["current_state_generation"], "cpsgen_V7_FSSE_04_AB072FDBB5E9")
        self.assertEqual(response["current_transition_id"], "FSSE_04_AUTONOMOUS_LOOP_TO_CONTINUE_OMP_V1")


if __name__ == "__main__":
    unittest.main()
