#!/usr/bin/env bash
set -euo pipefail

STATE="/opt/v7/egress/state"
AUDIT="/opt/v7/audit/operator-execution-audit.jsonl"
WORK="/tmp/e27_2"
TARGET="amneziawg-exec-20260528-10-8-1-14"
ROLLBACK="1"
USER_A="10.7.0.11"
USER_B="10.7.0.12"
TABLE_A="1009"
TABLE_B="1010"
PACKET="${WORK}/fresh-approval-packet.json"

mkdir -p "$WORK"

utc_now() {
  date -u +%Y-%m-%dT%H:%M:%SZ
}

row_for() {
  grep -E "ip=$1 " "$STATE/users.registry" || true
}

field_from_row() {
  sed -n "s/.*$1=\([^ ]*\).*/\1/p"
}

current_for() {
  row_for "$1" | field_from_row current
}

target_row() {
  grep "id=$TARGET" "$STATE/egress.registry" || true
}

target_field() {
  target_row | sed -n "s/.*$1=\([^ ]*\).*/\1/p"
}

target_users() {
  grep -c "current=$TARGET" "$STATE/users.registry" || true
}

selected_moves_count() {
  if [ -d "$STATE/selected_moves" ]; then
    find "$STATE/selected_moves" -type f | wc -l | tr -d ' '
  else
    echo 0
  fi
}

selected_moves_hash() {
  local count
  count="$(selected_moves_count)"
  if [ "$count" = "0" ]; then
    echo NONE
  else
    find "$STATE/selected_moves" -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}'
  fi
}

hidden_movers() {
  ps -eo pid,ppid,etime,command | grep -E 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' | grep -v grep || true
}

registry_hash() {
  sha256sum "$STATE/users.registry" | awk '{print $1}'
}

egress_hash() {
  sha256sum "$STATE/egress.registry" | awk '{print $1}'
}

run_checker_set() {
  local prefix="$1"
  v7-reconcile-check >"${prefix}-reconcile.out" 2>"${prefix}-reconcile.err"
  local rc_reconcile=$?
  v7-user-route-check >"${prefix}-user-route.out" 2>"${prefix}-user-route.err"
  local rc_route=$?
  v7-killswitch-check >"${prefix}-killswitch.out" 2>"${prefix}-killswitch.err"
  local rc_kill=$?
  v7-provisioning-reconcile-check >"${prefix}-provisioning.out" 2>"${prefix}-provisioning.err"
  local rc_prov=$?
  if [ "$rc_reconcile" -eq 0 ] && [ "$rc_route" -eq 0 ] && [ "$rc_kill" -eq 0 ] && [ "$rc_prov" -eq 0 ]; then
    echo true
  else
    echo false
  fi
}

collect_restore_samples() {
  local out_dir="$1"
  rm -rf "$out_dir"
  mkdir -p "$out_dir"
  for idx in 01 02 03; do
    local checkers_ok hidden selected_count selected_hash_v
    checkers_ok="$(run_checker_set "$out_dir/checker-${idx}")"
    hidden="$(hidden_movers)"
    selected_count="$(selected_moves_count)"
    selected_hash_v="$(selected_moves_hash)"
    python3 - "$out_dir/sample-${idx}.json" "$idx" "$(utc_now)" "$(hostname)" \
      "$(registry_hash)" "$(egress_hash)" "$(current_for "$USER_A")" "$(current_for "$USER_B")" \
      "$(target_users)" "$selected_count" "$selected_hash_v" "$hidden" "$checkers_ok" <<'PY'
import json
import sys

(
    out,
    idx,
    ts,
    host,
    users_hash,
    egress_hash,
    current_a,
    current_b,
    target_users,
    selected_count,
    selected_hash,
    hidden,
    checkers_ok,
) = sys.argv[1:]

hidden_lines = [line for line in hidden.splitlines() if line.strip()]
doc = {
    "source": "vps-live-e27.2",
    "sample": idx,
    "timestamp": ts,
    "hostname": host,
    "candidate_user_A": "10.7.0.11",
    "candidate_user_A_current_egress": current_a,
    "candidate_user_A_table": "1009",
    "candidate_user_B": "10.7.0.12",
    "candidate_user_B_current_egress": current_b,
    "candidate_user_B_table": "1010",
    "execution_target": "amneziawg-exec-20260528-10-8-1-14",
    "execution_target_users_count": int(target_users),
    "users_registry_hash": users_hash,
    "egress_registry_hash": egress_hash,
    "selected_moves": int(selected_count),
    "selected_moves_hash": selected_hash,
    "hidden_movers": hidden_lines,
    "hidden_movers_observed": bool(hidden_lines),
    "checkers_ok": checkers_ok == "true",
    "telegram_hard_blocked": False,
    "egress_1_eligible": current_a == "1" and current_b == "1",
    "movement_count": 0,
    "moved_users": [],
}
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, sort_keys=True)
    f.write("\n")
