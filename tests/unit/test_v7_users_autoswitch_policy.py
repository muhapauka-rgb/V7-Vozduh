import importlib.machinery
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock
from pathlib import Path
from typing import Optional

from admin_core.intelligence_snapshots import build_snapshot_envelope, snapshot_path
from admin_core import operator_execution


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-users-autoswitch"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class V7UsersAutoswitchPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def test_fast_profile_services_are_explicit_and_telegram_is_not_universal(self):
        # Planner ranking retains its historical best-effort defaults.
        self.assertEqual(
            self.tool.user_priority_services_from_pref({}),
            list(self.tool.DEFAULT_USER_PRIORITY_SERVICES),
        )
        planner = object.__new__(self.tool.AutoswitchPlanner)
        planner.users = []
        self.assertEqual(
            planner._verification_required_services({
                "important_services": list(self.tool.DEFAULT_USER_PRIORITY_SERVICES),
                "profile_required_services": ["telegram"],
            }),
            ["telegram"],
        )
        self.assertEqual(
            planner._verification_required_services({
                "important_services": list(self.tool.DEFAULT_USER_PRIORITY_SERVICES),
                "profile_required_services": [],
            }),
            [],
        )

    def test_empty_profile_uses_existing_path_owner_without_service_probes(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            (state / "service-matrix.json").write_text(
                json.dumps({"items": {"target": {"services": {}}}}),
                encoding="utf-8",
            )
            planner = object.__new__(self.tool.AutoswitchPlanner)
            planner.state_dir = state
            planner.args = SimpleNamespace(service_matrix_lock_timeout_sec=1)
            planner.emergency_failover_policy = {}
            current = {
                "status": "OK",
                "path_evidence": {
                    "path_fingerprint": "path-current",
                    "service_set_fingerprint": "services-current",
                    "egress_identity_generation": "identity-current",
                },
            }
            with mock.patch.object(
                self.tool.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(
                    ["v7-service-matrix-test"], 0, stdout=json.dumps(current),
                ),
            ) as run:
                result = planner._reuse_or_verify_emergency_required_services({
                    "recommended_egress": "target",
                    "important_services": [],
                })

        self.assertEqual(result.returncode, 0, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(
            payload["status"],
            "FRESH_CHANNEL_PATH_VERIFIED_NO_PROFILE_SERVICES",
        )
        self.assertEqual(payload["required_services"], [])
        self.assertEqual(payload["profile_service_probe_count"], 0)
        command = run.call_args.args[0]
        self.assertIn("--path-evidence-only", command)
        self.assertNotIn("--services", command)

    def test_route_writer_failure_code_is_safe_and_bounded(self):
        self.assertEqual(
            self.tool.route_writer_failure_code(
                "V7_ROUTE_WRITE_FAILURE=ROUTE_INTERFACE_UNAVAILABLE\n", 1
            ),
            "ROUTE_WRITER_ROUTE_INTERFACE_UNAVAILABLE",
        )
        self.assertEqual(
            self.tool.route_writer_failure_code(
                "STOP_SAFE: autonomous execution control denied\n", 2
            ),
            "EXECUTION_CONTROL_DENIED_BEFORE_ROUTE_WRITER",
        )
        self.assertEqual(
            self.tool.route_writer_failure_code("", 1),
            "ROUTE_WRITER_OUTPUT_UNAVAILABLE",
        )
        self.assertEqual(
            self.tool.route_writer_failure_code(
                "V7_ROUTE_WRITE_FAILURE=ROUTE_EGRESS_INTERFACE_MISSING\n", 1
            ),
            "ROUTE_WRITER_ROUTE_EGRESS_INTERFACE_MISSING",
        )
        self.assertEqual(
            self.tool.route_writer_failure_code(
                "V7_ROUTE_WRITE_FAILURE=ROUTE_POST_APPLY_OBSERVATION_FAILED\n", 1
            ),
            "ROUTE_WRITER_ROUTE_POST_APPLY_OBSERVATION_FAILED",
        )

    def write_fixture(
        self,
        root: Path,
        *,
        users: int = 1,
        egress_1_services: Optional[dict] = None,
        egress_1_state: str = "enabled",
        current_egress: str = "1",
        vless_registry_extra: str = "",
        route_fitness_1: str = "OK",
        service_signals: Optional[dict] = None,
        restore_barrier: Optional[dict] = None,
        authority_budget: Optional[dict] = None,
        emergency_failover_autonomy: Optional[dict] = None,
    ) -> None:
        state_dir = root / "state"
        event_dir = root / "events"
        state_dir.mkdir()
        event_dir.mkdir()
        registry = []
        for idx in range(users):
            registry.append(f"ip=10.0.0.{idx + 2} current={current_egress} table={100 + idx} enabled=1")
        (state_dir / "users.registry").write_text("\n".join(registry) + "\n", encoding="utf-8")
        (state_dir / "egress.registry").write_text(
            f"id=1 interface=v7one enabled=1 state={egress_1_state} role=GLOBAL_FAST\n"
            f"id=vless interface=tun0 enabled=1 role=GLOBAL_FAST{vless_registry_extra}\n",
            encoding="utf-8",
        )
        (state_dir / "v7-state.json").write_text(
            json.dumps(
                {
                    "egress": {
                        "1": {
                            "avg_mbps": 80,
                            "min_mbps": 70,
                            "stability": 0.95,
                            "code": "200",
                            "diagnose_severity": "OK",
                        },
                        "vless": {
                            "avg_mbps": 50,
                            "min_mbps": 45,
                            "stability": 0.9,
                            "code": "200",
                            "diagnose_severity": "OK",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        base_services = {
            "youtube": {"ok": True, "score": 100},
            "instagram": {"ok": True, "score": 100},
            "telegram": {"ok": True, "status": "OK", "score": 100},
            "google": {"ok": True, "score": 100},
            "google_auth": {"ok": True, "score": 100},
        }
        base_services.update(egress_1_services or {})
        (state_dir / "service-matrix.json").write_text(
            json.dumps(
                {
                    "items": {
                        "1": {
                            "services": base_services,
                            "route_class_fitness": {
                                "VIDEO_OPTIMIZED": {"status": route_fitness_1},
                                "GLOBAL_STABLE": {"status": "OK"},
                                "GLOBAL_FAST": {"status": "OK"},
                            },
                        },
                        "vless": {
                            "services": {
                                "youtube": {"ok": True, "score": 100},
                                "instagram": {"ok": True, "score": 100},
                                "telegram": {"ok": True, "status": "OK", "score": 100},
                                "google": {"ok": True, "score": 100},
                                "google_auth": {"ok": True, "score": 100},
                            },
                            "route_class_fitness": {
                                "VIDEO_OPTIMIZED": {"status": "OK"},
                                "GLOBAL_STABLE": {"status": "OK"},
                                "GLOBAL_FAST": {"status": "OK"},
                            },
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        policy = {
            "switch": {
                "autoswitch_enabled": True,
                "autoswitch_max_failover_per_run": 25,
                "cooldown_seconds": 0,
                "min_score_delta": 5000,
            },
            "load": {"rebalance_enabled": False},
            "reconnect": {"enabled": False},
            "service_signals": service_signals or {},
        }
        if authority_budget is not None:
            policy["authority_budget"] = dict(authority_budget)
            contract = policy["authority_budget"].get("current_action_class_contract")
            if not isinstance(contract, dict):
                contract = {
                    "schema_version": "v7.current-action-class-contract.v1",
                    "issuing_owner": operator_execution.CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
                    "active_program": "UNIT_TEST",
                    "action_class": "GOVERNED_ONLY",
                    "max_authority_class": "POOL",
                    "subject": {"user_ip": "10.0.0.2"},
                    "max_users": 100,
                    "max_concurrent_transactions": 100,
                    "incident_generation": {"incident_id": "unit-incident"},
                    "source_generation": {
                        "planner_generation_id": "unit-planner-generation",
                        "source_bundle_hash": "unit-source-bundle",
                        "snapshot_bundle_hash": "unit-snapshot-bundle",
                        "selected_move_hash": "unit-selected-move",
                    },
                    "issued_at": "2026-01-01T00:00:00+00:00",
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "scope": {"source_egress": "fixture-source", "target_egress": "fixture-target"},
                    "verification_contract": {"owner": "unit-test", "required": True},
                    "rollback_containment_contract": {"owner": "unit-test", "required": True},
                    "cooldown": {"required": True, "seconds": 180},
                    "anti_flap": {"required": True},
                    "required_gates": {
                        "fresh_evidence_required": True,
                        "verification_required": True,
                        "rollback_required": True,
                        "anti_flap_required": True,
                        "cooldown_seconds": 180,
                    },
                    "stop_conditions": ["no_safe_target", "stale_evidence", "verification_failure"],
                    "authority_decision": {
                        "decision": operator_execution.ENGINEERING_AUTHORITY_APPROVAL,
                        "request_id": "accauth_r1_unit",
                        "request_hash": "unit-request-hash",
                        "decided_at": "2026-01-01T00:00:00+00:00",
                    },
                    "one_use_consumption": {
                        "state": "ISSUED", "allowed_uses": 1, "consumed_uses": 0,
                        "consumption_owner": "tools/v7-users-autoswitch", "retry_allowed": False,
                    },
                }
                contract["contract_hash"] = operator_execution.current_action_class_contract_hash(contract)
                contract["contract_id"] = "acc_" + contract["contract_hash"][:24]
                policy["authority_budget"]["current_action_class_contract"] = contract
        if emergency_failover_autonomy is not None:
            policy["emergency_failover_autonomy"] = emergency_failover_autonomy
        (root / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
        (root / "org-policy.json").write_text("{}", encoding="utf-8")
        for name in [
            "egress-quality-summary.json",
            "autoswitch-safety.json",
            "telegram-sentinel.json",
            "client-reconnect-state.json",
            "vless-activity.json",
            "egress-load-summary.json",
        ]:
            (state_dir / name).write_text("{}", encoding="utf-8")
        (state_dir / "autoswitch-restore-barrier.json").write_text(
            json.dumps(restore_barrier or {}), encoding="utf-8"
        )

    def args_for(self, root: Path, extra_args: Optional[list[str]] = None):
        parser = self.tool.build_arg_parser()
        control_file = root / "safe-mode.json"
        if not control_file.exists():
            control_file.write_text(
                json.dumps(self.tool.operator_execution.build_autonomous_execution_control_state(
                    False,
                    actor="unit-test",
                    reason="unit-test-controlled-window",
                )),
                encoding="utf-8",
            )
        base_args = [
            "--state-dir",
            str(root / "state"),
            "--policy-file",
            str(root / "policy.json"),
            "--org-policy-file",
            str(root / "org-policy.json"),
            "--event-dir",
            str(root / "events"),
            "--quality-summary-file",
            str(root / "state" / "egress-quality-summary.json"),
            "--safety-file",
            str(root / "state" / "autoswitch-safety.json"),
            "--telegram-sentinel-file",
            str(root / "state" / "telegram-sentinel.json"),
            "--reconnect-state-file",
            str(root / "state" / "client-reconnect-state.json"),
            "--vless-activity-file",
            str(root / "state" / "vless-activity.json"),
            "--load-summary-file",
            str(root / "state" / "egress-load-summary.json"),
            "--restore-barrier-file",
            str(root / "state" / "autoswitch-restore-barrier.json"),
            "--execution-control-file",
            str(control_file),
        ]
        return parser.parse_args(base_args + list(extra_args or []))

    def plan(self, root: Path) -> dict:
        planner = self.tool.AutoswitchPlanner(self.args_for(root))
        plan = planner.plan()
        plan["apply_result"] = planner.apply(plan)
        planner.finalize_operation(plan)
        return plan

    def test_action_class_contract_reconciliation_entrypoint_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, authority_budget={
                "enabled": True,
                "authority_class": "POOL",
                "prepared_authority_class": "POOL",
                "certified_authority_class": "POOL",
                "current_allowed_user_budget": 1,
            })
            result = self.tool.action_class_contract_reconciliation_only(self.args_for(root))

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["mode"], "POLICY_READ_ONLY_HANDOFF_WITH_EXISTING_SNAPSHOT_REFRESH")
        self.assertIn("performed", result["coherent_snapshot_preflight"])
        self.assertFalse(result["forbidden_effects"]["policy_write"])
        self.assertFalse(result["forbidden_effects"]["authority_granted"])
        self.assertFalse(result["forbidden_effects"]["runtime_apply"])
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)

    def _runtime_scope_gate_fixture(self, *, controlled: bool):
        planner = object.__new__(self.tool.AutoswitchPlanner)
        planner.emergency_failover_policy = {
            "enabled": True,
            "max_users_per_run": 4,
            "max_users_per_channel": 4,
            "require_restore_barrier": False,
            "require_rollback": False,
            "require_verification": False,
            "retry_budget_per_incident": 1,
            "runtime_scope_axes": {
                "authority_approved_max": 48,
                "controlled_certification_runtime_max": 48,
                "ordinary_production_runtime_max": 4,
            },
        }
        planner.args = mock.Mock(
            source_egress="",
            rollback_on_verify_fail=True,
            verify=True,
            emergency_failover_autonomy=True,
            apply=False,
        )
        planner.authority_budget_policy = {"current_allowed_user_budget": 48}
        planner.generation = {"planner_generation_id": "generation"}
        moves = [{
            "user_ip": f"10.7.0.{index + 2}",
            "current_egress": "controlled" if controlled else "ordinary",
            "recommended_egress": "target",
            "move_type": "failover",
        } for index in range(6)]
        source = "controlled" if controlled else "ordinary"
        context = {
            "active": True,
            "incident_source": source,
            "incident_key": "incident",
            "scope": {
                "source_failed": True,
                "controlled_certification_failure": {
                    "confirmed": controlled,
                },
            },
        }
        proof = {
            "confirmed": controlled,
            "certification_user_in_scope": controlled,
        }
        with mock.patch.object(
            planner,
            "_l3_active_incident_source_context",
            return_value=context,
        ), mock.patch.object(
            planner,
            "_controlled_certification_failure_context",
            return_value=proof,
        ), mock.patch.object(
            planner,
            "_emergency_failover_move_evidence",
            side_effect=lambda move: {
                "ok": True,
                "blockers": [],
                "user_ip": move["user_ip"],
                "current_egress": move["current_egress"],
                "recommended_egress": move["recommended_egress"],
                "current_failures": [{"service": "telegram"}],
                "current_channel_failure": {},
            },
        ), mock.patch.object(
            planner,
            "_l3_wake_decision",
            return_value={"accepted": True, "blockers": []},
        ), mock.patch.object(
            planner,
            "_l3_incident_attempt_count",
            return_value=0,
        ), mock.patch.object(
            planner,
            "_l3_semantic_attempt_signature",
            return_value="attempt",
        ), mock.patch.object(
            planner,
            "_l3_consumed_retry_attempts",
            return_value=[],
        ):
            selected, gate = planner._emergency_failover_authority_gate(
                moves,
                {},
            )
        return selected, gate

    def test_ordinary_service_failure_is_capped_to_proven_tier4(self):
        selected, gate = self._runtime_scope_gate_fixture(controlled=False)

        self.assertEqual(len(selected), 4)
        self.assertEqual(
            gate["runtime_scope"]["context"],
            "ORDINARY_PRODUCTION_SERVICE_FAILURE",
        )
        self.assertEqual(gate["effective_max_users_per_run"], 4)
        self.assertFalse(gate["runtime_scope"]["authority_expanded"])

    def test_availability_first_gate_does_not_require_incident_source_failure(self):
        planner = object.__new__(self.tool.AutoswitchPlanner)
        planner.emergency_failover_policy = {
            "enabled": True,
            "max_users_per_run": 4,
            "max_users_per_channel": 4,
            "require_restore_barrier": True,
            "require_rollback": True,
            "require_verification": True,
            "retry_budget_per_incident": 1,
            "runtime_scope_axes": {
                "authority_approved_max": 48,
                "controlled_certification_runtime_max": 48,
                "ordinary_production_runtime_max": 4,
            },
        }
        planner.args = mock.Mock(
            source_egress="vless",
            rollback_on_verify_fail=True,
            verify=True,
            emergency_failover_autonomy=True,
            apply=True,
        )
        planner.authority_budget_policy = {
            "current_allowed_user_budget": 48,
        }
        planner.generation = {"planner_generation_id": "generation"}
        move = {
            "user_ip": "10.7.0.100",
            "current_egress": "vless",
            "recommended_egress": "awg3",
            "move_type": "failover",
            "availability_first_controlled_assignment": {
                "schema_version": (
                    "v7.availability-first-controlled-selection.v1"
                ),
                "event_provenance": "CONTROLLED_CERTIFICATION",
                "natural_production_credit": False,
                "source": "vless",
                "target": "awg3",
                "allocation_fingerprint": "c" * 64,
                "ordinary_user": False,
            },
        }
        availability_scope = {
            "ok": True,
            "sources": ["vless"],
            "event_provenance": "CONTROLLED_CERTIFICATION",
            "natural_production_credit": False,
        }
        with mock.patch.object(
            planner,
            "_approved_l3_production_validation_envelope",
            return_value={
                "ok": True,
                "selected_move_count": 1,
                "clearance_max_selected_moves": 1,
                "authorized_l3_budget": 1,
            },
        ), mock.patch.object(
            planner,
            "_l3_active_incident_source_context",
            return_value={
                "active": True,
                "incident_source": "1",
                "scope": {
                    "source_failed": True,
                    "controlled_certification_failure": {
                        "confirmed": False,
                    },
                },
            },
        ), mock.patch.object(
            planner,
            "_l3_failed_source_scope",
            return_value={"source_failed": False},
        ), mock.patch.object(
            planner,
            "_exact_availability_first_controlled_scope",
            return_value=availability_scope,
        ), mock.patch.object(
            planner,
            "_controlled_certification_failure_context",
            return_value={
                "confirmed": False,
                "certification_user_in_scope": False,
            },
        ), mock.patch.object(
            planner,
            "_emergency_failover_move_evidence",
        ) as ordinary_evidence:
            selected, gate = (
                planner._emergency_failover_authority_gate(
                    [move],
                    {"failover_quarantine": True},
                )
            )

        self.assertEqual(len(selected), 1)
        self.assertTrue(gate["ok"])
        self.assertEqual(gate["blockers"], [])
        self.assertEqual(
            gate["decision"],
            (
                "authorize_availability_first_controlled_"
                "certification_envelope"
            ),
        )
        self.assertEqual(
            gate["runtime_scope"]["context"],
            "AVAILABILITY_FIRST_CONTROLLED_CERTIFICATION_CONTEXT",
        )
        self.assertFalse(gate["natural_production_credit"])
        ordinary_evidence.assert_not_called()
        self.assertEqual(gate["effective_max_users_per_run"], 1)
        self.assertFalse(gate["runtime_scope"]["authority_expanded"])

    def test_exact_controlled_certification_context_can_consume_tier48_ceiling(self):
        selected, gate = self._runtime_scope_gate_fixture(controlled=True)

        self.assertEqual(len(selected), 6)
        self.assertEqual(
            gate["runtime_scope"]["context"],
            "CONTROLLED_CERTIFICATION_CONTEXT",
        )
        self.assertEqual(gate["effective_max_users_per_run"], 48)
        self.assertEqual(gate["runtime_scope"]["authority_approved_max"], 48)

    def test_action_contract_reconciliation_consumes_precontract_l3_wake_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={
                    "telegram": {
                        "ok": False,
                        "status": "DOWN",
                        "score": 0,
                        "consecutive_failures": 3,
                        "tested_at": fresh,
                    },
                },
                restore_barrier={
                    "enabled": True,
                    "expires_at": fresh,
                    "reason": "unit-test",
                },
                authority_budget={
                    "authority_class": "POOL",
                    "certified_authority_class": "POOL",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 1,
                    "current_action_class_contract": {},
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            result = self.tool.action_class_contract_reconciliation_only(self.args_for(root))

        request = result["result"]
        self.assertEqual(
            request["status"],
            "ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS",
        )
        self.assertTrue(request["issue_preflight"]["l3_wake_accepted"])
        self.assertIn("intelligence_snapshot_gate_stop_required", request["issue_preflight"]["blockers"])
        self.assertEqual(result["l3_evidence_mode"], "PRE_CONTRACT_SHADOW_SELECTION_READ_ONLY")
        self.assertFalse(result["forbidden_effects"]["policy_write"])
        self.assertFalse(result["forbidden_effects"]["runtime_apply"])
        self.assertFalse(result["forbidden_effects"]["candidate_created"])
        self.assertFalse(result["forbidden_effects"]["packet_created"])
        self.assertFalse(result["forbidden_effects"]["lease_created"])

    def test_action_contract_reconciliation_uses_coherent_observe_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = {
                "safety": {
                    "action_class_execution_boundary": {
                        "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                    },
                    "authority_budget_gate": {
                        "current_action_class_contract": {"required": True, "valid": False, "blockers": ["missing"]},
                    },
                    "intelligence_snapshots": {
                        "stop_required": False,
                        "pre_planner_refresh": {
                            "state": "REFRESH_SUCCESS",
                            "service_matrix_lock": {"acquired": True},
                            "refresh_result": {"source_stable": True},
                        },
                    },
                },
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "1",
                }],
            }
            with mock.patch.object(self.tool, "AutoswitchPlanner") as planner_class:
                planner_class.return_value.plan.return_value = plan
                result = self.tool.action_class_contract_reconciliation_only(self.args_for(root))

        coherent_calls = [
            call.args[0]
            for call in planner_class.call_args_list
            if call.args
            and getattr(call.args[0], "mode", "") == "observe"
            and getattr(call.args[0], "pre_planner_refresh", "") == "off"
            and getattr(call.args[0], "emergency_failover_autonomy", False)
        ]
        self.assertEqual(len(coherent_calls), 1)
        coherent_args = coherent_calls[0]
        self.assertEqual(coherent_args.mode, "observe")
        self.assertEqual(coherent_args.pre_planner_refresh, "off")
        self.assertTrue(coherent_args.emergency_failover_autonomy)
        self.assertTrue(result["coherent_snapshot_preflight"]["performed"])
        self.assertTrue(result["coherent_snapshot_preflight"]["source_stable"])
        self.assertTrue(result["coherent_snapshot_preflight"]["shared_service_matrix_lock_held"])

    def test_fresh_matching_channel_path_matrix_is_reused_after_user_route_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root))
            path = {
                "path_fingerprint": "a" * 64,
                "service_set_fingerprint": "b" * 64,
                "egress_identity_generation": "egid_test",
                "measured_at": "2999-01-01T00:00:00+00:00",
            }
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix.setdefault("items", {}).setdefault("1", {}).update({
                "path_evidence": path,
                "services": {
                    "telegram": {
                        "ok": True,
                        "status": "OK",
                        "tested_at": "2999-01-01T00:00:00+00:00",
                        "egress_identity_generation": "egid_test",
                    }
                },
            })
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            current = {**path}
            original_run = self.tool.subprocess.run

            def fake_run(command, **kwargs):
                self.assertIn("--path-evidence-only", command)
                return subprocess.CompletedProcess(
                    command, 0,
                    stdout=json.dumps({"status": "PASS", "path_evidence": current}),
                )

            try:
                self.tool.subprocess.run = fake_run
                result = planner._reuse_or_verify_emergency_required_services({
                    "recommended_egress": "1",
                    "important_services": ["telegram"],
                })
            finally:
                self.tool.subprocess.run = original_run

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "REUSED_FRESH_CHANNEL_PATH_MATRIX")
        self.assertFalse(payload["full_matrix_refreshed"])
        self.assertEqual(payload["matrix_scope"], "EGRESS_PATH_AND_CHANNEL_PROFILE")

    def test_changed_path_fingerprint_runs_full_existing_matrix_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root))
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix.setdefault("items", {}).setdefault("1", {}).update({
                "path_evidence": {
                    "path_fingerprint": "a" * 64,
                    "service_set_fingerprint": "b" * 64,
                    "egress_identity_generation": "egid_test",
                },
                "services": {
                    "telegram": {
                        "ok": True,
                        "status": "OK",
                        "tested_at": "2999-01-01T00:00:00+00:00",
                        "egress_identity_generation": "egid_test",
                    }
                },
            })
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            original_run = self.tool.subprocess.run
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(
                ["v7-service-matrix-test"], 0, stdout=json.dumps({"status": "OK"})
            )

            def fake_run(command, **kwargs):
                return subprocess.CompletedProcess(
                    command, 0,
                    stdout=json.dumps({
                        "status": "PASS",
                        "path_evidence": {
                            "path_fingerprint": "c" * 64,
                            "service_set_fingerprint": "b" * 64,
                            "egress_identity_generation": "egid_test",
                        },
                    }),
                )

            try:
                self.tool.subprocess.run = fake_run
                result = planner._reuse_or_verify_emergency_required_services({
                    "recommended_egress": "1",
                    "important_services": ["telegram"],
                })
            finally:
                self.tool.subprocess.run = original_run

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["matrix_reuse_decision"], "FULL_MATRIX_REFRESH_REQUIRED")
        self.assertIn("path_fingerprint_changed", payload["matrix_reuse_invalidation_reasons"])

    def test_controlled_verifier_lifecycle_start_failure_restores_source_without_direct_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            state_dir = root / "state"
            (state_dir / "users.registry").write_text(
                "ip=10.7.0.16 current=vless table=1014 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            (state_dir / "egress.registry").write_text(
                "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1\n"
                "id=vless interface=tun0 enabled=1 state=enabled role=GLOBAL_FAST\n",
                encoding="utf-8",
            )
            args = self.args_for(root, [
                "--emergency-failover-autonomy",
                "--controlled-verifier-contention",
                "--max-selected-moves", "1",
                "--user", "10.7.0.16",
                "--source-egress", "1",
                "--target-egress", "vless",
                "--approved-packet-id", "packet",
                "--approved-operation-id", "operation",
                "--approved-selected-move-hash", "move",
                "--approved-authority-generation", "authority",
                "--approved-breaker-generation", "breaker",
                "--approved-source-bundle-hash", "source-bundle",
                "--approved-snapshot-bundle-hash", "snapshot-bundle",
            ])
            planner = self.tool.AutoswitchPlanner(args)
            move = {"user_ip": "10.7.0.16", "current_egress": "1", "recommended_egress": "vless"}
            with mock.patch.object(self.tool.subprocess, "Popen", side_effect=OSError("lifecycle unavailable")), mock.patch.object(
                self.tool.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, stdout="source restored"),
            ) as run:
                result = planner._activate_controlled_verifier_contention(move, "operation")

        self.assertEqual(result["status"], "STOP_SAFE_LIFECYCLE_START_FAILED")
        self.assertFalse(result["ok"])
        self.assertFalse(result["direct_rollback_invoked"])
        self.assertEqual(run.call_args.args[0], ["v7-egress-set-state", "1", "enabled", "--apply"])

    def test_controlled_verifier_reads_runtime_registry_and_lifecycle_flags_without_snapshot_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            state_dir = root / "state"
            (state_dir / "users.registry").write_text(
                "ip=10.7.0.16 current=vless table=1014 enabled=1 certification_user=1\n",
                encoding="utf-8",
            )
            state = json.loads((state_dir / "v7-state.json").read_text(encoding="utf-8"))
            state["users"] = [{"ip": "10.7.0.16", "current": "vless", "table": "1014", "enabled": "1"}]
            (state_dir / "v7-state.json").write_text(json.dumps(state), encoding="utf-8")
            (state_dir / "egress.registry").write_text(
                "id=1 interface=v7one enabled=0 state=enabled role=GLOBAL_FAST controlled_certification_source=1\n"
                "id=vless interface=tun0 enabled=1 state=enabled role=GLOBAL_FAST\n",
                encoding="utf-8",
            )
            (state_dir / "egress-flags.state").write_text("1_state=maintenance\n", encoding="utf-8")
            args = self.args_for(root, [
                "--emergency-failover-autonomy",
                "--controlled-verifier-contention",
                "--max-selected-moves", "1",
                "--user", "10.7.0.16",
                "--source-egress", "1",
                "--target-egress", "vless",
                "--approved-packet-id", "packet",
                "--approved-operation-id", "operation",
                "--approved-selected-move-hash", "move",
                "--approved-authority-generation", "authority",
                "--approved-breaker-generation", "breaker",
                "--approved-source-bundle-hash", "source-bundle",
                "--approved-snapshot-bundle-hash", "snapshot-bundle",
            ])
            planner = self.tool.AutoswitchPlanner(args)
            move = {"user_ip": "10.7.0.16", "current_egress": "1", "recommended_egress": "vless"}
            scope = planner._exact_controlled_verifier_scope([move])

        self.assertTrue(scope["ok"])
        self.assertEqual(scope["reasons"], [])
        self.assertEqual(scope["fresh_user_source"], "vless")
        self.assertEqual(scope["fresh_user_egress"], "vless")
        self.assertFalse(scope["source_enabled"])
        self.assertEqual(scope["source_state"], "maintenance")

    def test_availability_first_scope_consumes_exact_standing_semantic_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                current_egress="vless",
                vless_registry_extra=(
                    " controlled_certification_source=1"
                ),
            )
            (root / "state" / "users.registry").write_text(
                (
                    "ip=10.7.0.100 current=vless table=1098 enabled=1 "
                    "certification_user=1\n"
                ),
                encoding="utf-8",
            )
            policy_path = root / "policy.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["delegated_autonomy_policy"] = {
                "contract_id": "sdpc_unit",
                "contract_hash": "a" * 64,
            }
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(
                self.args_for(
                    root,
                    [
                        "--user", "10.7.0.100",
                        "--source-egress", "vless",
                        "--target-egress", "1",
                        "--max-selected-moves", "1",
                    ],
                )
            )
            move = {
                "user_ip": "10.7.0.100",
                "current_egress": "vless",
                "recommended_egress": "1",
                "move_type": "failover",
                "availability_first_controlled_assignment": {
                    "schema_version": (
                        "v7.availability-first-controlled-selection.v1"
                    ),
                    "event_provenance": "CONTROLLED_CERTIFICATION",
                    "natural_production_credit": False,
                    "source": "vless",
                    "target": "1",
                    "allocation_fingerprint": "b" * 64,
                    "ordinary_user": False,
                },
            }
            standing_scope = {
                "policy_profile": (
                    operator_execution
                    .AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
                ),
                "allowed_action_classes": [
                    operator_execution
                    .AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
                ],
                "action_class_scopes": {
                    operator_execution
                    .AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS: {
                        "certification_identities_only": True,
                        "max_users_per_transaction": 48,
                    },
                },
            }
            with mock.patch.object(
                operator_execution,
                "read_audit_records",
                return_value=[],
            ), mock.patch.object(
                operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={
                    "ok": True,
                    "errors": [],
                    "policy": standing_scope,
                },
            ):
                scope = (
                    planner._exact_availability_first_controlled_scope(
                        [move]
                    )
                )
                invalid = json.loads(json.dumps(move))
                invalid[
                    "availability_first_controlled_assignment"
                ]["natural_production_credit"] = True
                rejected = (
                    planner._exact_availability_first_controlled_scope(
                        [invalid]
                    )
                )

        self.assertTrue(scope["ok"])
        self.assertEqual(scope["users"], ["10.7.0.100"])
        self.assertEqual(scope["sources"], ["vless"])
        self.assertEqual(scope["targets"], ["1"])
        self.assertEqual(
            scope["event_provenance"],
            "CONTROLLED_CERTIFICATION",
        )
        self.assertFalse(scope["natural_production_credit"])
        self.assertFalse(rejected["ok"])
        self.assertIn(
            "availability_first_natural_credit_invalid:10.7.0.100",
            rejected["reasons"],
        )

    def test_availability_first_baseline_reset_uses_standing_scope_without_l3_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                current_egress="1",
                vless_registry_extra=" controlled_certification_source=1",
                emergency_failover_autonomy={"enabled": True},
            )
            (root / "state" / "users.registry").write_text(
                (
                    "ip=10.7.0.100 current=1 table=1098 enabled=1 certification_user=1\n"
                    "ip=10.0.0.2 current=1 table=1099 enabled=1\n"
                ),
                encoding="utf-8",
            )
            policy_path = root / "policy.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["delegated_autonomy_policy"] = {
                "contract_id": "sdpc_unit",
                "contract_hash": "a" * 64,
            }
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(
                self.args_for(
                    root,
                    [
                        "--emergency-failover-autonomy",
                        "--mode", "guarded",
                        "--apply",
                        "--user", "10.7.0.100",
                        "--source-egress", "1",
                        "--target-egress", "vless",
                    ],
                )
            )
            move = {
                "user_ip": "10.7.0.100",
                "current_egress": "1",
                "recommended_egress": "vless",
                "move_type": "failover",
                "execution_mode": "emergency_failover",
                "operation_id": "reset-operation",
                "selected_move_hash": "reset-hash",
                "availability_first_controlled_assignment": {
                    "schema_version": "v7.availability-first-controlled-selection.v1",
                    "event_provenance": "CONTROLLED_CERTIFICATION",
                    "natural_production_credit": False,
                    "source": "1",
                    "target": "vless",
                    "allocation_fingerprint": "b" * 64,
                    "ordinary_user": False,
                    "baseline_reset": True,
                    "controlled_baseline_source": "vless",
                },
            }
            standing_scope = {
                "policy_profile": operator_execution.AVAILABILITY_FIRST_STANDING_POLICY_PROFILE,
                "allowed_action_classes": [operator_execution.AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS],
                "action_class_scopes": {
                    operator_execution.AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS: {
                        "certification_identities_only": True,
                        "max_users_per_transaction": 48,
                    },
                },
            }
            plan = {
                "summary": {"execution_mode": "emergency_failover"},
                "operation": {
                    "operation_id": "reset-operation",
                    "selected_move_hash": "reset-hash",
                },
                "selected_moves": [move],
                "safety": {"emergency_failover_autonomy": {"enabled": True, "ok": False}},
            }
            with mock.patch.object(
                operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={"ok": True, "errors": [], "policy": standing_scope},
            ):
                scope = planner._exact_availability_first_controlled_scope([move])
                eligibility = planner._l3_execution_eligibility(plan)

        self.assertTrue(scope["ok"], scope)
        self.assertTrue(eligibility["ok"], eligibility)
        self.assertNotIn("l3_authority_gate_not_authorized", eligibility["blockers"])

    def test_execution_control_open_denies_apply_without_changing_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, ["--apply"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            selected_before = json.loads(json.dumps(plan.get("selected_moves") or []))
            Path(args.execution_control_file).write_text(
                json.dumps(self.tool.operator_execution.build_autonomous_execution_control_state(True, actor="owner", reason="stop")),
                encoding="utf-8",
            )
            with mock.patch.object(planner, "_run_switch") as switch:
                result = planner.apply(plan)

        self.assertEqual(result["reason"], "autonomous_execution_control_stop_safe")
        self.assertEqual(plan.get("selected_moves") or [], selected_before)
        switch.assert_not_called()

    def test_apply_binds_control_window_to_approved_packet_operation_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, [
                "--apply", "--no-verify", "--max-selected-moves", "1",
                "--approved-operation-id", "packet-operation-id",
            ])
            planner = self.tool.AutoswitchPlanner(args)
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {"operation_id": "runtime-operation-id", "selected_move_hash": "hash-one"},
                "selected_moves": [
                    {"user_ip": "10.0.0.2", "current_egress": "1", "recommended_egress": "vless", "move_type": "failover"},
                ],
                "summary": {"selected_moves": 1},
                "safety": {"atomic_execution_envelope": {}},
            }
            allowed = {
                "allowed": True,
                "allowed_forward_mutation": True,
                "generation": "control-generation",
                "action_class": "EMERGENCY_FAILOVER",
                "operation_id": "packet-operation-id",
                "selected_move_hash": "hash-one",
                "source_bundle_hash": "",
                "snapshot_bundle_hash": "",
                "max_users": 1,
            }
            with mock.patch.object(planner, "_execution_control_decision", return_value=allowed) as decision, mock.patch.object(
                planner,
                "_run_switch",
                return_value=subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="", stderr=""),
            ):
                planner.apply(plan)

        self.assertEqual(decision.call_args_list[0].kwargs["operation_id"], "packet-operation-id")
        self.assertEqual(decision.call_args_list[1].kwargs["operation_id"], "packet-operation-id")

    def test_operation_controlled_window_consumes_operation_scoped_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            args = self.args_for(root, [
                "--apply", "--no-verify", "--max-selected-moves", "1",
                "--approved-operation-id", "packet-operation-id",
                "--approved-selected-move-hash", "hash-one",
                "--approved-source-bundle-hash", "operation-source-hash",
                "--approved-snapshot-bundle-hash", "operation-snapshot-hash",
            ])
            planner = self.tool.AutoswitchPlanner(args)
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {"operation_id": "runtime-operation-id", "selected_move_hash": "hash-one"},
                "selected_moves": [
                    {"user_ip": "10.0.0.2", "current_egress": "1", "recommended_egress": "vless", "move_type": "failover"},
                ],
                "summary": {"selected_moves": 1},
                "safety": {
                    "atomic_execution_envelope": {
                        "source_bundle_hash": "generic-source-hash",
                        "snapshot_bundle_hash": "generic-snapshot-hash",
                    },
                },
            }
            allowed = {
                "allowed": True,
                "allowed_forward_mutation": True,
                "generation": "control-generation",
                "scope": "operation",
            }
            operation_binding = {
                "status": "BOUND",
                "source_bundle_hash": "operation-source-hash",
                "snapshot_bundle_hash": "operation-snapshot-hash",
            }
            with mock.patch.object(planner, "_execution_control_decision", return_value=allowed), mock.patch.object(
                planner, "_operation_scoped_source_binding", return_value=operation_binding,
            ), mock.patch.object(
                planner, "_validate_atomic_execution_envelope", return_value={"ok": True},
            ), mock.patch.object(
                planner, "_run_switch", return_value=subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok", stderr=""),
            ) as switch:
                result = planner.apply(plan)

        self.assertTrue(result["applied"])
        switch.assert_called_once()

    def test_operation_controlled_window_rejects_generic_envelope_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            args = self.args_for(root, [
                "--apply", "--no-verify", "--max-selected-moves", "1",
                "--approved-operation-id", "packet-operation-id",
                "--approved-selected-move-hash", "hash-one",
                "--approved-source-bundle-hash", "generic-source-hash",
                "--approved-snapshot-bundle-hash", "generic-snapshot-hash",
            ])
            planner = self.tool.AutoswitchPlanner(args)
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {"operation_id": "runtime-operation-id", "selected_move_hash": "hash-one"},
                "selected_moves": [
                    {"user_ip": "10.0.0.2", "current_egress": "1", "recommended_egress": "vless", "move_type": "failover"},
                ],
                "summary": {"selected_moves": 1},
                "safety": {"atomic_execution_envelope": {}},
            }
            allowed = {
                "allowed": True,
                "allowed_forward_mutation": True,
                "generation": "control-generation",
                "scope": "operation",
            }
            operation_binding = {
                "status": "BOUND",
                "source_bundle_hash": "operation-source-hash",
                "snapshot_bundle_hash": "operation-snapshot-hash",
            }
            with mock.patch.object(planner, "_execution_control_decision", return_value=allowed), mock.patch.object(
                planner, "_operation_scoped_source_binding", return_value=operation_binding,
            ), mock.patch.object(planner, "_run_switch") as switch:
                result = planner.apply(plan)

        self.assertFalse(result["applied"])
        self.assertEqual(result["reason"], "approved_controlled_window_binding_mismatch")
        self.assertEqual(result["binding_mismatches"], ["source_bundle_hash", "snapshot_bundle_hash"])
        self.assertEqual(result["operation_scoped_binding"], operation_binding)
        switch.assert_not_called()

    def test_operation_scoped_atomic_envelope_uses_semantic_runtime_snapshot_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            selected_hash = "operation-selected-hash"
            source_hashes = {
                key: f"semantic-{key}-hash"
                for key in self.tool.operation_scoped_binding.SOURCE_KEYS
            }
            runtime_snapshot_hash = self.tool.sha256_json({
                "users_registry_hash": source_hashes["users_registry"],
                "egress_registry_hash": source_hashes["egress_registry"],
                "selected_move_hash": selected_hash,
            })
            plan = {
                "operation": {
                    "selected_move_hash": selected_hash,
                    "selected_move_count": 1,
                },
                "safety": {
                    "atomic_execution_envelope": {
                        "selected_move_hash": selected_hash,
                        "selected_move_count": 1,
                        "runtime_snapshot_hash": runtime_snapshot_hash,
                        "source_bundle_hash": self.tool.sha256_json(source_hashes),
                        "source_bundle": {"source_hashes": source_hashes},
                    },
                },
            }
            binding = {
                "status": "BOUND",
                "source_hashes": source_hashes,
                "source_bundle_hash": self.tool.sha256_json(source_hashes),
            }
            with mock.patch.object(
                planner, "_operation_scoped_source_binding", return_value=binding,
            ):
                validation = planner._validate_atomic_execution_envelope(plan)

        self.assertTrue(validation["ok"])
        self.assertEqual(validation["state"]["condition"], "ENVELOPE_VALID")
        self.assertEqual(validation["current_runtime_snapshot_hash"], runtime_snapshot_hash)

    def test_operation_scoped_binding_preserves_approved_locked_move_semantics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            locked = {
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "vless",
                "move_type": "failover",
                "readiness": "PACKET_BOUND",
            }
            merged_live = {
                **locked,
                "readiness": "LIVE_RECOMPUTED",
            }
            plan = {
                "selected_moves": [merged_live],
                "safety": {
                    "restore_barrier": {
                        "approved_plan_lock_validation": {
                            "ok": True,
                            "selected_moves": [locked],
                        },
                    },
                },
            }
            with mock.patch.object(
                self.tool.operation_scoped_binding,
                "read_binding",
                return_value={"status": "BOUND", "source_hashes": {}},
            ) as read_binding:
                binding = planner._operation_scoped_source_binding(plan)

        self.assertEqual(
            read_binding.call_args.kwargs["selected"]["readiness"],
            "PACKET_BOUND",
        )
        self.assertEqual(binding["selected_move_source"], "approved_plan_lock")

    def test_execution_control_generation_change_stops_remaining_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=2)
            args = self.args_for(root, ["--apply", "--max-selected-moves", "2", "--no-verify"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {"operation_id": "op-batch", "selected_move_hash": "hash-batch"},
                "selected_moves": [
                    {"user_ip": "10.0.0.2", "current_egress": "1", "recommended_egress": "vless", "move_type": "rebalance"},
                    {"user_ip": "10.0.0.3", "current_egress": "1", "recommended_egress": "vless", "move_type": "rebalance"},
                ],
                "summary": {"selected_moves": 2},
                "safety": {},
            }
            original = planner._run_switch
            calls = []

            def switch_once(ip, egress, reason):
                calls.append(ip)
                Path(args.execution_control_file).write_text(
                    json.dumps(self.tool.operator_execution.build_autonomous_execution_control_state(True, actor="owner", reason="batch stop")),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok")

            planner._run_switch = switch_once
            planner._validate_atomic_execution_envelope = lambda value: {"ok": True}
            planner._l3_execution_eligibility = lambda value: {"ok": True, "active": False}
            result = planner.apply(plan)
            planner._run_switch = original

        self.assertEqual(len(calls), 1)
        self.assertTrue(result["remaining_forward_mutations_stopped"])

    def test_cohort_circuit_breaker_stops_after_first_non_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=2)
            args = self.args_for(root, ["--apply", "--max-selected-moves", "2", "--no-verify"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {"operation_id": "op-cohort", "selected_move_hash": "hash-cohort"},
                "selected_moves": [
                    {"user_ip": "10.0.0.2", "current_egress": "1", "recommended_egress": "vless", "move_type": "rebalance"},
                    {"user_ip": "10.0.0.3", "current_egress": "1", "recommended_egress": "vless", "move_type": "rebalance"},
                ],
                "summary": {"selected_moves": 2},
                "safety": {},
            }
            calls = []

            def fail_first(ip, egress, reason):
                calls.append(ip)
                return subprocess.CompletedProcess(["v7-user-switch"], 1, stdout="failed")

            planner._run_switch = fail_first
            planner._validate_atomic_execution_envelope = lambda value: {"ok": True}
            planner._l3_execution_eligibility = lambda value: {"ok": True, "active": False}
            result = planner.apply(plan)

        self.assertEqual(calls, ["10.0.0.2"])
        self.assertTrue(result["remaining_forward_mutations_stopped"])
        self.assertEqual(result["cohort_circuit_breaker"]["remaining_not_attempted"], 1)
        self.assertEqual(result["results"][0]["terminal_outcome_classification"], "APPLY_FAILURE")
        checkpoint = result["bounded_cohort_transaction"]
        self.assertEqual(checkpoint["state"], "CONTAINED_STOP_SAFE")
        self.assertEqual(checkpoint["failed_or_contained"], ["10.0.0.2"])
        self.assertEqual(checkpoint["unapplied"], ["10.0.0.3"])
        self.assertEqual(len(checkpoint["subreceipts"]), 1)

    def test_bounded_cohort_checkpoint_blocks_duplicate_forward_apply_after_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=2)
            args = self.args_for(root, ["--apply", "--max-selected-moves", "2", "--no-verify"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {"operation_id": "op-restart", "selected_move_hash": "hash-restart"},
                "selected_moves": [
                    {"user_ip": "10.0.0.2", "current_egress": "1", "recommended_egress": "vless", "move_type": "rebalance"},
                    {"user_ip": "10.0.0.3", "current_egress": "1", "recommended_egress": "vless", "move_type": "rebalance"},
                ],
                "summary": {"selected_moves": 2},
                "safety": {},
            }
            calls = []

            def fail_first(ip, egress, reason):
                calls.append(ip)
                return subprocess.CompletedProcess(["v7-user-switch"], 1, stdout="failed")

            planner._run_switch = fail_first
            planner._validate_atomic_execution_envelope = lambda value: {"ok": True}
            planner._l3_execution_eligibility = lambda value: {"ok": True, "active": False}
            first = planner.apply(plan)
            second = planner.apply(plan)

        self.assertEqual(calls, ["10.0.0.2"])
        self.assertEqual(first["bounded_cohort_transaction"]["state"], "CONTAINED_STOP_SAFE")
        self.assertFalse(second["applied"])
        self.assertEqual(
            second["reason"],
            "bounded_cohort_restart_recovery_checkpoint_requires_causal_closure",
        )
        self.assertEqual(
            second["bounded_cohort_transaction"]["cohort_fingerprint"],
            first["bounded_cohort_transaction"]["cohort_fingerprint"],
        )

    def test_bounded_cohort_transaction_records_48_member_success_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=48)
            args = self.args_for(root, ["--apply", "--max-selected-moves", "48"])
            planner = self.tool.AutoswitchPlanner(args)
            selected = [
                {
                    "user_ip": f"10.0.0.{index + 2}",
                    "current_egress": "1",
                    "recommended_egress": "vless",
                    "move_type": "rebalance",
                    "selected_move_index": index,
                }
                for index in range(48)
            ]
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {"operation_id": "op-tier48", "selected_move_hash": "hash-tier48"},
                "selected_moves": selected,
                "summary": {"selected_moves": 48},
                "safety": {},
            }
            calls = []
            planner._run_switch = lambda ip, egress, reason: (
                calls.append(ip)
                or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok")
            )
            planner._verify_routes_for_apply = lambda *_args: subprocess.CompletedProcess(
                ["verify"], 0, stdout="ok",
            )
            planner._validate_atomic_execution_envelope = lambda value: {"ok": True}
            planner._l3_execution_eligibility = lambda value: {"ok": True, "active": False}
            result = planner.apply(plan)

        self.assertEqual(len(calls), 48)
        checkpoint = result["bounded_cohort_transaction"]
        self.assertEqual(checkpoint["state"], "SUCCESS")
        self.assertEqual(checkpoint["member_count"], 48)
        self.assertEqual(len(checkpoint["subreceipts"]), 48)
        self.assertEqual(len(checkpoint["applied_successfully"]), 48)
        self.assertEqual(checkpoint["failed_or_contained"], [])
        self.assertEqual(checkpoint["unapplied"], [])

    def test_bounded_cohort_transaction_contains_midstream_failure_at_tier48(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=48)
            args = self.args_for(root, ["--apply", "--max-selected-moves", "48"])
            planner = self.tool.AutoswitchPlanner(args)
            selected = [
                {
                    "user_ip": f"10.0.0.{index + 2}",
                    "current_egress": "1",
                    "recommended_egress": "vless",
                    "move_type": "rebalance",
                    "selected_move_index": index,
                }
                for index in range(48)
            ]
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {
                    "operation_id": "op-tier48-partial",
                    "selected_move_hash": "hash-tier48-partial",
                },
                "selected_moves": selected,
                "summary": {"selected_moves": 48},
                "safety": {},
            }
            calls = []

            def fail_at_twenty_five(ip, egress, reason):
                calls.append(ip)
                return subprocess.CompletedProcess(
                    ["v7-user-switch"],
                    1 if len(calls) == 25 else 0,
                    stdout="failed" if len(calls) == 25 else "ok",
                )

            planner._run_switch = fail_at_twenty_five
            planner._verify_routes_for_apply = lambda *_args: subprocess.CompletedProcess(
                ["verify"], 0, stdout="ok",
            )
            planner._validate_atomic_execution_envelope = lambda value: {"ok": True}
            planner._l3_execution_eligibility = lambda value: {"ok": True, "active": False}
            result = planner.apply(plan)

        self.assertEqual(len(calls), 25)
        checkpoint = result["bounded_cohort_transaction"]
        self.assertEqual(checkpoint["state"], "CONTAINED_STOP_SAFE")
        self.assertEqual(len(checkpoint["subreceipts"]), 25)
        self.assertEqual(len(checkpoint["applied_successfully"]), 24)
        self.assertEqual(checkpoint["failed_or_contained"], ["10.0.0.26"])
        self.assertEqual(len(checkpoint["unapplied"]), 23)
        self.assertTrue(result["remaining_forward_mutations_stopped"])
        self.assertEqual(result["cohort_circuit_breaker"]["remaining_not_attempted"], 23)

    def test_execution_control_open_denies_authority_promotion_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            args = self.args_for(root, ["--promote-authority-to", "SMALL_BATCH"])
            Path(args.execution_control_file).write_text(
                json.dumps(self.tool.operator_execution.build_autonomous_execution_control_state(True, actor="owner", reason="stop")),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(args)
            before = Path(args.policy_file).read_bytes()
            result = planner.promote_authority("SMALL_BATCH")
            after = Path(args.policy_file).read_bytes()

        self.assertIn("autonomous_execution_control_denied", result["blockers"])
        self.assertEqual(before, after)

    def test_scoped_post_apply_route_verification_uses_expected_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="1")
            (root / "state" / "user-10.0.0.2.assign").write_text("egress=vless\n", encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(self.args_for(root))

            def fake_run(cmd, **kwargs):
                if cmd[:3] == ["ip", "rule", "show"]:
                    return subprocess.CompletedProcess(
                        cmd, 0, stdout="100: from 10.0.0.2 lookup 100\n"
                    )
                if cmd[:4] == ["ip", "route", "show", "table"]:
                    return subprocess.CompletedProcess(cmd, 0, stdout="default dev tun0 scope link\n")
                if cmd[:4] == ["ip", "route", "get", "8.8.8.8"]:
                    return subprocess.CompletedProcess(
                        cmd,
                        0,
                        stdout="8.8.8.8 from 10.0.0.2 dev tun0 table 100\n    cache iif wg0\n",
                    )
                return subprocess.CompletedProcess(cmd, 1, stdout="unexpected command\n")

            with mock.patch.object(self.tool.subprocess, "run", side_effect=fake_run):
                result = planner._verify_user_route("10.0.0.2", expected_egress="vless")

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("REGISTRY_EGRESS=1", result.stdout)
        self.assertIn("ASSIGN_EGRESS=vless", result.stdout)
        self.assertIn("EXPECTED_EGRESS=vless", result.stdout)
        self.assertIn("policy rule selects table 100", result.stdout)
        self.assertIn("V7_SCOPED_USER_ROUTE_CHECK=OK", result.stdout)

    def test_scoped_route_verification_emits_safe_failure_categories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="1")
            planner = self.tool.AutoswitchPlanner(self.args_for(root))

            def fake_run(cmd, **kwargs):
                if cmd[:3] == ["ip", "rule", "show"]:
                    return subprocess.CompletedProcess(cmd, 0, stdout="")
                if cmd[:4] == ["ip", "route", "show", "table"]:
                    return subprocess.CompletedProcess(cmd, 0, stdout="default dev wrong0\n")
                if cmd[:4] == ["ip", "route", "get", "8.8.8.8"]:
                    return subprocess.CompletedProcess(cmd, 0, stdout="8.8.8.8 dev ens3\n")
                return subprocess.CompletedProcess(cmd, 1, stdout="unexpected command\n")

            with mock.patch.object(self.tool.subprocess, "run", side_effect=fake_run):
                result = planner._verify_user_route("10.0.0.2", expected_egress="vless")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "V7_SCOPED_USER_ROUTE_FAILURE_CATEGORIES=POLICY_RULE_MISSING,ROUTE_GET_PUBLIC_LEAK,TABLE_DEFAULT_MISMATCH",
            result.stdout,
        )

    def test_ct_m0f_cutover_consumer_fails_before_probe_without_full_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="1")
            args = self.args_for(root)
            args.ct_m0f_kernel_cutover_validation = True
            args.ct_m0f_validation_generation_id = ""
            args.ct_m0f_sample_kind = "warm"
            args.approved_packet_id = ""
            args.approved_execution_lease_id = ""
            args.approved_operation_id = ""
            planner = self.tool.AutoswitchPlanner(args)
            move = {
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "vless",
            }
            with mock.patch.object(self.tool.subprocess, "run") as run:
                result = planner._ct_m0f_kernel_cutover_evidence(
                    {"operation": {}, "safety": {}},
                    move,
                    {"verify_rc": 0, "service_verify_rc": 0},
                )
            run.assert_not_called()
        self.assertEqual(
            result["status"], "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID"
        )
        self.assertIn("packet_id_missing", result["blockers"])
        self.assertIn("lease_id_missing", result["blockers"])

    def test_ct_m0f_apply_emits_exact_evidence_on_route_verification_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="1")
            args = self.args_for(
                root,
                [
                    "--apply",
                    "--verify",
                    "--rollback-on-verify-fail",
                    "--ct-m0f-kernel-cutover-validation",
                    "--max-selected-moves",
                    "1",
                ],
            )
            planner = self.tool.AutoswitchPlanner(args)
            plan = {
                "enabled": True,
                "mode": "guarded",
                "operation": {
                    "operation_id": "op-ct-m0f-route-failure",
                    "selected_move_hash": "hash-ct-m0f-route-failure",
                },
                "selected_moves": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "1",
                    "recommended_egress": "vless",
                    "move_type": "failover",
                }],
                "summary": {"selected_moves": 1},
                "safety": {},
            }
            planner._validate_atomic_execution_envelope = lambda _plan: {"ok": True}
            planner._l3_execution_eligibility = lambda _plan: {
                "ok": True,
                "active": False,
            }
            planner._run_switch = lambda *_args: subprocess.CompletedProcess(
                ["v7-user-switch"], 0, stdout="ok\n"
            )
            planner._verify_routes_for_apply = lambda *_args: subprocess.CompletedProcess(
                ["v7-user-route-check"], 1, stdout="route failed\n"
            )
            planner._ct_m0f_kernel_cutover_evidence = mock.Mock(
                return_value={
                    "status": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID",
                    "ok": False,
                    "blockers": ["exact_user_route_verification_required"],
                }
            )

            result = planner.apply(plan)

        evidence = result["results"][0]["ct_m0f_kernel_cutover_evidence"]
        self.assertFalse(evidence["ok"])
        self.assertEqual(
            evidence["blockers"],
            ["exact_user_route_verification_required"],
        )
        planner._ct_m0f_kernel_cutover_evidence.assert_called_once()

    def test_ct_m0f_cutover_reuses_controlled_condition_and_nested_registry_ip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                current_egress="1",
                vless_registry_extra=" expected_ip=77.110.103.131",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                users_path.read_text(encoding="utf-8").strip()
                + " certification_user=1\n",
                encoding="utf-8",
            )
            audit = root / "audit.jsonl"
            contract_id = "ctm0fsdpc_test"
            contract_hash = "c" * 64
            condition = self.tool.operator_execution.append_record(
                audit,
                {
                    "record_type": (
                        "ct_m0f_standing_controlled_condition_prepared"
                    ),
                    "contract_id": contract_id,
                    "contract_hash": contract_hash,
                    "user": "10.0.0.2",
                    "source": "1",
                    "baseline_target": "vless",
                    "first_failed_observation_monotonic_ns": 100,
                    "confirmed_hard_failure_monotonic_ns": 100,
                },
            )
            args = self.args_for(root)
            args.action_class_audit_store = str(audit)
            args.ct_m0f_kernel_cutover_validation = True
            args.ct_m0f_validation_generation_id = "ctm0fgen_test"
            args.ct_m0f_sample_kind = "cold"
            args.ct_m0f_standing_validation_contract_id = contract_id
            args.ct_m0f_standing_validation_contract_hash = contract_hash
            args.ct_m0f_implementation_fingerprint = "i" * 64
            args.approved_packet_id = "pkt_test"
            args.approved_execution_lease_id = "lease_test"
            args.approved_operation_id = "operation_test"
            args.ct_m0f_first_failed_observation_monotonic_ns = 90
            args.ct_m0f_confirmed_hard_failure_monotonic_ns = 95
            planner = self.tool.AutoswitchPlanner(args)
            move = {
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "vless",
            }
            consumed_receipt = {}

            def consume_receipt(receipt):
                consumed_receipt.update(receipt)
                return {
                    "status": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS",
                    "ok": True,
                    "incident_id": receipt["incident_id"],
                    "incident_generation": receipt["incident_generation"],
                }

            def fake_run(command, **_kwargs):
                if command[:4] == ["ip", "-j", "addr", "show"]:
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        stdout=json.dumps([{
                            "addr_info": [{
                                "family": "inet",
                                "local": "172.19.0.1",
                            }],
                        }]),
                    )
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout=json.dumps({
                        "status": "TARGET_EGRESS_PAYLOAD_PASS",
                        "receipt_id": "payload_receipt",
                        "target_egress_payload_pass_monotonic_ns": 200,
                    }),
                )

            with mock.patch.object(
                self.tool.operator_execution,
                "validate_ct_m0f_standing_validation_sample_reservation",
                return_value={"ok": True, "errors": []},
            ), mock.patch.object(
                self.tool.subprocess,
                "run",
                side_effect=fake_run,
            ), mock.patch.object(
                self.tool.operator_execution_pipeline,
                "control_plane_kernel_path_cutover_contract",
                side_effect=consume_receipt,
            ):
                result = planner._ct_m0f_kernel_cutover_evidence(
                    {"operation": {}, "safety": {"l3_incident": {
                        "incident_id": "matrix_incident_shell",
                        "incident_generation": "matrix_generation_shell",
                        "first_failed_observation_monotonic_ns": 0,
                        "confirmed_hard_failure_monotonic_ns": 0,
                    }}},
                    move,
                    {
                        "verify_rc": 0,
                        "service_verify_rc": 0,
                        "verify_output": (
                            "policy_rule_fingerprint=" + "a" * 64
                            + "\nV7_SCOPED_USER_ROUTE_CHECK=OK\n"
                        ),
                        "route_writer_timing": {
                            "completed_monotonic_ns": 150,
                        },
                        "route_visibility_timing": {
                            "completed_monotonic_ns": 175,
                        },
                    },
                )

        self.assertTrue(result["ok"])
        self.assertEqual(result["incident_id"], "matrix_incident_shell")
        self.assertEqual(result["incident_generation"], "matrix_generation_shell")
        self.assertEqual(consumed_receipt["first_failed_observation_monotonic_ns"], 90)
        self.assertEqual(consumed_receipt["confirmed_hard_failure_monotonic_ns"], 95)

    def test_ct_m0f_invalid_evidence_preserves_safe_route_failure_categories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="1")
            args = self.args_for(root)
            args.ct_m0f_kernel_cutover_validation = True
            args.ct_m0f_validation_generation_id = "ctm0fgen_test"
            args.ct_m0f_standing_validation_contract_id = "ctm0fsdpc_test"
            args.ct_m0f_standing_validation_contract_hash = "c" * 64
            args.ct_m0f_implementation_fingerprint = "i" * 64
            args.approved_packet_id = "pkt_test"
            args.approved_execution_lease_id = "lease_test"
            args.approved_operation_id = "operation_test"
            planner = self.tool.AutoswitchPlanner(args)
            move = {
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "vless",
            }
            with mock.patch.object(
                self.tool.operator_execution,
                "validate_ct_m0f_standing_validation_sample_reservation",
                return_value={"ok": True, "errors": []},
            ):
                result = planner._ct_m0f_kernel_cutover_evidence(
                    {"operation": {}, "safety": {}},
                    move,
                    {
                        "verify_rc": 1,
                        "route_verification_scope": "selected_user",
                        "route_verification_expected_egress": "vless",
                        "route_verification_failure_categories": [
                            "TABLE_DEFAULT_MISMATCH",
                            "unsafe text is dropped",
                        ],
                    },
                )

        self.assertFalse(result["ok"])
        self.assertEqual(
            result["route_verification_failure_categories"],
            ["TABLE_DEFAULT_MISMATCH"],
        )
        self.assertEqual(result["route_verification_scope"], "selected_user")
        self.assertEqual(result["route_verification_expected_egress"], "vless")

    def test_ct_m0f_target_identity_reuses_single_declared_tunnel_endpoint(self):
        target = self.tool.Egress(
            id="controlled-target",
            interface="v7execwg0",
            raw={
                "registry": {
                    "protocol": "amneziawg",
                    "config": "/etc/amnezia/v7execwg0.conf",
                }
            },
        )
        with mock.patch.object(
            self.tool.Path,
            "read_text",
            return_value="[Peer]\nEndpoint = 8.8.8.8:34403\n",
        ):
            expected_ip, source = self.tool.declared_target_egress_ip(target)

        self.assertEqual(expected_ip, "8.8.8.8")
        self.assertEqual(source, "tunnel_endpoint_expected_ip")

        non_tunnel = self.tool.Egress(
            id="proxy-target",
            raw={"registry": {"protocol": "vless", "config": "/etc/amnezia/x.conf"}},
        )
        self.assertEqual(
            self.tool.declared_target_egress_ip(non_tunnel),
            ("", "no_declared_target_egress_identity"),
        )

    def write_intelligence_snapshots(self, root: Path, *, ctr_channels: Optional[list[dict]] = None) -> Path:
        snapshot_root = root / "state" / "intelligence"
        snapshot_root.mkdir(parents=True, exist_ok=True)
        generated_at = "2999-01-01T00:00:00+00:00"
        contents = {
            "service-scores": [],
            "channel-service-scores": [
                {"channel": "1", "aggregate_score": 82, "confidence": 0.9, "verdict": "OK"},
                {"channel": "vless", "aggregate_score": 78, "confidence": 0.9, "verdict": "OK"},
            ],
            "user-service-scores": [],
            "risk-summaries": [{"risk_score": 0, "average_service_score": 80, "average_channel_score": 80}],
            "trust-summaries": [{"trust": {"score": 80}, "trust_score": 80}],
            "blast-radius-summaries": [{"recommendation": {"recommended_budget": 1}}],
            "candidate-suitability-summary": [],
            "best-available-pool": [],
            "prediction-summaries": [],
            "trust-evolution-summaries": [
                {
                    "channel_trust_recovery": {
                        "channels": ctr_channels or [],
                    }
                }
            ],
        }
        for family, content in contents.items():
            payload = build_snapshot_envelope(
                family,
                generated_at=generated_at,
                confidence=0.95,
                source_hashes={},
                generator="unit-test",
                item_count=len(content) if isinstance(content, list) else 1,
                content=content,
            )
            snapshot_path(snapshot_root, family).write_text(json.dumps(payload), encoding="utf-8")
        return snapshot_root

    def write_feedback_records(
        self,
        root: Path,
        operation_id: str,
        users: list[str],
        *,
        omit: Optional[set[str]] = None,
        rollback_required: bool = False,
        stability_window_seconds: int = 0,
        created_at: str = "",
    ) -> None:
        state = root / "state"
        omit = omit or set()
        outcome_rows = []
        prediction_rows = []
        trust_rows = []
        recommendation_rows = []
        closure_rows = []
        for user in users:
            feedback_id = f"execfb_{operation_id[-8:]}_{user.replace('.', '')}"
            base = {
                "feedback_id": feedback_id,
                "user": user,
                "source_channel": "awg3",
                "target_channel": "vless",
                "outcome_status": "success",
                "audit_reference": operation_id,
                "closure_reference": "VERIFIED_READY",
                "stability_window_seconds": stability_window_seconds,
            }
            if created_at:
                base["created_at"] = created_at
            if "outcome" not in omit:
                outcome_rows.append(
                    {
                        "schema_version": "v7.execution-outcome-record.v1",
                        **base,
                        "execution_outcome": {"operation_id": operation_id, "terminal_state": "APPLIED"},
                        "verification_result": {"operation_id": operation_id, "success": True},
                        "rollback_result": {"rollback_required": rollback_required},
                    }
                )
            if "prediction" not in omit:
                prediction_rows.append(
                    {
                        "schema_version": "v7.execution-prediction-feedback.v1",
                        **base,
                        "prediction_expected": 0.8,
                        "prediction_actual": 0.82,
                        "delta": 0.98,
                    }
                )
            if "trust" not in omit:
                trust_rows.append(
                    {
                        "schema_version": "v7.execution-trust-feedback.v1",
                        **base,
                        "subject": "vless",
                        "delta": 1.0,
                        "reason": "success",
                    }
                )
            if "recommendation" not in omit:
                recommendation_rows.append(
                    {
                        "schema_version": "v7.execution-recommendation-feedback.v1",
                        **base,
                        "recommendation_hash": f"rec-{operation_id}-{user}",
                        "delta": 1.0,
                        "outcome": "success",
                    }
                )
            if "closure" not in omit:
                closure_rows.append(
                    {
                        "schema_version": "v7.execution-feedback-closure.v1",
                        **base,
                        "object_type": "execution_feedback",
                        "object_id": feedback_id,
                        "closure_state": "CLOSED",
                        "closure_reason": "execution feedback materialized: success",
                    }
                )
        if outcome_rows or prediction_rows:
            with (state / "execution-events.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(
                    "\n".join(json.dumps(row) for row in outcome_rows + prediction_rows) + "\n"
                )
        if trust_rows:
            with (state / "runtime-trust.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(
                    "\n".join(json.dumps(row) for row in trust_rows) + "\n"
                )
        if recommendation_rows:
            with (state / "proposal-records.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(
                    "\n".join(json.dumps(row) for row in recommendation_rows) + "\n"
                )
        if closure_rows:
            with (state / "closure-records.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(
                    "\n".join(json.dumps(row) for row in closure_rows) + "\n"
                )
        return

    def write_authority_test_binaries(self, root: Path, *, truth_pass: bool = True, audit_pass: bool = True) -> tuple[Path, Path, Path]:
        bin_dir = root / "bin"
        bin_dir.mkdir()
        truth = bin_dir / "truth-check"
        if truth_pass:
            truth.write_text('#!/bin/sh\nprintf \'{"status":"PASS","alignment":"FULLY_ALIGNED"}\\n\'\n', encoding="utf-8")
        else:
            truth.write_text('#!/bin/sh\nprintf \'{"status":"FAIL"}\\n\'\nexit 1\n', encoding="utf-8")
        truth.chmod(0o755)
        audit = bin_dir / "v7-audit-log"
        audit.write_text("#!/bin/sh\nexit 0\n" if audit_pass else "#!/bin/sh\nexit 1\n", encoding="utf-8")
        audit.chmod(0o755)
        return bin_dir, truth, audit

    def write_balanced_pool_users(self, root: Path, *, users_on_one: int = 13, users_on_vless: int = 12) -> None:
        rows = []
        table = 100
        for idx in range(users_on_one):
            rows.append(f"ip=10.0.0.{idx + 2} current=1 table={table} enabled=1")
            table += 1
        for idx in range(users_on_vless):
            rows.append(f"ip=10.0.1.{idx + 2} current=vless table={table} enabled=1")
            table += 1
        (root / "state" / "users.registry").write_text("\n".join(rows) + "\n", encoding="utf-8")

    def apply_plan_with_mocks(self, root: Path) -> tuple[dict, list[tuple[str, str, str]]]:
        args = self.args_for(root, ["--apply"])
        planner = self.tool.AutoswitchPlanner(args)
        plan = planner.plan()
        switch_calls = []

        def fake_run_switch(ip: str, egress: str, reason: str):
            switch_calls.append((ip, egress, reason))
            return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

        def fake_verify_routes():
            return subprocess.CompletedProcess(["v7-user-route-check"], 1, stdout="verify failed\n")

        def fake_emit_terminal_audit(audit: dict) -> dict:
            audit["emitted"] = True
            audit["status"] = "emitted"
            audit["output"] = "mock audit emission"
            return audit

        planner._run_switch = fake_run_switch
        planner._verify_routes = fake_verify_routes
        planner._emit_terminal_audit = fake_emit_terminal_audit
        plan["apply_result"] = planner.apply(plan)
        planner.finalize_operation(plan)
        return plan, switch_calls

    def governed_source_bundle_lease_plan(
        self,
        root: Path,
        *,
        users: int = 2,
        max_selected_moves: int = 2,
        allowed_users: Optional[list[str]] = None,
        clearance_expires_at: str = "2999-01-01T00:00:00+00:00",
    ):
        self.write_fixture(
            root,
            users=users,
            egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            restore_barrier={
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "reason": "unit-test-source-bundle-lease-bootstrap",
            },
            authority_budget={
                "authority_class": "SMALL_BATCH",
                "certified_authority_class": "CANARY",
                "authority_lifecycle_state": "CANARY_EXPANSION",
                "current_allowed_user_budget": 2,
                "next_allowed_user_budget": 2,
            },
        )
        bootstrap_args = self.args_for(
            root,
            ["--apply", "--target-egress", "vless", "--max-selected-moves", str(max_selected_moves)],
        )
        bootstrap_planner = self.tool.AutoswitchPlanner(bootstrap_args)
        bootstrap = bootstrap_planner.plan()
        envelope = bootstrap["safety"]["atomic_execution_envelope"]
        selected_hash = bootstrap["operation"]["selected_move_hash"]
        selected_users = [move["user_ip"] for move in bootstrap["selected_moves"]]
        approved = {
            "enabled": True,
            "expires_at": "2000-01-01T00:00:00+00:00",
            "generation_clearance": True,
            "clearance_max_selected_moves": max_selected_moves,
            "generation_token": "unit-test-source-bundle-lease-token",
            "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
            "approved_selected_moves_hash": selected_hash,
            "clearance_expected_selected_moves": len(bootstrap["selected_moves"]),
            "clearance_expires_at": clearance_expires_at,
            "allowed_users": allowed_users if allowed_users is not None else selected_users,
            "allowed_targets": ["vless"],
            "approved_atomic_execution_envelope_id": envelope["envelope_id"],
            "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
            "approved_source_bundle_hash": envelope["source_bundle_hash"],
            "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
            "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
            "owner": "admin_core/operator_execution.py",
        }
        (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
        refresh_script = root / "refresh-ok"
        refresh_script.write_text("#!/bin/sh\nprintf '{\"source_stable\": true, \"snapshot_count\": 6}\\n'\n", encoding="utf-8")
        refresh_script.chmod(0o755)
        args = self.args_for(
            root,
            [
                "--apply",
                "--mode",
                "guarded",
                "--target-egress",
                "vless",
                "--max-selected-moves",
                str(max_selected_moves),
                "--pre-planner-refresh",
                "write",
                "--pre-planner-refresh-command",
                str(refresh_script),
                "--allow-pre-planner-refresh-with-apply",
            ],
        )
        planner = self.tool.AutoswitchPlanner(args)
        plan = planner.plan()
        switch_calls = []

        def fake_run_switch(ip: str, egress: str, reason: str):
            switch_calls.append((ip, egress, reason))
            return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

        def fake_verify_routes():
            return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

        planner._run_switch = fake_run_switch
        planner._verify_routes = fake_verify_routes
        return planner, plan, switch_calls

    def expected_selected_move_hash(self, selected: list[dict]) -> str:
        normalized = [
            {
                "user_ip": str(move.get("user_ip") or ""),
                "from": str(move.get("current_egress") or ""),
                "to": str(move.get("recommended_egress") or ""),
                "move_type": str(move.get("move_type") or ""),
            }
            for move in selected
        ]
        return self.tool.sha256_json(normalized)

    def approved_plan_lock_from_plan(self, plan: dict, *, expires_at: str = "2999-01-01T00:00:00+00:00") -> dict:
        selected = plan["selected_moves"]
        envelope = plan["safety"]["atomic_execution_envelope"]
        return {
            "schema_version": "v7.approved-plan-lock.v1",
            "lock_id": "apl-unit-test",
            "lock_hash": "lock-hash-unit-test",
            "planner_generation_id": plan["safety"]["generation"]["planner_generation_id"],
            "selected_move_hash": plan["operation"]["selected_move_hash"],
            "selected_move_count": len(selected),
            "selected_moves": [
                {
                    **{
                        "user_ip": move["user_ip"],
                        "current_egress": move["current_egress"],
                        "recommended_egress": move["recommended_egress"],
                        "move_type": move.get("move_type", "failover"),
                    },
                    **{
                        key: move[key]
                        for key in ("reason", "important_services", "candidates", "scores", "service_failover")
                        if key in move
                    },
                }
                for move in selected
            ],
            "allowed_users": [move["user_ip"] for move in selected],
            "allowed_targets": sorted({move["recommended_egress"] for move in selected}),
            "atomic_execution_envelope_id": envelope["envelope_id"],
            "atomic_execution_envelope_hash": envelope["envelope_hash"],
            "source_bundle_hash": envelope["source_bundle_hash"],
            "source_hashes": envelope["source_bundle"]["source_hashes"],
            "snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
            "packet_id": "pkt-unit-test",
            "packet_hash": "packet-hash-unit-test",
            "restore_barrier_id": "restore-barrier-unit-test",
            "restore_barrier_hash": "restore-barrier-hash-unit-test",
            "expires_at": expires_at,
            "owner": "admin_core/operator_execution.py",
            "executor_may_reselect": False,
            "executor_may_replace_users": False,
            "executor_may_replace_targets": False,
        }

    def approved_restore_barrier_from_plan(
        self,
        plan: dict,
        *,
        max_selected_moves: Optional[int] = None,
        expires_at: str = "2999-01-01T00:00:00+00:00",
    ) -> dict:
        selected = plan["selected_moves"]
        envelope = plan["safety"]["atomic_execution_envelope"]
        max_moves = len(selected) if max_selected_moves is None else max_selected_moves
        lock = self.approved_plan_lock_from_plan(plan, expires_at=expires_at)
        lock["identity_source"] = "approved_preview_packet"
        return {
            "enabled": True,
            "expires_at": "2000-01-01T00:00:00+00:00",
            "allow_post_ttl_apply": True,
            "generation_clearance": True,
            "clearance_max_selected_moves": max_moves,
            "generation_token": "unit-test-l3-production-validation-token",
            "clearance_generation_id": plan["safety"]["generation"]["planner_generation_id"],
            "approved_selected_moves_hash": plan["operation"]["selected_move_hash"],
            "clearance_expected_selected_moves": len(selected),
            "clearance_expires_at": expires_at,
            "allowed_users": [move["user_ip"] for move in selected],
            "allowed_targets": sorted({move["recommended_egress"] for move in selected}),
            "approved_atomic_execution_envelope_id": envelope["envelope_id"],
            "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
            "approved_source_bundle_hash": envelope["source_bundle_hash"],
            "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
            "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
            "approved_plan_lock": lock,
            "owner": "admin_core/operator_execution.py",
        }

    def prepare_l3_validation_envelope(self, root: Path, *, users: int = 1) -> dict:
        fresh = "2999-01-01T00:00:00+00:00"
        authority_budget = None
        if users > 1:
            authority_budget = {
                "authority_class": "SMALL_BATCH",
                "certified_authority_class": "CANARY",
                "authority_lifecycle_state": "CANARY_EXPANSION",
                "current_allowed_user_budget": users,
            }
        self.write_fixture(
            root,
            users=users,
            egress_1_services={
                "telegram": {
                    "ok": False,
                    "status": "DOWN",
                    "score": 0,
                    "consecutive_failures": 3,
                    "tested_at": fresh,
                }
            },
            authority_budget=authority_budget,
        )
        bootstrap_args = self.args_for(
            root,
            [
                "--apply",
                "--mode",
                "guarded",
                "--target-egress",
                "vless",
                "--max-selected-moves",
                str(users),
            ],
        )
        bootstrap_planner = self.tool.AutoswitchPlanner(bootstrap_args)
        bootstrap = bootstrap_planner.plan()
        barrier = self.approved_restore_barrier_from_plan(bootstrap)
        (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(barrier), encoding="utf-8")
        policy_path = root / "policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        policy["emergency_failover_autonomy"] = {
            "enabled": True,
            "max_users_per_run": 1,
            "max_users_per_channel": 1,
        }
        policy_path.write_text(json.dumps(policy), encoding="utf-8")
        return bootstrap

    def _set_emergency_wake_source(self, root: Path, source: str) -> None:
        policy_path = root / "policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        policy.setdefault("emergency_failover_autonomy", {})["wake_source"] = source
        policy_path.write_text(json.dumps(policy), encoding="utf-8")

    def mark_current_channel_failed(self, root: Path, *, egress: str = "1") -> None:
        state_path = root / "state" / "v7-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.setdefault("egress", {}).setdefault(egress, {}).update(
            {
                "avg_mbps": 0,
                "min_mbps": 0,
                "stability": 0,
                "code": "000",
                "diagnose_severity": "FAIL",
                "diagnose_reason": "interface_down_or_missing",
                "diagnose_detail": "protocol=openvpn",
            }
        )
        state_path.write_text(json.dumps(state), encoding="utf-8")

    def add_failed_egress(self, root: Path, *, egress: str = "2") -> None:
        registry_path = root / "state" / "egress.registry"
        registry = registry_path.read_text(encoding="utf-8")
        registry_path.write_text(
            registry + f"id={egress} interface=v7two enabled=1 state=enabled role=GLOBAL_FAST\n",
            encoding="utf-8",
        )
        state_path = root / "state" / "v7-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.setdefault("egress", {})[egress] = {
            "avg_mbps": 0,
            "min_mbps": 0,
            "stability": 0,
            "code": "000",
            "diagnose_severity": "FAIL",
            "diagnose_reason": "interface_down_or_missing",
        }
        state_path.write_text(json.dumps(state), encoding="utf-8")
        matrix_path = root / "state" / "service-matrix.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        matrix.setdefault("items", {})[egress] = {
            "services": {
                "youtube": {"ok": True, "score": 100},
                "instagram": {"ok": True, "score": 100},
                "telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": "2999-01-01T00:00:00+00:00"},
                "google": {"ok": True, "score": 100},
                "google_auth": {"ok": True, "score": 100},
            },
            "route_class_fitness": {
                "VIDEO_OPTIMIZED": {"status": "FAIL"},
                "GLOBAL_STABLE": {"status": "FAIL"},
                "GLOBAL_FAST": {"status": "FAIL"},
            },
        }
        matrix_path.write_text(json.dumps(matrix), encoding="utf-8")

    def assert_operation_envelope(self, plan: dict) -> None:
        for key in ("schema_version", "summary", "safety", "decisions", "selected_moves"):
            self.assertIn(key, plan)
        operation = plan.get("operation")
        self.assertIsInstance(operation, dict)
        self.assertTrue(operation.get("operation_id", "").startswith("runtime_autoswitch_"))
        self.assertEqual(operation["operation_owner"], "tools/v7-users-autoswitch")
        self.assertEqual(operation["operation_type"], "runtime_autoswitch")
        self.assertTrue(operation.get("operation_started_at"))
        self.assertEqual(
            operation["planner_generation_id"],
            plan["safety"]["generation"]["planner_generation_id"],
        )
        self.assertEqual(operation["selected_move_hash"], self.expected_selected_move_hash(plan["selected_moves"]))
        self.assertEqual(operation["selected_move_count"], len(plan["selected_moves"]))
        self.assertEqual(operation["selected_move_count"], plan["summary"]["selected_moves"])
        self.assertTrue(operation.get("runtime_snapshot_hash"))
        self.assertIn("terminal_state", operation)
        self.assertIn("terminal_reason", operation)
        audit = plan.get("audit")
        self.assertIsInstance(audit, dict)
        self.assertEqual(audit["action"], "runtime_operation_terminal")
        self.assertEqual(audit["component"], "autoswitch")
        self.assertEqual(audit["object_type"], "runtime_operation")
        self.assertEqual(audit["object_id"], operation["operation_id"])
        self.assertEqual(audit["result"], operation["terminal_state"])
        self.assertEqual(audit["metadata"]["operation_id"], operation["operation_id"])
        self.assertEqual(audit["metadata"]["selected_move_hash"], operation["selected_move_hash"])
        self.assertEqual(audit["metadata"]["runtime_snapshot_hash"], operation["runtime_snapshot_hash"])
        envelope = plan["safety"].get("atomic_execution_envelope")
        self.assertIsInstance(envelope, dict)
        self.assertEqual(envelope["schema_version"], "v7.atomic-execution-envelope.v1")
        self.assertEqual(operation["atomic_execution_envelope_id"], envelope["envelope_id"])
        self.assertEqual(operation["atomic_execution_envelope_hash"], envelope["envelope_hash"])
        self.assertEqual(envelope["selected_move_hash"], operation["selected_move_hash"])
        self.assertEqual(envelope["selected_move_count"], operation["selected_move_count"])
        self.assertIn(envelope["state"]["condition"], {"ENVELOPE_VALID", "ENVELOPE_STALE", "SOURCE_CHANGED"})
        if not plan["apply_requested"]:
            self.assertFalse(audit["emitted"])
            self.assertEqual(audit["status"], "ready_not_emitted_dry_run")
        closure = plan.get("closure_target")
        self.assertIsInstance(closure, dict)
        self.assertEqual(closure["object_type"], "runtime")
        self.assertEqual(closure["object_id"], operation["operation_id"])
        self.assertEqual(closure["closure_owner"], "admin/v7-admin-api")
        self.assertEqual(closure["observability_owner"], "admin_core/operator_observability.py")
        if not audit["emitted"]:
            self.assertEqual(closure["closure_state"], "OPEN")
            self.assertEqual(closure["closure_blocker"], "audit_missing")

    def test_ctr_advisory_is_visible_without_changing_candidate_score_or_selected_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=1)
            snapshot_root = self.write_intelligence_snapshots(root, ctr_channels=[])
            baseline_planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--intelligence-snapshot-root", str(snapshot_root)])
            )
            baseline = baseline_planner.plan()

            self.write_intelligence_snapshots(
                root,
                ctr_channels=[
                    {
                        "channel": "vless",
                        "lifecycle": "QUARANTINED",
                        "lifecycle_reason": "hard_negative_feedback_or_service_gap",
                        "trust_score": 22,
                        "current_service_score": 78,
                        "confidence": 0.9,
                        "feedback": {
                            "successes": 0,
                            "failures": 2,
                            "rollback_successes": 0,
                            "rollback_failures": 0,
                        },
                        "recovery": {
                            "state": "BLOCKED",
                            "safe_to_restore_eligibility": False,
                            "operator_review_required": True,
                        },
                    }
                ],
            )
            ctr_planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--intelligence-snapshot-root", str(snapshot_root)])
            )
            with_ctr = ctr_planner.plan()

        baseline_vless = next(row for row in baseline["decisions"][0]["candidates"] if row["egress"] == "vless")
        ctr_vless = next(row for row in with_ctr["decisions"][0]["candidates"] if row["egress"] == "vless")

        self.assertEqual(baseline_vless["score"], ctr_vless["score"])
        self.assertEqual(baseline_vless["score_parts"], ctr_vless["score_parts"])
        self.assertNotIn("ctr", ctr_vless["score_parts"])
        self.assertEqual(baseline["operation"]["selected_move_hash"], with_ctr["operation"]["selected_move_hash"])
        self.assertEqual(baseline["selected_moves"], with_ctr["selected_moves"])

        ctr = ctr_vless["ctr_advisory"]
        self.assertEqual(ctr["state"], "QUARANTINED")
        self.assertEqual(ctr["recommended_action"], "emergency_or_rollback_review_only")
        self.assertFalse(ctr["planner_score_applied"])
        self.assertFalse(ctr["hard_gate_applied"])
        self.assertFalse(ctr["target_suppression_applied"])
        self.assertIn("normal_target_use", ctr["blocked_actions"])
        self.assertEqual(
            with_ctr["routing_brain"]["ctr_advisory"]["pool_soft_influence"],
            "dry_run_score_simulation_only",
        )
        self.assertFalse(with_ctr["routing_brain"]["ctr_advisory"]["planner_score_applied"])
        simulation = ctr_vless["ctr_score_simulation"]
        self.assertEqual(simulation["mode"], "dry_run_simulation_only")
        self.assertEqual(simulation["ctr_soft_adjustment"], -24.0)
        self.assertAlmostEqual(simulation["simulated_score"], simulation["existing_score"] - 24.0, places=3)
        self.assertFalse(simulation["planner_score_applied"])
        self.assertFalse(simulation["planner_ranking_changed"])
        self.assertFalse(simulation["selected_moves_changed"])
        self.assertFalse(simulation["runtime_behavior_changed"])

    def test_ctr_soft_score_simulation_can_detect_ranking_delta_without_runtime_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=1, vless_registry_extra=" weight=170")
            snapshot_root = self.write_intelligence_snapshots(
                root,
                ctr_channels=[
                    {
                        "channel": "1",
                        "lifecycle": "QUARANTINED",
                        "lifecycle_reason": "hard_negative_feedback_or_service_gap",
                        "trust_score": 25,
                        "current_service_score": 82,
                        "confidence": 0.91,
                        "recovery": {
                            "state": "BLOCKED",
                            "safe_to_restore_eligibility": False,
                            "operator_review_required": True,
                        },
                    },
                    {
                        "channel": "vless",
                        "lifecycle": "TRUSTED",
                        "lifecycle_reason": "stable_success_history",
                        "trust_score": 92,
                        "current_service_score": 91,
                        "confidence": 0.94,
                        "recovery": {
                            "state": "HEALTHY",
                            "safe_to_restore_eligibility": True,
                            "operator_review_required": False,
                        },
                    },
                ],
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--intelligence-snapshot-root", str(snapshot_root)])
            )
            plan = planner.plan()

        candidates = plan["decisions"][0]["candidates"]
        current = next(row for row in candidates if row["egress"] == "1")
        vless = next(row for row in candidates if row["egress"] == "vless")

        self.assertGreater(current["score"], vless["score"])
        self.assertEqual(current["ctr_score_simulation"]["ctr_soft_adjustment"], -24.0)
        self.assertEqual(vless["ctr_score_simulation"]["ctr_soft_adjustment"], 20.0)
        self.assertGreater(current["ctr_score_simulation"]["new_position"], current["ctr_score_simulation"]["old_position"])
        self.assertLess(vless["ctr_score_simulation"]["new_position"], vless["ctr_score_simulation"]["old_position"])
        self.assertLess(current["ctr_score_simulation"]["ranking_delta"], 0)
        self.assertGreater(vless["ctr_score_simulation"]["ranking_delta"], 0)
        self.assertFalse(vless["ctr_score_simulation"]["planner_ranking_changed"])
        self.assertFalse(vless["ctr_score_simulation"]["selected_moves_changed"])
        self.assertEqual(plan["routing_brain"]["ctr_advisory"]["simulated_ranking_changes"], 2)
        self.assertTrue(plan["routing_brain"]["ctr_advisory"]["simulated_value_detected"])
        self.assertFalse(plan["apply_requested"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        shadow = plan["ctr_shadow_comparison"]
        self.assertEqual(shadow["mode"], "dry_run_shadow_comparison_only")
        self.assertEqual(shadow["final_verdict"], "CTR_POSITIVE_VALUE")
        self.assertEqual(shadow["statistics"]["total_planner_cycles"], 1)
        self.assertEqual(shadow["statistics"]["cycles_with_ranking_change"], 1)
        self.assertEqual(shadow["statistics"]["top_candidate_changes"], 1)
        self.assertEqual(shadow["statistics"]["top3_changes"], 1)
        self.assertEqual(shadow["statistics"]["decision_quality_improvements"], 1)
        self.assertEqual(shadow["statistics"]["service_improvements"], 0)
        self.assertEqual(shadow["statistics"]["service_regressions"], 0)
        self.assertEqual(shadow["ctr_influence_quality"], "USEFUL")
        self.assertEqual(shadow["readiness_review"]["shadow_scoring"], "READY")
        self.assertEqual(shadow["readiness_review"]["planner_influence"], "NOT_READY")
        self.assertFalse(shadow["no_bypass"]["selected_moves_changed"])
        self.assertFalse(shadow["no_bypass"]["planner_ranking_changed"])
        cycle = shadow["cycles"][0]
        self.assertEqual(cycle["winner_without_ctr"], "1")
        self.assertEqual(cycle["winner_with_ctr"], "vless")
        self.assertFalse(cycle["same_winner"])
        self.assertEqual(cycle["quality_delta"]["verdict"], "improved")
        self.assertEqual(
            cycle["service_aware_validation"]["telegram"]["verdict"],
            "no_effect",
        )
        self.assertEqual(shadow["state_analysis"]["TRUSTED"]["promoted"], 1)
        self.assertEqual(shadow["state_analysis"]["QUARANTINED"]["demoted"], 1)

    def test_instagram_one_sample_fail_is_degraded_not_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=15, egress_1_services={"instagram": {"ok": False, "score": 0}})
            plan = self.plan(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_no_selected_moves")
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertTrue(current["eligible"])
            self.assertIn("service_instagram_degraded", current["reasons"])
            self.assertIn("service_signal_DEGRADED_SERVICE", current["reasons"])

    def test_instagram_persistent_fail_can_trigger_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"instagram": {"ok": False, "score": 0, "consecutive_failures": 3}},
            )
            plan = self.plan(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_selected_moves_available")
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)
            self.assertEqual(plan["selected_moves"][0]["move_type"], "failover")
            self.assertEqual(plan["selected_moves"][0]["operation_id"], plan["operation"]["operation_id"])
            self.assertEqual(plan["selected_moves"][0]["selected_move_hash"], plan["operation"]["selected_move_hash"])
            self.assertEqual(plan["selected_moves"][0]["selected_move_index"], 0)

    def test_source_egress_limits_selected_moves_to_current_channel(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"instagram": {"ok": False, "score": 0, "consecutive_failures": 3}},
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--source-egress", "1"]))
            source_plan = planner.plan()
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--source-egress", "vless"]))
            unrelated_source_plan = planner.plan()

        self.assertEqual(source_plan["source_egress"], "1")
        self.assertEqual(source_plan["summary"]["candidate_moves"], 1)
        self.assertEqual(source_plan["summary"]["selected_moves"], 1)
        self.assertEqual(source_plan["selected_moves"][0]["current_egress"], "1")
        self.assertEqual(unrelated_source_plan["source_egress"], "vless")
        self.assertEqual(unrelated_source_plan["summary"]["candidate_moves"], 0)
        self.assertEqual(unrelated_source_plan["summary"]["selected_moves"], 0)

    def test_multiple_single_sample_fails_are_transient_not_hard_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=15,
                route_fitness_1="FAIL",
                egress_1_services={
                    "instagram": {"ok": False, "status": "FAIL", "score": 0},
                    "google_auth": {"ok": False, "status": "FAIL", "score": 0},
                },
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertTrue(current["eligible"])
            self.assertIn("service_signal_TRANSIENT_REVALIDATION_REQUIRED", current["reasons"])
            self.assertIn("service_instagram_transient_fail", current["reasons"])
            self.assertIn("service_google_auth_transient_fail", current["reasons"])
            self.assertIn("route_class_VIDEO_OPTIMIZED_failed_nonpersistent_service_truth", current["reasons"])
            self.assertNotIn("service_multiple_critical_failed", current["blocked"])
            self.assertNotIn("route_class_VIDEO_OPTIMIZED_failed", current["blocked"])
            self.assertEqual(
                current["service_suitability"]["per_service"]["instagram"]["truth_class"],
                "TRANSIENT_FAIL",
            )
            revalidation = current["service_suitability"]["per_service"]["instagram"]["revalidation"]
            self.assertEqual(
                revalidation["existing_command"][:3],
                ["tools/v7-service-matrix-test", "1", "instagram"],
            )
            self.assertFalse(revalidation["scope"]["full_matrix_refresh"])
            self.assertFalse(revalidation["scope"]["healthy_services_scanned"])

    def test_multiple_persistent_service_fails_still_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                route_fitness_1="FAIL",
                egress_1_services={
                    "instagram": {"ok": False, "status": "FAIL", "score": 0, "consecutive_failures": 3},
                    "google_auth": {"ok": False, "status": "FAIL", "score": 0, "consecutive_failures": 3},
                },
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertFalse(current["eligible"])
            self.assertIn("service_instagram_persistent_failed", current["blocked"])
            self.assertIn("route_class_VIDEO_OPTIMIZED_failed", current["blocked"])

    def test_probe_methodology_issue_is_visible_not_transport_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=15,
                egress_1_services={
                    "google_auth": {
                        "ok": False,
                        "status": "FAIL",
                        "score": 0,
                        "http_code": 403,
                        "reason": "http_403_probe_endpoint_requires_auth",
                    }
                },
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertTrue(current["eligible"])
            self.assertIn("service_google_auth_probe_methodology_issue", current["reasons"])
            self.assertNotIn("service_google_auth_persistent_failed", current["blocked"])
            self.assertEqual(
                current["service_suitability"]["per_service"]["google_auth"]["truth_class"],
                "PROBE_METHODOLOGY_ISSUE",
            )

    def test_stale_required_service_truth_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={
                    "google_auth": {
                        "ok": True,
                        "status": "OK",
                        "score": 100,
                        "tested_at": "2000-01-01T00:00:00+00:00",
                    }
                },
                service_signals={"service_truth_stale_seconds": 1, "service_truth_expired_seconds": 2},
            )
            args = self.args_for(root, ["--service", "google_auth"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertFalse(current["eligible"])
            self.assertIn("service_google_auth_truth_stale", current["blocked"])
            self.assertEqual(
                current["service_suitability"]["per_service"]["google_auth"]["truth_class"],
                "STALE_SERVICE_TRUTH",
            )

    def test_profile_irrelevant_failure_is_classified_and_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=15,
                egress_1_services={"anthropic": {"ok": False, "status": "FAIL", "score": 0}},
            )
            plan = self.plan(root)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertTrue(current["eligible"])
            ignored = {
                item["service"]: item["truth_class"]
                for item in current["service_suitability"]["ignored_failures"]
            }
            self.assertEqual(ignored["anthropic"], "PROFILE_IRRELEVANT_FAIL")

    def test_telegram_degraded_not_hard_blocked_does_not_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_services={"telegram": {"ok": True, "status": "DEGRADED", "score": 40}})
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "1")
            self.assertTrue(current["eligible"])

    def test_telegram_hard_blocked_can_trigger_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}})
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)
            self.assertIn("current_egress_not_eligible", plan["selected_moves"][0]["reason"])

    def test_max_selected_moves_caps_blast_radius_downward(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=4,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--max-selected-moves", "2"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(plan["summary"]["candidate_moves_total"], 4)
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertEqual(plan["safety"]["requested_max_selected_moves"], 2)
        self.assertTrue(plan["safety"]["blast_radius_cap_applied"])

    def test_dynamic_blast_radius_bounds_large_request_by_affected_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=4,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, ["--max-selected-moves", "25"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        dynamic = plan["safety"]["dynamic_blast_radius"]
        self.assertEqual(plan["summary"]["candidate_moves_total"], 4)
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertEqual(dynamic["requested_max_selected_moves"], 25)
        self.assertEqual(dynamic["affected_candidate_moves"], 4)
        self.assertEqual(dynamic["selected_after_policy_count"], 4)
        self.assertEqual(dynamic["selected_after_authority_budget_count"], 1)
        self.assertEqual(dynamic["authority_allowed_user_budget"], 1)
        self.assertEqual(dynamic["effective_blast_radius"], 1)
        self.assertEqual(dynamic["scope"], "bounded_by_authority_budget")
        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(gate["authority_class"], "CANARY")
        self.assertEqual(gate["current_allowed_user_budget"], 1)
        self.assertTrue(gate["authority_cap_applied"])

    def test_xlarge_governed_incident_selection_can_use_authority_budget_above_legacy_failover_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=60,
                egress_1_state="maintenance",
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 50,
                    "max_users_per_channel": 50,
                },
                authority_budget={
                    "authority_class": "XLARGE_BATCH",
                    "certified_authority_class": "XLARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 50,
                    "next_allowed_user_budget": 50,
                },
            )
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=maintenance role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1 certification_group=xlarge-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "\n".join(
                    row + " certification_user=1 certification_group=xlarge-batch"
                    for row in users_path.read_text(encoding="utf-8").strip().splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            args = self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "50"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        dynamic = plan["safety"]["dynamic_blast_radius"]
        continuity = plan["safety"]["incident_source_continuity"]
        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["candidate_moves_total"], 60)
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(dynamic["requested_max_selected_moves"], 50)
        self.assertEqual(dynamic["affected_candidate_moves"], 60)
        self.assertEqual(dynamic["selected_after_policy_count"], 50)
        self.assertEqual(dynamic["selected_after_authority_budget_count"], 50)
        self.assertEqual(dynamic["authority_allowed_user_budget"], 50)
        self.assertEqual(dynamic["scope"], "blocked_by_emergency_failover_autonomy_gate")
        self.assertFalse(gate["authority_cap_applied"])
        self.assertTrue(continuity["active"])
        self.assertTrue(continuity["failover_limit_raised_by_governed_authority"])
        self.assertEqual(continuity["base_failover_limit"], 25)
        self.assertEqual(continuity["governed_failover_limit"], 50)

    def test_legacy_failover_cap_still_applies_without_explicit_governed_batch_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=60,
                egress_1_state="maintenance",
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 50,
                    "max_users_per_channel": 50,
                },
                authority_budget={
                    "authority_class": "XLARGE_BATCH",
                    "certified_authority_class": "XLARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 50,
                    "next_allowed_user_budget": 50,
                },
            )
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=maintenance role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1 certification_group=xlarge-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "\n".join(
                    row + " certification_user=1 certification_group=xlarge-batch"
                    for row in users_path.read_text(encoding="utf-8").strip().splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        dynamic = plan["safety"]["dynamic_blast_radius"]
        continuity = plan["safety"]["incident_source_continuity"]
        self.assertEqual(plan["summary"]["candidate_moves_total"], 60)
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(dynamic["requested_max_selected_moves"], 0)
        self.assertEqual(dynamic["selected_after_policy_count"], 25)
        self.assertEqual(dynamic["selected_after_authority_budget_count"], 25)
        self.assertEqual(dynamic["scope"], "blocked_by_emergency_failover_autonomy_gate")
        self.assertNotIn("failover_limit_raised_by_governed_authority", continuity)

    def test_authority_budget_caps_prepared_small_batch_to_certified_canary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=4,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 10,
                },
            )
            args = self.args_for(root, ["--max-selected-moves", "25"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["candidate_moves_total"], 4)
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertEqual(gate["authority_class"], "CANARY")
        self.assertEqual(gate["prepared_authority_class"], "SMALL_BATCH")
        self.assertEqual(gate["certified_authority_class"], "CANARY")
        self.assertEqual(gate["authority_lifecycle_state"], "PREPARED")
        self.assertEqual(gate["current_allowed_user_budget"], 1)
        self.assertEqual(gate["decision"], "cap_prepared_authority_to_certified_evidence")
        self.assertIn("promotion_without_certification", gate["blocked_actions"])
        self.assertTrue(gate["authority_cap_applied"])
        lifecycle = gate["authority_lifecycle"]
        self.assertTrue(lifecycle["prepared_exceeds_certified"])
        self.assertFalse(lifecycle["governance"]["promotion"]["eligible"])
        self.assertIn("prepared_authority_exceeds_certified_evidence", lifecycle["governance"]["promotion"]["blockers"])

    def test_authority_bridge_allows_transitional_five_user_budget_without_certifying_small_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=6,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 5,
                },
            )
            args = self.args_for(root, ["--max-selected-moves", "25"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["candidate_moves_total"], 6)
        self.assertEqual(plan["summary"]["selected_moves"], 5)
        self.assertEqual(gate["authority_class"], "CANARY")
        self.assertEqual(gate["prepared_authority_class"], "SMALL_BATCH")
        self.assertEqual(gate["certified_authority_class"], "CANARY")
        self.assertEqual(gate["authority_lifecycle_state"], "CANARY_EXPANSION")
        self.assertEqual(gate["current_allowed_user_budget"], 5)
        self.assertEqual(gate["decision"], "allow_transitional_authority_bridge_budget")
        self.assertEqual(gate["action"], "permit_next_blast_radius_step_without_certifying_prepared_authority")
        self.assertIn("promotion_without_certification", gate["blocked_actions"])
        self.assertIn("apply_above_bridge_budget", gate["blocked_actions"])
        self.assertTrue(gate["authority_bridge"]["active"])
        self.assertFalse(gate["authority_bridge"]["promotion_certification"])
        self.assertEqual(gate["authority_bridge"]["bridge_budget_ceiling"], 5)
        self.assertEqual(gate["authority_lifecycle"]["bridge_model"]["states"]["CANARY_EXPANSION"]["budget"], 5)
        self.assertFalse(gate["authority_lifecycle"]["governance"]["promotion"]["eligible"])
        self.assertIn("bridge_state_is_not_certification", gate["authority_lifecycle"]["governance"]["promotion"]["blockers"])

    def test_authority_budget_allows_certified_small_batch_to_class_ceiling(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=6,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 10,
                },
            )
            args = self.args_for(root, ["--max-selected-moves", "25"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["candidate_moves_total"], 6)
        self.assertEqual(plan["summary"]["selected_moves"], 5)
        self.assertEqual(gate["authority_class"], "SMALL_BATCH")
        self.assertEqual(gate["prepared_authority_class"], "SMALL_BATCH")
        self.assertEqual(gate["certified_authority_class"], "SMALL_BATCH")
        self.assertEqual(gate["authority_lifecycle_state"], "CERTIFIED")
        self.assertEqual(gate["current_allowed_user_budget"], 5)
        self.assertEqual(gate["next_authority_class"], "MEDIUM_BATCH")
        self.assertEqual(gate["next_allowed_user_budget"], 10)
        self.assertTrue(gate["authority_cap_applied"])
        self.assertTrue(gate["authority_lifecycle"]["governance"]["promotion"]["eligible"])

    def test_authority_budget_cannot_raise_canary_above_class_ceiling(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=4,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "CANARY",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 10,
                },
            )
            args = self.args_for(root, ["--max-selected-moves", "25"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertEqual(gate["authority_class"], "CANARY")
        self.assertEqual(gate["current_allowed_user_budget"], 1)
        self.assertEqual(gate["next_allowed_user_budget"], 5)
        self.assertEqual(gate["policy"]["class_budget_ceiling"], 1)

    def test_authority_budget_disabled_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={"enabled": False},
            )
            plan = self.plan(root)

        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(gate["decision"], "authority_budget_gate_disabled_by_policy")
        self.assertIn("disable_authority_budget_gate_in_production", gate["blocked_actions"])

    def test_historical_broad_authority_without_current_action_contract_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=4,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "XLARGE_BATCH",
                    "certified_authority_class": "XLARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 50,
                    "promoted_at": "2026-07-03T10:53:23+00:00",
                },
            )
            policy_path = root / "policy.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["authority_budget"].pop("current_action_class_contract", None)
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            plan = self.tool.AutoswitchPlanner(self.args_for(root, ["--max-selected-moves", "25"])).plan()

        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(gate["authority_lifecycle_state"], "FROZEN")
        self.assertEqual(gate["current_allowed_user_budget"], 0)
        self.assertEqual(gate["decision"], "block_all_selected_moves_current_action_class_contract_required")
        self.assertIn("current_action_class_contract_missing_or_schema_invalid", gate["blocked_actions"])

    def test_active_standing_policy_is_a_valid_bounded_runtime_gate_not_a_one_use_contract(self):
        standing = {
            "contract_id": "sdpc_unit",
            "contract_hash": "a" * 64,
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "expires_at": "2099-01-01T00:00:00+00:00",
            "issuing_owner": "admin_core/operator_execution.py",
            "authority_decision": {"decision_id": "sdpdec_unit"},
        }
        standing_policy = {
            "policy_state": "APPROVED",
            "current_mode": "DELEGATED_AUTONOMY",
            "max_users_per_action": 1,
            "max_concurrent_transactions": 1,
            "candidate_identity": "FRESH_ONLY",
            "packet_generation": "FRESH_IMMEDIATELY_BEFORE_EXECUTION",
            "packet_reuse": "FORBIDDEN",
            "runtime_apply_enabled": True,
            "self_expansion_allowed": False,
            "cooldown": {"per_user_seconds": 1800},
            "stop_conditions": ["ANTI_FLAP_BLOCK"],
        }
        with mock.patch.object(
            self.tool.operator_execution,
            "validate_standing_delegated_operational_policy",
            return_value={"ok": True, "errors": [], "policy": standing_policy},
        ):
            gate = self.tool.runtime_authority_contract_status(
                {},
                prepared_class="POOL",
                certified_class="CANARY",
                standing_policy_contract=standing,
                authority_audit_records=[{"record_type": "existing-audit"}],
            )

        self.assertTrue(gate["required"])
        self.assertTrue(gate["valid"])
        self.assertEqual(gate["max_users"], 1)
        self.assertFalse(gate["provenance"]["strict_provenance_contract"])
        self.assertTrue(gate["provenance"]["standing_policy_contract"])

    def test_authority_governance_frozen_state_blocks_all_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "current_allowed_user_budget": 5,
                    "authority_lifecycle_state": "FROZEN",
                },
            )
            plan = self.plan(root)

        gate = plan["safety"]["authority_budget_gate"]
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(gate["authority_lifecycle_state"], "FROZEN")
        self.assertEqual(gate["current_allowed_user_budget"], 0)
        self.assertEqual(gate["decision"], "block_all_selected_moves_authority_budget_zero")
        self.assertIn("authority_frozen", gate["authority_lifecycle"]["governance"]["promotion"]["blockers"])
        self.assertIn("user_movement", gate["authority_lifecycle"]["action_matrix"]["FROZEN"]["blocked_actions"])

    def test_restore_barrier_exposes_telegram_failover_proposal_but_blocks_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "failover_quarantine": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
            )
            plan = self.plan(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_restore_barrier_active")
            self.assertTrue(plan["safety"]["restore_barrier"]["active"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["proposal_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertTrue(plan["summary"]["execution_blocked"])
            self.assertEqual(plan["summary"]["execution_blocker"], "restore_barrier")
            self.assertEqual(plan["safety"]["restore_barrier_execution_gate"]["decision"], "block_selected_moves_restore_barrier")
            self.assertEqual(plan["safety"]["restore_barrier_execution_gate"]["selected_moves_before_gate"], 1)
            self.assertEqual(plan["safety"]["restore_barrier_execution_gate"]["selected_moves_after_gate"], 0)
            self.assertEqual(plan["decisions"][0]["action"], "switch")
            self.assertEqual(plan["decisions"][0]["move_type"], "failover")
            self.assertEqual(plan["decisions"][0]["recommended_egress"], "vless")
            self.assertIn(
                "restore_barrier_execution_blocked",
                plan["decisions"][0]["reason"],
            )

    def test_restore_barrier_execution_gate_keeps_apply_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--mode", "guarded", "--apply"]))
            planner._run_switch = lambda *args, **kwargs: self.fail("_run_switch must not run while restore barrier blocks execution")
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(plan["summary"]["proposal_moves_total"], 1)
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertTrue(plan["summary"]["execution_blocked"])
        self.assertEqual(plan["apply_result"]["reason"], "no_selected_moves")
        self.assertEqual(plan["operation"]["terminal_state"], "NOOP")

    def test_emergency_failover_autonomy_authorizes_bounded_failover_when_gates_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                users=3,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertTrue(gate["ok"])
        self.assertEqual(gate["decision"], "authorize_bounded_emergency_failover")
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertEqual(plan["summary"]["execution_mode"], "emergency_failover")
        self.assertFalse(plan["summary"]["execution_blocked"])
        self.assertEqual(plan["selected_moves"][0]["execution_mode"], "emergency_failover")

    def test_emergency_failover_without_approved_envelope_remains_single_user_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                users=5,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 5,
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "5"])
            )
            plan = planner.plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertTrue(gate["ok"])
        self.assertEqual(gate["selected_moves_before_gate"], 5)
        self.assertEqual(gate["selected_moves_after_gate"], 1)
        self.assertEqual(gate["effective_max_users_per_run"], 1)
        self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_approved_production_validation_envelope_preserves_batch_through_runtime_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bootstrap = self.prepare_l3_validation_envelope(root, users=5)
            args = self.args_for(
                root,
                [
                    "--emergency-failover-autonomy",
                    "--apply",
                    "--verify",
                    "--mode",
                    "guarded",
                    "--max-selected-moves",
                    "5",
                    "--approved-packet-id",
                    "pkt-unit-test",
                    "--approved-selected-move-hash",
                    bootstrap["operation"]["selected_move_hash"],
                ],
            )
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            planner._run_switch = fake_run_switch
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 0, stdout="service ok\n")
            planner._emit_terminal_audit = lambda audit: {**audit, "emitted": True, "status": "emitted"}
            plan["apply_result"] = planner.apply(plan)

        gate = plan["safety"]["emergency_failover_autonomy"]
        eligibility = plan["apply_result"]["l3_execution_eligibility"]
        self.assertTrue(gate["ok"])
        self.assertEqual(gate["decision"], "authorize_governed_production_validation_envelope")
        self.assertEqual(gate["selected_moves_before_gate"], 5)
        self.assertEqual(gate["selected_moves_after_gate"], 5)
        self.assertEqual(gate["effective_max_users_per_run"], 5)
        self.assertEqual(plan["summary"]["selected_moves"], 5)
        self.assertEqual(len(plan["selected_moves"]), 5)
        self.assertTrue(eligibility["ok"])
        self.assertTrue(eligibility["approved_batch_scope"])
        self.assertEqual(eligibility["approved_selected_move_count"], 5)
        self.assertEqual(len(eligibility["checked_moves"]), 5)
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(len(plan["apply_result"]["results"]), 5)
        self.assertEqual(len(switch_calls), 5)
        self.assertEqual({move["current_egress"] for move in plan["selected_moves"]}, {"1"})
        self.assertEqual({call[2] for call in switch_calls}, {"failover"})

    def test_l3_wake_accepts_confirmed_service_failure_and_incident_consumes_planner_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                    "wake_source": "confirmed_service_failure",
                },
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        wake = plan["safety"]["l3_wake"]
        incident = plan["safety"]["l3_incident"]
        self.assertEqual(wake["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_service_failure", wake["accepted_wake_sources"])
        self.assertIn("confirmed_current_channel_failure", wake["accepted_wake_sources"])
        self.assertEqual(incident["incident_state"], "READY_FOR_EXECUTION")
        self.assertEqual(incident["authority_object"], "EMERGENCY_FAILOVER_AUTONOMY")
        self.assertEqual(incident["allowed_move"], "FAILOVER")
        self.assertEqual(incident["allowed_reason"], "CURRENT_CHANNEL_FAILED")
        self.assertEqual(incident["affected_users"], ["10.0.0.2"])
        self.assertEqual(incident["failed_sources"], ["1"])
        self.assertEqual(incident["target_channels"], ["vless"])
        self.assertEqual(incident["selected_move_hash"], plan["operation"]["selected_move_hash"])
        self.assertFalse(incident["planner_consumption"]["runtime_replaced_planner"])
        self.assertFalse(incident["runtime_apply_allowed_now"])
        self.assertFalse(incident["authority_expanded"])
        self.assertEqual(plan["summary"]["l3_incident_state"], "READY_FOR_EXECUTION")

    def test_missing_action_contract_keeps_fresh_l3_wake_observable_without_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                authority_budget={
                    "authority_class": "POOL",
                    "certified_authority_class": "POOL",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 1,
                    "current_action_class_contract": {},
                },
                emergency_failover_autonomy={"enabled": True, "max_users_per_run": 1, "max_users_per_channel": 1},
            )
            plan = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"])).plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        wake = plan["safety"]["l3_wake"]
        boundary = plan["safety"]["action_class_execution_boundary"]
        self.assertEqual(plan["selected_moves"], [])
        self.assertFalse(gate["ok"])
        self.assertEqual(gate["move_evidence_source"], "pre_contract_shadow_selection_read_only")
        self.assertEqual(len(gate["move_evidence"]), 1)
        self.assertEqual(wake["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_service_failure", wake["accepted_wake_sources"])
        self.assertEqual(boundary["status"], "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED")
        self.assertFalse(boundary["candidate_created"])
        self.assertFalse(boundary["packet_created"])
        self.assertFalse(boundary["lease_created"])

    def test_observation_fail_with_affected_users_produces_confirmed_current_channel_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=13,
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            self.mark_current_channel_failed(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()
            replay = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"])).plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        wake = plan["safety"]["l3_wake"]
        incident = plan["safety"]["l3_incident"]
        current_events = [
            row for row in wake["observed_events"]
            if row["wake_source"] == "confirmed_current_channel_failure"
        ]
        replay_events = [
            row for row in replay["safety"]["l3_wake"]["observed_events"]
            if row["wake_source"] == "confirmed_current_channel_failure"
        ]
        self.assertTrue(gate["ok"])
        self.assertEqual(plan["summary"]["proposal_moves_total"], 13)
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertGreater(plan["safety"]["selected_moves_diagnostics"]["selected_moves_before_restore_barrier"], 0)
        self.assertEqual(plan["safety"]["selected_moves_diagnostics"]["selected_moves_after_gate"], 1)
        self.assertEqual(plan["selected_moves"][0]["current_egress"], "1")
        self.assertIn(plan["selected_moves"][0]["user_ip"], {f"10.0.0.{idx}" for idx in range(2, 15)})
        self.assertEqual(plan["selected_moves"][0]["move_type"], "failover")
        self.assertEqual(wake["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_current_channel_failure", wake["accepted_wake_sources"])
        self.assertNotIn("confirmed_service_failure", wake["accepted_wake_sources"])
        self.assertEqual(current_events[0]["path"], "inferred:v7-state-current-channel-failure")
        self.assertEqual(current_events[0]["event_id"], replay_events[0]["event_id"])
        self.assertEqual(incident["incident_state"], "READY_FOR_EXECUTION")
        self.assertNotIn(incident["incident_state"], {"NO_INCIDENT_DISABLED", "NO_INCIDENT_NO_EVIDENCE"})
        self.assertEqual(incident["failed_sources"], ["1"])
        self.assertEqual(incident["failed_required_services"], [])
        self.assertEqual(incident["incident_key_components"]["service_family"], ["current_channel_failure"])
        self.assertEqual(incident["confirmed_current_channel_failures"][0]["diagnose_reason"], "interface_down_or_missing")
        self.assertTrue(gate["move_evidence"][0]["current_channel_failure"]["confirmed"])
        self.assertNotIn("required_service_failure_required", gate["blockers"])
        self.assertFalse(gate["broad_automation_enabled"])

    def test_controlled_certification_maintenance_produces_confirmed_current_channel_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=3,
                egress_1_state="maintenance",
                restore_barrier={
                    "enabled": True,
                    "failover_quarantine": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 2,
                    "max_users_per_channel": 2,
                },
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "authority_lifecycle_state": "CERTIFIED",
                    "current_allowed_user_budget": 2,
                },
            )
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=maintenance role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1 certification_group=medium-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "\n".join(
                    row + " certification_user=1 certification_group=medium-batch"
                    for row in users_path.read_text(encoding="utf-8").strip().splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            state_path = root / "state" / "v7-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["users"] = [
                {"ip": f"10.0.0.{idx + 2}", "current": "1", "table": str(100 + idx), "enabled": "1"}
                for idx in range(2)
            ]
            state_path.write_text(json.dumps(state), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "2"]))
            plan = planner.plan()

        wake = plan["safety"]["l3_wake"]
        incident = plan["safety"]["l3_incident"]
        selected = plan["selected_moves"]
        self.assertEqual(wake["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_current_channel_failure", wake["accepted_wake_sources"])
        self.assertEqual(incident["incident_state"], "READY_FOR_EXECUTION")
        self.assertEqual(incident["incident_source"], "1")
        self.assertEqual(incident["failed_sources"], ["1"])
        self.assertEqual(incident["incident_source_continuity"]["affected_users_count"], 3)
        self.assertEqual(len(selected), 2)
        self.assertTrue(all(move["current_egress"] == "1" for move in selected))
        self.assertTrue(
            all(
                row["current_channel_failure"]["diagnose_reason"] == "controlled_certification_source_unavailable"
                for row in plan["safety"]["emergency_failover_autonomy"]["move_evidence"]
            )
        )
        self.assertFalse(plan["safety"]["emergency_failover_autonomy"]["broad_automation_enabled"])

    def test_controlled_certification_failure_overrides_ok_state_reason_before_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                egress_1_state="maintenance",
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=maintenance role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1 certification_group=medium-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "\n".join(
                    row + " certification_user=1 certification_group=medium-batch"
                    for row in users_path.read_text(encoding="utf-8").strip().splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            state_path = root / "state" / "v7-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["egress"]["1"]["diagnose_severity"] = "OK"
            state["egress"]["1"]["diagnose_reason"] = "OK"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "1"])
            )
            plan = planner.plan()
            eligibility = planner._l3_execution_eligibility(plan)

        wake = plan["safety"]["l3_wake"]
        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertEqual(wake["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_current_channel_failure", wake["accepted_wake_sources"])
        self.assertNotIn("required_service_failure_required", gate["blockers"])
        self.assertEqual(eligibility["decision"], "EXECUTE")
        self.assertTrue(eligibility["ok"])
        self.assertNotIn("source_recovered_before_apply", eligibility["blockers"])
        self.assertEqual(
            eligibility["checked_moves"][0]["live_evidence_blockers"],
            [],
        )

    def test_controlled_certification_failure_survives_missing_current_candidate_before_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                egress_1_state="maintenance",
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=maintenance role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1 certification_group=medium-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "\n".join(
                    row + " certification_user=1 certification_group=medium-batch"
                    for row in users_path.read_text(encoding="utf-8").strip().splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "1"])
            )
            plan = planner.plan()
            plan["selected_moves"][0]["candidates"] = [
                row for row in plan["selected_moves"][0]["candidates"] if row.get("egress") != "1"
            ]
            eligibility = planner._l3_execution_eligibility(plan)

        self.assertTrue(eligibility["ok"])
        self.assertEqual(eligibility["decision"], "EXECUTE")
        self.assertNotIn("source_recovered_before_apply", eligibility["blockers"])
        self.assertNotIn("source_failure_evidence_not_fresh_before_apply", eligibility["blockers"])

    def test_controlled_certification_failure_suppresses_stale_service_failure_before_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                egress_1_state="maintenance",
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=maintenance role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1 certification_group=medium-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "\n".join(
                    row + " certification_user=1 certification_group=medium-batch"
                    for row in users_path.read_text(encoding="utf-8").strip().splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "1"])
            )
            plan = planner.plan()
            current = next(
                row for row in plan["selected_moves"][0]["candidates"] if row.get("egress") == "1"
            )
            current["eligible"] = True
            current["service_suitability"]["per_service"]["telegram"] = {
                "available": False,
                "status": "DOWN",
                "truth_class": "PERSISTENT_FAIL",
                "freshness": {"state": "STALE"},
            }
            eligibility = planner._l3_execution_eligibility(plan)

        self.assertTrue(eligibility["ok"])
        self.assertEqual(eligibility["decision"], "EXECUTE")
        blockers = eligibility["checked_moves"][0]["live_evidence_blockers"]
        self.assertNotIn("current_candidate_still_eligible", blockers)
        self.assertNotIn("fresh_service_failure_evidence_required", blockers)
        self.assertNotIn("source_failure_evidence_not_fresh_before_apply", eligibility["blockers"])

    def test_plain_maintenance_does_not_produce_confirmed_current_channel_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=3,
                egress_1_state="maintenance",
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 2,
                    "max_users_per_channel": 2,
                },
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "2"]))
            plan = planner.plan()

        self.assertEqual(plan["safety"]["l3_wake"]["decision"], "REJECT_WAKE")
        self.assertNotEqual(plan["summary"]["l3_incident_state"], "READY_FOR_EXECUTION")
        self.assertEqual(plan["selected_moves"], [])
        self.assertEqual(plan["summary"]["execution_blocker"], "emergency_failover_autonomy")
        evidence = plan["safety"]["emergency_failover_autonomy"]["move_evidence"]
        self.assertTrue(evidence)
        self.assertTrue(all(not row["current_channel_failure"] for row in evidence))

    def test_active_failed_source_incident_constrains_next_l3_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=3,
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            self.add_failed_egress(root, egress="2")
            self.mark_current_channel_failed(root, egress="1")
            (root / "state" / "users.registry").write_text(
                "ip=10.0.0.2 current=2 table=100 enabled=1\n"
                "ip=10.0.0.3 current=1 table=101 enabled=1\n"
                "ip=10.0.0.4 current=1 table=102 enabled=1\n",
                encoding="utf-8",
            )
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        "incident-open-1": {
                            "incident_key": "incident-open-1",
                            "status": "OPEN",
                            "authority_object": "EMERGENCY_FAILOVER_AUTONOMY",
                            "failed_sources": ["1"],
                            "incident_source": "1",
                            "failed_required_services": [],
                            "updated_at": "2999-01-01T00:00:00+00:00",
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        continuity = plan["safety"]["incident_source_continuity"]
        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertTrue(continuity["active"])
        self.assertEqual(continuity["incident_source"], "1")
        self.assertEqual(continuity["selected_candidates_after_filter"], 2)
        self.assertEqual(plan["selected_moves"][0]["current_egress"], "1")
        self.assertIn(plan["selected_moves"][0]["user_ip"], {"10.0.0.3", "10.0.0.4"})
        self.assertEqual(plan["safety"]["l3_incident"]["incident_key"], "incident-open-1")
        self.assertEqual(gate["selected_moves_after_gate"], 1)
        self.assertEqual(plan["safety"]["l3_wake"]["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_current_channel_failure", plan["safety"]["l3_wake"]["accepted_wake_sources"])

    def test_requested_failed_source_overrides_unrelated_active_incident_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=3,
                egress_1_state="maintenance",
                restore_barrier={
                    "enabled": True,
                    "failover_quarantine": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 2,
                    "max_users_per_channel": 2,
                },
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "authority_lifecycle_state": "CERTIFIED",
                    "current_allowed_user_budget": 2,
                },
            )
            self.add_failed_egress(root, egress="2")
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=maintenance role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 state=maintenance role=GLOBAL_FAST controlled_certification_source=1 certification_group=medium-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "ip=10.0.0.2 current=1 table=100 enabled=1 certification_user=1 certification_group=medium-batch\n"
                "ip=10.0.0.3 current=1 table=101 enabled=1 certification_user=1 certification_group=medium-batch\n"
                "ip=10.0.0.4 current=1 table=102 enabled=1 certification_user=1 certification_group=medium-batch\n"
                "ip=10.0.1.2 current=2 table=200 enabled=1\n"
                "ip=10.0.1.3 current=2 table=201 enabled=1\n"
                "ip=10.0.1.4 current=2 table=202 enabled=1\n"
                "ip=10.0.1.5 current=2 table=203 enabled=1\n"
                "ip=10.0.1.6 current=2 table=204 enabled=1\n"
                "ip=10.0.1.7 current=2 table=205 enabled=1\n",
                encoding="utf-8",
            )
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        "incident-open-2": {
                            "incident_key": "incident-open-2",
                            "status": "OPEN",
                            "authority_object": "EMERGENCY_FAILOVER_AUTONOMY",
                            "failed_sources": ["2"],
                            "incident_source": "2",
                            "failed_required_services": [],
                            "updated_at": "2999-01-01T00:00:00+00:00",
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "2", "--source-egress", "1"])
            )
            plan = planner.plan()

        continuity = plan["safety"]["incident_source_continuity"]
        self.assertTrue(continuity["active"])
        self.assertEqual(continuity["incident_source"], "1")
        self.assertEqual(continuity["continuity_source"], "requested_source_egress")
        self.assertEqual(continuity["overrode_incident_source"], "2")
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertTrue(all(move["current_egress"] == "1" for move in plan["selected_moves"]))
        self.assertEqual(plan["safety"]["l3_wake"]["decision"], "ACCEPT_WAKE")

    def test_active_incident_skips_exhausted_semantic_attempt_and_selects_next_user(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=4,
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                    "retry_budget_per_incident": 1,
                },
            )
            self.add_failed_egress(root, egress="2")
            self.mark_current_channel_failed(root, egress="1")
            (root / "state" / "users.registry").write_text(
                "ip=10.0.0.2 current=1 table=100 enabled=1\n"
                "ip=10.0.0.3 current=1 table=101 enabled=1\n"
                "ip=10.0.0.4 current=1 table=102 enabled=1\n"
                "ip=10.0.0.5 current=2 table=103 enabled=1\n",
                encoding="utf-8",
            )
            incident_key = "incident-open-1"
            exhausted_signature = self.tool.AutoswitchPlanner._l3_semantic_attempt_signature(
                [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "1",
                    "recommended_egress": "vless",
                    "move_type": "failover",
                }],
                incident_key=incident_key,
            )
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        incident_key: {
                            "incident_key": incident_key,
                            "status": "OPEN",
                            "authority_object": "EMERGENCY_FAILOVER_AUTONOMY",
                            "failed_sources": ["1"],
                            "incident_source": "1",
                            "failed_required_services": [],
                            "updated_at": "2999-01-01T00:00:00+00:00",
                            "attempts": [
                                {
                                    "operation_id": "runtime-autoswitch-rolled-back",
                                    "selected_move_hash": "unit-test-hash",
                                    "semantic_attempt_signature": exhausted_signature,
                                    "terminal_outcome": "ROLLBACK_SUCCESS",
                                    "terminal_state": "ROLLED_BACK",
                                    "applied": True,
                                }
                            ],
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, [
                    "--emergency-failover-autonomy",
                    "--target-egress",
                    "vless",
                    "--max-selected-moves",
                    "1",
                ])
            )
            plan = planner.plan()

        continuity = plan["safety"]["incident_source_continuity"]
        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertTrue(continuity["active"])
        self.assertEqual(continuity["incident_key"], incident_key)
        self.assertEqual(continuity["incident_source"], "1")
        self.assertTrue(continuity["retry_filter_applied"])
        self.assertEqual(continuity["retry_exhausted_attempts_excluded"][0]["user_ip"], "10.0.0.2")
        self.assertEqual(continuity["retry_exhausted_attempts_excluded"][0]["semantic_attempt_signature"], exhausted_signature)
        self.assertEqual(continuity["selected_candidates_after_filter"], 3)
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertEqual(gate["selected_moves_after_gate"], 1)
        self.assertTrue(gate["ok"])
        self.assertEqual(gate["incident_key"], incident_key)
        self.assertNotIn("duplicate_apply_attempt", gate["blockers"])
        self.assertNotIn("l3_retry_budget_exhausted", gate["blockers"])
        self.assertEqual(plan["selected_moves"][0]["current_egress"], "1")
        self.assertEqual(plan["selected_moves"][0]["recommended_egress"], "vless")
        self.assertEqual(plan["selected_moves"][0]["move_type"], "failover")
        self.assertNotEqual(plan["selected_moves"][0]["user_ip"], "10.0.0.2")
        self.assertIn(plan["selected_moves"][0]["user_ip"], {"10.0.0.3", "10.0.0.4"})
        self.assertNotEqual(plan["selected_moves"][0]["current_egress"], "2")
        self.assertEqual(plan["safety"]["l3_incident"]["incident_key"], incident_key)

    def test_lost_incident_source_recovers_from_confirmed_failed_source_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=3,
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            self.add_failed_egress(root, egress="2")
            self.mark_current_channel_failed(root, egress="1")
            (root / "state" / "users.registry").write_text(
                "ip=10.0.0.2 current=2 table=100 enabled=1\n"
                "ip=10.0.0.3 current=1 table=101 enabled=1\n"
                "ip=10.0.0.4 current=1 table=102 enabled=1\n",
                encoding="utf-8",
            )
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        "incident-lost-source": {
                            "incident_key": "incident-lost-source",
                            "status": "SUSPENDED",
                            "authority_object": "EMERGENCY_FAILOVER_AUTONOMY",
                            "failed_sources": [],
                            "incident_source": "",
                            "failed_required_services": [],
                            "updated_at": "2999-01-01T00:00:00+00:00",
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        continuity = plan["safety"]["incident_source_continuity"]
        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertTrue(continuity["active"])
        self.assertEqual(continuity["reason"], "confirmed_failed_source_observation_with_affected_users")
        self.assertEqual(continuity["incident_source"], "1")
        self.assertEqual(continuity["continuity_source"], "confirmed_observation")
        self.assertEqual(continuity["affected_users_count"], 2)
        self.assertEqual(plan["selected_moves"][0]["current_egress"], "1")
        self.assertIn(plan["selected_moves"][0]["user_ip"], {"10.0.0.3", "10.0.0.4"})
        self.assertNotEqual(plan["selected_moves"][0]["current_egress"], "2")
        self.assertEqual(gate["selected_moves_after_gate"], 1)
        self.assertEqual(plan["safety"]["l3_wake"]["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_current_channel_failure", plan["safety"]["l3_wake"]["accepted_wake_sources"])

    def test_stale_persisted_incident_source_does_not_override_larger_failed_source_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=3,
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            self.add_failed_egress(root, egress="2")
            self.mark_current_channel_failed(root, egress="1")
            (root / "state" / "users.registry").write_text(
                "ip=10.0.0.2 current=2 table=100 enabled=1\n"
                "ip=10.0.0.3 current=1 table=101 enabled=1\n"
                "ip=10.0.0.4 current=1 table=102 enabled=1\n",
                encoding="utf-8",
            )
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        "incident-stale-source": {
                            "incident_key": "incident-stale-source",
                            "status": "OPEN",
                            "authority_object": "EMERGENCY_FAILOVER_AUTONOMY",
                            "failed_sources": ["2"],
                            "incident_source": "2",
                            "failed_required_services": [],
                            "updated_at": "2999-01-01T00:00:00+00:00",
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        continuity = plan["safety"]["incident_source_continuity"]
        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertTrue(continuity["active"])
        self.assertEqual(continuity["reason"], "confirmed_failed_source_observation_with_affected_users")
        self.assertEqual(continuity["continuity_source"], "confirmed_observation")
        self.assertEqual(continuity["incident_source"], "1")
        self.assertEqual(continuity["affected_users_count"], 2)
        self.assertEqual(plan["selected_moves"][0]["current_egress"], "1")
        self.assertIn(plan["selected_moves"][0]["user_ip"], {"10.0.0.3", "10.0.0.4"})
        self.assertNotEqual(plan["selected_moves"][0]["current_egress"], "2")
        self.assertEqual(gate["selected_moves_after_gate"], 1)
        self.assertEqual(plan["safety"]["l3_wake"]["decision"], "ACCEPT_WAKE")

    def test_current_channel_failure_source_wins_over_larger_service_only_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=5,
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                },
            )
            self.mark_current_channel_failed(root, egress="1")
            (root / "state" / "egress.registry").write_text(
                (root / "state" / "egress.registry").read_text(encoding="utf-8")
                + "id=2 interface=v7two enabled=1 state=enabled role=GLOBAL_FAST\n",
                encoding="utf-8",
            )
            state_path = root / "state" / "v7-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state.setdefault("egress", {})["2"] = {
                "avg_mbps": 80,
                "min_mbps": 70,
                "stability": 0.95,
                "code": "200",
                "diagnose_severity": "OK",
                "diagnose_reason": "OK",
            }
            state_path.write_text(json.dumps(state), encoding="utf-8")
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix.setdefault("items", {})["2"] = {
                "services": {
                    "youtube": {"ok": True, "score": 100},
                    "instagram": {"ok": True, "score": 100},
                    "telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": "2999-01-01T00:00:00+00:00"},
                    "google": {"ok": True, "score": 100},
                    "google_auth": {"ok": True, "score": 100},
                },
                "route_class_fitness": {
                    "VIDEO_OPTIMIZED": {"status": "FAIL"},
                    "GLOBAL_STABLE": {"status": "OK"},
                    "GLOBAL_FAST": {"status": "OK"},
                },
            }
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            (root / "state" / "users.registry").write_text(
                "ip=10.0.0.2 current=1 table=100 enabled=1\n"
                "ip=10.0.0.3 current=1 table=101 enabled=1\n"
                "ip=10.0.0.4 current=2 table=102 enabled=1\n"
                "ip=10.0.0.5 current=2 table=103 enabled=1\n"
                "ip=10.0.0.6 current=2 table=104 enabled=1\n",
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        continuity = plan["safety"]["incident_source_continuity"]
        self.assertTrue(continuity["active"])
        self.assertEqual(continuity["incident_source"], "1")
        self.assertTrue(continuity["scope"]["current_channel_failure"])
        self.assertEqual(continuity["affected_users_count"], 2)
        self.assertEqual(plan["selected_moves"][0]["current_egress"], "1")
        self.assertIn(plan["selected_moves"][0]["user_ip"], {"10.0.0.2", "10.0.0.3"})

    def test_approved_plan_lock_rejects_non_incident_source_during_l3_continuation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=3)
            self.add_failed_egress(root, egress="2")
            self.mark_current_channel_failed(root, egress="1")
            (root / "state" / "users.registry").write_text(
                "ip=10.0.0.2 current=2 table=100 enabled=1\n"
                "ip=10.0.0.3 current=1 table=101 enabled=1\n"
                "ip=10.0.0.4 current=1 table=102 enabled=1\n",
                encoding="utf-8",
            )
            bootstrap_args = self.args_for(root, ["--target-egress", "vless", "--max-selected-moves", "1"])
            bootstrap = self.tool.AutoswitchPlanner(bootstrap_args).plan()
            self.assertEqual(bootstrap["selected_moves"][0]["current_egress"], "2")
            barrier = self.approved_restore_barrier_from_plan(bootstrap, max_selected_moves=1)
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(barrier), encoding="utf-8")
            policy_path = root / "policy.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["emergency_failover_autonomy"] = {"enabled": True, "max_users_per_run": 1, "max_users_per_channel": 1}
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        "incident-open-1": {
                            "incident_key": "incident-open-1",
                            "status": "OPEN",
                            "authority_object": "EMERGENCY_FAILOVER_AUTONOMY",
                            "failed_sources": ["1"],
                            "incident_source": "1",
                            "updated_at": "2999-01-01T00:00:00+00:00",
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            )
            plan = planner.plan()

        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertFalse(validation["ok"])
        self.assertIn("approved_plan_lock_incident_source_mismatch", validation["reasons"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_l3_success_keeps_failed_source_incident_open_when_users_remain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            planner._run_switch = lambda ip, egress, reason: subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 0, stdout="service ok\n")
            planner._emit_terminal_audit = lambda audit: {**audit, "emitted": True, "status": "emitted"}
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)
            runtime_state = json.loads((root / "state" / "l3-runtime-state.json").read_text(encoding="utf-8"))

        incident = runtime_state["incidents"][plan["safety"]["l3_incident"]["incident_key"]]
        self.assertEqual(incident["status"], "OPEN")
        self.assertTrue(incident["incident_source_continuity"]["kept_open"])
        self.assertEqual(incident["incident_source_continuity"]["scopes"][0]["affected_users_count"], 1)

    def test_observation_fail_does_not_legalize_timer_wake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={
                    "enabled": True,
                    "max_users_per_run": 1,
                    "max_users_per_channel": 1,
                    "wake_source": "timer",
                },
            )
            self.mark_current_channel_failed(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        wake = plan["safety"]["l3_wake"]
        current_events = [
            row for row in wake["observed_events"]
            if row["wake_source"] == "confirmed_current_channel_failure"
        ]
        self.assertFalse(gate["ok"])
        self.assertEqual(wake["decision"], "REJECT_WAKE")
        self.assertIn("rejected_wake_source_timer", gate["blockers"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertFalse(current_events[0]["consumed_by_runtime"])
        self.assertNotEqual(plan["summary"]["l3_incident_state"], "NO_INCIDENT_NO_EVIDENCE")

    def test_l3_wake_rejects_timer_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True, "wake_source": "timer"},
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertFalse(gate["ok"])
        self.assertEqual(plan["safety"]["l3_wake"]["decision"], "REJECT_WAKE")
        self.assertIn("rejected_wake_source_timer", gate["blockers"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertTrue(plan["summary"]["execution_blocked"])

    def test_l3_incident_key_merges_same_scope_and_splits_different_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root))

            first = planner._l3_incident_key(
                source_channels=["1"],
                services=["telegram"],
                authority="EMERGENCY_FAILOVER_AUTONOMY",
                generation="gen-1",
            )
            same = planner._l3_incident_key(
                source_channels=["1"],
                services=["telegram"],
                authority="EMERGENCY_FAILOVER_AUTONOMY",
                generation="gen-1",
            )
            split_source = planner._l3_incident_key(
                source_channels=["vless"],
                services=["telegram"],
                authority="EMERGENCY_FAILOVER_AUTONOMY",
                generation="gen-1",
            )
            split_service = planner._l3_incident_key(
                source_channels=["1"],
                services=["youtube"],
                authority="EMERGENCY_FAILOVER_AUTONOMY",
                generation="gen-1",
            )

        self.assertEqual(first["key"], same["key"])
        self.assertNotEqual(first["key"], split_source["key"])
        self.assertNotEqual(first["key"], split_service["key"])

    def test_l3_phase3_behavior_contracts_and_operator_surface_are_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            plan = planner.plan()

        incident = plan["safety"]["l3_incident"]
        contracts = incident["production_behavior_contracts"]
        behavior_names = {row["behavior"] for row in contracts["behaviors"]}
        self.assertEqual(contracts["schema_version"], "v7.l3-production-behavior-contracts.v1")
        self.assertTrue(contracts["all_required_behaviors_mapped"])
        self.assertFalse(contracts["new_behavior_framework_created"])
        self.assertEqual(
            behavior_names,
            {
                "Event Collapse",
                "Incident Merge",
                "Incident Split",
                "Retry Budget",
                "Backoff",
                "Target Lost Before Apply",
                "Partial Success",
                "Verification Timeout",
                "Unknown State Quarantine",
                "Recovery During Execution",
                "Recovery After Suspend",
                "Late Event Handling",
                "Budget Exhaustion",
                "Duplicate Event Suppression",
            },
        )
        surface = incident["operator_surface"]
        self.assertEqual(surface["schema_version"], "v7.l3-operator-surface.v1")
        self.assertEqual(surface["reason"], "CURRENT_CHANNEL_FAILED")
        self.assertEqual(surface["authority"], "EMERGENCY_FAILOVER_AUTONOMY")
        self.assertEqual(surface["execution_state"], "READY")
        self.assertFalse(surface["new_ui_framework_created"])
        self.assertEqual(plan["summary"]["l3_operator_surface"]["incident"], incident["incident_key"])
        self.assertEqual(plan["summary"]["l3_production_validation_ladder"]["schema_version"], "v7.l3-production-validation-ladder.v1")
        self.assertEqual(plan["summary"]["l3_certification_pipeline"]["schema_version"], "v7.l3-certification-pipeline.v1")

    def test_l3_retry_budget_exhaustion_blocks_without_new_incident_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True, "retry_budget_per_incident": 0},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            plan = planner.plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        incident = plan["safety"]["l3_incident"]
        budget = {
            row["behavior"]: row
            for row in incident["production_behavior_contracts"]["behaviors"]
        }["Budget Exhaustion"]
        self.assertFalse(gate["ok"])
        self.assertIn("l3_retry_budget_exhausted", gate["blockers"])
        self.assertEqual(budget["decision"], "STOP_SAFE_BUDGET_EXHAUSTED")
        self.assertEqual(budget["terminal_outcome"], "BUDGET_EXHAUSTED")
        self.assertFalse(incident["new_incident_framework_created"])

    def test_emergency_failover_autonomy_off_keeps_proposal_visible_but_not_executable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root))
            plan = planner.plan()

        self.assertFalse(plan["summary"]["emergency_failover_enabled"])
        self.assertGreater(plan["summary"]["proposal_moves_total"], 0)
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertTrue(plan["summary"]["execution_blocked"])

    def test_emergency_failover_autonomy_blocks_non_failover_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, emergency_failover_autonomy={"enabled": True})
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            selected = [{
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "vless",
                "move_type": "planned",
                "reason": ["candidate_score_beats_current"],
                "important_services": ["telegram"],
                "candidates": [
                    {"egress": "1", "eligible": False, "service_suitability": {"per_service": {"telegram": {"available": False, "status": "DOWN", "truth_class": "PERSISTENT_FAIL", "freshness": {"state": "FRESH"}}}}},
                    {"egress": "vless", "eligible": True, "service_suitability": {"per_service": {"telegram": {"available": True, "status": "OK", "freshness": {"state": "FRESH"}}}}},
                ],
            }]
            _, gate = planner._emergency_failover_authority_gate(selected, {"failover_quarantine": True})

        self.assertFalse(gate["ok"])
        self.assertIn("emergency_allows_failover_only", gate["blockers"])

    def test_emergency_failover_autonomy_blocks_recent_cooldown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True, "cooldown_seconds": 180},
            )
            (root / "events" / "switch-history.jsonl").write_text(
                json.dumps({"ts": self.tool.now_iso(), "user_ip": "10.0.0.2", "from": "vless", "to": "1"}) + "\n",
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        self.assertFalse(plan["safety"]["emergency_failover_autonomy"]["ok"])
        self.assertIn("emergency_failover_cooldown_active", plan["safety"]["emergency_failover_autonomy"]["blockers"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_active_l3_failed_source_incident_cooldown_does_not_trap_affected_user(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "failover_quarantine": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True, "cooldown_seconds": 180, "max_users_per_run": 1, "max_users_per_channel": 1},
            )
            policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            policy["switch"]["cooldown_seconds"] = 180
            (root / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
            (root / "events" / "switch-history.jsonl").write_text(
                json.dumps({"ts": self.tool.now_iso(), "user_ip": "10.0.0.2", "from": "vless", "to": "1"}) + "\n",
                encoding="utf-8",
            )
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        "incident-open-1": {
                            "incident_key": "incident-open-1",
                            "status": "OPEN",
                            "authority_object": "EMERGENCY_FAILOVER_AUTONOMY",
                            "failed_sources": ["1"],
                            "incident_source": "1",
                            "failed_required_services": ["telegram"],
                            "updated_at": "2999-01-01T00:00:00+00:00",
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        self.assertEqual(plan["summary"]["selected_moves"], 1)
        move = plan["selected_moves"][0]
        self.assertEqual(move["current_egress"], "1")
        self.assertEqual(move["move_type"], "failover")
        self.assertIn("l3_failed_source_cooldown_override", move["reason"])
        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertEqual(gate["selected_moves_after_gate"], 1)
        self.assertNotIn("emergency_failover_cooldown_active", gate["blockers"])
        self.assertIn("confirmed_current_channel_failure", plan["safety"]["l3_wake"]["accepted_wake_sources"])

    def test_requested_controlled_failed_source_cooldown_does_not_trap_certification_user(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                users=3,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "failover_quarantine": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True, "cooldown_seconds": 180, "max_users_per_run": 2, "max_users_per_channel": 2},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "authority_lifecycle_state": "CERTIFIED",
                    "current_allowed_user_budget": 2,
                },
            )
            policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            policy["switch"]["cooldown_seconds"] = 180
            (root / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
            egress_path = root / "state" / "egress.registry"
            egress_path.write_text(
                egress_path.read_text(encoding="utf-8").replace(
                    "id=1 interface=v7one enabled=1 state=enabled role=GLOBAL_FAST",
                    "id=1 interface=v7one enabled=0 role=GLOBAL_FAST controlled_certification_source=1 certification_group=medium-batch",
                ),
                encoding="utf-8",
            )
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                "\n".join(
                    row + " certification_user=1 certification_group=medium-batch"
                    for row in users_path.read_text(encoding="utf-8").strip().splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            state_path = root / "state" / "v7-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["users"] = [
                {"ip": f"10.0.0.{idx + 2}", "current": "1", "table": str(100 + idx), "enabled": "1"}
                for idx in range(3)
            ]
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (root / "events" / "switch-history.jsonl").write_text(
                "\n".join(
                    json.dumps({"ts": self.tool.now_iso(), "user_ip": f"10.0.0.{idx + 2}", "from": "vless", "to": "1"})
                    for idx in range(3)
                )
                + "\n",
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--max-selected-moves", "2", "--source-egress", "1"])
            )
            plan = planner.plan()

        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertEqual(plan["safety"]["l3_wake"]["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_current_channel_failure", plan["safety"]["l3_wake"]["accepted_wake_sources"])
        self.assertTrue(all(move["current_egress"] == "1" for move in plan["selected_moves"]))
        self.assertTrue(all("l3_failed_source_cooldown_override" in move["reason"] for move in plan["selected_moves"]))

    def test_emergency_failover_autonomy_blocks_stale_service_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        gate = plan["safety"]["emergency_failover_autonomy"]
        self.assertFalse(gate["ok"])
        self.assertIn("fresh_service_failure_evidence_required", gate["blockers"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertTrue(plan["summary"]["execution_blocked"])
        self.assertEqual(plan["summary"]["execution_blocker"], "emergency_failover_autonomy")

    def test_emergency_failover_autonomy_blocks_when_rollback_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--no-rollback-on-verify-fail"])
            )
            plan = planner.plan()

        self.assertIn("rollback_required_for_emergency_failover", plan["safety"]["emergency_failover_autonomy"]["blockers"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_emergency_failover_autonomy_blocks_when_no_safe_target_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["vless"]["services"]["telegram"] = {
                "ok": False,
                "status": "DOWN",
                "score": 0,
                "consecutive_failures": 3,
                "tested_at": fresh,
            }
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--emergency-failover-autonomy"]))
            plan = planner.plan()

        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertTrue(plan["summary"]["execution_blocked"])
        self.assertIn("no_selected_moves_for_emergency_failover", plan["safety"]["emergency_failover_autonomy"]["blockers"])

    def test_emergency_apply_success_verifies_required_services(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            switch_calls = []
            planner._run_switch = lambda ip, egress, reason: switch_calls.append((ip, egress, reason)) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 0, stdout="service ok\n")
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover")])
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(plan["operation"]["terminal_state"], "APPLIED")
        self.assertEqual(plan["apply_result"]["results"][0]["service_verify_rc"], 0)
        self.assertEqual(plan["apply_result"]["results"][0]["terminal_outcome_classification"], "SUCCESS")
        self.assertTrue(plan["apply_result"]["l3_execution_eligibility"]["ok"])
        self.assertEqual(plan["safety"]["l3_execution_eligibility"]["decision"], "EXECUTE")
        self.assertEqual(plan["safety"]["l3_incident"]["terminal_outcome"], "SUCCESS")
        self.assertEqual(plan["safety"]["l3_incident"]["operator_surface"]["execution_state"], "TERMINAL")
        self.assertEqual(plan["safety"]["l3_incident"]["operator_surface"]["terminal_outcome"], "SUCCESS")
        self.assertEqual(plan["safety"]["l3_incident"]["operator_surface"]["next_action"], "close_outcome_and_report")

    def test_emergency_service_verification_parent_timeout_includes_lock_timeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(
                    root,
                    [
                        "--emergency-failover-autonomy",
                        "--mode",
                        "guarded",
                        "--apply",
                        "--service-matrix-lock-timeout-sec",
                        "17",
                    ],
                )
            )
            captured = {}
            original_run = self.tool.subprocess.run

            def fake_run(command, **kwargs):
                captured["command"] = command
                captured["timeout"] = kwargs.get("timeout")
                return subprocess.CompletedProcess(command, 0, stdout="service ok\n")

            try:
                self.tool.subprocess.run = fake_run
                proc = planner._verify_emergency_required_services({
                    "recommended_egress": "vless",
                    "important_services": ["telegram"],
                })
            finally:
                self.tool.subprocess.run = original_run

        self.assertEqual(proc.returncode, 0)
        self.assertIn("--lock-timeout-sec", captured["command"])
        self.assertIn("--services", captured["command"])
        self.assertEqual(
            captured["command"][captured["command"].index("--services") + 1],
            "telegram",
        )
        self.assertEqual(captured["command"][captured["command"].index("--lock-timeout-sec") + 1], "17")
        self.assertEqual(captured["timeout"], 27)

    def test_emergency_apply_service_verification_failure_rolls_back_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            switch_calls = []
            planner._run_switch = lambda ip, egress, reason: switch_calls.append((ip, egress, reason)) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 1, stdout="service fail\n")
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover"), ("10.0.0.2", "1", "rollback")])
        row = plan["apply_result"]["results"][0]
        self.assertEqual(row["verification_failure_reason"], "required_service_verify_failed")
        self.assertEqual(row["rollback_verdict"], "ROLLBACK_COMPLETED")
        self.assertEqual(row["terminal_outcome_classification"], "ROLLBACK_SUCCESS")
        self.assertEqual(plan["safety"]["l3_incident"]["terminal_outcome"], "ROLLBACK_SUCCESS")
        self.assertEqual(plan["operation"]["terminal_state"], "ROLLED_BACK")

    def test_availability_first_execution_eligibility_does_not_require_failed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                current_egress="vless",
                vless_registry_extra=(
                    " controlled_certification_source=1"
                ),
                emergency_failover_autonomy={"enabled": True},
            )
            (root / "state" / "users.registry").write_text(
                (
                    "ip=10.7.0.100 current=vless table=1098 enabled=1 "
                    "certification_user=1\n"
                ),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(
                    root,
                    [
                        "--emergency-failover-autonomy",
                        "--mode", "guarded",
                        "--apply",
                        "--user", "10.7.0.100",
                        "--source-egress", "vless",
                        "--target-egress", "1",
                    ],
                )
            )
            move = {
                "user_ip": "10.7.0.100",
                "current_egress": "vless",
                "recommended_egress": "1",
                "move_type": "failover",
                "execution_mode": "emergency_failover",
                "operation_id": "availability-operation",
                "selected_move_hash": "availability-hash",
                "availability_first_controlled_assignment": {
                    "schema_version": (
                        "v7.availability-first-controlled-selection.v1"
                    ),
                    "event_provenance": "CONTROLLED_CERTIFICATION",
                    "natural_production_credit": False,
                    "source": "vless",
                    "target": "1",
                    "allocation_fingerprint": "d" * 64,
                    "ordinary_user": False,
                },
            }
            plan = {
                "summary": {"execution_mode": "emergency_failover"},
                "operation": {
                    "operation_id": "availability-operation",
                    "selected_move_hash": "availability-hash",
                },
                "selected_moves": [move],
                "safety": {
                    "emergency_failover_autonomy": {
                        "enabled": True,
                        "ok": True,
                        "approved_production_validation_envelope": {
                            "ok": True,
                        },
                    },
                    "restore_barrier": {
                        "clearance_max_selected_moves": 1,
                        "approved_plan_lock_validation": {
                            "ok": True,
                            "selected_move_count": 1,
                        },
                    },
                },
            }
            with mock.patch.object(
                planner,
                "_exact_availability_first_controlled_scope",
                return_value={
                    "ok": True,
                    "sources": ["vless"],
                    "targets": ["1"],
                    "natural_production_credit": False,
                },
            ), mock.patch.object(
                planner,
                "_emergency_failover_move_evidence",
            ) as ordinary_evidence:
                eligibility = planner._l3_execution_eligibility(plan)

        self.assertTrue(eligibility["ok"])
        self.assertEqual(eligibility["decision"], "EXECUTE")
        self.assertEqual(eligibility["blockers"], [])
        self.assertTrue(
            eligibility["availability_first_controlled_scope"]["ok"]
        )
        ordinary_evidence.assert_not_called()

    def test_ct_m0f_standing_reset_does_not_require_failed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                current_egress="1",
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(
                    root,
                    [
                        "--emergency-failover-autonomy",
                        "--mode", "guarded",
                        "--apply",
                        "--user", "10.0.0.2",
                        "--source-egress", "1",
                        "--target-egress", "vless",
                        "--ct-m0f-standing-reset-reservation-id",
                        "ctm0fsample_test",
                    ],
                )
            )
            move = {
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "vless",
                "move_type": "failover",
                "execution_mode": "emergency_failover",
                "operation_id": "ct-reset-operation",
                "selected_move_hash": "ct-reset-hash",
            }
            plan = {
                "summary": {"execution_mode": "emergency_failover"},
                "operation": {
                    "operation_id": "ct-reset-operation",
                    "selected_move_hash": "ct-reset-hash",
                },
                "selected_moves": [move],
                "safety": {
                    "emergency_failover_autonomy": {
                        "enabled": True,
                        "ok": False,
                    },
                    "l3_wake": {"accepted": False},
                    "l3_incident": {"incident_state": "RECOVERED"},
                    "restore_barrier": {
                        "clearance_max_selected_moves": 1,
                        "approved_plan_lock_validation": {
                            "ok": True,
                            "selected_move_count": 1,
                        },
                    },
                },
            }
            with mock.patch.object(
                planner,
                "_exact_availability_first_controlled_scope",
                return_value={"ok": False, "reasons": ["not_applicable"]},
            ), mock.patch.object(
                planner,
                "_exact_ct_m0f_standing_reset_scope",
                return_value={
                    "ok": True,
                    "reservation_id": "ctm0fsample_test",
                    "natural_production_credit": False,
                },
            ), mock.patch.object(
                planner,
                "_emergency_failover_move_evidence",
            ) as ordinary_evidence:
                eligibility = planner._l3_execution_eligibility(plan)

        self.assertTrue(eligibility["ok"], eligibility)
        self.assertEqual(eligibility["decision"], "EXECUTE")
        self.assertEqual(eligibility["blockers"], [])
        self.assertTrue(eligibility["ct_m0f_standing_reset_scope"]["ok"])
        ordinary_evidence.assert_not_called()

    def test_ct_m0f_standing_reset_reads_rotated_live_lineage(self):
        source = (ROOT / "tools" / "v7-users-autoswitch").read_text(
            encoding="utf-8"
        )
        start = source.index("def _exact_ct_m0f_standing_reset_scope")
        end = source.index("def _activate_controlled_verifier_contention", start)
        reset_scope = source[start:end]
        self.assertIn("read_live_execution_lineage_records", reset_scope)
        self.assertNotIn("read_audit_records(audit_store)", reset_scope)

    def test_l3_execution_stops_safe_when_target_lost_before_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            plan = planner.plan()
            switch_calls = []
            planner._run_switch = lambda *args, **kwargs: switch_calls.append(args) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._load_egress = lambda: {key: value for key, value in planner.egress.items() if key != "vless"}
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(switch_calls, [])
        self.assertFalse(plan["apply_result"]["applied"])
        self.assertEqual(plan["apply_result"]["reason"], "l3_execution_eligibility_stop_safe")
        self.assertIn("target_lost_before_apply", plan["apply_result"]["unsafe_blocker"])
        self.assertEqual(plan["safety"]["l3_execution_eligibility"]["decision"], "STOP_SAFE")
        self.assertEqual(plan["safety"]["l3_incident"]["terminal_outcome"], "STOP_SAFE")
        self.assertEqual(plan["safety"]["l3_incident"]["operator_surface"]["execution_state"], "STOP_SAFE")
        self.assertEqual(plan["operation"]["terminal_state"], "DENIED")

    def test_l3_unknown_incident_state_stops_safe_before_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            plan = planner.plan()
            plan["safety"]["l3_incident"]["incident_state"] = "UNKNOWN_STATE"
            switch_calls = []
            planner._run_switch = lambda *args, **kwargs: switch_calls.append(args) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            plan["apply_result"] = planner.apply(plan)

        self.assertEqual(switch_calls, [])
        self.assertFalse(plan["apply_result"]["applied"])
        self.assertEqual(plan["apply_result"]["reason"], "l3_execution_eligibility_stop_safe")
        self.assertIn("l3_incident_not_ready", plan["apply_result"]["unsafe_blocker"])
        self.assertEqual(plan["safety"]["l3_incident"]["operator_surface"]["execution_state"], "STOP_SAFE")

    def test_emergency_apply_service_verification_timeout_rolls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            switch_calls = []
            planner._run_switch = lambda ip, egress, reason: switch_calls.append((ip, egress, reason)) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 1, stdout="service verify error: timeout\n")
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        row = plan["apply_result"]["results"][0]
        self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover"), ("10.0.0.2", "1", "rollback")])
        self.assertEqual(row["verification_failure_reason"], "required_service_verify_timeout")
        self.assertEqual(row["rollback_verdict"], "ROLLBACK_COMPLETED")
        self.assertEqual(row["terminal_outcome_classification"], "ROLLBACK_SUCCESS")

    def test_emergency_apply_rollback_failure_is_terminal_rollback_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            switch_calls = []

            def fake_run_switch(ip, egress, reason):
                switch_calls.append((ip, egress, reason))
                rc = 1 if reason == "rollback" else 0
                return subprocess.CompletedProcess(["v7-user-switch"], rc, stdout=("rollback failed\n" if rc else "ok\n"))

            planner._run_switch = fake_run_switch
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 1, stdout="service fail\n")
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        row = plan["apply_result"]["results"][0]
        self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover"), ("10.0.0.2", "1", "rollback")])
        self.assertEqual(row["rollback_verdict"], "ROLLBACK_FAILED")
        self.assertEqual(row["terminal_outcome_classification"], "ROLLBACK_FAILURE")
        self.assertEqual(plan["operation"]["terminal_state"], "ROLLBACK_FAILED")
        self.assertEqual(plan["safety"]["l3_incident"]["terminal_outcome"], "ROLLBACK_FAILURE")

    def test_l3_success_closes_learning_evidence_capability_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            (root / "events" / "l3-wake-events.jsonl").write_text(
                json.dumps({
                    "event_id": "evt-l3-service-failure",
                    "wake_source": "confirmed_service_failure",
                    "channel": "1",
                    "service": "telegram",
                    "ts": fresh,
                }) + "\n",
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            switch_calls = []
            planner._run_switch = lambda ip, egress, reason: switch_calls.append((ip, egress, reason)) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 0, stdout="service ok\n")
            planner._emit_terminal_audit = lambda audit: {**audit, "emitted": True, "status": "emitted"}
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

            self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover")])
            self.assertTrue(plan["l3_learning_closure"]["materialized"])
            self.assertTrue(plan["l3_learning_closure"]["capability_state"]["active_capability"])
            closure = plan["l3_learning_closure"]["execution_closure_verification"]
            self.assertEqual(closure["schema_version"], "v7.l3-execution-closure-verification.v1")
            self.assertEqual(closure["behavior_chain_status"], "COMPLETE")
            self.assertTrue(closure["ready_for_safe_deploy"])
            self.assertTrue(closure["terminal_consumer_verified"])
            self.assertEqual(closure["broken_chains"], [])
            self.assertEqual(
                [row["stage"] for row in closure["chains"]],
                [
                    "Wake",
                    "Incident",
                    "Planner",
                    "Authority",
                    "Eligibility",
                    "Execution",
                    "Verification",
                    "Rollback or Success",
                    "Learning",
                    "Evidence",
                    "Capability State",
                    "OMP",
                    "Next Runtime Cycle",
                ],
            )
            for row in closure["chains"]:
                self.assertEqual(row["output_produced"], "PASS")
                self.assertEqual(row["output_consumed"], "PASS")
                self.assertEqual(row["consumption_verified"], "PASS")
                self.assertEqual(row["behavior_changed"], "PASS")
                self.assertEqual(row["next_output_produced"], "PASS")
            self.assertIn("evt-l3-service-failure", plan["safety"]["l3_wake"]["consumed_event_ids"])
            self.assertEqual(plan["safety"]["l3_execution_closure_verification"]["behavior_chain_status"], "COMPLETE")
            runtime_state = json.loads((root / "state" / "l3-runtime-state.json").read_text(encoding="utf-8"))
            incident = runtime_state["incidents"][plan["safety"]["l3_incident"]["incident_key"]]
            self.assertEqual(incident["status"], "CLOSED")
            self.assertEqual(incident["attempt_count"], 1)
            self.assertTrue(incident["feeds_next_runtime_cycle"])
            capability_state = json.loads((root / "state" / "l3-capability-state.json").read_text(encoding="utf-8"))
            self.assertEqual(capability_state["state"], "ACTIVE_CAPABILITY")
            self.assertTrue((root / "state" / "execution-events.jsonl").read_text(encoding="utf-8"))
            self.assertTrue((root / "state" / "runtime-trust.jsonl").read_text(encoding="utf-8"))
            self.assertTrue((root / "state" / "proposal-records.jsonl").read_text(encoding="utf-8"))
            self.assertTrue((root / "state" / "closure-records.jsonl").read_text(encoding="utf-8"))

    def test_l3_persistent_retry_budget_blocks_second_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True, "retry_budget_per_incident": 1},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            planner._run_switch = lambda ip, egress, reason: subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 0, stdout="service ok\n")
            planner._emit_terminal_audit = lambda audit: {**audit, "emitted": True, "status": "emitted"}
            first = planner.plan()
            first["apply_result"] = planner.apply(first)
            planner.finalize_operation(first)

            second_planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            second = second_planner.plan()

        self.assertFalse(second["safety"]["emergency_failover_autonomy"]["ok"])
        self.assertIn("l3_retry_budget_exhausted", second["safety"]["emergency_failover_autonomy"]["blockers"])
        self.assertEqual(second["summary"]["selected_moves"], 0)

    def test_l3_retry_budget_ignores_denied_no_execution_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True, "retry_budget_per_incident": 1},
            )
            first = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            ).plan()
            gate = first["safety"]["emergency_failover_autonomy"]
            incident_key = gate["incident_key"]
            signature = gate["semantic_attempt_signature"]
            (root / "state" / "l3-runtime-state.json").write_text(
                json.dumps({
                    "schema_version": "v7.l3-runtime-state.v1",
                    "incidents": {
                        incident_key: {
                            "incident_key": incident_key,
                            "attempts": [
                                {
                                    "operation_id": "runtime-autoswitch-denied",
                                    "selected_move_hash": first["operation"]["selected_move_hash"],
                                    "semantic_attempt_signature": signature,
                                    "terminal_outcome": "STOP_SAFE",
                                    "terminal_state": "DENIED",
                                    "applied": False,
                                }
                            ],
                        }
                    },
                    "processed_event_ids": [],
                    "capability": {},
                }),
                encoding="utf-8",
            )
            second = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            ).plan()

        second_gate = second["safety"]["emergency_failover_autonomy"]
        self.assertTrue(second_gate["ok"])
        self.assertEqual(second_gate["previous_attempts"], 0)
        self.assertNotIn("l3_retry_budget_exhausted", second_gate["blockers"])
        self.assertNotIn("duplicate_apply_attempt", second_gate["blockers"])
        self.assertEqual(second["summary"]["selected_moves"], 1)

    def test_l3_recovery_before_apply_stops_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fresh = "2999-01-01T00:00:00+00:00"
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0, "consecutive_failures": 3, "tested_at": fresh}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
                emergency_failover_autonomy={"enabled": True},
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--mode", "guarded", "--apply"])
            )
            plan = planner.plan()
            for candidate in plan["selected_moves"][0]["candidates"]:
                if candidate["egress"] == "1":
                    candidate["service_suitability"]["per_service"]["telegram"] = {
                        "available": True,
                        "status": "OK",
                        "freshness": {"state": "FRESH"},
                    }
            switch_calls = []
            planner._run_switch = lambda *args, **kwargs: switch_calls.append(args) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            plan["apply_result"] = planner.apply(plan)

        self.assertEqual(switch_calls, [])
        self.assertFalse(plan["apply_result"]["applied"])
        self.assertIn("source_recovered_before_apply", plan["apply_result"]["unsafe_blocker"])

    def test_apply_verify_failure_records_operation_rollback_and_audit_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"instagram": {"ok": False, "score": 0, "consecutive_failures": 3}},
            )
            plan, switch_calls = self.apply_plan_with_mocks(root)
            self.assert_operation_envelope(plan)
            self.assertEqual(plan["operation"]["terminal_state"], "ROLLED_BACK")
            self.assertEqual(plan["operation"]["terminal_reason"], "verification_failed_rollback_completed")
            self.assertEqual(plan["operation"]["rollback_verdict"], "ROLLBACK_COMPLETED")
            self.assertEqual(len(switch_calls), 2)
            self.assertEqual(switch_calls[0][2], "failover")
            self.assertEqual(switch_calls[1][2], "rollback")
            row = plan["apply_result"]["results"][0]
            self.assertEqual(row["operation_id"], plan["operation"]["operation_id"])
            self.assertEqual(row["selected_move_hash"], plan["operation"]["selected_move_hash"])
            self.assertEqual(row["selected_move_index"], 0)
            self.assertTrue(row["rollback_attempted"])
            self.assertEqual(row["rollback_result"], "OK")
            self.assertEqual(row["rollback_verdict"], "ROLLBACK_COMPLETED")
            self.assertTrue(plan["audit"]["emitted"])
            self.assertEqual(plan["audit"]["status"], "emitted")
            self.assertEqual(plan["closure_target"]["closure_state"], "VERIFIED_READY")
            self.assertEqual(plan["closure_target"]["closure_blocker"], "")

    def test_emergency_batch_apply_uses_scoped_route_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root, users=2)
            plan["summary"]["execution_mode"] = "emergency_failover"
            plan["safety"]["emergency_failover_autonomy"].update({
                "enabled": True,
                "ok": True,
                "decision": "authorized",
                "approved_production_validation_envelope": {"ok": True},
            })
            plan["safety"]["l3_wake"].update({"accepted": True, "decision": "ACCEPT_WAKE"})
            plan["safety"]["l3_incident"].update({"incident_state": "READY_FOR_EXECUTION"})
            plan["safety"]["restore_barrier"]["approved_plan_lock_validation"] = {
                "ok": True,
                "selected_move_count": len(plan["selected_moves"]),
            }
            plan["safety"]["restore_barrier"]["clearance_max_selected_moves"] = len(plan["selected_moves"])
            for move in plan["selected_moves"]:
                move["execution_mode"] = "emergency_failover"
            planner.emergency_failover_policy["require_fresh_evidence"] = False
            selected_users = [move["user_ip"] for move in plan["selected_moves"]]
            selected_targets = [move["recommended_egress"] for move in plan["selected_moves"]]
            verify_calls = []

            def fake_verify_routes(user_ip: str = "", expected_egress: str = ""):
                verify_calls.append((user_ip, expected_egress))
                if not user_ip:
                    return subprocess.CompletedProcess(["v7-user-route-check"], 1, stdout="global remaining users failed\n")
                return subprocess.CompletedProcess(
                    ["v7-users-autoswitch", "--verify-user-route", user_ip, expected_egress],
                    0,
                    stdout=f"scoped verify ok {user_ip} {expected_egress}\n",
                )

            planner._verify_routes = fake_verify_routes
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(
                ["v7-service-matrix-test"],
                0,
                stdout="service verify ok\n",
            )
            plan["apply_result"] = planner.apply(plan)

        self.assertEqual([call[0] for call in switch_calls], selected_users)
        self.assertEqual(verify_calls, list(zip(selected_users, selected_targets)))
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertTrue(all(row["verify_rc"] == 0 for row in plan["apply_result"]["results"]))
        self.assertTrue(all(not row["rollback_attempted"] for row in plan["apply_result"]["results"]))
        self.assertTrue(all(row["terminal_outcome_classification"] == "SUCCESS" for row in plan["apply_result"]["results"]))

    def test_committed_emergency_moves_keep_scoped_verification_without_summary_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root, users=2)
            plan["safety"]["emergency_failover_autonomy"].update({
                "enabled": True,
                "ok": True,
                "decision": "authorized",
                "approved_production_validation_envelope": {"ok": True},
            })
            plan["safety"]["l3_wake"].update({"accepted": True, "decision": "ACCEPT_WAKE"})
            plan["safety"]["l3_incident"].update({"incident_state": "READY_FOR_EXECUTION"})
            committed_moves = json.loads(json.dumps(plan["selected_moves"]))
            selected_users = [move["user_ip"] for move in committed_moves]
            selected_targets = [move["recommended_egress"] for move in committed_moves]
            plan["safety"]["restore_barrier"]["approved_plan_lock_validation"] = {
                "present": True,
                "ok": True,
                "reason": "approved_plan_lock_valid",
                "selected_move_hash": plan["operation"]["selected_move_hash"],
                "selected_move_count": len(committed_moves),
                "selected_moves": committed_moves,
            }
            plan["safety"]["restore_barrier"]["clearance_max_selected_moves"] = len(committed_moves)
            plan["selected_moves"] = []
            plan["summary"].pop("execution_mode", None)
            plan["summary"]["selected_moves"] = 0
            planner.emergency_failover_policy["require_fresh_evidence"] = False
            verify_calls = []

            def fake_verify_routes(user_ip: str = "", expected_egress: str = ""):
                verify_calls.append((user_ip, expected_egress))
                if not user_ip:
                    return subprocess.CompletedProcess(["v7-user-route-check"], 1, stdout="global verify should not run\n")
                return subprocess.CompletedProcess(
                    ["v7-users-autoswitch", "--verify-user-route", user_ip, expected_egress],
                    0,
                    stdout=f"scoped verify ok {user_ip} {expected_egress}\n",
                )

            planner._verify_routes = fake_verify_routes
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(
                ["v7-service-matrix-test"],
                0,
                stdout="service verify ok\n",
            )
            plan["apply_result"] = planner.apply(plan)

        self.assertEqual([call[0] for call in switch_calls], selected_users)
        self.assertEqual(verify_calls, list(zip(selected_users, selected_targets)))
        self.assertNotEqual(plan["summary"].get("execution_mode"), "emergency_failover")
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertTrue(all(row["route_verification_scope"] == "selected_user" for row in plan["apply_result"]["results"]))
        self.assertEqual(
            [row["route_verification_expected_egress"] for row in plan["apply_result"]["results"]],
            selected_targets,
        )
        self.assertTrue(all(row["terminal_outcome_classification"] == "SUCCESS" for row in plan["apply_result"]["results"]))

    def test_strict_one_user_contract_uses_scoped_route_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, _switch_calls = self.governed_source_bundle_lease_plan(
                root, users=1, max_selected_moves=1
            )
            move = plan["selected_moves"][0]
            plan["safety"].setdefault("authority_budget_gate", {})[
                "current_action_class_contract"
            ] = {
                "contract_id": "acc_strict_scope_unit",
                "contract_hash": "strict-scope-hash",
                "provenance": {"strict_provenance_contract": True},
            }
            verify_calls = []

            def fake_verify_routes(user_ip: str = "", expected_egress: str = ""):
                verify_calls.append((user_ip, expected_egress))
                if not user_ip:
                    return subprocess.CompletedProcess(
                        ["v7-user-route-check"], 1, stdout="global verify must not run\n"
                    )
                return subprocess.CompletedProcess(
                    ["v7-users-autoswitch", "--verify-user-route", user_ip],
                    1,
                    stdout=(
                        "scoped verify failed\n"
                        "V7_SCOPED_USER_ROUTE_FAILURE_CATEGORIES=TABLE_DEFAULT_MISMATCH\n"
                    ),
                )

            planner._verify_routes = fake_verify_routes
            with mock.patch.object(
                self.tool.operator_execution,
                "consume_current_action_class_contract_to_policy",
                return_value={
                    "policy": planner.policy,
                    "consumption": {"state": "CONSUMED", "consumption_id": "acc-consume-unit"},
                },
            ):
                result = planner.apply(plan)

        self.assertTrue(result["applied"])
        self.assertEqual(verify_calls, [(move["user_ip"], move["recommended_egress"])])
        row = result["results"][0]
        self.assertEqual(row["route_verification_scope"], "selected_user")
        self.assertEqual(row["route_verification_expected_egress"], move["recommended_egress"])
        self.assertEqual(
            row["route_verification_failure_categories"],
            ["TABLE_DEFAULT_MISMATCH"],
        )

    def test_global_route_verification_failure_does_not_quarantine_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            planner._update_safety_after_apply([
                {
                    "user_ip": "10.0.0.2",
                    "from": "1",
                    "to": "vless",
                    "move_type": "failover",
                    "rc": 0,
                    "verify_rc": 1,
                    "route_verification_scope": "global",
                    "verification_failure_reason": "route_verify_failed",
                },
                {
                    "user_ip": "10.0.0.3",
                    "from": "1",
                    "to": "vless",
                    "move_type": "failover",
                    "rc": 0,
                    "verify_rc": 1,
                    "route_verification_scope": "global",
                    "verification_failure_reason": "route_verify_failed",
                },
            ])
            safety = json.loads((root / "state" / "autoswitch-safety.json").read_text(encoding="utf-8"))

        target = safety["egress"]["vless"]
        self.assertIsNone(target.get("quarantine_until"))
        self.assertEqual(target["failed_verifications_1h"], 0)
        self.assertEqual(target["failed_verifications_1h_unattributed"], 2)

    def test_selected_user_route_verification_failure_still_quarantines_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            planner._update_safety_after_apply([
                {
                    "user_ip": "10.0.0.2",
                    "from": "1",
                    "to": "vless",
                    "move_type": "failover",
                    "rc": 0,
                    "verify_rc": 1,
                    "route_verification_scope": "selected_user",
                    "route_verification_expected_egress": "vless",
                    "verification_failure_reason": "route_verify_failed",
                },
                {
                    "user_ip": "10.0.0.3",
                    "from": "1",
                    "to": "vless",
                    "move_type": "failover",
                    "rc": 0,
                    "verify_rc": 1,
                    "route_verification_scope": "selected_user",
                    "route_verification_expected_egress": "vless",
                    "verification_failure_reason": "route_verify_failed",
                },
            ])
            safety = json.loads((root / "state" / "autoswitch-safety.json").read_text(encoding="utf-8"))

        target = safety["egress"]["vless"]
        self.assertTrue(target.get("quarantine_until"))
        self.assertEqual(target["quarantine_reason"], "selected_user_route_verification_failed")
        self.assertEqual(target["failed_verifications_1h"], 2)
        self.assertEqual(target["failed_verifications_1h_unattributed"], 0)

    def test_legacy_selected_user_failures_without_expected_target_do_not_keep_quarantine(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            safety_path = root / "state" / "autoswitch-safety.json"
            safety_path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "users": {},
                    "egress": {
                        "vless": {
                            "failed_verifications": [
                                {
                                    "ts": "2999-01-01T00:00:00+00:00",
                                    "user_ip": "10.0.0.2",
                                    "verify_rc": 1,
                                    "verification_scope": "selected_user_route_check",
                                    "verification_failure_reason": "route_verify_failed",
                                },
                                {
                                    "ts": "2999-01-01T00:00:01+00:00",
                                    "user_ip": "10.0.0.3",
                                    "verify_rc": 1,
                                    "verification_scope": "selected_user_route_check",
                                    "verification_failure_reason": "route_verify_failed",
                                },
                            ],
                            "quarantine_until": "2999-01-01T01:00:00+00:00",
                        }
                    },
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root))
            compacted = planner._load_safety()

        target = compacted["egress"]["vless"]
        self.assertIsNone(target.get("quarantine_until"))
        self.assertEqual(target["failed_verifications_1h"], 0)
        self.assertEqual(target["failed_verifications_1h_unattributed"], 2)
        self.assertEqual(target["quarantine_clear_reason"], "unattributed_route_verification_not_counted")

    def test_legacy_unscoped_failed_verifications_do_not_keep_quarantine(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            safety_path = root / "state" / "autoswitch-safety.json"
            safety_path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "users": {},
                    "egress": {
                        "vless": {
                            "failed_verifications": [
                                {"ts": "2999-01-01T00:00:00+00:00", "user_ip": "10.0.0.2", "verify_rc": 1},
                                {"ts": "2999-01-01T00:00:01+00:00", "user_ip": "10.0.0.3", "verify_rc": 1},
                            ],
                            "quarantine_until": "2999-01-01T01:00:00+00:00",
                        }
                    },
                }),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(self.args_for(root))
            target = planner.safety_state["egress"]["vless"]

        self.assertIsNone(target.get("quarantine_until"))
        self.assertEqual(target["quarantine_clear_reason"], "unattributed_route_verification_not_counted")
        self.assertEqual(target["failed_verifications_1h"], 0)
        self.assertEqual(target["failed_verifications_1h_unattributed"], 2)

    def test_apply_partial_success_is_classified_without_new_execution_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"instagram": {"ok": False, "score": 0, "consecutive_failures": 3}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--apply"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            self.assertEqual(plan["summary"]["selected_moves"], 2)
            switch_calls = []

            def fake_run_switch(ip, egress, reason):
                switch_calls.append((ip, egress, reason))
                rc = 1 if ip == "10.0.0.3" else 0
                return subprocess.CompletedProcess(["v7-user-switch"], rc, stdout=("fail\n" if rc else "ok\n"))

            planner._run_switch = fake_run_switch
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(len(switch_calls), 2)
        self.assertEqual(plan["operation"]["terminal_state"], "PARTIAL_SUCCESS")
        self.assertEqual(plan["operation"]["terminal_reason"], "partial_apply_failure")
        self.assertEqual([row["terminal_outcome_classification"] for row in plan["apply_result"]["results"]], ["SUCCESS", "APPLY_FAILURE"])

    def test_apply_stops_when_atomic_envelope_source_changes_before_switch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"instagram": {"ok": False, "score": 0, "consecutive_failures": 3}},
            )
            args = self.args_for(root, ["--apply"])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            self.assertEqual(plan["summary"]["selected_moves"], 1)
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            planner._run_switch = fake_run_switch
            matrix_path = root / "state" / "service-matrix.json"
            matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix_payload["items"]["1"]["services"]["youtube"]["score"] = 1
            matrix_path.write_text(json.dumps(matrix_payload), encoding="utf-8")
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(switch_calls, [])
        self.assertFalse(plan["apply_result"]["applied"])
        self.assertEqual(plan["operation"]["terminal_state"], "DENIED")
        self.assertEqual(plan["operation"]["terminal_reason"], "atomic_execution_envelope_source_changed")
        validation = plan["safety"]["atomic_execution_envelope_validation"]
        self.assertFalse(validation["ok"])
        self.assertEqual(validation["state"]["condition"], "SOURCE_CHANGED")
        self.assertIn("source_bundle_hash", validation["state"]["mismatches"])

    def test_governed_apply_accepts_service_matrix_drift_with_source_bundle_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root)
            self.assertEqual(plan["summary"]["selected_moves"], 2)
            matrix_path = root / "state" / "service-matrix.json"
            matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix_payload["items"]["1"]["services"]["youtube"]["score"] = 99
            matrix_path.write_text(json.dumps(matrix_payload), encoding="utf-8")
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(len(switch_calls), 2)
        self.assertEqual({call[0] for call in switch_calls}, {"10.0.0.2", "10.0.0.3"})
        self.assertEqual({call[1] for call in switch_calls}, {"vless"})
        validation = plan["safety"]["atomic_execution_envelope_validation"]
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["source_bundle_stability_lease_used"])
        self.assertEqual(validation["changed_source_keys"], ["service_matrix"])
        self.assertEqual(validation["state"]["condition"], "SOURCE_BUNDLE_LEASE_VALID")

    def test_governed_apply_accepts_restore_barrier_prevalidated_source_bundle_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root)
            plan.setdefault("safety", {}).setdefault("intelligence_snapshots", {}).pop("source_bundle_lease_used", None)
            plan["safety"]["intelligence_snapshots"].pop("pre_planner_refresh", None)
            planner.pre_planner_refresh = {}
            matrix_path = root / "state" / "service-matrix.json"
            matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix_payload["items"]["1"]["services"]["youtube"]["score"] = 97
            matrix_path.write_text(json.dumps(matrix_payload), encoding="utf-8")
            plan["safety"]["restore_barrier"]["clearance_generation_reason"] = (
                "restore_barrier_clearance_generation_match_source_bundle_lease"
            )
            plan["safety"]["restore_barrier"]["source_bundle_lease"] = {
                "ok": True,
                "reason": "restore_barrier_source_bundle_lease_service_matrix_only",
                "changed_source_keys": ["service_matrix"],
            }
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(len(switch_calls), 2)
        validation = plan["safety"]["atomic_execution_envelope_validation"]
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["source_bundle_stability_lease_used"])
        self.assertTrue(validation["prevalidated_restore_barrier_lease_used"])
        self.assertEqual(validation["changed_source_keys"], ["service_matrix"])
        self.assertEqual(validation["state"]["condition"], "SOURCE_BUNDLE_LEASE_VALID")

    def test_governed_apply_accepts_stable_bundle_without_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root)
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(len(switch_calls), 2)
        validation = plan["safety"]["atomic_execution_envelope_validation"]
        self.assertTrue(validation["ok"])
        self.assertFalse(validation.get("source_bundle_stability_lease_used", False))
        self.assertEqual(validation["state"]["condition"], "ENVELOPE_VALID")

    def test_restore_barrier_accepts_service_matrix_only_source_bundle_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, _switch_calls = self.governed_source_bundle_lease_plan(root)
            self.assertEqual(plan["summary"]["selected_moves"], 2)
            matrix_path = root / "state" / "service-matrix.json"
            matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix_payload["items"]["1"]["services"]["youtube"]["score"] = 88
            matrix_path.write_text(json.dumps(matrix_payload), encoding="utf-8")
            replanned = self.tool.AutoswitchPlanner(planner.args).plan()

        barrier = replanned["safety"]["restore_barrier"]
        self.assertEqual(replanned["summary"]["selected_moves"], 2)
        self.assertTrue(barrier["clearance_generation_ok"])
        self.assertEqual(
            barrier["clearance_generation_reason"],
            "restore_barrier_clearance_generation_match_source_bundle_lease",
        )
        self.assertTrue(barrier["source_bundle_lease"]["ok"])
        self.assertEqual(barrier["source_bundle_lease"]["changed_source_keys"], ["service_matrix"])

    def test_governed_apply_blocks_real_runtime_source_change_with_lease_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root)
            users_path = root / "state" / "users.registry"
            users_path.write_text(
                users_path.read_text(encoding="utf-8").replace("current=1", "current=vless", 1),
                encoding="utf-8",
            )
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertFalse(plan["apply_result"]["applied"])
        self.assertEqual(switch_calls, [])
        self.assertEqual(plan["operation"]["terminal_state"], "DENIED")
        self.assertEqual(plan["operation"]["terminal_reason"], "atomic_execution_envelope_source_changed")
        validation = plan["safety"]["atomic_execution_envelope_validation"]
        self.assertFalse(validation["ok"])
        self.assertIn("runtime_snapshot_hash", validation["state"]["mismatches"])

    def test_governed_apply_blocks_expired_source_bundle_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root)
            plan["safety"]["restore_barrier"]["clearance_expires_at"] = "2000-01-01T00:00:00+00:00"
            matrix_path = root / "state" / "service-matrix.json"
            matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix_payload["items"]["1"]["services"]["youtube"]["score"] = 98
            matrix_path.write_text(json.dumps(matrix_payload), encoding="utf-8")
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertFalse(plan["apply_result"]["applied"])
        self.assertEqual(switch_calls, [])
        validation = plan["safety"]["atomic_execution_envelope_validation"]
        self.assertFalse(validation["ok"])
        self.assertIn("source_bundle_hash", validation["state"]["mismatches"])
        self.assertEqual(plan["operation"]["terminal_reason"], "atomic_execution_envelope_source_changed")

    def test_governed_apply_source_bundle_lease_blocks_unapproved_user(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(
                root,
                allowed_users=["10.0.0.2"],
            )
            matrix_path = root / "state" / "service-matrix.json"
            matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix_payload["items"]["1"]["services"]["youtube"]["score"] = 97
            matrix_path.write_text(json.dumps(matrix_payload), encoding="utf-8")
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertFalse(plan["apply_result"]["applied"])
        self.assertEqual(switch_calls, [])
        validation = plan["safety"]["atomic_execution_envelope_validation"]
        self.assertFalse(validation["ok"])
        self.assertIn("source_bundle_hash", validation["state"]["mismatches"])
        self.assertEqual(plan["operation"]["terminal_reason"], "atomic_execution_envelope_source_changed")

    def test_governed_apply_source_bundle_lease_keeps_two_user_blast_radius(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planner, plan, switch_calls = self.governed_source_bundle_lease_plan(root, users=4)
            matrix_path = root / "state" / "service-matrix.json"
            matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix_payload["items"]["1"]["services"]["youtube"]["score"] = 96
            matrix_path.write_text(json.dumps(matrix_payload), encoding="utf-8")
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(plan["summary"]["candidate_moves_total"], 4)
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(len(switch_calls), 2)

    def test_operation_scoped_rollback_packet_executes_with_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="vless")
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            forward_result = {
                "operation": {
                    "operation_id": "runtime_autoswitch_forward_test",
                    "operation_owner": "tools/v7-users-autoswitch",
                    "operation_type": "runtime_autoswitch",
                    "planner_generation_id": "gen-test",
                    "selected_move_hash": "hash-test",
                    "selected_move_count": 1,
                    "runtime_snapshot_hash": "runtime-snapshot-test",
                    "terminal_state": "APPLIED",
                    "terminal_reason": "selected_moves_applied",
                },
                "apply_result": {
                    "applied": True,
                    "results": [
                        {
                            "user_ip": "10.0.0.2",
                            "from": "1",
                            "to": "vless",
                            "move_type": "failover",
                            "operation_id": "runtime_autoswitch_forward_test",
                            "selected_move_hash": "hash-test",
                            "selected_move_index": 0,
                            "rc": 0,
                            "rollback_attempted": False,
                        }
                    ],
                },
            }
            packet_result = planner.generate_rollback_packet_from_result(forward_result)
            packet = packet_result["packet"]
            packet_path = root / "rollback-packet.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            def fake_emit_terminal_audit(audit: dict) -> dict:
                audit["emitted"] = True
                audit["status"] = "emitted"
                audit["output"] = "mock rollback audit emission"
                return audit

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            planner._emit_terminal_audit = fake_emit_terminal_audit
            result = planner.execute_rollback_packet(packet_path)

        self.assertEqual(packet_result["validation_errors"], [])
        self.assertEqual(packet["schema_version"], self.tool.ROLLBACK_PACKET_SCHEMA)
        self.assertEqual(packet["items"][0]["source_operation_id"], "runtime_autoswitch_forward_test")
        self.assertEqual(switch_calls, [("10.0.0.2", "1", "rollback")])
        self.assertEqual(result["operation"]["terminal_state"], "ROLLBACK_COMPLETED")
        self.assertEqual(result["rollback_result"]["results"][0]["rollback_verdict"], "ROLLBACK_COMPLETED")
        self.assertEqual(result["audit"]["metadata"]["source_operation_id"], "runtime_autoswitch_forward_test")
        self.assertEqual(result["audit"]["metadata"]["selected_move_hash"], "hash-test")
        self.assertTrue(result["audit"]["emitted"])
        self.assertEqual(result["closure_target"]["closure_state"], "VERIFIED_READY")

    def test_operation_scoped_rollback_packet_executes_multiple_users_with_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, users=2, current_egress="vless")
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--apply"]))
            forward_result = {
                "operation": {
                    "operation_id": "runtime_autoswitch_forward_multi",
                    "operation_owner": "tools/v7-users-autoswitch",
                    "operation_type": "runtime_autoswitch",
                    "planner_generation_id": "gen-test",
                    "selected_move_hash": "hash-multi",
                    "selected_move_count": 2,
                    "runtime_snapshot_hash": "runtime-snapshot-test",
                    "terminal_state": "APPLIED",
                    "terminal_reason": "selected_moves_applied",
                },
                "apply_result": {
                    "applied": True,
                    "results": [
                        {
                            "user_ip": "10.0.0.2",
                            "from": "1",
                            "to": "vless",
                            "move_type": "failover",
                            "operation_id": "runtime_autoswitch_forward_multi",
                            "selected_move_hash": "hash-multi",
                            "selected_move_index": 0,
                            "rc": 0,
                            "rollback_attempted": False,
                        },
                        {
                            "user_ip": "10.0.0.3",
                            "from": "1",
                            "to": "vless",
                            "move_type": "failover",
                            "operation_id": "runtime_autoswitch_forward_multi",
                            "selected_move_hash": "hash-multi",
                            "selected_move_index": 1,
                            "rc": 0,
                            "rollback_attempted": False,
                        },
                    ],
                },
            }
            packet_result = planner.generate_rollback_packet_from_result(forward_result)
            packet = packet_result["packet"]
            packet_path = root / "rollback-packet.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            def fake_emit_terminal_audit(audit: dict) -> dict:
                audit["emitted"] = True
                audit["status"] = "emitted"
                audit["output"] = "mock rollback audit emission"
                return audit

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            planner._emit_terminal_audit = fake_emit_terminal_audit
            result = planner.execute_rollback_packet(packet_path)

        self.assertEqual(packet_result["validation_errors"], [])
        self.assertEqual(packet["constraints"]["max_rollback_users"], 2)
        self.assertEqual(len(packet["items"]), 2)
        self.assertEqual(switch_calls, [("10.0.0.2", "1", "rollback"), ("10.0.0.3", "1", "rollback")])
        self.assertEqual(result["operation"]["terminal_state"], "ROLLBACK_COMPLETED")
        self.assertEqual(result["operation"]["rollback_count"], 2)
        self.assertEqual(len(result["rollback_result"]["results"]), 2)
        self.assertTrue(result["audit"]["emitted"])

    def test_restore_barrier_exposes_non_service_failover_proposal_but_blocks_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_state="disabled",
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2999-01-01T00:00:00+00:00",
                    "reason": "unit-test",
                },
            )
            plan = self.plan(root)
            self.assertTrue(plan["safety"]["restore_barrier"]["active"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["proposal_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertTrue(plan["summary"]["execution_blocked"])
            self.assertEqual(plan["decisions"][0]["action"], "switch")
            self.assertEqual(plan["decisions"][0]["move_type"], "failover")
            self.assertIn("restore_barrier_execution_blocked", plan["decisions"][0]["reason"])

    def test_expired_restore_barrier_requires_generation_clearance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "reason": "unit-test-expired",
                },
            )
            plan = self.plan(root)
            self.assertFalse(plan["safety"]["restore_barrier"]["active"])
            self.assertTrue(plan["safety"]["restore_barrier"]["expired"])
            self.assertTrue(plan["safety"]["restore_barrier"]["post_ttl_blocking"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["proposal_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertTrue(plan["summary"]["execution_blocked"])
            self.assertIn(
                "restore_barrier_post_ttl_execution_blocked",
                plan["decisions"][0]["reason"],
            )

    def test_expired_restore_barrier_with_clearance_allows_telegram_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "allow_post_ttl_apply": True,
                    "reason": "unit-test-expired-cleared",
                },
            )
            plan = self.plan(root)
            self.assertFalse(plan["safety"]["restore_barrier"]["active"])
            self.assertTrue(plan["safety"]["restore_barrier"]["expired"])
            self.assertTrue(plan["safety"]["restore_barrier"]["cleared"])
            self.assertFalse(plan["safety"]["restore_barrier"]["post_ttl_blocking"])
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_expired_restore_barrier_clearance_budget_blocks_selected_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 0,
                    "reason": "unit-test-expired-cleared-budget-zero",
                },
            )
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["active"])
            self.assertTrue(barrier["expired"])
            self.assertTrue(barrier["cleared"])
            self.assertFalse(barrier["post_ttl_blocking"])
            self.assertEqual(barrier["clearance_max_selected_moves"], 0)
            self.assertEqual(barrier["clearance_selected_moves_before_guard"], 1)
            self.assertTrue(barrier["clearance_budget_exceeded"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_selected_moves_exceed_budget",
            )
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_requires_generation_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                    "reason": "unit-test-nonzero-budget-no-generation",
                },
            )
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertEqual(barrier["clearance_selected_moves_before_guard"], 1)
            self.assertFalse(barrier["clearance_budget_exceeded"])
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_generation_token_missing",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_with_matching_generation_allows_selected_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                    "reason": "unit-test-nonzero-budget-bootstrap",
                },
            )
            bootstrap = self.plan(root)
            barrier = bootstrap["safety"]["restore_barrier"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": barrier["clearance_selected_moves_hash"],
                "clearance_expected_selected_moves": 1,
                "reason": "unit-test-nonzero-budget-approved",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertTrue(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_budget_and_generation_ok",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_governed_apply_pre_refresh_reuses_restore_barrier_clearance_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 2,
                    "allowed_users": ["10.0.0.2", "10.0.0.3"],
                    "allowed_targets": ["vless"],
                    "approved_atomic_execution_envelope_id": "aee-test",
                    "approved_atomic_execution_envelope_hash": "aee-hash-test",
                    "approved_source_bundle_hash": "source-hash-test",
                    "approved_snapshot_bundle_hash": "snapshot-hash-test",
                    "owner": "admin_core/operator_execution.py",
                },
            )
            refresh_script = root / "refresh-ok"
            refresh_script.write_text("#!/bin/sh\nprintf '{\"source_stable\": true, \"snapshot_count\": 6}\\n'\n", encoding="utf-8")
            refresh_script.chmod(0o755)
            args = self.args_for(
                root,
                [
                    "--apply",
                    "--mode",
                    "guarded",
                    "--pre-planner-refresh",
                    "write",
                    "--pre-planner-refresh-command",
                    str(refresh_script),
                    "--allow-pre-planner-refresh-with-apply",
                    "--target-egress",
                    "vless",
                    "--max-selected-moves",
                    "2",
                ],
            )
            planner = self.tool.AutoswitchPlanner(args)

        refresh = planner.pre_planner_refresh
        self.assertEqual(refresh["state"], "REFRESH_SUCCESS")
        self.assertEqual(refresh["decision"], "freshness_refreshed")
        self.assertEqual(refresh["apply_refresh_scope"]["target_egress"], "vless")
        self.assertEqual(refresh["apply_refresh_scope"]["max_selected_moves"], 2)
        self.assertEqual(refresh["apply_refresh_scope"]["approved_atomic_execution_envelope_id"], "aee-test")
        self.assertEqual(refresh["apply_refresh_scope"]["governance_owner"], "admin_core/operator_execution.py")
        self.assertNotEqual(refresh["state"], "SKIPPED_APPLY_FORBIDDEN")

    def test_governed_apply_pre_refresh_accepts_approved_multi_target_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 5,
                    "allowed_users": [
                        "10.0.0.2",
                        "10.0.0.3",
                        "10.0.0.4",
                        "10.0.0.5",
                        "10.0.0.6",
                    ],
                    "allowed_targets": ["awg0", "awg3"],
                    "approved_atomic_execution_envelope_id": "aee-ba3-test",
                    "approved_atomic_execution_envelope_hash": "aee-ba3-hash-test",
                    "approved_source_bundle_hash": "source-ba3-hash-test",
                    "approved_snapshot_bundle_hash": "snapshot-ba3-hash-test",
                    "owner": "admin_core/operator_execution.py",
                },
            )
            refresh_script = root / "refresh-ok"
            refresh_script.write_text("#!/bin/sh\nprintf '{\"source_stable\": true, \"snapshot_count\": 11}\\n'\n", encoding="utf-8")
            refresh_script.chmod(0o755)
            args = self.args_for(
                root,
                [
                    "--apply",
                    "--mode",
                    "guarded",
                    "--pre-planner-refresh",
                    "write",
                    "--pre-planner-refresh-command",
                    str(refresh_script),
                    "--allow-pre-planner-refresh-with-apply",
                    "--max-selected-moves",
                    "5",
                ],
            )
            planner = self.tool.AutoswitchPlanner(args)

        refresh = planner.pre_planner_refresh
        self.assertEqual(refresh["state"], "REFRESH_SUCCESS")
        self.assertEqual(refresh["decision"], "freshness_refreshed")
        self.assertEqual(refresh["apply_refresh_scope"]["target_scope"], "approved_plan_lock_targets")
        self.assertEqual(refresh["apply_refresh_scope"]["allowed_targets"], ["awg0", "awg3"])
        self.assertEqual(refresh["apply_refresh_scope"]["max_selected_moves"], 5)
        self.assertEqual(refresh["apply_refresh_scope"]["clearance_max_selected_moves"], 5)
        self.assertEqual(refresh["apply_refresh_scope"]["approved_atomic_execution_envelope_id"], "aee-ba3-test")
        self.assertNotEqual(refresh["state"], "SKIPPED_APPLY_FORBIDDEN")

    def test_target_egress_scope_prevents_projected_target_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                current_egress="awg3",
                egress_1_services={"telegram": {"ok": True, "status": "OK", "score": 100}},
            )
            args = self.args_for(root, ["--target-egress", "vless", "--max-selected-moves", "1"])
            planner = self.tool.AutoswitchPlanner(args)
            move = {
                "user_ip": "10.0.0.2",
                "current_egress": "awg3",
                "recommended_egress": "vless",
                "move_type": "failover",
                "recommended_score": 10,
                "current_score": 0,
                "candidates": [
                    {"egress": "1", "eligible": True, "score": 999},
                    {"egress": "vless", "eligible": True, "score": 10},
                ],
                "reason": [],
            }
            selected = planner._pick_projected_moves([move], 1, {"1": 0, "vless": 0}, allow_over_soft=True)

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["recommended_egress"], "vless")
        self.assertNotIn("projected_load_target_adjusted", selected[0]["reason"])

    def test_planner_generation_excludes_fast_signal_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            first = self.plan(root)
            (root / "state" / "telegram-sentinel.json").write_text(
                json.dumps({"updated": "volatile-change"}), encoding="utf-8"
            )
            (root / "state" / "service-matrix.json").write_text(
                (root / "state" / "service-matrix.json").read_text(encoding="utf-8").replace(
                    '"score": 100', '"score": 99', 1
                ),
                encoding="utf-8",
            )
            (root / "state" / "v7-state.json").write_text(
                (root / "state" / "v7-state.json").read_text(encoding="utf-8").replace(
                    '"avg_mbps": 80', '"avg_mbps": 79', 1
                ),
                encoding="utf-8",
            )
            second = self.plan(root)

        self.assertEqual(
            first["safety"]["generation"]["planner_generation_id"],
            second["safety"]["generation"]["planner_generation_id"],
        )
        self.assertNotEqual(
            first["safety"]["generation"]["volatile_inputs"],
            second["safety"]["generation"]["volatile_inputs"],
        )

    def test_nonzero_clearance_budget_rejects_stale_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                    "generation_token": "unit-test-token",
                    "clearance_generation_id": "stale-generation",
                    "approved_selected_moves_hash": "stale-hash",
                    "clearance_expected_selected_moves": 1,
                },
            )
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_generation_mismatch",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_rejects_selected_move_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                },
            )
            bootstrap = self.plan(root)
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": "stale-hash",
                "clearance_expected_selected_moves": 1,
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_selected_moves_hash_mismatch",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_nonzero_clearance_budget_rejects_expired_generation_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                restore_barrier={
                    "enabled": True,
                    "expires_at": "2000-01-01T00:00:00+00:00",
                    "generation_clearance": True,
                    "clearance_max_selected_moves": 1,
                },
            )
            bootstrap = self.plan(root)
            barrier = bootstrap["safety"]["restore_barrier"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": barrier["clearance_selected_moves_hash"],
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2000-01-01T00:00:00+00:00",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.plan(root)
            barrier = plan["safety"]["restore_barrier"]
            self.assertFalse(barrier["clearance_generation_ok"])
            self.assertEqual(
                barrier["clearance_guard_reason"],
                "restore_barrier_clearance_generation_expired",
            )
            self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_apply_uses_approved_plan_lock_when_recomputed_planner_would_select_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            bootstrap_args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap_planner = self.tool.AutoswitchPlanner(bootstrap_args)
            bootstrap = bootstrap_planner.plan()
            self.assertEqual(len(bootstrap["selected_moves"]), 2)
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-approved-plan-lock-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": bootstrap["safety"]["atomic_execution_envelope"]["envelope_id"],
                "approved_atomic_execution_envelope_hash": bootstrap["safety"]["atomic_execution_envelope"]["envelope_hash"],
                "approved_source_bundle_hash": bootstrap["safety"]["atomic_execution_envelope"]["source_bundle_hash"],
                "approved_source_hashes": bootstrap["safety"]["atomic_execution_envelope"]["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": bootstrap["safety"]["atomic_execution_envelope"]["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["1"]["services"]["telegram"] = {"ok": True, "status": "OK", "score": 100}
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(bootstrap_args)
            plan = planner.plan()
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            def fake_emit_terminal_audit(audit: dict) -> dict:
                audit["emitted"] = True
                audit["status"] = "emitted"
                return audit

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            planner._emit_terminal_audit = fake_emit_terminal_audit
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertEqual(plan["safety"]["selected_moves_diagnostics"]["source"], "approved_plan_lock")
        self.assertFalse(plan["safety"]["selected_moves_diagnostics"]["planner_recomputed_after_approval"])
        self.assertEqual(
            (plan["safety"]["restore_barrier"]["approved_plan_lock_validation"] or {}).get("reason"),
            "approved_plan_lock_valid",
        )
        self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover"), ("10.0.0.3", "vless", "failover")])
        self.assertEqual(plan["operation"]["terminal_state"], "APPLIED")

    def test_l3_production_validation_envelope_reaches_switch_without_certifying_autonomy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare_l3_validation_envelope(root)
            planner = self.tool.AutoswitchPlanner(
                self.args_for(
                    root,
                    [
                        "--emergency-failover-autonomy",
                        "--apply",
                        "--mode",
                        "guarded",
                        "--target-egress",
                        "vless",
                        "--max-selected-moves",
                        "1",
                    ],
                )
            )
            switch_calls = []
            planner._run_switch = lambda ip, egress, reason: switch_calls.append((ip, egress, reason)) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 0, stdout="service ok\n")
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["emergency_failover_autonomy"]
        envelope = gate["approved_production_validation_envelope"]
        lock = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        wake = plan["safety"]["l3_wake"]
        self.assertTrue(envelope["ok"])
        self.assertTrue(gate["ok"])
        self.assertEqual(gate["decision"], "authorize_one_user_production_validation_envelope")
        self.assertEqual(gate["authority_source"], "current_approved_emergency_envelope")
        self.assertTrue(gate["production_validation_only"])
        self.assertFalse(gate["autonomy_certified"])
        self.assertFalse(gate["broad_automation_enabled"])
        self.assertIn("telegram", lock["selected_moves"][0]["important_services"])
        self.assertEqual(gate["move_evidence"][0]["current_failures"][0]["service"], "telegram")
        self.assertEqual(wake["decision"], "ACCEPT_WAKE")
        self.assertIn("confirmed_current_channel_failure", wake["accepted_wake_sources"])
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover")])
        self.assertTrue(plan["apply_result"]["applied"])

    def test_l3_production_validation_envelope_negative_cases_stop_safe(self):
        cases = [
            ("expired_envelope", lambda root, barrier: barrier["approved_plan_lock"].update({"expires_at": "2000-01-01T00:00:00+00:00"}), [], "approved_plan_lock_expired"),
            ("wrong_user", lambda root, barrier: barrier["approved_plan_lock"]["selected_moves"][0].update({"user_ip": "10.0.0.99"}), [], "approved_plan_lock_user_missing"),
            ("wrong_source", lambda root, barrier: (root / "state" / "users.registry").write_text("ip=10.0.0.2 current=vless table=100 enabled=1\n", encoding="utf-8"), [], "approved_plan_lock_user_source_mismatch"),
            ("wrong_target", lambda root, barrier: barrier["approved_plan_lock"].update({"allowed_targets": ["other"]}), [], "approved_plan_lock_allowed_targets_mismatch"),
            ("hash_mismatch", lambda root, barrier: barrier.update({"approved_selected_moves_hash": "wrong-hash"}), [], "restore_barrier_clearance_selected_moves_hash_mismatch"),
            ("missing_verify", lambda root, barrier: None, ["--no-verify"], "verification_required_for_emergency_failover"),
            ("missing_rollback", lambda root, barrier: None, ["--no-rollback-on-verify-fail"], "rollback_required_for_emergency_failover"),
            ("target_unsafe", lambda root, barrier: (root / "state" / "egress.registry").write_text("id=1 interface=v7one enabled=1 state=enabled role=GLOBAL_FAST\nid=vless interface=tun0 enabled=0 state=down role=GLOBAL_FAST\n", encoding="utf-8"), [], "approved_plan_lock_target_disabled"),
            ("timer_path", lambda root, barrier: self._set_emergency_wake_source(root, "timer"), [], "rejected_wake_source_timer"),
        ]
        for name, mutate, extra_args, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.prepare_l3_validation_envelope(root)
                barrier_path = root / "state" / "autoswitch-restore-barrier.json"
                barrier = json.loads(barrier_path.read_text(encoding="utf-8"))
                mutate(root, barrier)
                barrier_path.write_text(json.dumps(barrier), encoding="utf-8")
                planner = self.tool.AutoswitchPlanner(
                    self.args_for(
                        root,
                        [
                            "--emergency-failover-autonomy",
                            "--apply",
                            "--mode",
                            "guarded",
                            "--target-egress",
                            "vless",
                            "--max-selected-moves",
                            "1",
                        ]
                        + extra_args,
                    )
                )
                switch_calls = []
                planner._run_switch = lambda ip, egress, reason: switch_calls.append((ip, egress, reason)) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
                plan = planner.plan()
                plan["apply_result"] = planner.apply(plan)

            gate = plan["safety"]["emergency_failover_autonomy"]
            lock = plan["safety"]["restore_barrier"].get("approved_plan_lock_validation") or {}
            barrier = plan["safety"]["restore_barrier"]
            envelope = gate.get("approved_production_validation_envelope") or {}
            blockers = (
                set(gate.get("blockers") or [])
                | set(lock.get("reasons") or [])
                | set(envelope.get("failed_conditions") or [])
                | {str(barrier.get("clearance_guard_reason") or "")}
            )
            self.assertFalse(plan["apply_result"].get("applied"), name)
            self.assertEqual(switch_calls, [], name)
            self.assertIn(expected, blockers, name)

    def test_l3_production_validation_blocks_two_users_and_source_recovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare_l3_validation_envelope(root, users=2)
            policy_path = root / "policy.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["authority_budget"] = {
                "enabled": True,
                "authority_class": "CANARY",
                "certified_authority_class": "CANARY",
                "current_allowed_user_budget": 1,
            }
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            )
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
        self.assertFalse(plan["apply_result"].get("applied"))
        self.assertIn("selected_moves_within_authorized_l3_budget", plan["safety"]["emergency_failover_autonomy"]["approved_production_validation_envelope"]["failed_conditions"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare_l3_validation_envelope(root)
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["1"]["services"]["telegram"] = {"ok": True, "status": "OK", "score": 100}
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--emergency-failover-autonomy", "--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            )
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
        self.assertFalse(plan["apply_result"].get("applied"))
        self.assertIn("required_service_failure_required", plan["safety"]["emergency_failover_autonomy"]["blockers"])

    def test_approved_preview_packet_identity_overrides_structural_selected_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "CANARY",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 1,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            bootstrap_planner = self.tool.AutoswitchPlanner(args)
            bootstrap = bootstrap_planner.plan()
            self.assertEqual(len(bootstrap["selected_moves"]), 1)
            approved_hash = "preview-approved-selected-hash"
            lock = self.approved_plan_lock_from_plan(bootstrap)
            lock["identity_source"] = "approved_preview_packet"
            lock["selected_move_hash"] = approved_hash
            lock["authority_generation"] = "preview-authority-generation"
            lock["snapshot_bundle_hash"] = "preview-derived-snapshot-bundle-hash"
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-approved-preview-packet-token",
                "clearance_generation_id": "preview-authority-generation",
                "approved_selected_moves_hash": approved_hash,
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": [bootstrap["selected_moves"][0]["user_ip"]],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": "aee-preview-derived",
                "approved_atomic_execution_envelope_hash": "preview-derived-envelope-hash",
                "approved_source_bundle_hash": "preview-derived-source-bundle-hash",
                "approved_source_hashes": {"preview_packet": "preview-source"},
                "approved_snapshot_bundle_hash": "preview-derived-snapshot-bundle-hash",
                "approved_plan_lock": lock,
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertEqual(validation["reason"], "approved_plan_lock_valid")
        self.assertEqual(validation["selected_move_hash_source"], "approved_preview_packet")
        self.assertEqual(validation["selected_move_hash"], approved_hash)
        self.assertNotEqual(validation["structural_selected_move_hash"], approved_hash)
        self.assertTrue(plan["safety"]["restore_barrier"]["approved_preview_identity_consumed"])
        self.assertTrue(plan["safety"]["restore_barrier"]["clearance_generation_ok"])
        self.assertEqual(
            plan["safety"]["restore_barrier"]["clearance_generation_reason"],
            "restore_barrier_clearance_preview_packet_identity_match",
        )
        self.assertEqual(plan["operation"]["selected_move_hash"], approved_hash)
        self.assertEqual(plan["selected_moves"][0]["selected_move_hash"], approved_hash)

    def test_committed_apply_identity_must_match_approved_plan_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "CANARY",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 1,
                },
            )
            bootstrap = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            ).plan()
            move = bootstrap["selected_moves"][0]
            approved = self.approved_restore_barrier_from_plan(bootstrap)
            approved["packet_id"] = "pkt-unit-test"
            approved["operation_id"] = "operation-unit-test"
            approved["clearance_generation_id"] = bootstrap["safety"]["generation"]["planner_generation_id"]
            approved["approved_plan_lock"]["packet_id"] = "pkt-unit-test"
            approved["approved_plan_lock"]["operation_id"] = "operation-unit-test"
            approved["approved_plan_lock"]["authority_generation"] = approved["clearance_generation_id"]
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            args = self.args_for(root, [
                "--apply",
                "--mode",
                "guarded",
                "--user",
                move["user_ip"],
                "--source-egress",
                move["current_egress"],
                "--target-egress",
                move["recommended_egress"],
                "--max-selected-moves",
                "1",
                "--approved-packet-id",
                "pkt-unit-test",
                "--approved-operation-id",
                "operation-unit-test",
                "--approved-selected-move-hash",
                bootstrap["operation"]["selected_move_hash"],
                "--approved-authority-generation",
                approved["clearance_generation_id"],
            ])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()

        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["committed_apply_identity"]["ok"])
        self.assertEqual(validation["committed_apply_identity"]["requested_identity"]["packet_id"], "pkt-unit-test")
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertEqual(plan["operation"]["selected_move_hash"], bootstrap["operation"]["selected_move_hash"])

    def test_committed_apply_identity_mismatch_blocks_approved_plan_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "CANARY",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 1,
                },
            )
            bootstrap = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            ).plan()
            move = bootstrap["selected_moves"][0]
            approved = self.approved_restore_barrier_from_plan(bootstrap)
            approved["packet_id"] = "pkt-unit-test"
            approved["operation_id"] = "operation-unit-test"
            approved["approved_plan_lock"]["packet_id"] = "pkt-unit-test"
            approved["approved_plan_lock"]["operation_id"] = "operation-unit-test"
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            args = self.args_for(root, [
                "--apply",
                "--mode",
                "guarded",
                "--user",
                move["user_ip"],
                "--source-egress",
                move["current_egress"],
                "--target-egress",
                move["recommended_egress"],
                "--max-selected-moves",
                "1",
                "--approved-packet-id",
                "pkt-unit-test",
                "--approved-operation-id",
                "operation-unit-test",
                "--approved-selected-move-hash",
                "wrong-selected-hash",
            ])
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)

        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertFalse(validation["ok"])
        self.assertFalse(validation["committed_apply_identity"]["ok"])
        self.assertIn("approved_plan_lock_committed_selected_move_hash_mismatch", validation["reasons"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(plan["apply_result"]["reason"], "approved_plan_lock_selected_moves_missing")

    def test_approved_plan_lock_uses_source_bundle_lease_for_service_matrix_snapshot_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap_planner = self.tool.AutoswitchPlanner(args)
            bootstrap = bootstrap_planner.plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-approved-plan-lock-snapshot-lease",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["1"]["services"]["youtube"]["score"] = 99
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores", "channel-service-scores"],
                "source_mismatch_families": ["service-scores", "channel-service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:service-scores:service_matrix"],
                    },
                    "channel-service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:channel-service-scores:service_matrix"],
                    },
                },
            }
            plan = planner.plan()
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["intelligence_snapshots"]
        self.assertTrue(gate["source_bundle_lease_used"])
        self.assertFalse(gate["stop_required"])
        self.assertEqual(gate["source_bundle_lease_changed_keys"], ["service_matrix"])
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(len(switch_calls), 2)
        self.assertEqual(plan["operation"]["terminal_state"], "APPLIED")

    def test_readiness_dry_run_uses_source_bundle_lease_for_service_matrix_snapshot_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            bootstrap_args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap_planner = self.tool.AutoswitchPlanner(bootstrap_args)
            bootstrap = bootstrap_planner.plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-readiness-source-bundle-lease",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["1"]["services"]["youtube"]["score"] = 99
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            readiness_args = self.args_for(root, ["--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            planner = self.tool.AutoswitchPlanner(readiness_args)
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores", "channel-service-scores"],
                "source_mismatch_families": ["service-scores", "channel-service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:service-scores:service_matrix"],
                    },
                    "channel-service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:channel-service-scores:service_matrix"],
                    },
                },
            }
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["intelligence_snapshots"]
        barrier = plan["safety"]["restore_barrier"]
        self.assertTrue(barrier["clearance_generation_ok"])
        self.assertTrue(barrier["source_bundle_lease"]["ok"])
        self.assertEqual(barrier["source_bundle_lease"]["changed_source_keys"], ["service_matrix"])
        self.assertTrue(gate["source_bundle_lease_used"])
        self.assertFalse(gate["stop_required"])
        self.assertEqual(gate["source_bundle_lease_scope"], "approved_plan_lock_readiness_recheck")
        self.assertEqual(gate["source_bundle_lease_changed_keys"], ["service_matrix"])
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertFalse(plan["apply_requested"])
        self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
        self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_selected_moves_available")

    def test_approved_plan_lock_accepts_stable_sources_with_service_matrix_snapshot_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap_planner = self.tool.AutoswitchPlanner(args)
            bootstrap = bootstrap_planner.plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-approved-plan-lock-stable-source-snapshot-lease",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores", "channel-service-scores"],
                "source_mismatch_families": ["service-scores", "channel-service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:service-scores:service_matrix"],
                    },
                    "channel-service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:channel-service-scores:service_matrix"],
                    },
                },
            }
            plan = planner.plan()
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        barrier = plan["safety"]["restore_barrier"]
        gate = plan["safety"]["intelligence_snapshots"]
        self.assertTrue(barrier["clearance_generation_ok"])
        self.assertEqual(
            barrier["source_bundle_lease"]["reason"],
            "restore_barrier_source_bundle_lease_hard_sources_stable",
        )
        self.assertEqual(barrier["source_bundle_lease"]["changed_source_keys"], [])
        self.assertTrue(gate["source_bundle_lease_used"])
        self.assertFalse(gate["stop_required"])
        self.assertEqual(gate["source_bundle_lease_changed_keys"], [])
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(len(switch_calls), 2)
        self.assertEqual(plan["operation"]["terminal_state"], "APPLIED")

    def test_approved_plan_lock_allows_freshness_only_snapshot_stop_to_reach_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            bootstrap_planner = self.tool.AutoswitchPlanner(args)
            bootstrap = bootstrap_planner.plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-approved-plan-lock-freshness-only",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["trust-summaries"],
                "source_mismatch_families": [],
                "results": {
                    "trust-summaries": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": True,
                        "validation_errors": [],
                        "freshness_state": "STALE",
                    },
                },
            }
            plan = planner.plan()
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["intelligence_snapshots"]
        diagnostics = plan["safety"]["selected_moves_diagnostics"]
        self.assertEqual(gate["snapshot_gate_decision"], "allow_approved_plan_lock_non_material_snapshot_drift")
        self.assertFalse(gate["snapshot_gate_material_change"])
        self.assertTrue(gate["approved_plan_lock_consumed"])
        self.assertEqual(diagnostics["snapshot_gate_decision"], gate["snapshot_gate_decision"])
        self.assertEqual(plan["summary"]["selected_moves"], 1)
        self.assertTrue(plan["apply_result"]["applied"])
        self.assertEqual(switch_calls, [("10.0.0.2", "vless", "failover")])

    def test_approved_plan_lock_blocks_material_snapshot_source_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            bootstrap = self.tool.AutoswitchPlanner(args).plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-approved-plan-lock-material-snapshot",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores"],
                "source_mismatch_families": ["service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:service-scores:users_registry"],
                    },
                },
            }
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["intelligence_snapshots"]
        self.assertEqual(gate["snapshot_gate_decision"], "block_material_snapshot_change")
        self.assertTrue(gate["snapshot_gate_material_change"])
        self.assertIn("source_hash_mismatch:service-scores:users_registry", gate["snapshot_gate_changed_fields"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(plan["apply_result"]["reason"], "approved_plan_lock_selected_moves_missing")
        self.assertEqual(plan["apply_result"]["unsafe_blocker"], "approved_plan_lock_snapshot_gate_stop_required")

    def test_restore_clearance_reuses_exact_operation_scoped_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            args = self.args_for(root, ["--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            planner = self.tool.AutoswitchPlanner(args)
            planner.plan()
            selected = [{
                "user_ip": "10.0.0.2",
                "current_egress": "1",
                "recommended_egress": "vless",
                "move_type": "failover",
            }]
            selected_hash = self.tool.sha256_json(selected)
            source_hashes = {
                "users_registry": "users-semantic",
                "egress_registry": "egress-semantic",
                "runtime_state": "runtime-semantic",
                "candidate_suitability": "candidate-semantic",
            }
            bundle_hash = self.tool.sha256_json(source_hashes)
            barrier = {
                "generation_token": "operation-scoped-unit-test",
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "clearance_generation_id": planner.generation["planner_generation_id"],
                "approved_selected_moves_hash": selected_hash,
                "clearance_expected_selected_moves": 1,
                "approved_atomic_execution_envelope_id": "aee_semantic",
                "approved_atomic_execution_envelope_hash": "semantic-envelope-hash",
                "approved_source_hashes": source_hashes,
                "approved_source_bundle_hash": bundle_hash,
                "approved_snapshot_bundle_hash": bundle_hash,
            }
            original_binding = self.tool.operation_scoped_binding.read_binding
            try:
                self.tool.operation_scoped_binding.read_binding = lambda **kwargs: {
                    "status": "BOUND",
                    "source_hashes": source_hashes,
                    "source_bundle_hash": bundle_hash,
                    "snapshot_bundle_hash": bundle_hash,
                }
                result = planner._restore_clearance_generation_check(barrier, selected, selected_hash)
            finally:
                self.tool.operation_scoped_binding.read_binding = original_binding

        self.assertTrue(result["clearance_generation_ok"], result)
        self.assertEqual(
            result["clearance_generation_reason"],
            "restore_barrier_clearance_operation_scoped_binding_match",
        )

    def test_missing_approved_snapshot_is_explicit_unsafe_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            bootstrap = self.tool.AutoswitchPlanner(args).plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            lock = self.approved_plan_lock_from_plan(bootstrap)
            lock.pop("snapshot_bundle_hash", None)
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-approved-plan-lock-missing-snapshot",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": lock,
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertFalse(validation["ok"])
        self.assertIn("approved_plan_lock_snapshot_missing", validation["reasons"])
        self.assertEqual(plan["apply_result"]["reason"], "approved_plan_lock_selected_moves_missing")
        self.assertEqual(plan["apply_result"]["unsafe_blocker"], "approved_plan_lock_invalid")

    def test_wrong_packet_snapshot_is_explicit_unsafe_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            bootstrap = self.tool.AutoswitchPlanner(args).plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            lock = self.approved_plan_lock_from_plan(bootstrap)
            lock["snapshot_bundle_hash"] = "wrong-packet-snapshot"
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-approved-plan-lock-wrong-snapshot",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": lock,
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertFalse(validation["ok"])
        self.assertIn("approved_plan_lock_snapshot_mismatch", validation["reasons"])
        self.assertEqual(plan["apply_result"]["reason"], "approved_plan_lock_selected_moves_missing")
        self.assertEqual(plan["apply_result"]["unsafe_blocker"], "approved_plan_lock_invalid")

    def test_approved_plan_lock_allows_non_material_source_mismatch_without_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap_planner = self.tool.AutoswitchPlanner(args)
            bootstrap = bootstrap_planner.plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-approved-plan-lock-snapshot-block",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["1"]["services"]["youtube"]["score"] = 99
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores"],
                "source_mismatch_families": ["service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:service-scores:quality_summary"],
                    },
                },
            }
            plan = planner.plan()
            gate = plan["safety"]["intelligence_snapshots"]
            self.assertNotIn("source_bundle_lease_used", gate)
            self.assertFalse(gate["stop_required"])
            self.assertEqual(gate["snapshot_gate_decision"], "allow_approved_plan_lock_non_material_source_mismatch")
            self.assertFalse(gate["snapshot_gate_material_change"])
            self.assertTrue(gate["approved_plan_lock_consumed"])
            self.assertEqual(plan["summary"]["selected_moves"], 2)
            switch_calls = []

            def fake_run_switch(ip: str, egress: str, reason: str):
                switch_calls.append((ip, egress, reason))
                return subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")

            def fake_verify_routes():
                return subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")

            planner._run_switch = fake_run_switch
            planner._verify_routes = fake_verify_routes
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)
            self.assertTrue(plan["apply_result"]["applied"])
            self.assertEqual(len(switch_calls), 2)
            self.assertEqual(plan["operation"]["terminal_state"], "APPLIED")

    def test_missing_approved_selected_moves_blocks_explicitly_not_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=1,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "CANARY",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 1,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "1"])
            bootstrap = self.tool.AutoswitchPlanner(args).plan()
            lock = self.approved_plan_lock_from_plan(bootstrap)
            lock["selected_moves"] = []
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 1,
                "generation_token": "unit-test-missing-approved-selected-moves",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 1,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": [bootstrap["selected_moves"][0]["user_ip"]],
                "allowed_targets": ["vless"],
                "approved_plan_lock": lock,
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertIn("approved_plan_lock_selected_moves_missing", validation["reasons"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertFalse(plan["apply_result"]["applied"])
        self.assertEqual(plan["apply_result"]["reason"], "approved_plan_lock_selected_moves_missing")
        self.assertEqual(plan["operation"]["terminal_state"], "DENIED")

    def test_readiness_dry_run_keeps_snapshot_gate_closed_for_unleased_quality_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            bootstrap_args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(bootstrap_args).plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-readiness-quality-drift-block",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            )
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores"],
                "source_mismatch_families": ["service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": ["source_hash_mismatch:service-scores:quality_summary"],
                    },
                },
            }
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["intelligence_snapshots"]
        self.assertNotIn("source_bundle_lease_used", gate)
        self.assertTrue(gate["stop_required"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
        self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_intelligence_snapshot_stop_required")

    def test_readiness_dry_run_allows_semantic_quality_and_service_matrix_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            bootstrap_args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(bootstrap_args).plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-readiness-semantic-drift",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["1"]["services"]["youtube"]["score"] = 98
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            (root / "state" / "egress-quality-summary.json").write_text(
                json.dumps({"items": {"vless": {"avg_mbps": 51, "stability": 0.91}}}),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            )
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores", "channel-service-scores"],
                "source_mismatch_families": ["service-scores", "channel-service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": [
                            "source_hash_mismatch:service-scores:quality_summary",
                            "source_hash_mismatch:service-scores:service_matrix",
                        ],
                    },
                    "channel-service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": [
                            "source_hash_mismatch:channel-service-scores:quality_summary",
                            "source_hash_mismatch:channel-service-scores:service_matrix",
                        ],
                    },
                },
            }
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["intelligence_snapshots"]
        barrier = plan["safety"]["restore_barrier"]
        self.assertTrue(barrier["clearance_generation_ok"])
        self.assertEqual(
            barrier["source_bundle_lease"]["reason"],
            "restore_barrier_source_bundle_lease_semantic_decision_stable",
        )
        self.assertEqual(barrier["source_bundle_lease"]["changed_source_keys"], ["quality_summary", "service_matrix"])
        self.assertTrue(gate["source_bundle_lease_used"])
        self.assertFalse(gate["stop_required"])
        self.assertEqual(gate["source_bundle_lease_changed_keys"], ["quality_summary", "service_matrix"])
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertFalse(plan["apply_requested"])
        self.assertEqual(plan["operation"]["terminal_state"], "DRY_RUN")
        self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_selected_moves_available")

    def test_readiness_dry_run_blocks_semantic_drift_without_stable_signature(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            bootstrap_args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(bootstrap_args).plan()
            envelope = bootstrap["safety"]["atomic_execution_envelope"]
            lock = self.approved_plan_lock_from_plan(bootstrap)
            lock["executor_may_replace_targets"] = True
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-readiness-semantic-drift-block",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_atomic_execution_envelope_id": envelope["envelope_id"],
                "approved_atomic_execution_envelope_hash": envelope["envelope_hash"],
                "approved_source_bundle_hash": envelope["source_bundle_hash"],
                "approved_source_hashes": envelope["source_bundle"]["source_hashes"],
                "approved_snapshot_bundle_hash": envelope["snapshot_bundle"]["hash"],
                "approved_plan_lock": lock,
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            matrix_path = root / "state" / "service-matrix.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["items"]["1"]["services"]["youtube"]["score"] = 98
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            (root / "state" / "egress-quality-summary.json").write_text(
                json.dumps({"items": {"vless": {"avg_mbps": 51, "stability": 0.91}}}),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(
                self.args_for(root, ["--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            )
            planner.intelligence_snapshots = {
                "active": True,
                "stop_required": True,
                "stop_families": ["service-scores"],
                "source_mismatch_families": ["service-scores"],
                "results": {
                    "service-scores": {
                        "stop_required": True,
                        "runtime_behavior": "STOP",
                        "validation_ok": False,
                        "validation_errors": [
                            "source_hash_mismatch:service-scores:quality_summary",
                            "source_hash_mismatch:service-scores:service_matrix",
                        ],
                    },
                },
            }
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)

        gate = plan["safety"]["intelligence_snapshots"]
        barrier = plan["safety"]["restore_barrier"]
        self.assertFalse(barrier["clearance_generation_ok"])
        self.assertEqual(
            barrier["source_bundle_lease"]["reason"],
            "restore_barrier_source_bundle_lease_decision_signature_unstable",
        )
        self.assertIn(
            "source_bundle_lease_requires_valid_approved_plan_lock",
            barrier["source_bundle_lease"]["reasons"],
        )
        self.assertNotIn("source_bundle_lease_used", gate)
        self.assertTrue(gate["stop_required"])
        self.assertEqual(plan["summary"]["selected_moves"], 0)

    def test_approved_plan_lock_rejects_changed_selected_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(args).plan()
            lock = self.approved_plan_lock_from_plan(bootstrap)
            lock["selected_move_hash"] = "stale-hash"
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_plan_lock": lock,
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.tool.AutoswitchPlanner(args).plan()

        self.assertEqual(plan["summary"]["selected_moves"], 0)
        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertIn("approved_plan_lock_selected_hash_mismatch", validation["reasons"])

    def test_approved_plan_lock_rejects_changed_user_source_and_target_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "awg3", "--max-selected-moves", "2"])
            bootstrap_args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(bootstrap_args).plan()
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap),
                "owner": "admin_core/operator_execution.py",
            }
            users_path = root / "state" / "users.registry"
            users_path.write_text(users_path.read_text(encoding="utf-8").replace("10.0.0.2 current=1", "10.0.0.2 current=awg0"), encoding="utf-8")
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.tool.AutoswitchPlanner(args).plan()

        self.assertEqual(plan["summary"]["selected_moves"], 0)
        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertIn("approved_plan_lock_user_source_mismatch", validation["reasons"])
        self.assertIn("approved_plan_lock_target_scope_mismatch", validation["reasons"])

    def test_approved_plan_lock_rejects_expired_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_EXPANSION",
                    "current_allowed_user_budget": 2,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--target-egress", "vless", "--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(args).plan()
            approved = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-token",
                "clearance_generation_id": bootstrap["safety"]["generation"]["planner_generation_id"],
                "approved_selected_moves_hash": bootstrap["operation"]["selected_move_hash"],
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2999-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(bootstrap, expires_at="2000-01-01T00:00:00+00:00"),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(json.dumps(approved), encoding="utf-8")
            plan = self.tool.AutoswitchPlanner(args).plan()

        self.assertEqual(plan["summary"]["selected_moves"], 0)
        validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
        self.assertIn("approved_plan_lock_expired", validation["reasons"])

    def test_readiness_dry_run_preserves_fresh_candidates_when_approved_lock_expired(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "MEDIUM_BATCH",
                    "certified_authority_class": "MEDIUM_BATCH",
                    "authority_lifecycle_state": "MEDIUM_BATCH_CERTIFIED",
                    "current_allowed_user_budget": 5,
                },
            )
            bootstrap_args = self.args_for(root, ["--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(bootstrap_args).plan()
            stale_clearance = {
                "enabled": True,
                "expires_at": "2000-01-01T00:00:00+00:00",
                "allow_post_ttl_apply": True,
                "generation_clearance": True,
                "clearance_max_selected_moves": 2,
                "generation_token": "unit-test-token",
                "clearance_generation_id": "stale-generation",
                "approved_selected_moves_hash": "stale-selected-hash",
                "clearance_expected_selected_moves": 2,
                "clearance_expires_at": "2000-01-01T00:00:00+00:00",
                "allowed_users": ["10.0.0.2", "10.0.0.3"],
                "allowed_targets": ["vless"],
                "approved_plan_lock": self.approved_plan_lock_from_plan(
                    bootstrap,
                    expires_at="2000-01-01T00:00:00+00:00",
                ),
                "owner": "admin_core/operator_execution.py",
            }
            (root / "state" / "autoswitch-restore-barrier.json").write_text(
                json.dumps(stale_clearance),
                encoding="utf-8",
            )
            plan = self.tool.AutoswitchPlanner(bootstrap_args).plan()

        barrier = plan["safety"]["restore_barrier"]
        validation = barrier["approved_plan_lock_validation"]
        self.assertIn("approved_plan_lock_expired", validation["reasons"])
        self.assertTrue(barrier["approved_plan_lock_ignored_for_fresh_planning"])
        self.assertEqual(barrier["clearance_selected_moves_before_guard"], 2)
        self.assertEqual(len(barrier["approved_candidate_moves_before_guard"]), 2)
        self.assertEqual(plan["summary"]["selected_moves"], 0)
        selected = operator_execution.selected_moves_from_plan(plan)
        self.assertEqual(selected["selected_move_count"], 2)
        self.assertEqual(len(selected["moves"]), 2)
        self.assertNotEqual(selected["selected_move_hash"], operator_execution.EMPTY_SELECTED_MOVES_HASH)

    def test_apply_uses_valid_approved_lock_moves_when_fresh_plan_selected_moves_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=2,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                authority_budget={
                    "authority_class": "MEDIUM_BATCH",
                    "certified_authority_class": "MEDIUM_BATCH",
                    "authority_lifecycle_state": "MEDIUM_BATCH_CERTIFIED",
                    "current_allowed_user_budget": 5,
                },
            )
            args = self.args_for(root, ["--apply", "--mode", "guarded", "--max-selected-moves", "2"])
            bootstrap = self.tool.AutoswitchPlanner(args).plan()
            self.assertEqual(len(bootstrap["selected_moves"]), 2)
            barrier = self.approved_restore_barrier_from_plan(bootstrap, max_selected_moves=2)
            (root / "state" / "autoswitch-restore-barrier.json").write_text(
                json.dumps(barrier),
                encoding="utf-8",
            )
            planner = self.tool.AutoswitchPlanner(args)
            plan = planner.plan()
            validation = plan["safety"]["restore_barrier"]["approved_plan_lock_validation"]
            self.assertTrue(validation["ok"])
            self.assertEqual(validation["selected_move_count"], 2)

            plan["selected_moves"] = []
            plan["summary"]["selected_moves"] = 0
            switch_calls = []
            planner._run_switch = lambda ip, egress, reason: switch_calls.append((ip, egress, reason)) or subprocess.CompletedProcess(["v7-user-switch"], 0, stdout="ok\n")
            planner._verify_routes = lambda: subprocess.CompletedProcess(["v7-user-route-check"], 0, stdout="verify ok\n")
            planner._verify_emergency_required_services = lambda move: subprocess.CompletedProcess(["v7-service-matrix-test"], 0, stdout="service ok\n")
            control_decisions = []
            original_control_decision = planner._execution_control_decision
            planner._execution_control_decision = lambda **kwargs: (
                control_decisions.append(dict(kwargs)) or original_control_decision(**kwargs)
            )

            apply_result = planner.apply(plan)

        self.assertTrue(apply_result["applied"])
        self.assertEqual([call[0] for call in switch_calls], validation["selected_users"])
        self.assertEqual(len(apply_result["results"]), 2)
        self.assertEqual(plan["summary"]["selected_moves"], 2)
        self.assertEqual(plan["operation"]["selected_move_count"], 2)
        self.assertEqual(plan["operation"]["selected_move_hash"], validation["selected_move_hash"])
        self.assertTrue(all(move["operation_id"] == plan["operation"]["operation_id"] for move in plan["selected_moves"]))
        self.assertTrue(all(move["selected_move_hash"] == validation["selected_move_hash"] for move in plan["selected_moves"]))
        self.assertTrue(all(move["execution_mode"] == "emergency_failover" for move in plan["selected_moves"]))
        self.assertEqual(control_decisions[0]["selected_move_hash"], validation["selected_move_hash"])
        rehydration = plan["safety"]["committed_selected_moves_rehydration"]
        self.assertTrue(rehydration["active"])
        self.assertEqual(rehydration["source"], "approved_plan_lock")
        self.assertTrue(rehydration["operation_identity_restored"])
        self.assertFalse(rehydration["new_execution_path_created"])

    def test_egress_disabled_is_hard_ineligible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_state="disabled")
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_multiple_critical_services_failed_can_trigger_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={
                    "instagram": {"ok": False, "score": 0},
                    "youtube": {"ok": False, "score": 0},
                },
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 1)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_restore_stage_suppresses_service_signal_failover_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=15,
                egress_1_services={
                    "instagram": {"ok": False, "score": 0},
                    "youtube": {"ok": False, "score": 0},
                },
                service_signals={"restore_stage": True, "apply_restore_approved": False},
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn("restore_stage_service_signal_failover_requires_approval", plan["decisions"][0]["reason"])

    def test_restore_stage_suppresses_telegram_signal_failover_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                service_signals={"restore_stage": True, "apply_restore_approved": False},
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertIn("restore_stage_service_signal_failover_requires_approval", plan["decisions"][0]["reason"])

    def test_restore_stage_approval_respects_max_failover_per_restore_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(
                root,
                users=15,
                egress_1_services={
                    "instagram": {"ok": False, "score": 0},
                    "youtube": {"ok": False, "score": 0},
                },
                service_signals={
                    "restore_stage": True,
                    "apply_restore_approved": True,
                    "max_failover_per_restore_stage": 1,
                },
            )
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 15)
            self.assertEqual(plan["summary"]["selected_moves"], 1)

    def test_canary_reserved_target_is_not_used_as_production_failover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, egress_1_state="disabled", vless_registry_extra=" canary_reserved=true")
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            vless = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "vless")
            self.assertFalse(vless["eligible"])
            self.assertTrue(vless["canary_reserved"])
            self.assertIn("canary_reserved_production_assignment_blocked", vless["blocked"])
            self.assertIn("no_eligible_failover_target", plan["decisions"][0]["reason"])

    def test_current_user_on_canary_reserved_target_is_not_auto_drained(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="vless", vless_registry_extra=" canary_reserved=true")
            plan = self.plan(root)
            self.assertEqual(plan["summary"]["candidate_moves_total"], 0)
            self.assertEqual(plan["summary"]["selected_moves"], 0)
            self.assertEqual(plan["decisions"][0]["recommended_egress"], "vless")
            self.assertIn(
                "canary_reserved_current_hold_requires_separate_drain_approval",
                plan["decisions"][0]["reason"],
            )
            current = next(row for row in plan["decisions"][0]["candidates"] if row["egress"] == "vless")
            self.assertFalse(current["eligible"])
            self.assertIn("canary_reserved_production_assignment_blocked", current["blocked"])

    def test_authority_promotion_to_medium_batch_updates_only_authority_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            truth = bin_dir / "truth-check"
            truth.write_text('#!/bin/sh\nprintf \'{"status":"PASS","alignment":"FULLY_ALIGNED"}\\n\'\n', encoding="utf-8")
            truth.chmod(0o755)
            audit = bin_dir / "v7-audit-log"
            audit.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            audit.chmod(0o755)
            self.write_fixture(
                root,
                users=5,
                authority_budget={
                    "enabled": True,
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "authority_lifecycle_state": "SMALL_BATCH_CERTIFIED",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 10,
                },
            )
            self.write_feedback_records(root, "runtime_autoswitch_small_1", [f"10.0.0.{idx}" for idx in range(2, 7)])
            self.write_feedback_records(root, "runtime_autoswitch_small_2", [f"10.7.0.{idx}" for idx in range(2, 7)])
            before_policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "MEDIUM_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_small_1",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_small_2",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("MEDIUM_BATCH")
            finally:
                os.environ["PATH"] = old_path
            after_policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "PROMOTED")
            self.assertTrue(result["authority_promoted"])
            self.assertEqual(after_policy["authority_budget"]["authority_class"], "MEDIUM_BATCH")
            self.assertEqual(after_policy["authority_budget"]["certified_authority_class"], "MEDIUM_BATCH")
            self.assertEqual(after_policy["authority_budget"]["current_allowed_user_budget"], 10)
            self.assertEqual(after_policy["switch"], before_policy["switch"])
            self.assertEqual(after_policy["load"], before_policy["load"])
            self.assertEqual(after_policy["reconnect"], before_policy["reconnect"])
            self.assertTrue(Path(result["backup_path"]).is_file())
            self.assertEqual(result["users_moved"], 0)
            self.assertFalse(result["routing_mutation_performed"])
            self.assertFalse(result["autoswitch_apply_run"])

    def test_authority_promotion_to_medium_batch_denied_without_two_successful_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            truth = bin_dir / "truth-check"
            truth.write_text('#!/bin/sh\nprintf \'{"status":"PASS","alignment":"FULLY_ALIGNED"}\\n\'\n', encoding="utf-8")
            truth.chmod(0o755)
            audit = bin_dir / "v7-audit-log"
            audit.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            audit.chmod(0o755)
            self.write_fixture(
                root,
                users=5,
                authority_budget={
                    "enabled": True,
                    "authority_class": "SMALL_BATCH",
                    "certified_authority_class": "SMALL_BATCH",
                    "authority_lifecycle_state": "SMALL_BATCH_CERTIFIED",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 10,
                },
            )
            self.write_feedback_records(root, "runtime_autoswitch_small_1", [f"10.0.0.{idx}" for idx in range(2, 7)])
            before = (root / "policy.json").read_text(encoding="utf-8")
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "MEDIUM_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_small_1",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("MEDIUM_BATCH")
            finally:
                os.environ["PATH"] = old_path
            after = (root / "policy.json").read_text(encoding="utf-8")
            self.assertEqual(result["status"], "DENIED")
            self.assertIn("two_successful_small_batch_operation_ids_required", result["blockers"])
            self.assertIn("medium_batch_evidence_validation_failed", result["blockers"])
            self.assertEqual(after, before)

    def test_authority_promotion_to_small_batch_uses_same_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=2,
                authority_budget={
                    "enabled": True,
                    "authority_class": "CANARY",
                    "certified_authority_class": "CANARY",
                    "authority_lifecycle_state": "CANARY_CERTIFIED",
                    "current_allowed_user_budget": 1,
                    "next_allowed_user_budget": 5,
                },
            )
            self.write_feedback_records(root, "runtime_autoswitch_canary_1", ["10.0.0.2"])
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "SMALL_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_canary_1",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("SMALL_BATCH")
            finally:
                os.environ["PATH"] = old_path
            after_policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "PROMOTED")
            self.assertEqual(after_policy["authority_budget"]["authority_class"], "SMALL_BATCH")
            self.assertEqual(after_policy["authority_budget"]["current_allowed_user_budget"], 5)
            self.assertEqual(after_policy["authority_budget"]["promotion_action"], "CANARY_TO_SMALL_BATCH")
            self.assertEqual(result["users_moved"], 0)
            self.assertFalse(result["autoswitch_apply_run"])

    def test_authority_promotion_to_large_batch_requires_two_medium_runs_and_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=10,
                authority_budget={
                    "enabled": True,
                    "authority_class": "MEDIUM_BATCH",
                    "certified_authority_class": "MEDIUM_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 10,
                    "next_allowed_user_budget": 25,
                },
            )
            self.write_feedback_records(
                root,
                "runtime_autoswitch_medium_1",
                [f"10.0.0.{idx}" for idx in range(2, 12)],
                stability_window_seconds=900,
            )
            self.write_feedback_records(
                root,
                "runtime_autoswitch_medium_2",
                [f"10.0.1.{idx}" for idx in range(2, 12)],
                stability_window_seconds=900,
            )
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "LARGE_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_medium_1",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_medium_2",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("LARGE_BATCH")
            finally:
                os.environ["PATH"] = old_path
            after_policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "PROMOTED")
            self.assertNotIn("only_medium_batch_promotion_supported_by_this_action", result["blockers"])
            self.assertEqual(after_policy["authority_budget"]["authority_class"], "LARGE_BATCH")
            self.assertEqual(after_policy["authority_budget"]["current_allowed_user_budget"], 25)
            self.assertEqual(after_policy["authority_budget"]["promotion_action"], "MEDIUM_BATCH_TO_LARGE_BATCH")
            self.assertEqual(after_policy["authority_budget"]["promotion_evidence"]["successful_medium_batch_runs"], 2)
            self.assertEqual(result["users_moved"], 0)
            self.assertFalse(result["routing_mutation_performed"])

    def test_authority_promotion_to_xlarge_batch_requires_two_large_runs_and_no_regression_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=50,
                authority_budget={
                    "enabled": True,
                    "authority_class": "LARGE_BATCH",
                    "certified_authority_class": "LARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 25,
                    "next_allowed_user_budget": 50,
                },
            )
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_1",
                [f"10.0.0.{idx}" for idx in range(2, 27)],
                stability_window_seconds=3600,
            )
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_2",
                [f"10.2.1.{idx}" for idx in range(2, 27)],
                stability_window_seconds=3600,
            )
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "XLARGE_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_1",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_2",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("XLARGE_BATCH")
            finally:
                os.environ["PATH"] = old_path
            after_policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "PROMOTED")
            self.assertEqual(after_policy["authority_budget"]["authority_class"], "XLARGE_BATCH")
            self.assertEqual(after_policy["authority_budget"]["current_allowed_user_budget"], 50)
            self.assertEqual(after_policy["authority_budget"]["promotion_action"], "LARGE_BATCH_TO_XLARGE_BATCH")
            self.assertEqual(after_policy["authority_budget"]["promotion_evidence"]["successful_large_batch_runs"], 2)
            self.assertEqual(result["users_moved"], 0)

    def test_legacy_pool_25_can_promote_to_xlarge_as_canonical_large_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=50,
                authority_budget={
                    "enabled": True,
                    "authority_class": "POOL",
                    "certified_authority_class": "POOL",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 25,
                    "next_allowed_user_budget": 25,
                },
            )
            old_created_at = "2000-01-01T00:00:00+00:00"
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_1",
                [f"10.0.0.{idx}" for idx in range(2, 27)],
                created_at=old_created_at,
            )
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_2",
                [f"10.2.1.{idx}" for idx in range(2, 27)],
                created_at=old_created_at,
            )
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "XLARGE_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_1",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_2",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("XLARGE_BATCH")
            finally:
                os.environ["PATH"] = old_path
            after_policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "PROMOTED")
            self.assertEqual(result["legacy_authority_class_alias"]["canonical_authority_class"], "LARGE_BATCH")
            self.assertEqual(after_policy["authority_budget"]["authority_class"], "XLARGE_BATCH")
            self.assertEqual(after_policy["authority_budget"]["current_allowed_user_budget"], 50)
            self.assertEqual(after_policy["authority_budget"]["promotion_action"], "LARGE_BATCH_TO_XLARGE_BATCH")

    def test_authority_promotion_to_full_incident_uses_existing_dynamic_authority_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=60,
                authority_budget={
                    "enabled": True,
                    "authority_class": "XLARGE_BATCH",
                    "certified_authority_class": "XLARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 50,
                    "next_allowed_user_budget": 50,
                    "next_authority_class": "FULL_INCIDENT",
                },
            )
            self.write_feedback_records(
                root,
                "runtime_autoswitch_xlarge_1",
                [f"10.0.0.{idx}" for idx in range(2, 52)],
                stability_window_seconds=3600,
            )
            self.write_feedback_records(
                root,
                "runtime_autoswitch_xlarge_2",
                [f"10.2.1.{idx}" for idx in range(2, 52)],
                stability_window_seconds=3600,
            )
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "FULL_INCIDENT",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_xlarge_1",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_xlarge_2",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("FULL_INCIDENT")
            finally:
                os.environ["PATH"] = old_path
            after_policy = json.loads((root / "policy.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "PROMOTED")
            self.assertEqual(after_policy["authority_budget"]["authority_class"], "FULL_INCIDENT")
            self.assertEqual(after_policy["authority_budget"]["current_allowed_user_budget"], 50)
            self.assertEqual(after_policy["authority_budget"]["next_authority_class"], "FULL_INCIDENT")
            self.assertEqual(after_policy["authority_budget"]["promotion_action"], "XLARGE_BATCH_TO_FULL_INCIDENT")
            self.assertEqual(after_policy["authority_budget"]["promotion_evidence"]["successful_xlarge_batch_runs"], 2)
            self.assertEqual(result["users_moved"], 0)

    def test_legacy_pool_promotion_is_not_canonical_next_after_large_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=25,
                authority_budget={
                    "enabled": True,
                    "authority_class": "LARGE_BATCH",
                    "certified_authority_class": "LARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 25,
                    "next_allowed_user_budget": 50,
                },
            )
            self.write_balanced_pool_users(root)
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_1",
                [f"10.0.0.{idx}" for idx in range(2, 12)],
                stability_window_seconds=3600,
            )
            before = (root / "policy.json").read_text(encoding="utf-8")
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "POOL",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_1",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("POOL")
            finally:
                os.environ["PATH"] = old_path
            self.assertEqual(result["status"], "DENIED")
            self.assertIn("invalid_target_authority_transition_LARGE_BATCH_to_POOL", result["blockers"])
            self.assertEqual((root / "policy.json").read_text(encoding="utf-8"), before)
            self.assertEqual(result["users_moved"], 0)
            self.assertFalse(result["autoswitch_apply_run"])

    def test_authority_promotion_to_pool_equivalence_still_requires_operator_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=25,
                authority_budget={
                    "enabled": True,
                    "authority_class": "LARGE_BATCH",
                    "certified_authority_class": "LARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 25,
                    "next_allowed_user_budget": 50,
                },
            )
            self.write_balanced_pool_users(root)
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_1",
                [f"10.0.0.{idx}" for idx in range(2, 12)],
                stability_window_seconds=3600,
            )
            before = (root / "policy.json").read_text(encoding="utf-8")
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "POOL",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_1",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("POOL")
            finally:
                os.environ["PATH"] = old_path
            self.assertEqual(result["status"], "DENIED")
            self.assertIn("missing_explicit_authority_promotion_confirmation", result["blockers"])
            self.assertIn("invalid_target_authority_transition_LARGE_BATCH_to_POOL", result["blockers"])
            self.assertEqual((root / "policy.json").read_text(encoding="utf-8"), before)

    def test_authority_promotion_to_pool_equivalence_denies_rollback_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=25,
                authority_budget={
                    "enabled": True,
                    "authority_class": "LARGE_BATCH",
                    "certified_authority_class": "LARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 25,
                    "next_allowed_user_budget": 50,
                },
            )
            self.write_balanced_pool_users(root)
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_1",
                [f"10.0.0.{idx}" for idx in range(2, 12)],
                rollback_required=True,
                stability_window_seconds=3600,
            )
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "POOL",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_1",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("POOL")
            finally:
                os.environ["PATH"] = old_path
            self.assertEqual(result["status"], "DENIED")
            self.assertIn("invalid_target_authority_transition_LARGE_BATCH_to_POOL", result["blockers"])

    def test_authority_promotion_to_pool_equivalence_denies_nonzero_planner_demand(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=25,
                egress_1_services={"telegram": {"ok": False, "status": "DOWN", "score": 0}},
                route_fitness_1="BLOCKED",
                authority_budget={
                    "enabled": True,
                    "authority_class": "LARGE_BATCH",
                    "certified_authority_class": "LARGE_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 25,
                    "next_allowed_user_budget": 50,
                },
            )
            self.write_balanced_pool_users(root)
            self.write_feedback_records(
                root,
                "runtime_autoswitch_large_1",
                [f"10.0.0.{idx}" for idx in range(2, 12)],
                stability_window_seconds=3600,
            )
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "POOL",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_large_1",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("POOL")
            finally:
                os.environ["PATH"] = old_path
            self.assertEqual(result["status"], "DENIED")
            self.assertIn("invalid_target_authority_transition_LARGE_BATCH_to_POOL", result["blockers"])

    def test_authority_promotion_denied_without_operator_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root)
            self.write_fixture(
                root,
                users=10,
                authority_budget={
                    "enabled": True,
                    "authority_class": "MEDIUM_BATCH",
                    "certified_authority_class": "MEDIUM_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 10,
                },
            )
            self.write_feedback_records(root, "runtime_autoswitch_medium_1", [f"10.0.0.{idx}" for idx in range(2, 7)], stability_window_seconds=900)
            self.write_feedback_records(root, "runtime_autoswitch_medium_2", [f"10.0.1.{idx}" for idx in range(2, 7)], stability_window_seconds=900)
            before = (root / "policy.json").read_text(encoding="utf-8")
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "LARGE_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_medium_1",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_medium_2",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("LARGE_BATCH")
            finally:
                os.environ["PATH"] = old_path
            self.assertEqual(result["status"], "DENIED")
            self.assertIn("missing_explicit_authority_promotion_confirmation", result["blockers"])
            self.assertEqual((root / "policy.json").read_text(encoding="utf-8"), before)

    def test_authority_promotion_denied_on_truth_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir, truth, _audit = self.write_authority_test_binaries(root, truth_pass=False)
            self.write_fixture(
                root,
                users=10,
                authority_budget={
                    "enabled": True,
                    "authority_class": "MEDIUM_BATCH",
                    "certified_authority_class": "MEDIUM_BATCH",
                    "authority_lifecycle_state": "PROMOTED",
                    "current_allowed_user_budget": 5,
                    "next_allowed_user_budget": 10,
                },
            )
            self.write_feedback_records(root, "runtime_autoswitch_medium_1", [f"10.0.0.{idx}" for idx in range(2, 7)], stability_window_seconds=900)
            self.write_feedback_records(root, "runtime_autoswitch_medium_2", [f"10.0.1.{idx}" for idx in range(2, 7)], stability_window_seconds=900)
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
            try:
                args = self.args_for(
                    root,
                    [
                        "--promote-authority-to",
                        "LARGE_BATCH",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_medium_1",
                        "--authority-promotion-operation-id",
                        "runtime_autoswitch_medium_2",
                        "--confirm-authority-promotion",
                        "PROMOTE_AUTHORITY_APPROVED",
                        "--authority-promotion-truth-check-command",
                        str(truth),
                    ],
                )
                result = self.tool.AutoswitchPlanner(args).promote_authority("LARGE_BATCH")
            finally:
                os.environ["PATH"] = old_path
            self.assertEqual(result["status"], "DENIED")
            self.assertIn("runtime_truth_check_failed", result["blockers"])

    def test_authority_promotion_denied_on_missing_feedback_rollback_or_window_failure(self):
        cases = [
            ("missing_feedback", {"omit": {"recommendation"}, "rollback_required": False, "stability_window_seconds": 900}),
            ("rollback_present", {"omit": set(), "rollback_required": True, "stability_window_seconds": 900}),
            ("window_failure", {"omit": set(), "rollback_required": False, "stability_window_seconds": 899}),
        ]
        for label, options in cases:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    bin_dir, truth, _audit = self.write_authority_test_binaries(root)
                    self.write_fixture(
                        root,
                        users=10,
                        authority_budget={
                            "enabled": True,
                            "authority_class": "MEDIUM_BATCH",
                            "certified_authority_class": "MEDIUM_BATCH",
                            "authority_lifecycle_state": "PROMOTED",
                            "current_allowed_user_budget": 5,
                            "next_allowed_user_budget": 10,
                        },
                    )
                    self.write_feedback_records(root, "runtime_autoswitch_medium_1", [f"10.0.0.{idx}" for idx in range(2, 7)], **options)
                    self.write_feedback_records(root, "runtime_autoswitch_medium_2", [f"10.0.1.{idx}" for idx in range(2, 7)], **options)
                    old_path = os.environ.get("PATH", "")
                    os.environ["PATH"] = f"{bin_dir}{os.pathsep}{old_path}"
                    try:
                        args = self.args_for(
                            root,
                            [
                                "--promote-authority-to",
                                "LARGE_BATCH",
                                "--authority-promotion-operation-id",
                                "runtime_autoswitch_medium_1",
                                "--authority-promotion-operation-id",
                                "runtime_autoswitch_medium_2",
                                "--confirm-authority-promotion",
                                "PROMOTE_AUTHORITY_APPROVED",
                                "--authority-promotion-truth-check-command",
                                str(truth),
                            ],
                        )
                        result = self.tool.AutoswitchPlanner(args).promote_authority("LARGE_BATCH")
                    finally:
                        os.environ["PATH"] = old_path
                    self.assertEqual(result["status"], "DENIED")
                    self.assertIn("large_batch_evidence_validation_failed", result["blockers"])
                    self.assertFalse(result["evidence_review"]["evidence_valid"])

    def test_operator_induced_passive_capture_consumes_once_without_execution_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, current_egress="vless")
            event = {
                "event_id": "pevt_operator_vless_1",
                "provenance": "OPERATOR_INDUCED",
                "capture_only": True,
                "channel": "vless",
                "affected_users": ["10.0.0.2"],
                "source_files": ["service-matrix.json", "egress.registry", "users.registry"],
                "source_hashes": {"service_matrix": "matrix-hash", "users_on_source": "users-hash"},
                "observed_at": "2026-07-25T06:19:23+00:00",
                "natural_production_credit": False,
                "l7_credit": False,
            }
            (root / "events" / "service-failure-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
            planner = self.tool.AutoswitchPlanner(self.args_for(root, ["--mode", "observe"]))
            first = planner._consume_passive_production_events()
            self.assertEqual(first["reason"], "consumed")
            self.assertTrue(first["execution_forbidden"])
            self.assertFalse(first["natural_production_credit"])
            outcome_rows = [json.loads(line) for line in (root / "state" / "execution-events.jsonl").read_text(encoding="utf-8").splitlines()]
            outcome = next(row for row in outcome_rows if row.get("schema_version") == "v7.passive-production-event-outcome.v1")
            self.assertEqual(outcome["terminal_outcome_classification"], "STOP_SAFE_NO_ACTION")
            self.assertFalse(outcome["candidate_created"])
            self.assertFalse(outcome["packet_created"])
            self.assertEqual(outcome["users_moved"], 0)
            second = planner._consume_passive_production_events()
            self.assertEqual(second["reason"], "already_consumed_idempotent")


if __name__ == "__main__":
    unittest.main()
