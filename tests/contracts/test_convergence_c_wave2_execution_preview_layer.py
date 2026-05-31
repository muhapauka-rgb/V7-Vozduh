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

CONVERGENCE_F_SIMULATION_ROUTES = {
    "/api/execution/blast-radius",
    "/api/execution/outcome-preview",
    "/api/execution/service-impact",
}

WAVE2_HELPERS = {
    "execution_contract_drafts_response",
    "execution_contract_draft_detail_response",
    "execution_validation_preview_response",
    "execution_verification_preview_response",
    "execution_rollback_preview_response",
    "execution_readiness_preview_response",
    "execution_gates_response",
    "execution_gate_detail_response",
    "execution_readiness_response",
    "execution_readiness_detail_response",
    "execution_readiness_explain_response",
    "execution_readiness_owners_response",
    "execution_readiness_actions_response",
    "execution_readiness_blockers_response",
    "execution_readiness_reviews_response",
    "execution_validation_evidence_response",
    "execution_readiness_forecast_response",
    "execution_rollback_impact_response",
}


class ConvergenceCWave2ExecutionPreviewLayerTest(unittest.TestCase):
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
            cfile="/private/tmp/convergence-c-wave2-v7-admin-api.pyc",
            doraise=True,
        )

    def test_wave1_and_wave2_execution_routes_are_preserved(self):
        execution_routes = {
            route for route in self.routes if route.startswith("/api/execution")
        }
        self.assertTrue((WAVE1_ROUTES | WAVE2_ROUTES) <= execution_routes)

    def test_convergence_f_simulation_routes_are_exposed_as_preview_read_apis(self):
        self.assertTrue(CONVERGENCE_F_SIMULATION_ROUTES <= self.routes)
        for route in sorted(CONVERGENCE_F_SIMULATION_ROUTES):
            with self.subTest(route=route):
                self.assertIn(f'"{route}": "viewer"', self.source)

    def test_wave2_routes_are_viewer_read_apis(self):
        for route in sorted(WAVE2_ROUTES - {"/api/execution/contracts/draft/", "/api/execution/gates/"}):
            with self.subTest(route=route):
                self.assertIn(f'"{route}": "viewer"', self.source)

    def test_wave2_helpers_are_present(self):
        for helper in sorted(WAVE2_HELPERS):
            with self.subTest(helper=helper):
                self.assertIn(f"def {helper}(", self.source)

    def test_preview_layer_remains_non_executable(self):
        self.assertIn('"execution_engine_present": False', self.source)
        self.assertIn('"runtime_hooks_present": False', self.source)
        self.assertIn('"execution_allowed_now": False', self.source)
        self.assertNotIn('"/api/execution/apply"', self.source)
        self.assertNotIn('"/api/execution/execute"', self.source)
        self.assertNotIn('"/api/execution/run"', self.source)


if __name__ == "__main__":
    unittest.main()
