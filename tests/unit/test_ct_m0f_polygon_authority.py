"""Authority version/scope regressions; unit fixtures are not E2E evidence."""

import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from admin_core import operator_execution as owner
from admin_core import operator_execution_isolation as isolation


class PolygonStandingAuthorityTest(unittest.TestCase):
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
        scope = {"max_cohort_members": 5, "max_concurrent_transactions": 1}
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
