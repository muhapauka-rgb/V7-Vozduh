from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-restore-settle-gate"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_restore_settle_gate", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class RestoreSettleGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def write_sample(
        self,
        root: Path,
        idx: int,
        *,
        selected_moves: int = 0,
        telegram_hard_blocked: bool = False,
        egress_1_eligible: bool = True,
        users_hash: str = "a" * 64,
        egress_hash: str = "b" * 64,
        checkers_ok: bool = True,
        movement_count: int = 0,
        timestamp: str | None = None,
    ) -> None:
        ts = timestamp or f"2026-05-26T07:{20 + idx:02d}:00+00:00"
        payload = {
            "timestamp": ts,
            "selected_moves": selected_moves,
            "candidate_moves_total": selected_moves,
            "telegram_hard_blocked": telegram_hard_blocked,
            "egress_1_eligible": egress_1_eligible,
            "users_registry_hash": users_hash,
            "egress_registry_hash": egress_hash,
            "checkers_ok": checkers_ok,
            "hidden_movers_observed": False,
            "movement_count": movement_count,
            "moved_users": ["10.7.0.5"] if movement_count else [],
        }
        (root / f"sample-{idx}.json").write_text(json.dumps(payload), encoding="utf-8")

    def report(self, root: Path, *, mode: str = "pre-restore") -> dict:
        return self.tool.evaluate_gate(
            self.tool.load_samples(root),
            mode=mode,
            required_samples=3,
            interval_seconds=60,
            required_timer_intervals=2,
            apply_timer_seconds=20,
        )

    def test_three_clean_samples_spanning_interval_is_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0, timestamp="2026-05-26T07:20:00+00:00")
            self.write_sample(root, 1, timestamp="2026-05-26T07:21:00+00:00")
            self.write_sample(root, 2, timestamp="2026-05-26T07:22:00+00:00")
            report = self.report(root)
            self.assertEqual(report["gate_status"], "GO")
            self.assertFalse(report["reasons"])

    def test_selected_moves_is_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0)
            self.write_sample(root, 1, selected_moves=1)
            self.write_sample(root, 2)
            report = self.report(root)
            self.assertEqual(report["gate_status"], "NO-GO")
            self.assertIn("selected_moves_observed", report["reasons"])

    def test_telegram_hard_block_is_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0)
            self.write_sample(root, 1, telegram_hard_blocked=True)
            self.write_sample(root, 2)
            report = self.report(root)
            self.assertEqual(report["gate_status"], "NO-GO")
            self.assertIn("telegram_hard_block_observed", report["reasons"])

    def test_egress_blocked_is_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0)
            self.write_sample(root, 1, egress_1_eligible=False)
            self.write_sample(root, 2)
            report = self.report(root)
            self.assertEqual(report["gate_status"], "NO-GO")
            self.assertIn("egress_1_blocked_or_ineligible", report["reasons"])

    def test_registry_hash_change_is_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0)
            self.write_sample(root, 1, users_hash="c" * 64)
            self.write_sample(root, 2)
            report = self.report(root)
            self.assertEqual(report["gate_status"], "NO-GO")
            self.assertIn("users_registry_hash_changed", report["reasons"])

    def test_too_short_window_is_conditional(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0, timestamp="2026-05-26T07:20:00+00:00")
            self.write_sample(root, 1, timestamp="2026-05-26T07:20:10+00:00")
            self.write_sample(root, 2, timestamp="2026-05-26T07:20:20+00:00")
            report = self.report(root)
            self.assertEqual(report["gate_status"], "CONDITIONAL")
            self.assertTrue(any(reason.startswith("apply_timer_intervals_below_required") for reason in report["reasons"]))

    def test_post_restore_delayed_movement_is_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0)
            self.write_sample(root, 1, movement_count=1)
            self.write_sample(root, 2)
            report = self.report(root, mode="post-restore")
            self.assertEqual(report["gate_status"], "NO-GO")
            self.assertIn("post_restore_movement_observed", report["reasons"])

    def test_post_restore_no_movement_is_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0)
            self.write_sample(root, 1)
            self.write_sample(root, 2)
            report = self.report(root, mode="post-restore")
            self.assertEqual(report["gate_status"], "GO")

    def test_cli_json_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_sample(root, 0)
            self.write_sample(root, 1)
            self.write_sample(root, 2)
            proc = subprocess.run(
                [sys.executable, str(TOOL), "--state-dir", str(root), "--json"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertFalse(payload["mutation"])
            self.assertFalse(payload["runtime_commands_executed"])


if __name__ == "__main__":
    unittest.main()
