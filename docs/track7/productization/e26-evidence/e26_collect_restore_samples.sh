#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-/tmp/e26_restore_samples}"
STATE="/opt/v7/egress/state"
CANDIDATE="10.7.0.11"
DRIFT="10.7.0.16"
TARGET="amneziawg-exec-20260528-10-8-1-14"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

sample() {
  local idx="$1"
  local out="$OUT_DIR/sample-${idx}.json"
  local ts host users_hash egress_hash candidate_row drift_row candidate_current candidate_table drift_current drift_table target_users selected_count selected_hash
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  host="$(hostname)"
  users_hash="$(sha256sum "$STATE/users.registry" | awk '{print $1}')"
  egress_hash="$(sha256sum "$STATE/egress.registry" | awk '{print $1}')"
  candidate_row="$(grep -E "ip=${CANDIDATE} " "$STATE/users.registry" || true)"
  drift_row="$(grep -E "ip=${DRIFT} " "$STATE/users.registry" || true)"
  candidate_current="$(printf "%s\n" "$candidate_row" | sed -n 's/.*current=\([^ ]*\).*/\1/p')"
  candidate_table="$(printf "%s\n" "$candidate_row" | sed -n 's/.*table=\([^ ]*\).*/\1/p')"
  drift_current="$(printf "%s\n" "$drift_row" | sed -n 's/.*current=\([^ ]*\).*/\1/p')"
  drift_table="$(printf "%s\n" "$drift_row" | sed -n 's/.*table=\([^ ]*\).*/\1/p')"
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
  v7-reconcile-check >/tmp/e26_reconcile.out 2>/tmp/e26_reconcile.err && reconcile_ok=true || reconcile_ok=false
  v7-user-route-check >/tmp/e26_user_route.out 2>/tmp/e26_user_route.err && user_route_ok=true || user_route_ok=false
  v7-killswitch-check >/tmp/e26_killswitch.out 2>/tmp/e26_killswitch.err && killswitch_ok=true || killswitch_ok=false
  v7-provisioning-reconcile-check >/tmp/e26_provisioning.out 2>/tmp/e26_provisioning.err && provisioning_ok=true || provisioning_ok=false

  python3 - "$out" \
    "$ts" "$host" "$users_hash" "$egress_hash" \
    "$candidate_current" "$candidate_table" "$drift_current" "$drift_table" \
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
    candidate_current,
    candidate_table,
    drift_current,
    drift_table,
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
    "source": "vps-live-e26-post-movement-review",
    "timestamp": ts,
    "hostname": host,
    "candidate_user": "10.7.0.11",
    "candidate_current_egress": candidate_current,
    "candidate_table": candidate_table,
    "drift_user": "10.7.0.16",
    "drift_user_current_egress": drift_current,
    "drift_user_table": drift_table,
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
    "egress_1_eligible": candidate_current == "1",
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
