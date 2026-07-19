from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "docs/reports/engineering/evidence/2026-07-19_232830_controlled_rollback_authority_request.json"


class L7L8R1AuthorityRequestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))

    def test_contract_hash_and_request_identity_are_stable(self):
        canonical = dict(self.packet)
        expected = canonical.pop("contract_hash")
        request_id = canonical.pop("request_id")
        actual = hashlib.sha256(json.dumps(
            canonical,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        self.assertEqual(actual, expected)
        self.assertEqual(request_id, f"engauth_r1_{actual[:24]}")

    def test_decision_and_one_use_contract_are_exact(self):
        self.assertEqual(self.packet["decision_set"], [
            "APPROVE_ONCE_AS_SCOPED",
            "APPROVE_WITH_NARROWER_SCOPE",
            "DENY",
            "EXPIRED",
        ])
        self.assertEqual(self.packet["one_use_law"]["approval_use_limit"], 1)
        self.assertFalse(self.packet["one_use_law"]["implicit_renewal"])
        self.assertFalse(self.packet["one_use_law"]["retry_under_same_approval"])
        self.assertLess(
            datetime.fromisoformat(self.packet["created_at"]),
            datetime.fromisoformat(self.packet["expires_at"]),
        )

    def test_scope_is_one_certification_user_and_one_serial_transaction(self):
        self.assertTrue(self.packet["subject"]["certification_user"])
        self.assertFalse(self.packet["subject"]["ordinary_customer"])
        self.assertEqual(self.packet["subject"]["user_ip"], "10.7.0.16")
        self.assertEqual(self.packet["scope"]["max_users"], 1)
        self.assertEqual(self.packet["scope"]["max_concurrent_transactions"], 1)
        self.assertEqual(self.packet["scope"]["max_material_outcomes"], 1)
        self.assertEqual(self.packet["scope"]["source_egress"], "wireguard-1779454504-c43409")
        self.assertEqual(self.packet["scope"]["target_egress"], "vless")

    def test_real_verifier_owns_the_rollback_decision(self):
        condition = self.packet["controlled_condition"]
        self.assertEqual(
            condition["registered_rollback_trigger"],
            "required_service_verify_timeout after successful bounded forward apply and exact selected-user route acknowledgement",
        )
        self.assertEqual(condition["expected_terminal"], "ROLLBACK_SUCCESS")
        self.assertFalse(condition["direct_rollback_invocation_for_evidence"])
        self.assertFalse(condition["rollback_failure_injection"])
        self.assertIn("rollback-failure injection", self.packet["excluded_effects"])
        self.assertIn("ordinary-customer experimentation", self.packet["excluded_effects"])


if __name__ == "__main__":
    unittest.main()
