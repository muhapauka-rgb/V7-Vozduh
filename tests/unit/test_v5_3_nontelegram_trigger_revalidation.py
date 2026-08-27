"""Revalidate the V5.3 current-source producer and Matrix receiver contract.

All scenarios use temporary Polygon state or checked-in owner contracts; no
production service, route or client is touched.
"""

from __future__ import annotations

import unittest
import importlib.machinery
import importlib.util
import json
import tempfile
from pathlib import Path
from unittest import mock


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
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "v7_service_matrix_refresh_shadow_trigger",
            str(ROOT / "tools/v7-service-matrix-refresh-all"),
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.matrix_refresh = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cls.matrix_refresh)

    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_frozen_17_class_inventory_is_exact(self):
        self.assertEqual(len(FROZEN_CLASSES), 17)
        self.assertEqual(len(set(FROZEN_CLASSES)), 17)

    def test_existing_local_failure_signal_reaches_existing_autoswitch_owner(self):
        diagnose = self.read("tools/v7-egress-diagnose")
        autoswitch = self.read("tools/v7-users-autoswitch")
        health = self.read("systemd/v7-health.service")

        self.assertIn("interface_down_or_missing", diagnose)
        health_loop = self.read("tools/runtime-support/v7-health-loop")
        self.assertIn("v7-health-loop", health)
        self.assertIn("v7-egress-diagnose", health_loop)
        self.assertIn("v7-state-merge", health_loop)
        # The health owner is the only automatic caller.  The governed
        # autoswitch service remains a manual recovery fallback, not a timer.
        installer = self.read("tools/v7-autoswitch-install-systemd")
        self.assertNotIn("v7-users-autoswitch.timer", installer)
        self.assertNotIn("enable --now v7-users-autoswitch.timer", installer)
        self.assertIn('reason == "interface_down_or_missing"', autoswitch)
        self.assertIn('"confirmed_current_channel_failure"', autoswitch)
        self.assertIn('"source_object": "v7-state.json:egress[].diagnose_severity/diagnose_reason + users.registry assignment"', autoswitch)
        self.assertIn('"owner": "tools/v7-users-autoswitch"', autoswitch)
        self.assertIn("--shadow-trigger-command", diagnose)
        self.assertIn("TUNNEL_UP_INTERNET_DEAD", diagnose)

    def test_generic_service_and_quality_surfaces_have_no_early_trigger(self):
        matrix_service = self.read("systemd/v7-service-matrix-refresh.service")
        quality = self.read("tools/v7-egress-quality-compact")
        self.assertIn("v7-service-matrix-refresh-all", matrix_service)
        self.assertNotIn("--services", matrix_service)
        self.assertNotIn("systemctl start", quality)
        self.assertNotIn("wake_existing_matrix_consumer", quality)

    def test_full_refresh_includes_only_disabled_controlled_interface_source(self):
        rows = [
            {"id": "ordinary-down", "enabled": "0", "type": "interface"},
            {
                "id": "controlled-down",
                "enabled": "0",
                "type": "interface",
                "controlled_certification_source": "1",
            },
            {"id": "healthy", "enabled": "1", "type": "interface"},
        ]
        selected, requested = self.matrix_refresh.select_probe_rows(rows, "")
        self.assertEqual(requested, [])
        self.assertEqual(
            sorted(row["id"] for row in selected),
            ["controlled-down", "healthy"],
        )
        with self.assertRaisesRegex(ValueError, "exact_egress_subset_not_enabled"):
            self.matrix_refresh.select_probe_rows(rows, "controlled-down")

    def test_shadow_trigger_is_exact_owner_backed_and_observation_only(self):
        contract = self.matrix_refresh.build_shadow_trigger_contract(
            source="hot",
            failure_class="REQUIRED_SERVICE_FAILURE",
            trigger_id="polygon-trigger-001",
            egresses=["hot"],
            services=["google", "telegram"],
        )
        self.assertEqual(contract["owner"], "tools/v7-service-matrix-refresh-all")
        self.assertEqual(contract["canonical_writer"], "tools/v7-service-matrix-test")
        self.assertEqual(contract["scope"], "EXACT_CURRENT_SOURCE_AND_REQUIRED_SERVICE_SUBSET")
        self.assertTrue(contract["idempotent"])
        self.assertTrue(contract["observation_only"])
        self.assertTrue(contract["full_matrix_fallback_preserved"])
        self.assertFalse(contract["consumer_invoked"])
        self.assertFalse(contract["routing_mutation_performed"])
        self.assertEqual(contract["users_moved"], 0)

    def test_shadow_trigger_cli_runs_exact_subset_without_consumer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            (state / "egress.registry").write_text(
                "id=hot enabled=1 state=enabled role=GLOBAL_FAST\n",
                encoding="utf-8",
            )
            argv = [
                "v7-service-matrix-refresh-all",
                "--state-dir", str(state),
                "--event-dir", str(root / "events"),
                "--checker", "/bin/echo",
                "--egresses", "hot",
                "--services", "google,telegram",
                "--shadow-trigger-source", "hot",
                "--shadow-trigger-class", "REQUIRED_SERVICE_FAILURE",
                "--shadow-trigger-id", "polygon-trigger-002",
                "--matrix-observation-only",
            ]
            fake_result = {
                "egress": "hot",
                "status": "OK",
                "ok": True,
                "service_matrix_lock": {"held": False},
                "service_results": {"google": {"ok": True, "status": "OK"}},
            }
            with mock.patch.object(self.matrix_refresh.subprocess, "run") as run:
                run.return_value = mock.Mock(returncode=0, stdout="{}", stderr="")
                with mock.patch.object(self.matrix_refresh, "run_one", return_value=fake_result):
                    with mock.patch("sys.argv", argv):
                        output = __import__("io").StringIO()
                        with mock.patch("sys.stdout", output):
                            rc = self.matrix_refresh.main()
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["mode"], "MATRIX_OBSERVATION_ONLY")
            self.assertEqual(payload["shadow_trigger"]["source_egress"], "hot")
            self.assertEqual(payload["shadow_trigger"]["services"], ["google", "telegram"])
            self.assertFalse(payload["shadow_trigger"]["consumer_invoked"])
            self.assertEqual(payload["observation_only"]["users_moved"], 0)

    def test_safe_coverage_and_exact_residual(self):
        covered = {
            "HARD_CHANNEL_DOWN",
            "INTERFACE_OR_TUNNEL_PROCESS_ABSENT",
            "TUNNEL_UP_INTERNET_DEAD",
            "TELEGRAM_PERSISTENT_FAILURE",
        }
        degraded_only = {"LATENCY_LOSS_JITTER_DEGRADATION"}
        recovery_only = {"CLEAN_RECOVERY", "FAIL_RECOVER_FAIL"}
        safety_only = {
            "TRANSIENT_FALSE_ALARM",
            "STALE_OR_UNKNOWN_STATE",
            "CONFLICTING_GENERATION",
            "TARGET_UNAVAILABLE",
            "CAPACITY_OR_POLICY_DENIAL",
        }
        residual = set(FROZEN_CLASSES) - covered - degraded_only - recovery_only - safety_only
        self.assertEqual(
            residual,
            {
                "REQUIRED_SERVICE_FAILURE",
                "OTHER_PROFILE_REQUIRED_SERVICE_FAILURE",
                "DNS_FAILURE",
                "PARTIAL_CENSORSHIP",
                "MULTI_SERVICE_FAILURE",
            },
        )


if __name__ == "__main__":
    unittest.main()
