"""Network and endpoint fixtures for the existing disposable Polygon.

No Matrix/Planner/Authority results are produced here. GRE paths model channel
transport; HTTPS/TCP endpoints model the configured remote services. The real
probe catalog, TLS validation and runtime writers remain unchanged.
"""

from __future__ import annotations

import http.server
import importlib.machinery
import importlib.util
import ipaddress
import json
from pathlib import Path
import secrets
import socketserver
import ssl
import subprocess
import struct
import threading
import time
from urllib.parse import urlparse


def run(*argv, input_text=None):
    return subprocess.run(argv, input=input_text, check=True, capture_output=True, text=True).stdout


def client_probe_owner():
    loader = importlib.machinery.SourceFileLoader("polygon_existing_client_owner", "/polygon/tools/v7-client-speed-api")
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def configure_wireguard_server(endpoint):
    """Ephemeral real WG profiles; private keys never leave disposable nodes."""
    profiles = Path("/polygon/client-profiles")
    profiles.mkdir(mode=0o700)
    secret = Path("/polygon/client-transport-secret")
    secret.write_text(secrets.token_hex(32))
    secret.chmod(0o600)
    private = run("wg", "genkey").strip()
    public = run("wg", "pubkey", input_text=private + "\n").strip()
    config = f"[Interface]\nPrivateKey = {private}\nListenPort = 51820\n"
    members = []
    for number in range(1, 6):
        address = f"10.7.254.{number}"
        key = run("wg", "genkey").strip()
        peer = run("wg", "pubkey", input_text=key + "\n").strip()
        folder = profiles / str(number)
        folder.mkdir(mode=0o700)
        path = folder / "client.conf"
        path.write_text(f"[Interface]\nPrivateKey = {key}\nAddress = {address}/32\n[Peer]\nPublicKey = {public}\nEndpoint = {endpoint}:51820\nAllowedIPs = 0.0.0.0/0\nPersistentKeepalive = 1\n")
        path.chmod(0o600)
        config += f"[Peer]\nPublicKey = {peer}\nAllowedIPs = {address}/32\n"
        members.append({"source_address": address, "public_key": peer, "client_interface": f"pgwc{number}"})
    run("ip", "link", "add", "wg0", "type", "wireguard")
    run("wg", "setconf", "wg0", "/dev/stdin", input_text=config)
    run("ip", "addr", "add", "10.7.254.254/24", "dev", "wg0")
    run("ip", "link", "set", "wg0", "up")
    # Docker sets this in the disposable network namespace before startup;
    # /proc/sys is deliberately read-only to the verifier process.
    if Path("/proc/sys/net/ipv4/ip_forward").read_text().strip() != "1":
        raise RuntimeError("isolated_router_forwarding_not_enabled")
    descriptor = {"schema": "v7.isolated-wg-client-substrate.v1", "server_endpoint": endpoint,
                  "server_public_key": public, "members": members,
                  "profile_root": str(profiles), "ingress_interface": "wg0"}
    Path("/polygon/client-ingress.json").write_text(json.dumps(descriptor))


def configure_wireguard_clients():
    """Five logical clients in the existing disposable client namespace."""
    owner = client_probe_owner()
    descriptor = json.loads(Path("/polygon/client-ingress.json").read_text())
    state = Path("/polygon/client-state")
    state.mkdir()
    (state / "egress.registry").write_text("".join(
        f"id=client-{number} interface={member['client_interface']} enabled=1 type=interface protocol=wireguard\n"
        for number, member in enumerate(descriptor["members"], 1)
    ))
    for number, member in enumerate(descriptor["members"], 1):
        interface, address = member["client_interface"], member["source_address"]
        profile = Path(descriptor["profile_root"]) / str(number) / "client.conf"
        run("ip", "link", "add", interface, "type", "wireguard")
        run("wg", "setconf", interface, "/dev/stdin", input_text=owner.wireguard_setconf_text(profile.read_text()))
        run("ip", "addr", "add", address + "/32", "dev", interface)
        run("ip", "link", "set", interface, "up")
        run("ip", "rule", "add", "priority", str(3000 + number), "from", address, "lookup", str(3000 + number))
        run("ip", "route", "add", "default", "dev", interface, "table", str(3000 + number))
    # Observe genuine protocol handshakes; no pre-written readiness receipt.
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if all(any(int(line.split()[1]) > 0 for line in run("wg", "show", member["client_interface"], "latest-handshakes").splitlines())
               for member in descriptor["members"]):
            break
        time.sleep(0.05)
    else:
        raise RuntimeError("isolated_wireguard_handshakes_not_observed")
    domains, _ = endpoint_catalog()
    with Path("/etc/hosts").open("a") as hosts:
        hosts.write("\n198.19.0.1 " + " ".join(domains) + "\n")
    run("update-ca-certificates")
    Path("/polygon/client-namespace-ready").touch()


