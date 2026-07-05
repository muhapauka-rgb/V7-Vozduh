import os
import subprocess
import tempfile
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / "tools" / "runtime-support" / "v7-egress-load"


class V7EgressLoadPolicyTest(unittest.TestCase):
    def run_load(self, extra_env=None):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "egress.registry").write_text("id=openvpn-1779388847-d2ad7c enabled=1\n", encoding="utf-8")
            (state / "users.registry").write_text(
                "ip=10.7.0.2 current=openvpn-1779388847-d2ad7c enabled=1\n"
                "ip=10.7.0.3 current=openvpn-1779388847-d2ad7c enabled=1\n"
                "ip=10.7.0.4 current=openvpn-1779388847-d2ad7c enabled=1\n",
                encoding="utf-8",
            )
            lib = state / "v7-egress-lib"
            lib.write_text(
                "v7_kv_get() { local line=\"$1\" key=\"$2\"; for part in $line; do case \"$part\" in ${key}=*) printf '%s\\n' \"${part#*=}\"; return;; esac; done; }\n",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env.update({
                "V7_EGRESS_LIB": str(lib),
                "V7_LOAD_SOFT_LIMIT": "",
                "V7_LOAD_HARD_LIMIT": "",
            })
            env.pop("V7_LOAD_SOFT_LIMIT", None)
            env.pop("V7_LOAD_HARD_LIMIT", None)
            if extra_env:
                env.update(extra_env)
            result = subprocess.run(
                [str(SCRIPT)],
                cwd=str(Path(__file__).resolve().parents[2]),
                env={**env, "V7_STATE_DIR": str(state)},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            return result.stdout

    def test_missing_load_env_does_not_create_artificial_hard_full(self):
        output = self.run_load()

        self.assertIn("openvpn-1779388847-d2ad7c_users=3", output)
        self.assertIn("openvpn-1779388847-d2ad7c_soft_limit=0", output)
        self.assertIn("openvpn-1779388847-d2ad7c_hard_limit=0", output)
        self.assertIn("openvpn-1779388847-d2ad7c_load_status=OK", output)

    def test_explicit_load_env_still_enforces_capacity(self):
        output = self.run_load({"V7_LOAD_SOFT_LIMIT": "1", "V7_LOAD_HARD_LIMIT": "2"})

        self.assertIn("openvpn-1779388847-d2ad7c_soft_limit=1", output)
        self.assertIn("openvpn-1779388847-d2ad7c_hard_limit=2", output)
        self.assertIn("openvpn-1779388847-d2ad7c_load_status=HARD_FULL", output)


if __name__ == "__main__":
    unittest.main()
