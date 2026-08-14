# V7 Vozduh - BLOCK 1.1 Telegram Sentinel Advisory-First Stabilization

Дата выполнения: 2026-05-23, live VPS `195.2.79.116`.

Цель: сохранить быстрый Telegram sentinel как sensor/observability source, но убрать прямое aggressive apply-pressure на autoswitch.

## Scope Guardrails

Не изменялось:

- kill switch;
- nftables;
- routing tables;
- route classes;
- direct/RU policy;
- TRUSTED_RU / Gosuslugi behavior;
- autoswitch code;
- autoswitch timer;
- Telegram sentinel timer cadence.

Изменено:

- live systemd drop-in для `v7-telegram-sentinel.service`;
- локальный systemd template `systemd/v7-telegram-sentinel.service`.

## Current Sentinel Escalation Model

Live unit до изменения:

```text
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1
```

Timer:

```text
OnUnitActiveSec=4s
AccuracySec=1s
```

Live binary supports advisory mode:

```text
--no-autoswitch
--dry-run-autoswitch
--autoswitch-cooldown-seconds
```

Code path:

```text
telegram check -> blocked_items -> run_autoswitch()
```

Default apply path when not disabled:

```text
v7-users-autoswitch --mode guarded --apply --service telegram --route-class GLOBAL_STABLE --pretty
```

With `--dry-run-autoswitch`, the command becomes non-apply:

```text
v7-users-autoswitch --service telegram --route-class GLOBAL_STABLE --pretty
```

With `--no-autoswitch`, sentinel still writes state and matrix updates, but does not execute `v7-users-autoswitch`.

## Evidence Before Change

Switch history before Block 1.1:

- switch total: `1158`
- last switch before advisory change: `2026-05-22T21:43:20.767491+00:00`
- new post-Block-1 guardrail switches were observed after the previous report:
  - `1 -> awg3`
  - around `2026-05-22T21:43Z`

This confirmed the Block 1 policy cap reduced blast radius but did not remove sentinel apply pressure.

## Live Runtime Change

Backup created:

```text
/etc/systemd/system/v7-telegram-sentinel.service.backup.block11-20260523-004340
```

Drop-in created:

```text
/etc/systemd/system/v7-telegram-sentinel.service.d/10-advisory-first.conf
```

Drop-in contents:

```ini
[Service]
ExecStart=
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Effective unit after `systemctl daemon-reload`:

```text
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Restart performed:

```text
systemctl restart v7-telegram-sentinel.service
```

The service is `Type=oneshot`; after successful run it returned to inactive, while the timer remained active.

## Local Template Change

Updated:

```text
systemd/v7-telegram-sentinel.service
```

New template command:

```text
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

This keeps future installs aligned with the live advisory-first behavior.

## Verification

Systemd status:

- `v7-telegram-sentinel.service`: inactive after successful one-shot run
- `v7-telegram-sentinel.timer`: active
- effective service has drop-in `10-advisory-first.conf`

Telegram state:

- `/opt/v7/egress/state/telegram-sentinel.json` updated after change.
- observed update: `2026-05-22T21:45:32.466619+00:00`
- checks continued across 6 egress channels.
- `autoswitch.started=false`
- `autoswitch.reason=no_blocked_egress_or_no_healthy_target`

Example post-change state for egress `1`:

```json
{
  "status": "DEGRADED",
  "matrix_status": "DEGRADED",
  "bad_now": false,
  "bad_since": "",
  "bad_for_seconds": 0.0,
  "blocked": false,
  "reason": "telegram partially reachable: 2/5 endpoints"
}
```

Switch history after advisory change:

- switches after change: `0`
- total remained: `1158`
- last switch remained: `2026-05-22T21:43:20.767491+00:00`

Datapath checks:

- `v7-killswitch-check`: `OK`
- `v7-user-route-check`: `OK`

## Events / Observability Note

`telegram-sentinel.json` and journald updated correctly after the change.

The JSONL event file did not append during the verification window because current sentinel code appends JSONL events only when:

- there are `blocked_items`; or
- autoswitch starts.

After advisory change, observed Telegram state was degraded/grace but not blocked, so no JSONL event was emitted. This is not a datapath regression, but it is an observability contract nuance.

Recommended follow-up: keep event stream event-based, but make the operator summary read from `telegram-sentinel.json` for live state. Do not require heartbeat JSONL events for every successful sentinel run.

## Risks Removed

Removed:

- Sentinel can no longer directly execute `v7-users-autoswitch --apply`.
- A Telegram timeout cannot immediately create a sentinel-triggered switch storm.
- Sentinel remains fast, but no longer acts as executor.

Preserved:

- Telegram checks.
- Telegram matrix updates.
- Telegram state file.
- journald visibility.
- autoswitch timer as the remaining apply authority.
- Block 1 policy bounds:
  - `cooldown_seconds=900`
  - `autoswitch_max_planned_per_run=1`
  - `autoswitch_max_failover_per_run=3`

## Remaining Risks

Autoswitch can still move users via `v7-users-autoswitch.timer` every 20 seconds.

The system still has health semantic gaps:

- quality summary can be empty;
- reconnect state can be empty per user;
- load summary may be missing;
- service matrix and sentinel can disagree.

Sentinel signal remains effective for observability, but the next stabilization step should ensure autoswitch treats Telegram as a supporting/persistent signal, not a single-signal route-changing trigger.

## Recommended Next Actions

1. Monitor switch-history for 2-6 hours.
2. Add compact operator incident summary:
   - sentinel advisory mode active;
   - latest Telegram degraded egress;
   - users currently anti-flap protected;
   - latest switch storm timestamp.
3. Align autoswitch signal semantics:
   - sentinel: fast service signal;
   - autoswitch timer: only apply authority;
   - policy: hard movement bounds;
   - safety file: anti-flap authority.
4. Prevent same-pair oscillation within a stability window:
   - no `A -> B -> A` unless multi-signal verified.

## Final Verdict

BLOCK 1.1 achieved the intended stabilization:

- Telegram sentinel is now advisory-first.
- Fast Telegram detection is preserved.
- Direct sentinel apply pressure is removed.
- No datapath or routing regression was observed.
- Kill switch and user routing checks remained OK.

The platform is calmer than after Block 1, but still needs health-semantic alignment before autoswitch can be considered production-mature.
