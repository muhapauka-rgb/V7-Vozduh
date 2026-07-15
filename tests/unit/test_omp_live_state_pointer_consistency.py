import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"
OMP = ROOT / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_omp_pointer_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpLiveStatePointerConsistencyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        cls.omp = OMP.read_text(encoding="utf-8")

    def validate(self, omp):
        return self.lib.omp_live_state_consistency(self.cps, omp)

    def test_01_unqualified_unsafe_current_blocker_fails(self):
        drift = self.omp + "\n## Test Drift\nCurrent blocker:\n\n`UNSAFE_IMPLEMENTATION`\n"
        self.assertIn("OMP_UNQUALIFIED_CURRENT_STATE", self.validate(drift)["errors"])

    def test_02_same_value_inside_historical_snapshot_passes(self):
        snapshot = (
            "\n## Historical Test Snapshot\nClassification: `HISTORICAL_SNAPSHOT`.\n"
            "Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`\n"
            "Scheduling Authority: `NONE`\nExecution Authority: `NONE`\n"
            "Historical blocker: `UNSAFE_IMPLEMENTATION`\n"
        )
        self.assertEqual(self.validate(self.omp + snapshot)["final_verdict"], "PASS")

    def test_03_unmarked_historical_packet_identity_fails(self):
        drift = self.omp + "\n## Old Packet\nPacket: `pkt_preview_deadbeef`\n"
        self.assertIn("OMP_HISTORICAL_STATE_LEAK", self.validate(drift)["errors"])

    def test_04_marked_historical_packet_with_no_authority_passes(self):
        snapshot = (
            "\n## Historical Packet Snapshot\nClassification: `HISTORICAL_SNAPSHOT`.\n"
            "Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`\n"
            "Scheduling Authority: `NONE`\nExecution Authority: `NONE`\n"
            "Packet: `pkt_preview_deadbeef`\n"
        )
        self.assertEqual(self.validate(self.omp + snapshot)["final_verdict"], "PASS")

    def test_05_pointer_not_resolving_to_cps_fails(self):
        drift = self.omp.replace(
            "Authoritative owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`",
            "Authoritative owner: `docs/programs/OTHER.md`",
            1,
        )
        self.assertIn("OMP_CURRENT_POINTER_MISMATCH", self.validate(drift)["errors"])

    def test_06_current_stop_mismatch_fails(self):
        drift = self.omp.replace("Resolved current stop: `UNSAFE_IMPLEMENTATION`", "Resolved current stop: `STOP_SAFE`", 1)
        self.assertIn("omp_current_stop_divergence", self.validate(drift)["omp_contradiction_ids"])

    def test_07_current_next_action_mismatch_fails(self):
        drift = self.omp.replace("Resolved current next action: `V7_FUTURE_SCALE_POLYGON_EXECUTION_HARNESS_V1`", "Resolved current next action: `DIAGNOSE_BINDING`", 1)
        self.assertIn("omp_current_next_action_divergence", self.validate(drift)["omp_contradiction_ids"])

    def test_08_latest_consumed_report_mismatch_fails(self):
        drift = self.omp.replace("docs/reports/engineering/2026-07-15_094920_future_scale_polygon_foundation.md", "docs/reports/engineering/stale.md")
        self.assertEqual(self.validate(drift)["omp_report_pointer_consistency"], "FAIL")

    def test_09_historical_section_cannot_create_mission(self):
        drift = self.omp.replace("Historical blocker:\n", "MISSION_ADMITTED = YES\n\nHistorical blocker:\n", 1)
        self.assertIn("OMP_HISTORICAL_STATE_LEAK", self.validate(drift)["errors"])

    def test_10_historical_section_cannot_authorize_packet_reuse(self):
        drift = self.omp.replace("Historical blocker:\n", "OLD_PACKETS_REUSABLE = YES\n\nHistorical blocker:\n", 1)
        self.assertIn("OMP_HISTORICAL_STATE_LEAK", self.validate(drift)["errors"])

    def test_11_section20_preserves_historical_evidence(self):
        section = self.lib._markdown_section(self.omp, "## 20. Stop Conditions", "## 21. Phase History")
        self.assertIn("Historical blocker:\n\n`UNSAFE_IMPLEMENTATION`", section)
        self.assertIn("pkt_preview_4eb137c926917c2761faadb4", section)

    def test_12_permanent_stop_rules_remain(self):
        section = self.lib._markdown_section(self.omp, "## 20. Stop Conditions", "## 21. Phase History")
        for stop in ("OPERATIONAL_AUTHORITY", "ENGINEERING_AUTHORITY", "REAL_WORLD_LIMIT", "UNSAFE_IMPLEMENTATION", "FUNDAMENTAL_ARCHITECTURE_GAP"):
            self.assertIn(stop, section)

    def test_13_cps_is_sole_volatile_owner(self):
        result = self.validate(self.omp)
        self.assertEqual(result["omp_current_pointer_consistency"], "PASS")
        self.assertEqual(result["omp_unqualified_live_heading_count"], 0)

    def test_14_cap_u01_complete_and_u07_waiting_use_live_state(self):
        cps_result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertIn("`COMPLETE`", cps_result["cap_u01"])
        self.assertIn("`CAP-U07`", cps_result["active_capability"])
        self.assertIn("| `UNSAFE_IMPLEMENTATION` |", cps_result["sequence_position_1"])

    def test_15_mission_identity_guard_remains_pass(self):
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(result["mission_identity_consistency"], "PASS")

    def test_16_cps_and_omp_contradictions_are_zero(self):
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(result["contradiction_count"], 0)
        self.assertEqual(result["omp_contradiction_count"], 0)

    def test_17_no_packet_lease_barrier_apply_or_movement(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"
        ))
        self.assertTrue(live["CONTROLLED_RUN_PACKET_PREVIEW"].strip("`").startswith("NONE_OPEN"))
        self.assertTrue(live["CONTROLLED_RUN_EXECUTION_AUTHORIZED"].strip("`").startswith("NO_CURRENT_PACKET"))
        self.assertTrue(live["USER_MOVEMENT"].strip("`").startswith("NO"))
        self.assertIn("state=OPEN", live["ADMIN_SAFE_MODE_LIVE_STATE"])

    def test_18_truth_consistency_is_go_only_when_omp_agrees(self):
        good = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(good["final_verdict"], "PASS")
        drift = self.omp.replace("Resolved current stop: `UNSAFE_IMPLEMENTATION`", "Resolved current stop: `STOP_SAFE`", 1)
        bad = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=drift)
        self.assertEqual(bad["final_verdict"], "NO-GO")


if __name__ == "__main__":
    unittest.main()
