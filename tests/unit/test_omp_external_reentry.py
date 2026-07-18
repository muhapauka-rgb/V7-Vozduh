from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_external_reentry", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpExternalReentryTest(unittest.TestCase):
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
        cps_path = self.root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
        active_state = dict(self.lib.NORMALIZED_CPS_LIVE_STATE)
        active_state.update({
            "active_program": "ROUTING_DIGITAL_TWIN_POLYGON_MASTER_PROGRAM",
            "current_state_generation": "cpsgen_V7_BACKGROUND_AUTOMATION_CERTIFIED_928718904BCD",
            "current_transition_id": "EXTERNAL_REENTRY_TWO_RUN_CERTIFIED_V1",
            "current_stop_condition": "NONE",
            "current_next_action_id": "PHASE6V2_MARGINAL_BENEFIT_STAY_DECISION",
            "current_safe_next_action": "EXECUTE PHASE6V2_MARGINAL_BENEFIT_STAY_DECISION",
            "current_program_execution_frontier": "PHASE6A_SCENARIO:PHASE6V2_MARGINAL_BENEFIT_STAY_DECISION",
            "authority_required_now": "NO_INSIDE_EXISTING_ENGINEERING_PROGRAM_SCOPE",
            "continuation_decision": "CONTINUE_PROGRAM_FRONTIER",
            "program_terminal_state": "NONE_MULTI_LANE_FRONTIER_ACTIVE",
            "program_terminal_class": "NONE",
            "omp_continuation_required": "TRUE",
            "external_input_required": "FALSE",
            "external_input_type": "NATURAL_PRODUCTION_EVIDENCE_FOR_PHASE6C_ONLY",
            "next_mission_formed": "TRUE",
            "next_mission_id": "V7_FUTURE_SCALE_HIGH_FIDELITY_VALIDATION_V1",
            "next_scenario_id": "PHASE6V2_MARGINAL_BENEFIT_STAY_DECISION",
            "smallest_existing_next_action": "EXECUTE PHASE6V2_MARGINAL_BENEFIT_STAY_DECISION",
            "wip_smallest_existing_next_action_id": "PHASE6V2_MARGINAL_BENEFIT_STAY_DECISION",
            "wip_smallest_existing_next_action": "EXECUTE PHASE6V2_MARGINAL_BENEFIT_STAY_DECISION; preserve CAP-U07 protected WIP",
            "sequence_execution_class": "Phase 6A test scenario reentry",
            "sequence_expected_output": "scenario result -> consumer -> next frontier",
            "program_reconciliation_footprint_class": "FULL_INDEPENDENT_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED",
            "omp_automation_level": "FULL_INDEPENDENT_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED",
            "current_completion_contract": "INTEGRATION_COMPLETION",
        })
        result = self.lib.atomic_reconcile_cps(cps_path, state=active_state)
        self.assertTrue(result["ok"], result)
        self.lease = self.root / "reentry.lease.json"
        self.evidence = self.root / "evidence.jsonl"
        self.now = datetime(2026, 7, 18, 9, 0, tzinfo=timezone.utc)

    def tearDown(self):
        self.temp.cleanup()

    def fake_runner(self, _root):
        return {
            "final_verdict": "PASS", "subprocess_returncode": 0,
            "real_consumer": "OMP_PROGRAM_EXECUTION_RECONCILIATION",
            "transitions": [{"transaction_terminal": "SCENARIO_PASS_CONSUMED"}],
            "program_terminal": "BOUNDED_INVOCATION_BUDGET_REACHED",
            "exact_next_operator_command": "Continue OMP", "errors": [],
        }

    def run_reentry(self, event_time="2026-07-18T08:59:00Z", **overrides):
        return self.lib.heartbeat_program_reentry(
            event_time=event_time, root=self.root, execute_continue_omp=True,
            continue_runner=self.fake_runner, lease_path=self.lease,
            evidence_path=self.evidence, now=self.now, **overrides,
        )

    def replace_live(self, field, value):
        path = self.root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
        text = path.read_text(encoding="utf-8")
        text = self.lib._replace_section_field(
            text, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            field, f"`{value}`",
        )
        path.write_text(text, encoding="utf-8")

    def test_owner_invokes_standard_consumer_and_releases_lease(self):
        result = self.run_reentry()
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["reentry_outcome"], "REENTRY_COMPLETED")
        self.assertTrue(result["standard_entrypoint_invoked"])
        self.assertTrue(result["consumer_invoked"])
        self.assertEqual(result["internal_iteration_count"], 1)
        self.assertTrue(result["lease_released"])
        self.assertFalse(self.lease.exists())
        self.assertEqual(len(self.evidence.read_text(encoding="utf-8").splitlines()), 1)

    def test_external_input_suppresses_entrypoint(self):
        self.replace_live("EXTERNAL_INPUT_REQUIRED", "TRUE")
        result = self.run_reentry()
        self.assertEqual(result["reentry_outcome"], "REENTRY_BLOCKED_EXTERNAL_INPUT")
        self.assertFalse(result["standard_entrypoint_invoked"])

    def test_continuation_not_required_is_legal_no_execution(self):
        self.replace_live("OMP_CONTINUATION_REQUIRED", "FALSE")
        result = self.run_reentry()
        self.assertEqual(result["reentry_outcome"], "REENTRY_NOT_REQUIRED")
        self.assertFalse(result["standard_entrypoint_invoked"])

    def test_active_lease_suppresses_overlap(self):
        self.lease.write_text(json.dumps({
            "lease_id": "active", "expires_at": (self.now + timedelta(minutes=5)).isoformat(),
        }), encoding="utf-8")
        result = self.run_reentry()
        self.assertEqual(result["reentry_outcome"], "REENTRY_ALREADY_ACTIVE")
        self.assertFalse(result["standard_entrypoint_invoked"])

    def test_stale_lease_is_recovered(self):
        self.lease.write_text(json.dumps({
            "lease_id": "stale", "expires_at": (self.now - timedelta(seconds=1)).isoformat(),
        }), encoding="utf-8")
        result = self.run_reentry()
        self.assertEqual(result["lease_acquisition_outcome"], "REENTRY_STALE_LEASE_RECOVERED")
        self.assertTrue(result["stale_lease_recovered"])
        self.assertTrue(result["lease_released"])

    def test_duplicate_platform_event_is_suppressed(self):
        first = self.run_reentry()
        duplicate = self.run_reentry(event_identity_override=first["event_id"])
        self.assertEqual(first["final_verdict"], "PASS")
        self.assertFalse(duplicate["standard_entrypoint_invoked"])
        self.assertIn(duplicate["adapter"]["activation_result"], {"NO_CHANGE_DUPLICATE_WAKEUP", "STOP_SAFE_REPLAY_FAILURE"})

    def test_authority_terminal_suppresses_entrypoint(self):
        self.replace_live("AUTHORITY_REQUIRED_NOW", "ENGINEERING_AUTHORITY")
        result = self.run_reentry()
        self.assertEqual(result["reentry_outcome"], "REENTRY_BLOCKED_PROGRAM_TERMINAL")
        self.assertFalse(result["standard_entrypoint_invoked"])

    def test_completion_gate_requires_two_natural_separated_reentries(self):
        base = {
            "platform_owner": "CODEX_AUTOMATION_PLATFORM", "no_user_prompt": True,
            "prior_context_exited": True, "standard_entrypoint_invoked": True,
            "consumer_invoked": True, "lease_released": True, "no_overlap": True,
            "reentry_outcome": "REENTRY_COMPLETED", "behavior_change": True,
        }
        runs = [
            {**base, "event_id": "event-b", "invocation_id": "inv-b"},
            {**base, "event_id": "event-c", "invocation_id": "inv-c"},
        ]
        gate = self.lib.external_reentry_completion_evidence_gate(
            runs, automation_enabled=True, fsse04_deployed=True,
            truth_passed=True, convergence_passed=True, snapshot_equal=True,
        )
        self.assertEqual(gate["completion_verdict"], "PASS")
        one = self.lib.external_reentry_completion_evidence_gate(
            runs[:1], automation_enabled=True, fsse04_deployed=True,
            truth_passed=True, convergence_passed=True, snapshot_equal=True,
        )
        self.assertEqual(one["completion_verdict"], "INCOMPLETE")

    def test_completion_gate_rejects_manual_or_active_context_trigger(self):
        run = {
            "platform_owner": "CODEX_AUTOMATION_PLATFORM", "no_user_prompt": False,
            "prior_context_exited": False, "standard_entrypoint_invoked": True,
            "consumer_invoked": True, "lease_released": True, "no_overlap": True,
            "reentry_outcome": "REENTRY_COMPLETED", "behavior_change": True,
            "event_id": "event", "invocation_id": "inv",
        }
        gate = self.lib.external_reentry_completion_evidence_gate(
            [run, {**run, "event_id": "event-2", "invocation_id": "inv-2"}],
            automation_enabled=True, fsse04_deployed=True,
            truth_passed=True, convergence_passed=True, snapshot_equal=True,
        )
        self.assertEqual(gate["independent_reentry_count"], 0)
        self.assertEqual(gate["completion_verdict"], "INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