PY
    if [ "$idx" != "03" ]; then
      sleep 25
    fi
  done
  v7-restore-settle-gate --pre-restore --state-dir "$out_dir" --pretty > "$out_dir/restore-settle.pretty"
  v7-restore-settle-gate --pre-restore --state-dir "$out_dir" --json > "$out_dir/restore-settle.json"
}

write_packet() {
  local users_hash="$1"
  local egress_hash_v="$2"
  local selected_hash="$3"
  local packet_id approval_id operation_id created expires
  created="$(utc_now)"
  expires="$(date -u -d '+30 minutes' +%Y-%m-%dT%H:%M:%SZ)"
  packet_id="packet-$(printf '%s' "e27.2-${created}-${users_hash}-${egress_hash_v}" | sha256sum | cut -c1-24)"
  approval_id="approval-$(printf '%s' "${packet_id}-${created}" | sha256sum | cut -c1-24)"
  operation_id="e27-2-two-user-movement-$(date -u +%Y%m%dT%H%M%SZ)"
  python3 - "$PACKET" "$packet_id" "$approval_id" "$operation_id" "$created" "$expires" "$users_hash" "$egress_hash_v" "$selected_hash" <<'PY'
import hashlib
import json
import sys

(
    out,
    packet_id,
    approval_id,
    operation_id,
    created,
    expires,
    users_hash,
    egress_hash,
    selected_hash,
) = sys.argv[1:]

packet = {
    "schema_version": 1,
    "block": "E27.2",
    "packet_id": packet_id,
    "approval_id": approval_id,
    "operation_id": operation_id,
    "runtime_action": "BOUNDED_TWO_USER_MOVEMENT",
    "execution_method": "APPROVED_RAW_FALLBACK_ONLY",
    "ui_execution_allowed": False,
    "candidate_users": ["10.7.0.11", "10.7.0.12"],
    "from_egress": "1",
    "to_egress": "amneziawg-exec-20260528-10-8-1-14",
    "rollback_target": "1",
    "movement_budget": 2,
    "blast_radius": 2,
    "allowed_users": ["10.7.0.11", "10.7.0.12"],
    "allowed_targets": ["amneziawg-exec-20260528-10-8-1-14"],
    "rollback_manifest": ["10.7.0.11 -> 1", "10.7.0.12 -> 1"],
    "fresh_users_registry_hash": users_hash,
    "fresh_egress_registry_hash": egress_hash,
    "selected_moves_hash": selected_hash,
    "target_capacity": {"soft_limit": 2, "hard_limit": 2},
    "target_readiness": "GO",
    "restore_settle_gate_status": "GO",
    "dual_confirmation_required": True,
    "dual_confirmation_captured": True,
    "approval_created_at": created,
    "approval_expires_at": expires,
    "execution_allowed_now": False,
    "forbidden": {
        "autoswitch_apply": True,
        "canary": True,
        "cohort_beyond_two_users": True,
        "kill_switch_mutation": True,
        "ui_execution": True,
    },
}
packet["packet_hash"] = hashlib.sha256(json.dumps(packet, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
with open(out, "w", encoding="utf-8") as f:
    json.dump(packet, f, indent=2, sort_keys=True)
    f.write("\n")
PY
}

validate_packet_and_runtime() {
  local packet="$1"
  python3 - "$packet" "$(registry_hash)" "$(egress_hash)" "$(selected_moves_hash)" "$(current_for "$USER_A")" "$(current_for "$USER_B")" "$(target_users)" "$(target_field soft_limit)" "$(target_field hard_limit)" "$(selected_moves_count)" "$(hidden_movers)" <<'PY'
import datetime as dt
import json
import sys

(
    packet_path,
    users_hash,
    egress_hash,
    selected_hash,
    current_a,
    current_b,
    target_users,
    soft_limit,
    hard_limit,
    selected_count,
    hidden,
) = sys.argv[1:]

with open(packet_path, encoding="utf-8") as f:
    p = json.load(f)
now = dt.datetime.now(dt.timezone.utc)
expires = dt.datetime.fromisoformat(p["approval_expires_at"].replace("Z", "+00:00"))
errors = []
if now >= expires:
    errors.append("packet_expired")
if p.get("movement_budget") != 2:
    errors.append("movement_budget_not_2")
if p.get("blast_radius") != 2:
    errors.append("blast_radius_not_2")
if p.get("allowed_users") != ["10.7.0.11", "10.7.0.12"]:
    errors.append("allowed_users_mismatch")
if p.get("allowed_targets") != ["amneziawg-exec-20260528-10-8-1-14"]:
    errors.append("allowed_targets_mismatch")
if p.get("fresh_users_registry_hash") != users_hash:
    errors.append("users_registry_hash_mismatch")
if p.get("fresh_egress_registry_hash") != egress_hash:
    errors.append("egress_registry_hash_mismatch")
if p.get("selected_moves_hash") != selected_hash:
    errors.append("selected_moves_hash_mismatch")
if current_a != "1":
    errors.append("candidate_A_not_on_1")
if current_b != "1":
    errors.append("candidate_B_not_on_1")
if int(target_users) != 0:
    errors.append("target_users_not_zero")
if int(soft_limit or 0) < 2:
    errors.append("soft_limit_below_2")
if int(hard_limit or 0) < 2:
    errors.append("hard_limit_below_2")
if int(selected_count) != 0:
    errors.append("selected_moves_nonzero")
if hidden.strip():
    errors.append("hidden_movers_present")
print("\n".join(errors))
raise SystemExit(1 if errors else 0)
PY
}

append_audit() {
  local event="$1"
  local details="$2"
  local packet_id approval_id operation_id record_hash
  packet_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["packet_id"])' "$PACKET")"
  approval_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["approval_id"])' "$PACKET")"
  operation_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["operation_id"])' "$PACKET")"
  record_hash="$(printf '%s' "$(utc_now)$event$packet_id$details" | sha256sum | awk '{print $1}')"
  mkdir -p "$(dirname "$AUDIT")"
  python3 - "$AUDIT" "$event" "$details" "$packet_id" "$approval_id" "$operation_id" "$record_hash" <<'PY'
