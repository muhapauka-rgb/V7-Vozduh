import contextlib
import fcntl
import json
import os
import sys
import tempfile
import threading
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, Tuple
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-telegram-sentinel"


def load_sentinel():
    loader = SourceFileLoader("v7_telegram_sentinel_under_test", str(TOOL))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TelegramSentinelLockScopeTest(unittest.TestCase):
    def setUp(self):
        self.sentinel = load_sentinel()

    def write_registry(self, state_dir: Path) -> None:
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "egress.registry").write_text(
            "\n".join([
                "id=vless interface=vless0 type=proxy enabled=true",
                "id=awg0 interface=awg0 type=wireguard enabled=true",
            ]) + "\n",
            encoding="utf-8",
        )

    def run_main(self, root: Path, *, extra_args: Optional[List[str]] = None) -> Tuple[int, dict]:
        state_dir = root / "state"
        argv = [
            "v7-telegram-sentinel",
            "--state-dir",
            str(state_dir),
            "--matrix-file",
            str(state_dir / "service-matrix.json"),
            "--sentinel-file",
            str(state_dir / "telegram-sentinel.json"),
            "--event-dir",
            str(root / "events"),
            "--threshold-seconds",
            "14",
            "--timeout",
            "0.01",
            "--lock-timeout-sec",
            "1",
            "--no-autoswitch",
        ]
        if extra_args:
            argv.extend(extra_args)
        with mock.patch.object(sys, "argv", argv), mock.patch("builtins.print") as mocked_print:
            rc = self.sentinel.main()
        printed = mocked_print.call_args.args[0] if mocked_print.call_args else "{}"
        return rc, json.loads(printed)

    def ok_probe(self, iface: str, timeout: float) -> dict:
        return {
            "sample_ok": True,
            "status": "OK",
            "score": 100,
            "ratio": 1.0,
            "critical_ok": True,
            "ok_count": 5,
            "total": 5,
            "reason": "unit probe ok",
            "samples": [],
            "first_byte_sec": 0.001,
            "total_sec": 0.001,
        }

    def test_network_probe_runs_without_service_matrix_lock_held(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)
            lock_path = state_dir / "service-matrix.lock"
            probe_mutex = threading.Lock()

            def probe_asserts_lock_free(iface: str, timeout: float) -> dict:
                # Two egress probes run concurrently; serialize this assertion
                # so a sibling probe cannot be mistaken for the Matrix writer.
                with probe_mutex:
                    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
                    try:
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        fcntl.flock(fd, fcntl.LOCK_UN)
                    finally:
                        os.close(fd)
                return self.ok_probe(iface, timeout)

            with (
                mock.patch.object(self.sentinel, "check_telegram", side_effect=probe_asserts_lock_free),
                mock.patch.object(
                    self.sentinel,
                    "publish_fast_signal_to_canonical_matrix",
                    return_value={"status": "NO_CONFIRMED_HARD_FAILURE", "ok": True},
                ),
            ):
                rc, payload = self.run_main(root)

            self.assertEqual(rc, 0, payload)
            self.assertTrue(payload["service_matrix_lock"]["held"])
            self.assertTrue(payload["service_matrix_lock"]["released"])
            self.assertLess(payload["service_matrix_lock"]["held_sec"], 0.05)

    def test_lock_wraps_only_matrix_merge_write_after_probes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)
            events: list[str] = []
            original_lock = self.sentinel.service_matrix_writer_lock
            original_write = self.sentinel.write_json_atomic

            def probe(iface: str, timeout: float) -> dict:
                events.append(f"probe:{iface}")
                return self.ok_probe(iface, timeout)

            @contextlib.contextmanager
            def observed_lock(matrix_file: Path, timeout_sec: int):
                events.append("lock_attempt")
                with original_lock(matrix_file, timeout_sec) as info:
                    events.append("lock_acquired")
                    try:
                        yield info
                    finally:
                        events.append("lock_releasing")
                events.append("lock_released")

            def observed_write(path: Path, data) -> None:
                if path.name == "service-matrix.json":
                    events.append("matrix_write")
                return original_write(path, data)

            with (
                mock.patch.object(self.sentinel, "check_telegram", side_effect=probe),
                mock.patch.object(self.sentinel, "service_matrix_writer_lock", side_effect=observed_lock),
                mock.patch.object(self.sentinel, "write_json_atomic", side_effect=observed_write),
            ):
                rc, payload = self.run_main(root)

            self.assertEqual(rc, 0, payload)
            self.assertLess(max(i for i, event in enumerate(events) if event.startswith("probe:")), events.index("lock_attempt"))
            self.assertGreater(events.index("matrix_write"), events.index("lock_acquired"))
            self.assertLess(events.index("matrix_write"), events.index("lock_releasing"))

    def test_service_matrix_write_is_atomic_and_preserves_existing_services(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)
            matrix_file = state_dir / "service-matrix.json"
            matrix_file.write_text(
                json.dumps({
                    "items": {
                        "vless": {
                            "services": {
                                "youtube": {"ok": True, "status": "OK"}
                            }
                        }
                    }
                }),
                encoding="utf-8",
            )

            with mock.patch.object(self.sentinel, "check_telegram", side_effect=self.ok_probe):
                rc, payload = self.run_main(root)

            self.assertEqual(rc, 0, payload)
            matrix = json.loads(matrix_file.read_text(encoding="utf-8"))
            self.assertTrue(matrix["items"]["vless"]["services"]["youtube"]["ok"])
            self.assertTrue(matrix["items"]["vless"]["services"]["telegram"]["ok"])
            self.assertFalse(list(state_dir.glob(".service-matrix.json.tmp.*")))

    def test_concurrent_writer_wait_does_not_corrupt_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)
            lock_path = state_dir / "service-matrix.lock"
            fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            original_sleep = self.sentinel.time.sleep
            released = threading.Event()

            def release_on_wait(seconds: float) -> None:
                if not released.is_set():
                    fcntl.flock(fd, fcntl.LOCK_UN)
                    os.close(fd)
                    released.set()
                original_sleep(0)

            try:
                with (
                    mock.patch.object(self.sentinel, "check_telegram", side_effect=self.ok_probe),
                    mock.patch.object(self.sentinel.time, "sleep", side_effect=release_on_wait),
                ):
                    rc, payload = self.run_main(root)
            finally:
                if not released.is_set():
                    fcntl.flock(fd, fcntl.LOCK_UN)
                    os.close(fd)

            self.assertEqual(rc, 0, payload)
            self.assertTrue(payload["service_matrix_lock"]["held"])
            self.assertTrue(payload["service_matrix_lock"]["released"])
            self.assertGreaterEqual(payload["service_matrix_lock"]["waited_sec"], 0)
            matrix = json.loads((state_dir / "service-matrix.json").read_text(encoding="utf-8"))
            self.assertIn("telegram", matrix["items"]["vless"]["services"])

    def test_probe_failure_does_not_leave_service_matrix_lock_held(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)

            with mock.patch.object(self.sentinel, "check_telegram", side_effect=RuntimeError("probe boom")):
                with self.assertRaises(RuntimeError):
                    self.run_main(root)

            fd = os.open(state_dir / "service-matrix.lock", os.O_RDWR | os.O_CREAT, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(fd, fcntl.LOCK_UN)
            finally:
                os.close(fd)

    def test_write_failure_releases_service_matrix_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)
            original_write = self.sentinel.write_json_atomic

            def fail_matrix_write(path: Path, data) -> None:
                if path.name == "service-matrix.json":
                    raise OSError("write boom")
                return original_write(path, data)

            with (
                mock.patch.object(self.sentinel, "check_telegram", side_effect=self.ok_probe),
                mock.patch.object(self.sentinel, "write_json_atomic", side_effect=fail_matrix_write),
            ):
                with self.assertRaises(OSError):
                    self.run_main(root)

            fd = os.open(state_dir / "service-matrix.lock", os.O_RDWR | os.O_CREAT, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(fd, fcntl.LOCK_UN)
            finally:
                os.close(fd)

    def test_existing_sentinel_behavior_produces_telegram_matrix_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)

            with mock.patch.object(self.sentinel, "check_telegram", side_effect=self.ok_probe):
                rc, payload = self.run_main(root)

            self.assertEqual(rc, 0, payload)
            self.assertEqual(payload["checked_egress"], 2)
            matrix = json.loads((state_dir / "service-matrix.json").read_text(encoding="utf-8"))
            telegram = matrix["items"]["vless"]["services"]["telegram"]
            self.assertTrue(telegram["ok"])
            self.assertEqual(telegram["status"], "OK")
            self.assertEqual(telegram["kind"], "telegram_tcp_sentinel")

    def test_confirmed_fast_failure_uses_canonical_matrix_event_owner(self):
        """A fast signal is a producer bridge, never a second failover owner."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)
            calls: list[dict] = []

            def canonical_update(*args, **kwargs):
                channel = str(args[1])
                calls.append({"channel": channel, "args": args, "kwargs": kwargs})
                return ({
                    "items": {
                        channel: {
                            "services": {
                                "telegram": {
                                    "failure_episode_id": f"sfep_{channel}",
                                    "failure_event_id": f"sfe_{channel}",
                                    "source_incident_id": f"sfinc_{channel}",
                                    "failure_state": "OBSERVED_NEW",
                                    "confirmed_hard_failure_monotonic_ns": 42,
                                }
                            }
                        }
                    }
                }, {"inherited": True})

            owner = SimpleNamespace(
                update_matrix=canonical_update,
                canonical_egress_identity=lambda *_args, **_kwargs: {
                    "egress_identity_generation": "egid_unit",
                },
                egress_row=lambda *_args, **_kwargs: {"id": "unit"},
            )
            down = {
                "sample_ok": False,
                "status": "NOT_STARTED",
                "score": 0,
                "ratio": 0.0,
                "critical_ok": False,
                "ok_count": 0,
                "total": 5,
                "reason": "unit hard failure",
                "samples": [],
                "first_byte_sec": "",
                "total_sec": 0.001,
            }
            with (
                mock.patch.object(self.sentinel, "check_telegram", return_value=down),
                mock.patch.object(self.sentinel, "service_matrix_owner", return_value=owner),
            ):
                rc, payload = self.run_main(root)

            self.assertEqual(rc, 0, payload)
            bridge = payload["fast_signal_bridge"]
            self.assertEqual(
                bridge["status"],
                "CONFIRMED_FAILURE_PUBLISHED_TO_EXISTING_MATRIX_OWNER",
            )
            self.assertEqual(sorted(row["channel"] for row in calls), ["awg0", "vless"])
            for call in calls:
                self.assertEqual(call["args"][3]["telegram"]["status"], "DOWN")
                self.assertEqual(call["kwargs"]["persistence_samples"], 1)
                self.assertEqual(call["kwargs"]["persistence_window_seconds"], 14)
            self.assertEqual(bridge["events_created"], 2)
            self.assertFalse(bridge["runtime_mutation_performed"])
            self.assertFalse(bridge["routing_mutation_performed"])
            self.assertEqual(bridge["users_moved"], 0)

    def test_fast_signal_does_not_call_canonical_owner_without_confirmed_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            self.write_registry(state_dir)
            with (
                mock.patch.object(self.sentinel, "check_telegram", side_effect=self.ok_probe),
                mock.patch.object(self.sentinel, "service_matrix_owner") as owner,
            ):
                rc, payload = self.run_main(root)
            self.assertEqual(rc, 0, payload)
            self.assertEqual(payload["fast_signal_bridge"]["status"], "NO_CONFIRMED_HARD_FAILURE")
            owner.assert_not_called()

    def test_fast_signal_preserves_threshold_crossing_into_canonical_episode(self):
        item = {
            "blocked": True,
            "matrix_status": "TELEGRAM_DOWN_14S",
            "bad_since": "2026-08-12T10:00:00+00:00",
            "checked_at": "2026-08-12T10:00:14+00:00",
            "bad_for_seconds": 14.0,
            "threshold_seconds": 14,
            "critical_ok": False,
            "ok_count": 0,
            "total": 5,
            "reason": "unit threshold crossed",
            "samples": [],
        }
        result = self.sentinel.fast_signal_result(item)
        self.assertEqual(result["status"], "TELEGRAM_DOWN_14S")
        self.assertEqual(result["failure_started_at"], item["bad_since"])
        self.assertEqual(result["bad_for_seconds"], 14.0)
        self.assertEqual(result["failure_samples"], 1)


if __name__ == "__main__":
    unittest.main()
