"""Disposable Linux substrate for the existing OMP Polygon owner.

This module supplies topology and starting fixtures, never recovery decisions,
Matrix events, execution receipts or S11. The current probe stops at the real
health/Matrix boundary and explicitly cannot satisfy full-E2E acceptance.
No host mounts, published ports, Docker socket or production state are used.
"""

from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import uuid


def command(argv, *, timeout=60):
    result = subprocess.run(argv, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{argv[:3]} exited {result.returncode}: {result.stderr[-2000:]}")
    return result


def traffic_probe(interface):
    checked = subprocess.run([
        "curl", "--interface", interface, "--connect-timeout", "1", "--max-time", "2",
        "-fsS", "-o", "/dev/null", "-w", "%{http_code}", "https://www.google.com/generate_204",
    ], text=True, capture_output=True, timeout=4)
    return {"interface": interface, "returncode": checked.returncode, "http_code": checked.stdout,
            "ok": checked.returncode == 0 and checked.stdout == "204"}


def inside_probe(*, traffic=False):
    # Host-side creation separately verifies Docker namespace and mount scope.
    if not Path("/.dockerenv").is_file() or (not traffic and Path("/sys/class/net/eth0").exists()):
        raise RuntimeError("isolated_network_none_container_required")
    state = Path("/polygon/state")
    events = Path("/polygon/events")
    state.mkdir()
    events.mkdir()
    # Deterministic lab-only starting identities. No production registry copy.
    (state / "users.registry").write_text("".join(
        f"ip=198.18.0.{i} current=polygon-source enabled=1 certification_user=1 "
        f"certification_group=isolated-runtime table={1000+i}\n"
        for i in range(1, 6)
    ))
    (state / "egress.registry").write_text(
        "id=polygon-source interface=pgsource enabled=1 type=interface protocol=gre\n"
        + ("id=polygon-target interface=pgtarget enabled=1 type=interface protocol=gre\n" if traffic else "")
    )
    if not traffic:
        command(["ip", "link", "add", "pgsource", "type", "dummy"])
        command(["ip", "link", "set", "pgsource", "up"])
    matrix = state / "service-matrix.json"
    # Empty initial state is not fabricated healthy/failed Matrix evidence.
    matrix.write_text('{"items":{}}\n')
    baseline_services = {}
    client_baseline = []
    fault_traffic = []
    target_during_fault = {}
    if traffic:
        for egress in ("polygon-source", "polygon-target"):
            probe = command([sys.executable, "/polygon/tools/v7-service-matrix-test",
                             egress, "all", "--state-dir", str(state), "--event-dir", str(events)], timeout=45)
            baseline_services[egress] = json.loads(probe.stdout)
            results = baseline_services[egress].get("results", {})
            if not results or not all(row.get("ok") is True for row in results.values()):
                raise RuntimeError("required_service_baseline_failed:" + probe.stdout[-3000:])
        with ThreadPoolExecutor(max_workers=5) as workers:
            client_baseline = list(workers.map(traffic_probe, [f"198.18.0.{i}" for i in range(1, 6)]))
        if not all(row["ok"] for row in client_baseline):
            raise RuntimeError("client_source_route_baseline_failed:" + json.dumps(client_baseline))
    args = [
        sys.executable, "/polygon/tools/runtime-support/v7-health-loop",
        "--role-based-fast", "--max-phases", "12",
        "--controlled-owner-root", "/polygon/tools",
        "--controlled-matrix-state-file", str(matrix),
        "--controlled-users-registry-file", str(state / "users.registry"),
        "--controlled-event-dir", str(events),
    ]
    # HARD detection is real. Other roles are explicitly out of this probe's
    # scope, not fake successful service probes or an E2E baseline.
    for role in ("hard", "telegram", "hot-target", "hot-target-other", "required", "planner-projection", "deep"):
        args.extend([f"--controlled-{role}-command", "/bin/true"])
    output_path = Path("/polygon/health.log")
    fault_ns = None
    row = {}
    with output_path.open("w") as output:
        process = subprocess.Popen(args, stdout=output, stderr=subprocess.STDOUT)
        try:
            # Wait for a completed healthy HARD cycle, not a sleep-based guess
            # about health readiness. Do not create or inject its observation.
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                log = output_path.read_text()
                if "V7_HEALTH_ROLE_COMPLETE role=hard" in log:
                    break
                if process.poll() is not None:
                    raise RuntimeError("health_exited_before_baseline:" + log[-2000:])
                time.sleep(0.02)
            else:
                raise RuntimeError("health_baseline_not_observed:" + output_path.read_text()[-2000:])
            if not traffic and json.loads(matrix.read_text()).get("items"):
                raise RuntimeError("unexpected_pre_fault_matrix_observation")
            fault_ns = time.monotonic_ns()
            command(["ip", "link", "set", "pgsource", "down"])
            fault_completed_ns = time.monotonic_ns()
            if traffic:
                with ThreadPoolExecutor(max_workers=5) as workers:
                    fault_traffic = list(workers.map(traffic_probe, [f"198.18.0.{i}" for i in range(1, 6)]))
                target_during_fault = traffic_probe("pgtarget")
                if any(row["ok"] for row in fault_traffic) or not target_during_fault["ok"]:
                    raise RuntimeError("source_fault_or_target_path_not_isolated")
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                data = json.loads(matrix.read_text())
                row = data.get("items", {}).get("polygon-source", {}).get("services", {}).get("__channel_liveness__", {})
                if row.get("ok") is False and row.get("failure_event_id") and (
                    not traffic or "V7_HEALTH_RECOVERY_CONSUMER_RECEIPT" in output_path.read_text()
                ):
                    break
                if process.poll() is not None:
                    break
                time.sleep(0.02)
            observed_ns = time.monotonic_ns()
        finally:
            # Restoration is teardown, never described as V7 failover/S11.
            command(["ip", "link", "set", "pgsource", "up"])
            try:
                process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                process.terminate()
                process.wait(timeout=5)
    log = output_path.read_text()
    event_rows = []
    for path in sorted(events.glob("*.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                event_rows.append(json.loads(line))
    return {
        "schema": "v7.polygon-real-health-matrix-probe.v1",
        "evidence_class": "PARTIAL_REAL_HEALTH_MATRIX_NOT_E2E",
        "physical_fault": "ip link set pgsource down",
        "physical_fault_dispatch_monotonic_ns": fault_ns,
        "physical_fault_command_completed_monotonic_ns": fault_completed_ns,
        "matrix_observed_by_harness_monotonic_ns": observed_ns,
        "observation_upper_bound_ms": round((observed_ns - fault_ns) / 1e6, 3),
        "matrix_failure_row": row,
        "events": event_rows,
        "health_log": log,
        "health_returncode": process.returncode,
        "baseline_services": baseline_services,
        "client_source_route_baseline": client_baseline,
        "client_traffic_during_source_fault": fault_traffic,
        "target_traffic_during_source_fault": target_during_fault,
        "full_e2e_proven": False,
        "required_service_s11_proven": False,
        "scale_proven": False,
        "missing_path": "fresh target/Authority -> Planner -> Packet/Lease/Barrier -> writer -> all-member S11",
    }


def execute(root: Path, *, traffic=False):
    """Called by the existing Polygon owner; creates only exact owned objects."""
    docker = shutil.which("docker")
    if not docker:
        raise RuntimeError("docker_unavailable")
    identity = "v7-pg-runtime-" + uuid.uuid4().hex[:12]
    image = identity + ":probe"
    label = "v7.polygon.runtime=" + identity
    created = False
    backend_created = False
    network_created = False
    backend = identity + "-backend"
    network = identity + "-net"
    result = {}
    owner_paths = ("tools/runtime-support/v7-health-loop", "tools/v7-egress-diagnose", "tools/v7-service-matrix-test", "tools/v7-service-matrix-refresh-all", "tools/v7-users-autoswitch")
    hashes = {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in owner_paths}
    try:
        with tempfile.TemporaryDirectory(prefix="v7-polygon-runtime-") as tmp:
            context = Path(tmp)
            for folder in ("tools", "admin_core"):
                shutil.copytree(root / folder, context / folder, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (context / "Dockerfile").write_text(
                "FROM python:3.11-slim\n"
                "RUN apt-get update && apt-get install -y --no-install-recommends iproute2 curl jq procps util-linux openssl ca-certificates iptables && rm -rf /var/lib/apt/lists/*\n"
                "COPY tools /polygon/tools\nCOPY admin_core /polygon/admin_core\n"
                "ENV PYTHONPATH=/polygon PYTHONDONTWRITEBYTECODE=1\n"
            )
            command([docker, "build", "-q", "-t", image, str(context)], timeout=300)
        if traffic:
            command([docker, "network", "create", "--internal", "--label", label, network])
            network_created = True
            if not json.loads(command([docker, "network", "inspect", network]).stdout)[0]["Internal"]:
                raise RuntimeError("external_network_forbidden")
        container_limits = ["--network", network if traffic else "none", "--cap-drop", "ALL", "--cap-add", "NET_ADMIN",
                 "--security-opt", "no-new-privileges", "--memory", "512m", "--cpus", "2",
                 "--pids-limit", "128"]
        command([docker, "create", "--name", identity, "--label", label, *container_limits,
                 image, *(["sleep", "120"] if traffic else ["python3", "/polygon/tools/polygon/runtime_chain.py", "--inside"])])
        created = True
        inspection = json.loads(command([docker, "inspect", identity]).stdout)[0]
        config = inspection["HostConfig"]
        if inspection.get("Mounts") or config["NetworkMode"] != (network if traffic else "none") or config["Privileged"] or config.get("PortBindings"):
            raise RuntimeError("container_isolation_verification_failed")
        if traffic:
            command([docker, "create", "--name", backend, "--label", label, *container_limits,
                     image, "sleep", "120"])
            backend_created = True
            backend_inspect = json.loads(command([docker, "inspect", backend]).stdout)[0]
            if backend_inspect.get("Mounts") or backend_inspect["HostConfig"]["Privileged"] or backend_inspect["HostConfig"].get("PortBindings"):
                raise RuntimeError("backend_isolation_verification_failed")
            command([docker, "start", identity, backend])
            inspected = json.loads(command([docker, "inspect", identity, backend]).stdout)
            local, remote = [row["NetworkSettings"]["Networks"][network]["IPAddress"] for row in inspected]
            command([docker, "exec", "-d", backend, "python3", "/polygon/tools/polygon/runtime_topology.py", "backend", remote, local])
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                ready = subprocess.run([docker, "exec", backend, "test", "-f", "/polygon/endpoints-listening"], capture_output=True)
                if ready.returncode == 0:
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError("backend_endpoints_not_listening")
            with tempfile.TemporaryDirectory(prefix="v7-polygon-ca-") as tmp:
                cert = str(Path(tmp) / "polygon-lab.crt")
                command([docker, "cp", backend + ":/polygon/lab.crt", cert])
                command([docker, "cp", cert, identity + ":/usr/local/share/ca-certificates/polygon-lab.crt"])
            command([docker, "exec", identity, "python3", "/polygon/tools/polygon/runtime_topology.py", "router", local, remote])
            started = command([docker, "exec", identity, "python3", "/polygon/tools/polygon/runtime_chain.py", "--inside-traffic"], timeout=90)
        else:
            started = command([docker, "start", "-a", identity], timeout=60)
        result = json.loads(started.stdout)
        result["owner_source_hashes"] = hashes
        result["isolation"] = {"network_mode": "internal" if traffic else "none", "host_mounts": 0, "published_ports": 0, "container_id": inspection["Id"]}
    finally:
        # Attempt every owned cleanup even if one removal fails. Never prune
        # shared images/networks or remove objects selected by a broad glob.
        cleanup_commands = []
        if created:
            cleanup_commands.append([docker, "rm", "-f", identity])
        if backend_created:
            cleanup_commands.append([docker, "rm", "-f", backend])
        if network_created:
            cleanup_commands.append([docker, "network", "rm", network])
        cleanup_commands.append([docker, "image", "rm", image])
        for cleanup_command in cleanup_commands:
            try:
                subprocess.run(cleanup_command, text=True, capture_output=True, timeout=30)
            except subprocess.TimeoutExpired:
                pass  # final absence checks below decide cleanup validity
        remaining = command([docker, "ps", "-aq", "--filter", "label=" + label]).stdout.strip()
        if remaining:
            raise RuntimeError("polygon_container_cleanup_failed")
        images = command([docker, "image", "ls", "-q", "--filter", "reference=" + image]).stdout.strip()
        if images:
            raise RuntimeError("polygon_image_cleanup_failed")
        networks = command([docker, "network", "ls", "-q", "--filter", "label=" + label]).stdout.strip()
        if networks:
            raise RuntimeError("polygon_network_cleanup_failed")
    result["container_cleanup_verified"] = True
    result["image_cleanup_verified"] = True
    result["network_cleanup_verified"] = True
    return result


if __name__ == "__main__":
    if sys.argv[1:] not in (["--inside"], ["--inside-traffic"]):
        raise SystemExit("Use the existing Polygon owner; this is not an independent agent entrypoint.")
    print(json.dumps(inside_probe(traffic=sys.argv[1:] == ["--inside-traffic"]), sort_keys=True))
