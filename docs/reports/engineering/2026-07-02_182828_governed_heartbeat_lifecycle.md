# Governed Autoswitch Heartbeat Lifecycle Forensic

Timestamp: 2026-07-02 18:28:28 +07
Mode: READ_ONLY_FORENSIC
Result: MISSING_AUTOMATIC_RESTART

## Mission

Determine whether the governed movement heartbeat lifecycle is canonical or an implementation defect, with focus on:

- allowed stop conditions;
- lifetime owner;
- restart responsibility;
- production state while a failed source still has affected users.

No code, deployment, systemd state, Runtime, Planner, Authority, or production routing was modified.

## Executive Finding

The movement heartbeat is a systemd timer:

```text
v7-users-autoswitch.timer
-> v7-users-autoswitch.service
-> /usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

It is the only movement-capable periodic path found in production. It can invoke the governed L3 owner, Runtime Apply, and Verification.

The timer is currently:

- `UnitFileState=enabled`
- `ActiveState=inactive`
- `SubState=dead`
- `NextElapseUSecRealtime=` empty
- last trigger: `Thu 2026-07-02 12:02:35 MSK`
- stopped: `Thu 2026-07-02 12:02:46 MSK`

The failed source still exists and still has affected users:

- source: `openvpn-1779388847-d2ad7c`
- severity: `FAIL`
- reason: `interface_down_or_missing`
- enabled users remaining on source: `10`

No canonical rule was found that allows the movement heartbeat to remain stopped while a failed source still has affected enabled users and the governed L3 production validation loop is the intended continuation path.

No automatic restart mechanism was found for a stopped timer.

## Classification

`MISSING_AUTOMATIC_RESTART`

This is not a Planner or Runtime implementation defect. It is a lifecycle/control-plane defect: after the movement heartbeat is stopped, no existing automatic owner brings it back even when failed-source work remains.

## Production Lifecycle Model

| Transition | Evidence | Initiator / owner | Expected behavior |
|---|---|---|---|
| Creation | `systemd/v7-users-autoswitch.timer`, `systemd/v7-users-autoswitch.service` | repo/systemd definition | define movement-capable governed heartbeat |
| Install / enable | `tools/v7-autoswitch-install-systemd` installs timer and runs `systemctl enable --now v7-users-autoswitch.timer` | deployment/operator tool | make timer enabled and active |
| Start | production journal `2026-07-02T12:00:23+03:00 Started v7-users-autoswitch.timer` | systemd job | enter active waiting state |
| Waiting | timer unit model: `OnUnitActiveSec=20s`, `AccuracySec=5s`, `Unit=v7-users-autoswitch.service` | systemd timer | schedule next governed service trigger |
| Trigger | production service starts at `12:00:23`, `12:00:47`, `12:01:08`, `12:01:44`, `12:02:08`, `12:02:35` MSK | systemd timer | run governed owner repeatedly |
| Service execution | `ExecStart=/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation ... --max-users 1` | `v7-users-autoswitch.service` | bounded one-user governed L3 validation |
| Completion | service `Type=oneshot`, `Restart=no`, exit status `0` | governed owner/service | service becomes inactive; timer should remain active |
| Next trigger | timer should calculate next `OnUnitActiveSec` trigger while active | systemd timer | continue until explicitly stopped |
| Stop | journal `2026-07-02T12:02:46+03:00 Stopped v7-users-autoswitch.timer` | systemd stop job | no next trigger after stop |
| Restart | no automatic restart policy found | none | requires explicit start/enable action |
| Disable | not observed; `UnitFileState=enabled` | none | timer is not disabled |

## Systemd Model

### `v7-users-autoswitch.timer`

- Type: systemd timer
- Description: `Run V7 guarded user egress autoswitch periodically`
- `OnBootSec=2min`
- `OnUnitActiveSec=20s`
- `AccuracySec=5s`
- `Unit=v7-users-autoswitch.service`
- `Persistent=no`
- `StopWhenUnneeded=no`
- `OnFailure=` empty
- `PartOf=` empty
- `Requires=sysinit.target`
- `Wants=` empty
- `Before=timers.target shutdown.target v7-users-autoswitch.service`
- `After=sysinit.target`
- `Triggers=v7-users-autoswitch.service`
- current `ActiveState=inactive`
- current `SubState=dead`
- current `UnitFileState=enabled`
- current `NextElapseUSecRealtime=` empty

### `v7-users-autoswitch.service`

- Type: `oneshot`
- Description: `V7 guarded user egress autoswitch`
- `Restart=no`
- `RemainAfterExit=no`
- `StopWhenUnneeded=no`
- `OnFailure=` empty
- `TriggeredBy=v7-users-autoswitch.timer`
- `Wants=network-online.target`
- `After=v7-health.service sysinit.target system.slice v7-benchmark.service systemd-journald.socket network-online.target basic.target v7-users-autoswitch.timer`
- current `ActiveState=inactive`
- current `SubState=dead`
- last `ExecMainStatus=0`
- last command:

```text
/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

