import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_polygon_supply_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpPolygonScenarioSupplyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")

    def source(self, **overrides):
        value = {
            "source_owner": "CPS_CURRENT_STATE_CONSISTENCY_OWNER",
            "source_evidence": "owner validator contradiction current_terminal_projection_drift",
            "engineering_intent": "Keep every current terminal projection equal to authoritative CPS state.",
            "current_reality": "One derived terminal projection differs from CPS section 0.",
            "expected_reality": "Every derived terminal projection matches CPS section 0.",
            "target_rule_or_contract": "Current State Consistency",
            "failure_or_gap_class": "CURRENT_TRUTH_CONTRADICTION",
            "affected_producer": "build_normalized_cps_document",
            "affected_consumer": "delegated_policy_live_state_consistency",
            "boundary": "existing CPS projection and validation owner only",
            "stimulus_or_replay_input": "replay stale derived terminal row",
            "expected_observation": "validator rejects drift and normalized builder repairs it",
            "pass_criteria": "current terminal projection equals CPS section 0",
            "fail_criteria": "derived terminal projection remains stale",
            "implementation_allowed": True,
            "verification_plan": "focused deterministic projection and validator regression",
            "rollback_or_stop_safe": "revert owner extension or STOP_SAFE on contradiction",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
            "maturity_impact": "PRODUCTION_MATURITY_CREDIT_FORBIDDEN",
            "new_owner_required": False,
            "new_architecture_required": False,
        }
        value.update(overrides)
        return value

    def test_01_no_sources_produce_no_valid_scenario(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps)
        self.assertEqual(result["supply_status"], "NO_VALID_ENGINEERING_SCENARIO")
        self.assertFalse(result["scenario_consumed_by_bdp"])

    def test_02_production_only_source_is_excluded(self):
        source = self.source(production_impact="USER_MOVEMENT")
        result = self.lib.select_engineering_polygon_scenario([source])
        self.assertEqual(result["selection_status"], "NO_VALID_ENGINEERING_SCENARIO")
        self.assertEqual(result["excluded_sources"][0]["reason"], "PRODUCTION_CONTOUR_ONLY")

    def test_03_valid_rule_gap_materializes_one_instance(self):
        result = self.lib.select_engineering_polygon_scenario([self.source()])
        self.assertEqual(result["selection_status"], "SCENARIO_SELECTED")
        self.assertTrue(result["selected_scenario"]["scenario_instance_id"].startswith("V7-POLYGON-SCENARIO-"))

    def test_04_equivalent_meaning_has_same_identity(self):
        first = self.lib.engineering_polygon_scenario_instance(self.source())["scenario_instance"]
        second = self.lib.engineering_polygon_scenario_instance(self.source(
            engineering_intent="  KEEP every CURRENT terminal projection equal to authoritative cps state. ",
        ))["scenario_instance"]
        self.assertEqual(first["deterministic_identity"], second["deterministic_identity"])

    def test_05_duplicate_scenario_is_suppressed(self):
        instance = self.lib.engineering_polygon_scenario_instance(self.source())["scenario_instance"]
        result = self.lib.select_engineering_polygon_scenario([self.source()], existing_scenarios=[instance])
        self.assertEqual(result["selection_status"], "NO_VALID_ENGINEERING_SCENARIO")
        self.assertEqual(result["duplicate_scenario_count"], 1)

    def test_06_multiple_scenarios_are_deterministically_sequenced(self):
        low = self.source(failure_or_gap_class="ENGINEERING_QUALITY_GAP", engineering_intent="Cover low priority quality gap.")
        high = self.source(engineering_intent="Close current truth contradiction.")
        first = self.lib.select_engineering_polygon_scenario([low, high])["selected_scenario"]
        replay = self.lib.select_engineering_polygon_scenario([high, low])["selected_scenario"]
        self.assertEqual(first["deterministic_identity"], replay["deterministic_identity"])
        self.assertEqual(first["failure_or_gap_class"], "CURRENT_TRUTH_CONTRADICTION")

    def test_07_truth_contradiction_outranks_coverage(self):
        coverage = self.source(failure_or_gap_class="EXECUTION_CERTIFICATION_COVERAGE_GAP", engineering_intent="Cover certification class.")
        result = self.lib.select_engineering_polygon_scenario([coverage, self.source()])
        self.assertEqual(result["selected_scenario"]["failure_or_gap_class"], "CURRENT_TRUTH_CONTRADICTION")

    def test_08_stop_safe_gap_outranks_quality(self):
        safety = self.source(failure_or_gap_class="STOP_SAFE_OR_ROLLBACK_GAP", engineering_intent="Close STOP_SAFE proof gap.")
        quality = self.source(failure_or_gap_class="ENGINEERING_QUALITY_GAP", engineering_intent="Improve quality.")
        result = self.lib.select_engineering_polygon_scenario([quality, safety])
        self.assertEqual(result["selected_scenario"]["failure_or_gap_class"], "STOP_SAFE_OR_ROLLBACK_GAP")

    def test_09_selected_scenario_passes_bdp_reality_gate(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        self.assertEqual(result["supply_status"], "SCENARIO_CONSUMED_BY_BDP")
        self.assertEqual(result["bdp"]["final_verdict"], "PASS")

    def test_10_scenario_uses_omp_admission(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        self.assertEqual(result["bdp"]["admission_decision"], "MISSION_ACCEPTED")
        self.assertEqual(result["bdp"]["candidate"]["omp_consumer"], "OMP_CANDIDATE_ADMISSION")

    def test_11_scenario_does_not_auto_execute_mission(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        self.assertFalse(result["mission_executed"])
        self.assertFalse(result["bdp"]["mission_executed"])

    def test_12_accepted_mission_is_prepared_for_existing_codex_consumer(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        self.assertEqual(result["bdp"]["admission"]["mission_state"], "PREPARED_NOT_ACTIVE")
        self.assertEqual(result["bdp"]["candidate"]["codex_readiness"], "CODEX_READY_WITH_LIMITS")

    def test_13_verification_is_mandatory(self):
        source = self.source(verification_plan="")
        result = self.lib.select_engineering_polygon_scenario([source])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("scenario_source_field_missing:verification_plan", result["errors"])

    def test_14_invalid_scenario_stops_supply(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source(fail_criteria="")])
        self.assertEqual(result["supply_status"], "STOP_SAFE")

    def test_15_runtime_impact_blocks_selection(self):
        result = self.lib.select_engineering_polygon_scenario([self.source(runtime_impact="RUNTIME_APPLY")])
        self.assertEqual(result["selection_status"], "NO_VALID_ENGINEERING_SCENARIO")

    def test_16_production_impact_blocks_selection(self):
        result = self.lib.select_engineering_polygon_scenario([self.source(production_impact="PRODUCTION_MUTATION")])
        self.assertEqual(result["selection_status"], "NO_VALID_ENGINEERING_SCENARIO")

    def test_17_authority_expansion_stops_safe(self):
        result = self.lib.select_engineering_polygon_scenario([self.source(authority_impact="EXPANSION")])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("scenario_authority_boundary", result["errors"])

    def test_18_maturity_credit_stops_safe(self):
        result = self.lib.select_engineering_polygon_scenario([self.source(maturity_impact="INCREASE")])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("scenario_maturity_boundary", result["errors"])

    def test_19_real_world_limit_intents_remain_waiting(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        self.assertEqual(result["bdp"]["candidate"]["state_generation"], "cpsgen_V7_BACKGROUND_AUTOMATION_DEPLOY_PENDING_928718904BCD")
        self.assertNotIn("production_maturity", result["bdp"]["candidate"])

    def test_20_historical_evidence_alone_is_not_a_source(self):
        result = self.lib.select_engineering_polygon_scenario([{"source_evidence": "historical report"}])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIsNone(result["selected_scenario"])

    def test_21_new_owner_requirement_stops_safe(self):
        result = self.lib.select_engineering_polygon_scenario([self.source(new_owner_required=True)])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("scenario_new_owner_boundary", result["errors"])

    def test_22_recalculation_selects_next_distinct_scenario(self):
        first = self.lib.select_engineering_polygon_scenario([self.source(), self.source(
            failure_or_gap_class="CANONICAL_RULE_VERIFICATION_GAP",
            engineering_intent="Verify another canonical rule.",
        )])["selected_scenario"]
        second = self.lib.select_engineering_polygon_scenario([self.source(), self.source(
            failure_or_gap_class="CANONICAL_RULE_VERIFICATION_GAP",
            engineering_intent="Verify another canonical rule.",
        )], existing_scenarios=[first])["selected_scenario"]
        self.assertNotEqual(first["scenario_instance_id"], second["scenario_instance_id"])

    def test_23_selector_returns_only_one_scenario(self):
        result = self.lib.select_engineering_polygon_scenario([
            self.source(),
            self.source(engineering_intent="Second distinct scenario."),
        ])
        self.assertIsInstance(result["selected_scenario"], dict)
        self.assertEqual(result["remaining_distinct_scenario_count"], 2)

    def test_24_replay_returns_identical_selection_and_verdict(self):
        first = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        replay = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        self.assertEqual(first["selection"]["selected_scenario"]["deterministic_identity"], replay["selection"]["selected_scenario"]["deterministic_identity"])
        self.assertEqual(first["bdp"]["admission_decision"], replay["bdp"]["admission_decision"])

    def test_25_every_selected_output_has_bdp_and_omp_consumer(self):
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[self.source()])
        self.assertTrue(result["scenario_consumed_by_bdp"])
        self.assertEqual(result["bdp"]["candidate"]["consumer"], "delegated_policy_live_state_consistency")
        self.assertEqual(result["bdp"]["admission"]["admission_decision"], "MISSION_ACCEPTED")

    def test_26_current_discovery_evaluates_every_source_class(self):
        result = self.lib.discover_engineering_polygon_scenario_sources(self.cps)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["evaluated_source_class_count"], 14)
        self.assertEqual(set(result["evaluated_source_classes"]), set(self.lib.POLYGON_SCENARIO_SOURCE_CLASSES))

    def test_27_current_truth_has_no_active_engineering_scenario(self):
        result = self.lib.current_engineering_polygon_scenario_supply(self.cps)
        self.assertTrue(result["all_source_classes_evaluated"])
        self.assertEqual(result["supply"]["supply_status"], "NO_VALID_ENGINEERING_SCENARIO")
        self.assertEqual(result["discovery"]["active_source_count"], 0)

    def test_28_current_supply_preserves_runtime_production_and_maturity(self):
        result = self.lib.current_engineering_polygon_scenario_supply(self.cps)
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["production_impact"], "NONE")
        self.assertEqual(result["maturity_impact"], "NONE")
        self.assertFalse(result["authority_expansion"])

    def test_29_validator_failure_materializes_owner_backed_source(self):
        error = "delegated_policy_cap_con_06_current_terminal_divergence"
        source = self.lib._polygon_validator_error_source(error)
        result = self.lib.engineering_polygon_scenario_supply_from_cps(self.cps, scenario_sources=[source])
        self.assertEqual(result["supply_status"], "SCENARIO_CONSUMED_BY_BDP")
        self.assertIn(error, result["bdp"]["candidate"]["current_reality"])


if __name__ == "__main__":
    unittest.main()
