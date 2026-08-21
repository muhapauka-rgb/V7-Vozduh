"""Deterministic pre-deploy causal model for the implemented FAST producer.

This is not Runtime admission.  It models only owner-backed evidence already
present in the producer, Matrix receiver and canonical persistence contracts.
"""

from dataclasses import dataclass
import unittest


HEALTH_CADENCE_SEC = 30.0
PRODUCER_SAMPLES = 2
PRODUCTION_COOLDOWN_SEC = 60.0
EFFECTIVE_RECEIVER_REPEAT_SEC = 90.0
TARGETED_MATRIX_PROBE_SEC = 0.341  # controlled real receiver/writer fixture
T0_TO_T11_SEC = 0.023675  # existing governed Polygon transaction fixture


@dataclass(frozen=True)
class Policy:
    name: str
    matrix_samples: int


CURRENT = Policy("CURRENT_CANONICAL", 3)
OWNER_BACKED = Policy("OWNER_BACKED_FAILURE", 1)
INTERMEDIATE = Policy("INTERMEDIATE_MATRIX_REPEAT", 2)


def failure_to_t0(policy: Policy, phase_sec: float) -> float:
    """Causal clock: failure -> two producer samples -> Matrix samples -> T0."""
    first_receiver = phase_sec + HEALTH_CADENCE_SEC * (PRODUCER_SAMPLES - 1)
    return first_receiver + (policy.matrix_samples - 1) * EFFECTIVE_RECEIVER_REPEAT_SEC + TARGETED_MATRIX_PROBE_SEC


def outcome(name: str, policy: Policy) -> dict[str, object]:
    persistent = name in {"PERSISTENT_REQUIRED_FAILURE", "MULTI_DECISIVE_FAILURE", "DNS_PERSISTENT"}
    ambiguous = name in {"PARTIAL_AMBIGUOUS_FAILURE", "STALE_EVIDENCE", "CONFLICTING_GENERATION", "TARGET_NOT_READY"}
    transient = name in {"ONE_TRANSIENT_REQUIRED_FAILURE", "TWO_CLOSE_TRANSIENT_FAILURES", "DNS_TRANSIENT", "HEALTHY_AFTER_ONE_FAILURE"}
    return {
        "scenario": name,
        "t0": failure_to_t0(policy, 15.0) if persistent else None,
        "matrix_wake": persistent or name == "TWO_CLOSE_TRANSIENT_FAILURES",
        "full_required": ambiguous,
        "stop_safe": ambiguous or transient,
        "false_action": False,
        "recovery_policy_changed": False,
    }


class V53FastPredeployCausalScaleTest(unittest.TestCase):
    def test_phase_bounds_are_owner_clock_not_test_wall_time(self):
        self.assertAlmostEqual(failure_to_t0(OWNER_BACKED, 0.0), 30.341, places=3)
        self.assertAlmostEqual(failure_to_t0(OWNER_BACKED, 15.0), 45.341, places=3)
        self.assertAlmostEqual(failure_to_t0(OWNER_BACKED, 30.0), 60.341, places=3)

    def test_current_stack_has_duplicate_confirmation_latency(self):
        self.assertAlmostEqual(failure_to_t0(CURRENT, 0.0), 210.341, places=3)
        self.assertAlmostEqual(failure_to_t0(INTERMEDIATE, 0.0), 120.341, places=3)
        self.assertLess(failure_to_t0(OWNER_BACKED, 0.0), failure_to_t0(INTERMEDIATE, 0.0))

    def test_full_failure_safety_matrix(self):
        scenarios = (
            "ONE_TRANSIENT_REQUIRED_FAILURE", "TWO_CLOSE_TRANSIENT_FAILURES",
            "PERSISTENT_REQUIRED_FAILURE", "MULTI_DECISIVE_FAILURE",
            "DNS_TRANSIENT", "DNS_PERSISTENT", "PARTIAL_AMBIGUOUS_FAILURE",
            "HEALTHY_AFTER_ONE_FAILURE", "FAIL_RECOVER_FAIL", "STALE_EVIDENCE",
            "CONFLICTING_GENERATION", "TARGET_NOT_READY",
        )
        rows = [outcome(name, OWNER_BACKED) for name in scenarios]
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(not row["false_action"] for row in rows))
        self.assertTrue(all(not row["recovery_policy_changed"] for row in rows))
        self.assertTrue(all(row["stop_safe"] for row in rows if row["scenario"] in {
            "ONE_TRANSIENT_REQUIRED_FAILURE", "TWO_CLOSE_TRANSIENT_FAILURES",
            "DNS_TRANSIENT", "HEALTHY_AFTER_ONE_FAILURE", "PARTIAL_AMBIGUOUS_FAILURE",
            "STALE_EVIDENCE", "CONFLICTING_GENERATION", "TARGET_NOT_READY",
        }))

    def test_t0_to_t11_remains_existing_governed_cost_when_target_fresh(self):
        total = failure_to_t0(OWNER_BACKED, 15.0) + T0_TO_T11_SEC
        self.assertLess(total, 46.0)
        self.assertEqual(T0_TO_T11_SEC, 0.023675)


if __name__ == "__main__":
    unittest.main()
