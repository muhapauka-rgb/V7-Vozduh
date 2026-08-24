import copy
import gzip
import json
import tempfile
import threading
import unittest
from unittest import mock
from datetime import datetime, timedelta, timezone
from pathlib import Path

from admin_core import autonomy_trust_acceleration, operator_execution
from admin_core.operator_execution import (
    AUTONOMOUS_EXECUTION_CONTROL_SCHEMA,
    CANONICAL_CLEARANCE_OWNER,
    EMPTY_SELECTED_MOVES_HASH,
    PacketError,
    RUNTIME_ACTION_CREATE_CLEARANCE,
    RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE,
    approved_packet_binding_status,
    autonomous_execution_control_decision,
    autonomous_execution_control_state,
    build_autonomous_execution_control_state,
    build_current_action_class_contract_authority_request,
    build_controlled_certification_substrate_authority_request,
    build_expiry_replacement_controlled_certification_substrate_request,
    build_standing_delegated_policy_authority_request,
    standing_delegated_operational_policy_template,
    standing_delegated_policy_contract_hash,
    standing_delegated_policy_runtime_axes,
    cancel_execution_lease,
    containment_forward_fix_classification,
    create_execution_lease_from_packet,
    create_execution_lease_from_preview,
    engineering_authority_binding_from_preview,
    engineering_authority_repair_continuation_policy_hash,
    execute_packet,
    execution_lease_state,
    extract_packet_preview,
    finish_execution_lease,
    issue_current_action_class_contract,
    consume_current_action_class_contract,
    consume_current_action_class_contract_to_policy,
    decline_current_action_class_contract_request,
    finalize_autonomous_execution_control_window,
    material_state_from_packet,
    packet_from_preview,
    packet_identity,
    packet_from_plan,
    preview_packet_identity,
    resolve_under_repo,
    rollback_operational_compensation_contract,
    runtime_recheck,
    selected_moves_from_plan,
    sha256_bytes,
    sha256_file,
    sha256_json,
    write_execution_lease,
    validate_engineering_authority_repair_continuation,
    validate_current_action_class_contract_authority_request,
    issue_current_action_class_contract_to_policy,
    issue_current_action_class_contract_from_audit,
    register_current_action_class_contract_request,
    current_action_class_contract_request_from_audit,
    issue_standing_delegated_policy_from_audit,
    latest_pending_standing_delegated_policy_request,
    register_standing_delegated_policy_request,
    register_controlled_certification_substrate_authority_request,
    record_controlled_certification_substrate_authority_decision,
    replace_expired_controlled_certification_substrate_request,
    controlled_certification_substrate_authority_status,
    controlled_certification_campaign_stage_status,
    controlled_certification_substrate_semantic_fingerprint,
    validate_controlled_certification_substrate_authority_request,
    validate_standing_delegated_operational_policy,
    validate_standing_delegated_policy_authority_request,
    read_audit_records,
    append_record,
)


def write_json(path, data):
    Path(path).write_text(json.dumps(data, sort_keys=True), encoding="utf-8")


def action_contract_template(policy_generation_hash="a" * 64):
    return {
        "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
        "action_class": "GOVERNED_ONLY",
        "max_authority_class": "POOL",
        "authority_ceiling": "POOL",
        "policy_generation_hash": policy_generation_hash,
        "subject": {"user_ip": "10.0.0.2"},
        "scope": {"source_egress": "vless", "target_egress": "awg3"},
        "max_users": 1,
        "max_concurrent_transactions": 1,
        "incident_generation": {"incident_id": "incident-1", "incident_generation": "generation-1"},
        "source_generation": {
            "planner_generation_id": "planner-1", "source_bundle_hash": "source-1",
            "snapshot_bundle_hash": "snapshot-1", "selected_move_hash": "move-1",
        },
        "verification_contract": {
            "owner": "tools/v7-users-autoswitch", "required": True,
            "immediate_and_temporal_observation": True, "success_criteria": "route_and_service_pass",
        },
        "rollback_containment_contract": {
            "owner": "tools/v7-users-autoswitch", "required": True,
            "triggered_by_verifier": True, "direct_terminal_manufacture_forbidden": True,
        },
        "cooldown": {"required": True, "seconds": 180},
        "anti_flap": {"required": True, "same_source_target_repeat_forbidden": True},
        "stop_conditions": [
            "no_safe_target", "stale_or_changed_situation", "selected_move_identity_changed",
            "target_capacity_or_service_gate_failed", "verification_failure", "rollback_required",
            "authority_decision_expired", "one_use_consumed_or_contended",
        ],
        "max_ttl_seconds": 300,
    }


