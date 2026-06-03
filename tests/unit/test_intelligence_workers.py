import json
import tempfile
import unittest
from pathlib import Path

from admin_core import intelligence_workers as workers
from admin_core.intelligence_snapshots import read_snapshot_family, validate_snapshot


GENERATED = "2026-06-03T10:00:00+00:00"


def service_matrix():
    return {
        "updated": GENERATED,
        "items": {
            "awg0": {
                "services": {
                    "telegram": {"ok": True, "status": "OK", "first_byte_sec": 0.2, "confidence": 0.9, "score": 90, "sample_count": 4},
                    "chatgpt": {"ok": True, "status": "OK", "first_byte_sec": 0.4, "confidence": 0.8, "score": 80, "sample_count": 4},
                }
            },
            "vless": {
                "services": {
                    "telegram": {"ok": False, "status": "FAIL", "first_byte_sec": 3.0, "confidence": 0.4, "score": 20, "sample_count": 4},
                    "chatgpt": {"ok": True, "status": "OK", "first_byte_sec": 0.5, "confidence": 0.8, "score": 82, "sample_count": 4},
                }
            },
        },
    }


def quality_summary():
    return {
        "updated": GENERATED,
        "items": {
            "awg0": {"windows": {"1h": {"avg_mbps": 100, "fail_rate": 0.01, "stability": 0.95, "samples": 20}}},
            "vless": {"windows": {"1h": {"avg_mbps": 50, "fail_rate": 0.2, "stability": 0.65, "samples": 20}}},
        },
    }


class IntelligenceWorkersTest(unittest.TestCase):
    def test_service_score_worker_outputs_valid_service_and_channel_snapshots(self):
        result = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        self.assertIn("service-scores", result)
        self.assertIn("channel-service-scores", result)
        for name, payload in result.items():
            validation = validate_snapshot(payload, name)
            self.assertTrue(validation.ok, validation.errors)
            self.assertEqual(payload["generator"], workers.GENERATOR)
            self.assertGreater(payload["item_count"], 0)
        channel_items = result["channel-service-scores"]["items"]
        awg0 = next(row for row in channel_items if row["channel"] == "awg0")
        vless = next(row for row in channel_items if row["channel"] == "vless")
        self.assertGreater(awg0["aggregate_score"], vless["aggregate_score"])

    def test_trust_worker_is_bounded_and_valid(self):
        records = [{"result": "success", "blast_radius": 1} for _ in range(workers.MAX_HISTORY_RECORDS + 20)]
        records.append({"result": "failed", "rollback_failed": True})
        payload = workers.build_trust_snapshot(audit_records=records, generated_at=GENERATED)
        validation = validate_snapshot(payload, "trust-summaries")
        self.assertTrue(validation.ok, validation.errors)
        item = payload["items"][0]
        self.assertTrue(item["bounded"])
        self.assertEqual(item["records_seen"], workers.MAX_HISTORY_RECORDS)
        self.assertIn("history_records_truncated_to_bound", payload["warnings"])

    def test_risk_worker_uses_service_snapshots(self):
        service = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        risk = workers.build_risk_snapshot(
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(risk, "risk-summaries").ok)
        summary = risk["items"][0]
        self.assertGreater(summary["service_risk"], 0)
        self.assertIn("vless", summary["high_risk_channels"])

    def test_blast_radius_worker_reuses_trust_and_risk_models(self):
        trust = workers.build_trust_snapshot(audit_records=[{"result": "success"}] * 20, generated_at=GENERATED)
        risk = workers.build_risk_snapshot(
            service_scores_snapshot={"items": [{"average_score": 90}], "confidence": 1.0},
            channel_service_scores_snapshot={"items": [{"channel": "awg0", "aggregate_score": 90, "verdict": "OK"}], "confidence": 1.0},
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        blast = workers.build_blast_radius_snapshot(
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            total_users=2000,
            affected_candidates=50,
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(blast, "blast-radius-summaries").ok)
        rec = blast["items"][0]["recommendation"]
        self.assertLessEqual(rec["recommended_budget"], 25)
        self.assertEqual(rec["runtime_decision_authority"], "none_shadow_only")

    def test_overview_worker_outputs_admin_only_summary(self):
        overview = workers.build_overview_snapshot(
            runtime_state={"egress": {"awg0": {"code": "200"}}},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}, {"ip": "10.7.0.3", "enabled": "0"}],
            egress_registry=[{"id": "awg0"}],
            snapshot_statuses={"service-scores": {"freshness_state": "FRESH", "runtime_behavior": "ALLOW"}},
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(overview, "overview-summary").ok)
        self.assertEqual(overview["summary"]["users_total"], 2)
        self.assertEqual(overview["summary"]["users_active"], 1)
        self.assertEqual(overview["summary"]["snapshot_families_fresh"], 1)

    def test_all_worker_generates_and_writes_readable_snapshots(self):
        result = workers.build_all_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            audit_records=[{"result": "success"}],
            runtime_state={"egress": {"awg0": {}}},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            egress_registry=[{"id": "awg0"}],
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        self.assertIn("service-scores", result.snapshots)
        self.assertIn("overview-summary", result.snapshots)
        self.assertGreater(result.metrics["snapshot_count"], 0)
        with tempfile.TemporaryDirectory() as tmp:
            written = workers.write_snapshots(Path(tmp), result.snapshots)
            self.assertIn("service-scores", written)
            read = read_snapshot_family(Path(tmp), "service-scores")
        self.assertTrue(read.validation.ok)

    def test_missing_inputs_fail_safely_with_warnings(self):
        result = workers.build_all_snapshots(
            service_matrix={"items": {}},
            quality_summary={"items": {}},
            service_preferences={},
            audit_records=[],
            runtime_state={},
            users_registry=[],
            egress_registry=[],
            generated_at=GENERATED,
        )
        self.assertIn("service_matrix_missing_or_empty", result.snapshots["service-scores"]["warnings"])
        self.assertIn("history_missing", result.snapshots["trust-summaries"]["warnings"])
        self.assertIn("runtime_state_missing", result.snapshots["overview-summary"]["warnings"])
        for name, payload in result.snapshots.items():
            self.assertTrue(validate_snapshot(payload, name).ok)

    def test_jsonl_tail_reader_bounds_history_and_skips_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.jsonl"
            path.write_text(
                "\n".join([json.dumps({"idx": i}) for i in range(20)] + ["broken"]),
                encoding="utf-8",
            )
            rows = workers.read_jsonl_tail(path, limit=5)
        self.assertEqual([row["idx"] for row in rows], [15, 16, 17, 18, 19])

    def test_worker_architecture_forbids_runtime_authority(self):
        architecture = workers.worker_architecture()
        forbidden = set(architecture["forbidden"])
        self.assertIn("user movement", forbidden)
        self.assertIn("runtime actions", forbidden)
        self.assertEqual(architecture["runtime_integration"], "none_in_PERF3")


if __name__ == "__main__":
    unittest.main()
