# Z8.10 Scheduler And Service Forensics

## Systemd

Only one active V7 unit was found:

- `v7-admin-api.service`: loaded, enabled, active/running

Autoswitch units:

- `v7-users-autoswitch.service`: loaded/static, inactive/dead since `2026-05-27 20:13:14 MSK`
- `v7-users-autoswitch.timer`: loaded/enabled, inactive/dead since `2026-05-27 20:13:19 MSK`, no next trigger

Service definition:

- `ExecStart=/usr/local/bin/v7-users-autoswitch --apply`

Timer definition:

- `OnBootSec=2min`
- `OnUnitActiveSec=20s`
- `AccuracySec=5s`
- `Unit=v7-users-autoswitch.service`

## Cron

- Root crontab: absent
- `/etc/cron.d`: no V7 autoswitch scheduler found
- `/etc/cron.daily`: no V7 autoswitch scheduler found

## Running processes

Running V7-related processes include:

- `python3 /usr/local/bin/v7-api`
- `python3 /usr/local/bin/v7-admin-api`
- `python3 /usr/local/bin/v7-public-gateway`
- a 300-second egress benchmark loop
- a 30-second state maintenance loop

No running autoswitch process was found. The state maintenance loops do not execute `v7-users-autoswitch`.

## Verdict

Scheduler truth is known: the autoswitch systemd timer is configured but inactive, and no alternate autoswitch scheduler was found. This is a NO-GO for retrying Z9 because live runtime execution cannot be assumed active.

