"""Environment binding for the existing Authority owner's isolated lab scope.

Read-only admission checks, not a scheduler, registry, writer or health owner.
Host Docker inspection is a pre-fault input. Every later validation also reads
the actual local namespaces, network topology and resource limits; a copied
policy or a string claiming 'Polygon' is never sufficient.
"""

from __future__ import annotations

import hashlib
import ipaddress
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

from admin_core.registry_readers import parse_registry_lines


SCHEMA = "v7.ct-m0f-isolated-polygon-scope.v1"
IMPLEMENTATION_PATHS = (
    "admin_core/operator_execution.py", "admin_core/operator_execution_isolation.py",
    "admin_core/operator_execution_pipeline.py", "tools/v7-users-autoswitch",
    "tools/v7-governed-canary-dry-run-cycle", "tools/v7-service-matrix-refresh-all",
    "tools/v7-service-matrix-test", "tools/v7-egress-diagnose",
    "tools/runtime-support/v7-health-loop", "tools/runtime-support/v7-user-switch",
    "tools/runtime-support/v7-routing-sync", "tools/runtime-support/v7-egress-lib",
    "tools/v7-client-speed-api",
    "tools/runtime-support/v7-state-json", "tools/runtime-support/v7-state-json-save",
    "tools/v7-intelligence-snapshot-refresh",
)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def implementation_hashes():
    root = Path(__file__).resolve().parents[1]
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in IMPLEMENTATION_PATHS}


def external_default_route_present(routes):
    # Losing an isolated default route is an expected physical fault, not an
    # escape from the lab. Only an actual alternative external default denies
    # admission; reachability remains the Matrix owner's independent gate.
    return any(row.get("dev") not in {"pgsource", "pgtarget"} or row.get("gateway")
               for row in routes if row.get("dst") == "default")


def cold_capacity_observation_errors(observation, scope):
    """Validate signed pre-fault evidence, not create performance observations."""
    errors = []
    try:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(observation["observed_at"])).total_seconds()
        if not 0 <= age <= 120:
            errors.append("polygon_cold_observation_stale")
        if observation["completed_monotonic_ns"] <= 0 or not 0 <= time.monotonic_ns() - observation["completed_monotonic_ns"] <= 120_000_000_000:
            errors.append("polygon_cold_monotonic_observation_stale")
        if (observation.get("schema") != "v7.isolated-polygon-cold-capacity-observation.v1"
                or observation.get("owner") != "tools/v7-client-speed-api"
                or observation.get("network_namespace") != scope["environment"]["network_namespace"]
                or observation.get("cohort_members") != scope["members"]
                or observation.get("concurrent_streams") != len(scope["members"])
                or observation.get("payload_bytes_per_stream") != 1024 * 1024
                or observation.get("rounds_per_channel") != 3
                or observation.get("long_window_coverage") != {"5m": "NOT_OBSERVED", "1h": "NOT_OBSERVED"}):
            errors.append("polygon_cold_observation_binding_invalid")
        for channel in [scope["source_egress"], *scope["allowed_target_egresses"]]:
            rounds = observation["observations"][channel]["rounds"]
            if len(rounds) != 3:
                errors.append("polygon_cold_round_count_invalid")
            for row in rounds:
                samples = row["samples"]
                if (len(samples) != len(scope["members"])
                        or not 0 < row["completed_ns"] - row["started_ns"] <= 2_000_000_000
                        or row["memory_events_before"] != row["memory_events_after"]
                        or max(row["memory_before_bytes"], row["memory_after_bytes"]) >= scope["environment"]["memory_max"] * 0.85):
                    errors.append("polygon_cold_wave_or_resource_bound_failed")
                for sample in samples:
                    duration = sample["completed_ns"] - sample["started_ns"]
                    if (sample.get("ok") is not True or sample["bytes"] != 1024 * 1024
                            or not 0 < duration <= 2_000_000_000
                            or sample["bytes"] * 8000 / max(1, duration) < 10):
                        errors.append("polygon_cold_payload_or_throughput_failed")
                if samples and not max(sample["started_ns"] for sample in samples) < min(sample["completed_ns"] for sample in samples):
                    errors.append("polygon_cold_simultaneous_load_not_observed")
    except (KeyError, TypeError, ValueError, OverflowError):
        errors.append("polygon_cold_observation_malformed")
    return sorted(set(errors))


