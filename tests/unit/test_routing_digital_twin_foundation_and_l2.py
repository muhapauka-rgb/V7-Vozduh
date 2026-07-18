from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_digital_twin_test", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RoutingDigitalTwinFoundationAndL2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.foundation = cls.lib.routing_digital_twin_foundation(root=ROOT)
        cls.l2 = cls.lib.execute_routing_digital_twin_l2_obligation(root=ROOT)
        cls.l4 = cls.lib.execute_routing_digital_twin_outcome_counterfactual_shadow_learning(
            root=ROOT, l2_result=cls.l2,
        )
        cls.synthetic_l3 = {
            "final_verdict": "PASS", "fidelity_levels": ["L3", "L4"],
            "cleanup": {"containers_remaining": [], "networks_remaining": []},
        }
        cls.l5 = cls.lib.execute_routing_digital_twin_snapshot_and_hybrid_scale(
            root=ROOT, l2_result=cls.l2, l3_l4_result=cls.synthetic_l3,
        )

    def test_01_foundation_closes_and_forms_exact_l2_obligation(self):
        self.assertEqual(self.foundation["final_verdict"], "PASS", self.foundation.get("errors"))
        self.assertEqual(
            self.foundation["mission_terminal"],
            "DIGITAL_TWIN_FOUNDATION_AND_FIRST_L2_OBLIGATION_CERTIFIED",
        )
        self.assertEqual(
            self.foundation["first_l2_obligation"]["obligation_id"],
            "DT-L2-VIRTUAL-APPLY-001",
        )

    def test_02_identity_contract_is_complete_and_extensible(self):
        identity = self.foundation["identity_contract"]
        self.assertEqual(identity["final_verdict"], "PASS", identity.get("errors"))
        self.assertTrue(set(self.lib.ROUTING_DIGITAL_TWIN_IDENTITY_FIELDS).issubset(identity["identity"]))
        self.assertTrue(identity["compatible_extension_required"])

    def test_03_fidelity_and_sufficiency_are_criterion_scoped(self):
        fidelity = self.foundation["fidelity_contract"]
        self.assertEqual([row["level"] for row in fidelity["levels"]], [f"L{i}" for i in range(1, 9)])
        self.assertTrue(fidelity["criterion_scoped"])
        self.assertIn(
            "REQUIRES_NATURAL_PRODUCTION",
            self.foundation["criterion_sufficiency_contract"]["coverage_states"],
        )

    def test_04_isolation_contract_has_no_production_path(self):
        isolation = self.foundation["isolation_contract"]
        self.assertEqual(isolation["final_verdict"], "PASS", isolation.get("errors"))
        self.assertFalse(isolation["production_path_overlap"])
        self.assertFalse(isolation["production_executor_callable"])
        self.assertFalse(any(isolation["forbidden_effects"].values()))

    def test_05_world_practices_are_mapped_without_new_owner(self):
        rows = self.foundation["world_practice_mapping"]
        self.assertGreaterEqual(len(rows), 6)
        self.assertTrue(all(row["decision"] in {"REUSE", "ADAPT", "REJECT_AS_DEFAULT"} for row in rows))
        self.assertEqual(self.foundation["duplication_audit"], "PASS_REUSE_EXISTING_ENGINEERING_POLYGON_AND_OMP_OWNERS")

    def test_06_real_v7_l2_loop_closes(self):
        self.assertEqual(self.l2["final_verdict"], "PASS", self.l2.get("errors"))
        self.assertEqual(self.l2["mission_terminal"], "REAL_V7_DECISION_AND_VIRTUAL_EXECUTION_LOOP_CERTIFIED")
        self.assertEqual(self.l2["next_mission_id"], self.lib.ROUTING_DIGITAL_TWIN_L3_MISSION_ID)
        self.assertTrue(all(self.l2["checks"].values()))

    def test_07_l2_uses_real_planner_packet_and_lease_owners(self):
        execution = self.l2["real_owner_execution"]
        self.assertEqual(execution["planner"]["selected_count"], 1)
        self.assertTrue(execution["packet_identity"]["packet_id"].startswith("dtpkt_"))
        self.assertTrue(execution["lease_active"])
        self.assertFalse(execution["production_packet_executed"])

    def test_08_virtual_apply_covers_success_stay_rollback_and_containment(self):
        terminals = self.l2["virtual_execution_terminals"]
        self.assertTrue({"SUCCESS", "CORRECT_STAY", "ROLLBACK", "STOP_SAFE"}.issubset(terminals))
        self.assertTrue(terminals["SUCCESS"]["isolated_state_changed"])
        self.assertEqual(terminals["ROLLBACK"]["before_fingerprint"], terminals["ROLLBACK"]["after_fingerprint"])
        self.assertEqual(terminals["STOP_SAFE"]["before_fingerprint"], terminals["STOP_SAFE"]["after_fingerprint"])

    def test_09_forbidden_effects_are_absent(self):
        self.assertFalse(any(self.l2["forbidden_effects"].values()))
        self.assertEqual(self.l2["production_impact"], "NONE")
        self.assertEqual(self.l2["authority_impact"], "NONE")

    def test_10_non_test_master_entrypoint_is_wired(self):
        source = (ROOT / "tools/v7-truth-check").read_text(encoding="utf-8")
        self.assertIn("--omp-routing-digital-twin-program", source)
        self.assertIn("execute_routing_digital_twin_master_program", source)

    def test_11_counterfactual_shadow_learning_loop_closes(self):
        self.assertEqual(self.l4["final_verdict"], "PASS", self.l4.get("errors"))
        self.assertFalse(self.l4["counterfactual"]["weighted_score_used"])
        self.assertEqual(self.l4["counterfactual"]["selected_branch"], "EXECUTE_SELECTED_V7_DECISION")
        self.assertTrue(self.l4["checks"]["held_out_replay_consumed"])
        self.assertTrue(self.l4["shadow_learning"]["cleanup"]["discarded"])

    def test_12_sanitized_snapshot_is_one_way_and_secret_free(self):
        snapshot = self.l5["snapshot_contract"]
        self.assertEqual(snapshot["final_verdict"], "PASS", snapshot.get("errors"))
        self.assertTrue(snapshot["one_way_export"])
        self.assertFalse(snapshot["reverse_write_path"])
        self.assertFalse(snapshot["raw_command_outputs_included"])
        self.assertFalse(snapshot["scanner_findings"])

    def test_13_hybrid_scale_is_deterministic_and_compacted(self):
        self.assertEqual(self.l5["final_verdict"], "PASS", self.l5.get("errors"))
        envelope = self.l5["resource_envelope"]
        self.assertGreaterEqual(envelope["logical_events"], 2_000_000)
        self.assertEqual(envelope["logical_fingerprint"], envelope["replay_fingerprint"])
        self.assertEqual(envelope["materialized_event_rows"], 0)
        self.assertTrue(self.l5["checks"]["logical_10k_100"])

    def test_14_substrate_degradation_never_claims_real_world_limit(self):
        probe = self.lib.routing_digital_twin_substrate_probe()
        self.assertEqual(probe["final_verdict"], "PASS")
        self.assertFalse(probe["global_real_world_limit"])

    def test_15_integrated_terminal_is_reserved_for_deployment_truth(self):
        technical = self.lib.certify_routing_digital_twin_integrated_program(mission_results=[])
        self.assertNotEqual(technical["program_terminal"], "AUTONOMOUS_HIGH_FIDELITY_ROUTING_DIGITAL_TWIN_POLYGON_CERTIFIED")
        self.assertFalse(technical["program_complete"])

    def test_16_production_caller_consumes_entrypoint_and_stops_at_isolation(self):
        result = self.lib.certify_routing_digital_twin_production_entrypoint(root=Path("/opt/v7"))
        self.assertEqual(result["final_verdict"], "PASS", result.get("errors"))
        self.assertEqual(result["guarded_master_call"]["program_terminal"], "FOUNDATION_STOP_SAFE")
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["user_movement"], 0)


if __name__ == "__main__":
    unittest.main()
