import os
import hashlib
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

    def test_controlled_source_reserve_and_release_are_exact_and_reversible(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=vless protocol=vless type=interface interface=tun0 "
                "enabled=1 role=GLOBAL_FAST\n"
            )
            ordinary_users = (
                "ip=10.0.0.2 current=awg0 table=100 enabled=1\n"
            )
            state = self.write_state(Path(tmp), original, ordinary_users)
            fingerprint = hashlib.sha256(original.rstrip("\n").encode()).hexdigest()

            reserve = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--reservation-id",
                "csr_test_1",
                "--reservation-expires-at",
                "2099-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                fingerprint,
                "--certification-group",
                "t48-rebind",
                "--apply",
                "--confirm",
                "RESERVE_CONTROLLED_CERTIFICATION_SOURCE",
            )

            self.assertEqual(
                reserve.returncode, 0, reserve.stdout + reserve.stderr
            )
            self.assertIn("ACTION=controlled_source_reserved", reserve.stdout)
            self.assertIn("users_moved=0", reserve.stdout)
            reserved = (
                state / "egress.registry"
            ).read_text(encoding="utf-8")
            self.assertIn("controlled_certification_source=1", reserved)
            self.assertIn("canary_reserved=1", reserved)
            self.assertIn("production_assignment_allowed=false", reserved)
            self.assertEqual(
                (state / "users.registry").read_text(encoding="utf-8"),
                ordinary_users,
            )
            restore_backup = next(
                line.split("=", 1)[1]
                for line in reserve.stdout.splitlines()
                if line.startswith("restore_backup=")
            )
            reserved_fingerprint = next(
                line.split("=", 1)[1]
                for line in reserve.stdout.splitlines()
                if line.startswith("reserved_egress_fingerprint=")
            )

            release = self.run_set_state(
                state,
                "vless",
                "certification-release",
                "--reservation-id",
                "csr_test_1",
                "--expected-egress-fingerprint",
                reserved_fingerprint,
                "--restore-backup",
                restore_backup,
                "--apply",
                "--confirm",
                "RELEASE_CONTROLLED_CERTIFICATION_SOURCE",
            )

            self.assertEqual(
                release.returncode, 0, release.stdout + release.stderr
            )
            self.assertIn("ACTION=controlled_source_released", release.stdout)
            self.assertEqual(
                (state / "egress.registry").read_text(encoding="utf-8"),
                original,
            )
            self.assertEqual(
                (state / "users.registry").read_text(encoding="utf-8"),
                ordinary_users,
            )

    def test_controlled_source_reserve_blocks_nonempty_or_changed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=vless protocol=vless type=interface interface=tun0 "
                "enabled=1 role=GLOBAL_FAST\n"
            )
            state = self.write_state(
                Path(tmp),
                original,
                "ip=10.7.0.2 current=vless enabled=1 certification_user=1\n",
            )
            fingerprint = hashlib.sha256(original.rstrip("\n").encode()).hexdigest()

            nonempty = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--reservation-id",
                "csr_test_2",
                "--reservation-expires-at",
                "2099-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                fingerprint,
            )
            self.assertEqual(nonempty.returncode, 2, nonempty.stdout)
            self.assertIn(
                "controlled_source_reservation_requires_empty_source",
                nonempty.stdout,
            )

            changed = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--reservation-id",
                "csr_test_2",
                "--reservation-expires-at",
                "2099-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                "0" * 64,
            )
            self.assertEqual(changed.returncode, 2, changed.stdout)
            self.assertIn("egress_fingerprint_changed", changed.stdout)

    def test_controlled_source_reservation_expiry_duplicate_and_release_identity_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=vless protocol=vless type=interface interface=tun0 "
                "enabled=1 role=GLOBAL_FAST\n"
            )
            state = self.write_state(Path(tmp), original, "")
            fingerprint = hashlib.sha256(
                original.rstrip("\n").encode()
            ).hexdigest()
            expired = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--reservation-id",
                "csr_expired",
                "--reservation-expires-at",
                "2025-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                fingerprint,
                "--apply",
                "--confirm",
                "RESERVE_CONTROLLED_CERTIFICATION_SOURCE",
            )
            self.assertEqual(expired.returncode, 1, expired.stdout)
            self.assertIn(
                "reservation expiry must be a future timezone-aware ISO8601 timestamp",
                expired.stdout,
            )
            self.assertEqual(
                (state / "egress.registry").read_text(encoding="utf-8"),
                original,
            )

            reserve = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--reservation-id",
                "csr_exact",
                "--reservation-expires-at",
                "2099-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                fingerprint,
                "--apply",
                "--confirm",
                "RESERVE_CONTROLLED_CERTIFICATION_SOURCE",
            )
            self.assertEqual(
                reserve.returncode, 0, reserve.stdout + reserve.stderr
            )
            restore_backup = next(
                line.split("=", 1)[1]
                for line in reserve.stdout.splitlines()
                if line.startswith("restore_backup=")
            )
            reserved_fingerprint = next(
                line.split("=", 1)[1]
                for line in reserve.stdout.splitlines()
                if line.startswith("reserved_egress_fingerprint=")
            )
            duplicate = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--reservation-id",
                "csr_duplicate",
                "--reservation-expires-at",
                "2099-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                fingerprint,
                "--apply",
                "--confirm",
                "RESERVE_CONTROLLED_CERTIFICATION_SOURCE",
            )
            self.assertEqual(duplicate.returncode, 2, duplicate.stdout)
            self.assertIn("egress_fingerprint_changed", duplicate.stdout)

            wrong_release = self.run_set_state(
                state,
                "vless",
                "certification-release",
                "--reservation-id",
                "csr_wrong",
                "--expected-egress-fingerprint",
                reserved_fingerprint,
                "--restore-backup",
                restore_backup,
                "--apply",
                "--confirm",
                "RELEASE_CONTROLLED_CERTIFICATION_SOURCE",
            )
            self.assertEqual(
                wrong_release.returncode, 2, wrong_release.stdout
            )
            self.assertIn(
                "controlled_source_reservation_identity_mismatch",
                wrong_release.stdout,
            )
            self.assertIn(
                "controlled_source_reservation_id=csr_exact",
                (state / "egress.registry").read_text(encoding="utf-8"),
            )

            release = self.run_set_state(
                state,
                "vless",
                "certification-release",
                "--reservation-id",
                "csr_exact",
                "--expected-egress-fingerprint",
                reserved_fingerprint,
                "--restore-backup",
                restore_backup,
                "--apply",
                "--confirm",
                "RELEASE_CONTROLLED_CERTIFICATION_SOURCE",
            )
            self.assertEqual(
                release.returncode, 0, release.stdout + release.stderr
            )
            repeated_release = self.run_set_state(
                state,
                "vless",
                "certification-release",
                "--reservation-id",
                "csr_exact",
                "--expected-egress-fingerprint",
                fingerprint,
                "--restore-backup",
                restore_backup,
                "--apply",
                "--confirm",
                "RELEASE_CONTROLLED_CERTIFICATION_SOURCE",
            )
            self.assertEqual(
                repeated_release.returncode, 2, repeated_release.stdout
            )
            self.assertIn(
                "controlled_source_reservation_identity_mismatch",
                repeated_release.stdout,
            )
            self.assertEqual(
                (state / "egress.registry").read_text(encoding="utf-8"),
                original,
            )


if __name__ == "__main__":
    unittest.main()
