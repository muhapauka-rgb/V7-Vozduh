from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import tempfile
import unittest

from admin_core import operator_execution


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_ar_equivalence", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AutonomousRecoveryEquivalenceCertificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def execution(self):
        rows = []
        for scale in (1_000, 10_000):
            candidate = operator_execution.build_isolated_generic_movement_equivalence_candidate(scale)
            for target in candidate["class_contract"]["targets"]:
                subset = [row["member"] for row in candidate["assignments"] if row["target"] == target]
                representative = {
                    "scale": scale, "logical_target": target,
                    "class_generation": candidate["class_contract"]["generation"],
                    "class_fingerprint": candidate["class_fingerprint"],
                    "packet_fingerprint": candidate["packet_fingerprint"],
                    "membership_subset_count": len(subset),
                    "membership_subset_fingerprint": self.lib._execution_contract_fingerprint(subset),
                    "kernel_route_ok": True, "kernel_route_fingerprint": f"route-{target}",
                    "required_service_ok": True, "required_service_s11_ns": 1,
                    "representative_fingerprint": f"rep-{scale}-{target}",
                }
                rows.append(representative)
        return {"final_verdict": "PASS", "equivalence_representatives": rows,
                "checks": {
                    "verification_timeout_observed": True,
                    "asymmetric_route_failure_observed": True,
                    "dns_service_failure_observed": True,
                    "combined_delay_loss_required_service_verified": True,
                    "independent_channel_off_surviving_target_verified": True,
                    "client_namespace_restart_and_service_reentry_verified": True,
                    "rollback_and_recovery_verified": True,
                },
                "authority_impact": "NONE", "production_impact": "NONE"}

    def test_valid_two_target_stages_certify_engineering_only(self):
        result = self.lib.certify_autonomous_recovery_equivalence_stages(self.execution())
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])
        self.assertEqual(result["engineering_certified_scopes"], [1_000, 10_000])
        self.assertEqual(result["production_certified_max_change"], 0)

    def test_missing_target_representative_stops_safe(self):
        execution = self.execution(); execution["equivalence_representatives"].pop()
        result = self.lib.certify_autonomous_recovery_equivalence_stages(execution)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertTrue(any("one_real_representative_per_target" in error for error in result["errors"]))

    def test_forged_fingerprint_and_stale_generation_stop_safe(self):
        execution = self.execution()
        execution["equivalence_representatives"][0]["packet_fingerprint"] = "forged"
        execution["equivalence_representatives"][1]["class_generation"] = "stale"
        result = self.lib.certify_autonomous_recovery_equivalence_stages(execution)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertTrue(any("class_packet_generation_bound" in error for error in result["errors"]))

    def test_shared_capacity_breach_stops_candidate(self):
        original = operator_execution.build_isolated_generic_movement_equivalence_candidate
        def breached(scale):
            row = copy.deepcopy(original(scale))
            row["target_counts"]["polygon-target-a"] = 6_001
            return row
        operator_execution.build_isolated_generic_movement_equivalence_candidate = breached
        try:
            result = self.lib.certify_autonomous_recovery_equivalence_stages(self.execution())
        finally:
            operator_execution.build_isolated_generic_movement_equivalence_candidate = original
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertTrue(any("shared_capacity_safe" in error for error in result["errors"]))

    def test_full_fault_catalog_and_generated_combinations_are_consumed(self):
        result = self.lib.certify_autonomous_recovery_fault_catalog(self.execution())
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])
        self.assertEqual(len(result["catalog"]), 12)
        self.assertTrue(all(result["coverage"].values()))
        self.assertTrue(all(row["covered"] for row in result["coverage_directed_combinations"]))

    def test_distinct_member_binding_seed_repairs_and_replays(self):
        result = self.lib.certify_distinct_member_equivalence_seeded_repair_cycle(self.execution())
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])
        self.assertTrue(result["mission_executed"])
        self.assertEqual(result["seeded"]["final_verdict"], "STOP_SAFE")
        self.assertEqual(result["replay"]["final_verdict"], "PASS")

    def test_material_change_unchanged_duplicate_and_stale_fail_closed(self):
        generation = self.lib._autonomous_recovery_current_cps_generation(ROOT)
        unchanged = self.lib.autonomous_recovery_qualifying_material_change_continuation(
            "tools/v7_sync_lib.py", before_fingerprint="a", after_fingerprint="a",
            cps_generation=generation,
        )
        self.assertEqual(unchanged["disposition"], "NOOP_UNCHANGED")
        stale = self.lib.autonomous_recovery_qualifying_material_change_continuation(
            "tools/v7_sync_lib.py", before_fingerprint="a", after_fingerprint="b", cps_generation="stale",
        )
        self.assertEqual(stale["final_verdict"], "STOP_SAFE")

    def test_material_change_existing_evidence_lease_and_duplicate(self):
        original_probe = self.lib.routing_digital_twin_substrate_probe
        self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L4"}
        calls = []
        def runner(**kwargs):
            calls.append(kwargs)
            return {"final_verdict": "PASS", "internal_iteration_count": 2, "errors": []}
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = ROOT
                evidence = Path(directory) / "existing-omp-external-reentry.jsonl"
                result = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "tools/v7_sync_lib.py", before_fingerprint="old", after_fingerprint="new",
                    root=root, cps_generation=self.lib._autonomous_recovery_current_cps_generation(root),
                    iteration_budget=2, background_runner=runner, evidence_path=evidence,
                    lease_path=Path(directory) / "existing-omp.lease",
                )
                self.assertEqual(result["final_verdict"], "PASS", result["errors"])
                self.assertEqual(result["omp_caller"], "continue_omp_engineering_control_loop")
                self.assertEqual(result["background_owner"], "run_permanent_polygon_bounded_soak")
                self.assertTrue(result["single_flight"])
                self.assertTrue(result["lease_released"])
                self.assertEqual(result["iterations_executed"], 2)
                self.assertTrue(result["safe_independent_work_continued"])
                self.assertEqual(len(calls), 1)
                duplicate = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "tools/v7_sync_lib.py", before_fingerprint="old", after_fingerprint="new",
                    root=root, cps_generation=self.lib._autonomous_recovery_current_cps_generation(root),
                    iteration_budget=2, background_runner=runner, evidence_path=evidence,
                    lease_path=Path(directory) / "existing-omp.lease",
                )
                self.assertEqual(duplicate["disposition"], "DUPLICATE_SUPPRESSED")
                self.assertFalse(duplicate["trigger_invoked"])
                self.assertFalse(duplicate["single_flight"])
                self.assertEqual(len(calls), 1)
        finally:
            self.lib.routing_digital_twin_substrate_probe = original_probe

    def test_manual_full_creates_distinct_frozen_snapshots_without_source_diff(self):
        original_probe = self.lib.routing_digital_twin_substrate_probe
        self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L4"}
        calls = []

        def runner(**kwargs):
            calls.append(kwargs)
            return {"final_verdict": "PASS", "internal_iteration_count": kwargs["iteration_budget"], "errors": []}

        try:
            with tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                generation = self.lib._autonomous_recovery_current_cps_generation(ROOT)
                common = {
                    "changed_path": "AUTONOMOUS_RECOVERY_MANUAL_FULL",
                    "before_fingerprint": "NO_SOURCE_DIFF_REQUIRED",
                    "after_fingerprint": "NO_SOURCE_DIFF_REQUIRED",
                    "cps_generation": generation, "root": ROOT, "iteration_budget": 2,
                    "background_runner": runner, "evidence_path": temp / "existing.jsonl",
                    "lease_path": temp / "existing.lease", "trigger_kind": "MANUAL_FULL",
                }
                first = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    **common, experiment_nonce="manual-a",
                )
                second = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    **common, experiment_nonce="manual-b",
                )
                self.assertEqual(first["final_verdict"], "PASS", first["errors"])
                self.assertEqual(second["final_verdict"], "PASS", second["errors"])
                self.assertEqual(first["trigger_kind"], "MANUAL_FULL")
                self.assertNotEqual(first["frozen_snapshot_identity"], second["frozen_snapshot_identity"])
                self.assertEqual(len(calls), 2)
                missing_nonce = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    **common, experiment_nonce="",
                )
                self.assertEqual(missing_nonce["disposition"], "STOP_SAFE_MANUAL_SNAPSHOT_IDENTITY")
        finally:
            self.lib.routing_digital_twin_substrate_probe = original_probe

    def test_bounded_cadence_dedupes_one_existing_omp_slot_without_busy_loop(self):
        original_probe = self.lib.routing_digital_twin_substrate_probe
        self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L4"}
        calls = []

        def runner(**kwargs):
            calls.append(kwargs)
            return {"final_verdict": "PASS", "internal_iteration_count": 1, "errors": []}

        try:
            with tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                now = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)
                common = {
                    "changed_path": "AUTONOMOUS_RECOVERY_BOUNDED_CADENCE",
                    "before_fingerprint": "NO_SOURCE_DIFF_REQUIRED",
                    "after_fingerprint": "NO_SOURCE_DIFF_REQUIRED", "root": ROOT,
                    "cps_generation": self.lib._autonomous_recovery_current_cps_generation(ROOT),
                    "background_runner": runner, "evidence_path": temp / "existing.jsonl",
                    "lease_path": temp / "existing.lease", "trigger_kind": "BOUNDED_CADENCE",
                    "cadence_seconds": 900,
                }
                first = self.lib.autonomous_recovery_qualifying_material_change_continuation(**common, now=now)
                duplicate = self.lib.autonomous_recovery_qualifying_material_change_continuation(**common, now=now)
                next_slot = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    **common, now=now + timedelta(seconds=900),
                )
                self.assertEqual(first["final_verdict"], "PASS", first["errors"])
                self.assertEqual(duplicate["disposition"], "DUPLICATE_SUPPRESSED")
                self.assertFalse(duplicate["trigger_invoked"])
                self.assertEqual(next_slot["final_verdict"], "PASS", next_slot["errors"])
                self.assertEqual(next_slot["cadence_slot"], first["cadence_slot"] + 1)
                self.assertEqual(len(calls), 2)
                invalid_common = {**common, "cadence_seconds": 59}
                invalid = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    **invalid_common, now=now,
                )
                self.assertEqual(invalid["disposition"], "STOP_SAFE_CADENCE_BUDGET")
        finally:
            self.lib.routing_digital_twin_substrate_probe = original_probe

    def test_material_change_budget_substrate_and_active_lease_stop_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                "x", before_fingerprint="a", after_fingerprint="b", root=ROOT,
                cps_generation=self.lib._autonomous_recovery_current_cps_generation(ROOT),
                iteration_budget=self.lib.OMP_CONTINUATION_MAX_ITERATIONS + 1,
            )
            self.assertEqual(invalid["disposition"], "STOP_SAFE_INVALID_BUDGET")
            original_probe = self.lib.routing_digital_twin_substrate_probe
            self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L2"}
            try:
                substrate = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "x", before_fingerprint="a", after_fingerprint="b", root=ROOT,
                    cps_generation=self.lib._autonomous_recovery_current_cps_generation(ROOT),
                )
            finally:
                self.lib.routing_digital_twin_substrate_probe = original_probe
            self.assertEqual(substrate["disposition"], "STOP_SAFE_SUBSTRATE")
            lease_path = root / "active.lease"
            lease_path.write_text(__import__("json").dumps({
                "lease_id": "existing", "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat(),
            }), encoding="utf-8")
            self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L4"}
            try:
                leased = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "x", before_fingerprint="a", after_fingerprint="b", root=ROOT,
                    cps_generation=self.lib._autonomous_recovery_current_cps_generation(ROOT),
                    lease_path=lease_path,
                    background_runner=lambda **_: {"final_verdict": "PASS"},
                )
            finally:
                self.lib.routing_digital_twin_substrate_probe = original_probe
            self.assertEqual(leased["disposition"], "STOP_SAFE_LEASE_ACTIVE")

    def test_material_change_requires_omp_runner_and_releases_after_failure(self):
        original_probe = self.lib.routing_digital_twin_substrate_probe
        self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L4"}
        try:
            with tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                generation = self.lib._autonomous_recovery_current_cps_generation(ROOT)
                missing = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "tools/v7_sync_lib.py", before_fingerprint="a", after_fingerprint="b",
                    cps_generation=generation, root=ROOT, evidence_path=temp / "existing.jsonl",
                )
                self.assertEqual(missing["disposition"], "STOP_SAFE_OMP_CALLER_REQUIRED")
                lease = temp / "existing.lease"
                failed = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "tools/v7_sync_lib.py", before_fingerprint="failure-a", after_fingerprint="failure-b",
                    cps_generation=generation, root=ROOT, lease_path=lease,
                    evidence_path=temp / "existing.jsonl",
                    background_runner=lambda **_: (_ for _ in ()).throw(RuntimeError("boom")),
                )
                self.assertEqual(failed["final_verdict"], "STOP_SAFE")
                self.assertTrue(failed["lease_released"])
                self.assertFalse(lease.exists())
        finally:
            self.lib.routing_digital_twin_substrate_probe = original_probe

    def test_material_change_malformed_existing_evidence_and_stale_reread_stop_safe(self):
        original_probe = self.lib.routing_digital_twin_substrate_probe
        original_generation = self.lib._autonomous_recovery_current_cps_generation
        self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L4"}
        try:
            with tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                evidence = temp / "existing.jsonl"
                evidence.write_text('{"schema":"v7.autonomous-recovery-material-change-continuation.v2"\n', encoding="utf-8")
                generation = original_generation(ROOT)
                malformed = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "tools/v7_sync_lib.py", before_fingerprint="a", after_fingerprint="b",
                    cps_generation=generation, root=ROOT, evidence_path=evidence,
                    background_runner=lambda **_: {"final_verdict": "PASS"},
                )
                self.assertEqual(malformed["disposition"], "STOP_SAFE_EVIDENCE_HISTORY")
                generations = iter(("first", "first", "second"))
                self.lib._autonomous_recovery_current_cps_generation = lambda root: next(generations)
                stale = self.lib.autonomous_recovery_qualifying_material_change_continuation(
                    "tools/v7_sync_lib.py", before_fingerprint="stale-a", after_fingerprint="stale-b",
                    cps_generation="first", root=ROOT, evidence_path=temp / "other.jsonl",
                    background_runner=lambda **_: {"final_verdict": "PASS"},
                )
                self.assertEqual(stale["disposition"], "STOP_SAFE_BACKGROUND")
                self.assertTrue(stale["lease_released"])
        finally:
            self.lib.routing_digital_twin_substrate_probe = original_probe
            self.lib._autonomous_recovery_current_cps_generation = original_generation

    def test_continue_omp_reaches_material_change_once_without_relay(self):
        original_probe = self.lib.routing_digital_twin_substrate_probe
        self.lib.routing_digital_twin_substrate_probe = lambda: {"highest_available_fidelity_candidate": "L4"}
        calls = []

        def soak_runner(**kwargs):
            calls.append(kwargs)
            return {"final_verdict": "PASS", "internal_iteration_count": kwargs["iteration_budget"], "errors": []}

        try:
            with tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                kwargs = {
                    "root": ROOT,
                    "changed_dependencies": ["AUTONOMOUS_RECOVERY_MATERIAL_CHANGE:tools/v7_sync_lib.py:old:new"], "iteration_budget": 2,
                    "scenario_budget": 1, "repair_budget": 1, "persist_cps": False,
                    "autonomous_recovery_continuation_runner": soak_runner,
                    "autonomous_recovery_lease_path": temp / "material.lease",
                    "autonomous_recovery_evidence_path": temp / "existing-omp-external-reentry.jsonl",
                }
                first = self.lib.continue_omp_engineering_control_loop(**kwargs)
                self.assertEqual(first["final_verdict"], "PASS", first.get("errors"))
                receipt = first["autonomous_recovery_material_change_continuation"]
                self.assertEqual(receipt["disposition"], "BOUNDED_BACKGROUND_CONTINUATION_CONSUMED")
                self.assertTrue(receipt["lease_released"])
                self.assertTrue(receipt["single_flight"])
                self.assertTrue(receipt["no_user_relay"])
                self.assertEqual(receipt["iterations_executed"], 2)
                self.assertEqual(len(calls), 1)

                manual = self.lib.continue_omp_engineering_control_loop(
                    root=ROOT, changed_dependencies=["AUTONOMOUS_RECOVERY_MANUAL_FULL:manual-proof"],
                    iteration_budget=2, scenario_budget=1, repair_budget=1, persist_cps=False,
                    autonomous_recovery_continuation_runner=soak_runner,
                    autonomous_recovery_lease_path=temp / "manual.lease",
                    autonomous_recovery_evidence_path=temp / "manual.jsonl",
                )
                manual_receipt = manual["autonomous_recovery_material_change_continuation"]
                self.assertEqual(manual["final_verdict"], "PASS", manual.get("errors"))
                self.assertEqual(manual_receipt["trigger_kind"], "MANUAL_FULL")
                self.assertTrue(manual_receipt["trigger_invoked"])
                self.assertEqual(len(calls), 2)

                duplicate = self.lib.continue_omp_engineering_control_loop(**kwargs)
                duplicate_receipt = duplicate["autonomous_recovery_material_change_continuation"]
                self.assertEqual(duplicate_receipt["disposition"], "DUPLICATE_SUPPRESSED")
                self.assertEqual(len(calls), 2)

                nonqualifying = self.lib.continue_omp_engineering_control_loop(
                    root=ROOT, changed_dependencies=["docs/reference/nonqualifying.md"],
                    iteration_budget=2, scenario_budget=1, repair_budget=1, persist_cps=False,
                    autonomous_recovery_continuation_runner=soak_runner,
                    autonomous_recovery_lease_path=temp / "other.lease",
                    autonomous_recovery_evidence_path=temp / "other.jsonl",
                )
                self.assertNotIn("autonomous_recovery_material_change_continuation", nonqualifying)
                self.assertEqual(len(calls), 2)
        finally:
            self.lib.routing_digital_twin_substrate_probe = original_probe


if __name__ == "__main__":
    unittest.main()
