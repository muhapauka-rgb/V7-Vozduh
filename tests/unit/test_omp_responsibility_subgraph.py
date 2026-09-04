from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_sync_lib_responsibility_subgraph", ROOT / "tools/v7_sync_lib.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpResponsibilitySubgraphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def test_current_pilot_is_bounded_derived_and_discardable(self):
        request = self.lib.responsibility_subgraph_pilot_request(root=ROOT)
        result = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["truth_class"], "DERIVED_EVIDENCE")
        self.assertFalse(result["canonical"])
        self.assertTrue(result["discardable"])
        self.assertEqual(result["decision_authority"], "NONE")
        self.assertEqual(result["cps_impact"], "NONE")
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertLessEqual(len(result["edges"]), request["max_edges"])
        self.assertEqual(result["evidence_fingerprint_scope"], "CANONICAL_STATIC_STRUCTURE_ONLY")
        self.assertTrue(result["counterfactual_references"])

    def test_static_subgraph_fingerprint_is_separate_from_full_result_fingerprint(self):
        request = self.lib.responsibility_subgraph_pilot_request(root=ROOT)
        first = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        second = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        self.assertEqual(first["subgraph_fingerprint"], second["subgraph_fingerprint"])
        self.assertNotEqual(first["subgraph_fingerprint"], first["result_fingerprint"])
        self.assertEqual(
            first["result_fingerprint_scope"],
            "FULL_DERIVED_RESULT_INCLUDING_FRESHNESS_METADATA",
        )

    def test_unknown_domain_and_path_fail_closed(self):
        request = self.lib.responsibility_subgraph_pilot_request(root=ROOT)
        request["domain_id"] = "UNBOUNDED_ALL_REPOSITORY"
        request["input_fingerprint"] = self.lib._responsibility_subgraph_fingerprint({
            key: value for key, value in request.items() if key != "input_fingerprint"
        })
        result = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("responsibility_subgraph_domain_unauthorized", result["errors"])

    def test_structural_delta_is_identity_only_not_semantic_deletion_verdict(self):
        request = self.lib.responsibility_subgraph_pilot_request(root=ROOT)
        result = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        delta = self.lib.responsibility_subgraph_structural_delta(result, result)
        self.assertEqual(delta["added_nodes"], [])
        self.assertEqual(delta["removed_edges"], [])
        self.assertEqual(delta["semantic_classification"], "UNCLASSIFIED")

    def test_submit_flag_slice_excludes_monolithic_main_siblings_deterministically(self):
        legacy_request = self.lib.responsibility_subgraph_pilot_request(
            root=ROOT, domain_id=self.lib.OMP_COMPLETION_SUBGRAPH_DOMAIN_ID,
        )
        legacy = self.lib.derive_responsibility_subgraph(legacy_request, root=ROOT)
        request = dict(legacy_request)
        request["entry_condition"] = "CLI_FLAG:--omp-code-optimization-submit"
        request["input_fingerprint"] = self.lib._responsibility_subgraph_fingerprint({
            key: value for key, value in request.items() if key != "input_fingerprint"
        })
        sliced = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        self.assertEqual(sliced["final_verdict"], "PASS")
        self.assertEqual(sliced["entry_condition"], request["entry_condition"])
        self.assertLess(len(sliced["nodes"]), len(legacy["nodes"]))
        self.assertLess(len(sliced["edges"]), len(legacy["edges"]))

    def test_continue_omp_change_slice_is_a_second_bounded_domain(self):
        request = self.lib.responsibility_subgraph_pilot_request(
            root=ROOT, domain_id=self.lib.OMP_CODE_OPTIMIZATION_BRIDGE_DOMAIN_ID,
        )
        request["entry_condition"] = "CLI_FLAG:--continue-omp-change"
        request["input_fingerprint"] = self.lib._responsibility_subgraph_fingerprint({
            key: value for key, value in request.items() if key != "input_fingerprint"
        })
        result = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["domain_id"], self.lib.OMP_CODE_OPTIMIZATION_BRIDGE_DOMAIN_ID)
        self.assertEqual(result["entry_condition"], request["entry_condition"])
        self.assertTrue(any(
            node.get("name") == "continue_omp_engineering_control_loop"
            for node in result["nodes"]
        ))

    def test_profile_review_and_completion_bind_exact_subgraph_without_bdp_or_cps_write(self):
        proof = self.lib.bounded_responsibility_subgraph_contract_proof(root=ROOT)
        self.assertEqual(proof["final_verdict"], "PASS")
        self.assertTrue(proof["no_bdp_mission_created"])
        self.assertTrue(proof["no_cps_effect"])
        self.assertTrue(proof["completion"]["responsibility_subgraph_binding_consumed"])


if __name__ == "__main__":
    unittest.main()
