import importlib.machinery
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-ctr-observation-window"


def load_module():
    loader = importlib.machinery.SourceFileLoader("v7_ctr_observation_window", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CTRI5ObservationWindowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_module()

    def sample_plan(self):
        return {
            "updated": "2999-01-01T00:00:00+00:00",
            "ctr_shadow_comparison": {
                "cycles": [
                    {
                        "user_ip": "10.0.0.2",
                        "winner_without_ctr": "1",
                        "winner_with_ctr": "vless",
                        "same_winner": False,
                        "different_top3": True,
                        "different_pool_order": False,
                        "quality_delta": {
                            "verdict": "improved",
                            "trust_delta": 67,
                            "recovery_delta": 5,
                            "service_delta": 0,
                            "capacity_delta": 10,
                        },
                        "service_aware_validation": {
                            "telegram": {"verdict": "no_effect"},
                            "youtube": {"verdict": "no_effect"},
                            "instagram": {"verdict": "no_effect"},
                            "chatgpt": {"verdict": "no_effect"},
                            "google": {"verdict": "no_effect"},
                        },
                        "ctr_simulated_ranking": [
                            {
                                "channel": "vless",
                                "ctr_state": "TRUSTED",
                                "delta": 1,
                                "eligible": True,
                                "score": 98,
                                "service_impact": {"aggregate_score": 100},
                                "capacity_impact": {"capacity_score": 100},
                                "trust_impact": {"trust_score": 95},
                                "best_available_pool": True,
                            },
                            {
                                "channel": "1",
                                "ctr_state": "QUARANTINED",
                                "delta": -1,
                                "eligible": True,
                                "score": 100,
                                "service_impact": {"aggregate_score": 100},
                                "capacity_impact": {"capacity_score": 90},
                                "trust_impact": {"trust_score": 25},
                                "best_available_pool": True,
                            },
                        ],
                    }
                ],
                "no_bypass": {
                    "selected_moves_changed": False,
                    "planner_ranking_changed": False,
                    "runtime_behavior_changed": False,
                    "routing_changed": False,
                    "governance_authority_changed": False,
                    "packet_authority_changed": False,
                },
            },
        }

    def test_observation_window_certifies_positive_real_dry_run_window_when_threshold_met(self):
        report = self.tool.build_observation_window([self.sample_plan()], min_cycles=1)

        self.assertEqual(report["final_verdict"], "CTR_READY_FOR_SOFT_INFLUENCE")
        self.assertEqual(report["statistics"]["total_cycles"], 1)
        self.assertEqual(report["statistics"]["ranking_changes"], 1)
        self.assertEqual(report["statistics"]["winner_changes"], 1)
        self.assertEqual(report["statistics"]["positive_changes"], 1)
        self.assertEqual(report["statistics"]["negative_changes"], 0)
        self.assertEqual(report["statistics"]["ctr_usefulness_score"], 100.0)
        self.assertEqual(report["statistics"]["ctr_confidence_score"], 100.0)
        self.assertEqual(report["ctr_state_analysis"]["TRUSTED"]["winner_count"], 1)
        self.assertEqual(report["ctr_state_analysis"]["TRUSTED"]["top3_count"], 1)
        self.assertEqual(report["ctr_state_analysis"]["QUARANTINED"]["demoted"], 1)
        self.assertEqual(report["service_aware_certification"]["telegram"]["neutral"], 1)
        self.assertIn("MODEL_A_CURRENT", report["coefficient_calibration"])
        self.assertIn("MODEL_B_CONSERVATIVE", report["coefficient_calibration"])
        self.assertIn("MODEL_C_AGGRESSIVE", report["coefficient_calibration"])
        self.assertEqual(
            report["coefficient_calibration"]["MODEL_A_CURRENT"]["coefficients"]["TRUSTED"],
            20.0,
        )
        self.assertFalse(report["no_bypass"]["selected_moves_changed"])
        self.assertFalse(report["no_bypass"]["planner_ranking_changed"])
        self.assertFalse(report["no_bypass"]["runtime_changed"])
        self.assertEqual(report["readiness_review"]["soft_score_influence"], "READY")
        self.assertEqual(report["readiness_review"]["planner_influence"], "NOT_READY")

    def test_observation_window_requires_real_cycles(self):
        report = self.tool.build_observation_window([], min_cycles=1)

        self.assertEqual(report["final_verdict"], "INSUFFICIENT_DATA")
        self.assertEqual(report["statistics"]["total_cycles"], 0)
        self.assertTrue(report["readiness_review"]["more_observation_required"])


if __name__ == "__main__":
    unittest.main()
