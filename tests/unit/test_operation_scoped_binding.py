import json
import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path

from admin_core import operation_scoped_binding as binding


class OperationScopedBindingTest(unittest.TestCase):
    def payloads(self):
        selected = {
            "user": "10.7.0.5",
            "from": "awg0",
            "to": "vless",
            "action_class": "single-user governed candidate failover",
            "readiness": "PASS",
            "rollback_readiness": "READY",
            "verification_readiness": "READY",
            "confidence": 0.4,
            "risk": 0.1,
        }
        users = [
            {"ip": "10.7.0.5", "current": "awg0", "enabled": "1"},
            {"ip": "10.7.0.9", "current": "vless", "enabled": "1"},
        ]
        egress = [
            {"id": "awg0", "enabled": "1"},
            {"id": "vless", "enabled": "1"},
            {"id": "awg3", "enabled": "1"},
        ]
        runtime = {
            "updated": "t1",
            "users": [{"ip": "10.7.0.5", "current": "awg0"}, {"ip": "10.7.0.9", "current": "vless"}],
            "user_desired_state": [{"ip": "10.7.0.5", "current": "awg0", "status": "OK"}],
            "egress": {
                "awg0": {"code": "200", "load_status": "OK", "avg_mbps": 20.0, "stability": 0.8},
                "vless": {"code": "200", "load_status": "OK", "avg_mbps": 30.0, "stability": 0.9},
                "awg3": {"code": "500", "load_status": "BLOCKED"},
            },
        }
        suitability = {
            "generated_at": "t1",
            "freshness_state": "FRESH",
            "items": [
                {"user": "10.7.0.5", "runtime_decision_authority": "none_snapshot_only", "candidates": [
                    {"user": "10.7.0.5", "channel": "awg0", "confidence": 0.4, "suitability_score": 70, "recommendation": "keep", "authority": {"runtime": "none"}},
                    {"user": "10.7.0.5", "channel": "vless", "confidence": 0.5, "suitability_score": 80, "recommendation": "prefer", "authority": {"runtime": "none"}},
                ]},
                {"user": "10.7.0.9", "candidates": [{"channel": "awg3", "suitability_score": 99}]},
            ],
        }
        return selected, users, egress, runtime, suitability

    def build(self, selected=None, users=None, egress=None, runtime=None, suitability=None):
        values = list(self.payloads())
        supplied = [selected, users, egress, runtime, suitability]
        values = [new if new is not None else old for new, old in zip(supplied, values)]
        return binding.build_from_payloads(
            selected=values[0], users_registry=values[1], egress_registry=values[2],
            runtime_state=values[3], candidate_suitability=values[4],
            raw_source_hashes={"runtime_state": "raw"}, read_consistency={"stable": True, "attempts": 1},
        )

    def test_same_material_inputs_are_deterministic(self):
        self.assertEqual(self.build()["source_bundle_hash"], self.build()["source_bundle_hash"])

    def test_timestamp_and_continuous_metric_changes_are_non_material(self):
        first = self.build()
        selected, users, egress, runtime, suitability = self.payloads()
        runtime["updated"] = "t2"
        runtime["egress"]["awg0"]["avg_mbps"] = 19.1
        runtime["egress"]["vless"]["stability"] = 0.71
        suitability["generated_at"] = "t2"
        suitability["items"][0]["candidates"][1]["confidence"] = 0.42
        suitability["items"][0]["candidates"][1]["suitability_score"] = 79.1
        selected["confidence"] = 0.42
        selected["risk"] = 0.2
        second = self.build(selected, users, egress, runtime, suitability)
        self.assertEqual(first["source_bundle_hash"], second["source_bundle_hash"])

    def test_unrelated_scope_and_order_are_non_material(self):
        first = self.build()
        selected, users, egress, runtime, suitability = self.payloads()
        users.reverse()
        egress.reverse()
        runtime["users"].reverse()
        runtime["egress"]["awg3"]["code"] = "200"
        suitability["items"].reverse()
        second = self.build(selected, users, egress, runtime, suitability)
        self.assertEqual(first["source_bundle_hash"], second["source_bundle_hash"])

    def test_identity_changes_invalidate(self):
        first = self.build()
        for key, value in (("user", "10.7.0.6"), ("from", "vless"), ("to", "awg3")):
            selected = self.payloads()[0]
            selected[key] = value
            self.assertNotEqual(first["source_bundle_hash"], self.build(selected=selected)["source_bundle_hash"])

    def test_categorical_decision_and_safety_changes_invalidate(self):
        first = self.build()
        selected, users, egress, runtime, suitability = self.payloads()
        runtime["egress"]["vless"]["load_status"] = "BLOCKED"
        self.assertNotEqual(first["source_bundle_hash"], self.build(selected, users, egress, runtime, suitability)["source_bundle_hash"])
        selected, users, egress, runtime, suitability = self.payloads()
        suitability["items"][0]["candidates"][1]["recommendation"] = "reject"
        self.assertNotEqual(first["source_bundle_hash"], self.build(selected, users, egress, runtime, suitability)["source_bundle_hash"])
        selected, users, egress, runtime, suitability = self.payloads()
        selected["verification_readiness"] = "FAIL"
        self.assertNotEqual(first["source_bundle_hash"], self.build(selected, users, egress, runtime, suitability)["source_bundle_hash"])

    def test_missing_identity_and_mixed_generation_fail_closed(self):
        missing = self.build(selected={})
        self.assertEqual(missing["status"], "STOP_SAFE")
        selected, users, egress, runtime, suitability = self.payloads()
        mixed = binding.build_from_payloads(
            selected=selected, users_registry=users, egress_registry=egress,
            runtime_state=runtime, candidate_suitability=suitability,
            read_consistency={"stable": False, "attempts": 2},
        )
        self.assertEqual(mixed["status"], "STOP_SAFE")
        self.assertFalse(mixed["source_bundle_hash"])

    def test_atomic_reader_retries_and_stops_on_persistent_mixed_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            snapshots = state / "intelligence"
            snapshots.mkdir(parents=True)
            selected, users, egress, runtime, suitability = self.payloads()
            (state / "users.registry").write_text("ip=10.7.0.5 current=awg0 enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=awg0 enabled=1\nid=vless enabled=1\n", encoding="utf-8")
            (state / "v7-state.json").write_text(json.dumps(runtime), encoding="utf-8")
            suitability_path = snapshots / "candidate-suitability-summary.json"
            suitability_path.write_text(json.dumps(suitability), encoding="utf-8")

            stable = binding.read_binding(state_dir=state, snapshot_root=snapshots, selected=selected)
            self.assertEqual(stable["status"], "BOUND")

            def mutate(attempt):
                payload = dict(suitability)
                payload["generated_at"] = "changed-" + ("x" * attempt)
                suitability_path.write_text(json.dumps(payload), encoding="utf-8")

            mixed = binding.read_binding(
                state_dir=state, snapshot_root=snapshots, selected=selected,
                max_attempts=2, after_read_hook=mutate,
            )
            self.assertEqual(mixed["status"], "STOP_SAFE")
            self.assertTrue(mixed["fail_closed_on_mixed_generation"])

    def test_raw_provenance_is_preserved_separately(self):
        result = self.build()
        self.assertEqual(result["raw_source_hashes"], {"runtime_state": "raw"})
        self.assertNotEqual(result["source_hashes"].get("runtime_state"), "raw")

    def test_low_level_gate_uses_shared_builder(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-users-autoswitch"
        loader = importlib.machinery.SourceFileLoader("v7_users_autoswitch_binding_test", str(tool_path))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            snapshots = state / "intelligence"
            snapshots.mkdir(parents=True)
            selected, users, egress, runtime, suitability = self.payloads()
            (state / "users.registry").write_text("ip=10.7.0.5 current=awg0 enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=awg0 enabled=1\nid=vless enabled=1\n", encoding="utf-8")
            (state / "v7-state.json").write_text(json.dumps(runtime), encoding="utf-8")
            (snapshots / "candidate-suitability-summary.json").write_text(json.dumps(suitability), encoding="utf-8")
            planner = tool.AutoswitchPlanner.__new__(tool.AutoswitchPlanner)
            planner.state_dir = state
            planner.intelligence_snapshot_root = snapshots
            result = planner._operation_scoped_source_binding({"selected_moves": [selected]})
            direct = binding.read_binding(state_dir=state, snapshot_root=snapshots, selected=selected)
        self.assertEqual(result["source_hashes"], direct["source_hashes"])
        self.assertEqual(result["schema_version"], binding.SCHEMA_VERSION)


if __name__ == "__main__":
    unittest.main()
