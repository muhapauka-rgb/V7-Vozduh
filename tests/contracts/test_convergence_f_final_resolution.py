import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"

ROUTE_RE = re.compile(
    r"path\s*(?:==|!=)\s*[\"']([^\"']+)[\"']|path\.startswith\([\"']([^\"']+)[\"']\)"
)

SIMULATION_ROUTES = {
    "/api/execution/outcome-preview",
    "/api/execution/blast-radius",
    "/api/execution/service-impact",
}

REQUIRED_REPORTS = {
    "CONVERGENCE_F_DUPLICATION_REVIEW.md",
    "CONVERGENCE_F_TRUTH_SOURCE_REVIEW.md",
    "CONVERGENCE_F_DEFERRED_API_DECISION.md",
    "CONVERGENCE_F_SIMULATION_CONSOLIDATION.md",
    "CONVERGENCE_F_API_CERTIFICATION.md",
    "CONVERGENCE_F_UI_CERTIFICATION.md",
    "CONVERGENCE_F_TRUTH_SOURCE_CERTIFICATION.md",
    "CONVERGENCE_F_DUPLICATION_CERTIFICATION.md",
    "CONVERGENCE_F_BRANCH_CERTIFICATION.md",
    "CONVERGENCE_F_PUSH_READINESS.md",
    "CONVERGENCE_F_TEST_RESULTS.md",
    "BLOCK_CONVERGENCE_F_FINAL_CONVERGENCE_RESOLUTION_REPORT.md",
}


class ConvergenceFFinalResolutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ADMIN_API.read_text(encoding="utf-8")
        cls.routes = {
            match.group(1) or match.group(2)
            for match in ROUTE_RE.finditer(cls.source)
            if match.group(1) or match.group(2)
        }

    def test_simulation_routes_are_resolved_as_viewer_read_apis(self):
        self.assertTrue(SIMULATION_ROUTES <= self.routes)
        for route in sorted(SIMULATION_ROUTES):
            with self.subTest(route=route):
                self.assertIn(f'"{route}": "viewer"', self.source)

    def test_simulation_routes_reuse_existing_derived_models(self):
        self.assertIn("def execution_outcome_preview_response(", self.source)
        self.assertIn("def execution_blast_radius_response(", self.source)
        self.assertIn("def execution_service_impact_response(", self.source)
        self.assertIn('"canonical_model": "execution_candidate_outcome_for_draft"', self.source)
        self.assertIn("execution_candidate_outcome_for_draft(draft)", self.source)
        self.assertIn("execution_blast_radius_for_draft(draft)", self.source)
        self.assertIn("execution_service_impact_for_draft(draft)", self.source)

    def test_simulation_routes_remain_non_executable(self):
        self.assertIn('"execution_allowed_now": False', self.source)
        self.assertIn('"preview_only": True', self.source)
        forbidden = (
            '"/api/execution/apply"',
            '"/api/execution/execute"',
            '"/api/execution/run"',
            '"/api/execution/route-apply"',
            '"/api/execution/autoswitch-apply"',
        )
        for fragment in forbidden:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, self.source)

    def test_ui_uses_existing_execution_drawer_for_simulation_surfaces(self):
        tabs = set(re.findall(r'data-tab="([^"]+)"', self.source))
        self.assertFalse({"execution", "simulation", "impact"} & tabs)
        self.assertEqual(self.source.count("async function openExecutionSummaryDrawer("), 1)
        self.assertEqual(self.source.count("function executionOutcomePreviewHtml("), 1)
        self.assertEqual(self.source.count("function executionBlastRadiusHtml("), 1)
        self.assertEqual(self.source.count("function executionServiceImpactHtml("), 1)

    def test_required_convergence_f_reports_exist(self):
        missing = sorted(name for name in REQUIRED_REPORTS if not (ROOT / name).exists())
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
