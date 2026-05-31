import py_compile
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


class ConvergenceCWave4UiIntegrationLayerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ADMIN_API.read_text(encoding="utf-8")

    def test_admin_api_compiles(self):
        py_compile.compile(
            str(ADMIN_API),
            cfile="/private/tmp/convergence-c-wave4-v7-admin-api.pyc",
            doraise=True,
        )

    def test_no_new_top_level_navigation_sections(self):
        tabs = set(re.findall(r'data-tab="([^"]+)"', self.source))
        self.assertFalse({"execution", "candidate", "approval", "governance", "rehearsal"} & tabs)
        self.assertIn('id="operatorCandidateWorkflow"', self.source)
        self.assertIn('openExecutionSummaryDrawer()', self.source)

    def test_execution_and_candidate_use_existing_drawer_family(self):
        self.assertEqual(self.source.count("async function openExecutionSummaryDrawer("), 1)
        self.assertEqual(self.source.count("async function openExecutionCandidateDrawer("), 1)
        self.assertNotIn("Candidate Drawer", self.source)
        self.assertNotIn("candidate drawer", self.source)

    def test_ui_references_resolved_simulation_public_routes_inside_execution_drawer(self):
        self.assertIn("/api/execution/outcome-preview", self.source)
        self.assertIn("/api/execution/blast-radius", self.source)
        self.assertIn("/api/execution/service-impact", self.source)
        self.assertIn("function executionOutcomePreviewHtml(", self.source)
        self.assertIn("function executionBlastRadiusHtml(", self.source)
        self.assertIn("function executionServiceImpactHtml(", self.source)

    def test_candidate_bridge_reuses_existing_truth_sources(self):
        self.assertIn("/api/execution/candidate-workflow?limit=8", self.source)
        self.assertIn("Proposal -> Candidate -> Approval Center -> Governance Preview -> Rehearsal Preview", self.source)
        self.assertIn("Approval Center reused", self.source)
        self.assertIn("Governance reused", self.source)
        self.assertIn("Rehearsal reused", self.source)
        self.assertIn("no duplicate store", self.source)

    def test_ui_layer_remains_non_executable(self):
        self.assertNotIn('"/api/execution/apply"', self.source)
        self.assertNotIn('"/api/execution/execute"', self.source)
        self.assertNotIn('"/api/execution/run"', self.source)
        self.assertIn("Preview only", self.source)


if __name__ == "__main__":
    unittest.main()