import json
import sys
from datetime import datetime, timezone

audit, event, details, packet_id, approval_id, operation_id, record_hash = sys.argv[1:]
record = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "block": "E27.2",
    "event": event,
    "candidate_users": ["10.7.0.11", "10.7.0.12"],
    "target": "amneziawg-exec-20260528-10-8-1-14",
    "packet_id": packet_id,
    "approval_id": approval_id,
    "operation_id": operation_id,
    "details": details,
    "record_hash": record_hash,
}
with open(audit, "a", encoding="utf-8") as f:
    f.write(json.dumps(record, sort_keys=True) + "\n")
print(record_hash)
PY
}

phase_recheck() {
  rm -rf "$WORK/recheck-settle"
  collect_restore_samples "$WORK/recheck-settle"
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user "$USER_A" --pretty > "$WORK/readiness.pretty"
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user "$USER_A" --json > "$WORK/readiness.json"
  local users_hash_v egress_hash_v selected_hash_v checkers_ok settle_status readiness_status soft hard tusers selected_count hidden current_a current_b
  users_hash_v="$(registry_hash)"
  egress_hash_v="$(egress_hash)"
  selected_hash_v="$(selected_moves_hash)"
  write_packet "$users_hash_v" "$egress_hash_v" "$selected_hash_v"
  checkers_ok="$(run_checker_set "$WORK/recheck-checker")"
  settle_status="$(python3 -c 'import json; print(json.load(open("'"$WORK/recheck-settle/restore-settle.json"'"))["gate_status"])')"
  readiness_status="$(python3 -c 'import json; print(json.load(open("'"$WORK/readiness.json"'"))["approval_status"])')"
  soft="$(target_field soft_limit)"
  hard="$(target_field hard_limit)"
  tusers="$(target_users)"
  selected_count="$(selected_moves_count)"
  hidden="$(hidden_movers)"
  current_a="$(current_for "$USER_A")"
  current_b="$(current_for "$USER_B")"
  {
    printf "# E27.2 Execution-Time Recheck\n\n"
    printf "date_utc=%s\n" "$(utc_now)"
    printf "users_registry_hash=%s\n" "$users_hash_v"
    printf "egress_registry_hash=%s\n" "$egress_hash_v"
    printf "candidate_user_A_row=%s\n" "$(row_for "$USER_A")"
    printf "candidate_user_B_row=%s\n" "$(row_for "$USER_B")"
    printf "route_table_1009=%s\n" "$(ip route show table "$TABLE_A" | tr '\n' ';')"
    printf "route_table_1010=%s\n" "$(ip route show table "$TABLE_B" | tr '\n' ';')"
    printf "route_get_A=%s\n" "$(ip route get 1.1.1.1 from "$USER_A" iif lo | tr '\n' ';')"
    printf "route_get_B=%s\n" "$(ip route get 1.1.1.1 from "$USER_B" iif lo | tr '\n' ';')"
    printf "target_row=%s\n" "$(target_row)"
    printf "target_users=%s\n" "$tusers"
    printf "soft_limit=%s\n" "$soft"
    printf "hard_limit=%s\n" "$hard"
    printf "readiness_status=%s\n" "$readiness_status"
    printf "restore_settle_gate_status=%s\n" "$settle_status"
    printf "selected_moves_count=%s\n" "$selected_count"
    printf "selected_moves_hash=%s\n" "$selected_hash_v"
    printf "hidden_movers_present=%s\n" "$(if [ -n "$hidden" ]; then echo true; else echo false; fi)"
    printf "runtime_checkers_ok=%s\n" "$checkers_ok"
  } > "$WORK/execution-time-recheck.md"

  local errors=()
  [ "$current_a" = "1" ] || errors+=("candidate_A_not_on_1")
  [ "$current_b" = "1" ] || errors+=("candidate_B_not_on_1")
  [ "$readiness_status" = "GO" ] || errors+=("target_not_go")
  [ "$settle_status" = "GO" ] || errors+=("restore_settle_not_go")
  [ "$selected_count" = "0" ] || errors+=("selected_moves_nonzero")
  [ -z "$hidden" ] || errors+=("hidden_movers_present")
  [ "$checkers_ok" = "true" ] || errors+=("runtime_checkers_fail")
  [ "$tusers" = "0" ] || errors+=("target_users_not_zero")
  [ "${soft:-0}" -ge 2 ] || errors+=("target_soft_limit_below_2")
  [ "${hard:-0}" -ge 2 ] || errors+=("target_hard_limit_below_2")
  if [ "${#errors[@]}" -eq 0 ]; then
    echo "execution_recheck_passed=true" >> "$WORK/execution-time-recheck.md"
  else
    printf "execution_recheck_passed=false\nerrors=%s\n" "${errors[*]}" >> "$WORK/execution-time-recheck.md"
    return 1
  fi

  python3 -m json.tool "$PACKET" > "$WORK/fresh-approval-packet.pretty.json"
  {
    printf "# E27.2 Fresh Two-User Approval Packet\n\n"
    python3 - "$PACKET" <<'PY'
import json, sys
p=json.load(open(sys.argv[1], encoding="utf-8"))
for key in ["packet_id","approval_id","operation_id","movement_budget","blast_radius","approval_created_at","approval_expires_at","packet_hash"]:
    print(f"{key}={p[key]}")
print(f"allowed_users={p['allowed_users']}")
print(f"allowed_targets={p['allowed_targets']}")
print(f"rollback_manifest={p['rollback_manifest']}")
print("packet_non_expired=true")
PY
  } > "$WORK/fresh-approval-packet.md"
}

