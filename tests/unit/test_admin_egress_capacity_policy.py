import importlib.machinery
import importlib.util
from pathlib import Path
import unittest


def load_admin_api():
    path = Path(__file__).resolve().parents[2] / "admin" / "v7-admin-api"
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_capacity_test", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class AdminEgressCapacityPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_api = load_admin_api()

    def test_empty_limits_do_not_materialize_legacy_one_two_cap(self):
        policy = self.admin_api.egress_usage_policy_from_data({})

        self.assertEqual(policy["soft_limit"], "")
        self.assertEqual(policy["hard_limit"], "")
        self.assertNotIn("soft_limit=", self.admin_api.egress_usage_policy_registry_part(policy))
        self.assertNotIn("hard_limit=", self.admin_api.egress_usage_policy_registry_part(policy))

    def test_explicit_limits_are_preserved(self):
        policy = self.admin_api.egress_usage_policy_from_data({"soft_limit": "8", "hard_limit": "12"})

        self.assertEqual(policy["soft_limit"], "8")
        self.assertEqual(policy["hard_limit"], "12")
        part = self.admin_api.egress_usage_policy_registry_part(policy)
        self.assertIn("soft_limit=8", part)
        self.assertIn("hard_limit=12", part)

    def test_zero_clears_explicit_capacity_limit(self):
        policy = self.admin_api.egress_usage_policy_from_data({"soft_limit": "0", "hard_limit": "0"})

        self.assertEqual(policy["soft_limit"], "")
        self.assertEqual(policy["hard_limit"], "")

    def test_missing_registry_limit_means_uncapped_not_legacy_default(self):
        self.assertEqual(self.admin_api.egress_registry_load_limit({}, "soft_limit", 1), 0)
        self.assertEqual(self.admin_api.egress_registry_load_limit({}, "hard_limit", 2), 0)
        self.assertEqual(self.admin_api.egress_registry_load_limit({"hard_limit": "2"}, "hard_limit", 0), 2)


if __name__ == "__main__":
    unittest.main()
