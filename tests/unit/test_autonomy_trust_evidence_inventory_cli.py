import importlib.machinery
import importlib.util
import argparse
import json
import subprocess
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
    def test_live_packet_discovery_binds_genuine_candidate_identity(self):
        module = load_cli_module()
        payload = {
            "stop_reason": "AUTHORITY_BOUNDARY",
            "packet_preview": {
                "status": "PACKET_PREVIEW_READY",
                "allowed_users": ["10.0.0.2"],
                "allowed_targets": ["awg3"],
            },
            "candidate": {
                "execution_candidate": True,
                "review_required": False,
                "user": "10.0.0.2",
                "recommended_channel": "awg3",
                "reason_summary": ["higher suitability"],
            },
        }
        original = module.subprocess.run
        module.subprocess.run = lambda *_args, **_kwargs: subprocess.CompletedProcess([], 0, json.dumps(payload), "")
        try:
            result = module.discover_live_packet_preview(argparse.Namespace(
                state_dir="/state",
                event_dir="/events",
                snapshot_root="",
                audit_dir="",
            ))
        finally:
            module.subprocess.run = original

        self.assertTrue(result["genuine_production_candidate"])
        self.assertTrue(result["packet_preview"]["_v7_genuine_production_candidate"])

    def test_terminal_observation_consumes_finished_lease_and_live_route_verification(self):
        module = load_cli_module()
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "users.registry").write_text("ip=10.0.0.3 current=vless enabled=1\n", encoding="utf-8")
            (state_dir / "operator-execution-lease.json").write_text(json.dumps({
                "status": "EXECUTION_FINISHED",
                "operation_id": "runtime_autoswitch_observed",
                "packet_id": "pkt_observed",
                "finished_at": "2026-07-19T00:00:00+00:00",
                "immutable_packet_identity": {
                    "operation_id": "govdry_observed",
                    "packet_id": "pkt_observed",
                    "decision_id": "decision_observed",
                    "snapshot_bundle_hash": "snapshot_observed",
                    "user": "10.0.0.3",
                    "source": "awg3",
                    "target": "vless",
                },
            }), encoding="utf-8")
            original = module.subprocess.run
            module.subprocess.run = lambda *_args, **_kwargs: subprocess.CompletedProcess([], 0, "OK", "")
            try:
                row = module.terminal_execution_observation(state_dir, verify_routes=True)
            finally:
                module.subprocess.run = original

        self.assertEqual(row["evidence_class"], "CONTROLLED_PRODUCTION")
        self.assertTrue(row["verification_result"]["verification_passed"])
        self.assertTrue(row["delayed_1h_observation"])
        self.assertEqual(row["decision_trace_id"], "decision_observed")
        self.assertEqual(row["input_snapshot_identity"], "snapshot_observed")

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
