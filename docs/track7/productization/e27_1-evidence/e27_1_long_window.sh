#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-/tmp/e27_1_long_window}"
STATE="/opt/v7/egress/state"
TARGET="amneziawg-exec-20260528-10-8-1-14"
IFACE="v7execwg0"
URL="https://speed.cloudflare.com/__down?bytes=5242880"
SAMPLES="${SAMPLES:-20}"
SLEEP_SECONDS="${SLEEP_SECONDS:-60}"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
: > "${OUT_DIR}/quality-samples.tsv"

sample() {
  local idx="$1"
  local stamp out raw rc speed_bps mbps users_hash egress_hash target_row target_users selected_count selected_hash hidden ready_status ready_json
  stamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  out="${OUT_DIR}/sample-${idx}.json"
  users_hash="$(sha256sum "$STATE/users.registry" | awk '{print $1}')"
  egress_hash="$(sha256sum "$STATE/egress.registry" | awk '{print $1}')"
  target_row="$(grep "id=${TARGET}" "$STATE/egress.registry" || true)"
  target_users="$(grep -c "current=${TARGET}" "$STATE/users.registry" || true)"

  if [ -d "$STATE/selected_moves" ]; then
    selected_count="$(find "$STATE/selected_moves" -type f | wc -l | tr -d ' ')"
    if [ "$selected_count" = "0" ]; then
      selected_hash="NONE"
    else
      selected_hash="$(find "$STATE/selected_moves" -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')"
    fi
  else
    selected_count="0"
    selected_hash="NONE"
  fi

  hidden="$(ps -eo pid,ppid,etime,command | grep -E 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' | grep -v grep || true)"

  raw="$(curl --interface "$IFACE" -4 -L --max-time 30 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)" && rc=0 || rc=$?
  speed_bps="$(printf "%s\n" "$raw" | sed -n 's/.*speed_bps=\([0-9.]*\).*/\1/p')"
  if [ -n "$speed_bps" ]; then
    mbps="$(python3 - "$speed_bps" <<'PY'
import sys
print(round(float(sys.argv[1]) * 8 / 1_000_000, 3))
PY
)"
  else
    mbps="0"
  fi

  v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --json > "${OUT_DIR}/readiness-${idx}.json"
  ready_status="$(python3 - "${OUT_DIR}/readiness-${idx}.json" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    d=json.load(f)
print(d.get("approval_status") or d.get("second_canary_readiness") or "UNKNOWN")
PY
)"

  local reconcile_ok user_route_ok killswitch_ok provisioning_ok
  v7-reconcile-check >/tmp/e27_1_lw_reconcile.out 2>/tmp/e27_1_lw_reconcile.err && reconcile_ok=true || reconcile_ok=false
  v7-user-route-check >/tmp/e27_1_lw_user_route.out 2>/tmp/e27_1_lw_user_route.err && user_route_ok=true || user_route_ok=false
  v7-killswitch-check >/tmp/e27_1_lw_killswitch.out 2>/tmp/e27_1_lw_killswitch.err && killswitch_ok=true || killswitch_ok=false
  v7-provisioning-reconcile-check >/tmp/e27_1_lw_provisioning.out 2>/tmp/e27_1_lw_provisioning.err && provisioning_ok=true || provisioning_ok=false

  printf "%s\t%s\t%s\t%s\t%s\n" "$idx" "$stamp" "$rc" "$mbps" "$raw" >> "${OUT_DIR}/quality-samples.tsv"

  python3 - "$out" "$idx" "$stamp" "$users_hash" "$egress_hash" "$target_row" "$target_users" "$selected_count" "$selected_hash" "$hidden" "$rc" "$mbps" "$raw" "$ready_status" "$reconcile_ok" "$user_route_ok" "$killswitch_ok" "$provisioning_ok" <<'PY'
import json
import sys

