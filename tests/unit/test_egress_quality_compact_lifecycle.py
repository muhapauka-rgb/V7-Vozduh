import fcntl
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Optional


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-egress-quality-compact"


class EgressQualityCompactLifecycleTest(unittest.TestCase):
    def write_runtime_sources(self, state_dir: Path) -> None:
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "v7-state.json").write_text(
            json.dumps({
                "egress": {
                    "vless": {
                        "code": "200",
                        "avg_mbps": 52.4,
                        "min_mbps": 44.8,
                        "stability": 0.94,
                        "users": 3,
                        "diagnose_severity": "OK",
                    }
                }
            }),
            encoding="utf-8",
        )
        (state_dir / "egress-speed.json").write_text(
            json.dumps({"items": {"vless": {"server_v7_mbps": 52.4, "server_v7_min_mbps": 44.8}}}),
            encoding="utf-8",
        )
        (state_dir / "service-matrix.json").write_text(
            json.dumps({
                "items": {
                    "vless": {
                        "services": {
                            "telegram": {"ok": True, "first_byte_sec": 0.11},
                            "youtube": {"ok": True, "first_byte_sec": 0.2},
                        }
                    }
                }
            }),
            encoding="utf-8",
        )

    def run_compactor(self, state_dir: Path, env: Optional[Dict[str, str]] = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "--state-dir",
                str(state_dir),
                "--summary-file",
                str(state_dir / "egress-quality-summary.json"),
                "--ring-file",
                str(state_dir / "egress-quality-ring.json"),
                "--restore-barrier-file",
                str(state_dir / "autoswitch-restore-barrier.json"),
                "--lock-timeout-sec",
                "1",
            ],
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )

    def test_compactor_serializes_quality_summary_write_with_service_matrix_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            self.write_runtime_sources(state_dir)

            result = self.run_compactor(state_dir)

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertTrue(payload["service_matrix_lock"]["acquired"])
            self.assertTrue(payload["service_matrix_lock"]["released"])
            self.assertEqual(
                payload["service_matrix_lock"]["decision"],
                "quality_summary_writer_serialized_for_planner_lifecycle",
            )
            self.assertTrue((state_dir / "egress-quality-summary.json").exists())
            self.assertTrue((state_dir / "egress-quality-ring.json").exists())

    def test_compactor_does_not_write_when_lifecycle_lock_is_held(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            self.write_runtime_sources(state_dir)
            lock_path = state_dir / "service-matrix.lock"
            fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

                result = self.run_compactor(state_dir)
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
                os.close(fd)

            self.assertEqual(result.returncode, 2, result.stdout)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["status"], "LOCK_TIMEOUT")
            self.assertFalse(payload["service_matrix_lock"]["acquired"])
            self.assertEqual(payload["service_matrix_lock"]["decision"], "service_matrix_lifecycle_lock_timeout")
            self.assertFalse((state_dir / "egress-quality-summary.json").exists())
            self.assertFalse((state_dir / "egress-quality-ring.json").exists())

    def test_compactor_can_inherit_existing_lifecycle_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            self.write_runtime_sources(state_dir)
            env = dict(os.environ)
            env["V7_SERVICE_MATRIX_LOCK_HELD"] = "1"

            result = self.run_compactor(state_dir, env=env)

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertTrue(payload["service_matrix_lock"]["acquired"])
            self.assertTrue(payload["service_matrix_lock"]["inherited"])
            self.assertEqual(payload["service_matrix_lock"]["decision"], "service_matrix_lifecycle_lock_inherited")
            self.assertTrue((state_dir / "egress-quality-summary.json").exists())

    def test_compactor_skips_write_during_active_restore_barrier_clearance(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            self.write_runtime_sources(state_dir)
            (state_dir / "autoswitch-restore-barrier.json").write_text(
                json.dumps({
                    "clearance_expires_at": (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat(),
                    "clearance_expected_selected_moves": 5,
                    "approved_selected_moves_hash": "unit-test-selected-moves",
                    "allowed_users": ["10.0.0.2", "10.0.0.3"],
                }),
                encoding="utf-8",
            )

            result = self.run_compactor(state_dir)

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["status"], "SKIPPED_RESTORE_BARRIER_ACTIVE")
            self.assertEqual(
                payload["restore_barrier_pause"]["reason"],
                "active_restore_barrier_clearance_window",
            )
            self.assertTrue(payload["service_matrix_lock"]["acquired"])
            self.assertTrue(payload["service_matrix_lock"]["released"])
            self.assertFalse((state_dir / "egress-quality-summary.json").exists())
            self.assertFalse((state_dir / "egress-quality-ring.json").exists())


if __name__ == "__main__":
    unittest.main()
