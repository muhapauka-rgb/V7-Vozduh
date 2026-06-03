import inspect
import unittest

from admin_core import overview_views, performance_summaries


class Api4OverviewPerformanceTest(unittest.TestCase):
    def test_overview_snapshot_reuses_registry_rows(self):
        state = {"users": [{"ip": "10.7.0.4", "enabled": "1"}], "egress": {"awg0": {"code": "200"}}}
        registry_users = [{"ip": "10.7.0.2", "enabled": "1"}]
        registry_egress = [{"id": "awg0"}]
        snapshot = overview_views.create_snapshot(
            state=state,
            users_registry=registry_users,
            egress_registry=registry_egress,
            draft_evidence={"items": {}},
        )
        self.assertEqual(snapshot.users, state["users"])
        self.assertEqual(snapshot.users_registry, registry_users)
        self.assertEqual(snapshot.egress_registry, registry_egress)
        self.assertEqual(snapshot.active_users, state["users"])
        self.assertEqual(snapshot.egress_state, state["egress"])

    def test_overview_summary_matches_legacy_shape(self):
        summary = overview_views.build_summary(
            users=[{"ip": "10.7.0.2"}, {"ip": "10.7.0.3"}],
            active_users=[{"ip": "10.7.0.2"}],
            egress={"awg0": {}, "awg1": {}},
            healthy=1,
            route_rows=[{"ok": True, "leak_risk": False}, {"ok": False, "leak_risk": True}],
            killswitch_state={"ok": True, "normalized_status": "OK", "reason": "ready", "check_rc": 0},
            capacity_plan={"readiness_result": "WARN"},
            stale={"output": "V7_STALE_RESULT=OK"},
            client_speed_users={"10.7.0.2": {"agent_online": True}, "10.7.0.3": {"agent_online": False}},
            active_readiness={"10.7.0.2": {"status": "READY"}, "10.7.0.3": {"status": "BLOCKED"}},
            active_onboarding={"10.7.0.2": {"stage": "ready_to_deliver"}, "10.7.0.3": {"stage": "link_sent"}},
            direct_routing={"route_ok": True},
            identity={"summary": {"identity_users": 2, "allowed_users": 1}},
            proxy_runtime={"status": "OK", "needs_refresh": False},
        )
        self.assertEqual(summary["users_total"], 1)
        self.assertEqual(summary["users_registry_total"], 2)
        self.assertEqual(summary["egress_total"], 2)
        self.assertEqual(summary["egress_healthy"], 1)
        self.assertEqual(summary["route_ok"], 1)
        self.assertTrue(summary["route_leak_risk"])
        self.assertTrue(summary["killswitch_ok"])
        self.assertTrue(summary["capacity_ok"])
        self.assertTrue(summary["stale_ok"])
        self.assertEqual(summary["client_agents_online"], 1)
        self.assertEqual(summary["users_ready"], 1)
        self.assertEqual(summary["users_blocked"], 1)
        self.assertEqual(summary["users_ready_to_deliver"], 1)
        self.assertEqual(summary["users_link_sent"], 1)
        self.assertTrue(summary["direct_ru_route_ok"])
        self.assertEqual(summary["identity_users"], 2)
        self.assertTrue(summary["proxy_runtime_ok"])

    def test_egress_health_and_payload_builders(self):
        health = overview_views.egress_health_summary(
            {"awg0": {"code": "200"}, "awg1": {"code": "500"}},
            {"items": {"draft1": {"ready": True}, "awg0": {"ready": True}}},
        )
        self.assertEqual(health["healthy"], 2)
        registries = overview_views.build_registries(
            users_registry=[{"ip": "10.7.0.2"}],
            egress_registry=[{"id": "awg0"}],
            egress_flags="x=1\n",
            egress_flags_map={"x": "1"},
        )
        self.assertEqual(registries["users"][0]["ip"], "10.7.0.2")
        checks = overview_views.build_checks(
            stale={"rc": 0},
            killswitch={"rc": 0},
            killswitch_state={"ok": True},
            capacity={"rc": 0},
            capacity_readiness={"rc": 0},
            ipam_preview={"rc": 0},
            direct_routing={"quick_test": {"rc": 0}},
            trusted_ru={"updated": "now", "local_ok": 1, "total": 2, "temporary_ok": 0, "blocked": 1},
            rebalance={"rc": 0},
        )
        self.assertIn("local_ok=1/2", checks["trusted_ru"]["output"])

    def test_schema_and_performance_architecture(self):
        contract = overview_views.overview_schema_contract()
        self.assertTrue(contract["read_only"])
        self.assertIn("summary", contract["required"])
        contracts = overview_views.api4_schema_contracts()
        self.assertIn("dashboard", contracts)
        self.assertIn("routing_intelligence_summary", contracts)
        self.assertTrue(all(item["read_only"] for item in contracts.values()))
        architecture = performance_summaries.performance_architecture_summary()
        self.assertIn("overview", architecture["dependency_map"])
        self.assertIn("overview", {item["name"] for item in architecture["cache_candidates"]})
        self.assertIn("route_status_per_user_probe", architecture["async_candidates"])
        self.assertIn("user_movement", architecture["forbidden_request_path_items"])

    def test_new_modules_have_no_mutation_surface(self):
        forbidden = ("subprocess", "run_action", "write_json_atomic", "write_text_atomic", "audit_admin", "append_jsonl")
        for module in (overview_views, performance_summaries):
            source = inspect.getsource(module)
            for token in forbidden:
                self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
