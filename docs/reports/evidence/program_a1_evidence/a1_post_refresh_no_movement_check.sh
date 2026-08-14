#!/usr/bin/env bash
set +e
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

echo "=== NO_MOVEMENT_POST_REFRESH ==="
date -Is

echo "=== REGISTRY HASHES ==="
sha256sum /opt/v7/egress/state/users.registry /opt/v7/egress/state/egress.registry 2>/dev/null || true

echo "=== RECENT_SWITCH_LOG ==="
if command -v v7-switch-log >/dev/null 2>&1; then
  v7-switch-log 2>/dev/null | tail -n 80
else
  echo "v7-switch-log_missing"
fi

echo "=== RECENT_AUDIT_RUNTIME_OPERATION ==="
tail -n 80 /opt/v7/audit/audit.jsonl 2>/dev/null | grep 'runtime_operation_terminal' || true

echo "=== HIDDEN_MOVERS_AFTER ==="
pgrep -af 'v7-user-switch|v7-users-autoswitch.*--apply|v7-routing-sync|v7-rollback-last-change|v7-policy-live-rollback' || true
