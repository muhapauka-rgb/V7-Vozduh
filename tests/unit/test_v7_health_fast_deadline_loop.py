"""Controlled checks for the existing v7-health deadline loop."""

from __future__ import annotations

import re
import subprocess
import tempfile
import textwrap
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOOP = ROOT / "tools/runtime-support/v7-health-loop"


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
        self.assertIn("ExecStart=/usr/local/bin/v7-health-loop", service)
        self.assertNotIn("sleep 30", service)
        self.assertIn("time.monotonic_ns", loop)
        self.assertIn("start_new_session=True", loop)
        self.assertIn("os.killpg", loop)
        self.assertNotIn("&", loop)
        self.assertIn('"name": "v7-health-loop"', sync)

    def test_controlled_commands_require_a_finite_polygon_run(self):
        result = subprocess.run(
            [str(LOOP), "--controlled-fast-command", "/bin/true"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertRegex(result.stderr, re.compile("require finite --max-phases"))


if __name__ == "__main__":
    unittest.main()
