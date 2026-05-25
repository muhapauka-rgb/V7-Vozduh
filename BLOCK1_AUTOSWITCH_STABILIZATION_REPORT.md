# V7 Vozduh - BLOCK 1 Autoswitch Stabilization Report

Дата проверки: 2026-05-23, live VPS `195.2.79.116`.

Задача: расследовать failover loops autoswitch, проверить Telegram sentinel, policy bounds и применить только минимальные безопасные изменения, если они доказанно нужны.

## Scope Guardrails

Не изменялось:

- kill switch;
- nftables;
- routing tables;
- route classes;
- direct/RU policy;
- TRUSTED_RU / Gosuslugi behavior;
- systemd timers;
- autoswitch code;
- provisioning or datapath logic.

Изменено только `/etc/v7/policy.json`, секция `switch`, с backup перед изменением.

## Live Autoswitch Baseline

Systemd:

- `v7-users-autoswitch.service`: `ExecStart=/usr/local/bin/v7-users-autoswitch --apply`
- `v7-users-autoswitch.timer`: `OnUnitActiveSec=20s`
- `v7-telegram-sentinel.service`: `ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1`
- `v7-telegram-sentinel.timer`: `OnUnitActiveSec=4s`

Active policy before stabilization:

```json
{
  "autoswitch_enabled": true,
  "autoswitch_mode": "guarded",
  "cooldown_seconds": 300,
  "autoswitch_max_planned_per_run": 3,
  "autoswitch_max_failover_per_run": 100
}
```

Verdict: autoswitch was live in apply mode and bounded too loosely for a 16-user platform. The timer cadence and sentinel cadence were both aggressive, but timers were not changed in this block.

## Failover Loop Timeline

Evidence source: `/opt/v7/events/switch-history.jsonl`.

Since `2026-05-22T15:00:00Z`:

- total switches: `364`
- `autoswitch_failover`: `354`
- `autoswitch_rollback`: `8`
- `autoswitch_rebalance`: `2`

Since `2026-05-22T21:00:00Z`:

- total switches: `32`
- all `32` were `autoswitch_failover`
- transitions:
  - `1 -> vless`: `16`
  - `vless -> 1`: `16`

Latest burst pattern:

- `2026-05-22T21:10:13Z` to `21:10:30Z`: twelve users moved `1 -> vless`
- `2026-05-22T21:12:28Z` to `21:12:32Z`: four more users moved `1 -> vless`
- `2026-05-22T21:15:33Z` to `21:15:47Z`: twelve users moved `vless -> 1`
- `2026-05-22T21:17:37Z` to `21:17:41Z`: four more users moved `vless -> 1`

High burst minutes across the day:

- `2026-05-22T16:41Z`: `16` switches
- `2026-05-22T17:14Z`: `16` switches
- `2026-05-22T17:35Z`: `16` switches
- `2026-05-22T18:58Z`: `16` switches
- `2026-05-22T15:28Z`: `15` switches
- `2026-05-22T20:08Z`: `14` switches
- `2026-05-22T20:32Z`: `13` switches

Top observed transition pairs since `15:00Z`:

- `1 -> vless`: `62`
- `awg0 -> 1`: `58`
- `vless -> 1`: `50`
- `1 -> awg3`: `37`
- `1 -> awg0`: `35`
- `awg3 -> 1`: `32`
- `vless -> awg0`: `23`
- `awg3 -> vless`: `21`
- `vless -> awg3`: `20`

## Affected Users

Evidence source: `/opt/v7/egress/state/autoswitch-safety.json`.

All 16 users were in penalty/freeze state after the storm:

