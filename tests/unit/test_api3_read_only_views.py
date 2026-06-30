import importlib.machinery
import importlib.util
import inspect
import json
import tempfile
import unittest
from pathlib import Path

from admin_core import operator_views, route_views, service_views, summary_builders


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_admin_api():
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_api3", str(ADMIN_API))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class Api3ReadOnlyViewsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin = load_admin_api()

    def test_service_matrix_view_parity(self):
        matrix = {
            "services": {
                "telegram": {"ok": True, "status": "OK", "first_byte_sec": "0.4"},
                "google": {"ok": True, "status": "OK", "first_byte_sec": "0.2"},
                "unknown": {"ok": True},
            }
        }
        expected = service_views.normalize_service_matrix_row(
            matrix,
            known_services=self.admin.KNOWN_SERVICES,
            route_class_service_map=self.admin.ROUTE_CLASS_SERVICE_MAP,
            hard_statuses=self.admin.TELEGRAM_HARD_STATUSES,
            soft_statuses=self.admin.TELEGRAM_SOFT_STATUSES,
        )
        self.assertEqual(self.admin.normalize_service_matrix_row(matrix), expected)
        self.assertEqual(
            self.admin.service_matrix_telegram_state(matrix),
            service_views.service_matrix_telegram_state(
                matrix,
                hard_statuses=self.admin.TELEGRAM_HARD_STATUSES,
                soft_statuses=self.admin.TELEGRAM_SOFT_STATUSES,
            ),
        )
        self.assertNotIn("unknown", expected["services"])

    def test_service_recommendation_view_parity(self):
        users = [{"ip": "10.7.0.2", "current": "slow", "enabled": "1"}]
        matrix = {
            "items": {
                "slow": {"services": {"telegram": {"ok": False, "reason": "down"}}},
                "fast": {"services": {"telegram": {"ok": True, "first_byte_sec": 0.1}}},
            }
        }
        prefs = {"enabled": True, "users": {"10.7.0.2": {"schema_version": 2, "services": ["telegram"]}}}
        expected = service_views.service_recommendations(
            users,
            matrix,
            prefs,
            known_services=self.admin.KNOWN_SERVICES,
            default_user_priority_services=self.admin.DEFAULT_USER_PRIORITY_SERVICES,
        )
        self.assertEqual(self.admin.service_recommendations(users, matrix, prefs), expected)
        self.assertEqual(expected["user_required_routes"][0]["recommended_egress"], "fast")

    def test_route_view_parity(self):
        probe = "000 remote=1.2.3.4 err=timeout"
        self.assertEqual(self.admin.trusted_ru_parse_probe(probe, "direct_http"), route_views.trusted_ru_parse_probe(probe, "direct_http"))
        row = {"direct_http": "000", "direct_openssl": "FAIL", "vless_http": "000", "awg_http": "000"}
        self.assertEqual(self.admin.trusted_ru_domain_status(row), route_views.trusted_ru_domain_status(row))
        raw = {
            "updated": "2026-01-01T00:00:00+00:00",
            "count": "1",
            "item_1_domain": "www.gosuslugi.ru",
            "item_1_decision": "TRUSTED",
        }
        expected = route_views.trusted_ru_decision_summary(raw, decision_file="decision.state", age_func=lambda _: 123)
        self.assertEqual(expected["items"][0]["domain"], "www.gosuslugi.ru")
        self.assertEqual(expected["age_sec"], 123)

    def test_summary_builders_parity_and_bounded_jsonl(self):
        params = {"limit": ["2"], "cursor": ["1"], "q": ["abc"]}
        self.assertEqual(self.admin.query_value(params, "q"), summary_builders.query_value(params, "q"))
        self.assertEqual(self.admin.pagination_from_query(params), summary_builders.pagination_from_query(params))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text(
                "\n".join([
                    json.dumps({"id": 1, "token": "secret"}),
                    "broken",
                    json.dumps({"id": 2}),
                    json.dumps({"id": 3}),
                ]),
                encoding="utf-8",
            )
            rows = self.admin.read_jsonl_records(path, limit=2)
        self.assertEqual([row["id"] for row in rows], [2, 3])

    def test_operator_facade_reuses_existing_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = operator_views.operator_view_model(repo_root=root, state_dir=root / "state", event_dir=root / "events")
        self.assertFalse(model["overview"]["execution_allowed_now"])
        self.assertEqual(model["targets"]["freshness"]["state"], "MISSING")

    def test_schema_contracts_and_no_mutation_surface(self):
        contracts = summary_builders.api3_schema_contracts()
        self.assertIn("overview", contracts)
        self.assertIn("operator_summary", contracts)
        self.assertTrue(all(contract["read_only"] for contract in contracts.values()))
        forbidden = ("subprocess", "run_action", "write_json_atomic", "write_text_atomic", "audit_admin", "append_jsonl")
        for module in (operator_views, service_views, route_views, summary_builders):
            source = inspect.getsource(module)
            for token in forbidden:
                self.assertNotIn(token, source)

    def test_autoswitch_read_only_plan_uses_pre_planner_refresh(self):
        cmd, target, source = self.admin.autoswitch_read_only_plan_command("awg0")
        self.assertEqual(target, "awg0")
        self.assertEqual(source, "")
        self.assertEqual(cmd[:5], [
            "v7-users-autoswitch",
            "--pre-planner-refresh",
            "write",
            "--pre-planner-refresh-command",
            "v7-intelligence-snapshot-refresh",
        ])
        self.assertIn("--pretty", cmd)
        self.assertEqual(cmd[-2:], ["--target-egress", "awg0"])

    def test_autoswitch_read_only_plan_supports_source_and_target_scope(self):
        cmd, target, source = self.admin.autoswitch_read_only_plan_command("vless", "awg0")
        self.assertEqual(target, "vless")
        self.assertEqual(source, "awg0")
        self.assertIn("--source-egress", cmd)
        self.assertIn("awg0", cmd)
        self.assertEqual(cmd[-2:], ["--target-egress", "vless"])

    def test_autoswitch_plan_state_reuses_refresh_command(self):
        calls = []
        original = self.admin.run_json_command
        try:
            def fake_run_json_command(cmd, timeout=45, max_output=12000):
                calls.append((cmd, timeout, max_output))
                return {
                    "cmd": cmd,
                    "rc": 0,
                    "json": {"ok": True, "summary": {"proposal_moves_total": 2, "execution_blocked": True}},
                    "output": "{}",
                    "parse_error": "",
                    "output_truncated": False,
                }

            self.admin.run_json_command = fake_run_json_command
            result = self.admin.autoswitch_plan_state("vless", "awg0")
        finally:
            self.admin.run_json_command = original

        self.assertEqual(result["rc"], 0)
        self.assertEqual(result["plan"]["ok"], True)
        self.assertEqual(result["target_egress"], "vless")
        self.assertEqual(result["source_egress"], "awg0")
        self.assertEqual(result["proposal_count"], 2)
        self.assertTrue(result["execution_blocked"])
        self.assertEqual(result["cmd"], calls[0][0])
        self.assertIn("--pre-planner-refresh", calls[0][0])
        self.assertIn("write", calls[0][0])
        self.assertEqual(calls[0][1], 45)

    def test_run_json_command_parses_full_stdout_and_truncates_display_only(self):
        original = self.admin.subprocess.run

        class FakeProc:
            returncode = 0
            stdout = json.dumps({"ok": True, "payload": "x" * 20000})

        try:
            self.admin.subprocess.run = lambda *args, **kwargs: FakeProc()
            result = self.admin.run_json_command(["fake"], max_output=100)
        finally:
            self.admin.subprocess.run = original

        self.assertEqual(result["json"]["ok"], True)
        self.assertEqual(result["parse_error"], "")
        self.assertTrue(result["output_truncated"])
        self.assertLessEqual(len(result["output"]), 12000)


if __name__ == "__main__":
    unittest.main()
