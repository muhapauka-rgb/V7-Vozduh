import os
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
