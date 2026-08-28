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

    def test_new_profile_uses_existing_planner_admission_not_registry_order(self):
        planner_result = {
            "status": "ADMITTED",
            "ok": True,
            "selected_egress": "awg0",
            "candidates": [
                {"egress": "vless", "eligible": False, "blocked": ["severity_FAIL"]},
                {"egress": "awg0", "eligible": True, "blocked": []},
            ],
        }
        with mock.patch.object(self.admin, "run_json_command", return_value={
            "rc": 0, "json": planner_result, "parse_error": "",
        }) as command:
            admission = self.admin.identity_egress_admission("vless")

        self.assertTrue(admission["ok"])
        self.assertEqual(admission["selected_egress"], "awg0")
        self.assertFalse(admission["requested_egress_admitted"])
        self.assertEqual(admission["requested_egress_blockers"], ["severity_FAIL"])
        self.assertEqual(command.call_args.args[0], ["v7-users-autoswitch", "--new-user-admission"])

    def test_profile_issue_paths_use_admission_before_provisioning(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        quick = source[source.index("def identity_issue_config_quick"):source.index("def pending_profile_public_key")]
        device = source[source.index("def identity_issue_device"):source.index("def identity_issue_config_quick")]
        self.assertIn("admission = identity_egress_admission(requested_egress)", quick)
        self.assertIn("admission = identity_egress_admission(requested_egress)", device)
        self.assertNotIn("or default_egress_id()", quick)
        self.assertNotIn("or default_egress_id()", device)

    def test_profile_issue_uses_compact_admission_and_returns_result_before_overview(self):
        autoswitch = (ROOT / "tools" / "v7-users-autoswitch").read_text(encoding="utf-8")
        admission = autoswitch[
            autoswitch.index("def ordinary_new_user_admission_only"):
            autoswitch.index("def ct_m0f_precomputed_target_diagnostic_from_file")
        ]
        self.assertIn("def admission_candidate", admission)
        self.assertNotIn("planner._candidate_json(candidate)", admission)
        self.assertIn('"blocked": list(candidate.blocked)', admission)

        source = ADMIN_API.read_text(encoding="utf-8")
        handler = source[
            source.index('elif path == "/api/actions/identity-device-issue"'):
            source.index('elif path == "/api/actions/pending-profile-create"')
        ]
        self.assertIn("self.send_json(payload, status=status)", handler)
        self.assertNotIn('"overview": overview()', handler)
        page = self.admin.html_page_v2()
        self.assertIn("Это предпочтение, а не принудительное назначение", page)
        self.assertIn("Профиль не выдан", page)


if __name__ == "__main__":
    unittest.main()
