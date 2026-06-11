import importlib.machinery
import importlib.util
import inspect
import unittest
from pathlib import Path

from admin_core import operator_decision_surface as surface
from admin_core import operator_execution_feedback as feedback
from admin_core import operator_execution_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[2]
AUTOSWITCH = ROOT / "tools" / "v7-users-autoswitch"


def load_autoswitch_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_ctr_i2", str(AUTOSWITCH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CTRI2ReviewRequiredTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.autoswitch = load_autoswitch_module()

    def test_review_required_matrix_is_informational_only(self):
        for state in ("NEW", "WATCH", "RECOVERING", "DEGRADED", "QUARANTINED"):
            with self.subTest(state=state):
                review = surface.ctr_review_semantics(state)
                self.assertTrue(review["review_required"])
                self.assertRegex(review["review_reason"], r"[А-Яа-яЁё]")
                self.assertRegex(review["review_recommendation"], r"[А-Яа-яЁё]")
        trusted = surface.ctr_review_semantics("TRUSTED")
        self.assertFalse(trusted["review_required"])

    def test_review_required_does_not_change_packet_authority(self):
        row = {
            "user": "10.7.0.3",
            "current_channel": "awg0",
            "recommended_channel": "awg3",
            "recommendation_hash": "rec-ctr-i2",
            "ctr_governance_evidence": {
                "state": "QUARANTINED",
                "review_required": True,
                "review_reason": "Канал в карантине.",
                "packet_preview": {"ctr_state": "QUARANTINED", "ctr_review_status": "REVIEW_REQUIRED"},
            },
            "review_required": True,
            "review_required_reasons": ["ctr_state_requires_operator_review"],
            "review_category": "emergency_only_review",
            "review_severity": "critical",
            "review_recommendation": "Только emergency или rollback review.",
            "review_warning": "Нельзя использовать как обычную цель.",
            "review_next_action": "Починить причину.",
            "emergency_only": True,
        }
        contract = pipeline.recommendation_execution_contract(row)
        packet = feedback.recommendation_approval_packet(row, actor="operator-a")

        self.assertTrue(contract["review_required"])
        self.assertTrue(contract["emergency_only"])
        self.assertFalse(contract["execution_allowed_now"])
        self.assertEqual(contract["ctr_authority"]["approval_authority"], "none")
        self.assertEqual(contract["ctr_authority"]["denial_authority"], "none")
        self.assertEqual(contract["ctr_authority"]["restore_barrier_write_authority"], "none")
        self.assertFalse(contract["ctr_authority"]["packet_authority_changed"])
        self.assertTrue(packet["ctr_review"]["review_required"])
        self.assertFalse(packet["ctr_review"]["packet_authority_changed"])
        self.assertFalse(packet["ctr_review"]["execution_authority_changed"])
        self.assertFalse(packet["execution_allowed_now"])

    def test_review_required_code_does_not_call_runtime_or_restore_barrier(self):
        combined = "\n".join([
            inspect.getsource(surface.ctr_review_semantics),
            inspect.getsource(pipeline.recommendation_execution_contract),
            inspect.getsource(feedback.recommendation_approval_packet),
        ])
        forbidden = (
            "subprocess",
            "os.system",
            "run_action",
            "write_restore_barrier",
            "append_restore_barrier",
            "execute_packet(",
            "runtime_recheck(",
            "v7-user-switch",
        )
        for token in forbidden:
            self.assertNotIn(token, combined)

    def test_ctr_review_does_not_become_score_part(self):
        score_source = inspect.getsource(self.autoswitch.AutoswitchPlanner._score_parts)
        candidate_source = inspect.getsource(self.autoswitch.AutoswitchPlanner._candidate)

        self.assertIn("c.ctr_advisory", candidate_source)
        self.assertNotIn("ctr", score_source)
        self.assertNotIn("review_required", score_source)


if __name__ == "__main__":
    unittest.main()
