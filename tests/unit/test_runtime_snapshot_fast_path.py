import importlib.machinery
import importlib.util
import json
import textwrap
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional

from admin_core.intelligence_snapshots import (
    SNAPSHOT_FAMILIES,
    build_snapshot_envelope,
    snapshot_path,
)
from admin_core.intelligence_workers import build_all_snapshots, write_snapshots


ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "tools" / "v7-users-autoswitch"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_perf4", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class RuntimeSnapshotFastPathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool_module()

    def write_fixture(self, root: Path) -> None:
        state_dir = root / "state"
        event_dir = root / "events"
        state_dir.mkdir()
        event_dir.mkdir()
        (state_dir / "users.registry").write_text("ip=10.0.0.2 current=current table=100 enabled=1\n", encoding="utf-8")
        (state_dir / "egress.registry").write_text(
            "id=current interface=cur0 enabled=1 state=enabled role=GLOBAL_STABLE\n"
            "id=fast interface=f1 enabled=1 state=enabled role=GLOBAL_FAST\n",
            encoding="utf-8",
        )
        runtime_state = {
            "egress": {
                "current": {"avg_mbps": 4, "min_mbps": 2, "stability": 0.5, "code": "200", "diagnose_severity": "OK"},
                "fast": {"avg_mbps": 50, "min_mbps": 40, "stability": 0.9, "code": "200", "diagnose_severity": "OK"},
            }
        }
        (state_dir / "v7-state.json").write_text(json.dumps(runtime_state), encoding="utf-8")
        service_matrix = {
            "items": {
                "current": {"services": {"telegram": {"ok": False, "status": "DOWN", "score": 0, "confidence": 1.0}}},
                "fast": {"services": {"telegram": {"ok": True, "status": "OK", "score": 95, "first_byte_sec": 0.2, "confidence": 1.0}}},
            }
        }
        quality_summary = {
            "items": {
                "current": {"windows": {"1h": {"avg_mbps": 4, "stability": 0.5, "fail_rate": 0.2}}},
                "fast": {"windows": {"1h": {"avg_mbps": 50, "stability": 0.9, "fail_rate": 0.01}}},
            }
        }
        service_preferences = {"required_services": ["telegram"]}
        (state_dir / "service-matrix.json").write_text(json.dumps(service_matrix), encoding="utf-8")
        (state_dir / "egress-quality-summary.json").write_text(json.dumps(quality_summary), encoding="utf-8")
        (state_dir / "service-preferences.json").write_text(json.dumps(service_preferences), encoding="utf-8")
        (event_dir / "switch-history.jsonl").write_text(json.dumps({"result": "OK", "blast_radius": 1}) + "\n", encoding="utf-8")
        policy = {
            "required_services": ["telegram"],
            "switch": {"autoswitch_enabled": True, "cooldown_seconds": 0, "min_score_delta": 1},
            "load": {"rebalance_enabled": False},
            "reconnect": {"enabled": False},
        }
        (root / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
        (root / "org-policy.json").write_text("{}", encoding="utf-8")
        for name in [
            "autoswitch-safety.json",
            "telegram-sentinel.json",
            "client-reconnect-state.json",
            "vless-activity.json",
            "egress-load-summary.json",
            "autoswitch-restore-barrier.json",
        ]:
            (state_dir / name).write_text("{}", encoding="utf-8")

    def args_for(self, root: Path, extra: Optional[List[str]] = None):
        parser = self.tool.build_arg_parser()
        return parser.parse_args(
            [
                "--state-dir", str(root / "state"),
                "--policy-file", str(root / "policy.json"),
                "--org-policy-file", str(root / "org-policy.json"),
                "--event-dir", str(root / "events"),
                "--quality-summary-file", str(root / "state" / "egress-quality-summary.json"),
                "--intelligence-snapshot-root", str(root / "state" / "intelligence"),
                "--safety-file", str(root / "state" / "autoswitch-safety.json"),
                "--telegram-sentinel-file", str(root / "state" / "telegram-sentinel.json"),
                "--reconnect-state-file", str(root / "state" / "client-reconnect-state.json"),
                "--vless-activity-file", str(root / "state" / "vless-activity.json"),
                "--load-summary-file", str(root / "state" / "egress-load-summary.json"),
                "--restore-barrier-file", str(root / "state" / "autoswitch-restore-barrier.json"),
            ] + list(extra or [])
        )

    def write_good_snapshots(self, root: Path) -> None:
        state_dir = root / "state"
        service_matrix = json.loads((state_dir / "service-matrix.json").read_text(encoding="utf-8"))
        quality_summary = json.loads((state_dir / "egress-quality-summary.json").read_text(encoding="utf-8"))
        service_preferences = json.loads((state_dir / "service-preferences.json").read_text(encoding="utf-8"))
        runtime_state = json.loads((state_dir / "v7-state.json").read_text(encoding="utf-8"))
        result = build_all_snapshots(
            service_matrix=service_matrix,
            quality_summary=quality_summary,
            service_preferences=service_preferences,
            audit_records=[{"result": "OK", "operation": {"terminal_state": "APPLIED"}}],
            switch_records=[{"result": "OK", "blast_radius": 1}],
            rollback_records=[],
            runtime_state=runtime_state,
            users_registry=[{"ip": "10.0.0.2", "enabled": "1"}],
            egress_registry=[{"id": "current"}, {"id": "fast"}],
            total_users=1,
            affected_candidates=1,
        )
        write_snapshots(state_dir / "intelligence", result.snapshots)

    def load_snapshot(self, root: Path, family: str) -> dict:
        return json.loads(snapshot_path(root / "state" / "intelligence", family).read_text(encoding="utf-8"))

    def write_snapshot(self, root: Path, family: str, payload: dict) -> None:
        snapshot_path(root / "state" / "intelligence", family).write_text(json.dumps(payload), encoding="utf-8")

    def plan(self, root: Path) -> dict:
        planner = self.tool.AutoswitchPlanner(self.args_for(root))
        plan = planner.plan()
        plan["apply_result"] = planner.apply(plan)
        planner.finalize_operation(plan)
        return plan

    def plan_with_args(self, root: Path, extra: List[str]) -> dict:
        planner = self.tool.AutoswitchPlanner(self.args_for(root, extra))
        plan = planner.plan()
        plan["apply_result"] = planner.apply(plan)
        planner.finalize_operation(plan)
        return plan

    def test_snapshot_fast_path_does_not_read_runtime_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            self.write_good_snapshots(root)
            planner = self.tool.AutoswitchPlanner(self.args_for(root))
            planner._recent_audit_records = lambda *args, **kwargs: self.fail("snapshot fast path read runtime history")
            plan = planner.plan()
            self.assertEqual(plan["routing_brain"]["mode"], "snapshot_backed_planner_advisory_context")
            self.assertTrue(plan["safety"]["intelligence_snapshots"]["active"])
            self.assertFalse(plan["safety"]["intelligence_snapshots"]["stop_required"])
            self.assertEqual(len(plan["selected_moves"]), 1)
            fast_candidate = next(
                candidate
                for candidate in plan["decisions"][0]["candidates"]
                if candidate["egress"] == "fast"
            )
            self.assertEqual(
                fast_candidate["routing_intelligence"]["source"],
                "intelligence_snapshot:candidate-suitability-summary",
            )
            self.assertIn("best_available_pool_advice", plan["routing_brain"])
            self.assertEqual(
                plan["routing_brain"]["best_available_pool_advice"]["single_best_channel_authority"],
                "none",
            )
            self.assertIn("prediction_advice", plan["routing_brain"])
            self.assertTrue(plan["routing_brain"]["prediction_advice"]["available"])
            self.assertFalse(plan["routing_brain"]["prediction_advice"]["runtime_forecasting_performed"])
            self.assertEqual(plan["routing_brain"]["prediction_advice"]["execution_authority"], "none")
            self.assertIn("trust_evolution_advice", plan["routing_brain"])
            self.assertTrue(plan["routing_brain"]["trust_evolution_advice"]["available"])
            self.assertFalse(plan["routing_brain"]["trust_evolution_advice"]["autonomy_enabled"])
            self.assertFalse(plan["routing_brain"]["trust_evolution_advice"]["runtime_trust_training_performed"])
            self.assertEqual(plan["routing_brain"]["trust_evolution_advice"]["execution_authority"], "none")

    def test_missing_required_snapshot_suppresses_selected_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            self.write_good_snapshots(root)
            snapshot_path(root / "state" / "intelligence", "trust-summaries").unlink()
            plan = self.plan(root)
            gate = plan["safety"]["intelligence_snapshots"]
            self.assertTrue(gate["stop_required"])
            self.assertIn("trust-summaries", gate["stop_families"])
            self.assertEqual(plan["selected_moves"], [])
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_intelligence_snapshot_stop_required")

    def test_bad_required_snapshot_states_fail_closed(self):
        cases = {
            "corrupt": lambda root: snapshot_path(root / "state" / "intelligence", "trust-summaries").write_text("{broken", encoding="utf-8"),
            "expired": self.make_expired_trust,
            "unknown": self.make_unknown_trust,
            "low_confidence": self.make_low_confidence_trust,
            "source_hash_mismatch": self.make_source_hash_mismatch,
            "oversized": lambda root: snapshot_path(root / "state" / "intelligence", "trust-summaries").write_text("x" * 1_000_100, encoding="utf-8"),
            "stale_runtime_required": self.make_stale_runtime_required_trust,
        }
        for name, mutate in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_fixture(root)
                self.write_good_snapshots(root)
                mutate(root)
                plan = self.plan(root)
                gate = plan["safety"]["intelligence_snapshots"]
                self.assertTrue(gate["stop_required"])
                self.assertEqual(plan["selected_moves"], [])
                self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_intelligence_snapshot_stop_required")

    def test_stale_advisory_snapshot_is_ignored_without_suppressing_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            self.write_good_snapshots(root)
            old = datetime.now(timezone.utc) - timedelta(seconds=400)
            payload = build_snapshot_envelope(
                "user-service-scores",
                generated_at=old.isoformat(),
                freshness_state="STALE",
                confidence=0.8,
                source_hashes={"users_registry": "advisory"},
                generator="test",
                item_count=0,
                content=[],
            )
            self.write_snapshot(root, "user-service-scores", payload)
            plan = self.plan(root)
            gate = plan["safety"]["intelligence_snapshots"]
            self.assertFalse(gate["stop_required"])
            self.assertIn("user-service-scores", gate["ignored_families"])
            self.assertEqual(len(plan["selected_moves"]), 1)

    def test_pre_planner_refresh_writes_missing_snapshots_before_planning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan_with_args(
                root,
                [
                    "--pre-planner-refresh", "write",
                    "--pre-planner-refresh-command", str(ROOT / "tools" / "v7-intelligence-snapshot-refresh"),
                ],
            )
            gate = plan["safety"]["intelligence_snapshots"]
            refresh = gate["pre_planner_refresh"]
            self.assertEqual(refresh["state"], "REFRESH_SUCCESS")
            self.assertFalse(refresh["stop_required"])
            self.assertTrue(gate["active"])
            self.assertFalse(gate["stop_required"])
            self.assertTrue(snapshot_path(root / "state" / "intelligence", "service-scores").exists())
            self.assertEqual(len(plan["selected_moves"]), 1)

    def test_pre_planner_refresh_reloads_sources_before_gate_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            refresh_command = root / "refresh-and-change-source.py"
            refresh_command.write_text(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env python3
                    import argparse
                    import json
                    import sys
                    from pathlib import Path

                    sys.path.insert(0, {str(ROOT)!r})

                    from admin_core.intelligence_workers import build_all_snapshots, read_json, read_registry, write_snapshots

                    parser = argparse.ArgumentParser()
                    parser.add_argument("--state-dir", required=True)
                    parser.add_argument("--event-dir", required=True)
                    parser.add_argument("--out-dir", required=True)
                    parser.add_argument("--quality-summary-file", required=True)
                    args = parser.parse_args()

                    state = Path(args.state_dir)
                    events = Path(args.event_dir)
                    matrix_path = state / "service-matrix.json"
                    matrix = read_json(matrix_path, {{"items": {{}}}})
                    matrix["items"]["fast"]["services"]["telegram"]["score"] = 99
                    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
                    quality_summary = read_json(Path(args.quality_summary_file), {{"items": {{}}}})
                    result = build_all_snapshots(
                        service_matrix=matrix,
                        quality_summary=quality_summary,
                        service_preferences=read_json(state / "service-preferences.json", {{}}),
                        audit_records=[{{"result": "OK", "operation": {{"terminal_state": "APPLIED"}}}}],
                        switch_records=[{{"result": "OK", "blast_radius": 1}}],
                        rollback_records=[],
                        runtime_state=read_json(state / "v7-state.json", {{}}),
                        users_registry=read_registry(state / "users.registry"),
                        egress_registry=read_registry(state / "egress.registry"),
                        total_users=1,
                        affected_candidates=1,
                    )
                    written = write_snapshots(Path(args.out_dir), result.snapshots)
                    print(json.dumps({{
                        "source_stable": True,
                        "source_consistency_attempts": 1,
                        "source_consistency_errors": [],
                        "snapshot_count": len(result.snapshots),
                        "written": written,
                        "warnings": [],
                        "runtime_behavior_changed": False,
                        "governance_behavior_changed": False,
                        "users_moved": False,
                    }}))
                    """
                ),
                encoding="utf-8",
            )
            refresh_command.chmod(0o755)
            plan = self.plan_with_args(
                root,
                [
                    "--pre-planner-refresh", "write",
                    "--pre-planner-refresh-command", str(refresh_command),
                ],
            )
            gate = plan["safety"]["intelligence_snapshots"]
            refresh = gate["pre_planner_refresh"]
            self.assertEqual(refresh["state"], "REFRESH_SUCCESS")
            self.assertFalse(refresh["stop_required"])
            self.assertIn("source_reload", refresh)
            self.assertIn("service_matrix", refresh["source_reload"]["changed_keys"])
            self.assertFalse(gate["stop_required"])
            self.assertEqual(gate["source_mismatch_families"], [])
            self.assertEqual(len(plan["selected_moves"]), 1)

    def test_pre_planner_refresh_failure_fails_closed_without_selected_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            plan = self.plan_with_args(
                root,
                [
                    "--pre-planner-refresh", "write",
                    "--pre-planner-refresh-command", str(root / "missing-refresh-command"),
                ],
            )
            gate = plan["safety"]["intelligence_snapshots"]
            refresh = gate["pre_planner_refresh"]
            self.assertTrue(refresh["stop_required"])
            self.assertIn(refresh["state"], {"REFRESH_EXCEPTION", "REFRESH_FAILED"})
            self.assertTrue(gate["stop_required"])
            self.assertIn("pre-planner-refresh", gate["stop_families"])
            self.assertEqual(plan["selected_moves"], [])
            self.assertEqual(plan["operation"]["terminal_reason"], "dry_run_intelligence_snapshot_stop_required")

    def test_pre_planner_refresh_is_forbidden_with_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            self.write_good_snapshots(root)
            plan = self.plan_with_args(
                root,
                [
                    "--apply",
                    "--pre-planner-refresh", "write",
                    "--pre-planner-refresh-command", str(ROOT / "tools" / "v7-intelligence-snapshot-refresh"),
                ],
            )
            gate = plan["safety"]["intelligence_snapshots"]
            refresh = gate["pre_planner_refresh"]
            self.assertEqual(refresh["state"], "SKIPPED_APPLY_FORBIDDEN")
            self.assertEqual(refresh["decision"], "pre_planner_refresh_apply_requires_bounded_one_user_scope")
            self.assertTrue(gate["stop_required"])
            self.assertEqual(plan["selected_moves"], [])
            self.assertFalse(plan["apply_result"]["applied"])

    def test_pre_planner_refresh_apply_requires_explicit_bounded_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            self.write_good_snapshots(root)
            planner = self.tool.AutoswitchPlanner(
                self.args_for(
                    root,
                    [
                        "--apply",
                        "--pre-planner-refresh", "write",
                        "--pre-planner-refresh-command", str(ROOT / "tools" / "v7-intelligence-snapshot-refresh"),
                        "--allow-pre-planner-refresh-with-apply",
                        "--user", "10.0.0.2",
                        "--target-egress", "fast",
                        "--max-selected-moves", "1",
                    ],
                )
            )
            fake_proc = type("Proc", (), {"returncode": 0, "stdout": "OK\n"})
            planner._run_switch = lambda *args, **kwargs: fake_proc()
            planner._verify_routes = lambda *args, **kwargs: fake_proc()
            plan = planner.plan()
            plan["apply_result"] = planner.apply(plan)
            planner.finalize_operation(plan)
            gate = plan["safety"]["intelligence_snapshots"]
            refresh = gate["pre_planner_refresh"]
            self.assertEqual(refresh["state"], "REFRESH_SUCCESS")
            self.assertEqual(refresh["decision"], "freshness_refreshed")
            self.assertFalse(refresh["stop_required"])
            self.assertEqual(refresh["apply_refresh_scope"]["user"], "10.0.0.2")
            self.assertEqual(refresh["apply_refresh_scope"]["target_egress"], "fast")
            self.assertEqual(refresh["apply_refresh_scope"]["max_selected_moves"], 1)
            self.assertFalse(gate["stop_required"])
            self.assertEqual(len(plan["selected_moves"]), 1)
            self.assertTrue(plan["apply_result"]["applied"])
            self.assertEqual(len(plan["apply_result"]["results"]), 1)

    def make_expired_trust(self, root: Path) -> None:
        payload = self.load_snapshot(root, "trust-summaries")
        old = datetime.now(timezone.utc) - timedelta(seconds=700)
        payload["generated_at"] = old.isoformat()
        payload["expires_at"] = (old + timedelta(seconds=SNAPSHOT_FAMILIES["trust-summaries"].ttl_seconds)).isoformat()
        self.write_snapshot(root, "trust-summaries", payload)

    def make_unknown_trust(self, root: Path) -> None:
        payload = self.load_snapshot(root, "trust-summaries")
        payload["freshness_state"] = "UNKNOWN"
        self.write_snapshot(root, "trust-summaries", payload)

    def make_low_confidence_trust(self, root: Path) -> None:
        payload = self.load_snapshot(root, "trust-summaries")
        payload["confidence"] = 0.1
        self.write_snapshot(root, "trust-summaries", payload)

    def make_source_hash_mismatch(self, root: Path) -> None:
        payload = self.load_snapshot(root, "service-scores")
        payload["source_hashes"]["service_matrix"] = "bad"
        self.write_snapshot(root, "service-scores", payload)

    def make_stale_runtime_required_trust(self, root: Path) -> None:
        payload = self.load_snapshot(root, "trust-summaries")
        old = datetime.now(timezone.utc) - timedelta(seconds=400)
        payload["generated_at"] = old.isoformat()
        payload["expires_at"] = (old + timedelta(seconds=500)).isoformat()
        payload["freshness_state"] = "STALE"
        self.write_snapshot(root, "trust-summaries", payload)


if __name__ == "__main__":
    unittest.main()
