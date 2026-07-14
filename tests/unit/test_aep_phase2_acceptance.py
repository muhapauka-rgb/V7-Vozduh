from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "docs/reports/research/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_aep_phase2_acceptance", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AepPhase2AcceptanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.artifact = ARTIFACT.read_text(encoding="utf-8")

    def accept(self, artifact=None, **overrides):
        values = {
            "executor": "CODEX_PHASE_EXECUTION_OWNER",
            "acceptance_owner": "OPERATOR_ENGINEERING_AUTHORITY",
        }
        values.update(overrides)
        return self.lib.aep_phase2_acceptance(self.artifact if artifact is None else artifact, **values)

    def test_01_executor_cannot_accept_own_output(self):
        result = self.accept(acceptance_owner="CODEX_PHASE_EXECUTION_OWNER")
        self.assertEqual(result["acceptance_verdict"], "AEP_PHASE_2_HOLD")

    def test_02_missing_acceptance_owner_holds(self):
        self.assertEqual(self.accept(acceptance_owner="")["role_separation_status"], "HOLD")

    def test_03_ambiguous_artifact_holds(self):
        self.assertIn("phase2_artifact_ambiguous", self.accept(artifact_candidates=2)["holds"])

    def test_04_accepted_aos_reuse_satisfies_phase1_input(self):
        self.assertEqual(self.accept(phase1_accepted=True)["input_readiness"], "PASS")

    def test_05_missing_required_output_fails_schema(self):
        artifact = self.artifact.replace("## 8. Behaviour Coverage", "## 8. Removed Coverage")
        self.assertIn("Behaviour Coverage", self.accept(artifact)["missing_required_outputs"])

    def test_06_empty_heading_does_not_satisfy_output(self):
        artifact = self.artifact.replace("## 9. Behaviour Graph\n", "## 9. Behaviour Graph\nTODO\n", 1)
        self.assertIn("Behaviour Graph", self.accept(artifact)["empty_or_placeholder_outputs"])

    def test_07_bounded_bdp_cannot_claim_project_wide_scope(self):
        result = self.accept(declared_scope="PROJECT_WIDE", bdp_executed_scope="CURRENT_REPOSITORY_SCOPE")
        self.assertEqual(result["project_scope_claim_validity"], "FAIL")

    def test_08_limited_bdp_satisfies_declared_limited_scope(self):
        self.assertEqual(self.accept()["bdp_sufficiency"], "BDP_SUFFICIENT_WITH_EXPLICIT_UNKNOWNS")

    def test_09_missing_p19_blocks_when_applicable(self):
        artifact = self.artifact.replace("`BDP-P19`", "`BDP-PXX`", 1)
        self.assertIn("bdp_scope_insufficient", self.accept(artifact)["holds"])

    def test_10_architecture_only_behaviour_fails_admission(self):
        result = self.accept(behaviour_truth_levels={"BI-X": "T9"})
        self.assertIn("architecture_only_behaviour_admitted", result["errors"])

    def test_11_historical_evidence_cannot_override_current_implementation(self):
        result = self.accept(behaviour_truth_levels={"BI-H": "T8", "BI-C": "T4"})
        self.assertNotIn("architecture_only_behaviour_admitted", result["errors"])

    def test_12_duplicate_behaviour_does_not_increase_coverage(self):
        self.assertEqual(self.accept(duplicate_behaviours=3)["duplicates_suppressed"], 3)

    def test_13_ambiguous_identity_blocks_admission(self):
        self.assertIn("behaviour_identity_ambiguous", self.accept(ambiguous_identities=1)["holds"])

    def test_14_explicit_unknown_passes_with_minor_risks(self):
        self.assertEqual(self.accept()["acceptance_verdict"], "AEP_PHASE_2_ACCEPTED_WITH_MINOR_RISKS")

    def test_15_hidden_unknown_fails_completeness(self):
        self.assertIn("hidden_unknown", self.accept(hidden_unknowns=True)["errors"])

    def test_16_open_chain_requires_explicit_state_and_consumer(self):
        self.assertIn("Producer -> consumer -> terminal state", self.artifact)
        self.assertTrue(self.accept()["explicit_unknowns"])

    def test_17_orphan_behaviour_fails_traceability(self):
        self.assertIn("orphan_behaviour", self.accept(orphan_behaviours=1)["errors"])

    def test_18_phase2_cannot_certify_gaps(self):
        self.assertIn("phase_boundary_violation", self.accept(phase2_certified_gaps=True)["errors"])

    def test_19_phase2_cannot_create_missions(self):
        self.assertIn("phase_boundary_violation", self.accept(phase2_created_mission=True)["errors"])

    def test_20_phase2_cannot_mutate_runtime_or_production(self):
        result = self.accept(runtime_mutation=True, production_mutation=True)
        self.assertIn("phase_boundary_violation", result["errors"])

    def test_21_successful_acceptance_creates_lock(self):
        self.assertEqual(self.accept()["phase2_lock_status"], "LOCKED")

    def test_22_lock_preserves_fingerprint_and_supersession_identity(self):
        result = self.accept()
        self.assertEqual(result["phase2_lock_fingerprint"], result["artifact_fingerprint"])
        self.assertTrue(result["phase2_lock_id"].startswith("aep2lock_"))

    def test_23_lock_sets_aep_current_ready(self):
        self.assertEqual(self.accept()["current_aep_state"], "CURRENT_READY")

    def test_24_successful_lock_sets_phase3_ready(self):
        self.assertEqual(self.accept()["phase3_status"], "READY")

    def test_25_phase3_cannot_start_before_lock(self):
        self.assertEqual(self.accept(lock_requested=False)["phase3_status"], "BLOCKED")

    def test_26_consumer_confirmation_closes_phase2_phase3_edge(self):
        self.assertEqual(self.accept()["phase2_to_phase3_edge"], "COMPLETE")

    def test_27_pass_cannot_return_to_global_real_world_limit(self):
        result = self.accept()
        self.assertEqual(result["phase3_status"], "READY")
        self.assertNotIn("REAL_WORLD_LIMIT", result["acceptance_verdict"])

    def test_28_cps_frontier_target_is_atomic_phase3_identity(self):
        self.assertEqual(
            self.lib.NORMALIZED_CPS_LIVE_STATE["current_program_execution_frontier"],
            "AEP_PHASE_3_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER",
        )

    def test_29_self_continuation_forms_next_mission(self):
        self.assertEqual(
            self.accept()["phase3_mission_id"],
            "V7_AEP_PHASE_3_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER_V1",
        )

    def test_30_replay_reproduces_verdict_and_fingerprint(self):
        first = self.accept()
        second = self.accept()
        self.assertEqual(first["acceptance_verdict"], second["acceptance_verdict"])
        self.assertEqual(first["artifact_fingerprint"], second["artifact_fingerprint"])


if __name__ == "__main__":
    unittest.main()
