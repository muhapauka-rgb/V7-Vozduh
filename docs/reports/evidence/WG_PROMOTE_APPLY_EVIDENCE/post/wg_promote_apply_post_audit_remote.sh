#!/usr/bin/env bash
set -euo pipefail

STATE=/opt/v7/egress/state
REG="$STATE/egress.registry"
TARGET=wireguard-1779454504-c43409

echo "host=$(hostname)"
echo "timestamp=$(date -Is)"
echo "registry=$REG"
echo "target=$TARGET"
echo "target_row=$(grep "^id=$TARGET " "$REG")"
echo "registry_hash=$(sha256sum "$REG" | awk '{print $1}')"
echo "registry_lines=$(wc -l < "$REG")"

for path in \
  "$STATE/users.registry" \
  "$STATE/service-matrix.json" \
  "$STATE/egress-quality-summary.json" \
  "$STATE/telegram-sentinel.json" \
  "$STATE/load-summary.state"; do
  if [ -e "$path" ]; then
    echo "hash:$path=$(sha256sum "$path" | awk '{print $1}')"
  else
    echo "missing:$path=true"
  fi
done

if grep "^id=$TARGET " "$REG" | grep -Eq '(^| )canary_reserved=|(^| )reservation_reason=|(^| )reservation_owner='; then
  echo "reservation_removed=false"
  exit 1
fi

echo "reservation_removed=true"
