import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from admin_core import operator_execution


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ServiceFailureAutomationEvolutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.autoswitch = load_module("v7_users_autoswitch_automation", ROOT / "tools" / "v7-users-autoswitch")
        cls.sync = load_module("v7_sync_lib_automation", ROOT / "tools" / "v7_sync_lib.py")

    def test_stop_safe_is_materialized_once_with_bounded_shadow(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_1",
                "source_incident_id": "sfinc_1",
                "situation_id": "situation_1",
                "decision_trace_id": "decision_1",
                "closure_state": "CAPTURED_STOP_SAFE",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "NATURAL_PRODUCTION_CANDIDATE",
                "channel": "vless",
                "affected_users": ["10.0.0.2", "10.0.0.3"],
                "observed_at": "2026-07-26T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            plan = {
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                    "reason": ["healthy_target"],
                    "capacity_decision": {
                        "projected_load": {"users": 1, "hard_limit": 10},
                    },
                }],
            }
            first = planner.materialize_service_failure_automation_advisory(plan)
            self.assertTrue(first["active"])
            self.assertEqual(first["obligation"]["stop_safe_classification"], "STOP_SAFE_AUTHORITY_REQUIRED")
            self.assertEqual(first["obligation"]["bounded_recommendation_users"], 1)
            self.assertEqual(first["obligation"]["aggregate_impact_users"], 2)
            self.assertTrue(first["shadow_decision_id"])
            second = planner.materialize_service_failure_automation_advisory(plan)
            self.assertFalse(second["active"])
            rows = [json.loads(line) for line in (state_dir / "closure-records.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(sum(row.get("object_type") == "service_failure_automation_obligation" for row in rows), 1)

    def test_adaptive_cohort_uses_exact_count_load_and_authority_bounds(self):
        moves = [{
            "user_ip": f"10.0.0.{index + 2}",
            "current_egress": "vless",
            "recommended_egress": "awg0",
            "capacity_weight": 2 if index == 0 else 1,
            "capacity_decision": {
                "projected_load": {
                    "users": index + 1,
                    "hard_limit": 48,
                    "required_reserve": 2,
                },
            },
        } for index in range(12)]
        contract = self.autoswitch.build_service_failure_adaptive_cohort_contract(
            moves,
            incident_required_scope=48,
            generic_certified_scope=48,
            adapter_compatible_scope=48,
            authority_safe_scope=4,
            runtime_safe_scope=4,
            verification_safe_scope=48,
            rollback_containment_safe_scope=48,
            circuit_breaker_safe_scope=48,
            request_safe_scope=4,
            measured_at="2026-07-28T00:00:00+00:00",
            expires_at="2026-07-28T01:00:00+00:00",
        )
        self.assertEqual(contract["status"], "MOVE_READY_WITHIN_EXISTING_AUTHORITY")
        self.assertEqual(contract["effective_cohort"], 4)
        self.assertEqual(contract["effective_cohort_load"], 5)
        self.assertEqual(len(contract["selected_members"]), 4)
        self.assertIn("authority_safe_scope", contract["limiting_bounds"])
        self.assertIn("runtime_safe_scope", contract["limiting_bounds"])
        self.assertTrue(contract["cohort_fingerprint"])
        self.assertTrue(all(row["fingerprint"] for row in contract["bounds"].values()))

    def test_adaptive_cohort_separates_shadow_from_zero_authority(self):
        moves = [{
            "user_ip": f"10.0.0.{index + 2}",
            "current_egress": "vless",
            "recommended_egress": "awg0",
            "capacity_decision": {
                "projected_load": {"users": index + 1, "hard_limit": 10},
            },
        } for index in range(4)]
        contract = self.autoswitch.build_service_failure_adaptive_cohort_contract(
            moves,
            incident_required_scope=4,
            generic_certified_scope=48,
            adapter_compatible_scope=48,
            authority_safe_scope=0,
            runtime_safe_scope=4,
            verification_safe_scope=48,
            rollback_containment_safe_scope=48,
            circuit_breaker_safe_scope=48,
            request_safe_scope=4,
            measured_at="2026-07-28T00:00:00+00:00",
        )
        self.assertEqual(contract["status"], "STOP_SAFE")
        self.assertEqual(contract["effective_cohort"], 0)
        self.assertEqual(len(contract["bounded_shadow_moves"]), 4)

    def test_shared_target_availability_keeps_soft_quality_miss_distinct_from_hard_failure(self):
        result = self.autoswitch.classify_shared_target_availability(
            target_id="awg3",
            source_id="vless",
            health_ok=True,
            capacity_owner_reconciled=True,
            free_capacity_after_reserve=12,
            verification_supported=True,
            rollback_containment_supported=True,
            quality_fresh=True,
            stability_inputs={"current": 0.72, "5m": 0.71, "1h": 0.69},
            current_avg_mbps=45.0,
            current_min_mbps=9.0,
            normal_quality_blockers=["stability_below_floor"],
            non_quality_blockers=[],
        )

        self.assertEqual(result["state"], "DEGRADED_USABLE")
        self.assertEqual(result["technical_safe_additional_capacity"], 1)
        self.assertFalse(result["execution_admission"])
        self.assertEqual(
            result["policy_boundary"],
            "EXACT_DEGRADED_SHARED_TARGET_ACTION_CLASS_CONTRACT_REQUIRED",
        )

    def test_shared_target_availability_fails_closed_for_hard_or_insufficient_truth(self):
        hard = self.autoswitch.classify_shared_target_availability(
            target_id="vless",
            source_id="vless",
            health_ok=True,
            capacity_owner_reconciled=True,
            free_capacity_after_reserve=10,
            verification_supported=True,
            rollback_containment_supported=True,
            quality_fresh=True,
            stability_inputs={"current": 0.9, "5m": 0.9, "1h": 0.9},
            current_avg_mbps=30.0,
            current_min_mbps=4.0,
            normal_quality_blockers=[],
            non_quality_blockers=[],
        )
        insufficient = self.autoswitch.classify_shared_target_availability(
            target_id="awg0",
            source_id="vless",
            health_ok=True,
            capacity_owner_reconciled=True,
            free_capacity_after_reserve=10,
            verification_supported=True,
            rollback_containment_supported=True,
            quality_fresh=True,
            stability_inputs={"current": 0.0, "5m": -1.0, "1h": -1.0},
            current_avg_mbps=30.0,
            current_min_mbps=4.0,
            normal_quality_blockers=["stability_below_floor"],
            non_quality_blockers=[],
        )

        self.assertEqual(hard["state"], "HARD_INELIGIBLE")
        self.assertEqual(hard["technical_safe_additional_capacity"], 0)
        self.assertIn("source_cannot_be_its_own_target", hard["hard_reasons"])
        self.assertEqual(insufficient["state"], "DEGRADED_OBSERVATION_INSUFFICIENT")
        self.assertEqual(insufficient["technical_safe_additional_capacity"], 0)
        self.assertFalse(insufficient["hard_reasons"])

    def test_actual_source_reprojection_excludes_live_source_before_capacity_allocation(self):
        rows = [
            {
                "target_id": "vless",
                "shared_target_technically_eligible": True,
                "shared_target_availability": {"state": "HEALTHY"},
                "quality": {"current_stability": 0.99},
                "capacity": {"target_safe_additional_capacity": 12},
                "planner_score": 10.0,
                "correlation_domain": "vless-domain",
                "semantic_fingerprint": "v" * 64,
            },
            {
                "target_id": "awg0",
                "shared_target_technically_eligible": True,
                "shared_target_availability": {"state": "DEGRADED_USABLE"},
                "quality": {"current_stability": 0.72},
                "capacity": {"target_safe_additional_capacity": 1},
                "planner_score": 4.0,
                "correlation_domain": "awg0-domain",
                "semantic_fingerprint": "a" * 64,
            },
        ]
        allocation = self.autoswitch.shared_target_stage_allocations(
            rows=rows,
            stages=[1, 2],
            inventory_fingerprint="i" * 64,
            excluded_target_ids={"vless"},
        )

        self.assertEqual(allocation["excluded_target_ids"], ["vless"])
        self.assertEqual(allocation["ranked_target_ids"], ["awg0"])
        self.assertTrue(allocation["stage_allocations"]["1"]["feasible"])
        self.assertEqual(
            allocation["stage_allocations"]["1"]
            ["immutable_allocation_projection"][0]["target_id"],
            "awg0",
        )
        reservation = (
            allocation["stage_allocations"]["1"]
            ["immutable_allocation_projection"][0]
        )
        self.assertEqual(reservation["capacity_reservation"], 1)
        self.assertEqual(
            reservation["capacity_reservation_semantics"],
            (
                "SERIALIZED_PACKET_LEASE_RESERVATION_WITH_FRESH_"
                "PRE_APPLY_REVALIDATION"
            ),
        )
        self.assertFalse(allocation["stage_allocations"]["2"]["feasible"])

    def test_shared_allocator_continues_target_specific_proven_ladder(self):
        rows = [
            {
                "target_id": "higher-stability-unproven",
                "shared_target_technically_eligible": True,
                "shared_target_availability": {
                    "state": "DEGRADED_USABLE",
                },
                "quality": {"current_stability": 0.9},
                "capacity": {
                    "target_safe_additional_capacity": 1,
                    "planning_safe_additional_capacity": 1,
                    "availability_first_proven_additional_scope": 0,
                },
                "planner_score": 10.0,
                "correlation_domain": "domain-a",
                "semantic_fingerprint": "a" * 64,
            },
            {
                "target_id": "proven-stage-one",
                "shared_target_technically_eligible": True,
                "shared_target_availability": {
                    "state": "DEGRADED_USABLE",
                },
                "quality": {"current_stability": 0.5},
                "capacity": {
                    "target_safe_additional_capacity": 2,
                    "planning_safe_additional_capacity": 2,
                    "availability_first_proven_additional_scope": 1,
                },
                "planner_score": 5.0,
                "correlation_domain": "domain-b",
                "semantic_fingerprint": "b" * 64,
            },
        ]
        allocation = self.autoswitch.shared_target_stage_allocations(
            rows=rows,
            stages=[2],
            inventory_fingerprint="i" * 64,
        )

        self.assertEqual(
            allocation["ranked_target_ids"],
            ["proven-stage-one", "higher-stability-unproven"],
        )
        stage = allocation["stage_allocations"]["2"]
        self.assertTrue(stage["feasible"])
        self.assertEqual(
            stage["immutable_allocation_projection"],
            [{
                "target_id": "proven-stage-one",
                "correlation_domain": "domain-b",
                "allocated_users": 2,
                "capacity_reservation": 2,
                "capacity_reservation_semantics": (
                    "SERIALIZED_PACKET_LEASE_RESERVATION_WITH_FRESH_"
                    "PRE_APPLY_REVALIDATION"
                ),
                "capacity_bounds_fingerprint": (
                    self.autoswitch.sha256_json({})
                ),
                "ordinary_users_unchanged": 0,
                "availability_classification": "DEGRADED_USABLE",
                "availability_policy_boundary": "",
                "target_fault_injection": "FORBIDDEN",
                "target_fingerprint": "b" * 64,
            }],
        )

    def test_shared_target_fingerprint_ignores_display_age_but_binds_freshness(self):
        base = {
            "target_id": "awg3",
            "quality": {
                "updated": "2026-07-30T18:00:00+00:00",
                "age_seconds": 10.0,
                "fresh": True,
                "required_stability_inputs": {
                    "current": 0.3,
                    "5m": 0.3,
                    "1h": 0.3,
                },
            },
            "shared_target_availability": {
                "state": "DEGRADED_USABLE",
            },
            "capacity": {
                "target_safe_additional_capacity": 1,
            },
        }
        later_read = json.loads(json.dumps(base))
        later_read["quality"]["age_seconds"] = 14.5
        stale_read = json.loads(json.dumps(later_read))
        stale_read["quality"]["fresh"] = False

        first = self.autoswitch.shared_target_semantic_fingerprint(base)
        second = self.autoswitch.shared_target_semantic_fingerprint(
            later_read
        )
        stale = self.autoswitch.shared_target_semantic_fingerprint(stale_read)

        self.assertEqual(first, second)
        self.assertNotEqual(second, stale)

    def test_registry_capacity_limits_are_consumed_by_existing_load_owner(self):
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        planner.dynamic_load = {
            "soft_limit": 30,
            "hard_limit": 60,
            "failover_hard_limit": 80,
        }
        planner.load_policy = {"failover_capacity_multiplier": 1.25}
        egress = self.autoswitch.Egress(
            id="execution",
            users=9,
            raw={
                "registry": {
                    "soft_limit": "5",
                    "hard_limit": "10",
                },
            },
        )

        result = planner._load_limits_for_egress(egress)

        self.assertEqual(result["soft_limit"], 5)
        self.assertEqual(result["hard_limit"], 10)
        self.assertEqual(result["failover_hard_limit"], 10)
        self.assertEqual(result["status"], "SOFT_FULL")
        self.assertTrue(result["capacity_owner_reconciled"])
        self.assertIn("egress.registry", result["capacity_owner"])

    def test_controlled_target_diagnostic_ranks_safety_before_id_and_requires_rebind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "\n".join(
                    f"ip=10.7.0.{index} enabled=1 current=source "
                    "certification_user=1 certification_group=t48"
                    for index in range(10, 15)
                )
                + "\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface interface=wg-source "
                "enabled=1 controlled_certification_source=1\n"
                "id=a-exec-weak protocol=amneziawg type=interface interface=wg-a "
                "enabled=1 role=EXECUTION_ONLY execution_reserved=1 "
                "canary_reserved=1 manual_only=1 reserve_only=1 "
                "autoswitch_allowed=false rebalance_allowed=false "
                "production_assignment_allowed=false "
                "reservation_owner=operator_execution_governance "
                "soft_limit=5 hard_limit=10\n"
                "id=z-exec-good protocol=wireguard type=interface interface=wg-z "
                "enabled=1 role=EXECUTION_ONLY execution_reserved=1 "
                "canary_reserved=1 manual_only=1 reserve_only=1 "
                "autoswitch_allowed=false rebalance_allowed=false "
                "production_assignment_allowed=false "
                "reservation_owner=operator_execution_governance "
                "soft_limit=48 hard_limit=60\n"
                "id=ordinary-good protocol=wireguard type=interface interface=wg-o "
                "enabled=1 role=GLOBAL_STABLE soft_limit=48 hard_limit=60\n"
                "id=ordinary-degraded protocol=wireguard type=interface "
                "interface=wg-d enabled=1 role=GLOBAL_STABLE soft_limit=48 "
                "hard_limit=60\n",
                encoding="utf-8",
            )
            state_dir.joinpath("v7-state.json").write_text(json.dumps({
                "egress": {
                    "source": {
                        "code": "000", "avg_mbps": 0,
                        "min_mbps": 0, "stability": 0,
                    },
                    "a-exec-weak": {
                        "code": "200", "avg_mbps": 30,
                        "min_mbps": 12, "stability": 0.2,
                    },
                    "z-exec-good": {
                        "code": "200", "avg_mbps": 70,
                        "min_mbps": 55, "stability": 0.9,
                    },
                    "ordinary-good": {
                        "code": "200", "avg_mbps": 75,
                        "min_mbps": 60, "stability": 0.95,
                    },
                    "ordinary-degraded": {
                        "code": "200", "avg_mbps": 8,
                        "min_mbps": 2, "stability": 0.3,
                    },
                },
            }), encoding="utf-8")
            matrix_items = {}
            for target in (
                "a-exec-weak",
                "z-exec-good",
                "ordinary-good",
                "ordinary-degraded",
            ):
                matrix_items[target] = {
                    "services": {
                        "google": {
                            "ok": True,
                            "status": "OK",
                            "tested_at": "2099-01-01T00:00:00+00:00",
                        },
                    },
                }
            matrix_items["source"] = {
                "services": {
                    "google": {
                        "ok": False,
                        "status": "FAIL",
                        "tested_at": "2099-01-01T00:00:00+00:00",
                    },
                },
            }
            # A source baseline is intentionally strict because the source may
            # later receive a deliberate controlled condition.  The same
            # historical service row must not turn a non-destructive shared
            # target into a hard exclusion when the Planner's profile-aware
            # target checks still pass.
            matrix_items["ordinary-good"] = {
                "services": {
                    "google": {
                        "ok": False,
                        "status": "FAIL",
                        "tested_at": "2099-01-01T00:00:00+00:00",
                    },
                },
            }
            state_dir.joinpath("service-matrix.json").write_text(json.dumps({
                "updated": "2099-01-01T00:00:00+00:00",
                "items": matrix_items,
            }), encoding="utf-8")
            quality_items = {}
            for target, stability in (
                ("a-exec-weak", 0.2),
                ("z-exec-good", 0.9),
                ("ordinary-good", 0.95),
                ("ordinary-degraded", 0.3),
            ):
                quality_items[target] = {
                    "windows": {
                        "5m": {
                            "avg_mbps": 60,
                            "min_mbps": 40,
                            "stability": stability,
                        },
                        "1h": {
                            "avg_mbps": 60,
                            "min_mbps": 40,
                            "stability": stability,
                        },
                    },
                }
            quality_file = state_dir / "egress-quality-summary.json"
            quality_file.write_text(
                json.dumps({
                    "updated": "2099-01-01T00:00:00+00:00",
                    "items": quality_items,
                }),
                encoding="utf-8",
            )
            policy_file = root / "policy.json"
            policy_file.write_text(json.dumps({
                "quality": {"min_stability": 0.45},
                "load": {
                    "mode": "static",
                    "soft_limit": 48,
                    "hard_limit": 60,
                    "failover_hard_limit": 60,
                    "controlled_certification_required_reserve_users": 1,
                },
            }), encoding="utf-8")
            org_policy_file = root / "org-policy.json"
            org_policy_file.write_text("{}", encoding="utf-8")
            audit = root / "audit.jsonl"
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--policy-file", str(policy_file),
                "--org-policy-file", str(org_policy_file),
                "--quality-summary-file", str(quality_file),
                "--action-class-audit-store", str(audit),
            ])
            authority = {
                "status": "APPROVED",
                "request_id": "cpsauth_exact",
                "request_hash": "a" * 64,
                "expires_at": "2099-01-01T00:00:00+00:00",
                "request": {
                    "scope": {
                        "source_id": "source",
                        "controlled_target_id": "a-exec-weak",
                        "controlled_target_admission_class": (
                            "EXECUTION_ONLY_CONTROLLED_CERTIFICATION_TARGET"
                        ),
                        "campaign_stages": [5, 10, 25, 48],
                    },
                    "controlled_target_contract": {
                        "target_id": "a-exec-weak",
                        "ordinary_production_assignment_allowed": False,
                        "certification_only_assignment_allowed": True,
                    },
                },
            }
            campaign = {
                "ok": True,
                "stages": [5, 10, 25, 48],
                "completed_stages": [],
                "next_stage": 5,
            }
            with mock.patch.object(
                self.autoswitch.operator_execution,
                "read_audit_records",
                return_value=[],
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "controlled_certification_substrate_authority_status",
                return_value=authority,
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "controlled_certification_campaign_stage_status",
                return_value=campaign,
            ):
                result = (
                    self.autoswitch
                    .controlled_campaign_target_selection_diagnostic(args)
                )

        self.assertEqual(
            result["status"],
            "EXACT_TARGET_REBIND_AUTHORITY_REQUIRED",
        )
        self.assertEqual(
            result["selection"]["selected_target_id"],
            "z-exec-good",
        )
        self.assertEqual(
            result["selection"]["historical_selection_law"],
            "ID_SORT_THEN_FIRST",
        )
        self.assertIn(
            "EXACT_TARGET_REBIND_AUTHORITY_REQUIRED",
            result["current_residuals"],
        )
        self.assertIn(
            "CAMPAIGN_TARGET_ID_ORDER_SELECTION_DEFECT",
            result["historical_defects_closed"],
        )
        self.assertNotIn("defects", result)
        targets = {
            row["target_id"]: row for row in result["targets"]
        }
        self.assertFalse(
            targets["a-exec-weak"]["full_live_admission"]
        )
        self.assertTrue(
            targets["z-exec-good"]["controlled_rebind_eligible"]
        )
        self.assertFalse(
            targets["ordinary-good"]["controlled_rebind_eligible"]
        )
        self.assertTrue(
            targets["ordinary-good"]["shared_target_technically_eligible"]
        )
        self.assertFalse(targets["ordinary-good"]["health"]["source_baseline_ok"])
        self.assertTrue(targets["ordinary-good"]["health"]["ok"])
        self.assertEqual(
            targets["ordinary-good"]["shared_target_availability"]["state"],
            "HEALTHY",
        )
        self.assertEqual(
            targets["ordinary-good"]["shared_target_policy_scope_status"],
            "EXACT_SHARED_PRODUCTION_TARGET_ACTION_CLASS_CONTRACT_REQUIRED",
        )
        self.assertTrue(
            targets["ordinary-degraded"][
                "shared_target_technically_eligible"
            ]
        )
        self.assertEqual(
            targets["ordinary-degraded"][
                "shared_target_availability"
            ]["state"],
            "DEGRADED_USABLE",
        )
        self.assertFalse(
            targets["ordinary-degraded"][
                "shared_target_availability"
            ]["hard_reasons"]
        )
        ordinary_capacity = targets["ordinary-good"]["capacity"]
        self.assertGreater(
            ordinary_capacity["planning_safe_additional_capacity"],
            0,
        )
        self.assertEqual(
            ordinary_capacity["target_safe_additional_capacity"],
            0,
        )
        self.assertEqual(
            ordinary_capacity["authority_safe_increment"],
            0,
        )
        self.assertEqual(
            ordinary_capacity["runtime_safe_increment"],
            0,
        )
        self.assertEqual(
            set(ordinary_capacity["capacity_bounds"]),
            {
                "hard_capacity_remaining",
                "ordinary_protection_margin",
                "throughput_safe_increment",
                "quality_safe_increment",
                "verification_safe_increment",
                "rollback_containment_safe_increment",
                "authority_safe_increment",
                "runtime_safe_increment",
            },
        )
        self.assertTrue(all(
            row["owner"] and row["fingerprint"] and "reason" in row
            for row in ordinary_capacity["capacity_bounds"].values()
        ))
        self.assertIn(
            "controlled_assignment_permission_or_isolation_contract_missing",
            targets["ordinary-good"]["exclusion_reasons"],
        )
        shared = result["shared_production_target_capacity_projection"]
        self.assertTrue(shared["stage_allocations"]["48"]["feasible"])
        self.assertEqual(
            shared["ordinary_user_effect"], "FORBIDDEN"
        )
        self.assertEqual(shared["target_fault_injection"], "FORBIDDEN")
        self.assertFalse(
            result["forbidden_effects"]["inventory_store_created"]
        )

    def test_controlled_source_topology_prefers_safe_empty_rebind_and_emits_exact_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "\n".join(
                    f"ip=10.7.0.{index} enabled=1 current=source "
                    "certification_user=1 certification_group=t48"
                    for index in range(10, 58)
                )
                + "\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface interface=wg0 enabled=1\n"
                "id=vless protocol=vless type=interface interface=tun0 enabled=1\n",
                encoding="utf-8",
            )
            drafts = root / "drafts"
            drafts.mkdir()
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(drafts),
            ])
            target_projection = {
                "campaign": {
                    "request_id": "cpsauth_old",
                    "request_hash": "a" * 64,
                    "source_id": "source",
                },
                "targets": [{
                    "target_id": "vless",
                    "protocol": "vless",
                    "interface": "tun0",
                    "health": {"ok": True},
                    "quality": {"blockers": []},
                    "capacity": {
                        "ordinary_users": 0,
                        "certification_users": 0,
                        "current_assigned_users": 0,
                        "free_capacity_after_reserve": 60,
                    },
                    "verification_supported": True,
                    "rollback_containment_supported": True,
                    "owner_lineage": {
                        "inventory": "egress.registry",
                        "assignments": "users.registry",
                    },
                    "semantic_fingerprint": "b" * 64,
                }],
            }

            with mock.patch.object(
                self.autoswitch,
                "controlled_campaign_target_selection_diagnostic",
                return_value=target_projection,
            ):
                result = self.autoswitch.controlled_source_topology_diagnostic(
                    args
                )

        self.assertEqual(
            result["status"],
            "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
        )
        self.assertEqual(
            result["recommendation"]["selected_option"],
            "OPTION_1_REBIND_EXISTING_EMPTY_EGRESS",
        )
        self.assertEqual(
            result["recommendation"]["required_authority_action"],
            "REBIND_CONTROLLED_CERTIFICATION_SOURCE",
        )
        self.assertEqual(
            result["production_preflight"]["manifest"]["trial_identity_count"],
            1,
        )
        self.assertEqual(
            result["options"]["option_3_controlled_slice"]["result"],
            "UNSAFE_BY_PROVEN_INVARIANT",
        )
        self.assertTrue(result["authority_package"]["actionable"])
        self.assertFalse(result["authority_package"]["registered"])
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)

    def test_controlled_source_topology_reuses_combined_standing_policy_and_suppresses_one_off_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.18 enabled=1 current=vless "
                "certification_user=1 certification_group=t48\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface "
                "interface=wg0 enabled=1 certification_group=t48\n"
                "id=vless protocol=vless type=interface "
                "interface=tun0 enabled=1 controlled_certification_source=1 "
                "certification_group=t48 execution_reserved=1 "
                "canary_reserved=1 "
                "reservation_owner=operator_execution_governance "
                "autoswitch_allowed=false rebalance_allowed=false "
                "production_assignment_allowed=false "
                "controlled_source_reservation_id=ctres_exact "
                "controlled_source_reservation_expires_at="
                "2099-01-01T00:00:00+00:00\n"
                "id=awg3 protocol=amneziawg type=interface "
                "interface=awg3 enabled=1\n",
                encoding="utf-8",
            )
            policy_path = root / "policy.json"
            audit_path = root / "authority-audit.jsonl"
            policy_path.write_text(
                json.dumps({"authority_budget": {}}, sort_keys=True),
                encoding="utf-8",
            )
            now = operator_execution.utc_now()
            request = (
                operator_execution
                .build_standing_delegated_policy_authority_request(
                    policy_generation_hash=(
                        operator_execution.sha256_file(policy_path)
                    ),
                    active_program=(
                        "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                    ),
                    max_users=48,
                    include_controlled_topology=True,
                    include_availability_first=True,
                    now=now,
                )
            )
            operator_execution.register_standing_delegated_policy_request(
                request,
                audit_store=audit_path,
                now=now,
            )
            activated = (
                operator_execution.issue_standing_delegated_policy_from_audit(
                    policy_path,
                    request_id=request["request_id"],
                    request_hash=request["request_hash"],
                    decision=(
                        "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY"
                    ),
                    audit_store=audit_path,
                    actor_id="unit-authority",
                    now=now,
                )
            )
            # The live audit rotates independently of the policy contract.
            # Topology admission must retain the same durable Authority
            # lineage that policy-status and target-selection consume.
            audit_path.rename(root / "authority-audit.jsonl.1")
            audit_path.write_text("", encoding="utf-8")
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(root / "drafts"),
                "--policy-file", str(policy_path),
                "--action-class-audit-store", str(audit_path),
            ])
            target_projection = {
                "campaign": {
                    "request_id": "cpsauth_old",
                    "request_hash": "a" * 64,
                    "source_id": "source",
                },
                "shared_production_target_capacity_projection": {
                    "current_stage": 1,
                },
                "targets": [{
                    "target_id": "vless",
                    "protocol": "vless",
                    "interface": "tun0",
                    "correlation_domain": "vless:tun0",
                    "shared_target_technically_eligible": True,
                    "shared_target_availability": {
                        "state": "HARD_INELIGIBLE",
                        "policy_boundary": "NO_EXECUTION_ADMISSION",
                    },
                    "health": {"ok": False},
                    "quality": {"blockers": ["controlled_source_degraded"]},
                    "capacity": {
                        "ordinary_users": 0,
                        "certification_users": 1,
                        "current_assigned_users": 1,
                        "free_capacity_after_reserve": 60,
                        "planning_safe_additional_capacity": 60,
                        "capacity_bounds": {
                            "hard_capacity_remaining": {"value": 60},
                        },
                    },
                    "verification_supported": True,
                    "rollback_containment_supported": True,
                    "owner_lineage": {},
                    "semantic_fingerprint": "b" * 64,
                }, {
                    "target_id": "awg3",
                    "protocol": "amneziawg",
                    "interface": "awg3",
                    "correlation_domain": "amneziawg:awg3",
                    "shared_target_technically_eligible": True,
                    "shared_target_availability": {
                        "state": "DEGRADED_USABLE",
                        "policy_boundary": (
                            "EXACT_DEGRADED_SHARED_TARGET_"
                            "ACTION_CLASS_CONTRACT_REQUIRED"
                        ),
                    },
                    "health": {"ok": True},
                    "quality": {"blockers": ["below_normal_floor"]},
                    "capacity": {
                        "ordinary_users": 0,
                        "certification_users": 0,
                        "current_assigned_users": 0,
                        "free_capacity_after_reserve": 9,
                        "planning_safe_additional_capacity": 1,
                        "capacity_bounds": {
                            "hard_capacity_remaining": {"value": 9},
                        },
                    },
                    "verification_supported": True,
                    "rollback_containment_supported": True,
                    "owner_lineage": {},
                    "semantic_fingerprint": "c" * 64,
                }],
            }
            with mock.patch.object(
                self.autoswitch,
                "controlled_campaign_target_selection_diagnostic",
                return_value=target_projection,
            ):
                result = (
                    self.autoswitch.controlled_source_topology_diagnostic(args)
                )

        self.assertEqual(
            result["standing_policy_admission"]["status"],
            "AUTO_ADMITTED_BY_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY",
        )
        self.assertEqual(
            result["status"],
            "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED",
        )
        self.assertEqual(
            result["CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_PLAN"][
                "controlled_source"
            ],
            "vless",
        )
        self.assertEqual(
            result["shared_production_target_capacity_projection"][
                "actual_controlled_source_id"
            ],
            "vless",
        )
        self.assertEqual(
            result["standing_policy_admission"]["contract_id"],
            activated["contract"]["contract_id"],
        )
        self.assertFalse(result["authority_package"]["actionable"])
        self.assertTrue(
            result["authority_package"]["superseded_by_standing_policy"]
        )
        self.assertTrue(
            result["durable_successor"].startswith(
                "AUTO_ADMITTED_BY_STANDING_DELEGATED_"
                "AVAILABILITY_FIRST_POLICY"
            )
        )
        self.assertFalse(
            result["forbidden_effects"]["runtime_apply"]
        )
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)

    def test_availability_first_target_without_controlled_source_is_not_auto_admitted(self):
        """A target-only topology cannot be misreported as a CT-M0F source."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.18 enabled=1 current=vless "
                "certification_user=1 certification_group=t48\n",
                encoding="utf-8",
            )
            # No row is an isolated controlled-certification source.  ``awg3``
            # is deliberately only a healthy target with one availability slot.
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface interface=wg0 enabled=1 certification_group=t48\n"
                "id=vless protocol=vless type=interface interface=tun0 enabled=1 certification_group=t48\n"
                "id=awg3 protocol=amneziawg type=interface interface=awg3 enabled=1\n",
                encoding="utf-8",
            )
            policy_path = root / "policy.json"
            audit_path = root / "authority-audit.jsonl"
            policy_path.write_text(json.dumps({"authority_budget": {}}, sort_keys=True), encoding="utf-8")
            now = operator_execution.utc_now()
            request = operator_execution.build_standing_delegated_policy_authority_request(
                policy_generation_hash=operator_execution.sha256_file(policy_path),
                active_program="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                max_users=48,
                include_controlled_topology=True,
                include_availability_first=True,
                now=now,
            )
            operator_execution.register_standing_delegated_policy_request(
                request, audit_store=audit_path, now=now,
            )
            operator_execution.issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(root / "drafts"),
                "--policy-file", str(policy_path),
                "--action-class-audit-store", str(audit_path),
            ])
            target_projection = {
                "campaign": {"request_id": "historic", "request_hash": "a" * 64, "source_id": "source"},
                "shared_production_target_capacity_projection": {"current_stage": 1},
                "targets": [{
                    "target_id": "awg3",
                    "protocol": "amneziawg",
                    "interface": "awg3",
                    "correlation_domain": "amneziawg:awg3",
                    "shared_target_technically_eligible": True,
                    "shared_target_availability": {
                        "state": "DEGRADED_USABLE",
                        "policy_boundary": "EXACT_DEGRADED_SHARED_TARGET_ACTION_CLASS_CONTRACT_REQUIRED",
                    },
                    "health": {"ok": True},
                    "quality": {"blockers": ["below_normal_floor"]},
                    "capacity": {
                        "ordinary_users": 0,
                        "certification_users": 0,
                        "current_assigned_users": 0,
                        "free_capacity_after_reserve": 9,
                        "planning_safe_additional_capacity": 1,
                        "capacity_bounds": {"hard_capacity_remaining": {"value": 9}},
                    },
                    "verification_supported": True,
                    "rollback_containment_supported": True,
                    "owner_lineage": {},
                    "semantic_fingerprint": "c" * 64,
                }],
            }
            with mock.patch.object(
                self.autoswitch,
                "controlled_campaign_target_selection_diagnostic",
                return_value=target_projection,
            ):
                result = self.autoswitch.controlled_source_topology_diagnostic(args)

        self.assertEqual(result["status"], "CONTROLLED_SOURCE_TOPOLOGY_PROVISIONING_REQUIRED")
        self.assertEqual(
            result["durable_successor"],
            "SAFE_PREDECESSOR_REQUIRED:EXISTING_CONTROLLED_SOURCE_RESERVATION_AND_CERTIFICATION_GROUP_OWNER",
        )
        self.assertFalse(result["production_preflight"]["mutation_performed"])
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)

    def test_rebind_standing_policy_does_not_auto_admit_draft_provisioning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.102 enabled=1 current=source "
                "certification_user=1 certification_group=t48\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface "
                "interface=wg0 enabled=1\n",
                encoding="utf-8",
            )
            policy_path = root / "policy.json"
            audit_path = root / "authority-audit.jsonl"
            policy_path.write_text(
                json.dumps({"authority_budget": {}}, sort_keys=True),
                encoding="utf-8",
            )
            now = operator_execution.utc_now()
            request = (
                operator_execution
                .build_standing_delegated_policy_authority_request(
                    policy_generation_hash=(
                        operator_execution.sha256_file(policy_path)
                    ),
                    active_program=(
                        "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                    ),
                    max_users=48,
                    include_controlled_topology=True,
                    now=now,
                )
            )
            operator_execution.register_standing_delegated_policy_request(
                request,
                audit_store=audit_path,
                now=now,
            )
            operator_execution.issue_standing_delegated_policy_from_audit(
                policy_path,
                request_id=request["request_id"],
                request_hash=request["request_hash"],
                decision="APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                audit_store=audit_path,
                actor_id="unit-authority",
                now=now,
            )
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(root / "drafts"),
                "--policy-file", str(policy_path),
                "--action-class-audit-store", str(audit_path),
            ])
            target_projection = {
                "campaign": {
                    "request_id": "cpsauth_old",
                    "request_hash": "a" * 64,
                    "source_id": "source",
                },
                "targets": [],
            }
            draft = {
                "draft_id": "draft-exact",
                "one_identity_trial_capacity": 1,
                "ready_for_guarded_disabled_pool_preflight": True,
            }
            with (
                mock.patch.object(
                    self.autoswitch,
                    "controlled_campaign_target_selection_diagnostic",
                    return_value=target_projection,
                ),
                mock.patch.object(
                    self.autoswitch,
                    "_controlled_source_draft_candidates",
                    return_value=[draft],
                ),
            ):
                result = (
                    self.autoswitch.controlled_source_topology_diagnostic(args)
                )

        self.assertEqual(result["recommendation"]["selected_option"], "")
        self.assertEqual(
            result["status"],
            "CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED",
        )
        self.assertEqual(
            result["options"]["option_2_dedicated_source"]["result"],
            "UNSAFE_BY_PROVEN_INVARIANT",
        )
        self.assertEqual(
            result["options"]["option_2_dedicated_source"][
                "bootstrap_only_ready_drafts"
            ][0]["classification"],
            "BOOTSTRAP_ONLY_NO_CREDIBLE_CAMPAIGN_SUCCESSOR",
        )
        self.assertFalse(result["authority_package"]["actionable"])
        self.assertTrue(
            result["durable_successor"].startswith(
                "EXTERNAL_RESOURCE_REQUIRED:"
            )
        )

    def test_ct_m0f_one_user_profile_reuses_ready_capacity_two_draft_without_campaign_credit(self):
        """A one-user latency sample must not inherit the Tier-48 capacity gate."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.102 enabled=1 current=source "
                "certification_user=1 certification_group=ctm0f\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface "
                "interface=wg0 enabled=1 certification_group=ctm0f\n",
                encoding="utf-8",
            )
            policy_path = root / "policy.json"
            policy_path.write_text(json.dumps({
                operator_execution.CT_M0F_STANDING_VALIDATION_POLICY_KEY: {
                    "contract_id": "ctm0fsdpc_" + "b" * 24,
                    "contract_hash": "b" * 64,
                    "expires_at": "2099-01-01T00:00:00+00:00",
                    "authority_decision": {
                        "request_id": "ctm0fsdpauth_r1_" + "c" * 24,
                        "request_hash": "c" * 64,
                    },
                },
            }), encoding="utf-8")
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(root / "drafts"),
                "--policy-file", str(policy_path),
                "--controlled-source-validation-profile", "ct-m0f-one-user",
            ])
            target_projection = {
                "campaign": {
                    "request_id": "cpsauth_existing",
                    "request_hash": "a" * 64,
                    "source_id": "source",
                    "current_stage": 48,
                    "remaining_stages": [48],
                },
                "targets": [],
            }
            draft = {
                "draft_id": "draft-capacity-two",
                "hard_capacity": 2,
                "one_identity_trial_capacity": 1,
                "ready_for_guarded_disabled_pool_preflight": True,
            }
            with (
                mock.patch.object(
                    self.autoswitch,
                    "controlled_campaign_target_selection_diagnostic",
                    return_value=target_projection,
                ),
                mock.patch.object(
                    self.autoswitch,
                    "_controlled_source_draft_candidates",
                    return_value=[draft],
                ),
                mock.patch.object(
                    self.autoswitch,
                    "_controlled_source_reservation_owner_capability",
                    return_value={
                        "status": "READY",
                        "owner": "tools/v7-egress-set-state",
                    },
                ),
                mock.patch.object(
                    self.autoswitch.operator_execution,
                    "validate_ct_m0f_standing_validation_policy",
                    return_value={"ok": True},
                ),
            ):
                result = self.autoswitch.controlled_source_topology_diagnostic(args)

        self.assertEqual(
            result["status"],
            "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
        )
        self.assertEqual(result["validation_profile"], "ct-m0f-one-user")
        self.assertEqual(
            result["recommendation"]["selected_option"],
            "OPTION_2_PROVISION_EXISTING_VALID_DRAFT",
        )
        self.assertEqual(
            result["recommendation"]["required_authority_action"],
            "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
        )
        self.assertEqual(
            result["production_preflight"]["manifest"]["validation_profile"],
            "CT_M0F_ONE_USER_CONTROLLED_CONDITION",
        )
        self.assertEqual(
            result["authority_package"]["authority_basis"]["kind"],
            "CT_M0F_STANDING_VALIDATION_POLICY",
        )
        self.assertEqual(
            [row["stage"] for row in result[
                "CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_PLAN"]["stages"]],
            [1],
        )
        self.assertTrue(result["authority_package"]["actionable"])
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)

    def test_ct_m0f_one_user_profile_normalizes_missing_shared_stage_allocation(self):
        """A partial capacity projection is a safe no-allocation result, not a crash."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.102 enabled=1 current=source "
                "certification_user=1 certification_group=ctm0f\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface interface=wg0 enabled=1\n",
                encoding="utf-8",
            )
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(root / "drafts"),
                "--controlled-source-validation-profile", "ct-m0f-one-user",
            ])
            target_projection = {
                "campaign": {"source_id": "source", "current_stage": 48},
                "targets": [],
            }
            draft = {
                "draft_id": "draft-capacity-two",
                "hard_capacity": 2,
                "one_identity_trial_capacity": 1,
                "ready_for_guarded_disabled_pool_preflight": True,
            }
            with (
                mock.patch.object(
                    self.autoswitch,
                    "controlled_campaign_target_selection_diagnostic",
                    return_value=target_projection,
                ),
                mock.patch.object(
                    self.autoswitch,
                    "_controlled_source_draft_candidates",
                    return_value=[draft],
                ),
                mock.patch.object(
                    self.autoswitch,
                    "_controlled_source_reservation_owner_capability",
                    return_value={"status": "READY"},
                ),
                mock.patch.object(
                    self.autoswitch,
                    "shared_target_stage_allocations",
                    return_value={"stage_allocations": {"1": None}},
                ),
            ):
                result = self.autoswitch.controlled_source_topology_diagnostic(args)

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["shared_production_target_capacity_projection"]
            ["stage_allocations"],
            {},
        )

    def test_post_trial_topology_reuses_same_campaign_source_and_rejects_capacity_two_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            users = [
                (
                    f"ip=10.7.0.{index} enabled=1 current=source "
                    "certification_user=1 certification_group=t48"
                )
                for index in range(10, 57)
            ]
            users.append(
                "ip=10.7.0.100 enabled=1 current=vless "
                "certification_user=1 certification_group=t48"
            )
            state_dir.joinpath("users.registry").write_text(
                "\n".join(users) + "\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=source protocol=amneziawg type=interface "
                "interface=wg0 enabled=1 controlled_certification_source=1 "
                "certification_group=t48\n"
                "id=vless protocol=vless type=proxy interface=tun0 enabled=1 "
                "controlled_certification_source=1 "
                "certification_group=ctop-old execution_reserved=1 "
                "canary_reserved=1 "
                "reservation_owner=operator_execution_governance "
                "autoswitch_allowed=false rebalance_allowed=false "
                "production_assignment_allowed=false "
                "controlled_source_reservation_id=ctres_old "
                "controlled_source_reservation_expires_at="
                "2020-01-01T00:00:00+00:00\n",
                encoding="utf-8",
            )
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(root / "drafts"),
            ])
            target_projection = {
                "campaign": {
                    "request_id": "cpsauth_current",
                    "request_hash": "a" * 64,
                    "source_id": "source",
                    "current_stage": 5,
                    "remaining_stages": [5, 10, 25, 48],
                    "pinned_target_id": "exec",
                },
                "targets": [{
                    "target_id": "vless",
                    "protocol": "vless",
                    "interface": "tun0",
                    "health": {"ok": True},
                    "quality": {"blockers": []},
                    "capacity": {
                        "ordinary_users": 0,
                        "certification_users": 1,
                        "current_assigned_users": 1,
                        "free_capacity_after_reserve": 141,
                        "current_stage_safe_scope": 141,
                        "campaign_completion_safe_scope": 141,
                    },
                    "verification_supported": True,
                    "rollback_containment_supported": True,
                    "controlled_rebind_eligible": False,
                    "full_live_admission": False,
                    "owner_lineage": {},
                    "semantic_fingerprint": "b" * 64,
                }],
            }
            draft = {
                "draft_id": "draft-capacity-two",
                "hard_capacity": 2,
                "one_identity_trial_capacity": 1,
                "ready_for_guarded_disabled_pool_preflight": True,
            }
            with (
                mock.patch.object(
                    self.autoswitch,
                    "controlled_campaign_target_selection_diagnostic",
                    return_value=target_projection,
                ),
                mock.patch.object(
                    self.autoswitch,
                    "_controlled_source_draft_candidates",
                    return_value=[draft],
                ),
                mock.patch.object(
                    self.autoswitch,
                    "_controlled_source_reservation_owner_capability",
                    return_value={
                        "status": "READY",
                        "owner": "tools/v7-egress-set-state",
                    },
                ),
            ):
                result = (
                    self.autoswitch.controlled_source_topology_diagnostic(
                        args
                    )
                )

        post_trial = result[
            "POST_TRIAL_CONTROLLED_TOPOLOGY_DECISION_DIAGNOSTIC"
        ]
        self.assertEqual(
            post_trial["status"],
            "POST_TRIAL_DEDICATED_DRAFT_SELECTION_SUBOPTIMAL",
        )
        self.assertTrue(post_trial["all_48_identities_accounted_for"])
        self.assertEqual(
            post_trial["campaign_identity_locations"],
            {"source": 47, "vless": 1},
        )
        accounting = post_trial["campaign_identity_accounting"]
        self.assertEqual(accounting["status"], "ACCOUNTED")
        self.assertEqual(accounting["expected_identity_count"], 48)
        self.assertEqual(accounting["accounted_count"], 48)
        self.assertEqual(accounting["balance"]["baseline_source"], 47)
        self.assertEqual(accounting["balance"]["active_forward"], 1)
        self.assertEqual(accounting["balance"]["targets"], 0)
        self.assertFalse(accounting["raw_user_list_stored"])
        self.assertTrue(
            post_trial["post_trial_resource"][
                "can_accept_full_campaign_pool"
            ]
        )
        self.assertTrue(
            post_trial["post_trial_resource"][
                "can_remain_controlled_source_now"
            ]
        )
        self.assertEqual(
            result["recommendation"]["selected_option"],
            "OPTION_1_CONTINUE_EXISTING_CONTROLLED_EGRESS",
        )
        self.assertEqual(
            result["production_preflight"]["manifest"][
                "reservation_mode"
            ],
            "RENEW_AND_CONTINUE_SAME_CAMPAIGN_CERTIFICATION_SOURCE",
        )
        self.assertEqual(
            result["production_preflight"]["manifest"][
                "certification_group"
            ],
            "t48",
        )
        polygon = result["polygon_fault_verification_contract"]
        self.assertTrue({
            "valid_existing_draft_activation",
            "invalid_or_quarantined_draft_rejection",
            "draft_hard_capacity_below_requested_cohort",
            "stale_draft_generation",
            "source_target_role_confusion",
            "occupied_egress_rejection",
            "ordinary_user_route_mutation_rejection",
            "provisioning_without_rollback_rejection",
            "crash_after_resource_creation",
            "crash_after_interface_or_route_creation",
            "crash_after_assignment",
            "duplicate_wake",
            "duplicate_provisioning_request",
            "expired_lease",
            "policy_revocation",
            "cleanup_after_success",
            "cleanup_after_failure",
            "selection_change_after_live_inventory_change",
            "next_stage_automatic_continuation",
        }.issubset(set(polygon["scenarios"])))
        self.assertTrue({
            "NO_AUTHORITY_SELF_EXPANSION",
            "NO_ORDINARY_USER_EFFECT",
            "SOURCE_AND_TARGET_ROLES_EXACT",
            "PROVISIONED_CAPACITY_OWNER_BACKED",
            "NO_RESOURCE_ABOVE_HARD_CAPACITY",
            "NO_ORPHANED_CONTROLLED_RESOURCE",
            "RESTORE_BARRIER_BEFORE_APPLY",
            "ROLLBACK_BOUNDED_AND_IDEMPOTENT",
            "STALE_DRAFT_OR_POLICY_FAILS_CLOSED",
            "ONE_TRANSACTION_PER_LEASE",
            "ONE_DURABLE_SUCCESSOR",
            "NO_SYNTHETIC_PRODUCTION_CREDIT",
        }.issubset(set(polygon["invariants"])))
        self.assertTrue(result["authority_package"]["actionable"])

    def test_controlled_source_topology_authority_audit_is_exact_once(self):
        manifest = {
            "selected_option": "OPTION_1_REBIND_EXISTING_EMPTY_EGRESS",
            "existing_source": "source",
            "selected_source_or_draft": "vless",
            "trial_identity": "10.7.0.16",
            "trial_identity_count": 1,
            "identity_set_fingerprint": "b" * 64,
            "expected_assignment_delta": "10.7.0.16:source->vless",
            "expected_ordinary_assignment_delta": "NONE",
            "expected_ordinary_route_delta": "NONE",
            "capacity_reservation": 1,
            "max_concurrent_transactions": 1,
            "reservation_owner": "tools/v7-egress-set-state",
            "verification": "fresh Matrix baseline + current route",
            "rollback": "restore exact source binding and release reservation",
            "failure_mechanism": "existing controlled certification guard",
            "lease_and_expiry_required": True,
            "packet_required_before_effect": True,
            "restore_barrier_required_before_effect": True,
        }
        manifest["manifest_hash"] = operator_execution.sha256_json(manifest)
        payload = {
            "active_program": (
                "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
            ),
            "mission": (
                "CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_"
                "SLICE_FEASIBILITY_V1"
            ),
            "exact_action": "REBIND_CONTROLLED_CERTIFICATION_SOURCE",
            "manifest": manifest,
            "current_campaign_request_id": "cpsauth_existing",
            "current_campaign_request_hash": "a" * 64,
            "supersedes_source_binding_only": True,
            "tier48_capability_or_campaign_reapproval": False,
            "ordinary_customer_involvement": False,
            "self_expansion_allowed": False,
            "forbidden_effects": ["ordinary_user_movement"],
            "reentry_condition": "exact independent decision",
        }
        request = (
            operator_execution
            .build_controlled_source_topology_authority_request(payload)
        )
        self.assertTrue(
            operator_execution
            .validate_controlled_source_topology_authority_request(
                request
            )["ok"]
        )
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "operator-execution-audit.jsonl"
            first = (
                operator_execution
                .register_controlled_source_topology_authority_request(
                    request,
                    audit_store=audit,
                )
            )
            duplicate = (
                operator_execution
                .register_controlled_source_topology_authority_request(
                    request,
                    audit_store=audit,
                )
            )
            pending = (
                operator_execution.controlled_source_topology_authority_status(
                    operator_execution.read_audit_records(audit)
                )
            )
            approval = f"APPROVE_{request['exact_action']}"
            decision = (
                operator_execution
                .record_controlled_source_topology_authority_decision(
                    request_id=request["request_id"],
                    request_hash=request["request_hash"],
                    decision=approval,
                    actor_id="test-independent-authority",
                    audit_store=audit,
                )
            )
            exact_repeat = (
                operator_execution
                .record_controlled_source_topology_authority_decision(
                    request_id=request["request_id"],
                    request_hash=request["request_hash"],
                    decision=approval,
                    actor_id="test-independent-authority",
                    audit_store=audit,
                )
            )
            approved = (
                operator_execution.controlled_source_topology_authority_status(
                    operator_execution.read_audit_records(audit)
                )
            )
        self.assertEqual(first["status"], "REGISTERED")
        self.assertEqual(duplicate["status"], "ALREADY_REGISTERED_EXACT")
        self.assertEqual(pending["status"], "PENDING")
        self.assertEqual(decision["status"], "APPROVED")
        self.assertFalse(decision["topology_materialized"])
        self.assertEqual(decision["users_moved"], 0)
        self.assertEqual(exact_repeat["status"], "ALREADY_RECORDED_EXACT")
        self.assertEqual(approved["status"], "APPROVED")

        malformed = json.loads(json.dumps(request))
        malformed["manifest"]["expected_ordinary_route_delta"] = "CHANGED"
        malformed["request_hash"] = (
            operator_execution.controlled_source_topology_request_hash(
                malformed
            )
        )
        malformed["request_id"] = (
            f"cstopauth_r1_{malformed['request_hash'][:24]}"
        )
        validation = (
            operator_execution
            .validate_controlled_source_topology_authority_request(malformed)
        )
        self.assertFalse(validation["ok"])
        self.assertIn(
            "controlled_source_topology_ordinary_delta_invalid",
            validation["errors"],
        )

    def test_approved_topology_provision_reserves_existing_source_exact_once(self):
        """An approved provision reserves one existing empty source only."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text("", encoding="utf-8")
            state_dir.joinpath("egress.registry").write_text(
                "id=pool1 protocol=amneziawg type=interface interface=wg1 enabled=1 "
                "controlled_certification_source=1 certification_group=t48\n",
                encoding="utf-8",
            )
            audit_path = root / "authority-audit.jsonl"
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--egress-drafts-dir", str(root / "drafts"),
                "--action-class-audit-store", str(audit_path),
            ])
            future = "2099-01-01T00:00:00+00:00"
            diagnostic = {
                "status": "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY",
                "authority_lifecycle": {
                    "status": "APPROVED",
                    "matching_current_preflight": True,
                    "decision": "APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
                    "request_id": "cstopauth_exact",
                    "request_hash": "a" * 64,
                    "decision_id": "cstopdec_exact",
                    "expires_at": future,
                },
                "authority_package": {
                    "exact_action": "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
                    "authority_basis": {"expires_at": future},
                },
                "production_preflight": {"manifest": {
                    "validation_profile": "CT_M0F_ONE_USER_CONTROLLED_CONDITION",
                    "trial_identity_count": 1,
                    "expected_ordinary_assignment_delta": "NONE",
                    "expected_ordinary_route_delta": "NONE",
                    "selected_source_or_draft": "draft1",
                    "manifest_hash": "b" * 64,
                    "reservation_owner": "v7-egress-set-state",
                    "certification_group": "t48",
                }},
            }
            draft = {
                "draft_id": "draft1", "pool_egress_id": "pool1",
                "pool_action": "enabled", "runtime_profile_status": "READY",
                "protocol": "amneziawg",
            }
            proc = SimpleNamespace(
                returncode=0,
                stdout="ACTION=controlled_source_reserved\nrestore_backup=/tmp/backup\n",
            )
            with (
                mock.patch.object(
                    self.autoswitch, "controlled_source_topology_diagnostic",
                    return_value=diagnostic,
                ),
                mock.patch.object(
                    self.autoswitch, "_controlled_source_draft_candidates",
                    return_value=[draft],
                ),
                mock.patch.object(self.autoswitch.subprocess, "run", return_value=proc) as run,
            ):
                first = self.autoswitch.consume_approved_controlled_source_topology(args)
                second = self.autoswitch.consume_approved_controlled_source_topology(args)

        self.assertEqual(first["status"], "CONTROLLED_SOURCE_TOPOLOGY_PROVISIONED")
        self.assertTrue(first["registry_write"])
        self.assertEqual(first["users_moved"], 0)
        self.assertFalse(first["routing_mutation"])
        self.assertEqual(second["status"], "ALREADY_CONSUMED_EXACT")
        self.assertEqual(run.call_count, 1)

    def test_controlled_source_topology_prepare_reuses_active_semantic_request(self):
        manifest = {
            "selected_option": "OPTION_1_REBIND_EXISTING_EMPTY_EGRESS",
            "existing_source": "source",
            "selected_source_or_draft": "vless",
            "trial_identity": "10.7.0.16",
            "trial_identity_count": 1,
            "identity_set_fingerprint": "b" * 64,
            "expected_assignment_delta": "10.7.0.16:source->vless",
            "expected_ordinary_assignment_delta": "NONE",
            "expected_ordinary_route_delta": "NONE",
            "capacity_reservation": 1,
            "max_concurrent_transactions": 1,
            "reservation_owner": "tools/v7-egress-set-state",
            "verification": "fresh Matrix baseline + current route",
            "rollback": "restore exact source binding and release reservation",
            "failure_mechanism": "existing controlled certification guard",
            "lease_and_expiry_required": True,
            "packet_required_before_effect": True,
            "restore_barrier_required_before_effect": True,
        }
        manifest["manifest_hash"] = operator_execution.sha256_json(manifest)
        package = {
            "schema_version": (
                operator_execution.CONTROLLED_SOURCE_TOPOLOGY_REQUEST_SCHEMA
            ),
            "status": "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION",
            "active_program": (
                "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
            ),
            "mission": (
                "CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_"
                "SLICE_FEASIBILITY_V1"
            ),
            "decision_set": [
                "APPROVE_REBIND_CONTROLLED_CERTIFICATION_SOURCE",
                "DECLINE",
            ],
            "exact_action": "REBIND_CONTROLLED_CERTIFICATION_SOURCE",
            "manifest": manifest,
            "current_campaign_request_id": "cpsauth_existing",
            "current_campaign_request_hash": "a" * 64,
            "supersedes_source_binding_only": True,
            "tier48_capability_or_campaign_reapproval": False,
            "ordinary_customer_involvement": False,
            "self_expansion_allowed": False,
            "forbidden_effects": ["ordinary_user_movement"],
            "reentry_condition": "exact independent decision",
            "actionable": True,
            "registered": False,
        }
        diagnostic = {
            "status": (
                "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY"
            ),
            "authority_package": package,
            "recommendation": {
                "selected_option": "OPTION_1_REBIND_EXISTING_EMPTY_EGRESS",
                "selected_resource": "vless",
            },
            "forbidden_effects": {"user_movement": 0},
        }
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "operator-execution-audit.jsonl"
            args = self.autoswitch.build_arg_parser().parse_args([
                "--action-class-audit-store", str(audit),
            ])
            with mock.patch.object(
                self.autoswitch,
                "controlled_source_topology_diagnostic",
                return_value=diagnostic,
            ):
                first = (
                    self.autoswitch
                    .controlled_source_topology_authority_request_only(args)
                )
                second = (
                    self.autoswitch
                    .controlled_source_topology_authority_request_only(args)
                )
        self.assertEqual(first["status"], "PASS")
        self.assertEqual(first["registration"]["status"], "REGISTERED")
        self.assertEqual(second["status"], "PASS")
        self.assertEqual(
            second["registration"]["status"],
            "ALREADY_REGISTERED_SEMANTIC_ACTIVE",
        )
        self.assertEqual(
            first["request"]["request_id"],
            second["request"]["request_id"],
        )
        self.assertEqual(first["forbidden_effects"]["user_movement"], 0)

    def test_controlled_source_topology_material_change_supersedes_stale_request(self):
        manifest = {
            "selected_option": "OPTION_2_PROVISION_EXISTING_VALID_DRAFT",
            "existing_source": "source",
            "selected_source_or_draft": "draft-exact",
            "trial_identity": "10.7.0.16",
            "trial_identity_count": 1,
            "identity_set_fingerprint": "b" * 64,
            "expected_assignment_delta": (
                "10.7.0.16:source->NEW_DEDICATED_SOURCE"
            ),
            "expected_ordinary_assignment_delta": "NONE",
            "expected_ordinary_route_delta": "NONE",
            "capacity_reservation": 1,
            "max_concurrent_transactions": 1,
            "reservation_owner": "tools/v7-egress-set-state",
            "verification": "fresh Matrix baseline + current route",
            "rollback": "restore exact source binding and release reservation",
            "failure_mechanism": "existing controlled certification guard",
            "lease_and_expiry_required": True,
            "packet_required_before_effect": True,
            "restore_barrier_required_before_effect": True,
        }
        manifest["manifest_hash"] = operator_execution.sha256_json(manifest)
        payload = {
            "active_program": (
                "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
            ),
            "mission": (
                "CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_"
                "SLICE_FEASIBILITY_V1"
            ),
            "exact_action": (
                "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE"
            ),
            "manifest": manifest,
            "current_campaign_request_id": "cpsauth_existing",
            "current_campaign_request_hash": "a" * 64,
            "supersedes_source_binding_only": True,
            "tier48_capability_or_campaign_reapproval": False,
            "ordinary_customer_involvement": False,
            "self_expansion_allowed": False,
            "forbidden_effects": ["ordinary_user_movement"],
            "reentry_condition": "exact independent decision",
        }
        prior = (
            operator_execution
            .build_controlled_source_topology_authority_request(payload)
        )
        changed_payload = json.loads(json.dumps(payload))
        changed_payload["exact_action"] = (
            "REBIND_CONTROLLED_CERTIFICATION_SOURCE"
        )
        changed_payload["manifest"].update({
            "selected_option": "OPTION_1_REBIND_EXISTING_EMPTY_EGRESS",
            "selected_source_or_draft": "vless",
            "expected_assignment_delta": "10.7.0.16:source->vless",
        })
        changed_payload["manifest"].pop("manifest_hash")
        changed_payload["manifest"]["manifest_hash"] = (
            operator_execution.sha256_json(changed_payload["manifest"])
        )
        replacement = (
            operator_execution
            .build_controlled_source_topology_authority_request(
                changed_payload
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "operator-execution-audit.jsonl"
            operator_execution.register_controlled_source_topology_authority_request(
                prior,
                audit_store=audit,
            )
            registered = (
                operator_execution
                .register_controlled_source_topology_authority_request(
                    replacement,
                    audit_store=audit,
                )
            )
            duplicate = (
                operator_execution
                .register_controlled_source_topology_authority_request(
                    replacement,
                    audit_store=audit,
                )
            )
            current = (
                operator_execution.controlled_source_topology_authority_status(
                    operator_execution.read_audit_records(audit)
                )
            )
            with self.assertRaisesRegex(
                operator_execution.PacketError,
                "controlled_source_topology_request_superseded_stale_preflight",
            ):
                (
                    operator_execution
                    .record_controlled_source_topology_authority_decision(
                        request_id=prior["request_id"],
                        request_hash=prior["request_hash"],
                        decision="DECLINE",
                        actor_id="test-independent-authority",
                        audit_store=audit,
                    )
                )
            records = operator_execution.read_audit_records(audit)
        self.assertEqual(
            registered["status"],
            "REGISTERED_AFTER_STALE_PREFLIGHT_INVALIDATION",
        )
        self.assertEqual(len(registered["invalidated_requests"]), 1)
        self.assertEqual(
            registered["invalidated_requests"][0]["request_id"],
            prior["request_id"],
        )
        self.assertEqual(
            duplicate["status"],
            "ALREADY_REGISTERED_EXACT",
        )
        self.assertEqual(current["status"], "PENDING")
        self.assertEqual(current["request_id"], replacement["request_id"])
        self.assertEqual(
            len([
                row for row in records
                if row.get("record_type")
                == (
                    operator_execution
                    .CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE
                )
            ]),
            1,
        )

    def test_controlled_certification_pool_projection_is_compact_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("users.registry").write_text(
                "\n".join([
                    "ip=10.7.0.16 enabled=1 current=controlled certification_user=1 certification_group=pool",
                    "ip=10.7.0.17 enabled=1 current=controlled certification_user=1 certification_group=pool",
                    "ip=10.7.0.18 enabled=1 current=controlled certification_user=1 certification_group=pool",
                    "ip=10.7.0.19 enabled=1 current=other certification_user=1 certification_group=pool",
                    "ip=10.0.0.2 enabled=1 current=controlled",
                ]) + "\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=controlled enabled=1 controlled_certification_source=1 certification_group=pool\n"
                "id=other enabled=1\n",
                encoding="utf-8",
            )
            result = self.autoswitch.controlled_certification_pool_status(state_dir)
            self.assertEqual(
                result["status"],
                "CONTROLLED_CERTIFICATION_POOL_INSUFFICIENT_FOR_TIER_5",
            )
            self.assertEqual(result["total_enabled_certification_users"], 4)
            self.assertEqual(
                result["max_enabled_certification_users_on_one_active_source"], 3,
            )
            self.assertEqual(result["missing_users_for_tier_5"], 5)
            self.assertEqual(
                result[
                    "max_enabled_certification_users_on_one_isolated_active_source"
                ],
                0,
            )
            self.assertEqual(result["mixed_controlled_source_count"], 1)
            self.assertEqual(
                result["exact_blocker"],
                "active_controlled_source_contains_non_certification_users",
            )
            self.assertFalse(
                result["active_source_projections"][0][
                    "source_isolated_for_controlled_failure"
                ]
            )
            self.assertFalse(result["raw_user_list_stored"])
            self.assertFalse(result["ordinary_customer_reclassification_allowed"])
            rendered = json.dumps(result, sort_keys=True)
            self.assertNotIn("10.7.0.16", rendered)
            self.assertNotIn("10.0.0.2", rendered)

    def test_controlled_certification_source_candidate_requires_fresh_healthy_matrix_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("users.registry").write_text("", encoding="utf-8")
            state_dir.joinpath("egress.registry").write_text(
                "id=healthy protocol=wireguard type=interface interface=wg1 enabled=1\n"
                "id=dead protocol=amneziawg type=interface interface=wg2 enabled=1\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress-diagnose.state").write_text(
                "updated=2099-01-01T00:00:00Z\n"
                "healthy_diagnose_reason=OK\n"
                "healthy_diagnose_severity=OK\n"
                "healthy_diagnose_detail=handshake_age_seconds=10\n"
                "dead_diagnose_reason=curl_failed_and_handshake_stale\n"
                "dead_diagnose_severity=FAIL\n"
                "dead_diagnose_detail=handshake_age_seconds=999999\n",
                encoding="utf-8",
            )
            state_dir.joinpath("service-matrix.json").write_text(json.dumps({
                "updated": "2099-01-01T00:00:00+00:00",
                "items": {
                    "healthy": {
                        "services": {
                            "google": {
                                "ok": True,
                                "status": "OK",
                                "tested_at": "2099-01-01T00:00:00+00:00",
                            },
                        },
                    },
                    "dead": {
                        "services": {
                            "google": {
                                "ok": False,
                                "status": "FAIL",
                                "tested_at": "2099-01-01T00:00:00+00:00",
                            },
                        },
                    },
                },
            }), encoding="utf-8")

            result = self.autoswitch.controlled_certification_pool_status(
                state_dir,
            )

        candidates = {
            row["source_id"]: row
            for row in result["isolated_source_candidates"]
        }
        self.assertEqual(
            candidates["healthy"]["baseline_health"]["status"],
            "PASS_HEALTHY_BASELINE",
        )
        self.assertEqual(
            candidates["dead"]["baseline_health"]["status"],
            "STOP_SAFE_BASELINE_UNHEALTHY",
        )
        self.assertEqual(
            [
                row["source_id"]
                for row in result["healthy_isolated_source_candidates"]
            ],
            ["healthy"],
        )
        self.assertFalse(
            candidates["dead"]["baseline_health"]["raw_service_details_stored"]
        )
        self.assertEqual(
            candidates["dead"]["baseline_health"]["root_cause_class"],
            "EXTERNAL_INFRASTRUCTURE_OR_ACCESS_REQUIRED",
        )
        self.assertEqual(
            candidates["dead"]["baseline_health"]["exact_external_owner"],
            "EXTERNAL_AMNEZIAWG_PEER_OR_CREDENTIAL_PROVIDER",
        )
        self.assertEqual(
            candidates["dead"]["baseline_health"]["failed_producer_consumer_link"],
            "EXTERNAL_AMNEZIAWG_PEER_RESPONSE_OR_MATCHING_PROFILE"
            "->LOCAL_HANDSHAKE->MATRIX_BASELINE",
        )
        self.assertEqual(
            candidates["healthy"]["baseline_health"]["root_cause_class"],
            "NONE",
        )

    def test_substrate_authority_entrypoint_reuses_existing_owner_and_has_zero_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.16 enabled=1 current=controlled certification_user=1\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=controlled enabled=1 controlled_certification_source=1\n",
                encoding="utf-8",
            )
            state_dir.joinpath("service-matrix.json").write_text(json.dumps({
                "updated": "2099-01-01T00:00:00+00:00",
                "items": {
                    "controlled": {
                        "services": {
                            "google": {
                                "ok": True,
                                "status": "OK",
                                "tested_at": "2099-01-01T00:00:00+00:00",
                            },
                        },
                    },
                },
            }), encoding="utf-8")
            policy_file = root / "policy.json"
            policy_file.write_text(
                json.dumps({"delegated_autonomy_policy": {"contract_id": "sdpc", "contract_hash": "h"}}),
                encoding="utf-8",
            )
            audit = root / "audit.jsonl"
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--policy-file", str(policy_file),
                "--action-class-audit-store", str(audit),
            ])
            request = {
                "request_id": "cpsauth_r1_unit",
                "request_hash": "hash",
                "reentry_condition": "decision",
            }
            with mock.patch.object(
                self.autoswitch.operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={"ok": True, "policy": {"max_users_per_action": 48}},
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "build_controlled_certification_substrate_authority_request",
                return_value=request,
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "register_controlled_certification_substrate_authority_request",
                return_value={"status": "REGISTERED", "audit_write": True},
            ):
                result = (
                    self.autoswitch
                    .controlled_certification_substrate_authority_request_only(args)
                )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["authority_classification"], "ENGINEERING_AUTHORITY")
        self.assertTrue(result["forbidden_effects"]["audit_write"])
        self.assertFalse(result["forbidden_effects"]["policy_write"])
        self.assertFalse(result["forbidden_effects"]["registry_write"])
        self.assertFalse(result["forbidden_effects"]["identity_creation"])
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)

    def test_substrate_request_selects_existing_empty_isolated_source_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.16 enabled=1 current=mixed certification_user=1\n"
                "ip=10.0.0.2 enabled=1 current=mixed\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=mixed type=interface enabled=1 controlled_certification_source=1\n"
                "id=spare type=interface protocol=wireguard enabled=1\n"
                "id=execution type=interface enabled=1 execution_reserved=1 "
                "production_assignment_allowed=false\n",
                encoding="utf-8",
            )
            state_dir.joinpath("service-matrix.json").write_text(json.dumps({
                "updated": "2099-01-01T00:00:00+00:00",
                "items": {
                    "spare": {
                        "services": {
                            "google": {
                                "ok": True,
                                "status": "OK",
                                "tested_at": "2099-01-01T00:00:00+00:00",
                            },
                        },
                    },
                },
            }), encoding="utf-8")
            policy_file = root / "policy.json"
            policy_file.write_text(
                json.dumps({
                    "delegated_autonomy_policy": {
                        "contract_id": "sdpc",
                        "contract_hash": "h",
                    },
                }),
                encoding="utf-8",
            )
            audit = root / "audit.jsonl"
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--policy-file", str(policy_file),
                "--action-class-audit-store", str(audit),
            ])
            captured = {}

            def build_request(**kwargs):
                captured.update(kwargs)
                return {
                    "request_id": "cpsauth_r1_isolated",
                    "request_hash": "hash",
                    "reentry_condition": "decision",
                }

            with mock.patch.object(
                self.autoswitch.operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={
                    "ok": True,
                    "policy": {"max_users_per_action": 48},
                },
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "build_controlled_certification_substrate_authority_request",
                side_effect=build_request,
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "register_controlled_certification_substrate_authority_request",
                return_value={"status": "REGISTERED", "audit_write": True},
            ):
                result = (
                    self.autoswitch
                    .controlled_certification_substrate_authority_request_only(args)
                )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(captured["source_id"], "spare")

    def test_substrate_request_keeps_shared_planner_target_unbound_until_fresh_stage_revalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            state_dir.mkdir()
            policy_file = root / "policy.json"
            policy_file.write_text("{}", encoding="utf-8")
            audit = root / "audit.jsonl"
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(state_dir),
                "--policy-file", str(policy_file),
                "--action-class-audit-store", str(audit),
            ])
            pool = {
                "active_source_projections": [{
                    "source_id": "failed-controlled",
                    "source_isolated_for_controlled_failure": True,
                    "enabled_certification_users_on_source": 40,
                    "baseline_health": {"ok": False},
                }],
                "healthy_isolated_source_candidates": [],
                "execution_only_controlled_target_candidates": [],
            }
            captured = {}

            def build_request(**kwargs):
                captured.update(kwargs)
                return {
                    "request_id": "cpsauth_r1_shared_target",
                    "request_hash": "hash",
                    "reentry_condition": "decision",
                }

            with mock.patch.object(
                self.autoswitch,
                "controlled_certification_pool_status",
                return_value=pool,
            ), mock.patch.object(
                self.autoswitch,
                "controlled_campaign_target_selection_diagnostic",
                return_value={
                    "selection": {"selected_target_id": "shared-healthy"},
                    "targets": [{"target_id": "shared-healthy"}],
                    "inventory_fingerprint": "i" * 64,
                },
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={
                    "ok": True,
                    "policy": {
                        "max_users_per_action": 48,
                        "policy_profile": (
                            self.autoswitch.operator_execution
                            .AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
                        ),
                    },
                },
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "build_controlled_certification_substrate_authority_request",
                side_effect=build_request,
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "register_controlled_certification_substrate_authority_request",
                return_value={"status": "REGISTERED", "audit_write": True},
            ):
                result = (
                    self.autoswitch
                    .controlled_certification_substrate_authority_request_only(args)
                )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(captured["source_id"], "failed-controlled")
        self.assertEqual(captured["controlled_target_id"], "")

    def test_execution_only_target_is_separate_and_never_ordinary_eligible(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.16 enabled=1 current=controlled "
                "certification_user=1 certification_group=pool\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=controlled type=interface enabled=1 "
                "controlled_certification_source=1 certification_group=pool\n"
                "id=execution type=interface protocol=amneziawg enabled=1 "
                "role=EXECUTION_ONLY execution_reserved=1 canary_reserved=true "
                "manual_only=1 reserve_only=1 autoswitch_allowed=false "
                "rebalance_allowed=false production_assignment_allowed=false "
                "reservation_owner=operator_execution_governance\n",
                encoding="utf-8",
            )
            state_dir.joinpath("service-matrix.json").write_text(json.dumps({
                "updated": "2099-01-01T00:00:00+00:00",
                "items": {
                    "controlled": {
                        "services": {
                            "google": {
                                "ok": False,
                                "status": "FAIL",
                                "tested_at": "2099-01-01T00:00:00+00:00",
                            },
                        },
                    },
                    "execution": {
                        "services": {
                            "google": {
                                "ok": True,
                                "status": "OK",
                                "tested_at": "2099-01-01T00:00:00+00:00",
                            },
                        },
                    },
                },
            }), encoding="utf-8")

            result = self.autoswitch.controlled_certification_pool_status(
                state_dir,
            )

        self.assertEqual(result["healthy_isolated_source_candidates"], [])
        self.assertEqual(
            [
                row["source_id"]
                for row in result[
                    "healthy_execution_only_controlled_target_candidates"
                ]
            ],
            ["execution"],
        )
        target = result[
            "healthy_execution_only_controlled_target_candidates"
        ][0]
        self.assertFalse(target["ordinary_production_eligible"])
        self.assertTrue(target["controlled_certification_target_eligible"])

    def test_execution_only_target_requires_exact_approved_campaign_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("users.registry").write_text(
                "ip=10.7.0.16 enabled=1 current=controlled "
                "certification_user=1\n",
                encoding="utf-8",
            )
            state_dir.joinpath("egress.registry").write_text(
                "id=controlled type=interface enabled=1 "
                "controlled_certification_source=1\n"
                "id=execution type=interface enabled=1 role=EXECUTION_ONLY "
                "execution_reserved=1 canary_reserved=1 manual_only=1 "
                "reserve_only=1 autoswitch_allowed=false "
                "rebalance_allowed=false production_assignment_allowed=false "
                "reservation_owner=operator_execution_governance\n",
                encoding="utf-8",
            )
            args = argparse.Namespace(
                state_dir=str(state_dir),
                action_class_audit_store=str(state_dir / "audit.jsonl"),
                controlled_certification_campaign_request_id="cpsauth_r1_exact",
                controlled_certification_campaign_request_hash="h" * 64,
                controlled_certification_campaign_target="execution",
                target_egress="execution",
                source_egress="controlled",
                emergency_failover_autonomy=True,
            )
            with mock.patch.object(
                self.autoswitch.operator_execution,
                "read_audit_records",
                return_value=[],
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "controlled_certification_substrate_authority_status",
                return_value={
                    "status": "APPROVED",
                    "request_id": "cpsauth_r1_exact",
                    "request_hash": "h" * 64,
                    "request": {
                        "scope": {
                            "source_id": "controlled",
                            "controlled_target_id": "execution",
                            "controlled_target_admission_class": (
                                "EXECUTION_ONLY_CONTROLLED_CERTIFICATION_TARGET"
                            ),
                        },
                        "controlled_target_contract": {
                            "target_id": "execution",
                            "ordinary_production_assignment_allowed": False,
                            "certification_only_assignment_allowed": True,
                        },
                    },
                },
            ):
                admitted = (
                    self.autoswitch
                    .controlled_campaign_execution_target_admission(args)
                )
                args.controlled_certification_campaign_request_hash = "x" * 64
                denied = (
                    self.autoswitch
                    .controlled_campaign_execution_target_admission(args)
                )

        self.assertTrue(admitted["ok"], admitted["blockers"])
        self.assertFalse(admitted["ordinary_production_eligible"])
        self.assertFalse(denied["ok"])
        self.assertIn(
            "controlled_campaign_request_hash_mismatch",
            denied["blockers"],
        )

    def test_tier48_active_projects_exact_m8_pool_terminal(self):
        cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(
            encoding="utf-8",
        )
        live = self.sync._markdown_field_table(self.sync._markdown_section(
            cps, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        status = {
            "max_users_per_action": 48,
            "max_concurrent_transactions": 1,
            "action_class": "channel hard-fail failover",
            "contract_hash": "a" * 64,
            "policy_scope_hash": "b" * 64,
            "authority_request_id": "sdpauth_r1_" + ("c" * 24),
            "authority_request_hash": "c" * 64,
            "expires_at": "2099-01-01T00:00:00+00:00",
            "allowed_failure_families": ["channel_hard_fail"],
            "runtime_scope_axes": {
                "controlled_certification_runtime_max": 48,
                "ordinary_production_runtime_max": 4,
                "controlled_production_proven_max": 0,
                "ordinary_production_proven_max": 4,
            },
            "pending_tier_authority_request": {"status": "NONE"},
            "service_failure_causal_integrity": {
                "final_verdict": "PASS",
                "invalid_states": [],
                "open_incident_projections": [],
            },
            "controlled_certification_pool": {
                "status": "CONTROLLED_CERTIFICATION_POOL_INSUFFICIENT_FOR_TIER_5",
                "fingerprint": "d" * 64,
                "total_enabled_certification_users": 4,
                "active_controlled_source_count": 1,
                "max_enabled_certification_users_on_one_active_source": 3,
                "missing_users_for_tier_5": 2,
                "exact_blocker": "fewer_than_5_enabled_certification_users_on_one_active_controlled_source",
                "responsible_existing_owner": "existing Controlled Production owners",
                "reentry_condition": "five users on one controlled source",
            },
        }
        projection, detail = self.sync._service_failure_action_class_reuse_projection(
            status, live, root=ROOT,
        )
        expected = (
            "ENGINEERING_COMPLETE_AWAITING_EXACT_CONTROLLED_PRODUCTION_POOL_OR_AUTHORITY"
        )
        self.assertEqual(projection["PRODUCT_EVOLUTION_FRONTIER"].strip("`"), expected)
        self.assertEqual(projection["T48_M8_STATUS"].strip("`"), expected)
        self.assertEqual(detail["legal_terminal"], expected)
        self.assertEqual(
            detail["controlled_certification_pool"][
                "max_enabled_certification_users_on_one_active_source"
            ],
            3,
        )

    def test_approved_substrate_decision_becomes_safe_m8_successor(self):
        cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(
            encoding="utf-8",
        )
        live = self.sync._markdown_field_table(self.sync._markdown_section(
            cps, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        status = {
            "max_users_per_action": 48,
            "max_concurrent_transactions": 1,
            "action_class": "channel hard-fail failover",
            "contract_hash": "a" * 64,
            "policy_scope_hash": "b" * 64,
            "authority_request_id": "sdpauth_r1_" + ("c" * 24),
            "authority_request_hash": "c" * 64,
            "expires_at": "2099-01-01T00:00:00+00:00",
            "allowed_failure_families": ["channel_hard_fail"],
            "pending_tier_authority_request": {"status": "NONE"},
            "service_failure_causal_integrity": {
                "final_verdict": "PASS",
                "invalid_states": [],
                "open_incident_projections": [],
            },
            "controlled_certification_pool": {
                "status": "CONTROLLED_CERTIFICATION_POOL_INSUFFICIENT_FOR_TIER_5",
                "fingerprint": "d" * 64,
                "total_enabled_certification_users": 4,
                "active_controlled_source_count": 1,
                "max_enabled_certification_users_on_one_active_source": 3,
                "missing_users_for_tier_5": 2,
                "exact_blocker": "fewer_than_5_enabled_certification_users_on_one_active_controlled_source",
                "responsible_existing_owner": "existing Controlled Production owners",
                "reentry_condition": "five users on one controlled source",
            },
            "controlled_certification_substrate_authority": {
                "status": "APPROVED",
                "request_id": "cpsauth_r1_exact",
                "request_hash": "e" * 64,
                "expires_at": "2099-01-01T00:00:00+00:00",
                "decision": "APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN",
                "decision_id": "cpsdec_exact",
                "actor_id": "authority-owner",
                "semantic_request_fingerprint": "f" * 64,
            },
        }
        projection, detail = self.sync._service_failure_action_class_reuse_projection(
            status, live, root=ROOT,
        )
        expected = (
            "CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVED_INCREMENTAL_POOL_REQUIRED"
        )
        self.assertEqual(
            projection["PRODUCT_EVOLUTION_FRONTIER"].strip("`"), expected,
        )
        self.assertEqual(
            projection["T48_M8_STATUS"].strip("`"),
            "CONTROLLED_SUBSTRATE_AUTHORITY_APPROVED_T48_M8_REENTRY_READY",
        )
        self.assertEqual(
            projection["T48_CONTROLLED_SUBSTRATE_AUTHORITY_DECISION"].strip("`"),
            "APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN",
        )
        self.assertEqual(
            projection["SERVICE_FAILURE_EFFECTIVE_RUNTIME_TIER"].strip("`"), "4",
        )
        self.assertEqual(
            projection["SERVICE_FAILURE_CONTEXTUAL_RUNTIME_TIERS"].strip("`"),
            "CONTROLLED_CERTIFICATION=48; ORDINARY_PRODUCTION=4",
        )
        self.assertEqual(
            projection["CURRENT_ACTION_CLASS_RUNTIME_ENABLED_TIER"].strip("`"),
            "TIER_4_SERIAL_COHORT",
        )
        self.assertEqual(detail["legal_terminal"], expected)

    def test_tier48_pending_substrate_request_is_exact_primary_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps_path.parent.mkdir(parents=True)
            shutil.copy2(
                ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path,
            )
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                cps_path.read_text(encoding="utf-8"),
                "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
            ))
            contract_hash = live["CURRENT_AUTHORITY_CONTRACT_HASH"].strip("`")
            runtime_status = {
                "schema_version": "v7.standing-delegated-policy-runtime-status.v1",
                "status": "PASS",
                "ok": True,
                "contract_status": "ACTIVE",
                "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                "authority_decision": "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                "audit_provenance_verified": True,
                "contract_id": live["CURRENT_AUTHORITY_CONTRACT_ID"].strip("`"),
                "contract_hash": contract_hash,
                "authority_request_id": live["CURRENT_AUTHORITY_REQUEST_ID"].strip("`"),
                "authority_request_hash": live["CURRENT_AUTHORITY_REQUEST_HASH"].strip("`"),
                "expires_at": "2099-01-01T00:00:00+00:00",
                "policy_scope_hash": live["CURRENT_AUTHORITY_POLICY_SCOPE_HASH"].strip("`"),
                "action_class": "channel hard-fail failover",
                "max_users_per_action": 48,
                "max_concurrent_transactions": 1,
                "allowed_failure_families": [
                    "channel_hard_fail", "service_specific_failure",
                ],
                "cooldown": {
                    "per_user_seconds": 1800,
                    "per_source_target_pair_seconds": 1800,
                },
                "anti_flap": "PASS",
                "pending_tier_authority_request": {
                    "status": "NONE", "pending_count": 0,
                },
                "controlled_certification_substrate_authority": {
                    "status": "PENDING",
                    "request_id": "cpsauth_r1_exact",
                    "request_hash": "e" * 64,
                    "created_at": "2026-07-28T00:00:00+00:00",
                    "expires_at": "2099-01-01T00:00:00+00:00",
                    "semantic_request_fingerprint": "f" * 64,
                    "decision": "",
                    "decision_id": "",
                    "actor_id": "",
                    "admitted_subscopes": [],
                },
                "controlled_certification_pool": {
                    "status": "CONTROLLED_CERTIFICATION_POOL_INSUFFICIENT_FOR_TIER_5",
                    "fingerprint": "d" * 64,
                    "total_enabled_certification_users": 4,
                    "active_controlled_source_count": 1,
                    "max_enabled_certification_users_on_one_active_source": 3,
                    "missing_users_for_tier_5": 2,
                    "exact_blocker": "fewer_than_5_enabled_certification_users_on_one_active_controlled_source",
                    "responsible_existing_owner": "existing Controlled Production owners",
                    "reentry_condition": "five users on one controlled source",
                },
                "service_failure_causal_integrity": {
                    "schema_version": "v7.service-failure-causal-integrity-status.v1",
                    "final_verdict": "PASS",
                    "invalid_states": [],
                    "open_incident_projections": [{
                        "incident_id": live["CURRENT_VLESS_INCIDENT_ID"].strip("`"),
                        "incident_generation": "generation-runtime-drained",
                        "source_channel": "vless",
                        "incident_state": "SOURCE_SCOPE_EMPTY",
                        "affected_scope_count": 0,
                        "protected_scope_count": 0,
                        "unresolved_scope_count": 0,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                        "affected_scope_fingerprint": "affected-empty",
                        "protected_scope_fingerprint": "protected-empty",
                        "unresolved_scope_fingerprint": "unresolved-empty",
                        "explicitly_excluded_or_recovered_scope_fingerprint": "excluded-empty",
                        "last_execution_feedback_id": "execfb_last",
                        "last_outcome_id": "outcome_last",
                        "last_learning_id": "learning_last",
                        "last_packet_id": "packet_last",
                        "next_required_consumer": "tools/v7-service-matrix-refresh-all",
                        "reentry_condition": "fresh Matrix observation",
                    }],
                },
            }
            result = self.sync.reconcile_active_standing_delegated_policy_to_cps(
                runtime_status, root=root,
            )
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(
                result["next_action"],
                "ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY",
            )
            updated_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                updated_live["CURRENT_STOP_CONDITION"].strip("`"),
                "ENGINEERING_AUTHORITY",
            )
            self.assertEqual(
                updated_live["CURRENT_NEXT_ACTION_ID"].strip("`"),
                "ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY",
            )
            self.assertEqual(
                updated_live["PROGRAM_TERMINAL_STATE"].strip("`"),
                "ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY",
            )
            self.assertEqual(
                updated_live["CURRENT_PROGRAM_EXECUTION_FRONTIER"].strip("`"),
                "WAITING_INPUT:ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY",
            )
            self.assertEqual(
                updated_live["EXTERNAL_INPUT_TYPE"].strip("`"),
                "EXACT_CONTROLLED_CERTIFICATION_SUBSTRATE_AUTHORITY_DECISION",
            )
            self.assertNotEqual(
                updated_live["PROGRAM_TERMINAL_STATE"].strip("`"),
                "REAL_WORLD_LIMIT_WAIT_FOR_FRESH_MATCHING_SERVICE_FAILURE_EVENT",
            )
            runtime_status["controlled_certification_substrate_authority"].update({
                "status": "APPROVED",
                "decision": (
                    "APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN"
                ),
                "decision_id": "cpsdec_exact",
                "actor_id": "independent-authority-owner",
                "admitted_subscopes": [
                    "IDENTITY_PROVISIONING",
                    "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT",
                    "CONTROLLED_SOURCE_CONDITION",
                    "PROGRESSIVE_CAMPAIGN_EXECUTION",
                ],
            })
            approved = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(approved["final_verdict"], "PASS", approved)
            self.assertEqual(
                approved["next_action"],
                "CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVED_INCREMENTAL_POOL_REQUIRED",
            )
            approved_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                approved_live["CURRENT_EXECUTION_FRONTIER"].strip("`"), "NONE",
            )
            self.assertEqual(
                approved_live["CONTINUATION_DECISION"].strip("`"),
                "CONTINUE_PROGRAM_FRONTIER",
            )
            self.assertEqual(
                approved_live["CURRENT_STOP_CONDITION"].strip("`"), "NONE",
            )
            self.assertTrue(
                approved_live["AUTHORITY_REQUIRED_NOW"].strip("`").startswith(
                    "NO_INSIDE_EXISTING_ENGINEERING_PROGRAM_SCOPE"
                )
            )
            runtime_status[
                "controlled_certification_substrate_authority"
            ]["source_precondition_status"] = (
                "STOP_SAFE_MIXED_OR_UNAVAILABLE_SOURCE"
            )
            runtime_status["controlled_certification_pool"].update({
                "max_enabled_certification_users_on_one_isolated_active_source": 0,
                "mixed_controlled_source_count": 1,
                "exact_blocker": (
                    "active_controlled_source_contains_non_certification_users"
                ),
            })
            invalid_source = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                invalid_source["final_verdict"], "PASS", invalid_source,
            )
            self.assertEqual(
                invalid_source["next_action"],
                "ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_ISOLATED_SOURCE_REQUEST_REQUIRED",
            )
            invalid_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                invalid_live["CURRENT_STOP_CONDITION"].strip("`"),
                "ENGINEERING_AUTHORITY",
            )
            self.assertEqual(
                invalid_live["CURRENT_EXECUTION_FRONTIER"].strip("`"), "NONE",
            )
            self.assertEqual(
                invalid_live["CURRENT_PROGRAM_EXECUTION_FRONTIER"].strip("`"),
                "WAITING_INPUT:ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_ISOLATED_SOURCE_REQUEST_REQUIRED",
            )
            self.assertTrue(
                invalid_live["AUTHORITY_REQUIRED_NOW"].strip("`").startswith(
                    "YES_FOR_CERTIFICATION_POOL_OR_DELIBERATE_CONTROLLED_CONDITION"
                )
            )
            runtime_status[
                "controlled_certification_substrate_authority"
            ]["source_precondition_status"] = (
                "PASS_READY_FOR_APPROVED_SETUP"
            )
            isolated_candidate = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                isolated_candidate["final_verdict"], "PASS",
                isolated_candidate,
            )
            self.assertEqual(
                isolated_candidate["next_action"],
                "CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVED_INCREMENTAL_POOL_REQUIRED",
            )
            runtime_status[
                "controlled_certification_substrate_authority"
            ].update({
                "source_id": "1",
                "source_precondition_status": (
                    "STOP_SAFE_SOURCE_BASELINE_UNHEALTHY"
                ),
            })
            runtime_status["controlled_certification_pool"].update({
                "max_enabled_certification_users_on_one_isolated_active_source": 48,
                "active_source_projections": [{
                    "source_id": "1",
                    "enabled_non_certification_users_on_source": 0,
                }],
            })
            baseline_blocked = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                baseline_blocked["final_verdict"], "PASS",
                baseline_blocked,
            )
            self.assertEqual(
                baseline_blocked["next_action"],
                "EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED",
            )
            baseline_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                baseline_live["CURRENT_STOP_CONDITION"].strip("`"),
                "EXTERNAL_OWNER_REQUIRED",
            )
            self.assertEqual(
                baseline_live["EXTERNAL_INPUT_TYPE"].strip("`"),
                "EXACT_CONTROLLED_CERTIFICATION_SOURCE_HEALTHY_BASELINE",
            )
            self.assertEqual(
                baseline_live["AUTHORITY_REQUIRED_NOW"].strip("`"),
                "NO_NEW_AUTHORITY_REQUIRED; EXACT APPROVED SOURCE MUST FIRST RECOVER THROUGH ITS EXISTING EXTERNAL/EGRESS OWNER",
            )
            self.assertEqual(
                baseline_live["PROGRAM_TERMINAL_CLASS"].strip("`"),
                "EXTERNAL_OWNER_REQUIRED",
            )
            self.assertEqual(
                baseline_live["PROGRAM_TERMINAL_STATE"].strip("`"),
                "EXTERNAL_OWNER_REQUIRED_EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED",
            )
            self.assertEqual(
                baseline_live["CONTROLLED_SOURCE_ROOT_CAUSE_CLASS"].strip("`"),
                "UNKNOWN",
            )
            self.assertEqual(
                baseline_live["CURRENT_POOL_AND_CAMPAIGN_STATE"].strip("`"),
                "48 dedicated certification identities on exact source 1; "
                "controlled production proven max=0; completed stages=NONE; "
                "next stage=NONE",
            )
            runtime_status["controlled_source_topology"] = {
                "status": (
                    "CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY"
                ),
                "capability_map_fingerprint": "topology-map-fingerprint",
                "recommendation": {
                    "selected_option": (
                        "OPTION_1_REBIND_EXISTING_EMPTY_EGRESS"
                    ),
                    "selected_resource": "vless",
                    "required_authority_action": (
                        "REBIND_CONTROLLED_CERTIFICATION_SOURCE"
                    ),
                },
                "authority_package": {
                    "actionable": True,
                    "exact_action": (
                        "REBIND_CONTROLLED_CERTIFICATION_SOURCE"
                    ),
                    "request_id": "cstopauth_r1_exact",
                    "request_hash": "f" * 64,
                },
                "authority_lifecycle": {
                    "status": "PENDING",
                    "matching_current_preflight": True,
                    "request_id": "cstopauth_r1_exact",
                    "request_hash": "f" * 64,
                    "expires_at": "2099-01-01T00:00:00+00:00",
                    "decision": "",
                    "decision_id": "",
                },
                "production_preflight": {
                    "manifest": {"manifest_hash": "m" * 64},
                },
            }
            topology_boundary = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                topology_boundary["next_action"],
                "ENGINEERING_AUTHORITY_REBIND_CONTROLLED_CERTIFICATION_SOURCE_REQUIRED",
            )
            topology_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                topology_live["CURRENT_STOP_CONDITION"].strip("`"),
                "ENGINEERING_AUTHORITY",
                topology_boundary,
            )
            self.assertEqual(
                topology_live[
                    "CONTROLLED_SOURCE_TOPOLOGY_SELECTED_RESOURCE"
                ].strip("`"),
                "vless",
            )
            self.assertEqual(
                topology_live[
                    "CONTROLLED_SOURCE_TOPOLOGY_AUTHORITY_STATUS"
                ].strip("`"),
                "PENDING",
            )
            runtime_status["controlled_source_topology"][
                "authority_package"
            ]["actionable"] = False
            runtime_status["controlled_source_topology"][
                "authority_lifecycle"
            ].update({
                "status": "APPROVED",
                "decision": (
                    "APPROVE_REBIND_CONTROLLED_CERTIFICATION_SOURCE"
                ),
                "decision_id": "cstopdec_exact",
            })
            topology_approved = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                topology_approved["next_action"],
                "CONTROLLED_SOURCE_TOPOLOGY_APPROVED_PACKET_AND_"
                "RESTORE_BARRIER_PREFLIGHT_REQUIRED",
            )
            topology_approved_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                topology_approved_live["CURRENT_STOP_CONDITION"].strip("`"),
                "NONE",
                topology_approved,
            )
            self.assertEqual(
                topology_approved_live["CURRENT_EXECUTION_FRONTIER"].strip("`"),
                "CONTROLLED_SOURCE_TOPOLOGY_APPROVED_PACKET_AND_"
                "RESTORE_BARRIER_PREFLIGHT_REQUIRED",
            )
            self.assertEqual(
                topology_approved_live[
                    "CONTROLLED_SOURCE_TOPOLOGY_AUTHORITY_STATUS"
                ].strip("`"),
                "APPROVED",
            )
            runtime_status["controlled_source_topology"][
                "recommendation"
            ].update({
                "selected_option": "OPTION_2_PROVISION_EXISTING_VALID_DRAFT",
                "selected_resource": "draft-exact",
                "required_authority_action": (
                    "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE"
                ),
            })
            runtime_status["controlled_source_topology"][
                "authority_package"
            ].update({
                "actionable": True,
                "exact_action": (
                    "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE"
                ),
                "request_id": "cstopauth_r1_provision",
                "request_hash": "a" * 64,
            })
            runtime_status["controlled_source_topology"][
                "authority_lifecycle"
            ].update({
                "status": "PENDING",
                "matching_current_preflight": True,
                "request_id": "cstopauth_r1_provision",
                "request_hash": "a" * 64,
                "decision": "",
                "decision_id": "",
            })
            provision_boundary = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                provision_boundary["next_action"],
                "ENGINEERING_AUTHORITY_PROVISION_DEDICATED_CONTROLLED_"
                "CERTIFICATION_SOURCE_REQUIRED",
            )
            provision_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertIn(
                "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
                provision_live["AUTOMATIC_REENTRY_CONDITION"],
            )
            runtime_status["controlled_source_topology"].update({
                "status": (
                    "CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED"
                ),
                "POST_TRIAL_CONTROLLED_TOPOLOGY_DECISION_DIAGNOSTIC": {
                    "status": (
                        "POST_TRIAL_DEDICATED_DRAFT_SELECTION_SUBOPTIMAL"
                    ),
                    "campaign_identity_count": 48,
                    "campaign_identity_locations": {
                        "1": 46,
                        "vless": 1,
                        "exec": 1,
                    },
                },
                "CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_PLAN": {
                    "exact_external_resource": (
                        "OWNER_VERIFIED_ISOLATED_CONTROLLED_TARGET_OR_"
                        "CORRELATION_DISTINCT_TARGET_SET_WITH_USABLE_"
                        "CAPACITY_AT_LEAST_48"
                    ),
                    "exact_external_owner": (
                        "EXTERNAL_EGRESS_PEER_OR_PROFILE_PROVIDER"
                    ),
                    "existing_owner_reentry": (
                        "admin draft -> Matrix -> ranking"
                    ),
                },
                "CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_RECOMMENDATION": {
                    "status": "EXTERNAL_RESOURCE_REQUIRED",
                },
            })
            runtime_status["controlled_source_topology"][
                "recommendation"
            ].update({
                "selected_option": "",
                "selected_resource": "",
                "required_authority_action": "",
            })
            runtime_status["controlled_source_topology"][
                "authority_package"
            ].update({
                "actionable": False,
                "exact_action": "",
            })
            runtime_status["controlled_source_topology"][
                "authority_lifecycle"
            ].update({
                "status": "NONE",
                "matching_current_preflight": False,
                "decision": "",
                "decision_id": "",
            })
            full_path_boundary = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                full_path_boundary["next_action"],
                "EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_FULL_PATH_"
                "TARGET_CAPACITY_REQUIRED",
            )
            self.assertEqual(
                full_path_boundary["behavior_change"],
                "CONTROLLED_TOPOLOGY_FULL_PATH_SELECTION_RUNTIME_CONSUMED",
            )
            full_path_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                full_path_live["CURRENT_STOP_CONDITION"].strip("`"),
                "EXTERNAL_OWNER_REQUIRED",
            )
            self.assertEqual(
                full_path_live["PROGRAM_TERMINAL_CLASS"].strip("`"),
                "EXTERNAL_OWNER_REQUIRED",
            )
            self.assertEqual(
                full_path_live["EXTERNAL_INPUT_TYPE"].strip("`"),
                "OWNER_VERIFIED_ISOLATED_CONTROLLED_TARGET_OR_"
                "CORRELATION_DISTINCT_TARGET_SET_WITH_USABLE_"
                "CAPACITY_AT_LEAST_48",
            )
            self.assertEqual(
                full_path_live[
                    "CONTROLLED_SOURCE_TOPOLOGY_SELECTED_OPTION"
                ].strip("`"),
                "NONE",
            )
            self.assertIn(
                "locations={\"1\":46,\"exec\":1,\"vless\":1}",
                full_path_live["CURRENT_POOL_AND_CAMPAIGN_STATE"],
            )
            runtime_status["controlled_source_topology"].update({
                "status": (
                    "CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_CONTRACT_REQUIRED"
                ),
                "CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_PLAN": {
                    "shared_target_capacity": {
                        "availability_first_feasible": True,
                        "availability_first_target_set": ["awg0"],
                    },
                },
                "CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_RECOMMENDATION": {
                    "status": (
                        "SHARED_TARGET_AVAILABILITY_FIRST_"
                        "ACTION_CLASS_AUTHORITY_REQUIRED"
                    ),
                },
            })
            availability_boundary = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(
                availability_boundary["final_verdict"], "PASS",
                availability_boundary,
            )
            self.assertEqual(
                availability_boundary["next_action"],
                "ENGINEERING_AUTHORITY_EXACT_DEGRADED_SHARED_TARGET_"
                "ACTION_CLASS_CONTRACT_REQUIRED",
            )
            availability_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                availability_live["CURRENT_STOP_CONDITION"].strip("`"),
                "ENGINEERING_AUTHORITY",
            )
            self.assertIn(
                "AVAILABILITY_FIRST_AUTHORITY",
                availability_live["CURRENT_STATE_GENERATION"],
            )
            runtime_status.pop("controlled_source_topology")
            runtime_status[
                "controlled_certification_substrate_authority"
            ]["source_precondition_status"] = "PASS_READY_FOR_APPROVED_SETUP"
            runtime_status["controlled_certification_campaign_status"] = {
                "schema_version": (
                    "v7.controlled-certification-campaign-stage-status.v1"
                ),
                "status": "PASS",
                "ok": True,
                "request_id": "cpsauth_r1_exact",
                "request_hash": "e" * 64,
                "stages": [5, 10, 25, 48],
                "completed_stages": [],
                "controlled_production_proven_max": 0,
                "next_stage": 5,
                "completed": False,
                "receipt_ids": [],
                "blockers": [],
            }
            m9 = self.sync.reconcile_active_standing_delegated_policy_to_cps(
                runtime_status, root=root,
            )
            self.assertEqual(m9["final_verdict"], "PASS", m9)
            self.assertEqual(
                m9["next_action"],
                "CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED",
            )
            m9_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                m9_live["CURRENT_EXECUTION_FRONTIER"].strip("`"),
                "CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED",
            )
            self.assertEqual(
                m9_live["NEXT_MISSION_ID"].strip("`"),
                "T48-M9",
            )
            runtime_status[
                "controlled_certification_substrate_authority"
            ].update({
                "controlled_target_id": "execution-target-a",
                "controlled_target_currently_ready": False,
            })
            runtime_status["controlled_campaign_target_selection"] = {
                "schema_version": (
                    "v7.controlled-campaign-target-selection-diagnostic.v1"
                ),
                "status": "EXACT_TARGET_REBIND_AUTHORITY_REQUIRED",
                "ok": True,
                "inventory_fingerprint": "target-inventory-fingerprint",
                "selection": {
                    "pinned_target_full_live_admission": False,
                    "selected_target_id": "execution-target-b",
                },
            }
            rebind = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status, root=root,
                )
            )
            self.assertEqual(rebind["final_verdict"], "PASS", rebind)
            self.assertEqual(
                rebind["next_action"],
                "ENGINEERING_AUTHORITY_REBIND_CONTROLLED_CAMPAIGN_TARGET_REQUIRED",
            )
            rebind_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                rebind_live["CURRENT_STOP_CONDITION"].strip("`"),
                "ENGINEERING_AUTHORITY",
            )
            self.assertEqual(
                rebind_live["CONTROLLED_TARGET_SELECTION_STATUS"].strip("`"),
                "EXACT_TARGET_REBIND_AUTHORITY_REQUIRED",
            )
            self.assertEqual(
                rebind_live[
                    "CONTROLLED_TARGET_INVENTORY_FINGERPRINT"
                ].strip("`"),
                "target-inventory-fingerprint",
            )
            pending_hash = "a" * 64
            runtime_status["pending_tier_authority_request"] = {
                "status": "PENDING",
                "pending_count": 1,
                "request_id": f"sdpauth_r1_{pending_hash[:24]}",
                "request_hash": pending_hash,
                "created_at": "2026-07-29T00:00:00+00:00",
                "expires_at": "2099-01-01T00:00:00+00:00",
                "active_program": (
                    "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
                ),
                "requested_max_users": 48,
                "max_concurrent_transactions": 1,
                "action_class": (
                    "bounded autonomous controlled certification topology,"
                    "channel hard-fail failover"
                ),
                "policy_profile": (
                    "SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_"
                    "TOPOLOGY_V1"
                ),
                "policy_scope_hash": "b" * 64,
                "decision_set": [
                    "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                    "DECLINE",
                ],
            }
            combined_boundary = (
                self.sync.reconcile_active_standing_delegated_policy_to_cps(
                    runtime_status,
                    root=root,
                )
            )
            self.assertEqual(
                combined_boundary["final_verdict"],
                "PASS",
                combined_boundary,
            )
            self.assertEqual(
                combined_boundary["next_action"],
                "ENGINEERING_AUTHORITY_STANDING_DELEGATED_CONTROLLED_"
                "TOPOLOGY_POLICY_DECISION_REQUIRED",
                combined_boundary,
            )
            combined_live = self.sync._markdown_field_table(
                self.sync._markdown_section(
                    cps_path.read_text(encoding="utf-8"),
                    "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry",
                )
            )
            self.assertEqual(
                combined_live["CURRENT_AUTHORITY_REQUEST_ID"].strip("`"),
                f"sdpauth_r1_{pending_hash[:24]}",
            )
            self.assertEqual(
                combined_live["CURRENT_STOP_CONDITION"].strip("`"),
                "ENGINEERING_AUTHORITY",
            )
            self.assertEqual(
                combined_live["EXTERNAL_INPUT_TYPE"].strip("`"),
                "EXACT_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_"
                "POLICY_DECISION",
            )

    def test_obligation_reuses_live_incident_scope_not_stale_passive_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_live_scope"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            zero_incident_id = "sfinc_zero_scope"
            zero_incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": zero_incident_id,
            })[:24]
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n"
                "ip=10.0.0.4 current=vless enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({"incidents": {
                incident_key: {
                    "incident_key": incident_key, "incident_id": incident_id,
                    "source_incident_id": incident_id, "source_channel": "vless", "channel": "vless",
                    "incident_state": "OPEN", "channel_incident_state": "OPEN",
                    "next_required_consumer": "tools/v7-users-autoswitch.reconcile_service_failure_execution_outcomes",
                    "reentry_condition": "reconcile exact source-scope fingerprint with current route truth before any further action",
                    "scope_accounting": {
                        "status": "ACCOUNTED", "affected_scope_count": 3,
                        "affected_scope_fingerprint": "live-scope-fingerprint",
                    },
                    "current_source_scope": {
                        "status": "ACCOUNTED", "affected_scope_count": 3,
                        "affected_scope_fingerprint": "live-scope-fingerprint",
                    },
                },
                zero_incident_key: {
                    "incident_key": zero_incident_key, "incident_id": zero_incident_id,
                    "source_incident_id": zero_incident_id, "source_channel": "other", "channel": "other",
                    "incident_state": "OPEN", "channel_incident_state": "OPEN",
                    "scope_accounting": {
                        "status": "ACCOUNTED", "affected_scope_count": 0,
                        "affected_scope_fingerprint": "zero-scope-fingerprint",
                    },
                },
            }}), encoding="utf-8")
            closure = {
                "object_type": "passive_production_event", "object_id": incident_id,
                "source_incident_id": incident_id, "incident_key": incident_key,
                "situation_id": "situation_live_scope", "decision_trace_id": "decision_live_scope",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION", "channel": "vless",
                # An old compact passive closure legitimately has no raw list.
                "affected_users": [], "observed_at": "2026-07-27T00:00:00+00:00",
            }
            zero_closure = {
                "object_type": "passive_production_event", "object_id": zero_incident_id,
                "source_incident_id": zero_incident_id, "incident_key": zero_incident_key,
                "situation_id": "situation_zero_scope", "decision_trace_id": "decision_zero_scope",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION", "channel": "other",
                "affected_users": [], "observed_at": "2026-07-27T00:01:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(
                json.dumps(closure) + "\n" + json.dumps(zero_closure) + "\n", encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            result = planner.materialize_service_failure_automation_advisory({"decisions": [{
                "user_ip": "10.0.0.2", "current_egress": "vless", "recommended_egress": "awg0",
            }]})
        self.assertTrue(result["active"])
        self.assertEqual(result["obligation"]["source_incident_id"], incident_id)
        self.assertEqual(result["obligation"]["affected_users_count"], 3)
        self.assertEqual(result["obligation"]["current_source_scope"]["affected_scope_fingerprint"], "live-scope-fingerprint")
        self.assertFalse(result["obligation"]["current_source_scope"]["raw_user_list_stored"])

    def test_active_incident_scope_bridge_accepts_only_balanced_compact_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("l3-runtime-state.json").write_text(json.dumps({"incidents": {
                "passive_scope": {
                    "incident_id": "sfinc_scope_bridge", "incident_state": "OPEN",
                    "channel_incident_state": "OPEN", "next_required_consumer": "existing.consumer",
                    "reentry_condition": "fresh Matrix observation",
                    "scope_accounting": {
                        "status": "ACCOUNTED", "affected_scope_count": 3,
                        "protected_scope_count": 1, "unresolved_scope_count": 2,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                        "affected_scope_fingerprint": "scope-fingerprint",
                        "raw_user_list_stored": False,
                    },
                },
            }}), encoding="utf-8")
            scope = self.sync.service_failure_active_incident_scope_projection(
                "sfinc_scope_bridge", state_dir=state_dir,
            )
            self.assertEqual(scope["unresolved_scope_count"], 2)
            data = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            data["incidents"]["passive_scope"]["scope_accounting"]["unresolved_scope_count"] = 1
            (state_dir / "l3-runtime-state.json").write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(
                self.sync.service_failure_active_incident_scope_projection("sfinc_scope_bridge", state_dir=state_dir),
                {},
            )

    def test_packet_bound_execution_feedback_reconciles_only_its_existing_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_bound"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key, "incident_id": incident_id,
                        "incident_state": "OPEN", "channel_incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "next_required_consumer": "tools/v7_sync_lib.consume_service_failure_automation_frontier",
                        "reentry_condition": "fresh event", "causal_lineage": {},
                    },
                },
            }), encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb_bound", "source_channel": "vless", "target_channel": "awg3",
                "user": "10.0.0.2", "packet_id": "pkt_bound", "closure_reference": "operation_bound",
                "terminal_outcome_classification": "SUCCESS",
                "verification_result": {"success": True}, "learning_record": {"learning_record_id": "learn_bound"},
                "service_failure_causal_binding": {
                    "source_incident_id": incident_id, "source_event_id": "sfrev_bound",
                    "source_event_ids": ["sfrev_bound"], "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                },
            }
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            result = planner.reconcile_service_failure_execution_outcomes()
            repeated = planner.reconcile_service_failure_execution_outcomes()
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = state["incidents"][incident_key]
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["changed_records"], 1)
        self.assertEqual(repeated["changed_records"], 0)
        self.assertEqual(record["incident_state"], "PARTIALLY_PROTECTED")
        self.assertEqual(record["last_execution_feedback_id"], "execfb_bound")
        self.assertEqual(record["causal_lineage"]["source_event_ids"], ["sfrev_bound"])

    def test_execution_reconciliation_keeps_compact_incident_scope_balance(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_scope_bound"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg3 enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({"incidents": {
                incident_key: {
                    "incident_key": incident_key, "incident_id": incident_id,
                    "source_channel": "vless",
                    "incident_state": "OPEN", "channel_incident_state": "OPEN",
                    "scope_accounting": {
                        "baseline_event_id": "sfrev_scope", "baseline_observed_at": "2026-07-27T03:00:00+00:00",
                        "affected_scope_count": 2, "affected_scope_fingerprint": "scopehash",
                    },
                },
            }}), encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_scope",
                "source_channel": "vless", "target_channel": "awg3", "user": "10.0.0.2", "packet_id": "pkt_scope",
                "terminal_outcome_classification": "SUCCESS", "outcome_observed_at": "2026-07-27T03:01:00+00:00",
                "verification_result": {"success": True},
                "service_failure_causal_binding": {
                    "source_incident_id": incident_id, "source_event_id": "sfrev_scope",
                    "source_event_ids": ["sfrev_scope"], "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                    "source_scope": {
                        "source_channel": "vless", "affected_scope_count": 2,
                        "affected_scope_fingerprint": "scopehash",
                    },
                },
            }
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            first = planner.reconcile_service_failure_execution_outcomes()
            repeated = planner.reconcile_service_failure_execution_outcomes()
            record = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))["incidents"][incident_key]
        self.assertEqual(first["changed_records"], 1)
        self.assertEqual(repeated["changed_records"], 0)
        self.assertEqual(record["scope_accounting"]["status"], "ACCOUNTED")
        self.assertEqual(record["protected_scope_count"], 1)
        self.assertEqual(record["unresolved_scope_count"], 1)

    def test_scope_reconciliation_rejects_historical_feedback_without_matching_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_scope_generation"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg3 enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({"incidents": {
                incident_key: {
                    "incident_key": incident_key, "incident_id": incident_id, "source_channel": "vless",
                    "scope_accounting": {
                        "baseline_event_id": "sfrev_new", "affected_scope_count": 2,
                        "affected_scope_fingerprint": "newscope",
                    },
                },
            }}), encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_old",
                "source_channel": "vless", "target_channel": "awg3", "user": "10.0.0.2",
                "terminal_outcome_classification": "SUCCESS", "verification_result": {"success": True},
                "service_failure_causal_binding": {
                    "source_incident_id": incident_id, "source_event_id": "sfrev_old",
                    "event_type": "SERVICE_FAILURE_REVALIDATED", "source_channel": "vless",
                    "source_scope": {"source_channel": "vless", "affected_scope_count": 2,
                                     "affected_scope_fingerprint": "oldscope"},
                },
            }
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            planner.reconcile_service_failure_execution_outcomes()
            record = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))["incidents"][incident_key]
        self.assertEqual(record["scope_accounting"]["status"], "INCIDENT_SCOPE_ACCOUNTING_BROKEN")
        self.assertEqual(record["protected_scope_count"], 0)
        self.assertEqual(record["scope_accounting"]["nonmember_or_stale_feedback_pointers"], ["execfb_old"])
        self.assertEqual(record["current_source_scope"]["protected_scope_count"], 0)
        self.assertEqual(
            record["incident_cumulative_scope"]["classification_counts"]["HISTORICAL_PROTECTED_PRE_BASELINE"],
            1,
        )
        self.assertEqual(record["incident_cumulative_scope"]["current_source_scope_fingerprint"], "newscope")
        self.assertEqual(record["incident_cumulative_scope"]["lineage_pointers"], ["execfb_old"])

    def test_scope_reconciliation_joins_distinct_service_incidents_with_exact_same_cohort(self):
        """One channel-scope cohort may legitimately have several service incident IDs."""
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_google_auth"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg3 enabled=1\n"
                "ip=10.0.0.3 current=vless enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({"incidents": {
                incident_key: {
                    "incident_key": incident_key, "incident_id": incident_id, "source_channel": "vless",
                    "incident_state": "OPEN", "channel_incident_state": "OPEN",
                    "next_required_consumer": "tools/v7-users-autoswitch.reconcile_service_failure_execution_outcomes",
                    "reentry_condition": "reconcile exact source-scope fingerprint with current route truth before any further action",
                    "scope_accounting": {
                        "baseline_event_id": "sfe_google_auth", "affected_scope_count": 2,
                        "affected_scope_fingerprint": "same-channel-cohort",
                    },
                },
            }}), encoding="utf-8")
            outcome = {
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_spotify",
                "source_channel": "vless", "target_channel": "awg3", "user": "10.0.0.2",
                "terminal_outcome_classification": "SUCCESS", "verification_result": {"success": True},
                "service_failure_causal_binding": {
                    "source_incident_id": "sfinc_spotify", "source_event_id": "sfe_spotify",
                    "event_type": "SERVICE_FAILURE_OBSERVED", "source_channel": "vless",
                    "source_scope": {"source_channel": "vless", "affected_scope_count": 2,
                                     "affected_scope_fingerprint": "same-channel-cohort"},
                },
            }
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            planner.reconcile_service_failure_execution_outcomes()
            record = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))["incidents"][incident_key]
        self.assertEqual(record["scope_accounting"]["status"], "ACCOUNTED")
        self.assertEqual(record["protected_scope_count"], 1)
        self.assertEqual(record["unresolved_scope_count"], 1)
        self.assertEqual(record["scope_accounting"]["protected_scope_lineage_pointers"], ["execfb_spotify"])
        self.assertEqual(
            record["next_required_consumer"],
            "tools/v7-users-autoswitch.reconcile_service_failure_shadow_outcomes",
        )
        self.assertEqual(
            record["incident_cumulative_scope"]["classification_counts"]["SAME_SOURCE_SCOPE_COHORT_PROTECTED"],
            1,
        )

    def test_closed_incident_scope_is_frozen_from_later_live_route_generations(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n",
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            existing = {
                "incident_id": "sfinc_closed_scope",
                "source_channel": "vless",
                "incident_state": "INTENT_CLOSED",
                "intent_closure_evidence_pointer": "closure_recovery",
                "scope_accounting": {
                    "baseline_event_id": "sfrev_closed",
                    "baseline_observed_at": "2026-07-27T03:00:00+00:00",
                    "affected_scope_count": 0,
                    "affected_scope_fingerprint": "closed_scope",
                    "unresolved_scope_count": 1,
                    "status": "INCIDENT_SCOPE_ACCOUNTING_BROKEN",
                },
            }
            scope = planner._reconcile_incident_scope_accounting(
                existing=existing,
                execution_rows=[],
            )
        self.assertEqual(scope["status"], "ACCOUNTED")
        self.assertEqual(scope["affected_scope_count"], 0)
        self.assertEqual(scope["protected_scope_count"], 0)
        self.assertEqual(scope["unresolved_scope_count"], 0)
        self.assertEqual(scope["explicitly_excluded_or_recovered_scope_count"], 0)
        self.assertEqual(scope["accounted_scope_count"], 0)
        self.assertTrue(scope["terminal_scope_frozen"])
        self.assertEqual(
            scope["scope_membership_law"],
            "INTENT_CLOSED_TERMINAL_SCOPE_FROZEN",
        )

    def test_closed_partial_scope_assigns_terminal_residual_to_recovered_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n",
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            existing = {
                "incident_id": "sfinc_closed_partial_scope",
                "source_channel": "vless",
                "incident_state": "INTENT_CLOSED",
                "intent_closure_evidence_pointer": "closure_partial_recovery",
                "scope_accounting": {
                    "baseline_event_id": "sfrev_closed_partial",
                    "baseline_observed_at": "2026-07-27T03:00:00+00:00",
                    "affected_scope_count": 5,
                    "affected_scope_fingerprint": "closed_partial_scope",
                    "protected_scope_count": 1,
                    "protected_scope_lineage_pointers": ["execfb_protected"],
                },
            }
            scope = planner._reconcile_incident_scope_accounting(
                existing=existing,
                execution_rows=[],
            )
        self.assertEqual(scope["status"], "ACCOUNTED")
        self.assertEqual(scope["affected_scope_count"], 5)
        self.assertEqual(scope["protected_scope_count"], 1)
        self.assertEqual(scope["unresolved_scope_count"], 0)
        self.assertEqual(scope["explicitly_excluded_or_recovered_scope_count"], 4)
        self.assertEqual(scope["accounted_scope_count"], 5)
        self.assertEqual(
            scope["explicitly_excluded_or_recovered_lineage_pointers"],
            ["closure_partial_recovery"],
        )

    def test_open_unchanged_scope_reuses_baseline_fingerprint_for_ct_binding(self):
        """An unchanged cohort must not gain a second fingerprint namespace.

        The Matrix producer, L3 accounting and CT-M0F selector all bind the
        initial unresolved cohort to the existing source-scope fingerprint.
        A packet-free reconciliation must therefore preserve it exactly.
        """
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            users = ["10.0.0.2", "10.0.0.3"]
            (state_dir / "users.registry").write_text(
                "".join(f"ip={user} current=vless enabled=1\n" for user in users),
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            baseline_fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": users,
            })
            scope = planner._reconcile_incident_scope_accounting(
                existing={
                    "incident_id": "sfinc_same_cohort",
                    "source_channel": "vless",
                    "scope_accounting": {
                        "status": "ACCOUNTED",
                        "affected_scope_count": 2,
                        "affected_scope_fingerprint": baseline_fingerprint,
                    },
                },
                execution_rows=[],
            )
        self.assertEqual(scope["status"], "ACCOUNTED")
        self.assertEqual(scope["unresolved_scope_count"], 2)
        self.assertEqual(scope["unresolved_scope_fingerprint"], baseline_fingerprint)

    def test_cumulative_scope_retains_missing_binding_without_claiming_current_membership(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            (state_dir / "users.registry").write_text("ip=10.0.0.2 current=awg3 enabled=1\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            existing = {
                "incident_id": "sfinc_current", "source_channel": "vless",
                "scope_accounting": {"affected_scope_count": 1, "affected_scope_fingerprint": "freshscope"},
            }
            rows = [{
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_unbound",
                "packet_id": "pkt_unbound", "source_channel": "vless", "target_channel": "awg3",
                "user": "10.0.0.2", "terminal_outcome_classification": "SUCCESS",
                "verification_result": {"success": True},
            }]
            cumulative = planner._reconcile_incident_cumulative_scope(existing=existing, execution_rows=rows)
        self.assertEqual(cumulative["classification_counts"]["HISTORICAL_MOVED_INCIDENT_BINDING_MISSING"], 1)
        self.assertEqual(cumulative["current_source_scope_fingerprint"], "freshscope")
        self.assertEqual(cumulative["packet_bound_success_count"], 1)
        self.assertFalse(cumulative["raw_user_list_stored"])

    def test_exact_packet_bound_execution_feedback_updates_source_cps_without_new_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            feedback = {
                "schema_version": "v7.execution-outcome-record.v1",
                "feedback_id": "execfb_source_bound", "packet_id": "pkt_source_bound",
                "user": "10.0.0.2", "source_channel": "vless", "target_channel": "awg3",
                "terminal_outcome_classification": "SUCCESS",
                "verification_result": {"success": True},
                "execution_outcome": {"runtime_mutation_performed": True, "users_moved": 1},
                "service_failure_causal_binding": {
                    "source_incident_id": "sfinc_source_bound", "source_event_id": "sfrev_source_bound",
                    "source_event_ids": ["sfrev_source_bound"], "event_type": "SERVICE_FAILURE_REVALIDATED",
                    "source_channel": "vless",
                },
            }
            result = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
            repeated = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8"),
                "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry",
            ))
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertTrue(result["atomic_update"]["ok"])
        self.assertEqual(repeated["status"], "EXECUTION_FEEDBACK_ALREADY_CONSUMED")
        self.assertEqual(self.sync._plain_live_value(live, "LAST_SERVICE_FAILURE_EXECUTION_FEEDBACK_ID"), "execfb_source_bound")
        self.assertIn("PARTIALLY_PROTECTED", self.sync._plain_live_value(live, "CURRENT_VLESS_SERVICE_INCIDENT"))

    def test_accounted_scope_projects_active_incident_drain_into_source_cps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            feedback = {
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_scope_source", "packet_id": "pkt_scope_source",
                "user": "10.0.0.2", "source_channel": "vless", "target_channel": "awg3",
                "terminal_outcome_classification": "SUCCESS", "verification_result": {"success": True},
                "execution_outcome": {"runtime_mutation_performed": True, "users_moved": 1},
                "service_failure_causal_binding": {
                    "source_incident_id": "sfinc_scope_source", "source_event_id": "sfrev_scope_source",
                    "source_event_ids": ["sfrev_scope_source"], "event_type": "SERVICE_FAILURE_REVALIDATED", "source_channel": "vless",
                    "source_scope": {
                        "source_channel": "vless", "affected_scope_count": 5,
                        "affected_scope_fingerprint": "scope-fingerprint",
                    },
                },
                "incident_scope_accounting": {
                    "status": "ACCOUNTED", "affected_scope_count": 5, "protected_scope_count": 1,
                    "unresolved_scope_count": 4, "explicitly_excluded_or_recovered_scope_count": 0,
                    "affected_scope_fingerprint": "scope-fingerprint", "raw_user_list_stored": False,
                },
            }
            result = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8"),
                "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry",
            ))
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertEqual(self.sync._plain_live_value(live, "CURRENT_VLESS_UNRESOLVED_SCOPE"), "4")
        self.assertEqual(self.sync._plain_live_value(live, "CURRENT_SAFE_NEXT_ACTION").split()[0], "CONTINUE")

    def test_already_consumed_feedback_does_not_compare_against_newer_live_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            feedback = {
                "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_idempotent_scope",
                "packet_id": "pkt_idempotent_scope", "user": "10.0.0.2", "source_channel": "vless", "target_channel": "awg3",
                "terminal_outcome_classification": "SUCCESS", "verification_result": {"success": True},
                "execution_outcome": {"runtime_mutation_performed": True, "users_moved": 1},
                "service_failure_causal_binding": {
                    "source_incident_id": "sfinc_idempotent_scope", "source_event_id": "sfrev_idempotent_scope",
                    "event_type": "SERVICE_FAILURE_REVALIDATED", "source_channel": "vless",
                    "source_scope": {"source_channel": "vless", "affected_scope_count": 5, "affected_scope_fingerprint": "scope-before"},
                },
                "incident_scope_accounting": {
                    "status": "ACCOUNTED", "affected_scope_count": 5, "protected_scope_count": 1,
                    "unresolved_scope_count": 4, "explicitly_excluded_or_recovered_scope_count": 0,
                    "affected_scope_fingerprint": "scope-before", "raw_user_list_stored": False,
                },
            }
            first = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
            feedback["incident_scope_accounting"].update({
                "affected_scope_count": 4, "protected_scope_count": 1, "unresolved_scope_count": 3,
                "affected_scope_fingerprint": "scope-after",
            })
            repeated = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback, root=root)
        self.assertEqual(first["final_verdict"], "PASS", first)
        self.assertEqual(repeated["final_verdict"], "PASS", repeated)
        self.assertEqual(repeated["status"], "EXECUTION_FEEDBACK_ALREADY_CONSUMED")

    def test_source_cps_reconciliation_rejects_scope_from_another_generation(self):
        feedback = {
            "schema_version": "v7.execution-outcome-record.v1", "feedback_id": "execfb_scope_mismatch",
            "packet_id": "pkt_scope_mismatch", "source_channel": "vless", "target_channel": "awg3",
            "terminal_outcome_classification": "SUCCESS", "verification_result": {"success": True},
            "execution_outcome": {"runtime_mutation_performed": True, "users_moved": 1},
            "service_failure_causal_binding": {
                "source_incident_id": "sfinc_scope_mismatch", "source_event_id": "sfrev_scope_mismatch",
                "event_type": "SERVICE_FAILURE_REVALIDATED", "source_channel": "vless",
                "source_scope": {"source_channel": "vless", "affected_scope_count": 4, "affected_scope_fingerprint": "binding-scope"},
            },
            "incident_scope_accounting": {
                "status": "ACCOUNTED", "affected_scope_count": 5, "protected_scope_count": 1,
                "unresolved_scope_count": 4, "explicitly_excluded_or_recovered_scope_count": 0,
                "affected_scope_fingerprint": "l3-scope", "raw_user_list_stored": False,
            },
        }
        result = self.sync.reconcile_service_failure_execution_feedback_to_cps(feedback)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("execution_feedback_scope_binding_mismatch", result["errors"])

    def test_advisory_skips_expired_terminal_and_selects_open_revalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            expiry = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_old",
                "source_incident_id": "sfinc_old",
                "situation_id": "situation_old",
                "decision_trace_id": "decision_old",
                "terminal_outcome_classification": "EPISODE_EXPIRED_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "vless",
                "observed_at": "2026-07-27T03:10:00+00:00",
            }
            revalidated = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_current",
                "source_incident_id": "sfinc_current",
                "situation_id": "situation_current",
                "decision_trace_id": "decision_current",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "vless",
                "observed_at": "2026-07-27T03:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in (revalidated, expiry)),
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            result = planner.materialize_service_failure_automation_advisory({
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                }],
            })
            self.assertTrue(result["active"])
            self.assertEqual(result["obligation"]["source_incident_id"], "sfinc_current")

    def test_passive_terminal_projects_compact_dual_lifecycle_and_omp_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_causal_1",
                "source_incident_id": "sfinc_causal_1",
                "source_event_ids": ["evt_causal_1"],
                "source_hashes": {"service_matrix": "a" * 64},
                "situation_id": "situation_causal_1",
                "decision_trace_id": "decision_causal_1",
                "learning_record_id": "learn_causal_1",
                "closure_state": "CAPTURED_STOP_SAFE",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "NATURAL_PRODUCTION_CANDIDATE",
                "channel": "vless",
                "services": ["service-a"],
                "failure_families": ["connection_reset"],
                "affected_users": ["10.0.0.2", "10.0.0.3"],
                "observed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}

            first = planner.reconcile_passive_causal_projections()
            self.assertEqual(first["final_verdict"], "PASS")
            self.assertEqual(first["changed_records"], 1)
            self.assertEqual(first["invalid_open_incidents"], 0)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertEqual(record["incident_state"], "OPEN")
            self.assertEqual(record["attempt_terminal"], "STOP_SAFE_NO_ACTION")
            self.assertEqual(record["intent_scope_type"], "COHORT")
            self.assertEqual(record["user_protection_intent"]["affected_users_count"], 2)
            self.assertFalse(record["user_protection_intent"]["raw_user_list_stored"])
            self.assertEqual(
                record["next_required_consumer"],
                "tools/v7-users-autoswitch.materialize_service_failure_automation_advisory",
            )
            self.assertTrue(record["reentry_condition"])
            self.assertFalse(record["runtime_mutation_performed"])
            self.assertEqual(record["users_moved"], 0)
            self.assertEqual(planner.reconcile_passive_causal_projections()["changed_records"], 0)

            advisory = planner.materialize_service_failure_automation_advisory({
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                }],
            })
            self.assertTrue(advisory["active"])
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertTrue(record["obligation_id"])
            self.assertEqual(
                record["next_required_consumer"],
                "tools/v7_sync_lib.consume_service_failure_automation_frontier",
            )
            self.assertIn("closure-records.lock", record["reentry_condition"])

    def test_closed_passive_recovery_closes_intent_without_erasing_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_recovered",
                "source_incident_id": "sfinc_recovered",
                "source_event_ids": ["evt_recovered"],
                "situation_id": "situation_recovered",
                "decision_trace_id": "decision_recovered",
                "learning_record_id": "learn_recovered",
                "terminal_outcome_classification": "RECOVERY_OBSERVED_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "vless",
                "affected_users": ["10.0.0.2"],
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}

            result = planner.reconcile_passive_causal_projections()
            self.assertEqual(result["final_verdict"], "PASS")
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertEqual(record["incident_state"], "INTENT_CLOSED")
            self.assertEqual(record["status"], "CLOSED")
            self.assertEqual(record["intent_closure_reason"], "RECOVERY_OBSERVED")
            self.assertEqual(record["causal_lineage"]["decision_trace_id"], "decision_recovered")
            self.assertEqual(record["users_moved"], 0)
            self.assertEqual(planner.reconcile_passive_causal_projections()["changed_records"], 0)

    def test_compact_projection_uses_only_latest_historical_terminal_per_incident(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            old = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_history",
                "source_incident_id": "sfinc_history",
                "source_event_ids": ["evt_old"],
                "situation_id": "situation_old",
                "decision_trace_id": "decision_old",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "observed_at": "2026-07-26T00:00:00+00:00",
            }
            latest = {
                **old,
                "object_id": "sfinc_history_recovered",
                "source_event_ids": ["evt_new"],
                "situation_id": "situation_new",
                "decision_trace_id": "decision_new",
                "terminal_outcome_classification": "RECOVERY_OBSERVED_NO_ACTION",
                "observed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(
                json.dumps(old) + "\n" + json.dumps(latest) + "\n", encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}

            first = planner.reconcile_passive_causal_projections()
            self.assertEqual(first["projected_records"], 1)
            self.assertEqual(first["changed_records"], 1)
            self.assertEqual(planner.reconcile_passive_causal_projections()["changed_records"], 0)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = next(iter(state["incidents"].values()))
            self.assertEqual(record["incident_state"], "INTENT_CLOSED")
            self.assertEqual(record["decision_trace_id"], "decision_new")

    def test_active_standing_policy_replaces_stale_one_use_authority_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            closure = {
                "object_type": "passive_production_event",
                "object_id": "sfinc_standing",
                "source_incident_id": "sfinc_standing",
                "situation_id": "situation_standing",
                "decision_trace_id": "decision_standing",
                "closure_state": "CAPTURED_STOP_SAFE",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "evidence_class": "NATURAL_PRODUCTION_CANDIDATE",
                "channel": "vless",
                "affected_users": ["10.0.0.2"],
                "observed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(closure) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            planner._standing_delegated_policy_status = lambda: {
                "valid": True,
                "blockers": [],
                "contract_id": "sdpc_test",
                "expires_at": "2026-08-27T00:00:00+00:00",
            }
            result = planner.materialize_service_failure_automation_advisory({
                "decisions": [{
                    "user_ip": "10.0.0.2",
                    "current_egress": "vless",
                    "recommended_egress": "awg0",
                }],
            })
            obligation = result["obligation"]
            self.assertEqual(obligation["stop_safe_classification"], "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED")
            self.assertEqual(obligation["product_evolution_frontier"], "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION")
            self.assertEqual(
                obligation["action_class_execution_boundary"]["status"],
                "STANDING_DELEGATED_POLICY_ACTIVE_FRESH_EVENT_REVALIDATION_REQUIRED",
            )
            self.assertFalse(obligation["runtime_mutation_performed"])
            self.assertEqual(obligation["users_moved"], 0)

    def test_active_standing_policy_reuses_matching_controlled_target_when_ordinary_planner_has_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_id = "sfinc_controlled_target"
            incident_key = "passive_" + self.autoswitch.sha256_json({
                "owner": "tools/v7-users-autoswitch.passive-causal-projection",
                "source_incident_id": incident_id,
            })[:24]
            scope = {
                "status": "ACCOUNTED", "affected_scope_count": 1,
                "protected_scope_count": 0, "unresolved_scope_count": 1,
                "explicitly_excluded_or_recovered_scope_count": 0,
                "affected_scope_fingerprint": "controlled-scope",
                "raw_user_list_stored": False,
            }
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {incident_key: {
                    "incident_key": incident_key, "incident_id": incident_id,
                    "source_incident_id": incident_id, "source_channel": "source",
                    "channel": "source", "incident_state": "OPEN",
                    "channel_incident_state": "OPEN",
                    "current_source_scope": scope, "scope_accounting": scope,
                }},
            }), encoding="utf-8")
            closure = {
                "object_type": "passive_production_event", "object_id": incident_id,
                "source_incident_id": incident_id, "incident_key": incident_key,
                "situation_id": "situation_controlled_target",
                "decision_trace_id": "decision_controlled_target",
                "terminal_outcome_classification": "STOP_SAFE_NO_ACTION",
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "source", "affected_users": [],
            }
            obligation_id = self.autoswitch.sha256_json({
                "source_incident_id": incident_id,
                "situation_id": "situation_controlled_target",
                "decision_trace_id": "decision_controlled_target",
                "terminal": "STOP_SAFE_NO_ACTION",
                "provenance": "EXTERNAL_UNATTRIBUTED",
            })[:24]
            old_obligation = {
                "object_type": "service_failure_automation_obligation",
                "object_id": "sfaob_" + obligation_id,
                "automation_obligation_id": "sfaob_" + obligation_id,
                "created_at": "2026-08-01T00:00:00+00:00",
                "source_incident_id": incident_id,
                "incident_key": incident_key,
                "stop_safe_classification": "STOP_SAFE_NO_SAFE_TARGET",
                "current_source_scope": scope,
            }
            (state_dir / "closure-records.jsonl").write_text(
                "\n".join(json.dumps(row) for row in (closure, old_obligation)) + "\n",
                encoding="utf-8",
            )
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.l3_runtime_state = {}
            planner.args = SimpleNamespace()
            planner._standing_delegated_policy_status = lambda: {
                "valid": True, "contract_id": "sdpc_test",
                "expires_at": "2026-08-27T00:00:00+00:00",
            }
            with mock.patch.object(
                self.autoswitch,
                "ct_m0f_standing_source_selection_only",
                return_value={
                    # The first obligation is being materialized.  The
                    # selector cannot yet see an OMP-consumed binding, but it
                    # may prove the exact target and current live source
                    # scope.  The advisory must create that durable
                    # prospective binding without creating a Packet or apply.
                    "ok": False,
                    "selection_mode": "EXECUTE_CONTROLLED_FAILURE_CUTOVER",
                    "selected_source_id": "source",
                    "selected_user": "10.7.0.18",
                    "selected_target_id": "execution-target",
                    "sample_binding_fingerprint": "a" * 64,
                    "selected_target_admission": {
                        "controlled_contract_admitted": True,
                        "admission_law": "EXACT_EXISTING_CONTROLLED_EXECUTION_TARGET_ONE_USER",
                    },
                    "active_service_failure_binding": {
                        "status": "NO_CURRENT_ROUTE_MATCHING_ACTIVE_SERVICE_FAILURE_BINDING",
                        "requires_binding": True,
                        "live_source_scope": {
                            "source_channel": "source",
                            "affected_scope_fingerprint": "controlled-scope",
                            "affected_scope_count": 1,
                        },
                    },
                    "blockers": [
                        "ct_m0f_active_service_failure_causal_binding_required",
                    ],
                },
            ):
                result = planner.materialize_service_failure_automation_advisory({
                    "decisions": [],
                })
                unchanged = planner.materialize_service_failure_automation_advisory({
                    "decisions": [],
                })
        obligation = result["obligation"]
        self.assertEqual(
            obligation["stop_safe_classification"],
            "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED",
        )
        selection = obligation["action_class_execution_boundary"][
            "ct_m0f_controlled_selection"
        ]
        self.assertEqual(selection["target"], "execution-target")
        self.assertTrue(selection["read_only"])
        self.assertEqual(
            selection["binding_mode"],
            "PROSPECTIVE_PASSIVE_OBLIGATION_BINDING",
        )
        self.assertFalse(obligation["runtime_mutation_performed"])
        self.assertEqual(
            obligation["reconciliation"]["previous_stop_safe_classification"],
            "STOP_SAFE_NO_SAFE_TARGET",
        )
        self.assertFalse(unchanged["active"])
        self.assertEqual(
            unchanged["reason"], "current_obligation_semantics_already_materialized",
        )

    def test_policy_reconciliation_preserves_active_incident_drain_and_projects_tiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps_path.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path)
            source = cps_path.read_text(encoding="utf-8")
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                source, "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
            ))
            contract_hash = "a" * 64
            runtime_status = {
                "schema_version": "v7.standing-delegated-policy-runtime-status.v1",
                "status": "PASS", "ok": True, "contract_status": "ACTIVE",
                "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                "authority_decision": "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                "audit_provenance_verified": True,
                "contract_id": f"sdpc_{contract_hash[:24]}", "contract_hash": contract_hash,
                "authority_request_id": live["CURRENT_AUTHORITY_REQUEST_ID"].strip("`"),
                "authority_request_hash": "b" * 64,
                "expires_at": "2099-01-01T00:00:00+00:00", "policy_scope_hash": "c" * 64,
                "max_users_per_action": 1, "max_concurrent_transactions": 1,
                "allowed_failure_families": ["channel_hard_fail", "service_specific_failure"],
                "cooldown": {"per_user_seconds": 1800, "per_source_target_pair_seconds": 1800},
                "anti_flap": "PASS",
                "pending_tier_authority_request": {
                    "status": "PENDING",
                    "pending_count": 1,
                    "request_id": "sdpauth_r1_" + ("d" * 24),
                    "request_hash": "d" * 64,
                    "created_at": "2026-07-28T00:00:00+00:00",
                    "expires_at": "2099-01-02T00:00:00+00:00",
                    "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                    "requested_max_users": 4,
                    "max_concurrent_transactions": 1,
                    "action_class": "channel hard-fail failover",
                    "policy_scope_hash": "e" * 64,
                    "decision_set": [
                        "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                        "DECLINE",
                    ],
                },
                "service_failure_causal_integrity": {
                    "schema_version": "v7.service-failure-causal-integrity-status.v1",
                    "final_verdict": "PASS", "invalid_states": [],
                    "open_incident_projections": [{
                        "incident_id": live["CURRENT_VLESS_INCIDENT_ID"].strip("`"),
                        "incident_generation": "generation-runtime-current",
                        "source_channel": "vless",
                        "incident_state": "PARTIALLY_PROTECTED",
                        "affected_scope_count": 29,
                        "protected_scope_count": 2,
                        "unresolved_scope_count": 27,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                        "affected_scope_fingerprint": "affected-runtime-current",
                        "protected_scope_fingerprint": "protected-runtime-current",
                        "unresolved_scope_fingerprint": "unresolved-runtime-current",
                        "explicitly_excluded_or_recovered_scope_fingerprint": "excluded-runtime-current",
                        "last_execution_feedback_id": "execfb_runtime_current",
                        "last_outcome_id": "outcome_runtime_current",
                        "last_learning_id": "learning_runtime_current",
                        "last_packet_id": "packet_runtime_current",
                        "next_required_consumer": "tools/v7-service-matrix-refresh-all",
                        "reentry_condition": "fresh Matrix observation of the same incident",
                    }],
                },
            }
            result = self.sync.reconcile_active_standing_delegated_policy_to_cps(runtime_status, root=root)
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(result["next_action"], "CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN")
            updated = cps_path.read_text(encoding="utf-8")
            updated_live = self.sync._markdown_field_table(self.sync._markdown_section(
                updated, "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
            ))
            self.assertEqual(updated_live["CURRENT_PROGRAM_EXECUTION_FRONTIER"].strip("`"), "CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN")
            self.assertEqual(updated_live["OMP_CONTINUATION_REQUIRED"].strip("`"), "TRUE")
            self.assertEqual(updated_live["TIER_1_REUSE_CLASSIFICATION"].strip("`"), "REUSABLE_CERTIFIED_AND_APPROVED")
            self.assertEqual(
                updated_live["TIER_2_REUSE_CLASSIFICATION"].strip("`"),
                "ENGINEERING_ADAPTER_QUALIFIED_AUTHORITY_REQUIRED",
            )
            self.assertEqual(updated_live["TIER_2_REUSE_MISMATCH_FIELDS"].strip("`"), "Authority_scope_only")
            self.assertEqual(
                updated_live["CURRENT_ACTION_CLASS_CERTIFIED_TIER"].strip("`"),
                "TIER_48_ENGINEERING_QUALIFIED; TIER_1_AUTHORITY_ACTIVE; "
                "TIER_1_SERVICE_FAILURE_PRODUCTION_PROVEN",
            )
            self.assertEqual(updated_live["CURRENT_ACTION_CLASS_RUNTIME_ENABLED_TIER"].strip("`"), "TIER_1_SINGLE_USER_SERIAL")
            self.assertEqual(updated_live["CURRENT_ACTION_CLASS_CAN_REUSE_WITHOUT_CODEX"].strip("`"), "TRUE_MATRIX_RUNTIME_OWNER")
            self.assertEqual(
                updated_live["GENERIC_MOVEMENT_PRIMITIVE_STATUS"].strip("`"),
                "GENERIC_MOVEMENT_PRIMITIVE_EVIDENCE_NORMALIZED_AND_CONSUMED",
            )
            self.assertEqual(updated_live["GENERIC_MOVEMENT_ACTUAL_PROVEN_SCOPES"].strip("`"), "1,2,4,5,10,25,48")
            self.assertEqual(updated_live["GENERIC_MOVEMENT_ASSIGNMENT_MUTATION_PROVEN_MAX"].strip("`"), "48")
            self.assertEqual(updated_live["GENERIC_MOVEMENT_ROLLBACK_APPLIED_PROVEN_MAX"].strip("`"), "4")
            self.assertEqual(updated_live["GENERIC_MOVEMENT_CERTIFIED_NO_ROLLBACK_PROVEN_MAX"].strip("`"), "48")
            self.assertEqual(updated_live["GENERIC_MOVEMENT_REPLAY_DUPLICATE_SUPPRESSION_PROVEN_MAX"].strip("`"), "4")
            self.assertEqual(updated_live["GENERIC_MOVEMENT_PACKET_IDENTITY_PROVEN_MAX"].strip("`"), "25")
            self.assertEqual(updated_live["GENERIC_MOVEMENT_PARTIAL_APPLY_FAILURE_RECOVERY"].strip("`"), "NOT_PROVEN")
            self.assertEqual(updated_live["GENERIC_MOVEMENT_RESTART_RECOVERY"].strip("`"), "NOT_PROVEN_FOR_COHORT")
            self.assertEqual(
                updated_live["GENERIC_MOVEMENT_ENGINEERING_CERTIFIED_MAX"].strip("`"),
                "48",
            )
            self.assertEqual(
                updated_live["GENERIC_MOVEMENT_ENGINEERING_PACKET_IDENTITY_MAX"].strip("`"),
                "48",
            )
            self.assertEqual(
                updated_live["GENERIC_MOVEMENT_ENGINEERING_REPLAY_DUPLICATE_MAX"].strip("`"),
                "48",
            )
            self.assertEqual(
                updated_live[
                    "GENERIC_MOVEMENT_ENGINEERING_PARTIAL_APPLY_CONTAINMENT_MAX"
                ].strip("`"),
                "48",
            )
            self.assertEqual(
                updated_live["GENERIC_MOVEMENT_ENGINEERING_RESTART_RECOVERY_MAX"].strip("`"),
                "48",
            )
            self.assertEqual(updated_live["GENERIC_MOVEMENT_PARALLEL_CONCURRENT_TRANSACTIONS_PROVEN_MAX"].strip("`"), "1")
            self.assertEqual(
                updated_live["SERVICE_FAILURE_ADAPTER_STATUS"].strip("`"),
                "SERVICE_FAILURE_ADAPTER_BRIDGE_QUALIFIED_TO_EXACT_MAXIMUM_TIER",
            )
            self.assertEqual(updated_live["SERVICE_FAILURE_ADAPTER_GENERIC_COHORT_PATH_MAX"].strip("`"), "48")
            self.assertEqual(updated_live["SERVICE_FAILURE_ADAPTER_EXACT_COMPATIBLE_MAX"].strip("`"), "48")
            self.assertEqual(updated_live["SERVICE_FAILURE_EFFECTIVE_RUNTIME_TIER"].strip("`"), "1")
            self.assertEqual(
                updated_live["CAUSAL_M7_TIER_DECISION_CONSUMPTION"].strip("`"),
                "EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED",
            )
            self.assertEqual(
                updated_live["PRODUCT_EVOLUTION_FRONTIER"].strip("`"),
                "EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED",
            )
            self.assertEqual(
                updated_live["CURRENT_TIER_AUTHORITY_REQUEST_ID"].strip("`"),
                "sdpauth_r1_" + ("d" * 24),
            )
            self.assertEqual(
                updated_live["CURRENT_TIER_AUTHORITY_REQUEST_HASH"].strip("`"),
                "d" * 64,
            )
            self.assertEqual(
                updated_live["CURRENT_TIER_AUTHORITY_REQUESTED_MAX_USERS"].strip("`"),
                "4",
            )
            self.assertEqual(
                updated_live[
                    "CURRENT_TIER_AUTHORITY_REQUEST_MAX_CONCURRENT_TRANSACTIONS"
                ].strip("`"),
                "1",
            )
            self.assertEqual(
                result["action_class_reuse_projection"]["legal_terminal"],
                "EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED",
            )
            self.assertEqual(
                result["action_class_reuse_projection"]["tier_formula"]["generic_primitive_max"],
                48,
            )
            self.assertEqual(
                result["action_class_reuse_projection"]["tier_formula"]["runtime_enabled_max"],
                1,
            )
            tier_matrix = {
                row["tier"]: row
                for row in result["action_class_reuse_projection"]["service_failure_adapter_tier_matrix"]
            }
            self.assertEqual(
                tier_matrix[4]["exact_residual"],
                "covered_only_by_independent_exact_tier_48_Authority_decision",
            )
            self.assertIn(
                "controlled_service_failure_adapter_outcome_tier_5",
                tier_matrix[5]["exact_residual"],
            )
            self.assertIn(
                "controlled_service_failure_adapter_outcome_tier_48",
                tier_matrix[48]["exact_residual"],
            )
            self.assertEqual(updated_live["CURRENT_VLESS_AFFECTED_SCOPE"].strip("`"), "29")
            self.assertEqual(updated_live["CURRENT_VLESS_PROTECTED_SCOPE"].strip("`"), "2")
            self.assertEqual(updated_live["CURRENT_VLESS_UNRESOLVED_SCOPE"].strip("`"), "27")
            self.assertEqual(updated_live["CURRENT_VLESS_LAST_OUTCOME_ID"].strip("`"), "outcome_runtime_current")
            self.assertEqual(updated_live["CURRENT_VLESS_SCOPE_PROJECTION_STATUS"].strip("`"), "PASS_CURRENT_ROUTE_AND_CUMULATIVE_LINEAGE_RECONCILED")
            self.assertIn("affected=29, protected=2, unresolved=27", updated_live["CURRENT_VLESS_SERVICE_INCIDENT"])
            self.assertEqual(
                updated_live["CURRENT_VLESS_SERVICE_INCIDENT_TERMINAL"].strip("`"),
                "NOT_TERMINAL; existing Matrix owner retains the continuing incident and exact durable successor",
            )

    def test_policy_reconciliation_consumes_exact_pending_tier4_transition_and_closes_empty_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps_path.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path)
            source = cps_path.read_text(encoding="utf-8")
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                source, "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
            ))
            contract_hash = "a" * 64
            runtime_status = {
                "schema_version": "v7.standing-delegated-policy-runtime-status.v1",
                "status": "PASS", "ok": True, "contract_status": "ACTIVE",
                "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                "authority_decision": "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                "audit_provenance_verified": True,
                "contract_id": f"sdpc_{contract_hash[:24]}",
                "contract_hash": contract_hash,
                "authority_request_id": live[
                    "CURRENT_TIER_AUTHORITY_REQUEST_ID"
                ].strip("`"),
                "authority_request_hash": live[
                    "CURRENT_TIER_AUTHORITY_REQUEST_HASH"
                ].strip("`"),
                "expires_at": "2099-01-01T00:00:00+00:00",
                "policy_scope_hash": live[
                    "CURRENT_TIER_AUTHORITY_REQUEST_POLICY_SCOPE_HASH"
                ].strip("`"),
                "action_class": live[
                    "CURRENT_TIER_AUTHORITY_REQUEST_ACTION_CLASS"
                ].strip("`"),
                "max_users_per_action": 4,
                "max_concurrent_transactions": 1,
                "allowed_failure_families": [
                    "channel_hard_fail", "service_specific_failure",
                ],
                "cooldown": {
                    "per_user_seconds": 1800,
                    "per_source_target_pair_seconds": 1800,
                },
                "anti_flap": "PASS",
                "pending_tier_authority_request": {
                    "status": "NONE", "pending_count": 0,
                },
                "service_failure_causal_integrity": {
                    "schema_version": "v7.service-failure-causal-integrity-status.v1",
                    "final_verdict": "PASS", "invalid_states": [],
                    "open_incident_projections": [{
                        "incident_id": live["CURRENT_VLESS_INCIDENT_ID"].strip("`"),
                        "incident_generation": "generation-runtime-drained",
                        "source_channel": "vless",
                        "incident_state": "SOURCE_SCOPE_EMPTY",
                        "affected_scope_count": 0,
                        "protected_scope_count": 0,
                        "unresolved_scope_count": 0,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                        "affected_scope_fingerprint": "affected-empty",
                        "protected_scope_fingerprint": "protected-empty",
                        "unresolved_scope_fingerprint": "unresolved-empty",
                        "explicitly_excluded_or_recovered_scope_fingerprint": "excluded-empty",
                        "last_execution_feedback_id": "execfb_last",
                        "last_outcome_id": "outcome_last",
                        "last_learning_id": "learning_last",
                        "last_packet_id": "packet_last",
                        "next_required_consumer": "tools/v7-service-matrix-refresh-all",
                        "reentry_condition": "fresh Matrix observation",
                    }],
                },
            }
            result = self.sync.reconcile_active_standing_delegated_policy_to_cps(
                runtime_status, root=root,
            )
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(
                result["next_action"],
                "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION",
            )
            updated = cps_path.read_text(encoding="utf-8")
            updated_live = self.sync._markdown_field_table(self.sync._markdown_section(
                updated, "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
            ))
            self.assertEqual(
                updated_live["CURRENT_AUTHORITY_REQUEST_ID"].strip("`"),
                runtime_status["authority_request_id"],
            )
            self.assertEqual(
                updated_live["CURRENT_TIER_AUTHORITY_REQUEST_STATUS"].strip("`"),
                "NONE",
            )
            self.assertEqual(
                updated_live["CURRENT_ACTION_CLASS_AUTHORITY_APPROVED_TIER"].strip("`"),
                "TIER_4_CURRENT_STANDING_POLICY",
            )
            self.assertEqual(
                updated_live["CURRENT_ACTION_CLASS_RUNTIME_ENABLED_TIER"].strip("`"),
                "TIER_4_SERIAL_COHORT",
            )
            self.assertEqual(
                updated_live["CURRENT_ACTION_CLASS_PRODUCTION_PROVEN_TIER"].strip("`"),
                "TIER_1_CURRENT_CLASS; GENERIC_MOVEMENT_PRODUCTION_EVIDENCE_REUSED_TO_48; "
                "SERVICE_FAILURE_CONTROLLED_TIERS_5_10_25_48_PENDING",
            )
            self.assertEqual(
                updated_live["PRODUCT_EVOLUTION_FRONTIER"].strip("`"),
                "EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED",
            )
            self.assertEqual(
                updated_live["INCIDENT_FRONTIER"].strip("`"),
                "CURRENT_SOURCE_SCOPE_EMPTY",
            )
            self.assertEqual(
                updated_live["CURRENT_VLESS_UNRESOLVED_SCOPE"].strip("`"), "0",
            )
            self.assertEqual(
                result["action_class_reuse_projection"]["legal_terminal"],
                "EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED",
            )
            tier_matrix = {
                row["tier"]: row
                for row in result["action_class_reuse_projection"][
                    "service_failure_adapter_tier_matrix"
                ]
            }
            self.assertEqual(tier_matrix[4]["exact_residual"], "NONE")

    def test_policy_reconciliation_rejects_unproven_tier_request_transition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            cps_path.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path)
            contract_hash = "a" * 64
            runtime_status = {
                "schema_version": "v7.standing-delegated-policy-runtime-status.v1",
                "status": "PASS", "ok": True, "contract_status": "ACTIVE",
                "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
                "authority_decision": "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY",
                "audit_provenance_verified": True,
                "contract_id": f"sdpc_{contract_hash[:24]}",
                "contract_hash": contract_hash,
                "authority_request_id": "sdpauth_r1_" + ("f" * 24),
                "authority_request_hash": "f" * 64,
                "expires_at": "2099-01-01T00:00:00+00:00",
                "policy_scope_hash": "e" * 64,
                "action_class": "channel hard-fail failover",
                "max_users_per_action": 4,
                "max_concurrent_transactions": 1,
                "service_failure_causal_integrity": {
                    "schema_version": "v7.service-failure-causal-integrity-status.v1",
                    "final_verdict": "PASS", "invalid_states": [],
                    "open_incident_projections": [],
                },
            }
            result = self.sync.reconcile_active_standing_delegated_policy_to_cps(
                runtime_status, root=root,
            )
            self.assertEqual(result["final_verdict"], "STOP_SAFE")
            self.assertEqual(
                result["errors"], ["cps_runtime_authority_request_mismatch"],
            )

    def test_causal_integrity_status_names_missing_successor_scope_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("l3-runtime-state.json").write_text(json.dumps({
                "incidents": {
                    "broken": {
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "incident_state": "PARTIALLY_PROTECTED",
                        "attempt_terminal": "STOP_SAFE",
                        "durable_successor_published": True,
                        "last_execution_feedback_id": "execfb_missing",
                        "execution_feedback_ids": ["execfb_missing"],
                        "current_source_scope": {
                            "status": "ACCOUNTED",
                            "affected_scope_count": 3,
                            "protected_scope_count": 1,
                            "unresolved_scope_count": 1,
                            "explicitly_excluded_or_recovered_scope_count": 0,
                            "affected_scope_fingerprint": "new-generation",
                        },
                        "incident_cumulative_scope": {
                            "current_source_scope_fingerprint": "old-generation",
                            "entries": [],
                            "lineage_pointers": [],
                        },
                    },
                },
            }), encoding="utf-8")
            status = self.autoswitch.service_failure_causal_integrity_status(state_dir)
        self.assertEqual(status["final_verdict"], "STOP_SAFE")
        self.assertEqual(status["invalid_states"], [
            "CAUSAL_LINEAGE_BROKEN",
            "CURRENT_SCOPE_REPLACES_CUMULATIVE_HISTORY",
            "DURABLE_SUCCESSOR_WITHOUT_CONSUMER",
            "INCIDENT_SCOPE_ACCOUNTING_BROKEN",
            "INVALID_OPEN_INCIDENT_NO_SUCCESSOR",
            "NONTERMINAL_RESULT_WITHOUT_DURABLE_SUCCESSOR",
            "SUCCESSFUL_ATTEMPT_WITHOUT_SCOPE_UPDATE",
        ])

    def test_causal_integrity_status_accepts_open_incident_with_durable_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("l3-runtime-state.json").write_text(json.dumps({
                "incidents": {
                    "valid": {
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "incident_state": "PARTIALLY_PROTECTED",
                        "attempt_terminal": "SUCCESS",
                        "next_required_consumer": "tools/v7-service-matrix-refresh-all",
                        "reentry_condition": "fresh Matrix observation",
                        "last_execution_feedback_id": "execfb_valid",
                        "execution_feedback_ids": ["execfb_valid"],
                        "current_source_scope": {
                            "status": "ACCOUNTED",
                            "affected_scope_count": 3,
                            "protected_scope_count": 1,
                            "unresolved_scope_count": 2,
                            "explicitly_excluded_or_recovered_scope_count": 0,
                            "affected_scope_fingerprint": "current-generation",
                        },
                        "incident_cumulative_scope": {
                            "current_source_scope_fingerprint": "current-generation",
                            "packet_bound_success_count": 1,
                            "entries": [{"feedback_id": "execfb_valid"}],
                            "lineage_pointers": ["execfb_valid"],
                        },
                    },
                },
            }), encoding="utf-8")
            status = self.autoswitch.service_failure_causal_integrity_status(state_dir)
        self.assertEqual(status["final_verdict"], "PASS", status)
        self.assertEqual(status["open_incident_count"], 1)
        self.assertEqual(status["open_incident_projections"], [{
            "incident_id": "",
            "incident_generation": "",
            "source_channel": "",
            "incident_state": "PARTIALLY_PROTECTED",
            "affected_scope_count": 3,
            "protected_scope_count": 1,
            "unresolved_scope_count": 2,
            "explicitly_excluded_or_recovered_scope_count": 0,
            "affected_scope_fingerprint": "current-generation",
            "protected_scope_fingerprint": "",
            "unresolved_scope_fingerprint": "",
            "explicitly_excluded_or_recovered_scope_fingerprint": "",
            "packet_bound_success_count": 1,
            "cumulative_lineage_count": 1,
            "last_execution_feedback_id": "execfb_valid",
            "last_outcome_id": "",
            "last_learning_id": "",
            "last_packet_id": "",
            "next_required_consumer": "tools/v7-service-matrix-refresh-all",
            "reentry_condition": "fresh Matrix observation",
            "last_observed_at": "",
            "raw_user_list_stored": False,
        }])

    def test_causal_integrity_status_keeps_closed_legacy_anomaly_auditable(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            state_dir.joinpath("l3-runtime-state.json").write_text(json.dumps({
                "incidents": {
                    "closed-legacy": {
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "incident_id": "sfinc_closed",
                        "incident_generation": "old-generation",
                        "channel": "old-source",
                        "incident_state": "INTENT_CLOSED",
                        "last_execution_feedback_id": "execfb_old",
                        "execution_feedback_ids": ["execfb_old"],
                        "current_source_scope": {
                            "status": "ACCOUNTED",
                            "affected_scope_count": 1,
                            "protected_scope_count": 1,
                            "unresolved_scope_count": 0,
                            "explicitly_excluded_or_recovered_scope_count": 0,
                            "affected_scope_fingerprint": "old-scope",
                        },
                        "incident_cumulative_scope": {
                            "current_source_scope_fingerprint": "different-old-scope",
                            "entries": [],
                            "lineage_pointers": [],
                        },
                    },
                },
            }), encoding="utf-8")
            status = self.autoswitch.service_failure_causal_integrity_status(state_dir)
        self.assertEqual(status["final_verdict"], "PASS", status)
        self.assertEqual(status["invalid_states"], [])
        self.assertEqual(status["historical_integrity_warnings"], [{
            "incident_id": "sfinc_closed",
            "incident_generation": "old-generation",
            "source_channel": "old-source",
            "warning_states": [
                "CURRENT_SCOPE_REPLACES_CUMULATIVE_HISTORY",
                "SUCCESSFUL_ATTEMPT_WITHOUT_SCOPE_UPDATE",
            ],
            "owner": "existing l3-runtime-state closed historical projection",
            "blocks_live_execution": False,
            "raw_user_list_stored": False,
        }])

    def test_recovery_receipt_closes_older_broken_open_intent_same_source_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            now = self.autoswitch.now_iso()
            (state_dir / "service-matrix.json").write_text(json.dumps({
                "updated": now,
                "items": {"vless": {"services": {"google": {
                    "status": "OK", "ok": True, "observed_at": now,
                }}}},
            }), encoding="utf-8")
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {"old": {
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                    "incident_id": "sfinc_old",
                    "incident_generation": "egid_same",
                    "channel": "vless",
                    "services": ["google"],
                    "incident_state": "PARTIALLY_PROTECTED",
                    "last_observed_at": "2026-01-01T00:00:00+00:00",
                    "current_source_scope": {
                        "status": "INCIDENT_SCOPE_ACCOUNTING_BROKEN",
                        "affected_scope_count": 4,
                        "protected_scope_count": 1,
                        "unresolved_scope_count": 2,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                    },
                    "next_required_consumer": "existing-consumer",
                    "reentry_condition": "existing-reentry",
                }},
            }), encoding="utf-8")
            (state_dir / "closure-records.jsonl").write_text(json.dumps({
                "object_type": "passive_production_event",
                "object_id": "sre_recovered",
                "channel": "vless",
                "services": ["google"],
                "egress_identity_generation": "egid_same",
                "terminal_outcome_classification": "RECOVERY_OBSERVED_NO_ACTION",
                "observed_at": now,
            }) + "\n", encoding="utf-8")
            args = argparse.Namespace(
                state_dir=str(state_dir),
                action_class_audit_store=str(state_dir / "audit.jsonl"),
            )
            planner = self.autoswitch.AutoswitchPlanner.__new__(
                self.autoswitch.AutoswitchPlanner
            )
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.args = args
            result = planner.reconcile_service_failure_execution_outcomes()
            state = json.loads(
                (state_dir / "l3-runtime-state.json").read_text(encoding="utf-8")
            )
            status = self.autoswitch.service_failure_causal_integrity_status(state_dir)
        record = state["incidents"]["old"]
        self.assertEqual(result["recovery_terminal_reconciliation"]["changed"], 1)
        self.assertEqual(record["incident_state"], "INTENT_CLOSED")
        self.assertEqual(record["current_source_scope"]["unresolved_scope_count"], 0)
        self.assertEqual(
            record["current_source_scope"]["explicitly_excluded_or_recovered_scope_count"], 3,
        )
        self.assertEqual(status["final_verdict"], "PASS", status)

    def test_empty_current_route_scope_closes_protection_intent_not_channel_incident(self):
        """A source with no current users cannot remain an actionable cohort."""
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=awg0 enabled=1\n",
                encoding="utf-8",
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {"open": {
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                    "incident_id": "sfinc_empty_scope",
                    "incident_generation": "egid_same",
                    "channel": "source-a",
                    "incident_state": "OPEN",
                    "channel_incident_state": "OPEN",
                    "current_source_scope": {
                        "status": "ACCOUNTED",
                        "baseline_event_id": "sfe_source_a",
                        "affected_scope_count": 3,
                        "affected_scope_fingerprint": "a" * 64,
                        "protected_scope_count": 0,
                        "unresolved_scope_count": 3,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                    },
                    "scope_accounting": {
                        "status": "ACCOUNTED",
                        "baseline_event_id": "sfe_source_a",
                        "affected_scope_count": 3,
                        "affected_scope_fingerprint": "a" * 64,
                        "protected_scope_count": 0,
                        "unresolved_scope_count": 3,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                    },
                    "next_required_consumer": "existing-consumer",
                    "reentry_condition": "existing-reentry",
                }},
            }), encoding="utf-8")
            planner = self.autoswitch.AutoswitchPlanner.__new__(
                self.autoswitch.AutoswitchPlanner
            )
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.args = argparse.Namespace(
                state_dir=str(state_dir),
                action_class_audit_store=str(state_dir / "audit.jsonl"),
            )
            result = planner.reconcile_service_failure_execution_outcomes()
            state = json.loads(
                (state_dir / "l3-runtime-state.json").read_text(encoding="utf-8")
            )
        record = state["incidents"]["open"]
        scope = record["current_source_scope"]
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertEqual(record["incident_state"], "INTENT_CLOSED")
        self.assertEqual(record["channel_incident_state"], "OPEN_NO_ASSIGNED_USERS")
        self.assertEqual(record["attempt_terminal"], "CURRENT_SOURCE_SCOPE_EMPTY_NO_ACTION")
        self.assertEqual(scope["unresolved_scope_count"], 0)
        self.assertEqual(scope["explicitly_excluded_or_recovered_scope_count"], 3)
        self.assertEqual(
            scope["scope_membership_law"],
            "CURRENT_ROUTE_SOURCE_SCOPE_EMPTY_PROTECTION_INTENT_CLOSURE",
        )
        self.assertFalse(result["forbidden_effects"]["routing_mutation"])
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)

    def test_recovery_receipt_closes_old_episode_after_new_service_failure(self):
        """A later failure is a new episode, not a retroactive reopening."""
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "service-matrix.json").write_text(json.dumps({
                "items": {"vless": {"services": {"spotify": {
                    "status": "FAIL",
                    "ok": False,
                    "failure_started_at": "2026-01-01T02:00:00+00:00",
                }}}},
            }), encoding="utf-8")
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {"old": {
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                    "incident_id": "sfinc_old_episode",
                    "incident_generation": "egid_same",
                    "channel": "vless",
                    "services": ["spotify"],
                    "incident_state": "OPEN",
                    "last_observed_at": "2026-01-01T00:00:00+00:00",
                    "current_source_scope": {
                        "status": "INCIDENT_SCOPE_ACCOUNTING_BROKEN",
                        "affected_scope_count": 2,
                        "protected_scope_count": 0,
                        "unresolved_scope_count": 1,
                        "explicitly_excluded_or_recovered_scope_count": 0,
                    },
                }},
            }), encoding="utf-8")
            (state_dir / "closure-records.jsonl").write_text(json.dumps({
                "object_type": "passive_production_event",
                "object_id": "sre_old_episode_recovered",
                "channel": "vless",
                "services": ["spotify"],
                "egress_identity_generation": "egid_same",
                "terminal_outcome_classification": "RECOVERY_OBSERVED_NO_ACTION",
                "created_at": "2026-01-01T01:00:00+00:00",
            }) + "\n", encoding="utf-8")
            planner = self.autoswitch.AutoswitchPlanner.__new__(
                self.autoswitch.AutoswitchPlanner
            )
            planner.state_dir = state_dir
            planner.l3_runtime_state_file = state_dir / "l3-runtime-state.json"
            planner.args = argparse.Namespace(
                state_dir=str(state_dir),
                action_class_audit_store=str(state_dir / "audit.jsonl"),
            )
            result = planner.reconcile_service_failure_execution_outcomes()
            state = json.loads(
                (state_dir / "l3-runtime-state.json").read_text(encoding="utf-8")
            )
        record = state["incidents"]["old"]
        self.assertEqual(result["recovery_terminal_reconciliation"]["changed"], 1)
        self.assertEqual(record["incident_state"], "INTENT_CLOSED")
        self.assertEqual(
            record["attempt_terminal"],
            "RECOVERY_OBSERVED_NEW_FAILURE_GENERATION_SEPARATE",
        )
        self.assertEqual(
            record["current_source_scope"]["current_matrix_relation"],
            "SUBSEQUENT_FAILURE_EPOCH",
        )

    def test_existing_closure_owner_is_consumed_once_by_omp(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_test",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-26T00:00:00+00:00",
                "source_incident_id": "sfinc_test",
                "situation_id": "situation_test",
                "decision_trace_id": "decision_test",
                "stop_safe_classification": "STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")
            first = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(first["final_verdict"], "PASS")
            self.assertEqual(first["next_output"], "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR")
            second = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(second["final_verdict"], "NO_PENDING_OBLIGATION")

    def test_changed_current_obligation_semantics_reenter_once_without_replaying_lineage(self):
        """A stale receipt cannot suppress a later current-scope revalidation."""
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            old_scope = {"affected_scope_count": 2, "unresolved_scope_count": 2,
                         "affected_scope_fingerprint": "old"}
            current_scope = {"affected_scope_count": 1, "unresolved_scope_count": 1,
                             "affected_scope_fingerprint": "current"}
            base = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_same_lineage",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "source_incident_id": "sfinc_current",
                "situation_id": "situation_current",
                "decision_trace_id": "decision_current",
                "stop_safe_classification": "STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION",
            }
            def fingerprint(scope):
                encoded = json.dumps({
                    "automation_obligation_id": base["automation_obligation_id"],
                    "source_incident_id": base["source_incident_id"],
                    "situation_id": base["situation_id"],
                    "decision_trace_id": base["decision_trace_id"],
                    "classification": base["stop_safe_classification"],
                    "incident_frontier": base["incident_frontier"],
                    "product_evolution_frontier": base["product_evolution_frontier"],
                    "current_source_scope": scope,
                }, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
            old = {**base, "created_at": "2026-08-12T20:00:00+00:00",
                   "current_source_scope": old_scope,
                   "automation_consumption_fingerprint": fingerprint(old_scope)}
            current = {**base, "created_at": "2026-08-12T20:01:00+00:00",
                       "current_source_scope": current_scope,
                       "automation_consumption_fingerprint": fingerprint(current_scope)}
            old_receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": old["automation_obligation_id"],
                "automation_consumption_fingerprint": old["automation_consumption_fingerprint"],
            }
            (state_dir / "closure-records.jsonl").write_text(
                "\n".join(json.dumps(row) for row in (old, old_receipt, current)) + "\n",
                encoding="utf-8",
            )
            first = self.sync.consume_service_failure_automation_frontier(
                state_dir=state_dir, persist_cps=False
            )
            self.assertEqual(first["final_verdict"], "PASS", first)
            self.assertEqual(
                first["receipt"]["automation_consumption_fingerprint"],
                current["automation_consumption_fingerprint"],
            )
            second = self.sync.consume_service_failure_automation_frontier(
                state_dir=state_dir, persist_cps=False
            )
            self.assertEqual(second["final_verdict"], "NO_PENDING_OBLIGATION", second)

    def test_consumed_current_receipt_is_available_only_for_matching_execution_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            scope = {
                "status": "ACCOUNTED", "affected_scope_count": 3,
                "protected_scope_count": 0, "unresolved_scope_count": 3,
                "explicitly_excluded_or_recovered_scope_count": 0,
                "affected_scope_fingerprint": "f" * 64,
            }
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_current", "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "automation_consumption_fingerprint": "a" * 64,
                "source_incident_id": "sfinc_current", "situation_id": "sit_current",
                "decision_trace_id": "dec_current", "created_at": "2026-08-12T20:00:00+00:00",
                "current_source_scope": scope,
            }
            receipt = {
                "object_type": "service_failure_automation_omp_consumption", "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_current", "automation_consumption_fingerprint": "a" * 64,
                "source_incident_id": "sfinc_current", "situation_id": "sit_current",
                "decision_trace_id": "dec_current", "next_action": "CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN",
                "consumed_at": "2026-08-12T20:01:00+00:00", "current_source_scope": scope,
            }
            (state_dir / "closure-records.jsonl").write_text(
                "\n".join(json.dumps(row) for row in (obligation, receipt)) + "\n", encoding="utf-8"
            )
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {"current": {
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "incident_id": "sfinc_current",
                    "incident_state": "OPEN", "channel_incident_state": "OPEN", "current_source_scope": scope,
                }}
            }), encoding="utf-8")
            handoff = self.sync.service_failure_automation_consumed_execution_handoff(state_dir=state_dir)
            self.assertEqual(handoff["final_verdict"], "READY", handoff)
            self.assertEqual(handoff["obligation"]["automation_obligation_id"], "sfaob_current")

            receipt["current_source_scope"] = {**scope, "affected_scope_fingerprint": "b" * 64}
            (state_dir / "closure-records.jsonl").write_text(
                "\n".join(json.dumps(row) for row in (obligation, receipt)) + "\n", encoding="utf-8"
            )
            rejected = self.sync.service_failure_automation_consumed_execution_handoff(state_dir=state_dir)
            self.assertEqual(rejected["final_verdict"], "NO_CURRENT_CONSUMED_HANDOFF", rejected)

    def test_omp_frontier_prefers_live_accounted_scope_over_newer_zero_scope_terminal(self):
        """A historical no-scope terminal cannot starve the current incident."""
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            live = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_live_vless",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-08-08T18:09:43+00:00",
                "source_incident_id": "sfinc_live_vless",
                "channel": "vless",
                "current_source_scope": {
                    "status": "ACCOUNTED",
                    "affected_scope_count": 35,
                    "unresolved_scope_count": 35,
                },
            }
            newer_historical = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_historical_zero_scope",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-08-08T18:16:30+00:00",
                "source_incident_id": "sfinc_historical",
                "channel": "1",
                "current_source_scope": {
                    "status": "ACCOUNTED",
                    "affected_scope_count": 0,
                    "unresolved_scope_count": 0,
                },
            }
            (state_dir / "closure-records.jsonl").write_text(
                "\n".join(json.dumps(row) for row in (live, newer_historical)) + "\n",
                encoding="utf-8",
            )

            frontier = self.sync.service_failure_automation_frontier(state_dir=state_dir)

        self.assertEqual(frontier["selected"]["automation_obligation_id"], "sfaob_live_vless")

    def test_ct_m0f_coalesces_reobserved_same_failure_only_after_exact_omp_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            old = {
                "incident_id": "sfinc_old", "incident_state": "OPEN",
                "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                "incident_generation": "egid_same", "obligation_id": "sfaob_old",
                "updated_at": "2026-08-08T18:09:43+00:00",
                "current_source_scope": {"status": "ACCOUNTED", "affected_scope_count": 35,
                    "unresolved_scope_count": 35, "affected_scope_fingerprint": "f" * 64},
            }
            current = {
                "incident_id": "sfinc_current", "incident_state": "OPEN",
                "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                "incident_generation": "egid_same", "obligation_id": "sfaob_current",
                "updated_at": "2026-08-08T18:24:33+00:00",
                "current_source_scope": {"status": "ACCOUNTED", "affected_scope_count": 35,
                    "unresolved_scope_count": 35, "affected_scope_fingerprint": "f" * 64},
            }
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {"old": old, "current": current},
            }), encoding="utf-8")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_current",
                "source_incident_id": "sfinc_current",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(receipt) + "\n", encoding="utf-8")

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(state_dir, "vless")

        self.assertTrue(binding["ok"], binding)
        self.assertEqual(binding["source_incident_id"], "sfinc_current")

    def test_ct_m0f_keeps_different_live_scope_generations_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            records = {}
            receipts = []
            for suffix, generation, fingerprint in (("a", "egid_a", "a" * 64), ("b", "egid_b", "b" * 64)):
                incident_id = f"sfinc_{suffix}"
                obligation_id = f"sfaob_{suffix}"
                records[suffix] = {
                    "incident_id": incident_id, "incident_state": "OPEN",
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                    "incident_generation": generation, "obligation_id": obligation_id,
                    "current_source_scope": {"status": "ACCOUNTED", "affected_scope_count": 1,
                        "unresolved_scope_count": 1, "affected_scope_fingerprint": fingerprint},
                }
                receipts.append({"object_type": "service_failure_automation_omp_consumption",
                    "closure_state": "OMP_CONSUMED", "automation_obligation_id": obligation_id,
                    "source_incident_id": incident_id})
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({"incidents": records}), encoding="utf-8")
            (state_dir / "closure-records.jsonl").write_text("\n".join(json.dumps(row) for row in receipts) + "\n", encoding="utf-8")

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(state_dir, "vless")

        self.assertFalse(binding["ok"])
        self.assertEqual(binding["status"], "AMBIGUOUS_ACTIVE_SERVICE_FAILURE_BINDING")

    def test_ct_m0f_selects_one_consumed_scope_matching_current_route_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            live_users = ["10.0.0.2", "10.0.0.3"]
            live_fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": live_users,
            })
            stale_fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": ["10.0.0.2", "10.0.0.4"],
            })
            (state_dir / "users.registry").write_text(
                "\n".join(
                    f"ip={ip} current=vless enabled=1" for ip in live_users
                ) + "\n",
                encoding="utf-8",
            )
            records = {}
            receipts = []
            for suffix, fingerprint, observed_at in (
                ("current", live_fingerprint, "2026-08-09T10:08:03+00:00"),
                ("stale", stale_fingerprint, "2026-08-09T10:23:26+00:00"),
            ):
                incident_id = f"sfinc_{suffix}"
                obligation_id = f"sfaob_{suffix}"
                records[suffix] = {
                    "incident_id": incident_id, "incident_state": "OPEN",
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                    "incident_generation": "egid_same", "obligation_id": obligation_id,
                    "last_observed_at": observed_at,
                    "current_source_scope": {
                        "status": "ACCOUNTED", "affected_scope_count": 2,
                        "unresolved_scope_count": 2,
                        "affected_scope_fingerprint": fingerprint,
                    },
                }
                receipts.append({
                    "object_type": "service_failure_automation_omp_consumption",
                    "closure_state": "OMP_CONSUMED",
                    "automation_obligation_id": obligation_id,
                    "source_incident_id": incident_id,
                })
            (state_dir / "l3-runtime-state.json").write_text(
                json.dumps({"incidents": records}), encoding="utf-8"
            )
            (state_dir / "closure-records.jsonl").write_text(
                "\n".join(json.dumps(row) for row in receipts) + "\n",
                encoding="utf-8",
            )

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state_dir, "vless"
            )

        self.assertTrue(binding["ok"], binding)
        self.assertEqual(binding["source_incident_id"], "sfinc_current")
        self.assertEqual(binding["live_source_scope"]["affected_scope_count"], 2)
        self.assertFalse(binding["live_source_scope"]["raw_user_list_stored"])

    def test_ct_m0f_binds_next_packet_to_unresolved_live_subset(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            remaining_user = "10.0.0.3"
            remaining_fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": [remaining_user],
            })
            original_fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": ["10.0.0.2", remaining_user],
            })
            (state_dir / "users.registry").write_text(
                f"ip={remaining_user} current=vless enabled=1\n",
                encoding="utf-8",
            )
            incident = {
                "incident_id": "sfinc_partial", "incident_state": "OPEN",
                "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                "incident_generation": "egid_partial", "obligation_id": "sfaob_partial",
                "current_source_scope": {
                    "status": "ACCOUNTED",
                    "affected_scope_count": 2,
                    "affected_scope_fingerprint": original_fingerprint,
                    "protected_scope_count": 1,
                    "unresolved_scope_count": 1,
                    "unresolved_scope_fingerprint": remaining_fingerprint,
                    "explicitly_excluded_or_recovered_scope_count": 0,
                },
            }
            (state_dir / "l3-runtime-state.json").write_text(
                json.dumps({"incidents": {"partial": incident}}),
                encoding="utf-8",
            )
            (state_dir / "closure-records.jsonl").write_text(json.dumps({
                "object_type": "service_failure_automation_omp_consumption",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_partial",
                "source_incident_id": "sfinc_partial",
            }) + "\n", encoding="utf-8")

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state_dir, "vless"
            )

        self.assertTrue(binding["ok"], binding)
        self.assertEqual(binding["source_scope_count"], 1)
        self.assertEqual(binding["source_scope_fingerprint"], remaining_fingerprint)
        self.assertEqual(binding["incident_affected_scope_count"], 2)

    def test_ct_m0f_rejects_single_consumed_scope_stale_against_current_route_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n",
                encoding="utf-8",
            )
            stale_scope = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": ["10.0.0.3"],
            })
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {"stale": {
                    "incident_id": "sfinc_stale", "incident_state": "OPEN",
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                    "incident_generation": "egid_same", "obligation_id": "sfaob_stale",
                    "current_source_scope": {
                        "status": "ACCOUNTED", "affected_scope_count": 1,
                        "unresolved_scope_count": 1,
                        "affected_scope_fingerprint": stale_scope,
                    },
                }},
            }), encoding="utf-8")
            (state_dir / "closure-records.jsonl").write_text(json.dumps({
                "object_type": "service_failure_automation_omp_consumption",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_stale",
                "source_incident_id": "sfinc_stale",
            }) + "\n", encoding="utf-8")

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state_dir, "vless"
            )

        self.assertFalse(binding["ok"])
        self.assertEqual(
            binding["status"],
            "NO_CURRENT_ROUTE_MATCHING_ACTIVE_SERVICE_FAILURE_BINDING",
        )

    def test_ct_m0f_rejects_expired_event_before_governed_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            event_dir = root / "events"
            state_dir.mkdir()
            event_dir.mkdir()
            user = "10.0.0.2"
            fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": [user],
            })
            (state_dir / "users.registry").write_text(
                f"ip={user} current=vless enabled=1\n", encoding="utf-8"
            )
            incident = {
                "incident_id": "sfinc_expired", "incident_state": "OPEN",
                "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                "incident_generation": "egid_same", "obligation_id": "sfaob_expired",
                "current_source_scope": {
                    "status": "ACCOUNTED", "affected_scope_count": 1,
                    "affected_scope_fingerprint": fingerprint,
                    "unresolved_scope_count": 1,
                    "unresolved_scope_fingerprint": fingerprint,
                },
            }
            (state_dir / "l3-runtime-state.json").write_text(
                json.dumps({"incidents": {"expired": incident}}), encoding="utf-8"
            )
            (state_dir / "closure-records.jsonl").write_text(json.dumps({
                "object_type": "service_failure_automation_omp_consumption",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_expired",
                "source_incident_id": "sfinc_expired",
            }) + "\n", encoding="utf-8")
            (event_dir / "service-failure-events.jsonl").write_text(json.dumps({
                "event_id": "sfe_expired",
                "event_type": "SERVICE_FAILURE_OBSERVED",
                "capture_only": True,
                "event_provenance": "EXTERNAL_UNATTRIBUTED",
                "channel": "vless",
                "source_incident_id": "sfinc_expired",
                "observed_at": "2020-01-01T00:00:00+00:00",
                "source_scope": {
                    "affected_scope_count": 1,
                    "affected_scope_fingerprint": fingerprint,
                },
            }) + "\n", encoding="utf-8")

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state_dir, "vless", event_dir=event_dir,
            )

        self.assertFalse(binding["ok"])
        self.assertEqual(binding["fresh_event_status"], "MISSING")
        self.assertIn(
            "fresh_matching_service_failure_event_missing", binding["blockers"],
        )

    def test_ct_m0f_coalesces_repeated_current_scope_observations(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            (state_dir / "users.registry").write_text(
                "ip=10.0.0.2 current=vless enabled=1\n",
                encoding="utf-8",
            )
            fingerprint = self.autoswitch.sha256_json({
                "source_channel": "vless", "users": ["10.0.0.2"],
            })
            records = {}
            receipts = []
            for suffix, observed_at in (
                ("older", "2026-08-09T10:08:03+00:00"),
                ("newer", "2026-08-09T10:23:26+00:00"),
            ):
                incident_id = f"sfinc_{suffix}"
                obligation_id = f"sfaob_{suffix}"
                records[suffix] = {
                    "incident_id": incident_id, "incident_state": "OPEN",
                    "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                    "incident_generation": "egid_same", "obligation_id": obligation_id,
                    "last_observed_at": observed_at,
                    "current_source_scope": {
                        "status": "ACCOUNTED", "affected_scope_count": 1,
                        "unresolved_scope_count": 1,
                        "affected_scope_fingerprint": fingerprint,
                    },
                }
                receipts.append({
                    "object_type": "service_failure_automation_omp_consumption",
                    "closure_state": "OMP_CONSUMED",
                    "automation_obligation_id": obligation_id,
                    "source_incident_id": incident_id,
                })
            (state_dir / "l3-runtime-state.json").write_text(
                json.dumps({"incidents": records}), encoding="utf-8"
            )
            (state_dir / "closure-records.jsonl").write_text(
                "\n".join(json.dumps(row) for row in receipts) + "\n",
                encoding="utf-8",
            )

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state_dir, "vless"
            )

        self.assertTrue(binding["ok"], binding)
        self.assertEqual(binding["source_incident_id"], "sfinc_newer")

    def test_ct_m0f_ignores_broken_historical_scope_when_current_scope_is_consumed(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            current = {
                "incident_id": "sfinc_current", "incident_state": "OPEN",
                "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                "incident_generation": "egid_same", "obligation_id": "sfaob_current",
                "updated_at": "2026-08-09T07:49:42+00:00",
                "current_source_scope": {"status": "ACCOUNTED", "affected_scope_count": 34,
                    "unresolved_scope_count": 34, "affected_scope_fingerprint": "f" * 64},
            }
            broken_historical = {
                "incident_id": "sfinc_broken", "incident_state": "OPEN",
                "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE", "channel": "vless",
                "incident_generation": "egid_same", "obligation_id": "sfaob_broken",
                "updated_at": "2026-08-09T06:49:42+00:00",
                "current_source_scope": {"status": "INCIDENT_SCOPE_ACCOUNTING_BROKEN",
                    "affected_scope_count": 35, "unresolved_scope_count": 34,
                    "affected_scope_fingerprint": "b" * 64},
            }
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "incidents": {"current": current, "broken": broken_historical},
            }), encoding="utf-8")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_current",
                "source_incident_id": "sfinc_current",
            }
            (state_dir / "closure-records.jsonl").write_text(
                json.dumps(receipt) + "\n", encoding="utf-8"
            )

            binding = self.autoswitch.ct_m0f_active_service_failure_binding_projection(
                state_dir, "vless"
            )

        self.assertTrue(binding["ok"], binding)
        self.assertEqual(binding["source_incident_id"], "sfinc_current")

    def test_m2_receipt_is_materialized_into_existing_passive_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_key = "passive_m2_test"
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "schema_version": "v7.l3-runtime-state.v1",
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key,
                        "incident_id": "sfinc_m2_test",
                        "incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "next_required_consumer": "tools/v7_sync_lib.consume_service_failure_automation_frontier",
                        "reentry_condition": "ready obligation",
                        "transition_id": "ptr_m2_test",
                    },
                },
            }), encoding="utf-8")
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_m2_test",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-27T00:00:00+00:00",
                "incident_key": incident_key,
                "source_incident_id": "sfinc_m2_test",
                "situation_id": "situation_m2_test",
                "decision_trace_id": "decision_m2_test",
                "stop_safe_classification": "STOP_SAFE_DATA_OR_EVIDENCE_GAP",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")

            result = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(result["incident_projection_reconciliation"]["final_verdict"], "PASS")
            self.assertEqual(result["incident_projection_reconciliation"]["changed_records"], 1)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            record = state["incidents"][incident_key]
            self.assertEqual(record["omp_consumption_state"], "OMP_CONSUMED")
            self.assertTrue(record["omp_receipt_id"])
            self.assertEqual(record["next_required_consumer"], "tools/v7_sync_lib.continue_omp_engineering_control_loop")
            self.assertFalse(result["receipt"]["runtime_mutation_performed"])
            self.assertEqual(result["receipt"]["users_moved"], 0)

    def test_m2_repairs_interrupted_receipt_projection_without_second_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_key = "passive_m2_repair"
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "schema_version": "v7.l3-runtime-state.v1",
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key,
                        "incident_id": "sfinc_m2_repair",
                        "incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "next_required_consumer": "tools/v7_sync_lib.consume_service_failure_automation_frontier",
                        "reentry_condition": "ready obligation",
                        "transition_id": "ptr_m2_repair",
                    },
                },
            }), encoding="utf-8")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_m2_repair",
                "automation_obligation_id": "sfaob_m2_repair",
                "closure_state": "OMP_CONSUMED",
                "incident_key": incident_key,
                "source_incident_id": "sfinc_m2_repair",
                "next_action": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
                "consumed_at": "2026-07-27T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(receipt) + "\n", encoding="utf-8")

            result = self.sync.consume_service_failure_automation_frontier(state_dir=state_dir, persist_cps=False)
            self.assertEqual(result["final_verdict"], "NO_PENDING_OBLIGATION", result)
            self.assertEqual(result["incident_projection_reconciliation"]["changed_records"], 1)
            rows = [json.loads(line) for line in (state_dir / "closure-records.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 1)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["incidents"][incident_key]["omp_receipt_id"], "sfomp_m2_repair")

    def test_m2_legacy_receipt_cannot_consume_new_generation_by_source_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            incident_key = "passive_m2_strict"
            (state_dir / "l3-runtime-state.json").write_text(json.dumps({
                "schema_version": "v7.l3-runtime-state.v1",
                "incidents": {
                    incident_key: {
                        "incident_key": incident_key,
                        "incident_id": "sfinc_same_source",
                        "incident_state": "OPEN",
                        "authority_object": "PASSIVE_SERVICE_FAILURE_CAPTURE",
                        "situation_id": "situation_new_generation",
                        "decision_trace_id": "decision_new_generation",
                        "next_required_consumer": "tools/v7-users-autoswitch.materialize_service_failure_automation_advisory",
                        "reentry_condition": "fresh current generation",
                    },
                },
            }), encoding="utf-8")
            stale_receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_stale",
                "automation_obligation_id": "sfaob_stale",
                "closure_state": "OMP_CONSUMED",
                "source_incident_id": "sfinc_same_source",
                "situation_id": "situation_old_generation",
                "decision_trace_id": "decision_old_generation",
                "next_action": "HISTORICAL",
                "consumed_at": "2026-07-26T00:00:00+00:00",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(stale_receipt) + "\n", encoding="utf-8")

            result = self.sync.reconcile_service_failure_omp_receipts_to_incident_state(state_dir=state_dir)
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertEqual(result["changed_records"], 0)
            state = json.loads((state_dir / "l3-runtime-state.json").read_text(encoding="utf-8"))
            self.assertNotIn("omp_receipt_id", state["incidents"][incident_key])

    def test_existing_closure_owner_is_consumed_once_across_processes(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_cross_process",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-26T00:00:00+00:00",
                "source_incident_id": "sfinc_cross_process",
                "situation_id": "situation_cross_process",
                "decision_trace_id": "decision_cross_process",
                "stop_safe_classification": "STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")
            script = """
import importlib.machinery, importlib.util, json, sys
loader = importlib.machinery.SourceFileLoader('sync_child', sys.argv[1])
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = module.consume_service_failure_automation_frontier(state_dir=module.Path(sys.argv[2]), persist_cps=False)
print(json.dumps({'verdict': result.get('final_verdict')}))
"""
            processes = [
                subprocess.Popen(
                    [sys.executable, "-c", script, str(ROOT / "tools/v7_sync_lib.py"), str(state_dir)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                )
                for _ in range(4)
            ]
            verdicts = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=30)
                self.assertEqual(process.returncode, 0, stderr)
                verdicts.append(json.loads(stdout)["verdict"])
            self.assertEqual(verdicts.count("PASS"), 1)
            self.assertEqual(verdicts.count("NO_PENDING_OBLIGATION"), 3)

    def test_safe_service_failure_successor_materializes_event_driven_reentry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "egress/state"
            state_dir.mkdir(parents=True)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            obligation = {
                "object_type": "service_failure_automation_obligation",
                "automation_obligation_id": "sfaob_safe_successor",
                "closure_state": "READY_FOR_OMP_CONSUMPTION",
                "created_at": "2026-07-26T00:00:00+00:00",
                "source_incident_id": "sfinc_safe_successor",
                "situation_id": "situation_safe_successor",
                "decision_trace_id": "decision_safe_successor",
                "stop_safe_classification": "STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR",
            }
            (state_dir / "closure-records.jsonl").write_text(json.dumps(obligation) + "\n", encoding="utf-8")

            atomic_result = {
                "ok": True,
                "status": "ATOMIC_UPDATE_COMPLETE",
                "post_write_reread": "PASS",
                "external_wake": {"dispatch_required": True},
            }
            with mock.patch.object(
                self.sync, "atomic_reconcile_cps", return_value=atomic_result,
            ) as atomic:
                result = self.sync.consume_service_failure_automation_frontier(
                    root=root, state_dir=state_dir, persist_cps=True,
                )

            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertTrue(result["atomic_update"]["external_wake"]["dispatch_required"])
            self.assertEqual(result["next_output"], "V7_SERVICE_FAILURE_AUTOMATION_CALLER_REPAIR")
            self.assertTrue(atomic.call_args.kwargs["request_external_wake"])

    def test_exact_execution_outcome_is_compared_without_replaying_or_applying(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            state_dir.mkdir()
            decision = {
                "record_type": self.autoswitch.shadow_autonomy.DECISION_RECORD_TYPE,
                "decision_id": "shadow_exact",
                "source_incident_id": "sfinc_exact",
                "recommended_action": "MOVE_USER",
            }
            outcome = {
                "schema_version": "v7.execution-outcome-feedback.v1",
                "operation_id": "op_exact",
                "source_incident_id": "sfinc_exact",
                "outcome_status": "success",
                "verification_result": {"success": True},
            }
            (state_dir / "shadow-autonomy-decisions.jsonl").write_text(json.dumps(decision) + "\n", encoding="utf-8")
            (state_dir / "execution-events.jsonl").write_text(json.dumps(outcome) + "\n", encoding="utf-8")
            planner = object.__new__(self.autoswitch.AutoswitchPlanner)
            planner.state_dir = state_dir
            result = planner.reconcile_service_failure_shadow_outcomes()
            self.assertTrue(result["active"])
            rows = [json.loads(line) for line in (state_dir / "shadow-autonomy-decisions.jsonl").read_text(encoding="utf-8").splitlines()]
            comparison = rows[-1]
            self.assertEqual(comparison["record_type"], self.autoswitch.shadow_autonomy.OUTCOME_COMPARISON_RECORD_TYPE)
            self.assertTrue(comparison["prediction_matched_observed_outcome"])
            self.assertFalse(comparison["runtime_mutation_performed"])
            self.assertFalse(comparison["apply_executed"])

    def test_shadow_allowed_action_boundary_never_grants_execution(self):
        planner = object.__new__(self.autoswitch.AutoswitchPlanner)
        decisions = [{
            "user_ip": "10.0.0.2",
            "current_egress": "vless",
            "recommended_egress": "awg0",
        }]
        missing = planner._action_class_execution_boundary(
            decisions=decisions,
            selected=[],
            authority_budget_gate={"current_action_class_contract": {"valid": False, "blockers": ["contract_missing"]}},
            emergency_failover_gate={},
            restore_barrier_execution_gate={},
            intelligence_snapshot_gate={},
        )
        eligible = planner._action_class_execution_boundary(
            decisions=decisions,
            selected=[decisions[0]],
            authority_budget_gate={"current_action_class_contract": {"valid": True, "contract_id": "scoped"}},
            emergency_failover_gate={},
            restore_barrier_execution_gate={},
            intelligence_snapshot_gate={},
        )

        self.assertEqual(missing["status"], "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED")
        self.assertEqual(eligible["status"], "PACKET_MATERIALIZATION_ELIGIBLE")
        self.assertFalse(eligible["execution_authorized"])
        self.assertFalse(eligible["packet_created"])
        self.assertEqual(eligible["users_moved"], 0)

    def test_authority_stop_safe_emits_existing_policy_owner_request_without_grant(self):
        plan = {
            "operation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "certified_authority_class": "POOL",
                    "current_action_class_contract": {
                        "required": True,
                        "valid": False,
                        "blockers": ["current_action_class_contract_missing_or_schema_invalid"],
                    },
                },
                "l3_incident": {
                    "incident_id": "incident-1",
                    "incident_generation": "incident-generation-1",
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            policy_path.write_text("{}\n", encoding="utf-8")
            request = self.autoswitch.action_class_contract_reconciliation_request(
                plan, policy_path=policy_path,
            )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY")
        self.assertEqual(request["shadow_candidate"]["source_egress"], "vless")
        self.assertEqual(request["owner_issued_contract_template"]["max_users"], 1)
        self.assertEqual(request["owner_issued_contract_template"]["max_concurrent_transactions"], 1)
        self.assertTrue(request["authority_decision_request"]["request_id"])
        self.assertIn("existing /etc/v7/policy.json authority owner", request["next_consumer"])
        self.assertFalse(request["authority_granted"])
        self.assertFalse(request["contract_written"])
        self.assertFalse(request["runtime_apply"])
        self.assertEqual(request["users_moved"], 0)

    def test_restore_barrier_is_post_contract_gate_not_m5a_circular_blocker(self):
        plan = {
            "operation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "certified_authority_class": "POOL",
                    "current_action_class_contract": {
                        "required": True,
                        "valid": False,
                        "blockers": ["current_action_class_contract_missing_or_schema_invalid"],
                    },
                },
                "l3_wake": {"accepted": True, "blockers": []},
                "l3_incident": {
                    "incident_id": "incident-1",
                    "incident_generation": "incident-generation-1",
                },
                "emergency_failover_autonomy": {
                    "blockers": [
                        "no_selected_moves_for_emergency_failover",
                        "restore_barrier_required_for_emergency_failover",
                    ],
                },
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            policy_path.write_text("{}\n", encoding="utf-8")
            request = self.autoswitch.action_class_contract_reconciliation_request(
                plan, policy_path=policy_path,
            )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY")
        self.assertTrue(request["issue_preflight"]["ready"])
        self.assertEqual(
            request["pre_contract_execution_blockers"],
            [],
        )
        self.assertEqual(
            request["post_contract_operational_blockers"],
            ["restore_barrier_required_for_emergency_failover"],
        )
        self.assertNotIn("restore_barrier_required_for_emergency_failover", request["issue_preflight"]["blockers"])
        self.assertNotIn("no_selected_moves_for_emergency_failover", request["issue_preflight"]["blockers"])
        self.assertEqual(
            request["authority_classification"],
            "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
        )
        self.assertEqual(
            request["exact_legal_next_action"],
            "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST",
        )
        package = request["approval_package"]
        self.assertEqual(package["status"], "AWAITING_INDEPENDENT_AUTHORITY_DECISION")
        self.assertTrue(package["actionable"])
        self.assertTrue(package["request_id"])
        self.assertTrue(package["request_hash"])
        self.assertFalse(package["packet_identity"]["present"])
        self.assertEqual(package["packet_identity"]["packet_id"], "")
        self.assertEqual(package["scope"]["max_users"], 1)
        self.assertEqual(package["scope"]["max_concurrent_transactions"], 1)
        self.assertIn("restore_barrier_write", package["forbidden_effects"])
        self.assertFalse(request["authority_granted"])
        self.assertFalse(request["contract_written"])

    def test_valid_contract_reenters_packet_materialization_without_consumption(self):
        plan = {
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {"status": "PACKET_MATERIALIZATION_ELIGIBLE"},
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": True, "blockers": []},
                },
            },
        }
        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["authority_classification"], "SAFE_PACKET_MATERIALIZATION_PREDECESSOR_REQUIRED")
        self.assertEqual(request["exact_legal_next_action"], "REENTER_FRESH_PLANNER_FOR_PACKET_MATERIALIZATION")
        self.assertEqual(request["approval_package"]["status"], "SAFE_PACKET_MATERIALIZATION_PREDECESSOR_REQUIRED")
        self.assertFalse(request["approval_package"]["actionable"])
        self.assertFalse(request["packet_created"])
        self.assertFalse(request["lease_created"])
        self.assertFalse(request["contract_written"])

    def test_authority_request_waits_for_snapshot_revalidation_before_policy_owner(self):
        plan = {
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": False, "blockers": ["contract_missing"]},
                },
                "intelligence_snapshots": {
                    "stop_required": True,
                    "unsafe_blocker": "source_hash_mismatch:service_matrix",
                },
            },
        }
        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS")
        self.assertFalse(request["issue_preflight"]["ready"])
        self.assertIn("source_hash_mismatch:service_matrix", request["issue_preflight"]["blockers"])
        self.assertIn("v7-intelligence-snapshot-refresh", request["next_consumer"])
        self.assertFalse(request["authority_granted"])

    def test_authority_request_waits_for_current_l3_wake_before_policy_owner(self):
        plan = {
            "operation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "decisions": [{
                "user_ip": "10.0.0.2",
                "current_egress": "vless",
                "recommended_egress": "awg0",
            }],
            "safety": {
                "action_class_execution_boundary": {
                    "status": "STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED",
                },
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": False, "blockers": ["contract_missing"]},
                },
                "l3_incident": {
                    "incident_id": "incident-1",
                    "incident_generation": "incident-generation-1",
                },
                "l3_wake": {
                    "accepted": False,
                    "blockers": ["confirmed_l3_wake_required"],
                },
            },
        }

        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["status"], "ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS")
        self.assertFalse(request["issue_preflight"]["ready"])
        self.assertFalse(request["issue_preflight"]["l3_wake_accepted"])
        self.assertIn("confirmed_l3_wake_required", request["issue_preflight"]["blockers"])
        self.assertIn("action-class contract reconciliation", request["next_consumer"])

    def test_active_contract_reenters_existing_boundary_without_new_request(self):
        plan = {
            "decisions": [],
            "safety": {
                "action_class_execution_boundary": {"status": "NO_ACTION_NO_SHADOW_CANDIDATE"},
                "authority_budget_gate": {
                    "current_action_class_contract": {"required": True, "valid": True, "blockers": []},
                },
            },
        }
        request = self.autoswitch.action_class_contract_reconciliation_request(
            plan, policy_path=Path("/etc/v7/policy.json"),
        )

        self.assertEqual(request["status"], "CURRENT_ACTION_CLASS_CONTRACT_ACTIVE_REVALIDATE_EXISTING_CONSUMER")
        self.assertIn("action_class_execution_boundary", request["next_consumer"])
        self.assertFalse(request["contract_written"])

    def test_production_receipt_reconciles_source_cps_without_second_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_source_test",
                "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_source_test",
                "source_incident_id": "sfinc_source_test",
                "situation_id": "situation_source_test",
                "decision_trace_id": "decision_source_test",
                "classification": "STOP_SAFE_AUTHORITY_REQUIRED",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION",
                "next_action": "V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION",
                "runtime_mutation_performed": False,
                "routing_mutation_performed": False,
                "apply_executed": False,
                "authority_expanded": False,
                "production_maturity_changed": False,
                "users_moved": 0,
            }
            result = self.sync.reconcile_service_failure_automation_receipt_to_cps(receipt, root=root)
            self.assertEqual(result["final_verdict"], "PASS")
            self.assertEqual(result["receipt"]["object_id"], "sfomp_source_test")
            self.assertTrue(result["atomic_update"]["ok"])

    def test_historical_safe_receipt_cannot_replace_active_standing_policy_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path)
            text = cps_path.read_text(encoding="utf-8")
            for field, value in (
                ("ACTIVE_PROGRAM", "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"),
                ("CURRENT_AUTHORITY_REQUEST_STATUS", "ACTIVE_OWNER_BACKED_STANDING_POLICY"),
                ("CURRENT_NEXT_ACTION_ID", "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION"),
            ):
                text = self.sync._replace_section_field(
                    text, "## 0. Authoritative Live Current State",
                    "## Authoritative Unfinished Capability Closure Registry", field, f"`{value}`",
                )
            cps_path.write_text(text, encoding="utf-8")
            receipt = {
                "object_type": "service_failure_automation_omp_consumption",
                "object_id": "sfomp_historical_safe", "closure_state": "OMP_CONSUMED",
                "automation_obligation_id": "sfaob_historical_safe",
                "source_incident_id": "sfinc_historical_safe",
                "situation_id": "situation_historical_safe",
                "decision_trace_id": "decision_historical_safe",
                "classification": "CORRECT_SAFE_TERMINAL",
                "incident_frontier": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "product_evolution_frontier": "NONE",
                "next_action": "V7_SERVICE_FAILURE_AUTOMATION_INCIDENT_RECONCILIATION",
                "runtime_mutation_performed": False, "routing_mutation_performed": False,
                "apply_executed": False, "authority_expanded": False,
                "production_maturity_changed": False, "users_moved": 0,
            }
            result = self.sync.reconcile_service_failure_automation_receipt_to_cps(receipt, root=root)
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(result["status"], "HISTORICAL_RECEIPT_CONSUMED_ACTIVE_STANDING_POLICY_PRESERVED")
            live = self.sync._markdown_field_table(self.sync._markdown_section(
                cps_path.read_text(encoding="utf-8"), "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
            ))
            self.assertEqual(self.sync._plain_live_value(live, "CURRENT_NEXT_ACTION_ID"), "V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION")
            self.assertEqual(self.sync._plain_live_value(live, "LAST_SERVICE_FAILURE_RECEIPT_ID"), "sfomp_historical_safe")

    def test_fresh_m5a_request_is_atomically_projected_without_contract_or_packet(self):
        template = {
            "active_program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
            "action_class": "GOVERNED_ONLY",
            "max_authority_class": "CANARY",
            "authority_ceiling": "CANARY",
            "policy_generation_hash": "a" * 64,
            "subject": {"user_ip": "10.0.0.2"},
            "scope": {"source_egress": "vless", "target_egress": "awg0"},
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "incident_generation": {"incident_id": "incident-1", "incident_generation": "incident-generation-1"},
            "source_generation": {
                "planner_generation_id": "planner-generation-1",
                "source_bundle_hash": "source-bundle-1",
                "snapshot_bundle_hash": "snapshot-bundle-1",
                "selected_move_hash": "selected-move-1",
            },
            "verification_contract": {
                "owner": "tools/v7-users-autoswitch", "required": True,
                "immediate_and_temporal_observation": True, "success_criteria": "owner_verified",
            },
            "rollback_containment_contract": {
                "owner": "tools/v7-users-autoswitch", "required": True,
                "triggered_by_verifier": True, "direct_terminal_manufacture_forbidden": True,
            },
            "cooldown": {"required": True, "seconds": 180},
            "anti_flap": {"required": True, "same_source_target_repeat_forbidden": True},
            "stop_conditions": sorted(operator_execution.CURRENT_ACTION_CLASS_REQUIRED_STOP_CONDITIONS),
        }
        request = operator_execution.build_current_action_class_contract_authority_request(
            template, issue_preflight={"ready": True, "blockers": []},
        )
        package = {
            "schema_version": "v7.authority-normalized-approval-package.v1",
            "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION",
            "authority_classification": "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
            "actionable": True, "request_id": request["request_id"], "request_hash": request["request_hash"],
            "expires_at": request["expires_at"],
            "packet_identity": {"present": False, "packet_id": "", "packet_hash": ""},
            "forbidden_effects": [
                "contract_issuance", "policy_write", "restore_barrier_write", "candidate_creation",
                "execution_packet_or_lease_creation", "runtime_apply", "routing_mutation", "user_movement",
                "rollback_apply", "authority_expansion", "production_maturity_change",
            ],
        }
        reconciliation = {
            "schema_version": "v7.action-class-contract-reconciliation-request.v1",
            "status": "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY",
            "authority_classification": "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
            "exact_legal_next_action": "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST",
            "authority_decision_request": request, "approval_package": package,
            "authority_granted": False, "contract_written": False, "runtime_apply": False,
            "routing_mutation": False, "candidate_created": False, "packet_created": False,
            "lease_created": False, "users_moved": 0,
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/programs").mkdir(parents=True)
            cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
            shutil.copy2(ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md", cps_path)
            result = self.sync.reconcile_action_class_contract_request_to_cps(reconciliation, root=root)
            self.assertEqual(result["final_verdict"], "PASS", result)
            text = cps_path.read_text(encoding="utf-8")
            self.assertIn(f"| `CURRENT_AUTHORITY_REQUEST_ID` | `{request['request_id']}` |", text)
            self.assertIn("| `CURRENT_PACKET` | `NONE` |", text)
            self.assertIn("| `CURRENT_LEASE` | `NONE` |", text)
            self.assertFalse(result["contract_written"])
            self.assertFalse(result["packet_created"])

    def test_m5a_request_projection_rejects_changed_request_identity(self):
        rejected = self.sync.reconcile_action_class_contract_request_to_cps({
            "schema_version": "v7.action-class-contract-reconciliation-request.v1",
            "status": "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY",
            "authority_classification": "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY",
            "exact_legal_next_action": "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST",
            "authority_decision_request": {"request_id": "changed"},
            "approval_package": {"schema_version": "v7.authority-normalized-approval-package.v1"},
            "authority_granted": False, "contract_written": False, "runtime_apply": False,
            "routing_mutation": False, "candidate_created": False, "packet_created": False,
            "lease_created": False, "users_moved": 0,
        })
        self.assertEqual(rejected["final_verdict"], "STOP_SAFE")
        self.assertIn("current_action_class_contract_request_schema_invalid", rejected["errors"])

    def test_ct_m0f_validation_request_reuses_narrow_existing_authority_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.json"
            policy.write_text(json.dumps({
                "delegated_autonomy_policy": {
                    "contract_id": "sdpc_current",
                    "contract_hash": "a" * 64,
                },
            }), encoding="utf-8")
            audit = root / "audit.jsonl"
            args = self.autoswitch.build_arg_parser().parse_args([
                "--state-dir", str(root),
                "--policy-file", str(policy),
                "--action-class-audit-store", str(audit),
                "--prepare-ct-m0f-controlled-validation-authority-request",
                "--ct-m0f-controlled-validation-sample-kind", "cold",
            ])
            request = {
                "request_id": "ctm0fauth_r1_unit",
                "request_hash": "hash",
                "validation_generation_id": "ctm0fgen_unit",
                "reentry_condition": "exact decision",
            }
            with mock.patch.object(
                self.autoswitch.operator_execution,
                "validate_standing_delegated_operational_policy",
                return_value={"ok": True, "policy": {"max_users_per_action": 1}},
            ), mock.patch.object(
                self.autoswitch,
                "controlled_certification_pool_status",
                return_value={
                    "total_enabled_certification_users": 41,
                    "max_enabled_certification_users_on_one_active_source": 41,
                    "active_source_projections": [{
                        "source_id": "vless",
                        "enabled_certification_users_on_source": 41,
                    }],
                },
            ), mock.patch.object(
                self.autoswitch.operator_execution,
                "build_ct_m0f_controlled_validation_authority_request",
                return_value=request,
            ) as builder, mock.patch.object(
                self.autoswitch.operator_execution,
                "register_ct_m0f_controlled_validation_authority_request",
                return_value={"status": "REGISTERED", "audit_write": True},
            ):
                result = self.autoswitch.ct_m0f_controlled_validation_authority_request_only(args)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["authority_classification"], "ENGINEERING_AUTHORITY")
        self.assertEqual(builder.call_args.kwargs["source_id"], "vless")
        self.assertEqual(builder.call_args.kwargs["sample_kind"], "cold")
        self.assertEqual(result["forbidden_effects"]["user_movement"], 0)
        self.assertFalse(result["forbidden_effects"]["candidate_created"])
        self.assertFalse(result["forbidden_effects"]["authority_expansion"])


if __name__ == "__main__":
    unittest.main()
