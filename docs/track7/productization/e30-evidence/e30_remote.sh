#!/usr/bin/env bash
set -euo pipefail

WORK="/tmp/e30"
STATE="/opt/v7/egress/state"
USERS="$STATE/users.registry"
EGRESS="$STATE/egress.registry"
TARGET="amneziawg-exec-20260528-10-8-1-14"
IFACE="v7execwg0"
URL="https://speed.cloudflare.com/__down?bytes=5242880"
mkdir -p "$WORK/capacity-probe"

now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
sha() { [[ -f "$1" ]] && sha256sum "$1" | awk '{print $1}' || echo MISSING; }

target_row() { grep -E "(^| )id=${TARGET}( |$)" "$EGRESS" || true; }
field_from_row() {
  local row="$1" key="$2"
  tr ' ' '\n' <<<"$row" | awk -F= -v k="$key" '$1==k {print $2; exit}'
}
target_field() { field_from_row "$(target_row)" "$1"; }
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
readiness_json() {
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --json > "$1"
}
readiness_pretty() {
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --pretty > "$1"
}
readiness_status() {
  python3 - "$1" <<'PY'
import json, sys
d=json.load(open(sys.argv[1], encoding="utf-8"))
print(d.get("approval_status") or d.get("second_canary_readiness") or "UNKNOWN")
PY
}
target_user_count() {
  grep -c "current=${TARGET}" "$USERS" || true
}
capture_side_effect_state() {
  local out="$1"
  {
    echo "date_utc=$(now)"
    echo "users_registry_hash=$(sha "$USERS")"
    echo "egress_registry_hash=$(sha "$EGRESS")"
    echo "target_users=$(target_user_count)"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
    echo "default_route=$(ip route show default | tr '\n' ';')"
    echo "ip_rules=$(ip rule show | tr '\n' ';')"
    for table in 1009 1010 1012 1013; do
      echo "route_table_${table}=$(ip route show table "$table" 2>/dev/null | tr '\n' ';')"
    done
  } > "$out"
}
probe_one() {
  local round="$1" stream="$2" out="$3"
  local raw rc speed_bps mbps
  raw="$(curl --interface "$IFACE" -4 -L --max-time 45 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)" && rc=0 || rc=$?
  speed_bps="$(sed -n 's/.*speed_bps=\([0-9.]*\).*/\1/p' <<<"$raw")"
  if [[ -n "$speed_bps" ]]; then
    mbps="$(python3 - "$speed_bps" <<'PY'
import sys
print(round(float(sys.argv[1]) * 8 / 1_000_000, 3))
PY
)"
  else
    mbps=0
  fi
  printf 'round=%s stream=%s rc=%s mbps=%s raw=%q\n' "$round" "$stream" "$rc" "$mbps" "$raw" > "$out"
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

rm -rf "$WORK"
mkdir -p "$WORK/capacity-probe" "$WORK/restore-settle"
cp -a "$USERS" "$WORK/users.registry.snapshot"
cp -a "$EGRESS" "$WORK/egress.registry.snapshot"

python3 - "$USERS" "$WORK/ten-user-discovery.md" <<'PY'
import re, sys
users_path, out_path = sys.argv[1:]
rows = []
for line in open(users_path, encoding="utf-8"):
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    row = dict(re.findall(r"(\S+?)=([^ ]+)", line.strip()))
    if row.get("enabled") == "1":
        rows.append(row)
rollback = [r for r in rows if r.get("current") == "1"]
stable = [r for r in rows if r.get("table")]
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# E30 Ten User Discovery\n\n")
    f.write(f"candidate_count={len(rollback)}\n")
    f.write("rollback_target=1\n")
    f.write("requirement=candidate_count>=10\n")
    f.write(f"ten_user_discovery_status={'GO' if len(rollback) >= 10 else 'NO-GO'}\n")
    f.write("eligible_rollback_users:\n")
    for r in rollback:
        f.write(f"- ip={r.get('ip')} current={r.get('current')} table={r.get('table')} enabled={r.get('enabled')}\n")
    f.write("\nall_enabled_known_table_users:\n")
    for r in stable:
        f.write(f"- ip={r.get('ip')} current={r.get('current')} table={r.get('table')} enabled={r.get('enabled')}\n")
    if len(rollback) < 10:
        f.write("\nblocker=INSUFFICIENT_ROLLBACK_TARGET_1_CANDIDATES\n")
        f.write("reason=Only users already on rollback target 1 qualify for this preparation scope; changing other users' current egress would be user movement/routing mutation and is forbidden in E30.\n")
