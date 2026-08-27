import importlib.machinery
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "tools/runtime-support/v7-user-route-check"
SYNC = ROOT / "tools/runtime-support/v7-routing-sync"


class V7UserRouteCheckTest(unittest.TestCase):
    def run_checker(self, core_status):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            state_dir = root / "state"
            bin_dir.mkdir()
            state_dir.mkdir()
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg3 table=100 enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "user-10.0.0.2.assign").write_text(
                "egress=awg3\n", encoding="utf-8",
            )
            library = root / "v7-egress-lib"
            library.write_text(
                "v7_kv_get() { local line=$1 key=$2 part; for part in $line; do case $part in \"$key\"=*) printf '%s\\n' \"${part#*=}\"; return 0;; esac; done; }\n"
                "v7_safe_ip() { [[ $1 = 10.0.0.2 ]]; }\n"
                "v7_egress_interface() { printf 'awg3\\n'; }\n",
                encoding="utf-8",
            )
            (bin_dir / "v7-routing-sync").write_text(
                "#!/usr/bin/env bash\n"
                "printf '%s\\n' '"
                + json.dumps({
                    "status": core_status,
                    "legacy_primary_rules_present": False,
                })
                + "'\n",
                encoding="utf-8",
            )
            (bin_dir / "date").write_text(
                "#!/usr/bin/env bash\nprintf '2026-08-27T10:00:00+03:00\\n'\n",
                encoding="utf-8",
            )
            for path in bin_dir.iterdir():
                path.chmod(0o755)
            return subprocess.run(
                ["bash", str(CHECKER)],
                env={
                    **os.environ,
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "V7_STATE_DIR": str(state_dir),
                    "V7_EGRESS_LIB": str(library),
                },
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

    def test_core_primary_pass_does_not_require_retired_per_user_tables(self):
        result = self.run_checker("CORE_PRIMARY_VERIFY_PASS")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("routing_mode=CORE_PRIMARY_CLASS_ROUTING", result.stdout)
        self.assertIn("covered by verified Core-primary class routing", result.stdout)
        self.assertNotIn("does not default", result.stdout)
        self.assertIn("V7_USER_ROUTE_CHECK=OK", result.stdout)

    def test_unverified_core_fails_closed(self):
        result = self.run_checker("STOP_SAFE")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("routing_mode=CORE_PRIMARY_UNVERIFIED", result.stdout)
        self.assertIn("core-primary route owner is not independently verified", result.stdout)
        self.assertIn("V7_USER_ROUTE_CHECK=FAIL", result.stdout)

    def test_core_verify_requires_exact_live_map_membership(self):
        loader = importlib.machinery.SourceFileLoader("v7_routing_sync_verify", str(SYNC))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        users = [{"ip": "10.0.0.2", "current": "awg3", "enabled": "1", "table": "100"}]
        classes = [{"current_egress": "awg3", "interface": "awg3", "mark": 512, "table": 200, "members": ["10.0.0.2"]}]
        nft_payload = {
            "nftables": [
                {"map": {"name": "user_class", "elem": [["10.0.0.9", 512]]}},
                {"map": {"name": "class_egress", "elem": [[512, 512]]}},
            ]
        }
        responses = [
            mock.Mock(returncode=0, stdout=json.dumps(nft_payload)),
            mock.Mock(returncode=0, stdout=json.dumps([{"fwmark": "0x200"}])),
        ]
        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {"contract_id": "rcpp-test"})), mock.patch.object(
            module, "derived_classes", return_value=(users, classes),
        ), mock.patch.object(module, "run", side_effect=responses):
            result = module.verify()

        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertEqual(result["user_class_missing_count"], 1)
        self.assertEqual(result["user_class_unexpected_count"], 1)


if __name__ == "__main__":
    unittest.main()
