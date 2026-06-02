import importlib.machinery
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-users-autoswitch"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class V7UsersAutoswitchPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def write_fixture(
        self,
        root: Path,
        *,
        users: int = 1,
        egress_1_services: Optional[dict] = None,
        egress_1_state: str = "enabled",
        current_egress: str = "1",
        vless_registry_extra: str = "",
        service_signals: Optional[dict] = None,
        restore_barrier: Optional[dict] = None,
    ) -> None:
        state_dir = root / "state"
        event_dir = root / "events"
        state_dir.mkdir()
        event_dir.mkdir()
        registry = []
        for idx in range(users):
            registry.append(f"ip=10.0.0.{idx + 2} current={current_egress} table={100 + idx} enabled=1")
        (state_dir / "users.registry").write_text("\n".join(registry) + "\n", encoding="utf-8")
        (state_dir / "egress.registry").write_text(
            f"id=1 interface=v7one enabled=1 state={egress_1_state} role=GLOBAL_FAST\n"
            f"id=vless interface=tun0 enabled=1 role=GLOBAL_FAST{vless_registry_extra}\n",
            encoding="utf-8",
        )
        (state_dir / "v7-state.json").write_text(
            json.dumps(
                {
                    "egress": {
                        "1": {
                            "avg_mbps": 80,
                            "min_mbps": 70,
                            "stability": 0.95,
                            "code": "200",
                            "diagnose_severity": "OK",
                        },
                        "vless": {
                            "avg_mbps": 50,
                            "min_mbps": 45,
                            "stability": 0.9,
                            "code": "200",
                            "diagnose_severity": "OK",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        base_services = {
            "youtube": {"ok": True, "score": 100},
            "instagram": {"ok": True, "score": 100},
            "telegram": {"ok": True, "status": "OK", "score": 100},
            "google": {"ok": True, "score": 100},
            "google_auth": {"ok": True, "score": 100},
        }
        base_services.update(egress_1_services or {})
        (state_dir / "service-matrix.json").write_text(
            json.dumps(
                {
                    "items": {
                        "1": {
                            "services": base_services,
                            "route_class_fitness": {
                                "VIDEO_OPTIMIZED": {"status": "OK"},
                                "GLOBAL_STABLE": {"status": "OK"},
                                "GLOBAL_FAST": {"status": "OK"},
                            },
                        },
                        "vless": {
                            "services": {
                                "youtube": {"ok": True, "score": 100},
                                "instagram": {"ok": True, "score": 100},
                                "telegram": {"ok": True, "status": "OK", "score": 100},
                                "google": {"ok": True, "score": 100},
                                "google_auth": {"ok": True, "score": 100},
                            },
                            "route_class_fitness": {
                                "VIDEO_OPTIMIZED": {"status": "OK"},
                                "GLOBAL_STABLE": {"status": "OK"},
                                "GLOBAL_FAST": {"status": "OK"},
                            },
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        policy = {
            "switch": {
                "autoswitch_enabled": True,
                "autoswitch_max_failover_per_run": 25,
                "cooldown_seconds": 0,
                "min_score_delta": 5000,
            },
            "load": {"rebalance_enabled": False},
            "reconnect": {"enabled": False},
            "service_signals": service_signals or {},
        }
        (root / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
        (root / "org-policy.json").write_text("{}", encoding="utf-8")
        for name in [
            "egress-quality-summary.json",
            "autoswitch-safety.json",
            "telegram-sentinel.json",
            "client-reconnect-state.json",
            "vless-activity.json",
            "egress-load-summary.json",
        ]:
            (state_dir / name).write_text("{}", encoding="utf-8")
        (state_dir / "autoswitch-restore-barrier.json").write_text(
            json.dumps(restore_barrier or {}), encoding="utf-8"
        )

    def args_for(self, root: Path, extra_args: Optional[list[str]] = None):
        parser = self.tool.build_arg_parser()
        base_args = [
            "--state-dir",
            str(root / "state"),
            "--policy-file",
            str(root / "policy.json"),
            "--org-policy-file",
            str(root / "org-policy.json"),
            "--event-dir",
            str(root / "events"),
            "--quality-summary-file",
            str(root / "state" / "egress-quality-summary.json"),
            "--safety-file",
            str(root / "state" / "autoswitch-safety.json"),
            "--telegram-sentinel-file",
            str(root / "state" / "telegram-sentinel.json"),
            "--reconnect-state-file",
            str(root / "state" / "client-reconnect-state.json"),
            "--vless-activity-file",
            str(root / "state" / "vless-activity.json"),
            "--load-summary-file",
            str(root / "state" / "egress-load-summary.json"),
            "--restore-barrier-file",
            str(root / "state" / "autoswitch-restore-barrier.json"),
        ]
        return parser.parse_args(base_args + list(extra_args or []))

    def plan(self, root: Path) -> dict:
        planner = self.tool.AutoswitchPlanner(self.args_for(root))
        plan = planner.plan()
        plan["apply_result"] = planner.apply(plan)
        planner.finalize_operation(plan)
        return plan

    def apply_plan_with_mocks(self, root: Path) -> tuple[dict, list[tuple[str, str, str]]]:
        args = self.args_for(root, ["--apply"])
        planner = self.tool.AutoswitchPlanner(args)
        plan = planner.plan()
        switch_calls = []

        def fake_run_switch(ip: str, egress: str, reason: str):
            switch_calls.append((ip, egress, reason))
            return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

        def fake_verify_routes():
            return subprocess.CompletedProcess(["v7-user-route-check"], 1, stdout="verify failed\n")

        def fake_emit_terminal_audit(audit: dict) -> dict:
            audit["emitted"] = True
            audit["status"] = "emitted"
            audit["output"] = "mock audit emission"
            return audit

        planner._run_switch = fake_run_switch
        planner._verify_routes = fake_verify_routes
        planner._emit_terminal_audit = fake_emit_terminal_audit
        plan["apply_result"] = planner.apply(plan)
        planner.finalize_operation(plan)
        return plan, switch_calls

    def expected_selected_move_hash(self, selected: list[dict]) -> str:
        normalized = [
            {
                "user_ip": str(move.get("user_ip") or ""),
                "from": str(move.get("current_egress") or ""),
                "to": str(move.get("recommended_egress") or ""),
                "move_type": str(move.get("move_type") or ""),
            }
            for move in selected
        ]
        return self.tool.sha256_json(normalized)

    def assert_operation_envelope(self, plan: dict) -> None:
        for key in ("schema_version", "summary", "safety", "decisions", "selected_moves"):
            self.assertIn(key, plan)
        operation = plan.get("operation")
        self.assertIsInstance(operation, dict)
        self.assertTrue(operation.get("operation_id", "").startswith("runtime_autoswitch_"))
        self.assertEqual(operation["operation_owner"], "tools/v7-users-autoswitch")
        self.assertEqual(operation["operation_type"], "runtime_autoswitch")
        self.assertTrue(operation.get("operation_started_at"))
        self.assertEqual(
            operation["planner_generation_id"],
            plan["safety"]["generation"]["planner_generation_id"],
        )
        self.assertEqual(operation["selected_move_hash"], self.expected_selected_move_hash(plan["selected_moves"]))
        self.assertEqual(operation["selected_move_count"], len(plan["selected_moves"]))
        self.assertEqual(operation["selected_move_count"], plan["summary"]["selected_moves"])
        self.assertTrue(operation.get("runtime_snapshot_hash"))
        self.assertIn("terminal_state", operation)
        self.assertIn("terminal_reason", operation)
        audit = plan.get("audit")
        self.assertIsInstance(audit, dict)
        self.assertEqual(audit["action"], "runtime_operation_terminal")
        self.assertEqual(audit["component"], "autoswitch")
        self.assertEqual(audit["object_type"], "runtime_operation")
        self.assertEqual(audit["object_id"], operation["operation_id"])
        self.assertEqual(audit["result"], operation["terminal_state"])
        self.assertEqual(audit["metadata"]["operation_id"], operation["operation_id"])
        self.assertEqual(audit["metadata"]["selected_move_hash"], operation["selected_move_hash"])
        self.assertEqual(audit["metadata"]["runtime_snapshot_hash"], operation["runtime_snapshot_hash"])
        if not plan["apply_requested"]:
            self.assertFalse(audit["emitted"])
            self.assertEqual(audit["status"], "ready_not_emitted_dry_run")
        closure = plan.get("closure_target")
        self.assertIsInstance(closure, dict)
        self.assertEqual(closure["object_type"], "runtime")
        self.assertEqual(closure["object_id"], operation["operation_id"])
        self.assertEqual(closure["closure_owner"], "admin/v7-admin-api")
        self.assertEqual(closure["observability_owner"], "admin_core/operator_observability.py")
        if not audit["emitted"]:
            self.assertEqual(closure["closure_state"], "OPEN")
            self.assertEqual(closure["closure_blocker"], "audit_missing")

    def test_instagram_one_sample_fail_is_degraded_not_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=15, egress_1_services={"instagram": {"ok": False, "score": 0}})
            plan = self.plan(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_no_selected_moves")
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertTrue(current["eligible"])
            self.assertIn("service_instagram_degraded", current["reasons"])
            self.assertIn("service_signal_DEGRADED_SERVICE", current["reasons"])

    def test_instagram_persistent_fail_can_trigger_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"instagram": {"ok": False, "score": 0, "consecutive_failures": 3}},
            )
            plan = self.plan(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_selected_moves_available")
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)
            self.assertEqual(plan["selected_moves"][0]["move_type"], "failover")
            self.assertEqual(plan["selected_moves"][0]["operation_id"], plan["operation"]["operation_id"])
            self.assertEqual(plan["selected_moves"][0]["selected_move_hash"], plan["operation"]["selected_move_hash"])
            self.assertEqual(plan["selected_moves"][0]["selected_move_index"], 0)

    def test_telegram_degraded_not_hard_blocked_does_not_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_services={"telegram": {"ok": True, "status": "DEGRADED", "score": 40}})
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertTrue(current["eligible"])

    def test_telegram_hard_blocked_can_trigger_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}})
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)
            self.assertIn("current_egress_not_eligible", plan["selected_moves"][0]["reason"])

    def test_max_selected_moves_caps_blast_radius_downward(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=4,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, ["--max-selected-moves", "2"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(plan["summary"]["candidate_moves_total"], 4)
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertEqual(plan["safety"]["requested_max_selected_moves"], 2)
        self.assertTrue(plan["safety"]["blast_radius_cap_applied"])

    def test_restore_barrier_suppresses_telegram_service_signal_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
            )
            plan = self.plan(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_restore_barrier_active")
            self.assertTrue(plan["safety"]["restore_barrier"]["active"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn(
                "restore_barrier_failover_suppressed",
                plan["decisions"][0]["reason"],
            )

    def test_apply_verify_failure_records_operation_rollback_and_audit_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"instagram": {"ok": False, "score": 0, "consecutive_failures": 3}},
            )
            plan, switch_calls = self.apply_plan_with_mocks(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "ROLLED_BACK")
            self.assertEqual(plan["operation"]["terminal_reason"], "verification_failed_rollback_completed")
            self.assertEqual(plan["operation"]["rollback_verdict"], "ROLLBACK_COMPLETED")
            self.assertEqual(len(switch_calls), 2)
            self.assertEqual(switch_calls[0][2], "failover")
            self.assertEqual(switch_calls[1][2], "rollback")
            row = plan["apply_result"]["results"][0]
            self.assertEqual(row["operation_id"], plan["operation"]["operation_id"])
            self.assertEqual(row["selected_move_hash"], plan["operation"]["selected_move_hash"])
            self.assertEqual(row["selected_move_index"], 0)
            self.assertTrue(row["rollback_attempted"])
            self.assertEqual(row["rollback_result"], "OK")
            self.assertEqual(row["rollback_verdict"], "ROLLBACK_COMPLETED")
            self.assertTrue(plan["audit"]["emitted"])
            self.assertEqual(plan["audit"]["status"], "emitted")
            self.assertEqual(plan["closure_target"]["closure_state"], "VERIFIED_READY")
            self.assertEqual(plan["closure_target"]["closure_blocker"], "")

    def test_operation_scoped_rollback_packet_executes_with_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="vless")
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            forward_result = {
                "operation": {
                    "operation_id": "runtime_autoswitch_forward_test",
                    "operation_owner": "tools/v7-users-autoswitch",
                    "operation_type": "runtime_autoswitch",
                    "planner_generation_id": "gen-test",
                    "selected_move_hash": "hash-test",
                    "selected_move_count": 1,
                    "runtime_snapshot_hash": "runtime-snapshot-test",
                    "terminal_state": "APPLIED",
                    "terminal_reason": "selected_moves_applied",
                },
                "apply_result": {
                    "applied": True,
                    "results": [
                        {
                            "user_ip": "10.0.0.2",
                            "from": "1",
                            "to": "vless",
                            "move_type": "failover",
                            "operation_id": "runtime_autoswitch_forward_test",
                            "selected_move_hash": "hash-test",
                            "selected_move_index": 0,
                            "rc": 0,
                            "rollback_attempted": False,
                        }
                    ],
                },
            }
            packet_result = planner.generate_rollback_packet_from_result(forward_result)
            packet = packet_result["packet"]
            packet_path = root / "rollback-packet.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            def fake_emit_terminal_audit(audit: dict) -> dict:
                audit["emitted"] = True
                audit["status"] = "emitted"
                audit["output"] = "mock rollback audit emission"
                return audit

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            planner._emit_terminal_audit = fake_emit_terminal_audit
            result = planner.execute_rollback_packet(packet_path)

        self.assertEqual(packet_result["validation_errors"], [])
        self.assertEqual(packet["schema_version"], self.tool.ROLLBACK_PACKET_SCHEMA)
        self.assertEqual(packet["items"][0]["source_operation_id"], "runtime_autoswitch_forward_test")
        self.assertEqual(switch_calls, [("10.0.0.2", "1", "rollback")])
        self.assertEqual(result["operation"]["terminal_state"], "ROLLBACK_COMPLETED")
        self.assertEqual(result["rollback_result"]["results"][0]["rollback_verdict"], "ROLLBACK_COMPLETED")
        self.assertEqual(result["audit"]["metadata"]["source_operation_id"], "runtime_autoswitch_forward_test")
        self.assertEqual(result["audit"]["metadata"]["selected_move_hash"], "hash-test")
        self.assertTrue(result["audit"]["emitted"])
        self.assertEqual(result["closure_target"]["closure_state"], "VERIFIED_READY")

    def test_operation_scoped_rollback_packet_executes_multiple_users_with_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=2, current_egress="vless")
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            forward_result = {
                "operation": {
                    "operation_id": "runtime_autoswitch_forward_multi",
                    "operation_owner": "tools/v7-users-autoswitch",
                    "operation_type": "runtime_autoswitch",
                    "planner_generation_id": "gen-test",
                    "selected_move_hash": "hash-multi",
                    "selected_move_count": 2,
                    "runtime_snapshot_hash": "runtime-snapshot-test",
                    "terminal_state": "APPLIED",
                    "terminal_reason": "selected_moves_applied",
                },
                "apply_result": {
                    "applied": True,
                    "results": [
                        {
                            "user_ip": "10.0.0.2",
                            "from": "1",
                            "to": "vless",
                            "move_type": "failover",
                            "operation_id": "runtime_autoswitch_forward_multi",
                            "selected_move_hash": "hash-multi",
                            "selected_move_index": 0,
                            "rc": 0,
                            "rollback_attempted": False,
                        },
                        {
                            "user_ip": "10.0.0.3",
                            "from": "1",
                            "to": "vless",
                            "move_type": "failover",
                            "operation_id": "runtime_autoswitch_forward_multi",
                            "selected_move_hash": "hash-multi",
                            "selected_move_index": 1,
                            "rc": 0,
                            "rollback_attempted": False,
                        },
                    ],
                },
            }
            packet_result = planner.generate_rollback_packet_from_result(forward_result)
            packet = packet_result["packet"]
            packet_path = root / "rollback-packet.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            def fake_emit_terminal_audit(audit: dict) -> dict:
                audit["emitted"] = True
                audit["status"] = "emitted"
                audit["output"] = "mock rollback audit emission"
                return audit

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            planner._emit_terminal_audit = fake_emit_terminal_audit
            result = planner.execute_rollback_packet(packet_path)

        self.assertEqual(packet_result["validation_errors"], [])
        self.assertEqual(packet["constraints"]["max_rollback_users"], 2)
        self.assertEqual(len(packet["items"]), 2)
        self.assertEqual(switch_calls, [("10.0.0.2", "1", "rollback"), ("10.0.0.3", "1", "rollback")])
        self.assertEqual(result["operation"]["terminal_state"], "ROLLBACK_COMPLETED")
        self.assertEqual(result["operation"]["rollback_count"], 2)
        self.assertEqual(len(result["rollback_result"]["results"]), 2)
        self.assertTrue(result["audit"]["emitted"])

    def test_restore_barrier_suppresses_non_service_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_state="disabled",
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
            )
            plan = self.plan(root)
            self.assertTrue(plan["safety"]["restore_barrier"]["active"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn("restore_barrier_failover_suppressed", plan["decisions"][0]["reason"])

    def test_expired_restore_barrier_requires_generation_clearance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "reason": "unit-test-expired",
                },
            )
            plan = self.plan(root)
            self.assertFalse(plan["safety"]["restore_barrier"]["active"])
            self.assertTrue(plan["safety"]["restore_barrier"]["expired"])
            self.assertTrue(plan["safety"]["restore_barrier"]["post_ttl_blocking"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn(
                "restore_barrier_post_ttl_generation_clearance_required",
                plan["decisions"][0]["reason"],
            )

    def test_expired_restore_barrier_with_clearance_allows_telegram_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "allow_post_ttl_apply": True,
                    "reason": "unit-test-expired-cleared",
                },
            )
            plan = self.plan(root)
            self.assertFalse(plan["safety"]["restore_barrier"]["active"])
            self.assertTrue(plan["safety"]["restore_barrier"]["expired"])
            self.assertTrue(plan["safety"]["restore_barrier"]["cleared"])
            self.assertFalse(plan["safety"]["restore_barrier"]["post_ttl_blocking"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_expired_restore_barrier_clearance_budget_blocks_selected_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 0,
                    "reason": "unit-test-expired-cleared-budget-zero",
                },
            )
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["active"])
            self.assertTrue(barrier["expired"])
            self.assertTrue(barrier["cleared"])
            self.assertFalse(barrier["post_ttl_blocking"])
            self.assertEqual(barrier["clearance_max_selected_moves"], 0)
            self.assertEqual(barrier["clearance_selected_moves_before_guard"], 1)
            self.assertTrue(barrier["clearance_budget_exceeded"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_selected_moves_exceed_budget",
            )
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_requires_generation_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                    "reason": "unit-test-nonzero-budget-no-generation",
                },
            )
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertEqual(barrier["clearance_selected_moves_before_guard"], 1)
            self.assertFalse(barrier["clearance_budget_exceeded"])
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_generation_token_missing",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_with_matching_generation_allows_selected_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                    "reason": "unit-test-nonzero-budget-bootstrap",
                },
            )
            bootstrap = self.plan(root)
            barrier = bootstrap["safety"]["restore_barrier"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": barrier["clearance_selected_moves_hash"],
                "clearance_expected_selected_moves": 1,
                "reason": "unit-test-nonzero-budget-approved",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertTrue(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_budget_and_generation_ok",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_planner_generation_excludes_fast_signal_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            first = self.plan(root)
            (root / "state" / "telegram-sentinel.json").write_text(
                json.dumps({"updated": "volatile-change"}), encoding="utf-8"
            )
            (root / "state" / "service-matrix.json").write_text(
                (root / "state" / "service-matrix.json").read_text(encoding="utf-8").replace(
                    '"score": 100', '"score": 99', 1
                ),
                encoding="utf-8",
            )
            (root / "state" / "v7-state.json").write_text(
                (root / "state" / "v7-state.json").read_text(encoding="utf-8").replace(
                    '"avg_mbps": 80', '"avg_mbps": 79', 1
                ),
                encoding="utf-8",
            )
            second = self.plan(root)

        self.assertEqual(
            first["safety"]["generation"]["planner_generation_id"],
            second["safety"]["generation"]["planner_generation_id"],
        )
        self.assertNotEqual(
            first["safety"]["generation"]["volatile_inputs"],
            second["safety"]["generation"]["volatile_inputs"],
        )

    def test_nonzero_clearance_budget_rejects_stale_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                    "generation_token": "unit-test-token",
                    "clearance_generation_id": "stale-generation",
                    "approved_selected_moves_hash": "stale-hash",
                    "clearance_expected_selected_moves": 1,
                },
            )
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_generation_mismatch",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_rejects_selected_move_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                },
            )
            bootstrap = self.plan(root)
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": "stale-hash",
                "clearance_expected_selected_moves": 1,
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_selected_moves_hash_mismatch",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_rejects_expired_generation_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                },
            )
            bootstrap = self.plan(root)
            barrier = bootstrap["safety"]["restore_barrier"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": barrier["clearance_selected_moves_hash"],
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2000-01-01T00:00:00+00:00",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_generation_expired",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_egress_disabled_is_hard_ineligible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_state="disabled")
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_multiple_critical_services_failed_can_trigger_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={
                    "instagram": {"ok": False, "score": 0},
                    "youtube": {"ok": False, "score": 0},
                },
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_restore_stage_suppresses_service_signal_failover_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=15,
                egress_1_services={
                    "instagram": {"ok": False, "score": 0},
                    "youtube": {"ok": False, "score": 0},
                },
                service_signals={"restore_stage": True, "apply_restore_approved": False},
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn("restore_stage_service_signal_failover_requires_approval", plan["decisions"][0]["reason"])

    def test_restore_stage_suppresses_telegram_signal_failover_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                service_signals={"restore_stage": True, "apply_restore_approved": False},
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn("restore_stage_service_signal_failover_requires_approval", plan["decisions"][0]["reason"])

    def test_restore_stage_approval_respects_max_failover_per_restore_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=15,
                egress_1_services={
                    "instagram": {"ok": False, "score": 0},
                    "youtube": {"ok": False, "score": 0},
                },
                service_signals={
                    "restore_stage": True,
                    "apply_restore_approved": True,
                    "max_failover_per_restore_stage": 1,
                },
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 15)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_canary_reserved_target_is_not_used_as_production_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_state="disabled", vless_registry_extra=" canary_reserved=true")
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            vless = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "vless")
            self.assertFalse(vless["eligible"])
            self.assertTrue(vless["canary_reserved"])
            self.assertIn("canary_reserved_production_assignment_blocked", vless["blocked"])
            self.assertIn("no_eligible_failover_target", plan["decisions"][0]["reason"])

    def test_current_user_on_canary_reserved_target_is_not_auto_drained(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="vless", vless_registry_extra=" canary_reserved=true")
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertEqual(plan["decisions"][0]["recommended_egress"], "vless")
            self.assertIn(
                "canary_reserved_current_hold_requires_separate_drain_approval",
                plan["decisions"][0]["reason"],
            )
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "vless")
            self.assertFalse(current["eligible"])
            self.assertIn("canary_reserved_production_assignment_blocked", current["blocked"])


if __name__ == "__main__":
    unittest.main()
