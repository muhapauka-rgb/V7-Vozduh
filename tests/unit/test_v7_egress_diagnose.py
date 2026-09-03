import os
import json
import shlex
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

    def test_missing_profile_uses_existing_default_priority_services(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=vless enabled=1\n")
            (state / "users.registry").write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            checker_args = root / "checker.args"
            self.write_command(bin_dir, "ip", "echo '1: vless: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir,
                "profile-checker",
                "printf '%s\\n' \"$*\" > \"$CHECKER_ARGS\"\n"
                "printf '%s\\n' '{\"status\":\"OK\",\"results\":{}}'\n",
            )
            output = root / "fast-observation.state"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["CHECKER_ARGS"] = str(checker_args)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only",
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "profile-checker"),
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = output.read_text(encoding="utf-8")
            self.assertIn("fast_producer_active_source_count=1", state_text)
            self.assertIn("fast_producer_distinct_contract_count=1", state_text)
            self.assertIn("fast_producer_observation_count=1", state_text)
            args = checker_args.read_text(encoding="utf-8")
            self.assertIn("vless all --services google,google_auth,instagram,telegram,youtube", args)

    def test_fresh_matrix_failure_unblocks_batch_budget_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(
                root,
                "id=vless protocol=vless interface=v7tun enabled=1\n",
            )
            (state / "users.registry").write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            (state / "service-preferences.json").write_text(
                json.dumps({"enabled": True, "users": {}}), encoding="utf-8"
            )
            observed = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
            (state / "service-matrix.json").write_text(
                json.dumps({"items": {"vless": {"services": {
                    "youtube": {
                        "status": "FAIL", "severity": "FAIL",
                        "failure_state": "OBSERVED_CONTINUING",
                        "source_incident_id": "sfinc-current",
                        "observed_at": observed,
                    }
                }}}}),
                encoding="utf-8",
            )
            self.write_command(
                bin_dir,
                "ip",
                "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n",
            )
            self.write_command(
                bin_dir,
                "batch-checker",
                "printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":1,\"contracts\":[{\"source\":\"vless\",\"profile\":\"__GLOBAL__\",\"services\":[\"youtube\"],\"state_key\":\"vless-profile\",\"failure_count\":0,\"blockers\":[\"fast_service_budget_exceeded\"]}]}'\n",
            )
            receiver_log = root / "receiver.args"
            self.write_command(
                bin_dir,
                "receiver",
                "printf '%s\\n' \"$*\" > \"$RECEIVER_LOG\"\n",
            )
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            proc = subprocess.run(
                [
                    str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                    "--fast-producer-only", "--lightweight-batch-producer",
                    "--profile-service-suspicion-command", str(bin_dir / "batch-checker"),
                    "--shadow-trigger-command", str(bin_dir / "receiver"),
                    "--profile-service-failure-samples", "1",
                    "--profile-service-cooldown-sec", "0",
                ],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                env=env, check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "fast.state").read_text(encoding="utf-8")
            self.assertIn("profile_matrix_failure_fallback=USED", state_text)
            self.assertIn("profile_trigger_status=PASS", state_text)
            self.assertTrue(receiver_log.exists())
            self.assertIn("--shadow-trigger-source vless", receiver_log.read_text(encoding="utf-8"))

    def test_fast_producer_reuses_fresh_matrix_before_waking_consumer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=v7tun enabled=1\n")
            (state / "users.registry").write_text("ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8")
            observed = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
            (state / "service-matrix.json").write_text(json.dumps({"items": {"vless": {"services": {"youtube": {
                "status": "FAIL", "severity": "FAIL", "failure_state": "OBSERVED_CONTINUING",
                "source_incident_id": "sfinc-current", "observed_at": observed,
            }}}}}), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "batch-checker", "printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":1,\"contracts\":[{\"source\":\"vless\",\"profile\":\"__GLOBAL__\",\"services\":[\"youtube\"],\"state_key\":\"vless-profile\",\"failure_count\":0,\"blockers\":[\"fast_service_budget_exceeded\"]}]}'\n")
            shadow_log = root / "shadow.args"
            wake_log = root / "wake.args"
            self.write_command(bin_dir, "shadow", "printf '%s\\n' \"$*\" > \"$SHADOW_LOG\"\n")
            self.write_command(bin_dir, "wake", "printf '%s\\n' \"$*\" > \"$WAKE_LOG\"\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["SHADOW_LOG"] = str(shadow_log)
            env["WAKE_LOG"] = str(wake_log)
            proc = subprocess.run([str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                "--fast-producer-only", "--lightweight-batch-producer",
                "--profile-service-suspicion-command", str(bin_dir / "batch-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow"),
                "--consumer-wake-command", str(bin_dir / "wake"),
                "--profile-service-failure-samples", "1", "--profile-service-cooldown-sec", "0"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "fast.state").read_text(encoding="utf-8")
            self.assertIn("profile_matrix_confirmation=REUSED_CURRENT", state_text)
            self.assertIn("profile_consumer_wake=PASS", state_text)
            self.assertFalse(shadow_log.exists())
            self.assertTrue(wake_log.exists())

    def test_persistent_health_profile_producer_leaves_exact_binding_for_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=v7tun enabled=1\n")
            (state / "users.registry").write_text("ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8")
            observed = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
            (state / "service-matrix.json").write_text(json.dumps({"items": {"vless": {"services": {"youtube": {
                "status": "FAIL", "severity": "FAIL", "failure_state": "OBSERVED_CONTINUING",
                "source_incident_id": "sfinc-current", "observed_at": observed,
            }}}}}), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "batch-checker", "printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":1,\"contracts\":[{\"source\":\"vless\",\"profile\":\"__GLOBAL__\",\"services\":[\"youtube\"],\"state_key\":\"vless-profile\",\"failure_count\":0,\"blockers\":[\"fast_service_budget_exceeded\"]}]}'\n")
            wake_log = root / "health-wake.env"
            self.write_command(
                bin_dir,
                "v7-service-matrix-refresh-all",
                "printf '%s|%s|%s\\n' \"$V7_SERVICE_PERSISTENT_MATRIX_OWNER\" \"$V7_SERVICE_PROFILE_SOURCE_EGRESS\" \"$V7_SERVICE_T0_MONOTONIC_NS\" > \"$WAKE_LOG\"\n",
            )
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["WAKE_LOG"] = str(wake_log)
            env["V7_HEALTH_PERSISTENT_MATRIX_CONSUMER"] = "1"
            proc = subprocess.run([str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                "--fast-producer-only", "--lightweight-batch-producer",
                "--profile-service-suspicion-command", str(bin_dir / "batch-checker"),
                "--shadow-trigger-command", "/bin/true",
                "--consumer-wake-command", str(bin_dir / "v7-service-matrix-refresh-all"),
                "--profile-service-failure-samples", "1", "--profile-service-cooldown-sec", "0"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertFalse(
                wake_log.exists(),
                "the persistent health parent must be the sole Matrix consumer",
            )
            state_text = (state / "fast.state").read_text(encoding="utf-8")
            self.assertIn("profile_consumer_wake=PASS", state_text)

    def test_fast_batch_reuses_fresh_matrix_for_explicit_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=v7tun enabled=1\n")
            (state / "users.registry").write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            observed = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
            (state / "service-matrix.json").write_text(json.dumps({"items": {"vless": {"services": {"google": {
                "status": "FAIL", "severity": "FAIL", "failure_state": "OBSERVED_CONTINUING",
                "source_incident_id": "sfinc-current", "observed_at": observed,
            }}}}}), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir, "batch-checker",
                "printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":1,\"contracts\":[{\"source\":\"vless\",\"profile\":\"__GLOBAL__\",\"services\":[\"google\"],\"state_key\":\"vless-profile\",\"failure_count\":1,\"failed_services\":[\"google\"]}]}'\n",
            )
            shadow_log = root / "shadow.args"
            self.write_command(bin_dir, "shadow", "printf '%s\\n' \"$*\" > \"$SHADOW_LOG\"\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["SHADOW_LOG"] = str(shadow_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                "--fast-producer-only", "--lightweight-batch-producer",
                "--profile-service-suspicion-command", str(bin_dir / "batch-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow"),
                "--consumer-wake-command", "/bin/true",
                "--profile-service-failure-samples", "1", "--profile-service-cooldown-sec", "0",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "fast.state").read_text(encoding="utf-8")
            self.assertIn("profile_matrix_confirmation=REUSED_CURRENT", state_text)
            self.assertFalse(shadow_log.exists())

    def test_fast_batch_reconfirms_matrix_failure_older_than_live_window(self):
        """A continuing failure may not bypass the ten-second T0 freshness law."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=v7tun enabled=1\n")
            (state / "users.registry").write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            observed = time.strftime(
                "%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(time.time() - 11)
            )
            (state / "service-matrix.json").write_text(json.dumps({
                "items": {"vless": {"services": {"google": {
                    "status": "FAIL", "severity": "FAIL",
                    "failure_state": "OBSERVED_CONTINUING",
                    "source_incident_id": "sfinc-current", "observed_at": observed,
                }}}}
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir, "batch-checker",
                "printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":1,\"contracts\":[{\"source\":\"vless\",\"profile\":\"__GLOBAL__\",\"services\":[\"google\"],\"state_key\":\"vless-profile\",\"failure_count\":1,\"failed_services\":[\"google\"]}]}'\n",
            )
            definitive_log = root / "definitive.args"
            self.write_command(
                bin_dir, "definitive",
                "printf '%s\\n' \"$*\" > \"$DEFINITIVE_LOG\"\n",
            )
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["DEFINITIVE_LOG"] = str(definitive_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                "--fast-producer-only", "--lightweight-batch-producer",
                "--profile-service-suspicion-command", str(bin_dir / "batch-checker"),
                "--shadow-trigger-command", "/bin/true",
                "--definitive-matrix-command", str(bin_dir / "definitive"),
                "--profile-service-failure-samples", "1", "--profile-service-cooldown-sec", "0",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "fast.state").read_text(encoding="utf-8")
            self.assertIn("profile_matrix_confirmation=CANONICAL_EXACT_CURRENT", state_text)
            self.assertTrue(definitive_log.exists())
            self.assertIn("vless all --services google", definitive_log.read_text(encoding="utf-8"))

    def test_fast_batch_confirms_one_source_union_once_before_profile_reuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=v7tun enabled=1\n")
            (state / "users.registry").write_text(
                "ip=profile-a current=vless enabled=1\n"
                "ip=profile-b current=vless enabled=1\n", encoding="utf-8"
            )
            self.write_command(bin_dir, "ip", "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir, "batch-checker",
                "printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":2,\"contracts\":[{\"source\":\"vless\",\"profile\":\"profile-a\",\"services\":[\"google\"],\"state_key\":\"vless-a\",\"failure_count\":1,\"failed_services\":[\"google:TIMEOUT\"]},{\"source\":\"vless\",\"profile\":\"profile-b\",\"services\":[\"youtube\"],\"state_key\":\"vless-b\",\"failure_count\":1,\"failed_services\":[\"youtube:TIMEOUT\"]}]}'\n",
            )
            definitive_log = root / "definitive.args"
            self.write_command(bin_dir, "definitive", "printf '%s\\n' \"$*\" >> \"$DEFINITIVE_LOG\"\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["DEFINITIVE_LOG"] = str(definitive_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                "--fast-producer-only", "--lightweight-batch-producer",
                "--profile-service-suspicion-command", str(bin_dir / "batch-checker"),
                "--shadow-trigger-command", "/bin/true",
                "--definitive-matrix-command", str(bin_dir / "definitive"),
                "--profile-service-failure-samples", "1", "--profile-service-cooldown-sec", "0",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(len(definitive_log.read_text(encoding="utf-8").splitlines()), 1)
            self.assertIn("vless all --services google,youtube", definitive_log.read_text(encoding="utf-8"))
            state_text = (state / "fast.state").read_text(encoding="utf-8")
            self.assertEqual(state_text.count("SOURCE_CURRENT_NO_EXACT_FAILURE"), 4)

    def test_fast_batch_uses_one_second_parallel_sentinel_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=v7tun enabled=1\n")
            (state / "users.registry").write_text("ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8")
            args_log = root / "batch.args"
            self.write_command(bin_dir, "ip", "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "batch-checker", "printf '%s\\n' \"$*\" > \"$BATCH_ARGS\"; printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":1,\"contracts\":[]}'\n")
            self.write_command(bin_dir, "shadow", "exit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["BATCH_ARGS"] = str(args_log)
            proc = subprocess.run([str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                "--fast-producer-only", "--lightweight-batch-producer",
                "--profile-service-suspicion-command", str(bin_dir / "batch-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow")],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("--sentinel-timeout-ms 1000", args_log.read_text(encoding="utf-8"))

    def test_fast_producer_ignores_stale_matrix_revalidation_without_trigger(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(
                root,
                "id=vless protocol=vless interface=v7tun enabled=1\n",
            )
            (state / "users.registry").write_text(
                "ip=10.7.0.125 current=vless enabled=1\n", encoding="utf-8"
            )
            old = "2026-08-27T00:00:00+00:00"
            (state / "service-matrix.json").write_text(
                json.dumps({"items": {"vless": {"services": {
                    "youtube": {
                        "status": "FAIL", "severity": "FAIL",
                        "failure_state": "OBSERVED_CONTINUING",
                        "source_incident_id": "sfinc-old", "observed_at": old,
                    }
                }}}}), encoding="utf-8"
            )
            self.write_command(
                bin_dir, "ip",
                "echo '1: v7tun: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n",
            )
            self.write_command(
                bin_dir, "profile-checker",
                "if [ \"$1\" = \"__batch__\" ]; then printf '%s\\n' '{\"status\":\"PASS\",\"ok\":true,\"probe_count\":1,\"contracts\":[{\"source\":\"vless\",\"profile\":\"__GLOBAL__\",\"services\":[\"youtube\"],\"state_key\":\"vless-profile\",\"failure_count\":0,\"blockers\":[\"fast_service_budget_exceeded\"]}]}'; else printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"youtube\":{\"ok\":false,\"status\":\"FAIL\",\"reason\":\"probe failed\"}}}'; fi\n",
            )
            receiver_log = root / "receiver.args"
            self.write_command(
                bin_dir, "receiver", "printf '%s\\n' \"$*\" > \"$RECEIVER_LOG\"\n",
            )
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            proc = subprocess.run(
                [
                    str(TOOL), "--state-dir", str(state), "--output", str(state / "fast.state"),
                    "--fast-producer-only", "--lightweight-batch-producer",
                    "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                    "--shadow-trigger-command", str(bin_dir / "receiver"),
                    "--profile-service-failure-samples", "1",
                    "--profile-service-cooldown-sec", "0",
                ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                env=env, check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "fast.state").read_text(encoding="utf-8")
            self.assertNotIn("profile_targeted_revalidation=USED", state_text)
            self.assertNotIn("profile_trigger_status=PASS", state_text)
            self.assertFalse(receiver_log.exists())

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

    def test_profile_service_producer_repeats_before_required_failure_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgservice protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgservice_code=000\n", encoding="utf-8")
            (state / "users.registry").write_text("ip=profile-a current=wgservice enabled=1\n", encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({
                "required_services": ["google"],
                "users": {"profile-a": {"services": ["google", "telegram"]}},
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            self.write_command(bin_dir, "profile-checker", "printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"google\":{\"ok\":false,\"status\":\"DOWN\",\"reason\":\"HTTP_FAILURE\"},\"telegram\":{\"ok\":true,\"status\":\"OK\"}}}'\n")
            receiver_log = root / "receiver.args"
            self.write_command(bin_dir, "shadow-receiver", "printf '%s\\n' \"$*\" >> \"$RECEIVER_LOG\"\nexit 0\n")
            wake_log = root / "wake.log"
            self.write_command(bin_dir, "wake-consumer", "printf 'wake\\n' >> \"$WAKE_LOG\"\nexit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            env["WAKE_LOG"] = str(wake_log)
            args = [
                str(TOOL), "--state-dir", str(state),
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--consumer-wake-command", str(bin_dir / "wake-consumer"),
                "--profile-service-failure-samples", "2",
            ]
            first = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            first_state = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("profile_failure_count=1", first_state)
            self.assertIn("profile_trigger_status=WAITING_REPEAT", first_state)
            self.assertFalse(wake_log.exists())
            second = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(second.returncode, 0, second.stderr)
            second_state = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("profile_trigger_status=PASS", second_state)
            self.assertIn("profile_trigger_class=REQUIRED_SERVICE_FAILURE", second_state)
            self.assertIn("profile_consumer_wake=PASS", second_state)
            self.assertEqual(wake_log.read_text(encoding="utf-8"), "wake\n")
            receiver_args = receiver_log.read_text(encoding="utf-8")
            self.assertIn("--shadow-trigger-profile-user profile-a", receiver_args)
            self.assertIn("--shadow-trigger-class REQUIRED_SERVICE_FAILURE", receiver_args)

    def test_profile_failure_is_confirmed_by_canonical_matrix_before_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgservice protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgservice_code=000\n", encoding="utf-8")
            (state / "users.registry").write_text("ip=profile-a current=wgservice enabled=1\n", encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({
                "required_services": ["google"],
                "users": {"profile-a": {"services": ["google", "telegram"]}},
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            self.write_command(bin_dir, "profile-checker", "printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"google\":{\"ok\":false,\"status\":\"DOWN\",\"reason\":\"HTTP_FAILURE\"},\"telegram\":{\"ok\":true,\"status\":\"OK\"}}}'\n")
            definitive_log = root / "definitive.args"
            shadow_log = root / "shadow.args"
            wake_log = root / "wake.log"
            self.write_command(bin_dir, "definitive-matrix", "printf '%s\\n' \"$*\" > \"$DEFINITIVE_LOG\"\nexit 0\n")
            self.write_command(bin_dir, "shadow-receiver", "printf '%s\\n' \"$*\" > \"$SHADOW_LOG\"\nexit 0\n")
            self.write_command(bin_dir, "wake-consumer", "printf 'wake\\n' >> \"$WAKE_LOG\"\nexit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["DEFINITIVE_LOG"] = str(definitive_log)
            env["SHADOW_LOG"] = str(shadow_log)
            env["WAKE_LOG"] = str(wake_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state),
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--definitive-matrix-command", str(bin_dir / "definitive-matrix"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--consumer-wake-command", str(bin_dir / "wake-consumer"),
                "--profile-service-failure-samples", "1",
                "--profile-service-cooldown-sec", "0",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("profile_matrix_confirmation=CANONICAL_EXACT_CURRENT", state_text)
            self.assertIn("profile_consumer_wake=PASS", state_text)
            confirmation_args = definitive_log.read_text(encoding="utf-8")
            self.assertIn("wgservice all --services google", confirmation_args)
            self.assertIn("--failure-persistence-samples 1", confirmation_args)
            self.assertIn("--role-fast-timeout", confirmation_args)
            self.assertIn("--lock-timeout-sec 1", confirmation_args)
            self.assertIn("--timeout 1", confirmation_args)
            self.assertFalse(shadow_log.exists())

    def test_dns_profile_producer_has_dns_specific_class_and_cooldown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgdns protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgdns_code=000\n", encoding="utf-8")
            (state / "users.registry").write_text("ip=profile-dns current=wgdns enabled=1\n", encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {"profile-dns": {"services": ["google", "telegram"]}},
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            self.write_command(bin_dir, "profile-checker", "printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"google\":{\"ok\":false,\"status\":\"DOWN\",\"reason\":\"DNS_FAILURE\"},\"telegram\":{\"ok\":true,\"status\":\"OK\"}}}'\n")
            receiver_log = root / "receiver.args"
            self.write_command(bin_dir, "shadow-receiver", "printf '%s\\n' \"$*\" >> \"$RECEIVER_LOG\"\nexit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            args = [
                str(TOOL), "--state-dir", str(state),
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--profile-service-failure-samples", "2",
                "--profile-service-cooldown-sec", "600",
            ]
            for _ in range(3):
                proc = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
                self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("profile_trigger_family=DNS_SUSPICION_PRODUCER", state_text)
            self.assertIn("profile_trigger_class=DNS_FAILURE", state_text)
            self.assertIn("profile_trigger_status=SUPPRESSED_COOLDOWN", state_text)
            self.assertEqual(len(receiver_log.read_text(encoding="utf-8").splitlines()), 1)

    def test_profile_producer_reaches_actual_receiver_and_matrix_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgchain protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgchain_code=000\n", encoding="utf-8")
            (state / "users.registry").write_text("ip=profile-chain current=wgchain enabled=1\n", encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({
                "required_services": ["google"],
                "users": {"profile-chain": {"services": ["google"]}},
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            self.write_command(bin_dir, "curl", "printf '204 0.001 0.002\\n'\n")
            self.write_command(bin_dir, "profile-checker", "printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"google\":{\"ok\":false,\"status\":\"DOWN\",\"reason\":\"HTTP_FAILURE\"}}}'\n")
            actual_receiver = root / "actual-receiver"
            receiver_debug = root / "receiver-debug"
            actual_receiver.write_text(
                "#!/usr/bin/env bash\n" + shlex.quote(str(ROOT / "tools" / "v7-service-matrix-refresh-all")) + " \"$@\" >\"$RECEIVER_DEBUG\" 2>&1\nexit $?\n",
                encoding="utf-8",
            )
            actual_receiver.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_DEBUG"] = str(receiver_debug)
            args = [
                str(TOOL), "--state-dir", str(state),
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(actual_receiver),
                "--profile-service-failure-samples", "2",
            ]
            first = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            second = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            second_state = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("profile_trigger_status=PASS", second_state)
            matrix = json.loads((state / "service-matrix.json").read_text(encoding="utf-8"))
            self.assertEqual(set(matrix["items"]["wgchain"]["services"]), {"google"})

    def test_profile_producer_handles_second_profile_multi_and_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgprofiles protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgprofiles_code=000\n", encoding="utf-8")
            (state / "users.registry").write_text(
                "ip=profile-a current=wgprofiles enabled=1\n"
                "ip=profile-b current=wgprofiles enabled=1\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "required_services": ["google"],
                "users": {
                    "profile-a": {"services": ["google", "telegram"]},
                    "profile-b": {"services": ["youtube"]},
                },
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            self.write_command(
                bin_dir,
                "profile-checker",
                "if [[ \"$*\" == *\"google,telegram\"* ]]; then "
                "printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"google\":{\"ok\":false,\"status\":\"DOWN\",\"reason\":\"HTTP_FAILURE\"},\"telegram\":{\"ok\":false,\"status\":\"DOWN\",\"reason\":\"HTTP_FAILURE\"}}}'; "
                "else printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"youtube\":{\"ok\":false,\"status\":\"DEGRADED\",\"reason\":\"PARTIAL\"}}}'; fi\n",
            )
            receiver_log = root / "receiver.args"
            self.write_command(bin_dir, "shadow-receiver", "printf '%s\\n' \"$*\" >> \"$RECEIVER_LOG\"\nexit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state),
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--profile-service-failure-samples", "1",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("profile_trigger_class=MULTI_SERVICE_FAILURE", state_text)
            self.assertIn("profile_trigger_class=PARTIAL_CENSORSHIP", state_text)
            receiver_args = receiver_log.read_text(encoding="utf-8")
            self.assertIn("--shadow-trigger-profile-user profile-a", receiver_args)
            self.assertIn("--shadow-trigger-profile-user profile-b", receiver_args)
            self.assertIn("--shadow-trigger-class MULTI_SERVICE_FAILURE", receiver_args)
            self.assertIn("--shadow-trigger-class PARTIAL_CENSORSHIP", receiver_args)

    def test_profile_producer_keeps_unknown_state_stop_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgunknown protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgunknown_code=000\n", encoding="utf-8")
            (state / "users.registry").write_text("ip=profile-unknown current=wgunknown enabled=1\n", encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {"profile-unknown": {"services": ["google"]}},
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "awg", "exit 0\n")
            self.write_command(bin_dir, "profile-checker", "printf '%s\\n' '{\"status\":\"UNKNOWN\",\"results\":{\"google\":{\"ok\":false,\"status\":\"UNKNOWN\"}}}'\n")
            receiver_log = root / "receiver.args"
            self.write_command(bin_dir, "shadow-receiver", "printf '%s\\n' \"$*\" >> \"$RECEIVER_LOG\"\nexit 0\n")
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["RECEIVER_LOG"] = str(receiver_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state),
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--profile-service-failure-samples", "1",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = (state / "egress-diagnose.state").read_text(encoding="utf-8")
            self.assertIn("profile_trigger_status=STOP_SAFE_UNKNOWN", state_text)
            self.assertIn("profile_trigger_class=STALE_OR_UNKNOWN_STATE", state_text)
            self.assertFalse(receiver_log.exists())

    def test_fast_producer_aggregates_current_profile_probes_per_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgshared protocol=wireguard interface=v7wg enabled=1\n")
            (state / "users.registry").write_text(
                "ip=profile-a current=wgshared enabled=1\n"
                "ip=profile-b current=wgshared enabled=1\n"
                "ip=profile-c current=wgshared enabled=1\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {
                    "profile-a": {"services": ["google", "telegram"]},
                    "profile-b": {"services": ["telegram", "google"]},
                    "profile-c": {"services": ["youtube"]},
                },
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "profile-checker", "printf '%s\\n' '{\"status\":\"OK\",\"results\":{}}'\n")
            self.write_command(bin_dir, "shadow-receiver", "exit 0\n")
            output = root / "fast-observation.state"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only",
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--profile-service-failure-samples", "1",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = output.read_text(encoding="utf-8")
            self.assertIn("fast_producer_active_source_count=1", state_text)
            self.assertIn("fast_producer_distinct_contract_count=2", state_text)
            self.assertIn("fast_producer_observation_count=1", state_text)
            self.assertIn(
                "profile_services=google,telegram,youtube", state_text
            )
            self.assertIn("fast_producer_receiver_invocation_count=0", state_text)

    def test_fast_producer_excludes_certification_only_identity_from_ordinary_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(
                root,
                "id=wgprod protocol=wireguard interface=v7wg enabled=1\n"
                "id=wgcert protocol=wireguard interface=v7wg enabled=1\n",
            )
            (state / "users.registry").write_text(
                "ip=ordinary current=wgprod enabled=1\n"
                "ip=certification current=wgcert enabled=1 certification_user=1 certification_group=polygon\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {
                    "ordinary": {"services": ["google"]},
                    "certification": {"services": ["google"]},
                },
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "profile-checker", "printf '%s\\n' '{\"status\":\"OK\",\"results\":{}}'\n")
            self.write_command(bin_dir, "shadow-receiver", "exit 0\n")
            output = root / "ordinary-fast.state"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only",
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = output.read_text(encoding="utf-8")
            self.assertIn("fast_producer_active_source_count=1", state_text)
            self.assertIn("fast_producer_distinct_contract_count=1", state_text)
            self.assertIn("wgprod", state_text)
            self.assertNotIn("wgcert_profile", state_text)

    def test_fast_producer_uses_one_second_exact_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgprod protocol=wireguard interface=v7wg enabled=1\n")
            (state / "users.registry").write_text(
                "ip=ordinary current=wgprod enabled=1\n", encoding="utf-8"
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {"ordinary": {"services": ["google"]}},
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir, "profile-checker",
                "printf '%s\\n' \"$*\" >> \"$ARGS_LOG\"\n"
                "printf '%s\\n' '{\"status\":\"OK\",\"results\":{}}'\n",
            )
            self.write_command(bin_dir, "shadow-receiver", "exit 0\n")
            output = root / "fast.state"
            args_log = root / "profile-checker.args"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["ARGS_LOG"] = str(args_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only",
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            checker_args = args_log.read_text(encoding="utf-8")
            self.assertIn("--role-fast-timeout", checker_args)
            self.assertIn("--timeout 1", checker_args)

    def test_fast_producer_requires_explicit_controlled_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.base_state(root, "id=wgfast protocol=wireguard interface=v7wg enabled=1\n")
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--fast-producer-only",
                "--profile-service-suspicion-command", "/bin/true",
                "--shadow-trigger-command", "/bin/true",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("requires profile suspicion command and explicit output", proc.stderr)

    def test_controlled_fast_concurrency_is_bounded_and_preserves_all_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(
                root,
                "id=wgfast protocol=wireguard interface=v7wg enabled=1\n"
                "id=wgslow protocol=wireguard interface=v7wg enabled=1\n"
                "id=wgthird protocol=wireguard interface=v7wg enabled=1\n",
            )
            (state / "users.registry").write_text(
                "ip=profile-fast current=wgfast enabled=1\n"
                "ip=profile-slow current=wgslow enabled=1\n"
                "ip=profile-third current=wgthird enabled=1\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {
                    "profile-fast": {"services": ["google"]},
                    "profile-slow": {"services": ["google"]},
                    "profile-third": {"services": ["google"]},
                },
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir,
                "profile-checker",
                "if [[ \"$1\" == \"wgslow\" ]]; then sleep 0.2; fi\n"
                "printf '%s\\n' '{\"status\":\"OK\",\"results\":{}}'\n",
            )
            self.write_command(bin_dir, "shadow-receiver", "exit 0\n")
            output = root / "fast-parallel.state"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only", "--fast-producer-concurrency", "2",
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            state_text = output.read_text(encoding="utf-8")
            self.assertIn("fast_producer_observation_count=3", state_text)
            self.assertIn("fast_producer_concurrency_cap=2", state_text)
            self.assertIn("fast_producer_max_inflight=2", state_text)

    def test_parallel_fast_concurrency_is_rejected_outside_controlled_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.base_state(root, "id=wgfast protocol=wireguard interface=v7wg enabled=1\n")
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--fast-producer-concurrency", "2",
                "--profile-service-suspicion-command", "/bin/true",
                "--shadow-trigger-command", "/bin/true",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("requires --fast-producer-only", proc.stderr)

    def test_parallel_fast_result_streams_without_waiting_for_slow_unrelated_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(
                root,
                "id=wgslow protocol=wireguard interface=v7wg enabled=1\n"
                "id=wgfail protocol=wireguard interface=v7wg enabled=1\n",
            )
            (state / "users.registry").write_text(
                "ip=profile-slow current=wgslow enabled=1\n"
                "ip=profile-fail current=wgfail enabled=1\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "required_services": ["google"],
                "users": {
                    "profile-slow": {"services": ["google"]},
                    "profile-fail": {"services": ["google"]},
                },
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(
                bin_dir,
                "profile-checker",
                "if [[ \"$1\" == \"wgslow\" ]]; then sleep 1; touch \"$SLOW_DONE\"; "
                "printf '%s\\n' '{\"status\":\"OK\",\"results\":{}}'; "
                "else printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"google\":{\"ok\":false,\"status\":\"DOWN\",\"reason\":\"HTTP_FAILURE\"}}}'; fi\n",
            )
            self.write_command(
                bin_dir,
                "shadow-receiver",
                "if [[ -f \"$SLOW_DONE\" ]]; then echo after >> \"$RECEIVER_LOG\"; else echo before >> \"$RECEIVER_LOG\"; fi\n",
            )
            output = root / "fast-stream.state"
            slow_done = root / "slow.done"
            receiver_log = root / "receiver.log"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["SLOW_DONE"] = str(slow_done)
            env["RECEIVER_LOG"] = str(receiver_log)
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only", "--fast-producer-concurrency", "2",
                "--profile-service-suspicion-command", str(bin_dir / "profile-checker"),
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--profile-service-failure-samples", "1",
                "--profile-service-cooldown-sec", "0",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(receiver_log.read_text(encoding="utf-8").strip(), "before")
            self.assertIn("fast_producer_max_inflight=2", output.read_text(encoding="utf-8"))

    def test_persistent_health_parent_consumes_profile_failure_without_child_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=vless protocol=vless interface=v7tun enabled=1\n")
            (state / "users.registry").write_text(
                "ip=ordinary current=vless enabled=1\n", encoding="utf-8"
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {"ordinary": {"services": ["google"]}},
            }), encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7tun: <UP,LOWER_UP>'\n")
            self.write_command(
                bin_dir, "profile-checker",
                "printf '%s\\n' '{\"status\":\"FAIL\",\"results\":{\"google\":{\"ok\":false,\"status\":\"DOWN\"}}}'\n",
            )
            shadow_log = root / "shadow.log"
            wake_log = root / "wake.log"
            self.write_command(bin_dir, "shadow", "echo shadow >> \"$SHADOW_LOG\"\n")
            self.write_command(bin_dir, "wake", "echo wake >> \"$WAKE_LOG\"\n")
            output = root / "fast.state"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["SHADOW_LOG"] = str(shadow_log)
            env["WAKE_LOG"] = str(wake_log)
            env["V7_HEALTH_PERSISTENT_MATRIX_CONSUMER"] = "1"
            proc = subprocess.run([
                str(TOOL), "--state-dir", str(state), "--output", str(output),
                "--fast-producer-only", "--profile-service-suspicion-command",
                str(bin_dir / "profile-checker"), "--shadow-trigger-command",
                str(bin_dir / "shadow"), "--consumer-wake-command", str(bin_dir / "wake"),
                "--profile-service-failure-samples", "1", "--profile-service-cooldown-sec", "0",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(shadow_log.exists())
            self.assertFalse(wake_log.exists())

    def test_failed_receiver_records_its_real_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            state = self.base_state(root, "id=wgfail protocol=wireguard interface=v7wg enabled=1\n")
            (state / "summary.state").write_text("wgfail_code=000\n", encoding="utf-8")
            self.write_command(bin_dir, "ip", "echo '1: v7wg: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420'\n")
            self.write_command(bin_dir, "wg", "exit 0\n")
            self.write_command(bin_dir, "shadow-receiver", "exit 17\n")
            out = self.run_tool(state, bin_dir, [
                "--shadow-trigger-command", str(bin_dir / "shadow-receiver"),
                "--shadow-trigger-egress", "wgfail", "--shadow-trigger-services", "google",
            ])
            self.assertIn("wgfail_shadow_trigger_status=FAILED", out)
            self.assertIn("wgfail_shadow_trigger_rc=17", out)


if __name__ == "__main__":
    unittest.main()
