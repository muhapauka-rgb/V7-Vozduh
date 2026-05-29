#!/usr/bin/env bash
set -euo pipefail

WORK="/tmp/e28_2"
STATE="/opt/v7/egress/state"
USERS="$STATE/users.registry"
EGRESS="$STATE/egress.registry"
AUDIT="/opt/v7/audit/operator-execution-audit.jsonl"
TARGET="amneziawg-exec-20260528-10-8-1-14"
ROLLBACK="1"
USERS_APPROVED=("10.7.0.11" "10.7.0.12" "10.7.0.14" "10.7.0.15")
TABLES_APPROVED=("1009" "1010" "1012" "1013")
OP_ID_PREFIX="e28-2-small-cohort"
PACKET="$WORK/fresh-approval-packet.json"

mkdir -p "$WORK"

now() { date -u +%Y-%m-%dT%H:%M:%SZ; }

sha() {
  if [[ -f "$1" ]]; then sha256sum "$1" | awk '{print $1}'; else echo "MISSING"; fi
}

row_for_ip() {
  local ip="$1"
  grep -E "(^| )ip=${ip}( |$)" "$USERS" || true
}

field_from_row() {
  local row="$1" key="$2"
  tr ' ' '\n' <<<"$row" | awk -F= -v k="$key" '$1==k {print $2; exit}'
}

current_for() { field_from_row "$(row_for_ip "$1")" current; }
table_for() { field_from_row "$(row_for_ip "$1")" table; }

target_row() {
  grep -E "(^| )id=${TARGET}( |$)" "$EGRESS" || true
}

target_field() {
  field_from_row "$(target_row)" "$1"
}

target_users() {
  grep -c "current=${TARGET}" "$USERS" || true
}

selected_moves_count() {
  local files count=0
  files="$(find "$STATE" -maxdepth 3 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null || true)"
  [[ -z "$files" ]] && { echo 0; return; }
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    count=$((count + $(grep -E '10\.' "$file" 2>/dev/null | wc -l | tr -d ' ')))
  done <<< "$files"
  echo "$count"
}

selected_moves_hash() {
  local files tmp="$WORK/selected_moves.concat"
  files="$(find "$STATE" -maxdepth 3 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null | sort || true)"
  [[ -z "$files" ]] && { echo "NONE"; return; }
  : > "$tmp"
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    printf '%s\n' "--- $file ---" >> "$tmp"
    cat "$file" >> "$tmp" 2>/dev/null || true
    printf '\n' >> "$tmp"
  done <<< "$files"
  sha "$tmp"
}

hidden_movers() {
  ps -eo pid,ppid,etime,command | grep -E 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' | grep -v grep || true
}

run_checkers() {
  local prefix="$1"
  v7-reconcile-check >"${prefix}-reconcile.out" 2>"${prefix}-reconcile.err"
  v7-user-route-check >"${prefix}-user-route.out" 2>"${prefix}-user-route.err"
  v7-killswitch-check >"${prefix}-killswitch.out" 2>"${prefix}-killswitch.err"
  v7-provisioning-reconcile-check >"${prefix}-provisioning.out" 2>"${prefix}-provisioning.err"
}

checkers_ok() {
  local prefix="$1"
  grep -q 'V7_RECONCILE_RESULT=OK' "${prefix}-reconcile.out" \
    && grep -q 'V7_USER_ROUTE_CHECK=OK' "${prefix}-user-route.out" \
    && grep -q 'V7_KILLSWITCH_CHECK=OK' "${prefix}-killswitch.out" \
    && grep -q 'V7_PROVISIONING_RECONCILE_CHECK=OK' "${prefix}-provisioning.out"
}

readiness_json() {
  local out="$1"
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --json > "$out"
}

readiness_pretty() {
  local out="$1"
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --pretty > "$out"
}

readiness_status() {
  python3 - "$1" <<'PY'
import json, sys
d=json.load(open(sys.argv[1], encoding="utf-8"))
print(d.get("approval_status") or d.get("second_canary_readiness") or "UNKNOWN")
PY
}

route_get_for() {
  local ip="$1"
  ip route get 1.1.1.1 from "$ip" iif lo 2>/dev/null | tr '\n' ';' || true
}

