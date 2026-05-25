#!/usr/bin/env bash
set -u
exec 2>&1

E8_HELD=0
E8_RESTORED=0
E8_ABORT=0
E8_PGREP_PATTERN='v7-users-autoswit[c]h|v7-user-swit[c]h|v7-routing-syn[c]'

section() {
  printf '\n__V7_E8_FILE:%s__\n' "$1"
}

run_sh() {
  printf '\n+ %s\n' "$*"
  bash -lc "$*"
  local rc=$?
  printf 'rc=%s\n' "$rc"
  return 0
}

restore_timer() {
  if [ "$E8_HELD" -eq 1 ] && [ "$E8_RESTORED" -eq 0 ]; then
    printf '\n+ systemctl start v7-users-autoswitch.timer\n'
    systemctl start v7-users-autoswitch.timer
    printf 'rc=%s\n' "$?"
    E8_RESTORED=1
  fi
}

on_exit() {
  restore_timer
}
trap on_exit EXIT INT TERM

capture_common_sample() {
  run_sh 'date -u'
  run_sh "pgrep -a -f '$E8_PGREP_PATTERN' || true"
  run_sh 'sha256sum /opt/v7/egress/state/users.registry 2>/dev/null || true'
  run_sh 'ip -4 rule show'
  run_sh 'ip -4 route show table all'
  run_sh 'v7-reconcile-check || true'
  run_sh 'v7-user-route-check || true'
  run_sh 'v7-killswitch-check || true'
  run_sh 'v7-provisioning-reconcile-check || true'
}

section pre-rehearsal.txt
run_sh 'date -u'
run_sh 'systemctl is-active v7-users-autoswitch.timer || true'
run_sh 'systemctl is-enabled v7-users-autoswitch.timer || true'
run_sh 'systemctl show v7-users-autoswitch.timer --property=Unit,ActiveState,SubState,TimersCalendar,NextElapseUSecRealtime,OnUnitActiveUSec || true'
run_sh 'systemctl is-active v7-users-autoswitch.service || true'
run_sh "pgrep -a -f '$E8_PGREP_PATTERN' || true"
run_sh 'ip -4 rule show'
run_sh 'ip -4 route show table all'
run_sh 'v7-user-route-check || true'
run_sh 'v7-killswitch-check || true'
run_sh 'v7-provisioning-reconcile-check || true'
run_sh 'v7-reconcile-check || true'
run_sh 'sha256sum /opt/v7/egress/state/users.registry 2>/dev/null || true'
run_sh "find /opt/v7/egress/state -maxdepth 1 -type f \\( -name '*switch*' -o -name '*autoswitch*' -o -name '*reconnect*' \\) 2>/dev/null | sort | xargs -r stat -c '%n %s %Y'"

section hold-confirmation.txt
run_sh 'date -u'
run_sh 'systemctl stop v7-users-autoswitch.timer'
run_sh 'systemctl stop v7-users-autoswitch.service'
E8_HELD=1
run_sh 'systemctl is-active v7-users-autoswitch.timer || true'
run_sh 'systemctl is-active v7-users-autoswitch.service || true'
run_sh "pgrep -a -f '$E8_PGREP_PATTERN' || true"

if pgrep -f "$E8_PGREP_PATTERN" >/dev/null 2>&1; then
  E8_ABORT=1
  section abort.txt
  run_sh 'date -u'
  printf 'abort_reason=active_control_plane_process_after_hold\n'
  run_sh "pgrep -a -f '$E8_PGREP_PATTERN' || true"
  restore_timer
else
  section quiet-window-sample-a.txt
  capture_common_sample

  sleep 25

  section quiet-window-sample-b.txt
  capture_common_sample

  sleep 25

  section quiet-window-sample-c.txt
  capture_common_sample
fi

section post-restore.txt
restore_timer
run_sh 'date -u'
run_sh 'systemctl is-active v7-users-autoswitch.timer || true'
run_sh 'systemctl is-enabled v7-users-autoswitch.timer || true'
run_sh 'systemctl show v7-users-autoswitch.timer --property=ActiveState,SubState,NextElapseUSecRealtime,OnUnitActiveUSec || true'
run_sh "pgrep -a -f '$E8_PGREP_PATTERN' || true"

section summary.txt
printf 'rehearsal_executed=true\n'
printf 'autoswitch_hold_attempted=true\n'
printf 'autoswitch_timer_restore_attempted=true\n'
printf 'abort=%s\n' "$E8_ABORT"
printf 'runtime_commands_executed=bounded_autoswitch_hold_restore_and_read_only_checks_only\n'
