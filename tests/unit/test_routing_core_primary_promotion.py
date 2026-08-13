import json
from pathlib import Path
import tempfile
import unittest

from admin_core import operator_execution as owner


class RoutingCorePrimaryPromotionTests(unittest.TestCase):
    def test_request_and_issue_are_effect_separated_and_hash_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime = root / "runtime.json"
            sync = root / "sync"
            core = root / "core.py"
            policy = root / "policy.json"
            request_path = root / "request.json"
            audit = root / "audit.jsonl"
            runtime.write_text(json.dumps({"commit": "abc", "deploy_id": "deploy-1"}))
            sync.write_text("sync")
            core.write_text("core")
            policy.write_text("{}")
            request = owner.build_routing_core_primary_promotion_request(
                runtime_fingerprint_path=runtime, routing_sync_path=sync,
                routing_core_path=core,
            )
            self.assertEqual(request["status"], "AWAITING_INDEPENDENT_AUTHORITY_DECISION")
            request_path.write_text(json.dumps(request))
            result = owner.issue_routing_core_primary_promotion_to_policy(
                policy, request_path,
                decision="APPROVE_CORE_PRIMARY_WITH_FALLBACK",
                actor_id="operator-test", audit_store=audit,
            )
            self.assertEqual(result["status"], "ROUTING_CORE_PRIMARY_PROMOTION_ISSUED")
            self.assertFalse(result["runtime_apply"])
            contract = json.loads(policy.read_text())["routing_core_primary_promotion"]
            self.assertEqual(owner.routing_core_primary_promotion_hash(contract), contract["contract_hash"])
            self.assertTrue(contract["legacy_fallback_required"])


if __name__ == "__main__":
    unittest.main()
