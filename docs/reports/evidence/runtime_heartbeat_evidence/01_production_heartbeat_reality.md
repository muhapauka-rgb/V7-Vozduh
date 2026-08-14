# Runtime Heartbeat Evidence 01 - Production Heartbeat Reality

Read-only production audit sample:

```text
host=v3119922.hosted-by-vdsina.ru
time=2026-06-04T17:13:45+03:00
```

Compact systemd reality:

```text
===v7-autoswitch-planner.timer===
Triggers=v7-autoswitch-planner.service
LoadState=loaded
ActiveState=active
SubState=waiting
FragmentPath=/etc/systemd/system/v7-autoswitch-planner.timer
UnitFileState=enabled

===v7-autoswitch-planner.service===
TriggeredBy=v7-autoswitch-planner.timer
LoadState=loaded
ActiveState=inactive
SubState=dead
FragmentPath=/etc/systemd/system/v7-autoswitch-planner.service
UnitFileState=static
ExecStart=/usr/local/bin/v7-users-autoswitch

===v7-users-autoswitch.timer===
Triggers=v7-users-autoswitch.service
LoadState=loaded
ActiveState=inactive
SubState=dead
FragmentPath=/etc/systemd/system/v7-users-autoswitch.timer
UnitFileState=enabled

===v7-users-autoswitch.service===
TriggeredBy=v7-users-autoswitch.timer
LoadState=loaded
ActiveState=inactive
SubState=dead
FragmentPath=/etc/systemd/system/v7-users-autoswitch.service
UnitFileState=static
ExecStart=/usr/local/bin/v7-users-autoswitch --apply

===v7-intelligence-snapshot-refresh.timer===
LoadState=not-found
ActiveState=inactive
SubState=dead

===v7-intelligence-snapshot-refresh.service===
LoadState=not-found
ActiveState=inactive
SubState=dead
```

Production conclusion:

- Current heartbeat owner is `v7-autoswitch-planner.timer`.
- Current recurring service executes planner-only `/usr/local/bin/v7-users-autoswitch`.
- Movement-capable `v7-users-autoswitch.timer/service` exists but is held/inactive.
- No standalone intelligence snapshot refresh service/timer exists.
- Therefore snapshot cadence was missing before this local implementation.

