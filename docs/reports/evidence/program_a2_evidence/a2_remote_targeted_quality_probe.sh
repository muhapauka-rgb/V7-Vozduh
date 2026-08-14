#!/usr/bin/env bash
set +e
set -u
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

echo "=== A2 TARGETED QUALITY PROBE ==="
date -Is

echo "=== DIAGNOSE TO TMP ==="
v7-egress-diagnose --output /tmp/program-a2-egress-diagnose.state || true
cat /tmp/program-a2-egress-diagnose.state 2>/dev/null || true

for egress in awg0 awg3 vless wireguard-1779454504-c43409; do
  echo "=== PATH BENCHMARK ${egress} ==="
  v7-path-benchmark --egress "$egress" --runs 1 --timeout 12 --ping-timeout 1 --no-mtu --pretty || true
done

echo "=== A2 TARGETED QUALITY PROBE DONE ==="
