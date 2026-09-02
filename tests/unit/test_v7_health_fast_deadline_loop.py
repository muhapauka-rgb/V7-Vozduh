"""Controlled checks for the existing v7-health deadline loop."""

from __future__ import annotations

import re
import json
from datetime import datetime, timezone
import subprocess
import tempfile
import textwrap
import time
import unittest
import importlib.machinery
import importlib.util
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
LOOP = ROOT / "tools/runtime-support/v7-health-loop"


def load_health_loop_module():
    loader = importlib.machinery.SourceFileLoader(
        "v7_test_health_fast_deadline_loop", str(LOOP)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    __import__("sys").modules[loader.name] = module
    spec.loader.exec_module(module)
    return module


HEALTH_LOOP_MODULE = load_health_loop_module()


def phase_rows(output: str) -> list[dict[str, int]]:
    rows = []
    for line in output.splitlines():
        if not line.startswith("V7_HEALTH_FAST_PHASE "):
            continue
        values = dict(item.split("=", 1) for item in line.split()[1:])
        rows.append({key: int(value) for key, value in values.items()})
    return rows


class V7HealthFastDeadlineLoopTest(unittest.TestCase):
    def write_command(self, root: Path, name: str, body: str) -> Path:
        command = root / name
        command.write_text("#!/bin/sh\n" + textwrap.dedent(body), encoding="utf-8")
        command.chmod(0o755)
        return command

    def run_loop(self, fast: Path, legacy: Path, *, phases: int = 3, interval_ms: int = 500) -> tuple[str, float]:
        started = time.monotonic()
        completed = subprocess.run(
            [
                str(LOOP), "--fast-interval-ms", str(interval_ms), "--legacy-guard-ms", "50",
                "--max-phases", str(phases), "--controlled-fast-command", str(fast),
                "--controlled-legacy-command", str(legacy),
            ],
            text=True,
            capture_output=True,
            check=True,
            timeout=20,
        )
        return completed.stdout, time.monotonic() - started

    def test_slow_legacy_tail_does_not_add_to_fast_start_to_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fast = self.write_command(root, "fast", "sleep 0.01\n")
            legacy = self.write_command(root, "legacy", "sleep 3\n")
            output, elapsed = self.run_loop(fast, legacy)

        rows = phase_rows(output)
        self.assertEqual([row["phase"] for row in rows], [1, 2, 3])
        # A 3-second legacy command is synchronously stopped at the remaining
        # phase budget. It cannot turn a 0.5-second schedule into 3+ seconds.
        self.assertLess(elapsed, 4.5, output)
        self.assertLess(rows[1]["start_to_start_ms"], 800, output)
        self.assertLess(rows[2]["start_to_start_ms"], 800, output)
        self.assertIn("V7_HEALTH_LEGACY_DEFERRED", output)
        self.assertLess(rows[1]["phase_start_jitter_ms"], 300, output)
        self.assertLess(rows[2]["phase_start_jitter_ms"], 300, output)

    def test_overrun_is_serial_and_has_no_catchup_backlog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trace = root / "trace"
            fast = self.write_command(
                root,
                "fast",
                f"echo start >> {trace}\nsleep 0.65\necho end >> {trace}\n",
            )
            legacy = self.write_command(root, "legacy", "exit 0\n")
            output, _ = self.run_loop(fast, legacy, phases=3, interval_ms=400)

            trace_rows = trace.read_text(encoding="utf-8").splitlines()
        rows = phase_rows(output)
        self.assertEqual(trace_rows, ["start", "end", "start", "end", "start", "end"])
        self.assertTrue(all(row["deadline_overrun_ms"] > 0 for row in rows), output)
        self.assertTrue(all(row["deadline_miss"] == 1 for row in rows), output)
        # Consecutive starts happen after the one previous phase finishes, not
        # together and not after a completion-plus-new-interval drift. Startup
        # cost differs materially across supported hosts, so assert the actual
        # causal gap rather than an artificial pass-duration range.
        for previous, current in zip(rows, rows[1:]):
            self.assertGreaterEqual(current["actual_start_ns"], previous["finish_ns"], output)
            self.assertLess((current["actual_start_ns"] - previous["finish_ns"]) // 1_000_000, 80, output)
        self.assertNotIn("V7_HEALTH_LEGACY_COMPLETED", output)

    def test_service_uses_one_existing_foreground_owner_and_no_sleep_30_loop(self):
        service = (ROOT / "systemd/v7-health.service").read_text(encoding="utf-8")
        loop = LOOP.read_text(encoding="utf-8")
        sync = (ROOT / "tools/v7_sync_lib.py").read_text(encoding="utf-8")
        self.assertIn(
            "ExecStart=/usr/local/bin/v7-health-loop --role-based-fast", service,
        )
        self.assertIn(
            "ExecStartPre=/usr/local/bin/v7-service-matrix-refresh-all "
            "--initialize-standing-lineage-only",
            service,
        )
        self.assertNotIn("sleep 30", service)
        self.assertIn("time.monotonic_ns", loop)
        self.assertIn("start_new_session=True", loop)
        self.assertIn("os.killpg", loop)
        self.assertNotIn("&", loop)
        self.assertIn('"name": "v7-health-loop"', sync)
        self.assertIn('"telegram": 250', loop)
        self.assertIn('"hot_target": 500', loop)
        self.assertIn('"planner_projection": 19', loop)
        self.assertIn('"hot_target": 5', loop)
        self.assertIn('"hot_target_other": 19', loop)
        self.assertIn('"other_required": 0', loop)
        self.assertIn('"--lightweight-batch-producer",', loop)
        self.assertIn('"--fast-producer-concurrency", "12"', loop)
        self.assertEqual(loop.count('"--lock-timeout-sec", "1"'), 2)
        self.assertIn('"hard": -20', loop)
        self.assertIn('"telegram": 10', loop)
        self.assertIn("Nice=0", service)
        self.assertIn('["/usr/bin/nice", "-n", str(nice)', loop)
        self.assertIn("SLOW_ROLE_ALREADY_RUNNING", loop)
        self.assertIn("serialize_slow_roles=not any(controlled.values())", loop)
        self.assertIn('and role.name != "hard"', loop)
        self.assertIn('"--profile-service-failure-samples", "1"', loop)
        other_required_command = loop.split('"other_required", 3_500,', 1)[1].split(
            '"planner_projection", 30_000,', 1
        )[0]
        self.assertIn('"--lightweight-batch-producer",', other_required_command)
        self.assertNotIn(
            '"--consumer-wake-command", '
            '"/usr/local/bin/v7-service-matrix-refresh-all"',
            other_required_command,
        )
        self.assertIn(
            "persistent Matrix parent could consume the result",
            other_required_command,
        )
        self.assertIn('"other_required": 750', loop)

    def test_production_required_detector_uses_measured_stable_3500ms_interval(self):
        args = HEALTH_LOOP_MODULE.parse_args(["--role-based-fast"])
        self.assertEqual(args.required_interval_ms, 3_500)

    def test_prepared_path_timing_receipt_is_compact_and_non_authoritative(self):
        receipt = HEALTH_LOOP_MODULE.prepared_hot_target_timing_from_output(json.dumps({
            "prepared_path_timing": {
                "total_ms": 117.2,
                "owner_load_ms": 8.1,
                "parallel_probe_wall_ms": 92.7,
                "serialized_write_wall_ms": 16.4,
            },
            "service_matrix_lock": {"writer_lock_timeout_count": 0},
            "prepared_hot_target_scope": {
                "selected_target_count_for_service_class": 3,
            },
        }))
        self.assertEqual(receipt["total_ms"], 117.2)
        self.assertEqual(receipt["parallel_probe_wall_ms"], 92.7)
        self.assertEqual(receipt["writer_lock_timeout_count"], 0)
        self.assertEqual(receipt["selected_target_count"], 3)
        self.assertEqual(
            HEALTH_LOOP_MODULE.prepared_hot_target_timing_from_output("not-json"), {},
        )

    def test_ordinary_required_timing_receipt_is_diagnostic_only(self):
        receipt = HEALTH_LOOP_MODULE.ordinary_required_timing_from_output(
            "noise\nV7_EGRESS_DIAGNOSE_TIMING contract_build_ms=12 producer_to_receipt_ms=91 commit_output_ms=1 script_total_ms=103\n"
        )
        self.assertEqual(receipt["contract_build_ms"], 12)
        self.assertEqual(receipt["script_total_ms"], 103)
        self.assertEqual(
            HEALTH_LOOP_MODULE.ordinary_required_timing_from_output("not a receipt"), {},
        )

    def test_controlled_commands_require_a_finite_polygon_run(self):
        result = subprocess.run(
            [str(LOOP), "--controlled-fast-command", "/bin/true"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertRegex(result.stderr, re.compile("require finite --max-phases"))

    def test_role_loop_keeps_one_second_hard_lane_independent_of_slow_service_lane(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hard = self.write_command(root, "hard", "sleep 0.01\n")
            telegram = self.write_command(root, "telegram", "sleep 0.02\n")
            hot_target = self.write_command(root, "hot_target", "sleep 0.02\n")
            hot_target_other = self.write_command(root, "hot_target_other", "sleep 0.02\n")
            required = self.write_command(root, "required", "sleep 2.2\n")
            planner_projection = self.write_command(root, "planner_projection", "sleep 0.02\n")
            deep = self.write_command(root, "deep", "sleep 2.8\n")
            completed = subprocess.run(
                [
                    str(LOOP), "--role-based-fast", "--max-phases", "7",
                    "--hard-interval-ms", "500",
                    "--telegram-interval-ms", "500",
                    "--required-interval-ms", "1000",
                    "--controlled-hard-command", str(hard),
                    "--controlled-telegram-command", str(telegram),
                    "--controlled-hot-target-command", str(hot_target),
                    "--controlled-hot-target-other-command", str(hot_target_other),
                    "--controlled-required-command", str(required),
                    "--controlled-planner-projection-command", str(planner_projection),
                    "--controlled-deep-command", str(deep),
                    "--deep-interval-ms", "1000",
                ],
                text=True,
                capture_output=True,
                check=True,
                timeout=10,
            )
        lines = completed.stdout.splitlines()
        hard_rows = []
        for line in lines:
            if not line.startswith("V7_HEALTH_ROLE_START role=hard "):
                continue
            values = dict(item.split("=", 1) for item in line.split()[1:])
            hard_rows.append({key: int(value) for key, value in values.items() if key != "role"})
        # The host may occasionally delay the hard child itself, so a strict
        # wall-clock spacing assertion is not a scheduler-isolation proof.
        # Prove the causal invariant instead: while the first deliberately
        # slow service child is still running, HARD continues to start in its
        # own role and therefore is not synchronously blocked by that child.
        required_start = next(
            index for index, line in enumerate(lines)
            if line.startswith("V7_HEALTH_ROLE_START role=other_required start=1 ")
        )
        required_complete = next(
            index for index, line in enumerate(lines)
            if line.startswith("V7_HEALTH_ROLE_COMPLETE role=other_required completion=1 ")
        )
        hard_during_required = [
            line for line in lines[required_start + 1:required_complete]
            if line.startswith("V7_HEALTH_ROLE_START role=hard ")
        ]
        self.assertGreaterEqual(len(hard_rows), 5, completed.stdout)
        self.assertGreaterEqual(len(hard_during_required), 2, completed.stdout)
        self.assertIn("V7_HEALTH_ROLE_DEADLINE_MISS role=other_required", completed.stdout)
        self.assertIn("V7_HEALTH_ROLE_COMPLETE role=other_required", completed.stdout)
        self.assertIn(
            "V7_HEALTH_ROLE_DEFERRED role=deep reason=ORDINARY_REQUIRED_SERVICE_DETECTION_PRIORITY",
            completed.stdout,
        )

    def test_confirmed_hard_recovery_preempts_all_observation_children(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            matrix.write_text(json.dumps({
                "items": {
                    "source-a": {
                        "services": {
                            "__channel_liveness__": {
                                "ok": False,
                                "evidence_class": "DEFINITIVE_LOCAL_HARD_FAILURE",
                                "failure_state": "OBSERVED_NEW",
                                "source_incident_id": "sfinc_test",
                                "failure_event_id": "sfe_test",
                            }
                        }
                    }
                }
            }), encoding="utf-8")
            hard = self.write_command(root, "hard", "sleep 1.1\n")
            critical = self.write_command(root, "critical", "sleep 0.05\n")
            background = self.write_command(root, "background", "sleep 5\n")
            completed = subprocess.run(
                [
                    str(LOOP), "--role-based-fast", "--max-phases", "1",
                    "--controlled-matrix-state-file", str(matrix),
                    "--hard-interval-ms", "1000",
                    "--controlled-hard-command", str(hard),
                    "--controlled-telegram-command", str(background),
                    "--controlled-hot-target-command", str(critical),
                    "--controlled-hot-target-other-command", str(background),
                    "--controlled-required-command", str(background),
                    "--controlled-planner-projection-command", str(background),
                    "--controlled-deep-command", str(background),
                ],
                text=True,
                capture_output=True,
                check=True,
                timeout=5,
            )
        self.assertIn(
            "V7_HEALTH_ROLE_PREEMPTED role=telegram", completed.stdout,
        )
        self.assertIn(
            "V7_HEALTH_ROLE_PREEMPTED role=hot_target ", completed.stdout,
        )
        self.assertIn(
            "V7_HEALTH_ROLE_PREEMPTED role=hot_target_other",
            completed.stdout,
        )
        self.assertIn("reason=HARD_RECOVERY_PRIORITY", completed.stdout)
        self.assertIn(
            "V7_HEALTH_ROLE_COMPLETE role=hard completion=1",
            completed.stdout,
        )

    def test_completed_cutover_releases_background_roles_while_source_stays_down(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            matrix.write_text(json.dumps({
                "items": {
                    "source-a": {
                        "services": {
                            "__channel_liveness__": {
                                "ok": False,
                                "evidence_class": "DEFINITIVE_LOCAL_HARD_FAILURE",
                                "failure_state": "OBSERVED_CONFIRMED",
                                "source_incident_id": "sfinc_test",
                                "failure_event_id": "sfe_test",
                            }
                        }
                    }
                }
            }), encoding="utf-8")
            # The source is still definitively down, but the only enabled
            # client is already assigned to its recovered target.
            users.write_text(
                "ip=10.7.0.92 current=target-a enabled=1\n",
                encoding="utf-8",
            )
            hard = self.write_command(root, "hard", "sleep 0.2\n")
            background = self.write_command(root, "background", "sleep 0.05\n")
            completed = subprocess.run(
                [
                    str(LOOP), "--role-based-fast", "--max-phases", "1",
                    "--controlled-matrix-state-file", str(matrix),
                    "--controlled-users-registry-file", str(users),
                    "--controlled-hard-command", str(hard),
                    "--controlled-telegram-command", str(background),
                    "--controlled-hot-target-command", str(background),
                    "--controlled-hot-target-other-command", str(background),
                    "--controlled-required-command", str(background),
                    "--controlled-planner-projection-command", str(background),
                    "--controlled-deep-command", str(background),
                ],
                text=True,
                capture_output=True,
                check=True,
                timeout=5,
            )
        self.assertNotIn("reason=HARD_RECOVERY_PRIORITY", completed.stdout)
        self.assertIn(
            "V7_HEALTH_ROLE_DEFERRED role=planner_projection reason=ORDINARY_REQUIRED_SERVICE_DETECTION_PRIORITY",
            completed.stdout,
        )

    def test_hard_recovery_preempts_redundant_target_probe_when_path_is_fresh(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            matrix.write_text(json.dumps({
                "items": {
                    "source-a": {
                        "services": {
                            "__channel_liveness__": {
                                "ok": False,
                                "evidence_class": "DEFINITIVE_LOCAL_HARD_FAILURE",
                                "failure_state": "OBSERVED_NEW",
                                "source_incident_id": "sfinc_test",
                                "failure_event_id": "sfe_test",
                            }
                        }
                    },
                    "target-a": {
                        "status": "OK",
                        "path_evidence_updated": datetime.now(
                            timezone.utc
                        ).isoformat(),
                        "path_evidence": {
                            "component_status": {
                                "interface_addresses": "PASS",
                                "policy_rules": "PASS",
                                "routing_tables": "PASS",
                            }
                        },
                    },
                }
            }), encoding="utf-8")
            hard = self.write_command(root, "hard", "sleep 1.1\n")
            target = self.write_command(root, "target", "sleep 5\n")
            quick = self.write_command(root, "quick", "sleep 0.02\n")
            completed = subprocess.run(
                [
                    str(LOOP), "--role-based-fast", "--max-phases", "1",
                    "--controlled-matrix-state-file", str(matrix),
                    "--hard-interval-ms", "1000",
                    "--controlled-hard-command", str(hard),
                    "--controlled-telegram-command", str(quick),
                    "--controlled-hot-target-command", str(target),
                    "--controlled-hot-target-other-command", str(quick),
                    "--controlled-required-command", str(quick),
                    "--controlled-planner-projection-command", str(quick),
                    "--controlled-deep-command", str(quick),
                ],
                text=True,
                capture_output=True,
                check=True,
                timeout=5,
            )
        self.assertIn(
            "V7_HEALTH_ROLE_PREEMPTED role=hot_target ", completed.stdout,
        )
        self.assertIn("reason=HARD_RECOVERY_PRIORITY", completed.stdout)

    def test_hard_priority_stays_latched_until_exact_child_completes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            matrix.write_text(json.dumps({
                "items": {"source-a": {"services": {
                    "__channel_liveness__": {
                        "ok": False,
                        "evidence_class": "DEFINITIVE_LOCAL_HARD_FAILURE",
                        "failure_state": "OBSERVED_NEW",
                        "source_incident_id": "sfinc_test",
                        "failure_event_id": "sfe_test",
                    }
                }}}
            }), encoding="utf-8")
            hard = self.write_command(
                root, "hard",
                f"sleep 0.2\nprintf '{{\"items\":{{}}}}' > '{matrix}'\n"
                "sleep 0.9\n",
            )
            quick = self.write_command(root, "quick", "sleep 0.02\n")
            completed = subprocess.run(
                [
                    str(LOOP), "--role-based-fast", "--max-phases", "2",
                    "--controlled-matrix-state-file", str(matrix),
                    "--hard-interval-ms", "1000",
                    "--hot-target-interval-ms", "100",
                    "--controlled-hard-command", str(hard),
                    "--controlled-telegram-command", str(quick),
                    "--controlled-hot-target-command", str(quick),
                    "--controlled-hot-target-other-command", str(quick),
                    "--controlled-required-command", str(quick),
                    "--controlled-planner-projection-command", str(quick),
                    "--controlled-deep-command", str(quick),
                ],
                text=True,
                capture_output=True,
                check=True,
                timeout=6,
            )
        first_hard_complete = completed.stdout.index(
            "V7_HEALTH_ROLE_COMPLETE role=hard completion=1"
        )
        second_target_start = completed.stdout.index(
            "V7_HEALTH_ROLE_START role=hot_target start=2"
        )
        self.assertGreater(second_target_start, first_hard_complete)
        self.assertIn(
            "V7_HEALTH_ROLE_PREEMPTED role=hot_target ",
            completed.stdout,
        )
        self.assertIn(
            "V7_HEALTH_ROLE_DEFERRED role=hot_target "
            "reason=HARD_RECOVERY_PRIORITY",
            completed.stdout,
        )

    def test_slow_healthy_hard_observation_does_not_preempt_projection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            matrix.write_text(json.dumps({"items": {}}), encoding="utf-8")
            hard = self.write_command(root, "hard", "sleep 1.1\n")
            background = self.write_command(root, "background", "sleep 1.4\n")
            quick = self.write_command(root, "quick", "sleep 0.02\n")
            completed = subprocess.run(
                [
                    str(LOOP), "--role-based-fast", "--max-phases", "1",
                    "--controlled-matrix-state-file", str(matrix),
                    "--hard-interval-ms", "1000",
                    "--controlled-hard-command", str(hard),
                    "--controlled-telegram-command", str(quick),
                    "--controlled-hot-target-command", str(quick),
                    "--controlled-hot-target-other-command", str(quick),
                    "--controlled-required-command", str(quick),
                    "--controlled-planner-projection-command", str(background),
                    "--controlled-deep-command", str(quick),
                ],
                text=True,
                capture_output=True,
                check=True,
                timeout=5,
            )
        self.assertNotIn("reason=HARD_RECOVERY_PRIORITY", completed.stdout)
        self.assertIn(
            "reason=ORDINARY_REQUIRED_SERVICE_DETECTION_PRIORITY",
            completed.stdout,
        )
        self.assertIn(
            "V7_HEALTH_ROLE_DEFERRED role=planner_projection reason=ORDINARY_REQUIRED_SERVICE_DETECTION_PRIORITY",
            completed.stdout,
        )

    def test_persistent_matrix_consumer_uses_current_call_contract_and_restores_parent(self):
        observed = {}

        class MatrixConsumer:
            def main(self):
                observed["argv"] = list(__import__("sys").argv)
                observed["t0"] = __import__("os").environ.get(
                    "V7_HARD_T0_MONOTONIC_NS"
                )
                observed["owner"] = __import__("os").environ.get(
                    "V7_HARD_PERSISTENT_MATRIX_OWNER"
                )
                return 0

        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
        loop.persistent_matrix_ready = True
        loop.persistent_matrix_module = MatrixConsumer()
        previous_argv = list(__import__("sys").argv)
        self.assertEqual(loop._run_persistent_matrix_consumer(123_456), 0)
        self.assertEqual(
            observed["argv"],
            [
                "v7-service-matrix-refresh-all",
                "--consume-existing-service-failure-events-only",
                "--runtime-hot-path-only",
            ],
        )
        self.assertEqual(observed["t0"], "123456")
        self.assertEqual(observed["owner"], "1")
        self.assertEqual(__import__("sys").argv, previous_argv)
        self.assertIsNone(
            __import__("os").environ.get("V7_HARD_PERSISTENT_MATRIX_OWNER")
        )

    def test_persistent_fault_uses_exact_existing_external_matrix_consumer(self):
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
        with mock.patch.object(HEALTH_LOOP_MODULE.subprocess, "run") as run:
            loop._fallback_matrix_consumer(789)
        command = run.call_args.args[0]
        environment = run.call_args.kwargs["env"]
        self.assertEqual(
            command,
            [
                "/usr/local/bin/v7-service-matrix-refresh-all",
                "--consume-existing-service-failure-events-only",
                "--runtime-hot-path-only",
            ],
        )
        self.assertEqual(environment["V7_HARD_T0_MONOTONIC_NS"], "789")
        self.assertNotIn("V7_HARD_PERSISTENT_MATRIX_OWNER", environment)

    def test_persistent_consumer_does_not_replay_one_canonical_t0(self):
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
        loop.persistent_matrix_ready = True
        with mock.patch.object(
            loop, "_run_persistent_matrix_consumer", return_value=0
        ) as consumer:
            self.assertTrue(loop._consume_new_persistent_matrix_t0(123_456))
            self.assertFalse(loop._consume_new_persistent_matrix_t0(123_456))
            self.assertFalse(loop._consume_new_persistent_matrix_t0(123_455))
            self.assertTrue(loop._consume_new_persistent_matrix_t0(123_457))
        self.assertEqual(consumer.call_args_list, [
            mock.call(123_456), mock.call(123_457),
        ])
        self.assertEqual(loop.persistent_matrix_last_consumed_t0_ns, 123_457)

    def test_persistent_consumer_emits_outcome_receipt_without_operational_effect(self):
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
        loop.persistent_matrix_ready = True
        loop.persistent_matrix_last_result = {
            "status": "PASS",
            "next_output": "SERVICE_FAILURE_EVENT_CONSUMED",
            "current_failed_source_scope": {
                "active": True,
                "active_sources": [{"affected_scope_count": 2}],
            },
            "bounded_delegated_service_failure_action": {
                "status": "PASS",
                "action_attempted": True,
                "action_completed": True,
                "runtime_mutation_performed": True,
                "users_moved": 2,
                "consumer_result": {
                    "stop_reason": "",
                    "execution_timing": {
                        "schema_version": "v7.governed-execution-timing.v1",
                        "status": "MONOTONIC_BREAKDOWN_CONSUMED",
                        "total_ms": 3210.0,
                        "dominant_stage": "apply_and_verification",
                        "clock_source": "time.monotonic_ns",
                        "wall_clock_used_for_elapsed": False,
                        "spans": [
                            {"stage": "planner", "duration_ms": 123.0},
                            {"stage": "apply_and_verification", "duration_ms": 3087.0},
                        ],
                    },
                },
            },
        }
        with mock.patch.object(loop, "_run_persistent_matrix_consumer", return_value=0), \
             mock.patch("builtins.print") as printed:
            self.assertTrue(loop._consume_new_persistent_matrix_t0(123_456))
        receipt_lines = [
            str(call.args[0]) for call in printed.call_args_list
            if str(call.args[0]).startswith("V7_HEALTH_RECOVERY_CONSUMER_RECEIPT ")
        ]
        self.assertEqual(len(receipt_lines), 1)
        receipt = json.loads(receipt_lines[0].split(" ", 1)[1])
        self.assertEqual(receipt["affected_scope_count"], 2)
        self.assertTrue(receipt["action_completed"])
        self.assertEqual(receipt["users_moved"], 2)
        self.assertLessEqual(
            receipt["t0_monotonic_ns"],
            receipt["consumer_started_monotonic_ns"],
        )
        self.assertLessEqual(
            receipt["consumer_started_monotonic_ns"],
            receipt["consumer_completed_monotonic_ns"],
        )
        self.assertGreaterEqual(receipt["t0_to_consumer_complete_ms"], 0)
        self.assertGreaterEqual(receipt["consumer_execution_ms"], 0)
        self.assertEqual(
            receipt["governed_execution_timing"]["dominant_stage"],
            "apply_and_verification",
        )
        self.assertEqual(
            receipt["governed_execution_timing"]["spans"],
            [
                {"stage": "planner", "duration_ms": 123.0},
                {"stage": "apply_and_verification", "duration_ms": 3087.0},
            ],
        )

    def test_known_incomplete_downstream_validation_is_deduped_until_matrix_binding_changes(self):
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
        loop.persistent_matrix_ready = True
        incomplete = {
            "bounded_delegated_service_failure_action": {
                "action_attempted": True,
                "action_completed": False,
                "runtime_mutation_performed": False,
                "status": "STOP_SAFE",
                "consumer_result": {
                    "stop_reason": "l3_production_validation_downstream_proof_failed",
                },
            },
        }

        def incomplete_consumer(*_args):
            loop.persistent_matrix_last_result = incomplete
            return 0

        with mock.patch.object(
            loop, "_run_persistent_matrix_consumer", side_effect=incomplete_consumer,
        ) as consumer:
            self.assertTrue(loop._consume_new_persistent_matrix_t0(123_456))
            self.assertFalse(loop._consume_new_persistent_matrix_t0(123_456))
        self.assertEqual(consumer.call_count, 1)
        self.assertEqual(
            loop.persistent_matrix_last_consumed_t0_ns_by_role,
            {"hard": 123_456},
        )

    def test_stop_safe_reentry_uses_existing_prepared_invalidator_generations(self):
        """A changed lawful blocker re-enters without a new source outage."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            preferences = root / "service-preferences.json"
            summary = root / "service-matrix-refresh-summary.json"
            matrix.write_text(json.dumps({"items": {"vless": {"services": {
                "google": {
                    "ok": False, "status": "FAIL",
                    "failure_state": "OBSERVED_CONTINUING",
                    "source_incident_id": "same-incident",
                    "failure_event_id": "rotating-observation",
                    "observation_monotonic_ns": 100,
                },
            }}}}), encoding="utf-8")
            users.write_text("ip=10.7.0.127 enabled=1 current=vless\n", encoding="utf-8")
            preferences.write_text(json.dumps({"users": {
                "10.7.0.127": {"services": ["google"]},
            }}), encoding="utf-8")

            def write_summary(**changes):
                invalidators = {
                    key: f"{key}-stable"
                    for key in HEALTH_LOOP_MODULE.PREPARED_REENTRY_INVALIDATOR_KEYS
                }
                invalidators.update(changes)
                summary.write_text(json.dumps({
                    "prepared_class_decisions": {
                        "status": "PREPARED_CLASS_DECISION_AVAILABLE",
                        "invalidators": invalidators,
                    },
                    "prepared_class_decision_freshness": {
                        "status": "PREPARED_CLASS_DECISION_FRESH",
                        "invalidation_reasons": [],
                        "fact_specific_freshness": {
                            "capacity": {"fresh": True},
                            "identity_and_role": {"fresh": True},
                            "other_required_service": {"fresh": True},
                            "path_liveness": {"fresh": True},
                            "policy": {"fresh": True},
                        },
                    },
                }), encoding="utf-8")

            write_summary()
            initial = HEALTH_LOOP_MODULE.canonical_profile_service_failure_bindings(
                matrix, users, preferences, summary,
            )[0]
            # CASE G: a new Matrix observation for the unchanged problem and
            # unchanged current blockers does not create heavy duplicate work.
            matrix.write_text(json.dumps({"items": {"vless": {"services": {
                "google": {
                    "ok": False, "status": "FAIL",
                    "failure_state": "OBSERVED_CONTINUING",
                    "source_incident_id": "same-incident",
                    "failure_event_id": "new-observation-only",
                    "observation_monotonic_ns": 200,
                },
            }}}}), encoding="utf-8")
            unchanged = HEALTH_LOOP_MODULE.canonical_profile_service_failure_bindings(
                matrix, users, preferences, summary,
            )[0]
            self.assertEqual(initial["dedupe_identity"], unchanged["dedupe_identity"])

            loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
            loop.persistent_matrix_ready = True
            with mock.patch.object(loop, "_run_persistent_matrix_consumer", return_value=0) as consumer:
                self.assertTrue(loop._consume_new_persistent_matrix_t0(
                    initial["t0_ns"], dedupe_key="other_required:vless",
                    dedupe_identity=initial["dedupe_identity"],
                ))
                self.assertFalse(loop._consume_new_persistent_matrix_t0(
                    unchanged["t0_ns"], dedupe_key="other_required:vless",
                    dedupe_identity=unchanged["dedupe_identity"],
                ))
                # A-F map directly to existing Matrix/Planner invalidators.
                # Each changed blocker generation is a new governed
                # reconciliation with the same source, assignment, scope and
                # incident; no special STOP_SAFE reason branch is added.
                reentry_cases = {
                    "target_eligibility": "target_topology_generation",
                    "capacity": "capacity_reservation_generation",
                    "policy_authority": "policy_authority_generation",
                    "exact_conflict": "active_operation_generation",
                    "lease_barrier_cleanup": (
                        "rollback_target_availability_generation"
                    ),
                    "target_freshness": "target_health_and_path_generation",
                }
                for case, key in reentry_cases.items():
                    with self.subTest(case=case):
                        write_summary(**{key: f"{key}-changed"})
                        changed = HEALTH_LOOP_MODULE.canonical_profile_service_failure_bindings(
                            matrix, users, preferences, summary,
                        )[0]
                        self.assertNotEqual(
                            unchanged["dedupe_identity"], changed["dedupe_identity"],
                        )
                        self.assertTrue(loop._consume_new_persistent_matrix_t0(
                            changed["t0_ns"], dedupe_key="other_required:vless",
                            dedupe_identity=changed["dedupe_identity"],
                        ))
                        # Restore the same baseline before exercising the next
                        # independent current-owner blocker.
                        write_summary()
            self.assertEqual(consumer.call_count, 1 + len(reentry_cases))

    def test_reentry_invalidator_transition_space_is_exact_once_and_source_isolated(self):
        """100 deterministic + 1000 seeded transitions preserve no-starvation."""
        stable = {
            key: f"{key}-0"
            for key in HEALTH_LOOP_MODULE.PREPARED_REENTRY_INVALIDATOR_KEYS
        }

        with tempfile.TemporaryDirectory() as td:
            summary = Path(td) / "service-matrix-refresh-summary.json"

            def fingerprint(invalidators: dict[str, str]) -> str:
                summary.write_text(json.dumps({
                    "prepared_class_decisions": {
                        "status": "PREPARED_CLASS_DECISION_AVAILABLE",
                        "invalidators": invalidators,
                    },
                    "prepared_class_decision_freshness": {
                        "status": "PREPARED_CLASS_DECISION_FRESH",
                        "invalidation_reasons": [],
                        "fact_specific_freshness": {},
                    },
                }), encoding="utf-8")
                return HEALTH_LOOP_MODULE.prepared_reentry_invalidator_fingerprint(
                    summary,
                )

            # Deterministic owner transitions: each changed value creates
            # exactly one new current invalidator fingerprint; unchanged
            # values stay suppressed.
            stable_fingerprint = fingerprint(stable)
            for transition in range(100):
                changed = dict(stable)
                key = HEALTH_LOOP_MODULE.PREPARED_REENTRY_INVALIDATOR_KEYS[
                    transition % len(HEALTH_LOOP_MODULE.PREPARED_REENTRY_INVALIDATOR_KEYS)
                ]
                changed[key] = f"{key}-{transition + 1}"
                current = fingerprint(changed)
                self.assertNotEqual(stable_fingerprint, current)
                self.assertEqual(current, fingerprint(changed))

            # Seeded transition coverage invokes the actual existing-owner
            # projection reader only.  It neither creates
            # Candidate/Packet/Lease/Barrier nor invokes any Runtime path.
            import random
            rng = random.Random(20260902)
            seen = {stable_fingerprint}
            for transition in range(1000):
                changed = dict(stable)
                key = rng.choice(HEALTH_LOOP_MODULE.PREPARED_REENTRY_INVALIDATOR_KEYS)
                changed[key] = f"{key}-seed-{transition}"
                current = fingerprint(changed)
                self.assertNotIn(current, seen)
                seen.add(current)

    def test_profile_t0_is_not_suppressed_by_newer_unrelated_role_t0(self):
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
        loop.persistent_matrix_ready = True
        with mock.patch.object(
            loop, "_run_persistent_matrix_consumer", return_value=0,
        ) as consumer:
            self.assertTrue(
                loop._consume_new_persistent_matrix_t0(
                    900, dedupe_key="telegram",
                )
            )
            self.assertTrue(
                loop._consume_new_persistent_matrix_t0(
                    800, dedupe_key="other_required",
                )
            )
            self.assertFalse(
                loop._consume_new_persistent_matrix_t0(
                    800, dedupe_key="other_required",
                )
            )
        self.assertEqual(consumer.call_args_list, [mock.call(900), mock.call(800)])
        self.assertEqual(
            loop.persistent_matrix_last_consumed_t0_ns_by_role,
            {"telegram": 900, "other_required": 800},
        )

    def test_profile_scope_change_reconsumes_same_source_incident_once(self):
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=tuple())
        loop.persistent_matrix_ready = True
        with mock.patch.object(
            loop, "_run_persistent_matrix_consumer", return_value=0,
        ) as consumer:
            self.assertTrue(loop._consume_new_persistent_matrix_t0(
                800, dedupe_key="other_required", dedupe_identity="scope-a",
            ))
            self.assertFalse(loop._consume_new_persistent_matrix_t0(
                800, dedupe_key="other_required", dedupe_identity="scope-a",
            ))
            self.assertTrue(loop._consume_new_persistent_matrix_t0(
                800, dedupe_key="other_required", dedupe_identity="scope-b",
            ))
        self.assertEqual(consumer.call_args_list, [mock.call(800), mock.call(800)])

    def test_persistent_handoff_requires_current_matrix_t0_and_exact_assignment(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            matrix.write_text(json.dumps({
                "items": {"source-a": {"services": {
                    "__channel_liveness__": {
                        "ok": False,
                        "evidence_class": "DEFINITIVE_LOCAL_HARD_FAILURE",
                        "failure_state": "OBSERVED_NEW",
                        "source_incident_id": "sfinc_test",
                        "failure_event_id": "sfe_test",
                        "confirmed_hard_failure_monotonic_ns": 456_789,
                    },
                }}},
            }), encoding="utf-8")
            users.write_text(
                "ip=10.7.0.124 enabled=1 current=source-a certification_user=1\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HEALTH_LOOP_MODULE.canonical_definitive_hard_failure_t0_ns(
                    matrix, users
                ),
                456_789,
            )
            users.write_text(
                "ip=10.7.0.124 enabled=1 current=target-a certification_user=1\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HEALTH_LOOP_MODULE.canonical_definitive_hard_failure_t0_ns(
                    matrix, users
                ),
                0,
            )

    def test_persistent_handoff_accepts_only_current_assigned_telegram_event(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            matrix.write_text(json.dumps({
                "items": {"source-a": {"services": {
                    "telegram": {
                        "ok": False,
                        "failure_state": "OBSERVED_NEW",
                        "source_incident_id": "sfinc_telegram",
                        "failure_event_id": "sfe_telegram",
                        "confirmed_hard_failure_monotonic_ns": 567_890,
                    },
                }}},
            }), encoding="utf-8")
            users.write_text(
                "ip=10.7.0.124 enabled=1 current=source-a certification_user=1\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HEALTH_LOOP_MODULE.canonical_service_failure_t0_ns(
                    matrix, users, "telegram"
                ),
                567_890,
            )
            users.write_text(
                "ip=10.7.0.124 enabled=1 current=target-a certification_user=1\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HEALTH_LOOP_MODULE.canonical_service_failure_t0_ns(
                    matrix, users, "telegram"
                ),
                0,
            )

    def test_profile_service_handoff_requires_current_required_service_incident(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            preferences = root / "service-preferences.json"
            matrix.write_text(json.dumps({
                "items": {"source-a": {"services": {
                    "google": {
                        "ok": False,
                        "status": "FAIL",
                        "failure_state": "OBSERVED_NEW",
                        "source_incident_id": "sfinc_google",
                        "failure_event_id": "sfe_google",
                        "observation_monotonic_ns": 678_901,
                    },
                    "instagram": {"ok": True, "status": "OK"},
                }}},
            }), encoding="utf-8")
            users.write_text(
                "ip=10.7.0.127 enabled=1 current=source-a\n"
                "ip=10.7.0.128 enabled=1 current=source-a\n",
                encoding="utf-8",
            )
            preferences.write_text(json.dumps({"users": {
                "10.7.0.127": {"services": ["google", "instagram"]},
                "10.7.0.128": {"services": ["instagram"]},
            }}), encoding="utf-8")
            self.assertEqual(
                HEALTH_LOOP_MODULE.canonical_profile_service_failure_t0_ns(
                    matrix, users, preferences,
                ),
                678_901,
            )
            binding = HEALTH_LOOP_MODULE.canonical_profile_service_failure_binding(
                matrix, users, preferences,
            )
            self.assertEqual(binding["affected_profile_count"], 1)
            first_identity = binding["dedupe_identity"]
            users.write_text(
                "ip=10.7.0.127 enabled=1 current=source-a\n"
                "ip=10.7.0.128 enabled=1 current=source-a\n",
                encoding="utf-8",
            )
            preferences.write_text(json.dumps({"users": {
                "10.7.0.127": {"services": ["google", "instagram"]},
                "10.7.0.128": {"services": ["google"]},
            }}), encoding="utf-8")
            self.assertNotEqual(
                HEALTH_LOOP_MODULE.canonical_profile_service_failure_binding(
                    matrix, users, preferences,
                )["dedupe_identity"],
                first_identity,
            )
            users.write_text(
                "ip=10.7.0.127 enabled=1 current=target-a\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HEALTH_LOOP_MODULE.canonical_profile_service_failure_t0_ns(
                    matrix, users, preferences,
                ),
                0,
            )

    def test_profile_service_handoff_uses_current_observation_but_dedupes_continuing_incident(self):
        """A later placement needs a current clock, not a rotating event id."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            preferences = root / "service-preferences.json"
            users.write_text(
                "ip=10.7.0.127 enabled=1 current=vless\n",
                encoding="utf-8",
            )
            preferences.write_text(json.dumps({"users": {
                "10.7.0.127": {"services": ["google"]},
            }}), encoding="utf-8")

            def write_matrix(*, observation: int, event: str) -> None:
                matrix.write_text(json.dumps({"items": {"vless": {"services": {
                    "google": {
                        "ok": False, "status": "FAIL",
                        "failure_state": "OBSERVED_CONTINUING",
                        "source_incident_id": "stable-vless-incident",
                        "failure_event_id": event,
                        "confirmed_hard_failure_monotonic_ns": 100,
                        "observation_monotonic_ns": observation,
                    },
                }}}}), encoding="utf-8")

            write_matrix(observation=500, event="observation-a")
            first = HEALTH_LOOP_MODULE.canonical_profile_service_failure_bindings(
                matrix, users, preferences,
            )[0]
            write_matrix(observation=900, event="observation-b")
            second = HEALTH_LOOP_MODULE.canonical_profile_service_failure_bindings(
                matrix, users, preferences,
            )[0]

        self.assertEqual(first["t0_ns"], 500)
        self.assertEqual(second["t0_ns"], 900)
        self.assertEqual(second["incident_t0_ns"], 100)
        self.assertEqual(first["dedupe_identity"], second["dedupe_identity"])

    def test_profile_service_bindings_keep_simultaneous_sources_separate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            preferences = root / "service-preferences.json"
            matrix.write_text(json.dumps({"items": {
                "older-source": {"services": {"google": {
                    "ok": False, "status": "FAIL", "failure_state": "OBSERVED_CONTINUING",
                    "source_incident_id": "older", "failure_event_id": "event-older",
                    "observation_monotonic_ns": 100,
                }}},
                "newer-unrelated-source": {"services": {"telegram": {
                    "ok": False, "status": "FAIL", "failure_state": "OBSERVED_NEW",
                    "source_incident_id": "newer", "failure_event_id": "event-newer",
                    "observation_monotonic_ns": 200,
                }}},
            }}), encoding="utf-8")
            users.write_text(
                "ip=10.7.0.125 enabled=1 current=older-source\n"
                "ip=10.7.0.126 enabled=1 current=older-source\n"
                "ip=10.7.0.127 enabled=1 current=newer-unrelated-source\n",
                encoding="utf-8",
            )
            preferences.write_text(json.dumps({"users": {
                "10.7.0.125": {"services": ["google"]},
                "10.7.0.126": {"services": ["google"]},
                "10.7.0.127": {"services": ["telegram"]},
            }}), encoding="utf-8")
            bindings = HEALTH_LOOP_MODULE.canonical_profile_service_failure_bindings(
                matrix, users, preferences,
            )
            self.assertEqual(
                [(row["source_egress"], row["affected_profile_count"]) for row in bindings],
                [("newer-unrelated-source", 1), ("older-source", 2)],
            )
            self.assertNotIn("source_egress", HEALTH_LOOP_MODULE.canonical_profile_service_failure_binding(
                matrix, users, preferences,
            ))

    def test_profile_service_bindings_reject_stale_production_matrix_failure(self):
        """A historical Matrix failure must not wake the bounded live executor."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            preferences = root / "service-preferences.json"
            matrix.write_text(json.dumps({"items": {
                "stale-source": {"services": {"google": {
                    "ok": False, "status": "FAIL", "failure_state": "OBSERVED_CONTINUING",
                    "source_incident_id": "old", "failure_event_id": "event-old",
                    "observation_monotonic_ns": 100,
                    "observed_at": "2000-01-01T00:00:00+00:00",
                }}},
                "fresh-source": {"services": {"telegram": {
                    "ok": False, "status": "FAIL", "failure_state": "OBSERVED_NEW",
                    "source_incident_id": "new", "failure_event_id": "event-new",
                    "observation_monotonic_ns": 200,
                    "observed_at": datetime.now(timezone.utc).isoformat(),
                }}},
            }}), encoding="utf-8")
            users.write_text(
                "ip=10.7.0.125 enabled=1 current=stale-source\n"
                "ip=10.7.0.126 enabled=1 current=fresh-source\n",
                encoding="utf-8",
            )
            preferences.write_text(json.dumps({"users": {
                "10.7.0.125": {"services": ["google"]},
                "10.7.0.126": {"services": ["telegram"]},
            }}), encoding="utf-8")
            bindings = HEALTH_LOOP_MODULE.canonical_profile_service_failure_bindings(
                matrix, users, preferences,
            )
            self.assertEqual(len(bindings), 1)
            self.assertEqual(bindings[0]["source_egress"], "fresh-source")
            self.assertEqual(bindings[0]["t0_ns"], 200)
            self.assertEqual(bindings[0]["affected_profile_count"], 1)

    def test_due_projection_preempts_disposable_slow_observation(self):
        """A slow probe cannot defer the bounded prepared-decision refresh."""
        probe_process = mock.Mock()
        running_probe = HEALTH_LOOP_MODULE.ManagedRole(
            name="hot_target_other",
            cadence_ns=5_000_000_000,
            command=("/bin/true",),
            next_due_ns=10_000,
            process=probe_process,
            started_ns=1_000,
        )
        projection = HEALTH_LOOP_MODULE.ManagedRole(
            name="planner_projection",
            cadence_ns=30_000_000_000,
            command=("/bin/true",),
            next_due_ns=0,
        )
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(
            roles=(running_probe, projection),
        )
        with mock.patch.object(
            HEALTH_LOOP_MODULE, "terminate_process_group"
        ) as terminate, mock.patch.object(
            HEALTH_LOOP_MODULE.subprocess, "Popen", return_value=mock.Mock()
        ) as popen, mock.patch("builtins.print") as printed:
            loop._start_due_roles(5_000)
        terminate.assert_called_once_with(probe_process)
        self.assertIsNone(running_probe.process)
        popen.assert_called_once()
        self.assertTrue(projection.process)
        self.assertIn(
            "reason=PREPARED_PROJECTION_FRESHNESS_PRIORITY",
            " ".join(str(call) for call in printed.call_args_list),
        )

    def test_other_target_probe_is_preempted_for_other_required_detector(self):
        """Advisory target warming cannot delay a client-contract detector."""
        detector = HEALTH_LOOP_MODULE.ManagedRole(
            name="other_required", cadence_ns=5_000_000_000,
            command=("/bin/true",), next_due_ns=0,
            process=mock.Mock(), started_ns=1_000,
        )
        target_process = mock.Mock()
        target_probe = HEALTH_LOOP_MODULE.ManagedRole(
            name="hot_target_other", cadence_ns=5_000_000_000,
            command=("/bin/true",), next_due_ns=0,
            process=target_process, started_ns=1_000,
        )
        deep_process = mock.Mock()
        deep_probe = HEALTH_LOOP_MODULE.ManagedRole(
            name="deep", cadence_ns=60_000_000_000,
            command=("/bin/true",), next_due_ns=0,
            process=deep_process, started_ns=1_000,
        )
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(
            roles=(detector, target_probe, deep_probe),
        )
        with mock.patch.object(
            HEALTH_LOOP_MODULE, "terminate_process_group"
        ) as terminate:
            loop._recovery_critical_takeover(5_000)

        terminate.assert_has_calls((mock.call(target_process), mock.call(deep_process)))
        self.assertEqual(terminate.call_count, 2)
        self.assertIsNone(target_probe.process)
        self.assertIsNone(deep_probe.process)

    def test_running_detector_hands_new_matrix_t0_to_existing_consumer(self):
        """A fresh Matrix T0 must not wait for unrelated detector probes."""
        detector_process = mock.Mock()
        detector_process.poll.return_value = None
        detector_process.pid = 1234
        detector = HEALTH_LOOP_MODULE.ManagedRole(
            name="other_required",
            cadence_ns=5_000_000_000,
            command=("/bin/true",),
            process=detector_process,
            started_ns=1_000,
        )
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=(detector,))
        loop.persistent_matrix_ready = True
        with mock.patch.object(
            HEALTH_LOOP_MODULE,
            "canonical_profile_service_failure_bindings",
            return_value=[{
                "source_egress": "vless",
                "t0_ns": 4_000,
                "dedupe_identity": "fresh-vless-scope",
            }],
        ), mock.patch.object(
            HEALTH_LOOP_MODULE, "terminate_process_group"
        ) as terminate, mock.patch.object(
            loop, "_consume_new_persistent_matrix_t0", return_value=True
        ) as consume:
            loop._collect_roles(5_000)

        terminate.assert_called_once_with(detector_process)
        consume.assert_called_once()
        self.assertIsNone(detector.process)

    def test_running_detector_bounds_full_matrix_reads_to_250ms(self):
        """The 25ms parent tick must not continuously parse the full registry."""
        detector_process = mock.Mock()
        detector_process.poll.return_value = None
        detector = HEALTH_LOOP_MODULE.ManagedRole(
            name="other_required",
            cadence_ns=5_000_000_000,
            command=("/bin/true",),
            process=detector_process,
            started_ns=1_000,
        )
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(roles=(detector,))
        loop.persistent_matrix_ready = True
        with mock.patch.object(
            HEALTH_LOOP_MODULE,
            "canonical_profile_service_failure_bindings",
            return_value=[],
        ) as bindings:
            loop._collect_roles(5_000)
            loop._collect_roles(5_000 + 25_000_000)
            loop._collect_roles(
                5_000 + HEALTH_LOOP_MODULE.PROFILE_BINDING_POLL_NS
            )

        self.assertEqual(bindings.call_count, 2)

    def test_service_failure_detector_preempts_projection_and_is_not_preempted(self):
        """The recovery detector must get the shared Matrix lock first."""
        projection_process = mock.Mock()
        projection = HEALTH_LOOP_MODULE.ManagedRole(
            name="planner_projection",
            cadence_ns=30_000_000_000,
            command=("/bin/true",),
            next_due_ns=10_000,
            process=projection_process,
            started_ns=1_000,
        )
        detector = HEALTH_LOOP_MODULE.ManagedRole(
            name="other_required",
            cadence_ns=5_000_000_000,
            command=("/bin/true",),
            next_due_ns=0,
        )
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(
            roles=(projection, detector),
        )
        with mock.patch.object(
            HEALTH_LOOP_MODULE, "terminate_process_group"
        ) as terminate, mock.patch.object(
            HEALTH_LOOP_MODULE.subprocess, "Popen", return_value=mock.Mock()
        ) as popen, mock.patch("builtins.print") as printed:
            loop._start_due_roles(5_000)
        terminate.assert_called_once_with(projection_process)
        self.assertIsNone(projection.process)
        self.assertIsNotNone(detector.process)
        self.assertEqual(popen.call_count, 1)
        self.assertIn(
            "reason=RECOVERY_CRITICAL_FAILURE_DETECTION_PRIORITY",
            " ".join(str(call) for call in printed.call_args_list),
        )

    def test_ordinary_required_detector_releases_its_cpu_slot(self):
        """Target and Telegram observations cannot stretch the source probe."""
        telegram_process = mock.Mock()
        target_process = mock.Mock()
        telegram = HEALTH_LOOP_MODULE.ManagedRole(
            name="telegram", cadence_ns=1_000_000_000,
            command=("/bin/true",), next_due_ns=10_000,
            process=telegram_process, started_ns=1_000,
        )
        target = HEALTH_LOOP_MODULE.ManagedRole(
            name="hot_target", cadence_ns=1_000_000_000,
            command=("/bin/true",), next_due_ns=10_000,
            process=target_process, started_ns=1_000,
        )
        detector = HEALTH_LOOP_MODULE.ManagedRole(
            name="other_required", cadence_ns=5_000_000_000,
            command=("/bin/true",), next_due_ns=0,
        )
        loop = HEALTH_LOOP_MODULE.RoleHealthLoop(
            roles=(telegram, target, detector),
        )
        with mock.patch.object(
            HEALTH_LOOP_MODULE, "terminate_process_group"
        ) as terminate, mock.patch.object(
            HEALTH_LOOP_MODULE.subprocess, "Popen", return_value=mock.Mock()
        ), mock.patch("builtins.print") as printed:
            loop._start_due_roles(5_000)

        terminate.assert_has_calls((
            mock.call(telegram_process), mock.call(target_process),
        ))
        self.assertEqual(terminate.call_count, 2)
        self.assertIsNone(telegram.process)
        self.assertIsNone(target.process)
        self.assertIsNotNone(detector.process)
        self.assertIn(
            "reason=ORDINARY_REQUIRED_SERVICE_DETECTION_PRIORITY",
            " ".join(str(call) for call in printed.call_args_list),
        )

    def test_persistent_handoff_uses_freshest_t0_across_active_assignments(self):
        """A stale source listed first cannot suppress a newer Matrix wake."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            matrix = root / "service-matrix.json"
            users = root / "users.registry"
            matrix.write_text(json.dumps({
                "items": {
                    "source-stale": {"services": {"__channel_liveness__": {
                        "ok": False,
                        "evidence_class": "DEFINITIVE_LOCAL_HARD_FAILURE",
                        "failure_state": "OBSERVED_CONTINUING",
                        "source_incident_id": "sfinc_stale",
                        "failure_event_id": "sfe_stale",
                        "confirmed_hard_failure_monotonic_ns": 100,
                    }}},
                    "source-fresh": {"services": {"__channel_liveness__": {
                        "ok": False,
                        "evidence_class": "DEFINITIVE_LOCAL_HARD_FAILURE",
                        "failure_state": "OBSERVED_NEW",
                        "source_incident_id": "sfinc_fresh",
                        "failure_event_id": "sfe_fresh",
                        "confirmed_hard_failure_monotonic_ns": 200,
                    }}},
                },
            }), encoding="utf-8")
            # The older source deliberately occurs first in registry order.
            users.write_text(
                "ip=10.7.0.10 enabled=1 current=source-stale\n"
                "ip=10.7.0.11 enabled=1 current=source-fresh\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HEALTH_LOOP_MODULE.canonical_definitive_hard_failure_t0_ns(
                    matrix, users
                ),
                200,
            )


if __name__ == "__main__":
    unittest.main()
