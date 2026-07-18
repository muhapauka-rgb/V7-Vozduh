import importlib.machinery
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
MASTER_PROGRAM = ROOT / "docs/programs/V7_ROUTING_DIGITAL_TWIN_POLYGON_MASTER_PROGRAM.md"


def load_admin_api():
    path = ROOT / "admin" / "v7-admin-api"
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
        self.assertIn("docs/programs/V7_ROUTING_DIGITAL_TWIN_POLYGON_MASTER_PROGRAM.md", paths)
        self.assertIn("docs/reference/SYSTEM_MAP.md", paths)
        self.assertIn("docs/reference/V7_CANONICAL_REFERENCE.md", paths)
        self.assertEqual(index.get("source"), "docs/reference/V7_OPERATOR_FILE_MEMO.md")

    def test_live_dashboard_uses_authoritative_section_zero(self):
        response = self.admin_api.omp_dashboard_response()
        operator = response["operator_view"]
        self.assertEqual(operator["current_program"], "PERMANENT_POLYGON_OMP_INTEGRATION_PROGRAM")
        self.assertEqual(operator["current_step"], "PERMANENT_POLYGON_CAPABILITY_CLOSURE_GENERATION")
        self.assertEqual(operator["next_step"], "PERMANENT-POLYGON-TARGET-LEVEL-FINAL-CERTIFICATION-G1")
        self.assertEqual(operator["next_scenario"], "NONE")
        self.assertEqual(operator["current_stop"], "NONE")
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
        self.assertTrue(response["current_state_generation"].startswith("cpsgen_V7_PPOLY_M7_ACTIVE_"))
        self.assertEqual(response["current_transition_id"], "PERMANENT_POLYGON_FINAL_CERTIFICATION_ACTIVE_V1")

    def test_polygon_master_program_has_no_volatile_activation_status(self):
        text = MASTER_PROGRAM.read_text(encoding="utf-8")
        self.assertIn("Status: `APPROVED_EXECUTION_PLAN`", text)
        self.assertIn("Activation state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`", text)
        self.assertNotIn("APPROVED_EXECUTION_PLAN_NOT_ACTIVE", text)

    def test_polygon_master_program_preserves_compression_and_substrate_continuation(self):
        text = MASTER_PROGRAM.read_text(encoding="utf-8")
        self.assertIn("### 2.1 Dynamic Mission Compression", text)
        self.assertIn("`MISSION_NOT_REQUIRED_ALREADY_CONSUMED`", text)
        self.assertIn("### 2.2 Substrate Degradation Law", text)
        self.assertIn("A missing L3/L4 substrate is `POLYGON_SUBSTRATE_LIMIT`, not `REAL_WORLD_LIMIT`", text)


if __name__ == "__main__":
    unittest.main()
