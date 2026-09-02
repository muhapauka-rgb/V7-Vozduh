"""N9 scale/resource tournament for the current role-based health model.

This is an Engineering/Polygon harness.  It imports existing owners and writes
only temporary fixtures; it is not a Runtime owner, scheduler or state source.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import math
import resource
import socket
import subprocess
import tempfile
import time
import tracemalloc
import unittest
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUTOSWITCH = ROOT / "tools" / "v7-users-autoswitch"
HARD_OWNER = ROOT / "tools" / "v7-egress-diagnose"

SERVICES = (
    "telegram", "google", "google_auth", "youtube", "instagram",
    "facebook", "chatgpt", "openai_auth", "claude", "anthropic",
    "apple", "whatsapp", "spotify", "soundcloud",
)
PROFILE_PATTERNS = {
    "one": ((),),
    "few": ((), ("telegram",), ("google", "youtube")),
    "many": (
        (), ("telegram",), ("google",), ("youtube",),
        ("google_auth",), ("instagram",), ("chatgpt", "openai_auth"),
        ("claude", "anthropic"), ("apple", "whatsapp"),
        ("spotify", "soundcloud"),
    ),
}


def load_tool(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def generation() -> dict[str, Any]:
    return {
        "planner_generation_id": "n9-planner-generation",
        "inputs": {
            "users_registry": "n9-users", "egress_registry": "n9-egress",
            "policy": "n9-policy", "org_policy": "n9-org",
            "service_preferences": "n9-profiles",
        },
        "volatile_inputs": {
            "service_matrix": "n9-matrix", "egress_speed": "n9-capacity",
            "autoswitch_safety": "n9-safety",
        },
    }


def build_case(egress_count: int, user_count: int, shape: str) -> tuple[dict[str, Any], dict[str, Any]]:
    patterns = PROFILE_PATTERNS[shape]
    active = min(egress_count, user_count)
    candidates = [
        {
            "egress": f"hot-{index}", "eligible": True,
            "score": 100.0 - index, "role": "GLOBAL_FAST",
            "capacity_decision": {"status": "AVAILABLE"},
            "canary_reserved": False,
        }
        for index in range(4)
    ]
    decisions = []
    contracts: set[tuple[str, tuple[str, ...]]] = set()
    for index in range(user_count):
        source_index = index % active
        # Rotate profiles by complete source rounds so the many-profile case
        # gives every sufficiently populated source multiple contracts.
        services = patterns[(index // active) % len(patterns)]
        source = f"source-{source_index}"
        contracts.add((source, tuple(services)))
        decisions.append({
            "user_ip": f"synthetic-{index}",
            "current_egress": source,
            "recommended_egress": "hot-0",
            "important_services": list(services),
            "candidates": candidates,
        })
    plan = {
        "updated": "2026-08-23T17:30:00+00:00",
        "operation": {"operation_id": ""},
        "safety": {"generation": generation()},
        "decisions": decisions,
    }
    return plan, {
        "inventory_egresses": egress_count,
        "active_egresses": active,
        "users": user_count,
        "profile_shape": shape,
        "distinct_source_profile_contracts": len(contracts),
        "contracts": contracts,
    }


def budget_for(case: dict[str, Any], projection: dict[str, Any]) -> dict[str, Any]:
    contracts = case["contracts"]
    active = int(case["active_egresses"])
    inventory = int(case["inventory_egresses"])
    telegram_sources = {
        source for source, services in contracts if "telegram" in services
    }
    other_probe_count_per_pass = sum(
        len([service for service in services if service != "telegram"])
        for _source, services in contracts
    )
    hot_contracts = list(
        ((projection.get("hot_target_set") or {}).get("contracts") or [])
    )
    hot_targets = {str(row.get("target_id") or "") for row in hot_contracts}
    hot_telegram_targets = {
        str(row.get("target_id") or "") for row in hot_contracts
        if "telegram" in set(row.get("critical_services") or [])
    }
    hot_other_by_target: dict[str, set[str]] = {}
    for row in hot_contracts:
        target = str(row.get("target_id") or "")
        hot_other_by_target.setdefault(target, set()).update(
            service for service in (row.get("critical_services") or [])
            if service != "telegram"
        )
    deep_probes_per_sec = inventory * len(SERVICES) / 900.0
    other_timeout_bound_seconds = (
        math.ceil(other_probe_count_per_pass / 128) * 0.5
        if other_probe_count_per_pass else 0.0
    )
    other_fast_capacity_admitted = other_timeout_bound_seconds <= 5.0
    admitted_other_probes_per_sec = (
        other_probe_count_per_pass / 5.0 if other_fast_capacity_admitted else 0.0
    )
    source_network_probes_per_sec = (
        len(telegram_sources) + admitted_other_probes_per_sec
    )
    hot_network_probes_per_sec = (
        len(hot_telegram_targets)
        + sum(len(values) for values in hot_other_by_target.values()) / 5.0
    )
    network_probes_per_sec = (
        source_network_probes_per_sec + hot_network_probes_per_sec
        + deep_probes_per_sec
    )
    # Conservative traffic envelope for bounded DNS/TCP/TLS/light-HTTP
    # checks.  It is a modeled upper bound, not packet-capture evidence.
    bytes_per_sec_upper_bound = (
        (source_network_probes_per_sec + hot_network_probes_per_sec) * 4096
        + deep_probes_per_sec * 16384
    )
    deep_writes_per_sec = inventory / 900.0
    matrix_writes_per_sec_upper_bound = (
        1.0  # one batched Telegram Matrix update
        + 1.0  # one batched prepared PATH update
        + len(hot_targets) / 5.0  # bounded other-service target rows
        + deep_writes_per_sec
    )
    return {
        "hard_local_observations_per_sec": active,
        "source_network_probes_per_sec": round(source_network_probes_per_sec, 3),
        "other_required_probe_count_per_pass": other_probe_count_per_pass,
        "other_required_timeout_bound_seconds": round(other_timeout_bound_seconds, 3),
        "other_required_fast_capacity_admitted": other_fast_capacity_admitted,
        "other_required_fallback": (
            "NONE" if other_fast_capacity_admitted
            else "EXISTING_STAGGERED_DEEP_FULL_MATRIX"
        ),
        "hot_network_probes_per_sec": round(hot_network_probes_per_sec, 3),
        "deep_network_probes_per_sec": round(deep_probes_per_sec, 3),
        "network_probes_per_sec": round(network_probes_per_sec, 3),
        "bytes_per_sec_upper_bound": round(bytes_per_sec_upper_bound),
        "runtime_role_process_starts_per_sec_upper_bound": round(
            1 + 1 + 1 + 1 / 5 + 1 / 5 + 1 / 30 + 1 / 60
            + len(hot_targets) / 5 + deep_writes_per_sec,
            3,
        ),
        "socket_concurrency_cap": 128,
        "prepared_path_concurrency_cap": 16,
        "deep_concurrency_cap": 16,
        "matrix_writes_per_sec_upper_bound": round(
            matrix_writes_per_sec_upper_bound, 3,
        ),
        "matrix_lock_acquisitions_per_sec_upper_bound": round(
            matrix_writes_per_sec_upper_bound, 3,
        ),
        "endpoint_pressure": {
            "telegram_rotating_per_source_per_sec": len(telegram_sources),
            "other_required_timeout_ms": 500,
            "deep_full_horizon_seconds": 900,
            "full_14_service_every_second_forbidden": True,
        },
    }


def measure_projection(autoswitch: Any, egress_count: int, user_count: int, shape: str) -> dict[str, Any]:
    plan, case = build_case(egress_count, user_count, shape)
    before = resource.getrusage(resource.RUSAGE_SELF)
    tracemalloc.start()
    started = time.perf_counter()
    projection = autoswitch.build_prepared_class_decision_projection(plan)
    wall_ms = (time.perf_counter() - started) * 1000.0
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    after = resource.getrusage(resource.RUSAGE_SELF)
    encoded = json.dumps(projection, ensure_ascii=True, separators=(",", ":")).encode()
    return {
        **{key: value for key, value in case.items() if key != "contracts"},
        "prepared_class_count": int(projection.get("class_count") or 0),
        "prepared_hot_contract_count": int(
            (projection.get("hot_target_set") or {}).get(
                "deduplicated_target_service_contract_count"
            ) or 0
        ),
        "projection_bytes": len(encoded),
        "projection_wall_ms": round(wall_ms, 3),
        "projection_user_cpu_ms": round(
            (after.ru_utime - before.ru_utime) * 1000.0, 3,
        ),
        "projection_system_cpu_ms": round(
            (after.ru_stime - before.ru_stime) * 1000.0, 3,
        ),
        "projection_peak_allocated_bytes": int(peak),
        "budget": budget_for(case, projection),
    }


def measure_hard_owner(active_egresses: int, users: int) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        state = Path(tmp)
        interface_names = {name for _index, name in socket.if_nameindex()}
        loopback = "lo0" if "lo0" in interface_names else "lo"
        (state / "egress.registry").write_text("".join(
            f"id=source-{index} interface={loopback} enabled=1 role=GLOBAL_FAST\n"
            for index in range(active_egresses)
        ), encoding="utf-8")
        (state / "users.registry").write_text("".join(
            f"ip=synthetic-{index} current=source-{index % active_egresses} enabled=1\n"
            for index in range(users)
        ), encoding="utf-8")
        output = state / "hard.state"
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        started = time.perf_counter()
        proc = subprocess.run([
            str(HARD_OWNER), "--state-dir", str(state), "--output", str(output),
            "--hard-signal-only", "--definitive-matrix-command", "/bin/false",
        ], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            check=False, timeout=20)
        wall_ms = (time.perf_counter() - started) * 1000.0
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        values = {}
        for line in output.read_text(encoding="utf-8").splitlines() if output.exists() else []:
            key, sep, value = line.partition("=")
            if sep:
                values[key] = value
    return {
        "active_egresses": active_egresses,
        "users": users,
        "returncode": proc.returncode,
        "wall_ms": round(wall_ms, 3),
        "child_user_cpu_ms": round((after.ru_utime - before.ru_utime) * 1000.0, 3),
        "child_system_cpu_ms": round((after.ru_stime - before.ru_stime) * 1000.0, 3),
        "max_rss_kib": int(after.ru_maxrss),
        "active_source_count": int(values.get("hard_signal_active_source_count") or 0),
        "observations": int(values.get("hard_signal_observation_count") or 0),
        "deadline_miss": wall_ms > 1000.0,
    }


def measure_disjoint_source_preparation(
    autoswitch: Any, source_count: int,
) -> dict[str, Any]:
    """Exercise existing Planner preparation on disjoint Polygon source pairs.

    This is intentionally planning-only.  It proves that independent source /
    target preparation does not require a shared fixture lock; the existing
    governed Apply, Core-primary and route writer are not imported or invoked.
    """
    plan, _case = build_case(source_count, source_count * 10, "many")
    by_source: dict[str, list[dict[str, Any]]] = {}
    for decision in plan["decisions"]:
        by_source.setdefault(str(decision["current_egress"]), []).append(decision)

    def prepare(item: tuple[str, list[dict[str, Any]]]) -> tuple[str, str, str]:
        source, decisions = item
        index = int(source.rsplit("-", 1)[1])
        target = f"target-{index}"
        local = deepcopy(plan)
        local["decisions"] = deepcopy(decisions)
        for decision in local["decisions"]:
            decision["recommended_egress"] = target
            decision["candidates"] = [{
                "egress": target, "eligible": True, "score": 100.0,
                "role": "GLOBAL_FAST",
                "capacity_decision": {"status": "AVAILABLE"},
                "canary_reserved": False,
            }]
        projection = autoswitch.build_prepared_class_decision_projection(local)
        encoded = json.dumps(projection, sort_keys=True, separators=(",", ":"))
        return source, target, encoded

    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=min(16, source_count)) as pool:
        rows = list(pool.map(prepare, sorted(by_source.items())))
    wall_ms = (time.perf_counter() - started) * 1000.0
    return {
        "source_count": source_count,
        "completion_count": len(rows),
        "unique_sources": len({source for source, _target, _encoded in rows}),
        "unique_targets": len({target for _source, target, _encoded in rows}),
        "stable_result_count": len({encoded for _source, _target, encoded in rows}),
        "wall_ms": round(wall_ms, 3),
        "execution": "PREPARATION_ONLY_NO_APPLY_CORE_PRIMARY_OR_ROUTE_WRITER",
    }


class V53N9FullScaleTournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.autoswitch = load_tool("v7_autoswitch_n9_scale", AUTOSWITCH)

    def test_mandatory_scale_grid_preserves_health_cost_law(self):
        # Recovery-scale law is expressed as the operational 10/50/100/1000
        # grid.  Keep this test aligned with that canonical grid rather than
        # leaving an unrelated historical seven-egress sample in its place.
        for egresses in (10, 50, 100, 1000):
            for users in (250, 500, 10_000):
                for shape in ("one", "few", "many"):
                    with self.subTest(egresses=egresses, users=users, shape=shape):
                        plan, case = build_case(egresses, users, shape)
                        projection = self.autoswitch.build_prepared_class_decision_projection(plan)
                        budget = budget_for(case, projection)
                        self.assertLessEqual(
                            case["distinct_source_profile_contracts"],
                            case["active_egresses"] * len(PROFILE_PATTERNS[shape]),
                        )
                        self.assertLessEqual(
                            projection["hot_target_set"]["deduplicated_target_service_contract_count"],
                            4 * len(PROFILE_PATTERNS[shape]),
                        )
                        self.assertLess(
                            budget["network_probes_per_sec"],
                            egresses * len(SERVICES),
                        )
                        self.assertLessEqual(budget["socket_concurrency_cap"], 128)

    def test_ten_thousand_users_one_source_one_profile_is_one_contract(self):
        _plan, case = build_case(1, 10_000, "one")
        self.assertEqual(case["distinct_source_profile_contracts"], 1)

    def test_worst_shape_projection_is_bounded_and_compact(self):
        result = measure_projection(self.autoswitch, 1000, 10_000, "many")
        self.assertEqual(result["prepared_class_count"], 10_000)
        self.assertLessEqual(result["prepared_hot_contract_count"], 40)
        self.assertLess(result["projection_bytes"], 15_000_000)
        self.assertLess(result["projection_peak_allocated_bytes"], 256_000_000)
        self.assertFalse(result["budget"]["other_required_fast_capacity_admitted"])
        self.assertEqual(
            result["budget"]["other_required_fallback"],
            "EXISTING_STAGGERED_DEEP_FULL_MATRIX",
        )

    def test_hard_owner_meets_one_second_at_1000_active_egresses(self):
        result = measure_hard_owner(1000, 10_000)
        self.assertEqual(result["returncode"], 0, result)
        self.assertEqual(result["active_source_count"], 1000)
        self.assertEqual(result["observations"], 0)
        self.assertFalse(result["deadline_miss"], result)

    def test_disjoint_source_preparation_is_fair_at_recovery_scale_grid(self):
        # The current Program permits only source-local preparation in Polygon
        # when source/target/write sets are disjoint.  This fixture creates one
        # isolated target per source; it deliberately makes no Apply claim.
        for sources in (10, 50, 100):
            with self.subTest(sources=sources):
                result = measure_disjoint_source_preparation(self.autoswitch, sources)
                self.assertEqual(result["completion_count"], sources, result)
                self.assertEqual(result["unique_sources"], sources, result)
                self.assertEqual(result["unique_targets"], sources, result)
                self.assertEqual(result["stable_result_count"], sources, result)
                self.assertEqual(
                    result["execution"],
                    "PREPARATION_ONLY_NO_APPLY_CORE_PRIMARY_OR_ROUTE_WRITER",
                )

    def test_prepared_projection_reuses_stable_selection_but_not_changed_membership(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            policy = root / "policy.json"
            org_policy = root / "org-policy.json"
            safety = state / "autoswitch-safety.json"
            for path, value in (
                (state / "users.registry", "ip=synthetic-0 current=source-0 enabled=1\n"),
                (state / "egress.registry", "id=source-0 interface=lo enabled=1\n"),
                (state / "service-preferences.json", "{}\n"),
                (state / "egress-speed.json", "{}\n"),
                (state / "service-matrix.json", "{}\n"),
                (policy, "{}\n"), (org_policy, "{}\n"), (safety, "{}\n"),
            ):
                path.write_text(value, encoding="utf-8")
            args = SimpleNamespace(
                state_dir=str(state), policy_file=str(policy),
                org_policy_file=str(org_policy), safety_file=str(safety),
            )
            plan, _case = build_case(1, 1, "one")
            projection = self.autoswitch.build_prepared_class_decision_projection(plan)
            projection["produced_at"] = self.autoswitch.now_iso()
            projection["invalidators"].update(
                self.autoswitch.current_prepared_selection_invalidators(args)
            )
            (state / "service-matrix-refresh-summary.json").write_text(
                json.dumps({"prepared_class_decisions": projection}),
                encoding="utf-8",
            )

            first = self.autoswitch.reuse_current_prepared_class_projection(args)
            self.assertTrue(first["ok"], first)
            (state / "service-matrix.json").write_text('{"generation": 2}\n', encoding="utf-8")
            after_observation = self.autoswitch.reuse_current_prepared_class_projection(args)
            self.assertTrue(after_observation["ok"], after_observation)
            self.assertFalse(after_observation["matrix_observation_invalidates_selection"])

            (state / "users.registry").write_text(
                "ip=synthetic-0 current=source-0 enabled=1\n"
                "ip=synthetic-1 current=source-0 enabled=1\n",
                encoding="utf-8",
            )
            changed = self.autoswitch.reuse_current_prepared_class_projection(args)
            self.assertFalse(changed["ok"], changed)
            self.assertIn(
                "selection_input_changed:membership_generation", changed["blockers"],
            )


if __name__ == "__main__":
    unittest.main()
