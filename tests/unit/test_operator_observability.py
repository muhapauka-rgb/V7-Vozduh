import tempfile
import unittest
from pathlib import Path

from admin_core.operator_observability import (
    build_operator_approval_preview,
    build_operator_audit_export_preview,
    build_operator_audit_search,
    build_operator_evidence_archive,
    build_operator_evidence_file_detail,
    build_operator_execution_governance_preview,
    build_operator_execution_rehearsal_preview,
    build_operator_lineage_archive,
    build_operator_operation_detail,
    build_operator_view_model,
)


class OperatorObservabilityTest(unittest.TestCase):
    def test_missing_runtime_files_are_conservative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = build_operator_view_model(repo_root=root, state_dir=root / "missing-state", event_dir=root / "missing-events")

        self.assertFalse(model["overview"]["execution_allowed_now"])
        self.assertEqual(model["targets"]["freshness"]["state"], "MISSING")
        self.assertIn("target_pool_stale_or_missing", model["governance_verdict"]["blockers"])

    def test_target_pool_parses_registry_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.11 current=1 enabled=1\n"
                "ip=10.7.0.12 current=wireguard-1779454504-c43409 enabled=1\n",
                encoding="utf-8",
            )
            (state / "egress.registry").write_text(
                "id=1 enabled=1 protocol=amneziawg soft_limit=10 hard_limit=12\n"
                "id=wireguard-1779454504-c43409 enabled=1 protocol=wireguard soft_limit=1 hard_limit=2 canary_reserved=true\n",
                encoding="utf-8",
            )
            model = build_operator_view_model(repo_root=root, state_dir=state, event_dir=root / "events")

        targets = {row["target_id"]: row for row in model["targets"]["targets"]}
        self.assertEqual(targets["1"]["users"], 1)
        self.assertTrue(targets["wireguard-1779454504-c43409"]["reserved"])
        self.assertEqual(targets["wireguard-1779454504-c43409"]["users"], 1)

    def test_operations_history_redacts_secret_like_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BLOCK_E12_TEST_REPORT.md").write_text(
                "# BLOCK E12 Test\n\n"
                "execution_allowed_now=false\n"
                "token=SHOULD_NOT_RENDER\n"
                "Runtime mutation performed: NO\n",
                encoding="utf-8",
            )
            model = build_operator_view_model(repo_root=root, state_dir=root / "state", event_dir=root / "events")

        blob = str(model["operations"])
        self.assertIn("execution_allowed_now", blob)
        self.assertNotIn("SHOULD_NOT_RENDER", blob)

    def test_admin_operator_namespace_has_no_post_routes(self):
        source = Path("admin/v7-admin-api").read_text(encoding="utf-8")
        self.assertIn('elif path == "/api/operator/overview"', source)
        self.assertIn('elif path == "/api/operator/decision-surface"', source)
        self.assertIn('elif path == "/api/operator/approval-preview"', source)
        self.assertIn('elif path == "/api/operator/timeline"', source)
        self.assertIn('elif path == "/api/operator/operation-detail"', source)
        self.assertIn('elif path == "/api/operator/audit-search"', source)
        self.assertIn('elif path == "/api/operator/audit-export-preview"', source)
        self.assertIn('elif path == "/api/operator/execution-governance-preview"', source)
        self.assertIn('elif path == "/api/operator/execution-rehearsal-preview"', source)
        self.assertIn('elif path == "/api/operator/evidence-file-detail"', source)
        self.assertNotIn('elif path == "/api/actions/operator', source)
        self.assertNotIn('path == "/api/operator/', source.split("def do_POST", 1)[-1])
        self.assertIn('id="operatorApprovalContracts"', source)
        self.assertIn('id="operatorTimeline"', source)
        self.assertIn('id="operatorAuditResults"', source)
        self.assertIn('id="operatorRunbookPreview"', source)
        self.assertIn('id="operatorExecutionGovernance"', source)
        self.assertIn('id="operatorExecutionRehearsal"', source)
        self.assertIn('class="operator-disabled-action"', source)
        self.assertIn('openOperatorAuditExportPreview', source)
        self.assertIn('openOperatorExecutionGovernance', source)
        self.assertIn('openOperatorExecutionRehearsal', source)
        self.assertIn('aria-disabled="true"', source)

    def test_approval_preview_is_disabled_and_contract_shaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preview = build_operator_approval_preview(repo_root=root, state_dir=root / "state", event_dir=root / "events")

        self.assertTrue(preview["preview_only"])
        self.assertFalse(preview["execution_allowed_now"])
        self.assertIn("MovementApprovalPreview", preview["contracts"])
        self.assertIn("GenerationClearancePreview", preview["contracts"])
        self.assertIn("RollbackManifestPreview", preview["contracts"])
        self.assertTrue(preview["generation_guard"]["generation_id_required"])
        self.assertTrue(preview["generation_guard"]["selected_move_fingerprint_required"])
        self.assertTrue(all(action["disabled"] for action in preview["disabled_actions"]))
        self.assertTrue(preview["disabled_reason"])

    def test_approval_preview_redacts_secret_like_report_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BLOCK_E12_GENERATION_TOKEN_HARDENING_NONZERO_BUDGET_REHEARSAL_AND_ORCHESTRATION_MATURITY_REPORT.md").write_text(
                "selected_candidates=10.7.0.11,10.7.0.12\n"
                "token=SHOULD_NOT_RENDER\n",
                encoding="utf-8",
            )
            preview = build_operator_approval_preview(repo_root=root, state_dir=root / "state", event_dir=root / "events")

        blob = str(preview)
        self.assertIn("10.7.0.11", blob)
        self.assertNotIn("SHOULD_NOT_RENDER", blob)

    def test_lineage_archive_orders_and_groups_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "docs" / "track7" / "control-plane" / "e11_13-evidence"
            evidence.mkdir(parents=True)
            (evidence / "rollback-verification.txt").write_text("ok\n", encoding="utf-8")
            (root / "BLOCK_E11_13_TWO_USER_MINI_COHORT_FULL_EXECUTION_LIFECYCLE_REPORT.md").write_text(
                "# E11.13 report\n\n"
                "moved_users=10.7.0.11,10.7.0.12\n"
                "rollback_executed=true\n"
                "delayed_movement_observed=true\n"
                "execution_allowed_now=false\n"
                "Runtime mutation performed: YES\n"
                "User movement performed by this block: YES\n",
                encoding="utf-8",
            )
            (root / "BLOCK_E16_APPROVAL_CENTER_AND_SAFE_ACTION_UX_CONTRACT_IMPLEMENTATION_REPORT.md").write_text(
                "# E16 report\n\n"
                "execution_allowed_now=false\n"
                "Runtime mutation performed: NO\n",
                encoding="utf-8",
            )
            archive = build_operator_lineage_archive(repo_root=root)

        self.assertEqual(archive["operation_count"], 2)
        ids = [item["operation_id"] for item in archive["timeline"]]
        self.assertIn("E11_13_TWO_USER_MINI_COHORT_FULL_EXECUTION_LIFECYCLE_REPORT", ids)
        cohort = archive["operations_by_id"]["E11_13_TWO_USER_MINI_COHORT_FULL_EXECUTION_LIFECYCLE_REPORT"]
        self.assertEqual(cohort["operation_type"], "cohort")
        self.assertEqual(cohort["rollback"]["rollback_executed"], "true")
        self.assertEqual(cohort["delayed_movement"]["observed"], True)
        self.assertEqual(cohort["movement"]["users"], ["10.7.0.11", "10.7.0.12"])
        self.assertTrue(any(ref["kind"] == "evidence_dir" for ref in cohort["evidence_refs"]))

    def test_operation_detail_is_safe_and_missing_tolerant(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BLOCK_E12_TEST_REPORT.md").write_text(
                "# E12 report\n\n"
                "execution_allowed_now=false\n"
                "token=SHOULD_NOT_RENDER\n"
                "Canary performed: NO\n",
                encoding="utf-8",
            )
            detail = build_operator_operation_detail("E12_TEST_REPORT", repo_root=root)
            missing = build_operator_operation_detail("MISSING", repo_root=root)

        self.assertFalse(detail["execution_allowed_now"])
        self.assertIn("E12_TEST_REPORT", detail["operation"]["operation_id"])
        self.assertNotIn("SHOULD_NOT_RENDER", detail["safe_report_excerpt"])
        self.assertEqual(missing["error"], "operation_not_found")

    def test_audit_search_indexes_operations_and_evidence_safely(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "docs" / "track7" / "control-plane" / "e11_14-evidence"
            evidence.mkdir(parents=True)
            (evidence / "root-cause-matrix.md").write_text(
                "# Matrix\n\n"
                "delayed recompute contained\n"
                "token=SHOULD_NOT_RENDER\n",
                encoding="utf-8",
            )
            (root / "BLOCK_E11_14_DELAYED_APPLY_RESTORE_MOVEMENT_ROOT_CAUSE_AND_APPLY_TIMER_GOVERNANCE_FIX_REPORT.md").write_text(
                "# E11.14 report\n\n"
                "delayed_movement_observed=true\n"
                "execution_allowed_now=false\n"
                "Runtime mutation performed: YES\n",
                encoding="utf-8",
            )
            results = build_operator_audit_search(repo_root=root, query="delayed")
            archive = build_operator_evidence_archive(repo_root=root)
            evidence_items = [item for item in archive["items"] if item["label"] == "root-cause-matrix.md"]
            detail = build_operator_evidence_file_detail(evidence_items[0]["evidence_id"], repo_root=root)

        self.assertGreaterEqual(results["result_count"], 1)
        self.assertTrue(any(row["kind"] == "evidence" for row in results["results"]))
        self.assertIn("delayed recompute", detail["safe_excerpt"])
        self.assertNotIn("SHOULD_NOT_RENDER", detail["safe_excerpt"])
        self.assertIn("secret_like_lines_redacted", detail["warnings"])

    def test_evidence_detail_rejects_unknown_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            detail = build_operator_evidence_file_detail("missing", repo_root=Path(tmp))

        self.assertEqual(detail["error"], "evidence_not_found")
        self.assertFalse(detail["execution_allowed_now"])

    def test_audit_export_preview_is_readonly_and_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BLOCK_E18_OPERATOR_AUDIT_SEARCH_AND_READONLY_EVIDENCE_DETAIL_HARDENING_REPORT.md").write_text(
                "# E18 report\n\n"
                "audit_search_implemented=true\n"
                "execution_allowed_now=false\n"
                "token=SHOULD_NOT_RENDER\n"
                "Runtime mutation performed: NO\n"
                "User movement performed by this block: NO\n"
                "Routing mutation performed by this block: NO\n"
                "Kill switch mutation performed: NO\n"
                "Autoswitch apply performed manually: NO\n"
                "Canary performed: NO\n",
                encoding="utf-8",
            )
            preview = build_operator_audit_export_preview(
                "E18_OPERATOR_AUDIT_SEARCH_AND_READONLY_EVIDENCE_DETAIL_HARDENING_REPORT",
                repo_root=root,
            )

        blob = str(preview)
        self.assertTrue(preview["preview_only"])
        self.assertFalse(preview["execution_allowed_now"])
        self.assertIn("runbook_text", preview)
        self.assertIn("multi_operator_audit_model", preview)
        self.assertTrue(preview["multi_operator_audit_model"]["second_confirmation_required"])
        self.assertEqual(preview["mutation_statement"]["runtime"], "NO")
        self.assertNotIn("SHOULD_NOT_RENDER", blob)

    def test_execution_governance_preview_is_disabled_and_replay_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preview = build_operator_execution_governance_preview(repo_root=root)

        self.assertTrue(preview["preview_only"])
        self.assertFalse(preview["execution_allowed_now"])
        self.assertFalse(preview["safe_action_status"]["runtime_mutation_surface_present"])
        self.assertTrue(preview["dual_confirmation"]["both_operators_required"])
        self.assertTrue(preview["replay_protection"]["reject_on_generation_mismatch"])
        self.assertTrue(preview["replay_protection"]["reject_on_selected_move_fingerprint_mismatch"])
        self.assertTrue(preview["blast_radius_enforcement"]["deny_if_scope_expands"])
        self.assertIn("ExecutionIntent", preview["contracts"])
        self.assertIn("ExecutionAuditRecord", preview["contracts"])
        self.assertTrue(all(action["disabled"] for action in preview["disabled_actions"]))

    def test_execution_rehearsal_covers_denials_without_runtime_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preview = build_operator_execution_rehearsal_preview(repo_root=root)

        verdicts = {row["actual_rehearsal_verdict"] for row in preview["rehearsal_matrix"]}
        scenarios = {row["scenario"] for row in preview["rehearsal_matrix"]}
        self.assertTrue(preview["preview_only"])
        self.assertTrue(preview["rehearsal_only"])
        self.assertFalse(preview["execution_allowed_now"])
        self.assertTrue(preview["real_runtime_execution_still_disabled"])
        self.assertFalse(preview["runtime_mutation_surface_present"])
        self.assertIn("EXECUTION_ALLOWED", verdicts)
        self.assertIn("APPROVAL_EXPIRED", verdicts)
        self.assertIn("STALE_RUNTIME", verdicts)
        self.assertIn("GENERATION_MISMATCH", verdicts)
        self.assertIn("REPLAY_REJECTED", verdicts)
        self.assertIn("BLAST_RADIUS_CHANGED", verdicts)
        self.assertIn("RESTORE_INVALID", verdicts)
        self.assertIn("approval_replay_after_rollback", scenarios)
        self.assertIn("execution_after_containment", scenarios)
        self.assertTrue(preview["immutable_execution_audit"]["append_only_semantics"])
        self.assertTrue(preview["dual_confirmation_rehearsal"]["same_actor_rejected"])
        self.assertEqual(preview["denial_lifecycle"]["safe_fallback_state"], "NO_RUNTIME_ACTION_TAKEN")


if __name__ == "__main__":
    unittest.main()
