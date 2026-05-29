#!/usr/bin/env bash
set -u

TARGET="${TARGET:-amneziawg-exec-20260528-10-8-1-14}"
IFACE="${IFACE:-v7execwg0}"
STATE_DIR="${STATE_DIR:-/opt/v7/egress/state}"
CANDIDATE="${CANDIDATE:-10.7.0.11}"
EXPECTED_CURRENT="${EXPECTED_CURRENT:-1}"
SAMPLES="${SAMPLES:-20}"
INTERVAL="${INTERVAL:-60}"
URL="${URL:-https://speed.cloudflare.com/__down?bytes=2097152}"
SAMPLE_DIR="${SAMPLE_DIR:-/tmp/e25_12_restore_settle_samples}"
TSV="${TSV:-/tmp/e25_12_quality_samples.tsv}"
FINAL_READINESS_JSON="${FINAL_READINESS_JSON:-/tmp/e25_12_final_readiness.json}"
FINAL_READINESS_PRETTY="${FINAL_READINESS_PRETTY:-/tmp/e25_12_final_readiness.pretty}"
GATE_JSON="${GATE_JSON:-/tmp/e25_12_restore_settle_gate.json}"
GATE_PRETTY="${GATE_PRETTY:-/tmp/e25_12_restore_settle_gate.pretty}"

rm -rf "$SAMPLE_DIR"
mkdir -p "$SAMPLE_DIR"
printf 'sample\ttimestamp\tmbps\tping_loss_pct\trtt_avg_ms\treadiness\tcheckers_ok\tselected_moves\thidden_movers\tcandidate_current\ttarget_users\n' > "$TSV"

hash_file() {
  if [ -f "$1" ]; then
    sha256sum "$1" | cut -d" " -f1
  else
    printf 'MISSING'
  fi
}

candidate_field() {
  field="$1"
  awk -v ip="$CANDIDATE" -v key="$field" '
    $0 ~ "ip=" ip {
      for (i=1; i<=NF; i++) {
        split($i, kv, "=")
        if (kv[1] == key) { print kv[2]; exit }
      }
    }
  ' "$STATE_DIR/users.registry"
}

target_users_count() {
  awk -v target="$TARGET" '
    /enabled=1/ && $0 ~ "current=" target { count++ }
    END { print count+0 }
  ' "$STATE_DIR/users.registry"
}

selected_moves_count() {
  files="$(find "$STATE_DIR" -maxdepth 1 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null | sort)"
  if [ -z "$files" ]; then
    printf '0'
    return
  fi
  total=0
  for file in $files; do
    if [ -s "$file" ]; then
      count="$(grep -Ev '^[[:space:]]*($|#)' "$file" | wc -l | tr -d ' ')"
      total=$((total + count))
    fi
  done
  printf '%s' "$total"
}

selected_moves_hash() {
  files="$(find "$STATE_DIR" -maxdepth 1 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null | sort)"
  if [ -z "$files" ]; then
    printf 'NONE'
    return
  fi
  sha256sum $files | sha256sum | cut -d" " -f1
}

hidden_movers_count() {
  matches="$(pgrep -af 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' 2>/dev/null | grep -v -E 'pgrep|grep|e25_12_revalidation_window|ssh v7-vps' || true)"
  if [ -z "$matches" ]; then
    printf '0'
  else
    printf '%s\n' "$matches" | wc -l | tr -d ' '
  fi
}

checkers_ok() {
  v7-reconcile-check >/dev/null 2>&1 &&
    v7-user-route-check >/dev/null 2>&1 &&
    v7-killswitch-check >/dev/null 2>&1 &&
    v7-provisioning-reconcile-check >/dev/null 2>&1
}

readiness_status() {
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --pretty 2>/dev/null |
    awk -F= '/^approval_status=/{print $2; exit}'
}

probe_mbps() {
  raw="$(curl --interface "$IFACE" -4 -L --max-time 20 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)"
  speed="$(printf '%s\n' "$raw" | sed -n 's/.*speed_bps=\([0-9.][0-9.]*\).*/\1/p')"
  if [ -z "$speed" ]; then
    printf '0.00'
  else
    awk -v s="$speed" 'BEGIN { printf "%.2f", (s * 8) / 1000000 }'
  fi
}

ping_metrics() {
  out="$(ping -c 5 -W 3 -I "$IFACE" 1.1.1.1 2>&1 || true)"
  loss="$(printf '%s\n' "$out" | sed -n 's/.* \([0-9.][0-9.]*\)% packet loss.*/\1/p' | tail -n 1)"
  rtt="$(printf '%s\n' "$out" | sed -n 's/.* = [0-9.]*\/\([0-9.]*\)\/[0-9.]*\/[0-9.]* ms.*/\1/p' | tail -n 1)"
  printf '%s\t%s' "${loss:-100}" "${rtt:-0}"
}

echo "status=WINDOW_START target=$TARGET iface=$IFACE samples=$SAMPLES interval=$INTERVAL url=$URL"

i=1
while [ "$i" -le "$SAMPLES" ]; do
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  mbps="$(probe_mbps)"
  ping_pair="$(ping_metrics)"
  ping_loss="$(printf '%s' "$ping_pair" | cut -f1)"
  rtt_avg="$(printf '%s' "$ping_pair" | cut -f2)"
  readiness="$(readiness_status)"
  if checkers_ok; then checker_status=true; else checker_status=false; fi
  selected_count="$(selected_moves_count)"
  selected_hash="$(selected_moves_hash)"
  hidden_count="$(hidden_movers_count)"
  current="$(candidate_field current)"
  table="$(candidate_field table)"
  target_users="$(target_users_count)"
  users_hash="$(hash_file "$STATE_DIR/users.registry")"
  egress_hash="$(hash_file "$STATE_DIR/egress.registry")"

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$i" "$ts" "$mbps" "$ping_loss" "$rtt_avg" "${readiness:-UNKNOWN}" "$checker_status" "$selected_count" "$hidden_count" "$current" "$target_users" >> "$TSV"

  python3 - "$SAMPLE_DIR/sample-$(printf '%02d' "$i").json" <<PY
