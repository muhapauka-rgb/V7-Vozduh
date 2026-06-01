import json
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from admin_core.hybrid_approval import (
    SCHEMA_VERSION,
    build_expected,
    execute_record,
    proposal_fingerprint,
    runtime_state,
    utc_now,
    validate_packet,
)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


class V7HybridApprovalTest(unittest.TestCase):
    def make_state(self, root):
        state = root / "state"
        state.mkdir()
        (state / "users.registry").write_text(
            "\n".join([
                "ip=10.7.0.16 current=vless table=1014 enabled=1",
                "ip=10.7.0.17 current=awg0 table=1015 enabled=1",
            ])
            + "\n",
            encoding="utf-8",
        )
        (state / "egress.registry").write_text(
            "\n".join([
                "id=vless protocol=vless enabled=1 role=GLOBAL_STABLE soft_limit=5 hard_limit=10 exclude_route_classes=DIRECT_RU,TRUSTED_RU_SENSITIVE",
                "id=awg3 protocol=amneziawg enabled=1 role=GLOBAL_STABLE soft_limit=5 hard_limit=10 exclude_route_classes=DIRECT_RU,TRUSTED_RU_SENSITIVE",
                "id=exec-only protocol=amneziawg enabled=1 role=EXECUTION_ONLY soft_limit=1 hard_limit=1 manual_only=1 autoswitch_allowed=false exclude_route_classes=DIRECT_RU,TRUSTED_RU_SENSITIVE",
            ])
            + "\n",
            encoding="utf-8",
        )
        write_json(state / "autoswitch-safety.json", {"status": "ok"})
        return state

    def proposal(self, target="awg3", budget=1):
        return {
            "tool": "v7-autoswitch-proposal-cap",
            "budget": budget,
            "proposal_count": 1,
            "proposal_moves": [
                {
                    "user_ip": "10.7.0.16",
                    "action": "switch",
                    "move_type": "failover",
                    "current_egress": "vless",
                    "recommended_egress": target,
                    "route_class": "GLOBAL_STABLE",
                }
            ],
        }

    def packet(self, proposal, runtime, **overrides):
        now = utc_now()
        packet = {
            "schema_version": SCHEMA_VERSION,
            "packet_id": "pkt_z2_test",
            "approval_id": "appr_z2_test",
            "approval_mode": "HYBRID",
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(minutes=15)).isoformat(),
            "policy": {
                "approval_mode": "HYBRID",
                "budget": 1,
                "allowed_users": ["10.7.0.16"],
                "route_class": "GLOBAL_STABLE",
                "target_class": "BEST_HEALTHY",
                "trust_class": "RU_SENSITIVE_EXCLUDED",
                "policy_class": "AUTOSWITCH_ALLOWED",
                "capacity_rule": "NOT_HARD_FULL",
                "rollback": {"user_ip": "10.7.0.16", "target": "vless"},
            },
            "target_approval": {},
            "expected": {},
        }
        for key, value in overrides.items():
            packet[key] = value
        packet["expected"] = build_expected(packet, proposal, runtime)
        return packet

    def test_policy_approval_allows_same_class_one_user_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            runtime = runtime_state(state)
            proposal = self.proposal()
            packet = self.packet(proposal, runtime)

            result = validate_packet(packet, proposal, runtime, root / "audit.jsonl")

        self.assertTrue(result["allow"])
        self.assertEqual(result["verdict"], "ALLOW_HYBRID_BOUNDED_AUTONOMY")
        self.assertFalse(result["substitution"]["target_approval_required"])

    def test_execution_only_target_requires_exact_target_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            runtime = runtime_state(state)
            proposal = self.proposal(target="exec-only")
            packet = self.packet(proposal, runtime)

            result = validate_packet(packet, proposal, runtime, root / "audit.jsonl")

            packet["target_approval"] = {"exact_target": "exec-only"}
            packet["expected"] = build_expected(packet, proposal, runtime)
            exact = validate_packet(packet, proposal, runtime, root / "audit.jsonl")

        self.assertFalse(result["allow"])
        self.assertIn("target_approval_required_for_high_risk_or_class_change", result["errors"])
        self.assertTrue(exact["allow"])
        self.assertTrue(exact["substitution"]["target_approval_required"])

    def test_budget_expiry_hash_mismatch_and_replay_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = self.make_state(root)
            runtime = runtime_state(state)
            proposal = self.proposal()
            packet = self.packet(proposal, runtime)
            expired = dict(packet)
            expired["expires_at"] = (utc_now() - timedelta(seconds=1)).isoformat()
            stale = dict(packet)
            stale["expected"] = dict(packet["expected"])
            stale["expected"]["proposal_fingerprint"] = "bad"
            budget_two = self.proposal(budget=2)
            budget_packet = self.packet(budget_two, runtime)

            audit = root / "audit.jsonl"
            first = execute_record(packet, proposal, runtime, audit)
            replay = validate_packet(packet, proposal, runtime, audit)

        self.assertFalse(validate_packet(expired, proposal, runtime, root / "expired.jsonl")["allow"])
        self.assertFalse(validate_packet(stale, proposal, runtime, root / "stale.jsonl")["allow"])
        self.assertFalse(validate_packet(budget_packet, budget_two, runtime, root / "budget.jsonl")["allow"])
        self.assertTrue(first["validation"]["allow"])
        self.assertFalse(replay["allow"])
        self.assertIn("approval_replay", replay["errors"])
        self.assertEqual(proposal_fingerprint(proposal), packet["expected"]["proposal_fingerprint"])


if __name__ == "__main__":
    unittest.main()
