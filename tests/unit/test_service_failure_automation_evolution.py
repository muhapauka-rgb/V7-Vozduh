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

from admin_core import operator_execution


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

    def test_packet_bound_execution_feedback_reconciles_only_its_existing_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_bound"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key, "incident_id": incident_id,
                        "incident_state": "OPEN", "channel_incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "next_required_consumer": "tools/v7_sync_lib.consume_service_failure_automation_frontier",
                        "reentry_condition": "fresh event", "causal_lineage": {},
                    },
                },
            }), encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb_bound", "source_channel": "vless", "target_channel": "awg3",
                "user": "10.0.0.2", "packet_id": "pkt_bound", "closure_reference": "operation_bound",
                "terminal_outcome_classification": "SUCCESS",
                "verification_result": {"success": True}, "learning_record": {"learning_record_id": "learn_bound"},
                "service_failure_causal_binding": {
                    "source_incident_id": incident_id, "source_event_id": "sfrev_bound",
                    "source_event_ids": ["sfrev_bound"], "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                },
            }
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            result = planner.reconcile_service_failure_execution_outcomes()
            repeated = planner.reconcile_service_failure_execution_outcomes()
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = state["incidents"][incident_key]
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["changed_records"], 1)
        self.assertEqual(repeated["changed_records"], 0)
        self.assertEqual(record["incident_state"], "PARTIALLY_PROTECTED")
        self.assertEqual(record["last_execution_feedback_id"], "execfb_bound")
        self.assertEqual(record["causal_lineage"]["source_event_ids"], ["sfrev_bound"])

    def test_execution_reconciliation_keeps_compact_incident_scope_balance(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_scope_bound"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg3 enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({"incidents": {
                incident_key: {
                    "incident_key": incident_key, "incident_id": incident_id,
                    "incident_state": "OPEN", "channel_incident_state": "OPEN",
                    "scope_accounting": {
                        "baseline_event_id": "sfrev_scope", "baseline_observed_at": "2026-07-27T03:00:00+00:00",
                        "affected_scope_count": 2, "affected_scope_fingerprint": "scopehash",
                    },
                },
            }}), encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_scope",
                "source_channel": "vless", "target_channel": "awg3", "user": "10.0.0.2", "packet_id": "pkt_scope",
                "terminal_outcome_classification": "SUCCESS", "outcome_observed_at": "2026-07-27T03:01:00+00:00",
                "verification_result": {"success": True},
                "service_failure_causal_binding": {
                    "source_incident_id": incident_id, "source_event_id": "sfrev_scope",
                    "source_event_ids": ["sfrev_scope"], "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                },
            }
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            first = planner.reconcile_service_failure_execution_outcomes()
            repeated = planner.reconcile_service_failure_execution_outcomes()
            record = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))["incidents"][incident_key]
        self.assertEqual(first["changed_records"], 1)
        self.assertEqual(repeated["changed_records"], 0)
        self.assertEqual(record["scope_accounting"]["status"], "ACCOUNTED")
        self.assertEqual(record["protected_scope_count"], 1)
        self.assertEqual(record["unresolved_scope_count"], 1)

    def test_exact_packet_bound_execution_feedback_updates_source_cps_without_new_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            feedback = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb_source_bound", "packet_id": "pkt_source_bound",
                "user": "10.0.0.2", "source_channel": "vless", "target_channel": "awg3",
                "terminal_outcome_classification": "SUCCESS",
                "verification_result": {"success": True},
                "execution_outcome": {"runtime_mutation_performed": True, "users_moved": 1},
                "service_failure_causal_binding": {
                    "source_incident_id": "sfinc_source_bound", "source_event_id": "sfrev_source_bound",
                    "source_event_ids": ["sfrev_source_bound"], "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                },
            }
            result = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
            repeated = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8"),
                "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry",
            ))
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertTrue(result["atomic_update"]["ok"])
        self.assertEqual(repeated["status"], "EXECUTION_FEEDBACK_ALREADY_CONSUMED")
        self.assertEqual(self.sync._plain_live_value(live, "LAST_SERVICE_FAILURE_EXECUTION_FEEDBACK_ID"), "execfb_source_bound")
        self.assertIn("PARTIALLY_PROTECTED", self.sync._plain_live_value(live, "CURRENT_VLESS_SERVICE_INCIDENT"))

    def test_accounted_scope_projects_active_incident_drain_into_source_cps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            feedback = {
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_scope_source", "packet_id": "pkt_scope_source",
                "user": "10.0.0.2", "source_channel": "vless", "target_channel": "awg3",
                "terminal_outcome_classification": "SUCCESS", "verification_result": {"success": True},
                "execution_outcome": {"runtime_mutation_performed": True, "users_moved": 1},
                "service_failure_causal_binding": {
                    "source_incident_id": "sfinc_scope_source", "source_event_id": "sfrev_scope_source",
                    "source_event_ids": ["sfrev_scope_source"], "event_type": "SERVICE_FAILURE_REVALIDATED", "source_channel": "vless",
                },
                "incident_scope_accounting": {
                    "status": "ACCOUNTED", "affected_scope_count": 5, "protected_scope_count": 1,
                    "unresolved_scope_count": 4, "explicitly_excluded_or_recovered_scope_count": 0,
                    "affected_scope_fingerprint": "scope-fingerprint", "raw_user_list_stored": False,
                },
            }
            result = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8"),
                "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry",
            ))
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertEqual(self.sync._plain_live_value(live, "CURRENT_VLESS_UNRESOLVED_SCOPE"), "4")
        self.assertEqual(self.sync._plain_live_value(live, "CURRENT_SAFE_NEXT_ACTION").split()[0], "CONTINUE")

    def test_advisory_skips_expired_terminal_and_selects_open_revalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            expiry = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_old",
                "source_incident_id": "sfinc_old",
                "situation_id": "situation_old",
                "decision_trace_id": "decision_old",
                "terminal_outcome_classification": "EPISODE_EXPIRED_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "vless",
                "observed_at": "2026-07-27T03:10:00+00:00",
            }
            revalidated = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_current",
                "source_incident_id": "sfinc_current",
                "situation_id": "situation_current",
                "decision_trace_id": "decision_current",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "vless",
                "observed_at": "2026-07-27T03:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in (revalidated, expiry)),
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            result = planner.materialize_service_failure_automation_advisory({
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                }],
            })
            self.assertTrue(result["active"])
            self.assertEqual(result["obligation"]["source_incident_id"], "sfinc_current")

    def test_passive_terminal_projects_compact_dual_lifecycle_and_omp_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_causal_1",
                "source_incident_id": "sfinc_causal_1",
                "source_event_ids": ["evt_causal_1"],
                "source_hashes": {"service_matrix": "a" * 64},
                "situation_id": "situation_causal_1",
                "decision_trace_id": "decision_causal_1",
                "learning_record_id": "learn_causal_1",
                "closure_state": "CAPTURED_STOP_SAFE",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "NATURAL_PRODUCTION_CANDIDATE",
                "channel": "vless",
                "services": ["service-a"],
                "failure_families": ["connection_reset"],
                "affected_users": ["10.0.0.2", "10.0.0.3"],
                "observed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}

            first = planner.reconcile_passive_causal_projections()
            self.assertEqual(first["final_verdict"], "PASS")
            self.assertEqual(first["changed_records"], 1)
            self.assertEqual(first["invalid_open_incidents"], 0)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertEqual(record["incident_state"], "OPEN")
            self.assertEqual(record["attempt_terminal"], "STOP_SAFE_NO_ACTION")
            self.assertEqual(record["intent_scope_type"], "COHORT")
            self.assertEqual(record["user_protection_intent"]["affected_users_count"], 2)
            self.assertFalse(record["user_protection_intent"]["raw_user_list_stored"])
            self.assertEqual(
                record["next_required_consumer"],
                "tools/v7-users-autoswitch.materialize_service_failure_automation_advisory",
            )
            self.assertTrue(record["reentry_condition"])
            self.assertFalse(record["runtime_mutation_performed"])
            self.assertEqual(record["users_moved"], 0)
            self.assertEqual(planner.reconcile_passive_causal_projections()["changed_records"], 0)

            advisory = planner.materialize_service_failure_automation_advisory({
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                }],
            })
            self.assertTrue(advisory["active"])
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertTrue(record["obligation_id"])
            self.assertEqual(
                record["next_required_consumer"],
                "tools/v7_sync_lib.consume_service_failure_automation_frontier",
            )
            self.assertIn("closure-records.lock", record["reentry_condition"])

    def test_closed_passive_recovery_closes_intent_without_erasing_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_recovered",
                "source_incident_id": "sfinc_recovered",
                "source_event_ids": ["evt_recovered"],
                "situation_id": "situation_recovered",
                "decision_trace_id": "decision_recovered",
                "learning_record_id": "learn_recovered",
                "terminal_outcome_classification": "RECOVERY_OBSERVED_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "vless",
                "affected_users": ["10.0.0.2"],
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}

            result = planner.reconcile_passive_causal_projections()
            self.assertEqual(result["final_verdict"], "PASS")
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertEqual(record["incident_state"], "INTENT_CLOSED")
            self.assertEqual(record["status"], "CLOSED")
            self.assertEqual(record["intent_closure_reason"], "RECOVERY_OBSERVED")
            self.assertEqual(record["causal_lineage"]["decision_trace_id"], "decision_recovered")
            self.assertEqual(record["users_moved"], 0)
            self.assertEqual(planner.reconcile_passive_causal_projections()["changed_records"], 0)

    def test_compact_projection_uses_only_latest_historical_terminal_per_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            old = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_history",
                "source_incident_id": "sfinc_history",
                "source_event_ids": ["evt_old"],
                "situation_id": "situation_old",
                "decision_trace_id": "decision_old",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "observed_at": "2026-07-26T00:00:00+00:00",
            }
            latest = {
                **old,
                "object_id": "sfinc_history_recovered",
                "source_event_ids": ["evt_new"],
                "situation_id": "situation_new",
                "decision_trace_id": "decision_new",
                "terminal_outcome_classification": "RECOVERY_OBSERVED_NO_ACTION",
                "observed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(
                json.dumps(old) + "\n" + json.dumps(latest) + "\n", encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}

            first = planner.reconcile_passive_causal_projections()
            self.assertEqual(first["projected_records"], 1)
            self.assertEqual(first["changed_records"], 1)
            self.assertEqual(planner.reconcile_passive_causal_projections()["changed_records"], 0)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertEqual(record["incident_state"], "INTENT_CLOSED")
            self.assertEqual(record["decision_trace_id"], "decision_new")

    def test_active_standing_policy_replaces_stale_one_use_authority_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_standing",
                "source_incident_id": "sfinc_standing",
                "situation_id": "situation_standing",
                "decision_trace_id": "decision_standing",
                "closure_state": "CAPTURED_STOP_SAFE",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "NATURAL_PRODUCTION_CANDIDATE",
                "channel": "vless",
                "affected_users": ["10.0.0.2"],
                "observed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            planner._standing_delegated_policy_status = lambda: {
                "valid": True,
                "blockers": [],
                "contract_id": "sdpc_test",
                "expires_at": "2026-08-27T00:00:00+00:00",
            }
            result = planner.materialize_service_failure_automation_advisory({
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                }],
            })
            obligation = result["obligation"]
            self.assertEqual(obligation["stop_safe_classification"], "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED")
            self.assertEqual(obligation["product_evolution_frontier"], "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION")
            self.assertEqual(
                obligation["action_class_execution_boundary"]["status"],
                "STANDING_DELEGATED_POLICY_ACTIVE_FRESH_EVENT_REVALIDATION_REQUIRED",
            )
            self.assertFalse(obligation["runtime_mutation_performed"])
            self.assertEqual(obligation["users_moved"], 0)

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

    def test_m2_receipt_is_materialized_into_existing_passive_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_key = "passive_m2_test"
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "schema_version": "v7.l3-runtime-state.v1",
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key,
                        "incident_id": "sfinc_m2_test",
                        "incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "next_required_consumer": "tools/v7_sync_lib.consume_service_failure_automation_frontier",
                        "reentry_condition": "ready obligation",
                        "transition_id": "ptr_m2_test",
                    },
                },
            }), encoding="utf-8")
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_m2_test",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-27T00:00:00+00:00",
                "incident_key": incident_key,
                "source_incident_id": "sfinc_m2_test",
                "situation_id": "situation_m2_test",
                "decision_trace_id": "decision_m2_test",
                "stop_safe_classification": "STOP_SAFE_DATA_OR_EVIDENCE_GAP",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")

            result = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(result["incident_projection_reconciliation"]["final_verdict"], "PASS")
            self.assertEqual(result["incident_projection_reconciliation"]["changed_records"], 1)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = state["incidents"][incident_key]
            self.assertEqual(record["omp_consumption_state"], "OMP_CONSUMED")
            self.assertTrue(record["omp_receipt_id"])
            self.assertEqual(record["next_required_consumer"], "tools/v7_sync_lib.continue_omp_engineering_control_loop")
            self.assertFalse(result["receipt"]["runtime_mutation_performed"])
            self.assertEqual(result["receipt"]["users_moved"], 0)

    def test_m2_repairs_interrupted_receipt_projection_without_second_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_key = "passive_m2_repair"
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "schema_version": "v7.l3-runtime-state.v1",
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key,
                        "incident_id": "sfinc_m2_repair",
                        "incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "next_required_consumer": "tools/v7_sync_lib.consume_service_failure_automation_frontier",
                        "reentry_condition": "ready obligation",
                        "transition_id": "ptr_m2_repair",
                    },
                },
            }), encoding="utf-8")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_m2_repair",
                "automation_obligation_id": "sfaob_m2_repair",
                "closure_state": "OMP_CONSUMED",
                "incident_key": incident_key,
                "source_incident_id": "sfinc_m2_repair",
                "next_action": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
                "consumed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(receipt) + "\n", encoding="utf-8")

            result = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(result["final_verdict"], "NO_PENDING_OBLIGATION", result)
            self.assertEqual(result["incident_projection_reconciliation"]["changed_records"], 1)
            rows = [json.loads(line) for line in (state_dir / "closure-records.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 1)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["incidents"][incident_key]["omp_receipt_id"], "sfomp_m2_repair")

    def test_m2_legacy_receipt_cannot_consume_new_generation_by_source_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_key = "passive_m2_strict"
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "schema_version": "v7.l3-runtime-state.v1",
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key,
                        "incident_id": "sfinc_same_source",
                        "incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "situation_id": "situation_new_generation",
                        "decision_trace_id": "decision_new_generation",
                        "next_required_consumer": "tools/v7-users-autoswitch.materialize_service_failure_automation_advisory",
                        "reentry_condition": "fresh current generation",
                    },
                },
            }), encoding="utf-8")
            stale_receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_stale",
                "automation_obligation_id": "sfaob_stale",
                "closure_state": "OMP_CONSUMED",
                "source_incident_id": "sfinc_same_source",
                "situation_id": "situation_old_generation",
                "decision_trace_id": "decision_old_generation",
                "next_action": "HISTORICAL",
                "consumed_at": "2026-07-26T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(stale_receipt) + "\n", encoding="utf-8")

            result = self.sync.reconcile_service_failure_omp_receipts_to_incident_state(state_dir=state_dir)
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertEqual(result["changed_records"], 0)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            self.assertNotIn("omp_receipt_id", state["incidents"][incident_key])

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

    def test_restore_barrier_is_post_contract_gate_not_m5a_circular_blocker(self):
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

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY")
        self.assertTrue(request["issue_preflight"]["ready"])
        self.assertEqual(
            request["pre_contract_execution_blockers"],
            [],
        )
        self.assertEqual(
            request["post_contract_operational_blockers"],
            ["restore_barrier_required_for_emergency_failover"],
        )
        self.assertNotIn("restore_barrier_required_for_emergency_failover", request["issue_preflight"]["blockers"])
        self.assertNotIn("no_selected_moves_for_emergency_failover", request["issue_preflight"]["blockers"])
        self.assertEqual(
            request["authority_classification"],
            "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
        )
        self.assertEqual(
            request["exact_legal_next_action"],
            "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST",
        )
        package = request["approval_package"]
        self.assertEqual(package["status"], "AWAITING_INDEPENDENT_AUTHORITY_DECISION")
        self.assertTrue(package["actionable"])
        self.assertTrue(package["request_id"])
        self.assertTrue(package["request_hash"])
        self.assertFalse(package["packet_identity"]["present"])
        self.assertEqual(package["packet_identity"]["packet_id"], "")
        self.assertEqual(package["scope"]["max_users"], 1)
        self.assertEqual(package["scope"]["max_concurrent_transactions"], 1)
        self.assertIn("restore_barrier_write", package["forbidden_effects"])
        self.assertFalse(request["authority_granted"])
        self.assertFalse(request["contract_written"])

    def test_valid_contract_reenters_packet_materialization_without_consumption(self):
        plan = {
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {"status": "PACKET_MATERIALIZATION_ELIGIBLE"},
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": True, "blockers": []},
                },
            },
        }
        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["authority_classification"], "SAFE_PACKET_MATERIALIZATION_PREDECESSOR_REQUIRED")
        self.assertEqual(request["exact_legal_next_action"], "REENTER_FRESH_PLANNER_FOR_PACKET_MATERIALIZATION")
        self.assertEqual(request["approval_package"]["status"], "SAFE_PACKET_MATERIALIZATION_PREDECESSOR_REQUIRED")
        self.assertFalse(request["approval_package"]["actionable"])
        self.assertFalse(request["packet_created"])
        self.assertFalse(request["lease_created"])
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

    def test_historical_safe_receipt_cannot_replace_active_standing_policy_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path)
            text = cps_path.read_text(encoding="utf-8")
            for field, value in (
                ("ACTIVE_PROGRAM", "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"),
                ("CURRENT_AUTHORITY_REQUEST_STATUS", "ACTIVE_OWNER_BACKED_STANDING_POLICY"),
                ("CURRENT_NEXT_ACTION_ID", "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION"),
            ):
                text = self.sync._replace_section_field(
                    text, "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry", field, f"`{value}`",
                )
            cps_path.write_text(text, encoding="utf-8")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_historical_safe", "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_historical_safe",
                "source_incident_id": "sfinc_historical_safe",
                "situation_id": "situation_historical_safe",
                "decision_trace_id": "decision_historical_safe",
                "classification": "CORRECT_SAFE_TERMINAL",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "NONE",
                "next_action": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "runtime_mutation_performed": False, "routing_mutation_performed": False,
                "apply_executed": False, "authority_expanded": False,
                "production_maturity_changed": False, "users_moved": 0,
            }
            result = self.sync.reconcile_service_failure_automation_receipt_to_cps(receipt, root=root)
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(result["status"], "HISTORICAL_RECEIPT_CONSUMED_ACTIVE_STANDING_POLICY_PRESERVED")
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                cps_path.read_text(encoding="utf-8"), "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
            ))
            self.assertEqual(self.sync._plain_live_value(live, "CURRENT_NEXT_ACTION_ID"), "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION")
            self.assertEqual(self.sync._plain_live_value(live, "LAST_SERVICE_FAILURE_RECEIPT_ID"), "sfomp_historical_safe")

    def test_fresh_m5a_request_is_atomically_projected_without_contract_or_packet(self):
        template = {
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "action_class": "GOVERNED_ONLY",
            "max_authority_class": "CANARY",
            "authority_ceiling": "CANARY",
            "policy_generation_hash": "a" * 64,
            "subject": {"user_ip": "10.0.0.2"},
            "scope": {"source_egress": "vless", "target_egress": "awg0"},
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "incident_generation": {"incident_id": "incident-1", "incident_generation": "incident-generation-1"},
            "source_generation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "verification_contract": {
                "owner": "tools/v7-users-autoswitch", "required": True,
                "immediate_and_temporal_observation": True, "success_criteria": "owner_verified",
            },
            "rollback_containment_contract": {
                "owner": "tools/v7-users-autoswitch", "required": True,
                "triggered_by_verifier": True, "direct_terminal_manufacture_forbidden": True,
            },
            "cooldown": {"required": True, "seconds": 180},
            "anti_flap": {"required": True, "same_source_target_repeat_forbidden": True},
            "stop_conditions": sorted(operator_execution.CURRENT_ACTION_CLASS_REQUIRED_STOP_CONDITIONS),
        }
        request = operator_execution.build_current_action_class_contract_authority_request(
            template, issue_preflight={"ready": True, "blockers": []},
        )
        package = {
            "schema_version": "v7.authority-normalized-approval-package.v1",
            "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION",
            "authority_classification": "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
            "actionable": True, "request_id": request["request_id"], "request_hash": request["request_hash"],
            "expires_at": request["expires_at"],
            "packet_identity": {"present": False, "packet_id": "", "packet_hash": ""},
            "forbidden_effects": [
                "contract_issuance", "policy_write", "restore_barrier_write", "candidate_creation",
                "execution_packet_or_lease_creation", "runtime_apply", "routing_mutation", "user_movement",
                "rollback_apply", "authority_expansion", "production_maturity_change",
            ],
        }
        reconciliation = {
            "schema_version": "v7.action-class-contract-reconciliation-request.v1",
            "status": "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY",
            "authority_classification": "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
            "exact_legal_next_action": "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST",
            "authority_decision_request": request, "approval_package": package,
            "authority_granted": False, "contract_written": False, "runtime_apply": False,
            "routing_mutation": False, "candidate_created": False, "packet_created": False,
            "lease_created": False, "users_moved": 0,
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path)
            result = self.sync.reconcile_action_class_contract_request_to_cps(reconciliation, root=root)
            self.assertEqual(result["final_verdict"], "PASS", result)
            text = cps_path.read_text(encoding="utf-8")
            self.assertIn(f"| `CURRENT_AUTHORITY_REQUEST_ID` | `{request['request_id']}` |", text)
            self.assertIn("| `CURRENT_PACKET` | `NONE` |", text)
            self.assertIn("| `CURRENT_LEASE` | `NONE` |", text)
            self.assertFalse(result["contract_written"])
            self.assertFalse(result["packet_created"])

    def test_m5a_request_projection_rejects_changed_request_identity(self):
        rejected = self.sync.reconcile_action_class_contract_request_to_cps({
            "schema_version": "v7.action-class-contract-reconciliation-request.v1",
            "status": "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY",
            "authority_classification": "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
            "exact_legal_next_action": "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST",
            "authority_decision_request": {"request_id": "changed"},
            "approval_package": {"schema_version": "v7.authority-normalized-approval-package.v1"},
            "authority_granted": False, "contract_written": False, "runtime_apply": False,
            "routing_mutation": False, "candidate_created": False, "packet_created": False,
            "lease_created": False, "users_moved": 0,
        })
        self.assertEqual(rejected["final_verdict"], "STOP_SAFE")
        self.assertIn("current_action_class_contract_request_schema_invalid", rejected["errors"])


if __name__ == "__main__":
    unittest.main()
