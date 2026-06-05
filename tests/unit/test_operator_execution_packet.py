import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from admin_core.operator_execution import (
    CANONICAL_CLEARANCE_OWNER,
    EMPTY_SELECTED_MOVES_HASH,
    PacketError,
    RUNTIME_ACTION_CREATE_CLEARANCE,
    RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE,
    execute_packet,
    packet_from_plan,
    resolve_under_repo,
    runtime_recheck,
    sha256_bytes,
    sha256_file,
)


def write_json(path, data):
    Path(path).write_text(json.dumps(data, sort_keys=True), encoding="utf-8")


def packet_template(state_dir, expires_delta=timedelta(hours=1)):
    users_hash = sha256_file(Path(state_dir) / "users.registry")
    egress_hash = sha256_file(Path(state_dir) / "egress.registry")
    snapshot_hash = sha256_bytes(json.dumps(
        {
            "egress_registry_hash": egress_hash,
            "selected_move_hash": EMPTY_SELECTED_MOVES_HASH,
            "users_registry_hash": users_hash,
        },
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8"))
    now = datetime.now(timezone.utc)
    return {
        "schema_version": "e22.operator-execution-packet.v1",
        "packet_id": "pkt_test",
        "approval_id": "appr_test",
        "operation_id": "E22_TEST",
        "selected_first_action": "ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK",
        "runtime_action": "RECHECK_AND_RECORD_ONLY",
        "created_at": now.isoformat(),
        "expires_at": (now + expires_delta).isoformat(),
        "approvals": [
            {"operator_id": "operator-a", "role": "approval_author", "confirmed_at": now.isoformat()},
            {"operator_id": "operator-b", "role": "approval_reviewer", "confirmed_at": now.isoformat()},
        ],
        "constraints": {
            "selected_move_budget": 0,
            "allowed_users": [],
            "allowed_targets": [],
            "user_movement_allowed": False,
            "routing_mutation_allowed": False,
        },
        "expected": {
            "users_registry_hash": users_hash,
            "egress_registry_hash": egress_hash,
            "runtime_snapshot_hash": snapshot_hash,
            "selected_move_hash": EMPTY_SELECTED_MOVES_HASH,
            "generation_id": "gen-test",
        },
    }


class OperatorExecutionPacketTest(unittest.TestCase):
    def make_state(self, root):
        state = root / "state"
        state.mkdir()
        (state / "users.registry").write_text("ip=10.7.0.11 current=1 enabled=1\n", encoding="utf-8")
        (state / "egress.registry").write_text("id=1 enabled=1 protocol=amneziawg\n", encoding="utf-8")
        return state

    def movement_plan(self):
        atomic_envelope = {
            "schema_version": "v7.atomic-execution-envelope.v1",
            "envelope_id": "aee-test",
            "envelope_hash": "aee-hash-test",
            "source_bundle_hash": "source-bundle-hash-test",
            "snapshot_bundle_hash": "snapshot-bundle-hash-test",
        }
        return {
            "operation": {
                "runtime_snapshot_hash": "snapshot-test",
            },
            "safety": {
                "generation": {
                    "planner_generation_id": "gen-move",
                },
                "atomic_execution_envelope": atomic_envelope,
                "restore_barrier": {
                    "clearance_selected_moves_before_guard": 1,
                    "clearance_selected_moves_hash": "move-hash",
                },
            },
            "decisions": [
                {
                    "user_ip": "10.7.0.11",
                    "current_egress": "1",
                    "recommended_egress": "vless",
                    "action": "switch",
                    "move_type": "failover",
                }
            ],
        }

    def test_runtime_recheck_allows_record_only_for_matching_zero_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            packet = packet_template(state)
            result = runtime_recheck(packet, state)

        self.assertTrue(result["allow"])
        self.assertEqual(result["verdict"], "ALLOW_RECORD_ONLY")
        self.assertFalse(result["checks"]["real_runtime_action_after_recheck"])

    def test_execute_writes_approval_then_replay_denial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            packet = packet_template(state)
            first = execute_packet(packet, audit, state, mode="execute")
            replay = execute_packet(packet, audit, state, mode="execute")
            records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]

        self.assertTrue(first["record_written"])
        self.assertEqual(first["record"]["record_type"], "approval_record_persisted")
        self.assertEqual(first["recheck"]["verdict"], "ALLOW_RECORD_ONLY")
        self.assertEqual(replay["record"]["record_type"], "denial_record")
        self.assertEqual(replay["recheck"]["verdict"], "DENY_REPLAY")
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1]["previous_record_hash"], records[0]["record_hash"])
        self.assertFalse(records[0]["runtime_mutation"])

    def test_execute_runtime_action_writes_governance_transition_then_replay_denial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            governance = root / "governance.jsonl"
            packet = packet_template(state)
            packet["runtime_action"] = RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE
            first = execute_packet(packet, audit, state, mode="runtime_action", runtime_governance_store=governance)
            replay = execute_packet(packet, audit, state, mode="runtime_action", runtime_governance_store=governance)
            audit_records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            governance_records = [json.loads(line) for line in governance.read_text(encoding="utf-8").splitlines()]

        self.assertTrue(first["record_written"])
        self.assertEqual(first["record"]["record_type"], "runtime_action_record_persisted")
        self.assertTrue(first["record"]["runtime_mutation"])
        self.assertTrue(first["record"]["runtime_action_performed"])
        self.assertFalse(first["record"]["user_movement"])
        self.assertFalse(first["record"]["routing_mutation"])
        self.assertEqual(first["recheck"]["verdict"], "ALLOW_RECORD_ONLY")
        self.assertEqual(len(governance_records), 1)
        self.assertEqual(governance_records[0]["record_type"], "zero_move_governance_state_transition")
        self.assertFalse(governance_records[0]["user_movement"])
        self.assertFalse(governance_records[0]["routing_mutation"])
        self.assertEqual(replay["record"]["record_type"], "denial_record")
        self.assertEqual(replay["recheck"]["verdict"], "DENY_REPLAY")
        self.assertEqual(len(audit_records), 2)
        self.assertEqual(audit_records[1]["previous_record_hash"], audit_records[0]["record_hash"])

    def test_execute_runtime_action_denies_record_only_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            governance = root / "governance.jsonl"
            packet = packet_template(state)
            result = execute_packet(packet, audit, state, mode="runtime_action", runtime_governance_store=governance)
            records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(result["record"]["record_type"], "denial_record")
        self.assertEqual(result["recheck"]["verdict"], "DENY_RUNTIME_ACTION_UNSUPPORTED")
        self.assertFalse(governance.exists())
        self.assertFalse(records[0]["runtime_mutation"])

    def test_expired_missing_second_and_movement_packets_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            expired = packet_template(state, expires_delta=timedelta(seconds=-1))
            missing_second = packet_template(state)
            missing_second["approvals"] = missing_second["approvals"][:1]
            movement = packet_template(state)
            movement["constraints"]["allowed_users"] = ["10.7.0.11"]
            movement["constraints"]["user_movement_allowed"] = True

            self.assertEqual(runtime_recheck(expired, state)["verdict"], "DENY_PACKET_INVALID")
            self.assertIn("dual_confirmation_missing", runtime_recheck(missing_second, state)["errors"])
            self.assertIn("allowed_users_not_empty", runtime_recheck(movement, state)["errors"])

    def test_hash_generation_runtime_action_and_path_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            packet = packet_template(state)
            bad_hash = packet_template(state)
            bad_hash["expected"]["selected_move_hash"] = "bad"
            bad_generation = packet_template(state)
            bad_generation["expected"]["generation_id"] = ""
            bad_action = packet_template(state)
            bad_action["runtime_action"] = "MOVE_USER"
            missing_runtime = root / "missing"

            self.assertEqual(runtime_recheck(bad_hash, state)["verdict"], "DENY_PACKET_INVALID")
            self.assertIn("generation_id_missing", runtime_recheck(bad_generation, state)["errors"])
            self.assertIn("runtime_action_not_allowed", runtime_recheck(bad_action, state)["errors"])
            self.assertEqual(runtime_recheck(packet, missing_runtime)["verdict"], "DENY_STALE_RUNTIME")

    def test_path_traversal_blocked_for_packet_and_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(PacketError):
                resolve_under_repo("../outside.json", root)

    def test_nonzero_packet_generation_and_clearance_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            lifecycle = root / "lifecycle.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )
            barrier_data = json.loads(barrier.read_text(encoding="utf-8"))
            audit_records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            lifecycle_records = [json.loads(line) for line in lifecycle.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(packet["runtime_action"], RUNTIME_ACTION_CREATE_CLEARANCE)
        self.assertTrue(result["execution_allowed_now"])
        self.assertEqual(result["recheck"]["verdict"], "ALLOW_RESTORE_BARRIER_CLEARANCE")
        self.assertEqual(result["record"]["clearance_verdict"], "RESTORE_BARRIER_CLEARANCE_WRITTEN")
        self.assertEqual(barrier_data["clearance_generation_id"], "gen-move")
        self.assertEqual(barrier_data["approved_selected_moves_hash"], "move-hash")
        self.assertEqual(barrier_data["approved_atomic_execution_envelope_id"], "aee-test")
        self.assertEqual(barrier_data["approved_atomic_execution_envelope_hash"], "aee-hash-test")
        self.assertEqual(barrier_data["approved_source_bundle_hash"], "source-bundle-hash-test")
        self.assertEqual(barrier_data["clearance_expected_selected_moves"], 1)
        self.assertEqual(barrier_data["clearance_max_selected_moves"], 1)
        self.assertEqual(barrier_data["allowed_user"], "10.7.0.11")
        self.assertEqual(barrier_data["allowed_target"], "vless")
        self.assertEqual(len(audit_records), 1)
        self.assertEqual(len(lifecycle_records), 3)
        self.assertEqual(lifecycle_records[0]["record_type"], "restore_barrier_clearance_created")
        self.assertEqual(lifecycle_records[1]["record_type"], "operation_scoped_rollback_bound")
        self.assertEqual(lifecycle_records[2]["record_type"], "execution_readiness_closure_created")
        self.assertTrue(lifecycle_records[2]["execution_allowed_now"])

    def test_packet_from_plan_respects_clearance_selected_move_count(self):
        plan = self.movement_plan()
        plan["decisions"].extend([
            {
                "user_ip": "10.7.0.12",
                "current_egress": "1",
                "recommended_egress": "vless",
                "action": "switch",
                "move_type": "failover",
            },
            {
                "user_ip": "10.7.0.13",
                "current_egress": "1",
                "recommended_egress": "vless",
                "action": "switch",
                "move_type": "failover",
            },
        ])

        packet = packet_from_plan(
            plan,
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )

        self.assertEqual(packet["expected"]["selected_move_count"], 1)
        self.assertEqual(packet["expected"]["atomic_execution_envelope_id"], "aee-test")
        self.assertEqual(packet["expected"]["atomic_execution_envelope_hash"], "aee-hash-test")
        self.assertEqual(packet["expected"]["source_bundle_hash"], "source-bundle-hash-test")
        self.assertEqual(packet["constraints"]["selected_move_budget"], 1)
        self.assertEqual(packet["constraints"]["allowed_users"], ["10.7.0.11"])
        self.assertEqual(len(packet["rollback_manifest"]["items"]), 1)
        self.assertEqual(packet["rollback_manifest"]["items"][0]["user_ip"], "10.7.0.11")

    def test_nonzero_packet_rejects_generation_and_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            stale_plan = self.movement_plan()
            stale_plan["safety"]["generation"]["planner_generation_id"] = "stale-gen"
            stale_hash_plan = self.movement_plan()
            stale_hash_plan["safety"]["restore_barrier"]["clearance_selected_moves_hash"] = "other-hash"
            stale_envelope_plan = self.movement_plan()
            stale_envelope_plan["safety"]["atomic_execution_envelope"]["envelope_hash"] = "other-envelope-hash"

            stale_generation = runtime_recheck(packet, state, planner_snapshot=stale_plan)
            stale_hash = runtime_recheck(packet, state, planner_snapshot=stale_hash_plan)
            stale_envelope = runtime_recheck(packet, state, planner_snapshot=stale_envelope_plan)

        self.assertEqual(stale_generation["verdict"], "DENY_HASH_MISMATCH")
        self.assertIn("generation_id", stale_generation["errors"])
        self.assertEqual(stale_hash["verdict"], "DENY_HASH_MISMATCH")
        self.assertIn("selected_move_hash", stale_hash["errors"])
        self.assertEqual(stale_envelope["verdict"], "DENY_HASH_MISMATCH")
        self.assertIn("atomic_execution_envelope_hash", stale_envelope["errors"])

    def test_clearance_writer_rejects_duplicate_active_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            lifecycle = root / "lifecycle.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            write_json(
                barrier,
                {
                    "generation_clearance": True,
                    "allow_post_ttl_apply": True,
                    "clearance_expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                    "owner": "other-owner",
                },
            )
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )

        self.assertFalse(result["execution_allowed_now"])
        self.assertEqual(result["recheck"]["verdict"], "DENY_DUPLICATE_CLEARANCE_OWNER")
        self.assertIn("duplicate_clearance_owner", result["recheck"]["errors"])
        self.assertFalse(lifecycle.exists())

    def test_clearance_writer_allows_canonical_owner_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            audit = root / "audit.jsonl"
            lifecycle = root / "lifecycle.jsonl"
            barrier = state / "autoswitch-restore-barrier.json"
            write_json(
                barrier,
                {
                    "generation_clearance": True,
                    "allow_post_ttl_apply": True,
                    "clearance_expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
                    "clearance_generation_id": "old-gen",
                    "owner": CANONICAL_CLEARANCE_OWNER,
                },
            )
            packet = packet_from_plan(
                self.movement_plan(),
                approval_author="operator-a",
                approval_reviewer="operator-b",
            )
            result = execute_packet(
                packet,
                audit,
                state,
                mode="runtime_action",
                planner_snapshot=self.movement_plan(),
                restore_barrier_file=barrier,
                lifecycle_store=lifecycle,
            )
            refreshed = json.loads(barrier.read_text(encoding="utf-8"))
            backups = list(state.glob("autoswitch-restore-barrier.json.backup-c1-*"))

        self.assertTrue(result["execution_allowed_now"])
        self.assertEqual(result["record"]["clearance_verdict"], "RESTORE_BARRIER_CLEARANCE_WRITTEN")
        self.assertEqual(refreshed["clearance_generation_id"], "gen-move")
        self.assertEqual(refreshed["owner"], CANONICAL_CLEARANCE_OWNER)
        self.assertEqual(len(backups), 1)


if __name__ == "__main__":
    unittest.main()
