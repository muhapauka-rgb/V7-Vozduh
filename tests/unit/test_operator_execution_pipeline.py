import unittest
from pathlib import Path

from admin_core import operator_execution_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


class OperatorExecutionPipelineTest(unittest.TestCase):
    def recommendation_row(self):
        return {
            "user": "10.7.0.3",
            "current_channel": "awg0",
            "recommended_channel": "awg3",
            "confidence": 0.91,
            "trust": 88.0,
            "prediction": {"available": True, "confidence": 0.82},
            "risk": 3.2,
            "recommendation_hash": "rec-hash",
            "source_hash": "source-hash",
            "reasons": ["best available channel has higher advisory suitability"],
        }

    def test_recommendation_execution_contract_has_required_fields(self):
        contract = pipeline.recommendation_execution_contract(self.recommendation_row())

        for field in pipeline.REQUIRED_RECOMMENDATION_FIELDS:
            self.assertIn(field, contract)
        self.assertTrue(contract["execution_candidate"])
        self.assertFalse(contract["execution_allowed_now"])
        self.assertFalse(contract["runtime_mutation_performed"])
        self.assertEqual(contract["rollback_plan"]["rollback_target"], "awg0")
        self.assertEqual(contract["next_required_state"], "APPROVAL_PACKET_REQUIRED")

    def test_execution_action_matrix_satisfies_rule_16(self):
        required = {
            "condition",
            "decision",
            "action",
            "executor",
            "trigger",
            "written_evidence",
            "blocked_actions",
            "next_state",
        }
        matrix = pipeline.execution_action_matrix()

        self.assertEqual({row["state"] for row in matrix}, set(pipeline.EXECUTION_STATES))
        for row in matrix:
            with self.subTest(state=row["state"]):
                self.assertTrue(required.issubset(row))
                for key in required:
                    self.assertTrue(row[key], f"{row['state']} missing {key}")

    def test_pipeline_certification_is_single_path_and_non_mutating(self):
        cert = pipeline.pipeline_certification()
        verdicts = cert["final_verdicts"]

        self.assertTrue(verdicts["single_execution_path_certified"])
        self.assertTrue(verdicts["execution_action_matrix_complete"])
        self.assertFalse(verdicts["new_truth_sources_created"])
        self.assertFalse(verdicts["duplicate_systems_created"])
        self.assertFalse(verdicts["runtime_mutation_performed"])
        self.assertFalse(verdicts["users_moved"])
        self.assertFalse(verdicts["autoswitch_apply_run"])
        self.assertFalse(cert["single_execution_path"]["direct_user_switch_allowed"])
        self.assertEqual(cert["single_execution_path"]["runtime_apply"], pipeline.CANONICAL_RUNTIME_EXECUTOR)

    def test_direct_user_switch_blocker_is_fail_closed(self):
        blocked = pipeline.direct_user_switch_blocker("10.7.0.3", "awg3", "operator-a")

        self.assertEqual(blocked["status"], "blocked")
        self.assertEqual(blocked["error"], "governed_execution_pipeline_required")
        self.assertFalse(blocked["execution_allowed_now"])
        self.assertFalse(blocked["runtime_mutation_performed"])
        self.assertFalse(blocked["users_moved"])
        self.assertFalse(blocked["autoswitch_apply_run"])
        self.assertIn("v7-users-autoswitch --apply --verify", blocked["required_path"])

    def test_module_does_not_import_or_call_runtime_execution(self):
        source = Path(pipeline.__file__).read_text(encoding="utf-8")

        self.assertNotIn("subprocess", source)
        self.assertNotIn("run_action", source)
        self.assertNotIn("os.system", source)

    def test_admin_user_switch_endpoint_no_longer_calls_direct_switch(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        marker = 'elif path == "/api/actions/user-switch":'
        start = source.index(marker)
        end = source.index('elif path == "/api/actions/users-rebalance-dry-run":', start)
        handler = source[start:end]

        self.assertIn("governed_user_switch_blocker_response", handler)
        self.assertNotIn("run_action([\"v7-user-switch\"", handler)
        self.assertNotIn("proxy_runtime_switch_user_egress", handler)


if __name__ == "__main__":
    unittest.main()

