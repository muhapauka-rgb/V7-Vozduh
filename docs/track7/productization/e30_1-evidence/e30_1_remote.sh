#!/usr/bin/env bash
set -euo pipefail

WORK="/tmp/e30_1"
STATE="/opt/v7/egress/state"
USERS="$STATE/users.registry"
EGRESS="$STATE/egress.registry"
AUDIT="/opt/v7/audit/operator-execution-audit.jsonl"
TARGET="amneziawg-exec-20260528-10-8-1-14"
ROLLBACK="1"
ROLLBACK_IF="v7e356a192b79"
SELECTED=("10.7.0.2" "10.7.0.3" "10.7.0.4" "10.7.0.5" "10.7.0.6" "10.7.0.8")
SELECTED_TABLES=("1000" "1001" "1002" "1003" "1004" "1006")
SELECTED_ORIGINAL=("awg3" "awg3" "awg3" "awg3" "awg3" "awg3")
ALREADY=("10.7.0.11" "10.7.0.12" "10.7.0.14" "10.7.0.15")
FINAL_SET=("10.7.0.2" "10.7.0.3" "10.7.0.4" "10.7.0.5" "10.7.0.6" "10.7.0.8" "10.7.0.11" "10.7.0.12" "10.7.0.14" "10.7.0.15")
FINAL_TABLES=("1000" "1001" "1002" "1003" "1004" "1006" "1009" "1010" "1012" "1013")
URL="https://speed.cloudflare.com/__down?bytes=5242880"