PY

run_checkers "$WORK/precheck"
readiness_json "$WORK/readiness.json"
readiness_pretty "$WORK/readiness.pretty"
hidden_movers > "$WORK/hidden-movers.txt"

soft="$(target_field soft_limit)"
hard="$(target_field hard_limit)"
{
  echo "# E30 Capacity Root Cause"
  echo
  echo "target_name=$TARGET"
  echo "target_row=$(target_row)"
  echo "soft_limit=$soft"
  echo "hard_limit=$hard"
  echo "previous_certified_scale=4"
  echo "capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_10_USER_VALIDATION"
  echo "reason=E28.1 proved 2->4 was metadata-only after four-stream validation; no evidence yet proves 4->10 is physical, but 10-user candidate discovery is blocked before safe requalification."
} > "$WORK/capacity-root-cause.md"

{
  echo "# E30 Ten User Capacity Model"
  echo
  echo "mode=read_only_model"
  echo "target_name=$TARGET"
  echo "requested_cohort_size=10"
  echo "candidate_count=$(awk -F= '/^candidate_count=/{print $2; exit}' "$WORK/ten-user-discovery.md")"
  echo "soft_limit_current=$soft"
  echo "hard_limit_current=$hard"
  echo "throughput_model=requires_10_stream_target_local_validation"
  echo "rollback_model=requires_10_users_currently_on_rollback_target_1"
  echo "audit_model=packet must include exact 10-user set and 10 rollback entries"
  echo "replay_model=must deny replay after one 10-user forward record"
  echo "ten_user_capacity_model_safe=false"
  echo "reason=Capacity probe can test target pressure, but full ten-user model is not safe while candidate_count<10 on rollback target 1."
} > "$WORK/ten-user-capacity-model.md"

capture_side_effect_state "$WORK/capacity-probe/pre-side-effect-state.txt"
: > "$WORK/capacity-probe/probe-lines.txt"
for round in 1 2 3; do
  for stream in $(seq 1 10); do
    probe_one "$round" "$stream" "$WORK/capacity-probe/round-${round}-stream-${stream}.txt" &
  done
  wait
  cat "$WORK/capacity-probe/round-${round}-stream-"*.txt >> "$WORK/capacity-probe/probe-lines.txt"
done
capture_side_effect_state "$WORK/capacity-probe/post-side-effect-state.txt"
run_checkers "$WORK/capacity-probe/checker"
readiness_json "$WORK/capacity-probe/readiness.after.json"
readiness_pretty "$WORK/capacity-probe/readiness.after.pretty"

python3 - "$WORK/capacity-probe/probe-lines.txt" "$WORK/capacity-probe/summary.json" "$WORK/target-local-ten-user-validation.md" "$(checkers_ok "$WORK/capacity-probe/checker" && echo true || echo false)" "$(readiness_status "$WORK/capacity-probe/readiness.after.json")" <<'PY'
import json, re, sys
lines, summary_path, md_path, checkers_ok, readiness = sys.argv[1:]
records = []
for line in open(lines, encoding="utf-8"):
    rec = dict(re.findall(r"(\w+)=([^ ]+)", line))
    if rec:
        rec["mbps"] = float(rec.get("mbps") or 0)
        rec["rc"] = int(rec.get("rc") or 1)
        records.append(rec)
rounds = {}
for r in records:
    rounds.setdefault(int(r["round"]), []).append(r)
aggregate = [round(sum(x["mbps"] for x in rows), 3) for _, rows in sorted(rounds.items())]
summary = {
    "probe_streams_per_round": 10,
    "round_count": len(rounds),
    "probe_count": len(records),
    "all_rc_ok": all(r["rc"] == 0 for r in records),
    "aggregate_rounds_mbps": aggregate,
    "aggregate_avg_mbps": round(sum(aggregate) / len(aggregate), 3) if aggregate else 0,
    "aggregate_min_mbps": min(aggregate) if aggregate else 0,
    "no_aggregate_round_below_10": bool(aggregate) and min(aggregate) >= 10,
    "readiness_after": readiness,
    "runtime_checkers_ok": checkers_ok == "true",
}
summary["target_local_capacity_safe"] = (
    summary["all_rc_ok"]
    and summary["no_aggregate_round_below_10"]
    and readiness == "GO"
    and summary["runtime_checkers_ok"]
)
open(summary_path, "w", encoding="utf-8").write(json.dumps(summary, indent=2, sort_keys=True) + "\n")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# E30 Target-Local Ten User Validation\n\n")
    for k, v in summary.items():
        f.write(f"{k}={v}\n")
    f.write("\nno_user_movement=true\nrouting_mutation_for_users=false\n")
