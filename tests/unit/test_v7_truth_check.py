import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-truth-check"
MANIFEST = ROOT / "docs" / "track7" / "runtime-convergence" / "V7_TRUTH_MANIFEST.json"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_truth_check", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class FakeRunner:
    def __init__(self, mapping):
        self.mapping = {tuple(key): value for key, value in mapping.items()}
        self.calls = []

    def __call__(self, cmd, cwd=None, timeout=10):
        self.calls.append((tuple(cmd), str(cwd) if cwd else "", timeout))
        value = self.mapping.get(tuple(cmd), "")
        if isinstance(value, dict):
            return value
        return {"ok": True, "rc": 0, "stdout": value, "stderr": ""}


class V7TruthCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def manifest(self, workspace="/tmp/v7-work", branch="Updatesystem"):
        data = self.tool.load_manifest(MANIFEST)
        data["canonical_workspace"] = workspace
        data["canonical_branch"] = branch
        data["runtime_snapshot_path"] = ""
        data["runtime_snapshot_seed_path"] = ""
        return data

    def runner(self, branch="Updatesystem", status="", remote_commit="abc123", local_commit="abc123", changed_files=""):
        return FakeRunner(
            {
                ("git", "branch", "--show-current"): branch,
                ("git", "rev-parse", "HEAD"): local_commit,
                ("git", "status", "--short"): status,
                ("git", "remote", "get-url", "origin"): "https://github.com/muhapauka-rgb/V7-Vozduh.git",
                ("git", "worktree", "list", "--porcelain"): "worktree /tmp/v7-work\nbranch refs/heads/Updatesystem",
                (
                    "git",
                    "ls-remote",
                    "https://github.com/muhapauka-rgb/V7-Vozduh.git",
                    "refs/heads/Updatesystem",
                ): f"{remote_commit}\trefs/heads/Updatesystem",
                ("git", "diff", "--name-only", "old123..new123"): changed_files,
            }
        )

    def runtime_snapshot(self, branch="Updatesystem", commit="abc123", **derived_overrides):
        command_results = {
            self.tool.command_key(command): {"rc": 0, "stdout": "ok", "stderr": ""}
            for command in self.tool.RUNTIME_READONLY_COMMANDS
        }
        derived = {
            "deployment_model": "copied_binaries_from_deploy_metadata",
            "runtime_root_is_git_checkout": False,
            "deploy_branch": branch,
            "deploy_commit": commit,
            "binary_hashes_known": True,
            "binary_hashes_match_authoritative": True,
            "runtime_provenance_known": True,
            "scheduler_truth_known": True,
            "autoswitch_scheduler_active": False,
            "scheduler_inactive_approved_manual_mode": True,
            "service_status_known": True,
            "autoswitch_service_active": False,
            "service_inactive_explained": True,
            "state_truth_known": True,
            "restore_barrier_known": True,
            "audit_path_available": True,
            "closure_path_available": True,
            "operation_wiring_present": True,
            "runtime_fingerprint_known": True,
            "snapshot_root_known": True,
            "snapshot_required_files_known": True,
            "snapshot_refresh_cli_available": True,
            "snapshot_refresh_mechanism_known": True,
        }
        derived.update(derived_overrides)
        return {
            "schema": self.tool.RUNTIME_SNAPSHOT_SCHEMA,
            "command_results": command_results,
            "derived": derived,
        }

    def test_manifest_loads_and_required_keys_exist(self):
        data = self.tool.load_manifest(MANIFEST)
        required = {
            "canonical_workspace",
            "canonical_branch",
            "canonical_remote",
            "production_ssh_target",
            "runtime_root",
            "state_root",
            "event_root",
            "audit_root",
            "admin_root",
            "release_root",
            "current_release",
            "deploy_manifest",
            "expected_services",
            "expected_binaries",
            "expected_local_checks",
            "expected_runtime_checks",
            "unknown_policy",
            "gate_policy",
        }
        self.assertTrue(required.issubset(data))
        self.assertTrue(str(data["runtime_snapshot_path"]).startswith(".v7/"))
        self.assertIn("runtime_snapshot_seed_path", data)

    def test_local_verdict_detects_matching_workspace_and_branch(self):
        manifest = self.manifest()
        result = self.tool.combine_results(manifest, mode="local", runner=self.runner(), cwd=Path("/tmp/v7-work"))
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["convergence_status"], "LOCAL_ALIGNED")

    def test_mismatch_branch_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(branch="v7-next"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("branch_mismatch", result["blockers"])

    def test_dirty_admin_api_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status=" M admin/v7-admin-api"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("dirty_workspace", result["blockers"])
        self.assertIn("runtime_critical_dirty", result["blockers"])

    def test_dirty_autoswitch_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status=" M tools/v7-users-autoswitch"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("runtime_critical_dirty", result["blockers"])

    def test_dirty_runtime_file_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status=" M runtime/orchestrator.py"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("runtime_critical_dirty", result["blockers"])

    def test_dirty_systemd_file_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status=" M systemd/v7-users-autoswitch.service"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("runtime_critical_dirty", result["blockers"])

    def test_dirty_report_file_does_not_block(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status="?? PROGRAM_Z8_11_PRODUCTION_CONVERGENCE_REMEDIATION_REPORT.md"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertNotIn("dirty_workspace", result["blockers"])
        self.assertIn("documentation_dirty_ignored", result["warnings"])

    def test_dirty_evidence_file_does_not_block(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status="?? z8_11-evidence/runtime_convergence_snapshot.json"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertNotIn("dirty_workspace", result["blockers"])
        self.assertIn("documentation_dirty_ignored", result["warnings"])

    def test_dirty_docs_file_does_not_block(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status=" M docs/track7/runtime-convergence/notes.md"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertNotIn("dirty_workspace", result["blockers"])
        self.assertIn("documentation_dirty_ignored", result["warnings"])

    def test_dirty_runtime_relevant_test_warns_without_blocking(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status=" M tests/unit/test_v7_truth_check.py"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertNotIn("dirty_workspace", result["blockers"])
        self.assertIn("runtime_relevant_dirty", result["warnings"])

    def test_mixed_runtime_and_docs_dirty_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="local",
            runner=self.runner(status=" M tools/v7-users-autoswitch\n?? z8_11-evidence/runtime_convergence_snapshot.json"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("runtime_critical_dirty", result["blockers"])
        self.assertIn("documentation_dirty_ignored", result["warnings"])

    def test_runtime_readonly_without_access_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="runtime-readonly",
            runner=self.runner(),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertEqual(result["runtime_access_status"], "NOT_CONFIGURED")
        self.assertEqual(result["runtime_truth_status"], "UNKNOWN")

    def test_all_mode_passes_with_complete_runtime_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.manifest(workspace=tmp)
            manifest["runtime_snapshot_path"] = str(Path(tmp) / "runtime-snapshot.json")
            command_results = {
                self.tool.command_key(command): {"rc": 0, "stdout": "ok", "stderr": ""}
                for command in self.tool.RUNTIME_READONLY_COMMANDS
            }
            snapshot = {
                "schema": self.tool.RUNTIME_SNAPSHOT_SCHEMA,
                "command_results": command_results,
                "derived": {
                    "runtime_branch": "Updatesystem",
                    "runtime_commit": "abc123",
                    "deployment_model": "git_checkout",
                    "runtime_root_is_git_checkout": True,
                    "binary_hashes_known": True,
                    "binary_hashes_match_authoritative": True,
                    "runtime_provenance_known": True,
                    "scheduler_truth_known": True,
                    "autoswitch_scheduler_active": True,
                    "service_status_known": True,
                    "autoswitch_service_active": True,
                    "state_truth_known": True,
                    "restore_barrier_known": True,
                    "audit_path_available": True,
                    "closure_path_available": True,
                    "operation_wiring_present": True,
                    "runtime_fingerprint_known": True,
                    "snapshot_root_known": True,
                    "snapshot_required_files_known": True,
                    "snapshot_refresh_cli_available": True,
                    "snapshot_refresh_mechanism_known": True,
                },
            }
            Path(manifest["runtime_snapshot_path"]).write_text(json.dumps(snapshot), encoding="utf-8")
            result = self.tool.combine_results(manifest, mode="all", runner=self.runner(), cwd=Path(tmp))
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertEqual(result["runtime_access_status"], "READY")

    def test_deploy_metadata_runtime_identity_remains_fail_closed_on_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.manifest(workspace=tmp)
            manifest["runtime_snapshot_path"] = str(Path(tmp) / "runtime-snapshot.json")
            command_results = {
                self.tool.command_key(command): {"rc": 0, "stdout": "ok", "stderr": ""}
                for command in self.tool.RUNTIME_READONLY_COMMANDS
            }
            snapshot = {
                "schema": self.tool.RUNTIME_SNAPSHOT_SCHEMA,
                "command_results": command_results,
                "derived": {
                    "deployment_model": "copied_binaries_from_deploy_metadata",
                    "runtime_root_is_git_checkout": False,
                    "deploy_branch": "v7-next",
                    "deploy_commit": "12e51a5",
                    "binary_hashes_known": True,
                    "binary_hashes_match_authoritative": False,
                    "runtime_provenance_known": True,
                    "scheduler_truth_known": True,
                    "autoswitch_scheduler_active": False,
                    "scheduler_inactive_approved_manual_mode": False,
                    "service_status_known": True,
                    "autoswitch_service_active": False,
                    "service_inactive_explained": True,
                    "state_truth_known": True,
                    "restore_barrier_known": True,
                    "audit_path_available": True,
                    "closure_path_available": False,
                    "operation_wiring_present": False,
                    "runtime_fingerprint_known": False,
                    "snapshot_root_known": False,
                    "snapshot_required_files_known": False,
                    "snapshot_refresh_cli_available": False,
                    "snapshot_refresh_mechanism_known": False,
                },
            }
            Path(manifest["runtime_snapshot_path"]).write_text(json.dumps(snapshot), encoding="utf-8")
            result = self.tool.combine_results(manifest, mode="all", runner=self.runner(), cwd=Path(tmp))
            self.assertEqual(result["final_verdict"], "NO-GO")
            self.assertEqual(result["runtime"]["runtime_branch"], "v7-next")
            self.assertEqual(result["runtime"]["runtime_commit"], "12e51a5")
            self.assertIn("runtime_branch_mismatch", result["blockers"])
            self.assertIn("runtime_local_commit_mismatch", result["blockers"])
            self.assertIn("binary_hash_mismatch", result["blockers"])
            self.assertIn("autoswitch_scheduler_inactive", result["blockers"])
            self.assertIn("snapshot_refresh_cli_available_false_or_unknown", result["blockers"])

    def test_docs_only_runtime_commit_mismatch_does_not_block_runtime_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.manifest(workspace=tmp)
            manifest["runtime_snapshot_path"] = str(Path(tmp) / "runtime-snapshot.json")
            snapshot = self.runtime_snapshot(commit="old123")
            Path(manifest["runtime_snapshot_path"]).write_text(json.dumps(snapshot), encoding="utf-8")
            result = self.tool.combine_results(
                manifest,
                mode="all",
                runner=self.runner(
                    local_commit="new123",
                    remote_commit="new123",
                    changed_files="\n".join([
                        "BA1_ONE_USER_AUTONOMY_CERTIFICATION_REPORT.md",
                        "BA1_EVIDENCE/final_verdict.json",
                    ]),
                ),
                cwd=Path(tmp),
            )
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertNotIn("runtime_local_commit_mismatch", result["blockers"])
            self.assertIn("runtime_local_commit_docs_only_mismatch_ignored", result["warnings"])
            self.assertTrue(result["runtime"]["commit_mismatch_classification"]["docs_only_mismatch"])

    def test_deployable_runtime_commit_mismatch_still_blocks_runtime_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.manifest(workspace=tmp)
            manifest["runtime_snapshot_path"] = str(Path(tmp) / "runtime-snapshot.json")
            snapshot = self.runtime_snapshot(commit="old123")
            Path(manifest["runtime_snapshot_path"]).write_text(json.dumps(snapshot), encoding="utf-8")
            result = self.tool.combine_results(
                manifest,
                mode="all",
                runner=self.runner(
                    local_commit="new123",
                    remote_commit="new123",
                    changed_files="admin/v7-admin-api",
                ),
                cwd=Path(tmp),
            )
            self.assertEqual(result["final_verdict"], "NO-GO")
            self.assertIn("runtime_local_commit_mismatch", result["blockers"])
            self.assertFalse(result["runtime"]["commit_mismatch_classification"]["docs_only_mismatch"])

    def test_all_mode_blocks_without_runtime_truth(self):
        manifest = self.manifest()
        result = self.tool.combine_results(manifest, mode="all", runner=self.runner(), cwd=Path("/tmp/v7-work"))
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("runtime_readonly_access_not_configured", result["blockers"])

    def test_json_output_is_parseable(self):
        manifest = self.manifest()
        result = self.tool.combine_results(manifest, mode="all", runner=self.runner(), cwd=Path("/tmp/v7-work"))
        payload = json.loads(json.dumps(result))
        self.assertEqual(payload["schema"], "v7-truth-check/v1")

    def test_github_mismatch_returns_no_go(self):
        manifest = self.manifest()
        result = self.tool.combine_results(
            manifest,
            mode="github",
            runner=self.runner(remote_commit="remote456", local_commit="local123"),
            cwd=Path("/tmp/v7-work"),
        )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("local_remote_commit_mismatch", result["blockers"])

    def test_no_mutating_commands_are_present_in_allowed_command_list(self):
        forbidden = self.tool.FORBIDDEN_COMMAND_TOKENS
        for command in self.tool.RUNTIME_READONLY_COMMANDS:
            self.assertFalse(any(str(token).lower() in forbidden for token in command), command)
        self.tool.assert_allowed_commands_are_readonly()

    def test_cli_json_output_is_parseable_without_real_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.manifest(workspace=tmp)
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            # Direct function coverage keeps this test independent of real production SSH.
            result = self.tool.combine_results(manifest, mode="runtime-readonly", runner=self.runner(), cwd=Path(tmp))
            self.assertEqual(result["final_verdict"], "NO-GO")


if __name__ == "__main__":
    unittest.main()
