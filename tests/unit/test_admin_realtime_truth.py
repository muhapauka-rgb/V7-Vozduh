import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_admin_api():
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_realtime_truth", str(ADMIN_API))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class AdminRealtimeTruthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin = load_admin_api()

    def test_live_operational_truth_reads_current_registry_and_matrix_without_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "users.registry").write_text(
                "ip=10.7.0.125 current=awg0 table=1123 enabled=1\n",
                encoding="utf-8",
            )
            (state / "egress.registry").write_text(
                "id=vless interface=vless enabled=1\n"
                "id=awg0 interface=awg0 enabled=1\n",
                encoding="utf-8",
            )
            matrix = state / "service-matrix.json"
            matrix.write_text(json.dumps({
                "items": {
                    "vless": {"services": {"telegram": {"ok": False, "status": "FAIL"}}},
                    "awg0": {"services": {"telegram": {"ok": True, "status": "OK"}}},
                }
            }), encoding="utf-8")
            previous_state, previous_matrix = self.admin.STATE_DIR, self.admin.SERVICE_MATRIX_FILE
            self.addCleanup(setattr, self.admin, "STATE_DIR", previous_state)
            self.addCleanup(setattr, self.admin, "SERVICE_MATRIX_FILE", previous_matrix)
            self.admin.STATE_DIR = state
            self.admin.SERVICE_MATRIX_FILE = matrix

            payload = self.admin.live_operational_truth()

        self.assertTrue(payload["read_only"])
        self.assertEqual(payload["canonical_sources"]["assignment"], "users.registry")
        self.assertEqual(payload["registries"]["users"][0]["current"], "awg0")
        self.assertEqual(payload["channel_user_counts"], {"awg0": 1})
        self.assertFalse(payload["service_matrix"]["items"]["vless"]["services"]["telegram"]["ok"])

    def test_admin_page_uses_lightweight_live_status_polling(self):
        page = self.admin.html_page_v2()
        self.assertIn("/api/live-status", page)
        self.assertIn("liveOperationalTruthTimer = window.setInterval", page)
        self.assertIn("refreshLiveOperationalTruth('timer'), 500", page)
        self.assertIn("mergeLiveOperationalTruthIntoOverview", page)

    def test_new_profile_binds_requested_configured_egress_without_health_query(self):
        with mock.patch.object(self.admin, "egress_exists", return_value=True) as exists:
            binding = self.admin.identity_egress_issuance_binding("vless")

        self.assertTrue(binding["ok"])
        self.assertEqual(binding["selected_egress"], "vless")
        self.assertFalse(binding["health_checked"])
        self.assertEqual(binding["owner"], "existing egress.registry")
        exists.assert_called_once_with("vless", enabled_only=True)

    def test_profile_issue_paths_do_not_run_health_admission_before_provisioning(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        quick = source[source.index("def identity_issue_config_quick"):source.index("def pending_profile_public_key")]
        device = source[source.index("def identity_issue_device"):source.index("def identity_issue_config_quick")]
        self.assertIn("binding = identity_egress_issuance_binding(requested_egress)", quick)
        self.assertIn("binding = identity_egress_issuance_binding(requested_egress)", device)
        self.assertNotIn("identity_egress_admission", quick)
        self.assertNotIn("identity_egress_admission", device)

    def test_profile_issue_removes_obsolete_admission_and_returns_result_before_overview(self):
        autoswitch = (ROOT / "tools" / "v7-users-autoswitch").read_text(encoding="utf-8")
        self.assertNotIn("ordinary_new_user_admission_only", autoswitch)
        self.assertNotIn("--new-user-admission", autoswitch)

        source = ADMIN_API.read_text(encoding="utf-8")
        handler = source[
            source.index('elif path == "/api/actions/identity-device-issue"'):
            source.index('elif path == "/api/actions/pending-profile-create"')
        ]
        self.assertIn("self.send_json(payload, status=status)", handler)
        self.assertNotIn('"overview": overview()', handler)
        page = self.admin.html_page_v2()
        self.assertIn("Его здоровье не проверяется в момент выдачи", page)
        self.assertIn("Профиль не выдан", page)

    def test_completed_execution_control_does_not_freeze_profile_issuance(self):
        with tempfile.TemporaryDirectory() as tmp:
            safe_mode = Path(tmp) / "safe-mode.json"
            control = self.admin.operator_execution.build_autonomous_execution_control_state(
                True,
                actor="governed-execution-finalizer",
                reason="GOVERNED_TRANSACTION_COMPLETED",
            )
            self.admin.write_json_atomic(safe_mode, control)
            previous = self.admin.SAFE_MODE_FILE
            self.addCleanup(setattr, self.admin, "SAFE_MODE_FILE", previous)
            self.admin.SAFE_MODE_FILE = safe_mode

            state = self.admin.admin_safe_mode_state()
            self.assertTrue(state["execution_control_enabled"])
            self.assertFalse(state["enabled"])
            self.assertFalse(self.admin.admin_safe_mode_enabled())

            enabled = self.admin.set_admin_safe_mode("admin", True, "maintenance")
            self.assertTrue(enabled["enabled"])
            disabled = self.admin.set_admin_safe_mode("admin", False, "done")
            self.assertFalse(disabled["enabled"])


if __name__ == "__main__":
    unittest.main()
