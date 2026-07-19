import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"
OMP = ROOT / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_mission_roles_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CpsTerminalMissionIdentityRolesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        cls.omp = OMP.read_text(encoding="utf-8")
        cls.state = cls.lib._normalized_state_from_live_cps(cls.cps)
        cls.latest = cls.state["latest_terminal_mission_id"]
        cls.previous = cls.state["previous_terminal_mission_id"]
        cls.transition = cls.state["authoritative_transition_input_mission_id"]
        cls.report_path = cls.state["latest_terminal_mission_report"]
        cls.run_nonce = cls.state["latest_terminal_run_nonce"]

    def validate(self, cps=None, omp=None, root=ROOT):
        return self.lib.mission_role_consistency(
            cps or self.cps,
            root=root,
            omp_text=omp or self.omp,
            verify_external=True,
        )

    def replace_field(self, text, start, end, key, value):
        return self.lib._replace_section_field(text, start, end, key, value)

    def temp_root_with_report(self, first, second):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        report = root / self.report_path
        report.parent.mkdir(parents=True)
        report.write_text(f"{first}\n{second}\n", encoding="utf-8")
        return tmp, root

    def test_01_section0_new_registry_old_fails(self):
        drift = self.replace_field(self.cps, "### Registry Metadata And Truth Lifecycle", "### Active Protected Work In Progress", "LATEST_TERMINAL_MISSION_ID", f"`{self.previous}`")
        self.assertEqual(self.validate(drift)["registry_identity_consistency"], "FAIL")

    def test_02_section0_new_wip_old_latest_fails(self):
        drift = self.replace_field(self.cps, "### Active Protected Work In Progress", "### Complete Or Locked Capability Records", "latest_terminal_mission_id", f"`{self.previous}`")
        self.assertEqual(self.validate(drift)["active_wip_identity_consistency"], "FAIL")

    def test_03_terminal_mission_as_active_mission_fails(self):
        drift = self.replace_field(self.cps, "### Active Protected Work In Progress", "### Complete Or Locked Capability Records", "active_mission_id", f"`{self.latest}`")
        self.assertGreater(self.validate(drift)["terminal_mission_marked_active_count"], 0)

    def test_04_active_missions_none_with_execution_mission_fails(self):
        drift = self.replace_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "CURRENT_EXECUTION_MISSION_ID", f"`{self.latest}`")
        result = self.validate(drift)
        self.assertIn("active_missions_none_with_current_execution_mission", result["mission_identity_contradiction_ids"])

    def test_05_latest_differs_from_transition_with_explicit_roles_passes(self):
        self.assertNotEqual(self.latest, self.transition)
        self.assertEqual(self.validate()["transition_input_mission_consistency"], "PASS")

    def test_06_latest_differs_without_role_label_fails(self):
        drift = self.cps.replace("| `CURRENT_MISSION_ROLE` | `LATEST_TERMINAL_MISSION` |\n", "", 1)
        self.assertEqual(self.validate(drift)["cps_section0_identity_consistency"], "FAIL")

    def test_07_previous_terminal_role_is_explicit(self):
        self.assertEqual(self.validate()["previous_terminal_mission_consistency"], "PASS")

    def test_08_header_latest_differs_from_section0_fails(self):
        drift = self.cps.replace(f"Latest terminal Mission: `{self.latest}`", f"Latest terminal Mission: `{self.previous}`", 1)
        self.assertEqual(self.validate(drift)["cps_header_identity_consistency"], "FAIL")

    def test_09_header_timestamp_predates_latest_start_fails(self):
        captured = self.lib._cps_header_metadata(self.cps)["State captured"]
        drift = self.cps.replace(f"State captured: {captured}", "State captured: 2026-07-12T02:00:00+0700", 1)
        self.assertEqual(self.validate(drift)["mission_timestamp_consistency"], "FAIL")

    def test_10_latest_report_header_id_mismatch_fails(self):
        tmp, root = self.temp_root_with_report("Mission ID: `OLD`", f"Run Nonce: `{self.run_nonce}`")
        try:
            self.assertIn("latest_terminal_report_mission_id_mismatch", self.validate(root=root)["mission_identity_contradiction_ids"])
        finally:
            tmp.cleanup()

    def test_11_latest_report_nonce_mismatch_fails(self):
        tmp, root = self.temp_root_with_report(f"Mission ID: `{self.latest}`", "Run Nonce: `OLD`")
        try:
            self.assertEqual(self.validate(root=root)["mission_nonce_consistency"], "FAIL")
        finally:
            tmp.cleanup()

    def test_12_omp_latest_closure_pointer_mismatch_fails(self):
        drift = self.omp.replace(self.report_path, "docs/reports/engineering/stale.md")
        self.assertEqual(self.validate(omp=drift)["mission_report_pointer_consistency"], "FAIL")

    def test_13_omp_transition_input_pointer_mismatch_fails(self):
        drift = self.omp.replace("docs/reports/engineering/2026-07-11_225321_operation_scoped_binding_atomic_snapshot_closure_v3.md", "docs/reports/engineering/stale-binding.md")
        self.assertEqual(self.validate(omp=drift)["omp_transition_input_consistency"], "FAIL")

    def test_14_anti_replay_rejects_previous_as_latest(self):
        drift = self.replace_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "LATEST_TERMINAL_MISSION_ID", f"`{self.previous}`")
        self.assertEqual(self.validate(drift)["anti_replay_consistency"], "FAIL")

    def test_15_anti_replay_rejects_transition_input_as_latest(self):
        drift = self.replace_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "LATEST_TERMINAL_MISSION_ID", f"`{self.transition}`")
        self.assertEqual(self.validate(drift)["anti_replay_consistency"], "FAIL")

    def test_16_report_selector_requires_id_and_nonce_not_time(self):
        tmp, root = self.temp_root_with_report("Mission ID: `OLD`", "Run Nonce: `OLD`")
        try:
            self.assertEqual(self.validate(root=root)["report_selector_consistency"], "FAIL")
        finally:
            tmp.cleanup()

    def test_17_current_aliases_match_latest_fields(self):
        self.assertEqual(self.validate()["mission_role_ambiguity_count"], 0)

    def test_18_alias_divergence_fails(self):
        drift = self.replace_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "CURRENT_MISSION_ID", f"`{self.previous}`")
        self.assertIn("MISSION_ROLE_AMBIGUITY_STOP_SAFE", self.validate(drift)["errors"])

    def test_19_operational_state_is_production_certified(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"))
        self.assertEqual(live["CURRENT_STOP_CONDITION"].strip("`"), self.state["current_stop_condition"])
        self.assertEqual(live["CURRENT_ACTIVE_SCOPE"].strip("`"), self.state["current_active_scope"])
        self.assertEqual(live["CURRENT_ACTION_CLASS_STATE"].strip("`"), "GOVERNED_ONLY")

    def test_20_no_candidate_packet_lease_barrier_apply_or_movement(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"))
        self.assertTrue(live["CURRENT_CLASS_CANDIDATE_SELECTED"].strip("`").startswith("NONE_OPEN"))
        self.assertTrue(live["CONTROLLED_RUN_PACKET_PREVIEW"].strip("`").startswith("NONE_OPEN"))
        self.assertTrue(live["CONTROLLED_RUN_EXECUTION_AUTHORIZED"].strip("`").startswith("NO_CURRENT_PACKET"))
        movement = live["USER_MOVEMENT"].strip("`")
        self.assertTrue(
            movement.startswith("NO")
            or "owner-authorized bounded controlled user movement" in movement
        )

    def test_21_cap_u01_complete_and_u07_is_sequence_position_one(self):
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertIn("`CAP-U01`", result["cap_u01"])
        self.assertIn("`COMPLETE`", result["cap_u01"])
        self.assertIn("`CAP-U07`", result["active_capability"])
        self.assertIn(self.state["current_next_action_id"], result["sequence_position_1"])

    def test_22_current_stop_is_live_reality_only(self):
        self.assertEqual(self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)["current_stop"], self.state["current_stop_condition"])

    def test_23_omp_historical_isolation_remains_pass(self):
        self.assertEqual(self.lib.omp_live_state_consistency(self.cps, self.omp)["omp_historical_isolation"], "PASS")

    def test_24_full_truth_consistency_requires_all_roles(self):
        good = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(good["final_verdict"], "PASS")
        drift = self.replace_field(self.cps, "### Registry Metadata And Truth Lifecycle", "### Active Protected Work In Progress", "LATEST_TERMINAL_MISSION_ID", f"`{self.previous}`")
        bad = self.lib.cps_live_state_consistency(drift, root=ROOT, omp_text=self.omp)
        self.assertEqual(bad["final_verdict"], "NO-GO")


if __name__ == "__main__":
    unittest.main()
