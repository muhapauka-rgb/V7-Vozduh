"""Stage C Polygon failure matrix for V5.3 candidates A/B/C.

The test uses the existing Matrix owner and the pure governed execution
pipeline. It runs only in an ephemeral local response surface; the final
authority boundary is intentionally not crossed, so no route or user moves.
"""

from __future__ import annotations

import contextlib
import http.server
import importlib.machinery
import importlib.util
import io
import json
import sys
import tempfile
import threading
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from admin_core import operator_execution_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[2]
MATRIX_TOOL = ROOT / "tools" / "v7-service-matrix-test"


def load_matrix_module():
    loader = importlib.machinery.SourceFileLoader(
        "v7_matrix_candidate_failure_matrix", str(MATRIX_TOOL)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class _CandidateResponse(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - BaseHTTPRequestHandler contract
        time.sleep(float(getattr(self.server, "delay_seconds", 0.0)))
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


class V53CandidateFailureMatrixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_matrix_module()
        cls.server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), _CandidateResponse
        )
        cls.server.failed_services = set()
        cls.server.limited_services = set()
        cls.server.delay_seconds = 0.0
        cls.port = int(cls.server.server_port)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def candidate_specs(self):
        return {
            "A_FULL_MATRIX": {"services": "", "passive": False},
            "B_FAST_DEEP_EXISTING_OWNER": {
                "services": "telegram,google,google_auth",
                "passive": False,
            },
            "C_PASSIVE_ESCALATION_THROUGH_MATRIX": {
                "services": "telegram,google,google_auth",
                "passive": True,
            },
        }

    def run_matrix(self, services: str = "", *, failed_services=(), limited_services=()):
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
            "classes": tuple(
                self.matrix.SERVICE_CATALOG["telegram"].get("classes") or ()
            ),
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            argv = [
                str(MATRIX_TOOL),
                "polygon-control",
                "all",
                "--state-dir",
                str(root / "state"),
                "--event-dir",
                str(root / "events"),
                "--interface",
                "lo0",
                "--timeout",
                "3",
            ]
            if services:
                argv.extend(["--services", services])
            output = io.StringIO()
            endpoints = (("127.0.0.1", self.port, True),) * 3
            with mock.patch.object(self.matrix, "SERVICE_CATALOG", catalog), mock.patch.object(
                self.matrix, "TELEGRAM_ENDPOINTS", endpoints
            ), mock.patch.object(
                self.matrix, "bind_to_device", return_value=""
            ), mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                self.assertEqual(self.matrix.main(), 0)
            return json.loads(output.getvalue())

    @staticmethod
    def decision_surface(*, stale: bool = False):
        snapshot_status = {
            "status": "STALE" if stale else "OK",
            "validation_ok": not stale,
            "freshness_state": "STALE" if stale else "FRESH",
            "stop_required": stale,
            "validation_errors": ["stale"] if stale else [],
        }
        return {
            "controlled_execution_source_hashes": {
                "users_registry": "users-candidate-hash",
                "egress_registry": "egress-candidate-hash",
            },
            "controlled_execution_snapshot_bundle_hash": "snapshot-candidate-hash",
            "users_by_ip": {
                "10.7.0.5": {
                    "user": "10.7.0.5",
                    "current_channel": "vless",
                    "recommended_channel": "awg0",
                    "confidence": 0.92,
                    "trust": 88.0,
                    "prediction": {"confidence": 0.86},
                    "risk": 1.5,
                    "recommendation_hash": "candidate-recommendation",
                    "source_hash": "candidate-source",
                    "reasons": ["existing Planner selected bounded target"],
                }
            },
            "batch_preview": {
                "users_to_move": [
                    {
                        "user": "10.7.0.5",
                        "from": "vless",
                        "to": "awg0",
                        "confidence": 0.92,
                        "risk": 1.5,
                        "recommendation_hash": "candidate-recommendation",
                    }
                ]
            },
            "snapshot_statuses": {
                "service-scores": snapshot_status,
                "trust-summaries": dict(snapshot_status),
                "prediction-summaries": dict(snapshot_status),
            },
        }

    @staticmethod
    def passive_event():
        return [
            {
                "event_id": "candidate-passive-event",
                "source": "service_matrix",
                "channel": "vless",
                "message": "required service suspicion",
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "confidence": 0.95,
            }
        ]

    def test_same_failure_matrix_reaches_t0_t11_authority_boundary_for_all_candidates(self):
        results = {}
        for name, spec in self.candidate_specs().items():
            healthy = self.run_matrix(spec["services"])
            failed = self.run_matrix(spec["services"], failed_services=("google",))
            events = self.passive_event() if spec["passive"] else []
            cycle = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
                events=events,
                decision_surface=self.decision_surface(),
                max_users=1,
                now="2026-08-21T10:10:00Z",
            )
            results[name] = {
                "healthy": healthy,
                "failed": failed,
                "cycle": cycle,
            }

            self.assertEqual(healthy["status"], "OK", (name, healthy))
            self.assertEqual(failed["results"]["google"]["status"], "FAIL")
            self.assertEqual(failed["status"], "WARN", (name, failed))
            self.assertEqual(cycle["stop_reason"], "AUTHORITY_BOUNDARY")
            self.assertEqual(cycle["candidate"]["user"], "10.7.0.5")
            self.assertEqual(cycle["packet_preview"]["status"], "PACKET_PREVIEW_READY")
            self.assertEqual(cycle["restore_status"]["status"], "RESTORE_AND_ROLLBACK_PREVIEW_READY")
            self.assertEqual(cycle["verification_plan"]["status"], "VERIFICATION_PLAN_READY")
            self.assertEqual(cycle["outcome_closure_plan"]["status"], "OUTCOME_CLOSURE_PLAN_READY")
            self.assertFalse(cycle["safety"]["apply_executed"])
            self.assertEqual(cycle["safety"]["users_moved"], 0)

        self.assertEqual(set(results), set(self.candidate_specs()))

    def test_short_full_disagreement_forces_full_fallback(self):
        full = self.run_matrix(failed_services=("youtube",))
        short = self.run_matrix("telegram,google,google_auth")

        self.assertEqual(full["status"], "WARN", full)
        self.assertEqual(short["status"], "OK", short)
        self.assertNotEqual(
            full["results"]["youtube"]["status"],
            short["status"],
        )
        fallback = {
            "required": True,
            "reason": "SHORT_FULL_DISAGREEMENT",
            "canonical_result": "FULL",
            "action_allowed": False,
        }
        self.assertTrue(fallback["required"])
        self.assertEqual(fallback["canonical_result"], "FULL")
        self.assertFalse(fallback["action_allowed"])

    def test_stale_state_and_certification_identity_fail_closed(self):
        cycle = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            events=[],
            decision_surface=self.decision_surface(stale=True),
            max_users=1,
            now="2026-08-21T10:10:00Z",
        )
        self.assertEqual(cycle["stop_reason"], "MISSING_STATE_TRANSITION")
        self.assertIn(
            "snapshot_mismatch:service-scores",
            cycle["dry_run"]["safety_gates"]["hard_stop_blockers"],
        )
        self.assertFalse(cycle["safety"]["execution_allowed_now"])
        self.assertFalse(cycle["safety"]["apply_executed"])
        self.assertEqual(cycle["safety"]["users_moved"], 0)

    def test_ordinary_scope_binding_excludes_certification_identity(self):
        bound = pipeline  # keep the test's owner map explicit below
        del bound
        from importlib.machinery import SourceFileLoader

        loader = SourceFileLoader(
            "v7_canary_scope_binding", str(ROOT / "tools" / "v7-governed-canary-dry-run-cycle")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cli = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cli)
        result = cli.bind_ordinary_service_failure_selection(
            {
                "selected_moves": [
                    {"user": "10.7.0.5", "from": "vless", "to": "awg0"},
                    {"user": "10.7.0.6", "from": "vless", "to": "awg3"},
                ]
            },
            users_by_ip={"10.7.0.6": {"certification_user": True}},
            source="vless",
            max_users=1,
        )
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["selected_count"], 1)
        self.assertEqual(result["plan"]["selected_moves"][0]["user_ip"], "10.7.0.5")
        self.assertEqual(result["certification_selected_count"], 0)

    def test_scale_tournament_uses_same_failure_contract_and_bounds_hot_probe_budget(self):
        scales = (7, 50, 100, 1000)
        full_service_count = len(self.matrix.SERVICE_CATALOG)
        fast_service_count = 3
        hot_cohort_cap = 4
        for egress_count in scales:
            hot_cohort = min(egress_count, hot_cohort_cap)
            full_probes = egress_count * full_service_count
            fast_probes = hot_cohort * fast_service_count
            worst_case_all_hot = egress_count * fast_service_count

            self.assertEqual(full_probes, 14 * egress_count)
            self.assertEqual(fast_probes, 3 * hot_cohort)
            self.assertLess(fast_probes, full_probes)
            self.assertLessEqual(worst_case_all_hot, full_probes)
            self.assertEqual(fast_probes, 12 if egress_count >= 4 else 3 * egress_count)

        # The common failure contract is independent of scale: stale target
        # readiness remains fail-closed and never turns probe economy into a
        # route decision.
        stale = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            events=[],
            decision_surface=self.decision_surface(stale=True),
            max_users=1,
            now="2026-08-21T10:10:00Z",
        )
        self.assertEqual(stale["stop_reason"], "MISSING_STATE_TRANSITION")
        self.assertFalse(stale["safety"]["execution_allowed_now"])


if __name__ == "__main__":
    unittest.main()
