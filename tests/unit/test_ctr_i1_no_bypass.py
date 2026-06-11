import importlib.machinery
import importlib.util
import inspect
import unittest
from pathlib import Path

from admin_core import operator_decision_surface as surface
from admin_core import operator_execution_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[2]
AUTOSWITCH = ROOT / "tools" / "v7-users-autoswitch"


def load_autoswitch_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_ctr_i1", str(AUTOSWITCH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CTRI1NoBypassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.autoswitch = load_autoswitch_module()

    def test_ctr_reuses_existing_trust_evolution_snapshot_family(self):
        families = set(self.autoswitch.RUNTIME_INTELLIGENCE_SNAPSHOT_FAMILIES)

        self.assertIn("trust-evolution-summaries", families)
        self.assertFalse(any(str(name).startswith("ctr") for name in families))
        self.assertFalse(any("channel-trust-recovery" in str(name) for name in families))

    def test_ctr_advisory_policy_has_no_runtime_authority(self):
        planner = self.autoswitch.AutoswitchPlanner
        source = inspect.getsource(planner._ctr_advisory_for_egress)

        self.assertIn('"planner_score_applied": False', source)
        self.assertIn('"hard_gate_applied": False', source)
        self.assertIn('"target_suppression_applied": False', source)
        self.assertIn('"runtime_execution_authority": "none"', source)
        self.assertIn('"selected_moves_write_authority": "none"', source)

    def test_ctr_surface_and_contract_do_not_gain_execution_primitives(self):
        combined = "\n".join([
            inspect.getsource(surface),
            inspect.getsource(pipeline.recommendation_execution_contract),
        ])
        forbidden = (
            "subprocess",
            "os.system",
            "run_action",
            "write_restore_barrier",
            "approve_packet(",
            "--apply",
            "v7-user-switch",
            "autoswitch_apply_run",
        )
        for token in forbidden:
            self.assertNotIn(token, combined)

    def test_ctr_governance_evidence_is_evidence_only(self):
        row = {
            "user": "10.7.0.3",
            "current_channel": "awg0",
            "recommended_channel": "awg3",
            "ctr_governance_evidence": {
                "state": "QUARANTINED",
                "review_required": True,
                "approval_authority": "none",
                "denial_authority": "none",
            },
            "review_required": True,
            "review_required_reasons": ["ctr_state_requires_operator_review"],
        }
        contract = pipeline.recommendation_execution_contract(row)

        self.assertTrue(contract["approval_packet_required"])
        self.assertFalse(contract["execution_allowed_now"])
        self.assertFalse(contract["runtime_mutation_performed"])
        self.assertEqual(contract["ctr_authority"]["approval_authority"], "none")
        self.assertEqual(contract["ctr_authority"]["denial_authority"], "none")
        self.assertEqual(contract["ctr_authority"]["restore_barrier_write_authority"], "none")


if __name__ == "__main__":
    unittest.main()