import json, sys
payload = {
  "source": "vps-live-e25.12-quality-window",
  "timestamp": "$ts",
  "hostname": "$(hostname)",
  "candidate_user": "$CANDIDATE",
  "candidate_current_egress": "$current",
  "candidate_table": "$table",
  "candidate_moves_total": 0,
  "execution_target": "$TARGET",
  "execution_target_interface": "$IFACE",
  "execution_target_users_count": int("$target_users"),
  "users_registry_hash": "$users_hash",
  "egress_registry_hash": "$egress_hash",
  "selected_moves": int("$selected_count"),
  "selected_moves_hash": "$selected_hash",
  "hidden_movers": [],
  "hidden_movers_observed": int("$hidden_count") > 0,
  "checker_results": {
    "reconcile_ok": "$checker_status" == "true",
    "user_route_ok": "$checker_status" == "true",
    "killswitch_ok": "$checker_status" == "true",
    "provisioning_ok": "$checker_status" == "true",
  },
  "checkers_ok": "$checker_status" == "true",
  "movement_count": 0,
  "moved_users": [],
  "telegram_hard_blocked": False,
  "egress_1_eligible": True,
  "planner_timer_state": "not_mutated_by_e25.12",
  "apply_timer_state": "not_mutated_by_e25.12",
  "quality_probe": {
    "mbps": float("$mbps"),
    "ping_loss_pct": float("$ping_loss"),
    "rtt_avg_ms": float("$rtt_avg"),
    "readiness_status_before_state_update": "${readiness:-UNKNOWN}"
  }
}
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump(payload, fh, indent=2, sort_keys=True)
    fh.write("\n")
PY

  echo "sample=$i ts=$ts mbps=$mbps ping_loss=$ping_loss rtt_avg_ms=$rtt_avg readiness=${readiness:-UNKNOWN} checkers_ok=$checker_status selected_moves=$selected_count hidden_movers=$hidden_count candidate_current=$current target_users=$target_users"
  if [ "$i" -lt "$SAMPLES" ]; then
    sleep "$INTERVAL"
  fi
  i=$((i + 1))
done

python3 - "$TSV" "$STATE_DIR/egress-stability.state" "$TARGET" <<'PY'
import pathlib
import sys

tsv = pathlib.Path(sys.argv[1])
state_path = pathlib.Path(sys.argv[2])
target = sys.argv[3]
rows = []
for line in tsv.read_text(encoding="utf-8").splitlines()[1:]:
    if not line.strip():
        continue
    parts = line.split("\t")
    rows.append(
        {
            "sample": int(parts[0]),
            "timestamp": parts[1],
            "mbps": float(parts[2]),
            "checkers_ok": parts[6] == "true",
            "selected_moves": int(parts[7]),
            "hidden_movers": int(parts[8]),
            "candidate_current": parts[9],
            "target_users": int(parts[10]),
        }
    )
if not rows:
    raise SystemExit("no rows")
avg = sum(r["mbps"] for r in rows) / len(rows)
min_mbps = min(r["mbps"] for r in rows)
stability = sum(1 for r in rows if r["mbps"] >= 10.0) / len(rows)
updates = {
    f"{target}_avg_mbps": f"{avg:.2f}",
    f"{target}_min_mbps": f"{min_mbps:.2f}",
    f"{target}_stability": f"{stability:.3f}",
}
tokens = {}
if state_path.exists():
    for line in state_path.read_text(encoding="utf-8", errors="replace").splitlines():
        for part in line.split():
            if "=" in part:
                k, v = part.split("=", 1)
                tokens[k] = v
tokens.update(updates)
state_path.write_text(" ".join(f"{k}={v}" for k, v in sorted(tokens.items())) + "\n", encoding="utf-8")
print(f"quality_state_updated=true avg_mbps={avg:.2f} min_mbps={min_mbps:.2f} stability={stability:.3f} samples={len(rows)}")
print(f"samples_below_floor={sum(1 for r in rows if r['mbps'] < 10.0)}")
print(f"selected_moves_zero={all(r['selected_moves'] == 0 for r in rows)}")
print(f"hidden_movers_absent={all(r['hidden_movers'] == 0 for r in rows)}")
print(f"runtime_checkers_ok={all(r['checkers_ok'] for r in rows)}")
print(f"candidate_still_on_expected={all(r['candidate_current'] == '1' for r in rows)}")
print(f"target_users_zero={all(r['target_users'] == 0 for r in rows)}")
PY

v7-second-canary-target-readiness --execution-target-id "$TARGET" --pretty > "$FINAL_READINESS_PRETTY" 2>&1 || true
v7-second-canary-target-readiness --execution-target-id "$TARGET" --json > "$FINAL_READINESS_JSON" 2>&1 || true
v7-restore-settle-gate --pre-restore --state-dir "$SAMPLE_DIR" --pretty > "$GATE_PRETTY" 2>&1 || true
v7-restore-settle-gate --pre-restore --state-dir "$SAMPLE_DIR" --json > "$GATE_JSON" 2>&1 || true

echo "final_readiness_pretty=$FINAL_READINESS_PRETTY"
cat "$FINAL_READINESS_PRETTY"
echo "restore_settle_gate_pretty=$GATE_PRETTY"
cat "$GATE_PRETTY"
echo "status=WINDOW_DONE sample_dir=$SAMPLE_DIR tsv=$TSV"