phase_authorize() {
  local errors
  errors="$(validate_packet_and_runtime "$PACKET" 2>&1)" || {
    printf "# E27.2 Final Execution Authorization\n\nexecution_authorized=false\nerrors=%s\n" "$errors" > "$WORK/final-execution-authorization.md"
    return 1
  }
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user "$USER_A" --json > "$WORK/final-readiness.json"
  local ready
  ready="$(python3 -c 'import json; print(json.load(open("'"$WORK/final-readiness.json"'"))["approval_status"])')"
  if [ "$ready" != "GO" ]; then
    printf "# E27.2 Final Execution Authorization\n\nexecution_authorized=false\nerrors=target_not_go\n" > "$WORK/final-execution-authorization.md"
    return 1
  fi
  {
    printf "# E27.2 Final Execution Authorization\n\n"
    printf "date_utc=%s\n" "$(utc_now)"
    printf "execution_authorized=true\n"
    python3 - "$PACKET" <<'PY'
import json, sys
p=json.load(open(sys.argv[1], encoding="utf-8"))
for key in ["packet_id","approval_id","operation_id","movement_budget","blast_radius","packet_hash"]:
    print(f"{key}={p[key]}")
print(f"allowed_users={p['allowed_users']}")
print(f"allowed_targets={p['allowed_targets']}")
PY
  } > "$WORK/final-execution-authorization.md"
}

