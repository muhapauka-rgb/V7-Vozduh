import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def load_cli_module():
    path = Path(__file__).resolve().parents[2] / "tools" / "v7-autonomy-trust-evidence-inventory"
    loader = importlib.machinery.SourceFileLoader("v7_autonomy_trust_evidence_inventory", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class AutonomyTrustEvidenceInventoryCliTest(unittest.TestCase):
    def test_event_reader_consumes_actual_date_partitioned_owner_files(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            event_dir = Path(tmp)
            (event_dir / "telegram-sentinel-20260719.jsonl").write_text(
                json.dumps({"kind": "natural-sentinel"}) + "\n",
                encoding="utf-8",
            )
            (event_dir / "service-matrix-refresh-20260719.jsonl").write_text(
                json.dumps({"kind": "service-matrix"}) + "\n",
                encoding="utf-8",
            )
            rows = module.event_rows(event_dir, 5000)

        self.assertEqual({row["kind"] for row in rows}, {"natural-sentinel", "service-matrix"})


if __name__ == "__main__":
    unittest.main()
