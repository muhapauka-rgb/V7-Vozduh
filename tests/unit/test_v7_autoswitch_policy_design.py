import unittest


def classify_egress_policy(
    *,
    service_failures=None,
    persistent_failures=None,
    telegram_degraded=False,
    telegram_hard_blocked=False,
    interface_up=True,
    route_class_fail=False,
    restore_stage=False,
    operator_approved=False,
):
    """Pure design fixture for the proposed E9.3.7 eligibility semantics."""
    service_failures = service_failures or []
    persistent_failures = persistent_failures or []
    critical_failures = set(service_failures)
    persistent = set(persistent_failures)

    hard_reasons = []
    soft_reasons = []
    state = "OK"
    eligible = True
    selected_moves = 0
    apply_requires_approval = False

    if not interface_up:
        hard_reasons.append("interface_down")
    if telegram_hard_blocked:
        hard_reasons.append("telegram_hard_blocked")
    if route_class_fail:
        hard_reasons.append("route_class_fail")

    if hard_reasons:
        return {
            "state": "HARD_INELIGIBLE",
            "eligible": False,
            "selected_moves": 1,
            "apply_requires_approval": restore_stage and not operator_approved,
            "hard_reasons": hard_reasons,
            "soft_reasons": soft_reasons,
        }

    if telegram_degraded:
        soft_reasons.append("telegram_degraded")

    for service in service_failures:
        soft_reasons.append(f"service_{service}_failed")

    if len(critical_failures) >= 2 or persistent:
        state = "CONDITIONAL_INELIGIBLE"
        eligible = False
        apply_requires_approval = restore_stage and not operator_approved
        selected_moves = 0 if apply_requires_approval else 1
    elif soft_reasons:
        state = "DEGRADED_SERVICE"
        eligible = True
        selected_moves = 0

    return {
        "state": state,
        "eligible": eligible,
        "selected_moves": selected_moves,
        "apply_requires_approval": apply_requires_approval,
        "hard_reasons": hard_reasons,
        "soft_reasons": soft_reasons,
    }


class AutoswitchPolicyDesignTest(unittest.TestCase):
    def test_instagram_single_sample_failure_is_penalty_only(self):
        result = classify_egress_policy(service_failures=["instagram"])
        self.assertEqual(result["state"], "DEGRADED_SERVICE")
        self.assertTrue(result["eligible"])
        self.assertEqual(result["selected_moves"], 0)
        self.assertIn("service_instagram_failed", result["soft_reasons"])

    def test_instagram_persistent_failure_is_conditional(self):
        result = classify_egress_policy(
            service_failures=["instagram"],
            persistent_failures=["instagram"],
        )
        self.assertEqual(result["state"], "CONDITIONAL_INELIGIBLE")
        self.assertFalse(result["eligible"])

    def test_telegram_degraded_without_hard_block_is_not_failover(self):
        result = classify_egress_policy(telegram_degraded=True)
        self.assertEqual(result["state"], "DEGRADED_SERVICE")
        self.assertTrue(result["eligible"])
        self.assertEqual(result["selected_moves"], 0)

    def test_interface_down_is_hard_ineligible(self):
        result = classify_egress_policy(interface_up=False)
        self.assertEqual(result["state"], "HARD_INELIGIBLE")
        self.assertFalse(result["eligible"])
        self.assertIn("interface_down", result["hard_reasons"])

    def test_multiple_critical_services_failed_is_conditional(self):
        result = classify_egress_policy(service_failures=["instagram", "youtube"])
        self.assertEqual(result["state"], "CONDITIONAL_INELIGIBLE")
        self.assertFalse(result["eligible"])

    def test_restore_stage_requires_separate_approval_for_conditional_move(self):
        result = classify_egress_policy(
            service_failures=["instagram", "youtube"],
            restore_stage=True,
            operator_approved=False,
        )
        self.assertEqual(result["state"], "CONDITIONAL_INELIGIBLE")
        self.assertTrue(result["apply_requires_approval"])
        self.assertEqual(result["selected_moves"], 0)

    def test_restore_stage_can_bound_move_after_approval(self):
        result = classify_egress_policy(
            service_failures=["instagram", "youtube"],
            restore_stage=True,
            operator_approved=True,
        )
        self.assertEqual(result["state"], "CONDITIONAL_INELIGIBLE")
        self.assertFalse(result["apply_requires_approval"])
        self.assertEqual(result["selected_moves"], 1)


if __name__ == "__main__":
    unittest.main()

