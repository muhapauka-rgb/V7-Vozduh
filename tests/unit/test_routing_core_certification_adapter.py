import importlib.machinery
import importlib.util
import inspect
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-users-autoswitch"


def load_tool():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_reset_m6", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


autoswitch = load_tool()


class RoutingCoreCertificationAdapterTests(unittest.TestCase):
    def planner(self, *, max_moves=1):
        planner = autoswitch.AutoswitchPlanner.__new__(autoswitch.AutoswitchPlanner)
        planner.args = SimpleNamespace(
            user="10.7.0.114",
            source_egress="vless",
            target_egress="awg0",
            max_selected_moves=max_moves,
            approved_authority_generation="authority-reset-m6",
        )
        planner.egress = {
            "awg0": autoswitch.Egress(
                id="awg0", enabled=True, state="enabled", capacity_users=10, users=1
            )
        }
        return planner

    def plan(self):
        return {
            "operation": {
                "operation_id": "op-reset-m6",
                "planner_generation_id": "planner-reset-m6",
                "selected_move_hash": "moves-reset-m6",
            },
            "selected_moves": [
                {
                    "user_ip": "10.7.0.114",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                }
            ],
            "safety": {
                "atomic_execution_envelope": {
                    "envelope_id": "lease-reset-m6",
                    "envelope_hash": "fence-reset-m6",
                    "generation_id": "planner-reset-m6",
                },
                "authority_budget_gate": {},
            },
        }

    def authorized_plan(self):
        plan = self.plan()
        plan["safety"]["authority_budget_gate"] = {
            "current_action_class_contract": {
                "contract_id": "acc-reset-m6",
                "active_program": "V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1",
                "provenance": {"strict_provenance_contract": True},
            }
        }
        return plan

    def test_exact_core_decision_is_bound_to_existing_writer(self):
        plan = self.authorized_plan()
        result = self.planner().bind_routing_core_certification(plan)
        self.assertEqual(result["status"], "CORE_DECISION_BOUND_TO_EXISTING_WRITER")
        self.assertEqual(result["effect_writer"], "tools/v7-users-autoswitch.apply")
        self.assertTrue(result["decision_fingerprint"])
        self.assertFalse(result["runtime_mutation"])
        self.assertEqual(
            plan["operation"]["routing_core_decision_fingerprint"],
            result["decision_fingerprint"],
        )

    def test_non_one_user_scope_stops_safe(self):
        result = self.planner(max_moves=2).bind_routing_core_certification(self.authorized_plan())
        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertIn("core_certification_max_selected_moves_must_equal_one", result["blockers"])

    def test_direct_execute_dispatches_before_legacy_planner_initialization(self):
        result = {"status": "STOP_SAFE", "legacy_planner_initialized": False}
        argv = [
            "v7-users-autoswitch", "--routing-core-certification-execute",
            "--user", "10.7.0.114", "--source-egress", "awg0",
            "--target-egress", "awg3", "--max-selected-moves", "1",
        ]
        with mock.patch.object(autoswitch, "routing_core_certification_execute_only", return_value=result) as execute, \
             mock.patch.object(autoswitch, "AutoswitchPlanner", side_effect=AssertionError("legacy planner initialized")), \
             mock.patch("sys.argv", argv), mock.patch("builtins.print"):
            self.assertEqual(autoswitch.main(), 2)
        execute.assert_called_once()

    def test_direct_execute_uses_read_json_default_contract(self):
        source = inspect.getsource(autoswitch.routing_core_certification_execute_only)
        self.assertIn("read_json(policy_path, {})", source)


if __name__ == "__main__":
    unittest.main()
