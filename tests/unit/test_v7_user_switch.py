import os
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "runtime-support" / "v7-user-switch"


class V7UserSwitchCircuitBreakerTest(unittest.TestCase):
    def fixture(self, root: Path):
        state = root / "state"
        state.mkdir()
        (state / "users.registry").write_text("ip=10.7.0.2 current=1 table=100 enabled=1\n", encoding="utf-8")
        lib = root / "v7-egress-lib"
        lib.write_text(
            "v7_safe_ip(){ return 0; }\n"
            "v7_safe_id(){ return 0; }\n"
            "v7_kv_get(){ printf '%s\\n' \"$1\" | tr ' ' '\\n' | awk -F= -v k=\"$2\" '$1==k{print $2;exit}'; }\n"
            "v7_egress_exists(){ return 0; }\n"
            "v7_egress_enabled(){ return 0; }\n"
            "v7_egress_interface(){ printf 'tun0\\n'; }\n",
            encoding="utf-8",
        )
        bindir = root / "bin"
        bindir.mkdir()
        ip_log = root / "ip.log"
        ip = bindir / "ip"
        ip.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> '{ip_log}'\n", encoding="utf-8")
        ip.chmod(0o755)
        validator = bindir / "v7-operator-execution-packet"
        validator.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        validator.chmod(0o755)
        env = os.environ.copy()
        env.update({
            "PATH": f"{bindir}:{env.get('PATH', '')}",
            "V7_LOCKED_USER_SWITCH": "1",
            "V7_STATE_DIR": str(state),
            "V7_USERS_REGISTRY": str(state / "users.registry"),
            "V7_EGRESS_LIB": str(lib),
        })
        return env, ip_log

    def test_direct_invocation_denies_before_route_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            env, ip_log = self.fixture(Path(tmp))
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8") if ip_log.exists() else ""
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("route replace", calls)

    def test_owner_context_reaches_route_replace_after_validator_allows(self):
        with tempfile.TemporaryDirectory() as tmp:
            env, ip_log = self.fixture(Path(tmp))
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("route replace default dev tun0 table 100", calls)
        self.assertIn("rule add pref 100 from 10.7.0.2 table 100", calls)

    def test_exact_parent_control_hash_skips_duplicate_python_validator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            control = root / "safe-mode.json"
            control.write_text(json.dumps({
                "state": "CLOSED",
                "scope": "operation",
                "generation": "aec_test",
                "operation_id": "op-test",
                "action_class": "USER_SWITCH",
                "selected_move_hash": "move-test",
                "source_bundle_hash": "source-test",
                "snapshot_bundle_hash": "snapshot-test",
                "max_users": 1,
            }) + "\n", encoding="utf-8")
            validator = root / "bin" / "v7-operator-execution-packet"
            validator.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
            validator.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
                "V7_ADMIN_SAFE_MODE_FILE": str(control),
                "V7_EXECUTION_CONTROL_FILE_HASH": hashlib.sha256(
                    control.read_bytes()
                ).hexdigest(),
            })
            result = subprocess.run(
                [str(SCRIPT), "10.7.0.2", "vless"],
                env=env,
                text=True,
                capture_output=True,
            )
            calls = ip_log.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("route replace default dev tun0 table 100", calls)

    def test_exact_n10_cohort_control_allows_only_its_bounded_member_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            control = root / "safe-mode.json"
            control.write_text(json.dumps({
                "state": "CLOSED", "scope": "operation", "generation": "aec_n10",
                "operation_id": "op-n10", "action_class": "N10_SMALL_COHORT",
                "selected_move_hash": "move-n10", "source_bundle_hash": "source-n10",
                "snapshot_bundle_hash": "snapshot-n10", "max_users": 2,
            }) + "\n", encoding="utf-8")
            validator = root / "bin" / "v7-operator-execution-packet"
            validator.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
            validator.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_n10",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-n10",
                "V7_EXECUTION_ACTION_CLASS": "N10_SMALL_COHORT",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-n10",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-n10",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-n10",
                "V7_EXECUTION_MAX_USERS": "2",
                "V7_ADMIN_SAFE_MODE_FILE": str(control),
                "V7_EXECUTION_CONTROL_FILE_HASH": hashlib.sha256(control.read_bytes()).hexdigest(),
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("route replace default dev tun0 table 100", calls)

    def test_exact_emergency_failover_cohort_control_allows_its_bounded_member_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            control = root / "safe-mode.json"
            control.write_text(json.dumps({
                "state": "CLOSED", "scope": "operation", "generation": "aec_failover",
                "operation_id": "op-failover", "action_class": "EMERGENCY_FAILOVER",
                "selected_move_hash": "move-failover", "source_bundle_hash": "source-failover",
                "snapshot_bundle_hash": "snapshot-failover", "max_users": 3,
            }) + "\n", encoding="utf-8")
            validator = root / "bin" / "v7-operator-execution-packet"
            validator.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
            validator.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_failover",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-failover",
                "V7_EXECUTION_ACTION_CLASS": "EMERGENCY_FAILOVER",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-failover",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-failover",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-failover",
                "V7_EXECUTION_MAX_USERS": "3",
                "V7_ADMIN_SAFE_MODE_FILE": str(control),
                "V7_EXECUTION_CONTROL_FILE_HASH": hashlib.sha256(control.read_bytes()).hexdigest(),
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("route replace default dev tun0 table 100", calls)

    def test_non_failover_multi_user_context_is_denied_before_route_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            env, ip_log = self.fixture(Path(tmp))
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "2",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8") if ip_log.exists() else ""

        self.assertEqual(result.returncode, 2)
        self.assertIn("max users outside exact action scope", result.stdout)
        self.assertNotIn("route replace", calls)

    def test_changed_parent_control_hash_falls_back_and_denies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            control = root / "safe-mode.json"
            control.write_text('{"generation":"changed"}\n', encoding="utf-8")
            validator = root / "bin" / "v7-operator-execution-packet"
            validator.write_text("#!/bin/sh\nexit 2\n", encoding="utf-8")
            validator.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
                "V7_ADMIN_SAFE_MODE_FILE": str(control),
                "V7_EXECUTION_CONTROL_FILE_HASH": "0" * 64,
            })
            result = subprocess.run(
                [str(SCRIPT), "10.7.0.2", "vless"],
                env=env,
                text=True,
                capture_output=True,
            )
            calls = (
                ip_log.read_text(encoding="utf-8") if ip_log.exists() else ""
            )

        self.assertEqual(result.returncode, 2)
        self.assertNotIn("route replace", calls)

    def test_existing_exact_policy_rule_is_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            ip = root / "bin" / "ip"
            ip.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> '{ip_log}'\n"
                "if [ \"$*\" = \"-4 rule show\" ]; then "
                "printf '100: from 10.7.0.2 lookup 100\\n'; fi\n",
                encoding="utf-8",
            )
            ip.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })
            result = subprocess.run(
                [str(SCRIPT), "10.7.0.2", "vless"],
                env=env,
                text=True,
                capture_output=True,
            )
            calls = ip_log.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("rule add", calls)

    def test_policy_rule_failure_restores_previous_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            lib = root / "v7-egress-lib"
            lib.write_text(
                lib.read_text(encoding="utf-8").replace(
                    "v7_egress_interface(){ printf 'tun0\\n'; }",
                    "v7_egress_interface(){ if [ \"$1\" = \"1\" ]; then printf 'old0\\n'; else printf 'tun0\\n'; fi; }",
                ),
                encoding="utf-8",
            )
            ip = root / "bin" / "ip"
            ip.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> '{ip_log}'\n"
                "if [ \"$1 $2\" = \"rule add\" ]; then exit 2; fi\n",
                encoding="utf-8",
            )
            ip.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })
            result = subprocess.run(
                [str(SCRIPT), "10.7.0.2", "vless"],
                env=env,
                text=True,
                capture_output=True,
            )
            calls = ip_log.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "V7_ROUTE_WRITE_FAILURE=ROUTE_POLICY_RULE_WRITE_FAILED_ROUTE_RESTORED",
            result.stdout,
        )
        self.assertIn("route replace default dev tun0 table 100", calls)
        self.assertIn("route replace default dev old0 table 100", calls)

    def test_route_write_failure_is_safe_and_classified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, _ip_log = self.fixture(root)
            failing_ip = root / "bin" / "ip"
            failing_ip.write_text(
                "#!/bin/sh\necho 'Cannot find device \"tun0\"' >&2\nexit 2\n",
                encoding="utf-8",
            )
            failing_ip.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)

        self.assertEqual(result.returncode, 1)
        self.assertIn("V7_ROUTE_WRITE_FAILURE=ROUTE_INTERFACE_UNAVAILABLE", result.stdout)
        self.assertNotIn("Cannot find device", result.stdout)

    def test_missing_egress_interface_is_safe_and_classified_before_route_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            lib = root / "v7-egress-lib"
            lib.write_text(
                lib.read_text(encoding="utf-8").replace(
                    "v7_egress_interface(){ printf 'tun0\\n'; }",
                    "v7_egress_interface(){ return 0; }",
                ),
                encoding="utf-8",
            )
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8") if ip_log.exists() else ""

        self.assertEqual(result.returncode, 1)
        self.assertIn("V7_ROUTE_WRITE_FAILURE=ROUTE_EGRESS_INTERFACE_MISSING", result.stdout)
        self.assertNotIn("route replace", calls)

    def test_post_apply_route_observation_failure_is_safe_and_classified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, ip_log = self.fixture(root)
            ip = root / "bin" / "ip"
            ip.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> '{ip_log}'\n"
                "if [ \"$1 $2\" = \"route get\" ]; then exit 3; fi\n",
                encoding="utf-8",
            )
            ip.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 1)
        self.assertIn("V7_ROUTE_WRITE_FAILURE=ROUTE_POST_APPLY_OBSERVATION_FAILED", result.stdout)
        self.assertIn("route replace default dev tun0 table 100", calls)

    def test_owner_switch_preserves_certification_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, _ip_log = self.fixture(root)
            registry = root / "state" / "users.registry"
            registry.write_text(
                "ip=10.7.0.2 current=1 table=100 enabled=1 certification_user=1 certification_group=polygon-l7-canary\n",
                encoding="utf-8",
            )
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })

            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            row = registry.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("current=vless", row)
        self.assertIn("certification_user=1", row)
        self.assertIn("certification_group=polygon-l7-canary", row)

    def test_core_primary_contract_rebuilds_current_membership_after_registry_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, _ip_log = self.fixture(root)
            sync_log = root / "sync.log"
            sync = root / "bin" / "v7-routing-sync"
            sync.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> '{sync_log}'\n"
                "if [ \"$1\" = \"--core-primary-active\" ]; then\n"
                "  printf '{\\\"status\\\": \\\"CORE_PRIMARY_ACTIVE\\\"}\\n'\n"
                "  exit 0\n"
                "fi\n"
                "if [ \"$1\" = \"--core-primary-apply\" ]; then\n"
                "  printf '{\\\"status\\\": \\\"CORE_PRIMARY_APPLY_PASS\\\"}\\n'\n"
                "  exit 0\n"
                "fi\n"
                "exit 2\n",
                encoding="utf-8",
            )
            sync.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = sync_log.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("--core-primary-active --json", calls)
        self.assertIn("--core-primary-apply --json", calls)
        self.assertIn("V7_CORE_PRIMARY_SYNC=PASS", result.stdout)

    def test_exact_n10_cohort_member_stages_without_global_core_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, _ip_log = self.fixture(root)
            sync_log = root / "sync.log"
            sync = root / "bin" / "v7-routing-sync"
            sync.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> '{sync_log}'\n"
                "if [ \"$1\" = \"--core-primary-active\" ]; then\n"
                "  printf '{\\\"status\\\": \\\"CORE_PRIMARY_ACTIVE\\\"}\\n'\n"
                "  exit 0\n"
                "fi\n"
                "exit 97\n",
                encoding="utf-8",
            )
            sync.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_n10",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-n10",
                "V7_EXECUTION_ACTION_CLASS": "N10_SMALL_COHORT",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-n10",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-n10",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-n10",
                "V7_EXECUTION_MAX_USERS": "2",
                "V7_CORE_PRIMARY_COHORT_DEFER": "1",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = sync_log.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("V7_CORE_PRIMARY_SYNC=DEFERRED_COHORT", result.stdout)
        self.assertIn("--core-primary-active --json", calls)
        self.assertNotIn("--core-primary-apply", calls)

    def test_core_primary_sync_failure_is_returned_to_the_existing_caller(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, _ip_log = self.fixture(root)
            sync = root / "bin" / "v7-routing-sync"
            sync.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = \"--core-primary-active\" ]; then\n"
                "  printf '{\\\"status\\\": \\\"CORE_PRIMARY_ACTIVE\\\"}\\n'; exit 0\n"
                "fi\n"
                "printf '{\\\"status\\\": \\\"STOP_SAFE\\\"}\\n'; exit 2\n",
                encoding="utf-8",
            )
            sync.chmod(0o755)
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "forward",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
                "V7_EXECUTION_SELECTED_MOVE_HASH": "move-test",
                "V7_EXECUTION_SOURCE_BUNDLE_HASH": "source-test",
                "V7_EXECUTION_SNAPSHOT_BUNDLE_HASH": "snapshot-test",
                "V7_EXECUTION_MAX_USERS": "1",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            registry = (root / "state" / "users.registry").read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 1)
        self.assertIn("V7_ROUTE_WRITE_FAILURE=ROUTE_CORE_PRIMARY_SYNC_FAILED_ROLLBACK_FAILED", result.stdout)
        self.assertIn("current=1", registry)

    def test_uncertified_rollback_context_is_denied_before_validator_and_ip(self):
        with tempfile.TemporaryDirectory() as tmp:
            env, ip_log = self.fixture(Path(tmp))
            env.update({
                "V7_EXECUTION_CONTROL_GENERATION": "aec_test",
                "V7_EXECUTION_MUTATION_KIND": "rollback",
                "V7_EXECUTION_OPERATION_ID": "op-test",
                "V7_EXECUTION_ACTION_CLASS": "USER_SWITCH",
            })
            result = subprocess.run([str(SCRIPT), "10.7.0.2", "vless"], env=env, text=True, capture_output=True)
            calls = ip_log.read_text(encoding="utf-8") if ip_log.exists() else ""
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("route replace", calls)


if __name__ == "__main__":
    unittest.main()
