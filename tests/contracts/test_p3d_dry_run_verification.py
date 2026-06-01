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

VERIFICATION_STATES = {"VERIFIED_MATCH", "VERIFIED_MISMATCH", "INCONCLUSIVE", "STALE", "NOT_VERIFIED"}
CONFIDENCE_STATES = {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}
ALLOWED_OUTPUTS = {"NO_ACTION", "WOULD_MOVE", "WOULD_BLOCK", "WOULD_REVIEW", "WOULD_ROLLBACK"}


def load_admin_api_with_temp_state():
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
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
            "v7_admin_api_p3d_dry_run_verification",
            str(ADMIN_API),
        ).load_module()
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    return tmp, module


class P3DDryRunVerificationTest(unittest.TestCase):
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
            cfile="/private/tmp/p3d-dry-run-verification-v7-admin-api.pyc",
            doraise=True,
        )

    def test_verification_read_api_is_viewer_get_only(self):
        self.assertIn("/api/runtime/dry-run/verification", self.routes)
        self.assertIn('"/api/runtime/dry-run/verification": "viewer"', self.source)
        self.assertIn('elif path == "/api/runtime/dry-run/verification":', self.source)
        for fragment in (
            '"/api/runtime/dry-run/verification/apply"',
            '"/api/runtime/dry-run/verification/execute"',
            '"/api/runtime/dry-run/verification/rollback"',
            '"/api/runtime/dry-run/verification/autoswitch-apply"',
        ):
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, self.source)

    def test_verification_helpers_and_admin_mapping_are_present(self):
        for helper in (
            "runtime_dry_run_prediction_from_query",
            "runtime_dry_run_observed_reality",
            "runtime_dry_run_comparison",
            "runtime_dry_run_verification_confidence",
            "runtime_dry_run_verification_response",
            "runtimeDryRunVerificationCardHtml",
            "openRuntimeDryRunVerificationDrawer",
            "renderOperatorRuntimeDryRunVerification",
        ):
            with self.subTest(helper=helper):
                self.assertIn(helper, self.source)

    def test_verification_report_shape_and_match(self):
        tmp, module = load_admin_api_with_temp_state()
        self.addCleanup(tmp.cleanup)
        prediction = module.runtime_dry_run_summary_response({})
        report = module.runtime_dry_run_verification_response({
            "prediction_decision": [prediction["decision"]],
            "prediction_timestamp": [prediction["timestamp"]],
            "prediction_confidence": [prediction["confidence"]],
            "dry_run_id": [prediction["dry_run_id"]],
        })
        self.assertEqual(report["comparison"]["state"], "VERIFIED_MATCH")
        self.assertIn(report["confidence"]["state"], CONFIDENCE_STATES)
        self.assertIn(report["prediction"]["decision"], ALLOWED_OUTPUTS)
        self.assertIn(report["observed_reality"]["observed_outcome"], ALLOWED_OUTPUTS)
        self.assertTrue(report["read_only"])
        self.assertTrue(report["derived_only"])
        self.assertFalse(report["execution_allowed_now"])
        self.assertEqual(report["storage_backend"], "derived_on_demand")
        self.assertEqual(report["write_path"], "")

    def test_mismatch_and_invalid_prediction_are_safe(self):
        tmp, module = load_admin_api_with_temp_state()
        self.addCleanup(tmp.cleanup)
        mismatch = module.runtime_dry_run_verification_response({
            "prediction_decision": ["WOULD_MOVE"],
            "prediction_timestamp": [module.now_iso()],
            "prediction_confidence": ["HIGH"],
        })
        self.assertIn(mismatch["comparison"]["state"], {"VERIFIED_MISMATCH", "VERIFIED_MATCH"})
        invalid = module.runtime_dry_run_verification_response({
            "prediction_decision": ["APPLY"],
            "prediction_timestamp": [module.now_iso()],
        })
        self.assertEqual(invalid["comparison"]["state"], "INCONCLUSIVE")
        self.assertFalse(invalid["runtime_mutation_performed"])
        self.assertFalse(invalid["routing_changed"])
        self.assertFalse(invalid["users_moved"])
        self.assertFalse(invalid["autoswitch_apply_run"])
        self.assertFalse(invalid["rollback_executed"])
        self.assertFalse(invalid["runtime_hooks_with_authority"])

    def test_safety_and_state_sets_are_declared(self):
        for state in VERIFICATION_STATES:
            with self.subTest(state=state):
                self.assertIn(f'"{state}"', self.source)
        for state in CONFIDENCE_STATES:
            with self.subTest(state=state):
                self.assertIn(f'"{state}"', self.source)
        for fragment in (
            '"runtime_mutation_performed": False',
            '"routing_changed": False',
            '"users_moved": False',
            '"autoswitch_apply_run": False',
            '"policy_apply_run": False',
            '"rollback_executed": False',
            '"execution_engine_implemented": False',
            '"runtime_hooks_with_authority": False',
            '"deploy_performed": False',
            '"systemd_changed": False',
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.source)


if __name__ == "__main__":
    unittest.main()

