from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_sync_lib_permanent_polygon_autonomous_test", ROOT / "tools/v7_sync_lib.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PermanentPolygonAutonomousProgramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        cls.supply = cls.lib.permanent_polygon_obligation_supply(cls.cps, root=ROOT)
        cls.u06_obligation = next(
            row for row in cls.supply["obligations"]
            if row["criterion_id"] == cls.lib.PERMANENT_POLYGON_CAP_U06_CRITERION_ID
        )
        cls.u06_consumption = cls.lib.consume_permanent_polygon_obligation(
            cls.u06_obligation, cps_text=cls.cps, root=ROOT,
        )
        cls.integration = cls.lib.execute_permanent_polygon_omp_integration(root=ROOT)

    def test_generic_dispatch_executes_live_u06_owner_chain(self):
        first = self.u06_consumption
        execution = first["execution"]
        self.assertEqual(first["criterion_id"], self.lib.PERMANENT_POLYGON_CAP_U06_CRITERION_ID)
        self.assertEqual(first["final_verdict"], "PASS", first.get("errors"))
        self.assertEqual(first["criterion_coverage_state"], "COVERED_ENGINEERING_L3")
        self.assertTrue(execution["checks"]["real_b8_owner_consumed"])
        self.assertTrue(execution["checks"]["real_b9_owner_consumed"])
        self.assertTrue(execution["checks"]["real_b10_owner_consumed"])
        self.assertFalse(any(execution["forbidden_effects"].values()))

    def test_successor_is_admitted_and_not_false_started(self):
        successor = self.integration["next_mission_start"]
        self.assertEqual(successor["mission_state"], "ADMITTED_READY_FOR_DISPATCH")
        self.assertNotEqual(successor["mission_state"], "IN_PROGRESS")
        self.assertEqual(self.integration["mission_id"], "V7_POLYGON_CAP_U11_DECISION_EXPLAINABILITY_CONSUMER_MATRIX_V1")
        self.assertEqual(self.integration["next_obligation"]["capability_id"], "CAP-U04")

    def test_cps_registry_round_trip_and_legacy_migration(self):
        record = self.integration["criterion_record"]
        rendered = self.lib.render_permanent_polygon_criterion_registry(
            self.cps,
            self.lib.merge_permanent_polygon_criterion_records(self.cps, [record]),
        )
        registry = self.lib.permanent_polygon_criterion_registry(rendered)
        self.assertEqual(registry["migration_state"], "DURABLE_REGISTRY_ACTIVE")
        self.assertTrue(any(
            row["criterion_id"] == "CAP-U11:DECISION_EXPLAINABILITY_CONSUMER_MATRIX"
            for row in registry["records"]
        ))
        consumed = self.lib.permanent_polygon_consumed_criterion_ids(rendered)
        self.assertIn(self.lib.PERMANENT_POLYGON_CAP_U03_CRITERION_ID, consumed)
        self.assertIn(self.lib.PERMANENT_POLYGON_CAP_U05_CRITERION_ID, consumed)
        self.assertIn(self.lib.PERMANENT_POLYGON_CAP_U06_CRITERION_ID, consumed)

    def test_all_source_adapters_are_concrete_and_deduplicated(self):
        events = self.lib.permanent_polygon_source_events(
            self.cps,
            root=ROOT,
            changed_dependencies=["admin_core/autonomy_trust_acceleration.py"],
        )
        self.assertEqual(len(events), len(self.lib.PERMANENT_POLYGON_SOURCE_CATEGORIES))
        self.assertEqual({row["category"] for row in events}, set(self.lib.PERMANENT_POLYGON_SOURCE_CATEGORIES))
        self.assertEqual(len({row["source_fingerprint"] for row in events}), len(events))
        self.assertTrue(all(row["owner"] and row["applicability"] in {"APPLICABLE", "NOT_APPLICABLE"} for row in events))

    def test_executable_work_preempts_missing_adapter_without_hiding_gap(self):
        eligible = [row for row in self.supply["obligations"] if not row["consumed"]]
        self.assertTrue(any(row["executor_available"] is False for row in eligible))
        self.assertTrue(self.supply["next_obligation"]["executor_available"])
        self.assertGreater(self.supply["executable_eligible_obligation_count"], 0)

    def test_missing_adapter_routes_to_exact_bdp_repair_mission(self):
        unsupported = next(
            row for row in self.supply["obligations"]
            if row["criterion_id"] == "CAP-U12:RUNTIME_MATURATION_MEASUREMENT_MATRIX"
        )
        result = self.lib.route_permanent_polygon_executor_gap(unsupported)
        self.assertEqual(result["final_verdict"], "BOUNDED_CONTINUATION", result.get("errors"))
        self.assertEqual(result["program_terminal"], "PERMANENT_POLYGON_EXECUTOR_REPAIR_MISSION_ADMITTED")
        self.assertRegex(result["repair_mission_id"], r"^V7_OMP_BDP_[0-9A-F]{24}_V1$")
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["production_impact"], "NONE")

    def test_atomic_writer_rejects_stale_generation_without_write(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "V7_CURRENT_PROGRAM_STATE.md"
            path.write_text(self.cps, encoding="utf-8")
            before = path.read_text(encoding="utf-8")
            result = self.lib.atomic_reconcile_cps(
                path,
                state=self.lib._normalized_state_from_live_cps(self.cps),
                expected_generation="cpsgen_STALE_CALLER",
            )
            self.assertFalse(result["ok"])
            self.assertEqual(result["status"], "STALE_CPS_GENERATION_STOP_SAFE")
            self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_new_wake_clears_prior_lifecycle_timestamps(self):
        request = {
            "event_id": "1" * 64,
            "source_cps_generation": "cpsgen_test",
            "transition_id": "TEST_TRANSITION",
            "requested_at": "2026-07-18T10:00:00+00:00",
        }
        overrides = self.lib._event_driven_state_overrides(request)
        self.assertEqual(overrides["wake_dispatched_at"], "NONE")
        self.assertEqual(overrides["wake_started_at"], "NONE")
        self.assertEqual(overrides["wake_completed_at"], "NONE")
        self.assertEqual(overrides["last_dispatched_wake_id"], "NONE")

    def test_isolated_mismatch_bdp_repair_return_cycle(self):
        result = self.lib.certify_permanent_polygon_repair_return_cycle(root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS", result.get("errors"))
        self.assertTrue(result["checks"]["bdp_candidate_created"])
        self.assertTrue(result["checks"]["repair_mission_formed"])
        self.assertRegex(result["repair_mission_id"], r"^V7_OMP_BDP_[0-9A-F]{24}_V1$")
        self.assertEqual(result["return_obligation_id"], "POLYGON-CAP-U06-RECOVERY_ADMISSION_ENGINEERING_MATRIX-G1")

    def test_bounded_soak_proves_dedup_sources_and_resource_bound(self):
        result = self.lib.run_permanent_polygon_bounded_soak(root=ROOT, iteration_budget=10)
        self.assertEqual(result["final_verdict"], "PASS", result.get("errors"))
        self.assertEqual(result["iterations_executed"], 10)
        self.assertTrue(result["checks"]["all_duplicates_suppressed"])
        self.assertTrue(result["checks"]["deterministic_result_identity"])
        self.assertTrue(result["checks"]["no_cps_or_report_growth"])


if __name__ == "__main__":
    unittest.main()
