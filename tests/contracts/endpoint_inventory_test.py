import json
import py_compile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "docs" / "track5" / "endpoint-inventory.json"
FIXTURES = ROOT / "tests" / "contracts" / "fixtures"
ADMIN_API = ROOT / "admin" / "v7-admin-api"
EXPECTED_SUMMARY = {
    "endpoint_count": 211,
    "by_method": {
        "GET": 66,
        "HEAD": 8,
        "POST": 137,
    },
    "by_auth": {
        "public": 19,
        "required": 192,
    },
    "csrf_required_count": 132,
    "safe_mode_blocked_count": 86,
}


def load_inventory():
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def endpoint(data, method, path):
    for item in data["endpoints"]:
        if item["method"] == method and item["path"] == path:
            return item
    raise AssertionError(f"endpoint not found: {method} {path}")


class EndpointInventoryContractTest(unittest.TestCase):
    def test_admin_api_still_compiles(self):
        py_compile.compile(str(ADMIN_API), cfile="/private/tmp/v7-admin-api-contract.pyc", doraise=True)

    def test_inventory_shape_and_counts(self):
        data = load_inventory()
        self.assertEqual(data["schema_version"], 1)
        self.assertGreater(data["source_line_count"], 0)
        self.assertEqual(data["summary"]["endpoint_count"], EXPECTED_SUMMARY["endpoint_count"])
        self.assertEqual(data["summary"]["by_method"], EXPECTED_SUMMARY["by_method"])
        self.assertEqual(data["summary"]["by_auth"], EXPECTED_SUMMARY["by_auth"])
        self.assertEqual(data["summary"]["csrf_required_count"], EXPECTED_SUMMARY["csrf_required_count"])
        self.assertEqual(data["summary"]["safe_mode_blocked_count"], EXPECTED_SUMMARY["safe_mode_blocked_count"])
        self.assertIn("critical", data["summary"]["by_risk"])

    def test_required_readonly_endpoints_are_frozen(self):
        data = load_inventory()
        expected = {
            "/health": ("public", "low"),
            "/api/session": ("required", "low"),
            "/api/overview": ("required", "medium"),
            "/api/operator/overview": ("required", "low"),
            "/api/operator/targets": ("required", "low"),
            "/api/operator/operations": ("required", "low"),
            "/api/operator/evidence": ("required", "low"),
            "/api/operator/delayed-movement": ("required", "low"),
            "/api/operator/approval-preview": ("required", "low"),
            "/api/operator/approval-contracts": ("required", "low"),
            "/api/operator/rollback-preview": ("required", "low"),
            "/api/operator/timeline": ("required", "low"),
            "/api/operator/lineage": ("required", "low"),
            "/api/operator/runtime-verdicts": ("required", "low"),
            "/api/operator/operation-detail": ("required", "low"),
            "/api/operator/evidence-detail": ("required", "low"),
            "/api/operator/audit-search": ("required", "low"),
            "/api/operator/evidence-archive": ("required", "low"),
            "/api/operator/audit-export-preview": ("required", "low"),
            "/api/operator/execution-governance-preview": ("required", "low"),
            "/api/operator/execution-rehearsal-preview": ("required", "low"),
            "/api/operator/evidence-file-detail": ("required", "low"),
            "/api/events": ("required", "low"),
            "/api/diagnostics": ("required", "medium"),
        }
        for path, (auth, risk) in expected.items():
            with self.subTest(path=path):
                item = endpoint(data, "GET", path)
                self.assertEqual(item["auth"], auth)
                self.assertEqual(item["risk"], risk)
                self.assertEqual(item["response_type"], "json")
                self.assertFalse(item["csrf_required"])

    def test_fixture_specs_match_inventory(self):
        data = load_inventory()
        for fixture_path in sorted(FIXTURES.glob("*.json")):
            spec = json.loads(fixture_path.read_text(encoding="utf-8"))
            item = endpoint(data, spec["method"], spec["path"])
            self.assertEqual(item["auth"], spec["auth"])
            self.assertEqual(item["response_type"], spec["response_type"])
            for key in spec.get("authenticated_top_level_keys", []):
                self.assertIn(key, item["known_response_top_level_keys"])

    def test_mutating_actions_require_csrf_and_role(self):
        data = load_inventory()
        critical_paths = [
            "/api/actions/user-switch",
            "/api/actions/autoswitch-apply-guarded",
            "/api/actions/egress-draft-enable-apply",
            "/api/actions/policy-domain-add",
        ]
        for path in critical_paths:
            with self.subTest(path=path):
                item = endpoint(data, "POST", path)
                self.assertEqual(item["auth"], "required")
                self.assertTrue(item["csrf_required"])
                self.assertIn(item["role"], {"operator", "admin", "owner"})
                self.assertIn(item["risk"], {"high", "critical"})


if __name__ == "__main__":
    unittest.main()
