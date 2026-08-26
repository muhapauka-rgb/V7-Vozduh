import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_admin_api():
    loader = importlib.machinery.SourceFileLoader(
        "v7_admin_api_service_preferences_lifecycle", str(ADMIN_API),
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class AdminServicePreferencesLifecycleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin = load_admin_api()

    def test_certification_profile_can_be_removed_without_empty_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            prefs = Path(tmp) / "service-preferences.json"
            prefs.write_text(json.dumps({
                "enabled": True,
                "users": {"10.7.0.5": {"services": ["telegram"]}},
            }), encoding="utf-8")
            previous = self.admin.SERVICE_PREFS_FILE
            self.addCleanup(setattr, self.admin, "SERVICE_PREFS_FILE", previous)
            self.admin.SERVICE_PREFS_FILE = prefs

            created = self.admin.update_service_preferences(
                "certification-owner", user_ip="10.7.0.124", services=["telegram"],
            )
            self.assertEqual(created["users"]["10.7.0.124"]["services"], ["telegram"])

            restored = self.admin.update_service_preferences(
                "certification-owner", user_ip="10.7.0.124", clear_user=True,
            )
            self.assertNotIn("10.7.0.124", restored["users"])
            self.assertEqual(restored["users"]["10.7.0.5"]["services"], ["telegram"])
            persisted = json.loads(prefs.read_text(encoding="utf-8"))
            self.assertNotIn("10.7.0.124", persisted["users"])


if __name__ == "__main__":
    unittest.main()