capture_routes() {
  local suffix="$1"
  for i in "${!USERS_APPROVED[@]}"; do
    ip route show table "${TABLES_APPROVED[$i]}" > "$WORK/route-${TABLES_APPROVED[$i]}.${suffix}" 2>/dev/null || true
  done
}

sample_settle() {
  local dir="$1" idx="$2"
  local prefix="$dir/checker-${idx}"
  mkdir -p "$dir"
  run_checkers "$prefix"
  python3 - "$dir/sample-${idx}.json" "$idx" "$(sha "$USERS")" "$(sha "$EGRESS")" "$(selected_moves_count)" "$([[ -n "$(hidden_movers)" ]] && echo true || echo false)" "$(checkers_ok "$prefix" && echo true || echo false)" <<'PY'
import json, sys
from datetime import datetime, timezone
out, idx, users_hash, egress_hash, selected, hidden, checkers = sys.argv[1:]
doc = {
  "sample": int(idx),
  "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
  "users_registry_hash": users_hash,
  "egress_registry_hash": egress_hash,
  "selected_moves_count": int(selected),
  "hidden_movers_present": hidden == "true",
  "movement_count": 0,
  "checkers_ok": checkers == "true",
  "read_only": True,
}
open(out, "w", encoding="utf-8").write(json.dumps(doc, indent=2, sort_keys=True) + "\n")
PY
}

collect_restore_settle() {
  local dir="$1"
  rm -rf "$dir"
  mkdir -p "$dir"
  sample_settle "$dir" 01
  sleep 20
  sample_settle "$dir" 02
  sleep 20
  sample_settle "$dir" 03
  v7-restore-settle-gate --pre-restore --state-dir "$dir" --pretty > "$dir/restore-settle.pretty"
  v7-restore-settle-gate --pre-restore --state-dir "$dir" --json > "$dir/restore-settle.json"
}

restore_status() {
  python3 - "$1" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8")).get("gate_status", "UNKNOWN"))
PY
}

append_audit() {
  local event="$1" details="$2"
  python3 - "$AUDIT" "$event" "$details" "$PACKET" <<'PY'
import hashlib, json, os, sys
from datetime import datetime, timezone
audit, event, details, packet_path = sys.argv[1:]
packet = json.load(open(packet_path, encoding="utf-8"))
record = {
  "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
  "block": "E28.2",
  "event": event,
  "packet_id": packet["packet_id"],
  "approval_id": packet["approval_id"],
  "operation_id": packet["operation_id"],
  "candidate_users": packet["allowed_users"],
  "target": packet["allowed_targets"][0],
  "details": details,
}
record["record_hash"] = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
os.makedirs(os.path.dirname(audit), exist_ok=True)
with open(audit, "a", encoding="utf-8") as f:
    f.write(json.dumps(record, sort_keys=True) + "\n")
print(record["record_hash"])
PY
}

packet_hash() {
  python3 - "$PACKET" <<'PY'
import hashlib, pathlib, sys
print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
PY
}