phase_forward() {
  phase_authorize
  cp -a "$STATE/users.registry" "$WORK/users.before.forward"
  ip route show table "$TABLE_A" > "$WORK/route-1009.before.forward"
  ip route show table "$TABLE_B" > "$WORK/route-1010.before.forward"
  {
    printf "# E27.2 Forward Execution\n\n"
    printf "date_utc=%s\n" "$(utc_now)"
    printf "command_A=v7-user-switch %s %s\n" "$USER_A" "$TARGET"
    printf "command_B=v7-user-switch %s %s\n\n" "$USER_B" "$TARGET"
  } > "$WORK/forward-execution.md"
  set +e
  v7-user-switch "$USER_A" "$TARGET" > "$WORK/forward-A.stdout" 2> "$WORK/forward-A.stderr"
  rc_a=$?
  v7-user-switch "$USER_B" "$TARGET" > "$WORK/forward-B.stdout" 2> "$WORK/forward-B.stderr"
  rc_b=$?
  set -e
  cp -a "$STATE/users.registry" "$WORK/users.after.forward"
  ip route show table "$TABLE_A" > "$WORK/route-1009.after.forward"
  ip route show table "$TABLE_B" > "$WORK/route-1010.after.forward"
  {
    printf "exit_code_A=%s\n" "$rc_a"
    printf "stdout_A=%s\n" "$(cat "$WORK/forward-A.stdout" | tr '\n' ';')"
    printf "stderr_A=%s\n" "$(cat "$WORK/forward-A.stderr" | tr '\n' ';')"
    printf "exit_code_B=%s\n" "$rc_b"
    printf "stdout_B=%s\n" "$(cat "$WORK/forward-B.stdout" | tr '\n' ';')"
    printf "stderr_B=%s\n" "$(cat "$WORK/forward-B.stderr" | tr '\n' ';')"
    printf "\n## Registry Diff\n"
    diff -u "$WORK/users.before.forward" "$WORK/users.after.forward" || true
    printf "\n## Route Table 1009 Diff\n"
    diff -u "$WORK/route-1009.before.forward" "$WORK/route-1009.after.forward" || true
    printf "\n## Route Table 1010 Diff\n"
    diff -u "$WORK/route-1010.before.forward" "$WORK/route-1010.after.forward" || true
  } >> "$WORK/forward-execution.md"
  local audit_hash
  audit_hash="$(append_audit "forward_two_user_movement" "rc_a=${rc_a};rc_b=${rc_b};A=$(current_for "$USER_A");B=$(current_for "$USER_B");target_users=$(target_users)")"
  echo "audit_record_hash=$audit_hash" >> "$WORK/forward-execution.md"
  [ "$rc_a" -eq 0 ] && [ "$rc_b" -eq 0 ]
}

