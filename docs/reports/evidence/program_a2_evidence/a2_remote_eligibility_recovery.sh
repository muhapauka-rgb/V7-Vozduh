#!/usr/bin/env bash
set +e
set -u

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

section() {
  printf '\n=== %s ===\n' "$1"
}

run_cmd() {
  printf '\n$ %s\n' "$*"
  "$@"
  rc=$?
  printf 'rc=%s\n' "$rc"
}

state_summary() {
  python3 - <<'PY'
import json
from pathlib import Path

state_dir = Path("/opt/v7/egress/state")

def load(path, default):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return default

def kv(line):
    out = {}
    for part in line.split():
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
    return out

def registry(name):
    rows = []
    p = state_dir / name
    try:
        lines = p.read_text(errors="replace").splitlines()
    except Exception:
        return rows
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            rows.append(kv(line))
    return rows

def load_state_file():
    out = {}
    p = state_dir / "egress-load.state"
    try:
        for line in p.read_text(errors="replace").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                out[k] = v
    except Exception:
        pass
    return out

policy = load("/etc/v7/policy.json", {})
org_policy = load("/etc/v7/org-egress-policy.json", {})
state = load(state_dir / "v7-state.json", {})
matrix = load(state_dir / "service-matrix.json", {"items": {}})
telegram = load(state_dir / "telegram-sentinel.json", {"items": {}})
quality = load(state_dir / "egress-quality-summary.json", {"items": {}})
barrier = load(state_dir / "autoswitch-restore-barrier.json", {})
load_state = load_state_file()
egresses = registry("egress.registry")
users = registry("users.registry")
user_counts = {}
for row in users:
    cur = row.get("current", "")
    if cur:
        user_counts[cur] = user_counts.get(cur, 0) + 1

quality_policy = dict((policy.get("quality") or {}))
quality_policy.update(org_policy.get("quality") or {})
print("quality_policy", json.dumps(quality_policy, sort_keys=True))
print("service_matrix_updated", matrix.get("updated"), "items", len(matrix.get("items") or {}))
print("telegram_updated", telegram.get("updated"), "items", len(telegram.get("items") or {}))
print("quality_updated", quality.get("updated"), "items", len(quality.get("items") or {}))
print("restore_barrier", json.dumps({
    "enabled": barrier.get("enabled"),
    "expires_at": barrier.get("expires_at"),
    "clearance_expires_at": barrier.get("clearance_expires_at"),
    "clearance_generation_id": barrier.get("clearance_generation_id") or barrier.get("approved_generation_id"),
    "approved_selected_moves_hash": barrier.get("approved_selected_moves_hash"),
    "clearance_expected_selected_moves": barrier.get("clearance_expected_selected_moves"),
}, sort_keys=True))
print("egress_matrix_start")
for row in sorted(egresses, key=lambda r: r.get("id", "")):
    eid = row.get("id", "")
    live = ((state.get("egress") or {}).get(eid) or {})
    m = ((matrix.get("items") or {}).get(eid) or {})
    t = ((telegram.get("items") or {}).get(eid) or {})
    q = ((quality.get("items") or {}).get(eid) or {})
    q1h = ((q.get("windows") or {}).get("1h") or {})
    print(json.dumps({
        "id": eid,
        "enabled": row.get("enabled"),
        "interface": row.get("interface"),
        "role": row.get("role"),
        "manual_only": row.get("manual_only"),
        "reserve_only": row.get("reserve_only"),
        "canary_reserved": row.get("canary_reserved"),
        "execution_reserved": row.get("execution_reserved"),
        "autoswitch_allowed": row.get("autoswitch_allowed"),
        "rebalance_allowed": row.get("rebalance_allowed"),
        "production_assignment_allowed": row.get("production_assignment_allowed"),
        "users": user_counts.get(eid, 0),
        "load_users": load_state.get(f"{eid}_users"),
        "load_status": load_state.get(f"{eid}_load_status"),
        "health_code": live.get("code"),
        "health_severity": live.get("diagnose_severity"),
        "avg_mbps": live.get("avg_mbps"),
        "min_mbps": live.get("min_mbps"),
        "stability": live.get("stability"),
        "matrix_status": m.get("status"),
        "matrix_ok_count": m.get("ok_count"),
        "matrix_total": m.get("total"),
        "video_fitness": (((m.get("route_class_fitness") or {}).get("VIDEO_OPTIMIZED") or {}).get("status")),
        "global_fitness": (((m.get("route_class_fitness") or {}).get("GLOBAL_STABLE") or {}).get("status")),
        "telegram_status": t.get("status"),
        "telegram_blocked": t.get("blocked"),
        "telegram_bad_for_seconds": t.get("bad_for_seconds"),
        "quality_score": ((q.get("score") or {}).get("current")),
        "quality_trend": ((q.get("score") or {}).get("trend")),
        "quality_1h_avg": q1h.get("avg_mbps"),
        "quality_1h_min": q1h.get("min_mbps"),
        "quality_1h_stability": q1h.get("stability"),
        "quality_1h_fail_rate": q1h.get("fail_rate"),
    }, ensure_ascii=False, sort_keys=True))
print("egress_matrix_end")
PY
}

