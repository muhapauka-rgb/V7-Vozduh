# V7 Phase 34 Report: Guarded Autoswitch Engine

Date: 2026-05-18

## Goal

Add a production-oriented automatic channel switching layer that can scale to
dozens of external VPN egresses without losing the existing speed-based
selection logic.

The new layer must also support organization isolation: users from different
organizations can be constrained to different VPN pools so their traffic does
not share the same external egress unless policy explicitly allows it.

## Added

- `tools/v7-users-autoswitch`
- `tools/v7-egress-quality-compact`
- `tools/v7-autoswitch-install-systemd`
- `V7_AUTOSWITCH_ORG_POLICY.example.json`
- `systemd/v7-users-autoswitch.service`
- `systemd/v7-users-autoswitch.timer`
- `systemd/v7-egress-quality-compact.service`
- `systemd/v7-egress-quality-compact.timer`
- Admin API hooks in `admin/v7-admin-api`:
  - `GET /api/autoswitch-plan`
  - `GET /api/org-egress-policy`
  - `POST /api/actions/autoswitch-dry-run`
  - `POST /api/actions/autoswitch-apply-guarded`
  - `POST /api/actions/org-egress-policy-update`

## Operating Model

The command is read-only by default:

```bash
tools/v7-users-autoswitch --pretty
```

It emits a JSON plan with:

- all eligible and blocked candidates per user;
- current score and recommended score;
- switch reason;
- selected moves after global safety limits;
- organization isolation summary;
- bounded quality-history summary;
- anti-flapping safety state;
- human-readable explanation for each user decision;
- score breakdown for speed, stability, latency, service fitness, load, policy
  priority, group preference, quality history, and sticky behavior.

Autoswitch is enabled by default in policy:

```json
{
  "switch": {
    "autoswitch_enabled": true,
    "autoswitch_mode": "guarded"
  }
}
```

The Admin policy settings expose a toggle so operators can disable it without
removing the timer or scripts.

Apply is explicit at the command level:

```bash
tools/v7-users-autoswitch --mode guarded --apply --pretty
```

`autoswitch_enabled=false` or `mode=observe` blocks apply even if `--apply` is
passed.

## Scoring

The score keeps speed as a first-class factor:

- `avg_mbps`
- `min_mbps`
- client-measured speed when available

Speed is combined with:

- health;
- service matrix result;
- latency from first byte samples;
- stability;
- load/capacity;
- policy priority and weight;
- sticky bonus for the current egress;
- organization preference bonus.

A planned switch requires both:

- percentage improvement, default `20%`;
- absolute score delta, default `50`.

This avoids flapping when two VPNs trade places by small measurement noise.

## Gates Before Scoring

A candidate is blocked before scoring when it violates hard safety rules:

- disabled, maintenance, quarantine, or manual-only egress;
- non-200 health code;
- failing severity;
- hard-full capacity unless explicitly allowed;
- speed floor below policy;
- stability below policy;
- service matrix failure for a user-important service;
- trusted RU route requested but egress is not marked `trusted_ru`;
- organization policy mismatch.

## Compact Quality History

Long append-only logs are intentionally avoided. Quality history is compressed
into two bounded JSON files:

```text
/opt/v7/egress/state/egress-quality-summary.json
/opt/v7/egress/state/egress-quality-ring.json
```

`v7-egress-quality-summary.json` keeps EMA-style windows per egress:

- `5m`
- `1h`
- `24h`
- `7d`

`v7-egress-quality-ring.json` keeps only the latest samples, capped by
`--max-items` and defaulting to `2000`.

The autoswitch engine reads the summary file on every run. A channel with bad
recent history can be blocked by `quality_history_fail_rate_high`, and stable
history contributes to the score through `score_parts.quality_history`.

## Anti-Flapping State

Autoswitch safety state is stored in a compact file:

```text
/opt/v7/egress/state/autoswitch-safety.json
```

The file is rewritten atomically and pruned on every run. It keeps:

- up to the last `10` user switches within `24h`;
- per-user switch counters for `1h` and `24h`;
- short target blocks for A -> B -> A oscillation;
- per-egress incoming switch counters;
- failed verification counters and temporary egress quarantine.

Default safety policy:

```json
{
  "safety": {
    "user_freeze_switches_1h": 2,
    "user_freeze_switches_24h": 5,
    "user_freeze_1h_seconds": 3600,
    "user_freeze_24h_seconds": 21600,
    "target_block_seconds": 1800,
    "egress_quarantine_failed_verifications_1h": 2,
    "egress_quarantine_seconds": 3600
  }
}
```

## Dynamic Load Policy

Load limits can now be computed from the actual number of active users and
currently healthy channels:

```text
reserve_channels = max(1, ceil(healthy_channels * reserve_ratio))
working_channels = healthy_channels - reserve_channels
avg_load = active_users / working_channels

soft_limit = ceil(avg_load * soft_multiplier)
hard_limit = ceil(avg_load * hard_multiplier)
failover_hard_limit = ceil(avg_load * failover_hard_multiplier)
```

Default production-oriented values:

```json
{
  "load": {
    "mode": "dynamic",
    "reserve_ratio": 0.15,
    "soft_multiplier": 1.15,
    "hard_multiplier": 1.45,
    "failover_hard_multiplier": 2.0,
    "failover_capacity_multiplier": 1.25,
    "min_soft_limit": 5,
    "min_hard_limit": 10,
    "max_hard_limit": 80,
    "rebalance_max_moves_per_run": 3
  }
}
```

The autoswitch JSON plan exposes the computed values under `dynamic_load` and
per-channel values under each candidate's `load` block.

