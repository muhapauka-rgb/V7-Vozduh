import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_bdp_handoff_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BdpDevelopmentImpulseHandoffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def gap(self, **overrides):
        values = {
            "primary_class": "CONSUMER_CONFIRMATION_CHAIN_CLOSURE",
            "secondary_classes": ["IMPLEMENTATION_OWNER_EXTENSION"],
            "execution_depth": "L2",
            "engineering_intent": "Consume BDP output before a global development terminal.",
            "current_reality": "A bounded owner-backed gap exists without a live OMP handoff.",
            "expected_reality": "BDP output reaches OMP Candidate Admission.",
            "engineering_chain": "INTENT->BDP->CANDIDATE->OMP->MISSION",
            "engineering_chain_segment": "TRIGGER_TO_CONSUMER",
            "behaviour_instance": "OMP reaches a development terminal with one bounded engineering gap.",
            "behaviour": "BD-003 OMP Mission Routing And Continuation",
            "automation_logic": "BDP Discovery Economy plus OMP Self-Continuation.",
            "automation_break": "MISSING_TRIGGER_AND_LIVE_CONSUMER_INTEGRATION",
            "existing_rule": "Automation Gap Closure and OMP Candidate Admission.",
            "current_outcome": "NO_LIVE_CANDIDATE_HANDOFF",
            "expected_outcome": "CANDIDATE_CONSUMED_BY_OMP",
            "intent_closure_state": "AUTOMATION_BREAK",
            "owner": "EXISTING_BDP_AND_OMP_CODEX_OWNERS",
            "producer": "BDP_DISCOVERY_ECONOMY",
            "consumer": "OMP_CANDIDATE_ADMISSION",
            "evidence": "Current implementation, CPS, OMP and accepted admission evidence.",
            "implementation_scope": "tools/v7_sync_lib.py existing OMP validation owner",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "dependencies": "EXISTING_CONTRACTS_READY",
            "verification": "Focused deterministic handoff tests.",
            "verification_context": "No-gap, one-gap, duplicate, replay and STOP_SAFE fixtures.",
            "rollback": "Revert bounded validation integration and fail closed.",
            "authority": "EXISTING_ENGINEERING_PLANE_AUTHORITY",
            "authority_context": "No expansion; Mission execution remains separate.",
            "terminal_path": "OMP_MISSION_OR_LEGAL_TERMINAL",
            "implementation_readiness": "IMPLEMENTATION_READY",
            "omp_consumer": "OMP_CANDIDATE_ADMISSION",
            "codex_readiness": "CODEX_READY_WITH_LIMITS",
            "new_owner_required": False,
            "new_architecture_required": False,
        }
        values.update(overrides)
        return values

    def state(self, gaps):
        return {
            "state_generation": "cpsgen_TEST_BDP_HANDOFF_V1",
            "discovery_economy_decision": "DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE",
            "engineering_gaps": gaps,
            "real_world_limit_intents": 21,
        }

    def test_no_gap_returns_explicit_no_action(self):
        result = self.lib.bdp_development_impulse_handoff(self.state([]))
        self.assertEqual(result["handoff_status"], "NO_ACTION_REQUIRED")
        self.assertEqual(result["candidate_count"], 0)
        self.assertEqual(result["admission_decision"], "MISSION_NOT_APPLICABLE")
        self.assertFalse(result["mission_created"])
        self.assertEqual(result["real_world_limit_intents_preserved"], 21)

    def test_one_known_gap_produces_one_candidate_and_uses_admission(self):
        result = self.lib.bdp_development_impulse_handoff(self.state([self.gap()]))
        self.assertEqual(result["handoff_status"], "CANDIDATE_CONSUMED_BY_OMP")
        self.assertEqual(result["candidate_count"], 1)
        self.assertEqual(result["admission_decision"], "MISSION_ACCEPTED")
        self.assertTrue(result["mission_created"])
        self.assertFalse(result["mission_executed"])
        self.assertEqual(result["candidate"]["omp_consumer"], "OMP_CANDIDATE_ADMISSION")

    def test_repeated_identical_state_suppresses_duplicate(self):
        first = self.lib.bdp_development_impulse_handoff(self.state([self.gap()]))
        second = self.lib.bdp_development_impulse_handoff(
            self.state([self.gap()]),
            existing_candidates=[first["candidate"]],
        )
        self.assertEqual(second["handoff_status"], "DUPLICATE_SUPPRESSED")
        self.assertEqual(second["candidate_count"], 0)
        self.assertFalse(second["mission_created"])

    def test_replay_is_deterministic(self):
        first = self.lib.bdp_development_impulse_handoff(self.state([self.gap()]))
        replay = self.lib.bdp_development_impulse_handoff(self.state([self.gap()]))
        self.assertEqual(first["candidate"]["candidate_instance_id"], replay["candidate"]["candidate_instance_id"])
        self.assertEqual(first["candidate"]["identity_sha256"], replay["candidate"]["identity_sha256"])
        self.assertEqual(first["admission_decision"], replay["admission_decision"])

    def test_identity_normalizes_case_and_whitespace(self):
        first = self.lib.bdp_development_impulse_handoff(self.state([self.gap()]))
        equivalent = self.gap(
            engineering_intent="  CONSUME   bdp OUTPUT before a GLOBAL development terminal. ",
            current_reality="A bounded owner-backed gap exists without a live OMP handoff.",
        )
        replay = self.lib.bdp_development_impulse_handoff(self.state([equivalent]))
        self.assertEqual(first["candidate"]["identity_sha256"], replay["candidate"]["identity_sha256"])

    def test_historical_candidate_ids_are_not_mutated_or_counted_as_duplicate(self):
        historical = ["ECL-REAL-001", "ECL-REAL-025"]
        before = list(historical)
        result = self.lib.bdp_development_impulse_handoff(
            self.state([self.gap()]),
            existing_candidates=historical,
        )
        self.assertEqual(historical, before)
        self.assertEqual(result["candidate_count"], 1)

    def test_malformed_gap_stops_safe(self):
        result = self.lib.bdp_development_impulse_handoff(
            self.state([{"engineering_intent": "incomplete"}])
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertEqual(result["candidate_count"], 0)
        self.assertFalse(result["mission_created"])

    def test_malformed_state_stops_safe(self):
        state = self.state([])
        state["real_world_limit_intents"] = "unknown"
        result = self.lib.bdp_development_impulse_handoff(state)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("bdp_real_world_limit_intents_invalid", result["errors"])

    def test_more_than_one_gap_stops_safe_without_ranking(self):
        result = self.lib.bdp_development_impulse_handoff(
            self.state([self.gap(), self.gap(engineering_intent="Second gap")])
        )
        self.assertEqual(result["handoff_status"], "STOP_SAFE")
        self.assertIn("bdp_bounded_scope_requires_exactly_one_gap", result["errors"])

    def test_new_owner_or_architecture_requirement_stops_safe(self):
        for field in ("new_owner_required", "new_architecture_required"):
            with self.subTest(field=field):
                result = self.lib.bdp_development_impulse_handoff(
                    self.state([self.gap(**{field: True})])
                )
                self.assertEqual(result["final_verdict"], "STOP_SAFE")

    def test_admission_has_no_runtime_production_or_authority_impact(self):
        result = self.lib.bdp_development_impulse_handoff(self.state([self.gap()]))
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["production_impact"], "NONE")
        self.assertFalse(result["authority_expansion"])
        self.assertEqual(result["admission"]["mission_state"], "PREPARED_NOT_ACTIVE")

    def test_current_cps_runs_no_action_and_preserves_real_world_limits(self):
        result = self.lib.bdp_development_impulse_from_cps(CPS.read_text(encoding="utf-8"))
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["handoff_status"], "NO_ACTION_REQUIRED")
        self.assertEqual(result["candidate_count"], 0)
        self.assertEqual(result["real_world_limit_intents_preserved"], 21)

    def test_self_continuation_program_frontier_preempts_capability_bdp(self):
        result = self.lib.omp_self_continuation_consistency(CPS.read_text(encoding="utf-8"))
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["bdp_development_impulse_status"], "NOT_EVALUATED_PROGRAM_FRONTIER_PREEMPTS_CAPABILITY_GRAPH")
        self.assertEqual(result["bdp_admission_decision"], "NONE")
        self.assertGreaterEqual(result["bdp_real_world_limit_intents_preserved"], 1)


if __name__ == "__main__":
    unittest.main()
