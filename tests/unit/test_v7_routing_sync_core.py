import importlib.machinery
import importlib.util
import json
from pathlib import Path
import tempfile
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

        egress = [
            {"id": "source", "enabled": "1", "interface": "wg-source"},
            {"id": "target", "enabled": "1", "interface": "wg-target"},
        ]
        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {"contract_id": "rcpp-test"})), \
             mock.patch.object(module, "rows", side_effect=[users, egress]), \
             mock.patch.object(module, "live_classes_for_users", return_value=classes), \
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
        egress = [
            {"id": "source", "enabled": "1", "interface": "wg-source"},
            {"id": "target", "enabled": "1", "interface": "wg-target"},
        ]
        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {})), \
             mock.patch.object(module, "rows", side_effect=[users, egress]), \
             mock.patch.object(module, "live_classes_for_users", return_value=classes), \
             mock.patch.object(module, "run", return_value=mock.Mock(returncode=0, stdout=__import__("json").dumps(stale_payload))) as run_mock:
            result = module.core_primary_cohort_commit(["10.7.0.3", "10.7.0.4"])

        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertIn("core_primary_cohort_baseline_not_exact_or_class_delta_required", result["blockers"])

    def test_cohort_commit_retires_only_now_empty_source_class_atomically(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_empty_source", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        users = [
            {"ip": "10.7.0.2", "current": "target", "table": "1002", "enabled": "1"},
            {"ip": "10.7.0.3", "current": "target", "table": "1003", "enabled": "1"},
            {"ip": "10.7.0.4", "current": "target", "table": "1004", "enabled": "1"},
        ]
        classes = [{"mark": 513, "members": ["10.7.0.2", "10.7.0.3", "10.7.0.4"]}]
        egress = [
            {"id": "source", "enabled": "1", "interface": "wg-source"},
            {"id": "target", "enabled": "1", "interface": "wg-target"},
        ]
        payload = {"nftables": [
            {"map": {"name": "user_class", "elem": [
                ["10.7.0.2", "512"], ["10.7.0.3", "512"], ["10.7.0.4", "513"],
            ]}},
            {"map": {"name": "class_egress", "elem": [
                ["512", "512"], ["513", "513"],
            ]}},
        ]}
        calls = []

        def fake_run(argv, *, input_text=""):
            calls.append((argv, input_text))
            if argv[:3] == ["nft", "-j", "list"]:
                return mock.Mock(returncode=0, stdout=__import__("json").dumps(payload))
            return mock.Mock(returncode=0, stdout="")

        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {"contract_id": "rcpp-test"})), \
             mock.patch.object(module, "rows", side_effect=[users, egress]), \
             mock.patch.object(module, "live_classes_for_users", return_value=classes), \
             mock.patch.object(module, "run", side_effect=fake_run), \
             mock.patch.object(module, "verify", return_value={"status": "CORE_PRIMARY_VERIFY_PASS"}), \
             mock.patch.object(module, "retire_legacy_primary_routes", return_value={"rules_removed": 2, "routes_removed": 2}):
            result = module.core_primary_cohort_commit(["10.7.0.2", "10.7.0.3"], "op-empty-source")

        self.assertEqual(result["status"], "CORE_PRIMARY_COHORT_COMMIT_PASS")
        self.assertEqual(result["retired_empty_class_marks"], ["512"])
        batch = next(text for argv, text in calls if argv == ["nft", "-f", "-"])
        self.assertIn("delete element inet v7_routing_core class_egress { 0x200 }", batch)
        self.assertNotIn("10.7.0.4", batch)

    def test_cohort_admissibility_allows_retiring_only_an_empty_source_class(self):
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
            {"mark": 513, "members": ["10.7.0.2", "10.7.0.3", "10.7.0.4"]},
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
             mock.patch.object(module, "rows", side_effect=[users, egress]), \
             mock.patch.object(module, "live_classes_for_users", side_effect=[current_classes, prospective_classes]), \
             mock.patch.object(module, "run", return_value=mock.Mock(returncode=0, stdout=__import__("json").dumps(payload))) as run_mock:
            result = module.core_primary_cohort_admissible(
                ["10.7.0.2", "10.7.0.3"], "target",
            )

        self.assertEqual(result["status"], "CORE_PRIMARY_COHORT_ADMISSIBLE")
        self.assertEqual(result["retired_empty_class_marks"], ["512"])
        self.assertFalse(result["runtime_mutation"])
        self.assertEqual(run_mock.call_args_list[0].args[0][:3], ["nft", "-j", "list"])
        self.assertFalse(any(call.args[0] == ["nft", "-f", "-"] for call in run_mock.call_args_list))

    def test_stable_egress_identity_keeps_empty_source_class_and_unrelated_marks(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_stable_classes", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        egress = {
            "source": {
                "id": "source", "enabled": "1", "interface": "wg-source",
                "core_primary_mark": "0x200", "core_primary_table": "200",
            },
            "target": {
                "id": "target", "enabled": "1", "interface": "wg-target",
                "core_primary_mark": "0x201", "core_primary_table": "201",
            },
            "unrelated": {
                "id": "unrelated", "enabled": "1", "interface": "wg-other",
                "core_primary_mark": "0x202", "core_primary_table": "202",
            },
        }
        before = [
            {"ip": "10.7.0.2", "current": "source", "enabled": "1"},
            {"ip": "10.7.0.3", "current": "source", "enabled": "1"},
            {"ip": "10.7.0.4", "current": "unrelated", "enabled": "1"},
        ]
        after = [
            {"ip": "10.7.0.2", "current": "target", "enabled": "1"},
            {"ip": "10.7.0.3", "current": "target", "enabled": "1"},
            {"ip": "10.7.0.4", "current": "unrelated", "enabled": "1"},
        ]
        before_classes = module.classes_for_users(before, egress)
        after_classes = module.classes_for_users(after, egress)
        by_name_before = {row["current_egress"]: row for row in before_classes}
        by_name_after = {row["current_egress"]: row for row in after_classes}

        self.assertEqual(by_name_before["unrelated"]["mark"], by_name_after["unrelated"]["mark"])
        self.assertEqual(by_name_before["source"]["mark"], by_name_after["source"]["mark"])
        self.assertEqual(by_name_after["source"]["members"], [])
        self.assertEqual(by_name_before["target"]["mark"], by_name_after["target"]["mark"])

    def test_stable_cohort_admissibility_does_not_retire_last_source_class(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_stable_admissibility", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        users = [
            {"ip": "10.7.0.2", "current": "source", "enabled": "1"},
            {"ip": "10.7.0.3", "current": "source", "enabled": "1"},
            {"ip": "10.7.0.4", "current": "unrelated", "enabled": "1"},
        ]
        egress = [
            {"id": "source", "enabled": "1", "interface": "wg-source", "core_primary_mark": "512", "core_primary_table": "200"},
            {"id": "target", "enabled": "1", "interface": "wg-target", "core_primary_mark": "513", "core_primary_table": "201"},
            {"id": "unrelated", "enabled": "1", "interface": "wg-other", "core_primary_mark": "514", "core_primary_table": "202"},
        ]
        payload = {"nftables": [
            {"map": {"name": "user_class", "elem": [
                ["10.7.0.2", "512"], ["10.7.0.3", "512"], ["10.7.0.4", "514"],
            ]}},
            {"map": {"name": "class_egress", "elem": [
                ["512", "512"], ["513", "513"], ["514", "514"],
            ]}},
        ]}
        with mock.patch.object(module, "exact_reset_authority", return_value=(True, {"contract_id": "stable-test"})), \
             mock.patch.object(module, "rows", side_effect=[users, egress]), \
             mock.patch.object(module, "run", return_value=mock.Mock(returncode=0, stdout=__import__("json").dumps(payload))):
            result = module.core_primary_cohort_admissible(["10.7.0.2", "10.7.0.3"], "target")

        self.assertEqual(result["status"], "CORE_PRIMARY_COHORT_ADMISSIBLE")
        self.assertEqual(result["retired_empty_class_marks"], [])

    def test_stable_migration_extends_only_canonical_egress_registry(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_stable_migration", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            users_path = root / "users.registry"
            egress_path = root / "egress.registry"
            users_path.write_text(
                "ip=10.7.0.2 current=source enabled=1\n"
                "ip=10.7.0.3 current=target enabled=1\n",
                encoding="utf-8",
            )
            egress_path.write_text(
                "id=source enabled=1 interface=wg-source\n"
                "id=target enabled=1 interface=wg-target\n"
                "id=empty enabled=1 interface=wg-empty\n",
                encoding="utf-8",
            )
            payload = {"nftables": [
                {"map": {"name": "user_class", "elem": [
                    ["10.7.0.2", "512"], ["10.7.0.3", "513"],
                ]}},
                {"map": {"name": "class_egress", "elem": [
                    ["512", "512"], ["513", "513"],
                ]}},
            ]}
            calls = []

            def fake_run(argv, *, input_text=""):
                calls.append((argv, input_text))
                if argv[:3] == ["nft", "-j", "list"]:
                    return mock.Mock(returncode=0, stdout=json.dumps(payload))
                if argv[:3] == ["ip", "-j", "rule"]:
                    return mock.Mock(returncode=0, stdout="[]")
                if argv[:4] == ["ip", "-j", "route", "show"]:
                    return mock.Mock(returncode=0, stdout="[]")
                return mock.Mock(returncode=0, stdout="")

            with mock.patch.object(module, "USERS", users_path), \
                 mock.patch.object(module, "EGRESS", egress_path), \
                 mock.patch.object(module, "run", side_effect=fake_run), \
                 mock.patch.object(module, "replace_rule"), \
                 mock.patch.object(module, "_core_primary_projection_exact", return_value={"ok": True}):
                result = module.core_primary_stable_class_migrate()

            self.assertEqual(result["status"], "CORE_PRIMARY_STABLE_CLASS_MIGRATION_PASS")
            text = egress_path.read_text(encoding="utf-8")
            self.assertIn("id=source enabled=1 interface=wg-source core_primary_mark=0x200 core_primary_table=200", text)
            self.assertIn("id=target enabled=1 interface=wg-target core_primary_mark=0x201 core_primary_table=201", text)
            self.assertIn("id=empty enabled=1 interface=wg-empty core_primary_mark=0x202 core_primary_table=202", text)
            self.assertEqual(users_path.read_text(encoding="utf-8"),
                             "ip=10.7.0.2 current=source enabled=1\n"
                             "ip=10.7.0.3 current=target enabled=1\n")
            batches = [text for argv, text in calls if argv == ["nft", "-f", "-"]]
            self.assertEqual(len(batches), 1)
            self.assertIn("class_egress { 0x202 : 0x202 }", batches[0])

    def test_stable_migration_rolls_back_before_publishing_registry_on_projection_failure(self):
        loader = importlib.machinery.SourceFileLoader(
            "v7_routing_sync_stable_migration_rollback", str(SCRIPT),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            users_path = root / "users.registry"
            egress_path = root / "egress.registry"
            users_path.write_text("ip=10.7.0.2 current=source enabled=1\n", encoding="utf-8")
            original = (
                "id=source enabled=1 interface=wg-source\n"
                "id=empty enabled=1 interface=wg-empty\n"
            )
            egress_path.write_text(original, encoding="utf-8")
            payload = {"nftables": [
                {"map": {"name": "user_class", "elem": [["10.7.0.2", "512"]]}},
                {"map": {"name": "class_egress", "elem": [["512", "512"]]}},
            ]}
            calls = []

            def fake_run(argv, *, input_text=""):
                calls.append((argv, input_text))
                if argv[:3] == ["nft", "-j", "list"]:
                    return mock.Mock(returncode=0, stdout=json.dumps(payload))
                if argv[:3] == ["ip", "-j", "rule"] or argv[:4] == ["ip", "-j", "route", "show"]:
                    return mock.Mock(returncode=0, stdout="[]")
                if argv[:4] == ["ip", "rule", "del", "pref"]:
                    return mock.Mock(returncode=1, stdout="")
                return mock.Mock(returncode=0, stdout="")

            with mock.patch.object(module, "USERS", users_path), \
                 mock.patch.object(module, "EGRESS", egress_path), \
                 mock.patch.object(module, "run", side_effect=fake_run), \
                 mock.patch.object(module, "replace_rule"), \
                 mock.patch.object(module, "_core_primary_projection_exact", return_value={"ok": False}):
                result = module.core_primary_stable_class_migrate()

            self.assertEqual(result["status"], "STOP_SAFE")
            self.assertEqual(egress_path.read_text(encoding="utf-8"), original)
            batches = [text for argv, text in calls if argv == ["nft", "-f", "-"]]
            self.assertEqual(len(batches), 2)
            self.assertIn("add element", batches[0])
            self.assertIn("delete element", batches[1])


if __name__ == "__main__":
    unittest.main()
