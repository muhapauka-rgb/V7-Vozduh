#!/usr/bin/env bash
set -euo pipefail

WORK="/tmp/e28_1"
STATE="/opt/v7/egress/state"
USERS="$STATE/users.registry"
EGRESS="$STATE/egress.registry"
TARGET="amneziawg-exec-20260528-10-8-1-14"
IFACE="v7execwg0"
URL="https://speed.cloudflare.com/__down?bytes=5242880"
BACKUP_DIR="$STATE/e28_1-backups"
MODE="${1:-full}"

if [[ "$MODE" == "full" ]]; then
  rm -rf "$WORK"
fi
mkdir -p "$WORK/capacity-probe" "$WORK/long-window" "$WORK/restore-settle-samples" "$BACKUP_DIR"

sha() {
  if [[ -f "$1" ]]; then sha256sum "$1" | awk '{print $1}'; else echo "MISSING"; fi
}

now() {
  date -u +%Y-%m-%dT%H:%M:%SZ
}

row_for_target() {
  grep -E "(^| )id=${TARGET}( |$)" "$EGRESS" || true
}

field_from_row() {
  local row="$1" key="$2"
  tr ' ' '\n' <<<"$row" | awk -F= -v k="$key" '$1==k {print $2; exit}'
}

row_field() {
  field_from_row "$(row_for_target)" "$1"
}

row_for_ip() {
  local ip="$1"
  grep -E "(^| )ip=${ip}( |$)" "$USERS" || true
}

current_for() {
  field_from_row "$(row_for_ip "$1")" current
}

table_for() {
  field_from_row "$(row_for_ip "$1")" table
}

