#!/usr/bin/env bash
set -u

IFACE="${IFACE:-v7execwg0}"
URL="${URL:-https://speed.cloudflare.com/__down?bytes=2097152}"
VARIANTS="${VARIANTS:-1200 1360}"
PROBES="${PROBES:-8}"

orig_mtu="$(ip -o link show "$IFACE" | sed -n 's/.* mtu \([0-9][0-9]*\) .*/\1/p')"
if [ -z "$orig_mtu" ]; then
  echo "status=FAIL reason=missing_original_mtu iface=$IFACE"
  exit 2
fi

cleanup() {
  ip link set dev "$IFACE" mtu "$orig_mtu" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "status=START iface=$IFACE original_mtu=$orig_mtu url=$URL probes=$PROBES variants=\"$VARIANTS\""

for mtu in $VARIANTS; do
  echo "variant_start mtu=$mtu ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  ip link set dev "$IFACE" mtu "$mtu" || {
    echo "variant_status mtu=$mtu status=FAIL reason=set_mtu_failed"
    continue
  }
  sleep 2

  ping_line="$(ping -c 5 -W 3 -I "$IFACE" 1.1.1.1 2>&1 | tail -n 2 | tr '\n' ' ')"
  echo "ping mtu=$mtu ${ping_line}"

  i=1
  while [ "$i" -le "$PROBES" ]; do
    raw="$(curl --interface "$IFACE" -4 -L --max-time 20 -o /dev/null -sS -w 'http=%{http_code} speed_bps=%{speed_download} time_total=%{time_total}' "$URL" 2>&1)"
    speed="$(printf '%s\n' "$raw" | sed -n 's/.*speed_bps=\([0-9.][0-9.]*\).*/\1/p')"
    if [ -n "$speed" ]; then
      mbps="$(awk -v s="$speed" 'BEGIN { printf "%.2f", (s * 8) / 1000000 }')"
    else
      mbps="NA"
    fi
    echo "probe mtu=$mtu sample=$i ts=$(date -u +%Y-%m-%dT%H:%M:%SZ) mbps=$mbps raw=\"$raw\""
    i=$((i + 1))
    sleep 2
  done

  v7-reconcile-check >/dev/null || echo "checker_fail mtu=$mtu checker=v7-reconcile-check"
  v7-user-route-check >/dev/null || echo "checker_fail mtu=$mtu checker=v7-user-route-check"
  v7-killswitch-check >/dev/null || echo "checker_fail mtu=$mtu checker=v7-killswitch-check"
  v7-provisioning-reconcile-check >/dev/null || echo "checker_fail mtu=$mtu checker=v7-provisioning-reconcile-check"
  echo "variant_end mtu=$mtu ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
done

cleanup
echo "status=DONE restored_mtu=$orig_mtu ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
