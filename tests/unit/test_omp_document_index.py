import importlib.machinery
import importlib.util
from pathlib import Path
import unittest


def load_admin_api():
    path = Path(__file__).resolve().parents[2] / "admin" / "v7-admin-api"
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_omp_document_index_test", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class OmpDocumentIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_api = load_admin_api()

    def test_document_index_contains_core_operator_files(self):
        response = self.admin_api.omp_dashboard_response()
        index = response.get("document_index") or {}
        paths = {entry.get("path") for entry in index.get("entries", [])}

        self.assertIn("docs/programs/OPERATIONAL_MATURITY_PROGRAM.md", paths)
        self.assertIn("docs/programs/V7_CURRENT_PROGRAM_STATE.md", paths)
        self.assertIn("docs/reference/SYSTEM_MAP.md", paths)
        self.assertIn("docs/reference/V7_CANONICAL_REFERENCE.md", paths)
        self.assertEqual(index.get("source"), "docs/reference/V7_OPERATOR_FILE_MEMO.md")


if __name__ == "__main__":
    unittest.main()

