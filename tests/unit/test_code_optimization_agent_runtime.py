from __future__ import annotations

import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load_bundle_module():
    path = ROOT / "tools/v7-code-optimization-bundle"
    loader = importlib.machinery.SourceFileLoader("v7_code_optimization_bundle", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CodeOptimizationAgentRuntimeAcceptanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = load_bundle_module()

    def write_run(self, root: Path, manifest: dict, checkpoint: dict):
        manifest_sha = self.bundle._write_json(root / "run-manifest.json", manifest)
        checkpoint["manifest_sha256"] = manifest_sha
        self.bundle._write_checkpoint(root, checkpoint)

    def ingest_fixture(self, root: Path):
        packet = {
            "domain_id": "ONE", "packet_fingerprint": "1" * 64,
            "required_reviews": sorted(self.bundle.REVIEW_ASPECTS),
            "subgraph_result": {
                "domain_id": "ONE", "repo_fingerprint": "R",
                "subgraph_fingerprint": "S", "result_fingerprint": "SR",
                "generated_at": "2026-01-01T00:00:00+00:00",
                "expires_at": "2027-01-01T00:00:00+00:00",
            },
            "profile_contract": {
                "output_schema": "v7.test-output.v1", "profile_type": "CODE_OPTIMIZATION",
                "profile_version": "1", "mission_id": "M", "run_nonce": "N",
                "input_fingerprint": "I", "repo_fingerprint": "R",
                "profile_fingerprint": "P", "mission_intent_fingerprint": "MI",
            },
        }
        manifest = {
            "schema": self.bundle.RUN_MANIFEST_SCHEMA,
            "snapshot": {"base_commit": "head", "worktree_fingerprint": "tree", "system_map_sha256": "MISSING", "source_fingerprints": {}},
            "ordered_domain_ids": ["ONE"], "packets_by_domain": {"ONE": packet},
        }
        self.write_run(root, manifest, {
            "schema": self.bundle.RUN_CHECKPOINT_SCHEMA, "current_domain_index": 0,
            "current_domain_id": "ONE", "completed_domains": [], "review_attempt": 0,
        })
        analyst = {field: [] for field in self.bundle.sync_lib.CODE_OPTIMIZATION_OUTPUT_FIELDS}
        analyst.update({
            "mission_reference": "M", "profile_reference": "P", "input_fingerprint": "I",
            "domain_id": "ONE", "responsibility_subgraph": dict(packet["subgraph_result"]), "canonical_to_be_references": [],
            "structural_baseline": {}, "responsibility_classifications": [],
            "semantic_necessity_classifications": [], "counterfactual_hypotheses": [],
            "ranked_candidates": [], "selected_first_candidate": None,
            "owner_decision_required": False, "unproven_edges": [], "unproven_claims": [],
            "terminal_verdict": "NO_SAFE_COUNTERFACTUAL_CANDIDATE",
            "symbol_evidence": [], "counterfactual_attempts": [], "considered_mechanisms": [],
        })
        analyst_path = root / "analyst.json"
        analyst_path.write_text(json.dumps(analyst, sort_keys=True), encoding="utf-8")
        analyst_hash = self.bundle._sha(analyst_path.read_bytes())
        reviewer = {
            "schema": "v7.code-optimization-reviewer-output.v1",
            "analyst_payload_hash": analyst_hash,
            "sections": {name: {"reason": "bounded", "evidence": ["fixture"]} for name in self.bundle.REVIEW_ASPECTS},
            "verdict": "PASS", "rejected_candidate_ids": [], "rejection_reasons": [],
        }
        reviewer_path = root / "reviewer.json"
        reviewer_path.write_text(json.dumps(reviewer, sort_keys=True), encoding="utf-8")
        attestation = self.bundle.orchestrator_attestation(
            manifest_fingerprint=self.bundle._json_fingerprint(manifest),
            packet_fingerprint=packet["packet_fingerprint"], analyst_payload_hash=analyst_hash,
            reviewer_payload_hash=self.bundle._sha(reviewer_path.read_bytes()),
            analyst_context_ref="/root/analyst", reviewer_context_ref="/root/reviewer",
        )
        attestation_path = root / "attestation.json"
        attestation_path.write_text(json.dumps(attestation, sort_keys=True), encoding="utf-8")
        return SimpleNamespace(
            bundle_dir=str(root), analyst=str(analyst_path), reviewer=str(reviewer_path),
            attestation=str(attestation_path), output=str(root / "result.json"),
        )

    def fixture(self, root: Path):
        packet = {"packet_fingerprint": "a" * 64, "domain_id": "OWNER_BACKED_DOMAIN"}
        authors = ["/root/native-analyst"]
        reviewers = ["/root/native-reviewer"]
        result = {
            "packet_fingerprint": packet["packet_fingerprint"],
            "native_context_manifest": {
                "roles": [{"native_agent_id": identity} for identity in authors],
            },
            "reviews": [{
                "review_verdict": "PASS",
                "native_context_proof": {"native_agent_id": identity},
            } for identity in reviewers],
        }
        consumption = {
            "final_verdict": "PASS",
            "coverage_terminal": "FULL_ACTIVE_COVERAGE",
            "final_completion": "COMPLETE_WITH_LEGAL_TERMINAL",
            "domains_completed": [packet["domain_id"]],
            "blocked_domains": [], "errors": [], "cleanup_count": 0,
            "no_cps_effect": True, "runtime_impact": "NONE",
            "production_impact": "NONE", "authority_impact": "NONE",
        }
        benchmark = {
            "schema": "v7.code-optimization-hidden-benchmark-verified.v1",
            "final_verdict": "PASS", "terminal": "REDUNDANT_LINK_PROVEN",
            "dynamic_liveness_proven": True,
            "behavior_error_state_equivalence_proven": True,
            "cleanup_count": 1, "review_context_count": 1, "fixture_only": True,
            "cps_runtime_production_authority_effect": "NONE", "errors": [],
        }
        values = {
            "prepared-packets.json": [packet], "results.json": [result],
            "consumption.json": consumption, "benchmark.json": benchmark,
        }
        for name, value in values.items():
            (root / name).write_text(json.dumps(value), encoding="utf-8")
        system_map = ROOT / "docs/reference/SYSTEM_MAP.md"
        manifest = {
            "schema": self.bundle.RUN_MANIFEST_SCHEMA,
            "snapshot": {
                "base_commit": self.bundle._git_head(),
                "worktree_fingerprint": self.bundle._product_worktree_fingerprint(),
                "system_map_sha256": self.bundle._sha(system_map.read_bytes()),
                "source_fingerprints": {},
            },
            "ordered_domain_ids": [packet["domain_id"]],
            "packets_by_domain": {packet["domain_id"]: packet},
        }
        self.write_run(root, manifest, {
            "schema": self.bundle.RUN_CHECKPOINT_SCHEMA,
            "current_domain_index": 1, "current_domain_id": None,
            "completed_domains": [{
                "domain_id": packet["domain_id"],
                "packet_fingerprint": packet["packet_fingerprint"],
                "result_fingerprint": result.get("result_fingerprint"),
                "result_artifact_fingerprint": self.bundle._json_fingerprint(result),
            }],
            "review_attempt": 0,
        })
        return SimpleNamespace(
            bundle_dir=str(root), results=str(root / "results.json"),
            consumption=str(root / "consumption.json"),
            benchmark_verification=str(root / "benchmark.json"),
            output=str(root / "acceptance.json"),
        )

    def test_joint_gate_is_the_only_full_acceptance_terminal(self):
        with tempfile.TemporaryDirectory() as directory:
            args = self.fixture(Path(directory))
            with mock.patch.object(
                self.bundle.sync_lib, "validate_code_optimization_executor_result",
                return_value=[],
            ):
                accepted = self.bundle.final_accept(args)
        self.assertEqual(accepted["final_verdict"], "PASS")
        self.assertEqual(
            accepted["terminal"],
            "V7_CODE_OPTIMIZATION_AGENT_RUNTIME_FULLY_ACCEPTED",
        )
        self.assertEqual(accepted["native_author_context_count"], 1)
        self.assertEqual(accepted["native_reviewer_context_count"], 1)

    def test_joint_gate_fails_closed_when_benchmark_is_not_proved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self.fixture(root)
            benchmark = json.loads((root / "benchmark.json").read_text(encoding="utf-8"))
            benchmark["behavior_error_state_equivalence_proven"] = False
            (root / "benchmark.json").write_text(json.dumps(benchmark), encoding="utf-8")
            with mock.patch.object(
                self.bundle.sync_lib, "validate_code_optimization_executor_result",
                return_value=[],
            ):
                rejected = self.bundle.final_accept(args)
        self.assertEqual(rejected["final_verdict"], "STOP_SAFE")
        self.assertEqual(
            rejected["terminal"],
            "STOP_SAFE_CODE_OPTIMIZATION_AGENT_RUNTIME_ACCEPTANCE_INVALID",
        )
        self.assertIn("hidden_benchmark_not_accepted", rejected["errors"])

    def test_benchmark_authorization_binds_read_only_native_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared = self.bundle.benchmark_prepare(
                SimpleNamespace(output_dir=str(root)),
            )
            self.assertEqual(prepared["final_verdict"], "PASS")
            candidate_path = root / "candidate.json"
            candidate = {
                "terminal": "REDUNDANT_LINK_PROVEN",
                "mutation_performed": False,
                "answer_disclosed_to_executor": False,
                "changed_path": "benchmark_target.py",
                "redundant_symbol": "_stabilize_envelope",
                "evidence": ["dynamic call trace and exact wrapper body"],
                "control_observables": ["outputs, errors and AUDIT state"],
                "counterfactual_observables": ["same observations without wrapper"],
                "safety_compatibility_invariants": ["same output/error/state"],
                "rollback": "restore benchmark_target.py from control fixture",
                "native_agent_id": "/root/fresh-benchmark-agent",
                "fork_turns": "none", "platform_dispatch": "spawn_agent",
            }
            candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
            authorized = self.bundle.benchmark_authorize(SimpleNamespace(
                bundle_dir=str(root), candidate=str(candidate_path),
                output=str(root / "authorization.json"),
            ))
        self.assertEqual(authorized["final_verdict"], "PASS")
        self.assertEqual(authorized["terminal"], "BENCHMARK_FIXTURE_CLEANUP_AUTHORIZED")
        self.assertEqual(authorized["candidate_native_agent_id"], candidate["native_agent_id"])

    def test_hidden_benchmark_requires_read_only_candidate_before_authorization(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared = self.bundle.benchmark_prepare(
                SimpleNamespace(output_dir=str(root)),
            )
            self.assertEqual(prepared["final_verdict"], "PASS")
            candidate = {
                "terminal": "REDUNDANT_LINK_PROVEN",
                "mutation_performed": False,
                "answer_disclosed_to_executor": False,
                "changed_path": "benchmark_target.py",
                "redundant_symbol": "_stabilize_envelope",
                "evidence": ["dynamic call observed; identity result is bypass-equivalent"],
                "control_observables": ["outputs", "errors", "AUDIT state"],
                "counterfactual_observables": ["same outputs, errors and AUDIT state"],
                "safety_compatibility_invariants": ["validation remains the owner"],
                "rollback": "restore target_before_sha256",
                "native_agent_id": "/root/benchmark-agent",
                "fork_turns": "none",
                "platform_dispatch": "spawn_agent",
            }
            candidate_path = root / "candidate.json"
            candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
            authorized = self.bundle.benchmark_authorize(SimpleNamespace(
                bundle_dir=str(root), candidate=str(candidate_path),
                output=str(root / "authorization.json"),
            ))
        self.assertEqual(authorized["final_verdict"], "PASS")
        self.assertEqual(
            authorized["terminal"], "BENCHMARK_FIXTURE_CLEANUP_AUTHORIZED",
        )

    def test_hidden_benchmark_rejects_pre_authorization_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.bundle.benchmark_prepare(SimpleNamespace(output_dir=str(root)))
            candidate = {
                "terminal": "REDUNDANT_LINK_PROVEN", "mutation_performed": False,
                "answer_disclosed_to_executor": False,
                "changed_path": "benchmark_target.py",
                "redundant_symbol": "_stabilize_envelope",
                "evidence": ["bounded proof"], "control_observables": ["outputs"],
                "counterfactual_observables": ["outputs"],
                "safety_compatibility_invariants": ["validation retained"],
                "rollback": "restore target", "native_agent_id": "/root/benchmark-agent",
                "fork_turns": "none", "platform_dispatch": "spawn_agent",
            }
            candidate_path = root / "candidate.json"
            candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
            target = root / "fixture" / "benchmark_target.py"
            target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            rejected = self.bundle.benchmark_authorize(SimpleNamespace(
                bundle_dir=str(root), candidate=str(candidate_path),
                output=str(root / "authorization.json"),
            ))
        self.assertEqual(rejected["final_verdict"], "STOP_SAFE")
        self.assertIn(
            "benchmark_candidate_mutated_fixture_before_authorization",
            rejected["errors"],
        )

    def test_product_fingerprint_detects_content_change_with_same_status_class(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            tracked = root / "already-dirty.txt"
            tracked.write_text("base", encoding="utf-8")
            subprocess.run(["git", "add", "already-dirty.txt"], cwd=root, check=True)
            tracked.write_text("first dirty content", encoding="utf-8")
            with mock.patch.object(self.bundle, "ROOT", root):
                first = self.bundle._product_worktree_fingerprint()
                tracked.write_text("second dirty content", encoding="utf-8")
                second = self.bundle._product_worktree_fingerprint()
        self.assertNotEqual(first, second)

    def test_run_manifest_fails_closed_on_snapshot_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {
                "schema": self.bundle.RUN_MANIFEST_SCHEMA,
                "snapshot": {
                    "base_commit": "expected", "worktree_fingerprint": "expected",
                    "system_map_sha256": "MISSING", "source_fingerprints": {},
                },
            }
            checkpoint = {"schema": self.bundle.RUN_CHECKPOINT_SCHEMA}
            self.write_run(root, manifest, checkpoint)
            with mock.patch.object(self.bundle, "_git_head", return_value="changed"), mock.patch.object(
                self.bundle, "_product_worktree_fingerprint", return_value="expected"
            ), mock.patch.object(self.bundle, "ROOT", root):
                _, failure = self.bundle._verify_run_manifest(root)
        self.assertEqual(failure["terminal"], "STOP_SAFE_CODE_OPTIMIZATION_RUN_SNAPSHOT_DRIFT")
        self.assertIn("run_manifest_commit_drift", failure["errors"])

    def test_checkpoint_advances_exactly_one_domain(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = {"domain_id": "ONE", "packet_fingerprint": "1" * 64}
            second = {"domain_id": "TWO", "packet_fingerprint": "2" * 64}
            manifest = {
                "schema": self.bundle.RUN_MANIFEST_SCHEMA,
                "snapshot": {"base_commit": "head", "worktree_fingerprint": "tree", "system_map_sha256": "MISSING", "source_fingerprints": {}},
                "ordered_domain_ids": ["ONE", "TWO"],
                "packets_by_domain": {"ONE": first, "TWO": second},
            }
            checkpoint = {"schema": self.bundle.RUN_CHECKPOINT_SCHEMA, "current_domain_index": 0, "current_domain_id": "ONE", "completed_domains": [], "review_attempt": 0}
            self.write_run(root, manifest, checkpoint)
            (root / "result.json").write_text(json.dumps([{"packet_fingerprint": first["packet_fingerprint"], "reviews": []}]), encoding="utf-8")
            with mock.patch.object(self.bundle, "ROOT", root), mock.patch.object(self.bundle, "_git_head", return_value="head"), mock.patch.object(self.bundle, "_product_worktree_fingerprint", return_value="tree"), mock.patch.object(self.bundle, "_structural_native_receipt_errors", return_value=[]), mock.patch.object(self.bundle.sync_lib, "validate_code_optimization_executor_result", return_value=[]):
                result = self.bundle.checkpoint(SimpleNamespace(bundle_dir=str(root), results=str(root / "result.json"), output=str(root / "output.json")))
        self.assertEqual(result["terminal"], "NEXT_DOMAIN_PREPARED")
        self.assertEqual(result["current_domain_id"], "TWO")

    def test_checkpoint_rejects_missing_structural_agent_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = {"domain_id": "ONE", "packet_fingerprint": "1" * 64}
            self.write_run(
                root,
                {"schema": self.bundle.RUN_MANIFEST_SCHEMA, "snapshot": {"base_commit": "head", "worktree_fingerprint": "tree", "system_map_sha256": "MISSING", "source_fingerprints": {}}, "ordered_domain_ids": ["ONE"], "packets_by_domain": {"ONE": packet}},
                {"schema": self.bundle.RUN_CHECKPOINT_SCHEMA, "current_domain_index": 0, "current_domain_id": "ONE", "completed_domains": [], "review_attempt": 0},
            )
            (root / "result.json").write_text(json.dumps([{"packet_fingerprint": packet["packet_fingerprint"], "executor_context_id": "invented-id"}]), encoding="utf-8")
            with mock.patch.object(self.bundle, "ROOT", root), mock.patch.object(self.bundle, "_git_head", return_value="head"), mock.patch.object(self.bundle, "_product_worktree_fingerprint", return_value="tree"):
                result = self.bundle.checkpoint(SimpleNamespace(bundle_dir=str(root), results=str(root / "result.json"), output=str(root / "output.json")))
        self.assertEqual(result["terminal"], "STOP_SAFE_CODE_OPTIMIZATION_CURRENT_RESULT_INVALID")
        self.assertIn("native_analyst_receipt_missing", result["errors"])

    def test_ingest_domain_binds_external_artifacts_without_python_provenance_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self.ingest_fixture(root)
            with mock.patch.object(self.bundle, "ROOT", root), mock.patch.object(
                self.bundle, "_git_head", return_value="head"
            ), mock.patch.object(self.bundle, "_product_worktree_fingerprint", return_value="tree"):
                result = self.bundle.ingest_domain(args)
        self.assertEqual(result["terminal"], "CURRENT_DOMAIN_ARTIFACTS_INGESTED")
        self.assertFalse(result["provenance_verified_by_python"])
        self.assertEqual(result["provenance_level"], "ORCHESTRATOR_OBSERVED_NOT_CRYPTOGRAPHIC")

    def test_ingest_domain_rejects_reviewer_analyst_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self.ingest_fixture(root)
            reviewer = json.loads(Path(args.reviewer).read_text(encoding="utf-8"))
            reviewer["analyst_payload_hash"] = "0" * 64
            Path(args.reviewer).write_text(json.dumps(reviewer, sort_keys=True), encoding="utf-8")
            with mock.patch.object(self.bundle, "ROOT", root), mock.patch.object(
                self.bundle, "_git_head", return_value="head"
            ), mock.patch.object(self.bundle, "_product_worktree_fingerprint", return_value="tree"):
                result = self.bundle.ingest_domain(args)
        self.assertEqual(result["terminal"], "STOP_SAFE_INVALID_NATIVE_AGENT_OUTPUT")
        self.assertIn("reviewer_analyst_hash_mismatch", result["errors"])


if __name__ == "__main__":
    unittest.main()
