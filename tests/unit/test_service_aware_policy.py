import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-users-autoswitch"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_ab", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ServiceAwarePolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def write_fixture(
        self,
        root: Path,
        *,
        current: str = "awg0",
        vless_severity: str = "SUSPECT",
        vless_reason: str = "handshake_unsupported_for_protocol_vless",
        vless_extra: str = "",
        awg0_extra: str = "",
        required_services=None,
        include_chatgpt: bool = True,
        vless_services=None,
        route_fitness: str = "WARN",
    ) -> None:
        state_dir = root / "state"
        event_dir = root / "events"
        state_dir.mkdir()
        event_dir.mkdir()
        required_services = required_services or ["telegram", "youtube", "instagram", "chatgpt"]
        users = [f"ip=10.0.0.2 current={current} table=100 enabled=1"]
        (state_dir / "users.registry").write_text("\n".join(users) + "\n", encoding="utf-8")
        (state_dir / "egress.registry").write_text(
            f"id=awg0 interface=awg0 enabled=1 state=enabled role=GLOBAL_STABLE{awg0_extra}\n"
            f"id=vless interface=tun0 enabled=1 state=enabled role=GLOBAL_FAST{vless_extra}\n",
            encoding="utf-8",
        )
        (state_dir / "v7-state.json").write_text(
            json.dumps(
                {
                    "egress": {
                        "awg0": {
                            "avg_mbps": 1.2,
                            "min_mbps": 0.8,
                            "stability": 0.62,
                            "code": "200",
                            "diagnose_severity": "OK",
                            "diagnose_reason": "OK",
                        },
                        "vless": {
                            "avg_mbps": 38.7,
                            "min_mbps": 6.8,
                            "stability": 0.176,
                            "code": "200",
                            "diagnose_severity": vless_severity,
                            "diagnose_reason": vless_reason,
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        services = {
            "telegram": {"ok": True, "status": "OK", "score": 95, "first_byte_sec": 0.25},
            "youtube": {"ok": True, "status": "OK", "score": 88, "first_byte_sec": 0.7},
            "instagram": {"ok": True, "status": "OK", "score": 82, "first_byte_sec": 0.8},
        }
        if include_chatgpt:
            services["chatgpt"] = {"ok": True, "status": "OK", "score": 84, "first_byte_sec": 0.9}
        if vless_services is not None:
            services = vless_services
        matrix = {
            "items": {
                "awg0": {
                    "services": {
                        "telegram": {"ok": True, "status": "OK", "score": 95, "first_byte_sec": 0.25},
                        "youtube": {"ok": True, "status": "OK", "score": 88, "first_byte_sec": 0.7},
                        "instagram": {"ok": True, "status": "OK", "score": 82, "first_byte_sec": 0.8},
                        "chatgpt": {"ok": True, "status": "OK", "score": 84, "first_byte_sec": 0.9},
                    },
                    "route_class_fitness": {"VIDEO_OPTIMIZED": {"status": "OK"}},
                },
                "vless": {
                    "services": services,
                    "route_class_fitness": {"VIDEO_OPTIMIZED": {"status": route_fitness}},
                },
            }
        }
        (state_dir / "service-matrix.json").write_text(json.dumps(matrix), encoding="utf-8")
        (state_dir / "egress-quality-summary.json").write_text(
            json.dumps(
                {
                    "items": {
                        "awg0": {"windows": {"1h": {"avg_mbps": 1.7, "min_mbps": 1.1, "stability": 0.65, "fail_rate": 0.07}}},
                        "vless": {"windows": {"1h": {"avg_mbps": 37.2, "min_mbps": 16.2, "stability": 0.36, "fail_rate": 0.05}}},
                    }
                }
            ),
            encoding="utf-8",
        )
        policy = {
            "required_services": required_services,
            "switch": {"autoswitch_enabled": True, "cooldown_seconds": 0, "min_score_delta": 1},
            "load": {"rebalance_enabled": False},
            "reconnect": {"enabled": False},
        }
        (root / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
        (root / "org-policy.json").write_text("{}", encoding="utf-8")
        for name in [
            "autoswitch-safety.json",
            "telegram-sentinel.json",
            "client-reconnect-state.json",
            "vless-activity.json",
            "egress-load-summary.json",
            "autoswitch-restore-barrier.json",
        ]:
            (state_dir / name).write_text("{}", encoding="utf-8")

    def args_for(self, root: Path):
        parser = self.tool.build_arg_parser()
        return parser.parse_args(
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

    def plan(self, root: Path) -> dict:
        planner = self.tool.AutoswitchPlanner(self.args_for(root))
        plan = planner.plan()
        plan["apply_result"] = planner.apply(plan)
        planner.finalize_operation(plan)
        return plan

    def candidate(self, plan: dict, egress: str) -> dict:
        return next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == egress)

    def test_vless_protocol_limited_suspect_can_be_eligible_with_service_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan(root)
            vless = self.candidate(plan, "vless")
            self.assertTrue(vless["eligible"])
            self.assertEqual(
                vless["severity_classification"]["category"],
                "protocol_diagnostic_limited_suspect",
            )
            self.assertGreaterEqual(vless["service_suitability"]["aggregate_score"], 50)
            self.assertIn("quality_floor_overridden_by_service_evidence", vless["reasons"])
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_fail_severity_remains_hard_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, vless_severity="FAIL", vless_reason="routing_broken")
            plan = self.plan(root)
            vless = self.candidate(plan, "vless")
            self.assertFalse(vless["eligible"])
            self.assertIn("severity_FAIL", vless["blocked"])

    def test_fatal_suspect_remains_hard_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, vless_reason="packet_path_failure")
            plan = self.plan(root)
            vless = self.candidate(plan, "vless")
            self.assertFalse(vless["eligible"])
            self.assertIn("severity_SUSPECT", vless["blocked"])

    def test_missing_required_service_evidence_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, include_chatgpt=False)
            plan = self.plan(root)
            vless = self.candidate(plan, "vless")
            self.assertFalse(vless["eligible"])
            self.assertIn("service_chatgpt_evidence_unknown", vless["blocked"])

    def test_weak_awg_remains_usable_when_required_service_evidence_is_fresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan(root)
            awg0 = self.candidate(plan, "awg0")
            # Throughput floors are soft ranking signals.  A target with
            # current required-service evidence remains available for
            # failed-source recovery; otherwise a soft overload could leave
            # an ordinary user on a confirmed broken source.
            self.assertTrue(awg0["eligible"])
            # The raw floor observations remain visible for ranking and the
            # operator surface; availability-first must not convert them into
            # an ineligible target.
            self.assertIn("avg_mbps_below_floor", awg0["blocked"])
            self.assertIn("min_mbps_below_floor", awg0["blocked"])

    def test_reservation_and_manual_gates_remain_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, vless_extra=" canary_reserved=true", awg0_extra=" manual_only=1")
            plan = self.plan(root)
            vless = self.candidate(plan, "vless")
            awg0 = self.candidate(plan, "awg0")
            self.assertFalse(vless["eligible"])
            self.assertIn("canary_reserved_production_assignment_blocked", vless["blocked"])
            self.assertFalse(awg0["eligible"])
            self.assertIn("manual_only", awg0["blocked"])

    def test_service_suitability_is_not_generic_mbps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root))
            awg0 = planner.egress["awg0"]
            vless = planner.egress["vless"]
            awg0.avg_mbps = 1.0
            vless.avg_mbps = 100.0
            awg0_services = planner._service_suitability(awg0, ["telegram", "youtube"], "VIDEO_OPTIMIZED")
            vless_services = planner._service_suitability(vless, ["telegram", "youtube"], "VIDEO_OPTIMIZED")
            self.assertEqual(awg0_services["aggregate_score"], vless_services["aggregate_score"])
            self.assertEqual(awg0_services["semantics"], "service suitability 0-100; not generic Mbps")

    def test_relative_improvement_still_required_after_eligibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current="vless")
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn("current_is_best", plan["decisions"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
