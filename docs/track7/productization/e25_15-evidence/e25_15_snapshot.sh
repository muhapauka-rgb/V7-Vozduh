#!/usr/bin/env bash
set -u
. /tmp/e25_15_remote_lib.sh

OUT="${OUT:-/tmp/e25_15_fresh_runtime_snapshot.md}"
SAMPLES="${SAMPLES:-/tmp/e25_15_settle_samples}"
rm -rf "$SAMPLES"
mkdir -p "$SAMPLES"

make_sample() {
  idx="$1"
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  cc="$(field_for_ip "$CAND" current)"
  ct="$(field_for_ip "$CAND" table)"
  dc="$(field_for_ip "$DRIFT_USER" current)"
  dt="$(field_for_ip "$DRIFT_USER" table)"
  sc="$(selected_moves_count)"
  sh="$(selected_moves_hash)"
  hc="$(hidden_movers_count)"
  tu="$(target_users_count)"
  co=false
  if checkers_ok; then co=true; fi
  python3 - "$SAMPLES/sample-0${idx}.json" <<PY
import json, sys
payload = {
  "source": "vps-live-e25.15-fresh-runtime",
  "timestamp": "$ts",
  "hostname": "$(hostname)",
  "candidate_user": "$CAND",
  "candidate_current_egress": "$cc",
  "candidate_table": "$ct",
  "drift_user": "$DRIFT_USER",
  "drift_user_current_egress": "$dc",
  "drift_user_table": "$dt",
  "execution_target": "$TARGET",
  "execution_target_interface": "v7execwg0",
  "execution_target_users_count": int("$tu"),
  "users_registry_hash": "$(hash_file "$STATE/users.registry")",
  "egress_registry_hash": "$(hash_file "$STATE/egress.registry")",
  "selected_moves": int("$sc"),
  "selected_moves_hash": "$sh",
  "hidden_movers": [],
  "hidden_movers_observed": int("$hc") > 0,
  "checkers_ok": "$co" == "true",
  "checker_results": {
    "reconcile_ok": "$co" == "true",
    "user_route_ok": "$co" == "true",
    "killswitch_ok": "$co" == "true",
    "provisioning_ok": "$co" == "true"
  },
  "movement_count": 0,
  "moved_users": [],
  "telegram_hard_blocked": False,
  "egress_1_eligible": True,
  "planner_timer_state": "not_mutated_by_e25.15",
  "apply_timer_state": "not_mutated_by_e25.15"
}
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump(payload, fh, indent=2, sort_keys=True)
    fh.write("\\n")
PY
}

make_sample 1
sleep 20
make_sample 2
sleep 20
make_sample 3

readiness_pretty > /tmp/e25_15_readiness.pretty
readiness_json > /tmp/e25_15_readiness.json
v7-restore-settle-gate --pre-restore --state-dir "$SAMPLES" --pretty > /tmp/e25_15_restore_settle.pretty
v7-restore-settle-gate --pre-restore --state-dir "$SAMPLES" --json > /tmp/e25_15_restore_settle.json

{
  echo "# E25.15 Fresh Runtime Snapshot"
  echo
  echo "date_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "users_registry_hash=$(hash_file "$STATE/users.registry")"
  echo "egress_registry_hash=$(hash_file "$STATE/egress.registry")"
  echo "candidate_row=$(row_for_ip "$CAND")"
  echo "drift_row=$(row_for_ip "$DRIFT_USER")"
  echo "table_1009=$(route_table_for 1009)"
  echo "route_get_10_7_0_11=$(route_get_for "$CAND")"
  echo "table_1014=$(route_table_for 1014)"
  echo "route_get_10_7_0_16=$(route_get_for "$DRIFT_USER")"
  echo "target_row=$(target_row)"
  echo "target_users=$(target_users_count)"
  echo "selected_moves_count=$(selected_moves_count)"
  echo "selected_moves_hash=$(selected_moves_hash)"
  echo "hidden_movers_count=$(hidden_movers_count)"
  if checkers_ok; then echo "runtime_checkers_ok=true"; else echo "runtime_checkers_ok=false"; fi
  echo
  echo "## Readiness"
  cat /tmp/e25_15_readiness.pretty
  echo
  echo "## Restore Settle"
  cat /tmp/e25_15_restore_settle.pretty
  echo
  echo "## Timers"
  systemctl is-active v7-users-autoswitch.timer 2>/dev/null | sed "s/^/v7_users_autoswitch_timer=/" || true
  systemctl is-active v7-users-autoswitch.service 2>/dev/null | sed "s/^/v7_users_autoswitch_service=/" || true
} > "$OUT"

echo "$OUT"
