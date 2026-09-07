"""Disposable Linux substrate for the existing OMP Polygon owner.

This module supplies topology and starting fixtures, never recovery decisions,
Matrix events, execution receipts or S11. The current probe stops at the real
health/Matrix boundary and explicitly cannot satisfy full-E2E acceptance.
No host mounts, published ports, Docker socket or production state are used.
"""

from __future__ import annotations

import hashlib
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


def inside_probe():
    # Host-side creation separately verifies Docker namespace and mount scope.
    if not Path("/.dockerenv").is_file() or Path("/sys/class/net/eth0").exists():
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
        "id=polygon-source interface=pgsource enabled=1 type=interface protocol=lab\n"
    )
    command(["ip", "link", "add", "pgsource", "type", "dummy"])
    command(["ip", "link", "set", "pgsource", "up"])
    matrix = state / "service-matrix.json"
    # Empty initial state is not fabricated healthy/failed Matrix evidence.
    matrix.write_text('{"items":{}}\n')
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
            if json.loads(matrix.read_text()).get("items"):
                raise RuntimeError("unexpected_pre_fault_matrix_observation")
            fault_ns = time.monotonic_ns()
            command(["ip", "link", "set", "pgsource", "down"])
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                data = json.loads(matrix.read_text())
                row = data.get("items", {}).get("polygon-source", {}).get("services", {}).get("__channel_liveness__", {})
                if row.get("ok") is False and row.get("failure_event_id"):
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
        "matrix_observed_by_harness_monotonic_ns": observed_ns,
        "observation_upper_bound_ms": round((observed_ns - fault_ns) / 1e6, 3),
        "matrix_failure_row": row,
        "events": event_rows,
        "health_log": log,
        "health_returncode": process.returncode,
        "full_e2e_proven": False,
        "required_service_s11_proven": False,
        "scale_proven": False,
        "missing_path": "fresh target/Authority -> Planner -> Packet/Lease/Barrier -> writer -> all-member S11",
    }


def execute(root: Path):
    """Called by the existing Polygon owner; creates only exact owned objects."""
    docker = shutil.which("docker")
    if not docker:
        raise RuntimeError("docker_unavailable")
    identity = "v7-pg-runtime-" + uuid.uuid4().hex[:12]
    image = identity + ":probe"
    label = "v7.polygon.runtime=" + identity
    created = False
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
                "RUN apt-get update && apt-get install -y --no-install-recommends iproute2 curl jq procps util-linux && rm -rf /var/lib/apt/lists/*\n"
                "COPY tools /polygon/tools\nCOPY admin_core /polygon/admin_core\n"
                "ENV PYTHONPATH=/polygon PYTHONDONTWRITEBYTECODE=1\n"
            )
            command([docker, "build", "-q", "-t", image, str(context)], timeout=300)
        command([docker, "create", "--name", identity, "--label", label,
                 "--network", "none", "--cap-drop", "ALL", "--cap-add", "NET_ADMIN",
                 "--security-opt", "no-new-privileges", "--memory", "512m", "--cpus", "2",
                 "--pids-limit", "128", image, "python3", "/polygon/tools/polygon/runtime_chain.py", "--inside"])
        created = True
        inspection = json.loads(command([docker, "inspect", identity]).stdout)[0]
        config = inspection["HostConfig"]
        if inspection.get("Mounts") or config["NetworkMode"] != "none" or config["Privileged"] or config.get("PortBindings"):
            raise RuntimeError("container_isolation_verification_failed")
        started = command([docker, "start", "-a", identity], timeout=60)
        result = json.loads(started.stdout)
        result["owner_source_hashes"] = hashes
        result["isolation"] = {"network_mode": "none", "host_mounts": 0, "published_ports": 0, "container_id": inspection["Id"]}
    finally:
        if created:
            command([docker, "rm", "-f", identity])
        # The image has an exact random task-local tag, never a shared tag.
        subprocess.run([docker, "image", "rm", image], text=True, capture_output=True, timeout=30)
        remaining = command([docker, "ps", "-aq", "--filter", "label=" + label]).stdout.strip()
        if remaining:
            raise RuntimeError("polygon_container_cleanup_failed")
        images = command([docker, "image", "ls", "-q", "--filter", "reference=" + image]).stdout.strip()
        if images:
            raise RuntimeError("polygon_image_cleanup_failed")
    result["container_cleanup_verified"] = True
    result["image_cleanup_verified"] = True
    return result


if __name__ == "__main__":
    if sys.argv[1:] != ["--inside"]:
        raise SystemExit("Use the existing Polygon owner; this is not an independent agent entrypoint.")
    print(json.dumps(inside_probe(), sort_keys=True))