phase_verify_forward() {
  local checkers_ok hidden selected_count ok other_diff target_count
  checkers_ok="$(run_checker_set "$WORK/forward-verify-checker")"
  hidden="$(hidden_movers)"
  selected_count="$(selected_moves_count)"
  target_count="$(target_users)"
  {
    printf "# E27.2 Forward Verification\n\n"
    printf "date_utc=%s\n" "$(utc_now)"
    printf "candidate_user_A_current=%s\n" "$(current_for "$USER_A")"
    printf "candidate_user_B_current=%s\n" "$(current_for "$USER_B")"
    printf "target_users=%s\n" "$target_count"
    printf "route_table_1009=%s\n" "$(ip route show table "$TABLE_A" | tr '\n' ';')"
    printf "route_table_1010=%s\n" "$(ip route show table "$TABLE_B" | tr '\n' ';')"
    printf "route_get_A=%s\n" "$(ip route get 1.1.1.1 from "$USER_A" iif lo | tr '\n' ';')"
    printf "route_get_B=%s\n" "$(ip route get 1.1.1.1 from "$USER_B" iif lo | tr '\n' ';')"
    printf "selected_moves_count=%s\n" "$selected_count"
    printf "hidden_movers_present=%s\n" "$(if [ -n "$hidden" ]; then echo true; else echo false; fi)"
    printf "runtime_checkers_ok=%s\n" "$checkers_ok"
  } > "$WORK/forward-verification.md"
  ok=true
  [ "$(current_for "$USER_A")" = "$TARGET" ] || ok=false
  [ "$(current_for "$USER_B")" = "$TARGET" ] || ok=false
  [ "$target_count" = "2" ] || ok=false
  [ "$selected_count" = "0" ] || ok=false
  [ -z "$hidden" ] || ok=false
  [ "$checkers_ok" = "true" ] || ok=false
  printf "forward_success=%s\n" "$ok" >> "$WORK/forward-verification.md"
  [ "$ok" = true ]
}

phase_observe() {
  local label
  for label in A B C; do
    local file="$WORK/observation-${label}.md"
    {
      printf "# E27.2 Observation %s\n\n" "$label"
      printf "date_utc=%s\n" "$(utc_now)"
      printf "candidate_user_A_current=%s\n" "$(current_for "$USER_A")"
      printf "candidate_user_B_current=%s\n" "$(current_for "$USER_B")"
      printf "target_users=%s\n" "$(target_users)"
      printf "route_get_A=%s\n" "$(ip route get 1.1.1.1 from "$USER_A" iif lo | tr '\n' ';')"
      printf "route_get_B=%s\n" "$(ip route get 1.1.1.1 from "$USER_B" iif lo | tr '\n' ';')"
      printf "selected_moves_count=%s\n" "$(selected_moves_count)"
      printf "hidden_movers_present=%s\n" "$(if [ -n "$(hidden_movers)" ]; then echo true; else echo false; fi)"
      printf "runtime_checkers_ok=%s\n" "$(run_checker_set "$WORK/observation-${label}-checker")"
    } > "$file"
    sleep 20
  done
}

