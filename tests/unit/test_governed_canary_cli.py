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


if __name__ == "__main__":
    unittest.main()
