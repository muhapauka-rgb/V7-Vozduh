import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"
OMP = ROOT / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_dependency_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpDependencyGraphCompletionOrderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        cls.omp = OMP.read_text(encoding="utf-8")

    def validate(self, text=None):
        return self.lib.capability_dependency_consistency(text or self.cps)

    def graph_row(self, text, capability_id):
        graph = self.lib._markdown_section(
            text,
            "### Capability Dependency Graph And Execution Frontier",
            "### Owner Revalidation Requirements And Contradictions",
        )
        return next(line for line in graph.splitlines() if line.startswith(f"| `{capability_id}` |"))

    def live_field(self, text, key, value):
        return self.lib._replace_section_field(
            text,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            key,
            f"`{value}`",
        )

    def test_01_cap_u02_is_waiting_external_dependency(self):
        result = self.validate()
        self.assertIn("CAP-U02", result["waiting_capabilities"])
        self.assertEqual(result["waiting_state_consistency"], "PASS")

    def test_02_waiting_capability_does_not_stop_unrelated_ready_capability(self):
        result = self.validate()
        self.assertFalse(result["premature_program_stop"])
        self.assertEqual(result["execution_frontier"], ["CAP-U07"])

    def test_03_dependent_capability_remains_blocked(self):
        result = self.validate()
        self.assertIn("CAP-U04", result["blocked_capabilities"])
        self.assertIn("CAP-U09", result["blocked_capabilities"])

    def test_04_independent_capability_is_executable(self):
        row = self.graph_row(self.cps, "CAP-U07")
        self.assertIn("| `READY` |", row)
        self.assertIn("| `YES` | `NO` |", row)

    def test_05_dependency_completion_recalculates_ready_frontier(self):
        text = self.cps
        u07 = self.graph_row(text, "CAP-U07")
        u07_done = u07.replace("| `READY` |", "| `COMPLETED` |", 1).replace(
            "| `YES` | `NO` |", "| `NO` | `YES` |", 1
        )
        text = text.replace(u07, u07_done, 1)
        u04 = self.graph_row(text, "CAP-U04")
        u04_ready = u04.replace("| `BLOCKED_BY_DEPENDENCY` |", "| `READY` |", 1).replace(
            "| `NO` | `NO` |", "| `YES` | `NO` |", 1
        )
        text = text.replace(u04, u04_ready, 1)
        blocked = self.validate()["blocked_capabilities"]
        blocked.remove("CAP-U04")
        text = self.live_field(text, "CURRENT_EXECUTION_FRONTIER", "CAP-U04")
        text = self.live_field(text, "READY_CAPABILITIES", "CAP-U04")
        text = self.live_field(text, "BLOCKED_CAPABILITIES", ",".join(blocked))
        text = self.live_field(text, "NEXT_EXECUTABLE_CAPABILITY", "CAP-U04")
        result = self.validate(text)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["execution_frontier"], ["CAP-U04"])

    def test_06_completion_order_violation_is_rejected(self):
        row = self.graph_row(self.cps, "CAP-U04")
        drift = self.cps.replace(row, row.replace("| `NO` | `NO` |", "| `NO` | `YES` |", 1), 1)
        result = self.validate(drift)
        self.assertTrue(any(item.startswith("COMPLETION_ORDER_VIOLATION:CAP-U04") for item in result["errors"]))

    def test_07_intent_closure_token_is_mandatory(self):
        drift = self.cps.replace("+INTENT_CLOSED", "+INTENT_UNKNOWN", 1)
        result = self.validate(drift)
        self.assertTrue(any(item.startswith("INTENT_CHAIN_INCOMPLETE:") for item in result["errors"]))

    def test_08_waiting_capability_cannot_create_packet(self):
        row = self.graph_row(self.cps, "CAP-U02")
        drift = self.cps.replace(row, row.replace("qualifying movement-protection production evidence", "create packet after evidence"), 1)
        self.assertIn("waiting_mutation_path_present:CAP-U02", self.validate(drift)["errors"])

    def test_09_waiting_capability_cannot_request_authority(self):
        row = self.graph_row(self.cps, "CAP-U02")
        drift = self.cps.replace(row, row.replace("qualifying movement-protection production evidence", "request authority after evidence"), 1)
        self.assertIn("waiting_mutation_path_present:CAP-U02", self.validate(drift)["errors"])

    def test_10_continue_omp_consumes_ready_frontier(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"
        ))
        self.assertEqual(live["OMP_CONTINUATION_REQUIRED"].strip("`"), "TRUE")
        self.assertEqual(live["CONTINUATION_DECISION"].strip("`"), "CONTINUE_READY_FRONTIER")

    def test_11_program_cannot_stop_while_ready_frontier_exists(self):
        drift = self.live_field(self.cps, "PROGRAM_TERMINAL_CLASS", "REAL_WORLD_LIMIT")
        result = self.validate(drift)
        self.assertTrue(result["premature_program_stop"])
        self.assertIn("ready_frontier_stopped_program", result["errors"])

    def test_12_existing_self_continuation_remains_pass(self):
        self.assertEqual(self.lib.omp_self_continuation_consistency(self.cps)["final_verdict"], "PASS")

    def test_13_cap_u01_remains_complete(self):
        self.assertIn("| `CAP-U01` | `COMPLETED` |", self.cps)

    def test_14_mission_identity_remains_pass(self):
        result = self.lib.mission_role_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(result["mission_identity_consistency"], "PASS")

    def test_15_cps_omp_consistency_remains_pass(self):
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=self.omp)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["dependency_violation_count"], 0)


if __name__ == "__main__":
    unittest.main()
