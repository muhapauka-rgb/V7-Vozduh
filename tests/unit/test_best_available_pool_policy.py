import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-users-autoswitch"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_pool", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class BestAvailablePoolPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def write_fixture(
        self,
        root: Path,
        *,
        users: int = 6,
        current: str = "current",
        current_good: bool = False,
        fast2_extra: str = "",
        bad_services=None,
        min_score_delta: int = 1,
    ) -> None:
        state_dir = root / "state"
        event_dir = root / "events"
        state_dir.mkdir()
        event_dir.mkdir()
        (state_dir / "users.registry").write_text(
            "\n".join(f"ip=10.0.0.{idx + 2} current={current} table={100 + idx} enabled=1" for idx in range(users)) + "\n",
            encoding="utf-8",
        )
        (state_dir / "egress.registry").write_text(
            "id=current interface=cur0 enabled=1 state=enabled role=GLOBAL_STABLE\n"
            "id=fast1 interface=f1 enabled=1 state=enabled role=GLOBAL_FAST\n"
            f"id=fast2 interface=f2 enabled=1 state=enabled role=GLOBAL_FAST{fast2_extra}\n"
            "id=bad interface=bad0 enabled=1 state=enabled role=GLOBAL_FAST\n",
            encoding="utf-8",
        )
        current_speed = {"avg_mbps": 60, "min_mbps": 50, "stability": 0.95} if current_good else {"avg_mbps": 3, "min_mbps": 1, "stability": 0.5}
        (state_dir / "v7-state.json").write_text(
            json.dumps(
                {
                    "egress": {
                        "current": {**current_speed, "code": "200", "diagnose_severity": "OK"},
                        "fast1": {"avg_mbps": 58, "min_mbps": 45, "stability": 0.92, "code": "200", "diagnose_severity": "OK"},
                        "fast2": {"avg_mbps": 57, "min_mbps": 44, "stability": 0.91, "code": "200", "diagnose_severity": "OK"},
                        "bad": {"avg_mbps": 120, "min_mbps": 110, "stability": 0.95, "code": "200", "diagnose_severity": "OK"},
                    }
                }
            ),
            encoding="utf-8",
        )
        good_services = {
            "telegram": {"ok": True, "status": "OK", "score": 96, "first_byte_sec": 0.2},
            "youtube": {"ok": True, "status": "OK", "score": 90, "first_byte_sec": 0.6},
            "instagram": {"ok": True, "status": "OK", "score": 88, "first_byte_sec": 0.7},
        }
        bad_services = bad_services or {
            "telegram": {"ok": False, "status": "DOWN", "score": 0},
            "youtube": {"ok": False, "status": "FAIL", "score": 0},
            "instagram": {"ok": False, "status": "FAIL", "score": 0},
        }
        matrix = {
            "items": {
                "current": {"services": good_services if current_good else bad_services, "route_class_fitness": {"VIDEO_OPTIMIZED": {"status": "OK" if current_good else "FAIL"}}},
                "fast1": {"services": good_services, "route_class_fitness": {"VIDEO_OPTIMIZED": {"status": "OK"}}},
                "fast2": {"services": good_services, "route_class_fitness": {"VIDEO_OPTIMIZED": {"status": "OK"}}},
                "bad": {"services": bad_services, "route_class_fitness": {"VIDEO_OPTIMIZED": {"status": "FAIL"}}},
            }
        }
        (state_dir / "service-matrix.json").write_text(json.dumps(matrix), encoding="utf-8")
        quality = {
            "items": {
                key: {"windows": {"1h": {"avg_mbps": 55, "min_mbps": 40, "stability": 0.9, "fail_rate": 0.01}}}
                for key in ("current", "fast1", "fast2", "bad")
            }
        }
        if not current_good:
            quality["items"]["current"] = {"windows": {"1h": {"avg_mbps": 3, "min_mbps": 1, "stability": 0.5, "fail_rate": 0.2}}}
        (state_dir / "egress-quality-summary.json").write_text(json.dumps(quality), encoding="utf-8")
        policy = {
            "required_services": ["telegram", "youtube", "instagram"],
            "switch": {
                "autoswitch_enabled": True,
                "cooldown_seconds": 0,
                "min_score_delta": min_score_delta,
                "autoswitch_max_failover_per_run": users,
                "autoswitch_max_planned_per_run": users,
            },
            "load": {
                "mode": "static",
                "soft_limit": 4,
                "hard_limit": 6,
                "rebalance_enabled": False,
            },
            "best_available_pool": {"top_n": 3, "max_score_gap_pct": 0.25},
            "authority_budget": {
                "authority_class": "LARGE_BATCH",
                "current_allowed_user_budget": users,
                "next_allowed_user_budget": users,
            },
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
                "--state-dir", str(root / "state"),
                "--policy-file", str(root / "policy.json"),
                "--org-policy-file", str(root / "org-policy.json"),
                "--event-dir", str(root / "events"),
                "--quality-summary-file", str(root / "state" / "egress-quality-summary.json"),
                "--safety-file", str(root / "state" / "autoswitch-safety.json"),
                "--telegram-sentinel-file", str(root / "state" / "telegram-sentinel.json"),
                "--reconnect-state-file", str(root / "state" / "client-reconnect-state.json"),
                "--vless-activity-file", str(root / "state" / "vless-activity.json"),
                "--load-summary-file", str(root / "state" / "egress-load-summary.json"),
                "--restore-barrier-file", str(root / "state" / "autoswitch-restore-barrier.json"),
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

    def test_best_available_pool_includes_close_suitable_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan(root)
            self.assertTrue(self.candidate(plan, "fast1")["best_available_pool"])
            self.assertTrue(self.candidate(plan, "fast2")["best_available_pool"])

    def test_best_available_pool_excludes_unsafe_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan(root)
            bad = self.candidate(plan, "bad")
            self.assertFalse(bad["eligible"])
            self.assertFalse(bad["best_available_pool"])
            self.assertIn("route_class_VIDEO_OPTIMIZED_failed", bad["blocked"])

    def test_capacity_does_not_admit_bad_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan(root)
            targets = {move["recommended_egress"] for move in plan["selected_moves"]}
            self.assertNotIn("bad", targets)

    def test_capacity_distributes_among_pool_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=6)
            plan = self.plan(root)
            targets = [move["recommended_egress"] for move in plan["selected_moves"]]
            self.assertIn("fast1", targets)
            self.assertIn("fast2", targets)
            self.assertLess(max(targets.count("fast1"), targets.count("fast2")), len(targets))

    def test_canary_reserved_pool_candidate_remains_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, fast2_extra=" canary_reserved=true")
            plan = self.plan(root)
            fast2 = self.candidate(plan, "fast2")
            self.assertFalse(fast2["eligible"])
            self.assertIn("canary_reserved_production_assignment_blocked", fast2["blocked"])

    def test_sticky_preserved_when_improvement_is_weak(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current="current", current_good=True, min_score_delta=100000)
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn("sticky_keep_current", plan["decisions"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