def endpoint_catalog(root=Path("/polygon")):
    loader = importlib.machinery.SourceFileLoader("polygon_endpoint_catalog", str(root / "tools/v7-service-matrix-test"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    domains = {urlparse(row["url"]).hostname for row in module.SERVICE_CATALOG.values() if row.get("url")}
    domains.update({"icanhazip.com", "stun.cloudflare.com"})
    addresses = {"198.19.0.1"}
    for host, _port, _required in module.TELEGRAM_ENDPOINTS:
        try:
            addresses.add(str(ipaddress.ip_address(host)))
        except ValueError:
            domains.add(host)
    return sorted(domains), sorted(addresses)


def configure_paths(local, remote, *, backend):
    # Outer addresses are provided by the inspected private Docker network,
    # not arbitrary user-supplied remote infrastructure.
    for address in (local, remote):
        if not ipaddress.ip_address(address).is_private:
            raise ValueError("private_outer_transport_required")
    for number, name in ((1, "pgsource"), (2, "pgtarget")):
        run("ip", "tunnel", "add", name, "mode", "gre", "local", local, "remote", remote, "key", str(number))
        host = 2 if backend else 1
        run("ip", "addr", "add", f"10.201.{number}.{host}/30", "dev", name)
        run("ip", "link", "set", name, "up")
        if not backend:
            run("ip", "route", "add", "default", "dev", name, "table", str(200 + number))
            run("ip", "rule", "add", "priority", str(200 + number), "oif", name, "lookup", str(200 + number))
            # Replies return through the same tunnel even for a bound client
            # address. The host namespace and its firewall are not accessible.
            run("iptables", "-t", "nat", "-A", "POSTROUTING", "-o", name,
                "-s", "10.7.0.0/16", "-j", "SNAT", "--to-source", f"10.201.{number}.1")
    if not backend:
        run("ip", "route", "add", "default", "dev", "pgsource")


def start_backend(local, remote):
    configure_paths(local, remote, backend=True)
    domains, addresses = endpoint_catalog()
    for address in addresses:
        run("ip", "addr", "add", address + "/32", "dev", "lo")
    run("openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
        "-keyout", "/polygon/lab.key", "-out", "/polygon/lab.crt", "-days", "1",
        "-subj", "/CN=V7 isolated Polygon endpoints",
        "-addext", "subjectAltName=" + ",".join("DNS:" + name for name in domains))

    class Endpoint(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.headers.get("Host") == "icanhazip.com":
                payload = self.client_address[0].encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            if self.path == "/__v7_polygon_payload":
                payload = b"V" * (1024 * 1024)
                self.send_response(200)
                self.send_header("Content-Length", str(len(payload)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(payload)
                return
            self.send_response(204)
            self.end_headers()

        def log_message(self, *_args):
            pass

    class TCP(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.recv(1)

    class STUN(socketserver.BaseRequestHandler):
        def handle(self):
            data, sock = self.request
            if len(data) != 20 or struct.unpack("!HHI", data[:8]) != (1, 0, 0x2112A442):
                return
            address, port = self.client_address
            mapped = struct.pack("!BBHI", 0, 1, port ^ 0x2112, int(ipaddress.ip_address(address)) ^ 0x2112A442)
            sock.sendto(struct.pack("!HHI", 0x0101, 12, 0x2112A442) + data[8:20] + struct.pack("!HH", 0x0020, 8) + mapped, self.client_address)

    plain = http.server.ThreadingHTTPServer(("0.0.0.0", 80), Endpoint)
    secure = http.server.ThreadingHTTPServer(("0.0.0.0", 443), Endpoint)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("/polygon/lab.crt", "/polygon/lab.key")
    secure.socket = context.wrap_socket(secure.socket, server_side=True)
    tcp = socketserver.ThreadingTCPServer(("0.0.0.0", 5222), TCP)
    tcp.daemon_threads = True
    stun = socketserver.ThreadingUDPServer(("0.0.0.0", 3478), STUN)
    for server in (plain, secure, stun):
        threading.Thread(target=server.serve_forever, daemon=True).start()
    # Readiness denotes listening fixtures, never healthy Matrix truth.
    Path("/polygon/endpoints-listening").touch()
    tcp.serve_forever()


def configure_router(local, remote, *, wireguard_ingress=False):
    configure_paths(local, remote, backend=False)
    domains, _addresses = endpoint_catalog()
    with Path("/etc/hosts").open("a") as hosts:
        hosts.write("\n198.19.0.1 " + " ".join(domains) + "\n")
    run("update-ca-certificates")
    # Addresses and initial source rules are topology starting conditions;
    # post-fault route changes belong exclusively to the existing writer.
    for number in range(1, 6):
        address = f"10.7.254.{number}"
        if not wireguard_ingress:
            run("ip", "addr", "add", address + "/32", "dev", "lo")
        run("ip", "rule", "add", "priority", str(1000 + number), "from", address, "table", str(1000 + number))
        run("ip", "route", "add", "default", "dev", "pgsource", "table", str(1000 + number))


if __name__ == "__main__":
    import sys
    if not Path("/.dockerenv").is_file():
        raise SystemExit("container_required")
    if len(sys.argv) == 2 and sys.argv[1] == "wg-clients":
        configure_wireguard_clients()
    elif len(sys.argv) == 3 and sys.argv[1] == "wg-server":
        configure_wireguard_server(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] in {"backend", "router", "router-wg"}:
        if sys.argv[1] == "backend":
            start_backend(sys.argv[2], sys.argv[3])
        else:
            configure_router(sys.argv[2], sys.argv[3], wireguard_ingress=sys.argv[1] == "router-wg")
    else:
        raise SystemExit("Called only inside an inspected disposable Polygon container.")
