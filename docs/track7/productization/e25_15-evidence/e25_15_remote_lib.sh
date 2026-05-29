#!/usr/bin/env bash
set -u

STATE="${STATE:-/opt/v7/egress/state}"
AUDIT="${AUDIT:-/opt/v7/audit/operator-execution-audit.jsonl}"
PACKET="${PACKET:-/tmp/e25_15_packet.json}"
TARGET="${TARGET:-amneziawg-exec-20260528-10-8-1-14}"
CAND="${CAND:-10.7.0.11}"
DRIFT_USER="${DRIFT_USER:-10.7.0.16}"

hash_file() {
  if [ -f "$1" ]; then
    sha256sum "$1" | cut -d " " -f 1
  else
    echo MISSING
  fi
}

row_for_ip() {
  grep "ip=$1 " "$STATE/users.registry" || true
}

field_for_ip() {
  ip="$1"
  key="$2"
  awk -v ip="$ip" -v key="$key" '$0 ~ "ip=" ip {
    for (i=1; i<=NF; i++) {
      split($i, kv, "=")
      if (kv[1] == key) { print kv[2]; exit }
    }
  }' "$STATE/users.registry"
}

target_row() {
  grep "id=$TARGET" "$STATE/egress.registry" || true
}

target_field() {
  key="$1"
  awk -v id="$TARGET" -v key="$key" '$0 ~ "id=" id {
    for (i=1; i<=NF; i++) {
      split($i, kv, "=")
      if (kv[1] == key) { print kv[2]; exit }
    }
  }' "$STATE/egress.registry"
}

target_users_count() {
  grep "current=$TARGET" "$STATE/users.registry" | grep "enabled=1" | wc -l | tr -d " "
}

selected_moves_count() {
  files="$(find "$STATE" -maxdepth 1 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null | sort)"
  if [ -z "$files" ]; then echo 0; return; fi
  grep -hEv '^[[:space:]]*($|#)' $files | wc -l | tr -d " "
}

selected_moves_hash() {
  files="$(find "$STATE" -maxdepth 1 -type f \( -iname '*selected*move*' -o -iname '*selected_moves*' \) 2>/dev/null | sort)"
  if [ -z "$files" ]; then echo NONE; return; fi
  sha256sum $files | sha256sum | cut -d " " -f 1
}

hidden_movers_count() {
  matches="$(pgrep -af 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' 2>/dev/null | grep -v -E 'pgrep|grep|e25_15_|ssh v7-vps' || true)"
  if [ -z "$matches" ]; then echo 0; else printf "%s\n" "$matches" | wc -l | tr -d " "; fi
}

checkers_ok() {
  v7-reconcile-check >/dev/null 2>&1 &&
    v7-user-route-check >/dev/null 2>&1 &&
    v7-killswitch-check >/dev/null 2>&1 &&
    v7-provisioning-reconcile-check >/dev/null 2>&1
}

route_table_for() {
  table="$1"
  ip route show table "$table" | tr "\n" " "
}

route_get_for() {
  ip="$1"
  ip route get 8.8.8.8 from "$ip" iif wg0 2>/dev/null | tr "\n" " "
}

readiness_pretty() {
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --pretty
}

readiness_json() {
  v7-second-canary-target-readiness --execution-target-id "$TARGET" --json
}

packet_field() {
  python3 - "$PACKET" "$1" <<'PY'
import json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
cur = payload
for part in sys.argv[2].split("."):
    if isinstance(cur, dict):
        cur = cur.get(part)
    else:
        cur = None
        break
print("" if cur is None else cur)
PY
}

packet_hash_actual() {
  python3 - "$PACKET" <<'PY'
import hashlib, json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
payload.pop("packet_hash", None)
print(hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest())
PY
}

packet_non_expired() {
  python3 - "$PACKET" <<'PY'
import json, sys
from datetime import datetime, timezone
payload = json.load(open(sys.argv[1], encoding="utf-8"))
exp = datetime.fromisoformat(payload["approval_expires_at"].replace("Z", "+00:00"))
print("true" if exp > datetime.now(timezone.utc) else "false")
PY
}

write_audit_event() {
  event="$1"
  details="$2"
  mkdir -p "$(dirname "$AUDIT")"
  python3 - "$AUDIT" "$PACKET" "$event" "$details" <<'PY'
import hashlib, json, sys
from datetime import datetime, timezone
audit, packet_path, event, details = sys.argv[1:5]
packet = json.load(open(packet_path, encoding="utf-8"))
row = {
    "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "block": "E25.15",
    "event": event,
    "packet_id": packet.get("packet_id"),
    "approval_id": packet.get("approval_id"),
    "operation_id": packet.get("operation_id"),
    "candidate_user": packet.get("candidate_user"),
    "target": packet.get("to_egress"),
    "details": details,
}
row["record_hash"] = hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
with open(audit, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(row, sort_keys=True) + "\n")
print(row["record_hash"])
PY
}
