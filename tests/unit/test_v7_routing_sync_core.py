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

    def test_cohort_commit_updates_only_selected_members_in_one_nft_batch(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_cohort", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        users = [
            {"ip": "10.7.0.2", "current": "source", "table": "1002", "enabled": "1"},
            {"ip": "10.7.0.3", "current": "target", "table": "1003", "enabled": "1"},
            {"ip": "10.7.0.4", "current": "target", "table": "1004", "enabled": "1"},
        ]
        classes = [
            {"mark": 512, "members": ["10.7.0.2"]},
            {"mark": 513, "members": ["10.7.0.3", "10.7.0.4"]},
        ]
        payload = {
            "nftables": [
                {"map": {"name": "user_class", "elem": [
                    ["10.7.0.2", "512"], ["10.7.0.3", "513"], ["10.7.0.4", "512"],
                ]}},
                {"map": {"name": "class_egress", "elem": [
                    ["512", "512"], ["513", "513"],
                ]}},
            ],
        }
        calls = []

        def fake_run(argv, *, input_text=""):
            calls.append((argv, input_text))
            if argv[:3] == ["nft", "-j", "list"]:
                return mock.Mock(returncode=0, stdout=__import__("json").dumps(payload))
            return mock.Mock(returncode=0, stdout="")

        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {"contract_id": "rcpp-test"})), \
             mock.patch.object(module, "derived_classes", return_value=(users, classes)), \
             mock.patch.object(module, "run", side_effect=fake_run), \
             mock.patch.object(module, "verify", return_value={"status": "CORE_PRIMARY_VERIFY_PASS"}), \
             mock.patch.object(module, "retire_legacy_primary_routes", return_value={"rules_removed": 2, "routes_removed": 2}):
            result = module.core_primary_cohort_commit(
                ["10.7.0.3", "10.7.0.4"], "op-cohort",
            )

        self.assertEqual(result["status"], "CORE_PRIMARY_COHORT_COMMIT_PASS")
        self.assertEqual(result["affected_users"], 2)
        batch = [input_text for argv, input_text in calls if argv == ["nft", "-f", "-"]]
        self.assertEqual(len(batch), 1)
        self.assertIn("delete element inet v7_routing_core user_class", batch[0])
        self.assertIn("add element inet v7_routing_core user_class", batch[0])
        self.assertIn("10.7.0.3 : 0x201", batch[0])
        self.assertNotIn("10.7.0.2", batch[0])

    def test_cohort_commit_fails_closed_when_non_cohort_map_is_not_exact(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_cohort_stop", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        users = [
            {"ip": "10.7.0.2", "current": "source", "enabled": "1"},
            {"ip": "10.7.0.3", "current": "target", "enabled": "1"},
            {"ip": "10.7.0.4", "current": "target", "enabled": "1"},
        ]
        classes = [
            {"mark": 512, "members": ["10.7.0.2"]},
            {"mark": 513, "members": ["10.7.0.3", "10.7.0.4"]},
        ]
        stale_payload = {
            "nftables": [
                {"map": {"name": "user_class", "elem": [
                    ["10.7.0.2", "999"], ["10.7.0.3", "513"], ["10.7.0.4", "512"],
                ]}},
                {"map": {"name": "class_egress", "elem": [
                    ["512", "512"], ["513", "513"],
                ]}},
            ],
        }
        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {})), \
             mock.patch.object(module, "derived_classes", return_value=(users, classes)), \
             mock.patch.object(module, "run", return_value=mock.Mock(returncode=0, stdout=__import__("json").dumps(stale_payload))) as run_mock:
            result = module.core_primary_cohort_commit(["10.7.0.3", "10.7.0.4"])

        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertIn("core_primary_cohort_baseline_not_exact_or_class_delta_required", result["blockers"])

    def test_cohort_admissibility_refuses_class_removal_before_mutation(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_cohort_admissibility", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        users = [
            {"ip": "10.7.0.2", "current": "source", "enabled": "1"},
            {"ip": "10.7.0.3", "current": "source", "enabled": "1"},
            {"ip": "10.7.0.4", "current": "target", "enabled": "1"},
        ]
        current_classes = [
            {"mark": 512, "members": ["10.7.0.2", "10.7.0.3"]},
            {"mark": 513, "members": ["10.7.0.4"]},
        ]
        prospective_classes = [
            {"mark": 512, "members": ["10.7.0.2", "10.7.0.3", "10.7.0.4"]},
        ]
        payload = {
            "nftables": [
                {"map": {"name": "user_class", "elem": [
                    ["10.7.0.2", "512"], ["10.7.0.3", "512"], ["10.7.0.4", "513"],
                ]}},
                {"map": {"name": "class_egress", "elem": [
                    ["512", "512"], ["513", "513"],
                ]}},
            ],
        }
        egress = [
            {"id": "source", "enabled": "1", "interface": "wg-source"},
            {"id": "target", "enabled": "1", "interface": "wg-target"},
        ]
        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {"contract_id": "rcpp-test"})), \
             mock.patch.object(module, "derived_classes", return_value=(users, current_classes)), \
             mock.patch.object(module, "rows", return_value=egress), \
             mock.patch.object(module, "classes_for_users", return_value=prospective_classes), \
             mock.patch.object(module, "run", return_value=mock.Mock(returncode=0, stdout=__import__("json").dumps(payload))) as run_mock:
            result = module.core_primary_cohort_admissible(
                ["10.7.0.2", "10.7.0.3"], "target",
            )

        self.assertEqual(result["status"], "CORE_PRIMARY_COHORT_NOT_ADMISSIBLE")
        self.assertIn(
            "core_primary_cohort_changes_nonmember_class_or_class_egress",
            result["blockers"],
        )
        self.assertFalse(result["runtime_mutation"])
        self.assertEqual(run_mock.call_args_list[0].args[0][:3], ["nft", "-j", "list"])
        self.assertFalse(any(call.args[0] == ["nft", "-f", "-"] for call in run_mock.call_args_list))


if __name__ == "__main__":
    unittest.main()
