import importlib.machinery
import importlib.util
import json
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_external_baseline_heartbeat_avoids_write_when_projection_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps.parent.mkdir(parents=True)
            cps.write_text(
                "## 0. Authoritative Live Current State\n\n"
                "| Field | Current Value |\n| --- | --- |\n"
                "| `CURRENT_NEXT_ACTION_ID` | "
                "`EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED` |\n"
                "| `CONTROLLED_SOURCE_ROOT_CAUSE_CLASS` | "
                "`EXTERNAL_INFRASTRUCTURE_OR_ACCESS_REQUIRED` |\n"
                "| `EXACT_EXTERNAL_RESOURCE` | "
                "`AMNEZIAWG_REMOTE_PEER_OR_MATCHING_PROFILE_FOR_SOURCE_1` |\n"
                "| `EXACT_EXTERNAL_OWNER` | "
                "`EXTERNAL_AMNEZIAWG_PEER_OR_CREDENTIAL_PROVIDER` |\n"
                "| `EXACT_REQUIRED_INPUT` | `matching_profile` |\n\n"
                "## Authoritative Unfinished Capability Closure Registry\n",
                encoding="utf-8",
            )
            status = {
                "controlled_certification_substrate_authority": {
                    "source_precondition_status": (
                        "STOP_SAFE_SOURCE_BASELINE_UNHEALTHY"
                    ),
                    "source_baseline_health": {
                        "root_cause_class": (
                            "EXTERNAL_INFRASTRUCTURE_OR_ACCESS_REQUIRED"
                        ),
                        "exact_external_resource": (
                            "AMNEZIAWG_REMOTE_PEER_OR_MATCHING_PROFILE_FOR_SOURCE_1"
                        ),
                        "exact_external_owner": (
                            "EXTERNAL_AMNEZIAWG_PEER_OR_CREDENTIAL_PROVIDER"
                        ),
                        "exact_required_input": "matching_profile",
                    },
                },
            }
            with (
                mock.patch.object(
                    self.tool, "load_manifest",
                    return_value={"production_ssh_target": "v7-vps"},
                ),
                mock.patch.object(
                    self.tool,
                    "read_active_standing_policy_runtime_status",
                    return_value={
                        "ok": True, "errors": [], "status": status,
                    },
                ),
                mock.patch.object(
                    self.tool.sync_lib,
                    "reconcile_active_standing_delegated_policy_to_cps",
                ) as reconcile,
            ):
                result = self.tool.consume_controlled_source_baseline_reentry(
                    root=root,
                )
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertEqual(
                result["consumer_decision"],
                "LEGAL_NO_ACTION_EXTERNAL_BASELINE_UNCHANGED",
            )
            self.assertFalse(result["cps_mutated"])
            reconcile.assert_not_called()

    def test_external_baseline_heartbeat_consumes_health_and_releases_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps.parent.mkdir(parents=True)
            cps.write_text(
                "## 0. Authoritative Live Current State\n\n"
                "| Field | Current Value |\n| --- | --- |\n"
                "| `CURRENT_NEXT_ACTION_ID` | "
                "`EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED` |\n\n"
                "## Authoritative Unfinished Capability Closure Registry\n",
                encoding="utf-8",
            )
            status = {
                "controlled_certification_substrate_authority": {
                    "source_precondition_status": "PASS",
                    "source_baseline_health": {
                        "root_cause_class": "NONE",
                    },
                },
            }
            with (
                mock.patch.object(
                    self.tool, "load_manifest",
                    return_value={"production_ssh_target": "v7-vps"},
                ),
                mock.patch.object(
                    self.tool,
                    "read_active_standing_policy_runtime_status",
                    return_value={
                        "ok": True, "errors": [], "status": status,
                    },
                ),
                mock.patch.object(
                    self.tool.sync_lib,
                    "reconcile_active_standing_delegated_policy_to_cps",
                    return_value={
                        "final_verdict": "PASS",
                        "errors": [],
                    },
                ) as reconcile,
            ):
                result = self.tool.consume_controlled_source_baseline_reentry(
                    root=root,
                )
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertTrue(result["ready_for_heartbeat"])
            self.assertTrue(result["cps_mutated"])
            self.assertEqual(
                result["consumer_decision"],
                "HEALTHY_BASELINE_CONSUMED_CONTINUE_EXISTING_T48_SUCCESSOR",
            )
            reconcile.assert_called_once_with(status, root=root)

    def test_fetches_one_accounted_production_feedback_envelope_read_only(self):
        manifest = self.manifest()
        manifest["production_ssh_target"] = "v7-vps"
        envelope = {
            "schema_version": "v7.execution-outcome-record.v1",
            "feedback_id": "execfb_fetch", "packet_id": "pkt_fetch",
            "service_failure_causal_binding": {"source_incident_id": "sfinc_fetch"},
        }
        command = (
            "ssh", "v7-vps",
            f"python3 -c {shlex.quote(self.tool.SERVICE_FAILURE_PRODUCTION_ENVELOPE_SCRIPT)}",
        )
        result = self.tool.fetch_accounted_service_failure_feedback(
            manifest,
            runner=FakeRunner({command: json.dumps(envelope)}),
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["remote_read"]["feedback_id"], "execfb_fetch")
        self.assertTrue(result["remote_read"]["read_only"])

    def test_rejects_invalid_production_ssh_target_before_remote_read(self):
        manifest = self.manifest()
        manifest["production_ssh_target"] = "v7-vps; unsafe"
        result = self.tool.fetch_accounted_service_failure_feedback(manifest)
        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"], ["production_ssh_target_invalid"])

    def test_matrix_owned_controlled_campaign_successor_skips_vless_feedback_predecessor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps_path.parent.mkdir(parents=True)
            cps_path.write_text(
                "\n".join([
                    "## 0. Authoritative Live Current State",
                    "",
                    "| Field | Value |",
                    "|---|---|",
                    f"| `ACTIVE_PROGRAM` | `{self.tool.sync_lib.SERVICE_FAILURE_AUTOMATION_PROGRAM_ID}` |",
                    "| `CURRENT_NEXT_ACTION_ID` | `CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED` |",
                    "| `CURRENT_PROGRAM_EXECUTION_FRONTIER` | `CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED` |",
                    "",
                    "## Authoritative Unfinished Capability Closure Registry",
                ]),
                encoding="utf-8",
            )
            result = self.tool.current_matrix_owned_service_failure_successor(root)
        self.assertTrue(result["matrix_owned"], result)
        self.assertEqual(
            result["frontier"],
            "CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED",
        )
        self.assertEqual(
            result["consumer"],
            "tools/v7-service-matrix-refresh-all",
        )

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
            runner=self.runner(status="?? docs/reports/evidence/z8_11-evidence/runtime_convergence_snapshot.json"),
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
            runner=self.runner(status=" M tools/v7-users-autoswitch\n?? docs/reports/evidence/z8_11-evidence/runtime_convergence_snapshot.json"),
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

    def test_matrix_owned_successor_requires_live_health_matrix_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps_path.parent.mkdir(parents=True)
            cps_path.write_text(
                "\n".join([
                    "## 0. Authoritative Live Current State", "",
                    "| Field | Value |", "|---|---|",
                    f"| `ACTIVE_PROGRAM` | `{self.tool.sync_lib.SERVICE_FAILURE_AUTOMATION_PROGRAM_ID}` |",
                    "| `CURRENT_NEXT_ACTION_ID` | `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_25` |",
                    "| `CURRENT_PROGRAM_EXECUTION_FRONTIER` | `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_25` |",
                    "", "## Authoritative Unfinished Capability Closure Registry",
                ]),
                encoding="utf-8",
            )
            manifest = self.manifest(workspace=tmp)
            manifest["runtime_snapshot_path"] = str(root / "runtime-snapshot.json")
            snapshot = self.runtime_snapshot()
            owner_command = self.tool.command_key([
                "systemctl", "status", "v7-health.service", "--no-pager",
            ])
            snapshot["command_results"][owner_command] = {
                "rc": 3, "stdout": "Active: inactive (dead)", "stderr": "",
            }
            Path(manifest["runtime_snapshot_path"]).write_text(
                json.dumps(snapshot), encoding="utf-8"
            )
            result = self.tool.combine_results(
                manifest, mode="runtime-readonly", runner=self.runner(), cwd=root
            )
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn(
            "matrix_owned_successor_without_live_health_owner",
            result["blockers"],
        )
        self.assertEqual(
            result["runtime"]["matrix_runtime_consumer"]["status"],
            "MATRIX_SUCCESSOR_WITHOUT_LIVE_HEALTH_OWNER",
        )

    def test_matrix_owned_successor_accepts_live_health_matrix_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps_path.parent.mkdir(parents=True)
            cps_path.write_text(
                "\n".join([
                    "## 0. Authoritative Live Current State", "",
                    "| Field | Value |", "|---|---|",
                    f"| `ACTIVE_PROGRAM` | `{self.tool.sync_lib.SERVICE_FAILURE_AUTOMATION_PROGRAM_ID}` |",
                    "| `CURRENT_NEXT_ACTION_ID` | `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_25` |",
                    "| `CURRENT_PROGRAM_EXECUTION_FRONTIER` | `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_25` |",
                    "", "## Authoritative Unfinished Capability Closure Registry",
                ]),
                encoding="utf-8",
            )
            manifest = self.manifest(workspace=tmp)
            manifest["runtime_snapshot_path"] = str(root / "runtime-snapshot.json")
            snapshot = self.runtime_snapshot()
            owner_command = self.tool.command_key([
                "systemctl", "status", "v7-health.service", "--no-pager",
            ])
            snapshot["command_results"][owner_command] = {
                "rc": 0, "stdout": "Active: active (running)", "stderr": "",
            }
            Path(manifest["runtime_snapshot_path"]).write_text(
                json.dumps(snapshot), encoding="utf-8"
            )
            result = self.tool.combine_results(
                manifest, mode="runtime-readonly", runner=self.runner(), cwd=root
            )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(
            result["runtime"]["matrix_runtime_consumer"]["status"],
            "LIVE_V7_HEALTH_MATRIX_OWNER_PROVEN",
        )

    def test_runtime_snapshot_ignores_retired_matrix_timer_status_cells(self):
        """N11 retirement must not invalidate an otherwise fresh snapshot."""
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.manifest(workspace=tmp)
            manifest["runtime_snapshot_path"] = str(Path(tmp) / "runtime-snapshot.json")
            snapshot = self.runtime_snapshot()
            for unit in (
                "v7-users-autoswitch.timer",
                "v7-service-matrix-refresh.timer",
            ):
                key = self.tool.command_key([
                    "systemctl", "status", unit, "--no-pager",
                ])
                snapshot["command_results"][key] = {
                    "rc": 3, "stdout": "Active: inactive (dead)", "stderr": "",
                }
            Path(manifest["runtime_snapshot_path"]).write_text(
                json.dumps(snapshot), encoding="utf-8"
            )
            result = self.tool.combine_results(
                manifest, mode="all", runner=self.runner(), cwd=Path(tmp)
            )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["runtime"]["unknown_commands"], [])

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
                        "docs/reports/evidence/BA1_EVIDENCE/final_verdict.json",
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

    def test_delegated_policy_consistency_is_machine_readable_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            programs = root / "docs" / "programs"
            programs.mkdir(parents=True)
            (programs / "V7_CURRENT_PROGRAM_STATE.md").write_text(
                "| `DELEGATED_AUTONOMY_POLICY` | `APPROVED` |\n"
                "| `PACKET_APPROVAL_REQUIRED` | `NO` |\n"
                "| `CANDIDATE_APPROVAL_REQUIRED` | `NO` |\n",
                encoding="utf-8",
            )
            (programs / "OPERATIONAL_MATURITY_PROGRAM.md").write_text(
                "| Policy state | `APPROVED` |\n"
                "| Current mode | `GOVERNED_ONLY` |\n"
                "| Current action-class contract | `MISSING` |\n"
                "| Runtime apply enabled | `NO` |\n"
                "| Packet approval required | `NO` |\n",
                encoding="utf-8",
            )

            result = self.tool.delegated_policy_consistency_check(root)

            self.assertEqual(result["contradiction_count"], 0)
            self.assertEqual(result["contradiction_ids"], [])
            self.assertTrue(result["packet_approval_retired"])
            self.assertTrue(result["candidate_approval_retired"])
            self.assertTrue(result["policy_self_expansion_blocked"])
            self.assertTrue(result["single_user_blast_radius_enforced"])
            self.assertTrue(result["serial_execution_enforced"])
            self.assertEqual(len(result["policy_scope_hash"]), 64)

            (programs / "V7_CURRENT_PROGRAM_STATE.md").write_text(
                "| `PACKET_APPROVAL_REQUIRED` | `YES` |\n",
                encoding="utf-8",
            )
            failed = self.tool.delegated_policy_consistency_check(root)
            self.assertIn("packet_approval_retired", failed["contradiction_ids"])
            self.assertGreater(failed["contradiction_count"], 0)

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
