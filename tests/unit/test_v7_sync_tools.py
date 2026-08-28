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

    def test_current_cps_live_state_is_atomically_consistent(self):
        result = self.lib.current_cps_consistency(ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md")
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["status"], "ATOMIC_CPS_LIVE_STATE_CONSISTENT")
        self.assertEqual(result["errors"], [])

    def test_cps_consistency_rejects_stop_generation_and_stale_surface_divergence(self):
        cps = (ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        stop_drift = self.lib._replace_section_field(
            cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "CURRENT_STOP_CONDITION",
            "`STOP_SAFE`",
        )
        result = self.lib.cps_live_state_consistency(stop_drift)
        self.assertIn("delegated_policy_cps_stop_divergence", result["errors"])

        generation_drift = self.lib._replace_section_field(
            cps,
            "### Active Protected Work In Progress",
            "### Complete Or Locked Capability Records",
            "current_state_generation",
            "`stale_generation`",
        )
        result = self.lib.cps_live_state_consistency(generation_drift)
        self.assertIn("cps_generation_divergence", result["errors"])

        stale_surface = self.lib._replace_section_field(
            cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "CURRENT_SAFE_NEXT_ACTION",
            "`READ_ONLY_BINDING_DIAGNOSIS_ONLY`",
        )
        self.assertNotEqual(stale_surface, cps)
        result = self.lib.cps_live_state_consistency(stale_surface)
        self.assertTrue(any(item.startswith("cps_stale_live_marker:") for item in result["errors"]))

    def test_cps_consistency_rejects_current_looking_historical_heading(self):
        cps = (ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        drift = cps.replace("## 7. Historical Stop Question", "## 7. Current Stop Question", 1)
        result = self.lib.cps_live_state_consistency(drift)
        self.assertIn("cps_historical_current_looking_headings", result["errors"])

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
        restart_release = self.lib.build_release_manifest(
            branch="Updatesystem",
            commit="abc123",
            deploy_id="deploy-test-restart",
            service_restart_required=True,
        )
        self.assertTrue(restart_release["service_restart_required"])

    def test_source_scan_rejects_force_push_literal(self):
        safety = self.lib.ensure_no_unsafe_tool_body([ROOT / "tools" / "v7-safe-push"])
        self.assertEqual(safety["final_verdict"], "PASS")

    def test_approved_deploy_files_cover_runtime_package_and_perf4_dependencies(self):
        remote_paths = {item["remote_path"] for item in self.lib.APPROVED_DEPLOY_FILES}
        self.assertIn("/usr/local/bin/v7_sync_lib.py", remote_paths)
        self.assertIn("/usr/local/bin/v7-users-autoswitch", remote_paths)
        self.assertIn("/usr/local/bin/v7-user-switch", remote_paths)
        self.assertIn("/etc/systemd/system/v7-users-autoswitch.service", remote_paths)
        self.assertIn("/usr/local/bin/v7-intelligence-snapshot-refresh", remote_paths)
        self.assertIn("/usr/local/bin/v7-governed-canary-dry-run-cycle", remote_paths)
        self.assertIn("/usr/local/bin/v7-egress-diagnose", remote_paths)
        self.assertIn("/etc/systemd/system/v7-autoswitch-planner.service", remote_paths)
        self.assertIn("/etc/systemd/system/v7-service-matrix-refresh.service", remote_paths)
        self.assertIn("/usr/local/bin/v7-egress-guard", remote_paths)
        self.assertIn("/usr/local/bin/v7-egress-set-state", remote_paths)
        self.assertIn("/usr/local/bin/v7-user-desired-state", remote_paths)
        self.assertIn("/usr/local/bin/v7-user-desired-state-save", remote_paths)
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

    def test_autoswitch_timer_invokes_governed_l3_owner_not_direct_apply(self):
        service = (ROOT / "systemd" / "v7-users-autoswitch.service").read_text(encoding="utf-8")
        self.assertIn("/usr/local/bin/v7-service-matrix-refresh-all", service)
        self.assertIn("--consume-existing-service-failure-events-only", service)
        self.assertIn("--runtime-hot-path-only", service)
        self.assertNotIn("/usr/local/bin/v7-users-autoswitch --apply", service)

    def test_existing_planner_consumes_canonical_events_without_repeating_legacy_planner(self):
        service = (ROOT / "systemd/drafts/v7-autoswitch-planner.service").read_text(encoding="utf-8")
        self.assertIn("Restart=on-failure", service)
        self.assertIn("v7-service-matrix-refresh-all --consume-existing-service-failure-events-only", service)
        self.assertNotIn("v7-users-autoswitch --pre-planner-refresh=write", service)
        self.assertNotIn("v7-users-autoswitch --apply", service)

    def test_fast_event_consumer_defers_ct_m0f_certification_fallbacks(self):
        source = (ROOT / "tools" / "v7-service-matrix-refresh-all").read_text(encoding="utf-8")
        self.assertIn("DEFERRED_TO_CT_M0F_CERTIFICATION_LANE", source)
        self.assertIn("event_only_service_failure_consumer_preserves_hot_path", source)
        self.assertGreaterEqual(source.count("not event_only"), 3)

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
            snapshot = json.loads(operational.read_text(encoding="utf-8"))
            runtime_hashes = snapshot["additional_readonly_findings"]["safe_deploy_runtime_hashes"]
            self.assertIn("/usr/local/bin/v7-users-autoswitch", runtime_hashes)
            self.assertIn("sha256sum /usr/local/bin/v7-users-autoswitch", snapshot["command_results"])
            self.assertNotIn("sha256sum /usr/local/bin/admin_core/__init__.py", snapshot["command_results"])

    def test_runtime_action_guard_ready_when_aligned(self):
        status = {
            "final_verdict": "PASS",
            "local": {"commit": "abc"},
            "github": {"commit": "abc"},
            "production": {"commit": "abc"},
            "diagnosis": [],
            "deploy_delta_mismatches": [],
        }
        guard = self.lib.runtime_action_guard_for_status(status)
        self.assertEqual(guard["status"], "READY_FOR_RUNTIME_ACTION")
        self.assertTrue(guard["runtime_action_safe"])
        self.assertFalse(guard["deployment_required"])

    def test_runtime_action_guard_blocks_deployable_commit_mismatch(self):
        status = {
            "final_verdict": "NO-GO",
            "local": {"commit": "new"},
            "github": {"commit": "new"},
            "production": {"commit": "old"},
            "diagnosis": ["truth:runtime_local_commit_mismatch"],
            "deploy_delta_mismatches": [],
        }
        guard = self.lib.runtime_action_guard_for_status(
            status,
            changed_files=["tools/v7-users-autoswitch"],
        )
        self.assertEqual(guard["status"], "DEPLOY_REQUIRED")
        self.assertFalse(guard["runtime_action_safe"])
        self.assertTrue(guard["deployment_required"])

    def test_runtime_action_guard_classifies_docs_only_mismatch(self):
        status = {
            "final_verdict": "NO-GO",
            "local": {"commit": "new"},
            "github": {"commit": "new"},
            "production": {"commit": "old"},
            "diagnosis": ["truth:runtime_local_commit_mismatch"],
            "deploy_delta_mismatches": [],
        }
        guard = self.lib.runtime_action_guard_for_status(
            status,
            changed_files=[
                "PROGRAM_CANARY_EXPANSION_BRIDGE_EXECUTION_AND_SMALL_BATCH_CERTIFICATION_REPORT.md",
                "docs/reports/evidence/canary_expansion_execution_evidence/phase1_truth_check_all.json",
            ],
        )
        self.assertEqual(guard["status"], "DOCS_ONLY_MISMATCH")
        self.assertTrue(guard["runtime_action_safe"])
        self.assertTrue(guard["docs_only_mismatch"])

    def test_runtime_action_guard_blocks_unknown_change_classification(self):
        status = {
            "final_verdict": "NO-GO",
            "local": {"commit": "new"},
            "github": {"commit": "new"},
            "production": {"commit": "old"},
            "diagnosis": ["truth:runtime_local_commit_mismatch"],
            "deploy_delta_mismatches": [],
        }
        guard = self.lib.runtime_action_guard_for_status(status, changed_files=["mystery.file"])
        self.assertEqual(guard["status"], "NO_GO")
        self.assertFalse(guard["runtime_action_safe"])
        self.assertEqual(guard["safe_next_command"], "STOP_REVIEW_CHANGED_FILES")

    def test_runtime_action_guard_includes_exact_safe_deploy_command_for_admin_change(self):
        status = {
            "final_verdict": "PASS",
            "local": {"commit": "abc"},
            "github": {"commit": "abc"},
            "production": {"commit": "abc"},
            "diagnosis": [],
            "deploy_delta_mismatches": [{"name": "v7-admin-api", "matches": False}],
        }
        guard = self.lib.runtime_action_guard_for_status(status, changed_files=["admin/v7-admin-api"])
        self.assertEqual(guard["status"], "DEPLOY_REQUIRED")
        self.assertIn("--restart-admin-if-changed", guard["safe_next_command"])
        self.assertIn("DEPLOY_V7_APPROVED", guard["safe_next_command"])

    def test_safe_deploy_requires_health_restart_for_changed_health_loop(self):
        original_delta = self.lib.deploy_delta
        original_truth = self.lib.truth_check
        original_manifest = self.lib.load_manifest
        original_allowlist = self.lib.deploy_allowlist_validation
        try:
            self.lib.deploy_delta = lambda: [{
                "name": "v7-health-loop", "remote_path": "/usr/local/bin/v7-health-loop",
                "matches": False, "exists": True,
            }]
            self.lib.truth_check = lambda *args, **kwargs: {"final_verdict": "PASS"}
            self.lib.load_manifest = lambda: {"canonical_branch": self.lib.current_branch()}
            self.lib.deploy_allowlist_validation = lambda: {"final_verdict": "PASS"}
            result = self.lib.safe_deploy_plan(
                apply=True, confirm=self.lib.DEPLOY_CONFIRMATION,
                update_local_snapshot=False,
            )
        finally:
            self.lib.deploy_delta = original_delta
            self.lib.truth_check = original_truth
            self.lib.load_manifest = original_manifest
            self.lib.deploy_allowlist_validation = original_allowlist
        self.assertIn("health_loop_changed_requires_explicit_restart_flag", result["blockers"])

    def test_runtime_action_guard_exact_next_command_in_json_shape(self):
        status = {
            "final_verdict": "NO-GO",
            "local": {"commit": "new"},
            "github": {"commit": "new"},
            "production": {"commit": "old"},
            "diagnosis": ["truth:runtime_local_commit_mismatch"],
            "deploy_delta_mismatches": [],
        }
        guard = self.lib.runtime_action_guard_for_status(status, changed_files=["tools/v7-users-autoswitch"])
        self.assertEqual(
            guard["safe_next_command"],
            "tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED "
            "--update-local-snapshot --restart-admin-if-changed --json",
        )


if __name__ == "__main__":
    unittest.main()
