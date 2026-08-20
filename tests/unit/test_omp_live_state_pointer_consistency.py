import importlib.util
import shutil
import tempfile
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
        cls.state = cls.lib._normalized_state_from_live_cps(cls.cps)

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
        drift = self.omp.replace(f"Resolved current stop: `{self.state['current_stop_condition']}`", "Resolved current stop: `STOP_SAFE`", 1)
        self.assertIn("omp_current_stop_divergence", self.validate(drift)["omp_contradiction_ids"])

    def test_07_current_next_action_mismatch_fails(self):
        drift = self.omp.replace(f"Resolved current next action: `{self.state['current_next_action_id']}`", "Resolved current next action: `DIAGNOSE_BINDING`", 1)
        self.assertIn("omp_current_next_action_divergence", self.validate(drift)["omp_contradiction_ids"])

    def test_08_latest_consumed_report_mismatch_fails(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        report = live["CURRENT_MISSION_REPORT"].strip("`")
        drift = self.omp.replace(
            f"Current active Mission report: `{report}`",
            "Current active Mission report: `docs/reports/engineering/stale.md`",
        )
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
        self.assertIn(f"`{self.state['current_stop_condition']}`", cps_result["sequence_position_1"])
        self.assertIn(self.state["current_next_action_id"], cps_result["sequence_position_1"])

    def test_15_mission_identity_guard_remains_pass(self):
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(result["mission_identity_consistency"], "PASS")

    def test_16_cps_and_omp_contradictions_are_zero(self):
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(result["contradiction_count"], 0)
        self.assertEqual(result["omp_contradiction_count"], 0)

    def test_17_product_evolution_frontier_does_not_grant_packet_or_movement(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"
        ))
        self.assertTrue(live["CONTROLLED_RUN_PACKET_PREVIEW"].strip("`").startswith("NONE_OPEN"))
        self.assertTrue(live["CONTROLLED_RUN_EXECUTION_AUTHORIZED"].strip("`").startswith("NO_CURRENT_PACKET"))
        self.assertIn(
            live["PRODUCT_EVOLUTION_FRONTIER"].strip("`"),
            {
                "SELECTIVE_SERVICE_FAILURE_COHORT_ADAPTER_BRIDGE",
                "EXACT_TIER_AUTHORITY_DECISION_REQUIRED",
                "CONTROLLED_SERVICE_FAILURE_CERTIFICATION_PLAN_AND_SAFE_COHORT_REQUIRED",
                f"{self.state['current_next_action_id']}; READY",
            },
        )
        movement = live["USER_MOVEMENT"].strip("`")
        self.assertIn("no scope expansion", movement)
        self.assertIn("state=OPEN", live["ADMIN_SAFE_MODE_LIVE_STATE"])

    def test_18_truth_consistency_is_go_only_when_omp_agrees(self):
        good = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(good["final_verdict"], "PASS")
        drift = self.omp.replace(f"Resolved current stop: `{self.state['current_stop_condition']}`", "Resolved current stop: `STOP_SAFE`", 1)
        bad = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=drift)
        self.assertEqual(bad["final_verdict"], "NO-GO")

    def test_19_existing_owner_atomically_reconciles_only_current_omp_pointers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            programs = root / "docs/programs"
            programs.mkdir(parents=True)
            shutil.copy2(CPS, programs / CPS.name)
            drift = self.omp.replace(
                f"Resolved current stop: `{self.state['current_stop_condition']}`",
                "Resolved current stop: `ENGINEERING_AUTHORITY`",
            ).replace(
                f"Resolved current next action: `{self.state['current_next_action_id']}`",
                "Resolved current next action: `STALE_AUTHORITY_REQUEST`",
            ).replace(
                f"Current terminal report: `{self.state['latest_terminal_mission_report']}`",
                "Current terminal report: `docs/reports/engineering/stale.md`",
            )
            (programs / OMP.name).write_text(drift, encoding="utf-8")
            result = self.lib.atomic_reconcile_omp_current_pointer_from_cps(
                root=root,
            )
            reconciled = (programs / OMP.name).read_text(encoding="utf-8")
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["status"], "OMP_POINTER_ATOMIC_UPDATE_APPLIED")
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        self.assertIn(
            f"Current active Mission report: `{live['CURRENT_MISSION_REPORT'].strip('`')}`",
            reconciled,
        )
        self.assertEqual(
            self.lib.omp_live_state_consistency(self.cps, reconciled)[
                "final_verdict"
            ],
            "PASS",
        )

    def test_20_existing_owner_reconciles_active_rs7_mission_report_pointer(self):
        mission_id = "TEST_RS7_MISSION"
        report = "docs/reports/engineering/test_rs7.md"
        cps = self.cps
        for key, value in (
            ("CURRENT_NEXT_ACTION_ID", "EXECUTE_TEST_RS7_MISSION"),
            ("CURRENT_PROGRAM_STAGE", "RS7_PHYSICAL_SIMPLIFICATION_EXECUTION"),
            ("CURRENT_PROGRAM_EXECUTION_FRONTIER", f"ADMITTED_READY_FOR_IMPLEMENTATION:{mission_id}"),
            ("CURRENT_EXECUTION_MISSION_ID", mission_id),
            ("CURRENT_EXECUTION_MISSION_STATE", "MISSION_ADMITTED"),
            ("CURRENT_MISSION_ROLE", "ACTIVE_MISSION"),
            ("CURRENT_MISSION_ID", mission_id),
            ("CURRENT_MISSION_STATE", "MISSION_ADMITTED"),
            ("CURRENT_MISSION_REPORT", report),
        ):
            cps = self.lib._replace_section_field(
                cps,
                "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
                key,
                f"`{value}`",
            )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            programs = root / "docs/programs"
            programs.mkdir(parents=True)
            (programs / CPS.name).write_text(cps, encoding="utf-8")
            (programs / OMP.name).write_text(self.omp, encoding="utf-8")
            result = self.lib.atomic_reconcile_omp_current_pointer_from_cps(root=root)
            reconciled = (programs / OMP.name).read_text(encoding="utf-8")
        self.assertTrue(result["ok"], result)
        self.assertIn(f"Current active Mission report: `{report}`", reconciled)


if __name__ == "__main__":
    unittest.main()
