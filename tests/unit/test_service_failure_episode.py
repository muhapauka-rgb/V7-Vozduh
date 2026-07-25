import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"
AUTOSWITCH_TOOL = ROOT / "tools" / "v7-users-autoswitch"
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_module(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ServiceFailureEpisodeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_module("v7_service_matrix_episode", MATRIX_TOOL)
        cls.autoswitch = load_module("v7_users_autoswitch_episode", AUTOSWITCH_TOOL)

    def test_failure_episode_survives_repeated_matrix_writes_and_resets_on_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            failure = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T08:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": failure}, 1, event_dir=event_dir)
            failure["tested_at"] = "2026-07-25T08:01:00+00:00"
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": failure}, 1, event_dir=event_dir)
            failure["tested_at"] = "2026-07-25T08:02:00+00:00"
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": failure}, 1, event_dir=event_dir)

            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            self.assertEqual(row["failure_samples"], 3)
            self.assertEqual(row["consecutive_failures"], 3)
            self.assertGreaterEqual(row["bad_for_seconds"], 120)
            self.assertTrue(row["failure_episode_id"].startswith("sfep_"))
            self.assertEqual(row["probe_provenance"], "SERVICE_PROBE_OBSERVED")
            self.assertEqual(row["evidence_class"], "PROBE_OBSERVATION")
            events = [json.loads(line) for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["event_provenance"], "EXTERNAL_UNATTRIBUTED")
            self.assertFalse(events[0]["natural_production_credit"])

            recovery = {"ok": True, "status": "OK", "tested_at": "2026-07-25T08:03:00+00:00"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": recovery}, 1, event_dir=event_dir)
            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            self.assertEqual(row["failure_state"], "RECOVERY_OBSERVED")
            self.assertEqual(row["failure_samples"], 0)
            self.assertEqual(row["recovery_samples"], 1)

    def test_l3_consumer_rejects_transient_and_consumes_persistent_episode(self):
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        planner.service_signal_policy = {
            "service_failure_persistence_samples": 3,
            "service_failure_persistence_window_seconds": 180,
        }
        planner.switch_policy = {}
        planner.policy = {}
        planner.org_policy = {}
        planner.service_prefs = {}
        planner.matrix = {"items": {"vless": {"services": {
            "youtube": {
                "ok": False, "status": "FAIL", "failure_samples": 2,
                "failure_episode_id": "sfep_transient",
            },
            "google": {
                "ok": False, "status": "FAIL", "failure_samples": 3,
                "bad_for_seconds": 181, "failure_episode_id": "sfep_persistent",
                "observed_at": "2026-07-25T08:02:00+00:00",
            },
        }}}}
        failures = planner._l3_required_service_failures_for_source("vless")
        self.assertEqual([row["service"] for row in failures], ["google"])
        self.assertEqual(failures[0]["truth_class"], "PERSISTENT_FAIL")
        self.assertEqual(failures[0]["failure_episode_id"], "sfep_persistent")

    def test_passive_consumer_captures_natural_candidate_without_l8_credit_or_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            event = {
                "event_id": "sfe_natural_candidate",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "service": "youtube",
                "failure_episode_id": "sfep_1",
                "failure_samples": 3,
                "bad_for_seconds": 180,
                "observed_at": "2026-07-25T08:02:00+00:00",
                "source_hashes": {"service_row": "hash"},
            }
            (event_dir / "service-failure-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.event_dir = event_dir
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.service_signal_policy = {
                "service_failure_persistence_samples": 3,
                "service_failure_persistence_window_seconds": 180,
            }
            planner.l3_runtime_state = {}
            result = planner._consume_passive_production_events()
            self.assertTrue(result["active"])
            self.assertEqual(result["natural_event_candidates_captured"], 1)
            self.assertFalse(result["natural_production_credit"])
            rows = [json.loads(line) for line in (state_dir / "execution-events.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows[0]["evidence_class"], "NATURAL_PRODUCTION_CANDIDATE")
            self.assertEqual(rows[0]["decision"], "NO_ACTION_NATURAL_EVENT_PENDING_PROVENANCE_AND_LEGAL_OUTCOME")
            self.assertFalse(rows[0]["execution_performed"])

    def test_runtime_readiness_copy_never_claims_service_availability(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        self.assertIn("Runtime/config readiness: конфиг и runtime подтверждены текущим снимком; доступность сервисов этим не подтверждается.", source)
        self.assertIn("Сигнал: Runtime/config", source)


if __name__ == "__main__":
    unittest.main()
