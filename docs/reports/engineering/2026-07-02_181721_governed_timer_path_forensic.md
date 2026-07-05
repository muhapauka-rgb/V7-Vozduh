# Governed Timer Path Forensic

Timestamp: 2026-07-02 18:17:21 +07
Mode: READ_ONLY_FORENSIC
Result: GOVERNED_TIMER_DISABLED

## Mission

Determine why the latest production certification observed planner refresh cycles instead of the governed L3 execution path.

No code, production, Runtime, Planner, Authority, Restore Barrier, or systemd state was modified.

## Production Host

- SSH target used: `v7-vps`
- hostname: `v3119922.hosted-by-vdsina.ru`
- production sample time: `2026-07-02T11:15:29Z`

## Root Verdict

`v7-autoswitch-planner.timer` and `v7-users-autoswitch.timer` are different execution paths.

The active path during certification was:

```text
v7-autoswitch-planner.timer
-> v7-autoswitch-planner.service
-> /usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh
-> planner refresh / DRY_RUN records
-> no Runtime Apply
-> no Verification
```

The governed movement-capable path was installed and enabled, but inactive/dead:

```text
v7-users-autoswitch.timer
-> v7-users-autoswitch.service
-> /usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
-> Runtime Apply
-> Verification
```

Therefore the latest certification observed the wrong execution path for Incident Source Continuity.

## Execution Graph

| Node | Purpose | Trigger | Starts | Can invoke governed L3? | Can invoke Runtime Apply? | Can invoke Verification? |
|---|---|---|---|---|---|---|
| `v7-autoswitch-planner.timer` | planner heartbeat | systemd timer, `OnUnitActiveSec=30s` | `v7-autoswitch-planner.service` | NO | NO | NO |
| `v7-autoswitch-planner.service` | planner state refresh | `v7-autoswitch-planner.timer` | `/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh` | NO | NO | NO |
| `v7-users-autoswitch --pre-planner-refresh` | refresh intelligence snapshots and produce planner/advisory state | planner service | snapshot refresh and planner state calculation | NO | NO | NO |
| `v7-users-autoswitch.timer` | governed autoswitch heartbeat | systemd timer, `OnUnitActiveSec=20s` | `v7-users-autoswitch.service` | YES | YES, through governed owner | YES, through governed owner |
| `v7-users-autoswitch.service` | movement-capable governed L3 owner launcher | `v7-users-autoswitch.timer` | `/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation ... --max-users 1` | YES | YES | YES |
| `v7-governed-canary-dry-run-cycle` | existing bounded governed L3 validation owner | autoswitch service or manual governed call | planner, packet, restore barrier, Runtime apply, verification | YES | YES | YES |
| `v7-users-autoswitch --apply` | Runtime apply/verify engine when invoked by governed owner | governed owner | user switch + verification + rollback path | N/A | YES | YES |

## Production State

### `v7-autoswitch-planner.timer`

- enabled: `enabled`
- active: `active`
- substate: `waiting`
- unit: `v7-autoswitch-planner.service`
- last trigger: `Thu 2026-07-02 14:16:45 MSK`
- list-timers sample: next at `Thu 2026-07-02 14:17:15 MSK`
- result: `success`

### `v7-autoswitch-planner.service`

- enabled: `static`
- active: `inactive`
- substate: `dead`
- triggered by: `v7-autoswitch-planner.timer`
- last exit code: `0`
- result: `success`
- last command:

```text
/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh
```

### `v7-users-autoswitch.timer`

- enabled: `enabled`
- active: `inactive`
- substate: `dead`
- unit: `v7-users-autoswitch.service`
- active entered: `Thu 2026-07-02 12:00:23 MSK`
- inactive entered: `Thu 2026-07-02 12:02:46 MSK`
- last trigger: `Thu 2026-07-02 12:02:35 MSK`
- next trigger: none
- result: `success`

### `v7-users-autoswitch.service`

- enabled: `static`
- active: `inactive`
- substate: `dead`
- triggered by: `v7-users-autoswitch.timer`
- last exit code: `0`
- result: `success`
- last start: `Thu 2026-07-02 12:02:35 MSK`
- last stop: `Thu 2026-07-02 12:02:58 MSK`
- last command:

```text
/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

## Dependency Analysis

Systemd dependency evidence:

- `v7-autoswitch-planner.timer Triggers=v7-autoswitch-planner.service`
- `v7-autoswitch-planner.service TriggeredBy=v7-autoswitch-planner.timer`
- `v7-users-autoswitch.timer Triggers=v7-users-autoswitch.service`
- `v7-users-autoswitch.service TriggeredBy=v7-users-autoswitch.timer`

No dependency evidence showed:

- planner timer triggering governed service
- governed timer depending on planner timer
- planner service starting `v7-governed-canary-dry-run-cycle`
- planner service starting `v7-users-autoswitch --apply`

The two timers are parallel systemd timers, not a parent/child scheduling chain.

## Timeline

### Before deploy / earlier validated path

The report `2026-07-02_032221_automatic_l3_governed_trigger_fix.md` records that the governed timer was enabled after deploying the service unit:

```text
systemctl enable --now v7-users-autoswitch.timer
```

The same report records a successful production chain:

```text
v7-users-autoswitch.timer
-> v7-users-autoswitch.service
-> /usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation ... --max-users 1
-> /usr/local/bin/v7-users-autoswitch --emergency-failover-autonomy --mode guarded --max-selected-moves 1 --user 10.7.0.3 --target-egress awg0 --apply --verify
```

Successful outcome in that evidence:

- user: `10.7.0.3`
- source: `openvpn-1779388847-d2ad7c`
- target: `awg0`
- terminal state: `APPLIED`
- verification: PASS

### Certification window

Live systemd journal showed:

- `2026-07-02T12:00:23+03:00`: `Started v7-users-autoswitch.timer`
- `2026-07-02T12:00:23+03:00`: `Starting v7-users-autoswitch.service`
- `2026-07-02T12:00:47+03:00`: governed service finished, then restarted
- `2026-07-02T12:01:08+03:00`: governed service started again
- `2026-07-02T12:01:44+03:00`: governed service started again
- `2026-07-02T12:02:08+03:00`: governed service started again
- `2026-07-02T12:02:35+03:00`: governed service started again
- `2026-07-02T12:02:46+03:00`: `v7-users-autoswitch.timer: Deactivated successfully`
- `2026-07-02T12:02:46+03:00`: `Stopped v7-users-autoswitch.timer`
- `2026-07-02T12:02:58+03:00`: last governed service finished

After that, only the planner timer continued:

- `v7-autoswitch-planner.service` starts and finishes every roughly 30 seconds.
- `v7-users-autoswitch.timer` has no next elapse time.
- `v7-users-autoswitch.service` has no further timer starts after the stopped timer.

### Latest certification observation

The report `2026-07-02_181043_incident_source_continuity_production_certification.md` observed post-deploy natural cycles from `v7-autoswitch-planner.timer`, not from `v7-users-autoswitch.timer`.

The observed terminal state was:

- terminal_state: `DRY_RUN`
- terminal_reason: `dry_run_restore_barrier_clearance_selected_moves_exceed_budget`
- Runtime Apply: not run
- Verification: not run

## Chain Questions

1. Does planner.timer ever invoke governed L3?

Answer: NO.

Evidence: planner service `ExecStart` is `v7-users-autoswitch --pre-planner-refresh=write ...`, not `v7-governed-canary-dry-run-cycle`.

2. Does governed timer depend on planner.timer?

Answer: NO.

Evidence: systemd `Wants`, `Requires`, `Triggers`, and `TriggeredBy` show separate timer/service pairs.

3. Can planner.timer alone move users?

Answer: NO.

Evidence: planner timer starts the pre-planner refresh path. The canonical heartbeat report classifies it as planner heartbeat only, selected/advisory only, no apply.

4. Can planner.timer only refresh state?

Answer: YES.

Evidence: `ExecStart=/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh`.

5. Which timer is supposed to evacuate users from a failed source?

Answer: `v7-users-autoswitch.timer`.

Evidence: its service invokes `v7-governed-canary-dry-run-cycle --execute-l3-production-validation ... --max-users 1`, and earlier production validation used this chain to move `10.7.0.3`.

6. Why was `v7-users-autoswitch.timer` inactive?

Answer: It was stopped by a systemd stop job at `2026-07-02T12:02:46+03:00`.

Evidence: systemd journal has `JOB_TYPE=stop`, `JOB_RESULT=done`, and messages `Deactivated successfully` and `Stopped v7-users-autoswitch.timer`.

7. Was it intentionally disabled?

Answer: It was not disabled; it remained `UnitFileState=enabled`. Whether the stop was intentional is not proven by the allowed evidence.

8. Who disabled it?

Answer: Nobody disabled it in the persisted systemd state. It is enabled. The actor that stopped the active timer is not persisted in the unit journal.

9. When?

Answer: `2026-07-02T12:02:46+03:00`.

10. Should it have been running continuously?

Answer: For automatic continued evacuation, yes: this is the movement-capable bounded governed heartbeat. The canonical heartbeat report also says apply heartbeat is `v7-users-autoswitch.timer/service` only when explicitly restored.

11. Did safe deploy disable it?

Answer: NO evidence.

Evidence: local safe-deploy code performs `systemctl daemon-reload` when systemd files changed and optionally restarts only `v7-admin-api.service`. It does not stop or disable `v7-users-autoswitch.timer`.

12. Did previous investigations disable it?

Answer: UNKNOWN from allowed evidence.

Evidence: unit journal proves the timer was stopped. It does not persist the external actor. A broader auth/root-history search was not used because it exceeds this forensic scope.

13. Did bounded validation intentionally stop it?

Answer: UNKNOWN.

Evidence: the stop occurred during a short governed execution window, but neither the governed owner code nor Runtime path contains `systemctl stop/disable v7-users-autoswitch.timer`.

14. Was Incident Source Continuity code ever exercised after deployment?

Answer: PARTIALLY before the timer stopped, but NOT during the latest certification observation.

Evidence: governed service ran several times between `12:00:23` and `12:02:58` MSK. The latest certification observation, however, sampled the later active natural path, which was planner-only. The observed DRY_RUN path did not reach Runtime Apply or Verification and therefore did not certify Incident Source Continuity.

15. If not, why not?

Answer: Because after `12:02:46` MSK, the governed timer was inactive/dead and only the planner-only timer remained active.

## Certification Validity

Was the latest production certification actually exercising the new Incident Source Continuity implementation?

Answer: NO for the observed certification window.

Reason:

- active execution path was planner-only refresh
- governed timer had no next scheduled trigger
- no Runtime Apply occurred
- no Verification occurred
- latest incident remained a DRY_RUN planner artifact

## Final Classification

Root verdict: `GOVERNED_TIMER_DISABLED`

This is not proof of a Planner or Runtime implementation defect. It proves the certification watched the planner-only heartbeat after the governed heartbeat had been stopped.

## Next Required Action

No code patch is required by this forensic result.

The next required action is operational: restore or explicitly start the existing `v7-users-autoswitch.timer` through the approved governed production procedure, then rerun Incident Source Continuity production certification against that movement-capable path.
