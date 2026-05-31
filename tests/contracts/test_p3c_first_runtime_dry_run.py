import importlib.machinery
import os
import py_compile
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"

ROUTE_RE = re.compile(
    r"path\s*(?:==|!=)\s*[\"']([^\"']+)[\"']|path\.startswith\([\"']([^\"']+)[\"']\)"
)

REQUIRED_REPORT_FIELDS = {
    "dry_run_id",
    "timestamp",
    "scope",
    "input_refs",
    "input_hashes",
    "freshness",
    "decision",
    "reason",
    "evidence",
    "confidence",
    "verification_plan",
    "rollback_simulation",
    "expiry",
    "retention_class",
}

ALLOWED_OUTPUTS = {"NO_ACTION", "WOULD_MOVE", "WOULD_BLOCK", "WOULD_REVIEW", "WOULD_ROLLBACK"}
FORBIDDEN_OUTPUTS = {"MOVE", "EXECUTE", "APPLY", "ROUTE", "AUTOSWITCH_APPLY"}


class P3CFirstRuntimeDryRunTest(unittest.TestCase):
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
            cfile="/private/tmp/p3c-first-runtime-dry-run-v7-admin-api.pyc",
            doraise=True,
        )

    def test_read_api_is_viewer_get_only(self):
        self.assertIn("/api/runtime/dry-run/summary", self.routes)
        self.assertIn('"/api/runtime/dry-run/summary": "viewer"', self.source)
        self.assertIn('elif path == "/api/runtime/dry-run/summary":', self.source)
        self.assertNotIn('"/api/runtime/dry-run/apply"', self.source)
        self.assertNotIn('"/api/runtime/dry-run/execute"', self.source)
        self.assertNotIn('"/api/runtime/dry-run/route"', self.source)
        self.assertNotIn('"/api/runtime/dry-run/autoswitch-apply"', self.source)

    def test_model_helpers_are_present(self):
        for helper in (
            "runtime_dry_run_input_ref",
            "runtime_dry_run_input_adapters",
            "runtime_dry_run_evaluate",
            "runtime_dry_run_summary_response",
            "runtimeDryRunCardHtml",
            "openRuntimeDryRunDrawer",
            "renderOperatorRuntimeDryRun",
        ):
            with self.subTest(helper=helper):
                self.assertIn(helper, self.source)

    def test_forbidden_outputs_are_declared_impossible(self):
        self.assertIn("P3C_DRYRUN_ALLOWED_OUTPUTS", self.source)
        self.assertIn("P3C_DRYRUN_FORBIDDEN_OUTPUTS", self.source)
        for output in ALLOWED_OUTPUTS:
            with self.subTest(output=output):
                self.assertIn(f'"{output}"', self.source)
        for output in FORBIDDEN_OUTPUTS:
            with self.subTest(output=output):
                self.assertIn(f'"{output}"', self.source)
        self.assertIn("decision not in P3C_DRYRUN_ALLOWED_OUTPUTS", self.source)
        self.assertIn("decision in P3C_DRYRUN_FORBIDDEN_OUTPUTS", self.source)

    def test_dry_run_runtime_safety_flags_are_false(self):
        for fragment in (
            '"read_only": True',
            '"derived_only": True',
            '"preview_only": True',
            '"non_authoritative": True',
            '"execution_allowed_now": False',
            '"runtime_mutation_performed": False',
            '"routing_changed": False',
            '"users_moved": False',
            '"autoswitch_apply_run": False',
            '"policy_apply_run": False',
            '"killswitch_changed": False',
            '"trusted_ru_write_state": False',
            '"direct_ru_changed": False',
            '"execution_engine_implemented": False',
            '"runtime_hooks_with_authority": False',
            '"deploy_performed": False',
            '"systemd_changed": False',
            '"storage_backend": "derived_on_demand"',
            '"write_path": ""',
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.source)

    def test_runtime_dry_run_report_shape_and_fail_closed_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            audit = root / "audit"
            events = root / "events"
            state.mkdir()
            audit.mkdir()
            events.mkdir()
            (state / "users.registry").write_text("ip=10.7.0.2 current=vless enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=vless enabled=1 role=DEFAULT\n", encoding="utf-8")
            (state / "v7-state.json").write_text('{"users":[],"egress":{}}', encoding="utf-8")
            (state / "service-matrix.json").write_text('{"items":{"vless":{"services":{}}}}', encoding="utf-8")
            (state / "execution-contracts.json").write_text('{"contracts":[]}', encoding="utf-8")
            (state / "execution-events.jsonl").write_text("", encoding="utf-8")
            (state / "proposal-records.jsonl").write_text("", encoding="utf-8")
            (state / "trusted-ru-decision.state").write_text("overall=UNKNOWN\nroute_class_status=UNKNOWN\n", encoding="utf-8")
            (state / "runtime-trust.jsonl").write_text("", encoding="utf-8")
            (state / "release-trust.jsonl").write_text("", encoding="utf-8")
            (state / "closure-records.jsonl").write_text("", encoding="utf-8")
            (audit / "audit.jsonl").write_text("", encoding="utf-8")
            (events / "switch-history.jsonl").write_text("", encoding="utf-8")

            env = {
                "V7_STATE_DIR": str(state),
                "V7_AUDIT_FILE": str(audit / "audit.jsonl"),
                "V7_EVENT_DIR": str(events),
                "V7_SERVICE_MATRIX_FILE": str(state / "service-matrix.json"),
                "V7_TRUSTED_RU_DECISION_FILE": str(state / "trusted-ru-decision.state"),
                "V7_EXECUTION_CONTRACTS_FILE": str(state / "execution-contracts.json"),
                "V7_EXECUTION_EVENTS_FILE": str(state / "execution-events.jsonl"),
                "V7_PROPOSAL_STORE_FILE": str(state / "proposal-records.jsonl"),
                "V7_RUNTIME_TRUST_STORE_FILE": str(state / "runtime-trust.jsonl"),
                "V7_RELEASE_TRUST_STORE_FILE": str(state / "release-trust.jsonl"),
                "V7_CLOSURE_STORE_FILE": str(state / "closure-records.jsonl"),
                "V7_POLICY_FILE": str(root / "policy.json"),
                "V7_ORG_EGRESS_POLICY_FILE": str(root / "org-policy.json"),
                "V7_ROUTE_CLASSES_REG": str(root / "route-classes.registry"),
                "V7_REPO_ROOT": str(ROOT),
            }
            old = {key: os.environ.get(key) for key in env}
            os.environ.update(env)
            try:
                module = importlib.machinery.SourceFileLoader(
                    "v7_admin_api_p3c_runtime_dry_run",
                    str(ADMIN_API),
                ).load_module()
                report = module.runtime_dry_run_summary_response({})
            finally:
                for key, value in old.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value

        self.assertTrue(REQUIRED_REPORT_FIELDS <= set(report))
        self.assertIn(report["decision"], ALLOWED_OUTPUTS)
        self.assertNotIn(report["decision"], FORBIDDEN_OUTPUTS)
        self.assertTrue(report["read_only"])
        self.assertTrue(report["derived_only"])
        self.assertFalse(report["execution_allowed_now"])
        self.assertFalse(report["runtime_mutation_performed"])
        self.assertFalse(report["routing_changed"])
        self.assertFalse(report["users_moved"])
        self.assertFalse(report["autoswitch_apply_run"])
        self.assertFalse(report["runtime_hooks_with_authority"])
        self.assertEqual(report["storage_backend"], "derived_on_demand")
        self.assertEqual(report["write_path"], "")


if __name__ == "__main__":
    unittest.main()

