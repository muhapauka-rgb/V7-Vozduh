#!/usr/bin/env bash
set -euo pipefail

STATE=/opt/v7/egress/state
USERS="$STATE/users.registry"

echo "host=$(hostname)"
echo "timestamp=$(date -Is)"
echo "users_registry_hash=$(sha256sum "$USERS" | awk '{print $1}')"

for ip in 10.0.0.3 10.0.0.6 10.7.0.3 10.7.0.2 10.7.0.4; do
  echo "--- user=$ip registry ---"
  grep "^ip=$ip " "$USERS"
  table=$(grep "^ip=$ip " "$USERS" | tr ' ' '\n' | awk -F= '$1=="table"{print $2; exit}')
  current=$(grep "^ip=$ip " "$USERS" | tr ' ' '\n' | awk -F= '$1=="current"{print $2; exit}')
  echo "current=$current"
  echo "table=$table"
  if [ -n "$table" ]; then
    echo "--- user=$ip route ---"
    ip route show table "$table" || true
    ip route get 8.8.8.8 from "$ip" iif wg0 || true
  fi
done
