"""N5/N6 pre-ready target and fair staggered DEEP contracts."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from admin_core.routing_core import bounded_class_bucket_commit, prepare_semantic_classes


ROOT = Path(__file__).resolve().parents[2]


def load_tool(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class V53PreReadyAndStaggeredDeepTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.autoswitch = load_tool(
            "v7_autoswitch_n5_test", ROOT / "tools/v7-users-autoswitch",
        )
        cls.refresh = load_tool(
            "v7_matrix_n6_test", ROOT / "tools/v7-service-matrix-refresh-all",
        )

    @staticmethod
    def generation() -> dict:
        return {
            "planner_generation_id": "planner-generation",
            "inputs": {
                "users_registry": "users-generation",
                "egress_registry": "egress-generation",
                "policy": "policy-generation",
                "org_policy": "org-generation",
                "service_preferences": "service-generation",
            },
            "volatile_inputs": {
                "service_matrix": "matrix-generation",
                "egress_speed": "capacity-generation",
                "autoswitch_safety": "safety-generation",
            },
        }

    def test_n5_reuses_planner_top_h_and_deduplicates_1000_users(self):
        candidates = [
            {
                "egress": f"target-{index}", "eligible": True,
                "score": 100 - index, "role": "GLOBAL_FAST",
                "capacity_decision": {"status": "AVAILABLE"},
                "canary_reserved": False,
            }
            for index in range(6)
        ]
        candidates[-1]["canary_reserved"] = True
        decisions = [
            {
                "user_ip": f"10.7.{index // 250}.{index % 250 + 1}",
                "current_egress": "source-a",
                "recommended_egress": "target-0",
                "important_services": ["telegram", "google"],
                "candidates": candidates,
            }
            for index in range(1000)
        ]
        projection = self.autoswitch.build_prepared_class_decision_projection({
            "updated": "2026-08-23T12:00:00+00:00",
            "operation": {"operation_id": ""},
            "safety": {"generation": self.generation()},
            "decisions": decisions,
        })

        self.assertEqual(projection["class_count"], 1)
        prepared = projection["classes"][0]
        self.assertEqual(prepared["member_count"], 1000)
        self.assertEqual(prepared["hot_target_count"], 4)
        self.assertEqual(
            [row["target_id"] for row in prepared["hot_targets"]],
            ["target-0", "target-1", "target-2", "target-3"],
        )
        self.assertEqual(
            projection["hot_target_set"]["deduplicated_target_service_contract_count"],
            4,
        )
        self.assertNotIn("10.7.0.1", json.dumps(projection))
        self.assertFalse(projection["hot_target_set"]["incident_time_world_model_rebuild"])

    def test_n5_fact_specific_generation_change_stops_safe(self):
        plan = {
            "safety": {"generation": self.generation()},
            "decisions": [{
                "user_ip": "10.7.0.5", "current_egress": "source-a",
                "recommended_egress": "target-a",
                "important_services": ["telegram"],
            }],
        }
        projection = self.autoswitch.build_prepared_class_decision_projection(plan)
        current = dict(projection["invalidators"])
        current["capacity_reservation_generation"] = "changed"
        result = self.autoswitch.validate_prepared_class_decision_projection(
            projection, current,
        )

        self.assertEqual(result["status"], "PREPARED_CLASS_DECISION_STALE")
        self.assertEqual(
            result["invalidation_reasons"],
            ["capacity_reservation_generation"],
        )
        self.assertFalse(result["fact_specific_freshness"]["capacity"]["fresh"])
        self.assertTrue(result["fact_specific_freshness"]["identity_and_role"]["fresh"])

    def test_n5_no_official_target_is_explicit_no_3s_capacity(self):
        projection = self.autoswitch.build_prepared_class_decision_projection({
            "safety": {"generation": self.generation()},
            "decisions": [],
        })
        result = self.autoswitch.validate_prepared_class_decision_projection(
            projection, projection["invalidators"],
        )
        self.assertEqual(projection["hot_target_set"]["current_state"], "NO_3S_TARGET_CAPACITY")
        self.assertTrue(result["no_3s_target_capacity"])

    def test_n5_prepared_dataplane_hot_commit_is_member_count_independent(self):
        for count in (1, 10, 100, 1000):
            with self.subTest(count=count):
                semantic = {
                    "source_channel": "source-a",
                    "service_compatibility": "telegram+google",
                    "policy_set": "default",
                    "eligible_target_bucket": "target-a",
                    "path_fingerprint": "path-a",
                    "correlation_domain": "domain-a",
                    "exception_boundary": "none",
                }
                prepared = prepare_semantic_classes(
                    {f"user-{index}": semantic for index in range(count)},
                    generation=f"generation-{count}",
                )
                selected = prepared["classes"][0]
                commit = bounded_class_bucket_commit(
                    prepared,
                    class_id=selected["class_id"],
                    expected_generation=f"generation-{count}",
                    expected_projection_fingerprint=prepared["projection_fingerprint"],
                    target_bucket="target-a",
                    target_generation="target-generation",
                    capacity_available=count,
                )
                self.assertEqual(commit["status"], "CLASS_BUCKET_COMMIT_READY")
                self.assertEqual(commit["member_rows_scanned_in_hot_path"], 0)
                self.assertEqual(commit["per_user_writes_requested"], 0)

    def test_n6_every_inventory_row_has_one_fair_slot_at_1000(self):
        rows = [{"id": f"egress-{index:04d}", "enabled": "1"} for index in range(1000)]
        selected_sets = []
        for slot in range(15):
            selected, schedule = self.refresh.select_staggered_deep_rows(
                rows, {"items": {}}, now_epoch=float(slot * 60),
                horizon_seconds=900, slot_seconds=60,
            )
            selected_sets.append({row["id"] for row in selected})
            self.assertLessEqual(len(selected), 67)
            self.assertEqual(schedule["maximum_slice_size"], 67)
            self.assertEqual(schedule["missed_horizon_behavior"], "REMAIN_STALE_NO_CATCH_UP_BURST")
        self.assertEqual(len(set().union(*selected_sets)), 1000)
        self.assertEqual(sum(len(rows) for rows in selected_sets), 1000)

    def test_n6_stale_rows_do_not_create_catch_up_burst(self):
        rows = [{"id": f"egress-{index:03d}", "enabled": "1"} for index in range(100)]
        ancient = "2026-08-23T00:00:00+00:00"
        matrix = {"items": {row["id"]: {"checked_at": ancient} for row in rows}}
        now_epoch = datetime(2026, 8, 23, 12, 0, tzinfo=timezone.utc).timestamp()
        selected, schedule = self.refresh.select_staggered_deep_rows(
            rows, matrix, now_epoch=now_epoch,
            horizon_seconds=900, slot_seconds=60,
        )
        self.assertEqual(schedule["stale_count"], 100)
        self.assertLessEqual(len(selected), 7)
        self.assertEqual(schedule["selected_count"], len(selected))
        self.assertFalse(schedule["new_state_store_created"])

    def test_n7_prepared_hot_target_mode_runs_only_planner_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            (state / "egress.registry").write_text(
                "id=source-a interface=source enabled=1\n"
                "id=target-a interface=target enabled=1\n"
                "id=unrelated interface=unused enabled=1\n",
                encoding="utf-8",
            )
            projection = self.autoswitch.build_prepared_class_decision_projection({
                "updated": "2026-08-23T12:00:00+00:00",
                "operation": {"operation_id": ""},
                "safety": {"generation": self.generation()},
                "decisions": [{
                    "user_ip": "10.7.0.5", "current_egress": "source-a",
                    "recommended_egress": "target-a",
                    "important_services": ["telegram", "google"],
                }],
            })
            projection_file = root / "projection.json"
            projection_file.write_text(json.dumps({
                "prepared_class_decisions": projection,
            }), encoding="utf-8")
            argv = [
                str(ROOT / "tools/v7-service-matrix-refresh-all"),
                "--state-dir", str(state),
                "--prepared-hot-targets", "--matrix-observation-only",
                "--prepared-projection-file", str(projection_file),
            ]
            output = io.StringIO()
            with mock.patch.object(sys, "argv", argv), mock.patch.object(
                self.refresh, "run_one",
                return_value={"egress": "target-a", "ok": True, "status": "OK"},
            ) as run_one, contextlib.redirect_stdout(output):
                self.assertEqual(self.refresh.main(), 0)
            payload = json.loads(output.getvalue())

        self.assertEqual(payload["mode"], "PREPARED_HOT_TARGET_OBSERVATION_ONLY")
        self.assertEqual(payload["prepared_hot_target_scope"]["selected_targets"], ["target-a"])
        self.assertEqual(run_one.call_count, 1)
        self.assertEqual(run_one.call_args.args[0], "target-a")
        self.assertEqual(run_one.call_args.args[4], "google,telegram")
        self.assertFalse(payload["observation_only"]["routing_mutation_performed"])


if __name__ == "__main__":
    unittest.main()
