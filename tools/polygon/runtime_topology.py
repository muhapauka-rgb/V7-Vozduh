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
from pathlib import Path
import socketserver
import ssl
import subprocess
import threading
from urllib.parse import urlparse


def run(*argv):
    return subprocess.run(argv, check=True, capture_output=True, text=True).stdout


def endpoint_catalog(root=Path("/polygon")):
    loader = importlib.machinery.SourceFileLoader("polygon_endpoint_catalog", str(root / "tools/v7-service-matrix-test"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    domains = {urlparse(row["url"]).hostname for row in module.SERVICE_CATALOG.values() if row.get("url")}
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
                "-s", "198.18.0.0/24", "-j", "SNAT", "--to-source", f"10.201.{number}.1")
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

    plain = http.server.ThreadingHTTPServer(("0.0.0.0", 80), Endpoint)
    secure = http.server.ThreadingHTTPServer(("0.0.0.0", 443), Endpoint)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("/polygon/lab.crt", "/polygon/lab.key")
    secure.socket = context.wrap_socket(secure.socket, server_side=True)
    tcp = socketserver.ThreadingTCPServer(("0.0.0.0", 5222), TCP)
    tcp.daemon_threads = True
    for server in (plain, secure):
        threading.Thread(target=server.serve_forever, daemon=True).start()
    # Readiness denotes listening fixtures, never healthy Matrix truth.
    Path("/polygon/endpoints-listening").touch()
    tcp.serve_forever()


def configure_router(local, remote):
    configure_paths(local, remote, backend=False)
    domains, _addresses = endpoint_catalog()
    with Path("/etc/hosts").open("a") as hosts:
        hosts.write("\n198.19.0.1 " + " ".join(domains) + "\n")
    run("update-ca-certificates")
    # Addresses and initial source rules are topology starting conditions;
    # post-fault route changes belong exclusively to the existing writer.
    for number in range(1, 6):
        address = f"198.18.0.{number}"
        run("ip", "addr", "add", address + "/32", "dev", "lo")
        run("ip", "rule", "add", "priority", str(1000 + number), "from", address, "table", str(1000 + number))
        run("ip", "route", "add", "default", "dev", "pgsource", "table", str(1000 + number))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4 or sys.argv[1] not in {"backend", "router"}:
        raise SystemExit("Called only inside an inspected disposable Polygon container.")
    if not Path("/.dockerenv").is_file():
        raise SystemExit("container_required")
    (start_backend if sys.argv[1] == "backend" else configure_router)(sys.argv[2], sys.argv[3])
