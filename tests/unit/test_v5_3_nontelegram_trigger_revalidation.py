"""Revalidate existing non-Matrix trigger surfaces for V5.3.

This is a read-only Polygon contract test.  It inspects the checked-in owner
contracts and systemd wiring; it does not start services, probe production or
move a client.
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

FROZEN_CLASSES = (
    "HARD_CHANNEL_DOWN",
    "INTERFACE_OR_TUNNEL_PROCESS_ABSENT",
    "TUNNEL_UP_INTERNET_DEAD",
    "TELEGRAM_PERSISTENT_FAILURE",
    "REQUIRED_SERVICE_FAILURE",
    "OTHER_PROFILE_REQUIRED_SERVICE_FAILURE",
    "DNS_FAILURE",
    "PARTIAL_CENSORSHIP",
    "MULTI_SERVICE_FAILURE",
    "LATENCY_LOSS_JITTER_DEGRADATION",
    "TRANSIENT_FALSE_ALARM",
    "STALE_OR_UNKNOWN_STATE",
    "CONFLICTING_GENERATION",
    "TARGET_UNAVAILABLE",
    "CAPACITY_OR_POLICY_DENIAL",
    "FAIL_RECOVER_FAIL",
    "CLEAN_RECOVERY",
)


class V53NonTelegramTriggerRevalidationTest(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_frozen_17_class_inventory_is_exact(self):
        self.assertEqual(len(FROZEN_CLASSES), 17)
        self.assertEqual(len(set(FROZEN_CLASSES)), 17)

    def test_existing_local_failure_signal_reaches_existing_autoswitch_owner(self):
        diagnose = self.read("tools/v7-egress-diagnose")
        autoswitch = self.read("tools/v7-users-autoswitch")
        health = self.read("systemd/v7-health.service")
        caller = self.read("systemd/v7-users-autoswitch.service")
        timer = self.read("systemd/v7-users-autoswitch.timer")

        self.assertIn("interface_down_or_missing", diagnose)
        self.assertIn("v7-egress-diagnose", health)
        self.assertIn("v7-state-merge", health)
        self.assertIn("--execute-l3-production-validation", caller)
        self.assertIn("v7-users-autoswitch.service", timer)
        self.assertIn('reason == "interface_down_or_missing"', autoswitch)
        self.assertIn('"confirmed_current_channel_failure"', autoswitch)
        self.assertIn('"source_object": "v7-state.json:egress[].diagnose_severity/diagnose_reason + users.registry assignment"', autoswitch)
        self.assertIn('"owner": "tools/v7-users-autoswitch"', autoswitch)

    def test_generic_service_and_quality_surfaces_have_no_early_trigger(self):
        matrix_timer = self.read("systemd/v7-service-matrix-refresh.timer")
        matrix_service = self.read("systemd/v7-service-matrix-refresh.service")
        quality = self.read("tools/v7-egress-quality-compact")
        self.assertIn("OnUnitActiveSec=15min", matrix_timer)
        self.assertIn("v7-service-matrix-refresh-all", matrix_service)
        self.assertNotIn("--services", matrix_service)
        self.assertNotIn("systemctl start", quality)
        self.assertNotIn("wake_existing_matrix_consumer", quality)

    def test_safe_coverage_and_exact_residual(self):
        covered = {
            "HARD_CHANNEL_DOWN",
            "INTERFACE_OR_TUNNEL_PROCESS_ABSENT",
            "TELEGRAM_PERSISTENT_FAILURE",
        }
        safety_only = {
            "TRANSIENT_FALSE_ALARM",
            "STALE_OR_UNKNOWN_STATE",
            "CONFLICTING_GENERATION",
            "TARGET_UNAVAILABLE",
            "CAPACITY_OR_POLICY_DENIAL",
            "FAIL_RECOVER_FAIL",
        }
        residual = set(FROZEN_CLASSES) - covered - safety_only
        self.assertEqual(
            residual,
            {
                "TUNNEL_UP_INTERNET_DEAD",
                "REQUIRED_SERVICE_FAILURE",
                "OTHER_PROFILE_REQUIRED_SERVICE_FAILURE",
                "DNS_FAILURE",
                "PARTIAL_CENSORSHIP",
                "MULTI_SERVICE_FAILURE",
                "LATENCY_LOSS_JITTER_DEGRADATION",
                "CLEAN_RECOVERY",
            },
        )


if __name__ == "__main__":
    unittest.main()
