# Autoswitch Governance

This document is static governance only. `v7-users-autoswitch` was read for analysis but not executed.

## Role

`v7-users-autoswitch` is the planner and optional applier that can move users between egress channels. By default it returns a JSON plan. With `--apply`, it calls `v7-user-switch` for selected moves.

The installed systemd service is apply-capable:

```text
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

The timer currently represents a high-sensitivity control plane trigger because it can run apply periodically.

## State Inputs

```text
/opt/v7/egress/state/v7-state.json
/etc/v7/policy.json
/etc/v7/org-egress-policy.json
/opt/v7/egress/state/egress-quality-summary.json
/opt/v7/egress/state/autoswitch-safety.json
/opt/v7/egress/state/telegram-sentinel.json
/opt/v7/egress/state/egress-speed.json
/opt/v7/egress/state/client-speed.json
/opt/v7/egress/state/service-matrix.json
/opt/v7/egress/state/service-preferences.json
/opt/v7/egress/state/client-reconnect-state.json
/opt/v7/egress/state/vless-activity.json
/opt/v7/egress/state/egress-load-summary.json
/opt/v7/events/switch-history.jsonl
users.registry and egress.registry
```

## State Writes

Even without `--apply`, planning can write:

```text
/opt/v7/egress/state/egress-load-summary.json
/opt/v7/egress/state/client-reconnect-state.json when reconnect observation changes
```

With `--apply`, it can also write:

```text
/opt/v7/egress/state/autoswitch-safety.json
/opt/v7/egress/state/client-reconnect-state.json
```

and indirectly through `v7-user-switch`:

```text
per-user route table
users.registry
user-<ip>.assign
switch history
audit event
```

## Safety Gates

Observed gates:

- `autoswitch_enabled`;
- `autoswitch_mode`: `observe` blocks apply;
- per-run limits for planned, failover, reconnect, and rebalance moves;
- cooldown;
- user freeze thresholds for 1h and 24h;
- target block after A to B to A pattern;
- egress quarantine after failed route verifications;
- enabled/maintenance/manual-only egress gates;
- health code and severity gates;
- quality floors;
- load/capacity hard limits;
- org group allowed/preferred/excluded egress gates;
- `TRUSTED_RU_SENSITIVE` requires target egress metadata `trusted_ru`;
- Telegram hard statuses block candidates for Telegram-sensitive flows.

## Signals

| Signal | Authority |
|---|---|
| Health code / severity | Hard candidate gate |
| Load/capacity | Hard target gate and ranking |
| Quality floors | Hard candidate gate |
| Quality history high fail rate | Advisory in current code |
| Telegram hard status | Hard candidate gate for Telegram |
| Telegram degraded status | Scoring/advisory, not hard block |
| Reconnect observation | Can create reconnect rotation candidates |
| Org policy | Hard candidate gate |

## Oscillation Controls

Controls exist, but they depend on state being readable and fresh:

- cooldown;
- pair reversal window;
- blocked targets after repeated A/B/A;
- user freeze after too many switches;
- egress quarantine after verification failures;
- projected load accounting during move selection.

## Blast Radius

`autoswitch_max_failover_per_run` is the biggest immediate blast-radius lever. Historical reports showed `100` was too broad for a small platform. Current safe defaults should prefer:

```text
planned: 1
rebalance: 1-3
reconnect: bounded and lower than user count
failover: bounded by verified alternate capacity, not total users
```

## Execution Model

Default future posture:

```text
preview / read-only checker first
autoswitch dry-run only when low-risk state writes are accepted
one-user canary for apply
bounded apply only after route and kill-switch checks
```

`--apply` must require explicit operator approval unless in a separately governed automated window.

