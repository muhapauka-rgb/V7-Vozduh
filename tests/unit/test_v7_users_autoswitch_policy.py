import importlib.machinery
import importlib.util
import json
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

    def plan(self, root: Path) -> dict:
        parser = self.tool.build_arg_parser()
        args = parser.parse_args(
            [
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
        )
        planner = self.tool.AutoswitchPlanner(args)
        return planner.plan()

    def test_instagram_one_sample_fail_is_degraded_not_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=15, egress_1_services={"instagram": {"ok": False, "score": 0}})
            plan = self.plan(root)
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
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)
            self.assertEqual(plan["selected_moves"][0]["move_type"], "failover")

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
            self.assertTrue(plan["safety"]["restore_barrier"]["active"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn(
                "restore_barrier_failover_suppressed",
                plan["decisions"][0]["reason"],
            )

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
