import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/runtime-support/v7-user-desired-state"
SAVE_SCRIPT = ROOT / "tools/runtime-support/v7-user-desired-state-save"


class V7UserDesiredStateTest(unittest.TestCase):
    def run_checker(self, *, rules_present, route_matches, core_verify_status=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            state_dir = root / "state"
            bin_dir.mkdir()
            state_dir.mkdir()
            registry = state_dir / "users.registry"
            registry.write_text(
                "ip=10.0.0.2 current=sample table=100 enabled=1\n"
                "ip=10.0.0.3 current=sample table=101 enabled=1\n",
                encoding="utf-8",
            )
            wg_conf = root / "wg0.conf"
            wg_conf.write_text(
                "[Peer]\nAllowedIPs = 10.0.0.2/32\n[Peer]\nAllowedIPs = 10.0.0.3/32\n",
                encoding="utf-8",
            )
            library = root / "v7-egress-lib"
            library.write_text(
                "v7_kv_get() { local line=$1 key=$2 part; for part in $line; do case $part in \"$key\"=*) printf '%s\\n' \"${part#*=}\"; return 0;; esac; done; }\n"
                "v7_safe_ip() { [[ $1 =~ ^10\\.0\\.0\\.[0-9]+$ ]]; }\n"
                "v7_egress_interface() { printf 'egress0\\n'; }\n",
                encoding="utf-8",
            )
            rules_command = (
                "printf '100: from 10.0.0.2 lookup 100\\n101: from 10.0.0.3 lookup 101\\n'"
                if rules_present else ":"
            )
            route_dev = "egress0" if route_matches else "other0"
            (bin_dir / "wg").write_text(
                "#!/usr/bin/env bash\nprintf 'key 10.0.0.2/32\\nkey 10.0.0.3/32\\n'\n",
                encoding="utf-8",
            )
            (bin_dir / "date").write_text(
                "#!/usr/bin/env bash\nprintf '2026-08-14T12:00:00+03:00\\n'\n",
                encoding="utf-8",
            )
            (bin_dir / "ip").write_text(
                "#!/usr/bin/env bash\n"
                "if [ \"$1 $2 $3\" = \"-4 rule show\" ]; then\n"
                f"  {rules_command}\n"
                "elif [ \"$1 $2 $3\" = \"-4 route show\" ]; then\n"
                "  printf 'default dev egress0\\n'\n"
                "elif [ \"$1 $2 $3\" = \"route get 8.8.8.8\" ]; then\n"
                f"  printf '8.8.8.8 dev {route_dev}\\n'\n"
                "fi\n",
                encoding="utf-8",
            )
            if core_verify_status is not None:
                (bin_dir / "v7-routing-sync").write_text(
                    "#!/usr/bin/env bash\n"
                    "printf '%s\\n' '"
                    + json.dumps({
                        "status": core_verify_status,
                        "legacy_primary_rules_present": False,
                    })
                    + "'\n",
                    encoding="utf-8",
                )
            for command in (bin_dir / "wg", bin_dir / "ip", bin_dir / "date", bin_dir / "v7-routing-sync"):
                if not command.exists():
                    continue
                command.chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{bin_dir}:{os.environ['PATH']}",
                "V7_STATE_DIR": str(state_dir),
                "V7_USERS_REGISTRY": str(registry),
                "V7_WG_CONF": str(wg_conf),
                "V7_WG_IF": "wg0",
                "V7_EGRESS_LIB": str(library),
            }
            return subprocess.run(
                ["bash", str(SCRIPT)], env=env, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )

    def test_repeated_warnings_finish_with_terminal_warn(self):
        result = self.run_checker(rules_present=True, route_matches=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("status=WARN"), 2)
        self.assertIn("V7_USER_DESIRED_STATE=WARN", result.stdout)

    def test_fail_is_never_lowered_to_warn(self):
        result = self.run_checker(rules_present=False, route_matches=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout.count("status=FAIL"), 2)
        self.assertIn("V7_USER_DESIRED_STATE=FAIL", result.stdout)

    def test_core_primary_validation_does_not_require_retired_per_user_rules(self):
        result = self.run_checker(
            rules_present=False,
            route_matches=False,
            core_verify_status="CORE_PRIMARY_VERIFY_PASS",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("routing_mode=CORE_PRIMARY_CLASS_ROUTING", result.stdout)
        self.assertIn("core_verify_status=CORE_PRIMARY_VERIFY_PASS", result.stdout)
        self.assertNotIn("ip_rule_missing", result.stdout)
        self.assertIn("V7_USER_DESIRED_STATE=OK", result.stdout)

    def test_unverified_core_fails_closed_without_legacy_assumption(self):
        result = self.run_checker(
            rules_present=False,
            route_matches=False,
            core_verify_status="STOP_SAFE",
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("routing_mode=CORE_PRIMARY_UNVERIFIED", result.stdout)
        self.assertIn("core_primary_unverified", result.stdout)
        self.assertIn("V7_USER_DESIRED_STATE=FAIL", result.stdout)

    def test_saver_persists_terminal_fail_and_preserves_failure_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            state_dir = root / "state"
            bin_dir.mkdir()
            state_dir.mkdir()
            (bin_dir / "v7-user-desired-state").write_text(
                "#!/usr/bin/env bash\n"
                "printf 'subject=10.0.0.2 status=FAIL reason=missing_rule\\n'\n"
                "printf 'V7_USER_DESIRED_STATE=FAIL\\n'\n"
                "exit 1\n",
                encoding="utf-8",
            )
            (bin_dir / "v7-user-desired-state").chmod(0o755)
            output_file = state_dir / "user-desired-state.state"
            result = subprocess.run(
                ["bash", str(SAVE_SCRIPT)],
                env={
                    **os.environ,
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "V7_STATE_DIR": str(state_dir),
                    "V7_USER_DESIRED_STATE_FILE": str(output_file),
                },
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("V7_USER_DESIRED_STATE_SAVE=OK", result.stdout)
            self.assertTrue(output_file.exists())
            self.assertIn("V7_USER_DESIRED_STATE=FAIL", output_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
