import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"
AUTOSWITCH_TOOL = ROOT / "tools" / "v7-users-autoswitch"
REFRESH_TOOL = ROOT / "tools" / "v7-service-matrix-refresh-all"
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
        cls.refresh = load_module("v7_service_matrix_refresh_episode", REFRESH_TOOL)

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

    def test_availability_first_stage_receipt_is_exact_once_and_compact(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit_store = Path(tmp) / "operator-execution-audit.jsonl"
            result = {
                "final_verdict": "AVAILABILITY_FIRST_STANDING_STAGE_COMPLETED",
                "stage": 5,
                "standing_policy_contract_id": "sdpc_" + "a" * 24,
                "standing_policy_contract_hash": "a" * 64,
                "planner_allocation_fingerprint": "b" * 64,
                "execution_allocation_fingerprint": "b" * 64,
                "packet_set_fingerprint": "c" * 64,
                "allocation": [
                    {
                        "target_id": "awg3",
                        "allocated_users": 1,
                        "target_fingerprint": "d" * 64,
                        "capacity_bounds_fingerprint": "e" * 64,
                    },
                    {
                        "target_id": "awg0",
                        "allocated_users": 4,
                        "target_fingerprint": "f" * 64,
                        "capacity_bounds_fingerprint": "1" * 64,
                    },
                ],
                "allocation_immutable": True,
                "capacity_reservation_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "per_user_verification_passed": True,
                "per_target_verification_passed": True,
                "aggregate_verification_passed": True,
                "ordinary_user_protection_passed": True,
                "baseline_reset_verified": True,
            }
            first = self.refresh.record_availability_first_stage_consumption(
                audit_store=audit_store,
                result=result,
            )
            duplicate = self.refresh.record_availability_first_stage_consumption(
                audit_store=audit_store,
                result=result,
            )
            rows = [
                json.loads(line)
                for line in audit_store.read_text(encoding="utf-8").splitlines()
            ]

        self.assertTrue(first["audit_write"])
        self.assertTrue(duplicate["duplicate_suppressed"])
        self.assertEqual(first["receipt_id"], duplicate["receipt_id"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(
            sum(item["verified_scope"] for item in rows[0]["target_receipts"]),
            5,
        )
        self.assertFalse(rows[0]["raw_identity_list_stored"])
        self.assertNotIn("users", rows[0])
        self.assertFalse(rows[0]["natural_l8_credit"])

    def test_expected_http_response_is_visible_methodology_limit_not_failure_episode(self):
        for http_code in ("404", "405"):
            with self.subTest(http_code=http_code), mock.patch.object(
                self.matrix.subprocess,
                "run",
                return_value=SimpleNamespace(
                    stdout=f"{http_code} 0.101 0.202",
                    stderr="curl: (22) The requested URL returned error",
                    returncode=22,
                ),
            ):
                observed = self.matrix.run_curl_check(
                    "anthropic",
                    {"label": "Anthropic", "url": "https://api.anthropic.com/"},
                    "awg0",
                    8,
                )
            self.assertTrue(observed["ok"])
            self.assertTrue(observed["http_reachable"])
            self.assertTrue(observed["limited"])
            self.assertEqual(observed["status"], "HTTP_LIMITED")
            self.assertFalse(self.matrix.service_failure_observed(observed))
            episode = self.matrix.service_failure_episode(
                {"failure_episode_id": "sfep_old", "ok": False, "status": "FAIL"},
                observed,
                egress_id="awg0",
                service_id="anthropic",
                observed_at="2026-07-27T03:00:00+00:00",
                identity_generation="egid_test",
            )
            self.assertEqual(episode["probe_classification"], "HTTP_LIMITED")
            self.assertEqual(episode["failure_state"], "RECOVERY_OBSERVED")
            self.assertEqual(episode["failure_episode_id"], "")

    def test_actual_http_server_error_remains_failure(self):
        with mock.patch.object(
            self.matrix.subprocess,
            "run",
            return_value=SimpleNamespace(
                stdout="500 0.101 0.202",
                stderr="curl: (22) The requested URL returned error",
                returncode=22,
            ),
        ):
            observed = self.matrix.run_curl_check(
                "anthropic",
                {"label": "Anthropic", "url": "https://api.anthropic.com/"},
                "awg0",
                8,
            )
        self.assertFalse(observed["ok"])
        self.assertFalse(observed["http_reachable"])
        self.assertEqual(observed["status"], "FAIL")
        self.assertTrue(self.matrix.service_failure_observed(observed))

    def test_failure_episode_survives_production_timer_jitter_but_not_long_gap(self):
        self.assertEqual(
            self.matrix.FAILURE_EPISODE_CONTINUITY_SECONDS,
            2 * self.matrix.SERVICE_MATRIX_CADENCE_SECONDS
            + self.matrix.SERVICE_MATRIX_RANDOMIZED_DELAY_SECONDS
            + self.matrix.SERVICE_MATRIX_BATCH_BUDGET_SECONDS
            + self.matrix.SERVICE_MATRIX_CONTINUITY_SAFETY_SECONDS,
        )
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            first = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T08:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": first}, 1, event_dir=event_dir)
            jittered = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T08:16:10+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": jittered}, 1, event_dir=event_dir)
            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            first_episode = row["failure_episode_id"]
            self.assertEqual(row["failure_samples"], 2)
            self.assertGreaterEqual(row["bad_for_seconds"], 970)

            long_gap = {"ok": False, "status": "FAIL", "tested_at": "2026-07-25T09:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(matrix_file, "vless", "tun0", {"youtube": long_gap}, 1, event_dir=event_dir)
            row = json.loads(matrix_file.read_text(encoding="utf-8"))["items"]["vless"]["services"]["youtube"]
            self.assertEqual(row["failure_samples"], 1)
            self.assertNotEqual(row["failure_episode_id"], first_episode)

    def test_continuing_persistent_episode_emits_fresh_revalidation_without_new_episode(self):
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            first = {
                "ok": False,
                "status": "FAIL",
                "tested_at": "2026-07-27T03:00:00+00:00",
                "reason": "connection reset",
            }
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": first}, 1,
                event_dir=event_dir, persistence_samples=1,
            )
            second = dict(first, tested_at="2026-07-27T03:01:00+00:00")
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": second}, 1,
                event_dir=event_dir, persistence_samples=1,
            )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [row["event_type"] for row in events],
                ["SERVICE_FAILURE_OBSERVED", "SERVICE_FAILURE_REVALIDATED"],
            )
            revalidated = events[-1]
            self.assertEqual(revalidated["evidence_class"], "PROBE_OBSERVED_PRODUCTION_EVENT")
            self.assertTrue(revalidated["capture_only"])
            self.assertFalse(revalidated["natural_production_credit"])
            self.assertEqual(revalidated["correlated_services"], ["youtube"])
            self.assertTrue(revalidated["observation_generation"].startswith("sfrev_"))

    def test_matrix_revalidation_captures_compact_source_scope_without_raw_users(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n"
                "ip=10.0.0.4 current=awg0 enabled=1\n",
                encoding="utf-8",
            )
            matrix_file = state_dir / "service-matrix.json"
            event_dir = root / "events"
            failure = {"ok": False, "status": "FAIL", "tested_at": "2026-07-27T03:00:00+00:00", "reason": "reset"}
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", {"youtube": failure}, 1,
                event_dir=event_dir, persistence_samples=1, state_dir=state_dir,
            )
            event = json.loads((event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(event["source_scope"]["affected_scope_count"], 2)
        self.assertTrue(event["source_scope"]["affected_scope_fingerprint"])
        self.assertFalse(event["source_scope"]["raw_user_list_stored"])
        self.assertNotIn("affected_users", event["source_scope"])

    def test_failure_family_and_registry_generation_split_episode(self):
        previous = {
            "ok": False,
            "status": "FAIL",
            "reason": "connection refused",
            "observed_at": "2026-07-25T08:00:00+00:00",
            "failure_started_at": "2026-07-25T08:00:00+00:00",
            "failure_samples": 2,
            "failure_family": "TCP_CONNECTION_REFUSED",
            "egress_identity_generation": "egid_a",
            "failure_episode_id": "sfep_old",
        }
        changed_family = self.matrix.service_failure_episode(
            previous,
            {"ok": False, "status": "FAIL", "reason": "operation timed out"},
            egress_id="vless",
            service_id="youtube",
            observed_at="2026-07-25T08:01:00+00:00",
            identity_generation="egid_a",
        )
        self.assertEqual(changed_family["failure_family"], "TRANSPORT_TIMEOUT")
        self.assertEqual(changed_family["failure_samples"], 1)
        changed_generation = self.matrix.service_failure_episode(
            previous,
            {"ok": False, "status": "FAIL", "reason": "connection refused"},
            egress_id="vless",
            service_id="youtube",
            observed_at="2026-07-25T08:01:00+00:00",
            identity_generation="egid_b",
        )
        self.assertEqual(changed_generation["failure_samples"], 1)

    def test_correlated_failures_create_one_incident_and_recovery_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            matrix_file = Path(tmp) / "service-matrix.json"
            event_dir = Path(tmp) / "events"
            for minute in range(3):
                failures = {
                    service: {
                        "ok": False,
                        "status": "FAIL",
                        "tested_at": f"2026-07-25T08:0{minute}:00+00:00",
                        "reason": "connection refused",
                    }
                    for service in ("youtube", "google")
                }
                self.matrix.update_matrix(
                    matrix_file, "vless", "tun0", failures, 1,
                    event_dir=event_dir,
                    egress_identity={
                        "canonical_egress_id": "vless",
                        "egress_identity_generation": "egid_test",
                        "egress_identity_fingerprint": "fingerprint",
                    },
                )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            failure_events = [row for row in events if row["event_type"] == "SERVICE_FAILURE_OBSERVED"]
            self.assertEqual(len(failure_events), 2)
            self.assertEqual(len({row["source_incident_id"] for row in failure_events}), 1)
            self.assertEqual({row["failure_family"] for row in failure_events}, {"TCP_CONNECTION_REFUSED"})

            recovery = {
                service: {
                    "ok": True, "status": "OK",
                    "tested_at": "2026-07-25T08:03:00+00:00",
                }
                for service in ("youtube", "google")
            }
            self.matrix.update_matrix(
                matrix_file, "vless", "tun0", recovery, 1,
                event_dir=event_dir,
                egress_identity={
                    "canonical_egress_id": "vless",
                    "egress_identity_generation": "egid_test",
                    "egress_identity_fingerprint": "fingerprint",
                },
            )
            events = [
                json.loads(line)
                for line in (event_dir / "service-failure-events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            recovery_events = [row for row in events if row["event_type"] == "SERVICE_RECOVERY_OBSERVED"]
            self.assertEqual(len(recovery_events), 2)
            self.assertEqual(
                {row["source_incident_id"] for row in recovery_events},
                {failure_events[0]["source_incident_id"]},
            )

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

    def test_passive_consumer_correlates_children_and_emits_omp_frontier_then_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            incident = "sfinc_shared"
            children = [
                {
                    "event_id": f"sfe_{service}",
                    "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                    "channel": "vless",
                    "service": service,
                    "source_incident_id": incident,
                    "failure_episode_id": f"sfep_{service}",
                    "failure_family": "TCP_CONNECTION_REFUSED",
                    "failure_samples": 3,
                    "bad_for_seconds": 180,
                    "observed_at": "2026-07-25T08:02:00+00:00",
                    "source_hashes": {service: "hash"},
                }
                for service in ("youtube", "google")
            ]
            path = event_dir / "service-failure-events.jsonl"
            path.write_text(
                "".join(json.dumps(row) + "\n" for row in children),
                encoding="utf-8",
            )
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
            self.assertEqual(result["source_incident_ids"], [incident])
            self.assertEqual(result["records"]["outcome"], 1)
            self.assertEqual(
                result["omp_frontiers"][0]["frontier_id"],
                "V7_SERVICE_FAILURE_INCIDENT_RECONCILIATION",
            )
            self.assertEqual(
                result["omp_frontiers"][0]["failure_families"],
                ["TCP_CONNECTION_REFUSED"],
            )

            recovery = {
                "event_id": "sre_youtube",
                "event_type": "SERVICE_RECOVERY_OBSERVED",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_RECOVERY_EVENT",
                "channel": "vless",
                "service": "youtube",
                "source_incident_id": incident,
                "failure_episode_id": "sfep_youtube",
                "failure_family": "TCP_CONNECTION_REFUSED",
                "recovered_at": "2026-07-25T08:10:00+00:00",
            }
            with path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(recovery) + "\n")
            recovered = planner._consume_passive_production_events()
            self.assertEqual(
                recovered["omp_frontiers"][0]["frontier_id"],
                "V7_SERVICE_FAILURE_RECOVERY_RECONCILIATION",
            )
            outcomes = [
                json.loads(line)
                for line in (state_dir / "execution-events.jsonl").read_text(encoding="utf-8").splitlines()
                if "outcome_status" in json.loads(line)
            ]
            self.assertEqual(outcomes[-1]["temporal_observations"]["state"], "RECOVERED")

    def test_later_revalidation_reopens_incident_after_expiry_in_same_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            incident = "sfinc_expiry_then_revalidated"
            events = [
                {
                    "event_id": "sxe_old", "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_EPISODE_EXPIRY",
                    "source_incident_id": incident, "channel": "vless",
                    "observed_at": "2026-07-27T10:00:00+00:00",
                },
                {
                    "event_id": "sfrev_new", "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                    "source_incident_id": incident, "channel": "vless",
                    "failure_samples": 3, "bad_for_seconds": 180,
                    "observed_at": "2026-07-27T10:01:00+00:00",
                    "source_scope": {
                        "affected_scope_count": 2,
                        "affected_scope_fingerprint": "scope-reopened",
                        "source_channel": "vless",
                        "raw_user_list_stored": False,
                    },
                },
            ]
            (event_dir / "service-failure-events.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in events), encoding="utf-8",
            )
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
            rows = [json.loads(line) for line in (state_dir / "closure-records.jsonl").read_text(encoding="utf-8").splitlines()]
            closure = next(row for row in rows if row.get("object_type") == "passive_production_event")
        self.assertTrue(result["active"])
        self.assertEqual(closure["terminal_outcome_classification"], "STOP_SAFE_NO_ACTION")
        self.assertEqual(closure["source_scope"]["affected_scope_count"], 2)
        self.assertEqual(closure["terminal_resolution"]["latest_event_id"], "sfrev_new")
        self.assertEqual(closure["terminal_resolution"]["superseded_terminal_event_ids"], ["sxe_old"])

    def test_runtime_readiness_copy_never_claims_service_availability(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        self.assertIn("Runtime/config readiness: конфиг и runtime подтверждены текущим снимком; доступность сервисов этим не подтверждается.", source)
        self.assertIn("Сигнал: Runtime/config", source)
        self.assertIn("Устойчивый failure episode", source)
        self.assertIn("Parent incident:", source)
        self.assertIn("failure family:", source)
        self.assertIn("channelServiceEpisodeSummary", source)

    def test_capture_only_entrypoint_consumes_without_constructing_planner_side_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            event = {
                "event_id": "sfe_capture_only_entrypoint",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "service": "youtube",
                "failure_episode_id": "sfep_capture_only",
                "failure_samples": 3,
                "bad_for_seconds": 180,
                "observed_at": "2026-07-25T08:02:00+00:00",
                "source_hashes": {"service_row": "hash"},
            }
            (event_dir / "service-failure-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
            args = self.autoswitch.build_arg_parser().parse_args([
                "--consume-passive-events-only",
                "--state-dir", str(state_dir),
                "--event-dir", str(event_dir),
                "--policy-file", str(root / "missing-policy.json"),
                "--org-policy-file", str(root / "missing-org-policy.json"),
            ])
            result = self.autoswitch.consume_passive_events_only(args)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["result"]["natural_event_candidates_captured"], 1)
            self.assertFalse(any(result["forbidden_effects"].values()))
            self.assertFalse((state_dir / "client-reconnect-state.json").exists())
            self.assertFalse((state_dir / "autoswitch-safety.json").exists())
            self.assertTrue((state_dir / "execution-events.jsonl").exists())
            self.assertTrue((state_dir / "closure-records.jsonl").exists())
            self.assertTrue((state_dir / "runtime-trust.jsonl").exists())

    def test_capture_only_entrypoint_rejects_apply_or_authority_flags(self):
        args = self.autoswitch.build_arg_parser().parse_args([
            "--consume-passive-events-only",
            "--apply",
            "--promote-authority-to", "LARGE_BATCH",
        ])
        result = self.autoswitch.consume_passive_events_only(args)
        self.assertEqual(result["status"], "STOP_SAFE_FORBIDDEN_FLAGS")
        self.assertIn("passive_consumer_forbids_apply", result["blockers"])
        self.assertIn("passive_consumer_forbids_promote_authority_to", result["blockers"])

    def test_passive_idempotent_reentry_consumes_new_packet_bound_outcome(self):
        """An already-consumed observation must not hide a newer action Outcome."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            incident_id = "sfinc_idempotent_outcome"
            source_scope = {
                "source_channel": "vless",
                "affected_scope_count": 1,
                "affected_scope_fingerprint": "scope_idempotent_outcome",
                "observed_at": "2026-07-27T12:00:00+00:00",
            }
            event = {
                "event_id": "sfrev_idempotent_outcome",
                "source_incident_id": incident_id,
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "PROBE_OBSERVED_PRODUCTION_EVENT",
                "channel": "vless",
                "service": "youtube",
                "failure_episode_id": "sfep_idempotent_outcome",
                "failure_samples": 3,
                "bad_for_seconds": 180,
                "observed_at": "2026-07-27T12:00:00+00:00",
                "source_hashes": {"service_row": "hash"},
                "source_scope": source_scope,
            }
            (event_dir / "service-failure-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg3 enabled=1\n", encoding="utf-8",
            )
            args = self.autoswitch.build_arg_parser().parse_args([
                "--consume-passive-events-only",
                "--state-dir", str(state_dir),
                "--event-dir", str(event_dir),
                "--policy-file", str(root / "missing-policy.json"),
                "--org-policy-file", str(root / "missing-org-policy.json"),
            ])
            first = self.autoswitch.consume_passive_events_only(args)
            self.assertEqual(first["result"]["reason"], "consumed")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb_idempotent_outcome",
                "source_channel": "vless",
                "target_channel": "awg3",
                "user": "10.0.0.2",
                "packet_id": "pkt_idempotent_outcome",
                "terminal_outcome_classification": "SUCCESS",
                "verification_result": {"success": True},
                "service_failure_causal_binding": {
                    "source_incident_id": incident_id,
                    "source_event_id": event["event_id"],
                    "source_event_ids": [event["event_id"]],
                    "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                    "source_scope": source_scope,
                },
            }
            with (state_dir / "execution-events.jsonl").open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(outcome) + "\n")
            second = self.autoswitch.consume_passive_events_only(args)
            third = self.autoswitch.consume_passive_events_only(args)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(item for item in state["incidents"].values() if item.get("incident_id") == incident_id)
        self.assertEqual(second["result"]["reason"], "already_consumed_idempotent")
        self.assertEqual(second["result"]["scope_reconciliation"]["consumed_records"], 1)
        self.assertEqual(third["result"]["scope_reconciliation"]["changed_records"], 0)
        self.assertEqual(record["last_execution_feedback_id"], outcome["feedback_id"])
        self.assertFalse(any(second["forbidden_effects"].values()))

    def test_newer_owner_backed_scope_rotates_current_denominator_only(self):
        """A newer revalidation replaces only current scope, never Outcome history."""
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        state = {}
        incident_id = "sfinc_newer_scope"
        old = {
            "source_incident_id": incident_id,
            "event_id": "sfrev_old_scope",
            "source_event_ids": ["sfrev_old_scope"],
            "channel": "vless",
            "observed_at": "2026-07-27T12:00:00+00:00",
            "source_scope": {
                "source_channel": "vless", "affected_scope_count": 3,
                "affected_scope_fingerprint": "scope_old",
                "observed_at": "2026-07-27T12:00:00+00:00",
            },
        }
        newer = {
            **old,
            "event_id": "sfrev_new_scope",
            "source_event_ids": ["sfrev_new_scope"],
            "observed_at": "2026-07-27T12:15:00+00:00",
            "source_scope": {
                "source_channel": "vless", "affected_scope_count": 2,
                "affected_scope_fingerprint": "scope_new",
                "observed_at": "2026-07-27T12:15:00+00:00",
            },
        }
        planner._materialize_passive_incident_projection(state, old, terminal="STOP_SAFE_NO_ACTION")
        projection = planner._materialize_passive_incident_projection(state, newer, terminal="STOP_SAFE_NO_ACTION")
        record = state["incidents"][projection["incident_key"]]
        self.assertEqual(record["current_source_scope"]["baseline_event_id"], "sfrev_new_scope")
        self.assertEqual(record["current_source_scope"]["affected_scope_count"], 2)
        self.assertEqual(
            record["current_source_scope"]["supersedes_prior_scope_generation"]["rotation_reason"],
            "FRESHER_OWNER_BACKED_SOURCE_SCOPE_GENERATION",
        )

    def test_passive_consumer_does_not_materialize_unbound_expiry_as_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = root / "events"
            state_dir = root / "state"
            event_dir.mkdir()
            state_dir.mkdir()
            (event_dir / "service-failure-events.jsonl").write_text(
                json.dumps({
                    "event_id": "sxe_without_parent",
                    "event_type": "SERVICE_FAILURE_EPISODE_EXPIRED",
                    "capture_only": True,
                    "event_provenance": "EXTERNAL_UNATTRIBUTED",
                    "evidence_class": "PROBE_OBSERVED_EPISODE_EXPIRY",
                    "channel": "vless",
                }) + "\n",
                encoding="utf-8",
            )
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
            self.assertFalse(result["active"])
            self.assertEqual(result["reason"], "no_passive_capture_event")
            self.assertFalse((state_dir / "l3-runtime-state.json").exists())

    def test_matrix_lifecycle_reports_passive_consumer_success_and_failure_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            consumer = root / "passive-consumer"
            consumer.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'status':'PASS','result':{'reason':'consumed'}}))\n",
                encoding="utf-8",
            )
            consumer.chmod(0o755)
            ok = self.refresh.run_passive_consumer(
                str(consumer),
                state_dir=state_dir,
                event_dir=event_dir,
            )
            self.assertTrue(ok["ok"])
            self.assertEqual(ok["status"], "PASS")
            self.assertNotIn("omp_repair_frontier", ok)

            failed = self.refresh.run_passive_consumer(
                str(root / "missing-consumer"),
                state_dir=state_dir,
                event_dir=event_dir,
            )
            self.assertFalse(failed["ok"])
            self.assertEqual(failed["omp_repair_frontier"]["frontier_id"], "V7_PASSIVE_SERVICE_EVENT_CONSUMER_REPAIR")
            self.assertEqual(failed["omp_repair_frontier"]["forbidden_effects"], "NONE")

    def test_matrix_lifecycle_invokes_bounded_executor_only_with_active_standing_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            policy_file = root / "policy.json"
            policy_file.write_text("{}", encoding="utf-8")
            inactive = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertTrue(inactive["ok"])
            self.assertEqual(inactive["status"], "INACTIVE_NO_STANDING_POLICY")
            self.assertFalse(inactive["action_attempted"])

            valid_policy = {
                "delegated_autonomy_policy": {
                    "status": "ACTIVE",
                    "contract_id": "sdpc_test_tier4",
                    "contract_hash": "a" * 64,
                    "expires_at": "2099-08-27T02:06:51+00:00",
                    "policy": {
                        "allowed_action_classes": ["channel hard-fail failover"],
                        "max_users_per_action": 4,
                        "max_concurrent_transactions": 1,
                        "max_blast_radius": {"users": 4},
                        "policy_state": "APPROVED",
                        "runtime_apply_enabled": True,
                        "self_expansion_allowed": False,
                    },
                    "per_action_law": {
                        "max_users": 4,
                        "max_concurrent_transactions": 1,
                    },
                },
            }
            policy_file.write_text(
                json.dumps(valid_policy),
                encoding="utf-8",
            )
            obligation = {
                "schema_version": "v7.service-failure-automation-obligation.v1",
                "object_type": "service_failure_automation_obligation",
                "object_id": "sfaob_test_tier4",
                "automation_obligation_id": "sfaob_test_tier4",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "source_incident_id": "sfinc_test_tier4",
                "channel": "vless",
                "stop_safe_classification": "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED",
                "bounded_recommendation_users": 4,
                "current_source_scope": {
                    "affected_scope_count": 4,
                    "protected_scope_count": 0,
                    "unresolved_scope_count": 4,
                    "explicitly_excluded_or_recovered_scope_count": 0,
                    "affected_scope_fingerprint": "scope-test-tier4",
                    "raw_user_list_stored": False,
                },
            }
            executor = root / "executor"
            executor.write_text(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                "max_users=sys.argv[sys.argv.index('--max-users')+1]\n"
                "print(json.dumps({'final_verdict':'STOP_SAFE','users_moved':0,'apply_executed':False,'max_users_argument':max_users}))\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            executor.chmod(0o755)
            stop = self.refresh.run_bounded_delegated_service_failure_action(
                str(executor),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
                service_failure_obligation=obligation,
            )
            self.assertTrue(stop["ok"])
            self.assertEqual(stop["status"], "STOP_SAFE")
            self.assertTrue(stop["action_attempted"])
            self.assertEqual(stop["users_moved"], 0)
            self.assertEqual(stop["admitted_max_users"], 4)
            self.assertEqual(stop["max_concurrent_transactions"], 1)
            self.assertEqual(stop["consumer_result"]["max_users_argument"], "4")
            self.assertEqual(stop["contract_id"], "sdpc_test_tier4")
            command = stop["command"]
            self.assertEqual(
                command[command.index("--expected-standing-policy-contract-id") + 1],
                "sdpc_test_tier4",
            )
            self.assertEqual(
                command[command.index("--expected-standing-policy-contract-hash") + 1],
                "a" * 64,
            )
            self.assertEqual(
                command[command.index("--expected-service-failure-obligation-id") + 1],
                "sfaob_test_tier4",
            )
            self.assertEqual(
                command[command.index("--expected-service-failure-incident-id") + 1],
                "sfinc_test_tier4",
            )
            self.assertEqual(
                command[command.index("--expected-service-failure-scope-fingerprint") + 1],
                "scope-test-tier4",
            )
            self.assertEqual(
                command[command.index("--approved-source") + 1],
                "vless",
            )

            executor.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({"
                "'final_verdict':'GOVERNED_TRANSACTION_STOPPED',"
                "'transaction_status':'STOP_SAFE',"
                "'stop_reason':'packet_not_ready',"
                "'users_moved':0,'apply_executed':False}))\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            governed_stop = self.refresh.run_bounded_delegated_service_failure_action(
                str(executor),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
                service_failure_obligation=obligation,
            )
            self.assertTrue(governed_stop["ok"])
            self.assertEqual(governed_stop["status"], "STOP_SAFE")
            self.assertFalse(governed_stop["runtime_mutation_performed"])

            invalid_policy = json.loads(json.dumps(valid_policy))
            invalid_policy["delegated_autonomy_policy"]["per_action_law"]["max_users"] = 1
            policy_file.write_text(json.dumps(invalid_policy), encoding="utf-8")
            invalid = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertTrue(invalid["ok"])
            self.assertEqual(invalid["status"], "STOP_SAFE_INVALID_STANDING_POLICY_SCOPE")
            self.assertFalse(invalid["action_attempted"])
            self.assertEqual(invalid["users_moved"], 0)

            expired_policy = json.loads(json.dumps(valid_policy))
            expired_policy["delegated_autonomy_policy"]["expires_at"] = "2020-01-01T00:00:00+00:00"
            policy_file.write_text(json.dumps(expired_policy), encoding="utf-8")
            expired = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertTrue(expired["ok"])
            self.assertEqual(expired["status"], "STOP_SAFE_INVALID_STANDING_POLICY_SCOPE")
            self.assertFalse(expired["action_attempted"])

            zero_scope = json.loads(json.dumps(obligation))
            zero_scope["current_source_scope"]["affected_scope_count"] = 0
            zero_scope["current_source_scope"]["unresolved_scope_count"] = 0
            policy_file.write_text(json.dumps(valid_policy), encoding="utf-8")
            no_action = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
                service_failure_obligation=zero_scope,
            )
            self.assertEqual(no_action["status"], "STOP_SAFE_CURRENT_SOURCE_SCOPE_EMPTY")
            self.assertFalse(no_action["action_attempted"])
            self.assertEqual(no_action["users_moved"], 0)

            missing = self.refresh.run_bounded_delegated_service_failure_action(
                str(root / "missing-executor"),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertEqual(missing["status"], "STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION")
            self.assertFalse(missing["action_attempted"])

    def test_advisory_without_result_has_no_obligation_and_does_not_crash(self):
        self.assertEqual(
            self.refresh.service_failure_obligation_from_advisory(None),
            {},
        )
        self.assertEqual(
            self.refresh.service_failure_obligation_from_advisory(
                {"status": "PASS", "result": None}
            ),
            {},
        )
        obligation = {"automation_obligation_id": "sfaob_exact"}
        self.assertEqual(
            self.refresh.service_failure_obligation_from_advisory(
                {"status": "PASS", "result": {"obligation": obligation}}
            ),
            obligation,
        )

    def test_campaign_binding_rejects_shallow_ready_target_when_full_admission_fails(self):
        authority = {
            "status": "APPROVED",
            "request_id": "cpsauth_exact",
            "request_hash": "a" * 64,
            "decision": (
                "APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN"
            ),
            "decision_id": "cpsdec_exact",
            "request": {
                "scope": {
                    "source_id": "controlled-source",
                    "controlled_target_id": "execution-target",
                    "campaign_stages": [5, 10, 25, 48],
                    "max_concurrent_transactions": 1,
                    "ordinary_customer_involvement": False,
                },
            },
        }
        campaign = {
            "ok": True,
            "completed_stages": [],
            "next_stage": 5,
            "controlled_production_proven_max": 0,
            "receipt_ids": [],
        }
        with mock.patch.object(
            self.refresh.operator_execution,
            "read_audit_records",
            return_value=[],
        ), mock.patch.object(
            self.refresh.operator_execution,
            "controlled_certification_substrate_authority_status",
            return_value=authority,
        ), mock.patch.object(
            self.refresh.operator_execution,
            "validate_controlled_certification_substrate_authority_request",
            return_value={"ok": True, "errors": []},
        ), mock.patch.object(
            self.refresh.operator_execution,
            "controlled_certification_campaign_stage_status",
            return_value=campaign,
        ):
            result = self.refresh.controlled_certification_matrix_binding(
                audit_store=Path("/tmp/not-read"),
                source="controlled-source",
                target_selection_diagnostic={
                    "ok": True,
                    "status": (
                        "NO_CURRENT_TARGET_CAPACITY_WITH_EXACT_OWNER_BOUNDARY"
                    ),
                    "inventory_fingerprint": "b" * 64,
                },
            )

        self.assertFalse(result["active"])
        self.assertFalse(result["ok"])
        self.assertIn(
            "controlled_campaign_target_full_live_admission_failed",
            result["blockers"],
        )
        self.assertEqual(
            result["target_selection_status"],
            "NO_CURRENT_TARGET_CAPACITY_WITH_EXACT_OWNER_BOUNDARY",
        )

    def test_matrix_binds_controlled_source_to_next_approved_campaign_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            policy_file = root / "policy.json"
            policy_file.write_text(json.dumps({
                "delegated_autonomy_policy": {
                    "status": "ACTIVE",
                    "contract_id": "sdpc_campaign",
                    "contract_hash": "b" * 64,
                    "expires_at": "2099-08-27T02:06:51+00:00",
                    "policy": {
                        "allowed_action_classes": [
                            "channel hard-fail failover",
                        ],
                        "max_users_per_action": 48,
                        "max_concurrent_transactions": 1,
                        "max_blast_radius": {"users": 48},
                        "policy_state": "APPROVED",
                        "runtime_apply_enabled": True,
                        "self_expansion_allowed": False,
                    },
                    "per_action_law": {
                        "max_users": 48,
                        "max_concurrent_transactions": 1,
                    },
                },
            }), encoding="utf-8")
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_campaign",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "source_incident_id": "sfinc_campaign",
                "channel": "controlled-source",
                "stop_safe_classification": (
                    "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED"
                ),
                # The execution-only campaign target is intentionally absent
                # from the ordinary planner recommendation.  Exact campaign
                # binding must reach the governed executor, which rechecks
                # every live target gate independently.
                "bounded_recommendation_users": 0,
                "current_source_scope": {
                    "affected_scope_count": 48,
                    "unresolved_scope_count": 48,
                    "affected_scope_fingerprint": "scope-campaign",
                },
            }
            executor = root / "executor"
            executor.write_text(
                "#!/usr/bin/env python3\n"
                "import json,sys\n"
                "print(json.dumps({'final_verdict':'STOP_SAFE',"
                "'apply_executed':False,'users_moved':0,"
                "'argv':sys.argv[1:]}))\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            executor.chmod(0o755)
            binding = {
                "active": True,
                "ok": True,
                "request_id": "cpsauth_campaign",
                "request_hash": "c" * 64,
                "decision_id": "cpsdec_campaign",
                "source": "controlled-source",
                "target": "execution-target",
                "stages": [5, 10, 25, 48],
                "completed_stages": [],
                "next_stage": 5,
            }
            with mock.patch.object(
                self.refresh,
                "controlled_certification_matrix_binding",
                return_value=binding,
            ):
                result = self.refresh.run_bounded_delegated_service_failure_action(
                    str(executor),
                    state_dir=state_dir,
                    event_dir=event_dir,
                    policy_file=policy_file,
                    operator_execution_audit_store=root / "audit.jsonl",
                    service_failure_obligation=obligation,
                )
        self.assertEqual(result["status"], "STOP_SAFE", result)
        self.assertEqual(result["requested_max_users"], 5)
        argv = result["consumer_result"]["argv"]
        self.assertEqual(argv[argv.index("--max-users") + 1], "5")
        self.assertEqual(
            argv[
                argv.index(
                    "--controlled-certification-campaign-request-id"
                ) + 1
            ],
            "cpsauth_campaign",
        )
        self.assertEqual(
            argv[
                argv.index(
                    "--controlled-certification-campaign-stage"
                ) + 1
            ],
            "5",
        )
        self.assertEqual(result["users_moved"], 0)

    def test_campaign_stage_receipt_requires_consumed_outcome_replay_learning_and_is_exact_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.jsonl"
            binding = {
                "request_id": "cpsauth_stage",
                "request_hash": "d" * 64,
                "decision_id": "cpsdec_stage",
                "source": "controlled-source",
                "target": "execution-target",
                "next_stage": 5,
            }
            incomplete = self.refresh.record_controlled_campaign_stage_consumption(
                audit_store=audit,
                binding=binding,
                result={"fresh_packet_id": "pkt_incomplete"},
                reset_result={},
            )
            self.assertFalse(incomplete["audit_write"])
            self.assertFalse(audit.exists())

            result = {
                "fresh_packet_id": "pkt_stage",
                "final_verdict": "GOVERNED_TRANSACTION_COMPLETED",
                "apply_executed": True,
                "users_moved": 5,
                "feedback_materialization": {
                    "materialized": True,
                    "outcome_id": "out_stage",
                },
                "l3_learning_closure": {
                    "materialized": True,
                    "records": {"closure": 5},
                    "execution_closure_verification": {
                        "behavior_chain_status": "COMPLETE",
                        "terminal_consumer_verified": True,
                    },
                },
            }
            reset_result = {
                "ok": True,
                "consumer_result": {
                    "final_verdict": (
                        "CONTROLLED_CERTIFICATION_CAMPAIGN_STAGE_RESET_COMPLETE"
                    ),
                    "receipt_id": "reset_stage",
                    "target_user_count_after": 0,
                    "ordinary_customer_count": 0,
                    "users_moved": 5,
                    "final_safe_mode": "OPEN",
                },
            }
            first = self.refresh.record_controlled_campaign_stage_consumption(
                audit_store=audit,
                binding=binding,
                result=result,
                reset_result=reset_result,
            )
            second = self.refresh.record_controlled_campaign_stage_consumption(
                audit_store=audit,
                binding=binding,
                result=result,
                reset_result=reset_result,
            )
            self.assertTrue(first["audit_write"])
            self.assertFalse(second["audit_write"])
            self.assertTrue(second["duplicate_suppressed"])
            rows = [
                json.loads(line)
                for line in audit.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(rows), 1)
            self.assertTrue(rows[0]["outcome_consumed"])
            self.assertTrue(rows[0]["replay_consumed"])
            self.assertTrue(rows[0]["learning_consumed"])
            self.assertTrue(rows[0]["baseline_reset_verified"])

    def test_matrix_lifecycle_treats_no_pending_omp_obligation_as_legal_noop(self):
        completed = mock.Mock(
            returncode=0,
            stdout=json.dumps({
                "schema_version": "v7.service-failure-automation-omp-consumption.v1",
                "final_verdict": "NO_PENDING_OBLIGATION",
                "runtime_impact": "NONE",
                "routing_impact": "NONE",
                "user_movement": 0,
            }),
        )
        with mock.patch.object(self.refresh.subprocess, "run", return_value=completed):
            result = self.refresh.run_service_failure_omp_consumer()
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["consumer_result"]["final_verdict"], "NO_PENDING_OBLIGATION")

    def test_matrix_delegates_fresh_allocation_materialization_to_executor(self):
        fingerprint = "a" * 64
        diagnostic = {
            "status": "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED",
            "availability_first_standing_policy_admission": {
                "ok": True,
            },
            "shared_production_target_capacity_projection": {
                "availability_campaign": {
                    "next_stage": 1,
                    "completed": False,
                },
                "stage_allocations": {
                    "1": {
                        "feasible": True,
                        "allocation_fingerprint": fingerprint,
                    },
                },
            },
        }
        stopped = {
            "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
            "transaction_status": "STOP_SAFE",
            "stop_reason": "fresh_live_gate_failed",
            "blockers": ["fresh_live_gate_failed"],
        }
        calls = [
            mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
            mock.Mock(returncode=2, stdout=json.dumps(stopped)),
        ]
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=calls,
        ) as run:
            result = self.refresh.run_availability_first_standing_policy_stage(
                "v7-users-autoswitch",
                "v7-governed-canary-dry-run-cycle",
                state_dir=Path("/opt/v7/egress/state"),
                event_dir=Path("/opt/v7/events"),
                policy_file=Path("/etc/v7/policy.json"),
                audit_store=Path(
                    "/opt/v7/audit/operator-execution-audit.jsonl"
                ),
            )
        executor_command = run.call_args_list[1].args[0]
        self.assertIn(
            "--execute-availability-first-standing-stage",
            executor_command,
        )
        self.assertNotIn(
            "--expected-availability-first-allocation-fingerprint",
            executor_command,
        )
        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertEqual(
            result["allocation_fingerprint"],
            fingerprint,
        )

    def test_matrix_recovers_partial_apply_from_append_only_event_after_summary_advances(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.100 current=awg0 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix-refresh-summary.json").write_text(
                json.dumps({
                    "availability_first_standing_policy_action": {
                        "status": "STOP_SAFE",
                        "consumer_result": {
                            "stop_reason": (
                                "availability_first_standing_stage_not_admitted"
                            ),
                        },
                    },
                }),
                encoding="utf-8",
            )
            (events / "service-matrix-refresh-20260731.jsonl").write_text(
                json.dumps({
                    "availability_first_standing_policy_action": {
                        "status": "STOP_SAFE",
                        "stage": 1,
                        "consumer_result": {
                            "stage": 1,
                            "packet_set": [{
                                "stop_reason": (
                                    "l3_production_validation_downstream_proof_failed"
                                ),
                                "user": "10.7.0.100",
                                "source": "vless",
                                "target": "awg0",
                            }],
                        },
                    },
                }) + "\n",
                encoding="utf-8",
            )
            (events / "service-matrix-refresh-20260727.jsonl").write_bytes(
                b"x" * (
                    self.refresh.RECENT_MATRIX_EVENT_BYTE_LIMIT * 2
                )
            )
            diagnostic = {
                "status": "STOP_SAFE",
                "availability_first_standing_policy_admission": {
                    "ok": True,
                },
                "shared_production_target_capacity_projection": {
                    "availability_campaign": {
                        "next_stage": 1,
                        "completed": False,
                    },
                    "stage_allocations": {},
                },
            }
            reconciled = {
                "final_verdict": (
                    "AVAILABILITY_FIRST_PARTIAL_APPLY_BASELINE_RECONCILED"
                ),
                "transaction_status": "STOP_SAFE",
                "stop_reason": (
                    "fresh_retry_required_after_partial_apply_reconciliation"
                ),
                "stage": 1,
                "baseline_reset_verified": True,
            }
            calls = [
                mock.Mock(returncode=2, stdout=json.dumps(diagnostic)),
                mock.Mock(returncode=2, stdout=json.dumps(reconciled)),
            ]
            with mock.patch.object(
                self.refresh.subprocess,
                "run",
                side_effect=calls,
            ) as run:
                result = (
                    self.refresh.run_availability_first_standing_policy_stage(
                        "v7-users-autoswitch",
                        "v7-governed-canary-dry-run-cycle",
                        state_dir=state,
                        event_dir=events,
                        policy_file=root / "policy.json",
                        audit_store=root / "audit.jsonl",
                    )
                )

        self.assertEqual(len(run.call_args_list), 2)
        self.assertIn(
            "--execute-availability-first-standing-stage",
            run.call_args_list[1].args[0],
        )
        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertEqual(
            result["consumer_result"]["final_verdict"],
            "AVAILABILITY_FIRST_PARTIAL_APPLY_BASELINE_RECONCILED",
        )

    def test_matrix_projection_preserves_bounded_partial_reset_terminal(self):
        projected = self.refresh._consumer_projection({
            "status": "STOP_SAFE",
            "consumer_result": {
                "final_verdict": "AVAILABILITY_FIRST_STANDING_STAGE_STOPPED",
                "transaction_status": "STOP_SAFE",
                "stop_reason": "availability_first_partial_apply_recovery_failed",
                "partial_apply_recovery": {
                    "pending": True,
                    "ok": True,
                    "stage": 1,
                    "user": "10.7.0.100",
                    "source": "vless",
                    "target": "awg0",
                    "packet_id": "pkt_partial",
                    "operation_id": "govexec_partial",
                    "projection_source": "append_only_matrix_event",
                },
                "reset_transaction": {
                    "final_verdict": "GOVERNED_TRANSACTION_STOPPED",
                    "transaction_status": "STOP_SAFE",
                    "stop_reason": "packet_not_ready",
                    "runtime_mutation_performed": False,
                    "users_moved": 0,
                },
                "stage": 1,
                "baseline_reset_verified": True,
                "outcome_consumed": True,
                "replay_consumed": True,
                "learning_consumed": True,
                "durable_successor": (
                    "EXISTING_MATRIX_RECOMPUTE_"
                    "AVAILABILITY_FIRST_NEXT_STAGE"
                ),
                "baseline_reset_reconciliation": {
                    "ok": True,
                    "mode": (
                        "PARTIAL_CHILD_TERMINAL_RECONCILED_"
                        "FROM_EXISTING_OWNERS"
                    ),
                    "current_egress": "vless",
                    "packet_id": "pkt_reset",
                    "operation_id": "govexec_reset",
                    "switch_lineage": True,
                    "natural_l8_credit": False,
                    "production_outcome_credit": False,
                },
            },
        })

        consumer = projected["consumer_result"]
        self.assertTrue(consumer["partial_apply_recovery"]["ok"])
        self.assertEqual(
            consumer["reset_transaction"]["stop_reason"],
            "packet_not_ready",
        )
        self.assertEqual(consumer["stage"], 1)
        self.assertTrue(consumer["baseline_reset_verified"])
        self.assertTrue(consumer["outcome_consumed"])
        self.assertEqual(
            consumer["baseline_reset_reconciliation"]["mode"],
            (
                "PARTIAL_CHILD_TERMINAL_RECONCILED_"
                "FROM_EXISTING_OWNERS"
            ),
        )
        self.assertFalse(
            consumer["baseline_reset_reconciliation"][
                "production_outcome_credit"
            ]
        )

    def test_refresh_projection_keeps_child_consumer_output_out_of_periodic_journal(self):
        payload = {
            "updated": "2026-07-27T14:00:00+00:00",
            "total": 1,
            "ok_count": 1,
            "results": [{"egress": "vless", "ok": False, "status": "FAIL", "output_tail": "x" * 100000}],
            "bounded_delegated_service_failure_action": {
                "status": "ACTION_COMPLETED",
                "ok": True,
                "users_moved": 1,
                "consumer_result": {"packet_id": "pkt_test", "nested": "x" * 100000},
            },
            "availability_first_standing_policy_action": {
                "status": "STOP_SAFE",
                "ok": True,
                "stage": 1,
                "diagnostic_status": "MEASURED_STOP",
                "consumer_result": {
                    "final_verdict": "AVAILABILITY_FIRST_STANDING_STAGE_STOPPED",
                    "transaction_status": "STOP_SAFE",
                    "circuit_breaker": {
                        "tripped": True,
                        "remaining_subsets_stopped": True,
                        "reason": "fresh_capacity_gate_failed",
                        "nested": "x" * 100000,
                    },
                    "packet_set": [{
                        "final_verdict": "STOP_SAFE",
                        "stop_reason": "fresh_capacity_gate_failed",
                        "target_id": "awg3",
                        "users_moved": 0,
                        "nested": "x" * 100000,
                    }],
                    "nested": "x" * 100000,
                },
            },
        }
        projection = self.refresh.compact_refresh_projection(payload)
        serialized = json.dumps(projection)
        self.assertLess(len(serialized), 5000)
        self.assertEqual(projection["bounded_delegated_service_failure_action"]["consumer_result"]["packet_id"], "pkt_test")
        self.assertEqual(
            projection["availability_first_standing_policy_action"]["stage"],
            1,
        )
        self.assertEqual(
            projection["availability_first_standing_policy_action"][
                "diagnostic_status"
            ],
            "MEASURED_STOP",
        )
        availability_terminal = projection[
            "availability_first_standing_policy_action"
        ]["consumer_result"]
        self.assertEqual(
            availability_terminal["circuit_breaker"]["reason"],
            "fresh_capacity_gate_failed",
        )
        self.assertEqual(
            availability_terminal["packet_set"][0]["target_id"],
            "awg3",
        )
        self.assertEqual(
            availability_terminal["packet_set"][0]["users_moved"],
            0,
        )
        self.assertNotIn("nested", serialized)
        self.assertTrue(projection["candidate_or_execution_forbidden"])

    def test_compact_matrix_receipt_retains_nested_outcome_pointer_without_payload(self):
        projection = self.refresh.compact_refresh_projection({
            "bounded_delegated_service_failure_action": {
                "status": "ACTION_COMPLETED", "ok": True,
                "consumer_result": {
                    "final_verdict": "GOVERNED_TRANSACTION_COMPLETED",
                    "feedback_materialization": {
                        "feedback_id": "execfb_unit", "learning_record_id": "learn_unit",
                        "nested": "x" * 100000,
                    },
                },
            },
        })
        receipt = projection["bounded_delegated_service_failure_action"]["consumer_result"]
        self.assertEqual(receipt["feedback_id"], "execfb_unit")
        self.assertEqual(receipt["learning_record_id"], "learn_unit")
        self.assertNotIn("nested", json.dumps(projection))

    def test_topology_standing_consumer_routes_exact_manifest_to_existing_executor(self):
        diagnostic = {
            "status": "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
            "production_preflight": {
                "manifest": {
                    "manifest_hash": "a" * 64,
                    "trial_identity": "10.7.0.100",
                    "trial_identity_count": 1,
                    "existing_source": "1",
                    "selected_source_or_draft": "vless",
                    "expected_ordinary_assignment_delta": "NONE",
                    "expected_ordinary_route_delta": "NONE",
                },
            },
            "standing_policy_admission": {
                "status": (
                    "AUTO_ADMITTED_BY_STANDING_DELEGATED_"
                    "CONTROLLED_TOPOLOGY_POLICY"
                ),
                "ok": True,
                "contract_id": "sdpc_exact",
                "contract_hash": "b" * 64,
            },
        }
        executed = {
            "controlled_topology_final_verdict": (
                "ONE_IDENTITY_AUTONOMOUS_CONTROLLED_TOPOLOGY_TRIAL_PROVEN"
            ),
            "users_moved": 1,
            "runtime_mutation_performed": True,
            "fresh_packet_id": "pkt_exact",
        }
        calls = [
            mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
            mock.Mock(returncode=0, stdout=json.dumps(executed)),
        ]
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=calls,
        ) as run:
            result = (
                self.refresh.run_controlled_topology_standing_policy_action(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/state"),
                    event_dir=Path("/events"),
                    policy_file=Path("/policy"),
                    audit_store=Path("/audit"),
                )
            )
        self.assertEqual(result["status"], "ACTION_COMPLETED")
        self.assertTrue(result["action_completed"])
        self.assertEqual(result["users_moved"], 1)
        command = run.call_args_list[1].args[0]
        self.assertIn(
            "--execute-controlled-topology-standing-transaction",
            command,
        )
        self.assertEqual(
            command[
                command.index("--expected-controlled-topology-manifest-hash")
                + 1
            ],
            "a" * 64,
        )
        self.assertEqual(
            command[command.index("--controlled-topology-user") + 1],
            "10.7.0.100",
        )

    def test_topology_standing_consumer_does_not_execute_without_admission(self):
        diagnostic = {
            "status": "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
            "production_preflight": {"manifest": {}},
            "standing_policy_admission": {
                "status": "ENGINEERING_AUTHORITY_REQUIRED",
                "ok": False,
                "blockers": ["standing_policy_missing"],
            },
        }
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            return_value=mock.Mock(
                returncode=0,
                stdout=json.dumps(diagnostic),
            ),
        ) as run:
            result = (
                self.refresh.run_controlled_topology_standing_policy_action(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/state"),
                    event_dir=Path("/events"),
                    policy_file=Path("/policy"),
                    audit_store=Path("/audit"),
                )
            )
        self.assertEqual(result["status"], "NOT_REQUIRED_OR_NOT_ADMITTED")
        self.assertFalse(result["action_attempted"])
        self.assertEqual(run.call_count, 1)

    def test_topology_standing_consumer_preserves_exact_stop_reason(self):
        diagnostic = {
            "status": "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
            "production_preflight": {
                "manifest": {
                    "manifest_hash": "a" * 64,
                    "trial_identity": "10.7.0.100",
                    "trial_identity_count": 1,
                    "existing_source": "1",
                    "selected_source_or_draft": "vless",
                    "expected_ordinary_assignment_delta": "NONE",
                    "expected_ordinary_route_delta": "NONE",
                },
            },
            "standing_policy_admission": {
                "status": (
                    "AUTO_ADMITTED_BY_STANDING_DELEGATED_"
                    "CONTROLLED_TOPOLOGY_POLICY"
                ),
                "ok": True,
                "contract_id": "sdpc_exact",
                "contract_hash": "b" * 64,
            },
        }
        stopped = {
            "final_verdict": "STOP_SAFE",
            "stop_reason": "packet_materialization_failed",
            "reservation_mutation_performed": True,
            "reservation_released_after_stop": True,
            "users_moved": 0,
            "runtime_mutation_performed": False,
        }
        with mock.patch.object(
            self.refresh.subprocess,
            "run",
            side_effect=[
                mock.Mock(returncode=0, stdout=json.dumps(diagnostic)),
                mock.Mock(returncode=2, stdout=json.dumps(stopped)),
            ],
        ):
            result = (
                self.refresh.run_controlled_topology_standing_policy_action(
                    "v7-users-autoswitch",
                    "v7-governed-canary-dry-run-cycle",
                    state_dir=Path("/state"),
                    event_dir=Path("/events"),
                    policy_file=Path("/policy"),
                    audit_store=Path("/audit"),
                )
            )
        self.assertEqual(result["status"], "STOP_SAFE")
        self.assertEqual(
            result["stop_reason"],
            "packet_materialization_failed",
        )
        self.assertTrue(result["reservation_mutation_performed"])
        self.assertTrue(result["reservation_released_after_stop"])


if __name__ == "__main__":
    unittest.main()