section "A2 FRESH RUNTIME READ"
run_cmd hostname
run_cmd date -Is

section "DEPLOY LINKAGE"
python3 - <<'PY'
import json
from pathlib import Path
for p in ("/opt/v7/deploy-manifest.json", "/opt/v7/runtime-linkage.json"):
    try:
        d = json.loads(Path(p).read_text())
    except Exception as exc:
        print(p, "ERROR", exc)
        continue
    print(p, json.dumps(d, sort_keys=True))
PY

section "SERVICES AND DUPLICATION PROCESS SCAN"
run_cmd systemctl is-active v7-admin-api.service
run_cmd systemctl is-active v7-users-autoswitch.service
run_cmd systemctl is-active v7-users-autoswitch.timer
run_cmd systemctl is-active v7-service-matrix-refresh.timer
run_cmd systemctl is-active v7-telegram-sentinel.timer
run_cmd systemctl is-active v7-egress-quality-compact.timer
pgrep -af 'v7-user-switch|v7-users-autoswitch.*--apply|v7-routing-sync|v7-rollback-last-change|v7-policy-live-rollback' || true

section "STATE MTIMES BEFORE"
stat -c '%n %s %y' \
  /opt/v7/egress/state/v7-state.json \
  /opt/v7/egress/state/service-matrix.json \
  /opt/v7/egress/state/telegram-sentinel.json \
  /opt/v7/egress/state/egress-quality-summary.json \
  /opt/v7/egress/state/egress-load.state \
  /opt/v7/egress/state/autoswitch-restore-barrier.json \
  /opt/v7/egress/state/path-samples.json 2>/dev/null || true

section "STALE CHECK BEFORE"
v7-state-stale-check 300 || true

section "FULL ELIGIBILITY STATE BEFORE"
state_summary

section "PLANNER BEFORE"
/usr/local/bin/v7-users-autoswitch --mode guarded --pretty || true

section "SAFE REFRESH SERVICE MATRIX"
v7-service-matrix-refresh-all --pretty --timeout 8 || true

section "SAFE REFRESH TELEGRAM SENTINEL NO AUTOSWITCH"
v7-telegram-sentinel --no-autoswitch --pretty || true

section "SAFE REFRESH QUALITY COMPACT"
v7-egress-quality-compact --pretty || true

section "SAFE REFRESH EGRESS LOAD"
v7-egress-load || true

section "STATE MTIMES AFTER"
stat -c '%n %s %y' \
  /opt/v7/egress/state/v7-state.json \
  /opt/v7/egress/state/service-matrix.json \
  /opt/v7/egress/state/telegram-sentinel.json \
  /opt/v7/egress/state/egress-quality-summary.json \
  /opt/v7/egress/state/egress-load.state \
  /opt/v7/egress/state/autoswitch-restore-barrier.json \
  /opt/v7/egress/state/path-samples.json 2>/dev/null || true

section "STALE CHECK AFTER"
v7-state-stale-check 300 || true

section "FULL ELIGIBILITY STATE AFTER"
state_summary

section "PLANNER AFTER"
/usr/local/bin/v7-users-autoswitch --mode guarded --pretty || true

section "RESTORE SETTLE AFTER"
v7-restore-settle-gate --pretty --state-dir /opt/v7/egress/state || true

section "NO MOVEMENT CHECK"
sha256sum /opt/v7/egress/state/users.registry /opt/v7/egress/state/egress.registry 2>/dev/null || true
if command -v v7-switch-log >/dev/null 2>&1; then
  v7-switch-log 2>/dev/null | tail -n 80
fi
pgrep -af 'v7-user-switch|v7-users-autoswitch.*--apply|v7-routing-sync|v7-rollback-last-change|v7-policy-live-rollback' || true

section "A2 REMOTE SCRIPT DONE"
