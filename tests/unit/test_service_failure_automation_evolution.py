import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ServiceFailureAutomationEvolutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.autoswitch = load_module("v7_users_autoswitch_automation", ROOT / "tools" / "v7-users-autoswitch")
        cls.sync = load_module("v7_sync_lib_automation", ROOT / "tools" / "v7_sync_lib.py")

    def test_stop_safe_is_materialized_once_with_bounded_shadow(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_1",
                "source_incident_id": "sfinc_1",
                "situation_id": "situation_1",
                "decision_trace_id": "decision_1",
                "closure_state": "CAPTURED_STOP_SAFE",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "NATURAL_PRODUCTION_CANDIDATE",
                "channel": "vless",
                "affected_users": ["10.0.0.2", "10.0.0.3"],
                "observed_at": "2026-07-26T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            plan = {
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                    "reason": ["healthy_target"],
                }],
            }
            first = planner.materialize_service_failure_automation_advisory(plan)
            self.assertTrue(first["active"])
            self.assertEqual(first["obligation"]["stop_safe_classification"], "STOP_SAFE_AUTHORITY_REQUIRED")
            self.assertEqual(first["obligation"]["bounded_recommendation_users"], 1)
            self.assertEqual(first["obligation"]["aggregate_impact_users"], 2)
            self.assertTrue(first["shadow_decision_id"])
            second = planner.materialize_service_failure_automation_advisory(plan)
            self.assertFalse(second["active"])
            rows = [json.loads(line) for line in (state_dir / "closure-records.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(sum(row.get("object_type") == "service_failure_automation_obligation" for row in rows), 1)

    def test_existing_closure_owner_is_consumed_once_by_omp(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_test",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-26T00:00:00+00:00",
                "source_incident_id": "sfinc_test",
                "situation_id": "situation_test",
                "decision_trace_id": "decision_test",
                "stop_safe_classification": "STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")
            first = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(first["final_verdict"], "PASS")
            self.assertEqual(first["next_output"], "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR")
            second = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(second["final_verdict"], "NO_PENDING_OBLIGATION")

    def test_exact_execution_outcome_is_compared_without_replaying_or_applying(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            decision = {
                "record_type": self.autoswitch.shadow_autonomy.DECISION_RECORD_TYPE,
                "decision_id": "shadow_exact",
                "source_incident_id": "sfinc_exact",
                "recommended_action": "MOVE_USER",
            }
            outcome = {
                "schema_version": "v7.execution-outcome-feedback.v1",
                "operation_id": "op_exact",
                "source_incident_id": "sfinc_exact",
                "outcome_status": "success",
                "verification_result": {"success": True},
            }
            (state_dir / "shadow-autonomy-decisions.jsonl").write_text(json.dumps(decision) + "\n", encoding="utf-8")
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            result = planner.reconcile_service_failure_shadow_outcomes()
            self.assertTrue(result["active"])
            rows = [json.loads(line) for line in (state_dir / "shadow-autonomy-decisions.jsonl").read_text(encoding="utf-8").splitlines()]
            comparison = rows[-1]
            self.assertEqual(comparison["record_type"], self.autoswitch.shadow_autonomy.OUTCOME_COMPARISON_RECORD_TYPE)
            self.assertTrue(comparison["prediction_matched_observed_outcome"])
            self.assertFalse(comparison["runtime_mutation_performed"])
            self.assertFalse(comparison["apply_executed"])


if __name__ == "__main__":
    unittest.main()
