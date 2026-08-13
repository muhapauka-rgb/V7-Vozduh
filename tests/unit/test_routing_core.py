from copy import deepcopy
from datetime import datetime, timezone
import unittest

from admin_core.routing_core import (
    RoutingCoreContractError,
    bounded_class_bucket_commit,
    prepare_semantic_classes,
    run_shadow,
)


NOW = datetime(2026, 8, 13, 7, 30, tzinfo=timezone.utc)


def envelope():
    return {
        "schema": "v7.routing-core-input.v1",
        "generation": "failure-1",
        "observed_at": "2026-08-13T07:29:59.900000+00:00",
        "max_age_ms": 1000,
        "scope": {"source": "vless", "users": ["u2", "u1"]},
        "assignments": {"u1": "vless", "u2": "vless"},
        "targets": {
            "awg2": {"healthy": True, "capacity": 10, "assigned": 1},
            "awg1": {"healthy": True, "capacity": 10, "assigned": 1},
            "bad": {"healthy": False, "capacity": 100, "assigned": 0},
        },
        "policy": {
            "generation": "policy-1",
            "allowed_targets": ["awg2", "awg1"],
            "capacity_reserve": 1,
        },
        "authority": {
            "generation": "authority-1",
            "permitted_users": ["u1", "u2"],
            "max_users": 2,
        },
        "operation": {
            "id": "op-1",
            "lease_id": "lease-1",
            "fencing_token": "fence-1",
            "idempotency_key": "idem-1",
        },
    }


class RoutingCoreShadowTests(unittest.TestCase):
    def test_shadow_is_deterministic_and_effect_free(self):
        source = envelope()
        original = deepcopy(source)
        first = run_shadow(source, now=NOW)
        second = run_shadow(source, now=NOW)
        self.assertEqual(source, original)
        self.assertEqual(first["decision"], second["decision"])
        self.assertEqual(first["decision_fingerprint"], second["decision_fingerprint"])
        self.assertEqual(first["effects"], "ZERO")
        self.assertFalse(first["apply"]["apply_executed"])
        self.assertEqual(first["apply"]["users_moved"], 0)

    def test_tie_break_is_stable(self):
        result = run_shadow(envelope(), now=NOW)
        self.assertEqual([row["user"] for row in result["decision"]["moves"]], ["u1", "u2"])
        self.assertEqual({row["target"] for row in result["decision"]["moves"]}, {"awg1"})

    def test_stale_input_stops_safe(self):
        row = envelope()
        row["observed_at"] = "2026-08-13T07:29:00+00:00"
        with self.assertRaisesRegex(RoutingCoreContractError, "STALE_INPUT_STOP_SAFE"):
            run_shadow(row, now=NOW)

    def test_missing_fence_stops_safe(self):
        row = envelope()
        row["operation"]["fencing_token"] = ""
        with self.assertRaisesRegex(RoutingCoreContractError, "MISSING_FENCING_TOKEN"):
            run_shadow(row, now=NOW)

    def test_authority_scope_mismatch_stops_safe(self):
        row = envelope()
        row["authority"]["permitted_users"] = ["u1"]
        with self.assertRaisesRegex(RoutingCoreContractError, "AUTHORITY_SCOPE_MISMATCH_STOP_SAFE"):
            run_shadow(row, now=NOW)

    def test_unhealthy_and_disallowed_targets_are_excluded(self):
        row = envelope()
        row["policy"]["allowed_targets"] = ["bad"]
        result = run_shadow(row, now=NOW)
        self.assertEqual(result["decision"], {"decision": "STOP_SAFE_NO_LAWFUL_TARGET", "moves": []})

    def test_insufficient_capacity_stops_without_partial_plan(self):
        row = envelope()
        row["targets"]["awg1"] = {"healthy": True, "capacity": 2, "assigned": 0}
        row["targets"]["awg2"] = {"healthy": False, "capacity": 10, "assigned": 0}
        result = run_shadow(row, now=NOW)
        self.assertEqual(result["decision"], {"decision": "STOP_SAFE_INSUFFICIENT_CAPACITY", "moves": []})

    def test_engineering_plane_input_is_forbidden(self):
        row = envelope()
        row["omp"] = {"next_action": "anything"}
        with self.assertRaisesRegex(RoutingCoreContractError, "FORBIDDEN_ENGINEERING_INPUT:omp"):
            run_shadow(row, now=NOW)

    def test_10k_users_50_egresses_prepare_then_bounded_commit(self):
        assignments = {}
        for index in range(10_000):
            bucket = index % 50
            assignments[f"user-{index}"] = {
                "source_channel": f"egress-{bucket}",
                "service_compatibility": "global",
                "policy_set": "default",
                "eligible_target_bucket": f"bucket-{(bucket + 1) % 50}",
                "path_fingerprint": f"path-{bucket}",
                "correlation_domain": f"domain-{bucket}",
                "exception_boundary": "none",
            }
        prepared = prepare_semantic_classes(assignments, generation="scale-generation")
        self.assertEqual(prepared["input_member_count"], 10_000)
        self.assertEqual(prepared["class_count"], 50)
        selected = prepared["classes"][0]
        result = bounded_class_bucket_commit(
            prepared, class_id=selected["class_id"], expected_generation="scale-generation",
            expected_projection_fingerprint=prepared["projection_fingerprint"],
            target_bucket="target-bucket", target_generation="target-generation",
            capacity_available=selected["member_count"],
        )
        self.assertEqual(result["status"], "CLASS_BUCKET_COMMIT_READY")
        self.assertEqual(result["member_rows_scanned_in_hot_path"], 0)
        self.assertEqual(result["per_user_writes_requested"], 0)
        self.assertFalse(result["raw_members_loaded_in_hot_path"])


if __name__ == "__main__":
    unittest.main()