def kernel_environment():
    if not Path("/.dockerenv").is_file():
        raise ValueError("polygon_container_required")
    mounts = Path("/proc/self/mountinfo").read_text().splitlines()
    roots = [line for line in mounts if line.split()[4] == "/"]
    if len(roots) != 1 or roots[0].split(" - ")[1].split()[0] != "overlay":
        raise ValueError("polygon_disposable_root_required")
    links = json.loads(subprocess.run(
        ["ip", "-j", "-d", "link", "show"], check=True, capture_output=True, text=True, timeout=3,
    ).stdout)
    topology = {}
    for row in links:
        name = row.get("ifname")
        if name in {"eth0", "pgsource", "pgtarget"}:
            info = row.get("linkinfo", {})
            topology[name] = {key: row.get(key) for key in ("ifindex", "address")}
            topology[name]["kind"] = info.get("info_kind")
            if name != "eth0":
                topology[name]["tunnel"] = info.get("info_data", {})
    if topology.get("eth0", {}).get("kind") != "veth" or any(
        topology.get(name, {}).get("kind") != "gre" for name in ("pgsource", "pgtarget")
    ):
        raise ValueError("polygon_expected_virtual_paths_required")
    peers = {topology[name]["tunnel"].get("remote") for name in ("pgsource", "pgtarget")}
    if len(peers) != 1 or not ipaddress.ip_address(next(iter(peers))).is_private:
        raise ValueError("polygon_private_backend_required")
    routes = json.loads(subprocess.run(
        ["ip", "-j", "route", "show", "table", "main"], check=True, capture_output=True, text=True, timeout=3,
    ).stdout)
    if external_default_route_present(routes):
        raise ValueError("polygon_external_default_route_forbidden")
    memory = Path("/sys/fs/cgroup/memory.max").read_text().strip()
    quota, period = Path("/sys/fs/cgroup/cpu.max").read_text().split()
    if memory == "max" or quota == "max" or min(int(memory), int(quota), int(period)) <= 0:
        raise ValueError("polygon_bounded_resources_required")
    return {
        "network_namespace": os.readlink("/proc/self/ns/net"),
        "mount_namespace": os.readlink("/proc/self/ns/mnt"),
        "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
        "root_mount_fingerprint": fingerprint(roots[0]),
        "topology": topology,
        "memory_max": int(memory), "cpu_quota": int(quota), "cpu_period": int(period),
    }


