import py_compile
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"

ROUTE_RE = re.compile(
    r"path\s*(?:==|!=)\s*[\"']([^\"']+)[\"']|path\.startswith\([\"']([^\"']+)[\"']\)"
)

RUNTIME_EXECUTION_ROUTES = {
    "/api/execution/contracts",
    "/api/execution/contracts/",
    "/api/execution/events",
    "/api/execution/explain",
    "/api/execution/rollback",
    "/api/execution/summary",
    "/api/execution/timeline",
    "/api/execution/verification",
}

RUNTIME_ROLE_ENTRIES = {
    "/api/execution/summary",
    "/api/execution/contracts",
    "/api/execution/timeline",
    "/api/execution/events",
    "/api/execution/verification",
    "/api/execution/rollback",
    "/api/execution/explain",
}

CONVERGENCE_F_SIMULATION_ROUTES = {
    "/api/execution/blast-radius",
    "/api/execution/outcome-preview",
    "/api/execution/service-impact",
}

RUNTIME_HELPERS = {
    "execution_contract_by_id",
    "execution_contract_detail_response",
    "execution_contract_store_rows",
    "execution_contract_summary_item",
    "execution_contracts",
    "execution_contracts_response",
    "execution_events",
    "execution_events_for_contract",
    "execution_events_response",
    "execution_explain_response",
    "execution_rollback_response",
    "execution_rollback_summary",
    "execution_store_consistency",
    "execution_summary_response",
    "execution_timeline_items",
    "execution_timeline_response",
    "execution_verification_response",
    "execution_verification_summary",
    "normalize_execution_contract",
    "normalize_execution_event",
    "safe_execution_id",
}


class ConvergenceCRuntimeReadApiPreservationTest(unittest.TestCase):
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
            cfile="/private/tmp/convergence-c-v7-admin-api.pyc",
            doraise=True,
        )

    def test_runtime_execution_routes_are_preserved(self):
        execution_routes = {
            route for route in self.routes if route.startswith("/api/execution")
        }
        self.assertTrue(RUNTIME_EXECUTION_ROUTES <= execution_routes)

    def test_convergence_f_simulation_routes_are_resolved_as_read_only(self):
        self.assertTrue(CONVERGENCE_F_SIMULATION_ROUTES <= self.routes)
        for route in sorted(CONVERGENCE_F_SIMULATION_ROUTES):
            with self.subTest(route=route):
                self.assertIn(f'"{route}": "viewer"', self.source)

    def test_runtime_execution_routes_remain_viewer_read_apis(self):
        for route in sorted(RUNTIME_ROLE_ENTRIES):
            with self.subTest(route=route):
                self.assertIn(f'"{route}": "viewer"', self.source)

    def test_runtime_read_model_helpers_are_preserved(self):
        for helper in sorted(RUNTIME_HELPERS):
            with self.subTest(helper=helper):
                self.assertIn(f"def {helper}(", self.source)

    def test_preserved_api_remains_non_executable(self):
        self.assertIn('"execution_engine_present": False', self.source)
        self.assertIn('"execution_allowed_now": False', self.source)
        self.assertNotIn('"/api/execution/apply"', self.source)
        self.assertNotIn('"/api/execution/execute"', self.source)
        self.assertNotIn('"/api/execution/run"', self.source)


if __name__ == "__main__":
    unittest.main()
