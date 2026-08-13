import json
from pathlib import Path
import tempfile
import unittest

from admin_core import operator_execution


class CurrentActionClassContractCancellationTests(unittest.TestCase):
    def test_exact_unconsumed_contract_is_cancelled_without_runtime_effect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            audit_path = root / "audit.jsonl"
            contract = {
                "contract_id": "acc_old",
                "contract_hash": "hash_old",
                "one_use_consumption": {
                    "state": "ISSUED",
                    "consumed_uses": 0,
                    "allowed_uses": 1,
                    "retry_allowed": False,
                },
            }
            policy_path.write_text(json.dumps({"authority_budget": {"current_action_class_contract": contract}}))
            result = operator_execution.cancel_unconsumed_current_action_class_contract_to_policy(
                policy_path,
                expected_contract_id="acc_old",
                expected_contract_hash="hash_old",
                actor_id="operator-test",
                reason="misbound_generation",
                audit_store=audit_path,
            )
            self.assertEqual(result["status"], "CANCELLED_UNCONSUMED")
            self.assertEqual(result["contract"]["one_use_consumption"]["state"], "CANCELLED")
            self.assertFalse(result["runtime_apply"])
            self.assertEqual(result["users_moved"], 0)
            self.assertIn("current_action_class_contract_cancelled", audit_path.read_text())

    def test_consumed_contract_cannot_be_cancelled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy_path = root / "policy.json"
            policy_path.write_text(json.dumps({"authority_budget": {"current_action_class_contract": {
                "contract_id": "acc_old", "contract_hash": "hash_old",
                "one_use_consumption": {"state": "CONSUMED", "consumed_uses": 1},
            }}}))
            with self.assertRaisesRegex(operator_execution.PacketError, "requires_unconsumed"):
                operator_execution.cancel_unconsumed_current_action_class_contract_to_policy(
                    policy_path,
                    expected_contract_id="acc_old",
                    expected_contract_hash="hash_old",
                    actor_id="operator-test",
                    reason="must_fail",
                    audit_store=root / "audit.jsonl",
                )


if __name__ == "__main__":
    unittest.main()
