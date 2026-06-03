import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from admin_core.routing_brain import RoutingBrain, routing_brain_map


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-users-autoswitch"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_ri2", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def matrix_for_weights():
    return {
        "items": {
            "target": {
                "services": {
                    "telegram": {"ok": True, "status": "OK", "score": 95, "first_byte_sec": 0.2, "confidence": 0.9},
                    "chatgpt": {"ok": False, "status": "FAIL", "score": 0, "first_byte_sec": 5.0, "confidence": 0.2},
                }
            }
        }
    }


def quality_for_weights():
    return {
        "items": {
            "target": {
                "windows": {
                    "1h": {"avg_mbps": 30, "stability": 0.8, "fail_rate": 0.05},
                    "24h": {"avg_mbps": 30, "stability": 0.8, "fail_rate": 0.05},
                    "7d": {"avg_mbps": 30, "stability": 0.8, "fail_rate": 0.05},
                }
            }
        }
    }


class RoutingBrainContractTest(unittest.TestCase):
    def test_ri_cannot_move_users_or_write_selected_moves(self):
        advice = RoutingBrain(service_matrix=matrix_for_weights(), quality_summary=quality_for_weights()).advisory_context(
            total_users=10,
            affected_users=5,
            required_services=["telegram", "chatgpt"],
            candidate_targets=["target"],
        )
        self.assertEqual(advice["authority"]["routing_intelligence"], "advice_only")
        self.assertEqual(advice["selected_moves_write_authority"], "none")
        self.assertNotIn("selected_moves", advice)
        self.assertNotIn("apply_requested", advice)
        self.assertNotIn("runtime_action_record", advice)

    def test_ri_cannot_approve_governance(self):
        advice = RoutingBrain(service_matrix=matrix_for_weights(), quality_summary=quality_for_weights()).advisory_context(
            total_users=10,
            affected_users=5,
            required_services=["telegram", "chatgpt"],
            candidate_targets=["target"],
        )
        self.assertIn("approve_execution", advice["contract"]["may_not"])
        self.assertEqual(advice["authority"]["execution_authority"], "none")
        self.assertEqual(advice["authority"]["governance_authority"], "unchanged")

    def test_missing_ri_data_does_not_become_pass(self):
        advice = RoutingBrain().advisory_context(total_users=10, affected_users=5, required_services=["telegram"])
        self.assertFalse(advice["intelligence_present"])
        self.assertEqual(advice["service_history_score"], 0.0)
        self.assertEqual(advice["recommended_blast_radius"], 1)
        self.assertEqual(advice["service_scores"], {})

    def test_service_weights_affect_advisory_score(self):
        telegram_heavy = RoutingBrain(
            service_matrix=matrix_for_weights(),
            quality_summary=quality_for_weights(),
            service_preferences={"weights": {"telegram": 90, "chatgpt": 10}},
        ).advisory_context(total_users=10, affected_users=5, required_services=["telegram", "chatgpt"], candidate_targets=["target"])
        chatgpt_heavy = RoutingBrain(
            service_matrix=matrix_for_weights(),
            quality_summary=quality_for_weights(),
            service_preferences={"weights": {"telegram": 10, "chatgpt": 90}},
        ).advisory_context(total_users=10, affected_users=5, required_services=["telegram", "chatgpt"], candidate_targets=["target"])
        self.assertGreater(telegram_heavy["weighted_service_score"], chatgpt_heavy["weighted_service_score"])

    def test_execution_trust_affects_recommended_blast_radius(self):
        trusted = RoutingBrain(
            service_matrix=matrix_for_weights(),
            quality_summary=quality_for_weights(),
            audit_records=[{"result": "OK", "blast_radius": 1} for _ in range(20)],
        ).advisory_context(total_users=100, affected_users=50, required_services=["telegram"], candidate_targets=["target"])
        untrusted = RoutingBrain(
            service_matrix=matrix_for_weights(),
            quality_summary=quality_for_weights(),
            audit_records=[{"result": "failed", "governance_violation": True} for _ in range(5)],
        ).advisory_context(total_users=100, affected_users=50, required_services=["telegram"], candidate_targets=["target"])
        self.assertGreater(trusted["recommended_blast_radius"], untrusted["recommended_blast_radius"])

    def test_bad_service_history_lowers_and_strong_history_improves_suitability(self):
        advice = RoutingBrain(service_matrix=matrix_for_weights(), quality_summary=quality_for_weights()).advisory_context(
            total_users=10,
            affected_users=5,
            required_services=["telegram", "chatgpt"],
            candidate_targets=["target"],
        )
        per_service = {
            row["service"]: row["score"]
            for row in advice["service_scores"]["target"]["per_service"]
        }
        self.assertGreater(per_service["telegram"], per_service["chatgpt"])
        self.assertLess(advice["weighted_service_score"], 80)

    def test_feedback_loop_records_operation_outcomes_without_learning(self):
        feedback = RoutingBrain.feedback_envelope(
            operation_result={"terminal_state": "APPLIED"},
            rollback_result={"terminal_state": "ROLLBACK_DRY_RUN"},
            audit_result={"result": "OK"},
            closure_result={"closed": True},
            service_health_after={"telegram": "OK"},
        )
        self.assertEqual(feedback["schema_version"], "ri2.routing-brain-feedback.v1")
        self.assertFalse(feedback["autonomous_learning_enabled"])
        self.assertFalse(feedback["runtime_state_mutation"])
        self.assertEqual(feedback["feeds"]["execution_result"]["terminal_state"], "APPLIED")

    def test_no_duplicate_truth_source_created(self):
        model = routing_brain_map()
        self.assertEqual(model["single_source_of_truth"]["routing_decision"], "runtime planner")
        self.assertEqual(model["single_source_of_truth"]["execution_authorization"], "governance")
        self.assertIn("RI.2 RoutingBrain", [row["owner"] for row in model["chain"]])


class RoutingBrainPlannerIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def write_fixture(self, root: Path, *, include_service_matrix: bool = True) -> None:
        state_dir = root / "state"
        event_dir = root / "events"
        state_dir.mkdir()
        event_dir.mkdir()
        (state_dir / "users.registry").write_text("ip=10.0.0.2 current=current table=100 enabled=1\n", encoding="utf-8")
        (state_dir / "egress.registry").write_text(
            "id=current interface=cur0 enabled=1 state=enabled role=GLOBAL_STABLE\n"
            "id=fast interface=f1 enabled=1 state=enabled role=GLOBAL_FAST\n",
            encoding="utf-8",
        )
        (state_dir / "v7-state.json").write_text(
            json.dumps(
                {
                    "egress": {
                        "current": {"avg_mbps": 4, "min_mbps": 2, "stability": 0.5, "code": "200", "diagnose_severity": "OK"},
                        "fast": {"avg_mbps": 50, "min_mbps": 40, "stability": 0.9, "code": "200", "diagnose_severity": "OK"},
                    }
                }
            ),
            encoding="utf-8",
        )
        matrix = {
            "items": {
                "current": {"services": {"telegram": {"ok": False, "status": "DOWN", "score": 0}}},
                "fast": {"services": {"telegram": {"ok": True, "status": "OK", "score": 95, "first_byte_sec": 0.2}}},
            }
        }
        (state_dir / "service-matrix.json").write_text(json.dumps(matrix if include_service_matrix else {"items": {}}), encoding="utf-8")
        (state_dir / "egress-quality-summary.json").write_text(
            json.dumps(
                {
                    "items": {
                        "current": {"windows": {"1h": {"avg_mbps": 4, "stability": 0.5, "fail_rate": 0.2}}},
                        "fast": {"windows": {"1h": {"avg_mbps": 50, "stability": 0.9, "fail_rate": 0.01}}},
                    }
                }
            ),
            encoding="utf-8",
        )
        (state_dir / "service-preferences.json").write_text(json.dumps({"required_services": ["telegram"]}), encoding="utf-8")
        (event_dir / "switch-history.jsonl").write_text(json.dumps({"result": "OK", "blast_radius": 1}) + "\n", encoding="utf-8")
        policy = {
            "required_services": ["telegram"],
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

    def test_planner_remains_decision_owner_with_advisory_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan(root)
            brain = plan["routing_brain"]
            self.assertTrue(brain["intelligence_present"])
            self.assertEqual(brain["planner_decision_owner"], "tools/v7-users-autoswitch")
            self.assertEqual(brain["execution_authority"], "none")
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_missing_ri_data_does_not_override_planner_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, include_service_matrix=False)
            plan = self.plan(root)
            brain = plan["routing_brain"]
            self.assertTrue(brain["intelligence_present"])
            self.assertEqual(brain["service_history_score"], 0.0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            fast = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "fast")
            self.assertIn("service_telegram_evidence_unknown", fast["blocked"])


if __name__ == "__main__":
    unittest.main()