Autoswitch uses two load gates:

- planned optimization is blocked at `hard_limit`;
- failover is blocked only at `failover_hard_limit`.

Manual Admin switching remains an operator override. A direct admin-selected
`user-switch` can still move a user onto a hard-loaded channel; `HARD_FULL`
protects automatic selection, not deliberate manual routing.

## Organization Isolation

Organization policy is configured in `/etc/v7/org-egress-policy.json`.

Supported controls:

- `user_groups`: maps user IP to organization/group;
- `groups.<name>.allowed_egress`: exact or glob egress ids;
- `groups.<name>.preferred_egress`: egress ids that get a score bonus;
- `groups.<name>.excluded_egress`: blocked egress ids;
- `groups.<name>.isolation=exclusive`: block an egress already used by another
  group;
- `egress.<id>.groups`: access-control list for the egress;
- `egress.<id>.exclusive_group`: hard reservation for one group;
- `egress.<id>.capacity_users`: per-egress capacity for load scoring;
- `egress.<id>.trusted_ru`: required for sensitive RU route classes.

This lets 50 VPNs be partitioned as:

- per-organization dedicated pools;
- shared premium pools;
- trusted RU reserve pools;
- reserve-only failover pools;
- manual-only quarantine pools.

## Integration Points

Systemd flow:

```text
v7-health / v7-benchmark
  -> update v7-state.json, egress-speed.json, service-matrix.json
v7-egress-quality-compact.timer
  -> v7-egress-quality-compact.service
  -> compact egress-quality-summary.json and egress-quality-ring.json
v7-users-autoswitch.timer
  -> v7-users-autoswitch.service
  -> /usr/local/bin/v7-users-autoswitch --apply
```

The command reads policy on every run. The timer can stay enabled permanently;
the Admin toggle controls whether the engine applies selected moves.

Install preview:

```bash
tools/v7-autoswitch-install-systemd
```

Install apply on the server:

```bash
tools/v7-autoswitch-install-systemd --apply
```

Admin endpoints:

- `GET /api/autoswitch-plan`
- `GET /api/org-egress-policy`
- `POST /api/actions/autoswitch-dry-run`
- `POST /api/actions/autoswitch-apply-guarded`
- `POST /api/actions/org-egress-policy-update`

`autoswitch-apply-guarded` is blocked by Safe Mode, requires `admin` role, and
requires confirmation text:

```text
AUTOSWITCH
```

Admin UI:

- enabled/disabled toggle in policy settings;
- mode: observe / guarded / active;
- channel drawer controls in `Каналы -> Открыть -> Действия с каналом`:
  - per-channel `capacity_users`;
  - whether autoswitch may select this channel automatically;
  - reserve-only mode;
  - group ACL and exclusive organization;
  - target-channel preview and guarded apply;
- candidate table for all egresses;
- score breakdown;
- blocked reasons;
- organization pool view;
- selected moves;
- last automatic switches;
- apply one recommendation.
- readable per-user explanation:
  - selected channel;
  - speed/load/stability reasons;
  - quality-history trend;
  - rejected channels with block reasons.

## Safety

Apply uses the existing `v7-user-switch` command and sets:

```text
V7_SWITCH_REASON=autoswitch_planned
V7_SWITCH_REASON=autoswitch_failover
```

After every successful switch the engine can run:

```bash
v7-user-route-check
```

If verification fails, it rolls the user back to the previous egress unless
disabled with `--no-rollback-on-verify-fail`.

## Rollout Plan

1. Deploy the command, systemd timer, and org policy file.
2. Keep the timer enabled permanently.
3. Use the Admin `autoswitch_enabled` toggle to disable apply without removing
   the timer.
4. Review blocked reasons and score weights in Admin.
5. Use `guarded` with one planned move per run for normal production.
6. Add service-aware route apply after user-level autoswitch is stable.
7. Move to `active` only after switch history shows no flapping.

## Production Deployment

Deployed on VPS `195.2.79.116` on `2026-05-18`.

Server backup before install:

```text
/root/v7-autoswitch-deploy-backup-20260518-143555
```

Installed/updated:

- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-autoswitch-install-systemd`
- `/etc/systemd/system/v7-users-autoswitch.service`
- `/etc/systemd/system/v7-users-autoswitch.timer`
- `/etc/v7/org-egress-policy.json` only if it did not already exist
- `/usr/local/bin/v7-admin-api`

The production Admin API was patched from the live `/usr/local/bin/v7-admin-api`
copy rather than replacing it with the older local repository file.

Validation after install:

```json
{
  "v7-admin-api": "active",
  "v7-users-autoswitch.timer": "active",
  "v7-users-autoswitch.service": {
    "Result": "success",
    "ExecMainStatus": 0
  },
  "autoswitch": {
    "enabled": true,
    "mode": "guarded",
    "summary": {
      "users_total": 7,
      "egress_total": 2,
      "candidate_moves": 0,
      "selected_moves": 0,
      "org_groups": ["default"]
    }
  }
}
```

Authenticated endpoint smoke test:

```json
{
  "action": "autoswitch_plan",
  "rc": 0,
  "enabled": true,
  "mode": "guarded"
}
```

Current live reason for zero moves:

- both registered egresses are currently blocked as `HARD_FULL`;
- the engine is enabled and running, but it correctly avoids moving users into
  full channels.

## Notes

The local `admin/v7-admin-api` file still lags behind the live Admin API and was
already dirty before this phase. The deployed production file was patched from
the live server copy and is stored on the server; reconcile it back into the
repository in a dedicated sync pass to avoid mixing that large Admin UI update
with the autoswitch engine work.
