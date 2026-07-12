import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_heartbeat_adapter_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpHeartbeatBoundaryAdapterTest(unittest.TestCase):
    AUTOMATION_ID = "v7-omp-heartbeat-dry-run"
    THREAD_ID = "thread-v7-omp-current"
    PROJECT_ID = "/Users/ponch/Documents/New project"

    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        live = cls.lib._markdown_field_table(cls.lib._markdown_section(
            cls.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        cls.generation = live["CURRENT_STATE_GENERATION"].strip("`")

    def contract(self, **overrides):
        values = {
            "AUTOMATION_ID": self.AUTOMATION_ID,
            "TARGET_THREAD_ID": self.THREAD_ID,
            "PROJECT_ID": self.PROJECT_ID,
            "WAKEUP_RUN_ID": "wakeup-run-20260712T220000Z",
            "EVENT_ID": "c" * 64,
            "EVENT_OWNER": "CODEX_AUTOMATION_PLATFORM",
            "EVENT_SOURCE": "OWNER_BACKED_DEPENDENCY_EVIDENCE",
            "EVENT_GENERATION": "owner-generation-1",
            "EVENT_TIME": "2026-07-12T22:00:00+07:00",
            "FRESHNESS_RULE": "OWNER_DEFINED_CURRENT",
            "DEPENDENCY_FINGERPRINT_BEFORE": "a" * 64,
            "DEPENDENCY_FINGERPRINT_AFTER": "a" * 64,
            "DEPENDENCY_CHANGED": False,
            "TARGET_CAPABILITY": "CAP-U07",
            "CURRENT_CPS_GENERATION": self.generation,
            "MISSION_SCOPE": "HEARTBEAT_REENTRY_DRY_RUN_ONLY",
            "AUTHORIZATION_SCOPE": "START_ENGINEERING_EXECUTION_CONTEXT_ONLY",
            "REPLAY_PROTECTION": (
                "MISSION_IDENTITY+CPS_GENERATION+EVENT_ID+WAKEUP_RUN_ID+DEPENDENCY_FINGERPRINT"
            ),
            "CONCURRENCY_CONTROL": (
                "CURRENT_EXECUTION_MISSION_ID+CURRENT_EXECUTION_MISSION_STATE+CURRENT_STATE_GENERATION"
            ),
            "ACTIVATION_RESULT": "PENDING_DRY_RUN",
            "EVIDENCE_FRESHNESS_RESULT": "PASS",
            "EVIDENCE_SUFFICIENCY_RESULT": "INSUFFICIENT",
            "NO_RUNTIME_AUTHORITY": True,
            "NO_USER_MOVEMENT_AUTHORITY": True,
            "NO_PACKET_AUTHORITY": True,
            "NO_CANDIDATE_AUTHORITY": True,
        }
        values.update(overrides)
        return values

    def evaluate(self, contract=None, cps=None, **kwargs):
        return self.lib.heartbeat_boundary_dry_run(
            cps or self.cps,
            contract or self.contract(),
            expected_automation_id=self.AUTOMATION_ID,
            expected_target_thread_id=self.THREAD_ID,
            expected_project_id=self.PROJECT_ID,
            **kwargs,
        )

    def changed_contract(self, **overrides):
        values = {
            "DEPENDENCY_FINGERPRINT_AFTER": "b" * 64,
            "DEPENDENCY_CHANGED": True,
            "EVIDENCE_SUFFICIENCY_RESULT": "SUFFICIENT",
        }
        values.update(overrides)
        return self.contract(**values)

    def test_01_valid_unchanged_heartbeat_returns_no_change(self):
        result = self.evaluate()
        self.assertEqual(result["activation_result"], "NO_CHANGE_DEPENDENCY_UNCHANGED")
        self.assertEqual(result["final_verdict"], "PASS")

    def test_02_changed_u07_fingerprint_exposes_dry_run_frontier_only(self):
        result = self.evaluate(self.changed_contract())
        self.assertEqual(result["activation_result"], "READY_FRONTIER_AVAILABLE_DRY_RUN_ONLY")
        self.assertEqual(result["ready_frontier_after"], ["CAP-U07"])
        self.assertFalse(result["mission_created"])

    def test_03_invalid_automation_identity_fails_closed(self):
        result = self.evaluate(self.contract(AUTOMATION_ID="other-automation"))
        self.assertEqual(result["activation_result"], "STOP_SAFE_IDENTITY_FAILURE")
        self.assertEqual(result["validators"]["heartbeat_identity_consistency"], "FAIL")

    def test_04_invalid_thread_identity_fails_closed(self):
        result = self.evaluate(self.contract(TARGET_THREAD_ID="other-thread"))
        self.assertEqual(result["activation_result"], "STOP_SAFE_IDENTITY_FAILURE")

    def test_05_invalid_project_identity_fails_closed(self):
        result = self.evaluate(self.contract(PROJECT_ID="/tmp/not-v7"))
        self.assertEqual(result["activation_result"], "STOP_SAFE_IDENTITY_FAILURE")

    def test_06_duplicate_event_is_no_change(self):
        contract = self.contract()
        result = self.evaluate(contract, seen_event_ids={contract["EVENT_ID"]})
        self.assertEqual(result["activation_result"], "NO_CHANGE_DUPLICATE_WAKEUP")
        self.assertEqual(result["validators"]["heartbeat_replay_protection"], "FAIL")

    def test_07_duplicate_wakeup_run_is_no_change(self):
        contract = self.contract()
        result = self.evaluate(contract, seen_wakeup_run_ids={contract["WAKEUP_RUN_ID"]})
        self.assertEqual(result["activation_result"], "NO_CHANGE_DUPLICATE_WAKEUP")

    def test_08_stale_cps_generation_fails_closed(self):
        result = self.evaluate(self.contract(CURRENT_CPS_GENERATION="cpsgen_stale"))
        self.assertEqual(result["activation_result"], "STOP_SAFE_REPLAY_FAILURE")
        self.assertIn("heartbeat_cps_generation_stale", result["errors"])

    def test_09_active_mission_blocks_second_activation(self):
        cps = self.lib._replace_section_field(
            self.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "CURRENT_EXECUTION_MISSION_ID",
            "`ACTIVE_MISSION_V1`",
        )
        cps = self.lib._replace_section_field(
            cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "CURRENT_EXECUTION_MISSION_STATE",
            "`EXECUTING`",
        )
        result = self.evaluate(cps=cps)
        self.assertEqual(result["activation_result"], "NO_CHANGE_ALREADY_ACTIVE")
        self.assertEqual(result["validators"]["heartbeat_concurrency_protection"], "BLOCKED")

    def test_10_changed_but_insufficient_evidence_is_no_change(self):
        result = self.evaluate(self.changed_contract(EVIDENCE_SUFFICIENCY_RESULT="INSUFFICIENT"))
        self.assertEqual(result["activation_result"], "NO_CHANGE_EVIDENCE_INSUFFICIENT")

    def test_11_stale_evidence_is_no_change(self):
        result = self.evaluate(self.changed_contract(EVIDENCE_FRESHNESS_RESULT="FAIL"))
        self.assertEqual(result["activation_result"], "NO_CHANGE_EVIDENCE_INSUFFICIENT")

    def test_12_authority_scope_expansion_fails_closed(self):
        result = self.evaluate(self.contract(AUTHORIZATION_SCOPE="RUNTIME_APPLY"))
        self.assertEqual(result["activation_result"], "STOP_SAFE_IDENTITY_FAILURE")
        self.assertEqual(result["validators"]["heartbeat_no_authority_expansion"], "FAIL")

    def test_13_no_candidate_packet_authority_runtime_or_user_mutation(self):
        result = self.evaluate(self.changed_contract())
        self.assertFalse(result["candidate_created"])
        self.assertFalse(result["packet_created"])
        self.assertEqual(result["authority_impact"], "NONE")
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["user_movement"], "NONE")
        self.assertEqual(result["validators"]["heartbeat_no_mutation"], "PASS")

    def test_14_no_automation_or_mission_execution(self):
        result = self.evaluate(self.changed_contract())
        self.assertFalse(result["automation_enabled"])
        self.assertFalse(result["mission_executed"])
        self.assertFalse(result["cps_mutated"])
        self.assertFalse(result["report_created"])
        self.assertFalse(result["git_changed"])

    def test_15_existing_omp_continuation_remains_unchanged(self):
        self.assertEqual(self.lib.omp_self_continuation_consistency(self.cps)["final_verdict"], "PASS")

    def test_16_dependency_graph_remains_consistent(self):
        result = self.lib.capability_dependency_consistency(self.cps)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["dependency_violation_count"], 0)

    def test_17_waiting_capabilities_are_preserved(self):
        result = self.evaluate(self.changed_contract())
        self.assertEqual(
            result["waiting_capabilities_preserved"],
            ["CAP-U02", "CAP-U05", "CAP-U06", "CAP-U07"],
        )

    def test_18_adapter_does_not_modify_cps_file(self):
        before = CPS.read_bytes()
        self.evaluate(self.changed_contract())
        self.assertEqual(CPS.read_bytes(), before)

    def test_19_dependency_change_claim_mismatch_fails_closed(self):
        result = self.evaluate(self.contract(DEPENDENCY_CHANGED=True))
        self.assertEqual(result["activation_result"], "STOP_SAFE_REPLAY_FAILURE")

    def test_20_report_or_chat_cannot_be_event_source(self):
        result = self.evaluate(self.contract(EVENT_SOURCE="historical report chat context"))
        self.assertEqual(result["activation_result"], "STOP_SAFE_IDENTITY_FAILURE")


if __name__ == "__main__":
    unittest.main()
