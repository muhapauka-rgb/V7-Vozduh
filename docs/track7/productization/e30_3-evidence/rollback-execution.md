# E30.3 Rollback Execution

date_utc=2026-05-29T17:07:05Z
rollback_target=1
commands_executed=10

## 10.7.0.2
timestamp_utc=2026-05-29T17:07:01Z
command=v7-user-switch 10.7.0.2 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.2.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.2.stderr

## 10.7.0.3
timestamp_utc=2026-05-29T17:07:01Z
command=v7-user-switch 10.7.0.3 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.3.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.3.stderr

## 10.7.0.4
timestamp_utc=2026-05-29T17:07:01Z
command=v7-user-switch 10.7.0.4 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.4.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.4.stderr

## 10.7.0.5
timestamp_utc=2026-05-29T17:07:02Z
command=v7-user-switch 10.7.0.5 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.5.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.5.stderr

## 10.7.0.6
timestamp_utc=2026-05-29T17:07:02Z
command=v7-user-switch 10.7.0.6 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.6.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.6.stderr

## 10.7.0.8
timestamp_utc=2026-05-29T17:07:03Z
command=v7-user-switch 10.7.0.8 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.8.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.8.stderr

## 10.7.0.11
timestamp_utc=2026-05-29T17:07:03Z
command=v7-user-switch 10.7.0.11 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.11.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.11.stderr

## 10.7.0.12
timestamp_utc=2026-05-29T17:07:04Z
command=v7-user-switch 10.7.0.12 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.12.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.12.stderr

## 10.7.0.14
timestamp_utc=2026-05-29T17:07:04Z
command=v7-user-switch 10.7.0.14 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.14.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.14.stderr

## 10.7.0.15
timestamp_utc=2026-05-29T17:07:05Z
command=v7-user-switch 10.7.0.15 1
exit_code=0
stdout_file=/tmp/e30_3/rollback/10.7.0.15.stdout
stderr_file=/tmp/e30_3/rollback/10.7.0.15.stderr

users_registry_diff=/tmp/e30_3/users.rollback.diff
route_diff=/tmp/e30_3/routes.rollback.diff
audit_tail=/tmp/e30_3/audit-tail.after-rollback.txt
