import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-route-movement-preview"
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "route_movement"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_route_movement_preview", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class RouteMovementPreviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.preview = load_tool_module()

    def users(self, name="users.registry"):
        return FIXTURE_DIR / name

    def egress(self, name="egress.registry"):
        return FIXTURE_DIR / name

    def test_user_switch_one_user_plan_has_no_mutation_and_rollback(self):
        plan = self.preview.user_switch_preview(self.users(), self.egress(), "10.7.0.10", "awg3")
        self.assertFalse(plan["mutation"])
        self.assertFalse(plan["runtime_commands_executed"])
        self.assertEqual(plan["blast_radius"], "one_user")
        self.assertEqual(plan["from_egress"], "vless")
        self.assertEqual(plan["to_egress"], "awg3")
        self.assertEqual(plan["target_interface"], "awg3")
        self.assertEqual(
            plan["routes_would_change"],
            [
                {
                    "type": "route_replace_default",
                    "user": "10.7.0.10",
                    "table": "110",
                    "dev": "awg3",
                    "command": "ip route replace default dev awg3 table 110",
                }
            ],
        )
        self.assertEqual(plan["ip_rules_would_change"], [])
        self.assertEqual(plan["rollback"]["command"], "v7-user-switch 10.7.0.10 vless")
        self.assertFalse(plan["errors"])

    def test_user_switch_user_not_found(self):
        plan = self.preview.user_switch_preview(self.users(), self.egress(), "10.7.0.99", "awg3")
        self.assertIn({"code": "user_not_found", "detail": "10.7.0.99"}, plan["errors"])
        self.assertFalse(plan["routes_would_change"])

    def test_user_switch_target_egress_missing(self):
        plan = self.preview.user_switch_preview(self.users(), self.egress(), "10.7.0.10", "missing")
        self.assertIn({"code": "target_egress_missing", "detail": "missing"}, plan["errors"])

    def test_user_switch_target_egress_disabled(self):
        plan = self.preview.user_switch_preview(self.users(), self.egress(), "10.7.0.10", "disabled")
        self.assertIn({"code": "target_egress_disabled", "detail": "disabled"}, plan["errors"])

    def test_user_switch_same_egress_noop(self):
        plan = self.preview.user_switch_preview(self.users(), self.egress(), "10.7.0.10", "vless")
        self.assertTrue(plan["no_op"])
        self.assertEqual(plan["rollback"]["type"], "none")
        self.assertFalse(plan["routes_would_change"])
        self.assertFalse(plan["files_would_change"])

    def test_user_switch_duplicate_user_forbidden(self):
        plan = self.preview.user_switch_preview(self.users("users_duplicate.registry"), self.egress(), "10.7.0.10", "vless")
        self.assertIn({"code": "duplicate_user", "detail": "10.7.0.10", "count": 2}, plan["errors"])

    def test_routing_sync_plans_enabled_users_only(self):
        plan = self.preview.routing_sync_preview(self.users(), self.egress())
        self.assertFalse(plan["mutation"])
        self.assertFalse(plan["runtime_commands_executed"])
        self.assertEqual(plan["blast_radius"], "all_enabled_users_in_registry")
        self.assertEqual(len(plan["routes_would_change"]), 2)
        self.assertEqual(len(plan["ip_rules_would_change"]), 4)
        commands = [row["command"] for row in plan["routes_would_change"]]
        self.assertEqual(
            commands,
            [
                "ip route replace default dev tun0 table 110",
                "ip route replace default dev awg3 table 111",
            ],
        )
        disabled = [row for row in plan["users"] if row["ip"] == "10.7.0.12"][0]
        self.assertEqual(disabled["action"], "skip_disabled")

    def test_routing_sync_duplicate_users_are_errors(self):
        plan = self.preview.routing_sync_preview(self.users("users_duplicate.registry"), self.egress())
        self.assertIn({"code": "duplicate_user", "detail": "10.7.0.10", "count": 2}, plan["errors"])

    def test_routing_sync_invalid_and_missing_cases(self):
        plan = self.preview.routing_sync_preview(self.users("users_invalid.registry"), self.egress())
        error_codes = {(err.get("user"), err["code"]) for err in plan["errors"]}
        self.assertIn(("10.7.0.13", "egress_missing"), error_codes)
        self.assertIn(("10.7.0.14", "invalid_table"), error_codes)
        self.assertIn(("192.168.1.10", "invalid_user_ip"), error_codes)
        self.assertFalse(plan["routes_would_change"])

    def test_routing_sync_noop_when_no_enabled_users(self):
        plan = self.preview.routing_sync_preview(self.users("users_disabled_only.registry"), self.egress())
        self.assertTrue(plan["no_op"])
        self.assertEqual(plan["blast_radius"], "none")
        self.assertFalse(plan["routes_would_change"])
        self.assertFalse(plan["ip_rules_would_change"])

    def test_cli_outputs_json_and_does_not_call_runtime_commands(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "user-switch",
                "--users-registry",
                str(self.users()),
                "--egress-registry",
                str(self.egress()),
                "--user-ip",
                "10.7.0.10",
                "--to-egress",
                "awg3",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["mutation"])
        self.assertFalse(payload["runtime_commands_executed"])


if __name__ == "__main__":
    unittest.main()
