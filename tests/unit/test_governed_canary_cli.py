import importlib.machinery
import importlib.util
import json
import argparse
import tempfile
import unittest
from pathlib import Path


def load_cli_module():
    path = Path(__file__).resolve().parents[2] / "tools" / "v7-governed-canary-dry-run-cycle"
    loader = importlib.machinery.SourceFileLoader("v7_governed_canary_dry_run_cycle", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class GovernedCanaryCliTest(unittest.TestCase):
    def test_planner_executable_uses_repo_tool_when_available(self):
        module = load_cli_module()
        self.assertEqual(module.planner_observe_executable(), module.ROOT / "tools" / "v7-users-autoswitch")

    def test_planner_executable_falls_back_to_runtime_peer(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "bin"
            runtime_dir.mkdir(parents=True)
            script = runtime_dir / "v7-governed-canary-dry-run-cycle"
            peer = runtime_dir / "v7-users-autoswitch"
            script.write_text("", encoding="utf-8")
            peer.write_text("", encoding="utf-8")
            original_root = module.ROOT
            original_file = module.__file__
            try:
                module.ROOT = root / "missing-repo-root"
                module.__file__ = str(script)
                self.assertEqual(module.planner_observe_executable().resolve(), peer.resolve())
            finally:
                module.ROOT = original_root
                module.__file__ = original_file

    def transaction_args(self, root: Path):
        return argparse.Namespace(
            state_dir=str(root / "state"),
            event_dir=str(root / "events"),
            snapshot_root=str(root / "state" / "intelligence"),
            audit_dir=str(root / "audit"),
            max_users=1,
            max_events=25,
            skip_planner_observe=True,
            execution_lease_file=str(root / "state" / "operator-execution-lease.json"),
            create_execution_lease=False,
            execute_governed_transaction=True,
            confirm_governed_transaction="EXECUTE_GOVERNED_TRANSACTION_APPROVED",
            committed_preview_file="",
            restore_barrier_file=str(root / "state" / "autoswitch-restore-barrier.json"),
            approval_author="operator-a",
            approval_reviewer="operator-b",
            ttl_seconds=600,
            approved_packet_id="",
            approved_decision_id="",
            approved_operation_id="",
            approved_selected_move_hash="",
            approved_user="",
            approved_source="",
            approved_target="",
            approved_authority_generation="",
            pretty=False,
        )

    def ready_cycle(self):
        preview = {
            "schema_version": "v7.governed-canary.packet-preview.v1",
            "status": "PACKET_PREVIEW_READY",
            "packet_id": "pkt_preview_test",
            "operation_id": "govdry_test",
            "decision_id": "decision_commit_test",
            "authority_generation": "authgen_test",
            "selected_move_hash": "hash_test",
            "selected_move_count": 1,
            "allowed_users": ["10.7.0.5"],
            "allowed_targets": ["awg3"],
            "rollback_manifest_preview": {
                "rollback_manifest_id": "rb_preview_test",
                "items": [
                    {
                        "user_ip": "10.7.0.5",
                        "rollback_target": "vless",
                        "forward_target": "awg3",
                    }
                ],
            },
        }
        return {
            "stop_reason": "AUTHORITY_BOUNDARY",
            "packet_preview": preview,
            "action_class_runtime_enablement": {
                "current_action_class": "single-user governed candidate failover",
            },
        }

    def make_transaction_state(self, root: Path):
        state = root / "state"
        events = root / "events"
        snapshot = state / "intelligence"
        audit = root / "audit"
        for path in (state, events, snapshot, audit):
            path.mkdir(parents=True, exist_ok=True)
        (state / "users.registry").write_text("10.7.0.5 vless\n", encoding="utf-8")
        (state / "egress.registry").write_text("vless\nawg3\n", encoding="utf-8")

    def test_execute_governed_transaction_completes_one_attempt_and_terminalizes_lease(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            original_cycle = module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle
            original_apply = module.run_autoswitch_apply
            try:
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = (
                    lambda **kwargs: self.ready_cycle()
                )
                module.run_autoswitch_apply = lambda **kwargs: {
                    "ok": True,
                    "returncode": 0,
                    "payload": {
                        "operation": {
                            "operation_id": "runtime_autoswitch_test",
                            "terminal_state": "APPLIED",
                            "terminal_reason": "selected_moves_applied",
                        },
                        "apply_result": {
                            "applied": True,
                            "results": [
                                {"user_ip": "10.7.0.5", "from": "vless", "to": "awg3", "verify_rc": 0}
                            ],
                        },
                    },
                }
                result = module.execute_governed_transaction(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
                lease = json.loads((root / "state" / "operator-execution-lease.json").read_text(encoding="utf-8"))
                execution_rows = [
                    json.loads(line)
                    for line in (root / "state" / "execution-events.jsonl").read_text(encoding="utf-8").splitlines()
                ]
                trust_rows = [
                    json.loads(line)
                    for line in (root / "state" / "runtime-trust.jsonl").read_text(encoding="utf-8").splitlines()
                ]
                recommendation_rows = [
                    json.loads(line)
                    for line in (root / "state" / "proposal-records.jsonl").read_text(encoding="utf-8").splitlines()
                ]
                closure_rows = [
                    json.loads(line)
                    for line in (root / "state" / "closure-records.jsonl").read_text(encoding="utf-8").splitlines()
                ]
            finally:
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = original_cycle
                module.run_autoswitch_apply = original_apply

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_COMPLETED")
        self.assertEqual(result["fresh_packet_id"], "pkt_preview_test")
        self.assertTrue(result["restore_barrier_written_now"])
        self.assertTrue(result["apply_executed"])
        self.assertEqual(result["users_moved"], 1)
        self.assertFalse(result["runtime_automation_enabled"])
        self.assertFalse(result["authority_expanded"])
        self.assertEqual(lease["status"], "EXECUTION_FINISHED")
        self.assertTrue(lease["apply_executed"])
        self.assertEqual(lease["users_moved"], 1)
        self.assertTrue(result["feedback_materialization"]["materialized"])
        self.assertTrue(result["feedback_materialization"]["knowledge_gained"])
        self.assertTrue(result["a4_evidence_updated"])

        self.assertEqual(len(execution_rows), 2)
        self.assertEqual(len(trust_rows), 1)
        self.assertEqual(len(recommendation_rows), 1)
        self.assertEqual(len(closure_rows), 1)
        self.assertEqual(execution_rows[0]["packet_id"], "pkt_preview_test")
        self.assertEqual(execution_rows[0]["outcome_quality"]["outcome_quality"], "SUCCESS")
        self.assertEqual(closure_rows[0]["closure_state"], "CLOSED")

    def test_execute_governed_transaction_requires_explicit_transaction_confirmation(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.confirm_governed_transaction = ""
            result = module.execute_governed_transaction(
                args,
                state_dir=root / "state",
                event_dir=root / "events",
                snapshot_root=root / "state" / "intelligence",
                audit_dir=root / "audit",
                lease_file=root / "state" / "operator-execution-lease.json",
            )

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_STOPPED")
        self.assertEqual(result["stop_reason"], "transaction_confirmation_required")
        self.assertFalse(result["apply_executed"])

    def test_a4_bounded_evidence_collection_requires_explicit_confirmation(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_a4_bounded_evidence_collection = True
            args.confirm_a4_bounded_evidence_collection = ""
            args.max_evidence_outcomes = 2
            result = module.execute_a4_bounded_evidence_collection(
                args,
                state_dir=root / "state",
                event_dir=root / "events",
                snapshot_root=root / "state" / "intelligence",
                audit_dir=root / "audit",
                lease_file=root / "state" / "operator-execution-lease.json",
            )

        self.assertEqual(result["final_verdict"], "A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED")
        self.assertEqual(result["stop_reason"], "collection_confirmation_required")
        self.assertEqual(result["transactions_attempted"], 0)
        self.assertFalse(result["runtime_automation_enabled"])
        self.assertFalse(result["authority_expanded"])

    def test_a4_bounded_evidence_collection_runs_limited_one_user_transactions(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_a4_bounded_evidence_collection = True
            args.confirm_a4_bounded_evidence_collection = "EXECUTE_A4_BOUNDED_EVIDENCE_COLLECTION_APPROVED"
            args.max_evidence_outcomes = 2
            calls = []

            def fake_transaction(*_args, **_kwargs):
                idx = len(calls) + 1
                calls.append(idx)
                return {
                    "final_verdict": "GOVERNED_TRANSACTION_COMPLETED",
                    "fresh_packet_id": f"pkt_preview_{idx}",
                    "user": f"10.7.0.{idx}",
                    "source": "vless",
                    "target": "awg3",
                    "users_moved": 1,
                    "verification_result": "PASS",
                    "a4_evidence_updated": True,
                    "runtime_automation_enabled": False,
                    "authority_expanded": False,
                }

            original = module.execute_governed_transaction_with_guards
            original_missing = module.current_a4_missing_candidate_keys
            try:
                module.current_a4_missing_candidate_keys = lambda *_args, **_kwargs: {
                    ("10.7.0.1", "awg3"),
                    ("10.7.0.2", "awg3"),
                }
                module.execute_governed_transaction_with_guards = fake_transaction
                result = module.execute_a4_bounded_evidence_collection(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.execute_governed_transaction_with_guards = original
                module.current_a4_missing_candidate_keys = original_missing

        self.assertEqual(result["final_verdict"], "A4_BOUNDED_EVIDENCE_COLLECTION_COMPLETED")
        self.assertEqual(result["successful_outcomes"], 2)
        self.assertEqual(result["transactions_attempted"], 2)
        self.assertEqual(calls, [1, 2])
        self.assertTrue(result["one_user_per_transaction"])
        self.assertTrue(result["stop_on_first_failed_gate"])
        self.assertFalse(result["runtime_automation_enabled"])
        self.assertFalse(result["authority_expanded"])
        self.assertFalse(result["new_owner_created"])
        self.assertFalse(result["new_backlog_item_created"])

    def test_a4_bounded_evidence_collection_stops_on_first_failed_gate(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_a4_bounded_evidence_collection = True
            args.confirm_a4_bounded_evidence_collection = "EXECUTE_A4_BOUNDED_EVIDENCE_COLLECTION_APPROVED"
            args.max_evidence_outcomes = 3
            results = [
                {
                    "final_verdict": "GOVERNED_TRANSACTION_COMPLETED",
                    "fresh_packet_id": "pkt_preview_1",
                    "user": "10.7.0.1",
                    "source": "vless",
                    "target": "awg3",
                    "users_moved": 1,
                    "verification_result": "PASS",
                    "a4_evidence_updated": True,
                    "runtime_automation_enabled": False,
                    "authority_expanded": False,
                },
                {
                    "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
                    "stop_reason": "packet_not_ready",
                    "users_moved": 0,
                    "runtime_automation_enabled": False,
                    "authority_expanded": False,
                },
            ]

            def fake_transaction(*_args, **_kwargs):
                return results.pop(0)

            original = module.execute_governed_transaction_with_guards
            original_missing = module.current_a4_missing_candidate_keys
            try:
                module.current_a4_missing_candidate_keys = lambda *_args, **_kwargs: {("10.7.0.1", "awg3")}
                module.execute_governed_transaction_with_guards = fake_transaction
                result = module.execute_a4_bounded_evidence_collection(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.execute_governed_transaction_with_guards = original
                module.current_a4_missing_candidate_keys = original_missing

        self.assertEqual(result["final_verdict"], "A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED")
        self.assertEqual(result["stop_reason"], "packet_not_ready")
        self.assertEqual(result["successful_outcomes"], 1)
        self.assertEqual(result["transactions_attempted"], 2)
        self.assertFalse(result["runtime_automation_enabled"])
        self.assertFalse(result["authority_expanded"])

    def test_a4_bounded_evidence_collection_does_not_count_failed_verification(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_a4_bounded_evidence_collection = True
            args.confirm_a4_bounded_evidence_collection = "EXECUTE_A4_BOUNDED_EVIDENCE_COLLECTION_APPROVED"
            args.max_evidence_outcomes = 2

            def fake_transaction(*_args, **_kwargs):
                return {
                    "final_verdict": "GOVERNED_TRANSACTION_COMPLETED",
                    "fresh_packet_id": "pkt_preview_failed",
                    "user": "10.7.0.9",
                    "source": "vless",
                    "target": "awg3",
                    "users_moved": 1,
                    "verification_result": "FAIL",
                    "a4_evidence_updated": True,
                    "runtime_automation_enabled": False,
                    "authority_expanded": False,
                }

            original = module.execute_governed_transaction_with_guards
            original_missing = module.current_a4_missing_candidate_keys
            try:
                module.current_a4_missing_candidate_keys = lambda *_args, **_kwargs: {("10.7.0.9", "awg3")}
                module.execute_governed_transaction_with_guards = fake_transaction
                result = module.execute_a4_bounded_evidence_collection(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.execute_governed_transaction_with_guards = original
                module.current_a4_missing_candidate_keys = original_missing

        self.assertEqual(result["final_verdict"], "A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED")
        self.assertEqual(result["stop_reason"], "transaction_verification_failed")
        self.assertEqual(result["successful_outcomes"], 0)
        self.assertEqual(result["transactions_attempted"], 1)

    def test_governed_transaction_stops_before_apply_for_duplicate_candidate(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            original_cycle = module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle
            original_apply = module.run_autoswitch_apply
            try:
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = (
                    lambda **kwargs: self.ready_cycle()
                )

                def fail_apply(**_kwargs):
                    raise AssertionError("duplicate guard must stop before apply")

                module.run_autoswitch_apply = fail_apply
                result = module.execute_governed_transaction_with_guards(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                    blocked_transaction_identities={("pkt_preview_test", "10.7.0.5", "vless", "awg3")},
                )
                lease_exists = (root / "state" / "operator-execution-lease.json").exists()
                barrier_exists = (root / "state" / "autoswitch-restore-barrier.json").exists()
            finally:
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = original_cycle
                module.run_autoswitch_apply = original_apply

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_STOPPED")
        self.assertEqual(result["stop_reason"], "duplicate_transaction_candidate")
        self.assertEqual(result["duplicate_guard_stage"], "pre_lease_pre_restore_barrier_pre_apply")
        self.assertFalse(lease_exists)
        self.assertFalse(barrier_exists)

    def test_governed_transaction_stops_before_apply_for_non_missing_a4_candidate(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            original_cycle = module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle
            original_apply = module.run_autoswitch_apply
            try:
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = (
                    lambda **kwargs: self.ready_cycle()
                )

                def fail_apply(**_kwargs):
                    raise AssertionError("A4 evidence guard must stop before apply")

                module.run_autoswitch_apply = fail_apply
                result = module.execute_governed_transaction_with_guards(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                    required_a4_candidate_keys={("10.7.0.99", "awg3")},
                )
                lease_exists = (root / "state" / "operator-execution-lease.json").exists()
                barrier_exists = (root / "state" / "autoswitch-restore-barrier.json").exists()
            finally:
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = original_cycle
                module.run_autoswitch_apply = original_apply

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_STOPPED")
        self.assertEqual(result["stop_reason"], "candidate_not_missing_a4_evidence")
        self.assertEqual(result["evidence_guard_stage"], "pre_lease_pre_restore_barrier_pre_apply")
        self.assertFalse(lease_exists)
        self.assertFalse(barrier_exists)


if __name__ == "__main__":
    unittest.main()
