#!/usr/bin/env bash
set -u
. /tmp/e25_15_remote_lib.sh

OUT="${OUT:-/tmp/e25_15_forward_execution.md}"
BEFORE_USERS=/tmp/e25_15_users_before_forward.registry
AFTER_USERS=/tmp/e25_15_users_after_forward.registry
BEFORE_ROUTE=/tmp/e25_15_route_before_forward.txt
AFTER_ROUTE=/tmp/e25_15_route_after_forward.txt
STDOUT=/tmp/e25_15_forward_stdout.txt
STDERR=/tmp/e25_15_forward_stderr.txt

cp "$STATE/users.registry" "$BEFORE_USERS"
route_table_for 1009 > "$BEFORE_ROUTE"
before_route_get="$(route_get_for "$CAND")"
before_target_users="$(target_users_count)"
before_drift_row="$(row_for_ip "$DRIFT_USER")"

ts_start="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
set +e
v7-user-switch "$CAND" "$TARGET" >"$STDOUT" 2>"$STDERR"
rc=$?
set -e
ts_end="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cp "$STATE/users.registry" "$AFTER_USERS"
route_table_for 1009 > "$AFTER_ROUTE"
after_route_get="$(route_get_for "$CAND")"
after_target_users="$(target_users_count)"
after_candidate_current="$(field_for_ip "$CAND" current)"
after_drift_row="$(row_for_ip "$DRIFT_USER")"
after_selected="$(selected_moves_count)"
after_hidden="$(hidden_movers_count)"
after_checkers=false
if checkers_ok; then after_checkers=true; fi

audit_hash="$(write_audit_event forward_movement "rc=$rc;from=1;to=$TARGET;candidate_after=$after_candidate_current")"

{
  echo "# E25.15 Forward Execution"
  echo
  echo "timestamp_start_utc=$ts_start"
  echo "timestamp_end_utc=$ts_end"
  echo "command=v7-user-switch $CAND $TARGET"
  echo "exit_code=$rc"
  echo "audit_record_hash=$audit_hash"
  echo
  echo "## Stdout"
  sed 's/^/stdout: /' "$STDOUT"
  echo
  echo "## Stderr"
  sed 's/^/stderr: /' "$STDERR"
  echo
  echo "## Before"
  echo "candidate_row_before=$(grep "ip=$CAND " "$BEFORE_USERS")"
  echo "target_users_before=$before_target_users"
  echo "route_table_1009_before=$(cat "$BEFORE_ROUTE")"
  echo "route_get_before=$before_route_get"
  echo "drift_row_before=$before_drift_row"
  echo
  echo "## After"
  echo "candidate_row_after=$(row_for_ip "$CAND")"
  echo "target_users_after=$after_target_users"
  echo "route_table_1009_after=$(cat "$AFTER_ROUTE")"
  echo "route_get_after=$after_route_get"
  echo "drift_row_after=$after_drift_row"
  echo "selected_moves_after=$after_selected"
  echo "hidden_movers_after=$after_hidden"
  echo "runtime_checkers_ok_after=$after_checkers"
  echo
  echo "## Registry Diff"
  diff -u "$BEFORE_USERS" "$AFTER_USERS" || true
  echo
  echo "## Route Table Diff"
  diff -u "$BEFORE_ROUTE" "$AFTER_ROUTE" || true
} > "$OUT"

echo "$rc"