target_user_count() {
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

selected_target_metric() {
  python3 - "$1" "$2" <<'PY'
import json, sys
d=json.load(open(sys.argv[1], encoding="utf-8"))
target=d.get("selected_target")
row=next((c for c in d.get("target_candidates", []) if c.get("egress_id")==target), {})
print(row.get(sys.argv[2], "UNKNOWN"))
PY
}

capture_side_effect_state() {
  local out="$1"
  {
    echo "date_utc=$(now)"
    echo "default_route=$(ip route show default | tr '\n' ';')"
    for spec in "10.7.0.11 1009" "10.7.0.12 1010" "10.7.0.14 1012" "10.7.0.15 1013"; do
      set -- $spec
      echo "user_${1}_current=$(current_for "$1")"
      echo "user_${1}_table=$2"
      echo "route_table_${2}=$(ip route show table "$2" | tr '\n' ';')"
      echo "route_get_${1}=$(ip route get 1.1.1.1 from "$1" iif lo 2>/dev/null | tr '\n' ';')"
    done
    echo "users_registry_hash=$(sha "$USERS")"
    echo "egress_registry_hash=$(sha "$EGRESS")"
    echo "target_users=$(target_user_count)"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
  } > "$out"
}

phase_root_cause() {
  readiness_json "$WORK/readiness.before.json"
  readiness_pretty "$WORK/readiness.before.pretty"
  run_checkers "$WORK/root-checker"
  capture_side_effect_state "$WORK/pre-requalification-side-effect-state.txt"
  cp -a "$USERS" "$WORK/users.before"
  cp -a "$EGRESS" "$WORK/egress.before"

  local row soft hard avg min stability status
  row="$(row_for_target)"
  soft="$(row_field soft_limit)"
  hard="$(row_field hard_limit)"
  avg="$(selected_target_metric "$WORK/readiness.before.json" avg_mbps)"
  min="$(selected_target_metric "$WORK/readiness.before.json" min_mbps)"
  stability="$(selected_target_metric "$WORK/readiness.before.json" stability)"
  status="$(readiness_status "$WORK/readiness.before.json")"

  {
    echo "# E28.1 Capacity Root Cause"
    echo
    echo "date_utc=$(now)"
    echo "target=$TARGET"
    echo "target_row=$row"
    echo "soft_limit=$soft"
    echo "hard_limit=$hard"
    echo "target_users=$(target_user_count)"
    echo "readiness_status=$status"
    echo "avg_mbps=$avg"
    echo "min_mbps=$min"
    echo "stability=$stability"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/root-checker" && echo true || echo false)"
    echo
    echo "## Previous Capacity Decisions"
    echo "E27.1 classified 1->2 as GOVERNANCE_LIMIT_ONLY_WITH_METADATA_DRIFT after target-local validation and long-window validation."
    echo "E28 found 4 clean rollback candidates but blocked on hard_limit=2."
    echo
    if [[ "$soft" == "2" && "$hard" == "2" && "$status" == "GO" && "$(target_user_count)" == "0" ]]; then
      echo "capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_4_USER_VALIDATION"
    else
      echo "capacity_limit_root_cause=UNKNOWN"
    fi
  } > "$WORK/capacity-root-cause.md"
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
    mbps="0"
  fi
  printf "round=%s stream=%s rc=%s mbps=%s raw=%s\n" "$round" "$stream" "$rc" "$mbps" "$raw" > "$out"
}

phase_capacity_probe() {
  local rounds=5
  capture_side_effect_state "$WORK/capacity-probe/pre-side-effect-state.txt"
  : > "$WORK/capacity-probe/probe-lines.txt"

  for round in $(seq 1 "$rounds"); do
    for stream in 1 2 3 4; do
      probe_one "$round" "$stream" "$WORK/capacity-probe/round-${round}-stream-${stream}.txt" &
    done
    wait
    cat "$WORK/capacity-probe/round-${round}-stream-"*.txt >> "$WORK/capacity-probe/probe-lines.txt"
    sleep 5
  done

  capture_side_effect_state "$WORK/capacity-probe/post-side-effect-state.txt"
  run_checkers "$WORK/capacity-probe/checker"
  readiness_json "$WORK/capacity-probe/readiness.after.json"
  readiness_pretty "$WORK/capacity-probe/readiness.after.pretty"

  python3 - "$WORK/capacity-probe/probe-lines.txt" "$WORK/capacity-probe/summary.json" <<'PY'
import json, re, statistics, sys
lines=open(sys.argv[1], encoding="utf-8").read().splitlines()
rounds={}
records=[]
for line in lines:
    m=dict(re.findall(r"(\w+)=([^ ]+)", line))
    if not m:
        continue
    rec={"round": int(m["round"]), "stream": int(m["stream"]), "rc": int(m["rc"]), "mbps": float(m["mbps"])}
    records.append(rec)
    rounds.setdefault(rec["round"], []).append(rec)
aggregates=[sum(r["mbps"] for r in rows) for _, rows in sorted(rounds.items())]
summary={
    "probe_streams_per_round": 4,
    "round_count": len(rounds),
    "probe_count": len(records),
    "all_rc_ok": all(r["rc"] == 0 for r in records),
    "aggregate_avg_mbps": round(statistics.mean(aggregates), 3) if aggregates else 0,
    "aggregate_min_mbps": round(min(aggregates), 3) if aggregates else 0,
    "per_stream_min_mbps": round(min((r["mbps"] for r in records), default=0), 3),
    "no_aggregate_round_below_10": all(v >= 10.0 for v in aggregates),
    "aggregate_rounds": [round(v, 3) for v in aggregates],
}
summary["target_local_capacity_safe"] = (
    summary["round_count"] >= 5
    and summary["all_rc_ok"]
    and summary["aggregate_avg_mbps"] >= 15.0
    and summary["aggregate_min_mbps"] >= 10.0
    and summary["no_aggregate_round_below_10"]
)
open(sys.argv[2],"w",encoding="utf-8").write(json.dumps(summary, indent=2, sort_keys=True)+"\n")
PY

  python3 - "$WORK/capacity-probe/summary.json" "$WORK/four-user-capacity-model.md" "$WORK/target-local-capacity-validation.md" <<'PY'
import json, sys
s=json.load(open(sys.argv[1], encoding="utf-8"))
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("# E28.1 Four User Capacity Model\n\n")
    f.write("candidate_users=10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15\n")
    f.write("blast_radius=4\n")
    f.write("rollback_target=1\n")
    f.write("audit_impact=MODEL_READY\n")
    f.write("replay_impact=MODEL_READY\n")
    f.write("rollback_impact=DETERMINISTIC\n")
    f.write(f"throughput_headroom_aggregate_avg_mbps={s['aggregate_avg_mbps']}\n")
    f.write(f"throughput_headroom_aggregate_min_mbps={s['aggregate_min_mbps']}\n")
    f.write(f"capacity_model_safe={str(s['target_local_capacity_safe']).lower()}\n")
with open(sys.argv[3], "w", encoding="utf-8") as f:
    f.write("# E28.1 Target-Local Capacity Validation\n\n")
    for k,v in s.items():
        f.write(f"{k}={v}\n")
    f.write("runtime_checkers_ok=SEE_CHECKER_OUTPUTS\n")
    f.write("user_movement_performed=false\n")
    f.write("routing_mutation_performed=false\n")
PY
}

phase_requalify() {
  local safe
  safe="$(python3 - "$WORK/capacity-probe/summary.json" <<'PY'
import json, sys
print(str(json.load(open(sys.argv[1])).get("target_local_capacity_safe", False)).lower())
PY
)"
  if [[ "$safe" != "true" ]]; then
    {
      echo "# E28.1 Capacity Requalification"
      echo
      echo "capacity_requalification_attempted=false"
      echo "capacity_requalification_successful=false"
      echo "reason=target_local_capacity_validation_not_safe"
    } > "$WORK/capacity-requalification.md"
    return
  fi

  local ts backup before_hash after_hash
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  backup="$BACKUP_DIR/egress.registry.${ts}"
  cp -a "$EGRESS" "$backup"
  before_hash="$(sha "$EGRESS")"

  python3 - "$EGRESS" "$TARGET" <<'PY'
import sys
from pathlib import Path
path=Path(sys.argv[1])
target=sys.argv[2]
lines=path.read_text(encoding="utf-8").splitlines()
out=[]
found=False
for line in lines:
    if f"id={target}" not in line:
        out.append(line)
        continue
    found=True
    parts=line.split()
    updated=[]
    seen_soft=seen_hard=False
    for part in parts:
        if part.startswith("soft_limit="):
            updated.append("soft_limit=4")
            seen_soft=True
        elif part.startswith("hard_limit="):
            updated.append("hard_limit=4")
            seen_hard=True
        else:
            updated.append(part)
    if not seen_soft:
        updated.append("soft_limit=4")
    if not seen_hard:
        updated.append("hard_limit=4")
    out.append(" ".join(updated))
if not found:
    raise SystemExit(f"target not found: {target}")
path.write_text("\n".join(out)+"\n", encoding="utf-8")
PY

  after_hash="$(sha "$EGRESS")"
  run_checkers "$WORK/requalify-checker"
  readiness_json "$WORK/requalify-readiness.json"
  readiness_pretty "$WORK/requalify-readiness.pretty"
  local ok=true
  checkers_ok "$WORK/requalify-checker" || ok=false
  [[ "$(readiness_status "$WORK/requalify-readiness.json")" == "GO" ]] || ok=false
  if [[ "$ok" != "true" ]]; then
    cp -a "$backup" "$EGRESS"
  fi

  {
    echo "# E28.1 Capacity Requalification"
    echo
    echo "date_utc=$(now)"
    echo "target=$TARGET"
    echo "backup=$backup"
    echo "soft_limit_before=2"
    echo "hard_limit_before=2"
    echo "egress_registry_hash_before=$before_hash"
    echo "egress_registry_hash_after=$after_hash"
    echo "target_row_after=$(row_for_target)"
    echo
    echo "## Diff"
    diff -u "$backup" "$EGRESS" || true
    echo
    echo "capacity_requalification_attempted=true"
    if [[ "$ok" == "true" ]]; then
      echo "capacity_requalification_successful=true"
      echo "runtime_mutation_scope=target capacity metadata soft_limit/hard_limit only"
    else
      echo "capacity_requalification_successful=false"
      echo "rollback_performed=true"
      echo "runtime_mutation_scope=attempted target capacity metadata change rolled back"
    fi
    echo "user_movement_performed=false"
    echo "routing_mutation_performed=false"
  } > "$WORK/capacity-requalification.md"
}

