import importlib.machinery
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-autoswitch-proposal-cap"
EXEC_TARGET = "amneziawg-exec-20260528-10-8-1-14"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_autoswitch_proposal_cap", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class V7AutoswitchProposalCapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def shadow_fixture(self):
        return {
            "schema_version": 1,
            "apply_requested": False,
            "decisions": [
                {
                    "user_ip": "10.7.0.11",
                    "action": "switch",
                    "move_type": "failover",
                    "current_egress": EXEC_TARGET,
                    "recommended_egress": "awg3",
                    "current_score": 0,
                    "recommended_score": 900,
                },
                {
                    "user_ip": "10.7.0.16",
                    "action": "switch",
                    "move_type": "failover",
                    "current_egress": "vless",
                    "recommended_egress": "awg3",
                    "current_score": 10,
                    "recommended_score": 800,
                },
                {
                    "user_ip": "10.7.0.17",
                    "action": "switch",
                    "move_type": "failover",
                    "current_egress": "vless",
                    "recommended_egress": "awg3",
                    "current_score": 20,
                    "recommended_score": 700,
                },
            ],
        }

    def test_budget_and_current_egress_hold_reduce_proposal(self):
        result = self.tool.build_proposal(
            self.shadow_fixture(),
            budget=1,
            hold_current_egress={EXEC_TARGET},
            hold_user=set(),
            safety={"status": "ok"},
        )

        self.assertTrue(result["ready_for_operator_review"])
        self.assertEqual(result["raw_candidate_moves"], 3)
        self.assertEqual(result["held_candidates"], 1)
        self.assertEqual(result["eligible_candidates"], 2)
        self.assertEqual(result["proposal_count"], 1)
        self.assertEqual(result["proposal_moves"][0]["user_ip"], "10.7.0.16")
        self.assertFalse(result["autoswitch_apply_run"])
        self.assertFalse(result["users_moved"])

    def test_safety_critical_fails_closed(self):
        result = self.tool.build_proposal(
            self.shadow_fixture(),
            budget=1,
            hold_current_egress=set(),
            hold_user=set(),
            safety={"status": "critical"},
        )

        self.assertFalse(result["ready_for_operator_review"])
        self.assertEqual(result["proposal_count"], 0)
        self.assertIn("safety_status_not_ok_or_warn", result["fail_closed_reasons"])

    def test_invalid_budget_fails_closed(self):
        result = self.tool.build_proposal(
            self.shadow_fixture(),
            budget=3,
            hold_current_egress=set(),
            hold_user=set(),
            safety={"status": "ok"},
        )

        self.assertFalse(result["ready_for_operator_review"])
        self.assertEqual(result["proposal_count"], 0)
        self.assertIn("invalid_budget_allowed_values_1_2_5_10", result["fail_closed_reasons"])

    def test_apply_shadow_plan_fails_closed(self):
        shadow = self.shadow_fixture()
        shadow["apply_requested"] = True
        result = self.tool.build_proposal(
            shadow,
            budget=1,
            hold_current_egress=set(),
            hold_user=set(),
            safety={"status": "ok"},
        )

        self.assertFalse(result["ready_for_operator_review"])
        self.assertEqual(result["proposal_count"], 0)
        self.assertIn("shadow_plan_has_apply_requested_true", result["fail_closed_reasons"])


if __name__ == "__main__":
    unittest.main()
