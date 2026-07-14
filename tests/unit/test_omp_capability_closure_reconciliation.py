from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
CPS = ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
OMP = ROOT / "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md"
BACKLOG = ROOT / "docs/programs/V7_IMPLEMENTATION_BACKLOG.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpCapabilityClosureReconciliationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        cls.omp = OMP.read_text(encoding="utf-8")
        cls.backlog = BACKLOG.read_text(encoding="utf-8")

    def reconcile(self, *, cps=None, omp=None, backlog=None):
        return self.lib.capability_closure_reconciliation(
            self.cps if cps is None else cps,
            self.omp if omp is None else omp,
            self.backlog if backlog is None else backlog,
        )

    def classify(self, **values):
        return self.lib.classify_capability_remaining_criterion(values)

    def test_01_done_backlog_with_unconsumed_output_remains_open(self):
        self.assertEqual(self.classify(backlog_status="DONE", output_consumed=False), "ENGINEERING_CONSUMPTION_REMAINING")

    def test_02_done_backlog_with_closed_criterion_is_not_open(self):
        self.assertEqual(self.classify(backlog_status="DONE", criterion_closed=True), "NOT_APPLICABLE_WITH_REASON")

    def test_03_historical_done_blocker_is_stale_projection(self):
        self.assertEqual(self.classify(backlog_status="DONE", backlog_claimed_open=True), "ALREADY_COMPLETE_STALE_PROJECTION")

    def test_04_implementation_gap_invalidates_completion(self):
        self.assertEqual(self.classify(implementation_missing=True), "ENGINEERING_IMPLEMENTATION_REMAINING")

    def test_05_integration_gap_invalidates_completion(self):
        self.assertEqual(self.classify(integration_missing=True), "ENGINEERING_INTEGRATION_REMAINING")

    def test_06_executable_verification_gap_is_engineering_work(self):
        self.assertEqual(self.classify(verification_missing=True, verification_executable=True), "ENGINEERING_VERIFICATION_REMAINING")

    def test_07_consumption_gap_enters_engineering_frontier(self):
        self.assertEqual(self.classify(output_consumed=False), "ENGINEERING_CONSUMPTION_REMAINING")

    def test_08_intent_closure_gap_enters_engineering_frontier(self):
        self.assertEqual(self.classify(intent_closed=False), "ENGINEERING_INTENT_CLOSURE_REMAINING")

    def test_09_real_world_only_criterion_remains_waiting(self):
        result = self.classify(real_world_evidence_required=True, engineering_path_complete=True, concrete_real_event=True, reentry_condition="new governed outcome")
        self.assertEqual(result, "REAL_WORLD_EVIDENCE_REQUIRED")

    def test_10_authority_only_criterion_remains_blocked(self):
        self.assertEqual(self.classify(operational_authority_required=True), "OPERATIONAL_AUTHORITY_REQUIRED")

    def test_11_production_certification_is_not_real_world_evidence(self):
        self.assertEqual(self.classify(production_certification_required=True), "PRODUCTION_CERTIFICATION_REQUIRED")

    def test_12_dependency_wait_is_capability_local(self):
        self.assertEqual(self.classify(dependency_wait=True), "DEPENDENCY_WAIT")

    def test_13_independent_ready_criterion_prevents_global_stop(self):
        cps = self.cps.replace("| `CAP-U03` | `BLOCKED_BY_DEPENDENCY` |", "| `CAP-U03` | `READY` |")
        result = self.reconcile(cps=cps)
        self.assertNotEqual(result["global_real_world_limit_verdict"], "GLOBAL_REAL_WORLD_LIMIT_VALID")

    def test_14_no_executable_criteria_validates_implementation_complete(self):
        self.assertEqual(self.reconcile()["implementation_complete_verdict"], "IMPLEMENTATION_COMPLETE_VALID")

    def test_15_no_capability_remains_generic_live_in_progress(self):
        self.assertIn("Historical capability baseline (non-authoritative", self.omp)
        self.assertIn("scheduling_authority=NONE", self.omp)

    def test_16_stale_capability_dashboard_is_replaced_by_cps_pointer(self):
        self.assertIn("Capability Dashboard Source: CPS Authoritative Unfinished Capability Closure Registry", self.omp)

    def test_17_existing_candidate_precedes_new_discovery(self):
        gap = {
            "primary_class": "CONSUMER_CONFIRMATION_CHAIN_CLOSURE",
            "secondary_classes": ["IMPLEMENTATION_OWNER_EXTENSION"],
            "execution_depth": "L2",
            "engineering_intent": "Close current consumer gap.",
            "current_reality": "Output is pending consumer confirmation.",
            "expected_reality": "Output is consumed through OMP admission.",
            "engineering_chain": "INTENT->BDP->CANDIDATE->OMP->MISSION",
            "engineering_chain_segment": "TRIGGER_TO_CONSUMER",
            "behaviour_instance": "One current owner-backed gap.",
            "behaviour": "OMP Mission routing and continuation.",
            "automation_logic": "BDP Discovery Economy plus OMP Self-Continuation.",
            "automation_break": "MISSING_CONSUMER_CONFIRMATION",
            "existing_rule": "Automation Gap Closure and OMP Candidate Admission.",
            "current_outcome": "OUTPUT_PENDING",
            "expected_outcome": "OUTPUT_CONSUMED",
            "intent_closure_state": "AUTOMATION_BREAK",
            "owner": "EXISTING_BDP_AND_OMP_CODEX_OWNERS",
            "producer": "BDP_DISCOVERY_ECONOMY",
            "consumer": "OMP_CANDIDATE_ADMISSION",
            "evidence": "Current CPS and OMP contracts.",
            "implementation_scope": "Existing OMP validation owner.",
            "runtime_impact": "NONE", "production_impact": "NONE",
            "dependencies": "EXISTING_CONTRACTS_READY",
            "verification": "Deterministic admission replay.",
            "verification_context": "Duplicate Candidate fixture.",
            "rollback": "Revert bounded validation and stop safely.",
            "authority": "EXISTING_ENGINEERING_PLANE_AUTHORITY",
            "authority_context": "No expansion.",
            "terminal_path": "OMP_MISSION_OR_LEGAL_TERMINAL",
            "implementation_readiness": "IMPLEMENTATION_READY",
            "omp_consumer": "OMP_CANDIDATE_ADMISSION",
            "codex_readiness": "CODEX_READY_WITH_LIMITS",
            "new_owner_required": False, "new_architecture_required": False,
        }
        first = self.lib.bdp_development_impulse_from_cps(self.cps, engineering_gaps=[gap])
        duplicate = self.lib.bdp_development_impulse_from_cps(self.cps, engineering_gaps=[gap], existing_candidates=[first["candidate"]])
        self.assertEqual(duplicate["handoff_status"], "DUPLICATE_SUPPRESSED")

    def test_18_bdp_is_not_invoked_without_discovery_gap(self):
        self.assertEqual(self.reconcile()["bdp_inputs_created"], 0)

    def test_19_omp_admission_is_not_bypassed(self):
        self.assertIn("Candidate -> OMP admission", self.omp)

    def test_20_audit_output_cannot_start_implementation(self):
        self.assertEqual(self.reconcile()["missions_accepted"], 0)

    def test_21_recalculation_exposes_ready_item_after_wait_closes(self):
        self.assertEqual(self.classify(implementation_missing=True), "ENGINEERING_IMPLEMENTATION_REMAINING")
        self.assertEqual(self.classify(criterion_closed=True), "NOT_APPLICABLE_WITH_REASON")

    def test_22_runtime_and_production_boundaries_remain_unchanged(self):
        result = self.reconcile()
        self.assertEqual((result["runtime_impact"], result["production_impact"]), ("NONE", "NONE"))

    def test_23_reconciliation_does_not_raise_maturity(self):
        self.assertEqual(self.reconcile()["production_maturity_impact"], "NONE")

    def test_24_protected_wip_is_preserved(self):
        self.assertTrue(self.reconcile()["protected_wip_preserved"])

    def test_25_replay_is_deterministic(self):
        self.assertEqual(self.reconcile(), self.reconcile())

    def test_26_current_state_contradiction_fails_into_reconciliation(self):
        self.assertEqual(self.classify(current_state_contradiction=True), "CANONICAL_STATE_RECONCILIATION_REMAINING")

    def test_27_every_current_criterion_has_producer_and_consumer(self):
        self.assertTrue(all("->" in item["producer_consumer"] for item in self.reconcile()["criteria"]))

    def test_28_every_real_world_wait_has_reentry(self):
        rows = [item for item in self.reconcile()["criteria"] if item["primary_classification"] == "REAL_WORLD_EVIDENCE_REQUIRED"]
        self.assertTrue(rows and all(item["reentry_condition"] for item in rows))

    def test_29_backlog_aggregate_matches_item_states(self):
        result = self.reconcile()
        self.assertEqual((result["actionable_backlog_done"], result["actionable_backlog_count"]), (34, 34))

    def test_30_cps_and_omp_pointer_consistency_passes(self):
        self.assertEqual(self.reconcile()["final_verdict"], "PASS")
        self.assertEqual(self.lib.cps_live_state_consistency(self.cps, verify_external=False)["final_verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