def packet_template(state_dir, expires_delta=timedelta(hours=1)):
    users_hash = sha256_file(Path(state_dir) / "users.registry")
    egress_hash = sha256_file(Path(state_dir) / "egress.registry")
    snapshot_hash = sha256_bytes(json.dumps(
        {
            "egress_registry_hash": egress_hash,
            "selected_move_hash": EMPTY_SELECTED_MOVES_HASH,
            "users_registry_hash": users_hash,
        },
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8"))
    now = datetime.now(timezone.utc)
    return {
        "schema_version": "e22.operator-execution-packet.v1",
        "packet_id": "pkt_test",
        "approval_id": "appr_test",
        "operation_id": "E22_TEST",
        "selected_first_action": "ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK",
        "runtime_action": "RECHECK_AND_RECORD_ONLY",
        "created_at": now.isoformat(),
        "expires_at": (now + expires_delta).isoformat(),
        "approvals": [
            {"operator_id": "operator-a", "role": "approval_author", "confirmed_at": now.isoformat()},
            {"operator_id": "operator-b", "role": "approval_reviewer", "confirmed_at": now.isoformat()},
        ],
        "constraints": {
            "selected_move_budget": 0,
            "allowed_users": [],
            "allowed_targets": [],
            "user_movement_allowed": False,
            "routing_mutation_allowed": False,
        },
        "expected": {
            "users_registry_hash": users_hash,
            "egress_registry_hash": egress_hash,
            "runtime_snapshot_hash": snapshot_hash,
            "selected_move_hash": EMPTY_SELECTED_MOVES_HASH,
            "generation_id": "gen-test",
        },
    }


class OperatorExecutionPacketTest(unittest.TestCase):
    def test_packet_owner_accepts_only_exact_combined_topology_authority_scope(self):
        now = datetime(2026, 7, 29, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program=(
                    "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                ),
                max_users=48,
                include_controlled_topology=True,
                now=now,
            )
            register_standing_delegated_policy_request(
                request,
                audit_store=audit_path,
                now=now,
            )
            activated = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            contract = activated["contract"]
        policy = request["policy"]
        normalized = (
            autonomy_trust_acceleration.normalized_delegated_autonomy_scope(
                policy
            )
        )
        authority = {
            "authority_basis": "DELEGATED_AUTONOMY_POLICY",
            "policy_id": policy["policy_id"],
            "policy_scope_hash": request["policy_scope_hash"],
            "normalized_scope": normalized,
            "policy_state": policy["policy_state"],
            "current_mode": policy["current_mode"],
            "action_class": (
                operator_execution.CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS
            ),
            "max_users_per_transaction": 1,
            "max_concurrent_transactions": 1,
            "candidate_identity": "FRESH_ONLY",
            "packet_reuse": "FORBIDDEN",
            "self_expansion_allowed": False,
            "standing_policy_contract": contract,
            "authority_audit_verified": True,
        }
        packet = {
            "approvals": [],
            "delegated_policy_authority": authority,
        }
        errors = []
        operator_execution.validate_approvals(
            packet,
            errors,
            now=now + timedelta(seconds=1),
        )
        self.assertEqual(errors, [])

        service_failure = copy.deepcopy(packet)
        service_failure["delegated_policy_authority"]["action_class"] = (
            operator_execution.SERVICE_FAILURE_DELEGATED_ACTION_CLASSES[48]
        )
        service_failure["delegated_policy_authority"][
            "max_users_per_transaction"
        ] = 48
        service_errors = []
        operator_execution.validate_approvals(
            service_failure,
            service_errors,
            now=now + timedelta(seconds=1),
        )
        self.assertEqual(service_errors, [])

        narrowed_service_failure = copy.deepcopy(service_failure)
        narrowed_service_failure["delegated_policy_authority"][
            "max_users_per_transaction"
        ] = 4
        narrowed_service_errors = []
        operator_execution.validate_approvals(
            narrowed_service_failure,
            narrowed_service_errors,
            now=now + timedelta(seconds=1),
        )
        self.assertEqual(narrowed_service_errors, [])

        widened = copy.deepcopy(packet)
        widened["delegated_policy_authority"][
            "max_users_per_transaction"
        ] = 2
        widened_errors = []
        operator_execution.validate_approvals(
            widened,
            widened_errors,
            now=now + timedelta(seconds=1),
        )
        self.assertIn(
            "delegated_topology_blast_radius_invalid",
            widened_errors,
        )

    def test_packet_owner_accepts_only_narrowed_availability_first_stage(self):
        now = datetime(2026, 7, 30, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program=(
                    "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                ),
                max_users=48,
                include_availability_first=True,
                now=now,
            )
            register_standing_delegated_policy_request(
                request,
                audit_store=audit_path,
                now=now,
            )
            contract = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )["contract"]
        policy = request["policy"]
        authority = {
            "authority_basis": "DELEGATED_AUTONOMY_POLICY",
            "policy_id": policy["policy_id"],
            "policy_scope_hash": request["policy_scope_hash"],
            "normalized_scope": (
                autonomy_trust_acceleration
                .normalized_delegated_autonomy_scope(policy)
            ),
            "policy_state": policy["policy_state"],
            "current_mode": policy["current_mode"],
            "action_class": (
                operator_execution.AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
            ),
            "max_users_per_transaction": 5,
            "max_concurrent_transactions": 1,
            "candidate_identity": "FRESH_ONLY",
            "packet_reuse": "FORBIDDEN",
            "self_expansion_allowed": False,
            "standing_policy_contract": contract,
            "authority_audit_verified": True,
            "controlled_certification_target_id": "awg3",
            "availability_first_allocation_fingerprint": "a" * 64,
            "availability_first_subset_fingerprint": "b" * 64,
        }
        errors = []
        operator_execution.validate_approvals(
            {"approvals": [], "delegated_policy_authority": authority},
            errors,
            now=now + timedelta(seconds=1),
        )
        self.assertEqual(errors, [])

        widened = copy.deepcopy(authority)
        widened["max_users_per_transaction"] = 49
        widened_errors = []
        operator_execution.validate_approvals(
            {"approvals": [], "delegated_policy_authority": widened},
            widened_errors,
            now=now + timedelta(seconds=1),
        )
        self.assertIn(
            "delegated_availability_first_blast_radius_invalid",
            widened_errors,
        )

    def test_combined_standing_policy_extends_existing_owner_without_reinterpreting_legacy_scope(self):
        now = datetime(2026, 7, 29, tzinfo=timezone.utc)
        legacy = standing_delegated_operational_policy_template(max_users=48)
        legacy_scope = autonomy_trust_acceleration.normalized_delegated_autonomy_scope(
            legacy
        )
        legacy_hash = autonomy_trust_acceleration.delegated_autonomy_scope_hash(
            legacy
        )
        self.assertNotIn("policy_profile", legacy_scope)
        self.assertNotIn("action_class_scopes", legacy_scope)

        request = build_standing_delegated_policy_authority_request(
            policy_generation_hash="a" * 64,
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            max_users=48,
            include_controlled_topology=True,
            now=now,
        )
        validation = validate_standing_delegated_policy_authority_request(
            request,
            decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
            now=now,
        )
        self.assertTrue(validation["ok"], validation["errors"])
        policy = request["policy"]
        self.assertEqual(
            policy["policy_profile"],
            operator_execution.CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE,
        )
        self.assertIn(
            operator_execution.CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS,
            policy["allowed_action_classes"],
        )
        topology = policy["action_class_scopes"][
            operator_execution.CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS
        ]
        self.assertEqual(topology["max_users_per_transaction"], 1)
        self.assertEqual(topology["ordinary_identity_delta"], 0)
        self.assertEqual(topology["ordinary_route_delta"], 0)
        self.assertFalse(topology["ordinary_assignment_mutation_allowed"])
        self.assertFalse(topology["external_resource_creation_allowed"])
        self.assertFalse(topology["private_credential_mutation_allowed"])
        self.assertFalse(topology["authority_self_expansion_allowed"])
        self.assertNotEqual(
            request["policy_scope_hash"],
            legacy_hash,
        )
        self.assertEqual(
            autonomy_trust_acceleration.delegated_autonomy_scope_hash(legacy),
            legacy_hash,
        )

    def test_availability_first_standing_policy_is_one_exact_opt_in_envelope(self):
        now = datetime(2026, 7, 30, tzinfo=timezone.utc)
        legacy = standing_delegated_operational_policy_template(
            max_users=48,
            include_controlled_topology=True,
        )
        legacy_hash = autonomy_trust_acceleration.delegated_autonomy_scope_hash(
            legacy
        )

        request = build_standing_delegated_policy_authority_request(
            policy_generation_hash="a" * 64,
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            max_users=48,
            include_availability_first=True,
            now=now,
        )
        validation = validate_standing_delegated_policy_authority_request(
            request,
            decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
            now=now,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        policy = request["policy"]
        self.assertEqual(
            policy["policy_profile"],
            operator_execution.AVAILABILITY_FIRST_STANDING_POLICY_PROFILE,
        )
        self.assertIn(
            operator_execution.AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS,
            policy["allowed_action_classes"],
        )
        scope = policy["action_class_scopes"][
            operator_execution.AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
        ]
        self.assertEqual(scope["max_users_per_transaction"], 48)
        self.assertEqual(scope["max_concurrent_transactions"], 1)
        self.assertEqual(scope["ladder"], [1, 2, 5, 10, 25, 48])
        self.assertEqual(
            scope["ladder_stage_semantics"],
            "EXACT_TOTAL_COHORT_WITH_BASELINE_RESET",
        )
        self.assertTrue(scope["certification_identities_only"])
        self.assertFalse(scope["ordinary_assignment_mutation_allowed"])
        self.assertFalse(scope["ordinary_reclassification_allowed"])
        self.assertFalse(scope["shared_target_fault_injection_allowed"])
        self.assertFalse(scope["authority_self_expansion_allowed"])
        self.assertNotEqual(request["policy_scope_hash"], legacy_hash)
        self.assertEqual(
            autonomy_trust_acceleration.delegated_autonomy_scope_hash(legacy),
            legacy_hash,
        )
        self.assertNotIn("contract_id", request)
        self.assertFalse(request.get("authority_granted", False))

    def test_availability_first_standing_policy_activation_is_audited_and_fail_closed(self):
        now = datetime(2026, 7, 30, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program=(
                    "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                ),
                max_users=48,
                include_availability_first=True,
                now=now,
            )
            register_standing_delegated_policy_request(
                request,
                audit_store=audit_path,
                now=now,
            )
            activated = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            valid = validate_standing_delegated_operational_policy(
                activated["contract"],
                audit_records=read_audit_records(audit_path),
                now=now + timedelta(seconds=1),
            )
            self.assertTrue(valid["ok"], valid["errors"])

            malformed = copy.deepcopy(activated["contract"])
            availability = malformed["policy"]["action_class_scopes"][
                operator_execution.AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
            ]
            availability["shared_target_fault_injection_allowed"] = True
            malformed["contract_hash"] = standing_delegated_policy_contract_hash(
                malformed
            )
            malformed["contract_id"] = (
                f"sdpc_{malformed['contract_hash'][:24]}"
            )
            rejected = validate_standing_delegated_operational_policy(
                malformed,
                now=now + timedelta(seconds=1),
            )
            self.assertFalse(rejected["ok"])
            self.assertIn(
                "standing_delegated_policy_contract_scope_invalid",
                rejected["errors"],
            )

    def test_live_execution_lineage_option_keeps_runtime_clearance_after_rotation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audit_path = root / "operator-execution-audit.jsonl"
            runtime = {
                "record_type": "runtime_action_record_persisted",
                "record_hash": "a" * 64,
                "runtime_action_performed": True,
                "clearance_verdict": "RESTORE_BARRIER_CLEARANCE_WRITTEN",
                "packet_id": "pkt_stage25",
                "operation_id": "operation_stage25",
            }
            audit_path.write_text(
                json.dumps(runtime, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            audit_path.rename(root / "operator-execution-audit.jsonl.1")
            audit_path.write_text("", encoding="utf-8")
            compact = operator_execution.read_live_execution_lineage_records(
                audit_path,
            )
            recovery = operator_execution.read_live_execution_lineage_records(
                audit_path,
                include_runtime_actions=True,
            )
            self.assertFalse(any(row.get("packet_id") for row in compact))
            self.assertEqual(
                [row.get("packet_id") for row in recovery],
                ["pkt_stage25"],
            )

    def test_live_execution_lineage_process_cache_invalidates_on_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_path = Path(tmp) / "operator-execution-audit.jsonl"
            first = {
                "record_type": (
                    operator_execution
                    .CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE
                ),
                "record_hash": "a" * 64,
                "reservation_id": "sample-a",
            }
            second = {
                "record_type": (
                    operator_execution
                    .CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE
                ),
                "record_hash": "b" * 64,
                "reservation_id": "sample-a",
            }
            audit_path.write_text(
                json.dumps({"record_type": "irrelevant"})
                + "\n"
                + json.dumps(first)
                + "\n",
                encoding="utf-8",
            )
            initial = operator_execution.read_live_execution_lineage_records(
                audit_path,
            )
            initial[0]["reservation_id"] = "caller-mutated"
            cached = operator_execution.read_live_execution_lineage_records(
                audit_path,
            )
            self.assertEqual(
                [row.get("reservation_id") for row in cached],
                ["sample-a"],
            )
            with audit_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(second) + "\n")
            refreshed = (
                operator_execution.read_live_execution_lineage_records(
                    audit_path,
                )
            )
            self.assertEqual(
                [row.get("record_type") for row in refreshed],
                [
                    operator_execution
                    .CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE,
                    operator_execution
                    .CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE,
                ],
            )

    def test_live_execution_lineage_process_cache_extends_verified_chained_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_path = Path(tmp) / "operator-execution-audit.jsonl"
            decision_id = "decision-append-extension"
            operator_execution.append_record(
                audit_path,
                {
                    "record_type": (
                        operator_execution
                        .CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
                    ),
                    "decision_id": decision_id,
                },
            )
            first = operator_execution.read_live_execution_lineage_records(
                audit_path,
                required_decision_ids=(decision_id,),
            )
            operator_execution.append_record(
                audit_path,
                {
                    "record_type": (
                        operator_execution
                        .CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE
                    ),
                    "reservation_id": "sample-append-extension",
                },
            )
            with mock.patch(
                "builtins.open",
                side_effect=AssertionError("full lineage rescan"),
            ):
                extended = (
                    operator_execution.read_live_execution_lineage_records(
                        audit_path,
                        required_decision_ids=(decision_id,),
                    )
                )
            self.assertEqual(len(first), 1)
            self.assertEqual(
                [row.get("reservation_id") for row in extended if row.get("reservation_id")],
                ["sample-append-extension"],
            )

    def test_live_execution_lineage_process_cache_reuses_exact_generation_superset(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_path = Path(tmp) / "operator-execution-audit.jsonl"
            first_id = "decision-first"
            second_id = "decision-second"
            rows = [
                {
                    "record_type": (
                        operator_execution
                        .CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
                    ),
                    "decision_id": first_id,
                },
                {
                    "record_type": (
                        operator_execution
                        .STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE
                    ),
                    "decision_id": second_id,
                },
            ]
            audit_path.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )
            first = operator_execution.read_live_execution_lineage_records(
                audit_path,
                required_decision_ids=(first_id,),
            )
            with mock.patch("builtins.open", side_effect=AssertionError("audit reread")):
                second = operator_execution.read_live_execution_lineage_records(
                    audit_path,
                    required_decision_ids=(second_id,),
                )
            self.assertEqual(first, second)

    def test_live_execution_lineage_stops_after_exact_required_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audit_path = root / "operator-execution-audit.jsonl"
            decision_id = "ctm0f-decision-current"
            active = {
                "record_type": (
                    operator_execution
                    .CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE
                ),
                "reservation_id": "current-sample",
            }
            decision = {
                "record_type": (
                    operator_execution
                    .CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
                ),
                "decision_id": decision_id,
            }
            unrelated_older = {
                "record_type": (
                    operator_execution
                    .CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE
                ),
                "reservation_id": "older-unrelated-sample",
            }
            audit_path.write_text(json.dumps(active) + "\n", encoding="utf-8")
            audit_path.with_name(audit_path.name + ".1").write_text(
                json.dumps(decision) + "\n", encoding="utf-8",
            )
            audit_path.with_name(audit_path.name + ".2").write_text(
                json.dumps(unrelated_older) + "\n", encoding="utf-8",
            )
            records = operator_execution.read_live_execution_lineage_records(
                audit_path,
                required_decision_ids=(decision_id,),
            )
            self.assertEqual(
                [row.get("decision_id") or row.get("reservation_id") for row in records],
                [decision_id, "current-sample"],
            )

    def test_ct_m0f_lineage_checkpoint_keeps_new_build_on_live_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audit_path = root / "operator-execution-audit.jsonl"
            decision_id = "ctm0f-decision-checkpoint"
            availability_decision_id = "availability-decision-checkpoint"
            request_id = "ctm0f-request-checkpoint"
            request_hash = "a" * 64
            fingerprint = "b" * 64
            contract = {
                "contract_id": "ctm0fsdpc_checkpoint",
                "contract_hash": "c" * 64,
                "authority_decision": {
                    "decision": operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                    "decision_id": decision_id,
                    "request_id": request_id,
                    "request_hash": request_hash,
                },
            }
            decision = operator_execution.append_record(
                audit_path,
                {
                    "record_type": (
                        operator_execution
                        .CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
                    ),
                    "decision_id": decision_id,
                    "authority_request_id": request_id,
                    "authority_request_hash": request_hash,
                    "decision": (
                        operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL
                    ),
                },
            )
            availability_decision = operator_execution.append_record(
                audit_path,
                {
                    "record_type": (
                        operator_execution
                        .STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE
                    ),
                    "decision_id": availability_decision_id,
                },
            )
            audit_path.rename(root / "operator-execution-audit.jsonl.1")
            rotated = root / "operator-execution-audit.jsonl.1"
            with gzip.open(
                root / "operator-execution-audit.jsonl.1.gz",
                "wt",
                encoding="utf-8",
            ) as handle:
                handle.write(rotated.read_text(encoding="utf-8"))
            rotated.unlink()
            audit_path.write_text("", encoding="utf-8")
            lineage = operator_execution.read_live_execution_lineage_records(
                audit_path,
                required_decision_ids=(
                    decision_id,
                    availability_decision_id,
                ),
            )
            checkpoint = (
                operator_execution
                .ensure_ct_m0f_standing_validation_lineage_checkpoint(
                    contract,
                    fingerprint,
                    audit_store=audit_path,
                    audit_records=lineage,
                    supporting_authority_decision_ids=(
                        decision_id,
                        availability_decision_id,
                    ),
                )
            )
            self.assertEqual(checkpoint["status"], "CREATED")
            operator_execution.append_record(
                audit_path,
                {
                    "record_type": (
                        operator_execution
                        .CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE
                    ),
                    "contract_id": contract["contract_id"],
                    "implementation_fingerprint": "d" * 64,
                    "reservation_id": "unrelated-build-sample",
                },
            )
            operator_execution.append_record(
                audit_path,
                {
                    "record_type": "runtime_action_record_persisted",
                    "runtime_action_performed": True,
                    "clearance_verdict": (
                        "RESTORE_BARRIER_CLEARANCE_WRITTEN"
                    ),
                    "operation_id": "current-checkpoint-operation",
                },
            )
            operator_execution._LIVE_EXECUTION_LINEAGE_PROCESS_CACHE.clear()
            with mock.patch(
                "gzip.open",
                side_effect=AssertionError("rotated lineage reread"),
            ):
                compact = operator_execution.read_live_execution_lineage_records(
                    audit_path,
                    required_decision_ids=(
                        decision_id,
                        availability_decision_id,
                    ),
                    required_checkpoint_fingerprint=fingerprint,
                )
            anchors = [
                row for row in compact
                if row.get("record_type")
                == operator_execution
                .CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE
            ]
            self.assertEqual(len(anchors), 1)
            self.assertEqual(
                anchors[0]["source_authority_record_hash"],
                decision["record_hash"],
            )
            self.assertTrue(any(
                row.get("record_hash") == availability_decision["record_hash"]
                for row in compact
            ))
            self.assertFalse(any(
                row.get("reservation_id") == "unrelated-build-sample"
                for row in compact
            ))
            operator_execution._LIVE_EXECUTION_LINEAGE_PROCESS_CACHE.clear()
            with mock.patch(
                "gzip.open",
                side_effect=AssertionError("rotated lineage reread"),
            ):
                runtime = (
                    operator_execution.read_live_execution_lineage_records(
                        audit_path,
                        include_runtime_actions=True,
                        required_decision_ids=(decision_id,),
                        required_checkpoint_fingerprint=fingerprint,
                    )
                )
            self.assertTrue(any(
                row.get("operation_id") == "current-checkpoint-operation"
                for row in runtime
            ))

    def test_append_record_reads_only_last_predecessor_semantics(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_path = Path(tmp) / "operator-execution-audit.jsonl"
            first = {
                "record_type": "large_predecessor",
                "payload": "x" * 200000,
                "record_hash": "a" * 64,
            }
            audit_path.write_text(json.dumps(first) + "\n\n", encoding="utf-8")
            appended = operator_execution.append_record(
                audit_path,
                {"record_type": "bounded_successor", "created_at": "now"},
            )
            self.assertEqual(appended["previous_record_hash"], "a" * 64)
            self.assertEqual(
                operator_execution.read_last_audit_record(audit_path),
                appended,
            )

    def test_live_execution_lineage_keeps_authority_after_audit_rotation(self):
        now = datetime(2026, 7, 30, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "operator-execution-audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program=(
                    "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                ),
                max_users=48,
                include_availability_first=True,
                now=now,
            )
            register_standing_delegated_policy_request(
                request, audit_store=audit_path, now=now,
            )
            activated = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            audit_path.rename(root / "operator-execution-audit.jsonl.1")
            audit_path.write_text("", encoding="utf-8")
            lineage = operator_execution.read_live_execution_lineage_records(
                audit_path,
            )
            valid = validate_standing_delegated_operational_policy(
                activated["contract"],
                audit_records=lineage,
                now=now + timedelta(seconds=1),
            )
            self.assertTrue(valid["ok"], valid["errors"])

    def test_live_execution_lineage_keeps_controlled_topology_request_and_decision(self):
        now = datetime(2026, 8, 12, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audit_path = root / "operator-execution-audit.jsonl"
            manifest = {
                "validation_profile": "CT_M0F_ONE_USER_CONTROLLED_CONDITION",
                "selected_option": "OPTION_2_PROVISION_EXISTING_VALID_DRAFT",
                "existing_source": "source-1",
                "selected_source_or_draft": "draft-1",
                "trial_identity": "10.7.0.107",
                "trial_identity_count": 1,
                "identity_set_fingerprint": "d" * 64,
                "expected_assignment_delta": "10.7.0.107:source-1->NEW_DEDICATED_SOURCE",
                "expected_ordinary_assignment_delta": "NONE",
                "expected_ordinary_route_delta": "NONE",
                "capacity_reservation": 1,
                "certification_group": "ct-group",
                "reservation_mode": "INITIAL_EMPTY_CONTROLLED_SOURCE_RESERVATION",
                "max_concurrent_transactions": 1,
                "reservation_owner": "v7-egress-set-state",
                "verification": "fresh Matrix baseline",
                "rollback": "release exact reservation",
                "failure_mechanism": "existing controlled guard",
                "lease_and_expiry_required": True,
                "packet_required_before_effect": True,
                "restore_barrier_required_before_effect": True,
            }
            manifest["manifest_hash"] = operator_execution.sha256_json(manifest)
            request = {
                "schema_version": (
                    "v7.controlled-source-topology-authority-request.v1"
                ),
                "status": "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION",
                "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                "mission": "CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_SLICE_FEASIBILITY_V1",
                "decision_set": [
                    "APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
                    "DECLINE",
                ],
                "exact_action": "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
                "manifest": manifest,
                "authority_basis": {
                    "kind": "CT_M0F_STANDING_VALIDATION_POLICY",
                    "contract_id": "ct-contract",
                    "contract_hash": "b" * 64,
                    "authority_request_id": "ct-request",
                    "authority_request_hash": "c" * 64,
                    "expires_at": (now + timedelta(days=2)).isoformat(),
                },
                "current_campaign_request_id": "",
                "current_campaign_request_hash": "",
                "supersedes_source_binding_only": True,
                "tier48_capability_or_campaign_reapproval": False,
                "ordinary_customer_involvement": False,
                "self_expansion_allowed": False,
                "forbidden_effects": ["routing_mutation"],
                "reentry_condition": "one exact independent decision",
                "issuing_owner": "admin_core/operator_execution.py append-only Authority audit",
                "issuing_owner_required": "admin_core/operator_execution.py",
                "created_at": now.isoformat(),
                "expires_at": (now + timedelta(days=1)).isoformat(),
            }
            request["request_hash"] = operator_execution.controlled_source_topology_request_hash(request)
            request["request_id"] = f"cstopauth_r1_{request['request_hash'][:24]}"
            operator_execution.register_controlled_source_topology_authority_request(
                request, audit_store=audit_path, now=now,
            )
            operator_execution.record_controlled_source_topology_authority_decision(
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
                actor_id="unit-authority",
                audit_store=audit_path,
                now=now + timedelta(seconds=1),
            )
            audit_path.rename(root / "operator-execution-audit.jsonl.1")
            audit_path.write_text("", encoding="utf-8")
            lineage = operator_execution.read_live_execution_lineage_records(audit_path)
            status = operator_execution.controlled_source_topology_authority_status(
                lineage, now=now + timedelta(seconds=2),
            )
        self.assertEqual(status["status"], "APPROVED")
        self.assertEqual(status["request_id"], request["request_id"])
        expired = operator_execution.controlled_source_topology_authority_status(
            lineage, now=now + timedelta(days=1, seconds=1),
        )
        self.assertEqual(expired["status"], "EXPIRED")
        self.assertEqual(expired["decision"], "APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE")

    def test_availability_first_campaign_status_consumes_only_exact_prefix(self):
        now = datetime(2026, 7, 30, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program=(
                    "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                ),
                max_users=48,
                include_availability_first=True,
                now=now,
            )
            register_standing_delegated_policy_request(
                request,
                audit_store=audit_path,
                now=now,
            )
            contract = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )["contract"]
            initial = operator_execution.availability_first_campaign_stage_status(
                read_audit_records(audit_path),
                contract=contract,
                now=now + timedelta(seconds=1),
            )
            self.assertEqual(initial["next_stage"], 1)
            self.assertEqual(initial["completed_stages"], [])

            operator_execution.append_record(audit_path, {
                "record_type": (
                    operator_execution
                    .CONTROLLED_CERTIFICATION_CAMPAIGN_EFFECT_RECORD_TYPE
                ),
                "effect_class": (
                    operator_execution
                    .AVAILABILITY_FIRST_CAMPAIGN_STAGE_EFFECT_CLASS
                ),
                "receipt_id": "afstage_one",
                "standing_policy_contract_id": contract["contract_id"],
                "standing_policy_contract_hash": contract["contract_hash"],
                "campaign_stage": 1,
                "allocation_immutable": True,
                "capacity_reservation_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "per_user_verification_passed": True,
                "per_target_verification_passed": True,
                "aggregate_verification_passed": True,
                "ordinary_user_protection_passed": True,
                "baseline_reset_verified": True,
                "ordinary_customer_count": 0,
                "target_receipts": [{
                    "target_id": "awg3",
                    "verified_scope": 1,
                    "target_fingerprint": "a" * 64,
                    "capacity_bounds_fingerprint": "b" * 64,
                }],
            })
            advanced = operator_execution.availability_first_campaign_stage_status(
                read_audit_records(audit_path),
                contract=contract,
                now=now + timedelta(seconds=1),
            )
            self.assertTrue(advanced["ok"], advanced["blockers"])
            self.assertEqual(advanced["completed_stages"], [1])
            self.assertEqual(advanced["next_stage"], 2)
            self.assertEqual(
                advanced["target_proven_bounds"],
                {"awg3": 1},
            )
            operator_execution.append_record(audit_path, {
                "record_type": (
                    operator_execution
                    .CONTROLLED_CERTIFICATION_CAMPAIGN_EFFECT_RECORD_TYPE
                ),
                "effect_class": (
                    operator_execution
                    .AVAILABILITY_FIRST_TARGET_BOUND_EFFECT_CLASS
                ),
                "receipt_id": "aftbound_awg3_five",
                "standing_policy_contract_id": contract["contract_id"],
                "standing_policy_contract_hash": contract["contract_hash"],
                "campaign_next_stage": 25,
                "target_id": "awg3",
                "verified_scope": 5,
                "target_fingerprint": "c" * 64,
                "capacity_bounds_fingerprint": "d" * 64,
                "allocation_immutable": True,
                "capacity_reservation_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "per_user_verification_passed": True,
                "per_target_verification_passed": True,
                "aggregate_verification_passed": True,
                "ordinary_user_protection_passed": True,
                "baseline_reset_verified": True,
                "ordinary_customer_count": 0,
            })
            target_advanced = (
                operator_execution.availability_first_campaign_stage_status(
                    read_audit_records(audit_path),
                    contract=contract,
                    now=now + timedelta(seconds=1),
                )
            )
            self.assertTrue(
                target_advanced["ok"],
                target_advanced["blockers"],
            )
            self.assertEqual(target_advanced["next_stage"], 2)
            self.assertEqual(
                target_advanced["target_proven_bounds"],
                {"awg3": 5},
            )
            self.assertEqual(
                target_advanced["target_bound_receipt_ids"],
                ["aftbound_awg3_five"],
            )

    def test_combined_standing_policy_requires_independent_activation_and_fails_closed_on_scope_change(self):
        now = datetime(2026, 7, 29, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program=(
                    "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                ),
                max_users=48,
                include_controlled_topology=True,
                now=now,
            )
            topology_manifest = {
                "selected_option": "OPTION_1_REBIND_EXISTING_EMPTY_EGRESS",
                "existing_source": "source",
                "selected_source_or_draft": "vless",
                "trial_identity": "10.7.0.18",
                "trial_identity_count": 1,
                "identity_set_fingerprint": "b" * 64,
                "expected_assignment_delta": (
                    "10.7.0.18:source->vless"
                ),
                "expected_ordinary_assignment_delta": "NONE",
                "expected_ordinary_route_delta": "NONE",
                "capacity_reservation": 1,
                "max_concurrent_transactions": 1,
                "reservation_owner": "tools/v7-egress-set-state",
                "verification": "fresh Matrix baseline + current route",
                "rollback": (
                    "restore exact source binding and release reservation"
                ),
                "failure_mechanism": (
                    "existing controlled certification guard"
                ),
                "lease_and_expiry_required": True,
                "packet_required_before_effect": True,
                "restore_barrier_required_before_effect": True,
            }
            topology_manifest["manifest_hash"] = sha256_json(
                topology_manifest
            )
            topology_request = (
                operator_execution
                .build_controlled_source_topology_authority_request({
                    "active_program": (
                        "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                    ),
                    "mission": (
                        "CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_"
                        "SLICE_FEASIBILITY_V1"
                    ),
                    "exact_action": (
                        "REBIND_CONTROLLED_CERTIFICATION_SOURCE"
                    ),
                    "manifest": topology_manifest,
                    "current_campaign_request_id": "cpsauth_existing",
                    "current_campaign_request_hash": "c" * 64,
                    "supersedes_source_binding_only": True,
                    "tier48_capability_or_campaign_reapproval": False,
                    "ordinary_customer_involvement": False,
                    "self_expansion_allowed": False,
                    "forbidden_effects": ["ordinary_user_movement"],
                    "reentry_condition": "exact independent decision",
                }, now=now)
            )
            operator_execution.register_controlled_source_topology_authority_request(
                topology_request,
                audit_store=audit_path,
                now=now,
            )
            register_standing_delegated_policy_request(
                request,
                audit_store=audit_path,
                now=now,
            )
            self.assertNotIn(
                "delegated_autonomy_policy",
                json.loads(policy_path.read_text(encoding="utf-8")),
            )
            activated = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            valid = validate_standing_delegated_operational_policy(
                activated["contract"],
                audit_records=read_audit_records(audit_path),
                now=now + timedelta(seconds=1),
            )
            self.assertTrue(valid["ok"], valid["errors"])
            self.assertEqual(
                activated["superseded_one_off_topology_requests"][0][
                    "request_id"
                ],
                topology_request["request_id"],
            )
            topology_status = (
                operator_execution.controlled_source_topology_authority_status(
                    read_audit_records(audit_path),
                    now=now + timedelta(seconds=1),
                )
            )
            self.assertEqual(
                topology_status["status"],
                "SUPERSEDED_STALE_PREFLIGHT",
            )
            self.assertEqual(
                topology_status["invalidation_reason"],
                "SUPERSEDED_BY_STANDING_DELEGATED_"
                "CONTROLLED_TOPOLOGY_POLICY",
            )

            malformed = copy.deepcopy(activated["contract"])
            malformed["policy"]["action_class_scopes"][
                operator_execution.CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS
            ]["ordinary_assignment_mutation_allowed"] = True
            malformed["contract_hash"] = standing_delegated_policy_contract_hash(
                malformed
            )
            malformed["contract_id"] = (
                f"sdpc_{malformed['contract_hash'][:24]}"
            )
            invalid = validate_standing_delegated_operational_policy(
                malformed,
                now=now + timedelta(seconds=1),
            )
            self.assertFalse(invalid["ok"])
            self.assertIn(
                "standing_delegated_policy_contract_scope_invalid",
                invalid["errors"],
            )

    def test_standing_delegated_policy_requires_exact_registered_authority_and_activates_once(self):
        now = datetime(2026, 7, 26, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                now=now,
            )
            validation = validate_standing_delegated_policy_authority_request(
                request,
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                expected_request_id=request["request_id"],
                expected_request_hash=request["request_hash"],
                now=now,
            )
            self.assertTrue(validation["ok"], validation["errors"])
            registration = register_standing_delegated_policy_request(
                request, audit_store=audit_path, now=now,
            )
            self.assertEqual(registration["status"], "REGISTERED")
            result = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            self.assertEqual(result["status"], "ACTIVATED")
            self.assertEqual(result["users_moved"], 0)
            self.assertFalse(result["runtime_apply"])
            live = json.loads(policy_path.read_text(encoding="utf-8"))["delegated_autonomy_policy"]
            live_validation = validate_standing_delegated_operational_policy(
                live, now=now + timedelta(days=1),
            )
            self.assertTrue(live_validation["ok"], live_validation["errors"])
            self.assertEqual(live_validation["policy"]["max_users_per_action"], 1)
            self.assertEqual(live_validation["policy"]["max_concurrent_transactions"], 1)
            expired = validate_standing_delegated_operational_policy(
                live, now=now + timedelta(days=31),
            )
            self.assertFalse(expired["ok"])
            self.assertIn("standing_delegated_policy_contract_expired", expired["errors"])
            with self.assertRaisesRegex(PacketError, "decision_already_recorded"):
                issue_standing_delegated_policy_from_audit(
                    policy_path,
                    request_id=request["request_id"],
                    request_hash=request["request_hash"],
                    decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                    audit_store=audit_path,
                    actor_id="unit-authority",
                    now=now,
                )

    def test_standing_delegated_policy_request_and_contract_expire_fail_closed(self):
        now = datetime(2026, 7, 26, tzinfo=timezone.utc)
        request = build_standing_delegated_policy_authority_request(
            policy_generation_hash="a" * 64,
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            now=now,
        )
        validation = validate_standing_delegated_policy_authority_request(
            request,
            decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
            now=now + timedelta(days=1, seconds=1),
        )
        self.assertFalse(validation["ok"])
        self.assertIn("standing_delegated_policy_request_expired", validation["errors"])

    def test_latest_pending_standing_policy_request_reuses_audit_and_excludes_decided(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                max_users=4,
                now=now,
            )
            register_standing_delegated_policy_request(
                request, audit_store=audit_path, now=now,
            )
            pending = latest_pending_standing_delegated_policy_request(
                read_audit_records(audit_path),
                now=now + timedelta(seconds=1),
            )
            self.assertEqual(pending["status"], "PENDING")
            self.assertEqual(pending["pending_count"], 1)
            self.assertEqual(pending["request"]["request_id"], request["request_id"])
            self.assertEqual(pending["request"]["policy"]["max_users_per_action"], 4)

            issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now + timedelta(seconds=2),
            )
            consumed = latest_pending_standing_delegated_policy_request(
                read_audit_records(audit_path),
                now=now + timedelta(seconds=3),
            )
            self.assertEqual(consumed["status"], "NONE")
            self.assertEqual(consumed["pending_count"], 0)

    def test_tier4_standing_policy_is_decidable_but_does_not_activate_without_authority(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(policy_path),
                active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                max_users=4,
                now=now,
            )
            validation = validate_standing_delegated_policy_authority_request(
                request,
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                now=now,
            )
            self.assertTrue(validation["ok"], validation["errors"])
            self.assertEqual(request["policy"]["max_users_per_action"], 4)
            self.assertEqual(request["policy"]["max_concurrent_transactions"], 1)
            self.assertEqual(
                request["policy"]["allowed_action_classes"],
                ["channel hard-fail failover"],
            )
            self.assertEqual(request["per_action_law"]["max_users"], 4)
            self.assertEqual(request["status"], "AWAITING_INDEPENDENT_AUTHORITY_DECISION")
            register_standing_delegated_policy_request(
                request, audit_store=audit_path, now=now,
            )
            activated = issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            live = activated["contract"]
            self.assertEqual(live["policy"]["max_users_per_action"], 4)
            self.assertTrue(
                validate_standing_delegated_operational_policy(
                    live,
                    now=now + timedelta(seconds=1),
                )["ok"]
            )

    def test_tier48_standing_policy_request_is_exact_and_non_activating(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        request = build_standing_delegated_policy_authority_request(
            policy_generation_hash="a" * 64,
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            max_users=48,
            now=now,
        )
        validation = validate_standing_delegated_policy_authority_request(
            request,
            decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
            now=now,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(request["status"], "AWAITING_INDEPENDENT_AUTHORITY_DECISION")
        self.assertEqual(request["policy"]["max_users_per_action"], 48)
        self.assertEqual(request["policy"]["max_concurrent_transactions"], 1)
        self.assertEqual(
            request["policy"]["allowed_action_classes"],
            ["channel hard-fail failover"],
        )
        self.assertEqual(request["per_action_law"]["max_users"], 48)
        self.assertFalse(request["policy"]["self_expansion_allowed"])
        self.assertNotIn("contract_id", request)
        self.assertNotIn("contract_hash", request)

    def test_tier48_runtime_axes_separate_controlled_from_ordinary_proof(self):
        request = build_standing_delegated_policy_authority_request(
            policy_generation_hash="a" * 64,
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            max_users=48,
            now=datetime(2026, 7, 28, tzinfo=timezone.utc),
        )
        contract = {
            "policy": request["policy"],
            "contract_id": "historical",
            "contract_hash": "historical",
        }
        axes = standing_delegated_policy_runtime_axes(contract)

        self.assertEqual(axes["authority_approved_max"], 48)
        self.assertEqual(axes["controlled_certification_runtime_max"], 48)
        self.assertEqual(axes["ordinary_production_runtime_max"], 4)
        self.assertEqual(axes["controlled_production_proven_max"], 0)
        self.assertEqual(axes["ordinary_production_proven_max"], 4)
        self.assertFalse(axes["contract_rewritten"])
        self.assertFalse(axes["authority_expanded"])

    def test_controlled_certification_substrate_request_is_one_exact_non_transitive_package(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        pool = {
            "total_enabled_certification_users": 4,
            "max_enabled_certification_users_on_one_active_source": 3,
            "fingerprint": "f" * 64,
            "registry_hashes": {
                "users_registry": "a" * 64,
                "egress_registry": "b" * 64,
            },
        }
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled-source",
            current_pool_status=pool,
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            now=now,
        )
        validation = validate_controlled_certification_substrate_authority_request(
            request,
            decision="DECLINE",
            now=now,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(request["scope"]["campaign_stages"], [5, 10, 25, 48])
        self.assertEqual(request["scope"]["target_total_certification_identities"], 48)
        self.assertEqual(request["scope"]["max_new_certification_identities"], 45)
        self.assertFalse(request["scope"]["ordinary_customer_involvement"])
        self.assertTrue(request["subscope_law"]["no_implicit_cross_grant"])
        self.assertEqual(
            {row["id"] for row in request["coordinated_subscopes"]},
            {
                "IDENTITY_PROVISIONING",
                "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT",
                "CONTROLLED_SOURCE_CONDITION",
                "PROGRESSIVE_CAMPAIGN_EXECUTION",
            },
        )
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            first = register_controlled_certification_substrate_authority_request(
                request,
                audit_store=audit,
                now=now,
            )
            second = register_controlled_certification_substrate_authority_request(
                request,
                audit_store=audit,
                now=now,
            )
        self.assertEqual(first["status"], "REGISTERED")
        self.assertEqual(second["status"], "ALREADY_REGISTERED_EXACT")

    def test_ct_m0f_one_user_substrate_is_setup_only_and_non_campaign(self):
        now = datetime(2026, 8, 16, tzinfo=timezone.utc)
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled-source",
            current_pool_status={
                "total_enabled_certification_users": 0,
                "max_enabled_certification_users_on_one_active_source": 0,
                "fingerprint": "f" * 64,
                "registry_hashes": {"users_registry": "a" * 64, "egress_registry": "b" * 64},
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            profile=operator_execution.CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE,
            now=now,
        )
        validation = validate_controlled_certification_substrate_authority_request(
            request, decision="DECLINE", now=now,
        )
        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(request["scope"]["target_total_certification_identities"], 1)
        self.assertEqual(request["scope"]["max_new_certification_identities"], 1)
        self.assertEqual(request["scope"]["campaign_stages"], [1])
        self.assertFalse(request["scope"]["automatic_stage_progression"])
        self.assertEqual(
            {row["id"] for row in request["coordinated_subscopes"]},
            {"IDENTITY_PROVISIONING", "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT"},
        )

    def test_controlled_substrate_decision_is_exact_once_and_audit_only(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled-source",
            current_pool_status={
                "total_enabled_certification_users": 4,
                "max_enabled_certification_users_on_one_active_source": 3,
                "fingerprint": "f" * 64,
                "registry_hashes": {
                    "users_registry": "a" * 64,
                    "egress_registry": "b" * 64,
                },
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            now=now,
        )
        admitted = [
            "IDENTITY_PROVISIONING",
            "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT",
            "CONTROLLED_SOURCE_CONDITION",
            "PROGRESSIVE_CAMPAIGN_EXECUTION",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            register_controlled_certification_substrate_authority_request(
                request, audit_store=audit, now=now,
            )
            first = record_controlled_certification_substrate_authority_decision(
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN",
                actor_id="independent-authority-owner",
                admitted_subscopes=admitted,
                audit_store=audit,
                now=now + timedelta(minutes=1),
            )
            second = record_controlled_certification_substrate_authority_decision(
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN",
                actor_id="independent-authority-owner",
                admitted_subscopes=admitted,
                audit_store=audit,
                now=now + timedelta(minutes=2),
            )
            records = read_audit_records(audit)
            status = controlled_certification_substrate_authority_status(
                records, now=now + timedelta(minutes=2),
            )
        self.assertEqual(first["status"], "APPROVED")
        self.assertEqual(second["status"], "ALREADY_RECORDED_EXACT")
        self.assertTrue(first["audit_write"])
        self.assertFalse(second["audit_write"])
        self.assertFalse(first["policy_write"])
        self.assertFalse(first["runtime_apply"])
        self.assertEqual(first["users_moved"], 0)
        self.assertEqual(status["status"], "APPROVED")
        self.assertEqual(status["decision_id"], first["decision_id"])
        self.assertEqual(
            len([
                row for row in records
                if row.get("record_type")
                == "controlled_certification_substrate_authority_decision"
            ]),
            1,
        )

    def test_controlled_campaign_stage_projection_requires_ordered_exact_receipts(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled-source",
            current_pool_status={
                "total_enabled_certification_users": 48,
                "max_enabled_certification_users_on_one_active_source": 48,
                "fingerprint": "f" * 64,
                "registry_hashes": {
                    "users_registry": "a" * 64,
                    "egress_registry": "b" * 64,
                },
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            now=now,
        )
        admitted = [
            "IDENTITY_PROVISIONING",
            "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT",
            "CONTROLLED_SOURCE_CONDITION",
            "PROGRESSIVE_CAMPAIGN_EXECUTION",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            register_controlled_certification_substrate_authority_request(
                request, audit_store=audit, now=now,
            )
            record_controlled_certification_substrate_authority_decision(
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=(
                    "APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN"
                ),
                actor_id="independent-authority-owner",
                admitted_subscopes=admitted,
                audit_store=audit,
                now=now + timedelta(minutes=1),
            )
            append_record(audit, {
                "record_type": "controlled_certification_substrate_effect",
                "effect_class": (
                    "CONTROLLED_SERVICE_FAILURE_CAMPAIGN_STAGE_CONSUMED"
                ),
                "receipt_id": "cpsstage_5",
                "authority_request_id": request["request_id"],
                "authority_request_hash": request["request_hash"],
                "campaign_stage": 5,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "baseline_reset_verified": True,
                "ordinary_customer_count": 0,
            })
            progress = controlled_certification_campaign_stage_status(
                read_audit_records(audit),
                now=now + timedelta(minutes=2),
            )
            self.assertTrue(progress["ok"], progress)
            self.assertEqual(progress["completed_stages"], [5])
            self.assertEqual(progress["controlled_production_proven_max"], 5)
            self.assertEqual(progress["next_stage"], 10)

            append_record(audit, {
                "record_type": "controlled_certification_substrate_effect",
                "effect_class": (
                    "CONTROLLED_SERVICE_FAILURE_CAMPAIGN_STAGE_CONSUMED"
                ),
                "receipt_id": "cpsstage_5_duplicate",
                "authority_request_id": request["request_id"],
                "authority_request_hash": request["request_hash"],
                "campaign_stage": 5,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "baseline_reset_verified": True,
                "ordinary_customer_count": 0,
            })
            duplicate = controlled_certification_campaign_stage_status(
                read_audit_records(audit),
                now=now + timedelta(minutes=3),
            )
        self.assertFalse(duplicate["ok"])
        self.assertIn(
            "controlled_campaign_stage_duplicate:5",
            duplicate["blockers"],
        )

    def test_controlled_substrate_request_can_reuse_pool_with_exact_execution_target(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled",
            controlled_target_id="execution",
            controlled_target_admission={
                "role": "EXECUTION_ONLY",
                "reservation_owner": "operator_execution_governance",
                "execution_reserved": True,
                "canary_reserved": True,
                "enabled_assigned_users": 0,
                "fingerprint": "f" * 64,
            },
            current_pool_status={
                "total_enabled_certification_users": 48,
                "max_enabled_certification_users_on_one_active_source": 48,
                "fingerprint": "e" * 64,
                "registry_hashes": {
                    "users_registry": "a" * 64,
                    "egress_registry": "b" * 64,
                },
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            now=now,
        )
        validation = validate_controlled_certification_substrate_authority_request(
            request,
            decision="DECLINE",
            now=now,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(
            request["scope"]["identity_strategy"],
            "REUSE_EXISTING_VALID_POOL",
        )
        self.assertEqual(
            request["scope"]["max_new_certification_identities"],
            0,
        )
        self.assertEqual(
            request["scope"]["controlled_target_id"],
            "execution",
        )
        self.assertFalse(
            request["controlled_target_contract"][
                "ordinary_production_assignment_allowed"
            ]
        )

    def test_controlled_substrate_concurrent_consumers_append_one_decision(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled-source",
            current_pool_status={
                "total_enabled_certification_users": 4,
                "max_enabled_certification_users_on_one_active_source": 3,
                "fingerprint": "f" * 64,
                "registry_hashes": {
                    "users_registry": "a" * 64,
                    "egress_registry": "b" * 64,
                },
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            now=now,
        )
        admitted = [
            "IDENTITY_PROVISIONING",
            "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT",
            "CONTROLLED_SOURCE_CONDITION",
            "PROGRESSIVE_CAMPAIGN_EXECUTION",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            register_controlled_certification_substrate_authority_request(
                request, audit_store=audit, now=now,
            )
            results = []
            errors = []

            def consume():
                try:
                    results.append(
                        record_controlled_certification_substrate_authority_decision(
                            request_id=request["request_id"],
                            request_hash=request["request_hash"],
                            decision="APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN",
                            actor_id="independent-authority-owner",
                            admitted_subscopes=admitted,
                            audit_store=audit,
                            now=now + timedelta(minutes=1),
                        )
                    )
                except Exception as exc:  # pragma: no cover - captured for assertion
                    errors.append(str(exc))

            threads = [threading.Thread(target=consume) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            records = read_audit_records(audit)
        self.assertFalse(errors, errors)
        self.assertEqual(
            sorted(row["status"] for row in results),
            ["ALREADY_RECORDED_EXACT", "APPROVED"],
        )
        self.assertEqual(
            len([
                row for row in records
                if row.get("record_type")
                == "controlled_certification_substrate_authority_decision"
            ]),
            1,
        )

    def test_controlled_substrate_decision_rejects_incomplete_or_stale_input(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled-source",
            current_pool_status={
                "total_enabled_certification_users": 4,
                "max_enabled_certification_users_on_one_active_source": 3,
                "fingerprint": "f" * 64,
                "registry_hashes": {
                    "users_registry": "a" * 64,
                    "egress_registry": "b" * 64,
                },
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            now=now,
        )
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            register_controlled_certification_substrate_authority_request(
                request, audit_store=audit, now=now,
            )
            with self.assertRaisesRegex(
                PacketError, "approval_subscopes_incomplete",
            ):
                record_controlled_certification_substrate_authority_decision(
                    request_id=request["request_id"],
                    request_hash=request["request_hash"],
                    decision="APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN",
                    actor_id="owner",
                    admitted_subscopes=["IDENTITY_PROVISIONING"],
                    audit_store=audit,
                    now=now + timedelta(minutes=1),
                )
            with self.assertRaisesRegex(PacketError, "actor_missing"):
                record_controlled_certification_substrate_authority_decision(
                    request_id=request["request_id"],
                    request_hash=request["request_hash"],
                    decision="DECLINE",
                    actor_id="",
                    audit_store=audit,
                    now=now + timedelta(minutes=1),
                )
            with self.assertRaisesRegex(PacketError, "hash_mismatch"):
                record_controlled_certification_substrate_authority_decision(
                    request_id=request["request_id"],
                    request_hash="0" * 64,
                    decision="DECLINE",
                    actor_id="owner",
                    audit_store=audit,
                    now=now + timedelta(minutes=1),
                )
            with self.assertRaisesRegex(PacketError, "expired"):
                record_controlled_certification_substrate_authority_decision(
                    request_id=request["request_id"],
                    request_hash=request["request_hash"],
                    decision="DECLINE",
                    actor_id="owner",
                    audit_store=audit,
                    now=now + timedelta(days=2),
                )
            records = read_audit_records(audit)
        self.assertFalse(any(
            row.get("record_type")
            == "controlled_certification_substrate_authority_decision"
            for row in records
        ))

    def test_expiry_replacement_preserves_semantics_and_single_active_request(self):
        now = datetime(2026, 7, 28, tzinfo=timezone.utc)
        request = build_controlled_certification_substrate_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="controlled-source",
            current_pool_status={
                "total_enabled_certification_users": 4,
                "max_enabled_certification_users_on_one_active_source": 3,
                "fingerprint": "f" * 64,
                "registry_hashes": {
                    "users_registry": "a" * 64,
                    "egress_registry": "b" * 64,
                },
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="c" * 64,
            now=now,
        )
        replacement_time = now + timedelta(days=2)
        direct = build_expiry_replacement_controlled_certification_substrate_request(
            request, now=replacement_time,
        )
        self.assertEqual(
            controlled_certification_substrate_semantic_fingerprint(request),
            controlled_certification_substrate_semantic_fingerprint(direct),
        )
        self.assertEqual(
            direct["supersession"]["supersedes_request_id"],
            request["request_id"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            register_controlled_certification_substrate_authority_request(
                request, audit_store=audit, now=now,
            )
            result = replace_expired_controlled_certification_substrate_request(
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                audit_store=audit,
                now=replacement_time,
            )
            records = read_audit_records(audit)
            status = controlled_certification_substrate_authority_status(
                records, now=replacement_time,
            )
        self.assertEqual(result["status"], "EXPIRY_REPLACEMENT_REGISTERED")
        self.assertEqual(status["status"], "PENDING")
        self.assertEqual(status["request_id"], result["request"]["request_id"])
        self.assertEqual(
            status["semantic_request_fingerprint"],
            controlled_certification_substrate_semantic_fingerprint(request),
        )

    def test_current_action_contract_requires_existing_authority_decision_and_one_use_provenance(self):
        template = {
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "action_class": "GOVERNED_ONLY",
            "max_authority_class": "POOL",
            "subject": {"user_ip": "10.0.0.2"},
            "scope": {"source_egress": "vless", "target_egress": "awg3"},
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "incident_generation": {"incident_id": "incident-1", "incident_generation": "generation-1"},
            "source_generation": {
                "planner_generation_id": "planner-1",
                "source_bundle_hash": "source-1",
                "snapshot_bundle_hash": "snapshot-1",
                "selected_move_hash": "move-1",
            },
            "policy_generation_hash": "a" * 64,
            "authority_ceiling": "POOL",
            "verification_contract": {
                "owner": "tools/v7-users-autoswitch", "required": True,
                "immediate_and_temporal_observation": True, "success_criteria": "route_and_service_pass",
            },
            "rollback_containment_contract": {
                "owner": "tools/v7-users-autoswitch", "required": True,
                "triggered_by_verifier": True, "direct_terminal_manufacture_forbidden": True,
            },
            "cooldown": {"required": True, "seconds": 180},
            "anti_flap": {"required": True, "same_source_target_repeat_forbidden": True},
            "stop_conditions": [
                "no_safe_target", "stale_or_changed_situation", "selected_move_identity_changed",
                "target_capacity_or_service_gate_failed", "verification_failure", "rollback_required",
                "authority_decision_expired", "one_use_consumed_or_contended",
            ],
            "max_ttl_seconds": 300,
        }
        request = build_current_action_class_contract_authority_request(
            template, issue_preflight={"ready": True, "blockers": []},
        )
        valid = validate_current_action_class_contract_authority_request(
            request, decision="APPROVE_ONCE_AS_SCOPED",
            expected_request_id=request["request_id"], expected_request_hash=request["request_hash"],
        )
        self.assertTrue(valid["ok"], valid["errors"])
        issued = issue_current_action_class_contract(
            {"authority_budget": {}}, request, decision="APPROVE_ONCE_AS_SCOPED",
            expected_request_id=request["request_id"], expected_request_hash=request["request_hash"],
            authority_actor_id="test-authority", authority_decision_id="accdec-test",
        )
        contract = issued["contract"]
        self.assertEqual(contract["issuing_owner"], CANONICAL_CLEARANCE_OWNER)
        self.assertEqual(contract["max_users"], 1)
        self.assertEqual(contract["max_concurrent_transactions"], 1)
        self.assertEqual(contract["one_use_consumption"]["state"], "ISSUED")
        self.assertEqual(contract["authority_decision"]["request_id"], request["request_id"])
        consumed = consume_current_action_class_contract(
            issued["policy"], contract_id=contract["contract_id"], contract_hash=contract["contract_hash"],
            subject=contract["subject"], scope=contract["scope"],
            source_generation=contract["source_generation"], operation_id="operation-1",
        )
        self.assertEqual(consumed["consumption"]["state"], "CONSUMED")
        with self.assertRaises(PacketError):
            consume_current_action_class_contract(
                consumed["policy"], contract_id=contract["contract_id"], contract_hash=contract["contract_hash"],
                subject=contract["subject"], scope=contract["scope"],
                source_generation=contract["source_generation"], operation_id="operation-2",
            )

    def test_current_action_contract_request_expires_before_authority_issuance(self):
        now = datetime(2026, 7, 26, tzinfo=timezone.utc)
        request = build_current_action_class_contract_authority_request({
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "action_class": "GOVERNED_ONLY",
            "max_authority_class": "POOL",
            "subject": {"user_ip": "10.0.0.2"},
            "scope": {"source_egress": "vless", "target_egress": "awg3"},
            "max_users": 1, "max_concurrent_transactions": 1,
            "incident_generation": {"incident_id": "incident-1"},
            "source_generation": {
                "planner_generation_id": "planner-1", "source_bundle_hash": "source-1",
                "snapshot_bundle_hash": "snapshot-1", "selected_move_hash": "move-1",
            },
            "verification_contract": {"owner": "autoswitch"},
            "rollback_containment_contract": {"owner": "autoswitch"},
            "cooldown": {"required": True, "seconds": 180},
            "anti_flap": {"required": True}, "stop_conditions": ["verification_failure"],
        }, issue_preflight={"ready": True, "blockers": []}, now=now)
        result = validate_current_action_class_contract_authority_request(
            request, decision="APPROVE_ONCE_AS_SCOPED", now=now + timedelta(seconds=901),
        )
        self.assertFalse(result["ok"])
        self.assertIn("current_action_class_contract_request_expired", result["errors"])

    def test_current_action_contract_expiry_rejects_consumption(self):
        now = datetime(2026, 7, 26, tzinfo=timezone.utc)
        request = build_current_action_class_contract_authority_request(
            action_contract_template(), issue_preflight={"ready": True, "blockers": []}, now=now,
        )
        issued = issue_current_action_class_contract(
            {"authority_budget": {}}, request, decision="APPROVE_ONCE_AS_SCOPED",
            expected_request_id=request["request_id"], expected_request_hash=request["request_hash"], now=now,
            authority_actor_id="test-authority", authority_decision_id="accdec-test",
        )
        contract = issued["contract"]
        with self.assertRaisesRegex(PacketError, "consumption_expired"):
            consume_current_action_class_contract(
                issued["policy"], contract_id=contract["contract_id"], contract_hash=contract["contract_hash"],
                subject=contract["subject"], scope=contract["scope"],
                source_generation=contract["source_generation"], operation_id="expired-op",
                now=now + timedelta(seconds=301),
            )

    def test_current_action_contract_rejects_malformed_incident_and_authority_ceiling(self):
        malformed = action_contract_template()
        malformed["incident_generation"] = {"incident_id": ""}
        request = build_current_action_class_contract_authority_request(
            malformed, issue_preflight={"ready": True, "blockers": []},
        )
        result = validate_current_action_class_contract_authority_request(
            request, decision="APPROVE_ONCE_AS_SCOPED",
        )
        self.assertIn("current_action_class_contract_incident_generation_invalid", result["errors"])
        over_ceiling = action_contract_template()
        over_ceiling["max_authority_class"] = "FULL_INCIDENT"
        over_ceiling["authority_ceiling"] = "CANARY"
        request = build_current_action_class_contract_authority_request(
            over_ceiling, issue_preflight={"ready": True, "blockers": []},
        )
        result = validate_current_action_class_contract_authority_request(
            request, decision="APPROVE_ONCE_AS_SCOPED",
        )
        self.assertIn("current_action_class_contract_authority_exceeds_ceiling", result["errors"])

    def test_current_action_contract_authority_decisions_are_append_only_and_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            audit_path = Path(tmp) / "operator-execution-audit.jsonl"
            request_path = Path(tmp) / "request.json"
            write_json(policy_path, {"authority_budget": {}})
            request = build_current_action_class_contract_authority_request(
                action_contract_template(sha256_file(policy_path)), issue_preflight={"ready": True, "blockers": []},
            )
            write_json(request_path, request)
            result = issue_current_action_class_contract_to_policy(
                policy_path, request_path, decision="APPROVE_ONCE_AS_SCOPED",
                expected_request_id=request["request_id"], expected_request_hash=request["request_hash"],
                audit_store=audit_path, actor_id="authority-operator",
            )
            self.assertEqual(result["status"], "ISSUED")
            with self.assertRaisesRegex(PacketError, "decision_already_recorded"):
                issue_current_action_class_contract_to_policy(
                    policy_path, request_path, decision="APPROVE_ONCE_AS_SCOPED",
                    expected_request_id=request["request_id"], expected_request_hash=request["request_hash"],
                    audit_store=audit_path, actor_id="authority-operator",
                )
            records = read_audit_records(audit_path)
            self.assertEqual(len([r for r in records if r.get("decision") == "APPROVE_ONCE_AS_SCOPED"]), 1)

            decline_policy = Path(tmp) / "decline-policy.json"
            decline_request_path = Path(tmp) / "decline-request.json"
            decline_audit = Path(tmp) / "decline-audit.jsonl"
            write_json(decline_policy, {"authority_budget": {}})
            decline_request = build_current_action_class_contract_authority_request(
                action_contract_template(sha256_file(decline_policy)), issue_preflight={"ready": True, "blockers": []},
            )
            write_json(decline_request_path, decline_request)
            declined = decline_current_action_class_contract_request(
                decline_policy, decline_request_path, decision="DECLINE",
                expected_request_id=decline_request["request_id"], expected_request_hash=decline_request["request_hash"],
                audit_store=decline_audit, actor_id="authority-operator",
            )
            self.assertEqual(declined["status"], "DECLINED")
            with self.assertRaisesRegex(PacketError, "decision_already_recorded"):
                decline_current_action_class_contract_request(
                    decline_policy, decline_request_path, decision="DECLINE",
                    expected_request_id=decline_request["request_id"], expected_request_hash=decline_request["request_hash"],
                    audit_store=decline_audit, actor_id="authority-operator",
                )
            self.assertEqual(len([r for r in read_audit_records(decline_audit) if r.get("decision") == "DECLINE"]), 1)

    def test_current_action_request_audit_preserves_exact_preimage_without_grant(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            audit_path = Path(tmp) / "operator-execution-audit.jsonl"
            write_json(policy_path, {"authority_budget": {}})
            request = build_current_action_class_contract_authority_request(
                action_contract_template(sha256_file(policy_path)), issue_preflight={"ready": True, "blockers": []},
            )
            registered = register_current_action_class_contract_request(request, audit_store=audit_path)
            self.assertEqual(registered["status"], "REGISTERED")
            self.assertFalse(registered["policy_write"])
            envelope = {
                "schema_version": "v7.action-class-contract-reconciliation-request.v1",
                "status": "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY",
                "authority_classification": "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
                "exact_legal_next_action": "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST",
                "authority_decision_request": request,
                "approval_package": {
                    "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION", "actionable": True,
                    "request_id": request["request_id"], "request_hash": request["request_hash"],
                },
                "authority_granted": False, "contract_written": False, "runtime_apply": False,
                "routing_mutation": False, "candidate_created": False, "packet_created": False,
                "lease_created": False, "users_moved": 0,
            }
            self.assertEqual(
                register_current_action_class_contract_request(envelope, audit_store=audit_path)["status"],
                "ALREADY_REGISTERED",
            )
            recovered = current_action_class_contract_request_from_audit(
                request["request_id"], request["request_hash"], audit_store=audit_path,
            )
            self.assertEqual(recovered, request)
            issued = issue_current_action_class_contract_from_audit(
                policy_path, request_id=request["request_id"], request_hash=request["request_hash"],
                decision="APPROVE_ONCE_AS_SCOPED", audit_store=audit_path, actor_id="authority-operator",
            )
            self.assertEqual(issued["status"], "ISSUED")
            self.assertTrue(issued["policy_write"])
            with self.assertRaisesRegex(PacketError, "decision_already_recorded"):
                issue_current_action_class_contract_from_audit(
                    policy_path, request_id=request["request_id"], request_hash=request["request_hash"],
                    decision="APPROVE_ONCE_AS_SCOPED", audit_store=audit_path, actor_id="authority-operator",
                )

    def test_current_action_contract_interprocess_consumption_allows_exactly_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            audit_path = Path(tmp) / "operator-execution-audit.jsonl"
            request = build_current_action_class_contract_authority_request(
                action_contract_template(), issue_preflight={"ready": True, "blockers": []},
            )
            issued = issue_current_action_class_contract(
                {"authority_budget": {}}, request, decision="APPROVE_ONCE_AS_SCOPED",
                expected_request_id=request["request_id"], expected_request_hash=request["request_hash"],
                authority_actor_id="test-authority", authority_decision_id="accdec-test",
            )
            write_json(policy_path, issued["policy"])
            contract = issued["contract"]
            barrier = threading.Barrier(2)
            outcomes = []

            def consume(operation_id):
                barrier.wait()
                try:
                    consume_current_action_class_contract_to_policy(
                        policy_path, audit_store=audit_path, contract_id=contract["contract_id"],
                        contract_hash=contract["contract_hash"], subject=contract["subject"], scope=contract["scope"],
                        source_generation=contract["source_generation"], operation_id=operation_id,
                    )
                    outcomes.append("PASS")
                except PacketError:
                    outcomes.append("STOP_SAFE")

            threads = [threading.Thread(target=consume, args=(f"op-{n}",)) for n in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(sorted(outcomes), ["PASS", "STOP_SAFE"])
            self.assertEqual(len([r for r in read_audit_records(audit_path) if r.get("record_type") == "current_action_class_contract_consumed"]), 1)

    def test_autonomous_execution_control_is_fail_closed_and_generation_bound(self):
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe-mode.json"
            missing = autonomous_execution_control_decision(path, now=now)
            path.write_text("{bad", encoding="utf-8")
            malformed = autonomous_execution_control_decision(path, now=now)
            closed = build_autonomous_execution_control_state(False, actor="owner", reason="controlled window", now=now)
            write_json(path, closed)
            allowed = autonomous_execution_control_decision(
                path,
                expected_generation=closed["generation"],
                action_class="EMERGENCY_FAILOVER",
                operation_id="op-1",
                now=now,
            )
            mismatch = autonomous_execution_control_decision(
                path,
                expected_generation="aec_old",
                action_class="EMERGENCY_FAILOVER",
                operation_id="op-1",
                now=now,
            )
            stale = autonomous_execution_control_decision(
                path,
                action_class="EMERGENCY_FAILOVER",
                operation_id="op-1",
                now=now + timedelta(seconds=901),
            )

        self.assertFalse(missing["allowed"])
        self.assertFalse(malformed["allowed"])
        self.assertTrue(allowed["allowed_forward_mutation"])
        self.assertFalse(mismatch["allowed"])
        self.assertIn("execution_control_generation_mismatch", mismatch["blockers"])
        self.assertFalse(stale["allowed"])
        self.assertIn("execution_control_closed_expired", stale["blockers"])
        self.assertFalse(allowed["authority_granted"])

    def test_autonomous_execution_control_open_persists_and_allows_only_certified_rollback(self):
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe-mode.json"
            opened = build_autonomous_execution_control_state(True, actor="owner", reason="incident", now=now)
            write_json(path, opened)
            forward = autonomous_execution_control_decision(path, action_class="USER_SWITCH", operation_id="op-1", now=now + timedelta(days=30))
            rollback = autonomous_execution_control_decision(
                path,
                mutation_kind="rollback",
                action_class="USER_SWITCH",
                expected_generation=opened["generation"],
                rollback_certified=True,
                operation_id="op-1",
                now=now + timedelta(days=30),
            )
            uncertified = autonomous_execution_control_decision(
                path,
                mutation_kind="rollback",
                action_class="USER_SWITCH",
                operation_id="op-1",
                now=now,
            )

        self.assertEqual(opened["schema_version"], AUTONOMOUS_EXECUTION_CONTROL_SCHEMA)
        self.assertFalse(forward["allowed"])
        self.assertTrue(rollback["rollback_only_allowed"])
        self.assertFalse(uncertified["allowed"])

    def test_autonomous_execution_control_rejects_legacy_and_incomplete_state(self):
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe-mode.json"
            for payload in [
                {"schema_version": 1, "enabled": False},
                {"schema_version": AUTONOMOUS_EXECUTION_CONTROL_SCHEMA, "enabled": False, "state": "CLOSED"},
            ]:
                write_json(path, payload)
                decision = autonomous_execution_control_decision(path, now=now)
                self.assertFalse(decision["allowed"])

    def test_operation_scoped_controlled_window_binds_exact_identity_and_one_user(self):
        now = datetime.now(timezone.utc)
        bindings = {
            "operation_id": "op-bound",
            "selected_move_hash": "move-bound",
            "action_class": "USER_SWITCH",
            "source_bundle_hash": "source-bound",
            "snapshot_bundle_hash": "snapshot-bound",
            "max_users": 1,
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe-mode.json"
            closed = build_autonomous_execution_control_state(
                False, actor="owner", reason="one operation", now=now, **bindings
            )
            write_json(path, closed)
            allowed = autonomous_execution_control_decision(
                path, expected_generation=closed["generation"], now=now, **bindings
            )
            mismatches = {}
            for field, changed in {
                "operation_id": "op-other",
                "selected_move_hash": "move-other",
                "action_class": "RECOVERY_ADMISSION",
                "source_bundle_hash": "source-other",
                "snapshot_bundle_hash": "snapshot-other",
                "max_users": 2,
            }.items():
                candidate = dict(bindings)
                candidate[field] = changed
                mismatches[field] = autonomous_execution_control_decision(
                    path, expected_generation=closed["generation"], now=now, **candidate
                )

        self.assertEqual(closed["scope"], "operation")
        self.assertTrue(allowed["allowed_forward_mutation"])
        for field, decision in mismatches.items():
            self.assertFalse(decision["allowed"], field)
            self.assertIn(f"execution_control_{field}_mismatch", decision["blockers"])

    def test_controlled_window_finalization_is_expiry_safe_and_idempotent(self):
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe-mode.json"
            closed = build_autonomous_execution_control_state(
                False,
                actor="owner",
                reason="expiring operation",
                now=now,
                operation_id="op-finalize",
                selected_move_hash="move-finalize",
                action_class="USER_SWITCH",
                source_bundle_hash="source-finalize",
                snapshot_bundle_hash="snapshot-finalize",
                max_users=1,
            )
            write_json(path, closed)
            first = finalize_autonomous_execution_control_window(
                path,
                expected_generation=closed["generation"],
                operation_id="op-finalize",
                now=now + timedelta(seconds=901),
            )
            second = finalize_autonomous_execution_control_window(
                path,
                expected_generation=closed["generation"],
                operation_id="op-finalize",
                now=now + timedelta(seconds=902),
            )

        self.assertTrue(first["final_open"])
        self.assertEqual(first["after"]["state"], "OPEN")
        self.assertTrue(second["final_open"])
        self.assertTrue(second["idempotent"])

    def test_every_controlled_window_terminal_class_uses_same_final_open_owner(self):
        terminal_reasons = [
            "success",
            "deny_before_apply",
            "stale_packet",
            "generation_mismatch",
            "source_hash_mismatch",
            "snapshot_bundle_mismatch",
            "timeout",
            "verification_failure",
            "rollback_success",
            "rollback_failure",
            "partial_failure",
            "subprocess_failure",
            "internal_exception",
            "operator_cancellation",
            "expired_controlled_window",
            "process_restart_recovery",
        ]
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe-mode.json"
            for reason in terminal_reasons:
                closed = build_autonomous_execution_control_state(
                    False,
                    actor="owner",
                    reason=reason,
                    now=now,
                    operation_id=f"op-{reason}",
                    selected_move_hash=f"move-{reason}",
                    action_class="USER_SWITCH",
                    source_bundle_hash=f"source-{reason}",
                    snapshot_bundle_hash=f"snapshot-{reason}",
                    max_users=1,
                )
                write_json(path, closed)
                result = finalize_autonomous_execution_control_window(
                    path,
                    expected_generation=closed["generation"],
                    operation_id=f"op-{reason}",
                    reason=reason,
                    now=now + (timedelta(seconds=901) if reason == "expired_controlled_window" else timedelta()),
                )
                self.assertTrue(result["final_open"], reason)
                self.assertEqual(result["after"]["state"], "OPEN", reason)

    def test_restart_recovery_forces_malformed_state_to_valid_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe-mode.json"
            path.write_text('{"schema_version":"broken","state":"CLOSED"}', encoding="utf-8")
            result = finalize_autonomous_execution_control_window(
                path,
                actor="restart-recovery",
                reason="malformed_state_fail_closed_recovery",
                force_fail_closed_open=True,
            )
            recovered = autonomous_execution_control_state(path)

        self.assertTrue(result["forced_fail_closed_recovery"])
        self.assertTrue(result["final_open"])
        self.assertTrue(recovered["valid"])
        self.assertEqual(recovered["state"], "OPEN")

    def test_strict_packet_requires_source_snapshot_and_binds_identity(self):
        preview = self.preview_packet()
        with self.assertRaisesRegex(PacketError, "source_hashes_missing"):
            packet_from_preview(
                preview,
                approval_author="operator-a",
                approval_reviewer="operator-b",
                breaker_generation="aec_bound",
                require_execution_binding=True,
            )
        preview["source_hashes"] = {"users_registry": "users", "egress_registry": "egress"}
        preview["snapshot_bundle_hash"] = "snapshot"
        packet = packet_from_preview(
            preview,
            approval_author="operator-a",
            approval_reviewer="operator-b",
            breaker_generation="aec_bound",
            require_execution_binding=True,
        )
        identity = packet_identity(packet)
        self.assertEqual(identity["source_bundle_hash"], sha256_json(preview["source_hashes"]))
        self.assertEqual(identity["source_hashes_hash"], sha256_json(preview["source_hashes"]))
        self.assertEqual(identity["snapshot_bundle_hash"], "snapshot")
        self.assertEqual(identity["max_users"], 1)

    def test_breaker_generation_is_bound_to_packet_and_invalidates_lease(self):
        packet = packet_from_plan(
            self.movement_plan(),
            approval_author="operator-a",
            approval_reviewer="operator-b",
            breaker_generation="aec_generation_one",
        )
        lease = create_execution_lease_from_packet(packet)
        current = material_state_from_packet(packet)
        current["breaker_generation"] = "aec_generation_two"
        state = execution_lease_state(lease, current_material_state=current)

        self.assertEqual(packet_identity(packet)["breaker_generation"], "aec_generation_one")
        self.assertEqual(lease["immutable_packet_identity"]["breaker_generation"], "aec_generation_one")
        self.assertEqual(state["status"], "INVALIDATED")
        self.assertIn("breaker_generation", state["changed_fields"])

    def test_b15_containment_forward_fix_classification_matrix_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "users.registry").write_text("users", encoding="utf-8")
            (state_dir / "egress.registry").write_text("egress", encoding="utf-8")
            packet = packet_template(state_dir)
            packet["rollback_manifest"] = {
                "rollback_manifest_id": "rb-b15",
                "source_operation_id": packet["operation_id"],
                "partial_failure_policy": "stop_and_contain",
                "rollback_execution_owner": CANONICAL_CLEARANCE_OWNER,
                "items": [{
                    "user_ip": "10.7.0.2",
                    "rollback_target": "vless",
                    "forward_target": "awg0",
                    "source_operation_id": packet["operation_id"],
                }],
            }

        no_execution = containment_forward_fix_classification(packet=packet)
        forward_fix = containment_forward_fix_classification(
            packet=packet,
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": True, "result": "verified"},
        )
        contained = containment_forward_fix_classification(
            packet=packet,
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": False, "result": "failed", "rollback_required": True},
            rollback_result={"rollback_required": True, "rollback_verdict": "ROLLBACK_COMPLETED"},
        )
        failed = containment_forward_fix_classification(
            packet=packet,
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": False, "result": "failed", "rollback_required": True},
            rollback_result={"rollback_required": True, "rollback_verdict": "ROLLBACK_FAILED"},
        )
        partial = containment_forward_fix_classification(
            packet=packet,
            execution_result={"applied": True, "partial_success": True},
            verification_result={"partial_success": True},
        )

        self.assertEqual(no_execution["schema_version"], "v7.b15-containment-forward-fix-classification.v1")
        self.assertEqual(no_execution["backlog_item"], "B15")
        self.assertEqual(no_execution["classification"], "NO_EXECUTION_CONTAINED")
        self.assertEqual(forward_fix["classification"], "FORWARD_FIX_VERIFIED")
        self.assertEqual(contained["classification"], "CONTAINED_BY_ROLLBACK")
        self.assertEqual(failed["classification"], "CONTAINMENT_FAILED_OPERATOR_REVIEW_REQUIRED")
        self.assertEqual(partial["classification"], "PARTIAL_FORWARD_FIX_REQUIRES_CONTAINMENT_REVIEW")
        self.assertEqual(no_execution["partial_failure_policy"], "stop_and_contain")
        self.assertIn("b15_does_not_execute_runtime_apply_or_rollback", no_execution["canonical_rules"])
        for model in [no_execution, forward_fix, contained, failed, partial]:
            self.assertTrue(model["read_only"])
            self.assertFalse(model["runtime_mutation_performed"])
            self.assertFalse(model["restore_barrier_written_now"])
            self.assertFalse(model["apply_executed"])
            self.assertFalse(model["rollback_executed"])
            self.assertEqual(model["users_moved"], 0)
            self.assertFalse(model["authority_expanded"])
            self.assertFalse(model["synthetic_evidence_created"])

    def test_c5_rollback_operational_compensation_contract_is_read_only(self):
        contract = rollback_operational_compensation_contract(
            generated_at="2026-06-29T18:30:00+07:00"
        )

        self.assertEqual(
            contract["schema_version"],
            "v7.c5-rollback-operational-compensation.v1",
        )
        self.assertEqual(contract["backlog_item"], "C5")
        self.assertEqual(
            contract["semantic_contract"]["rollback_semantics"],
            "OPERATIONAL_COMPENSATION",
        )
        self.assertFalse(contract["semantic_contract"]["transaction_rollback_supported"])
        self.assertFalse(contract["semantic_contract"]["database_transaction_semantics_claimed"])
        self.assertIn(
            "c5_rollback_is_operational_compensation_not_transaction_rewind",
            contract["canonical_rules"],
        )
        self.assertIn("automatic_rollback_execution", contract["forbidden"])
        self.assertIn("runtime_apply", contract["forbidden"])
        self.assertEqual(
            contract["omp_output"]["c5_status"],
            "DONE_READ_ONLY_ROLLBACK_OPERATIONAL_COMPENSATION_PRESERVED",
        )
        self.assertEqual(
            contract["omp_output"]["unlocked_capability"],
            "C6_BOUNDED_STALE_ALLOWANCE_BY_ACTION_CLASS",
        )
        self.assertIn(
            "transaction_rollback_abstraction",
            contract["omp_output"]["blocked_later_steps"],
        )
        self.assertTrue(contract["read_only"])
        self.assertFalse(contract["runtime_mutation_performed"])
        self.assertFalse(contract["restore_barrier_written_now"])
        self.assertFalse(contract["apply_executed"])
        self.assertFalse(contract["rollback_executed"])
        self.assertEqual(contract["users_moved"], 0)
        self.assertFalse(contract["authority_expanded"])
        self.assertFalse(contract["synthetic_evidence_created"])
        self.assertFalse(contract["new_owner_created"])
        self.assertFalse(contract["new_runtime_created"])

    def make_state(self, root):
        state = root / "state"
        state.mkdir()
        (state / "users.registry").write_text("ip=10.7.0.11 current=1 enabled=1\n", encoding="utf-8")
        (state / "egress.registry").write_text("id=1 enabled=1 protocol=amneziawg\n", encoding="utf-8")
        return state

    def movement_plan(self):
        atomic_envelope = {
            "schema_version": "v7.atomic-execution-envelope.v1",
            "envelope_id": "aee-test",
            "envelope_hash": "aee-hash-test",
            "source_bundle_hash": "source-bundle-hash-test",
            "snapshot_bundle_hash": "snapshot-bundle-hash-test",
        }
        return {
            "operation": {
                "runtime_snapshot_hash": "snapshot-test",
            },
            "safety": {
                "generation": {
                    "planner_generation_id": "gen-move",
                },
                "atomic_execution_envelope": atomic_envelope,
                "restore_barrier": {
                    "clearance_selected_moves_before_guard": 1,
                    "clearance_selected_moves_hash": "move-hash",
                },
            },
            "decisions": [
                {
                    "user_ip": "10.7.0.11",
                    "current_egress": "1",
                    "recommended_egress": "vless",
                    "action": "switch",
                    "move_type": "failover",
                    "reason": ["current_egress_not_eligible"],
                    "important_services": ["telegram"],
                    "candidates": [
                        {
                            "egress": "1",
                            "eligible": False,
                            "service_suitability": {
                                "per_service": {
                                    "telegram": {
                                        "available": False,
                                        "status": "DOWN",
                                        "truth_class": "PERSISTENT_FAIL",
                                        "freshness": {"state": "FRESH"},
                                    }
                                }
                            },
                        },
                        {
                            "egress": "vless",
                            "eligible": True,
                            "service_suitability": {
                                "per_service": {
                                    "telegram": {
                                        "available": True,
                                        "status": "OK",
                                        "freshness": {"state": "FRESH"},
                                    }
                                }
                            },
                        },
                    ],
                }
            ],
        }

    def preview_packet(self):
        return {
            "schema_version": "v7.governed-canary.packet-preview.v1",
            "owner": "admin_core/operator_execution.py",
            "status": "PACKET_PREVIEW_READY",
            "packet_id": "pkt_preview_unit_identity",
            "operation_id": "govdry_unit_identity",
            "decision_id": "decision_preview_unit_identity",
            "authority_generation": "cycle-unit-identity",
            "selected_move_count": 1,
            "selected_move_hash": "preview-selected-hash-unit",
            "allowed_users": ["10.7.0.11"],
            "allowed_targets": ["vless"],
            "rollback_manifest_preview": {
                "rollback_manifest_id": "rb_preview_unit_identity",
                "items": [
                    {
                        "user_ip": "10.7.0.11",
                        "rollback_target": "1",
                        "forward_target": "vless",
                        "source_operation_id": "govdry_unit_identity",
                    }
                ],
                "partial_failure_policy": "stop_and_contain",
                "rollback_execution_owner": "admin_core/operator_execution.py",
            },
            "preview_only": True,
            "read_only": True,
        }

    def delegated_policy_authority(self):
        from admin_core import autonomy_trust_acceleration

        now = datetime.now(timezone.utc)
        policy = standing_delegated_operational_policy_template()
        normalized_scope = autonomy_trust_acceleration.normalized_delegated_autonomy_scope(policy)
        contract = {
            "schema_version": "v7.standing-delegated-operational-policy.v1",
            "status": "ACTIVE",
            "issued_at": now.isoformat(),
            "expires_at": (now + timedelta(days=30)).isoformat(),
            "issuing_owner": CANONICAL_CLEARANCE_OWNER,
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "policy_scope_hash": autonomy_trust_acceleration.delegated_autonomy_scope_hash(policy),
            "policy": policy,
            "authority_decision": {
                "decision": "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                "decision_id": "sdpdec-unit",
                "request_id": "sdpauth_r1_unit",
                "request_hash": "a" * 64,
                "actor_id": "unit-authority",
                "decided_at": now.isoformat(),
            },
            "per_action_law": {
                "candidate_owner": "tools/v7-users-autoswitch",
                "candidate_identity": "FRESH_ONLY",
                "packet_owner": CANONICAL_CLEARANCE_OWNER,
                "packet_generation": "FRESH_IMMEDIATELY_BEFORE_EXECUTION",
                "packet_reuse": "FORBIDDEN",
                "lease_required": True,
                "max_users": 1,
                "max_concurrent_transactions": 1,
                "verification_required": True,
                "rollback_or_certified_no_rollback_required": True,
                "final_safe_mode": "OPEN",
            },
        }
        contract_hash = standing_delegated_policy_contract_hash(contract)
        contract["contract_hash"] = contract_hash
        contract["contract_id"] = f"sdpc_{contract_hash[:24]}"
        return {
            "authority_basis": "DELEGATED_AUTONOMY_POLICY",
            "policy_id": "dap_default_tier1_readonly",
            "policy_scope_hash": autonomy_trust_acceleration.delegated_autonomy_scope_hash(policy),
            "normalized_scope": normalized_scope,
            "policy_state": "APPROVED",
            "current_mode": "DELEGATED_AUTONOMY",
            "action_class": "single-user governed candidate failover",
            "max_users_per_transaction": 1,
            "max_concurrent_transactions": 1,
            "candidate_identity": "FRESH_ONLY",
            "packet_reuse": "FORBIDDEN",
            "self_expansion_allowed": False,
            "standing_policy_contract": contract,
            "authority_audit_verified": True,
        }

    def engineering_authority_request(self):
        now = datetime.now(timezone.utc)
        authority = self.delegated_policy_authority()
        request = {
            "schema": "v7.controlled-rollback-condition-engineering-authority-request.v1",
            "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION",
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(hours=1)).isoformat(),
            "decision_set": ["APPROVE_ONCE_AS_SCOPED", "APPROVE_WITH_NARROWER_SCOPE", "DENY", "EXPIRED"],
            "evidence_cell": "rollback_and_no_rollback_present",
            "subject": {
                "user_ip": "10.7.0.11",
                "certification_user": True,
                "ordinary_customer": False,
            },
            "scope": {
                "max_users": 1,
                "max_concurrent_transactions": 1,
                "source_egress": "1",
                "target_egress": "vless",
                "policy_id": authority["policy_id"],
                "policy_scope_hash": authority["policy_scope_hash"],
            },
            "controlled_condition": {"name": "CONTROLLED_SOURCE_FAILURE_WITH_REAL_SERVICE_MATRIX_VERIFIER_CONTENTION"},
            "one_use_law": {
                "approval_use_limit": 1,
                "implicit_renewal": False,
                "retry_under_same_approval": False,
            },
        }
        contract_hash = sha256_json(request)
        request["request_id"] = "engauth_r1_" + contract_hash[:24]
        request["contract_hash"] = contract_hash
        return request

    def test_engineering_authority_binds_and_consumes_exact_request_once(self):
        preview = self.preview_packet()
        request = self.engineering_authority_request()
        binding = engineering_authority_binding_from_preview(
            request,
            preview,
            decision="APPROVE_ONCE_AS_SCOPED",
            expected_request_id=request["request_id"],
            expected_contract_hash=request["contract_hash"],
        )
        packet = packet_from_preview(
            preview,
            approval_author="",
            approval_reviewer="",
            delegated_policy_authority=self.delegated_policy_authority(),
            engineering_authority=binding,
        )
        lease = create_execution_lease_from_packet(packet, source_preview=preview)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            first = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                restore_barrier_file=barrier,
                execution_lease_id=lease["lease_id"],
            )
            replay = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                restore_barrier_file=barrier,
                execution_lease_id=lease["lease_id"],
            )
            records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            barrier_data = json.loads(barrier.read_text(encoding="utf-8"))

        self.assertTrue(first["execution_allowed_now"])
        self.assertEqual(records[0]["record_type"], "engineering_authority_consumed")
        self.assertEqual(records[0]["engineering_authority_request_id"], request["request_id"])
        self.assertEqual(records[0]["execution_lease_id"], lease["lease_id"])
        self.assertEqual(barrier_data["engineering_authority_request_id"], request["request_id"])
        self.assertEqual(barrier_data["engineering_authority_contract_hash"], request["contract_hash"])
        self.assertEqual(barrier_data["engineering_authority_transaction_nonce"], binding["transaction_nonce"])
        self.assertEqual(replay["recheck"]["verdict"], "DENY_REPLAY")
        self.assertIn("engineering_authority_request_already_consumed", replay["recheck"]["errors"])

    def test_engineering_authority_rejects_candidate_scope_drift(self):
        request = self.engineering_authority_request()
        preview = self.preview_packet()
        preview["allowed_targets"] = ["other"]
        preview["rollback_manifest_preview"]["items"][0]["forward_target"] = "other"
        with self.assertRaises(PacketError):
            engineering_authority_binding_from_preview(
                request,
                preview,
                decision="APPROVE_ONCE_AS_SCOPED",
                expected_request_id=request["request_id"],
                expected_contract_hash=request["contract_hash"],
            )

    def test_repair_continuation_policy_issues_fresh_one_use_decision_only_after_verified_preapply_stop(self):
        request = self.engineering_authority_request()
        request.update({
            "program_id": "V7_L7_L8_PRODUCTION_EVIDENCE_AND_AUTHORITY_EVOLUTION_PROGRAM_V1",
            "action_class": "single-user governed candidate failover",
            "current_commit": "repair-commit",
        })
        request["subject"].update({"user_ip": "10.7.0.16"})
        request["scope"].update({
            "max_material_outcomes": 1,
            "source_egress": "controlled-source",
            "source_interface": "wg-test",
            "source_protocol": "wireguard",
            "target_interface": "tun0",
            "target_protocol": "vless",
        })
        request["controlled_condition"].update({
            "rollback_failure_injection": False,
            "direct_rollback_invocation_for_evidence": False,
        })
        exact_scope = {
            "program_id": request["program_id"],
            "action_class": request["action_class"],
            "evidence_cell": request["evidence_cell"],
            "user_ip": "10.7.0.16",
            "certification_user": True,
            "ordinary_customer": False,
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "max_material_outcomes": 1,
            "source_egress": "controlled-source",
            "source_interface": "wg-test",
            "source_protocol": "wireguard",
            "target_egress": "vless",
            "target_interface": "tun0",
            "target_protocol": "vless",
            "policy_id": request["scope"]["policy_id"],
            "policy_scope_hash": request["scope"]["policy_scope_hash"],
            "controlled_condition": request["controlled_condition"]["name"],
            "rollback_failure_injection": False,
            "direct_rollback_invocation_for_evidence": False,
        }
        policy = {
            "schema": "v7.controlled-rollback-repair-continuation-policy.v1",
            "status": "APPROVED_EXACT_SCOPE_REPAIR_CONTINUATION",
            "allowed_decision": "APPROVE_ONCE_AS_SCOPED",
            "fresh_request_required": True,
            "approval_reuse_allowed": False,
            "background_runtime_allowed": False,
            "self_expansion_allowed": False,
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "exact_scope": exact_scope,
        }
        policy_hash = engineering_authority_repair_continuation_policy_hash(policy)
        policy["policy_hash"] = policy_hash
        policy["policy_id"] = "engrepair_" + policy_hash[:24]
        request["previous_consumed_request"] = {
            "request_id": "engauth_r1_consumed",
            "terminal": "CONSUMED_STOP_SAFE_BEFORE_APPLY",
            "apply_executed": False,
            "users_moved": 0,
            "rollback_attempted": False,
            "cleanup_result": "PASS_EXACT_PRESTATE_RESTORED",
            "blocker_fingerprint": "blocker-new",
            "repair_commit": "repair-commit",
            "repair_deploy_id": "deploy-repair",
            "repair_tests_passed": True,
            "truth_convergence_aligned": True,
            "reuse_forbidden": True,
        }
        request["automatic_reissue"] = {
            "policy_id": policy["policy_id"],
            "policy_hash": policy["policy_hash"],
            "previous_request_id": "engauth_r1_consumed",
            "fresh_request": True,
            "reuses_previous_approval": False,
            "prior_repaired_blocker_fingerprints": [],
        }
        request.pop("request_id", None)
        request.pop("contract_hash", None)
        contract_hash = sha256_json(request)
        request["contract_hash"] = contract_hash
        request["request_id"] = "engauth_r1_" + contract_hash[:24]

        allowed = validate_engineering_authority_repair_continuation(policy, request)
        request["automatic_reissue"]["prior_repaired_blocker_fingerprints"] = ["blocker-new"]
        denied = validate_engineering_authority_repair_continuation(policy, request)

        self.assertTrue(allowed["ok"])
        self.assertEqual(allowed["decision"], "APPROVE_ONCE_AS_SCOPED")
        self.assertFalse(allowed["approval_reused"])
        self.assertFalse(denied["ok"])
        self.assertIn("engineering_authority_repair_same_blocker_recurred", denied["errors"])

    def test_repair_continuation_allows_same_fingerprint_once_for_new_deployed_generation(self):
        request = self.engineering_authority_request()
        request.update({
            "program_id": "V7_L7_L8_PRODUCTION_EVIDENCE_AND_AUTHORITY_EVOLUTION_PROGRAM_V1",
            "action_class": "single-user governed candidate failover",
            "current_commit": "repair-new",
        })
        request["subject"].update({"user_ip": "10.7.0.16"})
        request["scope"].update({
            "max_material_outcomes": 1,
            "source_egress": "controlled-source",
            "source_interface": "wg-test",
            "source_protocol": "wireguard",
            "target_interface": "tun0",
            "target_protocol": "vless",
        })
        request["controlled_condition"].update({
            "rollback_failure_injection": False,
            "direct_rollback_invocation_for_evidence": False,
        })
        exact_scope = {
            "program_id": request["program_id"],
            "action_class": request["action_class"],
            "evidence_cell": request["evidence_cell"],
            "user_ip": "10.7.0.16",
            "certification_user": True,
            "ordinary_customer": False,
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "max_material_outcomes": 1,
            "source_egress": "controlled-source",
            "source_interface": "wg-test",
            "source_protocol": "wireguard",
            "target_egress": "vless",
            "target_interface": "tun0",
            "target_protocol": "vless",
            "policy_id": request["scope"]["policy_id"],
            "policy_scope_hash": request["scope"]["policy_scope_hash"],
            "controlled_condition": request["controlled_condition"]["name"],
            "rollback_failure_injection": False,
            "direct_rollback_invocation_for_evidence": False,
        }
        policy = {
            "schema": "v7.controlled-rollback-repair-continuation-policy.v1",
            "status": "APPROVED_EXACT_SCOPE_REPAIR_CONTINUATION",
            "allowed_decision": "APPROVE_ONCE_AS_SCOPED",
            "fresh_request_required": True,
            "approval_reuse_allowed": False,
            "background_runtime_allowed": False,
            "self_expansion_allowed": False,
            "repair_generation_aware": True,
            "max_attempts_per_repair_generation": 1,
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "exact_scope": exact_scope,
        }
        policy_hash = engineering_authority_repair_continuation_policy_hash(policy)
        policy["policy_hash"] = policy_hash
        policy["policy_id"] = "engrepair_" + policy_hash[:24]
        request["previous_consumed_request"] = {
            "request_id": "engauth_r1_consumed-v3",
            "terminal": "CONSUMED_STOP_SAFE_BEFORE_APPLY",
            "terminal_at": "2026-07-20T02:20:00+07:00",
            "apply_executed": False,
            "users_moved": 0,
            "rollback_attempted": False,
            "cleanup_result": "PASS_EXACT_PRESTATE_RESTORED",
            "blocker_fingerprint": "blocker-repeated",
            "repair_commit": "repair-new",
            "repair_deploy_id": "deploy-new",
            "repair_binary_sha256": "sha-new",
            "repair_deployed_at": "2026-07-20T02:31:52+07:00",
            "repair_deployed_after_terminal": True,
            "repair_tests_passed": True,
            "truth_convergence_aligned": True,
            "reuse_forbidden": True,
        }
        request["automatic_reissue"] = {
            "policy_id": policy["policy_id"],
            "policy_hash": policy["policy_hash"],
            "previous_request_id": "engauth_r1_consumed-v3",
            "fresh_request": True,
            "reuses_previous_approval": False,
            "max_attempts_per_repair_generation": 1,
            "prior_repaired_blocker_fingerprints": ["blocker-repeated"],
            "prior_repaired_blocker_generations": [{
                "blocker_fingerprint": "blocker-repeated",
                "repair_commit": "repair-old",
                "repair_deploy_id": "deploy-old",
                "repair_binary_sha256": "sha-old",
            }],
        }
        request.pop("request_id", None)
        request.pop("contract_hash", None)
        contract_hash = sha256_json(request)
        request["contract_hash"] = contract_hash
        request["request_id"] = "engauth_r1_" + contract_hash[:24]

        allowed = validate_engineering_authority_repair_continuation(policy, request)
        request["automatic_reissue"]["prior_repaired_blocker_generations"].append({
            "blocker_fingerprint": "blocker-repeated",
            "repair_commit": "repair-new",
            "repair_deploy_id": "deploy-new",
            "repair_binary_sha256": "sha-new",
        })
        denied = validate_engineering_authority_repair_continuation(policy, request)

        self.assertTrue(allowed["ok"], allowed)
        self.assertTrue(allowed["repeated_blocker_fingerprint"])
        self.assertEqual(allowed["repair_generation"]["repair_commit"], "repair-new")
        self.assertFalse(denied["ok"])
        self.assertIn("engineering_authority_repair_generation_already_attempted", denied["errors"])

    def test_runtime_recheck_allows_record_only_for_matching_zero_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            packet = packet_template(state)
            result = runtime_recheck(packet, state)

        self.assertTrue(result["allow"])
        self.assertEqual(result["verdict"], "ALLOW_RECORD_ONLY")
        self.assertFalse(result["checks"]["real_runtime_action_after_recheck"])

    def test_execute_writes_approval_then_replay_denial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            packet = packet_template(state)
            first = execute_packet(packet, audit, state, mode="execute")
            replay = execute_packet(packet, audit, state, mode="execute")
            records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]

        self.assertTrue(first["record_written"])
        self.assertEqual(first["record"]["record_type"], "approval_record_persisted")
        self.assertEqual(first["recheck"]["verdict"], "ALLOW_RECORD_ONLY")
        self.assertEqual(replay["record"]["record_type"], "denial_record")
        self.assertEqual(replay["recheck"]["verdict"], "DENY_REPLAY")
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1]["previous_record_hash"], records[0]["record_hash"])
        self.assertFalse(records[0]["runtime_mutation"])

    def test_execute_runtime_action_writes_governance_transition_then_replay_denial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            governance = root / "governance.jsonl"
            packet = packet_template(state)
            packet["runtime_action"] = RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE
            first = execute_packet(packet, audit, state, mode="runtime_action", runtime_governance_store=governance)
            replay = execute_packet(packet, audit, state, mode="runtime_action", runtime_governance_store=governance)
            audit_records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            governance_records = [json.loads(line) for line in governance.read_text(encoding="utf-8").splitlines()]

        self.assertTrue(first["record_written"])
        self.assertEqual(first["record"]["record_type"], "runtime_action_record_persisted")
        self.assertTrue(first["record"]["runtime_mutation"])
        self.assertTrue(first["record"]["runtime_action_performed"])
        self.assertFalse(first["record"]["user_movement"])
        self.assertFalse(first["record"]["routing_mutation"])
        self.assertEqual(first["recheck"]["verdict"], "ALLOW_RECORD_ONLY")
        self.assertEqual(len(governance_records), 1)
        self.assertEqual(governance_records[0]["record_type"], "zero_move_governance_state_transition")
        self.assertFalse(governance_records[0]["user_movement"])
        self.assertFalse(governance_records[0]["routing_mutation"])
        self.assertEqual(replay["record"]["record_type"], "denial_record")
        self.assertEqual(replay["recheck"]["verdict"], "DENY_REPLAY")
        self.assertEqual(len(audit_records), 2)
        self.assertEqual(audit_records[1]["previous_record_hash"], audit_records[0]["record_hash"])

    def test_execute_runtime_action_denies_record_only_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            governance = root / "governance.jsonl"
            packet = packet_template(state)
            result = execute_packet(packet, audit, state, mode="runtime_action", runtime_governance_store=governance)
            records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(result["record"]["record_type"], "denial_record")
        self.assertEqual(result["recheck"]["verdict"], "DENY_RUNTIME_ACTION_UNSUPPORTED")
        self.assertFalse(governance.exists())
        self.assertFalse(records[0]["runtime_mutation"])

    def test_expired_missing_second_and_movement_packets_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            expired = packet_template(state, expires_delta=timedelta(seconds=-1))
            missing_second = packet_template(state)
            missing_second["approvals"] = missing_second["approvals"][:1]
            movement = packet_template(state)
            movement["constraints"]["allowed_users"] = ["10.7.0.11"]
            movement["constraints"]["user_movement_allowed"] = True

            self.assertEqual(runtime_recheck(expired, state)["verdict"], "DENY_PACKET_INVALID")
            self.assertIn("dual_confirmation_missing", runtime_recheck(missing_second, state)["errors"])
            self.assertIn("allowed_users_not_empty", runtime_recheck(movement, state)["errors"])

    def test_hash_generation_runtime_action_and_path_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            packet = packet_template(state)
            bad_hash = packet_template(state)
            bad_hash["expected"]["selected_move_hash"] = "bad"
            bad_generation = packet_template(state)
            bad_generation["expected"]["generation_id"] = ""
            bad_action = packet_template(state)
            bad_action["runtime_action"] = "MOVE_USER"
            missing_runtime = root / "missing"

            self.assertEqual(runtime_recheck(bad_hash, state)["verdict"], "DENY_PACKET_INVALID")
            self.assertIn("generation_id_missing", runtime_recheck(bad_generation, state)["errors"])
            self.assertIn("runtime_action_not_allowed", runtime_recheck(bad_action, state)["errors"])
            self.assertEqual(runtime_recheck(packet, missing_runtime)["verdict"], "DENY_STALE_RUNTIME")

    def test_path_traversal_blocked_for_packet_and_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(PacketError):
                resolve_under_repo("../outside.json", root)

    def test_nonzero_packet_generation_and_clearance_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            lifecycle = root / "lifecycle.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )
            barrier_data = json.loads(barrier.read_text(encoding="utf-8"))
            audit_records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            lifecycle_records = [json.loads(line) for line in lifecycle.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(packet["runtime_action"], RUNTIME_ACTION_CREATE_CLEARANCE)
        self.assertTrue(result["execution_allowed_now"])
        self.assertEqual(result["recheck"]["verdict"], "ALLOW_RESTORE_BARRIER_CLEARANCE")
        self.assertEqual(result["record"]["clearance_verdict"], "RESTORE_BARRIER_CLEARANCE_WRITTEN")
        self.assertEqual(barrier_data["clearance_generation_id"], "gen-move")
        self.assertEqual(barrier_data["approved_selected_moves_hash"], "move-hash")
        self.assertEqual(barrier_data["approved_atomic_execution_envelope_id"], "aee-test")
        self.assertEqual(barrier_data["approved_atomic_execution_envelope_hash"], "aee-hash-test")
        self.assertEqual(barrier_data["approved_source_bundle_hash"], "source-bundle-hash-test")
        self.assertEqual(barrier_data["clearance_expected_selected_moves"], 1)
        self.assertEqual(barrier_data["clearance_max_selected_moves"], 1)
        self.assertEqual(barrier_data["allowed_user"], "10.7.0.11")
        self.assertEqual(barrier_data["allowed_target"], "vless")
        self.assertEqual(packet["approved_plan_lock"]["schema_version"], "v7.approved-plan-lock.v1")
        self.assertEqual(packet["approved_plan_lock"]["selected_move_count"], 1)
        self.assertEqual(packet["approved_plan_lock"]["selected_moves"][0]["user_ip"], "10.7.0.11")
        self.assertEqual(packet["approved_plan_lock"]["selected_moves"][0]["important_services"], ["telegram"])
        self.assertEqual(
            packet["approved_plan_lock"]["selected_moves"][0]["candidates"][0]["service_suitability"]["per_service"]["telegram"]["status"],
            "DOWN",
        )
        self.assertFalse(packet["approved_plan_lock"]["executor_may_reselect"])
        self.assertEqual(barrier_data["approved_plan_lock"]["selected_moves"][0]["recommended_egress"], "vless")
        self.assertEqual(barrier_data["approved_plan_lock"]["selected_moves"][0]["reason"], ["current_egress_not_eligible"])
        self.assertEqual(barrier_data["approved_plan_lock_id"], packet["approved_plan_lock"]["lock_id"])
        self.assertEqual(len(audit_records), 1)
        self.assertEqual(len(lifecycle_records), 3)
        self.assertEqual(lifecycle_records[0]["record_type"], "restore_barrier_clearance_created")
        self.assertEqual(lifecycle_records[1]["record_type"], "operation_scoped_rollback_bound")
        self.assertEqual(lifecycle_records[2]["record_type"], "execution_readiness_closure_created")
        self.assertTrue(lifecycle_records[2]["execution_allowed_now"])

    def test_packet_from_preview_preserves_approved_semantic_identity(self):
        preview = self.preview_packet()
        packet = packet_from_preview(
            preview,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(packet["identity_source"], "approved_preview_packet")
        self.assertEqual(packet["packet_id"], preview["packet_id"])
        self.assertEqual(packet["operation_id"], preview["operation_id"])
        self.assertEqual(packet["decision_id"], preview["decision_id"])
        self.assertEqual(packet["authority_generation"], preview["authority_generation"])
        self.assertEqual(packet["expected"]["selected_move_hash"], preview["selected_move_hash"])
        self.assertEqual(packet["expected"]["decision_id"], preview["decision_id"])
        self.assertEqual(packet["expected"]["generation_id"], preview["authority_generation"])
        self.assertEqual(packet["constraints"]["allowed_users"], preview["allowed_users"])
        self.assertEqual(packet["constraints"]["allowed_targets"], preview["allowed_targets"])
        self.assertEqual(packet["rollback_manifest"]["rollback_manifest_id"], "rb_preview_unit_identity")
        self.assertEqual(packet["approved_plan_lock"]["identity_source"], "approved_preview_packet")
        self.assertEqual(packet["approved_plan_lock"]["packet_id"], preview["packet_id"])
        self.assertEqual(packet["approved_plan_lock"]["operation_id"], preview["operation_id"])
        self.assertEqual(packet["approved_plan_lock"]["decision_id"], preview["decision_id"])
        self.assertEqual(packet["approved_plan_lock"]["authority_generation"], preview["authority_generation"])
        self.assertEqual(packet["approved_plan_lock"]["selected_move_hash"], preview["selected_move_hash"])

    def test_delegated_policy_packet_retires_operator_approval_but_preserves_lease_identity(self):
        preview = self.preview_packet()
        packet = packet_from_preview(
            preview,
            approval_author="",
            approval_reviewer="",
            delegated_policy_authority=self.delegated_policy_authority(),
        )
        lease = create_execution_lease_from_packet(packet, source_preview=preview)

        self.assertEqual(packet["approvals"], [])
        self.assertEqual(packet["delegated_policy_authority"]["authority_basis"], "DELEGATED_AUTONOMY_POLICY")
        self.assertEqual(lease["immutable_packet_identity"]["packet_id"], preview["packet_id"])
        self.assertEqual(lease["immutable_packet_identity"]["operation_id"], preview["operation_id"])
        self.assertEqual(lease["immutable_packet_identity"]["selected_move_hash"], preview["selected_move_hash"])

    def test_delegated_policy_packet_fails_closed_on_scope_expansion(self):
        for field, value in (
            ("max_users_per_transaction", 2),
            ("max_concurrent_transactions", 2),
            ("action_class", "small-batch movement"),
            ("self_expansion_allowed", True),
            ("packet_reuse", "ALLOWED"),
        ):
            authority = self.delegated_policy_authority()
            authority[field] = value
            with self.subTest(field=field), self.assertRaises(PacketError):
                packet_from_preview(
                    self.preview_packet(),
                    approval_author="",
                    approval_reviewer="",
                    delegated_policy_authority=authority,
                )

    def test_packet_from_full_governed_cycle_extracts_preview_identity(self):
        preview = self.preview_packet()
        full_cycle = {
            "schema_version": "v7.governed-canary.knowledge-gated-dry-run-cycle.v1",
            "cycle_id": preview["authority_generation"],
            "packet_preview": preview,
            "runtime_lifecycle_preview": {
                "packet_id": preview["packet_id"],
                "selected_move_hash": preview["selected_move_hash"],
            },
        }

        extracted = extract_packet_preview(full_cycle)
        packet = packet_from_preview(
            full_cycle,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(extracted["packet_id"], preview["packet_id"])
        self.assertEqual(packet["packet_id"], preview["packet_id"])
        self.assertEqual(packet["operation_id"], preview["operation_id"])
        self.assertEqual(packet["decision_id"], preview["decision_id"])
        self.assertEqual(packet["authority_generation"], preview["authority_generation"])
        self.assertEqual(packet["expected"]["selected_move_hash"], preview["selected_move_hash"])

    def test_packet_from_preview_recomputes_execution_envelope_with_approved_hash(self):
        preview = self.preview_packet()
        preview["source_hashes"] = {
            "users_registry": "users-hash-unit",
            "egress_registry": "egress-hash-unit",
            "service_matrix": "matrix-hash-unit",
        }
        preview["snapshot_bundle_hash"] = "snapshot-bundle-hash-unit"
        expected_runtime_snapshot = sha256_json({
            "users_registry_hash": "users-hash-unit",
            "egress_registry_hash": "egress-hash-unit",
            "selected_move_hash": "preview-selected-hash-unit",
        })
        expected_source_bundle = sha256_json(preview["source_hashes"])
        expected_envelope = sha256_json({
            "planner_generation_id": "cycle-unit-identity",
            "selected_move_hash": "preview-selected-hash-unit",
            "selected_move_count": 1,
            "runtime_snapshot_hash": expected_runtime_snapshot,
            "source_bundle_hash": expected_source_bundle,
            "snapshot_bundle_hash": "snapshot-bundle-hash-unit",
        })

        packet = packet_from_preview(
            preview,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(packet["expected"]["runtime_snapshot_hash"], expected_runtime_snapshot)
        self.assertEqual(packet["expected"]["source_bundle_hash"], expected_source_bundle)
        self.assertEqual(packet["expected"]["snapshot_bundle_hash"], "snapshot-bundle-hash-unit")
        self.assertEqual(packet["expected"]["atomic_execution_envelope_hash"], expected_envelope)
        self.assertEqual(packet["expected"]["atomic_execution_envelope_id"], "aee_" + expected_envelope[:24])

    def test_preview_derived_packet_clearance_recheck_does_not_require_rebuilt_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            packet = packet_from_preview(
                self.preview_packet(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action_preview",
                restore_barrier_file=barrier,
            )

        self.assertEqual(result["recheck"]["verdict"], "ALLOW_RESTORE_BARRIER_CLEARANCE")
        self.assertEqual(result["recheck"]["checks"]["identity_source"], "approved_preview_packet")
        self.assertEqual(result["clearance_preview"]["clearance"]["packet_id"], "pkt_preview_unit_identity")
        self.assertEqual(
            result["clearance_preview"]["clearance"]["approved_selected_moves_hash"],
            "preview-selected-hash-unit",
        )
        self.assertFalse(result["record_written"])

    def test_execution_lease_allows_immediate_approved_packet_execution_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            lease = create_execution_lease_from_preview(
                self.preview_packet(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                lease["packet"],
                audit,
                state,
                mode="runtime_action_preview",
                restore_barrier_file=barrier,
            )

        self.assertTrue(execution_lease_state(lease)["active"])
        self.assertEqual(result["recheck"]["verdict"], "ALLOW_RESTORE_BARRIER_CLEARANCE")
        self.assertEqual(result["clearance_preview"]["clearance"]["packet_id"], "pkt_preview_unit_identity")
        self.assertFalse(result["record_written"])

    def test_execution_lease_from_approved_packet_uses_same_packet_id(self):
        packet = packet_from_preview(
            self.preview_packet(),
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )
        lease = create_execution_lease_from_packet(packet, source_preview=self.preview_packet())

        self.assertEqual(lease["packet"]["packet_id"], packet["packet_id"])
        self.assertEqual(lease["immutable_packet_identity"]["packet_id"], packet["packet_id"])
        self.assertEqual(lease["immutable_packet_identity"]["decision_id"], packet["decision_id"])
        self.assertEqual(lease["immutable_packet_identity"]["operation_id"], packet["operation_id"])
        self.assertEqual(lease["immutable_packet_identity"]["selected_move_hash"], packet["expected"]["selected_move_hash"])
        self.assertEqual(lease["immutable_packet_identity"]["user"], "10.7.0.11")
        self.assertEqual(lease["immutable_packet_identity"]["source"], "1")
        self.assertEqual(lease["immutable_packet_identity"]["target"], "vless")

    def test_execution_lease_from_packet_never_regenerates_packet(self):
        preview = self.preview_packet()
        packet = packet_from_preview(
            preview,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )
        regenerated_preview = dict(preview)
        regenerated_preview["packet_id"] = "pkt_preview_regenerated"
        regenerated_preview["selected_move_hash"] = "different-selected-hash"

        lease = create_execution_lease_from_packet(packet, source_preview=regenerated_preview)

        self.assertEqual(lease["packet"]["packet_id"], "pkt_preview_unit_identity")
        self.assertEqual(lease["packet"]["expected"]["selected_move_hash"], "preview-selected-hash-unit")
        self.assertNotEqual(lease["packet"]["packet_id"], regenerated_preview["packet_id"])

    def test_approval_binding_rejects_changed_preview_identity(self):
        preview = self.preview_packet()
        approved_identity = preview_packet_identity(preview)
        changed_preview = dict(preview)
        changed_preview["allowed_targets"] = ["awg3"]
        changed_preview["rollback_manifest_preview"] = {
            **preview["rollback_manifest_preview"],
            "items": [
                {
                    **preview["rollback_manifest_preview"]["items"][0],
                    "forward_target": "awg3",
                }
            ],
        }

        binding = approved_packet_binding_status(preview_packet_identity(changed_preview), approved_identity)

        self.assertFalse(binding["ok"])
        self.assertEqual(binding["mismatches"][0]["field"], "target")

    def test_create_execution_lease_from_preview_requires_matching_approved_identity(self):
        preview = self.preview_packet()
        approved_identity = preview_packet_identity(preview)
        approved_identity["packet_id"] = "pkt_preview_other"

        with self.assertRaises(PacketError):
            create_execution_lease_from_preview(
                preview,
                approval_author="operator-a",
                approval_reviewer="operator-b",
                approved_identity=approved_identity,
            )

    def test_apply_consumes_identical_packet_from_execution_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            preview = self.preview_packet()
            preview["source_hashes"] = {
                "users_registry": sha256_file(state / "users.registry"),
                "egress_registry": sha256_file(state / "egress.registry"),
            }
            preview["snapshot_bundle_hash"] = "snapshot-unit-operational-authority"
            packet = packet_from_preview(
                preview,
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            lease = create_execution_lease_from_packet(packet, source_preview=preview)
            result = execute_packet(
                lease["packet"],
                audit,
                state,
                mode="runtime_action_preview",
                restore_barrier_file=barrier,
            )

        self.assertEqual(packet_identity(lease["packet"]), lease["immutable_packet_identity"])
        self.assertEqual(result["recheck"]["verdict"], "ALLOW_RESTORE_BARRIER_CLEARANCE")
        self.assertEqual(result["clearance_preview"]["clearance"]["packet_id"], packet["packet_id"])
        package = result["operational_authority_package"]
        self.assertEqual(package["status"], "OPERATIONAL_AUTHORITY_RESTORE_BARRIER_READY")
        self.assertFalse(package["actionable"])
        self.assertEqual(package["packet_identity"]["packet_id"], packet["packet_id"])
        self.assertEqual(package["scope"]["max_users"], 1)
        self.assertIn("runtime_apply", package["forbidden_effects"])
        self.assertEqual(
            result["clearance_preview"]["clearance"]["approved_selected_moves_hash"],
            packet["expected"]["selected_move_hash"],
        )

    def test_execution_lease_preserves_on_freshness_only_change(self):
        lease = create_execution_lease_from_preview(
            self.preview_packet(),
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )
        current_state = dict(lease["material_state"])
        current_state["freshness_timestamp"] = "2026-06-26T01:00:00Z"
        current_state["snapshot_generation"] = "new-snapshot-generation"

        state = execution_lease_state(lease, current_material_state=current_state)

        self.assertTrue(state["active"])
        self.assertFalse(state["material_state_change"])
        self.assertEqual(state["changed_fields"], [])
        self.assertEqual(state["lease_keep_reason"], "no_material_state_change")

    def test_execution_lease_preserves_regenerated_packet_with_identical_semantic_plan(self):
        lease = create_execution_lease_from_preview(
            self.preview_packet(),
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )
        current_state = dict(lease["material_state"])
        current_state["packet_id"] = "pkt_preview_regenerated_same_plan"
        current_state["operation_id"] = "govdry_regenerated_same_plan"

        state = execution_lease_state(lease, current_material_state=current_state)

        self.assertTrue(state["active"])
        self.assertFalse(state["material_state_change"])
        self.assertEqual(state["changed_fields"], [])

    def test_execution_lease_invalidates_on_target_change(self):
        lease = create_execution_lease_from_preview(
            self.preview_packet(),
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )
        current_state = dict(lease["material_state"])
        current_state["target_channel"] = ["awg3"]

        state = execution_lease_state(lease, current_material_state=current_state)

        self.assertFalse(state["active"])
        self.assertEqual(state["status"], "INVALIDATED")
        self.assertEqual(state["changed_fields"], ["target_channel"])

    def test_execution_lease_invalidates_on_rollback_policy_authority_or_hash_change(self):
        cases = {
            "rollback_target": ["awg0"],
            "policy_generation": "policy-generation-next",
            "authority_generation": "authority-generation-next",
            "selected_move_hash": "selected-move-hash-next",
        }
        for field, value in cases.items():
            with self.subTest(field=field):
                lease = create_execution_lease_from_preview(
                    self.preview_packet(),
                    approval_author="operator-a",
                    approval_reviewer="operator-b",
                )
                if field == "policy_generation":
                    lease["material_state"]["policy_generation"] = "policy-generation-current"
                current_state = dict(lease["material_state"])
                current_state[field] = value

                state = execution_lease_state(lease, current_material_state=current_state)

                self.assertFalse(state["active"])
                self.assertEqual(state["status"], "INVALIDATED")
                self.assertEqual(state["changed_fields"], [field])

    def test_execution_lease_expires_and_cancel_releases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lease_file = root / "execution-lease.json"
            lease = create_execution_lease_from_preview(
                self.preview_packet(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
                ttl_seconds=1,
            )
            write_result = write_execution_lease(lease_file, lease)
            duplicate = write_execution_lease(lease_file, lease)
            cancel = cancel_execution_lease(lease_file, reason="operator-test-cancel")
            cancelled = json.loads(lease_file.read_text(encoding="utf-8"))
            expired = create_execution_lease_from_preview(
                self.preview_packet(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
                ttl_seconds=1,
            )

        self.assertTrue(write_result["ok"])
        self.assertEqual(duplicate["verdict"], "DENY_DUPLICATE_EXECUTION_LEASE")
        self.assertTrue(cancel["ok"])
        self.assertFalse(execution_lease_state(cancelled)["active"])
        past = datetime.now(timezone.utc) + timedelta(seconds=2)
        self.assertEqual(execution_lease_state(expired, now=past)["status"], "EXPIRED")

    def test_finish_execution_lease_preserves_successful_apply_facts_and_releases_duplicate_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lease_file = root / "execution-lease.json"
            lease = create_execution_lease_from_preview(
                self.preview_packet(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            write_result = write_execution_lease(lease_file, lease)
            finish = finish_execution_lease(
                lease_file,
                status="EXECUTION_FINISHED",
                reason="selected_moves_applied",
                operation={
                    "operation_id": "op-finished",
                    "terminal_state": "APPLIED",
                    "terminal_reason": "selected_moves_applied",
                    "apply_result": {
                        "applied": True,
                        "results": [{"user_ip": "10.7.0.5", "from": "vless", "to": "awg3"}],
                    },
                },
            )
            finished = json.loads(lease_file.read_text(encoding="utf-8"))
            second_lease = create_execution_lease_from_preview(
                self.preview_packet(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            second_write = write_execution_lease(lease_file, second_lease)

        self.assertTrue(write_result["ok"])
        self.assertTrue(finish["ok"])
        self.assertEqual(execution_lease_state(finished)["status"], "EXECUTION_FINISHED")
        self.assertFalse(execution_lease_state(finished)["active"])
        self.assertTrue(finished["apply_executed"])
        self.assertEqual(finished["users_moved"], 1)
        self.assertEqual(finished["operation_terminal_state"], "APPLIED")
        self.assertEqual(second_write["verdict"], "EXECUTION_LEASE_WRITTEN")

    def test_runtime_action_preview_builds_clearance_without_writes_and_survives_reread(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            lifecycle = root / "lifecycle.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            first = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action_preview",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )
            second = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action_preview",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )

        self.assertEqual(first["recheck"]["verdict"], "ALLOW_RESTORE_BARRIER_CLEARANCE")
        self.assertEqual(first["clearance_preview"]["verdict"], "RESTORE_BARRIER_CLEARANCE_PREVIEW_VALID")
        self.assertEqual(first["clearance_preview"]["clearance"]["clearance_generation_id"], "gen-move")
        self.assertEqual(first["clearance_preview"]["clearance"]["approved_plan_lock"]["selected_move_count"], 1)
        self.assertFalse(first["record_written"])
        self.assertFalse(first["runtime_mutation"])
        self.assertFalse(first["real_runtime_action_performed"])
        self.assertFalse(first["execution_allowed_now"])
        self.assertFalse(barrier.exists())
        self.assertFalse(audit.exists())
        self.assertFalse(lifecycle.exists())
        self.assertEqual(second["recheck"]["verdict"], "ALLOW_RESTORE_BARRIER_CLEARANCE")
        self.assertEqual(second["clearance_preview"]["clearance"]["approved_selected_moves_hash"], "move-hash")

    def test_runtime_action_preview_preserves_duplicate_owner_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            write_json(
                barrier,
                {
                    "generation_clearance": True,
                    "allow_post_ttl_apply": True,
                    "clearance_expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                    "owner": "other-owner",
                },
            )
            before = barrier.read_text(encoding="utf-8")
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action_preview",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
            )
            after = barrier.read_text(encoding="utf-8")

        self.assertEqual(result["recheck"]["verdict"], "DENY_DUPLICATE_CLEARANCE_OWNER")
        self.assertIn("duplicate_clearance_owner", result["recheck"]["errors"])
        self.assertFalse(result["record_written"])
        self.assertFalse(result["runtime_mutation"])
        self.assertEqual(before, after)
        self.assertFalse(audit.exists())

    def test_packet_from_plan_respects_clearance_selected_move_count(self):
        plan = self.movement_plan()
        plan["decisions"].extend([
            {
                "user_ip": "10.7.0.12",
                "current_egress": "1",
                "recommended_egress": "vless",
                "action": "switch",
                "move_type": "failover",
            },
            {
                "user_ip": "10.7.0.13",
                "current_egress": "1",
                "recommended_egress": "vless",
                "action": "switch",
                "move_type": "failover",
            },
        ])

        packet = packet_from_plan(
            plan,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(packet["expected"]["selected_move_count"], 1)
        self.assertEqual(packet["expected"]["atomic_execution_envelope_id"], "aee-test")
        self.assertEqual(packet["expected"]["atomic_execution_envelope_hash"], "aee-hash-test")
        self.assertEqual(packet["expected"]["source_bundle_hash"], "source-bundle-hash-test")
        self.assertEqual(packet["constraints"]["selected_move_budget"], 1)
        self.assertEqual(packet["constraints"]["allowed_users"], ["10.7.0.11"])
        self.assertEqual(len(packet["rollback_manifest"]["items"]), 1)
        self.assertEqual(packet["rollback_manifest"]["items"][0]["user_ip"], "10.7.0.11")

    def test_packet_from_plan_prefers_final_selected_moves_over_decisions(self):
        plan = self.movement_plan()
        plan["safety"]["restore_barrier"]["clearance_selected_moves_before_guard"] = 2
        plan["selected_moves"] = [
            {
                "user_ip": "10.7.0.2",
                "current_egress": "amneziawg-exec-20260528-10-8-1-14",
                "recommended_egress": "awg3",
                "move_type": "failover",
            },
            {
                "user_ip": "10.7.0.3",
                "current_egress": "amneziawg-exec-20260528-10-8-1-14",
                "recommended_egress": "awg3",
                "move_type": "failover",
            },
        ]
        plan["decisions"] = [
            {
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg3",
                "action": "switch",
                "move_type": "rebalance",
            },
            {
                "user_ip": "10.0.0.3",
                "current_egress": "vless",
                "recommended_egress": "awg3",
                "action": "switch",
                "move_type": "rebalance",
            },
        ]

        packet = packet_from_plan(
            plan,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(packet["expected"]["selected_move_count"], 2)
        self.assertEqual(packet["constraints"]["allowed_users"], ["10.7.0.2", "10.7.0.3"])
        self.assertEqual(packet["constraints"]["allowed_targets"], ["awg3"])
        self.assertEqual([item["user_ip"] for item in packet["rollback_manifest"]["items"]], ["10.7.0.2", "10.7.0.3"])
        self.assertEqual([item["user_ip"] for item in packet["approved_plan_lock"]["selected_moves"]], ["10.7.0.2", "10.7.0.3"])
        self.assertEqual(packet["approved_plan_lock"]["allowed_targets"], ["awg3"])

    def test_packet_from_plan_uses_pre_barrier_selected_moves_when_final_selected_suppressed(self):
        plan = self.movement_plan()
        plan["selected_moves"] = []
        plan["safety"]["restore_barrier"]["clearance_selected_moves_before_guard"] = 2
        plan["safety"]["restore_barrier"]["approved_candidate_moves_before_guard"] = [
            {
                "user_ip": "10.7.0.2",
                "current_egress": "amneziawg-exec-20260528-10-8-1-14",
                "recommended_egress": "vless",
                "move_type": "failover",
            },
            {
                "user_ip": "10.7.0.3",
                "current_egress": "amneziawg-exec-20260528-10-8-1-14",
                "recommended_egress": "vless",
                "move_type": "failover",
            },
        ]
        plan["decisions"] = [
            {
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "awg3",
                "action": "switch",
                "move_type": "rebalance",
            },
            {
                "user_ip": "10.0.0.3",
                "current_egress": "1",
                "recommended_egress": "awg3",
                "action": "switch",
                "move_type": "rebalance",
            },
        ]

        packet = packet_from_plan(
            plan,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(packet["expected"]["selected_move_count"], 2)
        self.assertEqual(packet["constraints"]["allowed_users"], ["10.7.0.2", "10.7.0.3"])
        self.assertEqual(packet["constraints"]["allowed_targets"], ["vless"])
        self.assertEqual([item["user_ip"] for item in packet["approved_plan_lock"]["selected_moves"]], ["10.7.0.2", "10.7.0.3"])

    def test_packet_from_plan_uses_diagnostic_pre_restore_rows_before_decision_fallback(self):
        plan = self.movement_plan()
        plan["selected_moves"] = []
        plan["safety"]["restore_barrier"]["clearance_selected_moves_before_guard"] = 0
        plan["safety"]["restore_barrier"]["approved_candidate_moves_before_guard"] = []
        plan["safety"].setdefault("selected_moves_diagnostics", {})["selected_moves_before_restore_barrier_rows"] = [
            {
                "user_ip": "10.7.0.2",
                "current_egress": "wireguard-incident",
                "recommended_egress": "awg0",
                "move_type": "failover",
            },
            {
                "user_ip": "10.7.0.3",
                "current_egress": "wireguard-incident",
                "recommended_egress": "vless",
                "move_type": "failover",
            },
        ]
        plan["decisions"] = [
            {
                "user_ip": f"10.7.0.{idx}",
                "current_egress": "wireguard-incident",
                "recommended_egress": "awg0",
                "action": "switch",
                "move_type": "failover",
            }
            for idx in range(2, 7)
        ]

        selected = selected_moves_from_plan(plan)
        packet = packet_from_plan(
            plan,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(selected["selected_move_count"], 2)
        self.assertEqual([move["user_ip"] for move in selected["moves"]], ["10.7.0.2", "10.7.0.3"])
        self.assertEqual(packet["expected"]["selected_move_count"], 2)
        self.assertEqual(packet["constraints"]["allowed_users"], ["10.7.0.2", "10.7.0.3"])
        self.assertEqual(packet["constraints"]["allowed_targets"], ["awg0", "vless"])

    def test_packet_from_plan_recomputes_nonzero_envelope_for_pre_barrier_moves(self):
        plan = self.movement_plan()
        plan["selected_moves"] = []
        plan["safety"]["restore_barrier"]["clearance_selected_moves_before_guard"] = 2
        plan["safety"]["restore_barrier"]["clearance_selected_moves_hash"] = "approved-move-hash"
        plan["safety"]["restore_barrier"]["approved_candidate_moves_before_guard"] = [
            {
                "user_ip": "10.7.0.2",
                "current_egress": "amneziawg-exec-20260528-10-8-1-14",
                "recommended_egress": "awg3",
                "move_type": "failover",
            },
            {
                "user_ip": "10.7.0.3",
                "current_egress": "amneziawg-exec-20260528-10-8-1-14",
                "recommended_egress": "awg0",
                "move_type": "failover",
            },
        ]
        source_hashes = {
            "service_matrix": "matrix-hash",
            "quality_summary": "quality-hash",
            "service_preferences": "prefs-hash",
            "users_registry": "users-hash",
            "egress_registry": "egress-hash",
        }
        plan["safety"]["atomic_execution_envelope"] = {
            "schema_version": "v7.atomic-execution-envelope.v1",
            "envelope_id": "aee-zero-selected",
            "envelope_hash": "zero-selected-envelope-hash",
            "selected_move_hash": EMPTY_SELECTED_MOVES_HASH,
            "selected_move_count": 0,
            "runtime_snapshot_hash": "zero-runtime-snapshot",
            "source_bundle_hash": "stale-source-bundle",
            "snapshot_bundle_hash": "snapshot-bundle-hash",
            "source_bundle": {"source_hashes": source_hashes},
        }
        expected_runtime_snapshot = sha256_json({
            "users_registry_hash": "users-hash",
            "egress_registry_hash": "egress-hash",
            "selected_move_hash": "approved-move-hash",
        })
        expected_envelope_hash = sha256_json({
            "planner_generation_id": "gen-move",
            "selected_move_hash": "approved-move-hash",
            "selected_move_count": 2,
            "runtime_snapshot_hash": expected_runtime_snapshot,
            "source_bundle_hash": sha256_json(source_hashes),
            "snapshot_bundle_hash": "snapshot-bundle-hash",
        })

        packet = packet_from_plan(
            plan,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(packet["expected"]["selected_move_count"], 2)
        self.assertEqual(packet["expected"]["selected_move_hash"], "approved-move-hash")
        self.assertEqual(packet["expected"]["runtime_snapshot_hash"], expected_runtime_snapshot)
        self.assertEqual(packet["expected"]["atomic_execution_envelope_hash"], expected_envelope_hash)
        self.assertEqual(packet["expected"]["atomic_execution_envelope_id"], "aee_" + expected_envelope_hash[:24])
        self.assertEqual(packet["expected"]["source_bundle_hash"], sha256_json(source_hashes))
        self.assertEqual(packet["constraints"]["allowed_targets"], ["awg0", "awg3"])

    def test_nonzero_packet_rejects_generation_and_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            stale_plan = self.movement_plan()
            stale_plan["safety"]["generation"]["planner_generation_id"] = "stale-gen"
            stale_hash_plan = self.movement_plan()
            stale_hash_plan["safety"]["restore_barrier"]["clearance_selected_moves_hash"] = "other-hash"
            stale_envelope_plan = self.movement_plan()
            stale_envelope_plan["safety"]["atomic_execution_envelope"]["envelope_hash"] = "other-envelope-hash"

            stale_generation = runtime_recheck(packet, state, planner_snapshot=stale_plan)
            stale_hash = runtime_recheck(packet, state, planner_snapshot=stale_hash_plan)
            stale_envelope = runtime_recheck(packet, state, planner_snapshot=stale_envelope_plan)

        self.assertEqual(stale_generation["verdict"], "DENY_HASH_MISMATCH")
        self.assertIn("generation_id", stale_generation["errors"])
        self.assertEqual(stale_hash["verdict"], "DENY_HASH_MISMATCH")
        self.assertIn("selected_move_hash", stale_hash["errors"])
        self.assertEqual(stale_envelope["verdict"], "DENY_HASH_MISMATCH")
        self.assertIn("atomic_execution_envelope_hash", stale_envelope["errors"])

    def test_clearance_writer_rejects_duplicate_active_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            lifecycle = root / "lifecycle.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            write_json(
                barrier,
                {
                    "generation_clearance": True,
                    "allow_post_ttl_apply": True,
                    "clearance_expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                    "owner": "other-owner",
                },
            )
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )

        self.assertFalse(result["execution_allowed_now"])
        self.assertEqual(result["recheck"]["verdict"], "DENY_DUPLICATE_CLEARANCE_OWNER")
        self.assertIn("duplicate_clearance_owner", result["recheck"]["errors"])
        self.assertFalse(lifecycle.exists())

    def test_clearance_writer_allows_canonical_owner_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            lifecycle = root / "lifecycle.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            write_json(
                barrier,
                {
                    "generation_clearance": True,
                    "allow_post_ttl_apply": True,
                    "clearance_expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                    "clearance_generation_id": "old-gen",
                    "owner": CANONICAL_CLEARANCE_OWNER,
                },
            )
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )
            refreshed = json.loads(barrier.read_text(encoding="utf-8"))
            backups = list(state.glob("autoswitch-restore-barrier.json.backup-c1-*"))

        self.assertTrue(result["execution_allowed_now"])
        self.assertEqual(result["record"]["clearance_verdict"], "RESTORE_BARRIER_CLEARANCE_WRITTEN")
        self.assertEqual(refreshed["clearance_generation_id"], "gen-move")
        self.assertEqual(refreshed["owner"], CANONICAL_CLEARANCE_OWNER)
        self.assertEqual(len(backups), 1)

    def test_ct_m0f_one_generation_authority_request_and_exact_once_decision(self):
        now = datetime(2026, 8, 6, 3, 0, tzinfo=timezone.utc)
        pool = {
            "total_enabled_certification_users": 41,
            "max_enabled_certification_users_on_one_active_source": 41,
            "fingerprint": "f" * 64,
            "registry_hashes": {
                "users_registry": "u" * 64,
                "egress_registry": "e" * 64,
            },
        }
        request = operator_execution.build_ct_m0f_controlled_validation_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="vless",
            current_pool_status=pool,
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="a" * 64,
            sample_kind="cold",
            now=now,
        )
        validation = operator_execution.validate_ct_m0f_controlled_validation_authority_request(
            request,
            decision=operator_execution.CT_M0F_CONTROLLED_VALIDATION_APPROVAL,
            now=now + timedelta(seconds=1),
        )
        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(request["scope"]["max_users"], 1)
        self.assertEqual(request["scope"]["max_concurrent_transactions"], 1)
        self.assertFalse(request["scope"]["automatic_campaign_progression"])

        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "operator-audit.jsonl"
            registered = operator_execution.register_ct_m0f_controlled_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            first = operator_execution.record_ct_m0f_controlled_validation_authority_decision(
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_CONTROLLED_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            duplicate = operator_execution.record_ct_m0f_controlled_validation_authority_decision(
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_CONTROLLED_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=3),
            )
            records = operator_execution.read_audit_records(audit)

        self.assertEqual(registered["status"], "REGISTERED")
        self.assertEqual(first["status"], "APPROVED")
        self.assertEqual(duplicate["status"], "ALREADY_RECORDED_EXACT")
        self.assertEqual(
            len([
                row for row in records
                if row.get("record_type")
                == operator_execution.CT_M0F_CONTROLLED_VALIDATION_DECISION_RECORD_TYPE
            ]),
            1,
        )
        self.assertFalse(first["runtime_apply"])
        self.assertEqual(first["users_moved"], 0)

    def test_ct_m0f_expired_or_broadened_request_is_rejected(self):
        now = datetime(2026, 8, 6, 3, 0, tzinfo=timezone.utc)
        request = operator_execution.build_ct_m0f_controlled_validation_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="vless",
            current_pool_status={
                "total_enabled_certification_users": 1,
                "max_enabled_certification_users_on_one_active_source": 1,
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="a" * 64,
            now=now,
        )
        expired = operator_execution.validate_ct_m0f_controlled_validation_authority_request(
            request,
            decision="DECLINE",
            now=now + timedelta(hours=25),
        )
        broadened = copy.deepcopy(request)
        broadened["scope"]["max_users"] = 2
        broadened["request_hash"] = operator_execution.ct_m0f_controlled_validation_request_hash(
            broadened
        )
        broadened["request_id"] = "ctm0fauth_r1_" + broadened["request_hash"][:24]
        broadened_validation = operator_execution.validate_ct_m0f_controlled_validation_authority_request(
            broadened,
            decision="DECLINE",
            now=now + timedelta(seconds=1),
        )

        self.assertIn("ct_m0f_validation_request_expired", expired["errors"])
        self.assertIn("ct_m0f_validation_blast_radius_invalid", broadened_validation["errors"])

    def test_ct_m0f_approved_admission_is_consumed_once_and_lineage_is_proven(self):
        now = datetime(2026, 8, 6, 3, 0, tzinfo=timezone.utc)
        request = operator_execution.build_ct_m0f_controlled_validation_authority_request(
            active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            source_id="vless",
            current_pool_status={
                "total_enabled_certification_users": 1,
                "max_enabled_certification_users_on_one_active_source": 1,
            },
            current_policy_contract_id="sdpc_current",
            current_policy_contract_hash="a" * 64,
            now=now,
        )
        lineage = dict(
            request_id=request["request_id"],
            request_hash=request["request_hash"],
            validation_generation_id=request["validation_generation_id"],
            packet_id="packet-exact",
            operation_id="operation-exact",
            lease_id="lease-exact",
            user="10.7.0.18",
            source="vless",
            target="awg0",
        )
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "operator-audit.jsonl"
            operator_execution.register_ct_m0f_controlled_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            operator_execution.record_ct_m0f_controlled_validation_authority_decision(
                request_id=request["request_id"], request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_CONTROLLED_VALIDATION_APPROVAL,
                actor_id="independent-authority-test", audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            first = operator_execution.consume_ct_m0f_controlled_validation_admission(
                **lineage, audit_store=audit, now=now + timedelta(seconds=3),
            )
            proof = operator_execution.validate_ct_m0f_controlled_validation_consumption(
                **lineage, audit_store=audit,
            )
            duplicate = operator_execution.consume_ct_m0f_controlled_validation_admission(
                **lineage, audit_store=audit, now=now + timedelta(seconds=4),
            )
        self.assertTrue(first["ok"])
        self.assertTrue(proof["ok"])
        self.assertFalse(duplicate["ok"])
        self.assertIn("ct_m0f_validation_admission_already_consumed", duplicate["errors"])

    def test_ct_m0f_standing_policy_activation_and_sample_exact_once(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            audit = root / "operator-audit.jsonl"
            policy.write_text("{}\n", encoding="utf-8")
            request = operator_execution.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=operator_execution.sha256_file(policy),
                now=now,
            )
            registered = operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            pending = operator_execution.pending_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=operator_execution.sha256_file(policy),
                audit_store=audit,
                now=now + timedelta(seconds=1),
            )
            activated = operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            reactivated = operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=3),
            )
            contract = activated["contract"]
            lineage = dict(
                implementation_fingerprint="f" * 64,
                validation_generation_id="ctm0fgen_one",
                packet_id="packet-one",
                operation_id="operation-one",
                lease_id="lease-one",
                user="10.7.0.18",
                source="vless",
                target="awg0",
            )
            first = operator_execution.reserve_ct_m0f_standing_validation_sample(
                policy, **lineage, audit_store=audit, now=now + timedelta(seconds=4),
            )
            duplicate = operator_execution.reserve_ct_m0f_standing_validation_sample(
                policy, **lineage, audit_store=audit, now=now + timedelta(seconds=5),
            )
            concurrent = operator_execution.reserve_ct_m0f_standing_validation_sample(
                policy,
                **{**lineage, "validation_generation_id": "ctm0fgen_two", "packet_id": "packet-two", "operation_id": "operation-two", "lease_id": "lease-two"},
                audit_store=audit,
                now=now + timedelta(seconds=6),
            )
            reservation_id = first["reservation"]["reservation_id"]
            evidence = {
                "status": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS",
                "sample_kind": "cold",
                "validation_generation_id": "ctm0fgen_one",
                "metrics": {"control_plane_and_kernel_path_cutover_latency_ms": 100.0},
            }
            forward = operator_execution.record_ct_m0f_standing_validation_forward_evidence(
                reservation_id=reservation_id,
                sample_evidence=evidence,
                audit_store=audit,
                now=now + timedelta(seconds=7),
            )
            terminal = operator_execution.record_ct_m0f_standing_validation_sample_terminal(
                reservation_id=reservation_id,
                sample_valid=True,
                sample_evidence=evidence,
                terminal_reason="verified_cutover_and_baseline_reset_complete",
                audit_store=audit,
                now=now + timedelta(seconds=8),
            )
            budget = operator_execution.ct_m0f_standing_validation_budget_status(
                contract,
                "f" * 64,
                audit_records=operator_execution.read_audit_records(audit),
            )

        self.assertEqual(registered["status"], "REGISTERED")
        self.assertEqual(pending["request_id"], request["request_id"])
        self.assertFalse(activated["runtime_apply"])
        self.assertEqual(activated["users_moved"], 0)
        self.assertEqual(reactivated["status"], "ALREADY_ACTIVATED_EXACT")
        self.assertTrue(first["ok"])
        self.assertEqual(duplicate["status"], "ALREADY_RESERVED_EXACT")
        self.assertFalse(concurrent["ok"])
        self.assertIn("ct_m0f_standing_active_operation_exists", concurrent["errors"])
        self.assertEqual(forward["status"], "RECORDED")
        self.assertEqual(terminal["status"], "RECORDED")
        self.assertEqual(budget["valid_samples"], 1)
        self.assertEqual(budget["cold_valid_samples"], 1)
        self.assertEqual(budget["next_sample_kind"], "warm")

    def test_ct_m0f_transaction_reservation_blocks_only_independent_reassignment(self):
        now = datetime(2026, 8, 25, 9, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            audit = root / "operator-execution-audit.jsonl"
            policy.write_text("{}\n", encoding="utf-8")
            request = operator_execution.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=operator_execution.sha256_file(policy),
                now=now,
            )
            operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            contract = operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )["contract"]
            reserved = operator_execution.reserve_ct_m0f_standing_validation_transaction(
                contract=contract,
                implementation_fingerprint="f" * 64,
                user="10.7.0.18",
                source="exec-source",
                target="awg0",
                sample_binding_fingerprint="b" * 64,
                source_reservation_id="source-reservation",
                source_fingerprint="c" * 64,
                audit_store=audit,
                now=now + timedelta(seconds=3),
            )
            reservation_id = reserved["reservation"]["transaction_reservation_id"]
            independent = operator_execution.ct_m0f_standing_validation_transaction_guard(
                user="10.7.0.18", source="exec-source", target="awg0",
                audit_store=audit, now=now + timedelta(seconds=4),
            )
            bound = operator_execution.bind_ct_m0f_standing_validation_transaction(
                transaction_reservation_id=reservation_id,
                packet_id="packet-exact",
                operation_id="operation-exact",
                lease_id="lease-exact",
                matrix_sample_binding_fingerprint="d" * 64,
                audit_store=audit,
                now=now + timedelta(seconds=5),
            )
            governed = operator_execution.ct_m0f_standing_validation_transaction_guard(
                user="10.7.0.18", source="exec-source", target="awg0",
                operation_id="operation-exact", audit_store=audit,
                now=now + timedelta(seconds=6),
            )
            wrong_operation = operator_execution.ct_m0f_standing_validation_transaction_guard(
                user="10.7.0.18", source="exec-source", target="awg0",
                operation_id="operation-other", audit_store=audit,
                now=now + timedelta(seconds=6),
            )
            released = operator_execution.release_ct_m0f_standing_validation_transaction(
                transaction_reservation_id=reservation_id,
                reason="verified_terminal", audit_store=audit,
                now=now + timedelta(seconds=7),
            )
            after_release = operator_execution.ct_m0f_standing_validation_transaction_guard(
                user="10.7.0.18", source="exec-source", target="awg0",
                audit_store=audit, now=now + timedelta(seconds=8),
            )

        self.assertTrue(reserved["ok"])
        self.assertFalse(independent["ok"])
        self.assertEqual(
            independent["status"],
            "CT_M0F_TRANSACTION_RESERVATION_PROTECTS_IDENTITY",
        )
        self.assertTrue(bound["ok"])
        self.assertEqual(
            bound["binding"]["matrix_sample_binding_fingerprint"],
            "d" * 64,
        )
        self.assertTrue(governed["ok"])
        self.assertFalse(wrong_operation["ok"])
        self.assertTrue(released["ok"])
        self.assertTrue(after_release["independent_reassignment_allowed"])

    def test_ct_m0f_topology_request_uses_active_standing_contract_basis(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        manifest = {
            "validation_profile": "CT_M0F_ONE_USER_CONTROLLED_CONDITION",
            "selected_option": "OPTION_2_PROVISION_EXISTING_VALID_DRAFT",
            "existing_source": "vless",
            "selected_source_or_draft": "draft-one",
            "trial_identity": "10.7.0.76",
            "trial_identity_count": 1,
            "identity_set_fingerprint": "a" * 64,
            "expected_assignment_delta": (
                "10.7.0.76:vless->NEW_DEDICATED_SOURCE"
            ),
            "expected_ordinary_assignment_delta": "NONE",
            "expected_ordinary_route_delta": "NONE",
            "capacity_reservation": 1,
            "max_concurrent_transactions": 1,
            "reservation_owner": "tools/v7-egress-set-state",
            "verification": "fresh Matrix baseline + current route",
            "rollback": "restore exact source binding and release reservation",
            "failure_mechanism": "existing controlled certification guard",
            "lease_and_expiry_required": True,
            "packet_required_before_effect": True,
            "restore_barrier_required_before_effect": True,
        }
        manifest["manifest_hash"] = sha256_json(manifest)
        request = operator_execution.build_controlled_source_topology_authority_request(
            {
                "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                "mission": (
                    "CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_"
                    "SLICE_FEASIBILITY_V1"
                ),
                "exact_action": (
                    "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE"
                ),
                "manifest": manifest,
                "authority_basis": {
                    "kind": "CT_M0F_STANDING_VALIDATION_POLICY",
                    "contract_id": "ctm0fsdpc_" + "b" * 24,
                    "contract_hash": "b" * 64,
                    "authority_request_id": "ctm0fsdpauth_r1_" + "c" * 24,
                    "authority_request_hash": "c" * 64,
                    "expires_at": "2026-09-05T08:00:00+00:00",
                },
                "current_campaign_request_id": "",
                "current_campaign_request_hash": "",
                "supersedes_source_binding_only": True,
                "tier48_capability_or_campaign_reapproval": False,
                "ordinary_customer_involvement": False,
                "self_expansion_allowed": False,
                "forbidden_effects": ["ordinary_user_movement"],
                "reentry_condition": "exact independent decision",
            },
            now=now,
        )
        self.assertTrue(
            operator_execution.validate_controlled_source_topology_authority_request(
                request, now=now + timedelta(seconds=1),
            )["ok"]
        )
        malformed = copy.deepcopy(request)
        malformed["manifest"]["validation_profile"] = "CAMPAIGN_FULL_PATH"
        malformed["manifest"]["manifest_hash"] = sha256_json({
            key: value for key, value in malformed["manifest"].items()
            if key != "manifest_hash"
        })
        malformed["request_hash"] = (
            operator_execution.controlled_source_topology_request_hash(malformed)
        )
        malformed["request_id"] = (
            f"cstopauth_r1_{malformed['request_hash'][:24]}"
        )
        validation = operator_execution.validate_controlled_source_topology_authority_request(
            malformed, now=now + timedelta(seconds=1),
        )
        self.assertFalse(validation["ok"])
        self.assertIn(
            "controlled_source_topology_ct_m0f_profile_invalid",
            validation["errors"],
        )

    def test_ct_m0f_invalid_sample_diagnostic_is_durable_and_counts_once(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            audit = root / "operator-execution-audit.jsonl"
            policy.write_text("{}\n", encoding="utf-8")
            request = operator_execution.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=operator_execution.sha256_file(policy),
                now=now,
            )
            operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            activated = operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            reservation = operator_execution.reserve_ct_m0f_standing_validation_sample(
                policy,
                implementation_fingerprint="f" * 64,
                validation_generation_id="ctm0fgen_invalid",
                packet_id="packet-invalid",
                operation_id="operation-invalid",
                lease_id="lease-invalid",
                user="10.7.0.18",
                source="vless",
                target="awg0",
                audit_store=audit,
                now=now + timedelta(seconds=3),
            )["reservation"]
            evidence = {
                "status": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID",
                "ok": False,
                "blockers": [
                    "ct_m0f_cutover_evidence_not_emitted_by_route_apply_consumer"
                ],
            }
            recorded = operator_execution.record_ct_m0f_standing_validation_forward_evidence(
                reservation_id=reservation["reservation_id"],
                sample_evidence=evidence,
                audit_store=audit,
                now=now + timedelta(seconds=4),
            )
            lineage = operator_execution.ct_m0f_standing_validation_sample_from_audit(
                reservation["reservation_id"], audit_store=audit,
            )
            terminal = operator_execution.record_ct_m0f_standing_validation_sample_terminal(
                reservation_id=reservation["reservation_id"],
                sample_valid=False,
                sample_evidence=lineage["forward_evidence"]["sample_evidence"],
                terminal_reason="route_apply_consumer_evidence_missing",
                audit_store=audit,
                now=now + timedelta(seconds=5),
            )
            budget = operator_execution.ct_m0f_standing_validation_budget_status(
                activated["contract"],
                "f" * 64,
                audit_records=operator_execution.read_audit_records(audit),
            )
            with self.assertRaisesRegex(
                PacketError,
                "ct_m0f_standing_invalid_evidence_blockers_required",
            ):
                operator_execution.record_ct_m0f_standing_validation_forward_evidence(
                    reservation_id="another-reservation",
                    sample_evidence={
                        "status": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID"
                    },
                    audit_store=audit,
                    now=now + timedelta(seconds=6),
                )

        self.assertEqual(recorded["status"], "RECORDED_INVALID_DIAGNOSTIC")
        self.assertEqual(
            lineage["forward_evidence"]["evidence_classification"],
            "INVALID_DIAGNOSTIC_EVIDENCE",
        )
        self.assertEqual(
            lineage["forward_evidence"]["sample_evidence"]["blockers"],
            ["ct_m0f_cutover_evidence_not_emitted_by_route_apply_consumer"],
        )
        self.assertEqual(terminal["status"], "RECORDED")
        self.assertEqual(budget["invalid_or_safety_stopped_attempts"], 1)
        self.assertEqual(budget["active_reservations"], 0)

    def test_ct_m0f_standing_request_and_contract_expiry_fail_closed(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        request = operator_execution.build_ct_m0f_standing_validation_authority_request(
            policy_generation_hash="a" * 64,
            now=now,
        )
        request_validation = operator_execution.validate_ct_m0f_standing_validation_authority_request(
            request,
            decision=operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
            now=now + timedelta(hours=25),
        )
        self.assertIn("ct_m0f_standing_request_expired", request_validation["errors"])

    def test_ct_m0f_standing_contract_survives_bounded_audit_rotation(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            audit = root / "operator-execution-audit.jsonl"
            policy.write_text("{}\n", encoding="utf-8")
            request = (
                operator_execution.build_ct_m0f_standing_validation_authority_request(
                    policy_generation_hash=operator_execution.sha256_file(policy),
                    now=now,
                )
            )
            operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            activated = operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            audit.rename(root / "operator-execution-audit.jsonl.1")
            audit.write_text("", encoding="utf-8")
            lineage = operator_execution.read_live_execution_lineage_records(audit)
            validation = operator_execution.validate_ct_m0f_standing_validation_policy(
                activated["contract"], audit_records=lineage,
                now=now + timedelta(seconds=3),
            )
            reservation = operator_execution.reserve_ct_m0f_standing_validation_sample(
                policy,
                implementation_fingerprint="f" * 64,
                validation_generation_id="ctm0fgen_rotation",
                packet_id="packet-rotation",
                operation_id="operation-rotation",
                lease_id="lease-rotation",
                user="certification-identity",
                source="vless",
                target="awg0",
                audit_store=audit,
                now=now + timedelta(seconds=4),
            )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertTrue(reservation["ok"], reservation.get("errors"))

    def test_ct_m0f_standing_decline_is_audited_without_policy_activation(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            audit = root / "operator-audit.jsonl"
            policy.write_text("{}\n", encoding="utf-8")
            request = operator_execution.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=operator_execution.sha256_file(policy),
                now=now,
            )
            operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            result = operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="DECLINE_STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY",
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            policy_root = json.loads(policy.read_text(encoding="utf-8"))
        self.assertEqual(
            result["status"],
            "STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY_DECLINED",
        )
        self.assertFalse(result["policy_write"])
        self.assertNotIn(
            operator_execution.CT_M0F_STANDING_VALIDATION_POLICY_KEY,
            policy_root,
        )

    def test_audit_replay_flags_searches_only_exact_canonical_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "operator-audit.jsonl"
            audit.write_text(
                "{not-json}\n"
                + json.dumps(
                    {"approval_id": "different", "payload": "approval-wanted"},
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n",
                encoding="utf-8",
            )
            operator_execution.append_record(
                audit,
                {
                    "record_type": "runtime_action_record_persisted",
                    "approval_id": "approval-wanted",
                    "engineering_authority_request_id": "authority-wanted",
                },
            )

            found = operator_execution.audit_replay_flags(
                audit, "approval-wanted", "authority-wanted",
            )
            absent = operator_execution.audit_replay_flags(
                audit, "approval-absent", "authority-absent",
            )

        self.assertEqual(
            found,
            {"approval_seen": True, "engineering_authority_seen": True},
        )
        self.assertEqual(
            absent,
            {"approval_seen": False, "engineering_authority_seen": False},
        )

    def test_ct_m0f_runtime_fingerprint_includes_health_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = {}
            for name in (
                "governed", "matrix", "autoswitch", "health", "routing",
            ):
                paths[name] = root / name
                paths[name].write_text(name, encoding="utf-8")

            first = operator_execution.ct_m0f_runtime_implementation_fingerprint(
                governed_cycle=paths["governed"],
                matrix_failure_consumer=paths["matrix"],
                autoswitch=paths["autoswitch"],
                health_runtime=paths["health"],
                routing_runtime=paths["routing"],
            )
            paths["health"].write_text("changed-health", encoding="utf-8")
            second = operator_execution.ct_m0f_runtime_implementation_fingerprint(
                governed_cycle=paths["governed"],
                matrix_failure_consumer=paths["matrix"],
                autoswitch=paths["autoswitch"],
                health_runtime=paths["health"],
                routing_runtime=paths["routing"],
            )

        self.assertNotEqual(first, second)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = {}
            for name in (
                "governed", "matrix", "autoswitch", "health", "routing",
            ):
                paths[name] = root / name
                paths[name].write_text(name, encoding="utf-8")
            before_routing_change = (
                operator_execution.ct_m0f_runtime_implementation_fingerprint(
                    governed_cycle=paths["governed"],
                    matrix_failure_consumer=paths["matrix"],
                    autoswitch=paths["autoswitch"],
                    health_runtime=paths["health"],
                    routing_runtime=paths["routing"],
                )
            )
            paths["routing"].write_text("changed-routing", encoding="utf-8")
            after_routing_change = (
                operator_execution.ct_m0f_runtime_implementation_fingerprint(
                    governed_cycle=paths["governed"],
                    matrix_failure_consumer=paths["matrix"],
                    autoswitch=paths["autoswitch"],
                    health_runtime=paths["health"],
                    routing_runtime=paths["routing"],
                )
            )
        self.assertNotEqual(before_routing_change, after_routing_change)

    def test_ct_m0f_runtime_fingerprint_includes_exact_payload_consumer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = {}
            for name in (
                "governed", "matrix", "autoswitch", "health", "routing",
                "v7-service-matrix-test", "v7-user-switch",
                "v7-client-speed-api",
            ):
                paths[name] = root / name
                paths[name].write_text(name, encoding="utf-8")

            before = operator_execution.ct_m0f_runtime_implementation_fingerprint(
                governed_cycle=paths["governed"],
                matrix_failure_consumer=paths["matrix"],
                autoswitch=paths["autoswitch"],
                health_runtime=paths["health"],
                routing_runtime=paths["routing"],
            )
            paths["v7-client-speed-api"].write_text(
                "changed-payload-consumer", encoding="utf-8",
            )
            after = operator_execution.ct_m0f_runtime_implementation_fingerprint(
                governed_cycle=paths["governed"],
                matrix_failure_consumer=paths["matrix"],
                autoswitch=paths["autoswitch"],
                health_runtime=paths["health"],
                routing_runtime=paths["routing"],
            )

        self.assertNotEqual(before, after)


if __name__ == "__main__":
    unittest.main()
