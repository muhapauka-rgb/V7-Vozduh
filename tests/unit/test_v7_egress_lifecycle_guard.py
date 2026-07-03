import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / "tools" / "runtime-support" / "v7-egress-guard"
SET_STATE = ROOT / "tools" / "v7-egress-set-state"


class V7EgressLifecycleGuardTest(unittest.TestCase):
    def write_state(self, root: Path, egress_line: str, users: str) -> Path:
        state = root / "state"
        state.mkdir()
        bin_dir = root / "bin"
        bin_dir.mkdir()
        date_stub = bin_dir / "date"
        date_stub.write_text("#!/usr/bin/env bash\necho 2026-01-01T00:00:00+00:00\n", encoding="utf-8")
        date_stub.chmod(0o755)
        (state / "egress.registry").write_text(egress_line, encoding="utf-8")
        (state / "users.registry").write_text(users, encoding="utf-8")
        return state

    def env_for(self, state: Path) -> dict[str, str]:
        env = os.environ.copy()
        env["V7_STATE_DIR"] = str(state)
        env["PATH"] = f"{state.parent / 'bin'}:{ROOT / 'tools' / 'runtime-support'}:{env['PATH']}"
        return env

    def run_guard(self, state: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(GUARD), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env_for(state),
        )

    def run_set_state(self, state: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(SET_STATE), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env_for(state),
        )

    def test_default_guard_blocks_assigned_users(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1\n",
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1\n",
            )

            result = self.run_guard(state, "wg1")

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("V7_EGRESS_GUARD=BLOCK", result.stdout)
            self.assertIn("reason=users_assigned", result.stdout)

    def test_controlled_guard_blocks_unmarked_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1\n",
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1\n",
            )

            result = self.run_guard(state, "wg1", "--controlled-certification")

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("reason=controlled_certification_source_not_marked", result.stdout)

    def test_controlled_guard_blocks_non_certification_users(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 controlled_certification_source=1\n",
                "\n".join([
                    "ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1",
                    "ip=10.7.0.3 current=wg1 table=101 enabled=1",
                    "",
                ]),
            )

            result = self.run_guard(state, "wg1", "--controlled-certification")

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("reason=non_certification_users_assigned", result.stdout)
            self.assertIn("assigned_user=10.7.0.3", result.stdout)

    def test_controlled_guard_allows_marked_source_with_certification_users_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 controlled_certification_source=1\n",
                "\n".join([
                    "ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1",
                    "ip=10.7.0.3 current=wg1 table=101 enabled=1 certification_group=medium-batch",
                    "ip=10.7.0.4 current=vless table=102 enabled=1",
                    "",
                ]),
            )

            result = self.run_guard(state, "wg1", "--controlled-certification")

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("V7_EGRESS_GUARD=OK", result.stdout)
            self.assertIn("reason=assigned_certification_users_scoped", result.stdout)
            self.assertIn("assigned_certification_user=10.7.0.2 table=100", result.stdout)
            self.assertIn("assigned_certification_user=10.7.0.3 table=101", result.stdout)

    def test_set_state_passes_controlled_certification_guard_flag_in_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 controlled_certification_source=1 config=/tmp/wg1.conf\n",
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1\n",
            )

            result = self.run_set_state(state, "wg1", "maintenance", "--controlled-certification")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("V7_EGRESS_GUARD=OK", result.stdout)
            self.assertIn("reason=assigned_certification_users_scoped", result.stdout)
            self.assertIn("MODE=dry_run", result.stdout)
            self.assertIn("ACTION=none", result.stdout)

    def test_set_state_without_controlled_flag_still_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 controlled_certification_source=1 config=/tmp/wg1.conf\n",
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1\n",
            )

            result = self.run_set_state(state, "wg1", "maintenance")

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("reason=users_assigned", result.stdout)
            self.assertIn("ACTION=blocked", result.stdout)

    def test_certification_scope_dry_run_does_not_write_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 config=/tmp/wg1.conf\n",
                "ip=10.7.0.2 current=wg1 table=100 enabled=1\n",
            )

            result = self.run_set_state(
                state,
                "wg1",
                "certification-scope",
                "--certification-users",
                "10.7.0.2",
                "--certification-group",
                "medium-batch",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("MODE=dry_run", result.stdout)
            self.assertIn("would_mark_source=wg1", result.stdout)
            self.assertNotIn("controlled_certification_source=1", (state / "egress.registry").read_text(encoding="utf-8"))
            self.assertNotIn("certification_user=1", (state / "users.registry").read_text(encoding="utf-8"))

    def test_certification_scope_blocks_user_not_on_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 config=/tmp/wg1.conf\n",
                "ip=10.7.0.2 current=vless table=100 enabled=1\n",
            )

            result = self.run_set_state(
                state,
                "wg1",
                "certification-scope",
                "--certification-users",
                "10.7.0.2",
                "--apply",
            )

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("reason=certification_users_not_enabled_on_source", result.stdout)

    def test_certification_scope_apply_marks_source_and_users(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 config=/tmp/wg1.conf\n",
                "\n".join([
                    "ip=10.7.0.2 current=wg1 table=100 enabled=1",
                    "ip=10.7.0.3 current=wg1 table=101 enabled=1",
                    "ip=10.7.0.4 current=vless table=102 enabled=1",
                    "",
                ]),
            )

            result = self.run_set_state(
                state,
                "wg1",
                "certification-scope",
                "--certification-users",
                "10.7.0.2,10.7.0.3",
                "--certification-group",
                "medium-batch",
                "--apply",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("ACTION=certification_scope_marked", result.stdout)
            egress = (state / "egress.registry").read_text(encoding="utf-8")
            users = (state / "users.registry").read_text(encoding="utf-8")
            self.assertIn("controlled_certification_source=1", egress)
            self.assertIn("certification_group=medium-batch", egress)
            self.assertIn("ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1 certification_group=medium-batch", users)
            self.assertIn("ip=10.7.0.3 current=wg1 table=101 enabled=1 certification_user=1 certification_group=medium-batch", users)
            self.assertIn("ip=10.7.0.4 current=vless table=102 enabled=1\n", users)

    def test_certification_scope_then_controlled_maintenance_passes_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(
                Path(tmp),
                "id=wg1 protocol=wireguard type=interface interface=wg1 enabled=1 config=/tmp/wg1.conf\n",
                "ip=10.7.0.2 current=wg1 table=100 enabled=1\n",
            )

            mark = self.run_set_state(
                state,
                "wg1",
                "certification-scope",
                "--certification-users",
                "10.7.0.2",
                "--apply",
            )
            self.assertEqual(mark.returncode, 0, mark.stdout + mark.stderr)

            maintenance = self.run_set_state(state, "wg1", "maintenance", "--controlled-certification")

            self.assertEqual(maintenance.returncode, 0, maintenance.stdout + maintenance.stderr)
            self.assertIn("V7_EGRESS_GUARD=OK", maintenance.stdout)
            self.assertIn("reason=assigned_certification_users_scoped", maintenance.stdout)
            self.assertIn("MODE=dry_run", maintenance.stdout)


if __name__ == "__main__":
    unittest.main()
