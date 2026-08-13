import importlib.machinery
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/runtime-support/v7-routing-sync"


class RoutingSyncCoreTests(unittest.TestCase):
    def test_migration_owner_has_exact_authority_and_fallback_gates(self):
        source = SCRIPT.read_text()
        self.assertIn("exact_reset_authority", source)
        self.assertIn("routing_core_primary_promotion", source)
        self.assertIn("legacy_fallback_ready", source)
        self.assertIn("core_primary_fallback", source)
        self.assertIn("meta mark set ip saddr map @user_class", source)
        self.assertIn("meta mark set meta mark map @class_egress", source)
        self.assertIn("counter meta mark set ip saddr map @user_class", source)
        self.assertIn("result = core_primary_apply() if authority_ok else legacy_sync()", source)
        self.assertIn("def retire_legacy_primary_routes", source)
        self.assertIn('"legacy_fallback_ready": True', source)

    def test_script_parses(self):
        loader = importlib.machinery.SourceFileLoader("v7_routing_sync_core", str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        self.assertEqual(module.NFT_TABLE, "v7_routing_core")


if __name__ == "__main__":
    unittest.main()
