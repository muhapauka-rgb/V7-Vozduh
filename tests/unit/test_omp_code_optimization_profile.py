from __future__ import annotations

import copy
import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_sync_lib_code_optimization", ROOT / "tools/v7_sync_lib.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpCodeOptimizationProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def valid_profile(self):
        return self.lib.code_optimization_profile_contract(
            mission_id="V7_CODE_OPTIMIZATION_EXECUTION_PROFILE_AND_FIRST_DOMAIN_AUDIT_V1",
            run_nonce="code-optimization-test-run-v1",
            input_fingerprint="a" * 64,
            repo_fingerprint="b" * 64,
        )

    def test_valid_profile_is_admitted_with_two_exact_reviews(self):
        admitted = self.lib.admit_execution_profile_contract(
            self.valid_profile(),
            mission_id="V7_CODE_OPTIMIZATION_EXECUTION_PROFILE_AND_FIRST_DOMAIN_AUDIT_V1",
        )
        self.assertEqual(admitted["final_verdict"], "PASS")
        self.assertEqual(
            admitted["required_reviews"],
            ["ARCHITECTURE_REVIEW", "EVIDENCE_REVIEW"],
        )

    def test_continuous_profile_requires_all_four_independent_reviews(self):
        profile = self.lib.code_optimization_profile_contract(
            mission_id="V7_CODE_OPTIMIZATION_CONTINUOUS_ACCEPTANCE_V1",
            run_nonce="continuous-acceptance-test-v1",
            input_fingerprint="c" * 64,
            repo_fingerprint="d" * 64,
            continuous_acceptance=True,
        )
        admitted = self.lib.admit_execution_profile_contract(
            profile, mission_id=profile["mission_id"],
        )
        self.assertEqual(admitted["final_verdict"], "PASS")
        self.assertEqual(admitted["required_reviews"], [
            "ARCHITECTURE_REVIEW", "SAFETY_REGRESSION_REVIEW",
            "EVIDENCE_REVIEW", "QUALITY_COMPLEXITY_REVIEW",
        ])

    def test_material_change_bridge_uses_existing_domain_and_consumed_anti_regrowth(self):
        resolution = self.lib.code_optimization_resolve_material_change_domain(
            ["tools/v7_sync_lib.py", "tests/unit/test_omp_code_optimization_profile.py"],
        )
        self.assertEqual(resolution["final_verdict"], "PASS")
        self.assertEqual(
            resolution["domain_id"],
            self.lib.OMP_CODE_OPTIMIZATION_BRIDGE_DOMAIN_ID,
        )
        current = (ROOT / "tools/v7_sync_lib.py").read_text(encoding="utf-8")
        anti_regrowth = self.lib.code_optimization_bridge_anti_regrowth(current)
        self.assertEqual(anti_regrowth["final_verdict"], "PASS")
        self.assertTrue(anti_regrowth["existing_owner_resolver_consumed"])
        admission = self.lib.code_optimization_material_change_admission(
            ["tools/v7_sync_lib.py"], root=ROOT,
        )
        self.assertTrue(admission["eligible"])
        self.assertEqual(admission["anti_regrowth"]["final_verdict"], "PASS")
        self.assertEqual(len(admission["profile"]["required_reviews"]), 4)
        self.assertEqual(admission["subgraph"]["final_verdict"], "PASS")

    def test_controlled_recurrence_of_private_allowlist_is_detected(self):
        recurrence = """
def code_optimization_material_change_admission(changed_dependencies):
    allowed = {\"tools/v7_sync_lib.py\"}
    return set(changed_dependencies) & allowed
"""
        result = self.lib.code_optimization_bridge_anti_regrowth(recurrence)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertTrue(result["recurrence_detected"])
        self.assertTrue(result["private_allowlist_detected"])

    def test_material_change_admission_consumes_recurrence_fail_closed(self):
        recurrence = {
            "final_verdict": "STOP_SAFE", "recurrence_detected": True,
            "reason": "REMOVED_DUPLICATE_RESPONSIBILITY_MAPPING_RECURRED",
        }
        with mock.patch.object(
            self.lib, "code_optimization_bridge_anti_regrowth",
            return_value=recurrence,
        ):
            admission = self.lib.code_optimization_material_change_admission(
                ["tools/v7_sync_lib.py"], root=ROOT,
            )
        self.assertFalse(admission["eligible"])
        self.assertEqual(admission["reason"], "ANTI_REGROWTH_STOP_SAFE")
        self.assertTrue(admission["anti_regrowth"]["recurrence_detected"])

    def test_write_and_unknown_profiles_fail_closed(self):
        write_profile = self.valid_profile()
        write_profile["mutation_class"] = "SOURCE_WRITE"
        write = self.lib.admit_execution_profile_contract(
            write_profile, mission_id=write_profile["mission_id"],
        )
        self.assertEqual(write["final_verdict"], "STOP_SAFE")
        self.assertIn("execution_profile_mutation_class_unauthorized", write["errors"])

        unknown_profile = self.valid_profile()
        unknown_profile["profile_type"] = "UNBOUNDED_OPTIMIZER"
        unknown = self.lib.admit_execution_profile_contract(
            unknown_profile, mission_id=unknown_profile["mission_id"],
        )
        self.assertEqual(unknown["final_verdict"], "STOP_SAFE")
        self.assertIn("execution_profile_type_unauthorized", unknown["errors"])

    def test_current_domain_audit_revalidates_durable_spine_but_stops_without_live_evidence(self):
        request = self.lib.responsibility_subgraph_pilot_request(root=ROOT)
        subgraph = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        audit = self.lib.code_optimization_domain_audit(subgraph, root=ROOT)
        self.assertEqual(audit["terminal_verdict"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(audit["ranked_candidates"], [])
        self.assertIsNone(audit["selected_first_candidate"])
        self.assertEqual(
            audit["canonical_to_be_status"],
            "CANONICAL_DURABLE_CAUSAL_SPINE_REVALIDATED",
        )
        self.assertEqual(
            audit["canonical_causal_spine_revalidation"]["status"],
            "CANONICAL_DURABLE_CAUSAL_SPINE_REVALIDATED",
        )
        self.assertIn(
            "runtime_caller_consumer_and_s11_receipt_unproven", audit["errors"],
        )
        self.assertNotIn(
            "canonical_to_be_responsibility_spine_unproven", audit["errors"],
        )

    def test_stale_subgraph_is_rejected_by_completion_binding(self):
        proof = self.lib.bounded_code_optimization_contract_proof(root=ROOT)
        contract = {
            "EXECUTION_PROFILE_CONTRACT": proof["profile"],
            "EXECUTION_PROFILE_RESULT": proof["result"],
            "EXECUTION_PROFILE_REVIEWS": proof["reviews"],
            "RESPONSIBILITY_SUBGRAPH_RESULT": proof["subgraph"],
            "CURRENT_MISSION_ID": proof["profile"]["mission_id"],
            "CURRENT_RUN_NONCE": proof["profile"]["run_nonce"],
            "CURRENT_INPUT_FINGERPRINT": proof["profile"]["input_fingerprint"],
            "CURRENT_REPO_FINGERPRINT": proof["profile"]["repo_fingerprint"],
            "CURRENT_EVIDENCE_TIME": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
            "MISSION_CURRENT": True,
            "MISSION_SUPERSEDED": False,
            "EXPECTED_RESULT_FINGERPRINT": proof["result"]["result_fingerprint"],
            "EXISTING_RESULT_FINGERPRINTS": [],
        }
        binding = self.lib.responsibility_subgraph_completion_binding(contract)
        self.assertEqual(binding["final_verdict"], "STOP_SAFE")
        self.assertIn("responsibility_subgraph_stale_or_future", binding["errors"])

    def test_missing_evidence_review_is_rejected(self):
        proof = self.lib.bounded_code_optimization_contract_proof(root=ROOT)
        contract = {
            "MISSION_TYPE": "ACCEPTANCE", "COMPLETION_CONTRACT": "ACCEPTANCE_COMPLETION",
            "INDEPENDENT_ACCEPTANCE_PROVEN": True, "NEXT_OUTPUT_PROVEN": True,
            "EXECUTION_PROFILE_CONTRACT": proof["profile"],
            "EXECUTION_PROFILE_RESULT": proof["result"],
            "EXECUTION_PROFILE_REVIEWS": [proof["reviews"][0]],
            "RESPONSIBILITY_SUBGRAPH_RESULT": proof["subgraph"],
            "CURRENT_MISSION_ID": proof["profile"]["mission_id"],
            "CURRENT_RUN_NONCE": proof["profile"]["run_nonce"],
            "CURRENT_INPUT_FINGERPRINT": proof["profile"]["input_fingerprint"],
            "CURRENT_REPO_FINGERPRINT": proof["profile"]["repo_fingerprint"],
            "CURRENT_EVIDENCE_TIME": datetime.now(timezone.utc).isoformat(),
            "MISSION_CURRENT": True, "MISSION_SUPERSEDED": False,
            "EXPECTED_RESULT_FINGERPRINT": proof["result"]["result_fingerprint"],
            "EXISTING_RESULT_FINGERPRINTS": [],
        }
        completion = self.lib.mission_completion_evidence_gate(contract)
        errors = completion["execution_profile_binding"]["errors"]
        self.assertEqual(completion["completion_verdict"], "PREPARED_NOT_CONSUMED")
        self.assertIn("execution_profile_required_review_count_invalid:EVIDENCE_REVIEW", errors)

    def test_full_profile_proof_has_no_cps_or_runtime_effect(self):
        proof = self.lib.bounded_code_optimization_contract_proof(root=ROOT)
        self.assertEqual(proof["final_verdict"], "PASS")
        self.assertEqual(proof["selected_candidate_count"], 0)
        self.assertTrue(proof["no_cps_effect"])
        self.assertEqual(proof["runtime_impact"], "NONE")

    def test_submitted_actual_run_requires_evidence_and_accepts_honest_zero(self):
        request = self.lib.responsibility_subgraph_pilot_request(
            root=ROOT, domain_id=self.lib.OMP_COMPLETION_SUBGRAPH_DOMAIN_ID,
        )
        request.update({"mission_id": "V7_CODE_OPTIMIZATION_REAL_EXECUTION_PATH_AND_FIRST_EVIDENCE_BACKED_CANDIDATE_V1", "run_nonce": "actual-code-optimization-run-v1", "profile_id": "CODE_OPTIMIZATION"})
        request["input_fingerprint"] = self.lib._responsibility_subgraph_fingerprint({k: v for k, v in request.items() if k != "input_fingerprint"})
        subgraph = self.lib.derive_responsibility_subgraph(request, root=ROOT)
        profile = self.lib.admit_execution_profile_contract(self.lib.code_optimization_profile_contract(mission_id=request["mission_id"], run_nonce=request["run_nonce"], input_fingerprint=request["input_fingerprint"], repo_fingerprint=request["repo_fingerprint"]), mission_id=request["mission_id"])
        package = self.lib.code_optimization_evidence_package(mission_id=request["mission_id"], run_nonce=request["run_nonce"], profile=profile, subgraph=subgraph, root=ROOT)
        output = {"mission_reference": request["mission_id"], "profile_reference": profile["profile_fingerprint"], "input_fingerprint": request["input_fingerprint"], "domain_id": subgraph["domain_id"], "responsibility_subgraph": {k: subgraph[k] for k in ("domain_id", "repo_fingerprint", "subgraph_fingerprint", "result_fingerprint", "generated_at", "expires_at")}, "canonical_to_be_references": [], "structural_baseline": {}, "responsibility_classifications": [{"subject": "execution_profile_completion_binding", "classification": "SAFETY_ESSENTIAL", "evidence_item_ids": ["completion-consumer-v1"], "claim_type": "result_review_binding", "caller": "submit_code_optimization_result", "consumer": "mission_completion_evidence_gate", "behavior_state_effect": "rejects mismatched result/review", "semantic_contribution": "prevents unsafe completion", "invalidation_triggers": ["repo_fingerprint_change"]}], "semantic_necessity_classifications": [{"scope": "completion binding", "classification": "UNKNOWN"}], "counterfactual_hypotheses": [], "ranked_candidates": [], "selected_first_candidate": None, "owner_decision_required": False, "unproven_edges": [], "unproven_claims": ["runtime semantic redundancy"], "considered_mechanisms": [{"subject": "execution_profile_completion_binding", "rejection_reason": "identity and review binding is safety-essential"}], "terminal_verdict": "NO_SAFE_COUNTERFACTUAL_CANDIDATE"}
        provisional = self.lib.gpt_decision_review_result_contract(profile, output, executor_context_id="external-codex-bounded-code-optimization")
        reviews = [self.lib.execution_profile_review_record(profile, provisional, review_type="ARCHITECTURE_REVIEW", review_verdict="PASS", review_context_id="arch-review"), self.lib.execution_profile_review_record(profile, provisional, review_type="EVIDENCE_REVIEW", review_verdict="PASS", review_context_id="evidence-review")]
        run = self.lib.submit_code_optimization_result(profile=profile, subgraph=subgraph, evidence_package=package, output=output, reviews=reviews)
        self.assertEqual(run["final_verdict"], "PASS")
        package["expires_at"] = "2000-01-01T00:00:00+00:00"
        self.assertIn("code_optimization_evidence_fingerprint_mismatch", self.lib.validate_code_optimization_evidence_package(package, profile=profile, subgraph=subgraph))

    def test_full_baseline_consumes_every_currently_admitted_domain(self):
        baseline = self.lib.code_optimization_full_baseline(root=ROOT)
        self.assertEqual(baseline["final_verdict"], "PASS")
        self.assertEqual(baseline["terminal"], "CODE_OPTIMIZATION_STRUCTURAL_BASELINE_CAPTURED_INTERNAL")
        self.assertGreater(baseline["domain_count"], 3)
        self.assertTrue(baseline["no_cps_effect"])
        self.assertEqual(baseline["semantic_claim"], "NONE_STRUCTURAL_BASELINE_ONLY")
        self.assertTrue({
            self.lib.RESPONSIBILITY_SUBGRAPH_DOMAIN_ID,
            self.lib.OMP_COMPLETION_SUBGRAPH_DOMAIN_ID,
            self.lib.OMP_CODE_OPTIMIZATION_BRIDGE_DOMAIN_ID,
        }.issubset({item["domain_id"] for item in baseline["domains"]}))
        self.assertTrue(all(
            item["structural_derivation"] == "DERIVED_NO_SEMANTIC_EXECUTOR_RESULT"
            for item in baseline["domains"]
        ))

    def test_operational_campaign_requires_external_executor_before_semantic_completion(self):
        campaign = self.lib.code_optimization_operational_campaign(root=ROOT)
        self.assertEqual(campaign["final_verdict"], "CONTINUE_SAME_MISSION")
        self.assertEqual(campaign["terminal"], "SEMANTIC_EXECUTOR_REQUIRED")
        packet = campaign["pending_packets"][0]
        lifetime = (
            datetime.fromisoformat(packet["expires_at"])
            - datetime.fromisoformat(packet["generated_at"])
        )
        self.assertGreaterEqual(lifetime, timedelta(hours=5, minutes=59))
        stale = copy.deepcopy(packet)
        first_path = stale["source_paths"][0]
        stale["source_fingerprints"][first_path] = "0" * 64
        stale["packet_fingerprint"] = self.lib._execution_contract_fingerprint({
            key: value for key, value in stale.items()
            if key != "packet_fingerprint"
        })
        self.assertIn(
            f"executor_packet_source_stale:{first_path}",
            self.lib.validate_code_optimization_executor_packet(stale, root=ROOT),
        )
        self.assertEqual(campaign["intermediate_completion"], "CONTINUE_SAME_MISSION")
        self.assertGreater(len(campaign["executor_packets"]), 3)
        self.assertEqual(len(campaign["pending_packets"]), len(campaign["executor_packets"]))
        self.assertTrue(all(
            self.lib.validate_code_optimization_executor_packet(packet) == []
            for packet in campaign["executor_packets"]
        ))
        self.assertTrue(campaign["no_cps_effect"])

    def test_operational_campaign_accepts_honest_zero_or_one_cleanup_only(self):
        self.assertTrue(self.lib.code_optimization_cleanup_proof_set_valid([]))
        self.assertTrue(self.lib.code_optimization_cleanup_proof_set_valid([
            {"cleanup_id": "cleanup-proven-v1"},
        ]))
        self.assertFalse(self.lib.code_optimization_cleanup_proof_set_valid([
            {},
        ]))
        self.assertFalse(self.lib.code_optimization_cleanup_proof_set_valid([
            {"cleanup_id": "cleanup-a"}, {"cleanup_id": "cleanup-b"},
        ]))

    def test_operational_campaign_is_deterministic_and_supports_compact_scopes(self):
        first = self.lib.code_optimization_operational_campaign(root=ROOT)
        second = self.lib.code_optimization_operational_campaign(root=ROOT, mode="CONTINUE")
        self.assertEqual(first["mission_intent_fingerprint"], second["mission_intent_fingerprint"])
        domain = self.lib.code_optimization_operational_campaign(
            root=ROOT, mode="DOMAIN", domain_id=self.lib.OMP_COMPLETION_SUBGRAPH_DOMAIN_ID,
        )
        self.assertEqual(domain["selected_domain_ids"], [self.lib.OMP_COMPLETION_SUBGRAPH_DOMAIN_ID])
        self.assertEqual(domain["terminal"], "SEMANTIC_EXECUTOR_REQUIRED")
        changed = self.lib.code_optimization_operational_campaign(
            root=ROOT, mode="CHANGED", changed_dependencies=["tools/v7_sync_lib.py"],
        )
        self.assertEqual({packet["domain_id"] for packet in changed["executor_packets"]}, {
            self.lib.OMP_COMPLETION_SUBGRAPH_DOMAIN_ID,
            self.lib.OMP_CODE_OPTIMIZATION_BRIDGE_DOMAIN_ID,
        })

    def test_owner_backed_discovery_and_private_registry_recurrence(self):
        discovery = self.lib.code_optimization_discover_domains(root=ROOT)
        self.assertEqual(discovery["final_verdict"], "PASS")
        self.assertGreater(len(discovery["discovered_domains"]), 3)
        self.assertEqual(discovery["blocked_local_unknown_surfaces"], [])
        self.assertTrue(any(
            item["discovery_reason"] == "SYSTEM_MAP_CURRENT_OWNER_SURFACE"
            for item in discovery["discovered_domains"]
        ))
        self.assertFalse(discovery["duplicate_registry_created"])
        self.assertTrue(discovery["excluded_classes"])
        recurrence = """
def code_optimization_full_baseline():
    domain_specs = (\"A\", \"B\")
def code_optimization_operational_campaign():
    return None
"""
        anti = self.lib.code_optimization_operational_anti_regrowth(recurrence)
        self.assertEqual(anti["final_verdict"], "STOP_SAFE")
        self.assertTrue(anti["literal_domain_list_detected"])
        self.assertFalse(anti["owner_backed_discovery_consumed"])


if __name__ == "__main__":
    unittest.main()
