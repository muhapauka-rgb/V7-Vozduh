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

REQUIRED_REPORTS = {
    "CONVERGENCE_E_BASELINE_LOCK.md",
    "CONVERGENCE_E_WAVE1_RUNTIME_API_VERIFICATION.md",
    "CONVERGENCE_E_WAVE2_PREVIEW_VERIFICATION.md",
    "CONVERGENCE_E_WAVE3_CANDIDATE_VERIFICATION.md",
    "CONVERGENCE_E_WAVE4_UI_VERIFICATION.md",
    "CONVERGENCE_E_WAVE5_TESTS_DOCS.md",
    "CONVERGENCE_E_DEFERRED_API_DECISION.md",
    "CONVERGENCE_E_LOG_RETENTION_CHECK.md",
    "CONVERGENCE_E_TEST_RESULTS.md",
    "CONVERGENCE_E_CERTIFICATION.md",
    "BLOCK_CONVERGENCE_E_FULL_CONVERGENCE_INTEGRATION_REPORT.md",
}


class ConvergenceEFullConvergencePackageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ADMIN_API.read_text(encoding="utf-8")
        cls.routes = {
            match.group(1) or match.group(2)
            for match in ROUTE_RE.finditer(cls.source)
            if match.group(1) or match.group(2)
        }

    def test_complete_wave_route_inventory_is_present_with_resolved_simulation_routes(self):
        execution_routes = {
            route for route in self.routes if route.startswith("/api/execution")
        }
        self.assertEqual(execution_routes, WAVE1_ROUTES | WAVE2_ROUTES | WAVE3_ROUTES | CONVERGENCE_F_SIMULATION_ROUTES)
        for route in sorted(CONVERGENCE_F_SIMULATION_ROUTES):
            with self.subTest(route=route):
                self.assertIn(f'"{route}": "viewer"', self.source)

    def test_execution_family_has_no_mutating_execution_endpoints(self):
        forbidden_fragments = (
            '"/api/execution/apply"',
            '"/api/execution/execute"',
            '"/api/execution/run"',
            '"/api/execution/route-apply"',
            '"/api/execution/autoswitch-apply"',
        )
        for fragment in forbidden_fragments:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, self.source)

    def test_truth_sources_are_reused_not_recreated(self):
        self.assertIn("EXECUTION_CONTRACTS_FILE", self.source)
        self.assertIn("EXECUTION_EVENTS_FILE", self.source)
        self.assertIn('"approval_center": "operator_approval_preview"', self.source)
        self.assertIn('"governance_preview": "operator_execution_governance_preview"', self.source)
        self.assertIn('"rehearsal_preview": "operator_execution_rehearsal_preview"', self.source)
        self.assertIn('"no_duplicate_approval_store": True', self.source)
        self.assertIn('"no_duplicate_governance_store": True', self.source)
        self.assertIn('"no_duplicate_rehearsal_store": True', self.source)

    def test_ui_uses_existing_admin_surfaces(self):
        tabs = set(re.findall(r'data-tab="([^"]+)"', self.source))
        self.assertFalse({"execution", "candidate", "approval", "governance", "rehearsal"} & tabs)
        self.assertEqual(self.source.count("async function openExecutionSummaryDrawer("), 1)
        self.assertEqual(self.source.count("async function openExecutionCandidateDrawer("), 1)
        self.assertIn('id="operatorCandidateWorkflow"', self.source)
        self.assertIn("Approval Center reused", self.source)

    def test_retention_context_is_visible_for_convergence_logs(self):
        self.assertIn("HARDENING_RETENTION_DAYS", self.source)
        self.assertIn("def read_jsonl_records(", self.source)
        self.assertIn("def execution_candidate_timeline_response(", self.source)
        self.assertNotIn("CANDIDATE_QUEUE_FILE", self.source)
        self.assertNotIn("APPROVAL_QUEUE_FILE", self.source)

    def test_required_convergence_e_reports_exist(self):
        missing = sorted(name for name in REQUIRED_REPORTS if not (ROOT / name).exists())
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
