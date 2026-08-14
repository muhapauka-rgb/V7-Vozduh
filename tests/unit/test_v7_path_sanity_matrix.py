import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/runtime-support/v7-path-sanity-check"


class V7PathSanityMatrixTest(unittest.TestCase):
    def run_check(self, matrix, legacy_status="OK"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            state_dir = root / "state"
            bin_dir.mkdir()
            state_dir.mkdir()
            if matrix is not None:
                (state_dir / "service-matrix.json").write_text(
                    json.dumps(matrix), encoding="utf-8"
                )
            (state_dir / "service-matrix-refresh.state").write_text(
                f"status={legacy_status}\n", encoding="utf-8"
            )
            commands = {
                "date": "printf '2026-08-14T12:00:00+03:00\\n'",
                "sysctl": "printf '1\\n'",
                "iptables": "exit 0",
                "ip": "exit 1",
                "nft": (
                    "if [ \"$4\" = dstnat ]; then printf 'dport 53\\n'; "
                    "else printf 'block direct leak\\nallow explicit direct whitelist\\n'; fi"
                ),
                "v7-user-desired-state": "printf 'V7_USER_DESIRED_STATE=OK\\n'",
            }
            for name, body in commands.items():
                path = bin_dir / name
                path.write_text(f"#!/usr/bin/env bash\n{body}\n", encoding="utf-8")
                path.chmod(0o755)
            result = subprocess.run(
                ["bash", str(SCRIPT)],
                env={
                    **os.environ,
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "V7_STATE_DIR": str(state_dir),
                },
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout

    def test_canonical_matrix_overrides_stale_legacy_state(self):
        output = self.run_check(
            {"items": {"healthy": {"status": "OK"}, "failed": {"status": "FAIL"}}},
            legacy_status="OK",
        )
        self.assertIn("egress_service_matrix=FAIL", output)
        self.assertIn("service_matrix_canonical_egress_direct_not_full_client_path", output)
        self.assertNotIn("service_matrix_legacy_fallback", output)

    def test_canonical_unknown_does_not_fall_back_to_stale_legacy_state(self):
        output = self.run_check({"items": {}}, legacy_status="OK")
        self.assertIn("egress_service_matrix=UNKNOWN", output)
        self.assertIn("service_matrix_canonical_egress_direct_not_full_client_path", output)

    def test_legacy_state_is_used_only_when_canonical_matrix_is_absent(self):
        output = self.run_check(None, legacy_status="WARN")
        self.assertIn("egress_service_matrix=WARN", output)
        self.assertIn("service_matrix_legacy_fallback_egress_direct_not_full_client_path", output)


if __name__ == "__main__":
    unittest.main()
