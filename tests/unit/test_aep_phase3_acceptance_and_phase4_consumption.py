from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
REGISTER_FP = "b164319d05c8c70af130ef4b32066165b1a4e6b33fc7efad51f6d3d6e4e3b54f"
LOCK_FP = "f4e40b34f14e2743819e3a2e4bb61b6793493ba603f384a168f62bdff84c5e1d"
LOCK_ID = "aep3lock_f4e40b34f14e2743819e3a2e"
AUTHORITY_FP = "d9f30a5a4488a8231e705bad1725e091511fb84facb49e59260fa61f9df6987d"
CANDIDATE_ID = "BDP-ICI-7CFAE2C09DBC51947C9718E6"
MISSION_ID = "V7_OMP_PHASE_3_TO_PHASE_4_PROGRAM_CONSUMER_EXTENSION_V1"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_aep3_acceptance", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AepPhase3AcceptanceAndPhase4ConsumptionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.phase2 = (ROOT / "docs/reports/research/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY.md").read_text()
        cls.register = (ROOT / "docs/reports/research/V7_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER.md").read_text()
        cls.sources = {
            "stage2": (ROOT / "docs/programs/V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM.md").read_text(),
            "aep": (ROOT / "docs/programs/V7_AUTONOMOUS_EVOLUTION_PROGRAM.md").read_text(),
            "bdp": (ROOT / "docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md").read_text(),
            "implementation": (ROOT / "docs/programs/V7_IMPLEMENTATION_PROGRAM.md").read_text(),
            "backlog": (ROOT / "docs/programs/V7_IMPLEMENTATION_BACKLOG.md").read_text(),
            "omp": (ROOT / "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md").read_text(),
            "cps": (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(),
            "aep_phase1": (ROOT / "docs/reports/engineering/V7_AUTONOMOUS_EVOLUTION_FOUNDATION_PHASE1_EXECUTION_REPORT.md").read_text(),
            "aep_phase2": cls.phase2,
            "aep_phase2_execution": (ROOT / "docs/reports/engineering/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_EXECUTION_REPORT.md").read_text(),
            "aep_phase2_acceptance": (ROOT / "docs/reports/research/2026-07-14_100018_aep_phase_2_independent_acceptance.md").read_text(),
            "aep_phase3_register": cls.register,
        }

    def gap(self):
        return {
            "primary_classification": "OMP_CONTINUATION_GAP",
            "secondary_classes": ["CONSUMER_AUTOMATION_GAP", "OWNER_EXTENSION_GAP"],
            "behaviour_definition_id": "BD-016",
            "behaviour_instance_id": "BI-028",
            "engineering_chain_id": "AEP-PHASE3->ACCEPTANCE->PHASE4->OMP",
            "engineering_intent": "Accepted AEP output must reach its named next-stage OMP consumer.",
            "current_reality": "Program reconciliation stops at Phase 3 READY and always blocks Phase 4.",
            "expected_reality": "Accepted locked Phase 3 output deterministically opens Phase 4 consumption.",
            "failed_chain_segment": "PHASE3_ACCEPTED_OUTPUT_TO_PHASE4_CONSUMER",
            "producer": "AEP_PHASE_3_CERTIFICATION_OWNER",
            "consumer": "OMP_PROGRAM_EXECUTION_RECONCILIATION",
            "evidence": "tools/v7_sync_lib.py and focused tests",
            "truth_level": "T4",
            "freshness": "CURRENT_COMMIT",
            "owner": "OMP+AEP+CPS_EXISTING_OWNERS",
            "verification": "Focused tests plus CPS/OMP consumer confirmation.",
            "rollback": "Revert extension and retain Phase 3 acceptance STOP_SAFE.",
            "terminal_path": "PHASE4_OMP_ADMISSION_OR_LEGAL_HOLD",
            "implementation_scope": "Extend existing program reconciliation consumer only.",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_context": "Independent acceptance mandatory; no expansion.",
            "real_world_context": "No real-world evidence required.",
            "root_cause": "Existing deterministic consumer models only Phase 2 acceptance.",
            "smallest_existing_next_action": "Extend program_execution_reconciliation.",
            "dependencies": "EXISTING_CONTRACTS_READY",
            "new_owner_required": False,
            "new_architecture_required": False,
        }

    def accepted(self):
        return self.lib.aep_phase3_gap_certification(
            self.phase2,
            [self.gap()],
            expected_phase2_lock_fingerprint="128691e74c0b2087e1ffb0fc26c64d6425ef68ec46af79a747f60bae28a73951",
            executor="CODEX_PHASE_EXECUTION_OWNER",
            acceptance_owner="OPERATOR_ENGINEERING_AUTHORITY",
            operator_authority=True,
            acceptance_mission_id="V7_AEP_PHASE_3_INDEPENDENT_ACCEPTANCE_AND_LOCK_V1",
            acceptance_run_nonce="V7_AEP_PHASE_3_ACCEPTANCE_LOCK_V1_2F8C6D14A97E",
        )

    def accepted_register(self):
        text = self.register.replace("Status: `AEP_PHASE_3_READY_FOR_INDEPENDENT_ACCEPTANCE`", "Status: `AEP_PHASE_3_GAP_REGISTER_ACCEPTED_LOCKED`")
        text = text.replace("PHASE_3_ACCEPTANCE_STATUS = AEP_PHASE_3_READY_FOR_ACCEPTANCE", "PHASE_3_ACCEPTANCE_STATUS = AEP_PHASE_3_GAP_REGISTER_ACCEPTED")
        return text

    def acceptance_report(self, **overrides):
        values = {
            "PHASE_3_ACCEPTANCE_VERDICT": "AEP_PHASE_3_GAP_REGISTER_ACCEPTED",
            "PHASE_3_ACCEPTANCE_OWNER": "OPERATOR_ENGINEERING_AUTHORITY",
            "AUTHORITY_SCOPE_FINGERPRINT": AUTHORITY_FP,
            "PHASE_3_REGISTER_FINGERPRINT": REGISTER_FP,
            "PHASE_3_LOCK_ID": LOCK_ID,
            "PHASE_3_LOCK_FINGERPRINT": LOCK_FP,
        }
        values.update(overrides)
        return "\n".join(f"{key} = {value}" for key, value in values.items())

    def lock_report(self, **overrides):
        values = {
            "REGISTER_FINGERPRINT": REGISTER_FP,
            "PHASE_3_LOCK_STATUS": "LOCKED",
            "PHASE_3_LOCK_ID": LOCK_ID,
            "PHASE_3_LOCK_FINGERPRINT": LOCK_FP,
        }
        values.update(overrides)
        return "\n".join(f"{key} = {value}" for key, value in values.items())

    def phase4_report(self, *, real_consumer=False):
        lines = [
            f"MISSION_ID_CREATED = {MISSION_ID}",
            "OMP_ADMISSION_DECISION = MISSION_ACCEPTED",
            "IMPLEMENTATION_RESULT = COMPLETE_VERIFIED",
            "PHASE_3_TO_PHASE_4_CONSUMPTION_STATUS = PASS",
            "ENGINEERING_INTENT_CLOSURE_STATUS = CLOSED",
        ]
        if real_consumer:
            lines.extend((
                "REAL_TRIGGER_OCCURRED = TRUE",
                "REAL_ENTRYPOINT_INVOKED = TRUE",
                "RECONCILIATION_CALLED = TRUE",
                "CONSUMER_INVOKED = TRUE",
                "CONSUMER_BEHAVIOR_CHANGED = TRUE",
                "NEXT_OUTPUT_CREATED = TRUE",
            ))
        return "\n".join(lines)

    def reconcile(self, *, locked=False, implemented=False, real_consumer=False, **overrides):
        sources = dict(self.sources)
        if locked:
            sources.update({
                "aep_phase3_register": self.accepted_register(),
                "aep_phase3_acceptance": self.acceptance_report(),
                "aep_phase3_lock": self.lock_report(),
            })
        if implemented:
            sources["aep_phase4_execution"] = self.phase4_report(real_consumer=real_consumer)
        sources.update(overrides)
        return self.lib.program_execution_reconciliation(sources)

    def candidate(self):
        return self.accepted()["candidate_instances"][0]

    def test_01_unaccepted_phase3_keeps_phase4_locked(self):
        self.assertEqual(self.reconcile()["aep_phase4_status"], "BLOCKED")

    def test_02_accepted_without_lock_keeps_phase4_locked(self):
        result = self.reconcile(aep_phase3_register=self.accepted_register(), aep_phase3_acceptance=self.acceptance_report())
        self.assertFalse(result["aep_phase3_locked"])

    def test_03_lock_fingerprint_mismatch_stops_safe(self):
        result = self.reconcile(locked=True, aep_phase3_lock=self.lock_report(PHASE_3_LOCK_FINGERPRINT="0" * 64))
        self.assertIn("aep_phase3_lock_invalid", result["errors"])

    def test_04_register_fingerprint_mismatch_stops_safe(self):
        result = self.reconcile(locked=True, aep_phase3_acceptance=self.acceptance_report(PHASE_3_REGISTER_FINGERPRINT="0" * 64))
        self.assertIn("aep_phase3_acceptance_invalid", result["errors"])

    def test_05_accepted_locked_phase3_sets_gap_ready(self):
        self.assertEqual(self.reconcile(locked=True)["aep_state"], "GAP_READY")

    def test_06_accepted_locked_phase3_sets_phase4_ready(self):
        self.assertEqual(self.reconcile(locked=True)["aep_phase4_status"], "READY")

    def test_07_candidate_identity_is_deterministic(self):
        self.assertEqual(self.candidate(), self.candidate())

    def test_08_candidate_appears_only_after_lock(self):
        self.assertEqual(self.reconcile()["aep_phase3_candidate_ids"], [])
        self.assertEqual(self.reconcile(locked=True)["aep_phase3_candidate_ids"], [CANDIDATE_ID])

    def test_09_duplicate_candidate_is_suppressed(self):
        result = self.lib.omp_candidate_admission_decision(self.candidate(), existing_candidate_ids=[CANDIDATE_ID])
        self.assertEqual(result["admission_decision"], "MISSION_NOT_APPLICABLE")

    def test_10_unique_candidate_is_admitted(self):
        result = self.lib.omp_candidate_admission_decision(self.candidate(), mission_id=MISSION_ID)
        self.assertEqual(result["admission_decision"], "MISSION_ACCEPTED")

    def test_11_admission_uses_expected_mission_identity(self):
        result = self.lib.omp_candidate_admission_decision(self.candidate(), mission_id=MISSION_ID)
        self.assertEqual(result["mission_id"], MISSION_ID)

    def test_12_zero_gap_register_opens_legal_no_mission_path(self):
        register = self.accepted_register().replace("CERTIFIED_GAPS = 1", "CERTIFIED_GAPS = 0").replace(CANDIDATE_ID, "NON_CANDIDATE")
        lock_fp = self.lib._aep_phase3_lock_fingerprint(REGISTER_FP, "OPERATOR_ENGINEERING_AUTHORITY", AUTHORITY_FP, [])
        result = self.reconcile(
            locked=True,
            aep_phase3_register=register,
            aep_phase3_acceptance=self.acceptance_report(PHASE_3_LOCK_ID=f"aep3lock_{lock_fp[:24]}", PHASE_3_LOCK_FINGERPRINT=lock_fp),
            aep_phase3_lock=self.lock_report(PHASE_3_LOCK_ID=f"aep3lock_{lock_fp[:24]}", PHASE_3_LOCK_FINGERPRINT=lock_fp),
        )
        self.assertTrue(result["aep_phase4_consumed"])

    def test_13_one_gap_register_creates_one_candidate_frontier(self):
        self.assertEqual(len(self.reconcile(locked=True)["aep_phase3_candidate_ids"]), 1)

    def test_14_multiple_candidates_are_deterministically_sorted(self):
        register = self.accepted_register().replace("CERTIFIED_GAPS = 1", "CERTIFIED_GAPS = 2") + "\nBDP-ICI-000000000000000000000000"
        ids = ["BDP-ICI-000000000000000000000000", CANDIDATE_ID]
        lock_fp = self.lib._aep_phase3_lock_fingerprint(REGISTER_FP, "OPERATOR_ENGINEERING_AUTHORITY", AUTHORITY_FP, ids)
        acceptance = self.acceptance_report(PHASE_3_LOCK_ID=f"aep3lock_{lock_fp[:24]}", PHASE_3_LOCK_FINGERPRINT=lock_fp)
        lock = self.lock_report(PHASE_3_LOCK_ID=f"aep3lock_{lock_fp[:24]}", PHASE_3_LOCK_FINGERPRINT=lock_fp)
        first = self.reconcile(locked=True, aep_phase3_register=register, aep_phase3_acceptance=acceptance, aep_phase3_lock=lock)["aep_phase3_candidate_ids"]
        second = self.reconcile(locked=True, aep_phase3_register=register, aep_phase3_acceptance=acceptance, aep_phase3_lock=lock)["aep_phase3_candidate_ids"]
        self.assertEqual(first, second)
        self.assertEqual(first, ids)

    def test_15_candidate_cannot_bypass_omp_admission(self):
        incomplete = dict(self.candidate(), verification="")
        self.assertEqual(self.lib.omp_candidate_admission_decision(incomplete)["admission_decision"], "MISSION_REJECTED")

    def test_16_admission_failure_creates_no_mission(self):
        incomplete = dict(self.candidate(), verification="")
        self.assertFalse(self.lib.omp_candidate_admission_decision(incomplete)["mission_created"])

    def test_17_admission_pass_creates_one_mission(self):
        self.assertTrue(self.lib.omp_candidate_admission_decision(self.candidate(), mission_id=MISSION_ID)["mission_created"])

    def test_18_decision_trace_is_deterministic(self):
        first = self.lib.omp_candidate_admission_decision(self.candidate(), mission_id=MISSION_ID)
        second = self.lib.omp_candidate_admission_decision(self.candidate(), mission_id=MISSION_ID)
        self.assertEqual(first["decision_fingerprint"], second["decision_fingerprint"])

    def test_19_manual_implementation_does_not_open_phase5(self):
        self.assertEqual(self.reconcile(locked=True, implemented=True)["aep_phase5_status"], "BLOCKED")

    def test_20_phase4_missing_consumer_confirmation_does_not_open_phase5(self):
        self.assertEqual(self.reconcile(locked=True, aep_phase4_execution="IMPLEMENTATION_RESULT = COMPLETE_VERIFIED")["aep_phase5_status"], "BLOCKED")

    def test_21_phase2_only_state_remains_backward_compatible(self):
        self.assertEqual(self.lib.program_execution_reconciliation({**self.sources, "aep_phase3_register": ""})["aep_status"], "PHASE_3_READY")

    def test_22_replay_reproduces_program_state(self):
        self.assertEqual(self.reconcile(locked=True, implemented=True), self.reconcile(locked=True, implemented=True))

    def test_23_no_runtime_or_production_mutation(self):
        result = self.reconcile(locked=True, implemented=True)
        self.assertEqual((result["runtime_impact"], result["production_impact"]), ("NONE", "NONE"))

    def test_24_no_authority_expansion(self):
        self.assertEqual(self.reconcile(locked=True, implemented=True)["authority_impact"], "NONE")

    def test_25_role_separation_passes(self):
        self.assertEqual(self.accepted()["role_separation_status"], "PASS")

    def test_26_executor_cannot_self_accept(self):
        result = self.lib.aep_phase3_gap_certification(
            self.phase2, [self.gap()], expected_phase2_lock_fingerprint="128691e74c0b2087e1ffb0fc26c64d6425ef68ec46af79a747f60bae28a73951",
            executor="CODEX_PHASE_EXECUTION_OWNER", acceptance_owner="CODEX_PHASE_EXECUTION_OWNER", operator_authority=True,
        )
        self.assertEqual(result["role_separation_status"], "HOLD")

    def test_27_authority_scope_fingerprint_is_deterministic(self):
        self.assertEqual(self.accepted()["authority_scope_fingerprint"], self.accepted()["authority_scope_fingerprint"])

    def test_28_lock_fingerprint_is_deterministic(self):
        self.assertEqual(self.accepted()["phase3_lock_fingerprint"], LOCK_FP)

    def test_29_engineering_intent_requires_real_consumer_confirmation(self):
        self.assertFalse(self.reconcile(locked=True, implemented=True)["aep_phase4_consumed"])

    def test_30_next_omp_action_is_fsse03_when_external_reentry_is_deferred(self):
        self.assertEqual(
            self.reconcile(locked=True, implemented=True)["executable_program_frontier"],
            ["V7_FUTURE_SCALE_HIGH_FIDELITY_VALIDATION_V1"],
        )

    def test_31_real_consumer_proof_opens_phase5(self):
        result = self.reconcile(locked=True, implemented=True, real_consumer=True)
        self.assertTrue(result["aep_phase4_consumed"])
        self.assertEqual(result["aep_phase5_status"], "COMPLETE_CONSUMED")

    def test_32_each_real_consumer_proof_is_required(self):
        full = self.phase4_report(real_consumer=True)
        for token in (
            "REAL_TRIGGER_OCCURRED = TRUE",
            "REAL_ENTRYPOINT_INVOKED = TRUE",
            "RECONCILIATION_CALLED = TRUE",
            "CONSUMER_INVOKED = TRUE",
            "CONSUMER_BEHAVIOR_CHANGED = TRUE",
            "NEXT_OUTPUT_CREATED = TRUE",
        ):
            result = self.reconcile(locked=True, aep_phase4_execution=full.replace(token, ""))
            self.assertFalse(result["aep_phase4_consumed"], token)


if __name__ == "__main__":
    unittest.main()
