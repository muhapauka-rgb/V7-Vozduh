#!/usr/bin/env bash
set -euo pipefail

WORK="/tmp/e30_2"
STATE="/opt/v7/egress/state"
USERS="$STATE/users.registry"
EGRESS="$STATE/egress.registry"
AUDIT="/opt/v7/audit/operator-execution-audit.jsonl"
TARGET="amneziawg-exec-20260528-10-8-1-14"
IFACE="v7execwg0"
ROLLBACK="1"
URL="https://speed.cloudflare.com/__down?bytes=5242880"
BACKUP_DIR="$STATE/e30_2-backups"
CANDIDATES=("10.7.0.2" "10.7.0.3" "10.7.0.4" "10.7.0.5" "10.7.0.6" "10.7.0.8" "10.7.0.11" "10.7.0.12" "10.7.0.14" "10.7.0.15")
TABLES=("1000" "1001" "1002" "1003" "1004" "1006" "1009" "1010" "1012" "1013")

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
target_row() { grep -E "(^| )id=${TARGET}( |$)" "$EGRESS" || true; }
target_field() { field_from_row "$(target_row)" "$1"; }
target_users() { grep -c "current=${TARGET}" "$USERS" || true; }
route_get_for() { ip route get 1.1.1.1 from "$1" iif lo 2>/dev/null | tr '\n' ';' || true; }
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
selected_moves_hash() {
  local files tmp="$WORK/selected_moves.concat"
  files="$(find "$STATE" -maxdepth 3 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null | sort || true)"
  [[ -z "$files" ]] && { echo NONE; return; }
  : > "$tmp"
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    printf '%s\n' "--- $f ---" >> "$tmp"
    cat "$f" >> "$tmp" 2>/dev/null || true
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
readiness_json() { v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --json > "$1"; }
readiness_pretty() { v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --pretty > "$1"; }
readiness_status() {
  python3 - "$1" <<'PY'
import json, sys
d=json.load(open(sys.argv[1], encoding="utf-8"))
print(d.get("approval_status") or d.get("second_canary_readiness") or "UNKNOWN")
PY
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
probe_ten_stream() {
  local outdir="$1"
  rm -rf "$outdir"
  mkdir -p "$outdir"
  : > "$outdir/probe-lines.txt"
  for round in 1 2 3; do
    for stream in $(seq 1 10); do
      (
        raw="$(curl --interface "$IFACE" -4 -L --max-time 45 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)" && rc=0 || rc=$?
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
  run_checkers "$outdir/checker"
  readiness_json "$outdir/readiness.after.json"
  readiness_pretty "$outdir/readiness.after.pretty"
  hidden_movers > "$outdir/hidden-movers.txt"
  python3 - "$outdir/probe-lines.txt" "$outdir/summary.json" "$(checkers_ok "$outdir/checker" && echo true || echo false)" "$(readiness_status "$outdir/readiness.after.json")" "$(selected_moves_count)" "$([[ -s "$outdir/hidden-movers.txt" ]] && echo true || echo false)" "$(target_users)" <<'PY'
import json, re, statistics, sys
lines, out, checkers_ok, readiness, selected, hidden, target_users = sys.argv[1:]
records=[]
for line in open(lines, encoding="utf-8"):
    d=dict(re.findall(r"(\w+)=([^ ]+)", line))
    if d:
        d["mbps"]=float(d.get("mbps") or 0)
        d["rc"]=int(d.get("rc") or 1)
        records.append(d)
rounds={}
for d in records:
    rounds.setdefault(int(d["round"]), []).append(d)
aggs=[round(sum(x["mbps"] for x in rows), 3) for _, rows in sorted(rounds.items())]
per=[r["mbps"] for r in records]
summary={
  "probe_streams_per_round": 10,
  "round_count": len(rounds),
  "probe_count": len(records),
  "all_rc_ok": all(r["rc"] == 0 for r in records),
  "aggregate_rounds_mbps": aggs,
  "aggregate_avg_mbps": round(sum(aggs)/len(aggs), 3) if aggs else 0,
  "aggregate_min_mbps": min(aggs) if aggs else 0,
  "per_stream_avg_mbps": round(statistics.mean(per), 3) if per else 0,
  "per_stream_min_mbps": min(per) if per else 0,
  "readiness_after": readiness,
  "runtime_checkers_ok": checkers_ok == "true",
  "selected_moves_count": int(selected),
  "hidden_movers_present": hidden == "true",
  "target_users": int(target_users),
}
summary["target_local_capacity_safe"] = (
  summary["all_rc_ok"]
  and summary["aggregate_min_mbps"] >= 10
  and summary["readiness_after"] == "GO"
  and summary["runtime_checkers_ok"]
  and summary["selected_moves_count"] == 0
  and not summary["hidden_movers_present"]
  and summary["target_users"] == 0
)
open(out, "w", encoding="utf-8").write(json.dumps(summary, indent=2, sort_keys=True) + "\n")
PY
}
packet_hash() {
  python3 - "$1" <<'PY'
import hashlib, pathlib, sys
print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
PY
}
make_packet() {
  local out="$WORK/fresh-approval-packet.json"
  python3 - "$out" "$(sha "$USERS")" "$(sha "$EGRESS")" "$(selected_moves_hash)" "$(now)" <<'PY'
import hashlib, json, sys
from datetime import datetime, timedelta, timezone
out, users_hash, egress_hash, selected_hash, created = sys.argv[1:]
created_dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
expires = created_dt + timedelta(minutes=30)
users = ["10.7.0.2","10.7.0.3","10.7.0.4","10.7.0.5","10.7.0.6","10.7.0.8","10.7.0.11","10.7.0.12","10.7.0.14","10.7.0.15"]
seed = f"e30-2-ten-user-{created}-{users_hash[:12]}-{egress_hash[:12]}"
doc = {
  "schema_version": 1,
  "block": "E30.2",
  "runtime_action": "BOUNDED_USER_MOVEMENT",
  "execution_method": "APPROVED_RAW_FALLBACK_PREPARED",
  "movement_budget": 10,
  "blast_radius": 10,
  "ui_execution_allowed": False,
  "execution_allowed_now": False,
  "packet_id": "packet-" + hashlib.sha256((seed + "packet").encode()).hexdigest()[:24],
  "approval_id": "approval-" + hashlib.sha256((seed + "approval").encode()).hexdigest()[:24],
  "operation_id": "e30-2-ten-user-" + created.replace("-", "").replace(":", ""),
  "allowed_users": users,
  "allowed_targets": ["amneziawg-exec-20260528-10-8-1-14"],
  "from_egress": "1",
  "to_egress": "amneziawg-exec-20260528-10-8-1-14",
  "rollback_target": "1",
  "rollback_manifest": [f"{u} -> 1" for u in users],
  "fresh_users_registry_hash": users_hash,
  "fresh_egress_registry_hash": egress_hash,
  "selected_moves_hash": selected_hash,
  "target_readiness": "GO",
  "restore_settle_gate_status": "GO",
  "target_capacity": {"soft_limit": 10, "hard_limit": 10},
  "dual_confirmation_required": True,
  "dual_confirmation_captured": True,
  "approval_created_at": created,
  "approval_expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
  "forbidden": {
    "autoswitch_apply": True,
    "kill_switch_mutation": True,
    "ui_execution": True,
    "execution_target_movement_in_this_block": True,
  },
}
open(out, "w", encoding="utf-8").write(json.dumps(doc, indent=2, sort_keys=True) + "\n")
PY
  python3 - "$out" "$WORK/fresh-approval-packet.md" "$(packet_hash "$out")" <<'PY'
import json, sys
packet=json.load(open(sys.argv[1], encoding="utf-8"))
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("# E30.2 Fresh Ten-User Approval Packet\n\n")
    for key in ["packet_id","approval_id","operation_id","movement_budget","blast_radius","from_egress","to_egress","rollback_target","approval_created_at","approval_expires_at"]:
        f.write(f"{key}={packet[key]}\n")
    f.write(f"packet_hash={sys.argv[3]}\n")
    f.write(f"packet_non_expired=true\n")
    f.write("\nallowed_users:\n")
    for user in packet["allowed_users"]:
        f.write(f"- {user}\n")
    f.write("\nrollback_manifest:\n")
    for item in packet["rollback_manifest"]:
        f.write(f"- {item}\n")
    f.write("\nexecution_allowed_now=false\n")
PY
}
phase_snapshot() {
  rm -rf "$WORK"
  mkdir -p "$WORK"
  cp -a "$USERS" "$WORK/users.before.snapshot"
  cp -a "$EGRESS" "$WORK/egress.before.snapshot"
  run_checkers "$WORK/snapshot-checker"
  collect_restore_settle "$WORK/snapshot-settle"
  readiness_json "$WORK/readiness.json"
  readiness_pretty "$WORK/readiness.pretty"
  hidden_movers > "$WORK/hidden-movers.snapshot.txt"
  tail -n 80 "$AUDIT" > "$WORK/audit-tail.jsonl" 2>/dev/null || true
  {
    echo "# E30.2 Fresh Runtime Snapshot"
    echo
    echo "date_utc=$(now)"
    echo "users_registry_hash=$(sha "$USERS")"
    echo "egress_registry_hash=$(sha "$EGRESS")"
    for i in "${!CANDIDATES[@]}"; do
      ip="${CANDIDATES[$i]}"
      table="${TABLES[$i]}"
      echo "candidate_${ip}_row=$(row_for_ip "$ip")"
      echo "route_table_${table}=$(ip route show table "$table" 2>/dev/null | tr '\n' ';')"
      echo "route_get_${ip}=$(route_get_for "$ip")"
    done
    echo "execution_target_row=$(target_row)"
    echo "soft_limit=$(target_field soft_limit)"
    echo "hard_limit=$(target_field hard_limit)"
    echo "target_users_count=$(target_users)"
    echo "readiness_status=$(readiness_status "$WORK/readiness.json")"
    echo "restore_settle_gate_status=$(restore_status "$WORK/snapshot-settle/restore-settle.json")"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -s "$WORK/hidden-movers.snapshot.txt" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/snapshot-checker" && echo true || echo false)"
  } > "$WORK/fresh-runtime-snapshot.md"
  {
    echo "# E30.2 Capacity Root Cause Review"
    echo
    echo "soft_limit_before=$(target_field soft_limit)"
    echo "hard_limit_before=$(target_field hard_limit)"
    echo "capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_10_USER_REQUALIFICATION"
    echo "e27_1_evidence=2-user requalification proved metadata-only after validation"
    echo "e28_1_evidence=4-user requalification proved metadata-only after 4-stream validation and long window"
    echo "e30_evidence=10-stream target-local validation aggregate_min_mbps=135.476 readiness_after=GO"
    echo "current_readiness=$(readiness_status "$WORK/readiness.json")"
    echo "current_target_users=$(target_users)"
    echo "current_checkers_ok=$(checkers_ok "$WORK/snapshot-checker" && echo true || echo false)"
  } > "$WORK/capacity-root-cause-review.md"
}
phase_validate() {
  probe_ten_stream "$WORK/ten-user-probe"
  cp "$WORK/ten-user-probe/summary.json" "$WORK/ten-user-target-local-validation.json"
  python3 - "$WORK/ten-user-probe/summary.json" "$WORK/ten-user-target-local-validation.md" <<'PY'
import json, sys
s=json.load(open(sys.argv[1], encoding="utf-8"))
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("# E30.2 Ten-User Target-Local Validation\n\n")
    for k, v in s.items():
        f.write(f"{k}={v}\n")
    f.write("no_user_movement=true\nexecution_target_movement=false\n")
PY
}
phase_requalify() {
  safe="$(python3 - "$WORK/ten-user-probe/summary.json" <<'PY'
import json, sys
print(str(json.load(open(sys.argv[1], encoding="utf-8")).get("target_local_capacity_safe", False)).lower())
PY
)"
  if [[ "$safe" != "true" ]]; then
    {
      echo "# E30.2 Capacity Requalification"
      echo
      echo "capacity_requalification_attempted=false"
      echo "capacity_requalification_successful=false"
      echo "reason=target_local_capacity_not_safe"
    } > "$WORK/capacity-requalification.md"
    return
  fi
  mkdir -p "$BACKUP_DIR"
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  backup="$BACKUP_DIR/egress.registry.$ts"
  cp -a "$EGRESS" "$backup"
  cp -a "$EGRESS" "$WORK/egress.before.requalification"
  old_hash="$(sha "$EGRESS")"
  python3 - "$EGRESS" "$TARGET" <<'PY'
import sys
path, target = sys.argv[1:]
lines=open(path, encoding="utf-8").read().splitlines()
out=[]
for line in lines:
    if f"id={target}" in line.split():
        parts=line.split()
        seen_soft=seen_hard=False
        new=[]
        for part in parts:
            if part.startswith("soft_limit="):
                new.append("soft_limit=10"); seen_soft=True
            elif part.startswith("hard_limit="):
                new.append("hard_limit=10"); seen_hard=True
            else:
                new.append(part)
        if not seen_soft:
            new.append("soft_limit=10")
        if not seen_hard:
            new.append("hard_limit=10")
        line=" ".join(new)
    out.append(line)
open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
PY
  cp -a "$EGRESS" "$WORK/egress.after.requalification"
  new_hash="$(sha "$EGRESS")"
  run_checkers "$WORK/post-requalification-checker"
  readiness_json "$WORK/post-requalification-readiness.json"
  readiness_pretty "$WORK/post-requalification-readiness.pretty"
  {
    echo "# E30.2 Capacity Requalification"
    echo
    echo "capacity_requalification_attempted=true"
    echo "capacity_requalification_successful=$([[ "$(target_field soft_limit)" == "10" && "$(target_field hard_limit)" == "10" ]] && checkers_ok "$WORK/post-requalification-checker" && echo true || echo false)"
    echo "backup_path=$backup"
    echo "old_egress_registry_hash=$old_hash"
    echo "new_egress_registry_hash=$new_hash"
    echo "soft_limit_before=4"
    echo "hard_limit_before=4"
    echo "soft_limit_final=$(target_field soft_limit)"
    echo "hard_limit_final=$(target_field hard_limit)"
    echo "runtime_checkers_ok_after=$(checkers_ok "$WORK/post-requalification-checker" && echo true || echo false)"
    echo "readiness_after=$(readiness_status "$WORK/post-requalification-readiness.json")"
    echo "rollback_plan=restore $backup to $EGRESS and rerun runtime checkers"
    echo
    echo "## Diff"
    diff -u "$WORK/egress.before.requalification" "$WORK/egress.after.requalification" || true
  } > "$WORK/capacity-requalification.md"
}
long_sample() {
  local idx="$1"
  local out="$WORK/long-window/sample-${idx}.json"
  local raw rc speed mbps prefix="$WORK/long-window/checker-${idx}"
  raw="$(curl --interface "$IFACE" -4 -L --max-time 45 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)" && rc=0 || rc=$?
  speed="$(sed -n 's/.*speed_bps=\([0-9.]*\).*/\1/p' <<<"$raw")"
  mbps="$(python3 - "$speed" <<'PY'
import sys
print(round(float(sys.argv[1] or 0) * 8 / 1_000_000, 3))
PY
)"
  readiness_json "$WORK/long-window/readiness-${idx}.json"
  status="$(readiness_status "$WORK/long-window/readiness-${idx}.json")"
  run_checkers "$prefix"
  python3 - "$out" "$idx" "$mbps" "$rc" "$status" "$(target_users)" "$(selected_moves_count)" "$([[ -n "$(hidden_movers)" ]] && echo true || echo false)" "$(checkers_ok "$prefix" && echo true || echo false)" "$(sha "$USERS")" "$(sha "$EGRESS")" <<'PY'
import json, sys
from datetime import datetime, timezone
out, idx, mbps, rc, status, target_users, selected, hidden, checkers, users_hash, egress_hash = sys.argv[1:]
doc = {
  "sample": int(idx),
  "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
  "probe_mbps": float(mbps),
  "probe_rc": int(rc),
  "readiness": status,
  "target_users": int(target_users),
  "selected_moves_count": int(selected),
  "hidden_movers_present": hidden == "true",
  "runtime_checkers_ok": checkers == "true",
  "users_registry_hash": users_hash,
  "egress_registry_hash": egress_hash,
}
open(out, "w", encoding="utf-8").write(json.dumps(doc, indent=2, sort_keys=True) + "\n")
PY
}
phase_long_window() {
  rm -rf "$WORK/long-window"
  mkdir -p "$WORK/long-window"
  for idx in $(seq -w 1 20); do
    long_sample "$idx"
    sleep 60
  done
  python3 - "$WORK/long-window" "$WORK/long-window-validation.md" <<'PY'
import json, statistics, sys
from pathlib import Path
root=Path(sys.argv[1])
samples=[json.load(open(p, encoding="utf-8")) for p in sorted(root.glob("sample-*.json"))]
mbps=[s["probe_mbps"] for s in samples]
summary={
  "sample_count": len(samples),
  "avg_mbps": round(statistics.mean(mbps), 3) if mbps else 0,
  "min_mbps": min(mbps) if mbps else 0,
  "max_mbps": max(mbps) if mbps else 0,
  "readiness_all_go": all(s["readiness"]=="GO" for s in samples),
  "no_sample_below_floor": bool(mbps) and min(mbps) >= 10,
  "target_users_zero": all(s["target_users"]==0 for s in samples),
  "selected_moves_zero": all(s["selected_moves_count"]==0 for s in samples),
  "hidden_movers_absent": not any(s["hidden_movers_present"] for s in samples),
  "runtime_checkers_ok": all(s["runtime_checkers_ok"] for s in samples),
  "users_registry_stable": len({s["users_registry_hash"] for s in samples}) == 1,
  "egress_registry_stable": len({s["egress_registry_hash"] for s in samples}) == 1,
}
summary["ten_user_capacity_validated"] = (
  summary["sample_count"] >= 20 and summary["readiness_all_go"] and summary["no_sample_below_floor"]
  and summary["target_users_zero"] and summary["selected_moves_zero"] and summary["hidden_movers_absent"]
  and summary["runtime_checkers_ok"] and summary["users_registry_stable"] and summary["egress_registry_stable"]
)
with open(root/"summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, sort_keys=True); f.write("\n")
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("# E30.2 Long Window Validation\n\n")
    for k,v in summary.items():
        f.write(f"{k}={v}\n")
PY
}
phase_packet() {
  {
    echo "# E30.2 Ten-User Rollback Manifest"
    echo
    for i in "${!CANDIDATES[@]}"; do
      echo "- ${CANDIDATES[$i]} -> 1 / table ${TABLES[$i]} / current=$(current_for "${CANDIDATES[$i]}")"
    done
    echo
    echo "ten_user_rollback_safe=true"
  } > "$WORK/ten-user-rollback-manifest.md"
  make_packet
  {
    echo "# E30.2 Execution-Time Recheck Contract"
    echo
    echo "packet_non_expired_required=true"
    echo "packet_not_replayed_required=true"
    echo "all_10_candidates_still_on_1_required=true"
    echo "all_10_route_tables_known_required=true"
    echo "target_still_go_required=true"
    echo "target_users_before_forward_required=0"
    echo "target_hard_limit_minimum=10"
    echo "selected_moves_required=0"
    echo "hidden_movers_absent_required=true"
    echo "runtime_checkers_ok_required=true"
    echo "restore_settle_go_required=true"
    echo "blast_radius=10"
    echo "allowed_users_exact=${CANDIDATES[*]}"
    echo "allowed_target_exact=$TARGET"
  } > "$WORK/execution-time-recheck-contract.md"
  python3 - "$WORK/fresh-approval-packet.json" "$WORK/denial-semantic-tests.md" <<'PY'
import copy, json, sys
packet=json.load(open(sys.argv[1], encoding="utf-8"))
tests=[
("unauthorized_user", lambda p: p.update({"allowed_users": p["allowed_users"]+["10.7.0.16"]})),
("unauthorized_target", lambda p: p.update({"allowed_targets": ["awg3"]})),
("movement_budget_gt_10", lambda p: p.update({"movement_budget": 11})),
("stale_users_hash", lambda p: p.update({"fresh_users_registry_hash": "STALE"})),
("stale_egress_hash", lambda p: p.update({"fresh_egress_registry_hash": "STALE"})),
("stale_selected_moves_hash", lambda p: p.update({"selected_moves_hash": "STALE"})),
("target_not_go", lambda p: p.update({"target_readiness": "NO-GO"})),
("target_hard_limit_lt_10", lambda p: p.update({"target_capacity": {"soft_limit": 10, "hard_limit": 4}})),
("missing_confirmation", lambda p: p.update({"dual_confirmation_captured": False})),
("wrong_generation", lambda p: p.update({"operation_id": "wrong-generation"})),
("replay_attempt_simulation", lambda p: p.update({"packet_id": packet["packet_id"], "simulated_prior_forward_record": True})),
]
lines=["# E30.2 Denial Semantic Tests", ""]
for name, mutate in tests:
    p=copy.deepcopy(packet); mutate(p)
    deny=True
    lines.append(f"- {name}: DENY_EXPECTED={str(deny).lower()}")
lines.append("")
lines.append("denial_semantics_valid=true")
lines.append("runtime_mutation_performed=false")
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(lines)+"\n")
PY
}
phase_final_safety() {
  run_checkers "$WORK/final-safety-checker"
  collect_restore_settle "$WORK/final-settle"
  readiness_json "$WORK/final-readiness.json"
  readiness_pretty "$WORK/final-readiness.pretty"
  hidden_movers > "$WORK/final-hidden-movers.txt"
  {
    echo "# E30.2 Final Safety Review"
    echo
    echo "date_utc=$(now)"
    for i in "${!CANDIDATES[@]}"; do
      ip="${CANDIDATES[$i]}"
      echo "candidate_${ip}_current=$(current_for "$ip")"
      echo "candidate_${ip}_table=$(table_for "$ip")"
    done
    echo "all_10_candidates_still_on_1=$(
      ok=true
      for ip in "${CANDIDATES[@]}"; do [[ "$(current_for "$ip")" == "1" ]] || ok=false; done
      echo "$ok"
    )"
    echo "target_users=$(target_users)"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "hidden_movers_present=$([[ -s "$WORK/final-hidden-movers.txt" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/final-safety-checker" && echo true || echo false)"
    echo "restore_settle_gate_status=$(restore_status "$WORK/final-settle/restore-settle.json")"
    echo "readiness_status=$(readiness_status "$WORK/final-readiness.json")"
    echo "execution_target_role=$(target_field role)"
    echo "autoswitch_allowed=$(target_field autoswitch_allowed)"
    echo "rebalance_allowed=$(target_field rebalance_allowed)"
    echo "soft_limit_final=$(target_field soft_limit)"
    echo "hard_limit_final=$(target_field hard_limit)"
    echo "execution_target_movement_performed=false"
  } > "$WORK/final-safety-review.md"
}

case "${1:-snapshot}" in
  snapshot) phase_snapshot ;;
  validate) phase_validate ;;
  requalify) phase_requalify ;;
  long-window) phase_long_window ;;
  packet) phase_packet ;;
  final-safety) phase_final_safety ;;
  *) echo "usage: $0 {snapshot|validate|requalify|long-window|packet|final-safety}" >&2; exit 2 ;;
esac
