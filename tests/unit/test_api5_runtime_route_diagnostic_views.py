import importlib.machinery
import importlib.util
import inspect
import unittest
from pathlib import Path

from admin_core import diagnostic_views, performance_summaries, route_reality_views, runtime_read_views


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_admin_api():
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_api5", str(ADMIN_API))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class Api5RuntimeRouteDiagnosticViewsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin = load_admin_api()

    def test_runtime_fingerprint_view_parity(self):
        components = [
            {"name": "runtime_state", "present": True, "age_sec": 20, "hash": "secret"},
            {"name": "autoswitch", "present": False, "hash": "hidden"},
        ]
        old_components = self.admin.runtime_fingerprint_components
        old_store = self.admin.RUNTIME_TRUST_STORE_FILE
        try:
            self.admin.runtime_fingerprint_components = lambda: components
            self.admin.RUNTIME_TRUST_STORE_FILE = Path("/tmp/runtime-trust.jsonl")
            expected = runtime_read_views.runtime_fingerprint_payload(
                components,
                include_advanced=False,
                storage_path="/tmp/runtime-trust.jsonl",
            )
            self.assertEqual(self.admin.runtime_fingerprint_response(False), expected)
            advanced = self.admin.runtime_fingerprint_response(True)
            self.assertIn("advanced_details", advanced)
            self.assertNotIn("hash", advanced["components"][0])
            self.assertEqual(advanced["advanced_details"]["components"][0]["hash"], "secret")
        finally:
            self.admin.runtime_fingerprint_components = old_components
            self.admin.RUNTIME_TRUST_STORE_FILE = old_store

    def test_service_status_and_proxy_runtime_payload(self):
        old_run_readonly = self.admin.run_readonly
        try:
            self.admin.run_readonly = lambda cmd, timeout=0: {"output": "active\n" if cmd[-1] == "svc-a" else "inactive\n"}
            self.assertEqual(
                self.admin.service_status(["svc-a", "svc-b"]),
                runtime_read_views.service_status_payload(["svc-a", "svc-b"], {"svc-a": "active\n", "svc-b": "inactive\n"}),
            )
        finally:
            self.admin.run_readonly = old_run_readonly

        payload = runtime_read_views.proxy_runtime_payload(
            inbound_id="happ-test",
            unit="v7-proxy-inbound-happ-test.service",
            bindings=[{"user_ip": "10.7.0.2"}],
            runtime_users=1,
            auth_user_rules=1,
            legacy_user_rules=0,
            inbound_fallback_rules=0,
            service_active=True,
            candidate_meta={"status": "OK", "rendered_at": "2026-06-03T00:00:00+00:00"},
        )
        self.assertEqual(payload["status"], "OK")
        self.assertFalse(payload["needs_refresh"])

    def test_route_status_and_direct_routing_parity(self):
        old_run_readonly = self.admin.run_readonly
        old_egress_interface = self.admin.egress_interface
        try:
            self.admin.egress_interface = lambda current: "awg0" if current == "stable" else ""
            self.admin.run_readonly = lambda cmd, timeout=0: {"output": "8.8.8.8 dev awg0 src 10.7.0.2\n"}
            users = [
                {"ip": "10.7.0.2", "table": "1002", "current": "stable", "enabled": "1"},
                {"ip": "10.7.0.3", "table": "1003", "current": "stable", "enabled": "0"},
            ]
            self.assertEqual(
                self.admin.route_status(users),
                [
                    route_reality_views.route_status_row(
                        users[0],
                        expected_dev="awg0",
                        route_output="8.8.8.8 dev awg0 src 10.7.0.2\n",
                    )
                ],
            )
        finally:
            self.admin.run_readonly = old_run_readonly
            self.admin.egress_interface = old_egress_interface

        output = "\n".join([
            "domain=example.com",
            "user_ip=10.7.0.2",
            "resolved_ips=1.2.3.4",
            "ip=1.2.3.4 direct_set=yes direct_exclude=no",
            "decision=DIRECT_READY",
        ])
        self.assertEqual(self.admin.parse_direct_domain_test(output), route_reality_views.parse_direct_domain_test(output))

    def test_direct_routing_summaries(self):
        items = [
            {"domain": "ok.example", "status": "OK", "check": {"rc": 0}},
            {"domain": "stale.example", "status": "STALE_SET", "check": {"rc": 0}},
        ]
        freshness = route_reality_views.direct_routing_freshness_summary(
            user_ip="10.7.0.2",
            items=items,
            updated="2026-06-03T00:00:00+00:00",
        )
        self.assertEqual(freshness["status"], "STALE")
        self.assertEqual(freshness["stale_domains"], ["stale.example"])
        quick = route_reality_views.direct_routing_quick_summary(
            user_ip="10.7.0.2",
            status_result={"rc": 0, "output": "OK"},
            freshness=freshness,
            domains_state={"items": ["ok.example"]},
            fallback_domain="fallback.example",
        )
        self.assertFalse(quick["route_ok"])
        self.assertEqual(quick["quick_domain"], "ok.example")

    def test_diagnostic_view_parity(self):
        self.assertEqual(diagnostic_views.traffic_zero_summary("user", "10.7.0.2"), {
            "entity_type": "user", "entity_id": "10.7.0.2",
            "today": {"rx_bytes": 0, "tx_bytes": 0, "total_bytes": 0},
            "last_24h": {"rx_bytes": 0, "tx_bytes": 0, "total_bytes": 0},
            "week": {"rx_bytes": 0, "tx_bytes": 0, "total_bytes": 0},
            "month": {"rx_bytes": 0, "tx_bytes": 0, "total_bytes": 0},
            "all_time": {"rx_bytes": 0, "tx_bytes": 0, "total_bytes": 0},
            "updated_at": "", "snapshot": {},
        })

        users = [{"ip": "10.7.0.2", "current": "awg0", "enabled": "1"}]
        client_data = {
            "users": {
                "10.7.0.2": {
                    "latest": {
                        "v7": {"egress": "awg0", "mbps": 50},
                        "direct": {"awg0": {"mbps": 100}},
                    }
                }
            }
        }
        self.assertEqual(self.admin.client_speed_summary(users, client_data), diagnostic_views.client_speed_summary(users, client_data))

        check = {
            "rc": 0,
            "output": "\n".join([
                "V7_KILLSWITCH_CHECK=OK",
                "table=present",
                "client_source_set=present",
                "direct_leak_drop_rule=present",
            ]),
        }
        expected = diagnostic_views.killswitch_summary(
            output=check["output"],
            kv_data=self.admin.parse_command_kv(check["output"]),
            check_rc=0,
            status_rc=0,
        )
        self.assertEqual(self.admin.killswitch_summary(check, {"rc": 0}), expected)

        capacity = self.admin.capacity_state(
            {"output": "V7_CAPACITY_RESULT=OK target_users=500"},
            {"output": "V7_CAPACITY_READINESS=OK legacy_capacity=253 planned_ipam_capacity=1022"},
            {"output": "target_cidr=10.7.0.0/22 sample_01_ip=10.7.0.2 table=1002"},
            users,
        )
        self.assertEqual(capacity["total_capacity"], 1275)
        self.assertIn("New users", capacity["plain"])

    def test_schema_contracts_and_no_mutation_surface(self):
        contracts = {}
        contracts.update(runtime_read_views.runtime_read_schema_contracts())
        contracts.update(route_reality_views.route_reality_schema_contracts())
        contracts.update(diagnostic_views.diagnostic_schema_contracts())
        self.assertIn("runtime_summary", contracts)
        self.assertIn("route_reality", contracts)
        self.assertIn("traffic_summary", contracts)
        self.assertTrue(all(contract["read_only"] for contract in contracts.values()))

        foundation = performance_summaries.api5_performance_foundation()
        self.assertTrue(foundation["read_only"])
        self.assertTrue(foundation["no_cache_enabled"])
        self.assertIn("admin_core.runtime_read_views", foundation["payload_builder_modules"])

        forbidden = ("subprocess", "run_action", "write_json_atomic", "write_text_atomic", "audit_admin", "append_jsonl")
        for module in (runtime_read_views, route_reality_views, diagnostic_views, performance_summaries):
            source = inspect.getsource(module)
            for token in forbidden:
                self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
