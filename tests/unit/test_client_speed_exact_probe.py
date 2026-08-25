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
    def test_namespace_http_probe_uses_framed_response_completion(self):
        script = client_speed._exact_namespace_http_script()
        compile(script, "<exact-namespace-http>", "exec")
        self.assertIn("http.client.HTTPResponse", script)
        self.assertIn("STUN_XOR_MAPPED_ADDRESS", script)
        self.assertIn("stun_mapped_address_missing", script)
        self.assertNotIn("while total<65536", script)

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
            "source_identity_freebind_applied": True,
            "interface_bind_applied": True,
            "so_mark_applied": True,
            "payload_response_verified": True,
            "response_matches_expected_egress_ip": True,
            "payload_fingerprint": "payload_fp_unit",
        }

    def target_payload_context(self):
        context = {
            "schema_version": client_speed.TARGET_EGRESS_PAYLOAD_CONTEXT_SCHEMA,
            "contract_id": "cttarget_contract_unit",
            "validation_generation_id": "cttarget_generation_unit",
            "sample_kind": "warm",
            "issuing_owner": "existing-controlled-production-owner",
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "incident_id": "sfinc_unit",
            "incident_generation": "gen_unit",
            "user": "10.7.0.3",
            "source": "vless",
            "target": "awg3",
            "candidate_id": "candidate_unit",
            "packet_id": "packet_unit",
            "lease_id": "lease_unit",
            "operation_id": "operation_unit",
            "certification_identity": True,
            "source_address": "10.8.0.2",
            "interface": "awg3",
            "expected_egress_ip": "8.8.8.8",
            "expected_target_egress_fingerprint": "b" * 64,
            "target_url": "https://probe.example/ip",
            "timeout_ms": 1000,
            "retry_count": 1,
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat(),
        }
        context["context_hash"] = client_speed.exact_probe_context_hash(context)
        return context

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
        self.assertTrue(receipt["exact_user_source_fwmark_table_traversed"])
        self.assertEqual(receipt["scope"], "EXACT_CLIENT_NETWORK_CONTEXT")
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

    def test_existing_client_tunnel_and_host_policy_route_produce_ready_receipt(self):
        context = self.context()
        context["probe_transport"] = "EXISTING_LOCAL_CLIENT_PROFILE_NAMESPACE"
        attempt = self.successful_attempt()
        attempt.update({
            "source_identity_freebind_applied": False,
            "so_mark_applied": False,
            "host_policy_route_proven": True,
            "client_tunnel_ingress_proven": True,
            "client_profile_peer_mapping_proven": True,
            "client_namespace_isolated": True,
            "client_network_namespace_inode": 5252,
            "fresh_dns_resolution": False,
            "dns_mode": "DECLARED_NO_DNS",
        })
        with mock.patch.object(
            client_speed, "current_netns_inode", return_value=4242
        ), mock.patch.object(
            client_speed,
            "current_clock_domain_id",
            return_value="linux-boot:unit:netns:4242",
        ):
            receipt = client_speed.build_exact_probe_receipt(
                context, attempt, [attempt]
            )
        self.assertEqual(
            receipt["status"],
            "EXACT_CLIENT_NETWORK_CONTEXT_TRAFFIC_PROBE_RECEIPT_READY",
        )
        self.assertTrue(receipt["client_tunnel_ingress_proven"])
        self.assertTrue(receipt["exact_user_source_fwmark_table_traversed"])
        self.assertEqual(receipt["dns_mode"], "DECLARED_NO_DNS")
        consumed = client_speed.consume_exact_probe_receipt(receipt, context)
        self.assertTrue(consumed["ok"])

    def test_exact_namespace_prefers_stun_and_keeps_https_fallback(self):
        context = self.context()
        context.update({
            "probe_transport": "EXISTING_LOCAL_CLIENT_PROFILE_NAMESPACE",
            "preferred_probe_protocol": "STUN_XOR_MAPPED_ADDRESS",
            "stun_host": "stun.cloudflare.com",
            "stun_port": 3478,
            "protocol_fallback_allowed": True,
        })
        stun_attempt = {
            "payload_response_verified": True,
            "response_matches_expected_egress_ip": True,
            "probe_protocol": "STUN_XOR_MAPPED_ADDRESS",
        }
        with mock.patch.object(
            client_speed.socket,
            "getaddrinfo",
            return_value=[(
                client_speed.socket.AF_INET,
                client_speed.socket.SOCK_DGRAM,
                17,
                "",
                ("162.159.207.0", 3478),
            )],
        ), mock.patch.object(
            client_speed,
            "execute_ephemeral_client_namespace_probe",
            return_value=(stun_attempt, [stun_attempt]),
        ) as execute:
            successful, attempts = (
                client_speed.execute_fresh_exact_probe_request(context)
            )
        self.assertIs(successful, stun_attempt)
        self.assertEqual(attempts, [stun_attempt])
        called_context = execute.call_args.args[0]
        self.assertEqual(
            called_context["preferred_probe_protocol"],
            "STUN_XOR_MAPPED_ADDRESS",
        )
        self.assertEqual(called_context["destination_port"], 3478)

    def test_invalid_stun_context_fails_closed(self):
        context = self.context()
        context.update({
            "preferred_probe_protocol": "STUN_XOR_MAPPED_ADDRESS",
            "stun_host": "",
            "stun_port": 80,
        })
        context["context_hash"] = client_speed.exact_probe_context_hash(context)
        errors = client_speed.exact_probe_context_errors(context)
        self.assertIn("stun_host_missing", errors)
        self.assertIn("stun_port_invalid", errors)

    def test_profile_lookup_is_exact_and_wg_quick_fields_are_not_forwarded(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            profile = root / "client" / "client.conf"
            profile.parent.mkdir()
            profile.write_text(
                "[Interface]\nPrivateKey = private\nAddress = 10.7.0.3/32\nDNS = 10.0.0.1\n"
                "[Peer]\nPublicKey = public\nAllowedIPs = 0.0.0.0/0\nEndpoint = 192.0.2.1:51820\n",
                encoding="utf-8",
            )
            with mock.patch.object(client_speed, "CLIENT_PROFILE_ROOT", root):
                self.assertEqual(
                    client_speed.exact_certification_client_profile("10.7.0.3"),
                    profile,
                )
            stripped = client_speed.wireguard_setconf_text(profile.read_text())
            local_endpoint = client_speed.wireguard_setconf_text(
                profile.read_text(), endpoint_override="169.254.253.1:51820"
            )
            local_ingress = client_speed.wireguard_setconf_text(
                profile.read_text(), peer_public_key_override="current-ingress-key"
            )
            metadata = client_speed.wireguard_profile_metadata(profile.read_text())
        self.assertIn("PrivateKey = private", stripped)
        self.assertIn("AllowedIPs = 0.0.0.0/0", stripped)
        self.assertNotIn("Address =", stripped)
        self.assertNotIn("DNS =", stripped)
        self.assertIn("Endpoint = 169.254.253.1:51820", local_endpoint)
        self.assertIn("PublicKey = current-ingress-key", local_ingress)
        self.assertNotIn("PublicKey = public", local_ingress)
        self.assertEqual(metadata["endpoint_port"], "51820")

    def test_declared_identity_must_equal_bound_source_address(self):
        context = self.context()
        context["source_address"] = "10.7.0.99"
        attempt = self.successful_attempt()
        attempt["route"]["prefsrc"] = "10.7.0.99"
        with mock.patch.object(
            client_speed, "current_netns_inode", return_value=4242
        ), mock.patch.object(
            client_speed,
            "current_clock_domain_id",
            return_value="linux-boot:unit:netns:4242",
        ):
            receipt = client_speed.build_exact_probe_receipt(
                context, attempt, [attempt]
            )
        self.assertEqual(receipt["status"], "PROBE_INVALID")
        self.assertIn(
            "exact_certification_identity_context_not_proven",
            receipt["blockers"],
        )

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
                "capabilities": ["exact_client_network_context_traffic_probe_v1"],
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
        self.assertIn("exact_certification_client_execution_context_missing", result["blockers"])
        self.assertEqual(result["user_movement"], 0)

    def test_readiness_reuses_existing_local_polygon_profile_without_agent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            users = root / "users.registry"
            egress = root / "egress.registry"
            agents = root / "client-agents.json"
            profiles = root / "clients"
            profile = profiles / "cert" / "cert.conf"
            profile.parent.mkdir(parents=True)
            profile.write_text(
                "[Interface]\nPrivateKey = private\nAddress = 10.7.0.16/32\n"
                "[Peer]\nPublicKey = public\nAllowedIPs = 0.0.0.0/0\nEndpoint = 192.0.2.1:51820\n",
                encoding="utf-8",
            )
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
            ), mock.patch.object(client_speed, "AGENTS", agents), mock.patch.object(
                client_speed, "CLIENT_PROFILE_ROOT", profiles
            ), mock.patch.object(client_speed.os, "geteuid", return_value=0):
                result = client_speed.exact_client_probe_readiness()
        self.assertTrue(result["ok"])
        self.assertEqual(
            result["selected_context"]["execution_mode"],
            "EXISTING_LOCAL_CLIENT_PROFILE_NAMESPACE",
        )
        self.assertNotIn("10.7.0.16", json.dumps(result))

    def test_prepared_polygon_session_is_deterministic_and_runtime_only(self):
        self.assertEqual(
            client_speed.EXACT_PROBE_TUNNEL_KEEPALIVE_ADDRESS,
            "10.0.0.1",
        )
        first = client_speed.exact_probe_session_names("10.7.0.16")
        second = client_speed.exact_probe_session_names("10.7.0.16")
        other = client_speed.exact_probe_session_names("10.7.0.17")
        self.assertEqual(first, second)
        self.assertNotEqual(first, other)
        self.assertTrue(all(len(value) <= 15 for value in first.values()))
        prepared = {
            "status": "EXACT_CLIENT_PROBE_SESSION_PREPARED",
            "duration_ms": 12.5,
            "prepared_session_reused": True,
            "client_tunnel_ingress_proven": True,
        }
        with mock.patch.object(
            client_speed,
            "execute_ephemeral_client_namespace_probe",
            return_value=(prepared, [prepared]),
        ) as execute:
            result = client_speed.prepare_exact_client_probe_session(
                "10.7.0.16"
            )
        self.assertTrue(result["ok"])
        self.assertTrue(result["prepared_session_reused"])
        self.assertEqual(
            result["persistent_state_kind"],
            "RUNTIME_ONLY_POLYGON_CLIENT_NAMESPACE",
        )
        self.assertFalse(result["canonical_state_created"])
        self.assertFalse(result["routing_mutation_performed"])
        context = execute.call_args.args[0]
        self.assertTrue(context["reuse_prepared_client_session"])
        self.assertTrue(context["prepare_client_session_only"])

    def test_non_private_session_identity_fails_before_namespace_creation(self):
        with mock.patch.object(
            client_speed, "execute_ephemeral_client_namespace_probe"
        ) as execute:
            result = client_speed.prepare_exact_client_probe_session(
                "8.8.8.8"
            )
        execute.assert_not_called()
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "PROBE_INVALID")

    def test_target_payload_mode_reuses_payload_primitive_without_user_recovery_claim(self):
        context = self.target_payload_context()
        attempt = self.successful_attempt()
        attempt["route"] = {
            "ok": True,
            "dev": "awg3",
            "table": "main",
            "prefsrc": "10.8.0.2",
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "target-context.json"
            path.write_text(json.dumps(context), encoding="utf-8")
            with mock.patch.object(
                client_speed,
                "execute_fresh_exact_probe_request",
                return_value=(attempt, [attempt]),
            ) as execute:
                receipt = client_speed.run_target_egress_payload_context(path)
        execute.assert_called_once()
        self.assertEqual(
            receipt["status"],
            "TARGET_EGRESS_ROUTE_BOUND_PAYLOAD_PROBE_PROVEN",
        )
        self.assertEqual(receipt["scope"], "TARGET_EGRESS_PATH_ONLY")
        self.assertFalse(receipt["exact_user_source_fwmark_table_traversed"])
        self.assertFalse(receipt["remote_client_recovery_claimed"])
        self.assertEqual(receipt["user_movement"], 0)

    def test_target_payload_route_lookup_models_the_existing_interface_bound_socket(self):
        context = self.target_payload_context()
        context["target_egress_interface_bound_probe"] = True
        with mock.patch.object(
            client_speed.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(
                [], 0, stdout=json.dumps([{"dev": "awg3", "table": "main"}])
            ),
        ) as run:
            route = client_speed.route_lookup_for_exact_probe("1.1.1.1", context)
        self.assertTrue(route["ok"])
        self.assertEqual(route["dev"], "awg3")
        self.assertEqual(run.call_args.args[0][-2:], ["oif", "awg3"])

    def test_target_payload_context_requires_full_operation_lineage(self):
        context = self.target_payload_context()
        context.pop("lease_id")
        context["context_hash"] = client_speed.exact_probe_context_hash(context)
        errors = client_speed.target_egress_payload_context_errors(context)
        self.assertIn("lease_id_missing", errors)


if __name__ == "__main__":
    unittest.main()
