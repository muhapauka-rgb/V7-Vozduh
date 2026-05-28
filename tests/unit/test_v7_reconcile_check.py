import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "runtime-support" / "v7-reconcile-check"


class V7ReconcileCheckTest(unittest.TestCase):
    def run_checker(self, users_registry: str, rule_mode: str = "present_sigpipe"):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            state = tmp / "state"
            state.mkdir()
            fakebin = tmp / "bin"
            fakebin.mkdir()
            lib = tmp / "v7-egress-lib"

            (state / "users.registry").write_text(users_registry, encoding="utf-8")
            (state / "egress.registry").write_text(
                "id=vless enabled=1 interface=tun0\n",
                encoding="utf-8",
            )
            for ip in ("10.7.0.10", "10.7.0.11", "10.7.0.12"):
                (state / f"user-{ip}.assign").write_text("egress=vless\n", encoding="utf-8")

            lib.write_text(
                textwrap.dedent(
                    """\
                    v7_kv_get() {
                      local line="$1" key="$2" part
                      for part in $line; do
                        case "$part" in
                          "$key="*) printf '%s\\n' "${part#*=}"; return 0 ;;
                        esac
                      done
                      return 0
                    }
                    v7_safe_ip() {
                      case "$1" in
                        10.*.*.*) return 0 ;;
                        *) return 1 ;;
                      esac
                    }
                    v7_egress_exists() { [ "$1" = "vless" ]; }
                    v7_egress_enabled() { [ "$1" = "vless" ]; }
                    v7_egress_interface() {
                      [ "$1" = "vless" ] && printf '%s\\n' tun0
                    }
                    """
                ),
                encoding="utf-8",
            )

            (fakebin / "wg").write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env bash
                    if [ "$1" = "show" ] && [ "$3" = "allowed-ips" ]; then
                      printf 'peer-a 10.7.0.10/32\\n'
                      printf 'peer-b 10.7.0.11/32\\n'
                      printf 'peer-c 10.7.0.12/32\\n'
                    fi
                    """
                ),
                encoding="utf-8",
            )
            (fakebin / "date").write_text(
                "#!/usr/bin/env bash\nprintf '%s\\n' 2026-05-25T00:00:00+00:00\n",
                encoding="utf-8",
            )
            (fakebin / "ip").write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env bash
                    if [ "$1" = "link" ] && [ "$2" = "show" ]; then
                      exit 0
                    fi
                    if [ "$1" = "-4" ] && [ "$2" = "rule" ] && [ "$3" = "show" ]; then
                      printf '100: from 10.7.0.10 lookup 110\\n'
                      if [ "${FAKE_RULE_MODE:-present_sigpipe}" != "missing_second" ]; then
                        printf '111: from 10.7.0.11 lookup 111\\n'
                      fi
                      printf '32766: from all lookup main\\n'
                      if [ "${FAKE_RULE_MODE:-present_sigpipe}" = "present_sigpipe" ]; then
                        exit 141
                      fi
                      exit 0
                    fi
                    if [ "$1" = "route" ] && [ "$2" = "get" ]; then
                      from_ip=""
                      prev=""
                      for arg in "$@"; do
                        if [ "$prev" = "from" ]; then from_ip="$arg"; fi
                        prev="$arg"
                      done
                      case "$from_ip" in
                        10.7.0.10) printf '8.8.8.8 from 10.7.0.10 dev tun0 table 110\\n' ;;
                        10.7.0.11) printf '8.8.8.8 from 10.7.0.11 dev tun0 table 111\\n' ;;
                        10.7.0.12) printf '8.8.8.8 from 10.7.0.12 dev tun0 table 112\\n' ;;
                        *) printf '8.8.8.8 dev tun0\\n' ;;
                      esac
                      exit 0
                    fi
                    exit 1
                    """
                ),
                encoding="utf-8",
            )
            os.chmod(fakebin / "wg", 0o755)
            os.chmod(fakebin / "ip", 0o755)
            os.chmod(fakebin / "date", 0o755)

            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{fakebin}{os.pathsep}{env['PATH']}",
                    "V7_STATE_DIR": str(state),
                    "V7_EGRESS_LIB": str(lib),
                    "V7_WG_IF": "wg0",
                    "FAKE_RULE_MODE": rule_mode,
                }
            )
            return subprocess.run(
                ["bash", str(TOOL)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )

    def test_existing_rule_detected_when_ip_rule_show_exits_141(self):
        proc = self.run_checker(
            "ip=10.7.0.10 current=vless table=110 enabled=1\n"
            "ip=10.7.0.11 current=vless table=111 enabled=1\n",
            rule_mode="present_sigpipe",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("V7_RECONCILE_RESULT=OK", proc.stdout)
        self.assertNotIn("missing ip rule", proc.stdout)

    def test_missing_rule_still_fails(self):
        proc = self.run_checker(
            "ip=10.7.0.10 current=vless table=110 enabled=1\n"
            "ip=10.7.0.11 current=vless table=111 enabled=1\n",
            rule_mode="missing_second",
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("ERROR: user=10.7.0.11 missing ip rule lookup table 111", proc.stdout)
        self.assertIn("V7_RECONCILE_RESULT=FAIL", proc.stdout)

    def test_disabled_users_are_skipped(self):
        proc = self.run_checker(
            "ip=10.7.0.12 current=vless table=112 enabled=0\n",
            rule_mode="missing_second",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("user=10.7.0.12 enabled=0 current=vless table=112", proc.stdout)
        self.assertNotIn("missing ip rule", proc.stdout)


if __name__ == "__main__":
    unittest.main()