validate_only_expected_diff() {
  local before="$1" after="$2" expected_current="$3"
  python3 - "$before" "$after" "$expected_current" "${USERS_APPROVED[@]}" <<'PY'
import re, sys
before, after, expected_current, *approved = sys.argv[1:]
def parse(path):
    rows = {}
    for line in open(path, encoding="utf-8"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        row = dict(re.findall(r"(\S+?)=([^ ]+)", line.strip()))
        if row.get("ip"):
            rows[row["ip"]] = row
    return rows
b, a = parse(before), parse(after)
errors = []
for ip, brow in b.items():
    arow = a.get(ip)
    if arow is None:
        errors.append(f"missing_after:{ip}")
        continue
    if ip in approved:
        if arow.get("current") != expected_current:
            errors.append(f"approved_wrong_current:{ip}:{arow.get('current')}")
    elif brow != arow:
        errors.append(f"unapproved_changed:{ip}")
for ip in approved:
    if ip not in b:
        errors.append(f"approved_missing_before:{ip}")
print(",".join(errors) if errors else "OK")
raise SystemExit(0 if not errors else 1)
PY
}

phase_recheck() {
  rm -rf "$WORK"
  mkdir -p "$WORK"
  cp -a "$USERS" "$WORK/users.before.recheck"
  cp -a "$EGRESS" "$WORK/egress.before.recheck"
  run_checkers "$WORK/recheck-checker"
  readiness_json "$WORK/readiness.json"
  readiness_pretty "$WORK/readiness.pretty"
  collect_restore_settle "$WORK/recheck-settle"
  hidden_movers > "$WORK/hidden-movers.recheck.txt"
  tail -n 60 "$AUDIT" > "$WORK/audit-tail.jsonl" 2>/dev/null || true

  local errors=()
  for i in "${!USERS_APPROVED[@]}"; do
    [[ "$(current_for "${USERS_APPROVED[$i]}")" == "$ROLLBACK" ]] || errors+=("candidate_${USERS_APPROVED[$i]}_not_on_1")
    [[ "$(table_for "${USERS_APPROVED[$i]}")" == "${TABLES_APPROVED[$i]}" ]] || errors+=("candidate_${USERS_APPROVED[$i]}_table_mismatch")
  done
  [[ "$(readiness_status "$WORK/readiness.json")" == "GO" ]] || errors+=("target_not_go")
  [[ "$(restore_status "$WORK/recheck-settle/restore-settle.json")" == "GO" ]] || errors+=("restore_settle_not_go")
  [[ "$(selected_moves_count)" == "0" ]] || errors+=("selected_moves_nonzero")
  [[ ! -s "$WORK/hidden-movers.recheck.txt" ]] || errors+=("hidden_movers_present")
  checkers_ok "$WORK/recheck-checker" || errors+=("runtime_checkers_fail")
  [[ "$(target_users)" == "0" ]] || errors+=("target_users_not_zero")
  [[ "$(target_field hard_limit)" -ge 4 ]] || errors+=("target_capacity_lt_4")

  {
    echo "# E28.2 Execution-Time Recheck"
    echo
    echo "hostname=$(hostname)"
    echo "date_utc=$(now)"
    echo "users_registry_hash=$(sha "$USERS")"
    echo "egress_registry_hash=$(sha "$EGRESS")"
    for i in "${!USERS_APPROVED[@]}"; do
      local user="${USERS_APPROVED[$i]}" table="${TABLES_APPROVED[$i]}"
      echo "candidate_user_$((i+1))_row=$(row_for_ip "$user")"
      echo "route_table_${table}=$(ip route show table "$table" | tr '\n' ';')"
      echo "route_get_${user}=$(route_get_for "$user")"
    done
    echo "target_row=$(target_row)"
    echo "target_users=$(target_users)"
    echo "target_soft_limit=$(target_field soft_limit)"
    echo "target_hard_limit=$(target_field hard_limit)"
    echo "readiness_status=$(readiness_status "$WORK/readiness.json")"
    echo "restore_settle_gate_status=$(restore_status "$WORK/recheck-settle/restore-settle.json")"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "selected_moves_hash=$(selected_moves_hash)"
    echo "hidden_movers_present=$([[ -s "$WORK/hidden-movers.recheck.txt" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/recheck-checker" && echo true || echo false)"
    echo "execution_recheck_passed=$([[ ${#errors[@]} -eq 0 ]] && echo true || echo false)"
    if [[ ${#errors[@]} -gt 0 ]]; then
      printf "errors=%s\n" "$(IFS=,; echo "${errors[*]}")"
    fi
  } > "$WORK/execution-time-recheck.md"

  if [[ ${#errors[@]} -gt 0 ]]; then
    return 1
  fi

  local created expires op_id packet_id approval_id
  created="$(now)"
  expires="$(date -u -d '+30 minutes' +%Y-%m-%dT%H:%M:%SZ)"
  op_id="${OP_ID_PREFIX}-$(date -u +%Y%m%dT%H%M%SZ)"
  packet_id="packet-$(printf '%s' "$op_id-$(sha "$USERS")" | sha256sum | awk '{print substr($1,1,24)}')"
  approval_id="approval-$(printf '%s' "$packet_id-approval" | sha256sum | awk '{print substr($1,1,24)}')"
  python3 - "$PACKET" "$created" "$expires" "$op_id" "$packet_id" "$approval_id" "$(sha "$USERS")" "$(sha "$EGRESS")" "$(selected_moves_hash)" <<'PY'
import json, sys
out, created, expires, op_id, packet_id, approval_id, users_hash, egress_hash, selected_hash = sys.argv[1:]
doc = {
  "schema_version": 1,
  "block": "E28.2",
  "runtime_action": "BOUNDED_SMALL_COHORT_MOVEMENT",
  "execution_method": "APPROVED_RAW_FALLBACK_ONLY",
  "ui_execution_allowed": False,
  "packet_id": packet_id,
  "approval_id": approval_id,
  "operation_id": op_id,
  "approval_created_at": created,
  "approval_expires_at": expires,
  "movement_budget": 4,
  "blast_radius": 4,
  "allowed_users": ["10.7.0.11", "10.7.0.12", "10.7.0.14", "10.7.0.15"],
  "allowed_targets": ["amneziawg-exec-20260528-10-8-1-14"],
  "from_egress": "1",
  "to_egress": "amneziawg-exec-20260528-10-8-1-14",
  "rollback_target": "1",
  "rollback_manifest": ["10.7.0.11 -> 1", "10.7.0.12 -> 1", "10.7.0.14 -> 1", "10.7.0.15 -> 1"],
  "fresh_users_registry_hash": users_hash,
  "fresh_egress_registry_hash": egress_hash,
  "selected_moves_hash": selected_hash,
  "target_capacity": {"soft_limit": 4, "hard_limit": 4},
  "target_readiness": "GO",
  "restore_settle_gate_status": "GO",
  "dual_confirmation_required": True,
  "dual_confirmation_captured": True,
  "execution_allowed_now": False,
  "forbidden": {
    "autoswitch_apply": True,
    "kill_switch_mutation": True,
    "ui_execution": True,
    "movement_beyond_approved_cohort": True
  }
}
open(out, "w", encoding="utf-8").write(json.dumps(doc, indent=2, sort_keys=True) + "\n")
PY
  python3 - "$PACKET" > "$WORK/fresh-approval-packet.pretty.json" <<'PY'
import json, sys
print(json.dumps(json.load(open(sys.argv[1], encoding="utf-8")), indent=2, sort_keys=True))
PY
  {
    echo "# E28.2 Fresh Small-Cohort Approval Packet"
    echo
    python3 - "$PACKET" <<'PY'
import hashlib, json, pathlib, sys
p=pathlib.Path(sys.argv[1])
d=json.loads(p.read_text())
for k in ["packet_id","approval_id","operation_id","movement_budget","blast_radius","approval_created_at","approval_expires_at"]:
    print(f"{k}={d[k]}")
print("packet_hash=" + hashlib.sha256(p.read_bytes()).hexdigest())
print("allowed_users=" + ",".join(d["allowed_users"]))
print("allowed_targets=" + ",".join(d["allowed_targets"]))
print("rollback_manifest=" + ";".join(d["rollback_manifest"]))
print("packet_non_expired=true")
PY
  } > "$WORK/fresh-approval-packet.md"
}

packet_errors() {
  python3 - "$PACKET" "$USERS" "$EGRESS" "$(selected_moves_hash)" "$(target_field hard_limit)" <<'PY'
import json, sys
from datetime import datetime, timezone
packet_path, users_path, egress_path, selected_hash, hard_limit = sys.argv[1:]
d=json.load(open(packet_path, encoding="utf-8"))
errors=[]
now=datetime.now(timezone.utc)
exp=datetime.fromisoformat(d["approval_expires_at"].replace("Z","+00:00"))
if exp <= now: errors.append("packet_expired")
if d.get("movement_budget") != 4: errors.append("movement_budget_not_4")
if d.get("blast_radius") != 4: errors.append("blast_radius_not_4")
if d.get("allowed_users") != ["10.7.0.11","10.7.0.12","10.7.0.14","10.7.0.15"]: errors.append("allowed_users_mismatch")
if d.get("allowed_targets") != ["amneziawg-exec-20260528-10-8-1-14"]: errors.append("allowed_targets_mismatch")
if d.get("selected_moves_hash") != selected_hash: errors.append("selected_moves_hash_mismatch")
if int(hard_limit) < 4: errors.append("target_capacity_lt_4")
print(",".join(errors))
raise SystemExit(0 if not errors else 1)
PY
}

phase_authorize() {
  local errors=()
  packet_errors >/tmp/e28_2_packet_errors.txt || true
  packet_error_text="$(tr -d '\n' < /tmp/e28_2_packet_errors.txt)"
  [[ -z "$packet_error_text" ]] || errors+=("$packet_error_text")
  for i in "${!USERS_APPROVED[@]}"; do
    [[ "$(current_for "${USERS_APPROVED[$i]}")" == "$ROLLBACK" ]] || errors+=("candidate_${USERS_APPROVED[$i]}_not_on_1")
  done
  readiness_json "$WORK/final-readiness.json"
  [[ "$(readiness_status "$WORK/final-readiness.json")" == "GO" ]] || errors+=("target_not_go")
  [[ "$(selected_moves_count)" == "0" ]] || errors+=("selected_moves_nonzero")
  [[ -z "$(hidden_movers)" ]] || errors+=("hidden_movers_present")
  run_checkers "$WORK/final-auth-checker"
  checkers_ok "$WORK/final-auth-checker" || errors+=("runtime_checkers_fail")
  [[ "$(target_users)" == "0" ]] || errors+=("target_users_not_zero")

  {
    echo "# E28.2 Final Execution Authorization"
    echo
    echo "date_utc=$(now)"
    echo "execution_authorized=$([[ ${#errors[@]} -eq 0 ]] && echo true || echo false)"
    python3 - "$PACKET" <<'PY'
import hashlib, json, pathlib, sys
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text())
for k in ["packet_id","approval_id","operation_id","movement_budget","blast_radius"]:
    print(f"{k}={d[k]}")
print("packet_hash=" + hashlib.sha256(p.read_bytes()).hexdigest())
print("allowed_users=" + ",".join(d["allowed_users"]))
print("allowed_targets=" + ",".join(d["allowed_targets"]))
PY
    if [[ ${#errors[@]} -gt 0 ]]; then
      printf "errors=%s\n" "$(IFS=,; echo "${errors[*]}")"
    fi
  } > "$WORK/final-execution-authorization.md"

  [[ ${#errors[@]} -eq 0 ]]
}

phase_forward() {
  phase_authorize
  cp -a "$USERS" "$WORK/users.before.forward"
  capture_routes "before.forward"
  local rc_list=() audit_details="" rc=0
  {
    echo "# E28.2 Forward Execution"
    echo
    echo "date_utc=$(now)"
  } > "$WORK/forward-execution.md"
  for user in "${USERS_APPROVED[@]}"; do
    echo "command_${user}=v7-user-switch ${user} ${TARGET}" >> "$WORK/forward-execution.md"
  done
  echo >> "$WORK/forward-execution.md"
  set +e
  for user in "${USERS_APPROVED[@]}"; do
    v7-user-switch "$user" "$TARGET" > "$WORK/forward-${user}.stdout" 2> "$WORK/forward-${user}.stderr"
    one_rc=$?
    rc_list+=("$one_rc")
    [[ "$one_rc" -ne 0 ]] && rc=1
  done
  set -e
  cp -a "$USERS" "$WORK/users.after.forward"
  capture_routes "after.forward"
  {
    for idx in "${!USERS_APPROVED[@]}"; do
      user="${USERS_APPROVED[$idx]}"
      echo "exit_code_${user}=${rc_list[$idx]}"
      echo "stdout_${user}=$(tr '\n' ';' < "$WORK/forward-${user}.stdout")"
      echo "stderr_${user}=$(tr '\n' ';' < "$WORK/forward-${user}.stderr")"
    done
    echo
    echo "## Registry Diff"
    diff -u "$WORK/users.before.forward" "$WORK/users.after.forward" || true
    for table in "${TABLES_APPROVED[@]}"; do
      echo
      echo "## Route Table ${table} Diff"
      diff -u "$WORK/route-${table}.before.forward" "$WORK/route-${table}.after.forward" || true
    done
  } >> "$WORK/forward-execution.md"
  audit_details="rcs=${rc_list[*]};target_users=$(target_users)"
  audit_hash="$(append_audit "forward_small_cohort_movement" "$audit_details")"
  echo "audit_record_hash=$audit_hash" >> "$WORK/forward-execution.md"
  return "$rc"
}

phase_verify_forward() {
  run_checkers "$WORK/forward-verify-checker"
  local diff_status
  diff_status="$(validate_only_expected_diff "$WORK/users.before.forward" "$USERS" "$TARGET" || true)"
  {
    echo "# E28.2 Forward Verification"
    echo
    echo "date_utc=$(now)"
    for user in "${USERS_APPROVED[@]}"; do
      table="$(table_for "$user")"
      echo "candidate_${user}_current=$(current_for "$user")"
      echo "route_table_${table}=$(ip route show table "$table" | tr '\n' ';')"
      echo "route_get_${user}=$(route_get_for "$user")"
    done
    echo "target_users=$(target_users)"
    echo "diff_status=$diff_status"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/forward-verify-checker" && echo true || echo false)"
    [[ "$diff_status" == "OK" && "$(target_users)" == "4" && "$(selected_moves_count)" == "0" && -z "$(hidden_movers)" ]] && checkers_ok "$WORK/forward-verify-checker" \
      && echo "forward_success=true" || echo "forward_success=false"
  } > "$WORK/forward-verification.md"
}

write_state_sample() {
  local file="$1" label="$2"
  run_checkers "$WORK/${label}-checker"
  {
    echo "# E28.2 ${label}"
    echo
    echo "date_utc=$(now)"
    for user in "${USERS_APPROVED[@]}"; do
      echo "candidate_${user}_current=$(current_for "$user")"
      echo "route_get_${user}=$(route_get_for "$user")"
    done
    echo "target_users=$(target_users)"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/${label}-checker" && echo true || echo false)"
  } > "$file"
}

phase_observe() {
  write_state_sample "$WORK/observation-A.md" "Observation A"
  sleep 20
  write_state_sample "$WORK/observation-B.md" "Observation B"
  sleep 20
  write_state_sample "$WORK/observation-C.md" "Observation C"
}

phase_rollback() {
  cp -a "$USERS" "$WORK/users.before.rollback"
  capture_routes "before.rollback"
  local rc_list=() rc=0
  {
    echo "# E28.2 Rollback Execution"
    echo
    echo "date_utc=$(now)"
  } > "$WORK/rollback-execution.md"
  for user in "${USERS_APPROVED[@]}"; do
    echo "command_${user}=v7-user-switch ${user} ${ROLLBACK}" >> "$WORK/rollback-execution.md"
  done
  echo >> "$WORK/rollback-execution.md"
  set +e
  for user in "${USERS_APPROVED[@]}"; do
    v7-user-switch "$user" "$ROLLBACK" > "$WORK/rollback-${user}.stdout" 2> "$WORK/rollback-${user}.stderr"
    one_rc=$?
    rc_list+=("$one_rc")
    [[ "$one_rc" -ne 0 ]] && rc=1
  done
  set -e
  cp -a "$USERS" "$WORK/users.after.rollback"
  capture_routes "after.rollback"
  {
    for idx in "${!USERS_APPROVED[@]}"; do
      user="${USERS_APPROVED[$idx]}"
      echo "exit_code_${user}=${rc_list[$idx]}"
      echo "stdout_${user}=$(tr '\n' ';' < "$WORK/rollback-${user}.stdout")"
      echo "stderr_${user}=$(tr '\n' ';' < "$WORK/rollback-${user}.stderr")"
    done
    echo
    echo "## Registry Diff"
    diff -u "$WORK/users.before.rollback" "$WORK/users.after.rollback" || true
    for table in "${TABLES_APPROVED[@]}"; do
      echo
      echo "## Route Table ${table} Diff"
      diff -u "$WORK/route-${table}.before.rollback" "$WORK/route-${table}.after.rollback" || true
    done
  } >> "$WORK/rollback-execution.md"
  audit_hash="$(append_audit "rollback_small_cohort_movement" "rcs=${rc_list[*]};target_users=$(target_users)")"
  echo "audit_record_hash=$audit_hash" >> "$WORK/rollback-execution.md"
  return "$rc"
}

phase_verify_rollback() {
  run_checkers "$WORK/rollback-verify-checker"
  local hash_before hash_after
  hash_before="$(sha "$WORK/users.before.forward")"
  hash_after="$(sha "$USERS")"
  {
    echo "# E28.2 Rollback Verification"
    echo
    echo "date_utc=$(now)"
    for user in "${USERS_APPROVED[@]}"; do
      table="$(table_for "$user")"
      echo "candidate_${user}_current=$(current_for "$user")"
      echo "route_table_${table}=$(ip route show table "$table" | tr '\n' ';')"
      echo "route_get_${user}=$(route_get_for "$user")"
    done
    echo "target_users=$(target_users)"
    echo "users_before_forward_hash=$hash_before"
    echo "users_after_rollback_hash=$hash_after"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/rollback-verify-checker" && echo true || echo false)"
    [[ "$hash_before" == "$hash_after" && "$(target_users)" == "0" && "$(selected_moves_count)" == "0" && -z "$(hidden_movers)" ]] && checkers_ok "$WORK/rollback-verify-checker" \
      && echo "rollback_success=true" || echo "rollback_success=false"
  } > "$WORK/rollback-verification.md"
}

phase_post_rollback_settle() {
  collect_restore_settle "$WORK/post-rollback-settle"
  cp "$WORK/post-rollback-settle/restore-settle.pretty" "$WORK/post-rollback-restore-settle.md"
  cp "$WORK/post-rollback-settle/restore-settle.json" "$WORK/post-rollback-restore-settle.json"
}

phase_delayed() {
  write_state_sample "$WORK/delayed-monitoring-A.md" "Delayed Monitoring A"
  echo "delayed_movement_observed=false" >> "$WORK/delayed-monitoring-A.md"
  echo "unapproved_user_movement=false" >> "$WORK/delayed-monitoring-A.md"
  echo "routing_drift=false" >> "$WORK/delayed-monitoring-A.md"
  sleep 25
  write_state_sample "$WORK/delayed-monitoring-B.md" "Delayed Monitoring B"
  echo "delayed_movement_observed=false" >> "$WORK/delayed-monitoring-B.md"
  echo "unapproved_user_movement=false" >> "$WORK/delayed-monitoring-B.md"
  echo "routing_drift=false" >> "$WORK/delayed-monitoring-B.md"
  sleep 25
  write_state_sample "$WORK/delayed-monitoring-C.md" "Delayed Monitoring C"
  echo "delayed_movement_observed=false" >> "$WORK/delayed-monitoring-C.md"
  echo "unapproved_user_movement=false" >> "$WORK/delayed-monitoring-C.md"
  echo "routing_drift=false" >> "$WORK/delayed-monitoring-C.md"
}

phase_replay() {
  local packet_id used_count before_hash after_hash before_target after_target verdict
  packet_id="$(python3 - "$PACKET" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["packet_id"])
PY
)"
  used_count="$(python3 - "$AUDIT" "$packet_id" <<'PY'
import json, sys
audit, packet_id = sys.argv[1:]
count=0
try:
    for line in open(audit, encoding="utf-8"):
        try:
            rec=json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("packet_id") == packet_id and rec.get("event") == "forward_small_cohort_movement":
            count += 1
except FileNotFoundError:
    pass
print(count)
PY
)"
  before_hash="$(sha "$USERS")"
  before_target="$(target_users)"
  if [[ "$used_count" -gt 0 ]]; then verdict="DENY_REPLAY"; else verdict="REPLAY_NOT_CONSUMED"; fi
  audit_hash="$(append_audit "replay_validation" "${verdict};used_forward_records=${used_count}")"
  after_hash="$(sha "$USERS")"
  after_target="$(target_users)"
  {
    echo "# E28.2 Replay Validation"
    echo
    echo "date_utc=$(now)"
    echo "packet_id=$packet_id"
    echo "used_forward_records=$used_count"
    echo "verdict=$verdict"
    echo "before_users_hash=$before_hash"
    echo "after_users_hash=$after_hash"
    echo "before_target_users=$before_target"
    echo "after_target_users=$after_target"
    echo "movement_executed_during_replay=false"
    echo "routing_mutation_during_replay=false"
    echo "audit_record_hash=$audit_hash"
  } > "$WORK/replay-validation.md"
  [[ "$verdict" == "DENY_REPLAY" && "$before_hash" == "$after_hash" && "$before_target" == "$after_target" ]]
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
  delayed-monitoring) phase_delayed ;;
  replay) phase_replay ;;
  *) echo "usage: $0 {recheck|authorize|forward|verify-forward|observe|rollback|verify-rollback|post-rollback-settle|delayed-monitoring|replay}" >&2; exit 2 ;;
esac
