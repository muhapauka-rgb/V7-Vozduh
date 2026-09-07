"""Disposable Linux substrate for the existing OMP Polygon owner.

This module supplies topology and starting fixtures, never recovery decisions,
Matrix events, execution receipts or S11. The current probe stops at the real
health/Matrix boundary and explicitly cannot satisfy full-E2E acceptance.
No host mounts, published ports, Docker socket or production state are used.
"""

from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
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


def copy_owned_container_artifact(docker, source, target, path):
    # Stream ephemeral client secrets directly between exact owned nodes;
    # never print them or materialize them in the host checkout.
    producer = subprocess.Popen([docker, "cp", source + ":" + path, "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        consumer = subprocess.run([docker, "cp", "-", target + ":/polygon/"], stdin=producer.stdout,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
        producer.stdout.close()
        producer.wait(timeout=15)
    finally:
        if producer.poll() is None:
            producer.kill()
            producer.wait(timeout=5)
    if producer.returncode or consumer.returncode:
        raise RuntimeError("owned_client_artifact_copy_failed")


def existing_owner(name, path):
    loader = importlib.machinery.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def traffic_probe(interface):
    if interface.startswith("10.7.") and Path("/polygon/client-ingress.json").is_file():
        return existing_owner("polygon_client_transport", "/polygon/tools/v7-client-speed-api").isolated_client_transport_request(
            {"action": "path", "source_address": interface},
        )
    checked = subprocess.run([
        "curl", "--interface", interface, "--connect-timeout", "1", "--max-time", "2",
        "-fsS", "-o", "/dev/null", "-w", "%{http_code}", "https://www.google.com/generate_204",
    ], text=True, capture_output=True, timeout=4)
    return {"interface": interface, "returncode": checked.returncode, "http_code": checked.stdout,
            "ok": checked.returncode == 0 and checked.stdout == "204"}


def inside_probe(*, traffic=False, lab_authority=False):
    # Host-side creation separately verifies Docker namespace and mount scope.
    if not Path("/.dockerenv").is_file() or (not traffic and Path("/sys/class/net/eth0").exists()):
        raise RuntimeError("isolated_network_none_container_required")
    state = Path("/polygon/state")
    events = Path("/polygon/events")
    state.mkdir()
    events.mkdir()
    # Deterministic lab-only starting identities. No production registry copy.
    (state / "users.registry").write_text("".join(
        f"ip=10.7.254.{i} current=polygon-source enabled=1 certification_user=1 "
        f"certification_group=isolated-runtime table={1000+i}\n"
        for i in range(1, 6)
    ))
    (state / "egress.registry").write_text(
        "id=polygon-source interface=pgsource enabled=1 type=interface protocol=gre "
        "controlled_certification_source=1 certification_group=isolated-runtime "
        "reservation_owner=operator_execution_governance execution_reserved=1 canary_reserved=1 "
        "autoswitch_allowed=0 rebalance_allowed=0 production_assignment_allowed=0\n"
        + ("id=polygon-target interface=pgtarget enabled=1 type=interface protocol=gre expected_ip=10.201.2.1\n" if traffic else "")
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
    authority = {}
    post_fault_selection = {}
    post_fault_route_truth = {}
    if traffic:
        for egress in ("polygon-source", "polygon-target"):
            probe = command([sys.executable, "/polygon/tools/v7-service-matrix-test",
                             egress, "all", "--state-dir", str(state), "--event-dir", str(events)], timeout=45)
            baseline_services[egress] = json.loads(probe.stdout)
            results = baseline_services[egress].get("results", {})
            if not results or not all(row.get("ok") is True for row in results.values()):
                raise RuntimeError("required_service_baseline_failed:" + probe.stdout[-3000:])
        with ThreadPoolExecutor(max_workers=5) as workers:
            client_baseline = list(workers.map(traffic_probe, [f"10.7.254.{i}" for i in range(1, 6)]))
        if not all(row["ok"] for row in client_baseline):
            raise RuntimeError("client_source_route_baseline_failed:" + json.dumps(client_baseline))
    if lab_authority:
        from admin_core import operator_execution as owner
        from admin_core.operator_execution_isolation import capture_scope
        scope = capture_scope(
            state_dir=state,
            docker_inspection=json.loads(Path("/polygon/isolation-inspection.json").read_text()),
            required_services=list(baseline_services["polygon-source"]["results"]),
        )
        probe_owner = existing_owner("polygon_client_probe_owner", "/polygon/tools/v7-client-speed-api")
        capacity = probe_owner.measure_isolated_polygon_capacity(scope)
        (state / "polygon-cold-capacity-observation.json").write_text(json.dumps(capacity))
        scope["cold_capacity_observation_hash"] = hashlib.sha256(
            (state / "polygon-cold-capacity-observation.json").read_bytes(),
        ).hexdigest()
        # Initial disposable-node control state, produced by its existing
        # owner before the fault. This enables no host/Production operation;
        # the fresh lab contract and per-operation gates remain mandatory.
        control_path = owner.DEFAULT_AUTONOMOUS_EXECUTION_CONTROL_FILE
        control_path.parent.mkdir(parents=True, exist_ok=True)
        owner.write_json_atomic(control_path, owner.build_autonomous_execution_control_state(
            True, actor="OWNER_AUTHORIZED_ISOLATED_POLYGON_CAMPAIGN",
            reason="Initial disposable Polygon node; exact lab standing Authority required",
        ))
        command(["env", "V7_STATE_DIR=" + str(state),
                 "PATH=/polygon/tools/runtime-support:/polygon/tools:/usr/local/bin:/usr/bin:/bin",
                 "bash", "/polygon/tools/runtime-support/v7-state-json-save"])
        command([sys.executable, "/polygon/tools/v7-intelligence-snapshot-refresh",
                 "--state-dir", str(state), "--event-dir", str(events),
                 "--out-dir", str(state / "intelligence"),
                 "--audit-dir", "/polygon/audit"], timeout=30)
        policy = Path("/polygon/policy.json")
        policy.write_text("{}\n")
        audit = Path("/polygon/audit/operator-execution-audit.jsonl")
        request = owner.build_ct_m0f_standing_validation_authority_request(
            policy_generation_hash=owner.sha256_file(policy), isolated_polygon_scope=scope,
        )
        owner.register_ct_m0f_standing_validation_authority_request(request, audit_store=audit)
        issued = owner.issue_ct_m0f_standing_validation_policy_from_audit(
            policy, request_id=request["request_id"], request_hash=request["request_hash"],
            decision=owner.CT_M0F_POLYGON_APPROVAL, actor_id="OWNER_AUTHORIZED_ISOLATED_POLYGON_CAMPAIGN",
            audit_store=audit,
        )
        validation = owner.validate_ct_m0f_standing_validation_policy(
            issued["contract"], audit_records=owner.read_audit_records(audit),
        )
        if not validation["ok"]:
            raise RuntimeError("lab_authority_initial_validation_failed:" + json.dumps(validation["errors"]))
        authority = {"contract_id": issued["contract"]["contract_id"], "schema": issued["contract"]["schema_version"],
                     "pre_fault_validation": validation["status"], "max_members": scope["max_cohort_members"],
                     "max_concurrent_transactions": scope["max_concurrent_transactions"], "scope": scope}
        authority["cold_capacity_observation"] = capacity
        # Existing two-stage lifecycle: reserve the real prefault cohort;
        # incident, target and Packet/Lease are bound only by the later owners.
        implementation = owner.ct_m0f_runtime_implementation_fingerprint(
            governed_cycle=Path("/polygon/tools/v7-governed-canary-dry-run-cycle"),
            matrix_failure_consumer=Path("/polygon/tools/v7-service-matrix-refresh-all"),
            autoswitch=Path("/polygon/tools/v7-users-autoswitch"),
            health_runtime=Path("/polygon/tools/runtime-support/v7-health-loop"),
            routing_runtime=Path("/polygon/tools/runtime-support/v7-routing-sync"),
        )
        source_lines = [line for line in (state / "egress.registry").read_text().splitlines()
                        if line.startswith("id=" + scope["source_egress"] + " ")]
        if len(source_lines) != 1:
            raise RuntimeError("polygon_prefault_source_identity_not_exact")
        reservation = owner.reserve_ct_m0f_standing_validation_transaction(
            contract=issued["contract"], implementation_fingerprint=implementation,
            user=scope["members"][0], source=scope["source_egress"], target="",
            sample_binding_fingerprint=scope["pre_fault_matrix_hash"],
            source_reservation_id="polygon_" + owner.sha256_json(scope),
            source_fingerprint=hashlib.sha256(source_lines[0].encode()).hexdigest(),
            target_binding_mode="POST_T0_OWNER_SELECTED", audit_store=audit,
        )
        if not reservation.get("ok"):
            raise RuntimeError("polygon_prefault_transaction_reservation_failed:" + json.dumps(reservation))
        authority["prefault_transaction_reservation"] = reservation
    args = [
        sys.executable, "/polygon/tools/runtime-support/v7-health-loop",
        "--role-based-fast", "--max-phases", "12",
        "--controlled-owner-root", "/polygon/tools",
        "--controlled-matrix-state-file", str(matrix),
        "--controlled-users-registry-file", str(state / "users.registry"),
        "--controlled-event-dir", str(events),
    ]
    if lab_authority:
        args.extend(["--controlled-policy-file", str(policy), "--controlled-audit-store", str(audit)])
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
            consumer_log_offset = len(output_path.read_text())
            command(["ip", "link", "set", "pgsource", "down"])
            fault_completed_ns = time.monotonic_ns()
            if traffic:
                with ThreadPoolExecutor(max_workers=5) as workers:
                    fault_traffic = list(workers.map(traffic_probe, [f"10.7.254.{i}" for i in range(1, 6)]))
                target_during_fault = traffic_probe("pgtarget")
                if any(row["ok"] for row in fault_traffic) or not target_during_fault["ok"]:
                    raise RuntimeError("source_fault_or_target_path_not_isolated")
            deadline = time.monotonic() + (60 if lab_authority else 10)
            while time.monotonic() < deadline:
                data = json.loads(matrix.read_text())
                row = data.get("items", {}).get("polygon-source", {}).get("services", {}).get("__channel_liveness__", {})
                if lab_authority:
                    transaction_terminal = any(
                        item.get("record_type") == owner.CT_M0F_STANDING_VALIDATION_TRANSACTION_TERMINAL_RECORD_TYPE
                        and item.get("transaction_reservation_id") == reservation["reservation"]["transaction_reservation_id"]
                        for item in owner.read_audit_records(audit)
                    )
                else:
                    transaction_terminal = not traffic or "V7_HEALTH_RECOVERY_CONSUMER_RECEIPT" in output_path.read_text()[consumer_log_offset:]
                if row.get("ok") is False and row.get("failure_event_id") and transaction_terminal:
                    break
                if process.poll() is not None:
                    break
                time.sleep(0.02)
            observed_ns = time.monotonic_ns()
            if lab_authority:
                # Preserve the actual owner's full read-only diagnosis while
                # the source is still physically down. The health receipt is
                # intentionally compact and omits rejected-source details.
                matrix_owner = existing_owner(
                    "polygon_existing_matrix_owner", "/polygon/tools/v7-service-matrix-refresh-all",
                )
                planner = matrix_owner.in_process_autoswitch_module("/polygon/tools/v7-users-autoswitch")
                owner_args = matrix_owner.in_process_autoswitch_args(
                    planner, state_dir=state, event_dir=events, policy_file=policy, audit_store=audit,
                )
                target_diagnostic = planner.controlled_campaign_target_selection_diagnostic(owner_args)
                post_fault_selection = planner.ct_m0f_standing_source_selection_only(
                    owner_args, precomputed_target_diagnostic=target_diagnostic,
                )
                post_fault_selection["target_diagnostic"] = target_diagnostic
                post_fault_selection["source_health_diagnostic"] = planner.controlled_certification_source_health_status(
                    state, scope["source_egress"],
                )
                post_fault_selection["source_binding_diagnostic"] = planner.ct_m0f_certification_only_matrix_failure_binding_projection(
                    state, scope["source_egress"], event_dir=events,
                )
                # Capture actual residue before any restoration/deletion.
                # A failed writer return code is not proof of zero effects.
                with ThreadPoolExecutor(max_workers=len(scope["members"])) as workers:
                    client_path_payload = list(workers.map(traffic_probe, scope["members"]))
                post_fault_route_truth = {
                    "observed_monotonic_ns": time.monotonic_ns(),
                    "users_registry": (state / "users.registry").read_text(),
                    "kernel_rules": json.loads(command(["ip", "-j", "rule", "show"]).stdout),
                    "kernel_routes": json.loads(command(["ip", "-j", "route", "show", "table", "all"]).stdout),
                    "kernel_links": json.loads(command(["ip", "-j", "link", "show"]).stdout),
                    "client_path_payload": client_path_payload,
                    "required_service_s11_credit": False,
                    "observation_role": "post-terminal diagnostic; not the recovery clock",
                }
        finally:
            # Restoration is teardown, never described as V7 failover/S11.
            try:
                process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                process.terminate()
                process.wait(timeout=5)
            command(["ip", "link", "set", "pgsource", "up"])
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
        "consumer_decisions": [
            event["ct_m0f_standing_validation_campaign"] for event in event_rows
            if isinstance(event.get("ct_m0f_standing_validation_campaign"), dict)
        ],
        "health_log": log,
        "health_returncode": process.returncode,
        "pre_fault_lab_authority": authority,
        "execution_audit_records": owner.read_audit_records(audit) if lab_authority else [],
        "post_fault_source_selection_diagnostic": post_fault_selection,
        "post_fault_route_truth_before_teardown": post_fault_route_truth,
        "baseline_services": baseline_services,
        "client_source_route_baseline": client_baseline,
        "client_traffic_during_source_fault": fault_traffic,
        "target_traffic_during_source_fault": target_during_fault,
        "full_e2e_proven": False,
        "required_service_s11_proven": False,
        "scale_proven": False,
        "missing_path": "fresh target/Authority -> Planner -> Packet/Lease/Barrier -> writer -> all-member S11",
    }


def execute(root: Path, *, traffic=False, lab_authority=False):
    """Called by the existing Polygon owner; creates only exact owned objects."""
    docker = shutil.which("docker")
    if not docker:
        raise RuntimeError("docker_unavailable")
    identity = "v7-pg-runtime-" + uuid.uuid4().hex[:12]
    image = identity + ":probe"
    label = "v7.polygon.runtime=" + identity
    created = False
    backend_created = False
    client_created = False
    client_network_created = False
    network_created = False
    backend = identity + "-backend"
    network = identity + "-net"
    client = identity + "-client"
    client_network = identity + "-client-net"
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
                "RUN apt-get update && apt-get install -y --no-install-recommends iproute2 curl jq procps util-linux openssl ca-certificates iptables wireguard-tools && rm -rf /var/lib/apt/lists/*\n"
                "COPY tools /polygon/tools\nCOPY admin_core /polygon/admin_core\n"
                "COPY tools/runtime-support/v7-egress-lib /usr/local/lib/v7-egress-lib\n"
                "ENV PYTHONPATH=/polygon PYTHONDONTWRITEBYTECODE=1 V7_CLIENT_ROOT=/polygon/client-profiles\n"
                "ENV PATH=/polygon/tools/runtime-support:/polygon/tools:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin V7_STATE_DIR=/polygon/state\n"
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
                 *(["--sysctl", "net.ipv4.ip_forward=1"] if lab_authority else []),
                 image, *(["sleep", "120"] if traffic else ["python3", "/polygon/tools/polygon/runtime_chain.py", "--inside"])])
        created = True
        if lab_authority:
            command([docker, "network", "create", "--internal", "--label", label, client_network])
            client_network_created = True
            command([docker, "network", "connect", client_network, identity])
            command([docker, "create", "--name", client, "--label", label, "--network", client_network, *container_limits[2:],
                     image, "sleep", "120"])
            client_created = True
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
            command([docker, "start", identity, backend, *([client] if lab_authority else [])])
            inspected = json.loads(command([docker, "inspect", identity, backend, *([client] if lab_authority else [])]).stdout)
            local, remote = [row["NetworkSettings"]["Networks"][network]["IPAddress"] for row in inspected[:2]]
            if lab_authority:
                net = json.loads(command([docker, "network", "inspect", network]).stdout)[0]
                client_net = json.loads(command([docker, "network", "inspect", client_network]).stdout)[0]
                if ([len(row["NetworkSettings"]["Networks"]) for row in inspected] != [2, 1, 1]
                        or not client_net["Internal"]):
                    raise RuntimeError("polygon_additional_network_forbidden")
                host_inspection = {
                    "internal_network": net["Internal"], "network_id": net["Id"],
                    "container_count": len(inspected), "container_ids": [row["Id"] for row in inspected],
                    "host_mount_count": sum(len(row["Mounts"]) for row in inspected),
                    "published_port_count": sum(len(row["HostConfig"].get("PortBindings") or {}) for row in inspected),
                    "privileged": any(row["HostConfig"]["Privileged"] for row in inspected),
                    "router_memory": inspected[0]["HostConfig"]["Memory"],
                    "client_network_id": client_net["Id"], "client_network_internal": client_net["Internal"],
                    "network_counts": [len(row["NetworkSettings"]["Networks"]) for row in inspected],
                }
                with tempfile.TemporaryDirectory(prefix="v7-polygon-inspection-") as tmp:
                    evidence = Path(tmp) / "isolation-inspection.json"
                    evidence.write_text(json.dumps(host_inspection))
                    command([docker, "cp", str(evidence), identity + ":/polygon/isolation-inspection.json"])
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
                if lab_authority:
                    command([docker, "cp", cert, client + ":/usr/local/share/ca-certificates/polygon-lab.crt"])
            command([docker, "exec", identity, "python3", "/polygon/tools/polygon/runtime_topology.py", "router-wg" if lab_authority else "router", local, remote])
            if lab_authority:
                ingress_address = inspected[0]["NetworkSettings"]["Networks"][client_network]["IPAddress"]
                client_address = inspected[2]["NetworkSettings"]["Networks"][client_network]["IPAddress"]
                command([docker, "exec", identity, "python3", "/polygon/tools/polygon/runtime_topology.py", "wg-server", ingress_address])
                for path in ("/polygon/client-profiles", "/polygon/client-transport-secret", "/polygon/client-ingress.json"):
                    copy_owned_container_artifact(docker, identity, client, path)
                command([docker, "exec", client, "python3", "/polygon/tools/polygon/runtime_topology.py", "wg-clients"])
                client_inode = int(command([docker, "exec", client, "stat", "-Lc", "%i", "/proc/self/ns/net"]).stdout)
                # Public topology binding only; never read/print key files.
                descriptor = json.loads(command([docker, "exec", identity, "python3", "-c",
                                                  "from pathlib import Path; print(Path('/polygon/client-ingress.json').read_text())"]).stdout)
                descriptor.update({"client_transport_address": client_address, "client_network_namespace_inode": client_inode})
                with tempfile.TemporaryDirectory(prefix="v7-polygon-client-descriptor-") as tmp:
                    path = Path(tmp) / "client-ingress.json"
                    path.write_text(json.dumps(descriptor))
                    for node in (identity, client):
                        command([docker, "cp", str(path), node + ":/polygon/client-ingress.json"])
                command([docker, "exec", "-d", client, "env", "V7_CLIENT_SPEED_HOST=" + client_address,
                         "python3", "/polygon/tools/v7-client-speed-api"])
                command([docker, "exec", client, "python3", "-c",
                         "import socket,time; deadline=time.monotonic()+5\n"
                         "while True:\n"
                         " try:\n"
                         "  s=socket.create_connection(('" + client_address + "',7090),.2); s.close(); break\n"
                         " except OSError:\n"
                         "  if time.monotonic()>=deadline: raise\n"
                         "  time.sleep(.05)\n"])
            started = command([docker, "exec", identity, "python3", "/polygon/tools/polygon/runtime_chain.py",
                               "--inside-authority" if lab_authority else "--inside-traffic"], timeout=90)
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
        if client_created:
            cleanup_commands.append([docker, "rm", "-f", client])
        if network_created:
            cleanup_commands.append([docker, "network", "rm", network])
        if client_network_created:
            cleanup_commands.append([docker, "network", "rm", client_network])
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
    if sys.argv[1:] not in (["--inside"], ["--inside-traffic"], ["--inside-authority"]):
        raise SystemExit("Use the existing Polygon owner; this is not an independent agent entrypoint.")
    print(json.dumps(inside_probe(traffic=sys.argv[1:] != ["--inside"], lab_authority=sys.argv[1:] == ["--inside-authority"]), sort_keys=True))
