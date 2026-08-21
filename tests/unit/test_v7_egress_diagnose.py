import os
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-egress-diagnose"


class V7EgressDiagnoseTest(unittest.TestCase):
    def write_command(self, bin_dir: Path, name: str, body: str) -> None:
        path = bin_dir / name
        path.write_text("#!/usr/bin/env bash\n" + body, encoding="utf-8")
        path.chmod(0o755)

    def run_tool(self, state: Path, bin_dir: Path, extra_args: Optional[list[str]] = None) -> str:
        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        args = [str(TOOL), "--state-dir", str(state)] + list(extra_args or [])
        proc = subprocess.run(
            args,
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

    def test_current_source_suspicion_calls_existing_matrix_receiver_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgpath protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgpath_code=000\n", encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            receiver_log = root / "receiver.args"
            self.write_command(
                bin_dir,
                "shadow-receiver",
                "printf '%s\\n' \"$*\" > \"$RECEIVER_LOG\"\nexit 0\n",
            )
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            proc = subprocess.run(
                [
                    str(TOOL), "--state-dir", str(state),
                    "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                    "--shadow-trigger-egress", "wgpath",
                    "--shadow-trigger-services", "google,telegram",
                    "--shadow-trigger-event-dir", str(root / "events"),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            args = receiver_log.read_text(encoding="utf-8")
            self.assertIn("wgpath_shadow_trigger_status=PASS", out)
            self.assertIn("wgpath_shadow_trigger_class=TUNNEL_UP_INTERNET_DEAD", out)
            self.assertIn("--egresses wgpath", args)
            self.assertIn("--services google,telegram", args)
            self.assertIn("--shadow-trigger-source wgpath", args)
            self.assertIn("--matrix-observation-only", args)

    def test_current_source_suspicion_duplicate_is_suppressed_during_cooldown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgpath protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgpath_code=000\n", encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            receiver_log = root / "receiver.args"
            self.write_command(bin_dir, "shadow-receiver", "printf '%s\\n' \"$*\" >> \"$RECEIVER_LOG\"\nexit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            args = [
                str(TOOL), "--state-dir", str(state),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--shadow-trigger-egress", "wgpath",
                "--shadow-trigger-services", "google,telegram",
                "--shadow-trigger-event-dir", str(root / "events"),
                "--shadow-trigger-cooldown-sec", "600",
            ]
            first = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            second = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            out = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("wgpath_shadow_trigger_status=SUPPRESSED_COOLDOWN", out)
            self.assertEqual(len(receiver_log.read_text(encoding="utf-8").splitlines()), 1)

    def test_current_source_suspicion_reaches_real_matrix_writer_in_polygon(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgpath protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgpath_code=000\n", encoding="utf-8")
            ip_count = root / "ip.count"
            self.write_command(
                bin_dir,
                "ip",
                "count=$(cat \"$IP_COUNT\" 2>/dev/null || echo 0); count=$((count + 1)); "
                "echo \"$count\" > \"$IP_COUNT\"; "
                "if [ \"$count\" -eq 1 ]; then echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'; else exit 1; fi\n",
            )
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["IP_COUNT"] = str(ip_count)
            proc = subprocess.run(
                [
                    str(TOOL), "--state-dir", str(state),
                    "--shadow-trigger-command", str(ROOT / "tools" / "v7-service-matrix-refresh-all"),
                    "--shadow-trigger-egress", "wgpath",
                    "--shadow-trigger-services", "google,telegram",
                    "--shadow-trigger-event-dir", str(root / "events"),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            diagnose = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("wgpath_shadow_trigger_status=PASS", diagnose)
            matrix = json.loads((state / "service-matrix.json").read_text(encoding="utf-8"))
            services = matrix["items"]["wgpath"]["services"]
            self.assertEqual(set(services), {"google", "telegram"})
            self.assertTrue(all(isinstance(row, dict) for row in services.values()))

    def test_current_source_suspicion_uses_existing_profile_service_subset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgprofile protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgprofile_code=000\n", encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {
                    "profile-a": {"services": ["telegram", "google"]},
                    "profile-b": {"services": ["youtube"]},
                }
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            receiver_log = root / "receiver.args"
            self.write_command(bin_dir, "shadow-receiver", "printf '%s\\n' \"$*\" > \"$RECEIVER_LOG\"\nexit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--shadow-trigger-egress", "wgprofile",
                "--shadow-trigger-profile-user", "profile-a",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            args = receiver_log.read_text(encoding="utf-8")
            self.assertIn("--shadow-trigger-profile-user profile-a", args)
            self.assertNotIn("--services", args)

    def test_profile_service_subset_requires_existing_nonempty_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.base_state(root, "id=wgprofile protocol=wireguard interface=v7wg enabled=1\n")
            (state / "service-preferences.json").write_text(json.dumps({"users": {"empty": {"services": []}}}), encoding="utf-8")
            proc = subprocess.run([
                str(ROOT / "tools" / "v7-service-matrix-refresh-all"),
                "--state-dir", str(state), "--egresses", "wgprofile",
                "--shadow-trigger-source", "wgprofile",
                "--shadow-trigger-class", "REQUIRED_SERVICE_FAILURE",
                "--shadow-trigger-id", "test-profile-empty",
                "--shadow-trigger-profile-user", "empty",
                "--matrix-observation-only",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("profile_service_subset_missing_or_empty", proc.stdout)

    def test_profile_service_subset_reaches_real_matrix_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgprofile protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgprofile_code=000\n", encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {"profile-a": {"services": ["telegram", "google"]}}
            }), encoding="utf-8")
            ip_count = root / "ip.count"
            self.write_command(bin_dir, "ip", "count=$(cat \"$IP_COUNT\" 2>/dev/null || echo 0); count=$((count + 1)); echo \"$count\" > \"$IP_COUNT\"; if [ \"$count\" -eq 1 ]; then echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'; else exit 1; fi\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["IP_COUNT"] = str(ip_count)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state),
                "--shadow-trigger-command", str(ROOT / "tools" / "v7-service-matrix-refresh-all"),
                "--shadow-trigger-egress", "wgprofile",
                "--shadow-trigger-profile-user", "profile-a",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            matrix = json.loads((state / "service-matrix.json").read_text(encoding="utf-8"))
            self.assertEqual(set(matrix["items"]["wgprofile"]["services"]), {"google", "telegram"})


if __name__ == "__main__":
    unittest.main()
