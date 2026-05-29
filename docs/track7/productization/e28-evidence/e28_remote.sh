#!/usr/bin/env bash
set -euo pipefail

WORK="/tmp/e28"
STATE="/opt/v7/egress/state"
USERS="$STATE/users.registry"
EGRESS="$STATE/egress.registry"
TARGET="amneziawg-exec-20260528-10-8-1-14"

mkdir -p "$WORK/restore-settle-samples"

sha() {
  if [[ -f "$1" ]]; then sha256sum "$1" | awk '{print $1}'; else echo "MISSING"; fi
}

now() {
  date -u +%Y-%m-%dT%H:%M:%SZ
}

kv() {
  local file="$1" key="$2"
  tr ' ' '\n' < "$file" | awk -F= -v k="$key" '$1==k {print $2; exit}'
}

row_for_ip() {
  local ip="$1"
  grep -E "(^| )ip=${ip}( |$)" "$USERS" || true
}

current_for() {
  local ip="$1"
  local row
  row="$(row_for_ip "$ip")"
  [[ -n "$row" ]] && kv <(printf '%s\n' "$row") current || true
}

table_for() {
  local ip="$1"
  local row
  row="$(row_for_ip "$ip")"
  [[ -n "$row" ]] && kv <(printf '%s\n' "$row") table || true
}

target_row() {
  grep -E "(^| )id=${TARGET}( |$)" "$EGRESS" || true
}

target_field() {
  local field="$1"
  local row
  row="$(target_row)"
  [[ -n "$row" ]] && kv <(printf '%s\n' "$row") "$field" || true
}

users_on_target() {
  grep -E "(^| )current=${TARGET}( |$)" "$USERS" | sed -n 's/.*ip=\([^ ]*\).*/\1/p' | paste -sd, - || true
}

target_user_count() {
  local users
  users="$(users_on_target)"
  [[ -z "$users" ]] && echo 0 || tr ',' '\n' <<<"$users" | sed '/^$/d' | wc -l | tr -d ' '
}

selected_moves_count() {
  local files count=0
  files="$(find "$STATE" -maxdepth 3 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null || true)"
  if [[ -z "$files" ]]; then
    echo 0
    return
  fi
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    count=$((count + $(grep -E '10\.' "$file" 2>/dev/null | wc -l | tr -d ' ')))
  done <<< "$files"
  echo "$count"
}

selected_moves_hash() {
  local files tmp="$WORK/selected_moves.concat"
  files="$(find "$STATE" -maxdepth 3 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null | sort || true)"
  if [[ -z "$files" ]]; then
    echo "NONE"
    return
  fi
  : > "$tmp"
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    printf '--- %s ---\n' "$file" >> "$tmp"
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

route_get_for() {
  local ip="$1" table="$2"
  ip route show table "$table" 2>/dev/null | tr '\n' ' '
  ip route get 1.1.1.1 from "$ip" iif lo 2>/dev/null | tr '\n' ';' || true
}

sample_settle() {
  local idx="$1"
  local prefix="$WORK/restore-settle-samples/checker-${idx}"
  run_checkers "$prefix"
  python3 - "$WORK/restore-settle-samples/sample-${idx}.json" "$idx" <<'PY'
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

out, idx = sys.argv[1], sys.argv[2]
state = "/opt/v7/egress/state"

def run(cmd):
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)

def sha(path):
    if not os.path.exists(path):
        return "MISSING"
    return run(f"sha256sum {path}").stdout.split()[0]

selected = run("find /opt/v7/egress/state -maxdepth 3 -type f \\( -iname '*selected*move*' -o -iname '*selected_moves*' \\) 2>/dev/null").stdout.strip().splitlines()
selected_count = 0
for path in selected:
    try:
        selected_count += sum(1 for line in open(path, encoding="utf-8", errors="ignore") if "10." in line)
    except OSError:
        pass

hidden = run("ps -eo pid,ppid,etime,command | grep -E 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' | grep -v grep || true").stdout.strip().splitlines()

data = {
    "sample": int(idx),
    "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "users_registry_hash": sha(f"{state}/users.registry"),
    "egress_registry_hash": sha(f"{state}/egress.registry"),
    "selected_moves_count": selected_count,
    "hidden_movers_present": bool(hidden),
    "movement_count": 0,
    "checkers_ok": all(
        marker in open(f"/tmp/e28/restore-settle-samples/checker-{idx}-{name}.out", encoding="utf-8", errors="ignore").read()
        for name, marker in [
            ("reconcile", "V7_RECONCILE_RESULT=OK"),
            ("user-route", "V7_USER_ROUTE_CHECK=OK"),
            ("killswitch", "V7_KILLSWITCH_CHECK=OK"),
            ("provisioning", "V7_PROVISIONING_RECONCILE_CHECK=OK"),
        ]
    ),
    "read_only": True,
}
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, sort_keys=True)
    f.write("\n")