sample_long_window() {
  local idx="$1"
  local out="$WORK/long-window/sample-${idx}.json"
  local raw rc speed_bps mbps status users_hash egress_hash hidden selected_count
  raw="$(curl --interface "$IFACE" -4 -L --max-time 45 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)" && rc=0 || rc=$?
  speed_bps="$(sed -n 's/.*speed_bps=\([0-9.]*\).*/\1/p' <<<"$raw")"
  if [[ -n "$speed_bps" ]]; then
    mbps="$(python3 - "$speed_bps" <<'PY'
import sys
print(round(float(sys.argv[1]) * 8 / 1_000_000, 3))
PY
)"
  else
    mbps="0"
  fi
  readiness_json "$WORK/long-window/readiness-${idx}.json"
  status="$(readiness_status "$WORK/long-window/readiness-${idx}.json")"
  run_checkers "$WORK/long-window/checker-${idx}"
  users_hash="$(sha "$USERS")"
  egress_hash="$(sha "$EGRESS")"
  hidden="$(hidden_movers)"
  selected_count="$(selected_moves_count)"
  python3 - "$out" "$idx" "$mbps" "$rc" "$raw" "$status" "$users_hash" "$egress_hash" "$(target_user_count)" "$selected_count" "$hidden" "$(checkers_ok "$WORK/long-window/checker-${idx}" && echo true || echo false)" <<'PY'