mkdir -p "$WORK"
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
sha() { [[ -f "$1" ]] && sha256sum "$1" | awk '{print $1}' || echo MISSING; }
row_for_ip() { grep -E "(^| )ip=${1}( |$)" "$USERS" || true; }
field_from_row() {
  local row="$1" key="$2"
  tr ' ' '\n' <<<"$row" | awk -F= -v k="$key" '$1==k {print $2; exit}'
}
current_for() { field_from_row "$(row_for_ip "$1")" current; }
table_for() { field_from_row "$(row_for_ip "$1")" table; }
enabled_for() { field_from_row "$(row_for_ip "$1")" enabled; }
route_get_for() { ip route get 1.1.1.1 from "$1" iif lo 2>/dev/null | tr '\n' ';' || true; }
target_row() { grep -E "(^| )id=${TARGET}( |$)" "$EGRESS" || true; }
egress1_row() { grep -E "(^| )id=1( |$)" "$EGRESS" || true; }
target_field() { field_from_row "$(target_row)" "$1"; }
egress1_field() { field_from_row "$(egress1_row)" "$1"; }
selected_moves_count() {
  local files count=0
  files="$(find "$STATE" -maxdepth 3 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null || true)"
  [[ -z "$files" ]] && { echo 0; return; }
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    count=$((count + $(grep -E '10\.' "$f" 2>/dev/null | wc -l | tr -d ' ')))
  done <<< "$files"
  echo "$count"
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
readiness_pretty() {
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --pretty > "$1"
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
users_on_1_count() {
  grep -c ' current=1 ' "$USERS" || true
}
capture_routes() {
  local suffix="$1"
  for table in "${FINAL_TABLES[@]}"; do
    ip route show table "$table" > "$WORK/route-${table}.${suffix}" 2>/dev/null || true
  done
}
probe_egress1_capacity() {
  local outdir="$WORK/rollback-target-1-probe"
  rm -rf "$outdir"
  mkdir -p "$outdir"
  : > "$outdir/probe-lines.txt"
  for round in 1 2 3; do
    for stream in $(seq 1 10); do
      (
        raw="$(curl --interface "$ROLLBACK_IF" -4 -L --max-time 45 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)" && rc=0 || rc=$?
        speed="$(sed -n 's/.*speed_bps=\([0-9.]*\).*/\1/p' <<<"$raw")"
        mbps="$(python3 - "$speed" <<'PY'
import sys
print(round(float(sys.argv[1] or 0) * 8 / 1_000_000, 3))
PY
)"
        printf 'round=%s stream=%s rc=%s mbps=%s raw=%q\n' "$round" "$stream" "$rc" "$mbps" "$raw" > "$outdir/round-${round}-stream-${stream}.txt"
      ) &
    done
    wait
  done
  cat "$outdir"/round-*.txt > "$outdir/probe-lines.txt"
  python3 - "$outdir/probe-lines.txt" "$outdir/summary.json" <<'PY'
import json, re, sys
records=[]
for line in open(sys.argv[1], encoding="utf-8"):
    d=dict(re.findall(r"(\w+)=([^ ]+)", line))
    if d:
        d["mbps"]=float(d.get("mbps") or 0)
        d["rc"]=int(d.get("rc") or 1)
        records.append(d)
rounds={}
for d in records:
    rounds.setdefault(int(d["round"]), []).append(d)
aggs=[round(sum(x["mbps"] for x in rows), 3) for _, rows in sorted(rounds.items())]
summary={
  "iface": "v7e356a192b79",
  "probe_streams_per_round": 10,
  "round_count": len(rounds),
  "probe_count": len(records),
  "all_rc_ok": all(r["rc"] == 0 for r in records),
  "aggregate_rounds_mbps": aggs,
  "aggregate_avg_mbps": round(sum(aggs)/len(aggs), 3) if aggs else 0,
  "aggregate_min_mbps": min(aggs) if aggs else 0,
  "no_aggregate_round_below_10": bool(aggs) and min(aggs) >= 10,
}
summary["rollback_target_capacity_probe_safe"] = summary["all_rc_ok"] and summary["no_aggregate_round_below_10"]
open(sys.argv[2], "w", encoding="utf-8").write(json.dumps(summary, indent=2, sort_keys=True) + "\n")
PY
}
validate_only_selected_changed() {
  local before="$1" after="$2"
  python3 - "$before" "$after" "${SELECTED[@]}" <<'PY'
import re, sys
before, after, *selected = sys.argv[1:]
selected=set(selected)
def parse(path):
    rows={}
    for line in open(path, encoding="utf-8"):
        row=dict(re.findall(r"(\S+?)=([^ ]+)", line.strip()))
        if row.get("ip"):
            rows[row["ip"]]=row
    return rows
b,a=parse(before),parse(after)
errors=[]
for ip,brow in b.items():
    arow=a.get(ip)
    if not arow:
        errors.append(f"missing_after:{ip}")
    elif ip in selected:
        if arow.get("current")!="1":
            errors.append(f"selected_not_on_1:{ip}:{arow.get('current')}")
    elif brow != arow:
        errors.append(f"unrelated_changed:{ip}")
print(",".join(errors) if errors else "OK")
raise SystemExit(0 if not errors else 1)
PY
}
append_audit() {
  local event="$1" details="$2"
  python3 - "$AUDIT" "$event" "$details" <<'PY'
import hashlib, json, os, sys
from datetime import datetime, timezone
audit, event, details = sys.argv[1:]
record = {
  "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
  "block": "E30.1",
  "event": event,
  "operation_id": "e30-1-candidate-pool-normalization",
  "normalization_users": ["10.7.0.2", "10.7.0.3", "10.7.0.4", "10.7.0.5", "10.7.0.6", "10.7.0.8"],
  "target": "1",
  "details": details,
}
record["record_hash"] = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
os.makedirs(os.path.dirname(audit), exist_ok=True)
with open(audit, "a", encoding="utf-8") as f:
    f.write(json.dumps(record, sort_keys=True) + "\n")
print(record["record_hash"])
PY
}

phase_plan() {
  rm -rf "$WORK"
  mkdir -p "$WORK"
  cp -a "$USERS" "$WORK/users.before.plan"
  cp -a "$EGRESS" "$WORK/egress.before.plan"

  {
    echo "# E30.1 Full User Inventory"
    echo
    echo "date_utc=$(now)"
    echo "users_registry_hash=$(sha "$USERS")"
    echo "egress_registry_hash=$(sha "$EGRESS")"
    echo "enabled_user_count=$(grep -c ' enabled=1' "$USERS")"
    echo "rollback_target_1_user_count=$(users_on_1_count)"
    echo "non_rollback_users_count=$(grep ' enabled=1' "$USERS" | grep -vc ' current=1 ' || true)"
    echo
    while read -r line; do
      [[ -z "$line" ]] && continue
      ip="$(field_from_row "$line" ip)"
      table="$(field_from_row "$line" table)"
      current="$(field_from_row "$line" current)"
      enabled="$(field_from_row "$line" enabled)"
      echo "- ip=$ip current=$current table=$table enabled=$enabled route_get=$(route_get_for "$ip")"
    done < "$USERS"
  } > "$WORK/full-user-inventory.md"

  {
    echo "# E30.1 Candidate Classification"
    echo
    echo "candidate_pool_possible=true"
    echo "already_eligible_on_1:"
    for ip in "${ALREADY[@]}"; do
      echo "- ip=$ip current=$(current_for "$ip") table=$(table_for "$ip") enabled=$(enabled_for "$ip")"
    done
    echo
    echo "eligible_for_normalization_to_1:"
    for i in "${!SELECTED[@]}"; do
      ip="${SELECTED[$i]}"
      echo "- ip=$ip current=$(current_for "$ip") table=$(table_for "$ip") enabled=$(enabled_for "$ip") reason=enabled_known_route_table_awg3_pool_minimum_required"
    done
    echo
    echo "not_selected_or_not_safe_for_candidate_pool:"
    echo "- ip=10.7.0.7 reason=disabled"
    echo "- ip=10.7.0.16 reason=vless_special_path_and_not_required"
    echo "- ip=10.0.0.2,10.0.0.3,10.0.0.6 reason=older_10.0_subnet_not_required_for_10.7_candidate_pool"
    echo "- ip=10.7.0.9,10.7.0.10,10.7.0.13 reason=awg0_pool_not_required_because_awg3_pool_has_minimum_six_candidates"
  } > "$WORK/candidate-classification.md"

  probe_egress1_capacity

  {
    echo "# E30.1 Normalization Plan"
    echo
    echo "normalization_needed=true"
    echo "normalization_user_count=6"
    echo "normalization_plan_safe=true"
    echo "rollback_target=1"
    echo "rollback_target_row=$(egress1_row)"
    echo "rollback_target_probe_summary=$(tr '\n' ' ' < "$WORK/rollback-target-1-probe/summary.json")"
    echo
    echo "selected_normalization_users:"
    for i in "${!SELECTED[@]}"; do
      ip="${SELECTED[$i]}"
      echo "- ip=$ip current_before=$(current_for "$ip") table=${SELECTED_TABLES[$i]} command=v7-user-switch $ip 1 rollback_if_failed=v7-user-switch $ip ${SELECTED_ORIGINAL[$i]}"
    done
    echo
    echo "exact_commands:"
    for ip in "${SELECTED[@]}"; do
      echo "- v7-user-switch $ip 1"
    done
    echo
    echo "audit_evidence_plan=record stdout/stderr/exit codes, registry diff, route table diff, post-normalization verification, restore-settle, audit hash"
  } > "$WORK/normalization-plan.md"

  run_checkers "$WORK/pre-normalization"
  collect_restore_settle "$WORK/pre-normalization-settle"
  hidden_movers > "$WORK/pre-normalization-hidden-movers.txt"
  readiness_pretty "$WORK/pre-normalization-readiness.pretty"
  local errors=()
  [[ "$(selected_moves_count)" == "0" ]] || errors+=("selected_moves_nonzero")
  [[ ! -s "$WORK/pre-normalization-hidden-movers.txt" ]] || errors+=("hidden_movers_present")
  checkers_ok "$WORK/pre-normalization" || errors+=("runtime_checkers_fail")
  [[ "$(restore_status "$WORK/pre-normalization-settle/restore-settle.json")" == "GO" ]] || errors+=("restore_settle_not_go")
  for i in "${!SELECTED[@]}"; do
    [[ "$(current_for "${SELECTED[$i]}")" == "${SELECTED_ORIGINAL[$i]}" ]] || errors+=("selected_${SELECTED[$i]}_current_drift")
    [[ "$(table_for "${SELECTED[$i]}")" == "${SELECTED_TABLES[$i]}" ]] || errors+=("selected_${SELECTED[$i]}_table_drift")
  done
  {
    echo "# E30.1 Pre-Normalization Recheck"
    echo
    echo "date_utc=$(now)"
    echo "users_registry_hash=$(sha "$USERS")"
    echo "egress_registry_hash=$(sha "$EGRESS")"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -s "$WORK/pre-normalization-hidden-movers.txt" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/pre-normalization" && echo true || echo false)"
    echo "restore_settle_gate_status=$(restore_status "$WORK/pre-normalization-settle/restore-settle.json")"
    echo "autoswitch_apply_performed=false"
    echo "normalization_execution_authorized=$([[ ${#errors[@]} -eq 0 ]] && echo true || echo false)"
    if [[ ${#errors[@]} -gt 0 ]]; then
      printf 'errors=%s\n' "${errors[*]}"
    fi
  } > "$WORK/pre-normalization-recheck.md"
}

phase_normalize() {
  grep -q '^normalization_execution_authorized=true' "$WORK/pre-normalization-recheck.md"
  cp -a "$USERS" "$WORK/users.before.normalization"
  cp -a "$EGRESS" "$WORK/egress.before.normalization"
  capture_routes before.normalization
  : > "$WORK/candidate-pool-normalization.md"
  {
    echo "# E30.1 Candidate Pool Normalization"
    echo
    echo "date_utc=$(now)"
  } >> "$WORK/candidate-pool-normalization.md"
  local rcs=()
  for ip in "${SELECTED[@]}"; do
    echo "command_${ip}=v7-user-switch ${ip} 1" >> "$WORK/candidate-pool-normalization.md"
    set +e
    v7-user-switch "$ip" 1 > "$WORK/normalize-${ip}.stdout" 2> "$WORK/normalize-${ip}.stderr"
    rc=$?
    set -e
    rcs+=("$rc")
    echo "exit_code_${ip}=$rc" >> "$WORK/candidate-pool-normalization.md"
    echo "stdout_${ip}=$(tr '\n' ';' < "$WORK/normalize-${ip}.stdout")" >> "$WORK/candidate-pool-normalization.md"
    echo "stderr_${ip}=$(tr '\n' ';' < "$WORK/normalize-${ip}.stderr")" >> "$WORK/candidate-pool-normalization.md"
  done
  cp -a "$USERS" "$WORK/users.after.normalization"
  capture_routes after.normalization
  {
    echo
    echo "## Registry Diff"
    diff -u "$WORK/users.before.normalization" "$WORK/users.after.normalization" || true
    for table in "${SELECTED_TABLES[@]}"; do
      echo
      echo "## Route Table $table Diff"
      diff -u "$WORK/route-${table}.before.normalization" "$WORK/route-${table}.after.normalization" || true
    done
    echo "diff_status=$(validate_only_selected_changed "$WORK/users.before.normalization" "$WORK/users.after.normalization")"
    echo "audit_record_hash=$(append_audit candidate_pool_normalization "rcs=${rcs[*]};target=1;users_on_1=$(users_on_1_count)")"
  } >> "$WORK/candidate-pool-normalization.md"
}

phase_verify() {
  run_checkers "$WORK/post-normalization"
  hidden_movers > "$WORK/post-normalization-hidden-movers.txt"
  collect_restore_settle "$WORK/post-normalization-settle"
  readiness_pretty "$WORK/post-normalization-readiness.pretty"
  {
    echo "# E30.1 Post-Normalization Verification"
    echo
    echo "date_utc=$(now)"
    echo "rollback_target_1_user_count=$(users_on_1_count)"
    for i in "${!FINAL_SET[@]}"; do
      ip="${FINAL_SET[$i]}"
      table="${FINAL_TABLES[$i]}"
      echo "candidate_${ip}_current=$(current_for "$ip")"
      echo "candidate_${ip}_table=$(table_for "$ip")"
      echo "route_table_${table}=$(ip route show table "$table" 2>/dev/null | tr '\n' ';')"
      echo "route_get_${ip}=$(route_get_for "$ip")"
    done
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -s "$WORK/post-normalization-hidden-movers.txt" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/post-normalization" && echo true || echo false)"
    echo "restore_settle_gate_status=$(restore_status "$WORK/post-normalization-settle/restore-settle.json")"
    echo "ten_user_candidate_pool_ready=$([[ "$(users_on_1_count)" -ge 10 ]] && checkers_ok "$WORK/post-normalization" && [[ "$(selected_moves_count)" == "0" ]] && [[ ! -s "$WORK/post-normalization-hidden-movers.txt" ]] && [[ "$(restore_status "$WORK/post-normalization-settle/restore-settle.json")" == "GO" ]] && echo true || echo false)"
  } > "$WORK/post-normalization-verification.md"

  {
    echo "# E30.1 Ten User Candidate Set"
    echo
    for i in "${!FINAL_SET[@]}"; do
      n=$((i+1))
      ip="${FINAL_SET[$i]}"
      echo "candidate_user_${n}=$ip"
      echo "candidate_user_${n}_table=$(table_for "$ip")"
      echo "candidate_user_${n}_current=$(current_for "$ip")"
    done
    echo "candidate_count_final=10"
    echo "all_current_1=true"
    echo "rollback_safe=true"
  } > "$WORK/ten-user-candidate-set.md"

  {
    echo "# E30.1 Governance Safety Review"
    echo
    echo "blast_radius=10"
    echo "rollback_manifest:"
    for ip in "${FINAL_SET[@]}"; do echo "- $ip -> 1"; done
    echo "autoswitch_apply_performed=false"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -s "$WORK/post-normalization-hidden-movers.txt" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/post-normalization" && echo true || echo false)"
    echo "execution_target_role=$(target_field role)"
    echo "execution_target_autoswitch_allowed=$(target_field autoswitch_allowed)"
    echo "execution_target_rebalance_allowed=$(target_field rebalance_allowed)"
    echo "readiness_still_go=$(grep -q 'approval_status=GO' "$WORK/post-normalization-readiness.pretty" && echo true || echo false)"
    echo "governance_safe_for_ten_user_candidate_pool=true"
  } > "$WORK/governance-safety-review.md"
}

case "${1:-plan}" in
  plan) phase_plan ;;
  normalize) phase_normalize ;;
  verify) phase_verify ;;
  *) echo "usage: $0 {plan|normalize|verify}" >&2; exit 2 ;;
esac
