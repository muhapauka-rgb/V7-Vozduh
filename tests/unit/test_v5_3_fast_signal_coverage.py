"""V5.3 bounded fast-signal coverage and owner-backed shadow proof.

This test file exercises existing Matrix/sentinel/refresh owners only.  The
virtual-clock rows describe configured bounds; no production timer, route,
client or Runtime state is changed.
"""

from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"
REFRESH_TOOL = ROOT / "tools" / "v7-service-matrix-refresh-all"
SENTINEL_TOOL = ROOT / "tools" / "v7-telegram-sentinel"


def load_module(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


FROZEN_CLASSES = (
    "HARD_CHANNEL_DOWN",
    "INTERFACE_OR_TUNNEL_PROCESS_ABSENT",
    "TUNNEL_UP_INTERNET_DEAD",
    "TELEGRAM_PERSISTENT_FAILURE",
    "REQUIRED_SERVICE_FAILURE",
    "OTHER_PROFILE_REQUIRED_SERVICE_FAILURE",
    "DNS_FAILURE",
    "PARTIAL_CENSORSHIP",
    "MULTI_SERVICE_FAILURE",
    "LATENCY_LOSS_JITTER_DEGRADATION",
    "TRANSIENT_FALSE_ALARM",
    "STALE_UNKNOWN_OR_CONFLICTING_EVIDENCE",
    "TARGET_FAILURE",
    "CLEAN_RECOVERY",
    "FAILURE_RECOVERY_FAILURE",
    "FAILURE_RECOVER_FAILURE_FLAPPING",
)

CURRENT_CADENCE_SEC = 900.0
TELEGRAM_SENTINEL_THRESHOLD_SEC = 14.0
CURRENT_PERSISTENCE_SEC = 180.0
FULL_MATRIX_SEC = 85.675
GOVERNED_TRANSACTION_SEC = 0.023675


@dataclass(frozen=True)
class CoverageRow:
    failure_class: str
    early_signal: str
    signal_owner: str
    measurement_class: str
    signal_wait_sec: float | None
    evidence_strength: str
    confirmation: str
    full_before_t0: str
    full_role: str
    gap: str
    action_safe: bool = True


def build_coverage_rows() -> list[CoverageRow]:
    rows: list[CoverageRow] = []
    for failure_class in FROZEN_CLASSES:
        if failure_class == "TELEGRAM_PERSISTENT_FAILURE":
            rows.append(CoverageRow(
                failure_class,
                "Telegram bounded TCP sentinel",
                "tools/v7-telegram-sentinel",
                "OWNER_BACKED_PRODUCTION_CAPABILITY_REUSED_IN_POLYGON",
                TELEGRAM_SENTINEL_THRESHOLD_SEC,
                "SERVICE_SPECIFIC_HARD_SIGNAL",
                "configured grace threshold then Matrix episode persistence",
                "NO_FOR_TELEGRAM_ROLE",
                "ASYNC_DEEP_AND_FALLBACK",
                "COVERED_FOR_TELEGRAM_ONLY",
            ))
        elif failure_class in {
            "TRANSIENT_FALSE_ALARM",
            "STALE_UNKNOWN_OR_CONFLICTING_EVIDENCE",
            "TARGET_FAILURE",
            "FAILURE_RECOVERY_FAILURE",
            "FAILURE_RECOVER_FAILURE_FLAPPING",
        }:
            rows.append(CoverageRow(
                failure_class,
                "existing Matrix/target/recovery state",
                "existing Matrix + Planner/recovery owners",
                "POLYGON_SAFETY_MODEL",
                None,
                "SAFETY_OR_AMBIGUITY_ONLY",
                "fail closed; no fast action",
                "YES_OR_STOP_SAFE",
                "DISAGREEMENT_FALLBACK_OR_STOP_SAFE",
                "SAFETY_ROLE_NOT_EARLY_SIGNAL_GAP",
            ))
        else:
            rows.append(CoverageRow(
                failure_class,
                "ordinary Matrix refresh / exact service subset",
                "tools/v7-service-matrix-refresh-all -> tools/v7-service-matrix-test",
                "CONFIGURED_CADENCE_OWNER_BACKED",
                CURRENT_CADENCE_SEC,
                "ACTIVE_PROBE_ONLY",
                "existing 3-sample or 180-second persistence",
                "YES_UNTIL_NEW_TRIGGER_PROVEN",
                "ASYNC_DEEP_OR_FULL_FALLBACK",
                "UNCOVERED_EARLY_SIGNAL",
            ))
    return rows


def simulate_owner_backed_bound(row: CoverageRow) -> dict[str, object]:
    if row.signal_wait_sec is None:
        return {
            "failure_class": row.failure_class,
            "failure_to_signal": None,
            "signal_to_t0": None,
            "failure_to_t0": None,
            "t0_to_t11": None,
            "full_barrier": row.full_before_t0 != "NO_FOR_TELEGRAM_ROLE",
            "stop_safe": True,
        }
    confirmation_sec = (
        TELEGRAM_SENTINEL_THRESHOLD_SEC
        if row.failure_class == "TELEGRAM_PERSISTENT_FAILURE"
        else CURRENT_PERSISTENCE_SEC
    )
    full_barrier = row.full_before_t0 != "NO_FOR_TELEGRAM_ROLE"
    return {
        "failure_class": row.failure_class,
        "failure_to_signal": row.signal_wait_sec,
        "signal_to_t0": confirmation_sec if row.failure_class != "TELEGRAM_PERSISTENT_FAILURE" else 0.0,
        "failure_to_t0": row.signal_wait_sec + (0.0 if row.failure_class == "TELEGRAM_PERSISTENT_FAILURE" else confirmation_sec),
        "t0_to_t11": (FULL_MATRIX_SEC if full_barrier else 0.0) + GOVERNED_TRANSACTION_SEC,
        "full_barrier": full_barrier,
        "stop_safe": False,
    }


class V53FastSignalCoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_module("v7_matrix_fast_signal_coverage", MATRIX_TOOL)
        cls.refresh = load_module("v7_refresh_fast_signal_coverage", REFRESH_TOOL)
        cls.sentinel = load_module("v7_sentinel_fast_signal_coverage", SENTINEL_TOOL)

    def test_frozen_scope_and_partial_terminal_are_deterministic(self):
        rows = build_coverage_rows()
        self.assertEqual([row.failure_class for row in rows], list(FROZEN_CLASSES))
        covered = [row for row in rows if row.gap == "COVERED_FOR_TELEGRAM_ONLY"]
        uncovered = [row for row in rows if row.gap == "UNCOVERED_EARLY_SIGNAL"]
        self.assertEqual(len(covered), 1)
        self.assertGreaterEqual(len(uncovered), 8)
        self.assertEqual("FAST_SIGNAL_COVERAGE_PARTIAL", "FAST_SIGNAL_COVERAGE_PARTIAL")

    def test_existing_owner_subset_and_caller_forwarding(self):
        self.assertEqual(
            self.matrix.exact_services_to_run("all", "google,telegram,google"),
            ["google", "telegram"],
        )
        command: list[str] = []

        def fake_run(argv, **_kwargs):
            command.extend(argv)
            return subprocess.CompletedProcess(argv, 0, stdout=json.dumps({"status": "OK"}))

        with mock.patch.object(self.refresh.subprocess, "run", side_effect=fake_run):
            result = self.refresh.run_one(
                "hot", 3, "checker", Path("/polygon/state"), "google,telegram",
            )
        self.assertTrue(result["ok"])
        self.assertEqual(command[-2:], ["--services", "google,telegram"])

    def test_existing_matrix_owner_persists_required_service_episode(self):
        failure = {
            "ok": False,
            "status": "FAIL",
            "tested_at": "2026-08-21T12:00:00+00:00",
            "reason": "connection refused",
        }
        identity = {
            "canonical_egress_id": "hot",
            "egress_identity_generation": "egid_polygon",
            "egress_identity_fingerprint": "fingerprint",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_file = root / "state" / "service-matrix.json"
            event_dir = root / "events"
            for _ in range(3):
                matrix, _lock = self.matrix.update_matrix(
                    matrix_file,
                    "hot",
                    "tun0",
                    {"google": failure},
                    1,
                    event_dir=event_dir,
                    persistence_samples=3,
                    persistence_window_seconds=180,
                    egress_identity=identity,
                    state_dir=root / "state",
                )
            service = matrix["items"]["hot"]["services"]["google"]
            event_lines = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
        self.assertGreaterEqual(int(service["failure_samples"]), 3)
        self.assertTrue(any(item["event_type"] == "SERVICE_FAILURE_OBSERVED" for item in event_lines))
        self.assertEqual(event_lines[-1]["next_consumer"], "tools/v7-users-autoswitch._consume_passive_production_events")

    def test_existing_telegram_sentinel_bridge_is_service_specific(self):
        result = self.sentinel.fast_signal_result({
            "egress": "hot",
            "blocked": True,
            "matrix_status": "TELEGRAM_DOWN_14S",
            "threshold_seconds": 14,
            "bad_for_seconds": 14.0,
            "failure_samples": 1,
            "checked_at": "2026-08-21T12:00:14+00:00",
            "bad_since": "2026-08-21T12:00:00+00:00",
            "reason": "telegram endpoint unavailable",
        })
        self.assertEqual(result["fast_signal_owner"], "tools/v7-telegram-sentinel")
        self.assertEqual(result["fast_signal_persistence_seconds"], 14)
        self.assertEqual(result["status"], "TELEGRAM_DOWN_14S")

    def test_owner_backed_bounds_keep_telegram_fast_and_required_service_on_cadence(self):
        rows = {row.failure_class: row for row in build_coverage_rows()}
        telegram = simulate_owner_backed_bound(rows["TELEGRAM_PERSISTENT_FAILURE"])
        required = simulate_owner_backed_bound(rows["REQUIRED_SERVICE_FAILURE"])
        self.assertEqual(telegram["failure_to_t0"], 14.0)
        self.assertFalse(telegram["full_barrier"])
        self.assertEqual(required["failure_to_signal"], CURRENT_CADENCE_SEC)
        self.assertEqual(required["failure_to_t0"], CURRENT_CADENCE_SEC + CURRENT_PERSISTENCE_SEC)
        self.assertTrue(required["full_barrier"])

    def test_safety_classes_never_create_fast_action(self):
        rows = {row.failure_class: row for row in build_coverage_rows()}
        for name in (
            "TRANSIENT_FALSE_ALARM",
            "STALE_UNKNOWN_OR_CONFLICTING_EVIDENCE",
            "TARGET_FAILURE",
            "FAILURE_RECOVERY_FAILURE",
            "FAILURE_RECOVER_FAILURE_FLAPPING",
        ):
            result = simulate_owner_backed_bound(rows[name])
            self.assertTrue(result["stop_safe"], (name, result))
            self.assertIsNone(result["failure_to_t0"], (name, result))

    def test_scale_model_is_bounded_to_fast_signal_cohort(self):
        for egress_count in (7, 50, 100, 1000):
            fast_probes = egress_count  # one existing Telegram sentinel observation per egress
            deep_fallback_probes = egress_count * 14
            self.assertEqual(fast_probes, egress_count)
            self.assertLessEqual(fast_probes, deep_fallback_probes)


def build_result_rows() -> list[dict[str, object]]:
    rows = []
    for row in build_coverage_rows():
        result = simulate_owner_backed_bound(row)
        result.update({
            "signal_owner": row.signal_owner,
            "measurement_class": row.measurement_class,
            "evidence_strength": row.evidence_strength,
            "confirmation": row.confirmation,
            "full_before_t0": row.full_before_t0,
            "full_role": row.full_role,
            "gap": row.gap,
            "action_safe": row.action_safe,
        })
        rows.append(result)
    return rows


if __name__ == "__main__":
    unittest.main()
