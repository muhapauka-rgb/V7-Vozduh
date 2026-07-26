import importlib.machinery
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_existing_closure_owner_is_consumed_once_across_processes(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_cross_process",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-26T00:00:00+00:00",
                "source_incident_id": "sfinc_cross_process",
                "situation_id": "situation_cross_process",
                "decision_trace_id": "decision_cross_process",
                "stop_safe_classification": "STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")
            script = """
import importlib.machinery, importlib.util, json, sys
loader = importlib.machinery.SourceFileLoader('sync_child', sys.argv[1])
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = module.consume_service_failure_automation_frontier(state_dir=module.Path(sys.argv[2]), persist_cps=False)
print(json.dumps({'verdict': result.get('final_verdict')}))
"""
            processes = [
                subprocess.Popen(
                    [sys.executable, "-c", script, str(ROOT / "tools/v7_sync_lib.py"), str(state_dir)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                )
                for _ in range(4)
            ]
            verdicts = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=30)
                self.assertEqual(process.returncode, 0, stderr)
                verdicts.append(json.loads(stdout)["verdict"])
            self.assertEqual(verdicts.count("PASS"), 1)
            self.assertEqual(verdicts.count("NO_PENDING_OBLIGATION"), 3)

    def test_safe_service_failure_successor_materializes_event_driven_reentry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "egress/state"
            state_dir.mkdir(parents=True)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_safe_successor",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-26T00:00:00+00:00",
                "source_incident_id": "sfinc_safe_successor",
                "situation_id": "situation_safe_successor",
                "decision_trace_id": "decision_safe_successor",
                "stop_safe_classification": "STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")

            atomic_result = {
                "ok": True,
                "status": "ATOMIC_UPDATE_COMPLETE",
                "post_write_reread": "PASS",
                "external_wake": {"dispatch_required": True},
            }
            with mock.patch.object(
                self.sync, "atomic_reconcile_cps", return_value=atomic_result,
            ) as atomic:
                result = self.sync.consume_service_failure_automation_frontier(
                    root=root, state_dir=state_dir, persist_cps=True,
                )

            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertTrue(result["atomic_update"]["external_wake"]["dispatch_required"])
            self.assertEqual(result["next_output"], "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR")
            self.assertTrue(atomic.call_args.kwargs["request_external_wake"])

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

    def test_shadow_allowed_action_boundary_never_grants_execution(self):
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        decisions = [{
            "user_ip": "10.0.0.2",
            "current_egress": "vless",
            "recommended_egress": "awg0",
        }]
        missing = planner._action_class_execution_boundary(
            decisions=decisions,
            selected=[],
            authority_budget_gate={"current_action_class_contract": {"valid": False, "blockers": ["contract_missing"]}},
            emergency_failover_gate={},
            restore_barrier_execution_gate={},
            intelligence_snapshot_gate={},
        )
        eligible = planner._action_class_execution_boundary(
            decisions=decisions,
            selected=[decisions[0]],
            authority_budget_gate={"current_action_class_contract": {"valid": True, "contract_id": "scoped"}},
            emergency_failover_gate={},
            restore_barrier_execution_gate={},
            intelligence_snapshot_gate={},
        )

        self.assertEqual(missing["status"], "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED")
        self.assertEqual(eligible["status"], "PACKET_MATERIALIZATION_ELIGIBLE")
        self.assertFalse(eligible["execution_authorized"])
        self.assertFalse(eligible["packet_created"])
        self.assertEqual(eligible["users_moved"], 0)

    def test_authority_stop_safe_emits_existing_policy_owner_request_without_grant(self):
        plan = {
            "operation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "certified_authority_class": "POOL",
                    "current_action_class_contract": {
                        "required": True,
                        "valid": False,
                        "blockers": ["current_action_class_contract_missing_or_schema_invalid"],
                    },
                },
                "l3_incident": {
                    "incident_id": "incident-1",
                    "incident_generation": "incident-generation-1",
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            policy_path.write_text("{}\n", encoding="utf-8")
            request = self.autoswitch.action_class_contract_reconciliation_request(
                plan, policy_path=policy_path,
            )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY")
        self.assertEqual(request["shadow_candidate"]["source_egress"], "vless")
        self.assertEqual(request["owner_issued_contract_template"]["max_users"], 1)
        self.assertEqual(request["owner_issued_contract_template"]["max_concurrent_transactions"], 1)
        self.assertTrue(request["authority_decision_request"]["request_id"])
        self.assertIn("existing /etc/v7/policy.json authority owner", request["next_consumer"])
        self.assertFalse(request["authority_granted"])
        self.assertFalse(request["contract_written"])
        self.assertFalse(request["runtime_apply"])
        self.assertEqual(request["users_moved"], 0)

    def test_authority_request_waits_for_independent_restore_barrier_before_issue(self):
        plan = {
            "operation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "certified_authority_class": "POOL",
                    "current_action_class_contract": {
                        "required": True,
                        "valid": False,
                        "blockers": ["current_action_class_contract_missing_or_schema_invalid"],
                    },
                },
                "l3_wake": {"accepted": True, "blockers": []},
                "l3_incident": {
                    "incident_id": "incident-1",
                    "incident_generation": "incident-generation-1",
                },
                "emergency_failover_autonomy": {
                    "blockers": [
                        "no_selected_moves_for_emergency_failover",
                        "restore_barrier_required_for_emergency_failover",
                    ],
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            policy_path.write_text("{}\n", encoding="utf-8")
            request = self.autoswitch.action_class_contract_reconciliation_request(
                plan, policy_path=policy_path,
            )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS")
        self.assertFalse(request["issue_preflight"]["ready"])
        self.assertEqual(
            request["pre_contract_execution_blockers"],
            ["restore_barrier_required_for_emergency_failover"],
        )
        self.assertIn("restore_barrier_required_for_emergency_failover", request["issue_preflight"]["blockers"])
        self.assertNotIn("no_selected_moves_for_emergency_failover", request["issue_preflight"]["blockers"])
        self.assertEqual(request["authority_classification"], "SAFE_PREDECESSOR_REQUIRED")
        self.assertEqual(
            request["exact_legal_next_action"],
            "RECONCILE_PACKET_BOUND_RESTORE_BARRIER_PREDECESSOR_ORDERING",
        )
        package = request["approval_package"]
        self.assertEqual(package["status"], "STOP_SAFE_NOT_ACTIONABLE_EXACT_PACKET_ABSENT")
        self.assertFalse(package["actionable"])
        self.assertTrue(package["request_id"])
        self.assertTrue(package["request_hash"])
        self.assertFalse(package["packet_identity"]["present"])
        self.assertEqual(package["packet_identity"]["packet_id"], "")
        self.assertEqual(package["scope"]["max_users"], 1)
        self.assertEqual(package["scope"]["max_concurrent_transactions"], 1)
        self.assertIn("restore_barrier_write", package["forbidden_effects"])
        self.assertFalse(request["authority_granted"])
        self.assertFalse(request["contract_written"])

    def test_authority_request_waits_for_snapshot_revalidation_before_policy_owner(self):
        plan = {
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": False, "blockers": ["contract_missing"]},
                },
                "intelligence_snapshots": {
                    "stop_required": True,
                    "unsafe_blocker": "source_hash_mismatch:service_matrix",
                },
            },
        }
        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS")
        self.assertFalse(request["issue_preflight"]["ready"])
        self.assertIn("source_hash_mismatch:service_matrix", request["issue_preflight"]["blockers"])
        self.assertIn("v7-intelligence-snapshot-refresh", request["next_consumer"])
        self.assertFalse(request["authority_granted"])

    def test_authority_request_waits_for_current_l3_wake_before_policy_owner(self):
        plan = {
            "operation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": False, "blockers": ["contract_missing"]},
                },
                "l3_incident": {
                    "incident_id": "incident-1",
                    "incident_generation": "incident-generation-1",
                },
                "l3_wake": {
                    "accepted": False,
                    "blockers": ["confirmed_l3_wake_required"],
                },
            },
        }

        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS")
        self.assertFalse(request["issue_preflight"]["ready"])
        self.assertFalse(request["issue_preflight"]["l3_wake_accepted"])
        self.assertIn("confirmed_l3_wake_required", request["issue_preflight"]["blockers"])
        self.assertIn("action-class contract reconciliation", request["next_consumer"])

    def test_active_contract_reenters_existing_boundary_without_new_request(self):
        plan = {
            "decisions": [],
            "safety": {
                "action_class_execution_boundary": {"status": "NO_ACTION_NO_SHADOW_CANDIDATE"},
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": True, "blockers": []},
                },
            },
        }
        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["status"], "CURRENT_ACTION_CLASS_CONTRACT_ACTIVE_REVALIDATE_EXISTING_CONSUMER")
        self.assertIn("action_class_execution_boundary", request["next_consumer"])
        self.assertFalse(request["contract_written"])

    def test_production_receipt_reconciles_source_cps_without_second_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_source_test",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_source_test",
                "source_incident_id": "sfinc_source_test",
                "situation_id": "situation_source_test",
                "decision_trace_id": "decision_source_test",
                "classification": "STOP_SAFE_AUTHORITY_REQUIRED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION",
                "next_action": "V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION",
                "runtime_mutation_performed": False,
                "routing_mutation_performed": False,
                "apply_executed": False,
                "authority_expanded": False,
                "production_maturity_changed": False,
                "users_moved": 0,
            }
            result = self.sync.reconcile_service_failure_automation_receipt_to_cps(receipt, root=root)
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertEqual(result["receipt"]["object_id"], "sfomp_source_test")
            self.assertTrue(result["atomic_update"]["ok"])


if __name__ == "__main__":
    unittest.main()
