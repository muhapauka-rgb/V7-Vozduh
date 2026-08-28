import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