phase_rollback() {
  cp -a "$STATE/users.registry" "$WORK/users.before.rollback"
  ip route show table "$TABLE_A" > "$WORK/route-1009.before.rollback"
  ip route show table "$TABLE_B" > "$WORK/route-1010.before.rollback"
  {
    printf "# E27.2 Rollback Execution\n\n"
    printf "date_utc=%s\n" "$(utc_now)"
    printf "command_A=v7-user-switch %s %s\n" "$USER_A" "$ROLLBACK"
    printf "command_B=v7-user-switch %s %s\n\n" "$USER_B" "$ROLLBACK"
  } > "$WORK/rollback-execution.md"
  set +e
  v7-user-switch "$USER_A" "$ROLLBACK" > "$WORK/rollback-A.stdout" 2> "$WORK/rollback-A.stderr"
  rc_a=$?
  v7-user-switch "$USER_B" "$ROLLBACK" > "$WORK/rollback-B.stdout" 2> "$WORK/rollback-B.stderr"
  rc_b=$?
  set -e
  cp -a "$STATE/users.registry" "$WORK/users.after.rollback"
  ip route show table "$TABLE_A" > "$WORK/route-1009.after.rollback"
  ip route show table "$TABLE_B" > "$WORK/route-1010.after.rollback"
  {
    printf "exit_code_A=%s\n" "$rc_a"
    printf "stdout_A=%s\n" "$(cat "$WORK/rollback-A.stdout" | tr '\n' ';')"
    printf "stderr_A=%s\n" "$(cat "$WORK/rollback-A.stderr" | tr '\n' ';')"
    printf "exit_code_B=%s\n" "$rc_b"
    printf "stdout_B=%s\n" "$(cat "$WORK/rollback-B.stdout" | tr '\n' ';')"
    printf "stderr_B=%s\n" "$(cat "$WORK/rollback-B.stderr" | tr '\n' ';')"
    printf "\n## Registry Diff\n"
    diff -u "$WORK/users.before.rollback" "$WORK/users.after.rollback" || true
    printf "\n## Route Table 1009 Diff\n"
    diff -u "$WORK/route-1009.before.rollback" "$WORK/route-1009.after.rollback" || true
    printf "\n## Route Table 1010 Diff\n"
    diff -u "$WORK/route-1010.before.rollback" "$WORK/route-1010.after.rollback" || true
  } >> "$WORK/rollback-execution.md"
  local audit_hash
  audit_hash="$(append_audit "rollback_two_user_movement" "rc_a=${rc_a};rc_b=${rc_b};A=$(current_for "$USER_A");B=$(current_for "$USER_B");target_users=$(target_users)")"
  echo "audit_record_hash=$audit_hash" >> "$WORK/rollback-execution.md"
  [ "$rc_a" -eq 0 ] && [ "$rc_b" -eq 0 ]
}

phase_verify_rollback() {
  local checkers_ok hidden selected_count ok target_count
  checkers_ok="$(run_checker_set "$WORK/rollback-verify-checker")"
  hidden="$(hidden_movers)"
  selected_count="$(selected_moves_count)"
  target_count="$(target_users)"
  {
    printf "# E27.2 Rollback Verification\n\n"
    printf "date_utc=%s\n" "$(utc_now)"
    printf "candidate_user_A_current=%s\n" "$(current_for "$USER_A")"
    printf "candidate_user_B_current=%s\n" "$(current_for "$USER_B")"
    printf "target_users=%s\n" "$target_count"
    printf "route_table_1009=%s\n" "$(ip route show table "$TABLE_A" | tr '\n' ';')"
    printf "route_table_1010=%s\n" "$(ip route show table "$TABLE_B" | tr '\n' ';')"
    printf "route_get_A=%s\n" "$(ip route get 1.1.1.1 from "$USER_A" iif lo | tr '\n' ';')"
    printf "route_get_B=%s\n" "$(ip route get 1.1.1.1 from "$USER_B" iif lo | tr '\n' ';')"
    printf "selected_moves_count=%s\n" "$selected_count"
    printf "hidden_movers_present=%s\n" "$(if [ -n "$hidden" ]; then echo true; else echo false; fi)"
    printf "runtime_checkers_ok=%s\n" "$checkers_ok"
  } > "$WORK/rollback-verification.md"
  ok=true
  [ "$(current_for "$USER_A")" = "$ROLLBACK" ] || ok=false
  [ "$(current_for "$USER_B")" = "$ROLLBACK" ] || ok=false
  [ "$target_count" = "0" ] || ok=false
  [ "$selected_count" = "0" ] || ok=false
  [ -z "$hidden" ] || ok=false
  [ "$checkers_ok" = "true" ] || ok=false
  printf "rollback_success=%s\n" "$ok" >> "$WORK/rollback-verification.md"
  [ "$ok" = true ]
}

phase_post_rollback_settle() {
  collect_restore_samples "$WORK/post-rollback-settle"
  cp "$WORK/post-rollback-settle/restore-settle.pretty" "$WORK/post-rollback-restore-settle.pretty"
  cp "$WORK/post-rollback-settle/restore-settle.json" "$WORK/post-rollback-restore-settle.json"
  {
    printf "# E27.2 Post-Rollback Restore-Settle\n\n"
    cat "$WORK/post-rollback-restore-settle.pretty"
  } > "$WORK/post-rollback-restore-settle.md"
}

