#!/usr/bin/env bash
set -u
exec 2>&1

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

section trusted-ru-direct-policy-details
run 'for f in /opt/v7/egress/state/trusted-ru-diagnostic.state /opt/v7/egress/state/trusted-ru-decision.state /opt/v7/egress/state/route-classes.state /opt/v7/egress/state/direct-ru-autosync.state /etc/v7/direct/domains.conf /etc/v7/policy/direct_ru_domains.conf /etc/v7/policy/trusted_ru_sensitive_domains.conf; do [ -e "$f" ] && stat -c "%n %s %Y %a" "$f"; done'
run 'for f in /opt/v7/egress/state/trusted-ru-diagnostic.state /opt/v7/egress/state/trusted-ru-decision.state /opt/v7/egress/state/route-classes.state /opt/v7/egress/state/direct-ru-autosync.state; do [ -r "$f" ] && { echo "--- $f"; head -n 80 "$f"; }; done'

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
