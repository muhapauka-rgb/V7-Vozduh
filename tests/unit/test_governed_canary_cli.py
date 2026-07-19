import importlib.machinery
import importlib.util
import json
import hashlib
import argparse
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


def load_cli_module():
    path = Path(__file__).resolve().parents[2] / "tools" / "v7-governed-canary-dry-run-cycle"
    loader = importlib.machinery.SourceFileLoader("v7_governed_canary_dry_run_cycle", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class GovernedCanaryCliTest(unittest.TestCase):
    def test_controlled_setup_keeps_operator_packet_approval_contract(self):
        module = load_cli_module()
        admission = {"authority": {"authority_basis": "OPERATOR_ENGINEERING_AUTHORITY"}}

        setup_authority = module.packet_materialization_authority(
            delegated_mode=False,
            setup_mode=True,
            delegated_admission=admission,
        )
        delegated_authority = module.packet_materialization_authority(
            delegated_mode=True,
            setup_mode=False,
            delegated_admission={"authority": {"authority_basis": "DELEGATED_AUTONOMY_POLICY"}},
        )

        self.assertIsNone(setup_authority)
        self.assertEqual(delegated_authority["authority_basis"], "DELEGATED_AUTONOMY_POLICY")

    def test_controlled_setup_admits_only_historical_dedicated_identity_and_empty_source(self):
        module = load_cli_module()
        selection = module.controlled_certification_setup_selection(
            users=[{"ip": "10.7.0.16", "current": "vless", "enabled": "1"}],
            egress=[{
                "id": "controlled-source",
                "enabled": "1",
                "controlled_certification_source": "1",
            }],
            user="10.7.0.16",
            source="controlled-source",
        )
        ordinary = module.controlled_certification_setup_selection(
            users=[{"ip": "10.0.0.2", "current": "vless", "enabled": "1"}],
            egress=[{
                "id": "controlled-source",
                "enabled": "1",
                "controlled_certification_source": "1",
            }],
            user="10.0.0.2",
            source="controlled-source",
        )

        self.assertEqual(selection["selection_status"], "SELECTED")
        self.assertEqual(selection["evidence_class"], "ENGINEERING_SETUP")
        self.assertFalse(selection["ordinary_customer_used"])
        self.assertEqual(ordinary["selection_status"], "STOP_SAFE")
        self.assertIn("identity_not_in_durable_legacy_certification_pool", ordinary["blockers"])

    def test_due_delayed_observation_is_owner_store_backed_and_idempotent(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "users.registry").write_text(
                "ip=10.7.0.16 current=vless table=1014 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            (state_dir / "egress.registry").write_text(
                "id=vless interface=tun0 enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "user-10.7.0.16.assign").write_text("egress=vless\n", encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb-delayed",
                "packet_id": "pkt-delayed",
                "decision_id": "decision-delayed",
                "decision_trace_id": "decision-delayed",
                "input_snapshot_identity": "snapshot-delayed",
                "closure_reference": "runtime-delayed",
                "user": "10.7.0.16",
                "source_channel": "awg3",
                "target_channel": "vless",
                "terminal_outcome_classification": "SUCCESS",
                "outcome_observed_at": "2026-07-19T00:00:00+00:00",
                "selected_moves": [{"user": "10.7.0.16", "from": "awg3", "to": "vless"}],
                "evidence_class": "CONTROLLED_PRODUCTION",
            }
            (state_dir / "execution-events.jsonl").write_text(
                json.dumps(outcome) + "\n", encoding="utf-8",
            )
            module.scoped_user_route_check = lambda _state, _user: {
                "passed": True, "returncode": 0, "reason": "unit",
            }
            now = datetime(2026, 7, 19, 1, 1, tzinfo=timezone.utc)

            first = module.materialize_due_delayed_observations(state_dir, now=now)
            second = module.materialize_due_delayed_observations(state_dir, now=now)

            self.assertEqual(first["observations_written"], 1)
            self.assertEqual(second["observations_written"], 0)
            rows = [json.loads(line) for line in (state_dir / "execution-events.jsonl").read_text().splitlines()]
            self.assertEqual(rows[-1]["schema_version"], "v7.execution-delayed-observation.v1")
            self.assertTrue(rows[-1]["delayed_1h_observation"])
            self.assertFalse(rows[-1]["runtime_mutation_performed"])

    def test_due_delayed_observation_reuses_operation_closure_as_missing_trace_identity(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "users.registry").write_text(
                "ip=10.7.0.16 current=vless table=1014 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            (state_dir / "egress.registry").write_text(
                "id=vless interface=tun0 enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "user-10.7.0.16.assign").write_text("egress=vless\n", encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb-operation-trace",
                "packet_id": "pkt-operation-trace",
                "decision_id": "execfb-operation-trace",
                "decision_trace_id": "",
                "input_snapshot_identity": "snapshot-operation-trace",
                "closure_reference": "govexec_operation_trace",
                "user": "10.7.0.16",
                "source_channel": "awg3",
                "target_channel": "vless",
                "terminal_outcome_classification": "SUCCESS",
                "outcome_observed_at": "2026-07-19T00:00:00+00:00",
                "selected_moves": [{"user": "10.7.0.16", "from": "awg3", "to": "vless"}],
                "evidence_class": "CONTROLLED_PRODUCTION",
            }
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            module.scoped_user_route_check = lambda _state, _user: {
                "passed": True, "returncode": 0, "reason": "unit",
            }

            result = module.materialize_due_delayed_observations(
                state_dir,
                now=datetime(2026, 7, 19, 1, 1, tzinfo=timezone.utc),
            )

            self.assertEqual(result["observations_written"], 1)
            self.assertEqual(result["written"][0]["decision_trace_id"], "govexec_operation_trace")

    def test_event_reader_consumes_actual_date_partitioned_owner_files(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            event_dir = Path(tmp)
            (event_dir / "telegram-sentinel-20260719.jsonl").write_text(
                json.dumps({"kind": "natural-sentinel"}) + "\n",
                encoding="utf-8",
            )
            (event_dir / "service-matrix-refresh-20260719.jsonl").write_text(
                json.dumps({"kind": "service-matrix"}) + "\n",
                encoding="utf-8",
            )
            rows = module.event_rows(event_dir, 5000)

        self.assertEqual({row["kind"] for row in rows}, {"natural-sentinel", "service-matrix"})

    def test_read_only_surface_gets_controlled_execution_source_binding(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            snapshot_root = state_dir / "intelligence"
            snapshot_root.mkdir(parents=True)
            for path, content in {
                state_dir / "users.registry": "ip=10.7.0.5 current=vless table=1005 enabled=1\n",
                state_dir / "egress.registry": "id=vless enabled=1\n",
                state_dir / "v7-state.json": '{"status":"ok"}\n',
                snapshot_root / "candidate-suitability-summary.json": '{"status":"fresh"}\n',
            }.items():
                path.write_text(content, encoding="utf-8")
            surface = {}

            binding = module.attach_controlled_execution_source_binding(
                surface,
                state_dir=state_dir,
                snapshot_root=snapshot_root,
            )

        self.assertEqual(binding["source_hashes"], {})
        self.assertFalse(binding["source_bundle_hash"])
        self.assertEqual(binding["snapshot_bundle_hash"], binding["source_bundle_hash"])
        self.assertEqual(surface["controlled_execution_source_hashes"], binding["source_hashes"])
        self.assertEqual(
            surface["controlled_execution_snapshot_bundle_hash"],
            binding["snapshot_bundle_hash"],
        )
        self.assertEqual(len(binding["raw_source_hashes"]), 4)
        self.assertTrue(surface["controlled_execution_source_materiality"]["fail_closed_without_selected_identity"])

    def test_selected_decision_binding_ignores_non_material_snapshot_metadata(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            snapshot_root = state_dir / "intelligence"
            snapshot_root.mkdir(parents=True)
            users_registry = state_dir / "users.registry"
            egress_registry = state_dir / "egress.registry"
            users_registry.write_text("ip=10.0.0.2 current=vless table=100 enabled=1\nip=10.0.0.9 current=awg0 table=109 enabled=1\n", encoding="utf-8")
            egress_registry.write_text("id=vless enabled=1\nid=awg3 enabled=1\nid=awg0 enabled=1\n", encoding="utf-8")
            runtime = {
                "updated": "2026-07-11T00:00:00Z",
                "users": [{"ip": "10.0.0.2", "current": "vless", "enabled": "1"}],
                "user_desired_state": [{"ip": "10.0.0.2", "current": "vless", "status": "OK"}],
                "egress": {
                    "vless": {"code": "200", "diagnose_reason": "OK", "diagnose_detail": "age=1", "load_status": "OK"},
                    "awg3": {"code": "200", "diagnose_reason": "OK", "diagnose_detail": "age=2", "load_status": "OK"},
                },
            }
            suitability = {
                "generated_at": "2026-07-11T00:00:00Z",
                "expires_at": "2026-07-11T00:02:00Z",
                "freshness_state": "FRESH",
                "items": [
                    {"user": "10.0.0.2", "runtime_decision_authority": "none_snapshot_only", "candidates": [
                        {"user": "10.0.0.2", "channel": "vless", "confidence": 0.4, "suitability_score": 70.0, "recommendation": "keep"},
                        {"user": "10.0.0.2", "channel": "awg3", "confidence": 0.5, "suitability_score": 80.0, "recommendation": "prefer"},
                    ]},
                    {"user": "10.0.0.9", "candidates": [{"channel": "awg0", "suitability_score": 1.0}]},
                ],
            }
            runtime_path = state_dir / "v7-state.json"
            suitability_path = snapshot_root / "candidate-suitability-summary.json"
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            suitability_path.write_text(json.dumps(suitability), encoding="utf-8")
            surface = {"batch_preview": {"users_to_move": [{"user": "10.0.0.2", "from": "vless", "to": "awg3", "confidence": 0.5}]}}
            first = module.attach_controlled_execution_source_binding(surface, state_dir=state_dir, snapshot_root=snapshot_root)

            runtime["updated"] = "2026-07-11T00:01:00Z"
            runtime["egress"]["awg3"]["diagnose_detail"] = "age=62"
            suitability["generated_at"] = "2026-07-11T00:01:00Z"
            suitability["expires_at"] = "2026-07-11T00:03:00Z"
            suitability["items"][1]["candidates"][0]["suitability_score"] = 99.0
            users_registry.write_text("ip=10.0.0.2 current=vless table=100 enabled=1\nip=10.0.0.9 current=awg3 table=109 enabled=1\n", encoding="utf-8")
            egress_registry.write_text("id=vless enabled=1\nid=awg3 enabled=1\nid=awg0 enabled=0\n", encoding="utf-8")
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            suitability_path.write_text(json.dumps(suitability), encoding="utf-8")
            second = module.attach_controlled_execution_source_binding(surface, state_dir=state_dir, snapshot_root=snapshot_root)

        self.assertEqual(first["source_hashes"], second["source_hashes"])
        self.assertNotEqual(first["raw_source_hashes"], second["raw_source_hashes"])

    def test_selected_decision_binding_ignores_score_churn_and_invalidates_categorical_safety_changes(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            snapshot_root = state_dir / "intelligence"
            snapshot_root.mkdir(parents=True)
            (state_dir / "users.registry").write_text("ip=10.0.0.2 current=vless table=100 enabled=1\n", encoding="utf-8")
            (state_dir / "egress.registry").write_text("id=vless enabled=1\nid=awg3 enabled=1\n", encoding="utf-8")
            runtime = {
                "users": [{"ip": "10.0.0.2", "current": "vless"}],
                "user_desired_state": [{"ip": "10.0.0.2", "current": "vless", "status": "OK"}],
                "egress": {"vless": {"code": "200", "load_status": "OK"}, "awg3": {"code": "200", "load_status": "OK"}},
            }
            suitability = {
                "freshness_state": "FRESH",
                "items": [{"user": "10.0.0.2", "runtime_decision_authority": "none_snapshot_only", "candidates": [
                    {"user": "10.0.0.2", "channel": "vless", "suitability_score": 70.0},
                    {"user": "10.0.0.2", "channel": "awg3", "suitability_score": 80.0},
                ]}],
            }
            runtime_path = state_dir / "v7-state.json"
            suitability_path = snapshot_root / "candidate-suitability-summary.json"
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            suitability_path.write_text(json.dumps(suitability), encoding="utf-8")
            surface = {"batch_preview": {"users_to_move": [{"user": "10.0.0.2", "from": "vless", "to": "awg3"}]}}
            first = module.attach_controlled_execution_source_binding(surface, state_dir=state_dir, snapshot_root=snapshot_root)
            (state_dir / "users.registry").write_text("ip=10.0.0.2 current=awg0 table=100 enabled=1\n", encoding="utf-8")
            identity_changed = module.attach_controlled_execution_source_binding(surface, state_dir=state_dir, snapshot_root=snapshot_root)
            (state_dir / "users.registry").write_text("ip=10.0.0.2 current=vless table=100 enabled=1\n", encoding="utf-8")
            suitability["items"][0]["candidates"][1]["suitability_score"] = 60.0
            suitability_path.write_text(json.dumps(suitability), encoding="utf-8")
            score_changed = module.attach_controlled_execution_source_binding(surface, state_dir=state_dir, snapshot_root=snapshot_root)
            suitability["items"][0]["candidates"][1]["recommendation"] = "reject"
            suitability_path.write_text(json.dumps(suitability), encoding="utf-8")
            recommendation_changed = module.attach_controlled_execution_source_binding(surface, state_dir=state_dir, snapshot_root=snapshot_root)
            runtime["egress"]["awg3"]["load_status"] = "BLOCKED"
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            safety_changed = module.attach_controlled_execution_source_binding(surface, state_dir=state_dir, snapshot_root=snapshot_root)

        self.assertNotEqual(first["source_hashes"]["users_registry"], identity_changed["source_hashes"]["users_registry"])
        self.assertEqual(first["source_hashes"]["candidate_suitability"], score_changed["source_hashes"]["candidate_suitability"])
        self.assertNotEqual(score_changed["source_hashes"]["candidate_suitability"], recommendation_changed["source_hashes"]["candidate_suitability"])
        self.assertNotEqual(recommendation_changed["source_hashes"]["runtime_state"], safety_changed["source_hashes"]["runtime_state"])

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

    def test_l3_validation_plan_passes_approved_source_to_planner(self):
        module = load_cli_module()
        captured = {}

        class FakeProc:
            returncode = 0
            stdout = "{}"
            stderr = ""

        def fake_run(command, **kwargs):
            captured["command"] = command
            return FakeProc()

        original_run = module.subprocess.run
        try:
            module.subprocess.run = fake_run
            module.run_l3_production_validation_plan(
                state_dir=Path("/state"),
                event_dir=Path("/events"),
                snapshot_root=Path("/state/intelligence"),
                restore_barrier_file=Path("/state/autoswitch-restore-barrier.json"),
                max_users=10,
                source="wireguard-1779454504-c43409",
            )
        finally:
            module.subprocess.run = original_run

        self.assertIn("--source-egress", captured["command"])
        source_index = captured["command"].index("--source-egress")
        self.assertEqual(captured["command"][source_index + 1], "wireguard-1779454504-c43409")

    def test_autoswitch_apply_timeout_scales_with_batch_size(self):
        module = load_cli_module()
        self.assertEqual(module.autoswitch_apply_timeout_seconds(1), 90)
        self.assertEqual(module.autoswitch_apply_timeout_seconds(10), 360)
        self.assertEqual(module.autoswitch_apply_timeout_seconds(100), 900)

    def test_l3_production_proof_counts_service_verify_failure_as_verification_failure(self):
        module = load_cli_module()
        proof = module.l3_production_validation_proof_quality(
            {"ok": True, "returncode": 0},
            {
                "apply_result": {
                    "applied": True,
                    "results": [
                        {
                            "user_ip": "10.7.0.18",
                            "from": "wireguard-1779454504-c43409",
                            "to": "vless",
                            "verify_rc": 0,
                            "service_verify_rc": 1,
                            "rollback_rc": 1,
                        }
                    ],
                },
                "operation": {"rollback_verdict": "ROLLBACK_FAILED"},
            },
        )

        self.assertFalse(proof["ok"])
        self.assertIn("verification_failed", proof["blockers"])
        self.assertIn("rollback_failed", proof["blockers"])
        self.assertEqual(proof["verified_success_count"], 0)
        self.assertEqual(proof["verification_failures"][0]["user_ip"], "10.7.0.18")

    def test_run_autoswitch_apply_uses_batch_aware_timeout(self):
        module = load_cli_module()
        captured = {}

        class FakeProc:
            returncode = 0
            stdout = "{}"
            stderr = ""

        def fake_run(command, **kwargs):
            captured["command"] = command
            captured["timeout"] = kwargs.get("timeout")
            return FakeProc()

        original_run = module.subprocess.run
        try:
            module.subprocess.run = fake_run
            result = module.run_autoswitch_apply(
                state_dir=Path("/state"),
                event_dir=Path("/events"),
                snapshot_root=Path("/state/intelligence"),
                restore_barrier_file=Path("/state/autoswitch-restore-barrier.json"),
                max_users=10,
                emergency_failover_autonomy=True,
                service_matrix_lock_timeout_sec=5,
            )
        finally:
            module.subprocess.run = original_run

        self.assertEqual(captured["timeout"], 360)
        self.assertEqual(result["timeout_seconds"], 360)
        self.assertIn("--emergency-failover-autonomy", captured["command"])
        timeout_index = captured["command"].index("--service-matrix-lock-timeout-sec")
        self.assertEqual(captured["command"][timeout_index + 1], "5")

    def test_l3_restore_barrier_preflight_reset_archives_completed_lock_when_lease_inactive(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            barrier_path = root / "autoswitch-restore-barrier.json"
            barrier = {
                "owner": module.operator_execution.CANONICAL_CLEARANCE_OWNER,
                "operation_id": "govexec-old",
                "clearance_expected_selected_moves": 5,
                "approved_plan_lock": {"lock_id": "apl-old"},
            }
            barrier_path.write_text(json.dumps(barrier), encoding="utf-8")

            result = module.reset_completed_restore_barrier_for_fresh_l3_validation(
                barrier_path,
                {"active": False, "status": "EXECUTION_FINISHED"},
            )
            current = json.loads(barrier_path.read_text(encoding="utf-8"))
            backup_exists = Path(result["backup_path"]).exists()

        self.assertTrue(result["reset_performed"])
        self.assertEqual(result["approved_operation_id"], "govexec-old")
        self.assertEqual(result["approved_selected_move_count"], 5)
        self.assertEqual(current, {})
        self.assertTrue(backup_exists)

    def test_l3_restore_barrier_preflight_reset_preserves_active_lease_lock(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            barrier_path = root / "autoswitch-restore-barrier.json"
            barrier = {
                "owner": module.operator_execution.CANONICAL_CLEARANCE_OWNER,
                "operation_id": "govexec-active",
                "approved_plan_lock": {"lock_id": "apl-active"},
            }
            barrier_path.write_text(json.dumps(barrier), encoding="utf-8")

            result = module.reset_completed_restore_barrier_for_fresh_l3_validation(
                barrier_path,
                {"active": True, "status": "ACTIVE"},
            )
            current = json.loads(barrier_path.read_text(encoding="utf-8"))

        self.assertFalse(result["reset_performed"])
        self.assertEqual(result["reason"], "active_execution_lease_preserves_restore_barrier")
        self.assertEqual(current["operation_id"], "govexec-active")

    def transaction_args(self, root: Path, *, open_control: bool = False):
        control_file = root / "safe-mode.json"
        now = datetime.now(timezone.utc)
        control_file.write_text(json.dumps({
            "schema_version": "v7.autonomous-execution-control.v2",
            "enabled": open_control,
            "state": "OPEN" if open_control else "CLOSED",
            "scope": "global",
            "generation": "aec_unit_test",
            "updated_at": now.isoformat(),
            "valid_until": "" if open_control else (now + timedelta(seconds=900)).isoformat(),
            "updated_by": "unit-test",
            "reason": "unit-test-open" if open_control else "unit-test-window",
            "rollback_policy": "CERTIFIED_ROLLBACK_ONLY",
        }), encoding="utf-8")
        source_hashes = {"users_registry": "users-hash", "egress_registry": "egress-hash"}
        source_hash = hashlib.sha256(json.dumps(source_hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
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
            execute_bounded_delegated_transaction=False,
            confirm_governed_transaction="EXECUTE_GOVERNED_TRANSACTION_APPROVED",
            execute_l3_production_validation=False,
            confirm_l3_production_validation="",
            committed_preview_file="",
            restore_barrier_file=str(root / "state" / "autoswitch-restore-barrier.json"),
            approval_author="operator-a",
            approval_reviewer="operator-b",
            ttl_seconds=600,
            pre_planner_refresh_command="v7-intelligence-snapshot-refresh",
            approved_packet_id="pkt_preview_test",
            approved_decision_id="decision_commit_test",
            approved_operation_id="govdry_test",
            approved_selected_move_hash="hash_test",
            approved_user="10.7.0.5",
            approved_source="vless",
            approved_target="awg3",
            approved_authority_generation="authgen_test",
            approved_breaker_generation="",
            approved_source_bundle_hash=source_hash,
            approved_source_hashes_hash=source_hash,
            approved_snapshot_bundle_hash="snapshot-bundle-test",
            execution_control_file=str(control_file),
            pretty=False,
        )

    def ready_cycle(self, *, user="10.7.0.5", source="vless", target="awg3"):
        preview = {
            "schema_version": "v7.governed-canary.packet-preview.v1",
            "status": "PACKET_PREVIEW_READY",
            "packet_id": "pkt_preview_test",
            "operation_id": "govdry_test",
            "decision_id": "decision_commit_test",
            "authority_generation": "authgen_test",
            "selected_move_hash": "hash_test",
            "selected_move_count": 1,
            "allowed_users": [user],
            "allowed_targets": [target],
            "source_hashes": {"users_registry": "users-hash", "egress_registry": "egress-hash"},
            "snapshot_bundle_hash": "snapshot-bundle-test",
            "rollback_manifest_preview": {
                "rollback_manifest_id": "rb_preview_test",
                "items": [
                    {
                        "user_ip": user,
                        "rollback_target": source,
                        "forward_target": target,
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

    def ready_l3_plan(self, *, user="10.7.0.5", source="vless", target="awg3", moves=None, authority_budget=None):
        if moves is None:
            moves = [{
                "user_ip": user,
                "current_egress": source,
                "recommended_egress": target,
                "move_type": "failover",
            }]
        authority_budget = authority_budget or {
            "current_allowed_user_budget": 1,
            "authority_class": "CANARY",
            "certified_authority_class": "CANARY",
        }
        return {
            "operation": {
                "runtime_snapshot_hash": "l3-runtime-snapshot",
            },
            "summary": {
                "execution_mode": "emergency_failover",
            },
            "safety": {
                "generation": {
                    "planner_generation_id": "l3-generation",
                },
                "atomic_execution_envelope": {
                    "schema_version": "v7.atomic-execution-envelope.v1",
                    "envelope_id": "aee-l3",
                    "envelope_hash": "aee-l3-hash",
                    "source_bundle_hash": "l3-source-bundle",
                    "source_bundle": {
                        "source_hashes": {
                            "users_registry": "users-hash",
                            "egress_registry": "egress-hash",
                        },
                    },
                    "snapshot_bundle_hash": "l3-snapshot-bundle",
                },
                "restore_barrier": {
                    "clearance_selected_moves_before_guard": len(moves),
                    "clearance_selected_moves_hash": "l3-selected-hash",
                    "approved_candidate_moves_before_guard": moves,
                },
                "emergency_failover_autonomy": {
                    "enabled": True,
                },
                "authority_budget_gate": authority_budget,
                "selected_moves_diagnostics": {
                    "emergency_failover_authorized": True,
                },
            },
            "decisions": [
                {
                    "user_ip": move["user_ip"],
                    "current_egress": move["current_egress"],
                    "recommended_egress": move["recommended_egress"],
                    "action": "switch",
                    "move_type": "failover",
                    "reason": "CURRENT_CHANNEL_FAILED",
                    "important_services": ["telegram"],
                    "candidates": [
                        {
                            "egress": move["recommended_egress"],
                            "safe_now": True,
                            "service_suitability": {
                                "required_services_ok": True,
                                "current_failures": [
                                    {"service": "telegram", "status": "fail"},
                                ],
                            },
                        }
                    ],
                }
                for move in moves
            ],
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
        (state / "execution-events.jsonl").write_text("", encoding="utf-8")
        (snapshot / "candidate-suitability-summary.json").write_text(
            json.dumps({
                "schema_version": "v7.intelligence.candidate-suitability-summary.v1",
                "generated_at": "2026-06-27T00:00:00+00:00",
                "expires_at": "2026-06-27T00:02:00+00:00",
                "freshness_state": "FRESH",
                "confidence": 0.9,
                "items": [],
                "source_hashes": {"test": "hash"},
            }),
            encoding="utf-8",
        )

    def fake_candidate_snapshot(self, items):
        return type("Snapshot", (), {"payload": {"items": items, "source_hashes": {"test": "hash"}}})()

    def test_execute_governed_transaction_completes_one_attempt_and_terminalizes_lease(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
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
                final_control = module.operator_execution.autonomous_execution_control_state(args.execution_control_file)
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
        self.assertEqual(result["safe_mode_final_state"], "OPEN")
        self.assertTrue(result["controlled_window_finalization"]["final_open"])
        self.assertEqual(final_control["state"], "OPEN")
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

    def test_bounded_delegated_transaction_needs_no_packet_identity_or_operator_confirmation(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
            args.execute_governed_transaction = False
            args.execute_bounded_delegated_transaction = True
            args.confirm_governed_transaction = ""
            args.approval_author = ""
            args.approval_reviewer = ""
            for field in (
                "approved_packet_id", "approved_decision_id", "approved_operation_id",
                "approved_selected_move_hash", "approved_user", "approved_source",
                "approved_target", "approved_authority_generation", "approved_source_bundle_hash",
                "approved_source_hashes_hash", "approved_snapshot_bundle_hash",
            ):
                setattr(args, field, "")
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
                        "operation": {"terminal_state": "APPLIED", "terminal_reason": "selected_moves_applied"},
                        "apply_result": {
                            "applied": True,
                            "results": [{"user_ip": "10.7.0.5", "from": "vless", "to": "awg3", "verify_rc": 0}],
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
        self.assertTrue(result["runtime_automation_enabled"])
        self.assertFalse(result["candidate_approval_required"])
        self.assertFalse(result["packet_approval_required"])
        self.assertTrue(result["delegated_policy_admission"]["allowed"])
        self.assertEqual(lease["packet"]["approvals"], [])
        self.assertEqual(
            lease["packet"]["delegated_policy_authority"]["authority_basis"],
            "DELEGATED_AUTONOMY_POLICY",
        )
        self.assertEqual(result["users_moved"], 1)
        self.assertEqual(result["safe_mode_final_state"], "OPEN")

    def test_materialized_feedback_classifies_rollback_completed_as_rollback_success(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir(parents=True)
            packet = {
                "packet_id": "pkt_preview_rollback",
                "decision_id": "decision_commit_rollback",
                "operation_id": "govdry_rollback",
                "expected": {"selected_move_hash": "hash_rollback"},
            }
            apply_result = {
                "applied": True,
                "results": [
                    {
                        "user_ip": "10.7.0.24",
                        "from": "vless",
                        "to": "awg3",
                        "verify_rc": 1,
                        "rollback_attempted": True,
                        "rollback_rc": 0,
                        "rollback_verdict": "ROLLBACK_COMPLETED",
                    }
                ],
            }
            result = module.materialize_governed_transaction_feedback(
                state_dir=state,
                packet=packet,
                operation={
                    "operation_id": "runtime_autoswitch_rollback",
                    "terminal_state": "ROLLED_BACK",
                    "terminal_reason": "verification_failed_rollback_completed",
                    "rollback_verdict": "ROLLBACK_COMPLETED",
                },
                apply_result=apply_result,
                user="10.7.0.24",
                source="vless",
                target="awg3",
                rollback_attempted=True,
                verification_passed=False,
            )
            outcome_rows = [
                json.loads(line)
                for line in (state / "execution-events.jsonl").read_text(encoding="utf-8").splitlines()
                if '"schema_version":"v7.execution-outcome-record.v1"' in line
                or '"schema_version": "v7.execution-outcome-record.v1"' in line
            ]
            recommendation_rows = [
                json.loads(line)
                for line in (state / "proposal-records.jsonl").read_text(encoding="utf-8").splitlines()
            ]

        self.assertTrue(result["materialized"])
        self.assertEqual(result["terminal_outcome_classification"], "ROLLBACK_SUCCESS")
        self.assertEqual(result["outcome_quality"], "ROLLBACK_SUCCESS")
        self.assertEqual(result["outcome_status"], "rollback_success")
        self.assertEqual(outcome_rows[0]["outcome_quality"]["outcome_quality"], "ROLLBACK_SUCCESS")
        self.assertEqual(outcome_rows[0]["terminal_outcome_classification"], "ROLLBACK_SUCCESS")
        self.assertLess(recommendation_rows[0]["delta"], 0)

    def test_execute_governed_transaction_requires_explicit_transaction_confirmation(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
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

    def test_l3_production_validation_requires_explicit_confirmation(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
            args.execute_l3_production_validation = True
            args.confirm_l3_production_validation = ""
            result = module.execute_l3_production_validation(
                args,
                state_dir=root / "state",
                event_dir=root / "events",
                snapshot_root=root / "state" / "intelligence",
                audit_dir=root / "audit",
                lease_file=root / "state" / "operator-execution-lease.json",
            )

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_STOPPED")
        self.assertEqual(result["stop_reason"], "l3_production_validation_confirmation_required")
        self.assertFalse(result["apply_executed"])

    def test_l3_production_validation_open_breaker_creates_one_operation_window(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
            args.execute_l3_production_validation = True
            args.confirm_l3_production_validation = "EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED"
            state = module.operator_execution.build_autonomous_execution_control_state(True, actor="owner", reason="incident")
            Path(args.execution_control_file).write_text(json.dumps(state), encoding="utf-8")
            original_plan = module.run_l3_production_validation_plan
            original_binding = module.operation_scoped_binding.read_binding
            try:
                module.run_l3_production_validation_plan = lambda **kwargs: {
                    "ok": True,
                    "returncode": 0,
                    "command": ["l3-plan"],
                    "payload": self.ready_l3_plan(),
                }
                module.operation_scoped_binding.read_binding = lambda **kwargs: {
                    "schema_version": module.operation_scoped_binding.SCHEMA_VERSION,
                    "status": "BOUND",
                    "selected_identity": {
                        "user": "10.7.0.5",
                        "source": "vless",
                        "target": "awg3",
                    },
                    "source_hashes": {
                        "users_registry": "users-binding",
                        "egress_registry": "egress-binding",
                        "runtime_state": "runtime-binding",
                        "candidate_suitability": "candidate-binding",
                    },
                    "source_bundle_hash": "binding-bundle",
                    "snapshot_bundle_hash": "binding-bundle",
                }
                result = module.execute_l3_production_validation(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.run_l3_production_validation_plan = original_plan
                module.operation_scoped_binding.read_binding = original_binding

        self.assertNotEqual(result.get("stop_reason"), "autonomous_execution_control_denied_pre_lease")
        self.assertEqual(result["safe_mode_final_state"], "OPEN")
        rebound_envelope = result["l3_plan_run"]["payload"]["safety"]["atomic_execution_envelope"]
        self.assertTrue(rebound_envelope["envelope_id"].startswith("aee_"))
        self.assertEqual(rebound_envelope["selected_move_count"], 1)

    def test_controlled_certification_scope_requires_both_existing_owner_markers(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "users.registry").write_text(
                "ip=10.7.0.16 current=vless enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            (state / "egress.registry").write_text(
                "id=controlled enabled=0 controlled_certification_source=1\n",
                encoding="utf-8",
            )

            admitted = module.controlled_certification_evidence_scope(
                state, user="10.7.0.16", source="controlled"
            )
            denied = module.controlled_certification_evidence_scope(
                state, user="10.7.0.17", source="controlled"
            )

        self.assertTrue(admitted)
        self.assertFalse(denied)

    def test_l3_production_validation_routes_through_pipeline_before_apply(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_l3_production_validation = True
            args.confirm_l3_production_validation = "EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED"
            apply_calls = []
            original_plan = module.run_l3_production_validation_plan
            original_apply = module.run_autoswitch_apply
            try:
                module.run_l3_production_validation_plan = lambda **kwargs: {
                    "ok": True,
                    "returncode": 0,
                    "command": ["l3-plan"],
                    "payload": self.ready_l3_plan(),
                }

                def fake_apply(**kwargs):
                    apply_calls.append(kwargs)
                    return {
                        "ok": True,
                        "returncode": 0,
                        "payload": {
                            "operation": {
                                "operation_id": "l3-runtime-apply",
                                "terminal_state": "SUCCESS",
                                "terminal_reason": "l3_validated",
                            },
                            "apply_result": {
                                "applied": True,
                                "results": [
                                    {"user_ip": "10.7.0.5", "from": "vless", "to": "awg3", "verify_rc": 0}
                                ],
                            },
                            "l3_learning_closure": {
                                "materialized": True,
                                "capability_state": {
                                    "production_proven": True,
                                    "certified": False,
                                    "active_capability": False,
                                },
                            },
                        },
                    }

                module.run_autoswitch_apply = fake_apply
                result = module.execute_l3_production_validation(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.run_l3_production_validation_plan = original_plan
                module.run_autoswitch_apply = original_apply

            barrier = json.loads((root / "state" / "autoswitch-restore-barrier.json").read_text(encoding="utf-8"))

        self.assertEqual(result["final_verdict"], "L3_PRODUCTION_PROVEN")
        self.assertEqual(result["transition"]["owner"], "admin_core/operator_execution_pipeline.py")
        self.assertTrue(result["restore_barrier_written_now"])
        self.assertTrue(result["apply_executed"])
        self.assertEqual(result["users_moved"], 1)
        self.assertTrue(result["production_proven"])
        self.assertFalse(result["runtime_automation_enabled"])
        self.assertFalse(result["authority_expanded"])
        self.assertEqual(barrier["allowed_users"], ["10.7.0.5"])
        self.assertEqual(barrier["allowed_targets"], ["awg3"])
        self.assertEqual(len(apply_calls), 1)
        self.assertEqual(apply_calls[0]["user"], "10.7.0.5")
        self.assertEqual(apply_calls[0]["source"], "vless")
        self.assertEqual(apply_calls[0]["target"], "awg3")
        self.assertTrue(apply_calls[0]["packet_id"])
        self.assertEqual(apply_calls[0]["operation_id"], result["operation_id"])
        self.assertEqual(apply_calls[0]["selected_move_hash"], result["selected_move_hash"])
        self.assertTrue(apply_calls[0]["authority_generation"])
        self.assertTrue(apply_calls[0]["source_bundle_hash"])
        self.assertEqual(apply_calls[0]["snapshot_bundle_hash"], "l3-snapshot-bundle")
        self.assertEqual(barrier["packet_id"], apply_calls[0]["packet_id"])
        self.assertEqual(barrier["operation_id"], apply_calls[0]["operation_id"])
        locked_move = barrier["approved_plan_lock"]["selected_moves"][0]
        self.assertEqual(locked_move["reason"], "CURRENT_CHANNEL_FAILED")
        self.assertEqual(locked_move["important_services"], ["telegram"])
        self.assertEqual(locked_move["candidates"][0]["egress"], "awg3")
        self.assertTrue(apply_calls[0]["emergency_failover_autonomy"])

    def test_l3_production_validation_resets_completed_barrier_before_fresh_batch_plan(self):
        module = load_cli_module()
        stale_moves = [
            {"user_ip": f"10.7.0.{idx}", "current_egress": "openvpn-old", "recommended_egress": "vless", "move_type": "failover"}
            for idx in range(2, 7)
        ]
        fresh_moves = [
            {"user_ip": f"10.7.0.{idx}", "current_egress": "openvpn-failed", "recommended_egress": "vless", "move_type": "failover"}
            for idx in range(16, 26)
        ]
        authority_budget = {
            "current_allowed_user_budget": 10,
            "authority_class": "MEDIUM_BATCH",
            "certified_authority_class": "MEDIUM_BATCH",
            "authority_lifecycle_state": "PROMOTED",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_l3_production_validation = True
            args.confirm_l3_production_validation = "EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED"
            args.max_users = 10
            stale_barrier = {
                "owner": module.operator_execution.CANONICAL_CLEARANCE_OWNER,
                "operation_id": "govexec-stale-five",
                "clearance_expected_selected_moves": 5,
                "approved_plan_lock": {"lock_id": "apl-stale-five", "selected_moves": stale_moves},
            }
            barrier_path = root / "state" / "autoswitch-restore-barrier.json"
            barrier_path.write_text(json.dumps(stale_barrier), encoding="utf-8")
            apply_calls = []
            original_plan = module.run_l3_production_validation_plan
            original_apply = module.run_autoswitch_apply
            try:
                def fake_plan(**kwargs):
                    self.assertEqual(json.loads(barrier_path.read_text(encoding="utf-8")), {})
                    return {
                        "ok": True,
                        "returncode": 0,
                        "command": ["l3-plan"],
                        "payload": self.ready_l3_plan(moves=fresh_moves, authority_budget=authority_budget),
                    }

                def fake_apply(**kwargs):
                    apply_calls.append(kwargs)
                    return {
                        "ok": True,
                        "returncode": 0,
                        "payload": {
                            "operation": {
                                "operation_id": "l3-runtime-medium-apply",
                                "terminal_state": "SUCCESS",
                                "terminal_reason": "l3_medium_batch_validated",
                            },
                            "apply_result": {
                                "applied": True,
                                "results": [
                                    {"user_ip": move["user_ip"], "from": move["current_egress"], "to": move["recommended_egress"], "rc": 0, "verify_rc": 0}
                                    for move in fresh_moves
                                ],
                            },
                            "l3_learning_closure": {
                                "materialized": True,
                                "capability_state": {
                                    "production_proven": True,
                                    "certified": False,
                                    "active_capability": False,
                                },
                            },
                        },
                    }

                module.run_l3_production_validation_plan = fake_plan
                module.run_autoswitch_apply = fake_apply
                result = module.execute_l3_production_validation(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.run_l3_production_validation_plan = original_plan
                module.run_autoswitch_apply = original_apply
            barrier = json.loads(barrier_path.read_text(encoding="utf-8"))

        self.assertEqual(result["final_verdict"], "L3_PRODUCTION_PROVEN")
        self.assertTrue(result["restore_barrier_preflight_reset"]["reset_performed"])
        self.assertEqual(result["transition"]["selected_move_count"], 10)
        self.assertEqual(result["users"], [move["user_ip"] for move in fresh_moves])
        self.assertEqual(result["users_moved"], 10)
        self.assertEqual(barrier["allowed_users"], [move["user_ip"] for move in fresh_moves])
        self.assertEqual(len(apply_calls), 1)
        self.assertEqual(apply_calls[0]["max_users"], 10)

    def test_l3_production_validation_rejects_learning_proven_when_verification_failed(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_l3_production_validation = True
            args.confirm_l3_production_validation = "EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED"
            original_plan = module.run_l3_production_validation_plan
            original_apply = module.run_autoswitch_apply
            try:
                module.run_l3_production_validation_plan = lambda **kwargs: {
                    "ok": True,
                    "returncode": 0,
                    "command": ["l3-plan"],
                    "payload": self.ready_l3_plan(),
                }

                def fake_apply(**kwargs):
                    return {
                        "ok": True,
                        "returncode": 0,
                        "payload": {
                            "operation": {
                                "operation_id": "l3-runtime-apply",
                                "terminal_state": "SUCCESS",
                                "terminal_reason": "learning_claimed_success",
                            },
                            "apply_result": {
                                "applied": True,
                                "results": [
                                    {
                                        "user_ip": "10.7.0.5",
                                        "from": "vless",
                                        "to": "awg3",
                                        "verify_rc": 1,
                                        "rollback_rc": 1,
                                    }
                                ],
                            },
                            "l3_learning_closure": {
                                "materialized": True,
                                "capability_state": {
                                    "production_proven": True,
                                    "certified": True,
                                    "active_capability": True,
                                },
                            },
                        },
                    }

                module.run_autoswitch_apply = fake_apply
                result = module.execute_l3_production_validation(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.run_l3_production_validation_plan = original_plan
                module.run_autoswitch_apply = original_apply

        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertEqual(result["transaction_status"], "STOP_SAFE")
        self.assertEqual(result["stop_reason"], "l3_production_validation_downstream_proof_failed")
        self.assertTrue(result["apply_executed"])
        self.assertFalse(result["production_proven"])
        self.assertEqual(result["verification_result"], "FAIL")
        self.assertEqual(result["users_moved"], 0)
        self.assertIn("verification_failed", result["production_proof_quality"]["blockers"])
        self.assertIn("rollback_failed", result["production_proof_quality"]["blockers"])

    def test_l3_production_validation_rejects_requested_batch_above_canary_budget(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_l3_production_validation = True
            args.confirm_l3_production_validation = "EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED"
            args.max_users = 5
            original_plan = module.run_l3_production_validation_plan
            try:
                module.run_l3_production_validation_plan = lambda **kwargs: {
                    "ok": True,
                    "returncode": 0,
                    "command": ["l3-plan"],
                    "payload": self.ready_l3_plan(),
                }
                result = module.execute_l3_production_validation(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.run_l3_production_validation_plan = original_plan

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_STOPPED")
        self.assertEqual(result["stop_reason"], "l3_production_validation_requested_users_above_authorized_budget")
        self.assertEqual(result["authorized_l3_budget"]["authorized_l3_budget"], 1)
        self.assertTrue(result["authorized_l3_budget"]["canary_default_preserved"])
        self.assertFalse(result["apply_executed"])

    def test_l3_production_validation_accepts_medium_budget_batch_without_single_user_override(self):
        module = load_cli_module()
        moves = [
            {"user_ip": f"10.7.0.{idx}", "current_egress": "openvpn-failed", "recommended_egress": "vless", "move_type": "failover"}
            for idx in range(2, 7)
        ]
        authority_budget = {
            "current_allowed_user_budget": 5,
            "authority_class": "SMALL_BATCH",
            "certified_authority_class": "SMALL_BATCH",
            "authority_lifecycle_state": "PROMOTED",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root)
            args.execute_l3_production_validation = True
            args.confirm_l3_production_validation = "EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED"
            args.max_users = 5
            apply_calls = []
            original_plan = module.run_l3_production_validation_plan
            original_apply = module.run_autoswitch_apply
            try:
                module.run_l3_production_validation_plan = lambda **kwargs: {
                    "ok": True,
                    "returncode": 0,
                    "command": ["l3-plan"],
                    "payload": self.ready_l3_plan(moves=moves, authority_budget=authority_budget),
                }

                def fake_apply(**kwargs):
                    apply_calls.append(kwargs)
                    return {
                        "ok": True,
                        "returncode": 0,
                        "payload": {
                            "operation": {
                                "operation_id": "l3-runtime-batch-apply",
                                "terminal_state": "SUCCESS",
                                "terminal_reason": "l3_batch_validated",
                            },
                            "apply_result": {
                                "applied": True,
                                "results": [
                                    {"user_ip": move["user_ip"], "from": move["current_egress"], "to": move["recommended_egress"], "rc": 0, "verify_rc": 0}
                                    for move in moves
                                ],
                            },
                            "l3_learning_closure": {
                                "materialized": True,
                                "capability_state": {
                                    "production_proven": True,
                                    "certified": False,
                                    "active_capability": False,
                                },
                            },
                        },
                    }

                module.run_autoswitch_apply = fake_apply
                result = module.execute_l3_production_validation(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                )
            finally:
                module.run_l3_production_validation_plan = original_plan
                module.run_autoswitch_apply = original_apply

        self.assertEqual(result["final_verdict"], "L3_PRODUCTION_PROVEN")
        self.assertEqual(result["authorized_l3_budget"]["authorized_l3_budget"], 5)
        self.assertEqual(result["transition"]["selected_move_count"], 5)
        self.assertEqual(result["users"], [move["user_ip"] for move in moves])
        self.assertEqual(result["users_moved"], 5)
        self.assertFalse(result["one_execution_attempt"])
        self.assertEqual(len(apply_calls), 1)
        self.assertEqual(apply_calls[0]["max_users"], 5)
        self.assertEqual(apply_calls[0]["user"], "")
        self.assertEqual(apply_calls[0]["source"], "")
        self.assertEqual(apply_calls[0]["target"], "")
        self.assertTrue(apply_calls[0]["packet_id"])
        self.assertTrue(apply_calls[0]["selected_move_hash"])

    def test_l3_packet_constraints_reject_selected_count_above_authorized_budget(self):
        module = load_cli_module()
        packet = {
            "constraints": {
                "allowed_users": ["10.7.0.2", "10.7.0.3", "10.7.0.4"],
                "allowed_targets": ["vless"],
            },
            "expected": {
                "selected_move_count": 3,
            },
        }
        transition = {
            "status": "READY",
            "selected_moves": [
                {"user_ip": "10.7.0.2", "current_egress": "openvpn-failed", "recommended_egress": "vless", "move_type": "failover"},
                {"user_ip": "10.7.0.3", "current_egress": "openvpn-failed", "recommended_egress": "vless", "move_type": "failover"},
                {"user_ip": "10.7.0.4", "current_egress": "openvpn-failed", "recommended_egress": "vless", "move_type": "failover"},
            ],
        }

        result = module.l3_packet_constraints_ok(packet, transition, 3, authorized_l3_budget=2)

        self.assertFalse(result["ok"])
        self.assertIn("l3_validation_requested_users_above_authorized_budget", result["errors"])
        self.assertIn("selected_move_count_above_authorized_budget", result["errors"])

    def test_l3_packet_constraints_accept_small_batch_five_users_with_small_budget(self):
        module = load_cli_module()
        moves = [
            {"user_ip": f"10.7.0.{idx}", "current_egress": "openvpn-failed", "recommended_egress": "vless", "move_type": "failover"}
            for idx in range(2, 7)
        ]
        packet = {
            "constraints": {
                "allowed_users": [move["user_ip"] for move in moves],
                "allowed_targets": ["vless"],
            },
            "expected": {
                "selected_move_count": 5,
            },
        }
        transition = {
            "status": "READY",
            "selected_moves": moves,
        }

        result = module.l3_packet_constraints_ok(packet, transition, 5, authorized_l3_budget=5)

        self.assertTrue(result["ok"])
        self.assertEqual(result["selected_move_count"], 5)
        self.assertEqual(result["authorized_l3_budget"], 5)

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

    def test_a4_bounded_evidence_collection_fails_closed_when_runtime_state_missing(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = self.transaction_args(root)
            args.execute_a4_bounded_evidence_collection = True
            args.confirm_a4_bounded_evidence_collection = "EXECUTE_A4_BOUNDED_EVIDENCE_COLLECTION_APPROVED"
            args.max_evidence_outcomes = 1
            result = module.execute_a4_bounded_evidence_collection(
                args,
                state_dir=root / "missing-state",
                event_dir=root / "missing-events",
                snapshot_root=root / "missing-state" / "intelligence",
                audit_dir=root / "missing-audit",
                lease_file=root / "missing-state" / "operator-execution-lease.json",
            )

        self.assertEqual(result["final_verdict"], "A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED")
        self.assertEqual(result["stop_reason"], "runtime_state_unavailable")
        self.assertEqual(result["transactions_attempted"], 0)
        self.assertFalse(result["runtime_state_available"])
        self.assertIn("missing_required_inputs", result["input_status"])
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

    def test_a4_goal_directed_selection_skips_non_missing_and_selects_missing_candidate(self):
        module = load_cli_module()
        surface = {
            "users_by_ip": {
                "10.7.0.5": {"current_channel": "awg0"},
                "10.7.0.8": {"current_channel": "vless"},
            },
            "batch_preview": {"users_to_move": [{"user": "10.7.0.5", "from": "awg0", "to": "vless"}]},
        }
        original_snapshot = module.read_snapshot_family
        try:
            module.read_snapshot_family = lambda *_args, **_kwargs: self.fake_candidate_snapshot([
                {
                    "user": "10.7.0.5",
                    "candidates": [
                        {"channel": "vless", "eligible": True, "suitability_score": 99, "confidence": 0.9},
                    ],
                },
                {
                    "user": "10.7.0.8",
                    "candidates": [
                        {"channel": "awg3", "eligible": True, "suitability_score": 80, "confidence": 0.7},
                    ],
                },
            ])
            selection = module.select_a4_gap_reducing_candidate(
                surface=surface,
                snapshot_root=Path("/unused"),
                required_a4_candidate_keys={("10.7.0.8", "awg3")},
            )
        finally:
            module.read_snapshot_family = original_snapshot

        self.assertEqual(selection["selection_status"], "SELECTED")
        self.assertEqual(selection["eligible_candidate_count"], 2)
        self.assertEqual(selection["gap_reducing_candidate_count"], 1)
        self.assertEqual(selection["selected_candidate"]["user"], "10.7.0.8")
        self.assertEqual(selection["selected_candidate"]["target"], "awg3")
        self.assertFalse(selection["runtime_automation_enabled"])
        self.assertFalse(selection["authority_expanded"])
        merged = module.merge_a4_gap_candidate_into_surface(surface, selection)
        self.assertEqual(merged["batch_preview"]["users_to_move"][0]["user"], "10.7.0.8")
        self.assertEqual(merged["batch_preview"]["users_to_move"][0]["to"], "awg3")

    def test_governed_transaction_stops_when_no_safe_gap_reducing_a4_candidate_exists(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
            original_surface = module.operator_decision_surface.build_operator_decision_surface
            original_snapshot = module.read_snapshot_family
            original_cycle = module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle
            try:
                module.operator_decision_surface.build_operator_decision_surface = lambda **_kwargs: {
                    "users_by_ip": {"10.7.0.5": {"current_channel": "vless"}},
                    "batch_preview": {"users_to_move": []},
                }
                module.read_snapshot_family = lambda *_args, **_kwargs: self.fake_candidate_snapshot([
                    {
                        "user": "10.7.0.5",
                        "candidates": [
                            {"channel": "awg3", "eligible": False, "suitability_score": 90, "confidence": 0.9},
                            {"channel": "vless", "eligible": True, "suitability_score": 80, "confidence": 0.8},
                        ],
                    }
                ])

                def fail_cycle(**_kwargs):
                    raise AssertionError("A4 selector must stop before packet cycle when no safe gap candidate exists")

                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = fail_cycle
                result = module.execute_governed_transaction_with_guards(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                    required_a4_candidate_keys={("10.7.0.5", "awg3")},
                )
                lease_exists = (root / "state" / "operator-execution-lease.json").exists()
                barrier_exists = (root / "state" / "autoswitch-restore-barrier.json").exists()
            finally:
                module.operator_decision_surface.build_operator_decision_surface = original_surface
                module.read_snapshot_family = original_snapshot
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = original_cycle

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_STOPPED")
        self.assertEqual(result["stop_reason"], "NO_SAFE_GAP_REDUCING_A4_CANDIDATE")
        self.assertEqual(result["a4_goal_directed_selection"]["missing_candidate_keys_count"], 1)
        self.assertEqual(result["a4_goal_directed_selection"]["gap_reducing_candidate_count"], 0)
        self.assertFalse(result["apply_executed"])
        self.assertFalse(lease_exists)
        self.assertFalse(barrier_exists)

    def test_governed_transaction_uses_gap_reducing_candidate_before_packet_cycle(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
            args.approved_user = "10.7.0.8"
            original_surface = module.operator_decision_surface.build_operator_decision_surface
            original_snapshot = module.read_snapshot_family
            original_cycle = module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle
            original_apply = module.run_autoswitch_apply
            try:
                module.operator_decision_surface.build_operator_decision_surface = lambda **_kwargs: {
                    "users_by_ip": {
                        "10.7.0.5": {"current_channel": "awg0"},
                        "10.7.0.8": {"current_channel": "vless"},
                    },
                    "batch_preview": {"users_to_move": [{"user": "10.7.0.5", "from": "awg0", "to": "vless"}]},
                }
                module.read_snapshot_family = lambda *_args, **_kwargs: self.fake_candidate_snapshot([
                    {
                        "user": "10.7.0.5",
                        "candidates": [
                            {"channel": "vless", "eligible": True, "suitability_score": 99, "confidence": 0.9},
                        ],
                    },
                    {
                        "user": "10.7.0.8",
                        "candidates": [
                            {"channel": "awg3", "eligible": True, "suitability_score": 75, "confidence": 0.7},
                        ],
                    },
                ])

                def cycle_from_surface(**kwargs):
                    move = kwargs["decision_surface"]["batch_preview"]["users_to_move"][0]
                    self.assertEqual(move["user"], "10.7.0.8")
                    self.assertEqual(move["to"], "awg3")
                    return self.ready_cycle(user=move["user"], source=move["from"], target=move["to"])

                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = cycle_from_surface
                module.run_autoswitch_apply = lambda **_kwargs: {
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
                                {"user_ip": "10.7.0.8", "from": "vless", "to": "awg3", "verify_rc": 0}
                            ],
                        },
                    },
                }
                result = module.execute_governed_transaction_with_guards(
                    args,
                    state_dir=root / "state",
                    event_dir=root / "events",
                    snapshot_root=root / "state" / "intelligence",
                    audit_dir=root / "audit",
                    lease_file=root / "state" / "operator-execution-lease.json",
                    required_a4_candidate_keys={("10.7.0.8", "awg3")},
                )
            finally:
                module.operator_decision_surface.build_operator_decision_surface = original_surface
                module.read_snapshot_family = original_snapshot
                module.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle = original_cycle
                module.run_autoswitch_apply = original_apply

        self.assertEqual(result["final_verdict"], "GOVERNED_TRANSACTION_COMPLETED")
        self.assertEqual(result["user"], "10.7.0.8")
        self.assertEqual(result["target"], "awg3")
        self.assertEqual(result["a4_goal_directed_selection"]["selection_status"], "SELECTED")
        self.assertEqual(result["a4_goal_directed_selection"]["selected_candidate"]["target"], "awg3")
        self.assertFalse(result["runtime_automation_enabled"])
        self.assertFalse(result["authority_expanded"])

    def test_governed_transaction_stops_before_apply_for_duplicate_candidate(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
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

    def test_fresh_planner_result_replaces_stale_surface_candidate(self):
        module = load_cli_module()
        surface = {
            "users_by_ip": {"10.7.0.5": {"current_channel": "vless"}},
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.7.0.5", "from": "vless", "to": "awg0"}
                ]
            },
        }

        refreshed = module.merge_planner_moves_into_surface(
            surface,
            [],
            replace_existing=True,
        )

        self.assertEqual(refreshed["batch_preview"]["users_to_move"], [])
        self.assertTrue(refreshed["batch_preview"]["planner_observe_authoritative"])
        self.assertFalse(refreshed["batch_preview"]["stale_snapshot_candidates_retained"])

    def test_governed_transaction_stops_before_apply_when_no_gap_directed_candidate_is_available(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_transaction_state(root)
            args = self.transaction_args(root, open_control=True)
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
        self.assertEqual(result["stop_reason"], "NO_SAFE_GAP_REDUCING_A4_CANDIDATE")
        self.assertEqual(result["a4_goal_directed_selection"]["selection_status"], "NO_SAFE_GAP_REDUCING_A4_CANDIDATE")
        self.assertFalse(lease_exists)
        self.assertFalse(barrier_exists)


if __name__ == "__main__":
    unittest.main()
