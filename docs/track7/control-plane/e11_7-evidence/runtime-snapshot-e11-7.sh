#!/usr/bin/env bash
set +e

echo "# E11.7 current runtime truth snapshot"
echo "## date -u"
date -u

echo
echo "## diagnose tool hash"
sha256sum /usr/local/bin/v7-egress-diagnose 2>&1

echo
echo "## systemd state"
for unit in \
  v7-health.service \
  v7-autoswitch-planner.timer \
  v7-autoswitch-planner.service \
  v7-users-autoswitch.timer \
  v7-users-autoswitch.service
do
  printf "%s active=" "$unit"
  systemctl is-active "$unit" 2>&1
  printf "%s enabled=" "$unit"
  systemctl is-enabled "$unit" 2>&1
done

echo
echo "## process guards"
pgrep -a -f 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' 2>&1

echo
echo "## users.registry sha and enabled summary"
sha256sum /opt/v7/egress/state/users.registry 2>&1
grep -E '^(user|ip|client|10\.)|current=|enabled=' /opt/v7/egress/state/users.registry 2>/dev/null || cat /opt/v7/egress/state/users.registry

echo
echo "## egress.registry sha and enabled summary"
sha256sum /opt/v7/egress/state/egress.registry 2>&1
cat /opt/v7/egress/state/egress.registry

echo
echo "## wireguard row"
grep -n 'wireguard-1779454504-c43409' /opt/v7/egress/state/egress.registry

echo
echo "## users per egress from registry"
awk '
  BEGIN { FS="[ \t]+" }
  /^#/ || NF == 0 { next }
  {
    user=""; current=""; enabled="";
    for (i=1; i<=NF; i++) {
      split($i, kv, "=");
      if (kv[1] == "user" || kv[1] == "ip" || kv[1] == "client") user=kv[2];
      if (kv[1] == "current") current=kv[2];
      if (kv[1] == "enabled") enabled=kv[2];
    }
    if (enabled == "1" && user != "" && current != "") {
      count[current]++; users[current]=users[current] " " user;
    }
  }
  END {
    for (eg in count) printf "%s users=%d%s\n", eg, count[eg], users[eg];
  }
' /opt/v7/egress/state/users.registry

echo
echo "## state files"
for f in \
  /opt/v7/egress/state/egress-load.state \
  /opt/v7/egress/state/egress-load-summary.json \
  /opt/v7/egress/state/egress-diagnose.state \
  /opt/v7/egress/state/stability.state \
  /opt/v7/egress/state/egress-quality-summary.json
do
  echo "### $f"
  if [ -f "$f" ]; then
    cat "$f"
  else
    echo "missing"
  fi
done

echo
echo "## interface flags"
for iface in v7e06a394c478 awg0 awg3 v7e356a192b79 v7edb0c189291 tun0; do
  ip -o link show "$iface" 2>/dev/null
done

echo
echo "## live WireGuard evidence"
ip link show v7e06a394c478 2>&1
wg show v7e06a394c478 2>&1
wg show v7e06a394c478 latest-handshakes 2>&1
ip route show dev v7e06a394c478 2>&1
ip route get 8.8.8.8 dev v7e06a394c478 2>&1

echo
echo "## switch history tail"
tail -n 300 /opt/v7/egress/state/switch-history.log 2>&1

echo
echo "## latest autoswitch planner/apply journal"
journalctl -u v7-autoswitch-planner.service -u v7-users-autoswitch.service -n 120 --no-pager 2>&1

echo
echo "## runtime checks"
v7-reconcile-check 2>&1
v7-user-route-check 2>&1
v7-killswitch-check 2>&1
v7-provisioning-reconcile-check 2>&1
