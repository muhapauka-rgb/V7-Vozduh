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

section "A1 FRESH RUNTIME READ"
run_cmd hostname
run_cmd date -Is

section "REPO"
run_cmd git -C /opt/v7 branch --show-current
run_cmd git -C /opt/v7 rev-parse HEAD
run_cmd git -C /opt/v7 status --short

section "LINKAGE"
python3 - <<'PY'
import json
from pathlib import Path
for p in ("/opt/v7/deploy-manifest.json", "/opt/v7/runtime-linkage.json"):
    try:
        d = json.loads(Path(p).read_text())
    except Exception as exc:
        print(p, "ERROR", exc)
        continue
    print(p, d.get("commit") or d.get("commit_sha"), d.get("branch"), d.get("deploy_id"))
PY

section "SERVICES"
run_cmd systemctl is-active v7-admin-api.service
run_cmd systemctl is-active v7-users-autoswitch.service
run_cmd systemctl is-active v7-users-autoswitch.timer
run_cmd systemctl is-active v7-service-matrix-refresh.timer
run_cmd systemctl is-active v7-telegram-sentinel.timer
run_cmd systemctl is-active v7-egress-quality-compact.timer

section "DUPLICATION PROCESS SCAN"
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

section "STATE SUMMARY BEFORE"
python3 - <<'PY'
import json
from pathlib import Path
state_dir = Path("/opt/v7/egress/state")
def load(name, default):
    try:
        return json.loads((state_dir / name).read_text())
    except Exception:
        return default
matrix = load("service-matrix.json", {"items": {}})
telegram = load("telegram-sentinel.json", {"items": {}})
quality = load("egress-quality-summary.json", {"items": {}})
barrier = load("autoswitch-restore-barrier.json", {})
print("matrix_updated", matrix.get("updated"), "items", len(matrix.get("items") or {}))
for eid, row in sorted((matrix.get("items") or {}).items()):
    print("matrix", eid, row.get("status"), row.get("ok_count"), row.get("total"))
print("telegram_updated", telegram.get("updated"), "items", len(telegram.get("items") or {}))
for eid, row in sorted((telegram.get("items") or {}).items()):
    print("telegram", eid, row.get("status"), row.get("ok"), row.get("bad_for_seconds"), str(row.get("reason") or "")[:160])
print("quality_updated", quality.get("updated"), "items", len(quality.get("items") or {}))
for eid, row in sorted((quality.get("items") or {}).items()):
    score = (row.get("score") or {}).get("current")
    one = ((row.get("windows") or {}).get("1h") or {})
    print("quality", eid, "score", score, "avg", one.get("avg_mbps"), "min", one.get("min_mbps"), "fail", one.get("fail_rate"), "stab", one.get("stability"))
print("barrier_enabled", barrier.get("enabled"), "expires_at", barrier.get("expires_at"), "clearance_expires_at", barrier.get("clearance_expires_at"))
print("barrier_generation", barrier.get("clearance_generation_id") or barrier.get("approved_generation_id"))
print("barrier_hash", barrier.get("approved_selected_moves_hash"))
PY

section "PLANNER BEFORE"
/usr/local/bin/v7-users-autoswitch --mode guarded --pretty || true

section "SAFE REFRESH SERVICE MATRIX"
v7-service-matrix-refresh-all --pretty --timeout 8 || true

section "SAFE REFRESH TELEGRAM SENTINEL"
v7-telegram-sentinel --pretty || true

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

section "STATE SUMMARY AFTER"
python3 - <<'PY'
import json
from pathlib import Path
state_dir = Path("/opt/v7/egress/state")
def load(name, default):
    try:
        return json.loads((state_dir / name).read_text())
    except Exception:
        return default
matrix = load("service-matrix.json", {"items": {}})
telegram = load("telegram-sentinel.json", {"items": {}})
quality = load("egress-quality-summary.json", {"items": {}})
barrier = load("autoswitch-restore-barrier.json", {})
print("matrix_updated", matrix.get("updated"), "items", len(matrix.get("items") or {}))
for eid, row in sorted((matrix.get("items") or {}).items()):
    print("matrix", eid, row.get("status"), row.get("ok_count"), row.get("total"))
print("telegram_updated", telegram.get("updated"), "items", len(telegram.get("items") or {}))
for eid, row in sorted((telegram.get("items") or {}).items()):
    print("telegram", eid, row.get("status"), row.get("ok"), row.get("bad_for_seconds"), str(row.get("reason") or "")[:160])
print("quality_updated", quality.get("updated"), "items", len(quality.get("items") or {}))
for eid, row in sorted((quality.get("items") or {}).items()):
    score = (row.get("score") or {}).get("current")
    one = ((row.get("windows") or {}).get("1h") or {})
    print("quality", eid, "score", score, "avg", one.get("avg_mbps"), "min", one.get("min_mbps"), "fail", one.get("fail_rate"), "stab", one.get("stability"))
print("barrier_enabled", barrier.get("enabled"), "expires_at", barrier.get("expires_at"), "clearance_expires_at", barrier.get("clearance_expires_at"))
print("barrier_generation", barrier.get("clearance_generation_id") or barrier.get("approved_generation_id"))
print("barrier_hash", barrier.get("approved_selected_moves_hash"))
PY

section "PLANNER AFTER"
/usr/local/bin/v7-users-autoswitch --mode guarded --pretty || true

section "RESTORE SETTLE AFTER"
v7-restore-settle-gate --pretty --state-dir /opt/v7/egress/state || true

section "A1 REMOTE SCRIPT DONE"
