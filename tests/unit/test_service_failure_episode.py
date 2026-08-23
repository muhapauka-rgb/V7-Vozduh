import contextlib
import importlib.machinery
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"
AUTOSWITCH_TOOL = ROOT / "tools" / "v7-users-autoswitch"
REFRESH_TOOL = ROOT / "tools" / "v7-service-matrix-refresh-all"
CYCLE_TOOL = ROOT / "tools" / "v7-governed-canary-dry-run-cycle"
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_module(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ServiceFailureEpisodeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_module("v7_service_matrix_episode", MATRIX_TOOL)
        cls.autoswitch = load_module("v7_users_autoswitch_episode", AUTOSWITCH_TOOL)
        cls.refresh = load_module("v7_service_matrix_refresh_episode", REFRESH_TOOL)
        cls.cycle = load_module("v7_governed_cycle_episode", CYCLE_TOOL)

    def test_exact_service_subset_reuses_existing_parallel_probe_owner(self):
        selected = self.matrix.exact_services_to_run(
            "all", "telegram,google,telegram"
        )
        self.assertEqual(selected, ["telegram", "google"])
        with self.assertRaisesRegex(ValueError, "invalid_service_subset"):
            self.matrix.exact_services_to_run("all", "telegram,unknown")

    def test_matrix_observation_only_stops_before_event_and_downstream_consumers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            (state_dir / "egress.registry").write_text(
                "id=vless interface=tun0 enabled=1 state=enabled\n",
                encoding="utf-8",
            )
            argv = [
                str(REFRESH_TOOL), "--state-dir", str(state_dir),
                "--event-dir", str(root / "events"),
                "--matrix-observation-only", "--egresses", "vless",
                "--services", "telegram",
            ]
            output = io.StringIO()
            observed_calls = []

            def fake_run_one(*_args, **_kwargs):
                observed_calls.append(True)
                return {
                    "egress": "vless", "status": "OK", "ok": True,
                    "total": 1, "service_results": {
                        "telegram": {"ok": True, "status": "OK"},
                    },
                    "service_matrix_lock": {"held": True},
                }

            with mock.patch.object(self.refresh, "run_one", side_effect=fake_run_one), \
                 mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                self.assertEqual(self.refresh.main(), 0)

        payload = json.loads(output.getvalue())
        self.assertEqual(len(observed_calls), 1)
        self.assertEqual(payload["mode"], "MATRIX_OBSERVATION_ONLY")
        self.assertTrue(payload["observation_only"]["canonical_matrix_write_preserved"])
        self.assertFalse(payload["observation_only"]["downstream_consumer_invoked"])
        self.assertFalse(payload["observation_only"]["routing_mutation_performed"])

    def test_controlled_persistence_override_is_forwarded_with_the_existing_event_owner(self):
        calls = []

        def fake_run(*args, **kwargs):
            calls.append((args, kwargs))
            return SimpleNamespace(returncode=0, stdout='{"status":"OK"}')

        with mock.patch.object(self.refresh.subprocess, "run", side_effect=fake_run):
            result = self.refresh.run_one(
                "wgfast", 3, "checker", Path("/state"), "google",
                failure_persistence_samples=1,
                failure_persistence_window_seconds=60,
                event_dir=Path("/controlled-events"),
            )

        self.assertTrue(result["ok"])
        command = calls[0][0][0]
        self.assertIn("--failure-persistence-samples", command)
        self.assertIn("--failure-persistence-window-seconds", command)
        self.assertEqual(command[command.index("--event-dir") + 1], "/controlled-events")

    def test_controlled_persistence_override_requires_shadow_observation_mode(self):
        argv = [
            str(REFRESH_TOOL), "--shadow-failure-persistence-samples", "1",
        ]
        output = io.StringIO()
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            self.assertEqual(self.refresh.main(), 2)
        self.assertEqual(
            json.loads(output.getvalue())["error"],
            "shadow_persistence_override_requires_observation_only_shadow_trigger",
        )

    def test_probe_observation_only_does_not_create_a_second_matrix_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            (state_dir / "egress.registry").write_text(
                "id=wgfast interface=tun0 enabled=1\n", encoding="utf-8"
            )
            matrix_file = root / "ephemeral-matrix.json"
            argv = [
                str(MATRIX_TOOL), "wgfast", "all", "--services", "google",
                "--state-dir", str(state_dir), "--matrix-file", str(matrix_file),
                "--probe-observation-only",
            ]
            output = io.StringIO()
            probe_result = {"ok": True, "status": "OK", "elapsed_sec": 0.001}
            with mock.patch.object(self.matrix, "interface_live", return_value=True), \
                 mock.patch.object(self.matrix, "run_service", return_value=probe_result), \
                 mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                self.assertEqual(self.matrix.main(), 0)

        payload = json.loads(output.getvalue())
        self.assertEqual(payload["service_matrix_lock"]["scope"], "probe_observation_only_no_matrix_write")
        self.assertFalse(matrix_file.exists())

    def test_matrix_runtime_caller_passes_comparison_only_to_existing_advisory_owner(self):
        command = []

        def fake_run(argv, **_kwargs):
            command.extend(argv)
            return subprocess.CompletedProcess(argv, 0, stdout=json.dumps({"ok": True}))

        with mock.patch.object(self.refresh.subprocess, "run", side_effect=fake_run):
            result = self.refresh.run_service_failure_automation_advisory(
                "existing-autoswitch", state_dir=Path("/polygon/state"),
                event_dir=Path("/polygon/events"), matrix_comparative_preflight=True,
            )

        self.assertTrue(result["ok"])
        self.assertEqual(command[0], "existing-autoswitch")
        self.assertIn("--consume-service-failure-automation-only", command)
        self.assertIn("--matrix-comparative-preflight", command)
        self.assertNotIn("--apply", command)

    def test_active_ordinary_stop_safe_defers_certification_tail(self):
        active_scope = {"active": True}
        stop_safe = {
            "status": "STOP_SAFE_CURRENT_INCIDENT_NOT_ACTIONABLE",
            "action_completed": False,
        }
        self.assertTrue(self.refresh.should_defer_certification_tail(
            event_only=False,
            current_scope=active_scope,
            bounded_action=stop_safe,
        ))
        self.assertFalse(self.refresh.should_defer_certification_tail(
            event_only=False,
            current_scope={"active": False},
            bounded_action=stop_safe,
        ))
        self.assertFalse(self.refresh.should_defer_certification_tail(
            event_only=False,
            current_scope=active_scope,
            bounded_action={"status": "ACTION_COMPLETED", "action_completed": True},
        ))

    def test_ct_m0f_standing_matrix_consumer_resets_then_reenters(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            audit = root / "audit" / "operator-execution-audit.jsonl"
            policy = root / "policy.json"
            state.mkdir(parents=True)
            events.mkdir(parents=True)
            audit.parent.mkdir(parents=True)
            policy.write_text("{}\n", encoding="utf-8")
            request = self.refresh.operator_execution.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=self.refresh.operator_execution.sha256_file(policy),
                now=now,
            )
            self.refresh.operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            activated = self.refresh.operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=self.refresh.operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            reservation = self.refresh.operator_execution.reserve_ct_m0f_standing_validation_sample(
                policy,
                implementation_fingerprint="f" * 64,
                validation_generation_id="ctm0fgen_one",
                packet_id="packet-one",
                operation_id="operation-one",
                lease_id="lease-one",
                user="10.7.0.18",
                source="vless",
                target="awg0",
                audit_store=audit,
                now=now + timedelta(seconds=3),
            )["reservation"]
            evidence = {
                "status": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS",
                "sample_kind": "cold",
                "validation_generation_id": "ctm0fgen_one",
                "metrics": {"control_plane_and_kernel_path_cutover_latency_ms": 100.0},
            }
            self.refresh.operator_execution.record_ct_m0f_standing_validation_forward_evidence(
                reservation_id=reservation["reservation_id"],
                sample_evidence=evidence,
                audit_store=audit,
                now=now + timedelta(seconds=4),
            )
            calls = []

            def fake_run(command, **_kwargs):
                calls.append(command)
                if "--ct-m0f-standing-source-selection" in command:
                    payload = {
                        "status": "CT_M0F_STANDING_CONTROLLED_FAILURE_READY",
                        "ok": True,
                        "selection_mode": "EXECUTE_CONTROLLED_FAILURE_CUTOVER",
                        "selected_source_id": "vless",
                        "selected_user": "10.7.0.18",
                        "selected_target_id": "awg0",
                        "sample_binding_fingerprint": "b" * 64,
                    }
                    return self.refresh.subprocess.CompletedProcess(
                        command, 0, stdout=json.dumps(payload)
                    )
                if "--reset-ct-m0f-standing-validation-sample" in command:
                    self.refresh.operator_execution.record_ct_m0f_standing_validation_sample_terminal(
                        reservation_id=reservation["reservation_id"],
                        sample_valid=True,
                        sample_evidence=evidence,
                        terminal_reason="verified_cutover_and_baseline_reset_complete",
                        audit_store=audit,
                        now=now + timedelta(seconds=5),
                    )
                    budget = self.refresh.operator_execution.ct_m0f_standing_validation_budget_status(
                        activated["contract"],
                        "f" * 64,
                        audit_records=self.refresh.operator_execution.read_audit_records(audit),
                    )
                    payload = {
                        "final_verdict": "CT_M0F_STANDING_SAMPLE_RESET_AND_CLOSED",
                        "budget": budget,
                        "runtime_mutation_performed": True,
                    }
                    return self.refresh.subprocess.CompletedProcess(command, 0, stdout=json.dumps(payload))
                payload = {
                    "final_verdict": "STOP_SAFE",
                    "stop_reason": "no_current_controlled_sample_candidate",
                    "runtime_mutation_performed": False,
                    "users_moved": 0,
                }
                return self.refresh.subprocess.CompletedProcess(command, 2, stdout=json.dumps(payload))

            with mock.patch.object(self.refresh.subprocess, "run", side_effect=fake_run):
                result = self.refresh.run_ct_m0f_standing_validation_campaign(
                    "governed-executor",
                    "existing-planner",
                    state_dir=state,
                    event_dir=events,
                    policy_file=policy,
                    audit_store=audit,
                    max_successive_samples=2,
                )

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["status"],
            "CT_M0F_SAMPLE_CLOSED_NEXT_ORDINARY_MATRIX_GENERATION_REQUIRED",
        )
        self.assertEqual(len(calls), 1)
        self.assertIn("--reset-ct-m0f-standing-validation-sample", calls[0])
        self.assertNotIn("--ct-m0f-standing-source-selection", calls[0])
        self.assertEqual(
            result["durable_successor"],
            "NEXT_ORDINARY_MATRIX_GENERATION_PREPARES_FRESH_SAMPLE",
        )
        receipt = result["sample_preparation_receipt"]
        self.assertEqual(receipt["phase"], "ACTIVE_SAMPLE_CLOSURE")
        self.assertEqual(
            receipt["predicates"]["previous_sample_closure"]["state"], "PASS"
        )
        self.assertEqual(
            receipt["predicates"]["fresh_candidate_admission"]["state"],
            "NOT_EVALUATED",
        )

    def test_ct_m0f_standing_matrix_prepares_condition_then_waits_for_fresh_generation(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            audit = root / "audit" / "operator-execution-audit.jsonl"
            policy = root / "policy.json"
            state.mkdir(parents=True)
            events.mkdir(parents=True)
            audit.parent.mkdir(parents=True)
            policy.write_text("{}\n", encoding="utf-8")
            request = self.refresh.operator_execution.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=self.refresh.operator_execution.sha256_file(policy),
                now=now,
            )
            self.refresh.operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            self.refresh.operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=self.refresh.operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )
            calls = []

            def fake_run(command, **_kwargs):
                calls.append(command)
                if "--ct-m0f-standing-source-selection" in command:
                    payload = {
                        "status": "CT_M0F_STANDING_CONTROLLED_FAILURE_PREPARATION_READY",
                        "ok": True,
                        "selection_mode": "PREPARE_CONTROLLED_FAILURE_CONDITION",
                        "selected_source_id": "exec-source",
                        "selected_user": "10.7.0.18",
                        "selected_target_id": "vless",
                        "sample_binding_fingerprint": "b" * 64,
                    }
                else:
                    payload = {
                        "final_verdict": "CT_M0F_STANDING_CONTROLLED_CONDITION_PREPARED",
                        "runtime_mutation_performed": True,
                        "users_moved": 1,
                    }
                return self.refresh.subprocess.CompletedProcess(
                    command, 0, stdout=json.dumps(payload)
                )

            with mock.patch.object(self.refresh.subprocess, "run", side_effect=fake_run):
                result = self.refresh.run_ct_m0f_standing_validation_campaign(
                    "governed-executor",
                    "existing-planner",
                    state_dir=state,
                    event_dir=events,
                    policy_file=policy,
                    audit_store=audit,
                )

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["status"],
            "CT_M0F_CONTROLLED_CONDITION_PREPARED_WAITING_FRESH_MATRIX_GENERATION",
        )
        self.assertIn("--prepare-ct-m0f-standing-controlled-condition", calls[1])
        self.assertNotIn("--execute-l3-production-validation", calls[1])
        self.assertEqual(result["durable_successor"], "NEXT_ORDINARY_MATRIX_GENERATION_DETECTS_CONTROLLED_FAILURE")
        self.assertEqual(
            result["sample_preparation_receipt"]["next_required_consumer"],
            "next ordinary Matrix generation",
        )

    def test_ct_m0f_no_sample_admission_retains_predicate_receipt_in_matrix_projection(self):
        now = datetime(2026, 8, 6, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            audit = root / "audit" / "operator-execution-audit.jsonl"
            policy = root / "policy.json"
            state.mkdir(parents=True)
            events.mkdir(parents=True)
            audit.parent.mkdir(parents=True)
            policy.write_text("{}\n", encoding="utf-8")
            request = self.refresh.operator_execution.build_ct_m0f_standing_validation_authority_request(
                policy_generation_hash=self.refresh.operator_execution.sha256_file(policy),
                now=now,
            )
            self.refresh.operator_execution.register_ct_m0f_standing_validation_authority_request(
                request, audit_store=audit, now=now + timedelta(seconds=1),
            )
            self.refresh.operator_execution.issue_ct_m0f_standing_validation_policy_from_audit(
                policy,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision=self.refresh.operator_execution.CT_M0F_STANDING_VALIDATION_APPROVAL,
                actor_id="independent-authority-test",
                audit_store=audit,
                now=now + timedelta(seconds=2),
            )

            def fake_run(command, **_kwargs):
                if "--ct-m0f-standing-source-selection" in command:
                    payload = {
                        "status": "CT_M0F_STANDING_CONTROLLED_FAILURE_READY",
                        "ok": True,
                        "selection_mode": "EXECUTE_CONTROLLED_FAILURE_CUTOVER",
                        "selected_source_id": "vless",
                        "selected_user": "10.7.0.18",
                        "selected_target_id": "awg0",
                        "sample_binding_fingerprint": "b" * 64,
                    }
                    return self.refresh.subprocess.CompletedProcess(command, 0, stdout=json.dumps(payload))
                payload = {
                    "final_verdict": "STOP_SAFE",
                    "stop_reason": "l3_production_validation_transition_blocked",
                    "runtime_mutation_performed": False,
                    "users_moved": 0,
                    "l3_plan_run": {"ok": False},
                }
                return self.refresh.subprocess.CompletedProcess(command, 2, stdout=json.dumps(payload))

            with mock.patch.object(self.refresh.subprocess, "run", side_effect=fake_run):
                result = self.refresh.run_ct_m0f_standing_validation_campaign(
                    "governed-executor",
                    "existing-planner",
                    state_dir=state,
                    event_dir=events,
                    policy_file=policy,
                    audit_store=audit,
                )
            projection = self.refresh.compact_refresh_projection({
                "ct_m0f_standing_validation_campaign": result,
            })

        self.assertEqual(result["status"], "STOP_SAFE_NO_SAMPLE_ADMITTED")
        receipt = result["sample_preparation_receipt"]
        self.assertEqual(receipt["phase"], "FRESH_SAMPLE_EXECUTION")
        self.assertEqual(
            receipt["predicates"]["fresh_candidate_admission"]["state"],
            "NOT_YET_ADMITTED",
        )
        compact = projection["ct_m0f_standing_validation_campaign"]
        self.assertEqual(compact["status"], "STOP_SAFE_NO_SAMPLE_ADMITTED")
        self.assertEqual(
            compact["consumer_result"]["ct_m0f_sample_preparation"]["predicates"]
            ["fresh_packet"]["state"],
            "NOT_YET_MATERIALIZED",
        )

    def test_ct_m0f_condition_effect_publishes_durable_audit_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            audit_dir = root / "audit"
            state.mkdir()
            events.mkdir()
            audit_dir.mkdir()
            policy = root / "policy.json"
            contract = {
                "contract_id": "contract",
                "contract_hash": "a" * 64,
            }
            policy.write_text(json.dumps({
                self.cycle.operator_execution.CT_M0F_STANDING_VALIDATION_POLICY_KEY: contract,
            }), encoding="utf-8")
            args = SimpleNamespace(
                policy_file=str(policy),
                ct_m0f_standing_validation_contract_id="contract",
                ct_m0f_standing_validation_contract_hash="a" * 64,
                ct_m0f_standing_validation_user="10.7.0.18",
                ct_m0f_standing_validation_target="vless",
                ct_m0f_standing_sample_binding_fingerprint="b" * 64,
                approved_source="exec-source",
                egress_state_owner="v7-egress-set-state",
            )
            selection = {
                "ok": True,
                "selection_mode": "PREPARE_CONTROLLED_FAILURE_CONDITION",
                "selected_user": "10.7.0.18",
                "selected_source_id": "exec-source",
                "selected_target_id": "vless",
                "sample_binding_fingerprint": "b" * 64,
            }

            def fake_run(command, **_kwargs):
                payload = json.dumps(selection) if "--ct-m0f-standing-source-selection" in command else "condition applied"
                return self.cycle.subprocess.CompletedProcess(command, 0, stdout=payload)

            with mock.patch.object(
                self.cycle.operator_execution,
                "validate_ct_m0f_standing_validation_policy",
                return_value={"ok": True, "errors": []},
            ), mock.patch.object(
                self.cycle,
                "prepare_controlled_certification_condition",
                return_value={"final_verdict": "CONTROLLED_CERTIFICATION_CONDITION_PREPARED"},
            ), mock.patch.object(
                self.cycle.subprocess,
                "run",
                side_effect=fake_run,
            ):
                result = self.cycle.prepare_ct_m0f_standing_controlled_condition(
                    args,
                    state_dir=state,
                    event_dir=events,
                    snapshot_root=state / "intelligence",
                    audit_dir=audit_dir,
                    lease_file=state / "lease.json",
                )

            records = self.cycle.operator_execution.read_audit_records(
                audit_dir / "operator-execution-audit.jsonl"
            )

        self.assertEqual(
            result["final_verdict"],
            "CT_M0F_STANDING_CONTROLLED_CONDITION_PREPARED",
        )
        self.assertEqual(records[-1]["record_type"], "ct_m0f_standing_controlled_condition_prepared")
        self.assertEqual(records[-1]["next_required_consumer"], "ordinary fresh Matrix generation")
        self.assertGreater(
            int(records[-1]["first_failed_observation_monotonic_ns"]),
            0,
        )
        self.assertEqual(
            records[-1]["first_failed_observation_monotonic_ns"],
            records[-1]["confirmed_hard_failure_monotonic_ns"],
        )

    def test_ct_m0f_standing_source_selection_reuses_controlled_pool_owner(self):
        pool = {
            "active_source_projections": [
                {
                    "source_id": "unhealthy",
                    "certification_group": "g1",
                    "enabled_certification_users_on_source": 50,
                    "group_aligned_certification_users_on_source": 50,
                    "enabled_non_certification_users_on_source": 1,
                    "source_isolated_for_controlled_failure": False,
                    "baseline_health": {"ok": False},
                },
                {
                    "source_id": "exec-source",
                    "certification_group": "g1",
                    "enabled_certification_users_on_source": 0,
                    "group_aligned_certification_users_on_source": 0,
                    "enabled_non_certification_users_on_source": 0,
                    "source_isolated_for_controlled_failure": True,
                    "baseline_health": {
                        "ok": True,
                        "observation_fingerprint": "exec-health",
                    },
                },
                {
                    "source_id": "vless",
                    "certification_group": "g1",
                    "enabled_certification_users_on_source": 41,
                    "group_aligned_certification_users_on_source": 41,
                    "enabled_non_certification_users_on_source": 0,
                    "source_isolated_for_controlled_failure": True,
                    "baseline_health": {
                        "ok": True,
                        "observation_fingerprint": "fresh-health",
                    },
                },
                {
                    "source_id": "mixed",
                    "certification_group": "g1",
                    "enabled_certification_users_on_source": 45,
                    "group_aligned_certification_users_on_source": 45,
                    "enabled_non_certification_users_on_source": 1,
                    "source_isolated_for_controlled_failure": False,
                    "baseline_health": {"ok": True},
                },
            ]
        }
        args = SimpleNamespace(state_dir="/unused")
        with mock.patch.object(
            self.autoswitch,
            "controlled_certification_pool_status",
            return_value=pool,
        ), mock.patch.object(
            self.autoswitch,
            "parse_registry",
            side_effect=lambda path: ([{
                "ip": "10.7.0.18",
                "current": "vless",
                "enabled": "1",
                "certification_user": "1",
                "certification_group": "g1",
            }] if str(path).endswith("users.registry") else [{
                "id": "exec-source",
                "role": "EXECUTION_ONLY",
                "reservation_owner": "operator_execution_governance",
                "execution_reserved": "1",
            }]),
        ), mock.patch.object(
            self.autoswitch,
            "controlled_campaign_target_selection_diagnostic",
            return_value={
                "selection": {"selected_target_id": "awg0"},
                "targets": [{
                    "target_id": "awg0",
                    "full_live_admission": False,
                    "controlled_rebind_eligible": True,
                    "controlled_only_contract": True,
                    "ordinary_planner_eligible": False,
                    "shared_target_technically_eligible": True,
                    "current_stage_feasible": True,
                    "verification_supported": True,
                    "rollback_containment_supported": True,
                    "role": "EXECUTION_ONLY",
                    "reservation_owner": "operator_execution_governance",
                    "health": {"ok": True},
                    "capacity": {"target_safe_additional_capacity": 1},
                    "semantic_fingerprint": "target-fingerprint",
                }],
            },
        ):
            result = self.autoswitch.ct_m0f_standing_source_selection_only(args)

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["selection_mode"],
            "PREPARE_CONTROLLED_FAILURE_CONDITION",
        )
        self.assertEqual(result["selected_source_id"], "exec-source")
        self.assertEqual(result["selected_user"], "10.7.0.18")
        self.assertEqual(result["selected_target_id"], "vless")
        self.assertTrue(
            result["selected_target_admission"]["controlled_contract_admitted"]
        )
        self.assertFalse(
            result["selected_target_admission"]["ordinary_full_live_admission"]
        )
        self.assertEqual(len(result["sample_binding_fingerprint"]), 64)
        self.assertEqual(result["eligible_source_count"], 1)
        self.assertFalse(result["forbidden_effects"]["runtime_apply"])

    def test_ct_m0f_active_service_failure_binding_requires_accounted_live_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {
                    "passive_example": {
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "incident_id": "sfinc_example",
                        "incident_generation": "egid_example",
                        "incident_state": "OPEN",
                        "channel": "vless",
                        "obligation_id": "sfaob_example",
                        "source_event_ids": ["sfe_example"],
                        "current_source_scope": {
                            "status": "ACCOUNTED",
                            "affected_scope_count": 39,
                            "unresolved_scope_count": 38,
                            "affected_scope_fingerprint": "a" * 64,
                        },
                    },
                },
            }), encoding="utf-8")
            result = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state, "vless",
            )
        self.assertTrue(result["ok"])
        self.assertTrue(result["requires_binding"])
        self.assertEqual(result["automation_obligation_id"], "sfaob_example")
        self.assertEqual(result["source_incident_id"], "sfinc_example")
        self.assertEqual(result["source_scope_fingerprint"], "a" * 64)

    def test_ct_m0f_missing_live_binding_fails_closed_when_l3_owner_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "l3-runtime-state.json").write_text(
                json.dumps({"incidents": {}}), encoding="utf-8"
            )
            result = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state, "vless",
            )

        self.assertFalse(result["ok"])
        self.assertTrue(result["requires_binding"])
        self.assertEqual(result["status"], "NO_ACTIVE_SERVICE_FAILURE_BINDING")

    def test_ct_m0f_certification_only_matrix_binding_reuses_exact_current_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            users = ["10.7.0.18", "10.7.0.19"]
            (state / "users.registry").write_text(
                "\n".join(
                    f"ip={user} current=vless enabled=1 certification_user=1 "
                    "certification_group=g1"
                    for user in users
                ) + "\n",
                encoding="utf-8",
            )
            (state / "egress.registry").write_text(
                "id=vless enabled=1 controlled_certification_source=1\n",
                encoding="utf-8",
            )
            now = datetime.now(timezone.utc).isoformat()
            (state / "service-matrix.json").write_text(json.dumps({
                "items": {"vless": {
                    "checked_at": now,
                    "services": {"youtube": {
                        "ok": False,
                        "source_incident_id": "sfinc_vless_current",
                    }},
                }},
            }), encoding="utf-8")
            scope_fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": users,
            })
            event = {
                "event_id": "sfe_vless_current",
                "event_type": "SERVICE_FAILURE_REVALIDATED",
                "service": "youtube",
                "observed_at": now,
                "channel": "vless",
                "source_incident_id": "sfinc_vless_current",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "source_scope": {
                    "scope_classification": "CERTIFICATION_ONLY",
                    "source_channel": "vless",
                    "affected_scope_count": 0,
                    "controlled_certification_scope": {
                        "affected_scope_count": 2,
                        "affected_scope_fingerprint": scope_fingerprint,
                        "raw_user_list_stored": False,
                    },
                },
            }
            (events / "service-failure-events.jsonl").write_text(
                json.dumps(event) + "\n", encoding="utf-8"
            )
            result = (
                self.autoswitch
                .ct_m0f_certification_only_matrix_failure_binding_projection(
                    state, "vless", event_dir=events,
                )
            )

        self.assertTrue(result["ok"], result)
        self.assertEqual(
            result["binding_kind"], "CERTIFICATION_ONLY_MATRIX_FAILURE"
        )
        self.assertEqual(result["source_scope_count"], 2)
        self.assertFalse(result["raw_identity_list_stored"])

    def test_ct_m0f_certification_binding_uses_current_registry_not_event_snapshot(self):
        """A continuing Matrix episode may outlive a controlled scope change."""
        cases = {
            "unchanged": ["10.7.0.18"],
            "removed_and_replaced": ["10.7.0.19"],
            "added": ["10.7.0.18", "10.7.0.19"],
        }
        for name, current_users in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                state = root / "state"
                events = root / "events"
                state.mkdir()
                events.mkdir()
                (state / "users.registry").write_text(
                    "\n".join(
                        f"ip={user} current=vless enabled=1 certification_user=1 "
                        "certification_group=g1"
                        for user in current_users
                    ) + "\n",
                    encoding="utf-8",
                )
                (state / "egress.registry").write_text(
                    "id=vless enabled=1 controlled_certification_source=1\n",
                    encoding="utf-8",
                )
                now = datetime.now(timezone.utc).isoformat()
                (state / "service-matrix.json").write_text(json.dumps({
                    "items": {"vless": {
                        "checked_at": now,
                        "services": {"youtube": {
                            "ok": False,
                            "source_incident_id": "sfinc_vless_current",
                        }},
                    }},
                }), encoding="utf-8")
                # This is an immutable historical snapshot from the first
                # observation.  It intentionally does not track later moves.
                (events / "service-failure-events.jsonl").write_text(json.dumps({
                    "event_id": "sfrev_old_scope",
                    "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "service": "youtube",
                    "observed_at": now,
                    "channel": "vless",
                    "source_incident_id": "sfinc_vless_current",
                    "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "source_scope": {
                        "scope_classification": "CERTIFICATION_ONLY",
                        "affected_scope_count": 0,
                        "controlled_certification_scope": {
                            "affected_scope_count": 1,
                            "affected_scope_fingerprint": "old-snapshot",
                        },
                    },
                }) + "\n", encoding="utf-8")
                result = self.autoswitch.ct_m0f_certification_only_matrix_failure_binding_projection(
                    state, "vless", event_dir=events,
                )
                self.assertTrue(result["ok"], result)
                self.assertEqual(result["source_scope_count"], len(current_users))
                self.assertEqual(
                    result["scope_binding_model"],
                    "CURRENT_REGISTRY_SCOPE_ON_ACTIVE_MATRIX_EPISODE",
                )
                self.assertFalse(result["event_scope_snapshot_matches_current"])

    def test_ct_m0f_certification_binding_fails_closed_for_ordinary_stale_or_wrong_episode(self):
        variants = {
            "ordinary_user": {
                "users": (
                    "ip=10.7.0.18 current=vless enabled=1 certification_user=1\n"
                    "ip=10.7.0.19 current=vless enabled=1 certification_user=0\n"
                ),
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "matrix_incident": "sfinc_current",
                "event_incident": "sfinc_current",
                "event_at": datetime.now(timezone.utc).isoformat(),
                "blocker": "ordinary_users_present_on_controlled_source",
            },
            "empty_scope": {
                "users": "",
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "matrix_incident": "sfinc_current",
                "event_incident": "sfinc_current",
                "event_at": datetime.now(timezone.utc).isoformat(),
                "blocker": "controlled_certification_scope_empty",
            },
            "stale_matrix": {
                "users": "ip=10.7.0.18 current=vless enabled=1 certification_user=1\n",
                "checked_at": "2020-01-01T00:00:00+00:00",
                "matrix_incident": "sfinc_current",
                "event_incident": "sfinc_current",
                "event_at": datetime.now(timezone.utc).isoformat(),
                "blocker": "matrix_source_observation_not_fresh",
            },
            "stale_event": {
                "users": "ip=10.7.0.18 current=vless enabled=1 certification_user=1\n",
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "matrix_incident": "sfinc_current",
                "event_incident": "sfinc_current",
                "event_at": "2020-01-01T00:00:00+00:00",
                "blocker": "fresh_active_certification_only_matrix_event_missing",
            },
            "wrong_episode": {
                "users": "ip=10.7.0.18 current=vless enabled=1 certification_user=1\n",
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "matrix_incident": "sfinc_current",
                "event_incident": "sfinc_old",
                "event_at": datetime.now(timezone.utc).isoformat(),
                "blocker": "fresh_active_certification_only_matrix_event_missing",
            },
            "recovered_matrix": {
                "users": "ip=10.7.0.18 current=vless enabled=1 certification_user=1\n",
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "matrix_incident": "",
                "event_incident": "sfinc_old",
                "event_at": datetime.now(timezone.utc).isoformat(),
                "matrix_ok": True,
                "blocker": "matrix_source_not_currently_failed",
            },
        }
        for name, case in variants.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                state = root / "state"
                events = root / "events"
                state.mkdir()
                events.mkdir()
                (state / "users.registry").write_text(case["users"], encoding="utf-8")
                (state / "egress.registry").write_text(
                    "id=vless enabled=1 controlled_certification_source=1\n",
                    encoding="utf-8",
                )
                (state / "service-matrix.json").write_text(json.dumps({
                    "items": {"vless": {
                        "checked_at": case["checked_at"],
                        "services": {"youtube": {
                            "ok": case.get("matrix_ok", False),
                            "source_incident_id": case["matrix_incident"],
                        }},
                    }},
                }), encoding="utf-8")
                (events / "service-failure-events.jsonl").write_text(json.dumps({
                    "event_id": "sfrev_case",
                    "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "service": "youtube",
                    "observed_at": case["event_at"],
                    "channel": "vless",
                    "source_incident_id": case["event_incident"],
                    "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "source_scope": {
                        "scope_classification": "CERTIFICATION_ONLY",
                        "affected_scope_count": 0,
                        "controlled_certification_scope": {
                            "affected_scope_count": 1,
                            "affected_scope_fingerprint": "snapshot",
                        },
                    },
                }) + "\n", encoding="utf-8")
                result = self.autoswitch.ct_m0f_certification_only_matrix_failure_binding_projection(
                    state, "vless", event_dir=events,
                )
                self.assertFalse(result["ok"], result)
                self.assertIn(case["blocker"], result["blockers"])

    def test_ct_m0f_selector_reuses_stage_one_degraded_target_for_matrix_failure(self):
        availability_policy = {
            "action_class_scopes": {
                "bounded availability-first controlled failover": {
                    "allowed_actions": [
                        "ASSIGN_CERTIFICATION_COHORT_TO_SHARED_TARGET",
                    ],
                    "certification_identities_only": True,
                    "max_users_per_transaction": 48,
                    "max_concurrent_transactions": 1,
                    "ordinary_identity_delta": 0,
                    "ordinary_route_delta": 0,
                    "shared_target_fault_injection_allowed": False,
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            users = ["10.7.0.18", "10.7.0.19"]
            (state / "users.registry").write_text(
                "\n".join(
                    f"ip={user} current=vless enabled=1 certification_user=1 "
                    "certification_group=g1"
                    for user in users
                ) + "\n",
                encoding="utf-8",
            )
            (state / "egress.registry").write_text(
                "id=vless enabled=1 controlled_certification_source=1 "
                "certification_group=g1\n",
                encoding="utf-8",
            )
            now = datetime.now(timezone.utc).isoformat()
            (state / "service-matrix.json").write_text(json.dumps({
                "items": {"vless": {
                    "checked_at": now,
                    "services": {"youtube": {
                        "ok": False,
                        "source_incident_id": "sfinc_vless_current",
                    }},
                }},
            }), encoding="utf-8")
            scope_fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": users,
            })
            (events / "service-failure-events.jsonl").write_text(json.dumps({
                "event_id": "sfe_vless_current",
                "event_type": "SERVICE_FAILURE_REVALIDATED",
                "service": "youtube",
                "observed_at": now,
                "channel": "vless",
                "source_incident_id": "sfinc_vless_current",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "source_scope": {
                    "scope_classification": "CERTIFICATION_ONLY",
                    "source_channel": "vless",
                    "affected_scope_count": 0,
                    "controlled_certification_scope": {
                        "affected_scope_count": 2,
                        "affected_scope_fingerprint": scope_fingerprint,
                    },
                },
            }) + "\n", encoding="utf-8")
            policy = root / "policy.json"
            audit = root / "audit.jsonl"
            policy.write_text(
                json.dumps({"delegated_autonomy_policy": {"stub": True}}),
                encoding="utf-8",
            )
            audit.write_text("", encoding="utf-8")
            args = SimpleNamespace(
                state_dir=str(state), event_dir=str(events),
                policy_file=str(policy), action_class_audit_store=str(audit),
            )
            pool = {"active_source_projections": [{
                "source_id": "vless",
                "certification_group": "g1",
                "enabled_certification_users_on_source": 2,
                "group_aligned_certification_users_on_source": 2,
                "enabled_non_certification_users_on_source": 0,
                "source_isolated_for_controlled_failure": True,
                "baseline_health": {"ok": False},
                "controlled_condition_active": True,
            }]}
            target = {
                "target_id": "awg3",
                "ordinary_planner_eligible": True,
                "shared_target_technically_eligible": True,
                "shared_target_availability": {
                    "state": "DEGRADED_USABLE",
                    "policy_boundary": (
                        "EXACT_DEGRADED_SHARED_TARGET_ACTION_CLASS_"
                        "CONTRACT_REQUIRED"
                    ),
                },
                "health": {"ok": True, "observation_fingerprint": "target"},
                "capacity": {"target_safe_additional_capacity": 1},
                "verification_supported": True,
                "rollback_containment_supported": True,
            }
            with mock.patch.object(
                self.autoswitch, "controlled_certification_pool_status",
                return_value=pool,
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={"ok": True, "policy": availability_policy},
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "read_live_execution_lineage_records", return_value=[],
            ), mock.patch.object(
                self.autoswitch,
                "availability_first_standing_policy_semantic_coverage_gate",
                return_value={"ok": True},
            ), mock.patch.object(
                self.autoswitch,
                "controlled_campaign_target_selection_diagnostic",
                return_value={
                    "targets": [target],
                    "shared_production_target_capacity_projection": {
                        "stage_allocations": {"1": {
                            "immutable_allocation_projection": [{
                                "target_id": "awg3",
                                "allocated_users": 1,
                                "availability_classification": "DEGRADED_USABLE",
                            }],
                        }},
                    },
                },
            ):
                result = self.autoswitch.ct_m0f_standing_source_selection_only(args)

        self.assertTrue(result["ok"], result)
        self.assertEqual(result["selected_source_id"], "vless")
        self.assertEqual(result["selected_user"], "10.7.0.18")
        self.assertEqual(result["selected_target_id"], "awg3")
        self.assertEqual(
            result["selected_target_admission"]["admission_law"],
            "ACTIVE_AVAILABILITY_FIRST_MATRIX_FAILURE_ONE_USER",
        )
        self.assertEqual(
            result["active_service_failure_binding"]["binding_kind"],
            "CERTIFICATION_ONLY_MATRIX_FAILURE",
        )

    def test_ct_m0f_stale_certification_only_matrix_does_not_scan_l3_or_topology(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.18 current=vless enabled=1 certification_user=1 "
                "certification_group=g1\n",
                encoding="utf-8",
            )
            (state / "egress.registry").write_text(
                "id=vless enabled=1 controlled_certification_source=1 "
                "certification_group=g1\n",
                encoding="utf-8",
            )
            stale = "2020-01-01T00:00:00+00:00"
            (state / "service-matrix.json").write_text(json.dumps({
                "items": {"vless": {
                    "checked_at": stale,
                    "services": {"youtube": {"ok": False}},
                }},
            }), encoding="utf-8")
            policy = root / "policy.json"
            audit = root / "audit.jsonl"
            drafts = root / "drafts"
            drafts.mkdir()
            policy.write_text("{}", encoding="utf-8")
            audit.write_text("", encoding="utf-8")
            args = SimpleNamespace(
                state_dir=str(state), event_dir=str(events),
                policy_file=str(policy), action_class_audit_store=str(audit),
                egress_drafts_dir=str(drafts),
            )
            pool = {"active_source_projections": [{
                "source_id": "vless",
                "certification_group": "g1",
                "enabled_certification_users_on_source": 1,
                "group_aligned_certification_users_on_source": 1,
                "enabled_non_certification_users_on_source": 0,
                "source_isolated_for_controlled_failure": True,
                "baseline_health": {"ok": False},
            }]}
            with mock.patch.object(
                self.autoswitch, "controlled_certification_pool_status",
                return_value=pool,
            ), mock.patch.object(
                self.autoswitch,
                "ct_m0f_active_service_failure_binding_projection",
                side_effect=AssertionError("ordinary L3 fallback must not run"),
            ), mock.patch.object(
                self.autoswitch, "controlled_source_topology_diagnostic",
                side_effect=AssertionError("topology diagnostic must not run"),
            ):
                result = self.autoswitch.ct_m0f_standing_source_selection_only(args)

        self.assertFalse(result["ok"])
        self.assertEqual(result["selection_mode"], "STOP_SAFE")
        self.assertIn(
            "no_healthy_isolated_controlled_source_with_group_aligned_certification_identity",
            result["blockers"],
        )

    def test_controlled_pool_reuses_one_matrix_snapshot_for_all_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "users.registry").write_text("", encoding="utf-8")
            (state / "egress.registry").write_text(
                "id=one enabled=1 controlled_certification_source=1\n"
                "id=two enabled=1 controlled_certification_source=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix.json").write_text(
                json.dumps({"items": {}, "updated": "2020-01-01T00:00:00+00:00"}),
                encoding="utf-8",
            )
            (state / "egress-diagnose.state").write_text("", encoding="utf-8")
            original = self.autoswitch.controlled_certification_source_health_status
            with mock.patch.object(
                self.autoswitch,
                "controlled_certification_source_health_status",
                wraps=original,
            ) as health:
                self.autoswitch.controlled_certification_pool_status(state)

        self.assertGreaterEqual(health.call_count, 2)
        for call in health.call_args_list:
            self.assertIsInstance(call.kwargs.get("matrix"), dict)
            self.assertIsInstance(call.kwargs.get("diagnose"), dict)
            self.assertIsInstance(call.kwargs.get("egress_rows"), list)

    def test_ct_m0f_binding_reuses_ephemeral_current_owner_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "l3-runtime-state.json").write_text(
                json.dumps({"incidents": {}}), encoding="utf-8"
            )
            cache = {"l3_state": {"incidents": {}}, "users": []}
            with mock.patch.object(
                self.autoswitch,
                "read_json",
                side_effect=AssertionError("must reuse supplied L3 projection"),
            ), mock.patch.object(
                self.autoswitch,
                "parse_registry",
                side_effect=AssertionError("must reuse supplied users projection"),
            ):
                result = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                    state, "vless", evidence_cache=cache,
                )
        self.assertEqual(result["status"], "NO_ACTIVE_SERVICE_FAILURE_BINDING")

    def test_ct_m0f_selector_does_not_scan_targets_before_exact_source_binding(self):
        args = SimpleNamespace(state_dir="/unused", policy_file="/unused")
        pool = {"active_source_projections": [{
            "source_id": "unbound",
            "enabled_certification_users_on_source": 1,
            "enabled_non_certification_users_on_source": 0,
            "source_isolated_for_controlled_failure": True,
            "baseline_health": {"ok": False},
        }]}
        with mock.patch.object(
            self.autoswitch,
            "controlled_certification_pool_status",
            return_value=pool,
        ), mock.patch.object(
            self.autoswitch,
            "parse_registry",
            return_value=[],
        ), mock.patch.object(
            self.autoswitch,
            "ct_m0f_active_service_failure_binding_projection",
            return_value={"ok": False, "requires_binding": True},
        ), mock.patch.object(
            self.autoswitch,
            "controlled_campaign_target_selection_diagnostic",
            side_effect=AssertionError("target scan must wait for exact source binding"),
        ):
            result = self.autoswitch.ct_m0f_standing_source_selection_only(args)
        self.assertFalse(result["ok"])
        self.assertIn(
            "no_healthy_isolated_controlled_source_with_group_aligned_certification_identity",
            result["blockers"],
        )

    def test_ct_m0f_standing_source_selection_rejects_ordinary_only_target(self):
        pool = {
            "active_source_projections": [{
                "source_id": "failed",
                "certification_group": "g1",
                "enabled_certification_users_on_source": 1,
                "group_aligned_certification_users_on_source": 1,
                "enabled_non_certification_users_on_source": 0,
                "source_isolated_for_controlled_failure": True,
                "baseline_health": {"ok": False},
            }, {
                "source_id": "ordinary",
                "certification_group": "",
                "enabled_certification_users_on_source": 0,
                "group_aligned_certification_users_on_source": 0,
                "enabled_non_certification_users_on_source": 1,
                "source_isolated_for_controlled_failure": False,
                "baseline_health": {"ok": True},
            }]
        }
        args = SimpleNamespace(state_dir="/unused")
        with mock.patch.object(
            self.autoswitch,
            "controlled_certification_pool_status",
            return_value=pool,
        ), mock.patch.object(
            self.autoswitch,
            "parse_registry",
            return_value=[{
                "ip": "10.7.0.18",
                "current": "failed",
                "enabled": "1",
                "certification_user": "1",
                "certification_group": "g1",
            }],
        ), mock.patch.object(
            self.autoswitch,
            "controlled_campaign_target_selection_diagnostic",
            return_value={
                "selection": {"selected_target_id": "ordinary"},
                "targets": [{
                    "target_id": "ordinary",
                    "full_live_admission": True,
                    "ordinary_planner_eligible": True,
                    "health": {"ok": True},
                    "capacity": {"target_safe_additional_capacity": 10},
                }],
            },
        ):
            result = self.autoswitch.ct_m0f_standing_source_selection_only(args)

        self.assertFalse(result["ok"])
        self.assertIn(
            "no_distinct_controlled_contract_admitted_target",
            result["blockers"],
        )
        self.assertFalse(
            result["selected_target_admission"]["controlled_contract_admitted"]
        )

    def test_ct_m0f_selection_reuses_healthy_shared_target_under_active_policy(self):
        pool = {
            "active_source_projections": [{
                "source_id": "failed-cert-source",
                "certification_group": "g1",
                "enabled_certification_users_on_source": 40,
                "group_aligned_certification_users_on_source": 40,
                "enabled_non_certification_users_on_source": 0,
                "source_isolated_for_controlled_failure": True,
                "baseline_health": {"ok": False},
            }]
        }
        availability_policy = {
            "action_class_scopes": {
                "bounded availability-first controlled failover": {
                    "allowed_actions": [
                        "ASSIGN_CERTIFICATION_COHORT_TO_SHARED_TARGET",
                    ],
                    "certification_identities_only": True,
                    "max_users_per_transaction": 48,
                    "max_concurrent_transactions": 1,
                    "ordinary_identity_delta": 0,
                    "ordinary_route_delta": 0,
                    "shared_target_fault_injection_allowed": False,
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            audit = root / "audit.jsonl"
            policy.write_text(
                json.dumps({"delegated_autonomy_policy": {"stub": True}}),
                encoding="utf-8",
            )
            audit.write_text("", encoding="utf-8")
            args = SimpleNamespace(
                state_dir="/unused", policy_file=str(policy),
                action_class_audit_store=str(audit),
            )
            with mock.patch.object(
                self.autoswitch,
                "controlled_certification_pool_status",
                return_value=pool,
            ), mock.patch.object(
                self.autoswitch,
                "parse_registry",
                side_effect=lambda path: ([{
                    "ip": "10.7.0.18",
                    "current": "failed-cert-source",
                    "enabled": "1",
                    "certification_user": "1",
                    "certification_group": "g1",
                }] if str(path).endswith("users.registry") else []),
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={"ok": True, "policy": availability_policy},
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "read_live_execution_lineage_records",
                return_value=[],
            ), mock.patch.object(
                self.autoswitch,
                "controlled_campaign_target_selection_diagnostic",
                return_value={
                    "targets": [{
                        "target_id": "healthy-shared-target",
                        "ordinary_planner_eligible": True,
                        "shared_target_technically_eligible": True,
                        "shared_target_availability": {
                            "state": "HEALTHY", "policy_boundary": "NONE",
                        },
                        "health": {
                            "ok": True,
                            "observation_fingerprint": "target-health",
                        },
                        "capacity": {"target_safe_additional_capacity": 1},
                        "verification_supported": True,
                        "rollback_containment_supported": True,
                    }],
                },
            ):
                result = self.autoswitch.ct_m0f_standing_source_selection_only(args)

        self.assertTrue(result["ok"])
        self.assertEqual(result["selection_mode"], "EXECUTE_CONTROLLED_FAILURE_CUTOVER")
        self.assertEqual(result["selected_source_id"], "failed-cert-source")
        self.assertEqual(result["selected_target_id"], "healthy-shared-target")
        self.assertEqual(result["eligible_source_count"], 1)
        self.assertEqual(
            result["selected_target_admission"]["admission_law"],
            "ACTIVE_AVAILABILITY_FIRST_SHARED_TARGET_ONE_USER",
        )
        self.assertEqual(result["selected_target_admission"]["ordinary_user_delta"], 0)
        self.assertFalse(result["selected_target_admission"]["stage48_credit"])

    def test_ct_m0f_selection_consumes_existing_controlled_execution_target(self):
        pool = {
            "active_source_projections": [{
                "source_id": "failed-cert-source",
                "certification_group": "g1",
                "enabled_certification_users_on_source": 1,
                "group_aligned_certification_users_on_source": 1,
                "enabled_non_certification_users_on_source": 0,
                "source_isolated_for_controlled_failure": True,
                "baseline_health": {"ok": False},
            }]
        }
        availability_policy = {
            "action_class_scopes": {
                "bounded availability-first controlled failover": {
                    "allowed_actions": [
                        "ASSIGN_CERTIFICATION_COHORT_TO_SHARED_TARGET",
                    ],
                    "certification_identities_only": True,
                    "max_users_per_transaction": 1,
                    "max_concurrent_transactions": 1,
                    "ordinary_identity_delta": 0,
                    "ordinary_route_delta": 0,
                    "shared_target_fault_injection_allowed": False,
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            audit = root / "audit.jsonl"
            policy.write_text(
                json.dumps({"delegated_autonomy_policy": {"stub": True}}),
                encoding="utf-8",
            )
            audit.write_text("", encoding="utf-8")
            args = SimpleNamespace(
                state_dir="/unused", policy_file=str(policy),
                action_class_audit_store=str(audit),
            )
            with mock.patch.object(
                self.autoswitch,
                "controlled_certification_pool_status",
                return_value=pool,
            ), mock.patch.object(
                self.autoswitch,
                "parse_registry",
                side_effect=lambda path: ([{
                    "ip": "10.7.0.18",
                    "current": "failed-cert-source",
                    "enabled": "1",
                    "certification_user": "1",
                    "certification_group": "g1",
                }] if str(path).endswith("users.registry") else []),
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={"ok": True, "policy": availability_policy},
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "read_live_execution_lineage_records",
                return_value=[],
            ), mock.patch.object(
                self.autoswitch,
                "controlled_campaign_target_selection_diagnostic",
                return_value={
                    "selection": {"selected_target_id": "execution-target"},
                    "targets": [{
                        "target_id": "execution-target",
                        "controlled_rebind_eligible": True,
                        "controlled_only_contract": True,
                        "ordinary_planner_eligible": False,
                        "shared_target_technically_eligible": True,
                        "current_stage_feasible": True,
                        "role": "EXECUTION_ONLY",
                        "reservation_owner": "operator_execution_governance",
                        "shared_target_availability": {
                            "state": "HEALTHY", "policy_boundary": "NONE",
                        },
                        "health": {
                            "ok": True,
                            "observation_fingerprint": "target-health",
                        },
                        "capacity": {"target_safe_additional_capacity": 1},
                        "verification_supported": True,
                        "rollback_containment_supported": True,
                    }],
                },
            ):
                result = self.autoswitch.ct_m0f_standing_source_selection_only(args)

        self.assertTrue(result["ok"])
        self.assertEqual(result["selected_target_id"], "execution-target")
        self.assertTrue(
            result["selected_target_admission"]["controlled_contract_admitted"]
        )
        self.assertFalse(
            result["selected_target_admission"]["ordinary_planner_eligible"]
        )
        self.assertEqual(
            result["selected_target_admission"]["admission_law"],
            "EXACT_EXISTING_CONTROLLED_EXECUTION_TARGET_ONE_USER",
        )

    def test_ct_m0f_selection_retains_disabled_prepared_failure_lineage(self):
        pool = {
            "active_source_projections": [{
                "source_id": "vless",
                "certification_group": "baseline-group",
                "enabled_certification_users_on_source": 1,
                "group_aligned_certification_users_on_source": 1,
                "enabled_non_certification_users_on_source": 0,
                "source_isolated_for_controlled_failure": True,
                "baseline_health": {
                    "ok": True,
                    "observation_fingerprint": "baseline-health",
                },
            }],
        }
        users = [{
            "ip": "10.7.0.107",
            "current": "exec-source",
            "enabled": "1",
            "certification_user": "1",
            "certification_group": "identity-group",
        }, {
            "ip": "10.7.0.108",
            "current": "vless",
            "enabled": "1",
            "certification_user": "1",
            "certification_group": "baseline-group",
        }]
        egress = [{
            "id": "exec-source",
            "enabled": "0",
            "state": "maintenance",
            "type": "interface",
            "role": "EXECUTION_ONLY",
            "controlled_certification_source": "1",
            "reservation_owner": "operator_execution_governance",
            "execution_reserved": "1",
            "canary_reserved": "1",
            "autoswitch_allowed": "0",
            "rebalance_allowed": "0",
            "production_assignment_allowed": "0",
            "certification_group": "source-group",
        }]
        args = SimpleNamespace(state_dir="/unused")
        with mock.patch.object(
            self.autoswitch,
            "controlled_certification_pool_status",
            return_value=pool,
        ), mock.patch.object(
            self.autoswitch,
            "parse_registry",
            side_effect=lambda path: (
                users if str(path).endswith("users.registry") else egress
            ),
        ), mock.patch.object(
            self.autoswitch,
            "controlled_certification_source_health_status",
            return_value={
                "ok": True,
                "status": "PASS_HEALTHY_BASELINE",
                "observation_fingerprint": "interface-still-reachable",
            },
        ):
            result = self.autoswitch.ct_m0f_standing_source_selection_only(args)

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["selection_mode"],
            "EXECUTE_CONTROLLED_FAILURE_CUTOVER",
        )
        self.assertEqual(result["selected_source_id"], "exec-source")
        self.assertEqual(result["selected_user"], "10.7.0.107")
        self.assertEqual(result["selected_target_id"], "vless")
        self.assertEqual(result["eligible_source_count"], 1)
        self.assertNotIn(
            "no_healthy_isolated_controlled_source_with_group_aligned_certification_identity",
            result["blockers"],
        )

    def test_prepared_class_decision_is_compact_and_generation_bound(self):
        plan = {
            "updated": "2026-08-05T01:00:00+00:00",
            "operation": {"operation_id": "op_generation"},
            "safety": {"generation": {
                "planner_generation_id": "planner_generation",
                "inputs": {
                    "users_registry": "users_generation",
                    "egress_registry": "egress_generation",
                    "policy": "policy_generation",
                    "org_policy": "org_generation",
                    "service_preferences": "service_generation",
                },
                "volatile_inputs": {
                    "service_matrix": "matrix_generation",
                    "egress_speed": "capacity_generation",
                    "autoswitch_safety": "anti_flap_generation",
                },
            }},
            "decisions": [
                {"user_ip": "10.0.0.2", "current_egress": "vless", "recommended_egress": "awg0", "important_services": ["google", "telegram"]},
                {"user_ip": "10.0.0.3", "current_egress": "vless", "recommended_egress": "awg0", "important_services": ["telegram", "google"]},
            ],
        }
        prepared = self.autoswitch.build_prepared_class_decision_projection(plan)
        self.assertEqual(prepared["status"], "PREPARED_CLASS_DECISION_AVAILABLE")
        self.assertEqual(prepared["class_count"], 1)
        self.assertEqual(prepared["classes"][0]["member_count"], 2)
        self.assertFalse(prepared["classes"][0]["raw_member_list_stored"])
        self.assertNotIn("10.0.0.2", json.dumps(prepared))
        self.assertEqual(
            prepared["hot_validation_law"],
            "COMPARE_DECLARED_GENERATIONS_ONLY_NO_WORLD_MODEL_REBUILD",
        )
        freshness = self.autoswitch.validate_prepared_class_decision_projection(
            prepared, prepared["invalidators"],
        )
        self.assertEqual(freshness["status"], "PREPARED_CLASS_DECISION_FRESH")
        self.assertFalse(freshness["world_model_rebuilt"])

    def test_prepared_class_decision_consumer_rejects_changed_generation(self):
        projection = {
            "classes": [{"class_id": "pcd_unit"}],
            "invalidators": {"target_health_and_path_generation": "old"},
        }
        result = self.autoswitch.validate_prepared_class_decision_projection(
            projection, {"target_health_and_path_generation": "new"},
        )
        self.assertEqual(result["status"], "PREPARED_CLASS_DECISION_STALE")
        self.assertEqual(result["invalidation_reasons"], ["target_health_and_path_generation"])
        self.assertFalse(result["registry_scanned"])

    def test_bounded_checkpoint_recovers_deferred_closure_without_forward_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            checkpoint = {
                "operation_id": "op_unit",
                "packet_id": "pkt_unit",
                "selected_move_hash": "moves_hash",
                "cohort_fingerprint": "cohort_hash",
                "state": "IN_PROGRESS",
                "terminal_reason": "process_interrupted_after_generation_commit",
                "subreceipts": [{"terminal": "SUCCESS"}],
            }
            l3_path = state / "l3-runtime-state.json"
            l3_path.write_text(json.dumps({
                "bounded_cohort_transactions": {"op_unit": checkpoint},
            }), encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state
            planner.l3_runtime_state_file = l3_path
            planner.l3_runtime_state = {}
            result = planner.reconcile_bounded_cohort_closure_obligations()
            self.assertEqual(result["status"], "DEFERRED_CLOSURE_DURABLE_SUCCESSOR_PROVEN")
            self.assertEqual(result["closure_obligations_published"], 1)
            rows = [json.loads(line) for line in (state / "closure-records.jsonl").read_text().splitlines()]
            self.assertEqual(rows[0]["next_required_consumer"], "tools/v7-users-autoswitch.reconcile_service_failure_execution_outcomes")
            self.assertFalse(rows[0]["forward_apply_allowed"])
            again = planner.reconcile_bounded_cohort_closure_obligations()
            self.assertEqual(again["closure_obligations_published"], 0)

    def test_network_path_evidence_is_channel_path_scoped_and_secret_free(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "egress.registry").write_text(
                "id=awg0 interface=awg0 protocol=wireguard enabled=1 "
                "expected_ip=203.0.113.7 config_path=/etc/v7/awg0.conf\n",
                encoding="utf-8",
            )
            with mock.patch.object(
                self.matrix,
                "_bounded_command_fingerprint",
                return_value={"status": "PASS", "sha256": "a" * 64, "returncode": 0},
            ):
                evidence = self.matrix.network_path_evidence(
                    state,
                    self.matrix.egress_row(state, "awg0"),
                    egress_id="awg0",
                    iface="awg0",
                    service_ids=["telegram", "google"],
                )
        self.assertEqual(evidence["scope"], "EGRESS_PATH_AND_CHANNEL_PROFILE")
        self.assertFalse(evidence["probe_execution_context"]["user_route_binding_used"])
        self.assertEqual(len(evidence["path_fingerprint"]), 64)
        self.assertEqual(len(evidence["expected_egress_ip_fingerprint"]), 64)
        self.assertEqual(evidence["source_ip_class_fingerprint"], "a" * 64)
        self.assertNotIn("203.0.113.7", json.dumps(evidence))
        self.assertNotIn("raw_rules", evidence)
        self.assertEqual(
            evidence["performance_timeline"]["bounded_parallelism"], 4
        )
        self.assertEqual(
            set(evidence["performance_timeline"]["component_duration_ms"]),
            {
                "interface_addresses",
                "policy_rules",
                "routing_tables",
                "firewall_rules",
            },
        )

    def test_expected_egress_ip_change_invalidates_path_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            row = {"id": "awg0", "interface": "awg0", "protocol": "wireguard", "expected_ip": "203.0.113.7"}
            with mock.patch.object(
                self.matrix,
                "_bounded_command_fingerprint",
                return_value={"status": "PASS", "sha256": "a" * 64, "returncode": 0},
            ):
                first = self.matrix.network_path_evidence(
                    state, row, egress_id="awg0", iface="awg0", service_ids=["telegram"]
                )
                second = self.matrix.network_path_evidence(
                    state, {**row, "expected_ip": "203.0.113.8"},
                    egress_id="awg0", iface="awg0", service_ids=["telegram"]
                )
        self.assertNotEqual(first["path_fingerprint"], second["path_fingerprint"])

    def test_failure_episode_survives_repeated_matrix_writes_and_resets_on_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            failure = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T08:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": failure}, 1, event_dir=event_dir)
            failure["tested_at"] = "2026-07-25T08:01:00+00:00"
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": failure}, 1, event_dir=event_dir)
            failure["tested_at"] = "2026-07-25T08:02:00+00:00"
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": failure}, 1, event_dir=event_dir)

            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            self.assertEqual(row["failure_samples"], 3)
            self.assertEqual(row["consecutive_failures"], 3)
            self.assertGreaterEqual(row["bad_for_seconds"], 120)
            self.assertTrue(row["failure_episode_id"].startswith("sfep_"))
            self.assertEqual(row["probe_provenance"], "SERVICE_PROBE_OBSERVED")
            self.assertEqual(row["evidence_class"], "PROBE_OBSERVATION")
            self.assertTrue(str(row["monotonic_clock_domain"]).startswith("linux-boot:"))
            self.assertGreater(row["first_failed_observation_monotonic_ns"], 0)
            self.assertGreaterEqual(
                row["confirmed_hard_failure_monotonic_ns"],
                row["first_failed_observation_monotonic_ns"],
            )
            events = [json.loads(line) for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["event_provenance"], "EXTERNAL_UNATTRIBUTED")
            self.assertFalse(events[0]["natural_production_credit"])
            self.assertEqual(
                events[0]["monotonic_clock_domain"], row["monotonic_clock_domain"]
            )

            recovery = {"ok": True, "status": "OK", "tested_at": "2026-07-25T08:03:00+00:00"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": recovery}, 1, event_dir=event_dir)
            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            self.assertEqual(row["failure_state"], "RECOVERY_OBSERVED")
            self.assertEqual(row["failure_samples"], 0)
            self.assertEqual(row["recovery_samples"], 1)

    def test_availability_first_stage_receipt_is_exact_once_and_compact(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_store = Path(tmp) / "operator-execution-audit.jsonl"
            result = {
                "final_verdict": "AVAILABILITY_FIRST_STANDING_STAGE_COMPLETED",
                "stage": 5,
                "standing_policy_contract_id": "sdpc_" + "a" * 24,
                "standing_policy_contract_hash": "a" * 64,
                "planner_allocation_fingerprint": "b" * 64,
                "execution_allocation_fingerprint": "b" * 64,
                "packet_set_fingerprint": "c" * 64,
                "allocation": [
                    {
                        "target_id": "awg3",
                        "allocated_users": 1,
                        "target_fingerprint": "d" * 64,
                        "capacity_bounds_fingerprint": "e" * 64,
                    },
                    {
                        "target_id": "awg0",
                        "allocated_users": 4,
                        "target_fingerprint": "f" * 64,
                        "capacity_bounds_fingerprint": "1" * 64,
                    },
                ],
                "allocation_immutable": True,
                "capacity_reservation_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "per_user_verification_passed": True,
                "per_target_verification_passed": True,
                "aggregate_verification_passed": True,
                "ordinary_user_protection_passed": True,
                "baseline_reset_verified": True,
            }
            first = self.refresh.record_availability_first_stage_consumption(
                audit_store=audit_store,
                result=result,
            )
            duplicate = self.refresh.record_availability_first_stage_consumption(
                audit_store=audit_store,
                result=result,
            )
            rows = [
                json.loads(line)
                for line in audit_store.read_text(encoding="utf-8").splitlines()
            ]

        self.assertTrue(first["audit_write"])
        self.assertTrue(duplicate["duplicate_suppressed"])
        self.assertEqual(first["receipt_id"], duplicate["receipt_id"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(
            sum(item["verified_scope"] for item in rows[0]["target_receipts"]),
            5,
        )
        self.assertFalse(rows[0]["raw_identity_list_stored"])
        self.assertNotIn("users", rows[0])
        self.assertFalse(rows[0]["natural_l8_credit"])

    def test_target_bound_receipt_advances_target_only_and_is_exact_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_store = Path(tmp) / "operator-execution-audit.jsonl"
            result = {
                "final_verdict": (
                    "AVAILABILITY_FIRST_TARGET_BOUND_TRIAL_COMPLETED"
                ),
                "stage": 5,
                "target_bound_trial_target": "awg3",
                "campaign_next_stage": 25,
                "standing_policy_contract_id": "sdpc_" + "a" * 24,
                "standing_policy_contract_hash": "a" * 64,
                "planner_allocation_fingerprint": "b" * 64,
                "execution_allocation_fingerprint": "c" * 64,
                "packet_set_fingerprint": "d" * 64,
                "allocation": [{
                    "target_id": "awg3",
                    "allocated_users": 5,
                    "target_fingerprint": "e" * 64,
                    "capacity_bounds_fingerprint": "f" * 64,
                }],
                "allocation_immutable": True,
                "capacity_reservation_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "per_user_verification_passed": True,
                "per_target_verification_passed": True,
                "aggregate_verification_passed": True,
                "ordinary_user_protection_passed": True,
                "baseline_reset_verified": True,
            }
            first = (
                self.refresh
                .record_availability_first_target_bound_consumption(
                    audit_store=audit_store,
                    result=result,
                )
            )
            duplicate = (
                self.refresh
                .record_availability_first_target_bound_consumption(
                    audit_store=audit_store,
                    result=result,
                )
            )
            rows = [
                json.loads(line)
                for line in audit_store.read_text(
                    encoding="utf-8"
                ).splitlines()
            ]
        self.assertTrue(first["audit_write"])
        self.assertTrue(duplicate["duplicate_suppressed"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0]["effect_class"],
            "AVAILABILITY_FIRST_TARGET_BOUND_CONSUMED",
        )
        self.assertEqual(rows[0]["verified_scope"], 5)
        self.assertNotIn("users", rows[0])

    def test_target_growth_projection_breaks_aggregate_stage_cycle(self):
        rows = [{
            "target_id": "amnezia",
            "correlation_domain": "domain-a",
            "shared_target_technically_eligible": True,
            "shared_target_availability": {
                "state": "DEGRADED_USABLE",
                "policy_boundary": "EXACT_POLICY",
            },
            "semantic_fingerprint": "a" * 64,
            "capacity": {
                "availability_first_proven_additional_scope": 9,
                "availability_first_next_trial_scope": 10,
                "target_safe_additional_capacity": 9,
                "ordinary_users": 0,
                "capacity_bounds": {"safe": 9},
            },
        }, {
            "target_id": "awg3",
            "correlation_domain": "domain-b",
            "shared_target_technically_eligible": True,
            "shared_target_availability": {
                "state": "DEGRADED_USABLE",
                "policy_boundary": "EXACT_POLICY",
            },
            "semantic_fingerprint": "b" * 64,
            "capacity": {
                "availability_first_proven_additional_scope": 1,
                "availability_first_next_trial_scope": 2,
                "target_safe_additional_capacity": 2,
                "ordinary_users": 11,
                "capacity_bounds": {"safe": 2},
            },
        }]
        projection = (
            self.autoswitch
            .availability_first_target_growth_trial_projection(
                rows=rows,
                campaign={
                    "next_stage": 25,
                    "standing_policy_contract_id": "sdpc_test",
                    "target_proven_bounds": {
                        "amnezia": 9,
                        "awg3": 1,
                    },
                },
                inventory_fingerprint="c" * 64,
                excluded_target_ids={"vless"},
            )
        )
        self.assertTrue(projection["feasible"])
        self.assertEqual(projection["target_id"], "awg3")
        self.assertEqual(projection["trial_scope"], 2)
        self.assertEqual(
            projection["production_credit_class"],
            "TARGET_BOUND_ONLY_NOT_CAMPAIGN_STAGE",
        )

    def test_semantic_coverage_reuses_active_policy_for_shared_degraded_target(self):
        policy = (
            self.autoswitch.operator_execution
            .standing_delegated_operational_policy_template(
                max_users=48,
                include_availability_first=True,
            )
        )
        scope = policy["action_class_scopes"][
            self.autoswitch.operator_execution
            .AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
        ]
        allocation = {
            "feasible": True,
            "immutable_allocation_projection": [{
                "target_id": "awg3",
                "availability_classification": "DEGRADED_USABLE",
                "allocated_users": 25,
            }],
        }
        covered = (
            self.autoswitch
            .availability_first_standing_policy_semantic_coverage_gate(
                standing_validation={"ok": True, "errors": [], "policy": policy},
                policy_contract={"contract_id": "sdpc_unit", "contract_hash": "a" * 64},
                availability_scope=scope,
                stage=25,
                allocation=allocation,
            )
        )
        self.assertTrue(covered["ok"], covered)
        self.assertEqual(
            covered["status"],
            "AUTO_ADMITTED_BY_EXISTING_STANDING_POLICY",
        )
        self.assertEqual(covered["normalized_effect"]["ordinary_route_delta"], 0)
        self.assertFalse(covered["forbidden_effects"]["authority_expansion"])

        insufficient = dict(scope)
        insufficient["max_users_per_transaction"] = 10
        blocked = (
            self.autoswitch
            .availability_first_standing_policy_semantic_coverage_gate(
                standing_validation={"ok": True, "errors": [], "policy": policy},
                policy_contract={"contract_id": "sdpc_unit", "contract_hash": "a" * 64},
                availability_scope=insufficient,
                stage=25,
                allocation=allocation,
            )
        )
        self.assertFalse(blocked["ok"])
        self.assertEqual(
            blocked["status"],
            "GENUINE_AUTHORITY_EXPANSION_REQUIRED",
        )
        self.assertIn(
            "max_users_per_transaction",
            blocked["mismatched_dimensions"],
        )

    def test_matrix_consumes_target_bound_predecessor_before_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            audit_store = root / "audit.jsonl"
            policy_file = root / "policy.json"
            policy_file.write_text("{}", encoding="utf-8")
            planner_payload = {
                "status": (
                    "CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED"
                ),
                "availability_first_standing_policy_admission": {
                    "ok": True,
                    "blockers": [],
                },
                "shared_production_target_capacity_projection": {
                    "availability_campaign": {
                        "next_stage": 25,
                        "completed": False,
                        "blockers": [],
                    },
                    "stage_allocations": {
                        "25": {
                            "feasible": False,
                            "allocation_fingerprint": "",
                        },
                    },
                    "target_growth_trial": {
                        "status": "TARGET_BOUND_TRIAL_READY",
                        "ok": True,
                        "feasible": True,
                        "campaign_next_stage": 25,
                        "target_id": "awg3",
                        "trial_scope": 2,
                        "allocation_fingerprint": "a" * 64,
                        "immutable_allocation_projection": [{
                            "target_id": "awg3",
                            "allocated_users": 2,
                        }],
                    },
                },
            }
            executor_payload = {
                "final_verdict": (
                    "AVAILABILITY_FIRST_TARGET_BOUND_TRIAL_COMPLETED"
                ),
                "transaction_status": "COMPLETED",
                "stage": 2,
                "target_bound_trial_target": "awg3",
                "campaign_next_stage": 25,
                "standing_policy_contract_id": "sdpc_" + "b" * 24,
                "standing_policy_contract_hash": "b" * 64,
                "planner_allocation_fingerprint": "a" * 64,
                "execution_allocation_fingerprint": "c" * 64,
                "packet_set_fingerprint": "d" * 64,
                "allocation": [{
                    "target_id": "awg3",
                    "allocated_users": 2,
                    "target_fingerprint": "e" * 64,
                    "capacity_bounds_fingerprint": "f" * 64,
                }],
                "allocation_immutable": True,
                "capacity_reservation_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "per_user_verification_passed": True,
                "per_target_verification_passed": True,
                "aggregate_verification_passed": True,
                "ordinary_user_protection_passed": True,
                "baseline_reset_verified": True,
                "users_moved": 2,
                "runtime_mutation_performed": True,
            }
            calls = []

            def run(command, **_kwargs):
                calls.append(command)
                payload = (
                    planner_payload if len(calls) == 1 else executor_payload
                )
                return SimpleNamespace(
                    returncode=0,
                    stdout=json.dumps(payload),
                )

            with mock.patch.object(self.refresh.subprocess, "run", side_effect=run):
                result = (
                    self.refresh
                    ._run_availability_first_standing_policy_stage_once(
                        "planner",
                        "executor",
                        state_dir=state_dir,
                        event_dir=event_dir,
                        policy_file=policy_file,
                        audit_store=audit_store,
                        timeout_sec=30,
                    )
                )
        self.assertTrue(result["action_completed"], result)
        self.assertEqual(result["completion_kind"], "TARGET_BOUND_TRIAL")
        self.assertEqual(result["stage"], 2)
        self.assertIn(
            "--availability-first-target-bound-trial-target",
            calls[1],
        )
        self.assertTrue(
            result["stage_consumption"]["receipt_id"].startswith(
                "aftbound_"
            )
        )

    def test_expected_http_response_is_visible_methodology_limit_not_failure_episode(self):
        for http_code in ("404", "405"):
            with self.subTest(http_code=http_code), mock.patch.object(
                self.matrix.subprocess,
                "run",
                return_value=SimpleNamespace(
                    stdout=f"{http_code} 0.101 0.202",
                    stderr="curl: (22) The requested URL returned error",
                    returncode=22,
                ),
            ):
                observed = self.matrix.run_curl_check(
                    "anthropic",
                    {"label": "Anthropic", "url": "https://api.anthropic.com/"},
                    "awg0",
                    8,
                )
            self.assertTrue(observed["ok"])
            self.assertTrue(observed["http_reachable"])
            self.assertTrue(observed["limited"])
            self.assertEqual(observed["status"], "HTTP_LIMITED")
            self.assertFalse(self.matrix.service_failure_observed(observed))
            episode = self.matrix.service_failure_episode(
                {"failure_episode_id": "sfep_old", "ok": False, "status": "FAIL"},
                observed,
                egress_id="awg0",
                service_id="anthropic",
                observed_at="2026-07-27T03:00:00+00:00",
                identity_generation="egid_test",
            )
            self.assertEqual(episode["probe_classification"], "HTTP_LIMITED")
            self.assertEqual(episode["failure_state"], "RECOVERY_OBSERVED")
            self.assertEqual(episode["failure_episode_id"], "")

    def test_actual_http_server_error_remains_failure(self):
        with mock.patch.object(
            self.matrix.subprocess,
            "run",
            return_value=SimpleNamespace(
                stdout="500 0.101 0.202",
                stderr="curl: (22) The requested URL returned error",
                returncode=22,
            ),
        ):
            observed = self.matrix.run_curl_check(
                "anthropic",
                {"label": "Anthropic", "url": "https://api.anthropic.com/"},
                "awg0",
                8,
            )
        self.assertFalse(observed["ok"])
        self.assertFalse(observed["http_reachable"])
        self.assertEqual(observed["status"], "FAIL")
        self.assertTrue(self.matrix.service_failure_observed(observed))

    def test_failure_episode_survives_production_timer_jitter_but_not_long_gap(self):
        self.assertEqual(
            self.matrix.FAILURE_EPISODE_CONTINUITY_SECONDS,
            2 * self.matrix.SERVICE_MATRIX_CADENCE_SECONDS
            + self.matrix.SERVICE_MATRIX_RANDOMIZED_DELAY_SECONDS
            + self.matrix.SERVICE_MATRIX_BATCH_BUDGET_SECONDS
            + self.matrix.SERVICE_MATRIX_CONTINUITY_SAFETY_SECONDS,
        )
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            first = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T08:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": first}, 1, event_dir=event_dir)
            jittered = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T08:16:10+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": jittered}, 1, event_dir=event_dir)
            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            first_episode = row["failure_episode_id"]
            self.assertEqual(row["failure_samples"], 2)
            self.assertGreaterEqual(row["bad_for_seconds"], 970)

            long_gap = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T09:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": long_gap}, 1, event_dir=event_dir)
            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            self.assertEqual(row["failure_samples"], 1)
            self.assertNotEqual(row["failure_episode_id"], first_episode)

    def test_continuing_persistent_episode_emits_fresh_revalidation_without_new_episode(self):
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            first = {
                "ok": False,
                "status": "FAIL",
                "tested_at": "2026-07-27T03:00:00+00:00",
                "reason": "connection reset",
            }
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": first}, 1,
                event_dir=event_dir, persistence_samples=1,
            )
            second = dict(first, tested_at="2026-07-27T03:01:00+00:00")
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": second}, 1,
                event_dir=event_dir, persistence_samples=1,
            )
            third = dict(first, tested_at="2026-07-27T03:02:00+00:00")
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": third}, 1,
                event_dir=event_dir, persistence_samples=1,
            )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [row["event_type"] for row in events],
                [
                    "SERVICE_FAILURE_OBSERVED",
                    "SERVICE_FAILURE_REVALIDATED",
                    "SERVICE_FAILURE_REVALIDATED",
                ],
            )
            revalidated = events[-1]
            self.assertEqual(revalidated["evidence_class"], "PROBE_OBSERVED_PRODUCTION_EVENT")
            self.assertTrue(revalidated["capture_only"])
            self.assertFalse(revalidated["natural_production_credit"])
            self.assertEqual(revalidated["correlated_services"], ["youtube"])
            self.assertTrue(revalidated["observation_generation"].startswith("sfrev_"))
            self.assertEqual(events[-2]["event_id"], events[-1]["event_id"])

    def test_matrix_revalidation_captures_compact_source_scope_without_raw_users(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n"
                "ip=10.0.0.4 current=awg0 enabled=1\n",
                encoding="utf-8",
            )
            matrix_file = state_dir / "service-matrix.json"
            event_dir = root / "events"
            failure = {"ok": False, "status": "FAIL", "tested_at": "2026-07-27T03:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": failure}, 1,
                event_dir=event_dir, persistence_samples=1, state_dir=state_dir,
            )
            event = json.loads((event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(event["source_scope"]["affected_scope_count"], 2)
        self.assertTrue(event["source_scope"]["affected_scope_fingerprint"])
        self.assertFalse(event["source_scope"]["raw_user_list_stored"])
        self.assertNotIn("affected_users", event["source_scope"])

    def test_matrix_scope_change_emits_fresh_revalidation_generation(self):
        """A changed compact scope must reach the exact-once passive consumer."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            users = state_dir / "users.registry"
            users.write_text(
                "ip=10.0.0.2 current=vless enabled=1\n",
                encoding="utf-8",
            )
            matrix_file = state_dir / "service-matrix.json"
            event_dir = root / "events"
            failure = {
                "ok": False,
                "status": "FAIL",
                "tested_at": "2026-07-27T03:00:00+00:00",
                "reason": "reset",
            }
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": failure}, 1,
                event_dir=event_dir, persistence_samples=1, state_dir=state_dir,
            )
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0",
                {"youtube": {**failure, "tested_at": "2026-07-27T03:01:00+00:00"}},
                1, event_dir=event_dir, persistence_samples=1, state_dir=state_dir,
            )
            users.write_text(
                "ip=10.0.0.2 current=vless enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n",
                encoding="utf-8",
            )
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0",
                {"youtube": {**failure, "tested_at": "2026-07-27T03:02:00+00:00"}},
                1, event_dir=event_dir, persistence_samples=1, state_dir=state_dir,
            )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            ]
        self.assertEqual(
            [row["event_type"] for row in events],
            ["SERVICE_FAILURE_OBSERVED", "SERVICE_FAILURE_REVALIDATED", "SERVICE_FAILURE_REVALIDATED"],
        )
        self.assertNotEqual(events[-2]["event_id"], events[-1]["event_id"])
        self.assertEqual(events[-1]["source_scope"]["affected_scope_count"], 2)

    def test_failure_family_and_registry_generation_split_episode(self):
        previous = {
            "ok": False,
            "status": "FAIL",
            "reason": "connection refused",
            "observed_at": "2026-07-25T08:00:00+00:00",
            "failure_started_at": "2026-07-25T08:00:00+00:00",
            "failure_samples": 2,
            "failure_family": "TCP_CONNECTION_REFUSED",
            "egress_identity_generation": "egid_a",
            "failure_episode_id": "sfep_old",
        }
        changed_family = self.matrix.service_failure_episode(
            previous,
            {"ok": False, "status": "FAIL", "reason": "operation timed out"},
            egress_id="vless",
            service_id="youtube",
            observed_at="2026-07-25T08:01:00+00:00",
            identity_generation="egid_a",
        )
        self.assertEqual(changed_family["failure_family"], "TRANSPORT_TIMEOUT")
        self.assertEqual(changed_family["failure_samples"], 1)
        changed_generation = self.matrix.service_failure_episode(
            previous,
            {"ok": False, "status": "FAIL", "reason": "connection refused"},
            egress_id="vless",
            service_id="youtube",
            observed_at="2026-07-25T08:01:00+00:00",
            identity_generation="egid_b",
        )
        self.assertEqual(changed_generation["failure_samples"], 1)

    def test_correlated_failures_create_one_incident_and_recovery_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            for minute in range(3):
                failures = {
                    service: {
                        "ok": False,
                        "status": "FAIL",
                        "tested_at": f"2026-07-25T08:0{minute}:00+00:00",
                        "reason": "connection refused",
                    }
                    for service in ("youtube", "google")
                }
                self.matrix.update_matrix(
                    matrix_file, "vless", "tun0", failures, 1,
                    event_dir=event_dir,
                    egress_identity={
                        "canonical_egress_id": "vless",
                        "egress_identity_generation": "egid_test",
                        "egress_identity_fingerprint": "fingerprint",
                    },
                )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            failure_events = [row for row in events if row["event_type"] == "SERVICE_FAILURE_OBSERVED"]
            self.assertEqual(len(failure_events), 2)
            self.assertEqual(len({row["source_incident_id"] for row in failure_events}), 1)
            self.assertEqual({row["failure_family"] for row in failure_events}, {"TCP_CONNECTION_REFUSED"})

            recovery = {
                service: {
                    "ok": True, "status": "OK",
                    "tested_at": "2026-07-25T08:03:00+00:00",
                }
                for service in ("youtube", "google")
            }
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", recovery, 1,
                event_dir=event_dir,
                egress_identity={
                    "canonical_egress_id": "vless",
                    "egress_identity_generation": "egid_test",
                    "egress_identity_fingerprint": "fingerprint",
                },
            )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            recovery_events = [row for row in events if row["event_type"] == "SERVICE_RECOVERY_OBSERVED"]
            self.assertEqual(len(recovery_events), 2)
            self.assertEqual(
                {row["source_incident_id"] for row in recovery_events},
                {failure_events[0]["source_incident_id"]},
            )

    def test_component_recovery_does_not_close_correlated_open_source_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            identity = {
                "canonical_egress_id": "vless",
                "egress_identity_generation": "egid_test",
                "egress_identity_fingerprint": "fingerprint",
            }
            for minute in range(3):
                self.matrix.update_matrix(
                    matrix_file, "vless", "tun0", {
                        "youtube": {"ok": False, "status": "FAIL", "tested_at": f"2026-07-25T08:0{minute}:00+00:00", "reason": "connection refused"},
                        "google": {"ok": False, "status": "FAIL", "tested_at": f"2026-07-25T08:0{minute}:00+00:00", "reason": "connection refused"},
                    }, 1, event_dir=event_dir, egress_identity=identity,
                )
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {
                    "youtube": {"ok": True, "status": "OK", "tested_at": "2026-07-25T08:03:00+00:00"},
                    "google": {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T08:03:00+00:00", "reason": "connection refused"},
                }, 1, event_dir=event_dir, egress_identity=identity,
            )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]

        self.assertFalse(any(
            row["event_type"] == "SERVICE_RECOVERY_OBSERVED"
            for row in events
        ))

    def test_l3_consumer_rejects_transient_and_consumes_persistent_episode(self):
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        planner.service_signal_policy = {
            "service_failure_persistence_samples": 3,
            "service_failure_persistence_window_seconds": 180,
        }
        planner.switch_policy = {}
        planner.policy = {}
        planner.org_policy = {}
        planner.service_prefs = {}
        planner.matrix = {"items": {"vless": {"services": {
            "youtube": {
                "ok": False, "status": "FAIL", "failure_samples": 2,
                "failure_episode_id": "sfep_transient",
            },
            "google": {
                "ok": False, "status": "FAIL", "failure_samples": 3,
                "bad_for_seconds": 181, "failure_episode_id": "sfep_persistent",
                "observed_at": "2026-07-25T08:02:00+00:00",
            },
        }}}}
        failures = planner._l3_required_service_failures_for_source("vless")
        self.assertEqual([row["service"] for row in failures], ["google"])
        self.assertEqual(failures[0]["truth_class"], "PERSISTENT_FAIL")
        self.assertEqual(failures[0]["failure_episode_id"], "sfep_persistent")

    def test_passive_consumer_captures_natural_candidate_without_l8_credit_or_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            event = {
                "event_id": "sfe_natural_candidate",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "service": "youtube",
                "failure_episode_id": "sfep_1",
                "failure_samples": 3,
                "bad_for_seconds": 180,
                "observed_at": "2026-07-25T08:02:00+00:00",
                "source_hashes": {"service_row": "hash"},
            }
            (event_dir / "service-failure-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.event_dir = event_dir
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.service_signal_policy = {
                "service_failure_persistence_samples": 3,
                "service_failure_persistence_window_seconds": 180,
            }
            planner.l3_runtime_state = {}
            result = planner._consume_passive_production_events()
            self.assertTrue(result["active"])
            self.assertEqual(result["natural_event_candidates_captured"], 1)
            self.assertFalse(result["natural_production_credit"])
            rows = [json.loads(line) for line in (state_dir / "execution-events.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows[0]["evidence_class"], "NATURAL_PRODUCTION_CANDIDATE")
            self.assertEqual(rows[0]["decision"], "NO_ACTION_NATURAL_EVENT_PENDING_PROVENANCE_AND_LEGAL_OUTCOME")
            self.assertFalse(rows[0]["execution_performed"])

    def test_passive_consumer_correlates_children_and_emits_omp_frontier_then_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            incident = "sfinc_shared"
            children = [
                {
                    "event_id": f"sfe_{service}",
                    "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                    "channel": "vless",
                    "service": service,
                    "source_incident_id": incident,
                    "failure_episode_id": f"sfep_{service}",
                    "failure_family": "TCP_CONNECTION_REFUSED",
                    "failure_samples": 3,
                    "bad_for_seconds": 180,
                    "observed_at": "2026-07-25T08:02:00+00:00",
                    "source_hashes": {service: "hash"},
                }
                for service in ("youtube", "google")
            ]
            path = event_dir / "service-failure-events.jsonl"
            path.write_text(
                "".join(json.dumps(row) + "\n" for row in children),
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.event_dir = event_dir
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.service_signal_policy = {
                "service_failure_persistence_samples": 3,
                "service_failure_persistence_window_seconds": 180,
            }
            planner.l3_runtime_state = {}
            result = planner._consume_passive_production_events()
            self.assertEqual(result["source_incident_ids"], [incident])
            self.assertEqual(result["records"]["outcome"], 1)
            self.assertEqual(
                result["omp_frontiers"][0]["frontier_id"],
                "V7_SERVICE_FAILURE_INCIDENT_RECONCILIATION",
            )
            self.assertEqual(
                result["omp_frontiers"][0]["failure_families"],
                ["TCP_CONNECTION_REFUSED"],
            )

            recovery = {
                "event_id": "sre_youtube",
                "event_type": "SERVICE_RECOVERY_OBSERVED",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_RECOVERY_EVENT",
                "channel": "vless",
                "service": "youtube",
                "source_incident_id": incident,
                "failure_episode_id": "sfep_youtube",
                "failure_family": "TCP_CONNECTION_REFUSED",
                "recovered_at": "2026-07-25T08:10:00+00:00",
            }
            with path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(recovery) + "\n")
            recovered = planner._consume_passive_production_events()
            self.assertEqual(
                recovered["omp_frontiers"][0]["frontier_id"],
                "V7_SERVICE_FAILURE_RECOVERY_RECONCILIATION",
            )
            outcomes = [
                json.loads(line)
                for line in (state_dir / "execution-events.jsonl").read_text(encoding="utf-8").splitlines()
                if "outcome_status" in json.loads(line)
            ]
            self.assertEqual(outcomes[-1]["temporal_observations"]["state"], "RECOVERED")

    def test_later_revalidation_reopens_incident_after_expiry_in_same_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            incident = "sfinc_expiry_then_revalidated"
            events = [
                {
                    "event_id": "sxe_old", "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_EPISODE_EXPIRY",
                    "source_incident_id": incident, "channel": "vless",
                    "observed_at": "2026-07-27T10:00:00+00:00",
                },
                {
                    "event_id": "sfrev_new", "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                    "source_incident_id": incident, "channel": "vless",
                    "failure_samples": 3, "bad_for_seconds": 180,
                    "observed_at": "2026-07-27T10:01:00+00:00",
                    "source_scope": {
                        "affected_scope_count": 2,
                        "affected_scope_fingerprint": "scope-reopened",
                        "source_channel": "vless",
                        "raw_user_list_stored": False,
                    },
                },
            ]
            (event_dir / "service-failure-events.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in events), encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.event_dir = event_dir
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.service_signal_policy = {
                "service_failure_persistence_samples": 3,
                "service_failure_persistence_window_seconds": 180,
            }
            planner.l3_runtime_state = {}
            result = planner._consume_passive_production_events()
            rows = [json.loads(line) for line in (state_dir / "closure-records.jsonl").read_text(encoding="utf-8").splitlines()]
            closure = next(row for row in rows if row.get("object_type") == "passive_production_event")
        self.assertTrue(result["active"])
        self.assertEqual(closure["terminal_outcome_classification"], "STOP_SAFE_NO_ACTION")
        self.assertEqual(closure["source_scope"]["affected_scope_count"], 2)
        self.assertEqual(closure["terminal_resolution"]["latest_event_id"], "sfrev_new")
        self.assertEqual(closure["terminal_resolution"]["superseded_terminal_event_ids"], ["sxe_old"])

    def test_runtime_readiness_copy_never_claims_service_availability(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        self.assertIn("Runtime/config readiness: конфиг и runtime подтверждены текущим снимком; доступность сервисов этим не подтверждается.", source)
        self.assertIn("Сигнал: Runtime/config", source)
        self.assertIn("Устойчивый failure episode", source)
        self.assertIn("Parent incident:", source)
        self.assertIn("failure family:", source)
        self.assertIn("channelServiceEpisodeSummary", source)

    def test_capture_only_entrypoint_consumes_without_constructing_planner_side_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            event = {
                "event_id": "sfe_capture_only_entrypoint",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "service": "youtube",
                "failure_episode_id": "sfep_capture_only",
                "failure_samples": 3,
                "bad_for_seconds": 180,
                "observed_at": "2026-07-25T08:02:00+00:00",
                "source_hashes": {"service_row": "hash"},
            }
            (event_dir / "service-failure-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
            args = self.autoswitch.build_arg_parser().parse_args([
                "--consume-passive-events-only",
                "--state-dir", str(state_dir),
                "--event-dir", str(event_dir),
                "--policy-file", str(root / "missing-policy.json"),
                "--org-policy-file", str(root / "missing-org-policy.json"),
            ])
            result = self.autoswitch.consume_passive_events_only(args)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["result"]["natural_event_candidates_captured"], 1)
            self.assertEqual(
                [row["stage"] for row in result["performance_timeline"]["spans"]],
                [
                    "passive_l3_current_state_load",
                    "passive_policy_and_signal_inputs",
                    "passive_event_source_window_load",
                    "passive_event_window_classification",
                    "passive_current_l3_projection_load",
                    "passive_new_event_projection",
                    "passive_durable_receipt_append",
                    "passive_reconciliation_l3_projection_load",
                    "passive_reconciliation_execution_ledger_load",
                    "passive_reconciliation_l3_and_execution_ledger_load",
                    "passive_reconciliation_feedback_ingest",
                    "passive_reconciliation_all_incident_scope_refresh",
                    "passive_reconciliation_recovery_and_state_write",
                    "passive_post_consumption_scope_reconciliation",
                    "passive_exact_once_event_consumption",
                ],
            )
            self.assertTrue(
                all(
                    row["runtime_mutation_performed"] is False
                    for row in result["performance_timeline"]["spans"]
                )
            )
            self.assertFalse(any(result["forbidden_effects"].values()))
            self.assertFalse((state_dir / "client-reconnect-state.json").exists())
            self.assertFalse((state_dir / "autoswitch-safety.json").exists())
            self.assertTrue((state_dir / "execution-events.jsonl").exists())
            self.assertTrue((state_dir / "closure-records.jsonl").exists())
            self.assertTrue((state_dir / "runtime-trust.jsonl").exists())

    def test_capture_only_entrypoint_rejects_apply_or_authority_flags(self):
        args = self.autoswitch.build_arg_parser().parse_args([
            "--consume-passive-events-only",
            "--apply",
            "--promote-authority-to", "LARGE_BATCH",
        ])
        result = self.autoswitch.consume_passive_events_only(args)
        self.assertEqual(result["status"], "STOP_SAFE_FORBIDDEN_FLAGS")
        self.assertIn("passive_consumer_forbids_apply", result["blockers"])
        self.assertIn("passive_consumer_forbids_promote_authority_to", result["blockers"])

    def test_passive_idempotent_reentry_consumes_new_packet_bound_outcome(self):
        """An already-consumed observation must not hide a newer action Outcome."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            incident_id = "sfinc_idempotent_outcome"
            source_scope = {
                "source_channel": "vless",
                "affected_scope_count": 1,
                "affected_scope_fingerprint": "scope_idempotent_outcome",
                "observed_at": "2026-07-27T12:00:00+00:00",
            }
            event = {
                "event_id": "sfrev_idempotent_outcome",
                "source_incident_id": incident_id,
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "service": "youtube",
                "failure_episode_id": "sfep_idempotent_outcome",
                "failure_samples": 3,
                "bad_for_seconds": 180,
                "observed_at": "2026-07-27T12:00:00+00:00",
                "source_hashes": {"service_row": "hash"},
                "source_scope": source_scope,
            }
            (event_dir / "service-failure-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg3 enabled=1\n", encoding="utf-8",
            )
            args = self.autoswitch.build_arg_parser().parse_args([
                "--consume-passive-events-only",
                "--state-dir", str(state_dir),
                "--event-dir", str(event_dir),
                "--policy-file", str(root / "missing-policy.json"),
                "--org-policy-file", str(root / "missing-org-policy.json"),
            ])
            first = self.autoswitch.consume_passive_events_only(args)
            self.assertEqual(first["result"]["reason"], "consumed")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb_idempotent_outcome",
                "source_channel": "vless",
                "target_channel": "awg3",
                "user": "10.0.0.2",
                "packet_id": "pkt_idempotent_outcome",
                "terminal_outcome_classification": "SUCCESS",
                "verification_result": {"success": True},
                "service_failure_causal_binding": {
                    "source_incident_id": incident_id,
                    "source_event_id": event["event_id"],
                    "source_event_ids": [event["event_id"]],
                    "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                    "source_scope": source_scope,
                },
            }
            with (state_dir / "execution-events.jsonl").open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(outcome) + "\n")
            second = self.autoswitch.consume_passive_events_only(args)
            third = self.autoswitch.consume_passive_events_only(args)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(item for item in state["incidents"].values() if item.get("incident_id") == incident_id)
        self.assertEqual(second["result"]["reason"], "already_consumed_idempotent")
        self.assertIn(
            "passive_idempotent_scope_reconciliation",
            [row["stage"] for row in second["performance_timeline"]["spans"]],
        )
        self.assertEqual(second["result"]["scope_reconciliation"]["consumed_records"], 1)
        self.assertEqual(third["result"]["scope_reconciliation"]["changed_records"], 0)
        self.assertEqual(record["last_execution_feedback_id"], outcome["feedback_id"])
        self.assertTrue(record["scope_accounting"]["terminal_scope_frozen"])
        self.assertFalse(any(second["forbidden_effects"].values()))

    def test_passive_consumer_prunes_only_consumptions_outside_current_event_window(self):
        """The exact-once cache may shrink without forgetting a current event."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            event = {
                "event_id": "sfe_current_window",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "failure_samples": 3,
                "bad_for_seconds": 180,
            }
            (event_dir / "service-failure-events.jsonl").write_text(
                json.dumps(event) + "\n", encoding="utf-8"
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "passive_event_consumptions": {
                    "sfe_expired_cache_entry": {"consumed_at": "old"},
                    event["event_id"]: {"consumed_at": "current"},
                },
            }), encoding="utf-8")
            args = self.autoswitch.build_arg_parser().parse_args([
                "--consume-passive-events-only",
                "--state-dir", str(state_dir),
                "--event-dir", str(event_dir),
                "--policy-file", str(root / "missing-policy.json"),
                "--org-policy-file", str(root / "missing-org-policy.json"),
            ])
            result = self.autoswitch.consume_passive_events_only(args)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
        self.assertEqual(result["result"]["reason"], "already_consumed_idempotent")
        self.assertEqual(
            state["passive_event_consumptions"],
            {"sfe_current_window": {"consumed_at": "current"}},
        )
        self.assertFalse(any(result["forbidden_effects"].values()))

    def test_jsonl_tail_reader_preserves_exact_latest_event_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "service-failure-events.jsonl"
            rows = [
                {"event_id": f"evt_{index}", "padding": "x" * 96}
                for index in range(6)
            ]
            path.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )
            result = self.autoswitch.read_jsonl(
                path, tail_limit=2, tail_max_bytes=400
            )
        self.assertEqual([row["event_id"] for row in result], ["evt_4", "evt_5"])

    def test_jsonl_exact_schema_reader_keeps_complete_matching_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "execution-events.jsonl"
            rows = [
                {"schema_version": "v7.passive-production-event-decision-trace.v1", "id": "passive"},
                {"schema_version": "v7.execution-outcome-record.v1", "feedback_id": "first"},
                {"schema_version": "v7.other.v1", "note": "v7.execution-outcome-record.v1"},
                {"schema_version": "v7.execution-outcome-record.v1", "feedback_id": "last"},
            ]
            path.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )
            result, active = self.autoswitch.read_jsonl_exact_schema(
                path, "v7.execution-outcome-record.v1"
            )
        self.assertTrue(active)
        self.assertEqual([row["feedback_id"] for row in result], ["first", "last"])

    def test_newer_owner_backed_scope_rotates_current_denominator_only(self):
        """A newer revalidation replaces only current scope, never Outcome history."""
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        state = {}
        incident_id = "sfinc_newer_scope"
        old = {
            "source_incident_id": incident_id,
            "event_id": "sfrev_old_scope",
            "source_event_ids": ["sfrev_old_scope"],
            "channel": "vless",
            "observed_at": "2026-07-27T12:00:00+00:00",
            "source_scope": {
                "source_channel": "vless", "affected_scope_count": 3,
                "affected_scope_fingerprint": "scope_old",
                "observed_at": "2026-07-27T12:00:00+00:00",
            },
        }
        newer = {
            **old,
            "event_id": "sfrev_new_scope",
            "source_event_ids": ["sfrev_new_scope"],
            "observed_at": "2026-07-27T12:15:00+00:00",
            "source_scope": {
                "source_channel": "vless", "affected_scope_count": 2,
                "affected_scope_fingerprint": "scope_new",
                "observed_at": "2026-07-27T12:15:00+00:00",
            },
        }
        planner._materialize_passive_incident_projection(state, old, terminal="STOP_SAFE_NO_ACTION")
        projection = planner._materialize_passive_incident_projection(state, newer, terminal="STOP_SAFE_NO_ACTION")
        record = state["incidents"][projection["incident_key"]]
        self.assertEqual(record["current_source_scope"]["baseline_event_id"], "sfrev_new_scope")
        self.assertEqual(record["current_source_scope"]["affected_scope_count"], 2)
        self.assertEqual(
            record["current_source_scope"]["supersedes_prior_scope_generation"]["rotation_reason"],
            "FRESHER_OWNER_BACKED_SOURCE_SCOPE_GENERATION",
        )

    def test_newer_matrix_snapshot_repairs_legacy_broken_scope_with_same_fingerprint(self):
        """Repair needs a fresh owner snapshot, not a guessed membership list."""
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        incident_id = "sfinc_legacy_scope_repair"
        incident_key = planner._passive_incident_projection_key(incident_id)
        state = {
            "incidents": {
                incident_key: {
                    "incident_key": incident_key,
                    "incident_id": incident_id,
                    "source_incident_id": incident_id,
                    "channel": "vless",
                    "current_source_scope": {
                        "status": "INCIDENT_SCOPE_ACCOUNTING_BROKEN",
                        "baseline_event_id": "sfrev_legacy",
                        "baseline_observed_at": "2026-07-27T12:00:00+00:00",
                        "affected_scope_count": 2,
                        "affected_scope_fingerprint": "scope_current",
                    },
                },
            },
        }
        fresh = {
            "source_incident_id": incident_id,
            "event_id": "sfrev_repaired",
            "source_event_ids": ["sfrev_repaired"],
            "channel": "vless",
            "observed_at": "2026-07-27T12:15:00+00:00",
            "source_scope": {
                "source_channel": "vless",
                "affected_scope_count": 2,
                "affected_scope_fingerprint": "scope_current",
                "observed_at": "2026-07-27T12:15:00+00:00",
            },
        }
        projection = planner._materialize_passive_incident_projection(
            state, fresh, terminal="STOP_SAFE_NO_ACTION"
        )
        scope = state["incidents"][projection["incident_key"]]["current_source_scope"]
        self.assertEqual(scope["status"], "ACCOUNTED")
        self.assertEqual(scope["baseline_event_id"], "sfrev_repaired")
        self.assertEqual(scope["protected_scope_count"], 0)
        self.assertEqual(scope["unresolved_scope_count"], 2)
        self.assertEqual(
            scope["supersedes_prior_scope_generation"]["rotation_reason"],
            "LIVE_ROUTE_SCOPE_NO_LONGER_RECONCILABLE_WITH_LEGACY_GENERATION",
        )

    def test_consumed_revalidation_repairs_broken_scope_from_newer_snapshot(self):
        """Exact-once does not discard a newer Matrix scope repair snapshot."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            incident_id = "sfinc_consumed_scope_repair"
            event = {
                "event_id": "sfrev_consumed_scope_repair",
                "source_incident_id": incident_id,
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "failure_samples": 3,
                "bad_for_seconds": 180,
                "observed_at": "2026-07-27T12:15:00+00:00",
                "source_hashes": {"service_row": "hash"},
                "source_scope": {
                    "source_channel": "vless",
                    "affected_scope_count": 2,
                    "affected_scope_fingerprint": "scope_current",
                    "observed_at": "2026-07-27T12:15:00+00:00",
                },
            }
            (event_dir / "service-failure-events.jsonl").write_text(
                json.dumps(event) + "\n", encoding="utf-8"
            )
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n",
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            incident_key = planner._passive_incident_projection_key(incident_id)
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {incident_key: {
                    "incident_key": incident_key,
                    "incident_id": incident_id,
                    "source_incident_id": incident_id,
                    "current_source_scope": {
                        "status": "INCIDENT_SCOPE_ACCOUNTING_BROKEN",
                        "baseline_observed_at": "2026-07-27T12:00:00+00:00",
                        "affected_scope_count": 2,
                        "affected_scope_fingerprint": "scope_current",
                    },
                }},
                "passive_event_consumptions": {
                    event["event_id"]: {"consumed_at": "2026-07-27T12:00:00+00:00"},
                },
            }), encoding="utf-8")
            args = self.autoswitch.build_arg_parser().parse_args([
                "--consume-passive-events-only",
                "--state-dir", str(state_dir),
                "--event-dir", str(event_dir),
                "--policy-file", str(root / "missing-policy.json"),
                "--org-policy-file", str(root / "missing-org-policy.json"),
            ])
            result = self.autoswitch.consume_passive_events_only(args)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            repaired = state["incidents"][incident_key]["current_source_scope"]
        self.assertEqual(result["result"]["reason"], "consumed_scope_repair")
        self.assertEqual(repaired["status"], "ACCOUNTED")
        self.assertFalse(any(result["forbidden_effects"].values()))

    def test_passive_consumer_does_not_materialize_unbound_expiry_as_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            (event_dir / "service-failure-events.jsonl").write_text(
                json.dumps({
                    "event_id": "sxe_without_parent",
                    "event_type": "SERVICE_FAILURE_EPISODE_EXPIRED",
                    "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_EPISODE_EXPIRY",
                    "channel": "vless",
                }) + "\n",
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.event_dir = event_dir
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.service_signal_policy = {
                "service_failure_persistence_samples": 3,
                "service_failure_persistence_window_seconds": 180,
            }
            planner.l3_runtime_state = {}
            result = planner._consume_passive_production_events()
            self.assertFalse(result["active"])
            self.assertEqual(result["reason"], "no_passive_capture_event")
            self.assertFalse((state_dir / "l3-runtime-state.json").exists())

    def test_matrix_lifecycle_reports_passive_consumer_success_and_failure_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            consumer = root / "passive-consumer"
            consumer.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'status':'PASS','result':{'reason':'consumed'}}))\n",
                encoding="utf-8",
            )
            consumer.chmod(0o755)
            ok = self.refresh.run_passive_consumer(
                str(consumer),
                state_dir=state_dir,
                event_dir=event_dir,
            )
            self.assertTrue(ok["ok"])
            self.assertEqual(ok["status"], "PASS")
            self.assertNotIn("omp_repair_frontier", ok)

            failed = self.refresh.run_passive_consumer(
                str(root / "missing-consumer"),
                state_dir=state_dir,
                event_dir=event_dir,
            )
            self.assertFalse(failed["ok"])
            self.assertEqual(failed["omp_repair_frontier"]["frontier_id"], "V7_PASSIVE_SERVICE_EVENT_CONSUMER_REPAIR")
            self.assertEqual(failed["omp_repair_frontier"]["forbidden_effects"], "NONE")

    def test_matrix_lifecycle_invokes_bounded_executor_only_with_active_standing_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            policy_file = root / "policy.json"
            policy_file.write_text("{}", encoding="utf-8")
            inactive = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertTrue(inactive["ok"])
            self.assertEqual(inactive["status"], "INACTIVE_NO_STANDING_POLICY")
            self.assertFalse(inactive["action_attempted"])

            valid_policy = {
                "delegated_autonomy_policy": {
                    "status": "ACTIVE",
                    "contract_id": "sdpc_test_tier4",
                    "contract_hash": "a" * 64,
                    "expires_at": "2099-08-27T02:06:51+00:00",
                    "policy": {
                        "allowed_action_classes": ["channel hard-fail failover"],
                        "max_users_per_action": 4,
                        "max_concurrent_transactions": 1,
                        "max_blast_radius": {"users": 4},
                        "policy_state": "APPROVED",
                        "runtime_apply_enabled": True,
                        "self_expansion_allowed": False,
                    },
                    "per_action_law": {
                        "max_users": 4,
                        "max_concurrent_transactions": 1,
                    },
                },
            }
            policy_file.write_text(
                json.dumps(valid_policy),
                encoding="utf-8",
            )
            obligation = {
                "schema_version": "v7.service-failure-automation-obligation.v1",
                "object_type": "service_failure_automation_obligation",
                "object_id": "sfaob_test_tier4",
                "automation_obligation_id": "sfaob_test_tier4",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "source_incident_id": "sfinc_test_tier4",
                "channel": "vless",
                "stop_safe_classification": "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED",
                "bounded_recommendation_users": 4,
                "current_source_scope": {
                    "affected_scope_count": 4,
                    "protected_scope_count": 0,
                    "unresolved_scope_count": 4,
                    "explicitly_excluded_or_recovered_scope_count": 0,
                    "affected_scope_fingerprint": "scope-test-tier4",
                    "raw_user_list_stored": False,
                },
            }
            executor = root / "executor"
            executor.write_text(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                "max_users=sys.argv[sys.argv.index('--max-users')+1]\n"
                "print(json.dumps({'final_verdict':'STOP_SAFE','users_moved':0,'apply_executed':False,'max_users_argument':max_users}))\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            executor.chmod(0o755)
            stop = self.refresh.run_bounded_delegated_service_failure_action(
                str(executor),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
                service_failure_obligation=obligation,
            )
            self.assertTrue(stop["ok"])
            self.assertEqual(stop["status"], "STOP_SAFE")
            self.assertTrue(stop["action_attempted"])
            self.assertEqual(stop["users_moved"], 0)
            self.assertEqual(stop["admitted_max_users"], 4)
            self.assertEqual(stop["max_concurrent_transactions"], 1)
            self.assertEqual(stop["consumer_result"]["max_users_argument"], "4")
            self.assertEqual(stop["contract_id"], "sdpc_test_tier4")
            command = stop["command"]
            self.assertEqual(
                command[command.index("--expected-standing-policy-contract-id") + 1],
                "sdpc_test_tier4",
            )
            self.assertEqual(
                command[command.index("--expected-standing-policy-contract-hash") + 1],
                "a" * 64,
            )
            self.assertEqual(
                command[command.index("--expected-service-failure-obligation-id") + 1],
                "sfaob_test_tier4",
            )
            self.assertEqual(
                command[command.index("--expected-service-failure-incident-id") + 1],
                "sfinc_test_tier4",
            )
            self.assertEqual(
                command[command.index("--expected-service-failure-scope-fingerprint") + 1],
                "scope-test-tier4",
            )
            self.assertEqual(
                command[command.index("--approved-source") + 1],
                "vless",
            )

            executor.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({"
                "'final_verdict':'GOVERNED_TRANSACTION_STOPPED',"
                "'transaction_status':'STOP_SAFE',"
                "'stop_reason':'packet_not_ready',"
                "'users_moved':0,'apply_executed':False}))\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            governed_stop = self.refresh.run_bounded_delegated_service_failure_action(
                str(executor),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
                service_failure_obligation=obligation,
            )
            self.assertTrue(governed_stop["ok"])
            self.assertEqual(governed_stop["status"], "STOP_SAFE")
            self.assertFalse(governed_stop["runtime_mutation_performed"])

            invalid_policy = json.loads(json.dumps(valid_policy))
            invalid_policy["delegated_autonomy_policy"]["per_action_law"]["max_users"] = 1
            policy_file.write_text(json.dumps(invalid_policy), encoding="utf-8")
            invalid = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertTrue(invalid["ok"])
            self.assertEqual(invalid["status"], "STOP_SAFE_INVALID_STANDING_POLICY_SCOPE")
            self.assertFalse(invalid["action_attempted"])
            self.assertEqual(invalid["users_moved"], 0)

            expired_policy = json.loads(json.dumps(valid_policy))
            expired_policy["delegated_autonomy_policy"]["expires_at"] = "2020-01-01T00:00:00+00:00"
            policy_file.write_text(json.dumps(expired_policy), encoding="utf-8")
            expired = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertTrue(expired["ok"])
            self.assertEqual(expired["status"], "STOP_SAFE_INVALID_STANDING_POLICY_SCOPE")
            self.assertFalse(expired["action_attempted"])

            zero_scope = json.loads(json.dumps(obligation))
            zero_scope["current_source_scope"]["affected_scope_count"] = 0
            zero_scope["current_source_scope"]["unresolved_scope_count"] = 0
            policy_file.write_text(json.dumps(valid_policy), encoding="utf-8")
            no_action = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
                service_failure_obligation=zero_scope,
            )
            self.assertEqual(no_action["status"], "STOP_SAFE_CURRENT_SOURCE_SCOPE_EMPTY")
            self.assertFalse(no_action["action_attempted"])
            self.assertEqual(no_action["users_moved"], 0)

            missing = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertEqual(missing["status"], "STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION")
            self.assertFalse(missing["action_attempted"])

    def test_advisory_without_result_has_no_obligation_and_does_not_crash(self):
        self.assertEqual(
            self.refresh.service_failure_obligation_from_advisory(None),
            {},
        )
        self.assertEqual(
            self.refresh.service_failure_obligation_from_advisory(
                {"status": "PASS", "result": None}
            ),
            {},
        )
        obligation = {"automation_obligation_id": "sfaob_exact"}
        self.assertEqual(
            self.refresh.service_failure_obligation_from_advisory(
                {"status": "PASS", "result": {"obligation": obligation}}
            ),
            obligation,
        )

    def test_campaign_binding_rejects_shallow_ready_target_when_full_admission_fails(self):
        authority = {
            "status": "APPROVED",
            "request_id": "cpsauth_exact",
            "request_hash": "a" * 64,
            "decision": (
                "APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN"
            ),
            "decision_id": "cpsdec_exact",
            "request": {
                "scope": {
                    "source_id": "controlled-source",
                    "controlled_target_id": "execution-target",
                    "campaign_stages": [5, 10, 25, 48],
                    "max_concurrent_transactions": 1,
                    "ordinary_customer_involvement": False,
                },
            },
        }
        campaign = {
            "ok": True,
            "completed_stages": [],
            "next_stage": 5,
            "controlled_production_proven_max": 0,
            "receipt_ids": [],
        }
        with mock.patch.object(
            self.refresh.operator_execution,
            "read_audit_records",
            return_value=[],
        ), mock.patch.object(
            self.refresh.operator_execution,
            "controlled_certification_substrate_authority_status",
            return_value=authority,
        ), mock.patch.object(
            self.refresh.operator_execution,
            "validate_controlled_certification_substrate_authority_request",
            return_value={"ok": True, "errors": []},
        ), mock.patch.object(
            self.refresh.operator_execution,
            "controlled_certification_campaign_stage_status",
            return_value=campaign,
        ):
            result = self.refresh.controlled_certification_matrix_binding(
                audit_store=Path("/tmp/not-read"),
                source="controlled-source",
                target_selection_diagnostic={
                    "ok": True,
                    "status": (
                        "NO_CURRENT_TARGET_CAPACITY_WITH_EXACT_OWNER_BOUNDARY"
                    ),
                    "inventory_fingerprint": "b" * 64,
                },
            )

        self.assertFalse(result["active"])
        self.assertFalse(result["ok"])
        self.assertIn(
            "controlled_campaign_target_full_live_admission_failed",
            result["blockers"],
        )
        self.assertEqual(
            result["target_selection_status"],
            "NO_CURRENT_TARGET_CAPACITY_WITH_EXACT_OWNER_BOUNDARY",
        )

    def test_matrix_binds_controlled_source_to_next_approved_campaign_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            policy_file = root / "policy.json"
            policy_file.write_text(json.dumps({
                "delegated_autonomy_policy": {
                    "status": "ACTIVE",
                    "contract_id": "sdpc_campaign",
                    "contract_hash": "b" * 64,
                    "expires_at": "2099-08-27T02:06:51+00:00",
                    "policy": {
                        "allowed_action_classes": [
                            "channel hard-fail failover",
                        ],
                        "max_users_per_action": 48,
                        "max_concurrent_transactions": 1,
                        "max_blast_radius": {"users": 48},
                        "policy_state": "APPROVED",
                        "runtime_apply_enabled": True,
                        "self_expansion_allowed": False,
                    },
                    "per_action_law": {
                        "max_users": 48,
                        "max_concurrent_transactions": 1,
                    },
                },
            }), encoding="utf-8")
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_campaign",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "source_incident_id": "sfinc_campaign",
                "channel": "controlled-source",
                "stop_safe_classification": (
                    "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED"
                ),
                # The execution-only campaign target is intentionally absent
                # from the ordinary planner recommendation.  Exact campaign
                # binding must reach the governed executor, which rechecks
                # every live target gate independently.
                "bounded_recommendation_users": 0,
                "current_source_scope": {
                    "affected_scope_count": 48,
                    "unresolved_scope_count": 48,
                    "affected_scope_fingerprint": "scope-campaign",
                },
            }
            executor = root / "executor"
            executor.write_text(
                "#!/usr/bin/env python3\n"
                "import json,sys\n"
                "print(json.dumps({'final_verdict':'STOP_SAFE',"
                "'apply_executed':False,'users_moved':0,"
                "'argv':sys.argv[1:]}))\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            executor.chmod(0o755)
            binding = {
                "active": True,
                "ok": True,
                "request_id": "cpsauth_campaign",
                "request_hash": "c" * 64,
                "decision_id": "cpsdec_campaign",
                "source": "controlled-source",
                "target": "execution-target",
                "stages": [5, 10, 25, 48],
                "completed_stages": [],
                "next_stage": 5,
            }
            with mock.patch.object(
                self.refresh,
                "controlled_certification_matrix_binding",
                return_value=binding,
            ):
                result = self.refresh.run_bounded_delegated_service_failure_action(
                    str(executor),
                    state_dir=state_dir,
                    event_dir=event_dir,
                    policy_file=policy_file,
                    operator_execution_audit_store=root / "audit.jsonl",
                    service_failure_obligation=obligation,
                )
        self.assertEqual(result["status"], "STOP_SAFE", result)
        self.assertEqual(result["requested_max_users"], 5)
        argv = result["consumer_result"]["argv"]
        self.assertEqual(argv[argv.index("--max-users") + 1], "5")
        self.assertEqual(
            argv[
                argv.index(
                    "--controlled-certification-campaign-request-id"
                ) + 1
            ],
            "cpsauth_campaign",
        )
        self.assertEqual(
            argv[
                argv.index(
                    "--controlled-certification-campaign-stage"
                ) + 1
            ],
            "5",
        )
        self.assertEqual(result["users_moved"], 0)

    def test_campaign_stage_receipt_requires_consumed_outcome_replay_learning_and_is_exact_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            binding = {
                "request_id": "cpsauth_stage",
                "request_hash": "d" * 64,
                "decision_id": "cpsdec_stage",
                "source": "controlled-source",
                "target": "execution-target",
                "next_stage": 5,
            }
            incomplete = self.refresh.record_controlled_campaign_stage_consumption(
                audit_store=audit,
                binding=binding,
                result={"fresh_packet_id": "pkt_incomplete"},
                reset_result={},
            )
            self.assertFalse(incomplete["audit_write"])
            self.assertFalse(audit.exists())

            result = {
                "fresh_packet_id": "pkt_stage",
                "final_verdict": "GOVERNED_TRANSACTION_COMPLETED",
                "apply_executed": True,
                "users_moved": 5,
                "feedback_materialization": {
                    "materialized": True,
                    "outcome_id": "out_stage",
                },
                "l3_learning_closure": {
                    "materialized": True,
                    "records": {"closure": 5},
                    "execution_closure_verification": {
                        "behavior_chain_status": "COMPLETE",
                        "terminal_consumer_verified": True,
                    },
                },
            }
            reset_result = {
                "ok": True,
                "consumer_result": {
                    "final_verdict": (
                        "CONTROLLED_CERTIFICATION_CAMPAIGN_STAGE_RESET_COMPLETE"
                    ),
                    "receipt_id": "reset_stage",
                    "target_user_count_after": 0,
                    "ordinary_customer_count": 0,
                    "users_moved": 5,
                    "final_safe_mode": "OPEN",
                },
            }
            first = self.refresh.record_controlled_campaign_stage_consumption(
                audit_store=audit,
                binding=binding,
                result=result,
                reset_result=reset_result,
            )
            second = self.refresh.record_controlled_campaign_stage_consumption(
                audit_store=audit,
                binding=binding,
                result=result,
                reset_result=reset_result,
            )
            self.assertTrue(first["audit_write"])
            self.assertFalse(second["audit_write"])
            self.assertTrue(second["duplicate_suppressed"])
            rows = [
                json.loads(line)
                for line in audit.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(rows), 1)
            self.assertTrue(rows[0]["outcome_consumed"])
            self.assertTrue(rows[0]["replay_consumed"])
            self.assertTrue(rows[0]["learning_consumed"])
            self.assertTrue(rows[0]["baseline_reset_verified"])

    def test_matrix_lifecycle_treats_no_pending_omp_obligation_as_legal_noop(self):
        completed = mock.Mock(
            returncode=0,
            stdout=json.dumps({
                "schema_version": "v7.service-failure-automation-omp-consumption.v1",
                "final_verdict": "NO_PENDING_OBLIGATION",
                "runtime_impact": "NONE",
                "routing_impact": "NONE",
                "user_movement": 0,
            }),
        )
        with mock.patch.object(self.refresh.subprocess, "run", return_value=completed):
            result = self.refresh.run_service_failure_omp_consumer()
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["consumer_result"]["final_verdict"], "NO_PENDING_OBLIGATION")

    def test_matrix_delegates_fresh_allocation_materialization_to_executor(self):
        fingerprint = "a" * 64
        diagnostic = {
            "status": "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED",
            "availability_first_standing_policy_admission": {
                "ok": True,
            },
            "shared_production_target_capacity_projection": {
                "availability_campaign": {
                    "next_stage": 1,
                    "completed": False,
                },
                "stage_allocations": {
                    "1": {
                        "feasible": True,
                        "allocation_fingerprint": fingerprint,
                    },
                },
            },
        }
        stopped = {
            "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
            "transaction_status": "STOP_SAFE",
            "stop_reason": "fresh_live_gate_failed",
            "blockers": ["fresh_live_gate_failed"],
        }
        calls = [
            mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
            mock.Mock(returncode=2, stdout=json.dumps(stopped)),
        ]
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=calls,
        ) as run:
            result = self.refresh.run_availability_first_standing_policy_stage(
                "v7-users-autoswitch",
                "v7-governed-canary-dry-run-cycle",
                state_dir=Path("/opt/v7/egress/state"),
                event_dir=Path("/opt/v7/events"),
                policy_file=Path("/etc/v7/policy.json"),
                audit_store=Path(
                    "/opt/v7/audit/operator-execution-audit.jsonl"
                ),
            )
        executor_command = run.call_args_list[1].args[0]
        self.assertIn(
            "--execute-availability-first-standing-stage",
            executor_command,
        )
        self.assertNotIn(
            "--expected-availability-first-allocation-fingerprint",
            executor_command,
        )
        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertEqual(
            result["allocation_fingerprint"],
            fingerprint,
        )

    def test_matrix_prefers_canonical_current_stage_over_stale_campaign_row(self):
        fingerprint = "a" * 64
        diagnostic = {
            "status": "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED",
            "availability_first_standing_policy_admission": {"ok": True},
            "shared_production_target_capacity_projection": {
                "current_stage": 25,
                "availability_campaign": {
                    # Historical progress can still name the predecessor.
                    "next_stage": 10,
                    "completed": False,
                },
                "stage_allocations": {
                    "25": {
                        "feasible": True,
                        "allocation_fingerprint": fingerprint,
                    },
                },
            },
        }
        stopped = {
            "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
            "transaction_status": "STOP_SAFE",
            "stop_reason": "fresh_live_gate_failed",
        }
        calls = [
            mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
            mock.Mock(returncode=2, stdout=json.dumps(stopped)),
        ]
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=calls,
        ) as run:
            self.refresh.run_availability_first_standing_policy_stage(
                "v7-users-autoswitch",
                "v7-governed-canary-dry-run-cycle",
                state_dir=Path("/opt/v7/egress/state"),
                event_dir=Path("/opt/v7/events"),
                policy_file=Path("/etc/v7/policy.json"),
                audit_store=Path(
                    "/opt/v7/audit/operator-execution-audit.jsonl"
                ),
            )
        command = run.call_args_list[1].args[0]
        stage_index = command.index("--availability-first-stage") + 1
        self.assertEqual(command[stage_index], "25")

    def test_matrix_consumes_successive_availability_stages_boundedly(self):
        completed_one = {
            "status": "ACTION_COMPLETED",
            "ok": True,
            "started_at": "2026-07-31T06:00:00+00:00",
            "action_attempted": True,
            "action_completed": True,
            "runtime_mutation_performed": True,
            "users_moved": 1,
            "stage": 1,
            "stage_consumption": {"receipt_id": "afstage_1"},
            "consumer_result": {
                "final_verdict": (
                    "AVAILABILITY_FIRST_STANDING_STAGE_COMPLETED"
                ),
                "stage": 1,
            },
        }
        completed_two = {
            **completed_one,
            "users_moved": 2,
            "stage": 2,
            "stage_consumption": {"receipt_id": "afstage_2"},
            "consumer_result": {
                "final_verdict": (
                    "AVAILABILITY_FIRST_STANDING_STAGE_COMPLETED"
                ),
                "stage": 2,
            },
        }
        stage_five_blocked = {
            "status": "NOT_REQUIRED_OR_NOT_ADMITTED",
            "ok": True,
            "action_attempted": False,
            "action_completed": False,
            "runtime_mutation_performed": False,
            "users_moved": 0,
            "stage": 5,
            "blockers": ["stage_capacity_not_yet_proven"],
            "durable_successor": (
                "EXISTING_MATRIX_FRESH_CAPACITY_REVALIDATION"
            ),
        }
        with mock.patch.object(
            self.refresh,
            "_run_availability_first_standing_policy_stage_once",
            side_effect=[
                completed_one,
                completed_two,
                stage_five_blocked,
            ],
        ) as consume:
            result = (
                self.refresh.run_availability_first_standing_policy_stage(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/opt/v7/egress/state"),
                    event_dir=Path("/opt/v7/events"),
                    policy_file=Path("/etc/v7/policy.json"),
                    audit_store=Path(
                        "/opt/v7/audit/operator-execution-audit.jsonl"
                    ),
                    max_successive_stages=6,
                )
            )

        self.assertEqual(consume.call_count, 3)
        self.assertTrue(result["action_completed"])
        self.assertEqual(
            result["completed_stages_this_invocation"],
            [1, 2],
        )
        self.assertEqual(result["stage"], 2)
        self.assertEqual(result["users_moved"], 3)
        self.assertEqual(
            result["successor_probe"]["stage"],
            5,
        )
        self.assertFalse(result["authority_expanded"])
        self.assertFalse(result["natural_l8_credit"])
        projected = self.refresh._consumer_projection(result)
        self.assertEqual(
            projected["completed_stages_this_invocation"],
            [1, 2],
        )
        self.assertEqual(
            projected["stage_consumption"]["receipt_id"],
            "afstage_2",
        )
        self.assertEqual(
            projected["successor_probe"]["stage"],
            5,
        )

    def test_availability_stage_timeout_scales_with_exact_cohort(self):
        fingerprint = "a" * 64
        diagnostic = {
            "status": (
                "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED"
            ),
            "availability_first_standing_policy_admission": {"ok": True},
            "shared_production_target_capacity_projection": {
                "availability_campaign": {
                    "next_stage": 48,
                    "completed": False,
                },
                "stage_allocations": {
                    "48": {
                        "feasible": True,
                        "allocation_fingerprint": fingerprint,
                    },
                },
            },
        }
        stopped = {
            "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
            "transaction_status": "STOP_SAFE",
            "stop_reason": "fresh_live_gate_failed",
        }
        calls = [
            mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
            mock.Mock(returncode=2, stdout=json.dumps(stopped)),
        ]
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=calls,
        ) as run:
            self.refresh._run_availability_first_standing_policy_stage_once(
                "v7-users-autoswitch",
                "v7-governed-canary-dry-run-cycle",
                state_dir=Path("/opt/v7/egress/state"),
                event_dir=Path("/opt/v7/events"),
                policy_file=Path("/etc/v7/policy.json"),
                audit_store=Path(
                    "/opt/v7/audit/operator-execution-audit.jsonl"
                ),
                timeout_sec=1830,
            )

        self.assertEqual(run.call_args_list[1].kwargs["timeout"], 17280)
        command = run.call_args_list[1].args[0]
        self.assertIn("--execute-performance-closure-benchmark", command)
        self.assertNotIn("--execute-availability-first-standing-stage", command)
        self.assertNotIn("--availability-first-stage", command)

    def test_performance_closure_receipt_is_exact_once_and_has_no_stage_credit(self):
        timing = {
            "status": "MONOTONIC_BREAKDOWN_CONSUMED",
            "analysis_schema_version": "v7.execution-performance-foundation.v1",
            "spans": [{"stage": "planner", "duration_ms": 1.0}],
        }
        result = {
            "final_verdict": "GOVERNED_PERFORMANCE_CLOSURE_BENCHMARK_COMPLETED",
            "campaign_stage_credit": False,
            "standing_policy_contract_id": "sdpc_test",
            "execution_allocation_fingerprint": "a" * 64,
            "packet_set_fingerprint": "b" * 64,
            "cohort_execution_timings": [{"timing": timing}],
            "reset_execution_timings": [{
                "packet_id": "pkt_reset",
                "operation_id": "op_reset",
                "timing": timing,
            }],
            "performance_timeline": [],
            "allocation_immutable": True,
            "capacity_reservation_verified": True,
            "outcome_consumed": True,
            "replay_consumed": True,
            "learning_consumed": True,
            "per_user_verification_passed": True,
            "per_target_verification_passed": True,
            "aggregate_verification_passed": True,
            "ordinary_user_protection_passed": True,
            "baseline_reset_verified": True,
        }
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "audit.jsonl"
            first = self.refresh.record_performance_closure_consumption(
                audit_store=store, result=result
            )
            duplicate = self.refresh.record_performance_closure_consumption(
                audit_store=store, result=result
            )
            rows = self.refresh.operator_execution.read_audit_records(store)
        self.assertTrue(first["audit_write"])
        self.assertTrue(duplicate["duplicate_suppressed"])
        matches = [row for row in rows if row.get("record_type") == self.refresh.PERFORMANCE_CLOSURE_RECORD_TYPE]
        self.assertEqual(len(matches), 1)
        self.assertEqual(
            matches[0]["performance_revalidation_generation"],
            self.refresh.PERFORMANCE_REVALIDATION_GENERATION,
        )
        self.assertFalse(matches[0]["campaign_stage_credit"])
        self.assertFalse(matches[0]["stage_48_executed"])

    def test_reset_timing_projection_is_shared_by_recovery_and_normal_paths(self):
        timing = {
            "status": "MONOTONIC_BREAKDOWN_CONSUMED",
            "analysis_schema_version": (
                "v7.execution-performance-foundation.v1"
            ),
        }
        rows = self.cycle.reset_execution_timing_rows([{
            "fresh_packet_id": "pkt_reset",
            "operation_id": "op_reset",
            "execution_timing": timing,
        }])

        self.assertEqual(rows, [{
            "packet_id": "pkt_reset",
            "operation_id": "op_reset",
            "timing": timing,
        }])
        self.assertEqual(
            self.cycle.reset_execution_timing_rows([{
                "fresh_packet_id": "pkt_without_time",
            }]),
            [],
        )

    def test_performance_receipt_enables_stage_48_inside_active_standing_contract(self):
        diagnostic = {
            "status": "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED",
            "availability_first_standing_policy_admission": {"ok": True},
            "shared_production_target_capacity_projection": {
                "current_stage": 48,
                "availability_campaign": {
                    "next_stage": 48,
                    "completed": False,
                    "completed_stages": [1, 2, 5, 10, 25],
                },
                "stage_allocations": {
                    "48": {
                        "feasible": True,
                        "allocation_fingerprint": "a" * 64,
                    },
                },
            },
        }
        executor_result = {
            "final_verdict": "AVAILABILITY_FIRST_STANDING_STAGE_COMPLETED",
            "stage": 48,
            "runtime_mutation_performed": False,
            "users_moved": 0,
        }
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=[
                mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
                mock.Mock(returncode=0, stdout=json.dumps(executor_result)),
            ],
        ) as run, mock.patch.object(
            self.refresh,
            "current_performance_closure_receipt",
            return_value={"receipt_id": "perfclose_unit"},
        ), mock.patch.object(
            self.refresh,
            "record_availability_first_stage_consumption",
            return_value={
                "receipt_id": "afstage_unit",
                "audit_write": True,
                "duplicate_suppressed": False,
            },
        ):
            result = (
                self.refresh._run_availability_first_standing_policy_stage_once(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/opt/v7/egress/state"),
                    event_dir=Path("/opt/v7/events"),
                    policy_file=Path("/etc/v7/policy.json"),
                    audit_store=Path(
                        "/opt/v7/audit/operator-execution-audit.jsonl"
                    ),
                )
            )

        self.assertEqual(run.call_count, 2)
        self.assertEqual(result["status"], "ACTION_COMPLETED")
        self.assertTrue(result["stage_48_optimized_runtime_ready"])
        self.assertTrue(result["stage_48_execution_permitted"])
        self.assertTrue(result["action_attempted"])
        self.assertEqual(result["users_moved"], 0)

    def test_performance_projection_preserves_no_stage_credit_scope(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "final_verdict": (
                    "GOVERNED_PERFORMANCE_CLOSURE_BENCHMARK_COMPLETED"
                ),
                "stage": 1,
                "performance_benchmark": True,
                "campaign_stage_credit": False,
                "cohort_execution_timings": [{
                    "timing": {"status": "MONOTONIC_BREAKDOWN_CONSUMED"},
                }],
                "performance_timeline": [{"phase": "planner"}],
            },
        })

        projected = projected["consumer_result"]
        self.assertTrue(projected["performance_benchmark"])
        self.assertFalse(projected["campaign_stage_credit"])
        self.assertEqual(
            projected["execution_scope_kind"],
            "PERFORMANCE_BENCHMARK_NO_STAGE_CREDIT",
        )
        self.assertEqual(projected["benchmark_scope"], 1)
        self.assertEqual(projected["campaign_stage"], 0)
        self.assertEqual(len(projected["cohort_execution_timings"]), 1)

    def test_advisory_timing_projection_retains_only_compact_advisory_spans(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "status": "PASS",
                "performance_timeline": {
                    "schema_version": "v7.governed-transaction-nested-timing.v1",
                    "clock_source": "time.monotonic_ns",
                    "owner": "tools/v7-users-autoswitch",
                    "spans": [
                        {
                            "stage": "advisory_l3_and_closure_history_load",
                            "parent": "service_failure_advisory_materialization",
                            "owner": "tools/v7-users-autoswitch",
                            "duration_ms": 12.5,
                            "critical_path": True,
                            "started_monotonic_ns": 1,
                            "completed_monotonic_ns": 2,
                        },
                        {
                            "stage": "planner_initialization_total",
                            "parent": "governed_transaction",
                            "owner": "tools/v7-users-autoswitch",
                            "duration_ms": 1.0,
                            "critical_path": True,
                        },
                    ],
                },
            },
        })["consumer_result"]

        spans = projected["advisory_performance_timeline"]["spans"]
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0]["stage"], "advisory_l3_and_closure_history_load")
        self.assertNotIn("started_monotonic_ns", spans[0])

    def test_matrix_projection_retains_bounded_cohort_policy_stop_reason(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
                "transaction_status": "STOP_SAFE",
                "stop_reason": "standing_delegated_cohort_policy_binding_invalid",
                "standing_delegated_policy_binding": {
                    "ok": False,
                    "blockers": ["standing_policy_action_class_not_allowed"],
                    "max_users_per_action": 4,
                    "max_concurrent_transactions": 1,
                    "action_class": "SERVICE_FAILURE_COHORT_4",
                    "authority_audit_verified": True,
                    "self_expansion_allowed": False,
                    "full_contract": "must-not-project",
                },
            },
        })["consumer_result"]

        binding = projected["standing_delegated_policy_binding"]
        self.assertFalse(binding["ok"])
        self.assertEqual(
            binding["blockers"],
            ["standing_policy_action_class_not_allowed"],
        )
        self.assertNotIn("full_contract", binding)

    def test_matrix_projection_retains_bounded_planner_plan_diagnosis(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
                "transaction_status": "STOP_SAFE",
                "stop_reason": "l3_production_validation_plan_unavailable",
                "planner_plan_availability": {
                    "ok": False,
                    "returncode": 2,
                    "stderr_tail": "source has no eligible ordinary decision",
                    "raw_child_response": "must-not-project",
                },
            },
        })["consumer_result"]

        diagnosis = projected["planner_plan_availability"]
        self.assertFalse(diagnosis["ok"])
        self.assertEqual(diagnosis["returncode"], 2)
        self.assertEqual(
            diagnosis["stderr_tail"],
            "source has no eligible ordinary decision",
        )
        self.assertNotIn("raw_child_response", diagnosis)

    def test_matrix_projection_retains_ordinary_pre_packet_scope_counts(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "ordinary_pre_packet_scope": {
                    "valid": False,
                    "selected_count": 4,
                    "requested_max_users": 4,
                    "certification_selected_count": 1,
                    "selected_identities": ["must-not-project"],
                },
            },
        })["consumer_result"]

        scope = projected["ordinary_pre_packet_scope"]
        self.assertFalse(scope["valid"])
        self.assertEqual(scope["selected_count"], 4)
        self.assertEqual(scope["certification_selected_count"], 1)
        self.assertNotIn("selected_identities", scope)

    def test_matrix_projection_retains_bounded_packet_stop_error(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
                "transaction_status": "STOP_SAFE",
                "stop_reason": "l3_packet_materialization_failed",
                "error": "existing_packet_owner_rejected_incomplete_scope",
                "raw_packet": {"must-not-project": True},
            },
        })["consumer_result"]

        self.assertEqual(
            projected["error"],
            "existing_packet_owner_rejected_incomplete_scope",
        )
        self.assertNotIn("raw_packet", projected)

    def test_matrix_projection_retains_bounded_downstream_proof_terminal(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "final_verdict": "STOP_SAFE",
                "stop_reason": "l3_production_validation_downstream_proof_failed",
                "downstream_proof_diagnostic": {
                    "apply_command_ok": True,
                    "apply_returncode": 0,
                    "apply_timed_out": False,
                    "child_final_verdict": "STOP_SAFE",
                    "child_transaction_status": "STOP_SAFE",
                    "child_stop_reason": "route_visibility_not_confirmed",
                    "proof_blockers": ["route_visibility_not_confirmed"],
                    "route_apply_failure_count": 1,
                    "route_apply_failure_reasons": ["route_writer_apply_failed"],
                    "verification_failure_count": 1,
                    "verification_failure_reasons": ["route_verify_failed"],
                    "route_verification_failure_categories": ["TABLE_DEFAULT_MISMATCH"],
                    "route_verification_scopes": ["selected_user"],
                    "rollback_failure_count": 0,
                    "raw_child_payload": {"must-not-project": True},
                },
            },
        })["consumer_result"]

        diagnostic = projected["downstream_proof_diagnostic"]
        self.assertTrue(diagnostic["apply_command_ok"])
        self.assertEqual(diagnostic["route_apply_failure_count"], 1)
        self.assertEqual(
            diagnostic["route_apply_failure_reasons"],
            ["route_writer_apply_failed"],
        )
        self.assertEqual(
            diagnostic["child_stop_reason"],
            "route_visibility_not_confirmed",
        )
        self.assertEqual(
            diagnostic["verification_failure_reasons"],
            ["route_verify_failed"],
        )
        self.assertEqual(
            diagnostic["route_verification_failure_categories"],
            ["TABLE_DEFAULT_MISMATCH"],
        )
        self.assertEqual(diagnostic["route_verification_scopes"], ["selected_user"])
        self.assertNotIn("raw_child_payload", diagnostic)

    def test_matrix_recovers_partial_apply_from_append_only_event_after_summary_advances(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.100 current=awg0 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix-refresh-summary.json").write_text(
                json.dumps({
                    "availability_first_standing_policy_action": {
                        "status": "STOP_SAFE",
                        "consumer_result": {
                            "stop_reason": (
                                "availability_first_standing_stage_not_admitted"
                            ),
                        },
                    },
                }),
                encoding="utf-8",
            )
            (events / "service-matrix-refresh-20260731.jsonl").write_text(
                json.dumps({
                    "availability_first_standing_policy_action": {
                        "status": "STOP_SAFE",
                        "stage": 1,
                        "consumer_result": {
                            "stage": 1,
                            "packet_set": [{
                                "stop_reason": (
                                    "l3_production_validation_downstream_proof_failed"
                                ),
                                "user": "10.7.0.100",
                                "source": "vless",
                                "target": "awg0",
                            }],
                        },
                    },
                }) + "\n",
                encoding="utf-8",
            )
            (events / "service-matrix-refresh-20260727.jsonl").write_bytes(
                b"x" * (
                    self.refresh.RECENT_MATRIX_EVENT_BYTE_LIMIT * 2
                )
            )
            diagnostic = {
                "status": "STOP_SAFE",
                "availability_first_standing_policy_admission": {
                    "ok": True,
                },
                "shared_production_target_capacity_projection": {
                    "availability_campaign": {
                        "next_stage": 1,
                        "completed": False,
                    },
                    "stage_allocations": {},
                },
            }
            reconciled = {
                "final_verdict": (
                    "AVAILABILITY_FIRST_PARTIAL_APPLY_BASELINE_RECONCILED"
                ),
                "transaction_status": "STOP_SAFE",
                "stop_reason": (
                    "fresh_retry_required_after_partial_apply_reconciliation"
                ),
                "stage": 1,
                "baseline_reset_verified": True,
            }
            calls = [
                mock.Mock(returncode=2, stdout=json.dumps(diagnostic)),
                mock.Mock(returncode=2, stdout=json.dumps(reconciled)),
            ]
            with mock.patch.object(
                self.refresh.subprocess,
                "run",
                side_effect=calls,
            ) as run:
                result = (
                    self.refresh.run_availability_first_standing_policy_stage(
                        "v7-users-autoswitch",
                        "v7-governed-canary-dry-run-cycle",
                        state_dir=state,
                        event_dir=events,
                        policy_file=root / "policy.json",
                        audit_store=root / "audit.jsonl",
                    )
                )

        self.assertEqual(len(run.call_args_list), 2)
        self.assertIn(
            "--execute-availability-first-standing-stage",
            run.call_args_list[1].args[0],
        )
        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertEqual(
            result["consumer_result"]["final_verdict"],
            "AVAILABILITY_FIRST_PARTIAL_APPLY_BASELINE_RECONCILED",
        )

    def test_matrix_does_not_recover_completed_stage_over_current_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.100 current=awg0 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            # This is historical Stage-10 partial-reset evidence.  Its
            # immutable receipt already consumed Stage 10, so it cannot take
            # ownership from the live Stage-25 successor.
            (events / "service-matrix-refresh-20260801.jsonl").write_text(
                json.dumps({
                    "availability_first_standing_policy_action": {
                        "status": "STOP_SAFE",
                        "stage": 10,
                        "consumer_result": {
                            "stage": 10,
                            "circuit_breaker": {
                                "reason": (
                                    "availability_first_baseline_reset_failed"
                                ),
                            },
                            "packet_set": [{
                                "final_verdict": "L3_PRODUCTION_PROVEN",
                                "verification_result": "PASS",
                                "users_moved": 1,
                                "user": "10.7.0.100",
                                "source": "vless",
                                "target": "awg0",
                            }],
                        },
                    },
                }) + "\n",
                encoding="utf-8",
            )
            diagnostic = {
                "status": "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED",
                "availability_first_standing_policy_admission": {"ok": True},
                "shared_production_target_capacity_projection": {
                    "current_stage": 25,
                    "availability_campaign": {
                        "next_stage": 25,
                        "completed_stages": [1, 2, 5, 10],
                        "completed": False,
                    },
                    "stage_allocations": {
                        "25": {
                            "feasible": True,
                            "allocation_fingerprint": "a" * 64,
                        },
                    },
                },
            }
            stopped = {
                "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
                "transaction_status": "STOP_SAFE",
                "stop_reason": "fresh_live_gate_failed",
            }
            calls = [
                mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
                mock.Mock(returncode=2, stdout=json.dumps(stopped)),
            ]
            with mock.patch.object(
                self.refresh.subprocess,
                "run",
                side_effect=calls,
            ) as run:
                self.refresh.run_availability_first_standing_policy_stage(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=state,
                    event_dir=events,
                    policy_file=root / "policy.json",
                    audit_store=root / "audit.jsonl",
                )
        command = run.call_args_list[1].args[0]
        stage_index = command.index("--availability-first-stage") + 1
        self.assertEqual(command[stage_index], "25")

    def test_matrix_consumes_verified_stage_pending_only_baseline_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                (
                    "ip=10.7.0.100 current=awg0 enabled=1 "
                    "certification_user=1\n"
                ),
                encoding="utf-8",
            )
            (state / "service-matrix-refresh-summary.json").write_text(
                json.dumps({
                    "availability_first_standing_policy_action": {
                        "status": "STOP_SAFE",
                        "stage": 1,
                        "consumer_result": {
                            "stage": 1,
                            "circuit_breaker": {
                                "tripped": True,
                                "reason": (
                                    "availability_first_baseline_reset_failed"
                                ),
                            },
                            "packet_set": [{
                                "final_verdict": "L3_PRODUCTION_PROVEN",
                                "transaction_status": "COMPLETED",
                                "verification_result": "PASS",
                                "users_moved": 1,
                                "user": "10.7.0.100",
                                "source": "vless",
                                "target": "awg0",
                            }],
                        },
                    },
                }),
                encoding="utf-8",
            )
            diagnostic = {
                "status": "STOP_SAFE",
                "availability_first_standing_policy_admission": {
                    "ok": True,
                },
                "shared_production_target_capacity_projection": {
                    "availability_campaign": {
                        "next_stage": 1,
                        "completed": False,
                    },
                    "stage_allocations": {},
                },
            }
            reconciled = {
                "final_verdict": (
                    "AVAILABILITY_FIRST_STANDING_STAGE_COMPLETED"
                ),
                "transaction_status": "COMPLETED",
                "stage": 1,
                "standing_policy_contract_id": "sdpc_test",
                "standing_policy_contract_hash": "a" * 64,
                "allocation_immutable": True,
                "capacity_reservation_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "per_user_verification_passed": True,
                "per_target_verification_passed": True,
                "aggregate_verification_passed": True,
                "ordinary_user_protection_passed": True,
                "baseline_reset_verified": True,
                "allocation": [{
                    "target_id": "awg0",
                    "allocated_users": 1,
                    "target_fingerprint": "b" * 64,
                    "capacity_bounds_fingerprint": "c" * 64,
                }],
            }
            calls = [
                mock.Mock(returncode=2, stdout=json.dumps(diagnostic)),
                mock.Mock(returncode=0, stdout=json.dumps(reconciled)),
            ]
            with mock.patch.object(
                self.refresh.subprocess,
                "run",
                side_effect=calls,
            ) as run, mock.patch.object(
                self.refresh,
                "record_availability_first_stage_consumption",
                return_value={
                    "receipt_id": "afstage_test",
                    "audit_write": True,
                    "duplicate_suppressed": False,
                },
            ) as record:
                result = (
                    self.refresh.run_availability_first_standing_policy_stage(
                        "v7-users-autoswitch",
                        "v7-governed-canary-dry-run-cycle",
                        state_dir=state,
                        event_dir=events,
                        policy_file=root / "policy.json",
                        audit_store=root / "audit.jsonl",
                    )
                )

        self.assertEqual(len(run.call_args_list), 2)
        self.assertEqual(result["status"], "ACTION_COMPLETED")
        self.assertTrue(result["action_completed"])
        record.assert_called_once()

    def test_matrix_projection_preserves_bounded_partial_reset_terminal(self):
        projected = self.refresh._consumer_projection({
            "status": "STOP_SAFE",
            "consumer_result": {
                "final_verdict": "AVAILABILITY_FIRST_STANDING_STAGE_STOPPED",
                "transaction_status": "STOP_SAFE",
                "stop_reason": "availability_first_partial_apply_recovery_failed",
                "partial_apply_recovery": {
                    "pending": True,
                    "ok": True,
                    "stage": 1,
                    "user": "10.7.0.100",
                    "source": "vless",
                    "target": "awg0",
                    "packet_id": "pkt_partial",
                    "operation_id": "govexec_partial",
                    "projection_source": "append_only_matrix_event",
                },
                "reset_transaction": {
                    "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
                    "transaction_status": "STOP_SAFE",
                    "stop_reason": "packet_not_ready",
                    "runtime_mutation_performed": False,
                    "users_moved": 0,
                },
                "stage": 1,
                "baseline_reset_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "durable_successor": (
                    "EXISTING_MATRIX_RECOMPUTE_"
                    "AVAILABILITY_FIRST_NEXT_STAGE"
                ),
                "stage_total_duration_us": 123456,
                "serial_baseline_reset_count": 1,
                "allocation_lineage_refresh_count": 1,
                "performance_timeline": [{
                    "phase": "reset_transaction",
                    "owner": "existing governed transaction owner",
                    "status": "STOP_SAFE",
                    "member_id": "10.7.0.100",
                    "started_offset_us": 100,
                    "duration_us": 123000,
                    "sensitive_payload": "must-not-project",
                }],
                "baseline_reset_reconciliation": {
                    "ok": True,
                    "mode": (
                        "PARTIAL_CHILD_TERMINAL_RECONCILED_"
                        "FROM_EXISTING_OWNERS"
                    ),
                    "current_egress": "vless",
                    "packet_id": "pkt_reset",
                    "operation_id": "govexec_reset",
                    "switch_lineage": True,
                    "natural_l8_credit": False,
                    "production_outcome_credit": False,
                },
            },
        })

        consumer = projected["consumer_result"]
        self.assertTrue(consumer["partial_apply_recovery"]["ok"])
        self.assertEqual(
            consumer["reset_transaction"]["stop_reason"],
            "packet_not_ready",
        )
        self.assertEqual(consumer["stage"], 1)
        self.assertTrue(consumer["baseline_reset_verified"])
        self.assertTrue(consumer["outcome_consumed"])
        self.assertEqual(
            consumer["baseline_reset_reconciliation"]["mode"],
            (
                "PARTIAL_CHILD_TERMINAL_RECONCILED_"
                "FROM_EXISTING_OWNERS"
            ),
        )
        self.assertFalse(
            consumer["baseline_reset_reconciliation"][
                "production_outcome_credit"
            ]
        )
        self.assertEqual(consumer["stage_total_duration_us"], 123456)
        self.assertEqual(consumer["serial_baseline_reset_count"], 1)
        self.assertEqual(consumer["allocation_lineage_refresh_count"], 1)
        self.assertEqual(
            consumer["performance_timeline"][0]["phase"],
            "reset_transaction",
        )
        self.assertNotIn(
            "sensitive_payload", consumer["performance_timeline"][0]
        )

    def test_matrix_projection_distinguishes_target_trial_from_campaign_stage(self):
        projected = self.refresh._consumer_projection({
            "consumer_result": {
                "stage": 10,
                "target_bound_trial": True,
                "target_bound_trial_target": "awg3",
                "campaign_next_stage": 25,
                "transaction_status": "STOP_SAFE",
            },
        })
        result = projected["consumer_result"]
        self.assertEqual(result["execution_scope_kind"], "TARGET_BOUND_TRIAL")
        self.assertEqual(result["trial_scope"], 10)
        self.assertEqual(result["campaign_stage"], 25)
        self.assertEqual(result["target_bound_trial_target"], "awg3")

    def test_refresh_projection_keeps_child_consumer_output_out_of_periodic_journal(self):
        payload = {
            "updated": "2026-07-27T14:00:00+00:00",
            "total": 1,
            "ok_count": 1,
            "results": [{"egress": "vless", "ok": False, "status": "FAIL", "output_tail": "x" * 100000}],
            "bounded_delegated_service_failure_action": {
                "status": "ACTION_COMPLETED",
                "ok": True,
                "users_moved": 1,
                "consumer_result": {"packet_id": "pkt_test", "nested": "x" * 100000},
            },
            "availability_first_standing_policy_action": {
                "status": "STOP_SAFE",
                "ok": True,
                "stage": 1,
                "diagnostic_status": "MEASURED_STOP",
                "consumer_result": {
                    "final_verdict": "AVAILABILITY_FIRST_STANDING_STAGE_STOPPED",
                    "transaction_status": "STOP_SAFE",
                    "circuit_breaker": {
                        "tripped": True,
                        "remaining_subsets_stopped": True,
                        "reason": "fresh_capacity_gate_failed",
                        "nested": "x" * 100000,
                    },
                    "packet_set": [{
                        "final_verdict": "STOP_SAFE",
                        "stop_reason": "fresh_capacity_gate_failed",
                        "target_id": "awg3",
                        "users_moved": 0,
                        "downstream_proof_diagnostic": {
                            "apply_command_ok": False,
                            "apply_returncode": 2,
                            "apply_timed_out": False,
                            "child_stop_reason": "exact_child_terminal",
                            "proof_blockers": [
                                "runtime_apply_not_performed"
                            ],
                            "sensitive_payload": "must-not-project",
                        },
                        "nested": "x" * 100000,
                    }],
                    "nested": "x" * 100000,
                },
            },
        }
        projection = self.refresh.compact_refresh_projection(payload)
        serialized = json.dumps(projection)
        self.assertLess(len(serialized), 5000)
        self.assertEqual(projection["bounded_delegated_service_failure_action"]["consumer_result"]["packet_id"], "pkt_test")
        self.assertEqual(
            projection["availability_first_standing_policy_action"]["stage"],
            1,
        )
        self.assertEqual(
            projection["availability_first_standing_policy_action"][
                "diagnostic_status"
            ],
            "MEASURED_STOP",
        )
        availability_terminal = projection[
            "availability_first_standing_policy_action"
        ]["consumer_result"]
        self.assertEqual(
            availability_terminal["circuit_breaker"]["reason"],
            "fresh_capacity_gate_failed",
        )
        self.assertEqual(
            availability_terminal["packet_set"][0]["target_id"],
            "awg3",
        )
        self.assertEqual(
            availability_terminal["packet_set"][0]["users_moved"],
            0,
        )
        self.assertEqual(
            availability_terminal["packet_set"][0][
                "downstream_proof_diagnostic"
            ]["child_stop_reason"],
            "exact_child_terminal",
        )
        self.assertNotIn(
            "sensitive_payload",
            availability_terminal["packet_set"][0][
                "downstream_proof_diagnostic"
            ],
        )
        self.assertNotIn("nested", serialized)
        self.assertTrue(projection["candidate_or_execution_forbidden"])

    def test_refresh_projection_consumes_nested_prepared_and_closure_receipts(self):
        projection = self.refresh.compact_refresh_projection({
            "service_failure_automation_advisory": {
                "status": "PASS",
                "ok": True,
                "consumer_result": {
                    "status": "PASS",
                    "prepared_class_decisions": {
                        "status": "PREPARED_CLASS_DECISION_AVAILABLE",
                        "class_count": 2,
                        "classes": [{"class_id": "pcd_a"}, {"class_id": "pcd_b"}],
                    },
                    "prepared_class_decision_freshness": {
                        "status": "PREPARED_CLASS_DECISION_FRESH",
                        "world_model_rebuilt": False,
                    },
                    "bounded_closure_reconciliation": {
                        "status": "DEFERRED_CLOSURE_DURABLE_SUCCESSOR_PROVEN",
                        "closure_obligations_published": 1,
                    },
                },
            },
        })
        receipt = projection["service_failure_automation_advisory"]["consumer_result"]
        self.assertEqual(receipt["prepared_class_decisions"]["class_count"], 2)
        self.assertEqual(receipt["prepared_class_decision_freshness"]["status"], "PREPARED_CLASS_DECISION_FRESH")
        self.assertEqual(receipt["bounded_closure_reconciliation"]["status"], "DEFERRED_CLOSURE_DURABLE_SUCCESSOR_PROVEN")

    def test_compact_matrix_receipt_retains_passive_scalar_timings_only(self):
        projection = self.refresh.compact_refresh_projection({
            "passive_event_consumer": {
                "status": "PASS",
                "ok": True,
                "consumer_result": {
                    "status": "PASS",
                    "performance_timeline": {
                        "schema_version": "v7.passive-event-consumer-timing.v1",
                        "spans": [
                            {
                                "stage": "passive_l3_current_state_load",
                                "owner": "existing-owner",
                                "clock_source": "time.monotonic_ns",
                                "duration_ms": 12.3,
                                "raw_state": "must-not-project",
                            },
                        ],
                    },
                },
            },
        })
        receipt = projection["passive_event_consumer"]["consumer_result"]
        self.assertEqual(
            receipt["passive_performance_timeline"]["spans"][0]["duration_ms"],
            12.3,
        )
        self.assertNotIn("raw_state", json.dumps(projection))

    def test_compact_matrix_receipt_retains_nested_outcome_pointer_without_payload(self):
        projection = self.refresh.compact_refresh_projection({
            "bounded_delegated_service_failure_action": {
                "status": "ACTION_COMPLETED", "ok": True,
                "consumer_result": {
                    "final_verdict": "GOVERNED_TRANSACTION_COMPLETED",
                    "feedback_materialization": {
                        "feedback_id": "execfb_unit", "learning_record_id": "learn_unit",
                        "nested": "x" * 100000,
                    },
                },
            },
        })
        receipt = projection["bounded_delegated_service_failure_action"]["consumer_result"]
        self.assertEqual(receipt["feedback_id"], "execfb_unit")
        self.assertEqual(receipt["learning_record_id"], "learn_unit")
        self.assertNotIn("nested", json.dumps(projection))

    def test_topology_standing_consumer_routes_exact_manifest_to_existing_executor(self):
        diagnostic = {
            "status": "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
            "production_preflight": {
                "manifest": {
                    "manifest_hash": "a" * 64,
                    "trial_identity": "10.7.0.100",
                    "trial_identity_count": 1,
                    "existing_source": "1",
                    "selected_source_or_draft": "vless",
                    "expected_ordinary_assignment_delta": "NONE",
                    "expected_ordinary_route_delta": "NONE",
                },
            },
            "standing_policy_admission": {
                "status": (
                    "AUTO_ADMITTED_BY_STANDING_DELEGATED_"
                    "CONTROLLED_TOPOLOGY_POLICY"
                ),
                "ok": True,
                "contract_id": "sdpc_exact",
                "contract_hash": "b" * 64,
            },
        }
        executed = {
            "controlled_topology_final_verdict": (
                "ONE_IDENTITY_AUTONOMOUS_CONTROLLED_TOPOLOGY_TRIAL_PROVEN"
            ),
            "users_moved": 1,
            "runtime_mutation_performed": True,
            "fresh_packet_id": "pkt_exact",
        }
        calls = [
            mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
            mock.Mock(returncode=0, stdout=json.dumps(executed)),
        ]
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=calls,
        ) as run:
            result = (
                self.refresh.run_controlled_topology_standing_policy_action(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/state"),
                    event_dir=Path("/events"),
                    policy_file=Path("/policy"),
                    audit_store=Path("/audit"),
                )
            )
        self.assertEqual(result["status"], "ACTION_COMPLETED")
        self.assertTrue(result["action_completed"])
        self.assertEqual(result["users_moved"], 1)
        command = run.call_args_list[1].args[0]
        self.assertIn(
            "--execute-controlled-topology-standing-transaction",
            command,
        )
        self.assertEqual(
            command[
                command.index("--expected-controlled-topology-manifest-hash")
                + 1
            ],
            "a" * 64,
        )
        self.assertEqual(
            command[command.index("--controlled-topology-user") + 1],
            "10.7.0.100",
        )

    def test_topology_standing_consumer_chains_fresh_same_campaign_successors(self):
        attempts = [
            {
                "status": "ACTION_COMPLETED",
                "ok": True,
                "action_attempted": True,
                "action_completed": True,
                "runtime_mutation_performed": True,
                "reservation_mutation_performed": True,
                "users_moved": 1,
                "trial_identity": "10.7.0.76",
                "source": "1",
                "target": "vless",
                "manifest_hash": "a" * 64,
                "started_at": "2026-07-31T00:00:00+00:00",
            },
            {
                "status": "ACTION_COMPLETED",
                "ok": True,
                "action_attempted": True,
                "action_completed": True,
                "runtime_mutation_performed": True,
                "reservation_mutation_performed": True,
                "users_moved": 1,
                "trial_identity": "10.7.0.77",
                "source": "1",
                "target": "vless",
                "manifest_hash": "b" * 64,
            },
            {
                "status": "NOT_REQUIRED_OR_NOT_ADMITTED",
                "ok": True,
                "action_attempted": False,
                "action_completed": False,
                "runtime_mutation_performed": False,
                "users_moved": 0,
                "diagnostic_status": (
                    "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED"
                ),
            },
        ]
        with mock.patch.object(
            self.refresh,
            "_run_controlled_topology_standing_policy_action_once",
            side_effect=attempts,
        ) as consume:
            result = (
                self.refresh.run_controlled_topology_standing_policy_action(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/state"),
                    event_dir=Path("/events"),
                    policy_file=Path("/policy"),
                    audit_store=Path("/audit"),
                    max_successive_rebindings=48,
                )
            )

        self.assertEqual(consume.call_count, 3)
        self.assertEqual(result["status"], "ACTION_COMPLETED")
        self.assertEqual(result["users_moved"], 2)
        self.assertEqual(
            [
                row["trial_identity"]
                for row in result["completed_rebindings"]
            ],
            ["10.7.0.76", "10.7.0.77"],
        )
        self.assertFalse(result["authority_expanded"])

    def test_topology_standing_consumer_does_not_execute_without_admission(self):
        diagnostic = {
            "status": "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
            "production_preflight": {"manifest": {}},
            "standing_policy_admission": {
                "status": "ENGINEERING_AUTHORITY_REQUIRED",
                "ok": False,
                "blockers": ["standing_policy_missing"],
            },
        }
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            return_value=mock.Mock(
                returncode=0,
                stdout=json.dumps(diagnostic),
            ),
        ) as run:
            result = (
                self.refresh.run_controlled_topology_standing_policy_action(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/state"),
                    event_dir=Path("/events"),
                    policy_file=Path("/policy"),
                    audit_store=Path("/audit"),
                )
            )
        self.assertEqual(result["status"], "NOT_REQUIRED_OR_NOT_ADMITTED")
        self.assertFalse(result["action_attempted"])
        self.assertEqual(run.call_count, 1)

    def test_topology_standing_consumer_preserves_exact_stop_reason(self):
        diagnostic = {
            "status": "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
            "production_preflight": {
                "manifest": {
                    "manifest_hash": "a" * 64,
                    "trial_identity": "10.7.0.100",
                    "trial_identity_count": 1,
                    "existing_source": "1",
                    "selected_source_or_draft": "vless",
                    "expected_ordinary_assignment_delta": "NONE",
                    "expected_ordinary_route_delta": "NONE",
                },
            },
            "standing_policy_admission": {
                "status": (
                    "AUTO_ADMITTED_BY_STANDING_DELEGATED_"
                    "CONTROLLED_TOPOLOGY_POLICY"
                ),
                "ok": True,
                "contract_id": "sdpc_exact",
                "contract_hash": "b" * 64,
            },
        }
        stopped = {
            "final_verdict": "STOP_SAFE",
            "stop_reason": "packet_materialization_failed",
            "reservation_mutation_performed": True,
            "reservation_released_after_stop": True,
            "users_moved": 0,
            "runtime_mutation_performed": False,
        }
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=[
                mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
                mock.Mock(returncode=2, stdout=json.dumps(stopped)),
            ],
        ):
            result = (
                self.refresh.run_controlled_topology_standing_policy_action(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/state"),
                    event_dir=Path("/events"),
                    policy_file=Path("/policy"),
                    audit_store=Path("/audit"),
                )
            )
        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertEqual(
            result["stop_reason"],
            "packet_materialization_failed",
        )
        self.assertTrue(result["reservation_mutation_performed"])
        self.assertTrue(result["reservation_released_after_stop"])

    def test_fresh_advisory_obligation_defers_omp_receipt_until_after_executor(self):
        """Fresh execution must not wait for the Engineering-plane receipt."""
        source = REFRESH_TOOL.read_text(encoding="utf-8")
        defer_marker = source.index(
            "defer_omp_receipt_until_after_fresh_execution = bool("
        )
        executor_call = source.index(
            'payload["bounded_delegated_service_failure_action"] = run_bounded_delegated_service_failure_action('
        )
        deferred_receipt = source.index(
            '"receipt_deferred_until_after_fresh_execution"'
        )
        self.assertLess(defer_marker, executor_call)
        self.assertLess(executor_call, deferred_receipt)
        self.assertIn(
            "fresh_service_failure_obligation",
            source[defer_marker:executor_call],
        )

    def test_direct_l3_handoff_does_not_wait_for_omp_before_executor(self):
        """A validated fallback projection is a Runtime handoff, not an OMP wait."""
        source = REFRESH_TOOL.read_text(encoding="utf-8")
        direct_read = source.index("service_failure_direct_execution_handoff(")
        advisory_gate = source.index('if direct_service_failure_obligation:')
        direct_status = source.index('"NOT_REQUIRED_DIRECT_L3_HANDOFF_READY"')
        executor_call = source.index(
            'payload["bounded_delegated_service_failure_action"] = run_bounded_delegated_service_failure_action('
        )
        pre_executor = source[direct_read:executor_call]
        self.assertLess(direct_read, advisory_gate)
        self.assertLess(direct_read, direct_status)
        self.assertLess(direct_status, executor_call)
        self.assertNotIn("run_service_failure_automation_advisory(", pre_executor.split(
            'if direct_service_failure_obligation:', 1
        )[1].split('elif args.skip_service_failure_automation_advisory:', 1)[0])
        self.assertIn("elif direct_service_failure_obligation:", pre_executor)
        direct_branch = pre_executor.split("elif direct_service_failure_obligation:", 1)[1].split(
            "elif (payload.get(\"passive_event_consumer\")", 1
        )[0]
        self.assertNotIn("run_service_failure_omp_consumer(", direct_branch)

    def test_ready_direct_l3_handoff_defers_passive_reconciliation_until_after_executor(self):
        """An exact existing L3 handoff keeps passive history outside the hot path."""
        obligation = {
            "stop_safe_classification": "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED",
            "bounded_recommendation_users": 1,
        }
        mixed_scope_with_unrelated_certification_tail = {
            "active_sources": [{
                "scope_classification": "MIXED_ORDINARY_AND_CERTIFICATION",
            }],
            "requires_scope_reconciliation": True,
        }
        self.assertTrue(self.refresh.ordinary_direct_handoff_ready_for_passive_deferral(
            event_only=True,
            source_scope=mixed_scope_with_unrelated_certification_tail,
            obligation=obligation,
            skip_passive_consumer=False,
        ))
        self.assertFalse(self.refresh.ordinary_direct_handoff_ready_for_passive_deferral(
            event_only=True,
            source_scope={"active_sources": [{"scope_classification": "CERTIFICATION_ONLY"}]},
            obligation=obligation,
            skip_passive_consumer=False,
        ))
        source = REFRESH_TOOL.read_text(encoding="utf-8")
        readiness = source.index("ordinary_direct_handoff_ready_for_passive_deferral(")
        deferred = source.index('"DEFERRED_UNTIL_AFTER_DIRECT_EXECUTION"', readiness)
        executor_call = source.index(
            'payload["bounded_delegated_service_failure_action"] = run_bounded_delegated_service_failure_action('
        )
        post_executor_consumer = source.index(
            'if defer_passive_consumer_until_after_direct_execution:', executor_call
        )
        post_action_projection = source.index(
            'payload["service_failure_post_action_passive_consumer"] = (', executor_call
        )
        self.assertLess(readiness, deferred)
        self.assertLess(deferred, executor_call)
        self.assertLess(executor_call, post_executor_consumer)
        self.assertLess(post_executor_consumer, post_action_projection)

    def test_no_omp_fallback_exists_before_runtime_executor(self):
        """Runtime may use fresh or L3 evidence, never an OMP receipt fallback."""
        source = REFRESH_TOOL.read_text(encoding="utf-8")
        direct_read = source.index("service_failure_direct_execution_handoff(")
        executor_call = source.index(
            'payload["bounded_delegated_service_failure_action"] = run_bounded_delegated_service_failure_action('
        )
        pre_executor = source[direct_read:executor_call]
        self.assertIn("DEFERRED_OUTSIDE_RUNTIME_HOT_PATH", pre_executor)
        self.assertIn("STOP_SAFE_DIRECT_L3_HANDOFF_REQUIRED", pre_executor)
        self.assertNotIn("service_failure_automation_consumed_execution_handoff(", pre_executor)
        self.assertNotIn("run_service_failure_omp_consumer(", pre_executor)

    def test_runtime_hot_path_units_exclude_engineering_tail(self):
        """Runtime units must not synchronously invoke OMP/reporting tails."""
        source = REFRESH_TOOL.read_text(encoding="utf-8")
        flag = source.index('"--runtime-hot-path-only"')
        cert_exit = source.index(
            "CERTIFICATION_SCOPE_DEFERRED_TO_EXISTING_CONTROLLED_OWNER",
            flag,
        )
        action_exit = source.index(
            "RUNTIME_HOT_PATH_ACTION_ATTEMPT_COMPLETE",
            cert_exit,
        )
        post_action_omp = source.index(
            'payload["service_failure_post_action_omp_consumer"]',
            action_exit,
        )
        self.assertLess(flag, cert_exit)
        self.assertLess(cert_exit, action_exit)
        self.assertLess(action_exit, post_action_omp)
        planner_unit = (ROOT / "systemd/drafts/v7-autoswitch-planner.service").read_text(
            encoding="utf-8"
        )
        refresh_unit = (ROOT / "systemd/v7-service-matrix-refresh.service").read_text(
            encoding="utf-8"
        )
        self.assertIn("--runtime-hot-path-only", planner_unit)
        self.assertIn("--runtime-hot-path-only", refresh_unit)

    def test_source_bounded_planning_filters_before_decision_construction(self):
        """A source-bounded request must not score unrelated active users."""
        source = AUTOSWITCH_TOOL.read_text(encoding="utf-8")
        plan_start = source.index("    def plan(self) -> dict[str, Any]:")
        decision_build = source.index("decisions = [self._decision_for_user(user) for user in active]", plan_start)
        source_filter = source.index("if source_egress:", plan_start)
        bounded_filter = source.index(
            "if source_egress and requested_max_selected_moves > 0:",
            source_filter,
        )
        self.assertLess(source_filter, decision_build)
        self.assertLess(bounded_filter, decision_build)


if __name__ == "__main__":
    unittest.main()