(
    out,
    idx,
    stamp,
    users_hash,
    egress_hash,
    target_row,
    target_users,
    selected_count,
    selected_hash,
    hidden,
    probe_rc,
    mbps,
    raw,
    ready_status,
    reconcile_ok,
    user_route_ok,
    killswitch_ok,
    provisioning_ok,
) = sys.argv[1:]

hidden_lines = [line for line in hidden.splitlines() if line.strip()]
checkers = {
    "reconcile_ok": reconcile_ok == "true",
    "user_route_ok": user_route_ok == "true",
    "killswitch_ok": killswitch_ok == "true",
    "provisioning_ok": provisioning_ok == "true",
}
doc = {
    "sample": int(idx),
    "timestamp": stamp,
    "source": "vps-live-e27.1-long-window",
    "execution_target": "amneziawg-exec-20260528-10-8-1-14",
    "interface": "v7execwg0",
    "target_row": target_row,
    "target_users": int(target_users),
    "users_registry_hash": users_hash,
    "egress_registry_hash": egress_hash,
    "selected_moves": int(selected_count),
    "selected_moves_hash": selected_hash,
    "hidden_movers": hidden_lines,
    "hidden_movers_observed": bool(hidden_lines),
    "probe_rc": int(probe_rc),
    "probe_mbps": float(mbps),
    "probe_raw": raw,
    "readiness_status": ready_status,
    "checker_results": checkers,
    "checkers_ok": all(checkers.values()),
}
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, sort_keys=True)
    f.write("\n")
PY
}

for i in $(seq -w 1 "$SAMPLES"); do
  sample "$i"
  if [ "$i" != "$(printf "%02d" "$SAMPLES")" ]; then
    sleep "$SLEEP_SECONDS"
  fi
done

python3 - "$OUT_DIR" <<'PY' > "${OUT_DIR}/summary.json"
import json
import statistics
import sys
from pathlib import Path

out_dir = Path(sys.argv[1])
samples = []
for path in sorted(out_dir.glob("sample-*.json")):
    with path.open(encoding="utf-8") as f:
        samples.append(json.load(f))
mbps = [s["probe_mbps"] for s in samples]
summary = {
    "sample_count": len(samples),
    "avg_mbps": round(statistics.mean(mbps), 3) if mbps else 0,
    "min_mbps": round(min(mbps), 3) if mbps else 0,
    "max_mbps": round(max(mbps), 3) if mbps else 0,
    "no_sample_below_floor": all(v >= 10.0 for v in mbps),
    "readiness_all_go": all(s.get("readiness_status") == "GO" for s in samples),
    "selected_moves_zero": all(s.get("selected_moves") == 0 for s in samples),
    "hidden_movers_absent": all(not s.get("hidden_movers_observed") for s in samples),
    "runtime_checkers_ok": all(s.get("checkers_ok") for s in samples),
    "target_users_zero": all(s.get("target_users") == 0 for s in samples),
    "users_registry_stable": len({s.get("users_registry_hash") for s in samples}) == 1,
    "egress_registry_stable": len({s.get("egress_registry_hash") for s in samples}) == 1,
}
summary["two_user_capacity_validated"] = (
    summary["sample_count"] >= 20
    and summary["avg_mbps"] >= 15.0
    and summary["min_mbps"] >= 10.0
    and summary["no_sample_below_floor"]
    and summary["readiness_all_go"]
    and summary["selected_moves_zero"]
    and summary["hidden_movers_absent"]
    and summary["runtime_checkers_ok"]
    and summary["target_users_zero"]
)
print(json.dumps(summary, indent=2, sort_keys=True))
PY

python3 - "$OUT_DIR/summary.json" <<'PY' > "${OUT_DIR}/long-window-validation.md"
import json
import sys
with open(sys.argv[1], encoding="utf-8") as f:
    s=json.load(f)
print("# E27.1 Long Window Validation")
print()
for key, value in s.items():
    print(f"{key}={value}")
PY
