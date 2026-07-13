import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
OMP = ROOT / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_self_continue_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpSelfContinuationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def cps(self, **overrides):
        values = {
            "CURRENT_NEXT_ACTION_ID": "CONTINUE_OMP",
            "CURRENT_MISSION_STATE": "TRANSACTION_STOP_CONTINUE_OMP_READY",
            "OMP_CONTINUATION_REQUIRED": "TRUE",
            "EXTERNAL_INPUT_REQUIRED": "FALSE",
            "EXTERNAL_INPUT_TYPE": "NONE",
            "TRANSACTION_TERMINAL_CLASS": "STOP_SAFE",
            "PROGRAM_TERMINAL_CLASS": "NONE",
            "NEXT_MISSION_FORMED": "TRUE",
            "NEXT_MISSION_ID": "NEXT_MISSION_V1",
            "PREMATURE_OPERATOR_RETURN": "FALSE",
            "CONTINUATION_ITERATION": "2",
            "CONTINUATION_STOP_REASON": "NONE",
            "NO_PROGRESS_FINGERPRINT": "a" * 64,
        }
        values.update(overrides)
        rows = "\n".join(f"| `{key}` | `{value}` |" for key, value in values.items())
        return (
            "## 0. Authoritative Live Current State\n\n"
            "| Field | Current Value |\n| --- | --- |\n"
            f"{rows}\n\n"
            "## Authoritative Unfinished Capability Closure Registry\n"
        )

    def validate(self, **overrides):
        return self.lib.omp_self_continuation_consistency(self.cps(**overrides))

    def test_transaction_terminal_continues_with_next_mission(self):
        self.assertEqual(self.validate()["final_verdict"], "PASS")

    def test_continue_omp_ready_cannot_return_operator(self):
        result = self.validate(OMP_CONTINUATION_REQUIRED="FALSE", NEXT_MISSION_FORMED="FALSE")
        self.assertIn("PREMATURE_OMP_RETURN_TO_OPERATOR", result["errors"])

    def test_true_external_boundary_returns_once(self):
        result = self.validate(
            OMP_CONTINUATION_REQUIRED="FALSE",
            EXTERNAL_INPUT_REQUIRED="TRUE",
            EXTERNAL_INPUT_TYPE="OPERATIONAL_AUTHORITY",
            PROGRAM_TERMINAL_CLASS="OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY",
            TRANSACTION_TERMINAL_CLASS="ROLLBACK_SUCCESS",
        )
        self.assertEqual(result["final_verdict"], "PASS")

    def test_external_boundary_cannot_continue(self):
        result = self.validate(
            EXTERNAL_INPUT_REQUIRED="TRUE",
            EXTERNAL_INPUT_TYPE="OPERATIONAL_AUTHORITY",
            PROGRAM_TERMINAL_CLASS="OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY",
        )
        self.assertIn("omp_external_boundary_continuation_conflict", result["errors"])

    def test_missing_next_mission_is_not_continuation(self):
        result = self.validate(NEXT_MISSION_FORMED="FALSE", NEXT_MISSION_ID="NONE")
        self.assertIn("omp_next_mission_not_formed", result["errors"])

    def test_no_progress_fingerprint_is_required(self):
        self.assertIn(
            "omp_no_progress_fingerprint_invalid",
            self.validate(NO_PROGRESS_FINGERPRINT="stale")["errors"],
        )

    def test_omp_contains_canonical_contract(self):
        text = OMP.read_text(encoding="utf-8")
        self.assertIn("Version: `4.20`", text)
        self.assertIn("### 14.1 OMP Self-Continuation Contract", text)
        self.assertIn("Engineering Polygon Scenario Supply Consumption Rule", text)
        self.assertIn("Proactive Verification Input Consumption Rule", text)
        self.assertIn("PREMATURE_OMP_RETURN_TO_OPERATOR", text)
        self.assertIn("OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY", text)

    def test_materialized_cps_stops_at_empty_frontier_real_world_limit(self):
        result = self.lib.omp_self_continuation_consistency(CPS.read_text(encoding="utf-8"))
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["omp_continuation_required"], "FALSE")
        self.assertEqual(result["external_input_required"], "TRUE")
        self.assertEqual(result["external_input_type"], "REAL_WORLD_LIMIT")
        self.assertEqual(result["continuation_iteration"], "7")

    def test_materialized_external_boundary_cannot_be_marked_for_continuation(self):
        cps = CPS.read_text(encoding="utf-8")
        cps = cps.replace("| `OMP_CONTINUATION_REQUIRED` | `FALSE` |", "| `OMP_CONTINUATION_REQUIRED` | `TRUE` |", 1)
        result = self.lib.omp_self_continuation_consistency(cps)
        self.assertIn("omp_external_boundary_continuation_conflict", result["errors"])


if __name__ == "__main__":
    unittest.main()
