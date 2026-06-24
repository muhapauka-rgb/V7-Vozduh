import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_cli_module():
    path = Path(__file__).resolve().parents[2] / "tools" / "v7-governed-canary-dry-run-cycle"
    loader = importlib.machinery.SourceFileLoader("v7_governed_canary_dry_run_cycle", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class GovernedCanaryCliTest(unittest.TestCase):
    def test_planner_executable_uses_repo_tool_when_available(self):
        module = load_cli_module()
        self.assertEqual(module.planner_observe_executable(), module.ROOT / "tools" / "v7-users-autoswitch")

    def test_planner_executable_falls_back_to_runtime_peer(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "bin"
            runtime_dir.mkdir(parents=True)
            script = runtime_dir / "v7-governed-canary-dry-run-cycle"
            peer = runtime_dir / "v7-users-autoswitch"
            script.write_text("", encoding="utf-8")
            peer.write_text("", encoding="utf-8")
            original_root = module.ROOT
            original_file = module.__file__
            try:
                module.ROOT = root / "missing-repo-root"
                module.__file__ = str(script)
                self.assertEqual(module.planner_observe_executable().resolve(), peer.resolve())
            finally:
                module.ROOT = original_root
                module.__file__ = original_file


if __name__ == "__main__":
    unittest.main()
