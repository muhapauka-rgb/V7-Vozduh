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
        self.assertIn(
            "ExecStart=/usr/local/bin/v7-health-loop --role-based-fast", service,
        )
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
        self.assertIn("V7_HEALTH_ROLE_DEADLINE_MISS role=deep", completed.stdout)
        self.assertIn("V7_HEALTH_ROLE_COMPLETE role=deep", completed.stdout)


if __name__ == "__main__":
    unittest.main()
