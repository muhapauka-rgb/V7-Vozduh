import importlib.util
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

    def test_approved_deploy_files_are_limited_to_known_runtime_binaries(self):
        remote_paths = {item["remote_path"] for item in self.lib.APPROVED_DEPLOY_FILES}
        self.assertEqual(
            remote_paths,
            {
                "/usr/local/bin/v7-users-autoswitch",
                "/usr/local/bin/v7-audit-log",
                "/usr/local/bin/v7-admin-api",
                "/usr/local/bin/v7-operator-execution-packet",
                "/usr/local/bin/admin_core/operator_execution.py",
            },
        )

    def test_deploy_delta_reports_match_field_for_each_binary(self):
        delta = self.lib.deploy_delta()
        names = {item["name"] for item in delta}
        self.assertIn("v7-users-autoswitch", names)
        self.assertTrue(all("matches" in item for item in delta))

    def test_forbidden_runtime_tokens_are_policy_markers_not_commands(self):
        self.assertIn("autoswitch_apply", self.lib.FORBIDDEN_RUNTIME_TOKENS)
        self.assertNotIn("git_push_force", self.lib.FORBIDDEN_RUNTIME_TOKENS)


if __name__ == "__main__":
    unittest.main()