- `10.0.0.2`: `1h=4`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.0.0.3`: `1h=8`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.0.0.6`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.2`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.3`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.4`: `1h=8`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.5`: `1h=5`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.6`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.7`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.8`: `1h=8`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.9`: `1h=4`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.10`: `1h=8`, `24h=10`, penalty until `2026-05-23T03:15:48Z`
- `10.7.0.11`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:17:42Z`
- `10.7.0.12`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:17:42Z`
- `10.7.0.13`: `1h=6`, `24h=10`, penalty until `2026-05-23T03:17:42Z`
- `10.7.0.14`: `1h=8`, `24h=10`, penalty until `2026-05-23T03:17:42Z`

Verdict: anti-flap eventually protected users by freezing/penalizing them, but it triggered after excessive movement. It is a last-resort brake, not a calm routing strategy.

## Root Cause

The failover loop was caused by interaction of four factors:

1. Telegram sentinel can trigger real autoswitch apply.
2. Sentinel runs every 4 seconds and has its own short autoswitch cooldown behavior.
3. Active policy allowed `autoswitch_max_failover_per_run=100`, which is effectively unbounded for 16 users.
4. Health semantics were contradictory, so the chosen egress alternated between `1` and `vless` depending on which signal was active.

Observed examples from sentinel autoswitch output:

- When egress `1` was considered Telegram-blocked, autoswitch rejected `1` with `route_class_GLOBAL_STABLE_failed` and selected alternatives like `awg0` or `vless`.
- Later, autoswitch selected `1` again using reasons like `telegram_down_grace`, stronger speed/stability scores and sticky/current route logic.
- Alternatives were rejected for reasons such as `min_mbps_below_floor`, `stability_below_floor`, `target_blocked_for_user`, `quality_history_fail_rate_high` or `severity_SUSPECT`.

This creates a classic oscillation:

`1 degraded for Telegram` -> move users away -> alternate target degrades or becomes target-blocked -> `1` becomes attractive again under grace/sticky/speed scoring -> users move back.

## Telegram Sentinel Verdict

Evidence source: `/opt/v7/events/telegram-sentinel-20260522.jsonl`.

Since `2026-05-22T21:00:00Z`:

- sentinel events with blocked egress `1`: `23`
- sentinel autoswitch starts: `14`
- command used by sentinel:

```text
v7-users-autoswitch --mode guarded --apply --service telegram --route-class GLOBAL_STABLE --pretty
```

Verdict:

- Sentinel is not only observability. It can trigger live apply.
- With `OnUnitActiveSec=4s`, this creates high trigger pressure.
- The service-level signal is too strong relative to bounded migration limits.
- Keeping sentinel signal is useful, but sentinel-driven apply should become advisory or much more strongly bounded.

## Health Semantics Findings

Current source contradictions:

- `/opt/v7/egress/state/service-matrix.json`: egress statuses included `1=OK`, `vless=WARN`, `awg0=WARN`, `awg3=WARN`.
- `/opt/v7/egress/state/egress-quality-summary.json`: valid file, but `items={}` at the inspected moment.
- `/opt/v7/egress/state/client-reconnect-state.json`: 16 users present, but user entries were empty.
- `/opt/v7/egress/state/egress-load-summary.json`: missing.
- `/opt/v7/egress/state/telegram-sentinel.json`: at one sampled moment all checked egress were healthy and no blocked egress existed, but recent event history had repeated `1` blocked events.

Verdict: autoswitch is operating with incomplete and inconsistent health inputs. The platform has enough signals to explain the storm, but not enough semantic alignment to make calm decisions reliably.

## Dangerous Parameters

Critical:

- `autoswitch_max_failover_per_run=100`
  - Unsafe for a 16-user platform.
  - Allows a single apply run to move the whole user base several times in practice across repeated triggers.

High risk:

- Sentinel timer `OnUnitActiveSec=4s`
  - Too aggressive if sentinel can trigger apply.
  - Acceptable only if sentinel is advisory/no-apply.

High risk:

- Autoswitch timer `OnUnitActiveSec=20s`
  - Not automatically wrong, but unsafe with a high failover cap and unstable health semantics.

Medium risk:

- `cooldown_seconds=300`
  - Too short after a full platform storm.

## Stabilization Applied

Backup created:

```text
/etc/v7/policy.json.backup.block1-20260523-002634
```

Changed `/etc/v7/policy.json`:

Before:

```json
{
  "autoswitch_enabled": true,
  "autoswitch_mode": "guarded",
  "cooldown_seconds": 300,
  "autoswitch_max_planned_per_run": 3,
  "autoswitch_max_failover_per_run": 100
}
```

After:

```json
{
  "autoswitch_enabled": true,
  "autoswitch_mode": "guarded",
  "cooldown_seconds": 900,
  "autoswitch_max_planned_per_run": 1,
  "autoswitch_max_failover_per_run": 3
}
```

Rationale:

- Autoswitch remains enabled.
- Mode remains `guarded`.
- No timer was changed.
- No routing/datapath behavior was changed directly.
- The change only reduces maximum blast radius per run and increases stability window.

## Verification After Change

Policy updated at:

```text
2026-05-22T21:26:34.325117+00:00
```

Immediate safety checks:

- `v7-killswitch-check`: `V7_KILLSWITCH_CHECK=OK`
- `v7-user-route-check`: `OK`
- `v7-users-autoswitch.service`: inactive after run
- `v7-telegram-sentinel.service`: inactive after run
- `v7-users-autoswitch.timer`: active
- `v7-telegram-sentinel.timer`: active

Switch-history after policy change:

- total before policy change: `1155`
- last switch before policy change: `2026-05-22T21:17:41.075656Z`
- switches after policy change during verification window: `0`
- sentinel autoswitch starts after policy change during verification window: `0`

Important limitation: this is an immediate regression check, not a long-duration stability proof.

## Is Apply Mode Safe Currently?

Verdict: partially safer after policy guardrail, but not fully safe.

Apply mode is now bounded to 3 failover moves per run and 1 planned move per run, which is materially safer than 100. However, two risks remain:

- sentinel can still invoke autoswitch apply;
- health semantics remain inconsistent.

Production-safe autoswitch requires sentinel apply demotion or stronger sentinel-specific cooldown plus unified health authority.

## Are Timers Too Aggressive?

Verdict:

- `v7-users-autoswitch.timer` every 20 seconds is aggressive but tolerable only with strict caps and consistent health semantics.
- `v7-telegram-sentinel.timer` every 4 seconds is too aggressive if it can trigger apply.

Recommended future action: keep high-frequency sentinel only for detection, not for apply.

## Does Anti-Flap Work?

Verdict: technically yes, strategically too late.

Evidence:

- all 16 users were penalty/freeze protected after the loop;
- penalty windows extended to `2026-05-23T03:15Z-03:17Z`;
- target-blocked logic appeared in autoswitch rejection reasons.

Problem:

- anti-flap allowed users to hit 10 daily switches before strong protection;
- this is contrary to calm routing.

## Are Users Currently Protected?

Yes, in the narrow sense:

- all users have active penalty/freeze protection after the loop;
- the new policy reduces maximum failover blast radius;
- no immediate route or kill-switch regression was detected.

But this is not a clean state:

- all users were already affected by the storm;
- many users ended on egress `1`;
- storm prevention should happen before users reach freeze/penalty.

## Operator Visibility Recommendation

Add compact incident visibility, not a dashboard rewrite:

- `Autoswitch instability: high`
- `16 users protected by anti-flap`
- `last switch storm: 32 failovers since 21:00Z`
- `top loop: 1 <-> vless`
- `sentinel-triggered apply: observed`
- `current guardrail: failover cap 3, cooldown 900s`

Recommended grouping:

- Summary: `Autoswitch unstable, guardrail active`
- Impact: `16 users hit anti-flap protection`
- Cause: `Telegram sentinel apply + loose failover cap + inconsistent health`
- Safe action: `demote sentinel apply to advisory`
- Details: expandable timeline and switch counts

## Recommended Next Actions

Priority 0:

- Monitor switch history for 2 to 6 hours after guardrail.
- If switches resume, temporarily demote sentinel to no-apply/advisory mode.

Priority 1:

- Change sentinel systemd args to advisory mode:

```text
v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

This should be a separate explicit change because it affects automation behavior.

Priority 2:

- Add a sentinel-specific cooldown of at least 300 to 900 seconds if no-apply is not accepted.
- Add operator incident summary for switch storms.
- Align health authority:
  - service matrix: service signal;
  - sentinel: service-specific advisory;
  - autoswitch-safety: anti-flap authority;
  - policy: hard bounds;
  - quality/load/reconnect: supporting signals only until they are complete.

Priority 3:

- Prevent same-pair oscillation `A -> B -> A` within a stability window unless the current egress is objectively broken and verified by multiple signals.
- Require multi-signal persistence before platform-wide failover.

## Final Block 1 Verdict

The failover loop was real and severe. It was not caused by a kill-switch or route-table failure. It was caused by autoswitch being too permissive under frequent sentinel-triggered apply pressure and inconsistent health inputs.

The live system is safer after the policy guardrail, but it is not fully stabilized until sentinel apply is demoted or heavily bounded and health semantics are aligned.
