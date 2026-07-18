from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_permanent_polygon_test", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PermanentPolygonOmpIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        cls.supply = cls.lib.permanent_polygon_obligation_supply(cls.cps, root=ROOT)
        cls.integration_result = cls.lib.execute_permanent_polygon_omp_integration(root=ROOT)

    def test_01_permanent_contract_reuses_existing_owners(self):
        contract = self.lib.permanent_polygon_applicability_contract()
        self.assertEqual(contract["final_verdict"], "PASS")
        self.assertFalse(contract["new_owner"])
        self.assertFalse(contract["new_runtime"])
        self.assertFalse(contract["new_scheduler"])
        self.assertEqual(contract["live_state_owner"], "CPS")

    def test_02_all_permanent_source_categories_are_registered(self):
        self.assertEqual(
            set(self.supply["permanent_source_categories"]),
            set(self.lib.PERMANENT_POLYGON_SOURCE_CATEGORIES),
        )

    def test_03_u02_u22_are_first_seed_not_scope_boundary(self):
        self.assertEqual(self.supply["current_seed_role"], "FIRST_GENERATION_NOT_PERMANENT_SCOPE")
        self.assertEqual(len(self.supply["current_seed_capability_ids"]), 21)
        self.assertEqual(self.supply["current_seed_capability_ids"][0], "CAP-U02")
        self.assertEqual(self.supply["current_seed_capability_ids"][-1], "CAP-U22")

    def test_04_first_obligation_is_criterion_scoped_not_capability_completion(self):
        obligation = self.supply["next_obligation"]
        self.assertEqual(obligation["capability_id"], "CAP-U03")
        self.assertEqual(obligation["minimum_sufficient_fidelity"], "L2")
        self.assertFalse(obligation["whole_capability_completion_granted"])
        self.assertEqual(obligation["criterion_dependency_scope"], "INDEPENDENT_ENGINEERING_CRITERION")

    def test_05_first_obligation_consumes_real_v7_l2_path(self):
        first = self.integration_result["first_consumption"]
        self.assertEqual(first["final_verdict"], "PASS", first.get("errors"))
        self.assertTrue(first["criterion_consumed"])
        self.assertEqual(first["criterion_coverage_state"], "COVERED_ENGINEERING_L2")
        self.assertTrue(first["checks"]["real_planner_packet_lease_consumed"])
        self.assertTrue(first["checks"]["execute_stay_rollback_stop_safe"])

    def test_06_l7_l8_and_whole_capability_remain_open(self):
        first = self.integration_result["first_consumption"]
        self.assertFalse(first["whole_capability_complete"])
        self.assertEqual(first["remaining_l7_criterion"], "CONTROLLED_PRODUCTION_FIELD_VALIDITY")
        self.assertEqual(first["remaining_l8_criterion"], "NATURAL_PRODUCTION_REPRESENTATIVENESS")

    def test_07_next_obligation_is_materialized(self):
        self.assertEqual(
            self.integration_result["next_obligation_id"],
            "POLYGON-CAP-U05-ROLLBACK_CONTAINMENT_ENGINEERING_MATRIX-G1",
        )
        self.assertTrue(self.integration_result["next_mission_formed"])
        self.assertTrue(self.integration_result["omp_continuation_required"])

    def test_08_duplicate_is_suppressed_without_reexecution(self):
        duplicate = self.integration_result["duplicate_probe"]
        self.assertTrue(duplicate["duplicate_result"])
        self.assertEqual(duplicate["behavior_change"], "DUPLICATE_RESULT_SUPPRESSED")
        self.assertEqual(duplicate["execution"]["state"], "NOT_REEXECUTED_DUPLICATE_IDENTITY")

    def test_09_automation_completion_is_consumed(self):
        self.assertEqual(self.integration_result["completion_gate"]["completion_verdict"], "COMPLETE_CONSUMED")
        self.assertEqual(
            self.integration_result["mission_terminal"],
            "PERMANENT_POLYGON_OMP_CONSUMER_ACTIVE_AND_FIRST_CAPABILITY_OBLIGATION_CONSUMED",
        )

    def test_10_forbidden_effects_are_absent(self):
        first = self.integration_result["first_consumption"]
        self.assertFalse(any(first["forbidden_effects"].values()))
        self.assertEqual(first["runtime_impact"], "NONE")
        self.assertEqual(first["production_impact"], "NONE")
        self.assertEqual(first["user_movement"], 0)
        self.assertEqual(first["production_maturity_impact"], "NO_CHANGE")

    def test_11_production_entrypoint_is_fail_closed(self):
        result = self.lib.certify_permanent_polygon_production_entrypoint(root=Path("/opt/v7"))
        self.assertEqual(result["final_verdict"], "PASS", result.get("errors"))
        self.assertTrue(result["checks"]["isolation_guard_stop_safe"])
        self.assertTrue(result["checks"]["consumer_callable_installed"])

    def test_12_cli_exposes_non_test_and_production_callers(self):
        source = (ROOT / "tools/v7-truth-check").read_text(encoding="utf-8")
        self.assertIn("--omp-permanent-polygon-consumer", source)
        self.assertIn("--omp-permanent-polygon-production-certification", source)

    def test_13_selective_invalidation_reopens_only_declared_dependency(self):
        criterion = "CAP-U03:RUNTIME_ELIGIBILITY_EXECUTE_STAY_STOP_SAFE_MATRIX"
        related = self.lib.permanent_polygon_obligation_supply(
            self.cps, root=ROOT, consumed_criterion_ids=[criterion],
            changed_dependencies=["admin_core/operator_execution.py"],
        )
        unrelated = self.lib.permanent_polygon_obligation_supply(
            self.cps, root=ROOT, consumed_criterion_ids=[criterion],
            changed_dependencies=["docs/reference/UNRELATED.md"],
        )
        self.assertEqual(related["next_obligation"]["criterion_id"], criterion)
        self.assertIn(criterion, related["selectively_invalidated_criterion_ids"])
        self.assertNotEqual(unrelated["next_obligation"]["criterion_id"], criterion)
        self.assertNotIn(criterion, unrelated["selectively_invalidated_criterion_ids"])

    def test_14_completed_reentry_telemetry_preserves_only_matching_frontier(self):
        state = self.lib.normalized_cps_live_state()
        generation = "cpsgen_V7_REENTRY_COMPLETE_0123456789AB"
        live = {
            "CURRENT_TRANSITION_ID": "`EXTERNAL_REENTRY_COMPLETED_V1`",
            "CURRENT_STATE_GENERATION": f"`{generation}`",
            "HEARTBEAT_LAST_CPS_GENERATION": f"`{generation}`",
            "HEARTBEAT_LAST_DECISION": "`REENTRY_COMPLETED`",
            "CURRENT_MISSION_ID": f"`{state['current_mission_id']}`",
            "CURRENT_RUN_NONCE": f"`{state['current_run_nonce']}`",
            "CURRENT_NEXT_ACTION_ID": f"`{state['current_next_action_id']}`",
            "CURRENT_PROGRAM_EXECUTION_FRONTIER": f"`{state['current_program_execution_frontier']}`",
            "PENDING_WAKE_ID": "`NONE`",
            "REENTRY_ACTIVE_LEASE": "`NONE`",
            "REENTRY_PLATFORM_HEALTH": "`PASS`",
            "IMMEDIATE_INVOCATION_COUNT": "`9`",
        }
        preserved = self.lib._preserve_certified_external_reentry_telemetry(state, live)
        self.assertEqual(preserved["current_state_generation"], generation)
        self.assertEqual(preserved["immediate_invocation_count"], "9")

        live["CURRENT_RUN_NONCE"] = "`UNRELATED_RUN`"
        rejected = self.lib._preserve_certified_external_reentry_telemetry(state, live)
        self.assertEqual(rejected["current_state_generation"], state["current_state_generation"])
        self.assertEqual(rejected["immediate_invocation_count"], state["immediate_invocation_count"])


if __name__ == "__main__":
    unittest.main()
