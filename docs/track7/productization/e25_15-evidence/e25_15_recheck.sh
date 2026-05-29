#!/usr/bin/env bash
set -u
. /tmp/e25_15_remote_lib.sh

OUT="${OUT:-/tmp/e25_15_execution_time_recheck.md}"

readiness_pretty > /tmp/e25_15_recheck_readiness.pretty
readiness_json > /tmp/e25_15_recheck_readiness.json
v7-restore-settle-gate --pre-restore --state-dir /tmp/e25_15_settle_samples --pretty > /tmp/e25_15_recheck_restore_settle.pretty
v7-restore-settle-gate --pre-restore --state-dir /tmp/e25_15_settle_samples --json > /tmp/e25_15_recheck_restore_settle.json

packet_hash_expected="$(packet_field packet_hash)"
packet_hash_actual_value="$(packet_hash_actual)"
packet_users_hash="$(packet_field fresh_runtime_truth.users_registry_hash)"
packet_egress_hash="$(packet_field fresh_runtime_truth.egress_registry_hash)"
packet_selected_hash="$(packet_field fresh_runtime_truth.selected_moves_hash)"
packet_expired="$(packet_non_expired)"
current_users_hash="$(hash_file "$STATE/users.registry")"
current_egress_hash="$(hash_file "$STATE/egress.registry")"
current_selected_hash="$(selected_moves_hash)"
readiness_status="$(awk -F= '/^approval_status=/{print $2}' /tmp/e25_15_recheck_readiness.pretty)"
selected_target="$(awk -F= '/^selected_target=/{print $2}' /tmp/e25_15_recheck_readiness.pretty)"
settle_status="$(awk -F= '/^gate_status=/{print $2}' /tmp/e25_15_recheck_restore_settle.pretty)"
cc="$(field_for_ip "$CAND" current)"
dc="$(field_for_ip "$DRIFT_USER" current)"
tu="$(target_users_count)"
sc="$(selected_moves_count)"
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
[ "$dc" = "vless" ] || { authorized=false; reasons+=("drift_user_changed"); }
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
  echo "# E25.15 Execution-Time Recheck"
  echo
  echo "date_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "packet_id=$(packet_field packet_id)"
  echo "approval_id=$(packet_field approval_id)"
  echo "operation_id=$(packet_field operation_id)"
  echo "packet_non_expired=$packet_expired"
  echo "packet_hash_expected=$packet_hash_expected"
  echo "packet_hash_actual=$packet_hash_actual_value"
  echo "packet_users_registry_hash=$packet_users_hash"
  echo "users_registry_hash=$current_users_hash"
  echo "packet_egress_registry_hash=$packet_egress_hash"
  echo "egress_registry_hash=$current_egress_hash"
  echo "packet_selected_moves_hash=$packet_selected_hash"
  echo "selected_moves_hash=$current_selected_hash"
  echo "candidate_row=$(row_for_ip "$CAND")"
  echo "drift_row=$(row_for_ip "$DRIFT_USER")"
  echo "target_row=$(target_row)"
  echo "target_users=$tu"
  echo "selected_moves_count=$sc"
  echo "hidden_movers_count=$hc"
  echo "runtime_checkers_ok=$co"
  echo
  echo "## Readiness"
  cat /tmp/e25_15_recheck_readiness.pretty
  echo
  echo "## Restore Settle"
  cat /tmp/e25_15_recheck_restore_settle.pretty
  echo
  echo "## Authorization"
  echo "execution_authorized=$authorized"
  if [ "${#reasons[@]}" -gt 0 ]; then printf 'authorization_reasons=%s\n' "${reasons[*]}"; else echo "authorization_reasons=none"; fi
} > "$OUT"

echo "$authorized"
