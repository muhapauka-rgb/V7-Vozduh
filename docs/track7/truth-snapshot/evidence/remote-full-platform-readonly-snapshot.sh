#!/usr/bin/env bash
set -u
exec 2>&1

P='v7-users-autoswit[c]h|v7-user-swit[c]h|v7-routing-syn[c]|v7-policy-appl[y]|v7-direct-[a-z-]*|v7-trusted-ru-[a-z-]*|v7-proxy-[a-z-]*|v7-public-gatewa[y]|v7-client-speed-ap[i]|v7-path-sample-inges[t]'

section() {
  printf '\n__V7_TRUTH_SECTION:%s__\n' "$1"
}

run() {
  printf '\n+ %s\n' "$*"
  bash -lc "$*"
  local rc=$?
  printf 'rc=%s\n' "$rc"
  return 0
}

section runtime-identity
run 'date -u'
run 'hostname'
run 'hostnamectl 2>/dev/null || true'
run 'uname -a'
run 'uptime'
run 'ip -br addr show'
run 'ip -br link show'
run "find /opt/v7 /etc/v7 /usr/local/bin -maxdepth 2 \\( -name 'v7*' -o -name '*manifest*' \\) -printf '%p %s %TY-%Tm-%TdT%TH:%TM:%TS %m\\n' 2>/dev/null | sort | head -n 220"

section systemd-v7
run "systemctl list-units --type=service --all 'v7*' --no-pager || true"
run "systemctl list-timers --all 'v7*' --no-pager || true"
run "systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service v7-telegram-sentinel.service v7-telegram-sentinel.timer 2>/dev/null || true"
run "systemctl is-enabled v7-users-autoswitch.timer v7-users-autoswitch.service v7-telegram-sentinel.service v7-telegram-sentinel.timer 2>/dev/null || true"
run "systemctl show v7-users-autoswitch.timer --property=Unit,ActiveState,SubState,NextElapseUSecRealtime,OnUnitActiveUSec 2>/dev/null || true"

section processes
run "ps -eo pid,ppid,etime,stat,command | grep -E '$P' | grep -v grep || true"
run "pgrep -a -f '$P' || true"

section routing-datapath
run 'ip -4 rule show'
run 'ip -4 route show table all'
run 'v7-user-route-check || true'
run 'v7-reconcile-check || true'
run 'v7-provisioning-reconcile-check || true'

section killswitch
run 'v7-killswitch-check || true'
run "nft list ruleset 2>/dev/null | grep -E 'v7|wg0|tun0|awg|client|kill|drop|masquerade|mss|mark' | head -n 220 || true"

section autoswitch-state
run "sha256sum /opt/v7/egress/state/users.registry /opt/v7/egress/state/egress.registry 2>/dev/null || true"
run "stat -c '%n %s %Y %a' /opt/v7/egress/state/users.registry /opt/v7/egress/state/egress.registry 2>/dev/null || true"
run "find /opt/v7/egress/state -maxdepth 1 -type f \\( -name '*switch*' -o -name '*autoswitch*' -o -name '*reconnect*' -o -name '*load*' -o -name '*penalt*' -o -name '*fail*' \\) -printf '%p %s %T@ %m\\n' 2>/dev/null | sort"
run "tail -n 80 /opt/v7/events/switch-history.jsonl 2>/dev/null || true"

section provisioning-state
run "head -n 80 /opt/v7/egress/state/users.registry 2>/dev/null || true"
run "head -n 120 /opt/v7/egress/state/egress.registry 2>/dev/null || true"
run "find /opt/v7/egress/state -maxdepth 1 -type f \\( -name 'user-*.assign' -o -name '*ipam*' -o -name '*draft*' -o -name '*rollback*' -o -name '*backup*' \\) -printf '%p %s %T@ %m\\n' 2>/dev/null | sort | head -n 220"

section trusted-ru-direct-policy
run "find /opt/v7 /etc/v7 -maxdepth 5 -type f \\( -iname '*trusted*ru*' -o -iname '*gosuslugi*' -o -iname '*direct*' -o -iname '*route-class*' -o -iname '*policy*' -o -iname '*domains*' \\) -printf '%p %s %T@ %m\\n' 2>/dev/null | sort | head -n 240"
run "for f in /opt/v7/egress/state/trusted-ru-diagnostic.state /opt/v7/egress/state/trusted-ru-decision.state /opt/v7/egress/state/route-classes.state /opt/v7/egress/state/direct-domains.state /etc/v7/direct/domains.conf /opt/v7/direct/domains.conf; do [ -e \"$f\" ] && stat -c '%n %s %Y %a' \"$f\"; done"
run "for f in /opt/v7/egress/state/trusted-ru-diagnostic.state /opt/v7/egress/state/trusted-ru-decision.state /opt/v7/egress/state/route-classes.state; do [ -r \"$f\" ] && { echo '---' \"$f\"; head -n 80 \"$f\"; }; done"

section proxy-telemetry-admin
run "systemctl list-units --type=service --all 'v7*proxy*' 'v7*public*' 'v7*client*' 'v7*path*' 'v7*admin*' --no-pager || true"
run "ss -ltnup 2>/dev/null | grep -E '(:80|:443|:800|:808|:844|:300|v7|python|uvicorn|nginx|caddy|sing-box|xray)' || true"
run "ps -eo pid,ppid,etime,stat,command | grep -E 'v7-admin|v7-public-gateway|v7-client-speed-api|v7-path-sample-ingest|uvicorn|gunicorn|nginx|caddy|sing-box|xray' | grep -v grep || true"
run "find /opt/v7 /etc/systemd/system /etc/v7 -maxdepth 4 -type f \\( -iname '*admin*' -o -iname '*proxy*' -o -iname '*public*' -o -iname '*client-speed*' -o -iname '*path-sample*' \\) -printf '%p %s %T@ %m\\n' 2>/dev/null | sort | head -n 240"

section governance-markers
run "find /opt/v7 -maxdepth 6 -type f \\( -iname '*manifest*' -o -iname '*release*' -o -iname '*baseline*' \\) -printf '%p %s %T@ %m\\n' 2>/dev/null | sort | head -n 240"

section summary-marker
printf 'runtime_snapshot_read_only=true\n'
printf 'runtime_mutation_performed=false\n'
printf 'canary_executed=false\n'
