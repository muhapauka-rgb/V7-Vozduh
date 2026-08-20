"""Controlled Polygon-style comparison of existing Matrix probe selections.

The test invokes the production Matrix CLI entrypoint against a local,
ephemeral response surface.  It changes no V7 Runtime state, routes or users.
"""

import contextlib
import http.server
import importlib.machinery
import importlib.util
import io
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"


def load_matrix_module():
    loader = importlib.machinery.SourceFileLoader(
        "v7_matrix_controlled_comparison", str(MATRIX_TOOL)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class _HealthyResponse(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - required BaseHTTPRequestHandler name
        service_id = self.path.strip("/")
        if service_id in self.server.failed_services:
            self.send_response(503)
        elif service_id in self.server.limited_services:
            self.send_response(403)
        else:
            self.send_response(204)
        self.end_headers()

    def log_message(self, _format, *_args):
        return


class V53MatrixControlledComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_matrix_module()
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _HealthyResponse)
        cls.server.failed_services = set()
        cls.server.limited_services = set()
        cls.port = int(cls.server.server_port)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def run_matrix(
        self,
        services: str = "",
        *,
        failed_services=(),
        limited_services=(),
    ):
        self.server.failed_services = set(failed_services)
        self.server.limited_services = set(limited_services)
        catalog = {
            service_id: {
                "label": str(meta.get("label") or service_id),
                "url": f"http://127.0.0.1:{self.port}/{service_id}",
                "classes": tuple(meta.get("classes") or ()),
            }
            for service_id, meta in self.matrix.SERVICE_CATALOG.items()
            if service_id != "telegram"
        }
        catalog["telegram"] = {
            "label": "Telegram controlled TCP",
            "kind": "telegram_tcp",
            "classes": tuple(self.matrix.SERVICE_CATALOG["telegram"].get("classes") or ()),
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            argv = [
                str(MATRIX_TOOL), "polygon-control", "all",
                "--state-dir", str(root / "state"),
                "--event-dir", str(root / "events"),
                "--interface", "lo0", "--timeout", "3",
            ]
            if services:
                argv.extend(["--services", services])
            output = io.StringIO()
            endpoints = (("127.0.0.1", self.port, True),) * 3
            with mock.patch.object(self.matrix, "SERVICE_CATALOG", catalog), mock.patch.object(
                self.matrix, "TELEGRAM_ENDPOINTS", endpoints
            ), mock.patch.object(
                self.matrix, "bind_to_device", return_value=""
            ), mock.patch.object(sys, "argv", argv
            ), contextlib.redirect_stdout(output):
                self.assertEqual(self.matrix.main(), 0)
            return json.loads(output.getvalue())

    def test_full_and_exact_subset_are_equivalent_on_controlled_healthy_path(self):
        full = self.run_matrix()
        subset = self.run_matrix("telegram,google,google_auth")

        self.assertEqual(full["status"], "OK", full)
        self.assertEqual(subset["status"], "OK", subset)
        self.assertEqual(full["ok_count"], 14)
        self.assertEqual(full["total"], 14)
        self.assertEqual(subset["ok_count"], 3)
        self.assertEqual(subset["total"], 3)
        self.assertEqual(
            full["performance_timeline"]["selected_service_count"], 14
        )
        self.assertEqual(
            subset["performance_timeline"]["selected_service_count"], 3
        )
        self.assertEqual(
            [item["status"] for item in full["performance_timeline"]["probe_attempts"]],
            ["OK"] * 14,
        )
        self.assertEqual(
            [item["status"] for item in subset["performance_timeline"]["probe_attempts"]],
            ["OK"] * 3,
        )

    def test_required_service_failure_matches_in_full_and_subset(self):
        full = self.run_matrix(failed_services=("google",))
        subset = self.run_matrix(
            "telegram,google,google_auth", failed_services=("google",)
        )

        # One observation is deliberately WARN, not a persistent incident.
        # Both variants must still classify it identically and retain the
        # decisive service row for the existing persistence owner.
        self.assertEqual(full["status"], "WARN", full)
        self.assertEqual(subset["status"], "WARN", subset)
        self.assertEqual(full["results"]["google"]["status"], "FAIL")
        self.assertEqual(subset["results"]["google"]["status"], "FAIL")
        self.assertEqual(full["total"], 14)
        self.assertEqual(subset["total"], 3)

    def test_http_methodology_limit_is_not_a_failure_in_full_or_subset(self):
        full = self.run_matrix(limited_services=("google_auth",))
        subset = self.run_matrix(
            "telegram,google,google_auth", limited_services=("google_auth",)
        )

        self.assertEqual(full["results"]["google_auth"]["status"], "HTTP_LIMITED")
        self.assertEqual(subset["results"]["google_auth"]["status"], "HTTP_LIMITED")
        self.assertTrue(full["results"]["google_auth"]["ok"])
        self.assertTrue(subset["results"]["google_auth"]["ok"])
        self.assertEqual(full["status"], subset["status"])
