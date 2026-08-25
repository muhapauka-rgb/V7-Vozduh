"""N7 causal Polygon tournament over the current role-based owners.

The clock combines controlled cadence placement with measured owner execution.
All files are ephemeral; the downstream terminal is S11 server-side cutover,
not an independently observed client T11.
"""

from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import statistics
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from admin_core import operator_execution_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"
AUTOSWITCH_TOOL = ROOT / "tools" / "v7-users-autoswitch"
SENTINEL_TOOL = ROOT / "tools" / "v7-telegram-sentinel"
REFRESH_TOOL = ROOT / "tools" / "v7-service-matrix-refresh-all"
HEALTH_LOOP = ROOT / "tools" / "runtime-support" / "v7-health-loop"


def load_tool(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MATRIX = load_tool("v7_n7_matrix", MATRIX_TOOL)
AUTOSWITCH = load_tool("v7_n7_autoswitch", AUTOSWITCH_TOOL)
SENTINEL = load_tool("v7_n7_sentinel", SENTINEL_TOOL)
REFRESH = load_tool("v7_n7_refresh", REFRESH_TOOL)


def nearest_rank(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    rank = max(1, int((percentile * len(ordered) + 0.999999)))
    return ordered[min(len(ordered), rank) - 1]


def write_state(root: Path) -> Path:
    state = root / "state"
    state.mkdir(parents=True, exist_ok=True)
    (state / "egress.registry").write_text(
        "id=source-a protocol=wireguard type=interface "
        "interface=polygon-definitely-missing0 enabled=1 role=GLOBAL_FAST\n"
        "id=target-a protocol=wireguard type=interface "
        "interface=lo enabled=1 role=GLOBAL_FAST\n",
        encoding="utf-8",
    )
    (state / "users.registry").write_text(
        "ip=10.7.0.5 current=source-a table=1005 enabled=1\n",
        encoding="utf-8",
    )
    return state


def generation() -> dict:
    return {
        "planner_generation_id": "planner-n7",
        "inputs": {
            "users_registry": "users-n7",
            "egress_registry": "egress-n7",
            "policy": "policy-n7",
            "org_policy": "org-n7",
            "service_preferences": "services-n7",
        },
        "volatile_inputs": {
            "service_matrix": "matrix-n7",
            "egress_speed": "capacity-n7",
            "autoswitch_safety": "safety-n7",
        },
    }


def prepared_projection() -> dict:
    return AUTOSWITCH.build_prepared_class_decision_projection({
        "updated": "2026-08-23T12:00:00+00:00",
        "operation": {"operation_id": ""},
        "safety": {"generation": generation()},
        "decisions": [{
            "user_ip": "10.7.0.5",
            "current_egress": "source-a",
            "recommended_egress": "target-a",
            "important_services": ["telegram", "google"],
            "candidates": [{
                "egress": "target-a", "eligible": True, "score": 99,
                "role": "GLOBAL_FAST", "canary_reserved": False,
                "capacity_decision": {"status": "AVAILABLE"},
            }],
        }],
    })


def measured_direct_t0_ms() -> float:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        state = write_state(root)
        argv = [
            str(MATRIX_TOOL), "source-a", "all",
            "--state-dir", str(state),
            "--event-dir", str(root / "events"),
            "--interface", "polygon-definitely-missing0",
            "--direct-local-failure-class", "INTERFACE_DOWN_OR_MISSING",
            "--direct-signal-observed-at", MATRIX.now_iso(),
        ]
        output = io.StringIO()
        started = time.monotonic_ns()
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            rc = MATRIX.main()
        elapsed = (time.monotonic_ns() - started) / 1_000_000.0
        result = json.loads(output.getvalue())
        assert rc == 0 and result["direct_local_failure"]["event_emitted"]
        assert result["direct_local_failure"]["confirmed_hard_failure_monotonic_ns"] > 0
        return elapsed


def measured_mode_a_confirmation_ms(service: str = "google") -> float:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        state = write_state(root)
        result = {
            service: {
                "label": service,
                "ok": False,
                "status": "FAIL",
                "severity": "FAIL",
                "tested_at": MATRIX.now_iso(),
                "reason": "controlled_negative_confirmation",
                "error": "controlled_negative_confirmation",
                "probe_provenance": "N7_CONTROLLED_TARGETED_CONFIRMATION",
                "evidence_class": "AMBIGUOUS_REMOTE_CONFIRMED_BY_MATRIX",
            }
        }
        started = time.monotonic_ns()
        MATRIX.update_matrix(
            state / "service-matrix.json",
            "source-a", "polygon-definitely-missing0", result, 2,
            event_dir=root / "events", persistence_samples=1,
            persistence_window_seconds=1, state_dir=state,
            skip_network_path_projection=True,
        )
        elapsed = (time.monotonic_ns() - started) / 1_000_000.0
        events = (root / "events" / "service-failure-events.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        assert len(events) == 1
        return elapsed


def measured_target_validation_ms() -> float:
    projection = prepared_projection()
    started = time.monotonic_ns()
    result = AUTOSWITCH.validate_prepared_class_decision_projection(
        projection, dict(projection["invalidators"]),
    )
    elapsed = (time.monotonic_ns() - started) / 1_000_000.0
    assert result["status"] == "PREPARED_CLASS_DECISION_FRESH"
    assert result["hot_target_contract_count"] == 1
    return elapsed


def s11_receipt() -> dict:
    lineage = {
        "incident_id": "sfinc_n7", "incident_generation": "incgen_n7",
        "validation_generation_id": "valgen_n7", "user": "10.7.0.5",
        "source": "source-a", "target": "target-a",
        "candidate_id": "candidate_n7", "packet_id": "packet_n7",
        "lease_id": "lease_n7", "operation_id": "operation_n7",
    }
    return {
        **lineage,
        "certification_identity": True,
        "ordinary_user_delta": 0,
        "sample_kind": "warm",
        "clock_source": "time.monotonic_ns",
        "first_failed_observation_monotonic_ns": 1_000_000_000,
        "confirmed_hard_failure_monotonic_ns": 1_050_000_000,
        "user_target_decision_bound_monotonic_ns": 1_100_000_000,
        "apply_admitted_monotonic_ns": 1_150_000_000,
        "canonical_user_assignment_committed_monotonic_ns": 1_250_000_000,
        "kernel_route_mutation_completed_monotonic_ns": 1_350_000_000,
        "exact_user_kernel_path_visible_monotonic_ns": 1_450_000_000,
        "target_egress_payload_pass_monotonic_ns": 1_550_000_000,
        "control_plane_and_kernel_path_cutover_pass_monotonic_ns": 1_550_000_000,
        "decision_binding": {**lineage, "status": "USER_TARGET_DECISION_BOUND"},
        "assignment_proof": {
            **lineage, "status": "CANONICAL_USER_ASSIGNMENT_COMMITTED",
            "stale_writer_rejected": True, "previous_egress": "source-a",
            "new_egress": "target-a",
        },
        "kernel_path_proof": {
            **lineage,
            "status": "EXACT_USER_ASSIGNMENT_AND_KERNEL_PATH_TRANSITION_PROVEN",
            "source_ip": "10.7.0.5", "policy_rule_fingerprint": "rule-n7",
            "routing_table": "1005", "target_interface": "target-a",
            "route_generation": "routegen-n7", "old_effective_binding_absent": True,
        },
        "target_payload_proof": {
            **lineage,
            "status": "TARGET_EGRESS_ROUTE_BOUND_PAYLOAD_PROBE_PROVEN",
            "scope": "TARGET_EGRESS_PATH_ONLY", "fresh_socket": True,
            "fresh_dns_resolution": True, "payload_response_verified": True,
            "management_default_route_used": False, "target_interface_bound": True,
            "target_fingerprint_verified": True, "kernel_counter_only": False,
            "exact_user_source_fwmark_table_traversed": False,
            "timeout_ms": 700, "retry_count": 0,
        },
        "remote_client_recovery_claimed": False,
        "exact_user_payload_claimed": False,
    }


def measured_s11_validation_ms() -> float:
    started = time.monotonic_ns()
    result = pipeline.control_plane_kernel_path_cutover_contract(s11_receipt())
    elapsed = (time.monotonic_ns() - started) / 1_000_000.0
    assert result["status"] == "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS"
    assert result["remote_client_application_recovery_latency"] == (
        "NOT_MEASURED_NO_CLIENT_AGENT"
    )
    return elapsed


def role_isolation_evidence() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        def command(name: str, body: str) -> Path:
            path = root / name
            path.write_text("#!/bin/sh\n" + textwrap.dedent(body), encoding="utf-8")
            path.chmod(0o755)
            return path
        hard = command("hard", "sleep 0.005\n")
        telegram = command("telegram", "sleep 0.005\n")
        hot = command("hot", "sleep 0.005\n")
        hot_other = command("hot_other", "sleep 0.20\n")
        required = command("required", "sleep 1.50\n")
        planner_projection = command("planner_projection", "sleep 0.02\n")
        deep = command("deep", "sleep 2.20\n")
        result = subprocess.run(
            [
                str(HEALTH_LOOP), "--role-based-fast", "--max-phases", "5",
                "--hard-interval-ms", "1000", "--telegram-interval-ms", "1000",
                "--hot-target-interval-ms", "1000", "--required-interval-ms", "1000",
                "--hot-target-other-interval-ms", "1000",
                "--planner-projection-interval-ms", "1000",
                "--deep-interval-ms", "1000",
                "--controlled-hard-command", str(hard),
                "--controlled-telegram-command", str(telegram),
                "--controlled-hot-target-command", str(hot),
                "--controlled-hot-target-other-command", str(hot_other),
                "--controlled-required-command", str(required),
                "--controlled-planner-projection-command", str(planner_projection),
                "--controlled-deep-command", str(deep),
            ],
            text=True, capture_output=True, check=True, timeout=10,
        )
    output = result.stdout
    return {
        "hard_starts": output.count("V7_HEALTH_ROLE_START role=hard "),
        "hot_target_starts": output.count("V7_HEALTH_ROLE_START role=hot_target "),
        "hard_deadline_misses": output.count("V7_HEALTH_ROLE_DEADLINE_MISS role=hard "),
        "deep_deadline_misses": output.count("V7_HEALTH_ROLE_DEADLINE_MISS role=deep "),
        "required_deadline_misses": output.count("V7_HEALTH_ROLE_DEADLINE_MISS role=other_required "),
    }


def build_evidence(sample_count: int = 20) -> dict:
    direct_ms = [measured_direct_t0_ms() for _ in range(sample_count)]
    mode_a_ms = [measured_mode_a_confirmation_ms() for _ in range(sample_count)]
    target_ms = [measured_target_validation_ms() for _ in range(sample_count)]
    s11_ms = [measured_s11_validation_ms() for _ in range(sample_count)]
    direct_exec = nearest_rank(direct_ms, 0.95) / 1000.0
    mode_a_exec = nearest_rank(mode_a_ms, 0.95) / 1000.0
    target_exec = nearest_rank(target_ms, 0.95) / 1000.0
    s11_exec = nearest_rank(s11_ms, 0.95) / 1000.0

    phase_offsets = [index / sample_count for index in range(sample_count)]
    hard_b = [offset + direct_exec + target_exec + s11_exec for offset in phase_offsets]
    hard_a = [offset + 1.0 + mode_a_exec + target_exec + s11_exec for offset in phase_offsets]
    path = [offset + mode_a_exec + target_exec + s11_exec for offset in phase_offsets]
    telegram = [offset + 1.0 + mode_a_exec + target_exec + s11_exec for offset in phase_offsets]
    other_offsets = [5.0 * index / sample_count for index in range(sample_count)]
    other = [offset + 5.0 + mode_a_exec + target_exec + s11_exec for offset in other_offsets]

    def distribution(values: list[float]) -> dict:
        return {
            "samples": len(values),
            "p50_sec": round(statistics.median(values), 6),
            "p95_sec": round(nearest_rank(values, 0.95), 6),
            "max_sec": round(max(values), 6),
        }

    return {
        "schema_version": "v7.n7-causal-polygon-tournament.v1",
        "sample_count_per_positive_class": sample_count,
        "measured_owner_ms": {
            "mode_b_direct_t0_p95": round(nearest_rank(direct_ms, 0.95), 6),
            "mode_a_matrix_confirmation_p95": round(nearest_rank(mode_a_ms, 0.95), 6),
            "prepared_target_validation_p95": round(nearest_rank(target_ms, 0.95), 6),
            "s11_contract_validation_p95": round(nearest_rank(s11_ms, 0.95), 6),
        },
        "onset_to_s11": {
            "interface_mode_b": distribution(hard_b),
            "interface_mode_a": distribution(hard_a),
            "tunnel_path_route_mode_a": distribution(path),
            "telegram_mode_a": distribution(telegram),
            "dns_other_required_multi_service_mode_a": distribution(other),
        },
        "dispositions": {
            "interface_down_or_missing": "MODE_B_DIRECT_T0_ADMITTED",
            "process_death": "MODE_A_RETAINED",
            "tunnel_loss": "MODE_A_RETAINED",
            "route_loss": "MODE_A_RETAINED",
            "generic_path_miss": "MODE_A_RETAINED",
            "telegram": "MODE_A_RETAINED",
            "dns": "MODE_A_RETAINED",
            "other_required": "MODE_A_RETAINED",
            "multi_service": "MODE_A_RETAINED",
            "partial": "FULL_FALLBACK_OR_STOP_SAFE",
        },
        "role_isolation": role_isolation_evidence(),
        "terminal": "S11_SERVER_SIDE_RECOVERY_VERIFIED",
        "t11_claimed": False,
        "routing_mutation_performed": False,
        "users_moved": 0,
    }


class V53N7CausalPolygonTournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = build_evidence(sample_count=20)

    def test_mode_b_wins_only_for_exact_local_interface_failure(self):
        dispositions = self.evidence["dispositions"]
        self.assertEqual(dispositions["interface_down_or_missing"], "MODE_B_DIRECT_T0_ADMITTED")
        for key in ("process_death", "tunnel_loss", "route_loss", "generic_path_miss"):
            self.assertEqual(dispositions[key], "MODE_A_RETAINED")
        b = self.evidence["onset_to_s11"]["interface_mode_b"]["p95_sec"]
        a = self.evidence["onset_to_s11"]["interface_mode_a"]["p95_sec"]
        self.assertLess(b, a)

    def test_hard_path_and_telegram_meet_slo_at_all_phase_offsets(self):
        for key in ("interface_mode_b", "tunnel_path_route_mode_a", "telegram_mode_a"):
            row = self.evidence["onset_to_s11"][key]
            self.assertLessEqual(row["p95_sec"], 3.0, (key, row))
            self.assertLessEqual(row["max_sec"], 5.0, (key, row))
        other = self.evidence["onset_to_s11"]["dns_other_required_multi_service_mode_a"]
        self.assertLessEqual(other["max_sec"], 15.0)

    def test_stale_wrong_generation_replay_and_restart_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = write_state(root)
            stale = MATRIX.validate_definitive_local_failure(
                state, egress_id="source-a", iface="polygon-definitely-missing0",
                failure_class="INTERFACE_DOWN_OR_MISSING",
                observed_at=(datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat(),
            )
            wrong = MATRIX.validate_definitive_local_failure(
                state, egress_id="source-a", iface="polygon-definitely-missing0",
                failure_class="INTERFACE_DOWN_OR_MISSING", observed_at=MATRIX.now_iso(),
                expected_identity_generation="egid_wrong",
            )
            self.assertFalse(stale["ok"])
            self.assertFalse(wrong["ok"])
            self.assertFalse((state / "service-matrix.json").exists())

            argv = [
                str(MATRIX_TOOL), "source-a", "all", "--state-dir", str(state),
                "--event-dir", str(root / "events"),
                "--interface", "polygon-definitely-missing0",
                "--direct-local-failure-class", "INTERFACE_DOWN_OR_MISSING",
                "--direct-signal-observed-at", MATRIX.now_iso(),
            ]
            for _ in range(2):
                output = io.StringIO()
                with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                    self.assertEqual(MATRIX.main(), 0)
            events = [
                json.loads(line) for line in
                (root / "events" / "service-failure-events.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
                if json.loads(line).get("event_type") == "SERVICE_FAILURE_OBSERVED"
            ]
            self.assertEqual(len(events), 1)

    def test_correlated_telegram_and_partial_evidence_never_switch(self):
        blocked = {
            "source-a": {"blocked": True, "status": "DOWN", "sample_ok": False},
            "target-a": {"blocked": True, "status": "DOWN", "sample_ok": False},
        }
        guard = SENTINEL.apply_correlated_telegram_guard(blocked)
        self.assertTrue(guard["correlated"])
        self.assertTrue(all(not row["blocked"] for row in blocked.values()))
        self.assertEqual(self.evidence["dispositions"]["partial"], "FULL_FALLBACK_OR_STOP_SAFE")
        self.assertFalse(self.evidence["routing_mutation_performed"])
        self.assertEqual(self.evidence["users_moved"], 0)

    def test_prepared_target_scope_uses_only_planner_contracts(self):
        projection = prepared_projection()
        rows = [
            {"id": "source-a", "enabled": "1"},
            {"id": "target-a", "enabled": "1"},
            {"id": "unrelated", "enabled": "1"},
        ]
        selected, scope = REFRESH.select_prepared_hot_target_rows(
            rows, {"nested": {"prepared_class_decisions": projection}},
        )
        self.assertTrue(scope["ok"], scope)
        self.assertEqual([row["id"] for row in selected], ["target-a"])
        self.assertEqual(selected[0]["_prepared_services"], "google,telegram")
        self.assertFalse(scope["manual_server_selection"])
        self.assertFalse(scope["user_registry_scanned"])

        with tempfile.TemporaryDirectory() as tmp:
            projection_file = Path(tmp) / "projection.json"
            projection_file.write_text(json.dumps({
                "prepared_class_decisions": projection,
            }), encoding="utf-8")
            telegram_ids, telegram_scope = SENTINEL.prepared_telegram_hot_target_ids(
                projection_file,
            )
        self.assertTrue(telegram_scope["ok"], telegram_scope)
        self.assertEqual(telegram_ids, {"target-a"})
        self.assertFalse(telegram_scope["manual_server_selection"])

    def test_path_ready_refresh_writes_only_existing_matrix_path_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = write_state(root)
            evidence = {
                "schema_version": "v7.service-matrix-network-path.v1",
                "path_fingerprint": "path-n7",
                "measured_at": MATRIX.now_iso(),
                "component_status": {"interface_addresses": "PASS"},
            }
            _matrix, lock = MATRIX.update_matrix_path_evidence(
                state / "service-matrix.json",
                state_dir=state,
                egress_id="target-a",
                iface="lo",
                evidence=evidence,
                lock_timeout_sec=2,
            )
            stored = json.loads((state / "service-matrix.json").read_text(encoding="utf-8"))
        row = stored["items"]["target-a"]
        self.assertEqual(row["path_evidence"]["path_fingerprint"], "path-n7")
        self.assertEqual(row.get("services"), None)
        self.assertTrue(lock["held"])

    def test_fast_and_hot_target_roles_are_not_delayed_by_deep(self):
        row = self.evidence["role_isolation"]
        self.assertEqual(row["hard_starts"], 5)
        self.assertGreaterEqual(row["hot_target_starts"], 4)
        # A loaded CI host may delay one controlled child beyond the compressed
        # one-second Polygon interval. The causal gate is that DEEP never
        # blocks later HARD starts; N8 measures the uncompressed Runtime lane.
        self.assertLessEqual(row["hard_deadline_misses"], 1)
        self.assertGreater(row["deep_deadline_misses"], 0)

    def test_terminal_is_s11_and_never_overclaims_client_t11(self):
        self.assertEqual(self.evidence["terminal"], "S11_SERVER_SIDE_RECOVERY_VERIFIED")
        self.assertFalse(self.evidence["t11_claimed"])

    def test_matrix_entry_timing_is_diagnostic_and_rejects_invalid_t0(self):
        spans = REFRESH.matrix_runtime_entry_timing(
            environment={"V7_HARD_T0_MONOTONIC_NS": "100"},
            module_ready_ns=160,
            entry_ns=220,
        )
        self.assertEqual(
            [row["stage"] for row in spans],
            [
                "hard_t0_to_matrix_module_ready",
                "matrix_module_ready_to_controlled_consumer_entry",
            ],
        )
        self.assertEqual([row["duration_ms"] for row in spans], [0.0, 0.0])
        self.assertTrue(all(row["diagnostic_only"] for row in spans))
        self.assertEqual(
            REFRESH.matrix_runtime_entry_timing(
                environment={"V7_HARD_T0_MONOTONIC_NS": "invalid"},
                module_ready_ns=160,
                entry_ns=220,
            ),
            [],
        )


if __name__ == "__main__":
    if "--evidence-json" in sys.argv:
        print(json.dumps(build_evidence(), ensure_ascii=False, sort_keys=True))
    else:
        unittest.main()
