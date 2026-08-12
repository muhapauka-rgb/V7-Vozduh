import importlib.machinery
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-service-matrix-refresh-all"
loader = importlib.machinery.SourceFileLoader("v7_service_matrix_refresh_operator_capture", str(TOOL))
tool = loader.load_module()


class OperatorInducedPassiveCaptureTest(unittest.TestCase):
    def test_full_refresh_delegates_matrix_lock_to_each_durable_checker_write(self):
        """Network probes must not inherit a batch-wide Matrix writer lock."""
        with mock.patch.object(
            tool.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(
                ["checker"],
                0,
                stdout=json.dumps({
                    "status": "OK",
                    "ok_count": 2,
                    "total": 2,
                    "service_matrix_lock": {"held": True, "scope": "atomic_durable_write"},
                }),
            ),
        ) as run:
            result = tool.run_one("source", 3, "checker", Path("/state"))
        self.assertTrue(result["ok"])
        self.assertTrue(result["service_matrix_lock"]["held"])
        self.assertNotIn("env", run.call_args.kwargs)

    def test_recovered_vless_history_is_captured_once_by_canonical_channel(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            (state / "egress.registry").write_text("id=vless protocol=vless enabled=1\n", encoding="utf-8")
            (state / "users.registry").write_text("ip=10.0.0.2 current=vless enabled=1\n", encoding="utf-8")
            history = [
                {"time": "2026-07-25T09:18:00+03:00", "vless_code": "200"},
                {"time": "2026-07-25T09:19:23+03:00", "vless_code": "000"},
                {"time": "2026-07-25T09:24:41+03:00", "vless_code": "000"},
                {"time": "2026-07-25T09:35:14+03:00", "vless_code": "200"},
            ]
            (state / "egress-history.jsonl").write_text("".join(json.dumps(row) + "\n" for row in history), encoding="utf-8")
            rows = tool.append_passive_failure_capture(
                events,
                state_dir=state,
                matrix={"items": {"1": {"services": {"x": {"ok": False}}}}},
                refresh_payload={"results": [{"egress": "1", "ok": False}]},
                provenance="OPERATOR_INDUCED",
                trigger_reference="operator-vless-external-unavailability-20260725T091923MSK",
                declared_channel="vless",
            )
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["channel"], "vless")
            self.assertEqual(rows[0]["observed_at"], "2026-07-25T09:19:23+03:00")
            self.assertEqual(rows[0]["history_episode"]["recovered_at"], "2026-07-25T09:35:14+03:00")
            self.assertFalse(rows[0]["natural_production_credit"])
            self.assertEqual(rows[0]["users_moved"], 0)
            self.assertEqual(
                tool.append_passive_failure_capture(
                    events, state_dir=state, matrix={}, refresh_payload={}, provenance="OPERATOR_INDUCED",
                    trigger_reference="operator-vless-external-unavailability-20260725T091923MSK", declared_channel="vless",
                ),
                [],
            )

    def test_event_only_scope_uses_current_failure_and_current_assignment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.0.0.2 current=failed enabled=true\n"
                "ip=10.0.0.3 current=healthy enabled=true\n",
                encoding="utf-8",
            )
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "failed": {"services": {"telegram": {"ok": False, "failure_state": "OBSERVED_CONTINUING"}}},
                "healthy": {"services": {"telegram": {"ok": True, "failure_state": "HEALTHY"}}},
            }}), encoding="utf-8")
            (events / "service-failure-events.jsonl").write_text(
                json.dumps({
                    "event_id": "current", "event_type": "SERVICE_FAILURE_OBSERVED",
                    "channel": "failed", "source_incident_id": "incident-current",
                    "source_scope": {"affected_scope_count": 50, "affected_scope_fingerprint": "old"},
                }) + "\n" + json.dumps({
                    "event_id": "stale", "event_type": "SERVICE_FAILURE_OBSERVED",
                    "channel": "healthy", "source_incident_id": "incident-stale",
                    "source_scope": {"affected_scope_count": 20, "affected_scope_fingerprint": "stale"},
                }) + "\n",
                encoding="utf-8",
            )
            result = tool.current_failed_source_scope(events, state)

        self.assertTrue(result["active"])
        self.assertEqual(result["active_sources"], [{
            "channel": "failed", "source_incident_id": "incident-current",
            "affected_scope_count": 1, "source_scope_fingerprint": "old",
            "event_id": "current", "source_currently_failed": True,
        }])


if __name__ == "__main__":
    unittest.main()
