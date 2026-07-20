import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

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
        normalized_scope = {
            "allowed_action_classes": ["single-user governed candidate failover"],
            "max_users_per_action": 1,
            "max_concurrent_transactions": 1,
            "required_anti_flap": "PASS",
            "required_freshness": ["capacity", "quality", "route", "service"],
            "required_verification": ["immediate_post_action_user_verification"],
            "required_rollback": "class_level_rollback_or_certified_no_rollback_path",
            "final_safe_mode": "OPEN",
            "operator_packet_approval_required": False,
        }
        return {
            "authority_basis": "DELEGATED_AUTONOMY_POLICY",
            "policy_id": "dap_default_tier1_readonly",
            "policy_scope_hash": sha256_json(normalized_scope),
            "normalized_scope": normalized_scope,
            "policy_state": "APPROVED",
            "current_mode": "DELEGATED_AUTONOMY",
            "action_class": "single-user governed candidate failover",
            "max_users_per_transaction": 1,
            "max_concurrent_transactions": 1,
            "candidate_identity": "FRESH_ONLY",
            "packet_reuse": "FORBIDDEN",
            "self_expansion_allowed": False,
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


if __name__ == "__main__":
    unittest.main()