### `v7-autoswitch-planner.timer`

- Type: systemd timer
- Description: `Run V7 autoswitch planner periodically`
- `OnBootSec=2min`
- `OnUnitActiveSec=30s`
- `AccuracySec=5s`
- `Unit=v7-autoswitch-planner.service`
- `Persistent=no`
- `StopWhenUnneeded=no`
- `OnFailure=` empty
- current `ActiveState=active`
- current `SubState=waiting`
- current `UnitFileState=enabled`

### `v7-autoswitch-planner.service`

- Type: `oneshot`
- Description: `V7 autoswitch planner state refresh`
- `Restart=no`
- `RemainAfterExit=no`
- `TriggeredBy=v7-autoswitch-planner.timer`
- last command:

```text
/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh
```

This path refreshes planner/intelligence state and does not invoke Runtime Apply or Verification.

## Current Production Incident Analysis

Source evidence from production:

```text
openvpn-1779388847-d2ad7c:
  code=000
  avg_mbps=0
  min_mbps=0
  stability=0
  users=10
  load_status=HARD_FULL
  diagnose_reason=interface_down_or_missing
  diagnose_severity=FAIL
```

Enabled users remaining on `openvpn-1779388847-d2ad7c`:

1. `10.7.0.2`
2. `10.7.0.4`
3. `10.7.0.6`
4. `10.7.0.8`
5. `10.7.0.9`
6. `10.7.0.10`
7. `10.7.0.11`
8. `10.7.0.12`
9. `10.7.0.13`
10. `10.7.0.15`

Answer: the movement heartbeat should still be running if the intended production lifecycle is continued bounded L3 evacuation.

Why inactive:

- It was stopped by a systemd stop job at `2026-07-02T12:02:46+03:00`.
- It remained enabled, but inactive/dead.
- There is no automatic restart or reactivation policy for the stopped timer.

Why planner heartbeat is still active:

- `v7-autoswitch-planner.timer` is a separate enabled timer.
- It was not stopped.
- It has its own timer/service pair and continues planner refresh every ~30 seconds.

## Stop Investigation

Search targets:

- `systemctl stop`
- `systemctl disable`
- `StopUnit`
- `DisableUnitFiles`
- `EnableUnitFiles`
- explicit `v7-users-autoswitch.timer` start/stop/enable occurrences

### Code Owners

| Occurrence | Classification | Reachability | Notes |
|---|---|---|---|
| `tools/v7-autoswitch-install-systemd:57 systemctl enable --now v7-users-autoswitch.timer` | deployment/install tool | reachable by operator/deploy | starts/restores timer; does not stop it |
| `tools/v7_sync_lib.py` | safe deploy library | reachable by safe deploy | can `daemon-reload`; only optional restart is `v7-admin-api.service`; no stop/disable for autoswitch timer |
| `tools/v7-governed-canary-dry-run-cycle` | governed L3 owner | production path | no `systemctl stop/disable v7-users-autoswitch.timer` found |
| `tools/v7-users-autoswitch` | Planner/Runtime apply owner | production path | no `systemctl stop/disable v7-users-autoswitch.timer` found |
| `admin_core/operator_execution.py` | authority/packet owner | production path | no `systemctl stop/disable v7-users-autoswitch.timer` found |
| `admin_core/operator_execution_pipeline.py` | operator execution pipeline | production path | no timer stop/disable implementation found |
| `tools/v7-egress-set-state` | egress state helper | manual tool | stops `v7-egress-openvpn@...`, not autoswitch heartbeat |

### Documents / Runbooks / Historical Reports

Multiple historical control-plane runbooks and reports include manual hold/restore commands:

