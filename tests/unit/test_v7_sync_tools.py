import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_under_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeRunner:
    def __init__(self, mapping=None):
        self.mapping = {tuple(key): value for key, value in (mapping or {}).items()}
        self.calls = []

    def __call__(self, cmd, cwd=None, timeout=10):
        self.calls.append(tuple(cmd))
        value = self.mapping.get(tuple(cmd))
        if isinstance(value, dict):
            return value
        if value is None:
            return {"ok": True, "rc": 0, "stdout": "", "stderr": ""}
        return {"ok": True, "rc": 0, "stdout": value, "stderr": ""}


class V7SyncToolsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def test_commit_refuses_runtime_critical_dirty_without_explicit_allowance(self):
        dirty = self.lib.classify_status(" M tools/v7-users-autoswitch")
        self.assertTrue(self.lib.dirty_requires_runtime_approval(dirty))

    def test_commit_allows_documentation_only_dirty_as_non_blocking_category(self):
        dirty = self.lib.classify_status("?? PROGRAM_Z8_14_AUTOMATED_SOURCE_TO_PRODUCTION_SYNC_REPORT.md")
        self.assertFalse(self.lib.dirty_requires_runtime_approval(dirty))
        self.assertTrue(dirty["documentation_only"])

    def test_push_rejects_force_style_arguments(self):
        blockers = self.lib.reject_forbidden_args(["--apply", "--force-with-lease"])
        self.assertIn("forbidden_arg:--force-with-lease", blockers)

    def test_deploy_manifest_contains_backup_and_safety_truth(self):
        manifest = self.lib.build_deploy_manifest(branch="Updatesystem", commit="abc123", deploy_id="deploy-test")
        self.assertEqual(manifest["deploy_branch"], "Updatesystem")
        self.assertEqual(manifest["deploy_commit"], "abc123")
        self.assertTrue(manifest["approved_deploy_files"])
        self.assertFalse(manifest["safety"]["autoswitch_apply_executed"])
        self.assertFalse(manifest["safety"]["restore_barrier_modified"])

    def test_runtime_linkage_marks_copied_binary_model(self):
        linkage = self.lib.build_runtime_linkage(branch="Updatesystem", commit="abc123", deploy_id="deploy-test")
        self.assertFalse(linkage["runtime_root_is_git_checkout"])
        self.assertEqual(linkage["deploy_branch"], "Updatesystem")
        self.assertEqual(linkage["deploy_commit"], "abc123")

    def test_release_manifest_requires_rollback_manifest(self):
        release = self.lib.build_release_manifest(branch="Updatesystem", commit="abc123", deploy_id="deploy-test")
        self.assertTrue(release["rollback_manifest_required"])
        self.assertFalse(release["service_restart_required"])

    def test_source_scan_rejects_force_push_literal(self):
        safety = self.lib.ensure_no_unsafe_tool_body([ROOT / "tools" / "v7-safe-push"])
        self.assertEqual(safety["final_verdict"], "PASS")

    def test_approved_deploy_files_cover_runtime_package_and_perf4_dependencies(self):
        remote_paths = {item["remote_path"] for item in self.lib.APPROVED_DEPLOY_FILES}
        self.assertIn("/usr/local/bin/v7-users-autoswitch", remote_paths)
        self.assertIn("/usr/local/bin/v7-intelligence-snapshot-refresh", remote_paths)
        self.assertIn("/etc/systemd/system/v7-autoswitch-planner.service", remote_paths)
        self.assertIn("/usr/local/bin/admin_core/intelligence_snapshots.py", remote_paths)
        self.assertIn("/usr/local/bin/admin_core/intelligence_workers.py", remote_paths)
        self.assertIn("/usr/local/bin/admin_core/intelligence_platform.py", remote_paths)
        self.assertIn("/usr/local/bin/admin_core/routing_intelligence.py", remote_paths)

    def test_deploy_allowlist_validation_detects_missing_runtime_imports(self):
        validation = self.lib.deploy_allowlist_validation()
        self.assertEqual(validation["final_verdict"], "PASS")
        self.assertFalse(validation["missing_required_paths"])
        self.assertIn("admin_core/intelligence_snapshots.py", validation["approved_local_paths"])
        self.assertIn("admin_core/intelligence_platform.py", validation["approved_local_paths"])

    def test_deploy_manifest_contains_runtime_fingerprint(self):
        manifest = self.lib.build_deploy_manifest(branch="Updatesystem", commit="abc123", deploy_id="deploy-test")
        self.assertEqual(manifest["allowlist_validation"]["final_verdict"], "PASS")
        self.assertEqual(manifest["runtime_fingerprint"]["schema"], "v7-runtime-fingerprint/v1")
        self.assertEqual(manifest["runtime_fingerprint_validation"]["final_verdict"], "PASS")
        self.assertIn("snapshot_subsystem", manifest["runtime_fingerprint"])
        self.assertIn("v7-autoswitch-planner.service", manifest["runtime_fingerprint"]["systemd_units"])

    def test_runtime_fingerprint_validation_fails_closed(self):
        result = self.lib.validate_runtime_fingerprint({"schema": "bad"})
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("schema_mismatch", result["errors"])

    def test_convergence_status_exposes_single_operator_view(self):
        status = self.lib.convergence_status(runner=FakeRunner())
        self.assertEqual(status["schema"], "v7-convergence-status/v1")
        self.assertIn("local", status)
        self.assertIn("github", status)
        self.assertIn("production", status)
        self.assertEqual(status["canonical_truth_model"]["canonical_truth_gate"], "tools/v7-truth-check")

    def test_deploy_delta_reports_match_field_for_each_binary(self):
        delta = self.lib.deploy_delta()
        names = {item["name"] for item in delta}
        self.assertIn("v7-users-autoswitch", names)
        self.assertTrue(all("matches" in item for item in delta))

    def test_forbidden_runtime_tokens_are_policy_markers_not_commands(self):
        self.assertIn("autoswitch_apply", self.lib.FORBIDDEN_RUNTIME_TOKENS)
        self.assertNotIn("git_push_force", self.lib.FORBIDDEN_RUNTIME_TOKENS)

    def test_manifest_defines_production_ssh_target(self):
        manifest = self.lib.load_manifest()
        self.assertEqual(self.lib.production_ssh_target(manifest), "v7-vps")

    def test_convergence_owner_returns_single_next_action(self):
        owner = self.lib.convergence_owner_status(runner=FakeRunner())
        self.assertEqual(owner["schema"], "v7-convergence-owner/v1")
        self.assertIn("next_required_action", owner)
        self.assertIn("safe_command", owner)
        self.assertIn(owner["next_required_action"], {
            "NONE_MONITOR",
            "PUSH_CANONICAL_BRANCH",
            "RUN_APPROVED_SAFE_DEPLOY",
            "RETRY_WITH_NETWORK_ACCESS",
            "STOP_REVIEW_BLOCKERS",
        })

    def test_snapshot_update_writes_operational_path_from_seed(self):
        manifest = self.lib.load_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            operational = tmp_root / ".v7" / "runtime_convergence_snapshot.json"
            seed = tmp_root / "seed" / "runtime_convergence_snapshot.json"
            seed.parent.mkdir(parents=True)
            seed.write_text(json.dumps({
                "schema": "v7-runtime-truth-snapshot/v1",
                "command_results": {},
                "derived": {"deploy_commit": "old"},
            }), encoding="utf-8")
            patched = dict(manifest)
            patched["runtime_snapshot_path"] = str(operational)
            patched["runtime_snapshot_seed_path"] = str(seed)
            original_load_manifest = self.lib.load_manifest
            try:
                self.lib.load_manifest = lambda path=self.lib.MANIFEST_PATH: patched
                self.lib.update_snapshot_for_deploy(deploy_id="deploy-test", branch="Updatesystem", commit="new")
            finally:
                self.lib.load_manifest = original_load_manifest
            self.assertTrue(operational.exists())
            self.assertEqual(json.loads(operational.read_text(encoding="utf-8"))["derived"]["deploy_commit"], "new")
            self.assertEqual(json.loads(seed.read_text(encoding="utf-8"))["derived"]["deploy_commit"], "old")


if __name__ == "__main__":
    unittest.main()
