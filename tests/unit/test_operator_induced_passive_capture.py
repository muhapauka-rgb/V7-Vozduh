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
    def test_in_process_autoswitch_args_avoid_full_cli_parser(self):
        module = mock.Mock()
        module.DEFAULT_ORG_POLICY_FILE = Path("/etc/v7/org-egress-policy.json")
        module.DEFAULT_SAFETY_FILE = Path("/opt/v7/egress/state/autoswitch-safety.json")
        module.build_arg_parser.side_effect = AssertionError(
            "full CLI parser must stay off the Matrix hot path"
        )

        args = tool.in_process_autoswitch_args(
            module,
            state_dir=Path("/opt/v7/egress/state"),
            event_dir=Path("/opt/v7/events"),
            policy_file=Path("/etc/v7/policy.json"),
            audit_store=Path("/opt/v7/audit/operator-execution-audit.jsonl"),
        )

        self.assertEqual(args.state_dir, "/opt/v7/egress/state")
        self.assertEqual(args.controlled_source_validation_profile, "campaign")
        module.build_arg_parser.assert_not_called()

    def test_passive_capture_dedup_reads_only_bounded_ledger_tail(self):
        path = Path("/events/service-failure-events.jsonl")
        with mock.patch.object(
            tool.intelligence_workers,
            "read_jsonl_tail",
            return_value=[
                {"event_id": "older-in-window"},
                {"event_id": "latest"},
                {"unrelated": True},
            ],
        ) as tail_reader:
            result = tool.recent_passive_capture_event_ids(path)

        self.assertEqual(result, {"older-in-window", "latest"})
        tail_reader.assert_called_once_with(
            path,
            limit=tool.PASSIVE_CAPTURE_DEDUP_ROW_LIMIT,
            max_bytes=tool.PASSIVE_CAPTURE_DEDUP_BYTE_LIMIT,
        )

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

    def test_exact_service_subset_is_forwarded_to_existing_checker(self):
        with mock.patch.object(
            tool.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(
                ["checker"], 0, stdout=json.dumps({"status": "OK"}),
            ),
        ) as run:
            result = tool.run_one(
                "source", 3, "checker", Path("/state"), "google,telegram",
            )
        self.assertTrue(result["ok"])
        self.assertEqual(
            run.call_args.args[0][-2:], ["--services", "google,telegram"],
        )

    def test_exact_egress_subset_reuses_enabled_registry_and_fails_closed(self):
        rows = [
            {"id": "hot", "enabled": "1"},
            {"id": "cold", "enabled": "1"},
            {"id": "off", "enabled": "0"},
        ]
        selected, requested = tool.select_probe_rows(rows, "hot")
        self.assertEqual([row["id"] for row in selected], ["hot"])
        self.assertEqual(requested, ["hot"])
        with self.assertRaisesRegex(ValueError, "exact_egress_subset_not_enabled:off"):
            tool.select_probe_rows(rows, "off")
        with self.assertRaisesRegex(ValueError, "invalid_exact_egress_subset"):
            tool.select_probe_rows(rows, "bad/egress")

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
            "scope_classification": "LEGACY_UNPARTITIONED",
            "controlled_certification_scope_count": 0,
        }])

    def test_certification_only_failed_scope_is_reconciled_but_not_actionable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.2 current=failed enabled=true certification_user=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "failed": {"services": {"telegram": {
                    "ok": False, "failure_state": "OBSERVED_CONTINUING",
                }}},
            }}), encoding="utf-8")
            (events / "service-failure-events.jsonl").write_text(json.dumps({
                "event_id": "certification-only", "event_type": "SERVICE_FAILURE_OBSERVED",
                "channel": "failed", "source_incident_id": "incident-certification-only",
                "source_scope": {
                    "affected_scope_count": 0,
                    "affected_scope_fingerprint": "ordinary-empty",
                    "scope_classification": "CERTIFICATION_ONLY",
                    "ordinary_production_scope": {
                        "affected_scope_count": 0,
                        "affected_scope_fingerprint": "ordinary-empty",
                    },
                    "controlled_certification_scope": {
                        "affected_scope_count": 1,
                        "affected_scope_fingerprint": "certification-one",
                    },
                },
            }) + "\n", encoding="utf-8")
            result = tool.current_failed_source_scope(events, state)

        self.assertFalse(result["active"])
        self.assertTrue(result["requires_scope_reconciliation"])
        self.assertEqual(result["decision"], "RECONCILE_CONTROLLED_CERTIFICATION_SCOPE_ONLY")
        self.assertEqual(result["certification_only_active_sources"][0]["controlled_certification_scope_count"], 1)
        self.assertEqual(
            result["certification_only_active_sources"][0]["binding_event"]["event_id"],
            "certification-only",
        )

    def test_current_scope_excludes_historical_incidents_on_same_failed_channel(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.2 current=failed enabled=true certification_user=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "failed": {"services": {"telegram": {
                    "ok": False,
                    "failure_state": "OBSERVED_CONTINUING",
                    "source_incident_id": "incident-current",
                }}},
            }}), encoding="utf-8")
            rows = [
                {
                    "event_id": "historical",
                    "event_type": "SERVICE_FAILURE_OBSERVED",
                    "channel": "failed",
                    "source_incident_id": "incident-old",
                },
                {
                    "event_id": "current",
                    "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "channel": "failed",
                    "source_incident_id": "incident-current",
                },
            ]
            (events / "service-failure-events.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8",
            )
            result = tool.current_failed_source_scope(events, state)

        self.assertEqual(result["latest_source_count"], 1)
        self.assertEqual(
            [row["event_id"] for row in result["certification_only_active_sources"]],
            ["current"],
        )

    def test_multiple_failed_sources_selects_only_current_profile_impact(self):
        """An unrelated failed source must not force an all-user advisory run."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.127 current=vless enabled=true\n"
                "ip=10.7.0.5 current=awg0 enabled=true\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {
                    "10.7.0.127": {"services": ["google", "telegram"]},
                    "10.7.0.5": {"services": ["youtube"]},
                },
            }), encoding="utf-8")
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "vless": {"services": {
                    "google": {
                        "ok": False, "status": "FAIL",
                        "failure_state": "OBSERVED_CONTINUING",
                        "confirmed_hard_failure_monotonic_ns": 200,
                    },
                }},
                "awg0": {"services": {
                    "telegram": {
                        "ok": False, "status": "FAIL",
                        "failure_state": "OBSERVED_CONTINUING",
                        "confirmed_hard_failure_monotonic_ns": 100,
                    },
                }},
            }}), encoding="utf-8")
            source = tool.automatically_prioritized_failed_source(
                state_dir=state,
                active_sources=[
                    {"channel": "awg0", "source_incident_id": "old"},
                    {"channel": "vless", "source_incident_id": "new"},
                ],
            )

        self.assertEqual(source["channel"], "vless")
        self.assertEqual(source["profile_affected_count"], 1)
        self.assertEqual(source["profile_failure_monotonic_ns"], 200)
        self.assertEqual(
            source["source_selection"],
            "CURRENT_MATRIX_PROFILE_REQUIRED_SERVICE_IMPACT",
        )

    def test_direct_handoff_uses_matrix_profile_selected_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "users.registry").write_text(
                "ip=10.7.0.127 current=vless enabled=true\n"
                "ip=10.7.0.5 current=awg0 enabled=true\n",
                encoding="utf-8",
            )
            (state / "service-preferences.json").write_text(json.dumps({
                "users": {"10.7.0.127": {"services": ["google"]}},
            }), encoding="utf-8")
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "vless": {"services": {"google": {
                    "ok": False, "failure_state": "OBSERVED_NEW",
                    "confirmed_hard_failure_monotonic_ns": 20,
                }}},
                "awg0": {"services": {"telegram": {
                    "ok": False, "failure_state": "OBSERVED_NEW",
                    "confirmed_hard_failure_monotonic_ns": 10,
                }}},
            }}), encoding="utf-8")
            with mock.patch.object(
                tool, "service_failure_direct_execution_handoff",
                return_value={"final_verdict": "NOT_READY"},
            ) as handoff:
                tool.direct_service_failure_handoff_for_scope(
                    state_dir=state,
                    source_scope={"active_sources": [
                        {"channel": "awg0", "source_incident_id": "old", "source_scope_fingerprint": "a"},
                        {"channel": "vless", "source_incident_id": "new", "source_scope_fingerprint": "v"},
                    ]},
                )

        self.assertEqual(handoff.call_args.kwargs["source_incident_id"], "new")
        self.assertEqual(handoff.call_args.kwargs["source_scope_fingerprint"], "v")

    def test_current_scope_does_not_fallback_to_history_after_exact_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.2 current=source enabled=true certification_user=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "source": {"services": {"telegram": {
                    "ok": True,
                    "failure_state": "HEALTHY",
                    "source_incident_id": "incident-recovered",
                }}},
            }}), encoding="utf-8")
            (events / "service-failure-events.jsonl").write_text(json.dumps({
                "event_id": "historical",
                "event_type": "SERVICE_FAILURE_OBSERVED",
                "channel": "source",
                "source_incident_id": "incident-old",
            }) + "\n", encoding="utf-8")
            result = tool.current_failed_source_scope(events, state)

        self.assertFalse(result["active"])
        self.assertEqual(result["certification_only_active_sources"], [])
        self.assertEqual(result["latest_source_count"], 0)

    def test_definitive_local_recovery_supersedes_older_interface_failure_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.2 current=source enabled=true certification_user=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "source": {"services": {
                    "telegram": {
                        "ok": False,
                        "failure_state": "OBSERVED_NEW",
                        "failure_family": "RUNTIME_INTERFACE_UNAVAILABLE",
                        "observed_at": "2026-08-23T15:46:37+00:00",
                        "source_incident_id": "incident-old",
                    },
                    "__channel_liveness__": {
                        "ok": True,
                        "failure_state": "RECOVERY_OBSERVED",
                        "failure_family": "NONE",
                        "evidence_class": "DEFINITIVE_LOCAL_RECOVERY",
                        "observed_at": "2026-08-23T15:58:12+00:00",
                        "source_incident_id": "incident-old",
                    },
                }},
            }}), encoding="utf-8")
            (events / "service-failure-events.jsonl").write_text(json.dumps({
                "event_id": "historical-interface-failure",
                "event_type": "SERVICE_FAILURE_OBSERVED",
                "channel": "source",
                "source_incident_id": "incident-old",
            }) + "\n", encoding="utf-8")
            result = tool.current_failed_source_scope(events, state)

        self.assertFalse(result["active"])
        self.assertEqual(result["certification_only_active_sources"], [])
        self.assertEqual(result["latest_source_count"], 0)

    def test_failure_observed_after_local_recovery_remains_actionable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            events = root / "events"
            state.mkdir()
            events.mkdir()
            (state / "users.registry").write_text(
                "ip=10.7.0.2 current=source enabled=true certification_user=1\n",
                encoding="utf-8",
            )
            (state / "service-matrix.json").write_text(json.dumps({"items": {
                "source": {"services": {
                    "telegram": {
                        "ok": False,
                        "failure_state": "OBSERVED_NEW",
                        "failure_family": "RUNTIME_INTERFACE_UNAVAILABLE",
                        "observed_at": "2026-08-23T16:00:00+00:00",
                        "source_incident_id": "incident-new",
                    },
                    "__channel_liveness__": {
                        "ok": True,
                        "failure_state": "RECOVERY_OBSERVED",
                        "evidence_class": "DEFINITIVE_LOCAL_RECOVERY",
                        "observed_at": "2026-08-23T15:58:12+00:00",
                    },
                }},
            }}), encoding="utf-8")
            (events / "service-failure-events.jsonl").write_text(json.dumps({
                "event_id": "new-failure",
                "event_type": "SERVICE_FAILURE_OBSERVED",
                "channel": "source",
                "source_incident_id": "incident-new",
            }) + "\n", encoding="utf-8")
            result = tool.current_failed_source_scope(events, state)

        self.assertTrue(result["requires_scope_reconciliation"])
        self.assertEqual(
            result["certification_only_active_sources"][0]["event_id"],
            "new-failure",
        )


if __name__ == "__main__":
    unittest.main()
