import json
import secrets
from datetime import datetime, timezone
from pathlib import Path


packet = json.loads(Path("medium_batch_preparation_evidence/phase6_medium_batch_approval_packet.json").read_text())
recheck = json.loads(Path("medium_batch_preparation_evidence/phase6_packet_recheck_only.json").read_text())

expected = packet.get("expected") or {}
constraints = packet.get("constraints") or {}
rollback_manifest = packet.get("rollback_manifest") or {}
checks = (recheck.get("recheck") or {}).get("checks") or {}

barrier = {
    "schema_version": 1,
    "enabled": True,
    "owner": "admin_core/operator_execution.py",
    "reason": "review-only MEDIUM_BATCH restore barrier preview",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "expires_at": "2000-01-01T00:00:00+00:00",
    "allow_post_ttl_apply": False,
    "generation_clearance": True,
    "generation_token": secrets.token_hex(16),
    "clearance_expires_at": packet.get("expires_at", ""),
    "approval_id": packet.get("approval_id", ""),
    "packet_id": packet.get("packet_id", ""),
    "operation_id": packet.get("operation_id", ""),
    "rollback_manifest_id": rollback_manifest.get("rollback_manifest_id", ""),
    "clearance_generation_id": expected.get("generation_id", ""),
    "clearance_max_selected_moves": constraints.get("selected_move_budget", 0),
    "clearance_expected_selected_moves": expected.get("selected_move_count", 0),
    "allowed_users": constraints.get("allowed_users") or [],
    "allowed_targets": constraints.get("allowed_targets") or [],
    "approved_selected_moves_hash": expected.get("selected_move_hash", ""),
    "approved_atomic_execution_envelope_id": expected.get("atomic_execution_envelope_id", ""),
    "approved_atomic_execution_envelope_hash": expected.get("atomic_execution_envelope_hash", ""),
    "approved_source_bundle_hash": expected.get("source_bundle_hash", ""),
    "approved_snapshot_bundle_hash": expected.get("snapshot_bundle_hash", ""),
    "approved_source_hashes": expected.get("source_hashes") or {},
    "review_only": True,
    "production_write_performed": False,
    "recheck_verdict": (recheck.get("recheck") or {}).get("verdict", ""),
    "recheck_allow": bool((recheck.get("recheck") or {}).get("allow")),
    "users_registry_hash": checks.get("users_registry_hash", ""),
    "egress_registry_hash": checks.get("egress_registry_hash", ""),
}

print(json.dumps(barrier, ensure_ascii=False, indent=2, sort_keys=True))
