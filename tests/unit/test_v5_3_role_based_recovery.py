"""N1/N4 role-based local-failure and Matrix-owned T0 contracts.

All state is ephemeral.  The tests exercise the existing Matrix writer and do
not invoke Planner, Packet, lease, routes or users.
"""

from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
import subprocess
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"
DIAGNOSE_TOOL = ROOT / "tools" / "v7-egress-diagnose"
SENTINEL_TOOL = ROOT / "tools" / "v7-telegram-sentinel"


def load_matrix():
    loader = importlib.machinery.SourceFileLoader("v7_matrix_role_recovery", str(MATRIX_TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class V53RoleBasedRecoveryTest(unittest.TestCase):
    def test_service_matrix_majority_failure_wakes_existing_health_consumer(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_health_loop_matrix_majority", str(ROOT / "tools/runtime-support/v7-health-loop")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        health = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[loader.name] = health
        spec.loader.exec_module(health)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_path = root / "service-matrix.json"
            users_path = root / "users.registry"
            checked = datetime.now(timezone.utc).isoformat()
            failed = {
                "ok": False,
                "status": "FAIL",
                "source_incident_id": "sfinc_current",
                "failure_event_id": "sfe_current",
                "confirmed_hard_failure_monotonic_ns": 123456789,
            }
            matrix_path.write_text(json.dumps({
                "items": {"vless": {
                    "updated": checked,
                    "services": {
                        "google": failed,
                        "youtube": dict(failed),
                        "telegram": {"ok": True, "status": "OK"},
                        "__channel_liveness__": {"ok": True, "status": "OK"},
                    },
                }},
            }), encoding="utf-8")
            users_path.write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            self.assertEqual(
                health.canonical_service_failure_t0_ns(matrix_path, users_path),
                123456789,
            )

    def test_service_matrix_majority_failure_remains_fail_closed_when_stale(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_health_loop_matrix_stale", str(ROOT / "tools/runtime-support/v7-health-loop")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        health = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[loader.name] = health
        spec.loader.exec_module(health)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_path = root / "service-matrix.json"
            users_path = root / "users.registry"
            stale = (datetime.now(timezone.utc) - timedelta(seconds=1801)).isoformat()
            matrix_path.write_text(json.dumps({
                "items": {"vless": {
                    "updated": stale,
                    "services": {
                        "google": {
                            "ok": False, "status": "FAIL",
                            "source_incident_id": "sfinc_old",
                            "failure_event_id": "sfe_old",
                            "confirmed_hard_failure_monotonic_ns": 123,
                        },
                        "youtube": {"ok": True, "status": "OK"},
                    },
                }},
            }), encoding="utf-8")
            users_path.write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            self.assertEqual(
                health.canonical_service_failure_t0_ns(matrix_path, users_path),
                0,
            )

    def test_service_matrix_majority_ignores_unidentified_rows_without_blocking_identified_quorum(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_health_loop_matrix_mixed_identity", str(ROOT / "tools/runtime-support/v7-health-loop")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        health = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[loader.name] = health
        spec.loader.exec_module(health)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_path = root / "service-matrix.json"
            users_path = root / "users.registry"
            checked = datetime.now(timezone.utc).isoformat()
            matrix_path.write_text(json.dumps({
                "items": {"vless": {
                    "updated": checked,
                    "services": {
                        # A newly observed row may not have episode IDs yet.
                        "whatsapp": {"ok": False, "status": "FAIL"},
                        "google": {
                            "ok": False, "status": "FAIL",
                            "source_incident_id": "sfinc_google",
                            "failure_event_id": "sfe_google",
                            "confirmed_hard_failure_monotonic_ns": 111,
                        },
                        "youtube": {
                            "ok": False, "status": "FAIL",
                            "source_incident_id": "sfinc_youtube",
                            "failure_event_id": "sfe_youtube",
                            "confirmed_hard_failure_monotonic_ns": 222,
                        },
                        "telegram": {"ok": True, "status": "OK"},
                        "__channel_liveness__": {"ok": True, "status": "OK"},
                    },
                }},
            }), encoding="utf-8")
            users_path.write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            self.assertEqual(
                health.canonical_service_failure_t0_ns(matrix_path, users_path),
                222,
            )

    def test_hard_failure_keeps_fast_consumer_in_same_priority_window(self):
        diagnose = DIAGNOSE_TOOL.read_text(encoding="utf-8")
        service = (
            ROOT / "systemd" / "drafts" / "v7-autoswitch-planner.service"
        ).read_text(encoding="utf-8")

        # The current health parent consumes its one existing Matrix event
        # through the deployed Matrix consumer directly.  This avoids a
        # second systemd scheduling hop; it is not a manual Planner call.
        health_loop = (
            ROOT / "tools" / "runtime-support" / "v7-health-loop"
        ).read_text(encoding="utf-8")
        self.assertIn(
            '"--consumer-wake-command", "/usr/local/bin/v7-service-matrix-refresh-all"',
            health_loop,
        )
        self.assertIn(
            '--consume-existing-service-failure-events-only', diagnose,
        )
        self.assertIn('--runtime-hot-path-only', diagnose)
        self.assertNotIn("Nice=10", service)
        self.assertNotIn("IOSchedulingPriority=7", service)

    @classmethod
    def setUpClass(cls):
        cls.matrix = load_matrix()
        loader = importlib.machinery.SourceFileLoader("v7_sentinel_role_recovery", str(SENTINEL_TOOL))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.sentinel = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cls.sentinel)

    @staticmethod
    def write_state(root: Path, *, interface: str = "polygon-definitely-missing0") -> Path:
        state = root / "state"
        state.mkdir(parents=True)
        (state / "egress.registry").write_text(
            "id=source-a protocol=wireguard type=interface "
            f"interface={interface} enabled=1 role=GLOBAL_FAST\n",
            encoding="utf-8",
        )
        (state / "users.registry").write_text(
            "ip=10.7.0.5 current=source-a table=1005 enabled=1\n",
            encoding="utf-8",
        )
        return state

    def invoke_direct(self, root: Path, *, observed_at: str, generation: str = "") -> tuple[int, dict]:
        state = root / "state"
        argv = [
            str(MATRIX_TOOL), "source-a", "all",
            "--state-dir", str(state),
            "--event-dir", str(root / "events"),
            "--interface", "polygon-definitely-missing0",
            "--direct-local-failure-class", "INTERFACE_DOWN_OR_MISSING",
            "--direct-signal-observed-at", observed_at,
        ]
        if generation:
            argv.extend(["--direct-signal-identity-generation", generation])
        output = io.StringIO()
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            rc = self.matrix.main()
        return rc, json.loads(output.getvalue())

    def invoke_direct_recovery(self, root: Path) -> tuple[int, dict]:
        state = root / "state"
        argv = [
            str(MATRIX_TOOL), "source-a", "all",
            "--state-dir", str(state),
            "--event-dir", str(root / "events"),
            "--interface", "polygon-definitely-missing0",
            "--direct-local-recovery",
        ]
        output = io.StringIO()
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(self.matrix, "interface_live", return_value=True),
            contextlib.redirect_stdout(output),
        ):
            rc = self.matrix.main()
        return rc, json.loads(output.getvalue())

    def test_definitive_missing_interface_writes_t0_once_without_network_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(root)
            with mock.patch.object(
                self.matrix, "network_path_evidence",
                side_effect=AssertionError("direct T0 must not run a source network projection"),
            ):
                first_rc, first = self.invoke_direct(root, observed_at=self.matrix.now_iso())
                second_rc, second = self.invoke_direct(root, observed_at=self.matrix.now_iso())

            events = [
                json.loads(line)
                for line in (root / "events" / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            matrix = json.loads((root / "state" / "service-matrix.json").read_text(encoding="utf-8"))

        self.assertEqual(first_rc, 0, first)
        self.assertEqual(second_rc, 0, second)
        self.assertEqual(first["direct_local_failure"]["mode"], "MODE_B_DIRECT_T0")
        self.assertTrue(first["direct_local_failure"]["event_emitted"])
        self.assertFalse(second["direct_local_failure"]["event_emitted"])
        self.assertTrue(first["direct_local_failure"]["source_network_probe_skipped"])
        observed_events = [row for row in events if row.get("event_type") == "SERVICE_FAILURE_OBSERVED"]
        self.assertEqual(len(observed_events), 1)
        self.assertEqual(
            observed_events[0]["evidence_class"],
            "MATRIX_VALIDATED_DEFINITIVE_LOCAL_HARD_FAILURE",
        )
        self.assertEqual(observed_events[0]["direct_t0_mode"], "MODE_B_DIRECT_T0")
        self.assertTrue(observed_events[0]["source_network_probe_skipped"])
        self.assertEqual(matrix["items"]["source-a"]["status"], "NOT_STARTED")

    def test_stale_wrong_generation_and_ambiguous_class_fail_closed_without_write(self):
        cases = (
            {
                "failure_class": "INTERFACE_DOWN_OR_MISSING",
                "observed_at": (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat(),
                "generation": "",
                "blocker": "signal_stale",
            },
            {
                "failure_class": "INTERFACE_DOWN_OR_MISSING",
                "observed_at": self.matrix.now_iso(),
                "generation": "egid_wrong",
                "blocker": "egress_identity_generation_mismatch",
            },
            {
                "failure_class": "TUNNEL_UP_INTERNET_DEAD",
                "observed_at": self.matrix.now_iso(),
                "generation": "",
                "blocker": "failure_class_not_admitted_for_direct_t0",
            },
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                state = self.write_state(root)
                result = self.matrix.validate_definitive_local_failure(
                    state,
                    egress_id="source-a",
                    iface="polygon-definitely-missing0",
                    failure_class=case["failure_class"],
                    observed_at=case["observed_at"],
                    expected_identity_generation=case["generation"],
                )
                self.assertFalse(result["ok"], result)
                self.assertIn(case["blocker"], result["blockers"])
                self.assertFalse((state / "service-matrix.json").exists())

    def test_direct_local_recovery_closes_episode_once_and_emits_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(root)
            failure_rc, failure = self.invoke_direct(root, observed_at=self.matrix.now_iso())
            recovery_rc, recovery = self.invoke_direct_recovery(root)
            second_rc, second = self.invoke_direct_recovery(root)
            matrix = json.loads((root / "state" / "service-matrix.json").read_text(encoding="utf-8"))
            events = [
                json.loads(line)
                for line in (root / "events" / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]

        direct = matrix["items"]["source-a"]["services"]["__channel_liveness__"]
        self.assertEqual(failure_rc, 0, failure)
        self.assertEqual(recovery_rc, 0, recovery)
        self.assertTrue(recovery["direct_local_recovery"]["event_emitted"])
        self.assertEqual(second_rc, 0, second)
        self.assertEqual(second["status"], "HEALTHY_NO_OPEN_EPISODE")
        self.assertTrue(direct["ok"])
        self.assertEqual(direct["failure_state"], "RECOVERY_OBSERVED")
        self.assertEqual(
            len([event for event in events if event.get("event_type") == "SERVICE_RECOVERY_OBSERVED"]),
            1,
        )

    def test_mode_a_is_binding_for_every_remote_or_service_ambiguity(self):
        ambiguous = {
            "TUNNEL_UP_INTERNET_DEAD", "TELEGRAM_PERSISTENT_FAILURE",
            "REQUIRED_SERVICE_FAILURE", "OTHER_PROFILE_REQUIRED_SERVICE_FAILURE",
            "DNS_FAILURE", "PARTIAL_CENSORSHIP", "MULTI_SERVICE_FAILURE",
            "LATENCY_LOSS_JITTER_DEGRADATION", "STALE_UNKNOWN_OR_CONFLICTING_EVIDENCE",
        }
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(Path(tmp))
            for failure_class in sorted(ambiguous):
                result = self.matrix.validate_definitive_local_failure(
                    state,
                    egress_id="source-a",
                    iface="polygon-definitely-missing0",
                    failure_class=failure_class,
                    observed_at=self.matrix.now_iso(),
                )
                self.assertFalse(result["ok"], (failure_class, result))
                self.assertIn("failure_class_not_admitted_for_direct_t0", result["blockers"])

    def test_n1_n4_tournament_admits_one_second_mode_b_only_for_local_hard_failure(self):
        downstream_reserve_sec = 1.5
        matrix_commit_sec = 0.05
        candidates = []
        for cadence_ms in (250, 500, 1000, 2000):
            mode_b_to_s11 = cadence_ms / 1000 + matrix_commit_sec + downstream_reserve_sec
            candidates.append({
                "cadence_ms": cadence_ms,
                "checks_per_second_at_1000": 1000 * (1000 / cadence_ms),
                "mode_b_to_s11": mode_b_to_s11,
                "pass": mode_b_to_s11 <= 3.0,
            })
        winner = min(
            (row for row in candidates if row["pass"]),
            key=lambda row: row["checks_per_second_at_1000"],
        )
        self.assertEqual(winner["cadence_ms"], 1000)
        mode_a_repeat_to_s11 = 2.0 + matrix_commit_sec + downstream_reserve_sec
        self.assertGreater(mode_a_repeat_to_s11, 3.0)
        self.assertLessEqual(winner["mode_b_to_s11"], 3.0)

    def test_existing_diagnose_owner_scans_only_active_sources_and_wakes_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.write_state(root)
            with (state / "egress.registry").open("a", encoding="utf-8") as handle:
                handle.write(
                    "id=unused protocol=wireguard type=interface "
                    "interface=polygon-unused-missing0 enabled=1\n"
                )
            wake_trace = root / "wake.trace"
            wake = root / "wake"
            wake.write_text(f"#!/bin/sh\necho wake >> '{wake_trace}'\n", encoding="utf-8")
            wake.chmod(0o755)
            output = state / "egress-diagnose.state"
            command = [
                str(DIAGNOSE_TOOL),
                "--state-dir", str(state),
                "--output", str(output),
                "--hard-signal-only",
                "--definitive-matrix-command", str(MATRIX_TOOL),
                "--consumer-wake-command", str(wake),
            ]
            env = os.environ.copy()
            env["V7_EVENT_DIR"] = str(root / "events")
            first = subprocess.run(
                command, text=True, capture_output=True, check=False,
                timeout=10, env=env,
            )
            second = subprocess.run(
                command, text=True, capture_output=True, check=False,
                timeout=10, env=env,
            )
            values = dict(
                line.split("=", 1)
                for line in output.read_text(encoding="utf-8").splitlines()
                if "=" in line
            )
            wake_lines = wake_trace.read_text(encoding="utf-8").splitlines()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(values["hard_signal_active_source_count"], "1")
        self.assertEqual(values["hard_signal_observation_count"], "1")
        self.assertEqual(values["hard_signal_new_t0_count"], "0")
        self.assertNotIn("unused_hard_signal_status", values)
        self.assertEqual(wake_lines, ["wake"])

    def test_existing_diagnose_invokes_direct_matrix_consumer_with_unit_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.write_state(root)
            wake_trace = root / "wake.trace"
            wake = root / "v7-service-matrix-refresh-all"
            wake.write_text(
                f"#!/bin/sh\nprintf '%s\\n' \"$*\" > '{wake_trace}'\n",
                encoding="utf-8",
            )
            wake.chmod(0o755)
            command = [
                str(DIAGNOSE_TOOL),
                "--state-dir", str(state),
                "--output", str(state / "egress-diagnose.state"),
                "--hard-signal-only",
                "--definitive-matrix-command", str(MATRIX_TOOL),
                "--consumer-wake-command", str(wake),
            ]
            env = os.environ.copy()
            env["V7_EVENT_DIR"] = str(root / "events")
            result = subprocess.run(
                command, text=True, capture_output=True, check=False,
                timeout=10, env=env,
            )
            wake_args = wake_trace.read_text(encoding="utf-8").strip()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            wake_args,
            "--consume-existing-service-failure-events-only --runtime-hot-path-only",
        )

    def test_persistent_health_handoff_skips_child_only_after_matrix_t0_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.write_state(root)
            wake_trace = root / "wake.trace"
            wake = root / "v7-service-matrix-refresh-all"
            wake.write_text(
                f"#!/bin/sh\nprintf wake > '{wake_trace}'\n", encoding="utf-8"
            )
            wake.chmod(0o755)
            command = [
                str(DIAGNOSE_TOOL), "--state-dir", str(state),
                "--output", str(state / "egress-diagnose.state"),
                "--hard-signal-only",
                "--definitive-matrix-command", str(MATRIX_TOOL),
                "--consumer-wake-command", str(wake),
            ]
            env = os.environ.copy()
            env["V7_EVENT_DIR"] = str(root / "events")
            env["V7_HEALTH_PERSISTENT_MATRIX_CONSUMER"] = "1"
            result = subprocess.run(
                command, text=True, capture_output=True, check=False,
                timeout=10, env=env,
            )
            values = dict(
                line.split("=", 1)
                for line in (state / "egress-diagnose.state").read_text(
                    encoding="utf-8"
                ).splitlines()
                if "=" in line
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values["source-a_hard_signal_status"], "EMITTED")
        self.assertFalse(wake_trace.exists())

    def test_existing_diagnose_owner_closes_direct_episode_when_interface_recovers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.write_state(root, interface="lo")
            matrix = {
                "items": {
                    "source-a": {
                        "services": {
                            "__channel_liveness__": {
                                "ok": False,
                                "status": "NOT_STARTED",
                                "severity": "FAIL",
                                "failure_episode_id": "sfep_polygon_open",
                                "failure_event_id": "sfe_polygon_open",
                                "failure_state": "OBSERVED_CONTINUING",
                                "failure_family": "RUNTIME_INTERFACE_UNAVAILABLE",
                                "failure_started_at": self.matrix.now_iso(),
                                "observed_at": self.matrix.now_iso(),
                            }
                        }
                    }
                }
            }
            (state / "service-matrix.json").write_text(json.dumps(matrix), encoding="utf-8")
            wake_trace = root / "wake.trace"
            wake = root / "wake"
            wake.write_text(f"#!/bin/sh\necho wake >> '{wake_trace}'\n", encoding="utf-8")
            wake.chmod(0o755)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            ip_tool = bin_dir / "ip"
            ip_tool.write_text(
                "#!/bin/sh\necho '1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536'\n",
                encoding="utf-8",
            )
            ip_tool.chmod(0o755)
            matrix_trace = root / "matrix.trace"
            matrix_receiver = bin_dir / "matrix-receiver"
            matrix_receiver.write_text(
                "#!/bin/sh\nprintf '%s\\n' \"$*\" > \"$MATRIX_TRACE\"\n"
                "printf '%s\\n' '{\"direct_local_recovery\":{\"status\":\"CANONICAL_RECOVERY_WRITTEN\",\"event_emitted\":true}}'\n",
                encoding="utf-8",
            )
            matrix_receiver.chmod(0o755)
            output = state / "egress-diagnose.state"
            env = os.environ.copy()
            env["V7_EVENT_DIR"] = str(root / "events")
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["MATRIX_TRACE"] = str(matrix_trace)
            result = subprocess.run(
                [
                    str(DIAGNOSE_TOOL),
                    "--state-dir", str(state),
                    "--output", str(output),
                    "--hard-signal-only",
                    "--definitive-matrix-command", str(matrix_receiver),
                    "--consumer-wake-command", str(wake),
                ],
                text=True, capture_output=True, check=False, timeout=10, env=env,
            )
            out = output.read_text(encoding="utf-8")
            receiver_args = matrix_trace.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("source-a_hard_signal_recovery_status=EMITTED", out)
        self.assertIn("hard_signal_recovery_count=1", out)
        self.assertIn(
            "source-a_hard_signal_recovery_consumer_wake=NOT_REQUIRED_RECOVERY_EVENT",
            out,
        )
        self.assertFalse(wake_trace.exists())
        self.assertIn("--direct-local-recovery", receiver_args)
        self.assertIn(f"--event-dir {root / 'events'}", receiver_args)

    def test_production_hard_signal_uses_canonical_event_owner_path(self):
        source = DIAGNOSE_TOOL.read_text(encoding="utf-8")
        self.assertIn(
            'if [ "$STATE_DIR" = "/opt/v7/egress/state" ]; then',
            source,
        )
        self.assertIn('CANONICAL_EVENT_DIR="/opt/v7/events"', source)
        self.assertNotIn(
            '--event-dir "${SHADOW_TRIGGER_EVENT_DIR:-${STATE_DIR}/../events}"',
            source,
        )

    def test_telegram_role_scope_is_profile_contract_not_all_egresses_or_users(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "egress.registry").write_text(
                "id=source-a interface=a enabled=1\n"
                "id=source-b interface=b enabled=1\n"
                "id=cold-unused interface=c enabled=1\n",
                encoding="utf-8",
            )
            (state / "users.registry").write_text(
                "ip=10.7.0.1 current=source-a enabled=1\n"
                "ip=10.7.0.2 current=source-a enabled=1\n"
                "ip=10.7.0.3 current=source-b enabled=1\n"
                "ip=10.7.0.4 current=cold-unused enabled=0\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "enabled": True,
                "users": {
                    "10.7.0.1": {"services": ["telegram", "google"]},
                    "10.7.0.2": {"services": ["telegram"]},
                    "10.7.0.3": {"services": ["youtube"]},
                    "10.7.0.4": {"services": ["telegram"]},
                },
            }), encoding="utf-8")
            sources = self.sentinel.telegram_required_source_ids(state)
            rows = self.sentinel.egress_items(state, "", required_profiles_only=True)

        self.assertEqual(sources, {"source-a"})
        self.assertEqual([row["id"] for row in rows], ["source-a"])

    def test_telegram_requires_two_distinct_failed_targets_and_suppresses_correlation(self):
        args = SimpleNamespace(
            threshold_seconds=2,
            failure_samples=2,
            endpoint_samples_per_cycle=1,
            timeout=0.25,
        )
        row = {"id": "source-a", "interface": "lo", "type": "proxy"}
        failures = iter((
            {
                "sample_ok": False, "status": "DOWN", "score": 0,
                "ratio": 0.0, "critical_ok": False, "ok_count": 0, "total": 1,
                "reason": "target-a timeout", "samples": [],
                "sample_target_ids": ["target-a:443"], "total_sec": 0.25,
            },
            {
                "sample_ok": False, "status": "DOWN", "score": 0,
                "ratio": 0.0, "critical_ok": False, "ok_count": 0, "total": 1,
                "reason": "target-b timeout", "samples": [],
                "sample_target_ids": ["target-b:443"], "total_sec": 0.25,
            },
        ))
        with mock.patch.object(
            self.sentinel, "check_telegram_rotating_sample", side_effect=lambda *_a, **_k: next(failures),
        ):
            first = self.sentinel.check_egress(row, {}, args)
            second = self.sentinel.check_egress(row, {"source-a": first}, args)

        self.assertFalse(first["blocked"])
        self.assertEqual(first["failure_samples"], 1)
        self.assertTrue(second["blocked"])
        self.assertEqual(second["distinct_failure_target_count"], 2)

        peer = dict(second, egress="source-b")
        guard = self.sentinel.apply_correlated_telegram_guard({
            "source-a": second,
            "source-b": peer,
        })
        self.assertTrue(guard["correlated"])
        self.assertFalse(second["blocked"])
        self.assertFalse(peer["blocked"])
        self.assertEqual(second["matrix_status"], "DEGRADED")

    def test_n2_cadence_tournament_selects_one_second_on_slo_and_probe_budget(self):
        # Two distinct failed targets are required. Worst phase wait is one
        # cadence plus the second observation; endpoint cost is one socket per
        # role-scoped egress per phase.
        candidates = []
        for cadence_ms in (250, 500, 1000):
            worst_detection_ms = cadence_ms * 2
            probes_per_second_at_1000 = 1000 * (1000 / cadence_ms)
            candidates.append({
                "cadence_ms": cadence_ms,
                "worst_detection_ms": worst_detection_ms,
                "probes_per_second_at_1000": probes_per_second_at_1000,
                "slo_pass": worst_detection_ms <= 3000,
            })
        admitted = [row for row in candidates if row["slo_pass"]]
        winner = min(admitted, key=lambda row: row["probes_per_second_at_1000"])
        self.assertEqual(winner["cadence_ms"], 1000)
        self.assertEqual(winner["worst_detection_ms"], 2000)
        self.assertEqual(winner["probes_per_second_at_1000"], 1000)

    def test_n3_batch_uses_one_existing_matrix_process_and_no_canonical_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            count = 50
            (state / "egress.registry").write_text(
                "".join(
                    f"id=s{index} protocol=wireguard type=interface interface=if{index} enabled=1\n"
                    for index in range(count)
                ),
                encoding="utf-8",
            )
            contracts = root / "contracts.tsv"
            contracts.write_text(
                "".join(
                    f"s{index}\tu{index}\tgoogle\tstate-{index}\n"
                    for index in range(count)
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                self.matrix,
                "run_lightweight_service_sentinel",
                side_effect=lambda service, iface, _timeout: {
                    "ok": True, "status": "OK", "service": service, "interface": iface,
                },
            ):
                result = self.matrix.batch_lightweight_observations(
                    state, contracts, concurrency=16, timeout_seconds=0.5,
                )
            matrix_exists = (state / "service-matrix.json").exists()

        self.assertTrue(result["ok"], result)
        self.assertEqual(result["contract_count"], count)
        self.assertEqual(result["probe_count"], count)
        self.assertEqual(result["concurrency_cap"], 16)
        self.assertFalse(result["canonical_write_performed"])
        self.assertFalse(result["direct_t0_allowed"])
        self.assertTrue(all(row["failure_count"] == 0 for row in result["contracts"]))
        self.assertFalse(matrix_exists)

    def test_n9_n3_rejects_timeout_bound_overrun_before_opening_sockets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            count = 1000
            (state / "egress.registry").write_text(
                "".join(
                    f"id=s{index} interface=if{index} enabled=1\n"
                    for index in range(count)
                ),
                encoding="utf-8",
            )
            contracts = root / "contracts.tsv"
            contracts.write_text(
                "".join(
                    f"s{index}\tu{index}\tgoogle,youtube,google_auth\tstate-{index}\n"
                    for index in range(count)
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                self.matrix, "run_lightweight_service_sentinel",
            ) as probe:
                result = self.matrix.batch_lightweight_observations(
                    state, contracts, concurrency=128, timeout_seconds=0.5,
                )

        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "NO_5S_PROFILE_SERVICE_ROLE_CAPACITY")
        self.assertEqual(result["probe_count"], 3000)
        self.assertEqual(result["network_probes_started"], 0)
        self.assertEqual(result["fallback"], "EXISTING_STAGGERED_DEEP_FULL_MATRIX")
        probe.assert_not_called()

    def test_n3_tournament_selects_five_seconds_and_cap_128_for_1000_contracts(self):
        # One 500 ms lightweight socket per distinct contract.  At cap 128 the
        # timeout-bound pass is <=4 s. Two failed passes plus a bounded 3 s
        # targeted Matrix confirmation stay within the 15 s N3 class.
        caps = (8, 16, 32, 64, 128)
        cap_rows = [
            {
                "cap": cap,
                "timeout_bound_pass_sec": ((1000 + cap - 1) // cap) * 0.5,
            }
            for cap in caps
        ]
        passing_caps = [row for row in cap_rows if row["timeout_bound_pass_sec"] <= 5.0]
        self.assertEqual(min(row["cap"] for row in passing_caps), 128)
        cadence_rows = []
        for cadence in (5, 10, 15, 30):
            failure_to_t0 = cadence + 4.0 + 3.0
            cadence_rows.append({"cadence": cadence, "failure_to_t0": failure_to_t0})
        passing = [row for row in cadence_rows if row["failure_to_t0"] <= 15.0]
        self.assertEqual([row["cadence"] for row in passing], [5])

    def test_n3_batch_producer_keeps_two_samples_then_uses_existing_matrix_receiver(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.write_state(root, interface="v7wg")
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {"10.7.0.5": {"services": ["google"]}},
            }), encoding="utf-8")
            bindir = root / "bin"
            bindir.mkdir()
            ip = bindir / "ip"
            ip.write_text(
                "#!/bin/sh\necho '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n",
                encoding="utf-8",
            )
            ip.chmod(0o755)
            checker = bindir / "checker"
            checker.write_text(
                "#!/bin/sh\nprintf '%s\\n' '"
                '{"status":"PASS","ok":true,"probe_count":1,"contracts":['
                '{"source":"source-a","profile":"10.7.0.5","services":["google"],'
                '"state_key":"source-a-profile-unit","failure_count":1,'
                '"dns_services":[],"degraded_services":[],"failed_services":["google:TIMEOUT"],'
                '"unknown_services":[],"blockers":[]}]}'
                "'\n",
                encoding="utf-8",
            )
            checker.chmod(0o755)
            receiver_trace = root / "receiver.trace"
            receiver = bindir / "receiver"
            receiver.write_text(
                f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> '{receiver_trace}'\n",
                encoding="utf-8",
            )
            receiver.chmod(0o755)
            output = state / "egress-diagnose.state"
            env = dict(**__import__("os").environ)
            env["PATH"] = f"{bindir}:{env['PATH']}"
            command = [
                str(DIAGNOSE_TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only", "--lightweight-batch-producer",
                "--fast-producer-concurrency", "128",
                "--profile-service-suspicion-command", str(checker),
                "--shadow-trigger-command", str(receiver),
                "--profile-service-failure-samples", "2",
                "--profile-service-cooldown-sec", "0",
            ]
            first = subprocess.run(command, text=True, capture_output=True, env=env, check=False, timeout=10)
            first_state = output.read_text(encoding="utf-8")
            second = subprocess.run(command, text=True, capture_output=True, env=env, check=False, timeout=10)
            second_state = output.read_text(encoding="utf-8")
            receiver_lines = receiver_trace.read_text(encoding="utf-8").splitlines()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("profile_trigger_status=WAITING_REPEAT", first_state)
        self.assertIn("fast_producer_batch_status=PASS", second_state)
        self.assertIn("fast_producer_batch_probe_count=1", second_state)
        self.assertEqual(len(receiver_lines), 1)
        self.assertIn("--shadow-trigger-class OTHER_PROFILE_REQUIRED_SERVICE_FAILURE", receiver_lines[0])


if __name__ == "__main__":
    unittest.main()
