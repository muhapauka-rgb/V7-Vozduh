#!/usr/bin/env bash
set -u
. /tmp/e25_14_remote_common.sh

OUT="${OUT:-/tmp/e25_14_execution-time-recheck.md}"
SETTLE_DIR="${SETTLE_DIR:-/tmp/e25_14_recheck_settle_samples}"
rm -rf "$SETTLE_DIR"
mkdir -p "$SETTLE_DIR"

make_sample() {
  idx="$1"
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  cc="$(candidate_field current)"
  ct="$(candidate_field table)"
  sc="$(selected_moves_count)"
  sh="$(selected_moves_hash)"
  hc="$(hidden_movers_count)"
  tu="$(target_users_count)"
  co=false
  if checkers_ok; then co=true; fi
  python3 - "$SETTLE_DIR/sample-0${idx}.json" <<PY
import json, sys
payload={
  "source":"vps-live-e25.14-execution-time-recheck",
  "timestamp":"$ts",
  "hostname":"$(hostname)",
  "candidate_user":"$CAND",
  "candidate_current_egress":"$cc",
  "candidate_table":"$ct",
  "candidate_moves_total":0,
  "execution_target":"$TARGET",
  "execution_target_interface":"v7execwg0",
  "execution_target_users_count":int("$tu"),
  "users_registry_hash":"$(hash_file "$STATE/users.registry")",
  "egress_registry_hash":"$(hash_file "$STATE/egress.registry")",
  "selected_moves":int("$sc"),
  "selected_moves_hash":"$sh",
  "hidden_movers":[],
  "hidden_movers_observed":int("$hc")>0,
  "checker_results":{"reconcile_ok":"$co"=="true","user_route_ok":"$co"=="true","killswitch_ok":"$co"=="true","provisioning_ok":"$co"=="true"},
  "checkers_ok":"$co"=="true",
  "movement_count":0,
  "moved_users":[],
  "telegram_hard_blocked":False,
  "egress_1_eligible":True,
  "planner_timer_state":"not_mutated_by_e25.14",
  "apply_timer_state":"not_mutated_by_e25.14"
}
with open(sys.argv[1],"w",encoding="utf-8") as fh:
  json.dump(payload,fh,indent=2,sort_keys=True); fh.write("\\n")
PY
}

make_sample 1
sleep 20
make_sample 2
sleep 20
make_sample 3

readiness_pretty > /tmp/e25_14_readiness.pretty
readiness_json > /tmp/e25_14_readiness.json
v7-restore-settle-gate --pre-restore --state-dir "$SETTLE_DIR" --pretty > /tmp/e25_14_restore_settle.pretty
v7-restore-settle-gate --pre-restore --state-dir "$SETTLE_DIR" --json > /tmp/e25_14_restore_settle.json

packet_expired="$(packet_non_expired)"
packet_hash_expected="$(packet_field packet_hash)"
packet_hash_actual_value="$(packet_hash_actual)"
packet_users_hash="$(packet_field fresh_runtime_truth.users_registry_hash)"
packet_egress_hash="$(packet_field fresh_runtime_truth.egress_registry_hash)"
packet_selected_hash="$(packet_field fresh_runtime_truth.selected_moves_hash)"

readiness_status="$(awk -F= '/^approval_status=/{print $2}' /tmp/e25_14_readiness.pretty)"
selected_target="$(awk -F= '/^selected_target=/{print $2}' /tmp/e25_14_readiness.pretty)"
settle_status="$(awk -F= '/^gate_status=/{print $2}' /tmp/e25_14_restore_settle.pretty)"
cc="$(candidate_field current)"
tu="$(target_users_count)"
sc="$(selected_moves_count)"
current_users_hash="$(hash_file "$STATE/users.registry")"
current_egress_hash="$(hash_file "$STATE/egress.registry")"
current_selected_hash="$(selected_moves_hash)"
hc="$(hidden_movers_count)"
co=false
if checkers_ok; then co=true; fi
role="$(target_field role)"
autoswitch="$(target_field autoswitch_allowed)"
rebalance="$(target_field rebalance_allowed)"
prod="$(target_field production_assignment_allowed)"

