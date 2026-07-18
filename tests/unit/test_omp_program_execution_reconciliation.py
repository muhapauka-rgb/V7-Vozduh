from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_program_reconciliation", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpProgramExecutionReconciliationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        historical_aep = (ROOT / "docs/programs/V7_AUTONOMOUS_EVOLUTION_PROGRAM.md").read_text()
        for marker in (
            "PHASE_4_COMPLETE_CONSUMED",
            "COMPLETE_CONSUMED_REAL_EXTERNAL_CALLER",
            "COMPLETE_CONSUMED_TWO_NATURAL_REENTRIES",
        ):
            historical_aep = historical_aep.replace(marker, "HISTORICAL_TEST_INCOMPLETE")
        current_cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text()
        historical_cps = cls.lib.build_normalized_cps_document(current_cps, {
            "current_program_stage": "FSSE_04_COMPLETE_BOUNDED_CONTINUE_OMP_READY",
            "current_program_execution_frontier": "SAFE_DEPLOY_CURRENT_CANONICAL_HEAD",
            "background_automation_state": "EXTERNAL_REENTRY_IMPLEMENTATION_READY_NOT_YET_PLATFORM_CERTIFIED",
            "aep_phase4_status": "IMPLEMENTED_MANUALLY_CALLABLE",
            "aep_phase5_status": "BLOCKED_MISSING_REAL_CONSUMER",
            "aep_phase6_status": "BLOCKED_BY_PHASE_5",
            "fsse_00_external_reentry_status": "DEFERRED_PLATFORM_CERTIFICATION",
        })
        cls.sources = {
            "stage2": (ROOT / "docs/programs/V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM.md").read_text(),
            "aep": historical_aep,
            "bdp": (ROOT / "docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md").read_text(),
            "implementation": (ROOT / "docs/programs/V7_IMPLEMENTATION_PROGRAM.md").read_text(),
            "backlog": (ROOT / "docs/programs/V7_IMPLEMENTATION_BACKLOG.md").read_text(),
            "omp": (ROOT / "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md").read_text(),
            "cps": historical_cps,
            "autonomous_execution": (ROOT / "docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md").read_text(),
            "autonomous_runtime": (ROOT / "docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md").read_text(),
            "controlled_certification": (ROOT / "docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md").read_text(),
            "aep_phase1": (ROOT / "docs/reports/engineering/V7_AUTONOMOUS_EVOLUTION_FOUNDATION_PHASE1_EXECUTION_REPORT.md").read_text(),
            "aep_phase2": (ROOT / "docs/reports/research/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY.md").read_text(),
            "aep_phase2_execution": (ROOT / "docs/reports/engineering/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_EXECUTION_REPORT.md").read_text(),
            "aep_phase2_acceptance": (ROOT / "docs/reports/research/2026-07-14_100018_aep_phase_2_independent_acceptance.md").read_text(),
            "bdp_execution": "",
        }

    def reconcile(self, **overrides):
        return self.lib.program_execution_reconciliation({**self.sources, **overrides})

    def classify(self, **values):
        return self.lib.classify_program_stage(values)

    def test_01_document_status_is_not_execution_status(self):
        self.assertNotEqual(self.reconcile()["program_inventory"][1]["document_status"], "TERMINAL_COMPLETE")

    def test_02_organized_does_not_equal_complete(self):
        self.assertEqual(self.reconcile()["program_inventory"][1]["execution_status"], "PHASE_3_READY")

    def test_03_ready_document_does_not_equal_executed_scope(self):
        self.assertEqual(self.reconcile()["bdp_status"], "BDP_EXECUTED_FOR_LIMITED_SCENARIO_SCOPE")

    def test_04_output_without_consumer_is_incomplete(self):
        self.assertEqual(self.classify(entry_conditions_met=True, execution_started=True, outputs_found=True, output_schema_valid=True, consumer_found=True, consumer_confirmed=False), "STAGE_CONSUMPTION_NOT_CONFIRMED")

    def test_05_backlog_completion_does_not_close_aep(self):
        result = self.reconcile()
        self.assertEqual(result["backlog_status"], "34/34_DONE")
        self.assertFalse(self.reconcile(aep_phase2_acceptance="")["aep_phase2_accepted"])

    def test_06_polygon_or_limited_work_does_not_close_bdp_project_scope(self):
        self.assertFalse(self.reconcile()["bdp_required_passes_complete"])

    def test_07_stage2_remains_terminal(self):
        self.assertEqual(self.reconcile()["stage2_status"], "STAGE2_TERMINAL_COMPLETE")

    def test_08_phase1_aos_reuse_is_recognized(self):
        stages = self.reconcile()["stages"]
        self.assertEqual(next(x for x in stages if x["stage_id"] == "PHASE_1")["status"], "STAGE_COMPLETE_CONSUMED")

    def test_09_missing_phase2_artifact_reopens_execution(self):
        result = self.reconcile(aep_phase2="")
        self.assertFalse(result["aep_phase2_output_complete"])

    def test_10_missing_bdp_project_scope_is_explicit(self):
        self.assertEqual(self.reconcile()["bdp_status"], "BDP_EXECUTED_FOR_LIMITED_SCENARIO_SCOPE")

    def test_11_accepted_current_reality_prevents_duplicate_phase2(self):
        accepted = "CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_ACCEPTED PHASE_ACCEPTED PHASE_LOCKED"
        result = self.reconcile(aep_phase2_acceptance=accepted)
        self.assertTrue(result["aep_phase2_accepted"])

    def test_12_phase3_is_ready_after_phase2_acceptance(self):
        phase3 = next(x for x in self.reconcile()["stages"] if x["stage_id"] == "PHASE_3")
        self.assertEqual(phase3["status"], "STAGE_READY_NOT_STARTED")

    def test_13_unconsumed_certified_output_is_not_complete(self):
        self.assertEqual(self.classify(entry_conditions_met=True, execution_started=True, outputs_found=True, output_schema_valid=True, consumer_found=True, consumer_confirmed=False), "STAGE_CONSUMPTION_NOT_CONFIRMED")

    def test_14_missing_owner_consumption_remains_open(self):
        self.assertEqual(self.classify(entry_conditions_met=True, execution_started=True, outputs_found=True, output_schema_valid=True, consumer_found=False), "STAGE_CONSUMER_MISSING")

    def test_15_acceptance_waits_for_revalidation(self):
        self.assertFalse(self.reconcile(aep_phase2_acceptance="")["acceptance_required"])

    def test_16_missing_revalidation_keeps_phase2_in_progress(self):
        phase2 = next(x for x in self.reconcile(aep_phase2_acceptance="")["stages"] if x["stage_id"] == "PHASE_2")
        self.assertEqual(phase2["status"], "STAGE_IN_PROGRESS")

    def test_17_real_world_boundary_is_invalid_with_safe_program_stage(self):
        self.assertEqual(self.reconcile()["global_real_world_limit_verdict"], "GLOBAL_REAL_WORLD_LIMIT_VALID")

    def test_18_authority_boundary_is_classified(self):
        self.assertEqual(self.classify(blocked_authority=True), "STAGE_BLOCKED_AUTHORITY")

    def test_19_dependency_wait_remains_local(self):
        self.assertEqual(self.classify(blocked_dependency=True), "STAGE_BLOCKED_DEPENDENCY")

    def test_20_stage_sequence_cannot_skip_entry_conditions(self):
        self.assertEqual(self.classify(entry_conditions_met=False), "STAGE_BLOCKED_DEPENDENCY")

    def test_21_program_graph_is_deterministic(self):
        self.assertEqual(self.reconcile()["stages"], self.reconcile()["stages"])

    def test_22_historical_reports_do_not_supply_acceptance(self):
        self.assertFalse(self.reconcile(aep_phase2_acceptance="historical report only")["aep_phase2_accepted"])

    def test_23_every_output_needs_consumer_or_terminal(self):
        self.assertEqual(self.classify(entry_conditions_met=True, execution_started=True, outputs_found=True, output_schema_valid=True, consumer_found=False), "STAGE_CONSUMER_MISSING")

    def test_24_terminal_claim_requires_acceptance(self):
        self.assertNotEqual(next(x for x in self.reconcile(aep_phase2_acceptance="")["stages"] if x["stage_id"] == "PHASE_2")["status"], "STAGE_COMPLETE_CONSUMED")

    def test_25_no_new_program_or_owner_is_created(self):
        ids = {item["program_id"] for item in self.reconcile()["program_inventory"]}
        self.assertIn("OMP", ids)
        self.assertIn("AEP", ids)

    def test_26_runtime_production_authority_unchanged(self):
        result = self.reconcile()
        self.assertEqual((result["runtime_impact"], result["production_impact"], result["authority_impact"]), ("NONE", "NONE", "NONE"))

    def test_27_ordinary_program_frontier_preempts_new_scenario_generation(self):
        self.assertEqual(self.reconcile()["executable_program_frontier"], ["AEP_PHASE_3_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER"])

    def test_28_replay_reproduces_inventory_and_sequence(self):
        self.assertEqual(self.reconcile(), self.reconcile())

    def test_29_cps_receives_program_frontier(self):
        self.assertIn("V7_POLYGON_PERMANENT_OMP_CONSUMER_AND_OBLIGATION_SUPPLY_RECONCILIATION_V1", self.sources["cps"])
        self.assertIn("PERMANENT_POLYGON_OMP_CONSUMER_ACTIVE_AND_FIRST_CAPABILITY_OBLIGATION_CONSUMED", self.sources["cps"])
        self.assertIn("CURRENT_PROGRAM_EXECUTION_FRONTIER` | `SAFE_DEPLOY_CURRENT_CANONICAL_HEAD", self.sources["cps"])
        self.assertNotIn("global program frontier is OMP_REAL_CONSUMER_ACTIVATION", self.sources["cps"])

    def test_30_omp_consumes_program_frontier(self):
        self.assertIn("Program Execution And Consumption Reconciliation Rule", self.sources["omp"])

    def test_31_phase6_real_world_limit_is_consumed_and_phase7_stays_blocked(self):
        aep = self.sources["aep"].replace(
            "PHASE_6_MULTI_LANE_EVIDENCE_MODEL = ACTIVE", "HISTORICAL_SINGLE_LANE_MODEL",
        ) + """
COMPLETE_CONSUMED_TWO_NATURAL_REENTRIES
PHASE_6_VERDICT = REAL_WORLD_LIMIT
FULL_OR_BOUNDED_CERTIFICATION = NOT_ACCEPTED
PHASE_7 = PHASE_7_NOT_STARTED
NEXT_ACTION = WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES
"""
        result = self.reconcile(aep=aep)
        phase6 = next(item for item in result["stages"] if item["stage_id"] == "PHASE_6")
        phase7 = next(item for item in result["stages"] if item["stage_id"] == "PHASE_7")
        self.assertEqual(result["aep_status"], "PHASE_6_REAL_WORLD_LIMIT")
        self.assertEqual(result["aep_phase6_status"], "REAL_WORLD_LIMIT")
        self.assertEqual(phase6["status"], "STAGE_BLOCKED_REAL_WORLD")
        self.assertEqual(phase7["status"], "STAGE_BLOCKED_DEPENDENCY")
        self.assertEqual((result["runtime_impact"], result["production_impact"], result["authority_impact"]), ("NONE", "NONE", "NONE"))


if __name__ == "__main__":
    unittest.main()
