import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from admin_core import intelligence_snapshots as snapshots


NOW = datetime(2026, 6, 3, 10, 0, 0, tzinfo=timezone.utc)


class IntelligenceSnapshotsTest(unittest.TestCase):
    def write_snapshot(self, root: Path, family: str, payload: dict):
        path = snapshots.snapshot_path(root, family)
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def base_payload(self, family: str, generated_at="2026-06-03T09:59:30+00:00", **kwargs):
        payload = snapshots.build_snapshot_envelope(
            family,
            generated_at=generated_at,
            source_hashes={"source": "abc"},
            generator="unit-test",
            item_count=1,
            content=[{"id": "x"}],
        )
        payload.update(kwargs)
        return payload

    def test_snapshot_contracts_define_required_families(self):
        contracts = snapshots.snapshot_family_contracts()
        self.assertIn("service-scores", contracts)
        self.assertIn("channel-service-scores", contracts)
        self.assertIn("user-service-scores", contracts)
        self.assertIn("risk-summaries", contracts)
        self.assertIn("trust-summaries", contracts)
        self.assertIn("blast-radius-summaries", contracts)
        self.assertIn("candidate-suitability-summary", contracts)
        self.assertIn("best-available-pool", contracts)
        self.assertIn("capacity-forecast-summaries", contracts)
        self.assertIn("prediction-summaries", contracts)
        self.assertIn("trust-evolution-summaries", contracts)
        self.assertIn("overview-summary", contracts)
        envelope = snapshots.snapshot_envelope_schema()
        self.assertIn("generated_at", envelope["required"])
        self.assertIn("confidence", envelope["required"])
        self.assertEqual(str(snapshots.CANONICAL_SNAPSHOT_ROOT), "/opt/v7/egress/state/intelligence")

    def test_ri5_prediction_runtime_contract_is_advisory_only(self):
        contract = snapshots.runtime_read_contract()
        self.assertIn("prediction-summaries", contract["ri5_prediction_advisory_runtime_families"])
        self.assertIn("trust-evolution-summaries", contract["ri6_trust_evolution_advisory_runtime_families"])
        matrix = snapshots.stop_condition_matrix()
        self.assertEqual(matrix["prediction-summaries"]["LOW_CONFIDENCE"], "IGNORE")
        self.assertEqual(matrix["prediction-summaries"]["STALE"], "IGNORE")
        self.assertEqual(matrix["trust-evolution-summaries"]["LOW_CONFIDENCE"], "IGNORE")
        self.assertEqual(matrix["trust-evolution-summaries"]["STALE"], "IGNORE")

    def test_valid_snapshot_loads_as_fresh_and_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "service-scores", self.base_payload("service-scores"))
            result = snapshots.read_snapshot_family(root, "service-scores", now=NOW)
        self.assertTrue(result.exists)
        self.assertTrue(result.validation.ok)
        self.assertEqual(result.freshness_state, "FRESH")
        self.assertEqual(result.runtime_behavior, "ALLOW")
        self.assertFalse(result.stop_required)

    def test_missing_and_corrupt_snapshots_stop_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing = snapshots.read_snapshot_family(root, "risk-summaries", now=NOW)
            self.assertEqual(missing.freshness_state, "UNKNOWN")
            self.assertTrue(missing.stop_required)
            self.assertIn("missing_snapshot", missing.validation.errors)

            path = snapshots.snapshot_path(root, "risk-summaries")
            path.write_text("{broken", encoding="utf-8")
            corrupt = snapshots.read_snapshot_family(root, "risk-summaries", now=NOW)
        self.assertTrue(corrupt.stop_required)
        self.assertIn("snapshot_corrupt", corrupt.validation.errors)

    def test_expired_snapshot_stops_runtime(self):
        payload = self.base_payload("risk-summaries", generated_at="2026-06-03T09:00:00+00:00")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "risk-summaries", payload)
            result = snapshots.read_snapshot_family(root, "risk-summaries", now=NOW)
        self.assertEqual(result.freshness_state, "EXPIRED")
        self.assertEqual(result.runtime_behavior, "STOP")
        self.assertTrue(result.stop_required)

    def test_stale_behavior_is_family_specific(self):
        service_payload = self.base_payload("service-scores", generated_at="2026-06-03T09:58:30+00:00")
        trust_payload = self.base_payload("trust-summaries", generated_at="2026-06-03T09:54:30+00:00")
        prediction_payload = self.base_payload("prediction-summaries", generated_at="2026-06-03T09:49:00+00:00")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "service-scores", service_payload)
            self.write_snapshot(root, "trust-summaries", trust_payload)
            self.write_snapshot(root, "prediction-summaries", prediction_payload)
            service = snapshots.read_snapshot_family(root, "service-scores", now=NOW)
            trust = snapshots.read_snapshot_family(root, "trust-summaries", now=NOW)
            prediction = snapshots.read_snapshot_family(root, "prediction-summaries", now=NOW)
        self.assertEqual(service.freshness_state, "STALE")
        self.assertEqual(service.runtime_behavior, "WARN")
        self.assertEqual(trust.freshness_state, "STALE")
        self.assertEqual(trust.runtime_behavior, "STOP")
        self.assertEqual(prediction.freshness_state, "STALE")
        self.assertEqual(prediction.runtime_behavior, "IGNORE")

    def test_unknown_freshness_stops_runtime(self):
        payload = self.base_payload("blast-radius-summaries", freshness_state="UNKNOWN")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "blast-radius-summaries", payload)
            result = snapshots.read_snapshot_family(root, "blast-radius-summaries", now=NOW)
        self.assertEqual(result.freshness_state, "UNKNOWN")
        self.assertTrue(result.stop_required)

    def test_confidence_validation_and_runtime_behavior(self):
        low_required = self.base_payload("risk-summaries", confidence=0.4)
        low_advisory = self.base_payload("prediction-summaries", confidence=0.4)
        invalid = self.base_payload("service-scores", confidence=2.0)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "risk-summaries", low_required)
            self.write_snapshot(root, "prediction-summaries", low_advisory)
            self.write_snapshot(root, "service-scores", invalid)
            required = snapshots.read_snapshot_family(root, "risk-summaries", now=NOW)
            advisory = snapshots.read_snapshot_family(root, "prediction-summaries", now=NOW)
            invalid_result = snapshots.read_snapshot_family(root, "service-scores", now=NOW)
        self.assertIn("confidence_below_family_floor", required.validation.warnings)
        self.assertEqual(required.runtime_behavior, "STOP")
        self.assertEqual(advisory.runtime_behavior, "IGNORE")
        self.assertFalse(invalid_result.validation.ok)
        self.assertIn("confidence_invalid", invalid_result.validation.errors)
        self.assertTrue(invalid_result.stop_required)

    def test_schema_validation_rejects_wrong_schema_and_bad_fields(self):
        payload = self.base_payload("service-scores")
        payload["schema"] = "wrong"
        payload["source_hashes"] = []
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "service-scores", payload)
            result = snapshots.read_snapshot_family(root, "service-scores", now=NOW)
        self.assertFalse(result.validation.ok)
        self.assertIn("schema_mismatch", result.validation.errors)
        self.assertIn("source_hashes_invalid", result.validation.errors)
        self.assertEqual(result.runtime_behavior, "STOP")

    def test_bundle_reader_is_bounded_to_requested_families(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "overview-summary", snapshots.build_snapshot_envelope(
                "overview-summary",
                generated_at="2026-06-03T09:59:45+00:00",
                source_hashes={"overview": "abc"},
                generator="unit-test",
                item_count=1,
                content={"status": "OK"},
            ))
            bundle = snapshots.read_snapshot_bundle(root, ["overview-summary"], now=NOW)
        self.assertEqual(list(bundle), ["overview-summary"])
        self.assertEqual(bundle["overview-summary"].freshness_state, "FRESH")

    def test_candidate_suitability_uses_its_explicit_cohort_size_budget(self):
        # The candidate snapshot is user-scoped and can legitimately exceed
        # the 1 MB default as the current cohort grows.  It still remains
        # bounded by the family-specific 2 MB cap.
        payload = self.base_payload(
            "candidate-suitability-summary",
            content=[{"user": "10.7.0.125", "evidence": "x" * 1_050_000}],
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "candidate-suitability-summary", payload)
            result = snapshots.read_snapshot_family(root, "candidate-suitability-summary", now=NOW)
            self.assertGreater(Path(result.path).stat().st_size, snapshots.MAX_SNAPSHOT_BYTES)
        self.assertTrue(result.validation.ok)
        self.assertEqual(result.runtime_behavior, "ALLOW")
        self.assertFalse(result.stop_required)

    def test_contracts_expose_runtime_stop_matrix_and_perf3_workers(self):
        runtime_contract = snapshots.runtime_read_contract()
        self.assertIn("raw history", runtime_contract["planner_must_never_read"])
        self.assertEqual(runtime_contract["planner_integration_status"], "integrated_in_PERF4_runtime_fast_path")
        self.assertIn("trust-summaries", runtime_contract["perf4_integrated_runtime_families"])
        self.assertIn("candidate-suitability-summary", runtime_contract["ri4_b_advisory_runtime_families"])
        self.assertIn("best-available-pool", runtime_contract["ri4_b_advisory_runtime_families"])
        self.assertIn("trust-evolution-summaries", runtime_contract["ri6_trust_evolution_advisory_runtime_families"])
        stop = snapshots.stop_condition_matrix()
        self.assertEqual(stop["risk-summaries"]["UNKNOWN"], "STOP")
        self.assertEqual(stop["blast-radius-summaries"]["EXPIRED"], "STOP")
        self.assertEqual(stop["candidate-suitability-summary"]["LOW_CONFIDENCE"], "IGNORE")
        recommendations = snapshots.perf3_worker_recommendations()
        self.assertFalse(recommendations["service-scores"]["writes_runtime_state"])
        self.assertFalse(recommendations["trust-evolution-summaries"]["writes_runtime_state"])
        self.assertIn("service-matrix.json", recommendations["service-scores"]["inputs_required"])
        self.assertIn("prediction-summaries.json", recommendations["trust-evolution-summaries"]["inputs_required"])


if __name__ == "__main__":
    unittest.main()