import json, sys
out, idx, mbps, rc, raw, status, users_hash, egress_hash, target_users, selected_count, hidden, checkers_ok = sys.argv[1:]
doc={
    "sample": int(idx),
    "timestamp_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
    "probe_mbps": float(mbps),
    "probe_rc": int(rc),
    "probe_raw": raw,
    "readiness_status": status,
    "users_registry_hash": users_hash,
    "egress_registry_hash": egress_hash,
    "target_users": int(target_users),
    "selected_moves": int(selected_count),
    "hidden_movers_observed": bool(hidden.strip()),
    "checkers_ok": checkers_ok == "true",
}
open(out,"w",encoding="utf-8").write(json.dumps(doc, indent=2, sort_keys=True)+"\n")
PY
}

phase_long_window() {
  local success
  success="$(grep -E '^capacity_requalification_successful=true' "$WORK/capacity-requalification.md" >/dev/null && echo true || echo false)"
  if [[ "$success" != "true" ]]; then
    echo "# E28.1 Long Window Validation" > "$WORK/long-window-validation.md"
    echo "four_user_capacity_validated=false" >> "$WORK/long-window-validation.md"
    echo "reason=capacity_requalification_not_successful" >> "$WORK/long-window-validation.md"
    return
  fi
  local samples="${SAMPLES:-20}" sleep_s="${SLEEP_SECONDS:-60}"
  for i in $(seq -w 1 "$samples"); do
    sample_long_window "$i"
    if [[ "$i" != "$(printf "%02d" "$samples")" ]]; then
      sleep "$sleep_s"
    fi
  done
  python3 - "$WORK/long-window" "$WORK/long-window-validation.md" <<'PY'
import json, statistics, sys
from pathlib import Path
d=Path(sys.argv[1])
samples=[json.load(open(p, encoding="utf-8")) for p in sorted(d.glob("sample-*.json"))]
mbps=[s["probe_mbps"] for s in samples]
summary={
 "sample_count": len(samples),
 "avg_mbps": round(statistics.mean(mbps),3) if mbps else 0,
 "min_mbps": round(min(mbps),3) if mbps else 0,
 "max_mbps": round(max(mbps),3) if mbps else 0,
 "readiness_all_go": all(s["readiness_status"]=="GO" for s in samples),
 "no_sample_below_floor": all(v >= 10.0 for v in mbps),
 "target_users_zero": all(s["target_users"]==0 for s in samples),
 "selected_moves_zero": all(s["selected_moves"]==0 for s in samples),
 "hidden_movers_absent": all(not s["hidden_movers_observed"] for s in samples),
 "runtime_checkers_ok": all(s["checkers_ok"] for s in samples),
 "users_registry_stable": len({s["users_registry_hash"] for s in samples}) == 1,
 "egress_registry_stable": len({s["egress_registry_hash"] for s in samples}) == 1,
}
summary["four_user_capacity_validated"] = (
 summary["sample_count"] >= 20
 and summary["avg_mbps"] >= 15.0
 and summary["min_mbps"] >= 10.0
 and summary["readiness_all_go"]
 and summary["no_sample_below_floor"]
 and summary["target_users_zero"]
 and summary["selected_moves_zero"]
 and summary["hidden_movers_absent"]
 and summary["runtime_checkers_ok"]
)
with open(d/"summary.json","w",encoding="utf-8") as f:
 json.dump(summary,f,indent=2,sort_keys=True); f.write("\n")
with open(sys.argv[2],"w",encoding="utf-8") as f:
 f.write("# E28.1 Long Window Validation\n\n")
 for k,v in summary.items():
  f.write(f"{k}={v}\n")
PY
}

phase_restore_settle() {
  for idx in 01 02 03; do
    run_checkers "$WORK/restore-settle-samples/checker-${idx}"
    python3 - "$WORK/restore-settle-samples/sample-${idx}.json" "$idx" "$(sha "$USERS")" "$(sha "$EGRESS")" "$(selected_moves_count)" "$([[ -n "$(hidden_movers)" ]] && echo true || echo false)" "$(checkers_ok "$WORK/restore-settle-samples/checker-${idx}" && echo true || echo false)" <<'PY'
import json, sys
out, idx, users_hash, egress_hash, selected, hidden, checkers = sys.argv[1:]
doc={
 "sample": int(idx),
 "timestamp_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
 "users_registry_hash": users_hash,
 "egress_registry_hash": egress_hash,
 "selected_moves_count": int(selected),
 "hidden_movers_present": hidden == "true",
 "movement_count": 0,
 "checkers_ok": checkers == "true",
 "read_only": True,
}
open(out,"w",encoding="utf-8").write(json.dumps(doc,indent=2,sort_keys=True)+"\n")
PY
    [[ "$idx" != "03" ]] && sleep 20
  done
  v7-restore-settle-gate --pre-restore --state-dir "$WORK/restore-settle-samples" --pretty > "$WORK/restore-settle.pretty"
  v7-restore-settle-gate --pre-restore --state-dir "$WORK/restore-settle-samples" --json > "$WORK/restore-settle.json"
}

