import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from datetime import timedelta
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


def load_admin_api():
    loader = importlib.machinery.SourceFileLoader("v7_admin_api_realtime_truth", str(ADMIN_API))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class AdminRealtimeTruthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin = load_admin_api()

    def test_live_operational_truth_reads_current_registry_and_matrix_without_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "users.registry").write_text(
                "ip=10.7.0.125 current=awg0 table=1123 enabled=1\n",
                encoding="utf-8",
            )
            (state / "egress.registry").write_text(
                "id=vless interface=vless enabled=1\n"
                "id=awg0 interface=awg0 enabled=1\n",
                encoding="utf-8",
            )
            matrix = state / "service-matrix.json"
            matrix.write_text(json.dumps({
                "items": {
                    "vless": {"services": {"telegram": {"ok": False, "status": "FAIL"}}},
                    "awg0": {"services": {"telegram": {"ok": True, "status": "OK"}}},
                }
            }), encoding="utf-8")
            previous_state, previous_matrix = self.admin.STATE_DIR, self.admin.SERVICE_MATRIX_FILE
            self.addCleanup(setattr, self.admin, "STATE_DIR", previous_state)
            self.addCleanup(setattr, self.admin, "SERVICE_MATRIX_FILE", previous_matrix)
            self.admin.STATE_DIR = state
            self.admin.SERVICE_MATRIX_FILE = matrix

            payload = self.admin.live_operational_truth()

        self.assertTrue(payload["read_only"])
        self.assertEqual(payload["canonical_sources"]["assignment"], "users.registry")
        self.assertEqual(payload["registries"]["users"][0]["current"], "awg0")
        self.assertEqual(payload["channel_user_counts"], {"awg0": 1})
        self.assertFalse(payload["service_matrix"]["items"]["vless"]["services"]["telegram"]["ok"])

    def test_live_status_transport_cache_is_short_and_not_a_state_owner(self):
        source = ADMIN_API.read_text(encoding="utf-8")

        self.assertIn("LIVE_STATUS_CACHE_TTL_SEC = 1.0", source)
        self.assertIn("canonical registries and Matrix", source)
        self.assertIn("self.send_json_bytes(live_operational_truth_json())", source)

    def test_overview_uses_existing_killswitch_summary_without_duplicate_user_report(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        overview = source[source.index("def overview(session=None):"):source.index("def live_operational_truth():")]

        self.assertIn('["v7-killswitch-check", "--admin-summary"]', overview)
        self.assertIn("route_status(active_users)", overview)
        checker = (ROOT / "hardening" / "v7-killswitch-check").read_text(encoding="utf-8")
        self.assertIn("--admin-summary", checker)
        self.assertIn("user_route_check=deferred_to_admin_route_reality", checker)
        sync = (ROOT / "tools" / "v7_sync_lib.py").read_text(encoding="utf-8")
        self.assertIn('"local_path": "hardening/v7-killswitch-check"', sync)

    def test_overview_smart_profiles_reuse_one_artifact_tree_scan(self):
        users = [
            {"ip": "10.7.0.125", "enabled": "1"},
            {"ip": "10.7.0.126", "enabled": "1"},
        ]
        artifact_map = {
            "10.7.0.125": [{"name": "first-profile", "config_ready": True}],
            "10.7.0.126": [{"name": "second-profile", "config_ready": True}],
        }
        with mock.patch.object(self.admin, "client_artifacts_map", return_value=artifact_map) as scan, \
             mock.patch.object(self.admin, "smart_client_profiles_for_ip", return_value={"available": True}) as profiles:
            result = self.admin.smart_client_profiles_map(users)

        scan.assert_called_once_with(users)
        self.assertEqual(result, {"10.7.0.125": {"available": True}, "10.7.0.126": {"available": True}})
        self.assertEqual(profiles.call_count, 2)
        self.assertEqual(profiles.call_args_list[0].kwargs["client_name"], "first-profile")

    def test_overview_smart_profiles_do_not_rescan_users_without_wireguard_artifact(self):
        users = [{"ip": "10.7.0.125", "enabled": "1"}]
        with mock.patch.object(self.admin, "client_artifacts_map", return_value={"10.7.0.125": []}) as scan, \
             mock.patch.object(self.admin, "smart_client_profiles_for_ip", return_value={"available": True}) as profiles:
            self.admin.smart_client_profiles_map(users)

        scan.assert_called_once_with(users)
        profiles.assert_called_once()
        self.assertEqual(profiles.call_args.kwargs["client_name"], "user-10-7-0-125")

    def test_admin_page_uses_lightweight_live_status_polling(self):
        page = self.admin.html_page_v2()
        self.assertIn("/api/live-status", page)
        self.assertIn("liveOperationalTruthTimer = window.setInterval", page)
        self.assertIn("refreshLiveOperationalTruth('timer'), 2000", page)
        self.assertIn("Operator actions update their own rows immediately", page)
        self.assertIn("mergeLiveOperationalTruthIntoOverview", page)

    def test_new_profile_binds_requested_configured_egress_without_health_query(self):
        with mock.patch.object(self.admin, "egress_exists", return_value=True) as exists:
            binding = self.admin.identity_egress_issuance_binding("vless")

        self.assertTrue(binding["ok"])
        self.assertEqual(binding["selected_egress"], "vless")
        self.assertFalse(binding["health_checked"])
        self.assertEqual(binding["owner"], "existing egress.registry")
        exists.assert_called_once_with("vless", enabled_only=True)

    def test_profile_issue_paths_do_not_run_health_admission_before_provisioning(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        quick = source[source.index("def identity_issue_config_quick"):source.index("def pending_profile_public_key")]
        device = source[source.index("def identity_issue_device"):source.index("def identity_issue_config_quick")]
        self.assertIn("binding = identity_egress_issuance_binding(requested_egress)", quick)
        self.assertIn("binding = identity_egress_issuance_binding(requested_egress)", device)
        self.assertNotIn("identity_egress_admission", quick)
        self.assertNotIn("identity_egress_admission", device)

    def test_profile_issue_removes_obsolete_admission_and_returns_result_before_overview(self):
        autoswitch = (ROOT / "tools" / "v7-users-autoswitch").read_text(encoding="utf-8")
        self.assertNotIn("ordinary_new_user_admission_only", autoswitch)
        self.assertNotIn("--new-user-admission", autoswitch)

        source = ADMIN_API.read_text(encoding="utf-8")
        handler = source[
            source.index('elif path == "/api/actions/identity-device-issue"'):
            source.index('elif path == "/api/actions/pending-profile-create"')
        ]
        self.assertIn("self.send_json(payload, status=status)", handler)
        self.assertNotIn('"overview": overview()', handler)
        page = self.admin.html_page_v2()
        self.assertIn("Его здоровье не проверяется в момент выдачи", page)
        self.assertIn("Профиль не выдан", page)

    def test_existing_profile_selected_channel_uses_exact_operator_rebind_not_health_admission(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        operation = source[
            source.index("def operator_profile_egress_rebind"):
            source.index("def autoswitch_read_only_plan_command")
        ]
        page = self.admin.html_page_v2()

        self.assertIn('action_class="USER_SWITCH"', operation)
        self.assertIn('["v7-user-switch", user_ip, requested]', operation)
        self.assertIn('"health_checked": False', operation)
        self.assertNotIn("AutoswitchPlanner", operation)
        self.assertIn('/api/actions/operator-profile-egress-rebind', page)
        self.assertIn('OPERATOR_PROFILE_EGRESS_REBIND', page)

    def test_inline_channel_choice_starts_governed_rebind_without_intermediate_drawer(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        page = self.admin.html_page_v2()
        start = page.index("const USER_SWITCH_DEADLINE_MS")
        end = page.index("function v2PostEnableNextActions", start)
        inline = page[start:end]

        self.assertIn("setUserSwitchOptimistic(ip, egress, previous)", inline)
        self.assertIn("/api/actions/operator-profile-egress-rebind", inline)
        self.assertIn("OPERATOR_PROFILE_EGRESS_REBIND", inline)
        self.assertIn("USER_SWITCH_DEADLINE_MS = 7000", inline)
        self.assertIn("requestOperatorProfileEgressRebind(ip, egress)", inline)
        self.assertIn("operator_profile_execution_control_unavailable", inline)
        self.assertIn("USER_SWITCH_RETRY_MS = 140", inline)
        self.assertNotIn("openGovernedMovementRequired", inline)
        operation = source[
            source.index("def operator_profile_egress_rebind"):
            source.index("def autoswitch_read_only_plan_command")
        ]
        self.assertIn('timeout=7', operation)
        self.assertIn('writer_deadline_exceeded_7s', operation)

    def test_operator_rebind_uses_core_primary_commit_as_authoritative_kernel_evidence(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        operation = source[
            source.index("def operator_profile_egress_rebind"):
            source.index("def autoswitch_read_only_plan_command")
        ]

        self.assertIn('core_primary_committed = "V7_CORE_PRIMARY_SYNC=PASS" in writer_output', operation)
        self.assertIn('kernel_route_observed = core_primary_committed or legacy_route_observed', operation)
        self.assertIn('"verification_mode": "CORE_PRIMARY_COMMIT" if core_primary_committed else "LEGACY_ROUTE_OUTPUT"', operation)

    def test_mutating_requests_refresh_a_stale_csrf_token_once_before_failing(self):
        page = self.admin.html_page_v2()
        start = page.index("async function refreshCsrfToken")
        end = page.index("function showToast", start)
        post = page[start:end]

        self.assertIn("api('/api/session')", post)
        self.assertIn("r.status === 403 && data?.error === 'csrf_failed'", post)
        self.assertIn("return postJson(path, body, {csrfRetry:false})", post)
        self.assertIn("The server checks CSRF before dispatching", post)

    def test_priority_save_surfaces_rejection_and_reuses_written_preference_state(self):
        page = self.admin.html_page_v2()
        start = page.index("function saveUserPriorities")
        end = page.index("function userTableColumns", start)
        save = page[start:end]

        self.assertIn("if (!d._http_ok || d.error)", save)
        self.assertIn("showToast('Приоритеты не сохранены'", save)
        self.assertIn("overview.service_preferences = d.preferences", save)

    def test_priority_picker_saves_immediately_without_overview_round_trip(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        page = self.admin.html_page_v2()

        self.assertIn("onchange=\"queueUserPrioritySave", page)
        self.assertIn("Изменения сохраняются сразу после выбора", page)
        self.assertIn("if (path === '/api/actions/service-preferences-update') return false", page)
        start = source.index('elif path == "/api/actions/service-preferences-update":')
        end = source.index("        else:\n            self.send_json({\"error\": \"not_found\"", start)
        handler = source[start:end]
        self.assertIn('self.send_json({"action": "service_preferences_update", "preferences": prefs})', handler)
        self.assertNotIn('"overview": overview()', handler)

    def test_new_profile_materializes_the_displayed_standard_service_contract(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        device = source[source.index("def identity_issue_device"):source.index("def identity_issue_config_quick")]
        connect = source[source.index("def connect_onboard"):source.index("def audit_admin")]
        self.assertIn("def materialize_default_service_preferences_for_new_profile", source)
        self.assertIn("services=DEFAULT_USER_PRIORITY_SERVICES", source)
        self.assertIn("materialize_default_service_preferences_for_new_profile(actor, ip)", device)
        self.assertIn('materialize_default_service_preferences_for_new_profile("connect", parsed["ip"])', connect)

    def test_unchanged_karing_reissue_does_not_restart_public_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ip = "10.7.0.9"
            name = "known-device"
            auth_user = self.admin.proxy_auth_user(ip, name, "karing")
            proxy_uuid = "11111111-1111-4111-8111-111111111111"
            config_path = root / "config.json"
            binding_path = root / "binding.json"
            config = {
                "inbounds": [{"type": "vless", "users": [{"uuid": proxy_uuid, "name": auth_user}]}],
                "outbounds": [{"type": "direct", "tag": "v7-egress-vless", "bind_interface": "vless"}],
                "route": {"rules": [{"auth_user": [auth_user], "outbound": "v7-egress-vless"}]},
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            binding_path.write_text(json.dumps({
                "schema": "v7-proxy-identity-binding/v1",
                "status": "binding_active",
                "inbound_id": self.admin.PROXY_INBOUND_ID,
                "client": "karing",
                "user_ip": ip,
                "label": name,
                "proxy_protocol": "vless",
                "proxy_uuid": proxy_uuid,
                "auth_user": auth_user,
                "public_host": "profile.test",
                "public_port": self.admin.PROXY_PUBLIC_PORT,
                "included_in_runtime_config": True,
                "created_at": "2026-08-28T00:00:00+00:00",
                "updated_at": "2026-08-28T00:00:00+00:00",
            }), encoding="utf-8")
            calls = []

            def fake_action(command, actor, timeout=0):
                calls.append(command)
                return {"rc": 0, "output": "active"}

            with mock.patch.object(self.admin, "ensure_public_proxy_reply_route", return_value={"rc": 0}), \
                 mock.patch.object(self.admin, "proxy_public_config_path", return_value=config_path), \
                 mock.patch.object(self.admin, "proxy_binding_path", return_value=binding_path), \
                 mock.patch.object(self.admin, "public_profile_host", return_value="profile.test"), \
                 mock.patch.object(self.admin, "proxy_runtime_egress_for_user", return_value={"egress_id": "vless", "interface": "vless", "outbound_tag": "v7-egress-vless", "connect_timeout": ""}), \
                 mock.patch.object(self.admin, "run_action", side_effect=fake_action):
                result = self.admin.ensure_karing_vless_identity(ip, name, "test")

            self.assertEqual(result["rc"], 0)
            self.assertFalse(result["config_changed"])
            self.assertFalse(result["binding_changed"])
            self.assertFalse(result["runtime_restarted"])
            self.assertEqual(calls, [["systemctl", "is-active", "--quiet", self.admin.PROXY_PUBLIC_SERVICE]])

    def test_completed_execution_control_does_not_freeze_profile_issuance(self):
        with tempfile.TemporaryDirectory() as tmp:
            safe_mode = Path(tmp) / "safe-mode.json"
            control = self.admin.operator_execution.build_autonomous_execution_control_state(
                True,
                actor="governed-execution-finalizer",
                reason="GOVERNED_TRANSACTION_COMPLETED",
            )
            self.admin.write_json_atomic(safe_mode, control)
            previous = self.admin.SAFE_MODE_FILE
            self.addCleanup(setattr, self.admin, "SAFE_MODE_FILE", previous)
            self.admin.SAFE_MODE_FILE = safe_mode

            state = self.admin.admin_safe_mode_state()
            self.assertTrue(state["execution_control_enabled"])
            self.assertFalse(state["enabled"])
            self.assertFalse(self.admin.admin_safe_mode_enabled())

            enabled = self.admin.set_admin_safe_mode("admin", True, "maintenance")
            self.assertTrue(enabled["enabled"])
            disabled = self.admin.set_admin_safe_mode("admin", False, "done")
            self.assertFalse(disabled["enabled"])

    def test_expired_exact_operation_window_is_reconciled_before_admin_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            safe_mode = Path(tmp) / "safe-mode.json"
            control = self.admin.operator_execution.build_autonomous_execution_control_state(
                False,
                actor="runtime",
                reason="one_user_operation",
                operation_id="operation-1",
                selected_move_hash="move-hash",
                action_class="USER_SWITCH",
                source_bundle_hash="source-hash",
                snapshot_bundle_hash="snapshot-hash",
                max_users=1,
                now=self.admin.operator_execution.utc_now() - timedelta(seconds=901),
            )
            self.admin.write_json_atomic(safe_mode, control)
            previous = self.admin.SAFE_MODE_FILE
            self.addCleanup(setattr, self.admin, "SAFE_MODE_FILE", previous)
            self.admin.SAFE_MODE_FILE = safe_mode

            recovered = self.admin.reconcile_expired_operation_execution_control("operator")

            after = self.admin.operator_execution.autonomous_execution_control_state(safe_mode)
            self.assertTrue(recovered["attempted"])
            self.assertTrue(recovered["recovered"])
            self.assertTrue(after["valid"])
            self.assertEqual(after["state"], "OPEN")
            self.assertFalse(self.admin.admin_safe_mode_enabled())

    def test_expired_operation_window_with_explicit_admin_freeze_stays_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            safe_mode = Path(tmp) / "safe-mode.json"
            control = self.admin.operator_execution.build_autonomous_execution_control_state(
                False,
                actor="runtime",
                reason="one_user_operation",
                operation_id="operation-1",
                selected_move_hash="move-hash",
                action_class="USER_SWITCH",
                source_bundle_hash="source-hash",
                snapshot_bundle_hash="snapshot-hash",
                max_users=1,
                now=self.admin.operator_execution.utc_now() - timedelta(seconds=901),
            )
            control["admin_safe_mode"] = {"enabled": True, "reason": "maintenance"}
            self.admin.write_json_atomic(safe_mode, control)
            previous = self.admin.SAFE_MODE_FILE
            self.addCleanup(setattr, self.admin, "SAFE_MODE_FILE", previous)
            self.admin.SAFE_MODE_FILE = safe_mode

            recovered = self.admin.reconcile_expired_operation_execution_control("operator")

            after = self.admin.operator_execution.autonomous_execution_control_state(safe_mode)
            self.assertFalse(recovered["attempted"])
            self.assertEqual(after["state"], "CLOSED")


if __name__ == "__main__":
    unittest.main()
