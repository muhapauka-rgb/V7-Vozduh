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

            policy_file.write_text(
                json.dumps({"delegated_autonomy_policy": {"status": "ACTIVE"}}),
                encoding="utf-8",
            )
            executor = root / "executor"
            executor.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'final_verdict':'STOP_SAFE','users_moved':0,'apply_executed':False}))\n"
                "raise SystemExit(2)\n",
                encoding="utf-8",
            )
            executor.chmod(0o755)
            stop = self.refresh.run_bounded_delegated_service_failure_action(
                str(executor),
                state_dir=state_dir,
                event_dir=event_dir,
                policy_file=policy_file,
            )
            self.assertTrue(stop["ok"])
            self.assertEqual(stop["status"], "STOP_SAFE")
            self.assertTrue(stop["action_attempted"])
            self.assertEqual(stop["users_moved"], 0)

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
            )
            self.assertTrue(governed_stop["ok"])
            self.assertEqual(governed_stop["status"], "STOP_SAFE")
            self.assertFalse(governed_stop["runtime_mutation_performed"])

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
        }
        projection = self.refresh.compact_refresh_projection(payload)
        serialized = json.dumps(projection)
        self.assertLess(len(serialized), 5000)
        self.assertEqual(projection["bounded_delegated_service_failure_action"]["consumer_result"]["packet_id"], "pkt_test")
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


if __name__ == "__main__":
    unittest.main()
