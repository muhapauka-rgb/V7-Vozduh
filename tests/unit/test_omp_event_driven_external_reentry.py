from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_event_reentry", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpEventDrivenExternalReentryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in self.lib.PROGRAM_EXECUTION_SOURCE_PATHS.values():
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        for relative in ("tools/v7_sync_lib.py", "tools/v7-truth-check"):
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        self.cps = self.root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
        self.now = datetime(2026, 7, 16, 9, 0, tzinfo=timezone.utc)

    def tearDown(self):
        self.temp.cleanup()

    def state(self, **overrides):
        state = dict(self.lib.NORMALIZED_CPS_LIVE_STATE)
        state.update({
            "state_captured": self.now.isoformat(),
            "current_state_generation": "cpsgen_EVENT_REENTRY_TEST_001",
            "current_transition_id": "EVENT_REENTRY_TEST_TRANSITION_V1",
            "current_next_action_id": "CONTINUE_OMP",
            "current_stop_condition": "BOUNDED_INVOCATION_BUDGET_REACHED",
            "current_active_scope": "INDEPENDENT_BACKGROUND_CONTINUE_OMP",
            "current_safe_next_action": "RUN THE STANDARD CONTINUE OMP TRIGGER",
            "current_scope_class": "EXTERNAL_ENGINEERING_AUTOMATION",
            "current_program_execution_frontier": "CONTINUE_OMP",
            "current_execution_frontier": "NONE",
            "program_frontier_input": "event-driven certification Mission admitted; next scenario NONE",
            "continuation_decision": "CONTINUE_PROGRAM_FRONTIER",
            "program_terminal_state": "BOUNDED_INVOCATION_BUDGET_REACHED_EXACT_CONTINUATION_SAVED",
            "authority_required_now": "NO_INSIDE_EXISTING_ENGINEERING_PROGRAM_SCOPE",
            "smallest_existing_next_action": "run the standard Continue OMP trigger from fresh CPS",
            "omp_continuation_pointer": "run Continue OMP; preserve CAP-U07 WAITING WIP and recalculate ordinary work before scenario fallback",
            "required_workflow": "Continue OMP -> fresh CPS -> deterministic ordinary/scenario priority -> bounded legal terminal",
            "wip_current_primary_stop": "REAL_WORLD_LIMIT_CAPABILITY_LOCAL; global Continue OMP frontier is bounded at BOUNDED_INVOCATION_BUDGET_REACHED",
            "wip_smallest_existing_next_action": "preserve CAP-U07 evidence while the standard Continue OMP trigger recalculates the global frontier",
            "omp_continuation_required": "TRUE",
            "external_input_required": "FALSE",
            "external_input_type": "NONE",
            "program_terminal_class": "BOUNDED_INVOCATION_BUDGET_REACHED",
            "next_mission_formed": "TRUE",
            "next_mission_id": "CONTINUE_OMP",
            "continuation_stop_reason": "EVENT_REENTRY_TEST_READY; EXACT_CONTINUATION_SAVED",
        })
        state.update(overrides)
        return state

    def candidate(self, **overrides):
        original = self.cps.read_text(encoding="utf-8")
        return self.lib.build_normalized_cps_document(original, self.state(**overrides))

    def fake_runner(self, _root):
        return {
            "final_verdict": "PASS", "subprocess_returncode": 0,
            "real_consumer": "OMP_PROGRAM_EXECUTION_RECONCILIATION",
            "transitions": [{"transaction_terminal": "EVENT_REENTRY_TEST_CONSUMED"}],
            "program_terminal": "BOUNDED_INVOCATION_BUDGET_REACHED",
            "exact_next_operator_command": "Status", "errors": [],
        }

    def test_false_to_true_requests_one_deterministic_wake(self):
        original = self.cps.read_text(encoding="utf-8")
        result = self.lib.event_driven_external_wake_request(original, self.candidate(), requested_at=self.now)
        self.assertEqual(result["outcome"], "IMMEDIATE_REENTRY_REQUESTED")
        self.assertTrue(result["dispatch_required"])
        self.assertRegex(result["event_id"], r"^[0-9a-f]{64}$")
        repeated = self.lib.event_driven_external_wake_request(original, self.candidate(), requested_at=self.now)
        self.assertEqual(result["event_id"], repeated["event_id"])

    def test_true_to_true_unchanged_is_suppressed(self):
        current = self.candidate()
        result = self.lib.event_driven_external_wake_request(current, current, requested_at=self.now)
        self.assertEqual(result["outcome"], "IMMEDIATE_REENTRY_NOT_REQUIRED")
        self.assertFalse(result["dispatch_required"])

    def test_false_state_and_empty_frontier_are_noops(self):
        original = self.cps.read_text(encoding="utf-8")
        false_state = self.candidate(omp_continuation_required="FALSE")
        self.assertEqual(self.lib.event_driven_external_wake_request(original, false_state)["outcome"], "IMMEDIATE_REENTRY_NOT_REQUIRED")
        empty = self.candidate(
            current_program_execution_frontier="NONE", current_execution_frontier="NONE",
            next_mission_formed="FALSE", next_mission_id="NONE",
        )
        self.assertEqual(self.lib.event_driven_external_wake_request(original, empty)["reason"], "ready_frontier_empty")

    def test_external_input_and_active_lease_suppress(self):
        original = self.cps.read_text(encoding="utf-8")
        blocked = self.candidate(external_input_required="TRUE", external_input_type="SECURITY_OR_ACCESS_INPUT")
        self.assertEqual(self.lib.event_driven_external_wake_request(original, blocked)["outcome"], "IMMEDIATE_REENTRY_SUPPRESSED_EXTERNAL_INPUT")
        leased = self.candidate(reentry_active_lease="omplease_active")
        self.assertEqual(self.lib.event_driven_external_wake_request(original, leased)["outcome"], "IMMEDIATE_REENTRY_SUPPRESSED_ACTIVE_LEASE")

    def test_ready_mission_and_scenario_change_identity(self):
        original = self.cps.read_text(encoding="utf-8")
        mission = self.lib.event_driven_external_wake_request(original, self.candidate())
        scenario = self.lib.event_driven_external_wake_request(
            original, self.candidate(next_mission_id="NONE", next_mission_formed="FALSE", next_scenario_id="LEASE_CONFLICT")
        )
        self.assertTrue(mission["dispatch_required"])
        self.assertTrue(scenario["dispatch_required"])
        self.assertNotEqual(mission["event_id"], scenario["event_id"])

    def test_atomic_writer_returns_without_running_consumer_and_persists_pending(self):
        result = self.lib.atomic_reconcile_cps(self.cps, state=self.state())
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["external_wake"]["dispatch_required"])
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps.read_text(encoding="utf-8"), "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        self.assertEqual(live["PENDING_WAKE_ID"].strip("`"), result["external_wake"]["event_id"])
        self.assertEqual(live["WAKE_STARTED_AT"].strip("`"), "NONE")

    def test_dispatch_lifecycle_is_atomic_and_duplicate_safe(self):
        write = self.lib.atomic_reconcile_cps(self.cps, state=self.state())
        event_id = write["external_wake"]["event_id"]
        dispatched = self.lib.event_driven_wake_lifecycle(self.cps, event_id=event_id, phase="DISPATCHED", occurred_at=self.now)
        self.assertEqual(dispatched["outcome"], "IMMEDIATE_REENTRY_DISPATCHED")
        duplicate = self.lib.event_driven_wake_lifecycle(self.cps, event_id=event_id, phase="DISPATCHED", occurred_at=self.now)
        self.assertEqual(duplicate["outcome"], "IMMEDIATE_REENTRY_ALREADY_DISPATCHED")

    def test_immediate_dispatch_invokes_standard_consumer_once(self):
        write = self.lib.atomic_reconcile_cps(self.cps, state=self.state())
        event_id = write["external_wake"]["event_id"]
        self.lib.event_driven_wake_lifecycle(self.cps, event_id=event_id, phase="DISPATCHED", occurred_at=self.now)
        result = self.lib.heartbeat_program_reentry(
            event_time=self.now.isoformat(), event_identity_override=event_id,
            event_source_kind="IMMEDIATE_THREAD_SIGNAL", execute_continue_omp=True,
            continue_runner=self.fake_runner, lease_path=self.root / "lease.json",
            evidence_path=self.root / "evidence.jsonl", now=self.now, root=self.root,
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertTrue(result["standard_entrypoint_invoked"])
        self.assertTrue(result["consumer_invoked"])
        self.assertTrue(result["lease_released"])
        duplicate = self.lib.heartbeat_program_reentry(
            event_time=self.now.isoformat(), event_identity_override=event_id,
            event_source_kind="IMMEDIATE_THREAD_SIGNAL", execute_continue_omp=True,
            continue_runner=self.fake_runner, lease_path=self.root / "lease.json",
            evidence_path=self.root / "evidence.jsonl", now=self.now, root=self.root,
        )
        self.assertFalse(duplicate["standard_entrypoint_invoked"])

    def test_failed_dispatch_is_recovered_once_by_watchdog(self):
        write = self.lib.atomic_reconcile_cps(self.cps, state=self.state())
        event_id = write["external_wake"]["event_id"]
        failed = self.lib.event_driven_wake_lifecycle(self.cps, event_id=event_id, phase="FAILED", occurred_at=self.now)
        self.assertEqual(failed["outcome"], "IMMEDIATE_REENTRY_FAILED_SAFE")
        recovered = self.lib.heartbeat_program_reentry(
            event_time=self.now.isoformat(), execute_continue_omp=True,
            continue_runner=self.fake_runner, lease_path=self.root / "lease.json",
            evidence_path=self.root / "evidence.jsonl", now=self.now, root=self.root,
        )
        self.assertEqual(recovered["final_verdict"], "PASS")
        self.assertTrue(recovered["watchdog_recovery"])
        self.assertEqual(recovered["trigger_mode"], "WATCHDOG_LOST_WAKE_RECOVERY")

    def test_dispatched_pending_wake_makes_watchdog_noop(self):
        write = self.lib.atomic_reconcile_cps(self.cps, state=self.state())
        event_id = write["external_wake"]["event_id"]
        self.lib.event_driven_wake_lifecycle(self.cps, event_id=event_id, phase="DISPATCHED", occurred_at=self.now)
        watchdog = self.lib.heartbeat_program_reentry(
            event_time=self.now.isoformat(), execute_continue_omp=True,
            continue_runner=self.fake_runner, root=self.root,
        )
        self.assertEqual(watchdog["reentry_outcome"], "IMMEDIATE_REENTRY_ALREADY_DISPATCHED")
        self.assertFalse(watchdog["standard_entrypoint_invoked"])


if __name__ == "__main__":
    unittest.main()
