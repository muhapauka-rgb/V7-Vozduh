#!/usr/bin/env bash
set -euo pipefail

STATE="/opt/v7/egress/state"
REGISTRY="${STATE}/egress.registry"
TARGET="amneziawg-exec-20260528-10-8-1-14"
BACKUP_DIR="${STATE}/e27_1-backups"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="${BACKUP_DIR}/egress.registry.${TS}"
REPORT="/tmp/e27_1_capacity_requalification.md"

mkdir -p "$BACKUP_DIR"
cp -a "$REGISTRY" "$BACKUP"

{
  printf "# E27.1 Capacity Requalification\n\n"
  printf "date_utc=%s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf "target=%s\n" "$TARGET"
  printf "backup=%s\n\n" "$BACKUP"
  printf "## Before\n"
  sha256sum "$REGISTRY"
  grep "id=${TARGET}" "$REGISTRY" || true
} > "$REPORT"

python3 - "$REGISTRY" "$TARGET" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
target = sys.argv[2]
lines = path.read_text(encoding="utf-8").splitlines()
out = []
found = False
for line in lines:
    if f"id={target}" not in line:
        out.append(line)
        continue
    found = True
    parts = line.split()
    updated = []
    seen_soft = False
    seen_hard = False
    for part in parts:
        if part.startswith("soft_limit="):
            updated.append("soft_limit=2")
            seen_soft = True
        elif part.startswith("hard_limit="):
            updated.append("hard_limit=2")
            seen_hard = True
        else:
            updated.append(part)
    if not seen_soft:
        updated.append("soft_limit=2")
    if not seen_hard:
        updated.append("hard_limit=2")
    out.append(" ".join(updated))
if not found:
    raise SystemExit(f"target not found: {target}")
path.write_text("\n".join(out) + "\n", encoding="utf-8")
PY

{
  printf "\n## After\n"
  sha256sum "$REGISTRY"
  grep "id=${TARGET}" "$REGISTRY" || true
  printf "\n## Diff\n"
  diff -u "$BACKUP" "$REGISTRY" || true
  printf "\n## Validation\n"
} >> "$REPORT"

set +e
v7-reconcile-check >/tmp/e27_1_reconcile.out 2>/tmp/e27_1_reconcile.err
rc_reconcile=$?
v7-user-route-check >/tmp/e27_1_user_route.out 2>/tmp/e27_1_user_route.err
rc_route=$?
v7-killswitch-check >/tmp/e27_1_killswitch.out 2>/tmp/e27_1_killswitch.err
rc_kill=$?
v7-provisioning-reconcile-check >/tmp/e27_1_provisioning.out 2>/tmp/e27_1_provisioning.err
rc_prov=$?
v7-second-canary-target-readiness --execution-target-id "$TARGET" --candidate-user 10.7.0.11 --pretty >/tmp/e27_1_readiness.out 2>/tmp/e27_1_readiness.err
rc_ready=$?
set -e

{
  printf "v7-reconcile-check=%s\n" "$rc_reconcile"
  printf "v7-user-route-check=%s\n" "$rc_route"
  printf "v7-killswitch-check=%s\n" "$rc_kill"
  printf "v7-provisioning-reconcile-check=%s\n" "$rc_prov"
  printf "v7-second-canary-target-readiness=%s\n" "$rc_ready"
  printf "\n### Readiness\n"
  cat /tmp/e27_1_readiness.out /tmp/e27_1_readiness.err
} >> "$REPORT"

if [ "$rc_reconcile" -ne 0 ] || [ "$rc_route" -ne 0 ] || [ "$rc_kill" -ne 0 ] || [ "$rc_prov" -ne 0 ] || [ "$rc_ready" -ne 0 ]; then
  cp -a "$BACKUP" "$REGISTRY"
  {
    printf "\n## Rollback\n"
    printf "capacity_requalification_successful=false\n"
    printf "rollback_performed=true\n"
    sha256sum "$REGISTRY"
    grep "id=${TARGET}" "$REGISTRY" || true
  } >> "$REPORT"
  exit 1
fi

{
  printf "\n## Verdict\n"
  printf "capacity_requalification_attempted=true\n"
  printf "capacity_requalification_successful=true\n"
  printf "runtime_mutation_scope=target metadata soft_limit/hard_limit only\n"
  printf "user_movement_performed=false\n"
  printf "routing_mutation_for_users=false\n"
} >> "$REPORT"
