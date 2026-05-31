import py_compile
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"

ROUTE_RE = re.compile(
    r"path\s*(?:==|!=)\s*[\"']([^\"']+)[\"']|path\.startswith\([\"']([^\"']+)[\"']\)"
)

WAVE1_ROUTES = {
    "/api/execution/contracts",
    "/api/execution/contracts/",
    "/api/execution/events",
    "/api/execution/explain",
    "/api/execution/rollback",
    "/api/execution/summary",
    "/api/execution/timeline",
    "/api/execution/verification",
}

WAVE2_ROUTES = {
    "/api/execution/contracts/draft",
    "/api/execution/contracts/draft/",
    "/api/execution/gates",
    "/api/execution/gates/",
    "/api/execution/readiness",
    "/api/execution/readiness-preview",
    "/api/execution/readiness/actions",
    "/api/execution/readiness/blockers",
    "/api/execution/readiness/detail",
    "/api/execution/readiness/explain",
    "/api/execution/readiness/owners",
    "/api/execution/readiness/reviews",
    "/api/execution/readiness-forecast",
    "/api/execution/rollback-impact",
    "/api/execution/rollback-preview",
    "/api/execution/validation-evidence",
    "/api/execution/validation-preview",
    "/api/execution/verification-preview",
}

WAVE3_ROUTES = {
    "/api/execution/candidate-approval",
    "/api/execution/candidate-governance",
    "/api/execution/candidate-rehearsal",
    "/api/execution/candidate-workflow",
    "/api/execution/candidates",
    "/api/execution/candidates/",
    "/api/execution/candidates/explain",
    "/api/execution/candidates/readiness",
    "/api/execution/candidates/risks",
    "/api/execution/candidates/timeline",
}

CONVERGENCE_F_SIMULATION_ROUTES = {
    "/api/execution/blast-radius",
    "/api/execution/outcome-preview",
    "/api/execution/service-impact",
}

WAVE3_HELPERS = {
    "execution_candidates_response",
    "execution_candidate_detail_response",
    "execution_candidate_readiness_response",
    "execution_candidate_risks_response",
    "execution_candidate_explain_response",
    "execution_candidate_timeline_response",
    "execution_candidate_approval_response",
    "execution_candidate_governance_response",
    "execution_candidate_rehearsal_response",
    "execution_candidate_workflow_response",
    "p2_7_candidate_approval_detail",
    "p2_7_candidate_governance_detail",
    "p2_7_candidate_rehearsal_detail",
    "p2_7_candidate_workflow_detail",
}


class ConvergenceCWave3CandidateWorkflowLayerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ADMIN_API.read_text(encoding="utf-8")
        cls.routes = {
            match.group(1) or match.group(2)
            for match in ROUTE_RE.finditer(cls.source)
            if match.group(1) or match.group(2)
        }

    def test_admin_api_compiles(self):
        py_compile.compile(
            str(ADMIN_API),
            cfile="/private/tmp/convergence-c-wave3-v7-admin-api.pyc",
            doraise=True,
        )

    def test_candidate_workflow_route_set_is_exact_with_convergence_f_simulation_routes(self):
        execution_routes = {
            route for route in self.routes if route.startswith("/api/execution")
        }
        self.assertEqual(execution_routes, WAVE1_ROUTES | WAVE2_ROUTES | WAVE3_ROUTES | CONVERGENCE_F_SIMULATION_ROUTES)

    def test_candidate_routes_are_viewer_read_apis(self):
        for route in sorted(WAVE3_ROUTES - {"/api/execution/candidates/"}):
            with self.subTest(route=route):
                self.assertIn(f'"{route}": "viewer"', self.source)

    def test_candidate_workflow_reuses_existing_truth_sources(self):
        self.assertIn('"approval_center": "operator_approval_preview"', self.source)
        self.assertIn('"governance_preview": "operator_execution_governance_preview"', self.source)
        self.assertIn('"rehearsal_preview": "operator_execution_rehearsal_preview"', self.source)
        self.assertIn('"no_duplicate_approval_store": True', self.source)
        self.assertIn('"no_duplicate_governance_store": True', self.source)
        self.assertIn('"no_duplicate_rehearsal_store": True', self.source)

    def test_candidate_helpers_are_present_once(self):
        for helper in sorted(WAVE3_HELPERS):
            with self.subTest(helper=helper):
                self.assertEqual(self.source.count(f"def {helper}("), 1)

    def test_candidate_layer_remains_non_executable(self):
        self.assertIn('"execution_engine_implemented": False', self.source)
        self.assertIn('"runtime_hooks_implemented": False', self.source)
        self.assertIn('"execution_allowed_now": False', self.source)
        self.assertNotIn('"/api/execution/apply"', self.source)
        self.assertNotIn('"/api/execution/execute"', self.source)
        self.assertNotIn('"/api/execution/run"', self.source)


if __name__ == "__main__":
    unittest.main()
