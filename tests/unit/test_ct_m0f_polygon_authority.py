"""Authority version/scope regressions; unit fixtures are not E2E evidence."""

import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock

from admin_core import operator_execution as owner
from admin_core import operator_execution_isolation as isolation


class PolygonStandingAuthorityTest(unittest.TestCase):
    def test_lab_operation_control_never_uses_global_fallback_and_rechecks_authority(self):
        scope = {"members": [f"10.7.254.{i}" for i in range(1, 6)]}
        contract = {"schema_version": owner.CT_M0F_POLYGON_CONTRACT_SCHEMA,
                    "contract_id": "unit-contract", "contract_hash": "a" * 64,
                    "envelope": {"isolated_polygon_scope": scope}}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            owner, "validate_ct_m0f_standing_validation_policy", return_value={"ok": True},
        ) as validation:
            policy, audit, control = [Path(tmp) / name for name in ("policy.json", "audit.jsonl", "control.json")]
            policy.write_text(json.dumps({owner.CT_M0F_STANDING_VALIDATION_POLICY_KEY: contract}))
            binding = dict(policy_file=str(policy), audit_store=str(audit),
                           contract_id=contract["contract_id"], contract_hash=contract["contract_hash"])
            args = dict(actor="unit", reason="unit", operation_id="unit-operation", selected_move_hash="b" * 64,
                        action_class="EMERGENCY_FAILOVER", source_bundle_hash="c" * 64,
                        snapshot_bundle_hash="d" * 64, max_users=5, isolated_polygon_authority=binding)
            state = owner.build_autonomous_execution_control_state(False, **args)
            self.assertEqual(state["scope"], "operation")
            owner.write_json_atomic(control, state)
            check = dict(operation_id="unit-operation", selected_move_hash="b" * 64,
                         action_class="EMERGENCY_FAILOVER", source_bundle_hash="c" * 64,
                         snapshot_bundle_hash="d" * 64, max_users=5)
            self.assertTrue(owner.autonomous_execution_control_decision(control, **check)["allowed"])
            self.assertFalse(owner.autonomous_execution_control_decision(control, **{**check, "operation_id": "wrong"})["allowed"])
            self.assertFalse(owner.autonomous_execution_control_decision(control, **{**check, "max_users": 4})["allowed"])
            for changes in ({"operation_id": ""}, {"max_users": 4}):
                with self.assertRaises(owner.PacketError):
                    owner.build_autonomous_execution_control_state(False, **{**args, **changes})
            validation.return_value = {"ok": False, "errors": ["expired_or_revoked"]}
            self.assertFalse(owner.autonomous_execution_control_decision(control, **check)["allowed"])
            validation.return_value = {"ok": True}
            policy.write_text("{}")
            self.assertFalse(owner.autonomous_execution_control_decision(control, **check)["allowed"])

    def test_lab_reservation_protects_exact_whole_cohort_and_binds_target_after_fault(self):
        scope = {"members": ["10.7.254.1", "10.7.254.2"], "source_egress": "source",
                 "allowed_target_egresses": ["target"]}
        contract = {"schema_version": owner.CT_M0F_POLYGON_CONTRACT_SCHEMA,
                    "contract_id": "unit-contract", "contract_hash": "a" * 64,
                    "envelope": {"isolated_polygon_scope": scope}}
        # Authority signature/environment has separate tests; here exercise
        # actual append-only reserve/bind/guard/release with a unit contract.
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            owner, "validate_ct_m0f_standing_validation_policy", return_value={"ok": True},
        ):
            audit = Path(tmp) / "audit.jsonl"
            args = dict(contract=contract, implementation_fingerprint="f" * 64,
                        user=scope["members"][0], source="source", target="",
                        sample_binding_fingerprint="b" * 64,
                        source_reservation_id="polygon_" + owner.sha256_json(scope),
                        source_fingerprint="c" * 64,
                        target_binding_mode="POST_T0_OWNER_SELECTED", audit_store=audit)
            self.assertFalse(owner.reserve_ct_m0f_standing_validation_transaction(**{**args, "target": "target"})["ok"])
            self.assertFalse(owner.reserve_ct_m0f_standing_validation_transaction(**{**args, "user": "10.7.254.9"})["ok"])
            reserved = owner.reserve_ct_m0f_standing_validation_transaction(**args)
            self.assertTrue(reserved["ok"])
            self.assertEqual(reserved["reservation"]["cohort_members"], scope["members"])
            self.assertEqual(owner.reserve_ct_m0f_standing_validation_transaction(**args)["status"], "ALREADY_RESERVED_EXACT")
            reservation_id = reserved["reservation"]["transaction_reservation_id"]
            for user in scope["members"]:
                self.assertFalse(owner.ct_m0f_standing_validation_transaction_guard(
                    user=user, source="source", target="target", audit_store=audit)["ok"])
            binding = dict(transaction_reservation_id=reservation_id, packet_id="unit-packet",
                           operation_id="unit-operation", lease_id="unit-lease",
                           matrix_sample_binding_fingerprint="d" * 64, target="target", audit_store=audit)
            self.assertFalse(owner.bind_ct_m0f_standing_validation_transaction(**{**binding, "target": "outside"})["ok"])
            self.assertTrue(owner.bind_ct_m0f_standing_validation_transaction(**binding)["ok"])
            self.assertEqual(owner.bind_ct_m0f_standing_validation_transaction(**binding)["status"], "ALREADY_BOUND_EXACT")
            for user in scope["members"]:
                self.assertTrue(owner.ct_m0f_standing_validation_transaction_guard(
                    user=user, source="source", target="target", operation_id="unit-operation", audit_store=audit)["ok"])
                self.assertFalse(owner.ct_m0f_standing_validation_transaction_guard(
                    user=user, source="source", target="target", operation_id="wrong", audit_store=audit)["ok"])
            owner.release_ct_m0f_standing_validation_transaction(
                transaction_reservation_id=reservation_id, reason="unit-terminal", audit_store=audit)
            self.assertEqual(owner.active_ct_m0f_standing_validation_transactions(owner.read_audit_records(audit)), [])

    def test_cold_payload_contract_rejects_stale_partial_or_fabricated_window_coverage(self):
        scope = {"members": ["10.7.254.1", "10.7.254.2"], "source_egress": "source",
                 "allowed_target_egresses": ["target"],
                 "environment": {"network_namespace": "unit-only", "memory_max": 1000}}
        wave = {"started_ns": 1, "completed_ns": 10000001,
                "memory_events_before": "oom 0", "memory_events_after": "oom 0",
                "memory_before_bytes": 100, "memory_after_bytes": 100,
                "samples": [{"started_ns": 1, "completed_ns": 10000001,
                             "ok": True, "bytes": 1048576}] * 2}
        observation = {"schema": "v7.isolated-polygon-cold-capacity-observation.v1",
                       "owner": "tools/v7-client-speed-api", "observed_at": datetime.now(timezone.utc).isoformat(),
                       "completed_monotonic_ns": time.monotonic_ns(),
                       "network_namespace": "unit-only", "cohort_members": scope["members"],
                       "concurrent_streams": 2, "payload_bytes_per_stream": 1048576,
                       "rounds_per_channel": 3, "long_window_coverage": {"5m": "NOT_OBSERVED", "1h": "NOT_OBSERVED"},
                       "observations": {name: {"rounds": [wave] * 3} for name in ["source", "target"]}}
        self.assertEqual(isolation.cold_capacity_observation_errors(observation, scope), [])
        for changes in ({"concurrent_streams": 1}, {"completed_monotonic_ns": 0},
                        {"long_window_coverage": {"5m": "PASS", "1h": "PASS"}}):
            self.assertTrue(isolation.cold_capacity_observation_errors({**observation, **changes}, scope))
        bad = copy.deepcopy(observation)
        bad["observations"]["target"]["rounds"][0]["samples"][0]["ok"] = False
        self.assertIn("polygon_cold_payload_or_throughput_failed", isolation.cold_capacity_observation_errors(bad, scope))

    def test_source_route_loss_is_not_an_external_route_bypass(self):
        self.assertFalse(isolation.external_default_route_present([]))
        self.assertFalse(isolation.external_default_route_present([{"dst": "default", "dev": "pgtarget"}]))
        self.assertTrue(isolation.external_default_route_present([{"dst": "default", "dev": "eth0"}]))
        self.assertTrue(isolation.external_default_route_present([{"dst": "default", "dev": "pgsource", "gateway": "172.20.0.1"}]))

    def test_original_request_stays_one_member_and_rejects_new_approval(self):
        request = owner.build_ct_m0f_standing_validation_authority_request(policy_generation_hash="a" * 64)
        self.assertTrue(owner.validate_ct_m0f_standing_validation_authority_request(request)["ok"])
        self.assertEqual(request["envelope"]["execution_bounds"]["max_users_per_transaction"], 1)
        self.assertNotIn("isolated_polygon_scope", request["envelope"])
        self.assertFalse(owner.validate_ct_m0f_standing_validation_authority_request(
            request, decision=owner.CT_M0F_POLYGON_APPROVAL,
        )["ok"])

    def test_missing_actual_environment_cannot_admit_lab_scope(self):
        with mock.patch.object(isolation, "kernel_environment", side_effect=ValueError("container_required")):
            with self.assertRaises(owner.PacketError):
                owner.build_ct_m0f_standing_validation_authority_request(
                    policy_generation_hash="a" * 64,
                    isolated_polygon_scope={"schema": isolation.SCHEMA, "effect_scope": "ISOLATED_POLYGON"},
                )

    def test_fresh_lab_decision_cannot_reuse_v1_approval_and_is_short_lived(self):
        # Pure Authority unit fixture. Actual environment acceptance is tested
        # separately through the disposable Docker owner, never this mock.
        scope = {"max_cohort_members": 5, "max_concurrent_transactions": 1, "cold_capacity_observation_hash": "a" * 64}
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(isolation, "validate_scope", return_value=[]):
            policy = Path(tmp) / "policy.json"
            policy.write_text("{}\n")
            audit = Path(tmp) / "audit.jsonl"
            request = owner.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=owner.sha256_file(policy), now=now, isolated_polygon_scope=scope,
            )
            owner.register_ct_m0f_standing_validation_authority_request(request, audit_store=audit, now=now)
            args = dict(request_id=request["request_id"], request_hash=request["request_hash"],
                        actor_id="unit-test-not-production", audit_store=audit, now=now)
            with self.assertRaises(owner.PacketError):
                owner.issue_ct_m0f_standing_validation_policy_from_audit(
                    policy, decision=owner.CT_M0F_STANDING_VALIDATION_APPROVAL, **args,
                )
            self.assertEqual(json.loads(policy.read_text()), {})
            result = owner.issue_ct_m0f_standing_validation_policy_from_audit(
                policy, decision=owner.CT_M0F_POLYGON_APPROVAL, **args,
            )
            contract = result["contract"]
            self.assertEqual(contract["schema_version"], owner.CT_M0F_POLYGON_CONTRACT_SCHEMA)
            self.assertEqual(contract["envelope"]["execution_bounds"]["max_users_per_transaction"], 5)
            self.assertEqual(contract["envelope"]["execution_bounds"]["max_concurrent_transactions"], 1)
            self.assertTrue(owner.validate_ct_m0f_standing_validation_policy(contract, now=now)["ok"])
            self.assertFalse(owner.validate_ct_m0f_standing_validation_policy(
                contract, now=now + timedelta(seconds=121),
            )["ok"])
            changed = copy.deepcopy(contract)
            changed["schema_version"] = owner.CT_M0F_STANDING_VALIDATION_CONTRACT_SCHEMA
            changed["contract_hash"] = owner.ct_m0f_standing_validation_contract_hash(changed)
            changed["contract_id"] = "ctm0fsdpc_" + changed["contract_hash"][:24]
            self.assertFalse(owner.validate_ct_m0f_standing_validation_policy(changed, now=now)["ok"])

    def test_replayed_environment_binding_fails_closed(self):
        scope = {"schema": isolation.SCHEMA, "environment": {"network_namespace": "old"}}
        with mock.patch.object(isolation, "kernel_environment", return_value={"network_namespace": "different", "memory_max": 512}):
            self.assertIn("polygon_current_environment_binding_changed", isolation.validate_scope(scope))


if __name__ == "__main__":
    unittest.main()
