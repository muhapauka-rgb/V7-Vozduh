#!/usr/bin/env bash
set +e

echo "# E11.6 runtime post-deploy verification"
echo "## date -u"
date -u

echo
echo "## deployed diagnose tool"
stat -c 'owner=%U group=%G mode=%a size=%s mtime=%y path=%n' /usr/local/bin/v7-egress-diagnose 2>&1
sha256sum /usr/local/bin/v7-egress-diagnose 2>&1
bash -n /usr/local/bin/v7-egress-diagnose
echo "bash_n_rc=$?"

echo
echo "## pre-refresh diagnose entries"
grep -nE 'wireguard-1779454504-c43409|awg0|awg3|^1_' /opt/v7/egress/state/egress-diagnose.state 2>&1 || true

echo
echo "## run v7-egress-diagnose"
/usr/local/bin/v7-egress-diagnose 2>&1
echo "v7-egress-diagnose rc=$?"

echo
echo "## post-refresh diagnose entries"
grep -nE 'wireguard-1779454504-c43409|awg0|awg3|^1_' /opt/v7/egress/state/egress-diagnose.state 2>&1 || true

echo
echo "## live wireguard after"
ip link show v7e06a394c478 2>&1 || true
wg show v7e06a394c478 2>&1 || true
wg show v7e06a394c478 latest-handshakes 2>&1 || true
ip route show dev v7e06a394c478 2>&1 || true
ip route get 8.8.8.8 oif v7e06a394c478 2>&1 || true

echo
echo "## live awg after"
awg show awg0 2>&1 || true
awg show awg3 2>&1 || true

echo
echo "## focused state entries after"
for f in \
  /opt/v7/egress/state/egress-load.state \
  /opt/v7/egress/state/egress-load-summary.json \
  /opt/v7/egress/state/egress-diagnose.state \
  /opt/v7/egress/state/stability.state \
  /opt/v7/egress/state/interface-state.state
do
  echo "### $f"
  grep -nE 'wireguard-1779454504-c43409|v7e06a394c478|1779454504|wireguard|awg0|awg3|^1_' "$f" 2>&1 || true
done

echo
echo "## users on wireguard"
grep -n 'current=wireguard-1779454504-c43409' /opt/v7/egress/state/users.registry 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry /opt/v7/egress/state/egress.registry /opt/v7/egress/state/egress-diagnose.state 2>&1

echo
echo "## process guards"
pgrep -af 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' 2>&1 || true
ps -eo pid,ppid,etime,stat,args 2>&1 | grep -E '[v]7-user-switch|[v]7-routing-sync|[v]7-users-autoswitch.*--apply' || true

echo
echo "## planner/apply wireguard references"
journalctl -u v7-autoswitch-planner.service -n 80 --no-pager 2>&1 | grep -iE 'wireguard|c43409|v7e06a394c478|selected_moves|apply_result' || true
journalctl -u v7-users-autoswitch.service -n 80 --no-pager 2>&1 | grep -iE 'wireguard|c43409|v7e06a394c478|selected_moves|apply_result' || true

echo
echo "## runtime checkers"
for c in v7-reconcile-check v7-user-route-check v7-killswitch-check v7-provisioning-reconcile-check; do
  echo "--- $c"
  "$c" 2>&1
  echo "rc=$?"
done
