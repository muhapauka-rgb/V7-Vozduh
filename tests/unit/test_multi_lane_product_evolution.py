from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_multi_lane_product", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class MultiLaneProductEvolutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        cls.cps = cls.lib._replace_section_field(
            cls.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "ACTION_CLASS_ENGINEERING_FRONTIER",
            "`NONE`",
        )

    def test_l8_wait_selects_independent_engineering_not_production(self):
        result = self.lib.multi_lane_product_frontier_reconciliation(self.cps, root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])
        self.assertEqual(result["selection"], "SELECTED_CHANNEL_HARD_FAILURE_FAILOVER_ENGINEERING")
        self.assertEqual(result["candidate_action_class"], "channel hard-fail failover")
        self.assertEqual(
            result["product_engineering_frontier"],
            ["PHASE6_PRODUCT_ENGINEERING:POLYGON-ACTION-CLASS-CHANNEL_HARD_FAILURE_FAILOVER-ENGINEERING-G1"],
        )
        self.assertEqual(result["authority_status"], "NOT_GRANTED_ENGINEERING_ONLY; RUNTIME_APPLY_AND_USER_MOVEMENT_FORBIDDEN")

    def test_l8_evidence_does_not_cross_credit(self):
        result = self.lib.multi_lane_product_frontier_reconciliation(self.cps, root=ROOT)
        separation = result["evidence_separation"]
        self.assertFalse(separation["current_class_l8_credit_transfers_to_candidate"])
        self.assertFalse(separation["engineering_scenario_grants_l7_or_l8_credit"])
        self.assertFalse(separation["candidate_production_execution_admitted"])
        self.assertFalse(result["l8_observation_window"]["natural_event_creation_allowed"])

    def test_consumed_marker_suppresses_duplicate_dispatch(self):
        marked = self.lib._replace_section_field(
            self.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "ACTION_CLASS_ENGINEERING_FRONTIER",
            "`POLYGON-ACTION-CLASS-CHANNEL_HARD_FAILURE_FAILOVER-ENGINEERING-G1:CONSUMED`",
        ) if "ACTION_CLASS_ENGINEERING_FRONTIER" in self.cps else self.cps.replace(
            "| `CURRENT_ACTION_CLASS_STATE` | `GOVERNED_ONLY` |",
            "| `CURRENT_ACTION_CLASS_STATE` | `GOVERNED_ONLY` |\n| `ACTION_CLASS_ENGINEERING_FRONTIER` | `POLYGON-ACTION-CLASS-CHANNEL_HARD_FAILURE_FAILOVER-ENGINEERING-G1:CONSUMED` |",
            1,
        )
        result = self.lib.multi_lane_product_frontier_reconciliation(marked, root=ROOT)
        self.assertTrue(result["already_consumed"])
        self.assertEqual(result["product_engineering_frontier"], [])

    def test_engineering_execution_uses_existing_consumer_and_remains_isolated(self):
        result = self.lib.execute_multi_lane_product_action_class_engineering(self.cps, root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])
        self.assertEqual(result["real_consumer"], "OMP_PROGRAM_EXECUTION_RECONCILIATION")
        self.assertEqual(result["scenario"]["scenario_id"], "SINGLE_CHANNEL_FAILURE")
        self.assertFalse(any(result["forbidden_effects"].values()))
        self.assertEqual(result["production_maturity_impact"], "NO_CHANGE")

    def test_production_entrypoint_uses_materialized_owner_contract(self):
        result = self.lib.certify_multi_lane_product_evolution_production_entrypoint(root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])
        self.assertEqual(result["caller_class"], "PRODUCTION_NON_TEST_READ_ONLY_CALLER")
        self.assertEqual(result["real_consumer"], "OMP_PROGRAM_EXECUTION_RECONCILIATION")
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
