import importlib.machinery
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-service-matrix-refresh-all"
loader = importlib.machinery.SourceFileLoader("v7_service_matrix_refresh_operator_capture", str(TOOL))
tool = loader.load_module()


class OperatorInducedPassiveCaptureTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
