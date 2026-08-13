from pathlib import Path
import unittest

from tools import v7_sync_lib


ROOT = Path(__file__).resolve().parents[2]


class ResetCpsFrontierPreservationTests(unittest.TestCase):
    def test_reset_is_a_reconstructable_live_program(self):
        self.assertIn(
            "V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1",
            v7_sync_lib.LIVE_CPS_RECONSTRUCTION_PROGRAMS,
        )

    def test_normalizer_preserves_reset_frontier(self):
        source = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        state = v7_sync_lib._normalized_state_from_live_cps(source)
        self.assertEqual(state["active_program"], "V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1")
        self.assertEqual(state["current_program_stage"], "RESET-M6")
        self.assertEqual(
            state["current_execution_frontier"],
            "EXECUTE_RESET_M6_CONTROLLED_MIGRATION_SINGLE_WRITER_FENCED_CUTOVER",
        )
        self.assertEqual(state["continuation_decision"], "ENGINEERING_AUTHORITY_REQUIRED")
        self.assertEqual(state["current_stop_condition"], "ENGINEERING_AUTHORITY")


if __name__ == "__main__":
    unittest.main()
