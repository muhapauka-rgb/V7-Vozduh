#!/usr/bin/env bash
set -euo pipefail

REG="${V7_USERS_REGISTRY:-/opt/v7/egress/state/users.registry}"
STATE_DIR="${V7_STATE_DIR:-/opt/v7/egress/state}"
EGRESS_REG="${V7_EGRESS_REGISTRY:-$STATE_DIR/egress.registry}"
PUBLIC_IF="${V7_PUBLIC_IF:-ens3}"
VPN_SUBNETS="${V7_VPN_SUBNETS:-${V7_VPN_SUBNET:-10.0.0.0/24,10.7.0.0/22}}"
EGRESS_IFS=()
result="OK"

if [ -n "${V7_EGRESS_IFS:-}" ]; then
  # shellcheck disable=SC2206
  EGRESS_IFS=(${V7_EGRESS_IFS})
elif [ -r "$EGRESS_REG" ]; then
  while read -r ifname; do
    [ -n "$ifname" ] || continue
    [[ "$ifname" =~ ^[A-Za-z0-9_.-]{1,15}$ ]] || continue
    [ -e "/sys/class/net/$ifname" ] || continue
    EGRESS_IFS+=("$ifname")
  done < <(awk '
    {
      enabled="1"; iface="";
      for (i=1; i<=NF; i++) {
        split($i, a, "=");
        if (a[1] == "enabled") enabled=a[2];
        if (a[1] == "interface") iface=a[2];
      }
      if (enabled == "1" && iface != "") print iface;
    }
  ' "$EGRESS_REG" | sort -u)
fi
if [ "${#EGRESS_IFS[@]}" -eq 0 ]; then
  EGRESS_IFS=(awg2 tun0)
fi

echo "===== V7 PROVISIONING RECONCILE CHECK ====="
date -Is
echo "registry=$REG"
echo "vpn_subnets=$VPN_SUBNETS"
echo "public_if=$PUBLIC_IF"
echo "egress_ifs=${EGRESS_IFS[*]}"

egress_interface_for_id() {
  local want="$1"
  [ -r "$EGRESS_REG" ] || return 1
  awk -v want="$want" '
    {
      id=""; enabled="1"; iface="";
      for (i=1; i<=NF; i++) {
        split($i, a, "=");
        if (a[1] == "id") id=a[2];
        if (a[1] == "enabled") enabled=a[2];
        if (a[1] == "interface") iface=a[2];
      }
      if (id == want && enabled == "1" && iface != "") {
        print iface;
        exit;
      }
    }
  ' "$EGRESS_REG"
}

IFS=',' read -r -a VPN_SUBNET_ARR <<< "$VPN_SUBNETS"
client_src_set="$(nft list set inet v7_killswitch v7_client_src 2>/dev/null || true)"
postrouting_chain="$(nft list chain inet v7_killswitch postrouting 2>/dev/null || true)"
forward_chain="$(nft list chain inet v7_killswitch forward 2>/dev/null || true)"
iptables_postrouting="$(iptables -t nat -S POSTROUTING 2>/dev/null || true)"

echo
echo "===== SOURCE SET ====="
if [ -n "$client_src_set" ]; then
  echo "client_source_set=present"
  for subnet in "${VPN_SUBNET_ARR[@]}"; do
    subnet="${subnet//[[:space:]]/}"
    [ -n "$subnet" ] || continue
    if grep -Fq "$subnet" <<< "$client_src_set"; then
      echo "client_source_subnet=$subnet present"
    else
      echo "client_source_subnet=$subnet missing"
      result="FAIL"
    fi
    if ip -4 route show "$subnet" 2>/dev/null | grep -q ' dev wg0 '; then
      echo "reverse_route_subnet=$subnet present"
    else
      echo "reverse_route_subnet=$subnet missing"
      result="FAIL"
    fi
  done
else
  echo "client_source_set=missing"
  result="FAIL"
fi

echo
echo "===== NAT ====="
for egress_if in "${EGRESS_IFS[@]}"; do
  if grep -q "V7 NAT users via $egress_if" <<< "$postrouting_chain"; then
    echo "nat_$egress_if=present_nft"
  else
    nat_missing=0
    for subnet in "${VPN_SUBNET_ARR[@]}"; do
      subnet="${subnet//[[:space:]]/}"
      [ -n "$subnet" ] || continue
      if grep -F -- "-s $subnet" <<< "$iptables_postrouting" | grep -q -- "-o $egress_if .*MASQUERADE"; then
        echo "nat_${egress_if}_subnet=$subnet present_iptables"
      else
        echo "nat_${egress_if}_subnet=$subnet missing"
        nat_missing=1
      fi
    done
    if [ "$nat_missing" != "0" ]; then
      result="FAIL"
    fi
  fi
  if grep -q "V7 MSS clamp users via $egress_if" <<< "$forward_chain"; then
    echo "mss_clamp_$egress_if=present_nft"
  elif iptables -t mangle -S FORWARD 2>/dev/null | grep -F -- "-o $egress_if" | grep -q -- "TCPMSS"; then
    echo "mss_clamp_$egress_if=present_iptables"
  else
    echo "mss_clamp_$egress_if=missing"
    result="FAIL"
  fi
done

echo
echo "===== USERS ====="
if [ ! -f "$REG" ]; then
  echo "users_registry=missing"
  result="FAIL"
else
  wg_dump="$(wg show wg0 dump 2>/dev/null || true)"
  while read -r line; do
    [ -n "$line" ] || continue
    # shellcheck disable=SC2086
    eval "$line"
    [ "${enabled:-0}" = "1" ] || continue
    route="$(ip route get 8.8.8.8 from "$ip" iif wg0 2>&1 || true)"
    if echo "$wg_dump" | grep -q "$ip/32"; then
      wg_state="present"
    else
      wg_state="missing"
      result="FAIL"
    fi
    if echo "$route" | grep -q " dev $PUBLIC_IF "; then
      route_state="leak_risk_public_if"
      result="FAIL"
    elif echo "$route" | grep -q ' dev '; then
      route_state="ok"
    else
      route_state="inconclusive"
    fi
    expected_if="$(egress_interface_for_id "${current:-}" || true)"
    table_default="$(ip -4 route show table "${table:-0}" default 2>&1 || true)"
    if [ -z "$expected_if" ]; then
      table_state="egress_interface_missing"
      result="FAIL"
    elif grep -q " dev $expected_if\\b" <<< "$table_default"; then
      table_state="ok"
    else
      table_state="wrong_default_expected_$expected_if"
      result="FAIL"
    fi
    echo "user=$ip table=${table:-} current=${current:-} expected_if=$expected_if wg_peer=$wg_state route=$route_state table_default=$table_state detail=$route table_detail=$table_default"
  done < "$REG"
fi

echo
echo "===== RESULT ====="
echo "V7_PROVISIONING_RECONCILE_CHECK=$result"
[ "$result" = "OK" ]

--- killswitch ---
#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${V7_STATE_DIR:-/opt/v7/egress/state}"
REG="$STATE_DIR/users.registry"
EGRESS_REG="${V7_EGRESS_REGISTRY:-$STATE_DIR/egress.registry}"
PUBLIC_IF="ens3"
VPN_SUBNETS="${V7_VPN_SUBNETS:-${V7_VPN_SUBNET:-10.0.0.0/24,10.7.0.0/22}}"
DIRECT_MARK="0x77"
DIRECT_TABLE="70"
DIRECT_RULE_PREF="50"
EGRESS_IFS=()
result="OK"

if [ -r "$EGRESS_REG" ]; then
  while read -r ifname; do
    [ -n "$ifname" ] || continue
    [[ "$ifname" =~ ^[A-Za-z0-9_.-]{1,15}$ ]] || continue
    [ -e "/sys/class/net/$ifname" ] || continue
    EGRESS_IFS+=("$ifname")
  done < <(awk '
    {
      enabled="1"; iface="";
      for (i=1; i<=NF; i++) {
        split($i, a, "=");
        if (a[1] == "enabled") enabled=a[2];
        if (a[1] == "interface") iface=a[2];
      }
      if (enabled == "1" && iface != "") print iface;
    }
  ' "$EGRESS_REG" | sort -u)
fi
if [ "${#EGRESS_IFS[@]}" -eq 0 ]; then
  EGRESS_IFS=("awg2" "tun0")
fi

has_table=0
if nft list table inet v7_killswitch >/dev/null 2>&1; then
  has_table=1
fi
client_src_set="$(nft list set inet v7_killswitch v7_client_src 2>/dev/null || true)"
forward_chain="$(nft list chain inet v7_killswitch forward 2>/dev/null || true)"
prerouting_chain="$(nft list chain inet v7_killswitch prerouting 2>/dev/null || true)"
dstnat_chain="$(nft list chain inet v7_killswitch dstnat 2>/dev/null || true)"
postrouting_chain="$(nft list chain inet v7_killswitch postrouting 2>/dev/null || true)"
iptables_postrouting="$(iptables -t nat -S POSTROUTING 2>/dev/null || true)"

echo "===== V7 KILL SWITCH CHECK ====="
date -Is
echo "vpn_subnets=$VPN_SUBNETS"
echo "public_if=$PUBLIC_IF"
echo "egress_ifs=${EGRESS_IFS[*]}"

egress_interface_for_id() {
  local want="$1"
  [ -r "$EGRESS_REG" ] || return 1
  awk -v want="$want" '
    {
      id=""; enabled="1"; iface="";
      for (i=1; i<=NF; i++) {
        split($i, a, "=");
        if (a[1] == "id") id=a[2];
        if (a[1] == "enabled") enabled=a[2];
        if (a[1] == "interface") iface=a[2];
      }
      if (id == want && enabled == "1" && iface != "") {
        print iface;
        exit;
      }
    }
  ' "$EGRESS_REG"
}

if [ "$has_table" = "1" ]; then
  echo "table=present"
else
  echo "table=missing"
  result="FAIL"
fi

if [ -n "$client_src_set" ]; then
  echo "client_source_set=present"
else
  echo "client_source_set=missing"
  result="FAIL"
fi

IFS=',' read -r -a VPN_SUBNET_ARR <<< "$VPN_SUBNETS"
for subnet in "${VPN_SUBNET_ARR[@]}"; do
  subnet="${subnet//[[:space:]]/}"
  [ -n "$subnet" ] || continue
  if grep -Fq "$subnet" <<< "$client_src_set"; then
    echo "client_source_subnet=$subnet present"
  else
    echo "client_source_subnet=$subnet missing"
    result="FAIL"
  fi

  if ip -4 route show "$subnet" 2>/dev/null | grep -q ' dev wg0 '; then
    echo "reverse_route_subnet=$subnet present"
  else
    echo "reverse_route_subnet=$subnet missing"
    result="FAIL"
  fi
done

if grep -q 'V7 block direct leak to public interface' <<< "$forward_chain"; then
  echo "direct_leak_drop_rule=present"
else
  echo "direct_leak_drop_rule=missing"
  result="FAIL"
fi

if grep -q 'V7 allow explicit direct whitelist' <<< "$forward_chain"; then
  echo "direct_whitelist_rule=present"
else
  echo "direct_whitelist_rule=missing"
  result="FAIL"
fi

sysctl net.ipv4.ip_forward | sed 's/^/sysctl_/'

if ip -4 rule show pref "$DIRECT_RULE_PREF" 2>/dev/null | grep -q "fwmark $DIRECT_MARK lookup $DIRECT_TABLE"; then
  echo "direct_fwmark_rule=present"
else
  echo "direct_fwmark_rule=missing"
  result="FAIL"
fi

if ip -4 rule show 2>/dev/null | awk '$1 ~ /^[0-9]+:/ {gsub(":", "", $1); if ($1 < 98 && /fwmark 0x77/ && /lookup 70/) found=1} END {exit found ? 0 : 1}'; then
  echo "direct_fwmark_precedes_user_rules=OK"
else
  echo "direct_fwmark_precedes_user_rules=FAIL"
  result="FAIL"
fi

if ip -4 route show table "$DIRECT_TABLE" 2>/dev/null | grep -q "dev $PUBLIC_IF"; then
  echo "direct_route_table=present"
else
  echo "direct_route_table=missing"
  result="FAIL"
fi

if grep -q 'V7 mark explicit direct whitelist' <<< "$prerouting_chain"; then
  echo "direct_mark_rule=present"
else
  echo "direct_mark_rule=missing"
  result="FAIL"
fi

if grep -q 'V7 capture client UDP DNS' <<< "$dstnat_chain"; then
  echo "dns_capture_udp=present"
else
  echo "dns_capture_udp=missing"
  result="FAIL"
fi

if grep -q 'V7 capture client TCP DNS' <<< "$dstnat_chain"; then
  echo "dns_capture_tcp=present"
else
  echo "dns_capture_tcp=missing"
  result="FAIL"
fi

for egress_if in "${EGRESS_IFS[@]}"; do
  if grep -q "V7 NAT users via $egress_if" <<< "$postrouting_chain"; then
    echo "nat_$egress_if=present"
  else
    nat_missing=0
    for subnet in "${VPN_SUBNET_ARR[@]}"; do
      subnet="${subnet//[[:space:]]/}"
      [ -n "$subnet" ] || continue
      if grep -F -- "-s $subnet" <<< "$iptables_postrouting" | grep -q -- "-o $egress_if .*MASQUERADE"; then
        echo "nat_${egress_if}_subnet=$subnet present_iptables"
      else
        echo "nat_${egress_if}_subnet=$subnet missing"
        nat_missing=1
      fi
    done
    if [ "$nat_missing" = "0" ]; then