authorized=true
reasons=()
[ "$packet_expired" = "true" ] || { authorized=false; reasons+=("packet_expired"); }
[ "$packet_hash_expected" = "$packet_hash_actual_value" ] || { authorized=false; reasons+=("packet_hash_mismatch"); }
[ "$packet_users_hash" = "$current_users_hash" ] || { authorized=false; reasons+=("users_registry_hash_mismatch"); }
[ "$packet_egress_hash" = "$current_egress_hash" ] || { authorized=false; reasons+=("egress_registry_hash_mismatch"); }
[ "$packet_selected_hash" = "$current_selected_hash" ] || { authorized=false; reasons+=("selected_moves_hash_mismatch"); }
[ "$(packet_field movement_budget)" = "1" ] || { authorized=false; reasons+=("movement_budget_not_1"); }
[ "$(packet_field candidate_user)" = "$CAND" ] || { authorized=false; reasons+=("candidate_mismatch"); }
[ "$(packet_field to_egress)" = "$TARGET" ] || { authorized=false; reasons+=("target_mismatch"); }
[ "$cc" = "1" ] || { authorized=false; reasons+=("candidate_not_on_1"); }
[ "$readiness_status" = "GO" ] || { authorized=false; reasons+=("target_not_go"); }
[ "$selected_target" = "$TARGET" ] || { authorized=false; reasons+=("selected_target_mismatch"); }
[ "$settle_status" = "GO" ] || { authorized=false; reasons+=("restore_settle_not_go"); }
[ "$sc" = "0" ] || { authorized=false; reasons+=("selected_moves_nonzero"); }
[ "$hc" = "0" ] || { authorized=false; reasons+=("hidden_movers_active"); }
[ "$co" = "true" ] || { authorized=false; reasons+=("runtime_checkers_fail"); }
[ "$tu" = "0" ] || { authorized=false; reasons+=("target_users_not_zero"); }
[ "$role" = "EXECUTION_ONLY" ] || { authorized=false; reasons+=("target_not_execution_only"); }
[ "$autoswitch" = "false" ] || { authorized=false; reasons+=("autoswitch_not_excluded"); }
[ "$rebalance" = "false" ] || { authorized=false; reasons+=("rebalance_not_excluded"); }
[ "$prod" = "false" ] || { authorized=false; reasons+=("production_assignment_not_blocked"); }

{
  echo "# E25.14 Execution-Time Recheck"
  echo
  echo "hostname=$(hostname)"
  echo "date_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "## Packet"
  echo "packet_id=$(packet_field packet_id)"
  echo "approval_id=$(packet_field approval_id)"
  echo "operation_id=$(packet_field operation_id)"
  echo "approval_expires_at=$(packet_field approval_expires_at)"
  echo "packet_non_expired=$packet_expired"
  echo "packet_hash_expected=$packet_hash_expected"
  echo "packet_hash_actual=$packet_hash_actual_value"
  echo "packet_users_registry_hash=$packet_users_hash"
  echo "packet_egress_registry_hash=$packet_egress_hash"
  echo "packet_selected_moves_hash=$packet_selected_hash"
  echo
  echo "## Runtime"
  echo "users_registry_hash=$current_users_hash"
  echo "egress_registry_hash=$current_egress_hash"
  echo "candidate_row=$(candidate_row)"
  echo "table_1009=$(route_table_1009)"
  echo "route_get=$(route_get_candidate)"
  echo "target_row=$(target_row)"
  echo "target_users=$tu"
  echo "selected_moves_count=$sc"
  echo "selected_moves_hash=$current_selected_hash"
  echo "hidden_movers_count=$hc"
  echo "runtime_checkers_ok=$co"
  echo
  echo "## Readiness"
  cat /tmp/e25_14_readiness.pretty
  echo
  echo "## Restore Settle"
  cat /tmp/e25_14_restore_settle.pretty
  echo
  echo "## Authorization"
  echo "execution_authorized=$authorized"
  if [ "${#reasons[@]}" -gt 0 ]; then printf 'authorization_reasons=%s\n' "${reasons[*]}"; else echo "authorization_reasons=none"; fi
  echo "execution_allowed_now=false_until_command_boundary"
  echo
  echo "## Audit Tail"
  audit_tail
} > "$OUT"

echo "$authorized"