def validate_scope(scope):
    errors = []
    if not isinstance(scope, dict) or scope.get("schema") != SCHEMA:
        return ["polygon_scope_schema_invalid"]
    try:
        actual = kernel_environment()
        if actual != scope.get("environment"):
            errors.append("polygon_current_environment_binding_changed")
        inspection = scope.get("docker_inspection", {})
        if (
            inspection.get("internal_network") is not True
            or inspection.get("container_count") != 2
            or inspection.get("host_mount_count") != 0
            or inspection.get("published_port_count") != 0
            or inspection.get("privileged") is not False
            or not inspection.get("network_id")
            or len(set(inspection.get("container_ids", []))) != 2
        ):
            errors.append("polygon_host_isolation_preflight_invalid")
        if inspection.get("router_memory") != actual["memory_max"]:
            errors.append("polygon_resource_binding_changed")
        if implementation_hashes() != scope.get("implementation_hashes"):
            errors.append("polygon_implementation_changed")
        members = scope.get("members", [])
        if not members or members != sorted(set(members)) or any(
            ipaddress.ip_address(member) not in ipaddress.ip_network("10.7.0.0/16") for member in members
        ):
            errors.append("polygon_exact_lab_members_required")
        state = Path(scope.get("state_dir", "")).resolve()
        if state != Path("/polygon/state") or not state.is_dir():
            errors.append("polygon_exact_state_root_required")
        else:
            users = parse_registry_lines((state / "users.registry").read_text().splitlines())
            if sorted(row.get("ip", "") for row in users) != members or any(
                row.get("certification_user") != "1" or row.get("enabled") != "1" for row in users
            ):
                errors.append("polygon_live_subjects_changed_or_ordinary_present")
            source = scope.get("source_egress")
            targets = scope.get("allowed_target_egresses", [])
            if not source or not targets or source in targets or len(targets) != len(set(targets)):
                errors.append("polygon_distinct_target_scope_required")
            if any(row.get("current") not in [source, *targets] for row in users):
                errors.append("polygon_assignment_outside_bound_scope")
            if {row.get("ip"): row.get("table") for row in users} != scope.get("member_tables"):
                errors.append("polygon_member_route_binding_changed")
            egress = (state / "egress.registry").read_bytes()
            if hashlib.sha256(egress).hexdigest() != scope.get("egress_registry_hash"):
                errors.append("polygon_egress_contract_changed")
            channels = {row.get("id"): row for row in parse_registry_lines(egress.decode().splitlines())}
            if channels.get(source, {}).get("interface") != "pgsource" or any(
                channels.get(target, {}).get("interface") != "pgtarget" for target in targets
            ):
                errors.append("polygon_registry_kernel_path_binding_invalid")
        if not scope.get("required_services") or scope.get("max_cohort_members") != len(members):
            errors.append("polygon_service_or_cohort_contract_invalid")
        if scope.get("max_concurrent_transactions") != 1:
            errors.append("polygon_parallel_transactions_not_yet_admitted")
        if scope.get("rollback_required") is not True:
            errors.append("polygon_rollback_required")
        if scope.get("cold_capacity_observation_hash"):
            payload = (state / "polygon-cold-capacity-observation.json").read_bytes()
            if hashlib.sha256(payload).hexdigest() != scope["cold_capacity_observation_hash"]:
                errors.append("polygon_cold_observation_hash_changed")
            else:
                errors.extend(cold_capacity_observation_errors(json.loads(payload), scope))
    except ValueError as exc:
        # Stable guard names make a real post-fault admission failure
        # diagnosable without publishing subprocess output or local paths.
        reason = str(exc)
        errors.append(reason if reason.startswith("polygon_") else "polygon_current_environment_value_invalid")
    except (OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        errors.append("polygon_current_environment_unavailable:" + type(exc).__name__)
    return sorted(set(errors))


def capture_scope(*, state_dir, docker_inspection, required_services):
    state = Path(state_dir).resolve()
    users = parse_registry_lines((state / "users.registry").read_text().splitlines())
    members = sorted(row.get("ip", "") for row in users)
    sources = {row.get("current") for row in users}
    if len(sources) != 1:
        raise ValueError("polygon_single_initial_source_required")
    source = next(iter(sources))
    egress = parse_registry_lines((state / "egress.registry").read_text().splitlines())
    targets = sorted(row["id"] for row in egress if row.get("enabled") == "1" and row.get("id") != source)
    matrix_bytes = (state / "service-matrix.json").read_bytes()
    matrix = json.loads(matrix_bytes)
    for channel in [source, *targets]:
        services = matrix.get("items", {}).get(channel, {}).get("services", {})
        if not required_services or any(services.get(service, {}).get("ok") is not True for service in required_services):
            raise ValueError("polygon_owner_backed_service_baseline_required")
    scope = {
        "schema": SCHEMA, "state_dir": str(state), "members": members,
        "environment": kernel_environment(), "docker_inspection": docker_inspection,
        "implementation_hashes": implementation_hashes(),
        "source_egress": source,
        "allowed_target_egresses": targets,
        "pre_fault_matrix_hash": hashlib.sha256(matrix_bytes).hexdigest(),
        "member_tables": {row.get("ip"): row.get("table") for row in users},
        "egress_registry_hash": hashlib.sha256((state / "egress.registry").read_bytes()).hexdigest(),
        "required_services": sorted(set(required_services)), "max_cohort_members": len(members),
        "max_concurrent_transactions": 1, "rollback_required": True,
    }
    errors = validate_scope(scope)
    if errors:
        raise ValueError(",".join(errors))
    return scope