- `systemctl stop v7-users-autoswitch.timer`
- `systemctl start v7-users-autoswitch.timer`

Classification:

- manual/operator tools and historical rehearsal evidence;
- reachable only by an operator or script executing those runbooks;
- not Runtime, Planner, governed owner, or automatic production code.

### D-Bus / Equivalent Stop

No repository occurrence of `StopUnit`, `DisableUnitFiles`, or equivalent systemd D-Bus stop for `v7-users-autoswitch.timer` was found in production code owners.

## Lifetime Owner

Proven owner split:

- systemd owns timer mechanics: active/waiting/trigger/service scheduling.
- deployment/installer/operator owns enable/start via `tools/v7-autoswitch-install-systemd` or explicit `systemctl enable --now/start`.
- governed L3 owner owns bounded execution after the service starts.
- Runtime/Planner do not own timer lifetime.
- OMP/canonical policy owns whether movement authority may be enabled, but no automatic restart mechanism was found.

Therefore the timer lifetime owner is not a Runtime owner. It is systemd plus operator/deployment control.

## Restart Policy

If the timer stops:

- `Persistent=no`: missed triggers are not caught up after reactivation.
- `StopWhenUnneeded=no`: systemd will not stop it just because dependencies are inactive.
- no `Restart=` exists for timer units.
- service has `Restart=no`; this only affects the oneshot service, not timer reactivation.
- `OnFailure=` is empty.
- no companion service, OMP worker, or Runtime owner was found that restarts the timer.

Intended current design from canonical/current reports:

- older canonical posture: timer-only movement is rejected; autoswitch timer was intentionally inactive/manual.
- 2026-07-02 governed trigger fix changed the service command to the governed owner and explicitly enabled the timer after deployment for bounded one-user L3 validation.
- after that change, continued evacuation requires the movement heartbeat to remain active or be explicitly restored.

No rule was found that makes a stopped movement heartbeat automatically restart while failed-source users remain.

## Current Questions

1. Who is responsible for starting the governed heartbeat?

Answer: operator/deployment tooling. Evidence: `tools/v7-autoswitch-install-systemd` and the 2026-07-02 governed trigger fix report both start/enable `v7-users-autoswitch.timer`.

2. Who is responsible for stopping it?

Answer: operator/systemd control plane. Runtime, Planner, governed owner, and safe deploy code do not contain a production stop/disable path for this timer. Production journal proves a systemd stop job, but the external actor is not persisted in the allowed unit evidence.

3. Who is responsible for restarting it?

Answer: operator/deployment tooling, because no automatic restart owner exists.

4. Can it legally stop while failed source still exists and remaining affected users > 0?

Answer: No canonical rule was found allowing this in the post-governed-trigger lifecycle.

5. If YES, prove canonical rule.

Answer: Not proven.

6. If NO, identify implementation defect.

Answer: missing automatic restart/lifecycle owner for a stopped movement heartbeat after it has been explicitly enabled as the governed L3 trigger.

## Canonical Questions

Should movement heartbeat run forever, run until no work, run only by operator, or run only after wake?

Evidence supports this nuanced model:

- it must not be blind broad movement;
- it must execute only through the governed L3 owner and existing gates;
- older canonical documents kept it disabled while it was an old broad apply timer;
- the 2026-07-02 implementation converted it into a bounded governed trigger and explicitly enabled it;
- no canonical document defines a self-stop condition tied to no work, incident closure, or failed-source evacuation completion;
- no canonical document defines an automatic reactivation owner after a stop.

Therefore the intended post-fix architecture is: operator/deployment enables a bounded governed movement heartbeat; execution remains governed and max-users=1; if the heartbeat is stopped before work is complete, existing architecture does not automatically restore it.

## Final Verdict

Classification: `MISSING_AUTOMATIC_RESTART`

Lifecycle owner: `systemd + operator/deployment control`; Runtime/Planner do not own timer lifetime.

Who stopped it: `systemd stop job` at `2026-07-02T12:02:46+03:00`; external actor not persisted in allowed unit journal evidence.

Who should restart it: existing operator/deployment control path, unless the architecture is extended later with an approved lifecycle owner.

Should it still be running: YES, because failed source `openvpn-1779388847-d2ad7c` remains `FAIL` and 10 enabled users remain assigned to it, while this timer is the movement-capable governed L3 heartbeat.

Patch required: PATCH_REQUIRED.
