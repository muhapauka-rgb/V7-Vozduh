import importlib.machinery
import importlib.util
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-client-speed-api"
LOADER = importlib.machinery.SourceFileLoader("v7_client_speed_api", str(TOOL))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
client_speed = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(client_speed)


class ExactClientProbeOwnerTest(unittest.TestCase):
    def context(self):
        first = 1_000_000_000
        context = {
            "schema_version": client_speed.EXACT_PROBE_CONTEXT_SCHEMA,
            "contract_id": "ctprobe_contract_unit",
            "validation_generation_id": "ctprobe_generation_unit",
            "sample_kind": "cold",
            "issuing_owner": "existing-controlled-production-owner",
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "incident_id": "sfinc_unit",
            "incident_generation": "gen_unit",
            "user": "10.7.0.3",
            "source": "vless",
            "target": "awg3",
            "certification_identity": True,
            "network_namespace_inode": 4242,
            "source_address": "10.7.0.3",
            "interface": "awg-client0",
            "fwmark": 1003,
            "routing_table": "1003",
            "expected_egress_ip": "8.8.8.8",
            "expected_target_egress_fingerprint": "a" * 64,
            "target_url": "https://probe.example/ip",
            "clock_domain_id": "linux-boot:unit:netns:4242",
            "clock_uncertainty_ms": 0.1,
            "first_failed_observation_monotonic_ns": first,
            "confirmed_hard_failure_monotonic_ns": first + 200_000_000,
            "timeout_ms": 1000,
            "retry_count": 1,
            "observation_cadence_ms": 100,
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat(),
        }
        context["context_hash"] = client_speed.exact_probe_context_hash(context)
        return context

    def successful_attempt(self):
        return {
            "attempt": 1,
            "finished_monotonic_ns": 1_900_000_000,
            "route": {
                "ok": True,
                "dev": "awg-client0",
                "table": "1003",
                "prefsrc": "10.7.0.3",
            },
            "fresh_dns_resolution": True,
            "fresh_socket": True,
            "source_bind_applied": True,
            "interface_bind_applied": True,
            "so_mark_applied": True,
            "payload_response_verified": True,
            "response_matches_expected_egress_ip": True,
            "payload_fingerprint": "payload_fp_unit",
        }

    def test_matching_namespace_route_and_payload_produce_ready_receipt(self):
        context = self.context()
        attempt = self.successful_attempt()
        with mock.patch.object(client_speed, "current_netns_inode", return_value=4242), mock.patch.object(
            client_speed,
            "current_clock_domain_id",
            return_value="linux-boot:unit:netns:4242",
        ):
            receipt = client_speed.build_exact_probe_receipt(context, attempt, [attempt])

        self.assertEqual(
            receipt["status"],
            "EXACT_CLIENT_NETWORK_CONTEXT_TRAFFIC_PROBE_RECEIPT_READY",
        )
        self.assertTrue(receipt["exact_certification_identity_context"])
        self.assertTrue(receipt["routing_table_or_fwmark_bound"])
        self.assertEqual(receipt["observed_target_egress_fingerprint"], "a" * 64)
        self.assertFalse(receipt["management_default_route_used"])
        self.assertEqual(receipt["user_movement"], 0)
        consumed = client_speed.consume_exact_probe_receipt(receipt, context)
        self.assertEqual(
            consumed["status"],
            "EXACT_CLIENT_PROBE_AND_RECOVERY_CLOCK_CONSUMED",
        )
        self.assertTrue(consumed["ok"])

    def test_management_namespace_or_route_mismatch_fails_closed(self):
        context = self.context()
        attempt = self.successful_attempt()
        attempt["route"] = {"ok": True, "dev": "eth0", "table": "main", "prefsrc": "192.0.2.2"}
        with mock.patch.object(client_speed, "current_netns_inode", return_value=1), mock.patch.object(
            client_speed,
            "current_clock_domain_id",
            return_value="linux-boot:unit:netns:1",
        ):
            receipt = client_speed.build_exact_probe_receipt(context, attempt, [attempt])

        self.assertEqual(receipt["status"], "PROBE_INVALID")
        self.assertTrue(receipt["management_default_route_used"])
        self.assertIn("exact_certification_identity_context_not_proven", receipt["blockers"])
        self.assertIn("routing_table_or_fwmark_binding_not_proven", receipt["blockers"])

    def test_validation_generation_has_deterministic_duplicate_identity(self):
        context = self.context()
        first_attempt = self.successful_attempt()
        later_attempt = dict(first_attempt)
        later_attempt["finished_monotonic_ns"] += 500_000_000
        with mock.patch.object(client_speed, "current_netns_inode", return_value=4242), mock.patch.object(
            client_speed,
            "current_clock_domain_id",
            return_value="linux-boot:unit:netns:4242",
        ):
            first = client_speed.build_exact_probe_receipt(context, first_attempt, [first_attempt])
            duplicate = client_speed.build_exact_probe_receipt(context, later_attempt, [later_attempt])
        self.assertEqual(first["receipt_id"], duplicate["receipt_id"])

    def test_expired_or_unbound_context_never_opens_network(self):
        context = self.context()
        context["expires_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
        context.pop("incident_generation")
        errors = client_speed.exact_probe_context_errors(context)
        self.assertIn("context_expired", errors)
        self.assertIn("incident_generation_missing", errors)

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "context.json"
            path.write_text(json.dumps(context), encoding="utf-8")
            with mock.patch.object(client_speed, "execute_fresh_exact_probe_request") as execute:
                receipt = client_speed.run_exact_probe_context(path)
            execute.assert_not_called()
        self.assertEqual(receipt["status"], "PROBE_INVALID")

    def test_cli_propagates_fail_closed_exit_code(self):
        proc = subprocess.run(
            [str(TOOL), "--exact-client-probe-context", "/definitely/missing/context.json", "--json"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=5,
        )
        result = json.loads(proc.stdout)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(result["status"], "PROBE_INVALID")
        self.assertFalse(result["runtime_mutation_performed"])

    def test_readiness_reuses_online_certification_agent_without_disclosing_identity(self):
        now = int(client_speed.time.time())
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            users = root / "users.registry"
            egress = root / "egress.registry"
            agents = root / "client-agents.json"
            users.write_text(
                "ip=10.7.0.16 current=awg3 table=1014 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            egress.write_text(
                "id=awg3 enabled=1 interface=awg3 expected_ip=194.124.210.244\n",
                encoding="utf-8",
            )
            agents.write_text(json.dumps({"agents": {"10.7.0.16": {
                "last_seen": "2026-08-05T00:00:00+00:00",
                "online_until": now + 30,
            }}}), encoding="utf-8")
            with mock.patch.object(client_speed, "USERS_REG", users), mock.patch.object(
                client_speed, "EGRESS_REG", egress
            ), mock.patch.object(client_speed, "AGENTS", agents):
                result = client_speed.exact_client_probe_readiness()
        self.assertTrue(result["ok"])
        self.assertEqual(result["eligible_context_count"], 1)
        self.assertNotIn("10.7.0.16", json.dumps(result))
        self.assertFalse(result["command_enqueued"])
        self.assertFalse(result["network_probe_executed"])

    def test_readiness_names_exact_missing_agent_without_effects(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            users = root / "users.registry"
            egress = root / "egress.registry"
            agents = root / "client-agents.json"
            users.write_text(
                "ip=10.7.0.16 current=awg3 table=1014 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            egress.write_text(
                "id=awg3 enabled=1 interface=awg3 expected_ip=194.124.210.244\n",
                encoding="utf-8",
            )
            agents.write_text(json.dumps({"agents": {}}), encoding="utf-8")
            with mock.patch.object(client_speed, "USERS_REG", users), mock.patch.object(
                client_speed, "EGRESS_REG", egress
            ), mock.patch.object(client_speed, "AGENTS", agents):
                result = client_speed.exact_client_probe_readiness()
        self.assertFalse(result["ok"])
        self.assertIn("online_exact_certification_client_agent_missing", result["blockers"])
        self.assertEqual(result["user_movement"], 0)


if __name__ == "__main__":
    unittest.main()
