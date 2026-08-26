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
        nft_stub = bin_dir / "nft"
        nft_stub.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "state=${V7_NFT_FAKE_STATE:?}\n"
            "if [ \"${1:-}\" = list ] && [ \"${2:-}\" = table ]; then\n"
            "  [ -f \"$state\" ] || exit 1\n"
            "  cat \"$state\"\n"
            "  exit 0\n"
            "fi\n"
            "if [ \"${1:-}\" = -f ] && [ \"${2:-}\" = - ]; then\n"
            "  cat > \"$state\"\n"
            "  exit 0\n"
            "fi\n"
            "if [ \"${1:-}\" = delete ] && [ \"${2:-}\" = table ]; then\n"
            "  rm -f \"$state\"\n"
            "  exit 0\n"
            "fi\n"
            "exit 1\n",
            encoding="utf-8",
        )
        nft_stub.chmod(0o755)
        (state / "egress.registry").write_text(egress_line, encoding="utf-8")
        (state / "users.registry").write_text(users, encoding="utf-8")
        return state

    def env_for(self, state: Path) -> dict[str, str]:
        env = os.environ.copy()
        env["V7_STATE_DIR"] = str(state)
        env["V7_NFT_FAKE_STATE"] = str(state / "nft.table")
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

    def test_certification_failure_dry_run_preserves_enabled_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=wg1 protocol=wireguard type=interface interface=wg1 "
                "enabled=1 role=EXECUTION_ONLY config=/tmp/wg1.conf "
                "controlled_certification_source=1 "
                "reservation_owner=operator_execution_governance "
                "certification_group=n10 controlled_source_reservation_id=n10-r1 "
                "controlled_source_reservation_expires_at=2099-01-01T00:00:00+00:00\n"
            )
            state = self.write_state(
                Path(tmp),
                original,
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 "
                "certification_user=1 certification_group=n10\n",
            )
            fingerprint = hashlib.sha256(
                original.rstrip("\n").encode()
            ).hexdigest()

            result = self.run_set_state(
                state,
                "wg1",
                "certification-failure",
                "--controlled-certification",
                "--certification-users",
                "10.7.0.2",
                "--certification-group",
                "n10",
                "--reservation-id",
                "n10-r1",
                "--expected-egress-fingerprint",
                fingerprint,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("would_runtime=down_without_registry_disable", result.stdout)
            self.assertIn("registry_enabled_preserved=1", result.stdout)
            self.assertEqual(
                (state / "egress.registry").read_text(encoding="utf-8"),
                original,
            )

    def test_certification_failure_rejects_scope_or_reservation_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=wg1 protocol=wireguard type=interface interface=wg1 "
                "enabled=1 role=EXECUTION_ONLY config=/tmp/wg1.conf "
                "controlled_certification_source=1 "
                "reservation_owner=operator_execution_governance "
                "certification_group=n10 controlled_source_reservation_id=n10-r1 "
                "controlled_source_reservation_expires_at=2099-01-01T00:00:00+00:00\n"
            )
            state = self.write_state(
                Path(tmp),
                original,
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 "
                "certification_user=1 certification_group=n10\n",
            )
            fingerprint = hashlib.sha256(
                original.rstrip("\n").encode()
            ).hexdigest()

            result = self.run_set_state(
                state,
                "wg1",
                "certification-failure",
                "--controlled-certification",
                "--certification-users",
                "10.7.0.3",
                "--certification-group",
                "n10",
                "--reservation-id",
                "n10-r1",
                "--expected-egress-fingerprint",
                fingerprint,
            )

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("certification_failure_user_scope_changed", result.stdout)
            self.assertEqual(
                (state / "egress.registry").read_text(encoding="utf-8"),
                original,
            )

    def test_telegram_failure_and_recovery_are_exact_and_leave_no_rule_residue(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=wg1 protocol=wireguard type=interface interface=wg1 "
                "enabled=1 role=EXECUTION_ONLY config=/tmp/wg1.conf "
                "controlled_certification_source=1 "
                "reservation_owner=operator_execution_governance "
                "certification_group=n10 controlled_source_reservation_id=n10-r1 "
                "controlled_source_reservation_expires_at=2099-01-01T00:00:00+00:00\n"
            )
            state = self.write_state(
                Path(tmp),
                original,
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 "
                "certification_user=1 certification_group=n10\n",
            )
            fingerprint = hashlib.sha256(original.rstrip("\n").encode()).hexdigest()
            inject = self.run_set_state(
                state,
                "wg1",
                "certification-telegram-failure",
                "--controlled-certification",
                "--certification-users",
                "10.7.0.2",
                "--certification-group",
                "n10",
                "--reservation-id",
                "n10-r1",
                "--expected-egress-fingerprint",
                fingerprint,
                "--apply",
                "--confirm",
                "INJECT_CONTROLLED_CERTIFICATION_TELEGRAM_FAILURE",
            )
            self.assertEqual(inject.returncode, 0, inject.stdout + inject.stderr)
            self.assertIn("ACTION=controlled_certification_telegram_failure_injected", inject.stdout)
            self.assertIn("telegram_table=v7_ct_telegram_wg1", inject.stdout)
            nft_state = (state / "nft.table").read_text(encoding="utf-8")
            self.assertIn('oifname "wg1"', nft_state)
            self.assertIn("149.154.167.50", nft_state)
            self.assertEqual((state / "egress.registry").read_text(encoding="utf-8"), original)

            # The automatic path can move the one certification identity
            # before cleanup.  That empty source is the only additional
            # recovery state accepted by the existing state owner.
            (state / "users.registry").write_text(
                "ip=10.7.0.2 current=awg3 table=100 enabled=1 "
                "certification_user=1 certification_group=n10\n",
                encoding="utf-8",
            )
            recover = self.run_set_state(
                state,
                "wg1",
                "certification-telegram-recovery",
                "--controlled-certification",
                "--certification-users",
                "10.7.0.2",
                "--certification-group",
                "n10",
                "--reservation-id",
                "n10-r1",
                "--expected-egress-fingerprint",
                fingerprint,
                "--apply",
                "--confirm",
                "RECOVER_CONTROLLED_CERTIFICATION_TELEGRAM_FAILURE",
            )
            self.assertEqual(recover.returncode, 0, recover.stdout + recover.stderr)
            self.assertIn("ACTION=controlled_certification_telegram_failure_recovered", recover.stdout)
            self.assertFalse((state / "nft.table").exists())

    def test_telegram_failure_rejects_any_non_certification_source_member(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=wg1 protocol=wireguard type=interface interface=wg1 "
                "enabled=1 role=EXECUTION_ONLY config=/tmp/wg1.conf "
                "controlled_certification_source=1 "
                "reservation_owner=operator_execution_governance "
                "certification_group=n10 controlled_source_reservation_id=n10-r1 "
                "controlled_source_reservation_expires_at=2099-01-01T00:00:00+00:00\n"
            )
            state = self.write_state(
                Path(tmp),
                original,
                "ip=10.7.0.2 current=wg1 table=100 enabled=1 certification_user=1 certification_group=n10\n"
                "ip=10.7.0.3 current=wg1 table=101 enabled=1\n",
            )
            fingerprint = hashlib.sha256(original.rstrip("\n").encode()).hexdigest()
            result = self.run_set_state(
                state,
                "wg1",
                "certification-telegram-failure",
                "--controlled-certification",
                "--certification-users",
                "10.7.0.2",
                "--certification-group",
                "n10",
                "--reservation-id",
                "n10-r1",
                "--expected-egress-fingerprint",
                fingerprint,
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("reason=non_certification_users_assigned", result.stdout)
            self.assertFalse((state / "nft.table").exists())

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

    def test_controlled_source_release_to_verified_base_requires_exact_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=vless protocol=vless type=interface interface=tun0 enabled=1 "
                "role=EXECUTION_ONLY route_table=1250 manual_only=1 reserve_only=1 "
                "canary_reserved=true execution_reserved=true "
                "reservation_owner=operator_execution_governance "
                "autoswitch_allowed=false rebalance_allowed=false "
                "production_assignment_allowed=false service_tags=governance "
                "exclude_route_classes=DIRECT_RU\n"
            )
            state = self.write_state(Path(tmp), original, "")
            fingerprint = hashlib.sha256(original.rstrip("\n").encode()).hexdigest()
            reserve = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--reservation-id",
                "csr_chain_1",
                "--reservation-expires-at",
                "2099-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                fingerprint,
                "--certification-group",
                "telegram-test",
                "--apply",
                "--confirm",
                "RESERVE_CONTROLLED_CERTIFICATION_SOURCE",
            )
            self.assertEqual(reserve.returncode, 0, reserve.stdout + reserve.stderr)
            reserved_fingerprint = next(
                line.split("=", 1)[1]
                for line in reserve.stdout.splitlines()
                if line.startswith("reserved_egress_fingerprint=")
            )
            base_backup = state / "egress.registry.backup.v7-egress-set-state.base"
            base_backup.write_text(original, encoding="utf-8")

            missing_mode = self.run_set_state(
                state,
                "vless",
                "certification-release",
                "--reservation-id",
                "csr_chain_1",
                "--expected-egress-fingerprint",
                reserved_fingerprint,
                "--restore-backup",
                str(base_backup),
            )
            self.assertEqual(missing_mode.returncode, 1, missing_mode.stdout)
            self.assertIn("base restore requires --release-to-base", missing_mode.stdout)

            wrong_group = self.run_set_state(
                state,
                "vless",
                "certification-release",
                "--reservation-id",
                "csr_chain_1",
                "--expected-egress-fingerprint",
                reserved_fingerprint,
                "--restore-backup",
                str(base_backup),
                "--release-to-base",
                "--certification-group",
                "other-campaign",
            )
            self.assertEqual(wrong_group.returncode, 2, wrong_group.stdout)
            self.assertIn(
                "controlled_source_base_release_group_not_exact", wrong_group.stdout
            )

            release = self.run_set_state(
                state,
                "vless",
                "certification-release",
                "--reservation-id",
                "csr_chain_1",
                "--expected-egress-fingerprint",
                reserved_fingerprint,
                "--restore-backup",
                str(base_backup),
                "--release-to-base",
                "--certification-group",
                "telegram-test",
                "--apply",
                "--confirm",
                "RELEASE_CONTROLLED_CERTIFICATION_SOURCE_TO_BASE",
            )
            self.assertEqual(release.returncode, 0, release.stdout + release.stderr)
            self.assertIn("release_mode=base_restore", release.stdout)
            self.assertEqual(
                (state / "egress.registry").read_text(encoding="utf-8"),
                original,
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
                "controlled_source_reservation_requires_empty_or_same_campaign_certification_source",
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

    def test_controlled_source_reserve_renews_same_campaign_certification_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = (
                "id=vless protocol=vless type=interface interface=tun0 "
                "enabled=1 controlled_certification_source=1 "
                "reservation_owner=operator_execution_governance "
                "certification_group=old-group\n"
            )
            state = self.write_state(
                Path(tmp),
                original,
                (
                    "ip=10.7.0.100 current=vless enabled=1 "
                    "certification_user=1 certification_group=t48\n"
                ),
            )
            fingerprint = hashlib.sha256(
                original.rstrip("\n").encode()
            ).hexdigest()

            renewed = self.run_set_state(
                state,
                "vless",
                "certification-reserve",
                "--certification-group",
                "t48",
                "--reservation-id",
                "csr_renewed",
                "--reservation-expires-at",
                "2099-01-01T00:00:00+00:00",
                "--expected-egress-fingerprint",
                fingerprint,
                "--apply",
                "--confirm",
                "RESERVE_CONTROLLED_CERTIFICATION_SOURCE",
            )

            self.assertEqual(
                renewed.returncode,
                0,
                renewed.stdout + renewed.stderr,
            )
            self.assertIn("ACTION=controlled_source_reserved", renewed.stdout)
            self.assertIn("same_campaign_continuation=1", renewed.stdout)
            self.assertIn(
                "certification_group=t48",
                (state / "egress.registry").read_text(encoding="utf-8"),
            )

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
