from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_polygon_design_time_test", ROOT / "tools/v7_sync_lib.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PolygonDesignTimeEngineeringTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        cls.corpus = cls.lib.load_future_scale_scenario_corpus(root=ROOT)
        cls.scenario = next(
            row for row in cls.corpus["scenarios"]
            if row["SCENARIO_ID"] == "SINGLE_CHANNEL_FAILURE"
        )

    def design_change(self, dependencies=None, semantic=True):
        return {
            "change_id": "TEST-CHANGE-1",
            "objective": "Preserve routing safety after a product change",
            "acceptance_criteria": ["same safety invariants", "exact next frontier"],
            "changed_dependencies": dependencies or ["tools/v7-users-autoswitch"],
            "semantic_change": semantic,
            "baseline_identity": "baseline-test",
            "proposed_identity": "proposed-test",
            "allowed_semantic_changes": [],
        }

    def test_contract_reuses_existing_owners_and_fails_closed(self):
        result = self.lib.polygon_design_change_contract(self.design_change(), root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertFalse(result["new_owner"])
        self.assertFalse(result["new_runtime"])
        invalid = self.design_change(["../escape.py"])
        stopped = self.lib.polygon_design_change_contract(invalid, root=ROOT)
        self.assertEqual(stopped["final_verdict"], "STOP_SAFE")
        self.assertIn("design_change_dependency_invalid_or_duplicate", stopped["errors"])

    def test_semantic_code_change_materializes_consumed_frontier(self):
        result = self.lib.compile_polygon_design_change(
            self.design_change(), self.cps, root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertTrue(result["obligations"])
        self.assertEqual(result["consumer_result"]["consumer"], "OMP_PROGRAM_EXECUTION_RECONCILIATION")
        self.assertTrue(result["consumer_result"]["consumed"])
        self.assertTrue(result["next_output"].startswith("EXECUTE_BASELINE_PROPOSED:"))

    def test_documentation_change_is_explicitly_retired(self):
        result = self.lib.compile_polygon_design_change(
            self.design_change(["docs/programs/example.md"], semantic=False),
            self.cps, root=ROOT,
        )
        self.assertEqual(result["decision"], "NO_EXECUTION_NON_SEMANTIC_CHANGE")
        self.assertEqual(result["consumer_result"]["behavior_change"], "NON_SEMANTIC_CHANGE_RETIRED_WITH_REASON")
        self.assertEqual(result["next_output"], "RETURN_TO_PRODUCT_PROGRAM_FRONTIER")

    def test_semantic_differential_allows_only_declared_paths(self):
        baseline = {
            "scenario_id": "X", "scale": {"users": 10}, "terminal_class": "PASS",
            "failed_invariant": "NONE", "final_verdict": "PASS",
            "produced_outputs": {"planner": {"selected_moves": [], "candidate_moves": 0, "selected_count": 0}},
            "invariant_verdicts": [], "forbidden_effects": {},
            "situation_decision_trace": {"actual_terminal": "PASS", "selected_decision": "STAY"},
        }
        proposed = json.loads(json.dumps(baseline))
        proposed["produced_outputs"]["planner"]["selected_count"] = 1
        denied = self.lib.polygon_semantic_differential(baseline, proposed)
        allowed = self.lib.polygon_semantic_differential(
            baseline, proposed, allowed_changes=["selected_count"],
        )
        self.assertEqual(denied["final_verdict"], "STOP_SAFE")
        self.assertEqual(allowed["final_verdict"], "PASS")

    def test_counterexample_minimizer_preserves_same_failure(self):
        def evaluator(candidate):
            return {
                "final_verdict": "SCENARIO_MISMATCH",
                "failed_invariant": "HARD_FAILURE_OVERRIDE_SAFETY",
                "scenario_id": candidate["SCENARIO_ID"],
            }

        result = self.lib.minimize_polygon_counterexample(
            self.scenario, root=ROOT,
            expected_failed_invariant="HARD_FAILURE_OVERRIDE_SAFETY",
            evaluator=evaluator,
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertTrue(result["same_failure_preserved"])
        self.assertGreater(result["reduction"], 0)
        self.assertEqual(result["minimized_scenario"]["USER_POPULATION_PROFILE"]["users"], 1)
        self.assertEqual(result["minimized_scenario"]["CHANNEL_POPULATION_PROFILE"]["channels"], 2)

    def test_mismatch_classification_separates_polygon_and_product(self):
        harness = self.lib.classify_future_scale_mismatch("HARNESS_DEFECT")
        model = self.lib.classify_future_scale_mismatch("POLYGON_MODEL_DEFECT")
        product = self.lib.classify_future_scale_mismatch("REPRODUCIBLE_V7_REAL_SOURCE_DEFECT")
        self.assertFalse(harness["product_candidate_allowed"])
        self.assertFalse(model["product_candidate_allowed"])
        self.assertTrue(product["product_candidate_allowed"])

    def test_calibration_changes_risk_frontier(self):
        records = [
            {"record_id": str(index), "predicted": "PASS", "actual": "PASS", "confidence": 0.9, "owner_backed": True}
            for index in range(5)
        ]
        calibration = self.lib.polygon_historical_calibration(records, root=ROOT)
        risk_without_mutation = self.lib.polygon_risk_coverage(
            self.corpus["scenarios"], calibration=calibration,
        )
        risk_with_mutation = self.lib.polygon_risk_coverage(
            self.corpus["scenarios"], calibration=calibration,
            mutation_evidence=[{"detected": True} for _ in range(5)],
        )
        self.assertEqual(calibration["final_verdict"], "PASS")
        self.assertIn("mutation_detection_not_count_only", [row["criterion"] for row in risk_without_mutation["risk_obligations"]])
        self.assertNotIn("mutation_detection_not_count_only", [row["criterion"] for row in risk_with_mutation["risk_obligations"]])

    def test_protocol_fidelity_preserves_exact_high_fidelity_residuals(self):
        result = self.lib.polygon_protocol_tunnel_fidelity_contract(root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertFalse(result["global_real_world_limit"])
        self.assertIn("WIREGUARD_AMNEZIAWG", result["protocol_criteria"])
        self.assertIn("OPENVPN", result["protocol_criteria"])
        self.assertIn("VLESS_XRAY", result["protocol_criteria"])

    def test_bounded_repair_does_not_promote_certification_seam(self):
        result = self.lib.certify_polygon_bounded_source_repair_path(root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertTrue(result["automation_path_certified"])
        self.assertFalse(result["real_product_repair_closed"])
        self.assertEqual(result["evidence_class"], "AUTOMATION_PATH_CERTIFICATION_EVIDENCE")

    def test_cli_real_caller_consumes_and_produces_next_frontier(self):
        completed = subprocess.run(
            [str(ROOT / "tools/v7-truth-check"), "--omp-polygon-design-time", "--json"],
            cwd=ROOT, text=True, capture_output=True, check=False, timeout=600,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["real_consumer"], "OMP_PROGRAM_EXECUTION_RECONCILIATION")
        self.assertEqual(result["scenario_campaign"]["affected_scenario_count"], 62)
        self.assertEqual(result["scenario_campaign"]["consumed_scenario_count"], 62)
        self.assertTrue(result["scenario_campaign"]["coverage_restored"])
        self.assertTrue(result["scenario_campaign"]["final_frontier"]["FRONTIER_EXHAUSTED"])
        self.assertTrue(result["next_output"])

    def test_cps_deployment_frontier_is_atomic_and_preserves_product_wip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            report_path = root / "docs/reports/engineering/mission.md"
            cps_path.parent.mkdir(parents=True)
            report_path.parent.mkdir(parents=True)
            cps_path.write_text(self.cps, encoding="utf-8")
            report_path.write_text(
                "Mission ID: `V7_PERMANENT_POLYGON_RISK_COVERAGE_AND_FEEDBACK_GENERATION_V1`\n"
                "Run Nonce: `V7_PPDT_TEST_STAGE`\n",
                encoding="utf-8",
            )
            result = self.lib.stage_permanent_polygon_design_time_deployment_frontier(
                report_path="docs/reports/engineering/mission.md", root=root,
            )
            self.assertEqual(result["final_verdict"], "PASS", result.get("errors"))
            live = self.lib._normalized_state_from_live_cps(cps_path.read_text(encoding="utf-8"))
            self.assertEqual(live["active_program"], "PERMANENT_POLYGON_DESIGN_TIME_ENGINEERING_COMPLETION_PROGRAM")
            self.assertEqual(live["global_engineering_stop"], "NONE")
            self.assertIn("CAP-U07", live["protected_capability_wip"])
            self.assertEqual(live["production_maturity_change_status"], "NONE")

    def test_m8_finalization_requires_all_real_evidence_and_preserves_state_on_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            report_path = root / "docs/reports/engineering/m8.md"
            cps_path.parent.mkdir(parents=True)
            report_path.parent.mkdir(parents=True)
            cps_path.write_text(self.cps, encoding="utf-8")
            report_path.write_text(
                "Mission ID: `V7_PERMANENT_POLYGON_DESIGN_TIME_CI_DEPLOY_AND_E2E_CERTIFICATION_V1`\n"
                "Run Nonce: `V7_PPDT_M8_TEST`\n",
                encoding="utf-8",
            )
            before = cps_path.read_text(encoding="utf-8")
            result = self.lib.finalize_permanent_polygon_design_time_deployment_certification(
                report_path="docs/reports/engineering/m8.md",
                evidence={"safe_deploy": "PASS"}, root=root,
            )
            self.assertEqual(result["final_verdict"], "STOP_SAFE")
            self.assertFalse(result["state_changed"])
            self.assertEqual(cps_path.read_text(encoding="utf-8"), before)

    def test_m8_finalization_atomically_returns_exact_residual_frontier(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            report_path = root / "docs/reports/engineering/m8.md"
            cps_path.parent.mkdir(parents=True)
            report_path.parent.mkdir(parents=True)
            cps_path.write_text(self.cps, encoding="utf-8")
            report_path.write_text(
                "Mission ID: `V7_PERMANENT_POLYGON_DESIGN_TIME_CI_DEPLOY_AND_E2E_CERTIFICATION_V1`\n"
                "Run Nonce: `V7_PPDT_M8_TEST`\n",
                encoding="utf-8",
            )
            evidence = {
                "safe_deploy": "PASS", "production_non_test_caller": "PASS",
                "omp_consumer": "PASS", "truth": "PASS", "convergence": "PASS",
                "snapshot_equality": "PASS", "deploy_commit": "a" * 40,
                "deploy_id": "deploy-test", "forbidden_effects": {},
            }
            result = self.lib.finalize_permanent_polygon_design_time_deployment_certification(
                report_path="docs/reports/engineering/m8.md", evidence=evidence, root=root,
            )
            self.assertEqual(result["final_verdict"], "PASS", result.get("errors"))
            self.assertFalse(result["target_terminal_claimed"])
            live = self.lib._normalized_state_from_live_cps(cps_path.read_text(encoding="utf-8"))
            self.assertEqual(live["current_next_action_id"], "PPDT-RISK-CALIBRATION_REPRESENTATIVE")
            self.assertEqual(live["environment_alignment_status"], "FULLY_ALIGNED")
            self.assertEqual(live["production_maturity_change_status"], "NONE")

    def test_production_layout_reuses_runtime_fingerprint_and_canonical_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory)
            corpus_artifact = runtime / "engineering/future-scale/foundation.json"
            corpus_artifact.parent.mkdir(parents=True)
            corpus_artifact.symlink_to(ROOT / self.lib.FUTURE_SCALE_SCENARIO_CORPUS_PATH)
            rows = []
            for local_path in (
                "tools/v7_sync_lib.py", "tools/v7-users-autoswitch",
                "admin_core/operator_execution_pipeline.py",
                "docs/reference/V7_RUNTIME_MODEL.md",
            ):
                rows.append({
                    "local_path": local_path,
                    "remote_path": str(ROOT / local_path),
                    "sha256": "a" * 64,
                })
            (runtime / "runtime-fingerprint.json").write_text(json.dumps({
                "schema": "v7-runtime-fingerprint/v1", "commit": "b" * 40,
                "deploy_id": "deploy-test", "critical_files": rows,
                "snapshot_subsystem": {"refresh_cli": "none", "required_files": ["none"]},
                "authority": {
                    "canonical_deploy_tool": "tools/v7-safe-deploy",
                    "canonical_status_command": "tools/v7-convergence-status",
                    "canonical_truth_gate": "tools/v7-truth-check",
                },
            }), encoding="utf-8")
            with self.lib.polygon_production_certification_layout(root=runtime) as layout:
                self.assertEqual(layout["final_verdict"], "PASS")
                self.assertEqual(layout["layout_class"], "DEPLOY_MANIFEST_MATERIALIZED_READ_ONLY_LAYOUT")
                cps = (layout["root"] / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text()
                self.assertIn("SCENARIO_COVERED_COUNT` | `64", cps)
                self.assertTrue((layout["root"] / "docs/reference/V7_RUNTIME_MODEL.md").is_file())
                repair = self.lib.certify_polygon_bounded_source_repair_path(root=layout["root"])
                self.assertEqual(repair["final_verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