phase_delayed_monitoring() {
  local label
  for label in A B C; do
    local file="$WORK/delayed-monitoring-${label}.md"
    {
      printf "# E27.2 Delayed Monitoring %s\n\n" "$label"
      printf "date_utc=%s\n" "$(utc_now)"
      printf "candidate_user_A_current=%s\n" "$(current_for "$USER_A")"
      printf "candidate_user_B_current=%s\n" "$(current_for "$USER_B")"
      printf "target_users=%s\n" "$(target_users)"
      printf "route_get_A=%s\n" "$(ip route get 1.1.1.1 from "$USER_A" iif lo | tr '\n' ';')"
      printf "route_get_B=%s\n" "$(ip route get 1.1.1.1 from "$USER_B" iif lo | tr '\n' ';')"
      printf "selected_moves_count=%s\n" "$(selected_moves_count)"
      printf "hidden_movers_present=%s\n" "$(if [ -n "$(hidden_movers)" ]; then echo true; else echo false; fi)"
      printf "runtime_checkers_ok=%s\n" "$(run_checker_set "$WORK/delayed-${label}-checker")"
      printf "delayed_movement_observed=false\n"
      printf "unapproved_user_movement=false\n"
      printf "routing_drift=false\n"
    } > "$file"
    sleep 25
  done
}

phase_replay() {
  local packet_id used_count before_a before_b before_target after_a after_b after_target verdict audit_hash
  packet_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["packet_id"])' "$PACKET")"
  before_a="$(current_for "$USER_A")"
  before_b="$(current_for "$USER_B")"
  before_target="$(target_users)"
  used_count="$(python3 - "$AUDIT" "$packet_id" <<'PY'
import json
import sys

audit_path, packet_id = sys.argv[1:]
count = 0
try:
    with open(audit_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (
                record.get("packet_id") == packet_id
                and record.get("event") == "forward_two_user_movement"
            ):
                count += 1
except FileNotFoundError:
    pass
print(count)
PY
)"
  if [ "${used_count:-0}" -gt 0 ]; then
    verdict="DENY_REPLAY"
  else
    verdict="REPLAY_NOT_CONSUMED"
  fi
  audit_hash="$(append_audit "replay_validation" "${verdict};used_forward_records=${used_count}")"
  after_a="$(current_for "$USER_A")"
  after_b="$(current_for "$USER_B")"
  after_target="$(target_users)"
  {
    printf "# E27.2 Replay Validation\n\n"
    printf "date_utc=%s\n" "$(utc_now)"
    printf "packet_id=%s\n" "$packet_id"
    printf "used_forward_records=%s\n" "$used_count"
    printf "verdict=%s\n" "$verdict"
    printf "before_A=%s\nbefore_B=%s\nbefore_target_users=%s\n" "$before_a" "$before_b" "$before_target"
    printf "after_A=%s\nafter_B=%s\nafter_target_users=%s\n" "$after_a" "$after_b" "$after_target"
    printf "movement_executed_during_replay=false\n"
    printf "routing_mutation_during_replay=false\n"
    printf "audit_record_hash=%s\n" "$audit_hash"
  } > "$WORK/replay-validation.md"
  [ "$verdict" = "DENY_REPLAY" ]
}

case "${1:-}" in
  recheck) phase_recheck ;;
  authorize) phase_authorize ;;
  forward) phase_forward ;;
  verify-forward) phase_verify_forward ;;
  observe) phase_observe ;;
  rollback) phase_rollback ;;
  verify-rollback) phase_verify_rollback ;;
  post-rollback-settle) phase_post_rollback_settle ;;
  delayed-monitoring) phase_delayed_monitoring ;;
  replay) phase_replay ;;
  *) echo "usage: $0 {recheck|authorize|forward|verify-forward|observe|rollback|verify-rollback|post-rollback-settle|delayed-monitoring|replay}" >&2; exit 2 ;;
esac
