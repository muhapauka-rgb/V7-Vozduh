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

    def test_normalizer_preserves_reset_terminal(self):
        source = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        state = v7_sync_lib._normalized_state_from_live_cps(source)
        self.assertEqual(state["active_program"], "V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1")
        self.assertEqual(state["current_program_stage"], "PROGRAM_COMPLETE")
        self.assertEqual(
            state["current_execution_frontier"],
            "NONE",
        )
        self.assertEqual(state["continuation_decision"], "PROGRAM_TERMINAL_RESET_COMPLETE")
        self.assertEqual(state["current_stop_condition"], "RESET_PROGRAM_TERMINAL")


if __name__ == "__main__":
    unittest.main()
