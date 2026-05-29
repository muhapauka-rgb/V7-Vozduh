#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-/tmp/e27_restore_samples}"
STATE="/opt/v7/egress/state"
TARGET="amneziawg-exec-20260528-10-8-1-14"
USER_A="10.7.0.11"
USER_B="10.7.0.12"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

sample() {
  local idx="$1"
  local out="$OUT_DIR/sample-${idx}.json"
  local ts host users_hash egress_hash row_a row_b current_a current_b table_a table_b target_users selected_count selected_hash
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  host="$(hostname)"
  users_hash="$(sha256sum "$STATE/users.registry" | awk '{print $1}')"
  egress_hash="$(sha256sum "$STATE/egress.registry" | awk '{print $1}')"
  row_a="$(grep -E "ip=${USER_A} " "$STATE/users.registry" || true)"
  row_b="$(grep -E "ip=${USER_B} " "$STATE/users.registry" || true)"
  current_a="$(printf "%s\n" "$row_a" | sed -n 's/.*current=\([^ ]*\).*/\1/p')"
  current_b="$(printf "%s\n" "$row_b" | sed -n 's/.*current=\([^ ]*\).*/\1/p')"
  table_a="$(printf "%s\n" "$row_a" | sed -n 's/.*table=\([^ ]*\).*/\1/p')"
  table_b="$(printf "%s\n" "$row_b" | sed -n 's/.*table=\([^ ]*\).*/\1/p')"
  target_users="$(grep -c "current=${TARGET}" "$STATE/users.registry" || true)"
  if [ -d "$STATE/selected_moves" ]; then
    selected_count="$(find "$STATE/selected_moves" -type f | wc -l | tr -d ' ')"
    if [ "$selected_count" = "0" ]; then
      selected_hash="NONE"
    else
      selected_hash="$(find "$STATE/selected_moves" -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')"
    fi
  else
    selected_count="0"
    selected_hash="NONE"
  fi

  local hidden
  hidden="$(ps -eo pid,ppid,etime,command | grep -E 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' | grep -v grep || true)"

  local reconcile_ok user_route_ok killswitch_ok provisioning_ok
  v7-reconcile-check >/tmp/e27_reconcile.out 2>/tmp/e27_reconcile.err && reconcile_ok=true || reconcile_ok=false
  v7-user-route-check >/tmp/e27_user_route.out 2>/tmp/e27_user_route.err && user_route_ok=true || user_route_ok=false
  v7-killswitch-check >/tmp/e27_killswitch.out 2>/tmp/e27_killswitch.err && killswitch_ok=true || killswitch_ok=false
  v7-provisioning-reconcile-check >/tmp/e27_provisioning.out 2>/tmp/e27_provisioning.err && provisioning_ok=true || provisioning_ok=false

  python3 - "$out" \
    "$ts" "$host" "$users_hash" "$egress_hash" \
    "$current_a" "$table_a" "$current_b" "$table_b" \
    "$target_users" "$selected_count" "$selected_hash" \
    "$hidden" "$reconcile_ok" "$user_route_ok" "$killswitch_ok" "$provisioning_ok" <<'PY'
import json
import sys

(
    out,
    ts,
    host,
    users_hash,
    egress_hash,
    current_a,
    table_a,
    current_b,
    table_b,
    target_users,
    selected_count,
    selected_hash,
    hidden,
    reconcile_ok,
    user_route_ok,
    killswitch_ok,
    provisioning_ok,
) = sys.argv[1:]

hidden_lines = [line for line in hidden.splitlines() if line.strip()]
checkers = {
    "reconcile_ok": reconcile_ok == "true",
    "user_route_ok": user_route_ok == "true",
    "killswitch_ok": killswitch_ok == "true",
    "provisioning_ok": provisioning_ok == "true",
}
doc = {
    "source": "vps-live-e27-two-user-preparation",
    "timestamp": ts,
    "hostname": host,
    "candidate_user_A": "10.7.0.11",
    "candidate_user_A_current_egress": current_a,
    "candidate_user_A_table": table_a,
    "candidate_user_B": "10.7.0.12",
    "candidate_user_B_current_egress": current_b,
    "candidate_user_B_table": table_b,
    "execution_target": "amneziawg-exec-20260528-10-8-1-14",
    "execution_target_users_count": int(target_users),
    "users_registry_hash": users_hash,
    "egress_registry_hash": egress_hash,
    "selected_moves": int(selected_count),
    "selected_moves_hash": selected_hash,
    "hidden_movers": hidden_lines,
    "hidden_movers_observed": bool(hidden_lines),
    "checker_results": checkers,
    "checkers_ok": all(checkers.values()),
    "telegram_hard_blocked": False,
    "egress_1_eligible": current_a == "1" and current_b == "1",
    "movement_count": 0,
    "moved_users": [],
}
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, sort_keys=True)
    f.write("\n")
PY
}

sample 01
sleep 25
sample 02
sleep 25
sample 03

v7-restore-settle-gate --pre-restore --state-dir "$OUT_DIR" --pretty > "$OUT_DIR/restore-settle.pretty"
v7-restore-settle-gate --pre-restore --state-dir "$OUT_DIR" --json > "$OUT_DIR/restore-settle.json"