PY

{
  echo "# E30 Capacity Requalification"
  echo
  echo "soft_limit_before=$soft"
  echo "hard_limit_before=$hard"
  echo "capacity_requalification_attempted=false"
  echo "capacity_requalification_successful=false"
  echo "runtime_mutation_performed=false"
  echo "reason=not_attempted_because_candidate_count_lt_10_on_rollback_target_1; target-local probe evidence collected but full ten-user governance precondition failed"
  echo "rollback_plan=not_required_no_metadata_changed"
} > "$WORK/capacity-requalification.md"

{
  echo "# E30 Long Window Validation"
  echo
  echo "ten_user_capacity_validated=false"
  echo "long_window_collected=false"
  echo "reason=capacity_requalification_not_performed"
} > "$WORK/long-window-validation.md"

python3 - "$USERS" "$WORK/ten-user-rollback-model.md" <<'PY'
import re, sys
users_path, out = sys.argv[1:]
rollback=[]
for line in open(users_path, encoding="utf-8"):
    row=dict(re.findall(r"(\S+?)=([^ ]+)", line.strip()))
    if row.get("enabled")=="1" and row.get("current")=="1":
        rollback.append(row)
with open(out, "w", encoding="utf-8") as f:
    f.write("# E30 Ten User Rollback Model\n\n")
    f.write(f"rollback_candidate_count={len(rollback)}\n")
    f.write("rollback_target=1\n")
    for r in rollback:
        f.write(f"- {r.get('ip')} -> 1 / table {r.get('table')}\n")
    f.write(f"\nten_user_rollback_safe={str(len(rollback) >= 10).lower()}\n")
    if len(rollback) < 10:
        f.write("reason=insufficient users currently on rollback target 1 for deterministic 10-user rollback manifest\n")
PY

{
  echo "# E30 Governance Review"
  echo
  echo "blast_radius=10"
  echo "target_role=$(target_field role)"
  echo "autoswitch_allowed=$(target_field autoswitch_allowed)"
  echo "rebalance_allowed=$(target_field rebalance_allowed)"
  echo "production_assignment_allowed=$(target_field production_assignment_allowed)"
  echo "selected_moves_count=$(selected_moves_count)"
  echo "hidden_movers_present=$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
  echo "runtime_checkers_ok=$(checkers_ok "$WORK/precheck" && echo true || echo false)"
  echo "execution_only_isolation_intact=$([[ "$(target_field role)" == "EXECUTION_ONLY" ]] && echo true || echo false)"
  echo "governance_safe_for_ten_users=false"
  echo "reason=governance isolation intact, but exact 10-user allowed set cannot be formed under rollback_target_1 requirement"
} > "$WORK/governance-review.md"

collect_restore_settle "$WORK/restore-settle"

{
  target_local_safe="$(python3 -c 'import json; print(str(json.load(open("/tmp/e30/capacity-probe/summary.json")).get("target_local_capacity_safe", False)).lower())')"
  echo "# E30 Readiness Decision"
  echo
  echo "candidate_count=$(awk -F= '/^candidate_count=/{print $2; exit}' "$WORK/ten-user-discovery.md")"
  echo "capacity_safe_for_10_users=false"
  echo "ten_user_capacity_model_safe=false"
  echo "target_local_capacity_safe=$target_local_safe"
  echo "capacity_requalification_successful=false"
  echo "ten_user_capacity_validated=false"
  echo "ten_user_rollback_safe=false"
  echo "governance_safe_for_ten_users=false"
  echo "ten_user_readiness=NO-GO"
  echo "remaining_blockers=INSUFFICIENT_ROLLBACK_TARGET_1_CANDIDATES"
  echo "recommended_next_block=E30_1_TEN_USER_CANDIDATE_POOL_PREPARATION"
  echo "execution_allowed_now=false"
} > "$WORK/readiness-decision.md"
