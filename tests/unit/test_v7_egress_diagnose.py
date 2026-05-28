import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-egress-diagnose"


class V7EgressDiagnoseTest(unittest.TestCase):
    def write_command(self, bin_dir: Path, name: str, body: str) -> None:
        path = bin_dir / name
        path.write_text("#!/usr/bin/env bash\n" + body, encoding="utf-8")
        path.chmod(0o755)

    def run_tool(self, state: Path, bin_dir: Path) -> str:
        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        proc = subprocess.run(
            [str(TOOL), "--state-dir", str(state)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return (state / "egress-diagnose.state").read_text(encoding="utf-8")

    def base_state(self, root: Path, registry: str) -> Path:
        state = root / "state"
        state.mkdir()
        (state / "egress.registry").write_text(registry, encoding="utf-8")
        (state / "summary.state").write_text("", encoding="utf-8")
        return state

    def test_wireguard_uses_wg_not_awg(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(
                root,
                "id=wireguard-1779454504-c43409 protocol=wireguard interface=v7wg enabled=1\n",
            )
            now = int(time.time())
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", f"echo 'peerkey {now - 9}'\n")
            self.write_command(bin_dir, "awg", "echo 'awg should not be called' >&2\nexit 42\n")

            out = self.run_tool(state, bin_dir)

            self.assertIn("wireguard-1779454504-c43409_diagnose_severity=OK", out)
            self.assertIn("wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=", out)

    def test_awg_uses_awg_not_wg(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=awg0 protocol=amneziawg interface=awg0 enabled=1\n")
            self.write_command(bin_dir, "ip", "echo '1: awg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir,
                "awg",
                "cat <<'EOF'\npeer: p\n  latest handshake: 12 seconds ago\nEOF\n",
            )
            self.write_command(bin_dir, "wg", "echo 'wg should not be called' >&2\nexit 42\n")

            out = self.run_tool(state, bin_dir)

            self.assertIn("awg0_diagnose_severity=OK", out)
            self.assertIn("awg0_diagnose_detail=handshake_age_seconds=12", out)

    def test_fresh_wireguard_handshake_clears_stale_suspect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgfast protocol=wireguard interface=v7wg enabled=1\n")
            (state / "egress-diagnose.state").write_text(
                "wgfast_diagnose_severity=SUSPECT\nwgfast_diagnose_detail=handshake_age_seconds=999999\n",
                encoding="utf-8",
            )
            now = int(time.time())
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", f"echo 'peerkey {now - 3}'\n")
            self.write_command(bin_dir, "awg", "exit 42\n")

            out = self.run_tool(state, bin_dir)

            self.assertIn("wgfast_diagnose_severity=OK", out)
            self.assertNotIn("SUSPECT", out)

    def test_missing_handshake_and_failed_curl_is_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgfail protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgfail_code=000\n", encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")

            out = self.run_tool(state, bin_dir)

            self.assertIn("wgfail_diagnose_severity=FAIL", out)
            self.assertIn("wgfail_diagnose_reason=curl_failed_and_handshake_stale", out)

    def test_missing_wireguard_handshake_with_curl_ok_is_warn(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgidle protocol=wireguard interface=v7wg enabled=1\n")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")

            out = self.run_tool(state, bin_dir)

            self.assertIn("wgidle_diagnose_severity=WARN", out)
            self.assertIn("wgidle_diagnose_reason=curl_ok_but_wireguard_handshake_unavailable", out)

    def test_unknown_protocol_is_not_false_stale_handshake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=mystery protocol=mysteryvpn interface=m0 enabled=1\n")
            self.write_command(bin_dir, "ip", "echo '1: m0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 42\n")
            self.write_command(bin_dir, "awg", "exit 42\n")

            out = self.run_tool(state, bin_dir)

            self.assertIn("mystery_diagnose_severity=SUSPECT", out)
            self.assertIn("mystery_diagnose_reason=handshake_unsupported_for_protocol_mysteryvpn", out)
            self.assertNotIn("curl_ok_but_handshake_stale", out)

    def test_interface_down_is_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgdown protocol=wireguard interface=v7wg enabled=1\n")
            self.write_command(bin_dir, "ip", "exit 1\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")

            out = self.run_tool(state, bin_dir)

            self.assertIn("wgdown_diagnose_severity=FAIL", out)
            self.assertIn("wgdown_diagnose_reason=interface_down_or_missing", out)


if __name__ == "__main__":
    unittest.main()