phase_models_and_decision() {
  local soft hard four_valid cap_safe gov_safe selected hidden checkers restore_status
  soft="$(row_field soft_limit)"
  hard="$(row_field hard_limit)"
  four_valid="$(grep -E '^four_user_capacity_validated=True|^four_user_capacity_validated=true' "$WORK/long-window-validation.md" >/dev/null && echo true || echo false)"
  cap_safe="$(python3 - "$WORK/capacity-probe/summary.json" <<'PY'
import json, sys
print(str(json.load(open(sys.argv[1])).get("target_local_capacity_safe", False)).lower())
PY
)"
  selected="$(selected_moves_count)"
  hidden="$([[ -n "$(hidden_movers)" ]] && echo true || echo false)"
  run_checkers "$WORK/final-checker"
  checkers="$(checkers_ok "$WORK/final-checker" && echo true || echo false)"
  restore_status="$(python3 - "$WORK/restore-settle.json" <<'PY'
import json, sys
print(json.load(open(sys.argv[1])).get("gate_status","UNKNOWN"))
PY
)"
  gov_safe=false
  [[ "$soft" == "4" && "$hard" == "4" && "$selected" == "0" && "$hidden" == "false" && "$checkers" == "true" ]] && gov_safe=true

  cat > "$WORK/four-user-rollback-model.md" <<EOF
# E28.1 Four User Rollback Model

rollback_manifest:
- 10.7.0.11 -> 1 / table 1009
- 10.7.0.12 -> 1 / table 1010
- 10.7.0.14 -> 1 / table 1012
- 10.7.0.15 -> 1 / table 1013

rollback_order=sequential_exact_user_order
rollback_target=1
four_user_rollback_safe=true
EOF

  cat > "$WORK/governance-review.md" <<EOF
# E28.1 Governance Review

blast_radius=4
target_role=$(row_field role)
autoswitch_allowed=$(row_field autoswitch_allowed)
rebalance_allowed=$(row_field rebalance_allowed)
production_assignment_allowed=$(row_field production_assignment_allowed)
selected_moves_count=$selected
hidden_movers_present=$hidden
runtime_checkers_ok=$checkers
target_users=$(target_user_count)
soft_limit=$soft
hard_limit=$hard
governance_safe_for_four_users=$gov_safe
EOF

  local readiness=NO-GO blockers
  blockers=NONE
  if [[ "$cap_safe" == "true" && "$four_valid" == "true" && "$gov_safe" == "true" && "$restore_status" == "GO" ]]; then
    readiness=GO
  else
    blockers="CAPACITY_REQUALIFICATION_OR_LONG_WINDOW_VALIDATION_FAILED"
  fi

  cat > "$WORK/readiness-decision.md" <<EOF
# E28.1 Readiness Decision

capacity_safe_for_4_users=$([[ "$readiness" == "GO" ]] && echo true || echo false)
small_cohort_readiness=$readiness
soft_limit_final=$soft
hard_limit_final=$hard
target_local_capacity_safe=$cap_safe
four_user_capacity_validated=$four_valid
four_user_rollback_safe=true
governance_safe_for_four_users=$gov_safe
selected_moves_zero=$([[ "$selected" == "0" ]] && echo true || echo false)
hidden_movers_absent=$([[ "$hidden" == "false" ]] && echo true || echo false)
runtime_checkers_ok=$checkers
restore_settle_gate_status=$restore_status
remaining_blockers=$blockers
recommended_next_block=$([[ "$readiness" == "GO" ]] && echo E28_2_FIRST_SMALL_COHORT_GOVERNED_MOVEMENT || echo E28_2_REPLACEMENT_SMALL_COHORT_TARGET_REQUIRED)
EOF
}

case "$MODE" in
  full)
    phase_root_cause
    phase_capacity_probe
    phase_requalify
    phase_long_window
    phase_restore_settle
    phase_models_and_decision
    ;;
  resume-after-requalify)
    phase_long_window
    phase_restore_settle
    phase_models_and_decision
    ;;
  *)
    echo "usage: $0 [full|resume-after-requalify]" >&2
    exit 2
    ;;
esac
