from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
EVENT_TIME = "2026-07-14T16:46:18.891Z"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_heartbeat_real_consumer", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpHeartbeatRealConsumerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def run_reentry(self, **overrides):
        return self.lib.heartbeat_program_reentry(event_time=EVENT_TIME, root=ROOT, **overrides)

    def test_platform_heartbeat_target_matches_current_service_failure_task(self):
        self.assertEqual(
            self.lib.HEARTBEAT_TARGET_THREAD_ID,
            "019f651d-542b-7c53-9a6c-504648e692ee",
        )

    def test_natural_no_change_reaches_reconciliation_and_legal_consumer(self):
        result = self.run_reentry()
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertTrue(result["reconciliation_invoked"])
        self.assertTrue(result["consumer_invoked"])
        self.assertEqual(result["consumer_decision"], "LEGAL_NO_ACTION")
        self.assertTrue(result["legal_terminal"])

    def test_fresh_cps_is_loaded_by_existing_owner(self):
        result = self.run_reentry()
        cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text()
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        self.assertEqual(result["fresh_cps_generation"], live["CURRENT_STATE_GENERATION"].strip("`"))

    def test_identity_mismatch_stops_before_reconciliation(self):
        result = self.run_reentry(automation_id="wrong-heartbeat")
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertFalse(result["reconciliation_invoked"])
        self.assertFalse(result["consumer_invoked"])

    def test_duplicate_wakeup_is_suppressed_before_reconciliation(self):
        first = self.run_reentry()
        duplicate = self.run_reentry(seen_wakeup_run_ids=[first["wakeup_run_id"]])
        self.assertEqual(duplicate["adapter"]["activation_result"], "NO_CHANGE_DUPLICATE_WAKEUP")
        self.assertFalse(duplicate["reconciliation_invoked"])
        self.assertFalse(duplicate["consumer_invoked"])

    def test_processed_platform_event_is_suppressed_from_cps_state(self):
        cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text()
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        duplicate = self.lib.heartbeat_program_reentry(
            event_time=EVENT_TIME,
            event_identity_override=live["HEARTBEAT_LAST_EVENT_ID"].strip("`"),
            root=ROOT,
        )
        self.assertEqual(duplicate["adapter"]["activation_result"], "NO_CHANGE_DUPLICATE_WAKEUP")
        self.assertFalse(duplicate["reconciliation_invoked"])
        self.assertFalse(duplicate["consumer_invoked"])

    def test_decision_is_deterministic(self):
        first = self.run_reentry()
        second = self.run_reentry()
        self.assertEqual(first["decision_fingerprint"], second["decision_fingerprint"])
        self.assertEqual(first["next_output"], second["next_output"])

    def test_legal_no_action_never_creates_execution_objects(self):
        result = self.run_reentry()
        self.assertFalse(result["mission_created"])
        self.assertFalse(result["candidate_created"])
        self.assertFalse(result["packet_created"])
        self.assertFalse(result["cps_mutated"])
        self.assertFalse(result["git_changed"])

    def test_runtime_production_and_authority_remain_unchanged(self):
        result = self.run_reentry()
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["production_impact"], "NONE")
        self.assertEqual(result["authority_impact"], "NONE")

    def test_no_recursive_trigger_is_produced(self):
        result = self.run_reentry()
        self.assertTrue(result["no_unbounded_recursion"])
        self.assertEqual(result["next_trigger_policy"], "NATURAL_SCHEDULE_ONLY_NO_RECURSION")

    def test_source_loader_reads_all_existing_program_owners(self):
        sources = self.lib.load_program_execution_sources(ROOT)
        self.assertEqual(set(sources), set(self.lib.PROGRAM_EXECUTION_SOURCE_PATHS))
        self.assertTrue(all(sources.values()))


if __name__ == "__main__":
    unittest.main()
