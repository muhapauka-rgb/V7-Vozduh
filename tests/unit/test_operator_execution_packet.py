import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from admin_core.operator_execution import (
    CANONICAL_CLEARANCE_OWNER,
    EMPTY_SELECTED_MOVES_HASH,
    PacketError,
    RUNTIME_ACTION_CREATE_CLEARANCE,
    RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE,
    approved_packet_binding_status,
    cancel_execution_lease,
    containment_forward_fix_classification,
    create_execution_lease_from_packet,
    create_execution_lease_from_preview,
    execute_packet,
    execution_lease_state,
    extract_packet_preview,
    finish_execution_lease,
    packet_from_preview,
    packet_identity,
    packet_from_plan,
    preview_packet_identity,
    resolve_under_repo,
    rollback_operational_compensation_contract,
    runtime_recheck,
    sha256_bytes,
    sha256_file,
    sha256_json,
    write_execution_lease,
)


def write_json(path, data):
    Path(path).write_text(json.dumps(data, sort_keys=True), encoding="utf-8")


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
            packet = packet_from_preview(
                self.preview_packet(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            lease = create_execution_lease_from_packet(packet, source_preview=self.preview_packet())
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


if __name__ == "__main__":
    unittest.main()
