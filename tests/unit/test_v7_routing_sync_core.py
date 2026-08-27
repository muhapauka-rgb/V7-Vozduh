import importlib.machinery
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

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
        self.assertIn("def core_primary_active", source)

    def test_script_parses(self):
        loader = importlib.machinery.SourceFileLoader("v7_routing_sync_core", str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        self.assertEqual(module.NFT_TABLE, "v7_routing_core")

    def test_core_primary_active_exposes_only_existing_contract_state(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_active", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        with mock.patch.object(
            module, "exact_reset_authority", return_value=(True, {"contract_id": "rcpp-test"}),
        ):
            active = module.core_primary_active()
        with mock.patch.object(module, "exact_reset_authority", return_value=(False, {})):
            inactive = module.core_primary_active()
        self.assertEqual(active["status"], "CORE_PRIMARY_ACTIVE")
        self.assertEqual(active["authority_contract_id"], "rcpp-test")
        self.assertFalse(active["runtime_mutation"])
        self.assertEqual(inactive["status"], "CORE_PRIMARY_INACTIVE")

    def test_scoped_user_sync_repairs_only_exact_registry_identity(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_scoped", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        user = {
            "ip": "10.7.0.92", "current": "execution-source",
            "table": "1090", "enabled": "1",
        }
        target = {
            "id": "execution-source", "interface": "v7execwg0",
            "enabled": "1",
        }
        with mock.patch.object(
            module, "rows", side_effect=[[user], [target]],
        ), mock.patch.object(
            module, "run", return_value=mock.Mock(returncode=0, stdout=""),
        ) as run_mock, mock.patch.object(module, "replace_rule") as rule_mock:
            result = module.scoped_user_sync("10.7.0.92")

        self.assertEqual(result["status"], "SCOPED_USER_SYNC_PASS")
        self.assertFalse(result["assignment_changed"])
        self.assertEqual(result["users"], 1)
        run_mock.assert_called_once_with([
            "ip", "route", "replace", "default", "dev", "v7execwg0",
            "table", "1090",
        ])
        rule_mock.assert_called_once_with(
            pref=1090, selector=["from", "10.7.0.92"], table=1090,
        )


if __name__ == "__main__":
    unittest.main()
