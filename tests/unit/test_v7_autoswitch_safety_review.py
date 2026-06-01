import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-autoswitch-safety-review"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_autoswitch_safety_review", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class V7AutoswitchSafetyReviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def test_kv_registry_counts_enabled_egress(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            egress_path = root / "egress.registry"
            users_path = root / "users.registry"
            egress_path.write_text(
                "id=awg0 protocol=amneziawg enabled=1 state=enabled\n"
                "id=vless protocol=vless enabled=0 state=disabled\n"
                "id=awg3 protocol=amneziawg enabled=true state=enabled\n",
                encoding="utf-8",
            )
            users_path.write_text(
                "ip=10.7.0.11 current=awg0 enabled=1\n"
                "ip=10.7.0.12 current=awg3 enabled=true\n",
                encoding="utf-8",
            )

            egress, egress_status = self.tool.read_registry(egress_path)
            users, users_status = self.tool.read_registry(users_path)
            findings = []
            result = self.tool.evaluate_capacity(
                users,
                egress,
                {
                    "max_planned_per_run": 1,
                    "max_failover_per_run": 3,
                    "max_reconnect_per_run": 1,
                },
                findings,
            )

        self.assertEqual(egress_status, "ok")
        self.assertEqual(users_status, "ok")
        self.assertEqual(result["users"], 2)
        self.assertEqual(result["enabled_egress"], 2)
        self.assertEqual(result["enabled_egress_ids"], ["awg0", "awg3"])
        self.assertFalse([item for item in findings if item["severity"] == "critical"])

    def test_legacy_two_column_registry_still_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            egress_path = root / "egress.registry"
            users_path = root / "users.registry"
            egress_path.write_text("awg0 enabled\n", encoding="utf-8")
            users_path.write_text("10.7.0.11 active\n", encoding="utf-8")
            egress, _ = self.tool.read_registry(egress_path)
            users, _ = self.tool.read_registry(users_path)
            findings = []
            result = self.tool.evaluate_capacity(
                users,
                egress,
                {
                    "max_planned_per_run": 1,
                    "max_failover_per_run": 3,
                    "max_reconnect_per_run": 1,
                },
                findings,
            )

        self.assertEqual(result["users"], 1)
        self.assertEqual(result["enabled_egress"], 1)
        self.assertEqual(result["enabled_egress_ids"], ["awg0"])
        self.assertFalse([item for item in findings if item["severity"] == "critical"])


if __name__ == "__main__":
    unittest.main()