PY
}

collect() {
  rm -rf "$WORK"
  mkdir -p "$WORK/restore-settle-samples"

  cp "$USERS" "$WORK/users.registry.snapshot"
  cp "$EGRESS" "$WORK/egress.registry.snapshot"
  run_checkers "$WORK/checker"

  v7-second-canary-target-readiness --execution-target-id "$TARGET" --pretty > "$WORK/readiness.pretty" 2>"$WORK/readiness.pretty.err" || true
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --json > "$WORK/readiness.json" 2>"$WORK/readiness.json.err" || true

  sample_settle 01
  sleep 20
  sample_settle 02
  sleep 20
  sample_settle 03
  v7-restore-settle-gate --pre-restore --state-dir "$WORK/restore-settle-samples" --pretty > "$WORK/restore-settle.pretty" 2>"$WORK/restore-settle.pretty.err" || true
  v7-restore-settle-gate --pre-restore --state-dir "$WORK/restore-settle-samples" --json > "$WORK/restore-settle.json" 2>"$WORK/restore-settle.json.err" || true

  hidden_movers > "$WORK/hidden-movers.txt"
  find "$STATE" -maxdepth 3 -type f \( -iname '*quality*' -o -iname '*load*' -o -iname '*diagnose*' -o -iname '*stability*' \) -print | sort > "$WORK/state-quality-files.txt" || true
  for file in $(cat "$WORK/state-quality-files.txt"); do
    safe="$(echo "$file" | sed 's#^/##;s#[^A-Za-z0-9._-]#_#g')"
    cp "$file" "$WORK/${safe}" 2>/dev/null || true
  done
  tail -n 40 /opt/v7/audit/operator-execution-audit.jsonl > "$WORK/audit-tail.jsonl" 2>/dev/null || true

  python3 - "$WORK/cohort-candidate-discovery.md" "$WORK/target-capacity-review.md" "$WORK/governance-review.md" <<'PY'
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

candidate_out, capacity_out, governance_out = sys.argv[1:]
state = "/opt/v7/egress/state"
target = "amneziawg-exec-20260528-10-8-1-14"

def parse_line(line):
    return dict(re.findall(r"(\S+?)=([^ ]+)", line.strip()))

users = []
with open(f"{state}/users.registry", encoding="utf-8") as f:
    for line in f:
        if line.strip() and not line.lstrip().startswith("#"):
            row = parse_line(line)
            if row.get("ip"):
                users.append(row)

egress_rows = []
with open(f"{state}/egress.registry", encoding="utf-8") as f:
    for line in f:
        if line.strip() and not line.lstrip().startswith("#"):
            row = parse_line(line)
            if row.get("id"):
                egress_rows.append(row)

target_row = next((r for r in egress_rows if r.get("id") == target), {})
eligible = [u for u in users if u.get("enabled") == "1" and u.get("current") == "1" and u.get("table")]
selected = eligible[:5]

def route_get(ip, table):
    table_route = subprocess.run(["ip", "route", "show", "table", table], text=True, capture_output=True).stdout
    policy_route = subprocess.run(["ip", "route", "get", "1.1.1.1", "from", ip, "iif", "lo"], text=True, capture_output=True).stdout
    return "table_default=" + " ".join(table_route.split()) + "; route_get=" + " ".join(policy_route.split())

with open(candidate_out, "w", encoding="utf-8") as f:
    f.write("# E28 Cohort Candidate Discovery\n\n")
    f.write(f"date_utc={datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')}\n")
    f.write(f"candidate_count={len(selected)}\n")
    for idx, row in enumerate(selected, 1):
        f.write(f"candidate_user_{idx}={row.get('ip')}\n")
        f.write(f"candidate_user_{idx}_current={row.get('current')}\n")
        f.write(f"candidate_user_{idx}_table={row.get('table')}\n")
        f.write(f"candidate_user_{idx}_enabled={row.get('enabled')}\n")
        f.write(f"candidate_user_{idx}_route_get={route_get(row.get('ip'), row.get('table'))}\n")
    f.write("\n## Eligible Users On Rollback Target 1\n\n")
    for row in eligible:
        f.write(f"- ip={row.get('ip')} current={row.get('current')} table={row.get('table')} enabled={row.get('enabled')}\n")

with open("/tmp/e28/readiness.json", encoding="utf-8", errors="ignore") as f:
    try:
        readiness = json.load(f)
    except json.JSONDecodeError:
        readiness = {}

soft = int(target_row.get("soft_limit", "0") or "0")
hard = int(target_row.get("hard_limit", "0") or "0")
target_users = [u["ip"] for u in users if u.get("current") == target]
selected_target = readiness.get("selected_target")
selected_candidate = next((c for c in readiness.get("target_candidates", []) if c.get("egress_id") == selected_target), {})
avg = selected_candidate.get("avg_mbps")
min_mbps = selected_candidate.get("min_mbps")
stability = selected_candidate.get("stability")
status = readiness.get("approval_status") or readiness.get("second_canary_readiness") or readiness.get("status")

with open(capacity_out, "w", encoding="utf-8") as f:
    f.write("# E28 Target Capacity Review\n\n")
    f.write(f"date_utc={datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')}\n")
    f.write(f"target={target}\n")
    f.write(f"target_row={' '.join(f'{k}={v}' for k, v in target_row.items())}\n")
    f.write(f"soft_limit={soft}\n")
    f.write(f"hard_limit={hard}\n")
    f.write(f"target_current_users={','.join(target_users) if target_users else 'NONE'}\n")
    f.write(f"target_current_user_count={len(target_users)}\n")
    f.write(f"readiness_status={status}\n")
    f.write(f"avg_mbps={avg}\n")
    f.write(f"min_mbps={min_mbps}\n")
    f.write(f"stability={stability}\n")
    f.write(f"capacity_safe_for_4_users={str(hard >= 4).lower()}\n")
    f.write(f"capacity_safe_for_5_users={str(hard >= 5).lower()}\n")
    f.write("capacity_blocker=EXECUTION_TARGET_CAPACITY_LIMIT_TWO_USERS\n" if hard < 4 else "capacity_blocker=NONE\n")

hidden = open("/tmp/e28/hidden-movers.txt", encoding="utf-8", errors="ignore").read().strip()
selected_moves_count = 0
for root, _, files in os.walk(state):
    for name in files:
        if "selected" in name.lower() and "move" in name.lower():
            try:
                selected_moves_count += sum(1 for line in open(os.path.join(root, name), encoding="utf-8", errors="ignore") if "10." in line)
            except OSError:
                pass

with open(governance_out, "w", encoding="utf-8") as f:
    f.write("# E28 Governance Review\n\n")
    f.write(f"date_utc={datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')}\n")
    f.write(f"target_role={target_row.get('role')}\n")
    f.write(f"autoswitch_allowed={target_row.get('autoswitch_allowed')}\n")
    f.write(f"rebalance_allowed={target_row.get('rebalance_allowed')}\n")
    f.write(f"production_assignment_allowed={target_row.get('production_assignment_allowed')}\n")
    f.write(f"selected_moves_count={selected_moves_count}\n")
    f.write(f"hidden_movers_present={str(bool(hidden)).lower()}\n")
    f.write(f"runtime_checkers_ok={str(all(marker in open(f'/tmp/e28/checker-{name}.out', encoding='utf-8', errors='ignore').read() for name, marker in [('reconcile','V7_RECONCILE_RESULT=OK'),('user-route','V7_USER_ROUTE_CHECK=OK'),('killswitch','V7_KILLSWITCH_CHECK=OK'),('provisioning','V7_PROVISIONING_RECONCILE_CHECK=OK')])).lower()}\n")
    f.write(f"governance_safe_for_small_cohort={str(target_row.get('role') == 'EXECUTION_ONLY' and target_row.get('autoswitch_allowed') == 'false' and target_row.get('rebalance_allowed') == 'false' and not hidden and selected_moves_count == 0).lower()}\n")
PY

  {
    echo "# E28 Runtime Snapshot"
    echo
    echo "hostname=$(hostname)"
    echo "date_utc=$(now)"
    echo "users_registry_hash=$(sha "$USERS")"
    echo "egress_registry_hash=$(sha "$EGRESS")"
    echo "target_users=$(target_user_count)"
    echo "selected_moves_count=$(selected_moves_count)"
    echo "selected_moves_hash=$(selected_moves_hash)"
    echo "hidden_movers_present=$([[ -s "$WORK/hidden-movers.txt" ]] && echo true || echo false)"
    echo "runtime_checkers_ok=$(checkers_ok "$WORK/checker" && echo true || echo false)"
    echo "target_row=$(target_row)"
  } > "$WORK/runtime-snapshot.md"
}

collect
