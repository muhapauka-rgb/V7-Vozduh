#!/usr/bin/env bash
set -euo pipefail

STATE=/opt/v7/egress/state
REG="$STATE/egress.registry"
TARGET=wireguard-1779454504-c43409
TS="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="$STATE/egress.registry.wg_promote_apply_backup.$TS"
TMP="$(mktemp "$STATE/egress.registry.wg_promote_apply.XXXXXX")"

cleanup() {
  rm -f "$TMP"
}
trap cleanup EXIT

echo "host=$(hostname)"
echo "timestamp=$(date -Is)"
echo "registry=$REG"
echo "target=$TARGET"

before_hash="$(sha256sum "$REG" | awk '{print $1}')"
before_lines="$(wc -l < "$REG" | tr -d ' ')"
before_row="$(grep "^id=$TARGET " "$REG")"

cp -p "$REG" "$BACKUP"

awk -v id="$TARGET" '
  BEGIN { changed = 0 }
  $0 ~ "^id=" id " " {
    out = ""
    for (i = 1; i <= NF; i++) {
      if ($i ~ /^(canary_reserved|reservation_reason|reservation_owner)=/) {
        continue
      }
      out = out (out ? " " : "") $i
    }
    print out
    changed += 1
    next
  }
  { print }
  END {
    if (changed != 1) {
      exit 42
    }
  }
' "$REG" > "$TMP"

after_lines="$(wc -l < "$TMP" | tr -d ' ')"
if [ "$before_lines" != "$after_lines" ]; then
  echo "line_count_check=FAIL before=$before_lines after=$after_lines"
  exit 43
fi

after_row="$(grep "^id=$TARGET " "$TMP")"
if printf '%s\n' "$after_row" | grep -Eq '(canary_reserved|reservation_reason|reservation_owner)='; then
  echo "reservation_removal_check=FAIL"
  exit 44
fi

if ! grep -q '^id=amneziawg-exec-20260528-10-8-1-14 ' "$TMP"; then
  echo "neighbor_row_check=FAIL"
  exit 45
fi

cat "$TMP" > "$REG"
after_hash="$(sha256sum "$REG" | awk '{print $1}')"

echo "backup_path=$BACKUP"
echo "rollback_command=cp -p $BACKUP $REG"
echo "before_hash=$before_hash"
echo "after_hash=$after_hash"
echo "before_lines=$before_lines"
echo "after_lines=$after_lines"
echo "before_row=$before_row"
echo "after_row=$after_row"
echo "line_count_check=PASS"
echo "reservation_removal_check=PASS"
echo "neighbor_row_check=PASS"

if command -v v7-audit-log >/dev/null 2>&1; then
  v7-audit-log \
    "wg_canary_dereservation" \
    "egress" \
    "id=$TARGET removed_canary_reserved=true backup=$BACKUP" \
    object_type=egress \
    object_id="$TARGET" \
    result=OK >/dev/null 2>&1 || true
  echo "audit_log_attempted=true"
else
  echo "audit_log_attempted=false"
fi

echo "WG_PROMOTE_APPLY_MUTATION=OK"
