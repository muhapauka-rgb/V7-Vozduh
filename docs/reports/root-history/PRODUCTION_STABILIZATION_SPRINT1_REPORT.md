# V7 Vozduh Production Stabilization Sprint 1 Report

Дата: 2026-05-22  
VPS: `195.2.79.116` / `v3119922.hosted-by-vdsina.ru`  
Scope: autoswitch safety, health semantics, identity DB path contract, deploy baseline, operator incident visibility  
Runtime mutation status: **no live routing/datapath/timer/policy changes applied**

## Executive Verdict

Sprint 1 подтвердил, что production runtime operational, но autoswitch behavior сейчас слишком шумный для governance V7.

Главная находка:

- за период `2026-05-22T15:00:00Z` и позже найдено **332 switch events**;
- **322** из них `autoswitch_failover`;
- Telegram sentinel за тот же период видел `blocked_egress=['1']` **303 раза**;
- Telegram sentinel запускал autoswitch apply **135 раз**;
- у отдельных пользователей до **8 switches/hour** и **10 switches/day**;
- основной loop pattern: `awg0 -> 1 -> vless -> 1 -> awg0/awg3`.

Это не соответствует Calm Routing / Stability Preservation. Anti-flap в итоге сработал и заморозил пользователей, но система сначала допустила заметную oscillation.

## What Was Changed

Live VPS:

- Nothing changed.
- No timers disabled.
- No autoswitch policy changed.
- No routing changed.
- No nftables changed.
- No user registry changed.
- No Trusted RU/Gosuslugi behavior changed.

Repository:

- Updated `tools/v7-runtime-contract-validate` default identity DB path from the stale path to the live canonical path:
  - old: `/opt/v7/identity/v7-identity.db`
  - new: `/opt/v7/admin/v7-identity.db`
- Added `V7_IDENTITY_DB_FILE` env override support in that validator.

Verification:

- `PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m py_compile tools/v7-runtime-contract-validate` passed.
- `tools/v7-runtime-contract-validate --allow-missing` now reports missing local DB at `/opt/v7/admin/v7-identity.db`, which matches live VPS.

## Objective 1 — Autoswitch Safety Stabilization

### Current Live Policy

`/etc/v7/policy.json`:

```json
{
  "switch": {
    "cooldown_seconds": 300,
    "autoswitch_max_planned_per_run": 3,
    "autoswitch_max_failover_per_run": 100,
    "autoswitch_enabled": true,
    "autoswitch_mode": "guarded"
  },
  "quality": {
    "min_avg_mbps": 15.0,
    "min_floor_mbps": 10.0,
    "min_stability": 0.45
  },
  "load": {
    "mode": "dynamic",
    "soft_limit": 1,
    "hard_limit": 2,
    "rebalance_max_moves_per_run": 1,
    "reserve_ratio": 0.15,
    "min_soft_limit": 5,
    "min_hard_limit": 10,
    "max_hard_limit": 80
  }
}
```

Systemd:

```text
v7-users-autoswitch.timer: OnUnitActiveSec=20s
v7-users-autoswitch.service: /usr/local/bin/v7-users-autoswitch --apply

v7-telegram-sentinel.timer: OnUnitActiveSec=4s
v7-telegram-sentinel.service: /usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1
```

### Failover Loop Facts

From `/opt/v7/events/switch-history.jsonl`, since `2026-05-22T15:00:00Z`:

```text
switches: 332
autoswitch_failover: 322
autoswitch_rollback: 8
autoswitch_rebalance: 2
```

Transitions:

```text
awg0 -> 1      58
1 -> vless     46
1 -> awg3      37
1 -> awg0      35
vless -> 1     34
awg3 -> 1      32
vless -> awg0  23
awg3 -> vless  21
vless -> awg3  20
```

Targets:

```text
1      124
vless   75
awg0    70
awg3    63
```

Sources:

```text
1      118
vless   77
awg0    74
awg3    63
```

Most affected users:

```text
10.0.0.3   25 switches
10.7.0.4   25
10.7.0.8   25
10.7.0.12  22
10.7.0.10  21
10.0.0.6   21
10.7.0.3   21
10.7.0.2   21
10.7.0.7   21
10.7.0.14  21
```

Burst minutes:

```text
2026-05-22T16:41  16 switches
2026-05-22T17:14  16
2026-05-22T17:35  16
2026-05-22T18:58  16
2026-05-22T15:28  15
2026-05-22T16:28  15
2026-05-22T20:08  14
2026-05-22T20:32  13
```

From `/opt/v7/egress/state/autoswitch-safety.json`:

```text
10.0.0.3: switches_1h=8, switches_24h=10
10.7.0.4: switches_1h=8, switches_24h=10
10.7.0.8: switches_1h=8, switches_24h=10
10.7.0.10: switches_1h=8, switches_24h=10
10.7.0.14: switches_1h=8, switches_24h=10
```

Egress incoming in the latest safety window:

```text
1:     incoming_1h=50
awg0:  incoming_1h=21
awg3:  incoming_1h=13
vless: incoming_1h=10
```

### Sentinel Interaction

From `/opt/v7/events/telegram-sentinel-20260522.jsonl`, since `15:00Z`:

```text
sentinel_events_since_15utc: 303
blocked_counts: {'1': 303}
autoswitch_started_events: 135
```

This is the clearest root-cause signal:

- Telegram sentinel repeatedly saw egress `1` as blocked/degraded for Telegram.
- Sentinel repeatedly invoked autoswitch apply.
- Egress `1` was also repeatedly selected as target by autoswitch due to strong general quality/speed score.
- Then `1` became a bad source again for Telegram-specific checks.
- Result: users oscillated between `1`, `vless`, `awg0`, `awg3`.

### Policy Loading

Policy file is present and loaded from `/etc/v7/policy.json`.

The issue is not missing policy fallback. The issue is the live policy permits aggressive failover:

- `autoswitch_max_failover_per_run=100`;
- sentinel can start apply frequently;
- users-autoswitch timer also runs apply every 20s;
- cooldown is 300s, but burst moves still happened because different targets and failover paths kept reopening opportunities.

### Service Matrix Influence

Service matrix currently reports:

```text
1: OK, Telegram DEGRADED
awg0: WARN, Telegram OK
awg3: WARN, Telegram OK
openvpn: WARN, Telegram OK
vless: WARN, Telegram OK
wireguard: WARN, Telegram OK
```

Important: `1` can be globally strong but Telegram-degraded. This creates a service-specific contradiction: `1` is attractive by speed/quality but not stable for Telegram.

### Load Influence

Load semantics are inconsistent:

- `summary.state` says `awg0_load_status=HARD_FULL` and `awg3_load_status=HARD_FULL` because static `soft_limit=1`, `hard_limit=2`.
- Autoswitch dynamic load considers `awg0` and `awg3` OK around `8/24`.

Load was probably not the primary trigger of the failover loop, but the conflicting load semantics confuse operator clarity.

### Reconnect Influence

No evidence that reconnect rotation was the primary cause. Switch history is dominated by:

```text
reason=autoswitch_failover
```

### Exact Root Cause

The loop is caused by a mismatch between:

1. **Telegram sentinel fast degradation signal** for egress `1`;
2. **autoswitch apply being callable from sentinel**;
3. **high general score of egress `1`** in quality/speed;
4. **high failover bound** (`100`);
5. **insufficient persistence/target dampening** for a service-specific failure;
6. **multiple apply sources**:
   - `v7-users-autoswitch.timer`;
   - `v7-telegram-sentinel.timer`.

Anti-flap eventually froze users, but only after a large amount of switching. That is not acceptable for production calmness.

### Bounded Stabilization Recommendations

Do not disable kill switch. Do not touch routing.

Recommended safe order:

1. **Stop sentinel from applying switches**
   - Change sentinel to signal-only:
     - systemd option: add `--no-autoswitch`; or
     - softer option: add `--dry-run-autoswitch`.
   - Keep `v7-users-autoswitch.timer` as the single apply authority.
   - Rationale: one apply loop is easier to reason about than two.

2. **Lower failover cap**
   - Current: `autoswitch_max_failover_per_run=100`.
   - Proposal: `3` for current 16 users.
   - Conservative alternative: `5`.
   - Never above 25 without capacity proof.

3. **Increase cooldown**
   - Current: `300s`.
   - Proposal: `900s`.
   - Conservative alternative: `600s`.

4. **Make Telegram-degraded target sticky-block stronger**
   - If an egress is Telegram-degraded, do not select it again as target for Telegram-required users until a stability window passes.
   - This should be parameter/config-level if existing code supports it; otherwise defer code change.

5. **Add operator incident on switching frequency**
   - If user has `switches_1h >= 3`, show incident.
   - If any egress has `incoming_1h >= 10`, show incident.

No live changes were applied because these are runtime-affecting and should be approved as a maintenance action.

## Objective 2 — Health Semantics Consistency

### Current Health Source Map

| Source | Current Role | Should Be |
|---|---|---|
| `users.registry` | user desired/current assignment | authoritative for assignment contract |
| `egress.registry` | enabled egress pool | authoritative for egress presence/config |
| `v7-state.json` | synthesized runtime state | observed/effective summary |
| `autoswitch-safety.json` | switch safety ledger | authoritative for autoswitch behavior risk |
| `telegram-sentinel.json` | fast Telegram signal | service-specific advisory/blocker with persistence |
| `service-matrix.json` | per-service checks | service-specific health, not global route truth |
| `egress-quality-summary.json` | speed/stability history | performance trend/supporting signal |
| `summary.state` | operator summary | should be derived, not independent authority |
| `egress-status.state` | status counters | supporting historical state |
| `trusted-ru-diagnostic.state` | sensitive RU diagnostics | separate route-class diagnostic; out of scope this sprint |

### Current Contradictions

1. **Service matrix vs sentinel**
   - Sentinel can say Telegram OK for several egress.
   - Service matrix can say WARN because unrelated AI services are HTTP_LIMITED.
   - Operator sees WARN even if core access is fine.

2. **Quality summary vs sentinel**
   - `openvpn` and new `wireguard` show Telegram OK in sentinel.
   - Quality summary shows `fail_rate ~0.9999`, making autoswitch mark them suspect.

3. **Static load vs dynamic load**
   - `summary.state`: `awg0`/`awg3` HARD_FULL due static `1/2` limits.
   - autoswitch dynamic load: `8/24` OK.

4. **Global quality vs service-specific quality**
   - egress `1` has strong speed/stability.
   - egress `1` repeatedly fails Telegram sentinel.
   - It is both attractive and unsafe depending on service context.

### Proposed Authority Hierarchy

Assignment/routing authority:

1. `users.registry`
2. per-user `.assign` files
3. `ip rule` / route tables
4. `v7-user-route-check`

Datapath safety authority:

1. kill switch nftables rules
2. `v7-killswitch-check`
3. `v7-provisioning-reconcile-check`

Egress eligibility authority:

1. `egress.registry`
2. explicit enabled/disabled/maintenance/quarantine flags
3. route class compatibility
4. service-specific blockers

Autoswitch behavior authority:

1. `autoswitch-safety.json`
2. policy file
3. selected moves from autoswitch planner
4. switch history

Operator health summary authority:

1. synthesized incident model
2. grouped service impact
3. current assignment/routing verification
4. supporting metrics hidden in drilldown

### Unified Operator Health Summary Proposal

For each egress:

```text
healthy
degraded
unstable
overloaded
blocked
quarantined
maintenance
unknown
```

Rules:

- `blocked`: required service hard-blocked or route verification fails.
- `unstable`: high switch churn, high fail rate, repeated sentinel degradation.
- `degraded`: service-specific WARN or below-floor quality, but still usable.
- `overloaded`: authoritative dynamic load says over threshold.
- `healthy`: no blockers, no severe service degradation, acceptable quality.
- `unknown`: missing fresh signals.

Do not let one HTTP_LIMITED AI service make the whole channel look globally bad if core internet access is OK.

## Objective 3 — Identity DB Path Contract Fix

### Live Reality

Real:

```text
/opt/v7/admin/v7-identity.db
```

Missing:

```text
/opt/v7/identity/v7-identity.db
```

Live DB contents:

```text
organizations 3
groups 1
identity_users 11
devices 20
allowed_users 6
connect_sessions 8
pending_profiles 3
provisioning_jobs 8
onboarding_attempts 41
```

### Dependency Map

Correct references:

- `admin/v7-admin-api`
- `tools/v7-identity-consistency-review`
- `docs/phase0/RUNTIME_INVENTORY.md`
- `docs/phase0/STATE_CONTRACTS.md`
- `V7_PROJECT_DOCUMENTATION.md`
- live admin UI/design references

Wrong/stale reference fixed:

- `tools/v7-runtime-contract-validate`

### Canonical Path

Canonical path should be:

```text
/opt/v7/admin/v7-identity.db
```

Rationale:

- live VPS uses it;
- admin service uses it;
- identity consistency review uses it;
- onboarding/profile delivery depend on it.

### Safe Compatibility Strategy

1. Keep live DB in place.
2. Use `V7_IDENTITY_DB_FILE` override in all tools.
3. Update validators to default to `/opt/v7/admin/v7-identity.db`.
4. Do not create a second DB under `/opt/v7/identity`.
5. If a future move is desired, use explicit migration with backup and symlink/compat plan.

## Objective 4 — Deployment Baseline Cleanup

### Current Deploy Structure

Runtime/config:

- `/usr/local/bin/v7-*`
- `/etc/v7/*`
- `/opt/v7/*`
- `/etc/systemd/system/v7-*`

Active production admin:

```text
/usr/local/bin/v7-admin-api
sha256=f7fbb4234fa1d9a4cf4ef92f4b52bf30d315a9f818a235b7073a18c8a9ffb5d3
```

No git checkout baseline found on VPS.

### Executable Map

`/usr/local/bin` classification:

```text
active v7-* commands: 145
backup/tmp v7-* executables: 201
```

Examples of active authoritative runtime files:

- `v7-admin-api`
- `v7-users-autoswitch`
- `v7-telegram-sentinel`
- `v7-killswitch-check`
- `v7-killswitch-enable`
- `v7-user-switch`
- `v7-user-route-check`
- `v7-provisioning-reconcile-check`
- `v7-service-matrix-test`
- `v7-egress-set-state`
- `v7-policy-*`
- `v7-direct-*`

Dangerous PATH clutter:

- `v7-admin-api.backup-*`
- `v7-admin-api.bak.*`
- `v7-users-autoswitch.backup.*`
- `v7-users-autoswitch.bak.*`
- many other `.bak` tool variants.

### Safe Deploy Baseline Model

Recommended model:

```text
/usr/local/bin/
  only current executable command names

/opt/v7/releases/<timestamp-or-git-sha>/
  immutable deployed files

/opt/v7/releases/current -> <release>

/opt/v7/backups/bin-archive/<date>/
  old executable backups, not in PATH

/opt/v7/deploy-manifest.json
  command name
  sha256
  source git sha
  deployed_at
  deployed_by
  rollback target
```

Do not move/delete backups in this sprint without explicit maintenance approval.

## Objective 5 — Operator Incident Visibility

### Current Gap

The system knows about instability, but the operator needs a calm incident summary:

- frequent switching;
- frozen users;
- dominant loop pattern;
- egress repeatedly becoming failed target/source;
- sentinel-triggered autoswitch starts.

### Proposed Compact Incidents

Incident 1:

```text
Autoswitch instability observed
Severity: high
Affected users: 16
Peak: 8 switches/hour, 10 switches/day
Dominant loop: awg0 -> 1 -> vless -> 1
Suggested action: reduce failover bounds; keep sentinel signal-only
```

Incident 2:

```text
Telegram-specific degradation on egress 1
Severity: medium/high
Signal: 303 sentinel blocked events since 15:00Z
Impact: repeated failover selection/source churn
Suggested action: mark egress 1 as Telegram-unstable until stable window passes
```

Incident 3:

```text
Health semantics conflict
Severity: medium
Signals: service matrix WARN, sentinel OK, quality fail_rate high, load summary conflict
Suggested action: use unified operator health summary
```

Do not show this as a metrics wall. Show summary first, drilldown second.

## Recommended Maintenance Action Set

These were **not applied**.

### Option A — Minimal Calming

1. Set sentinel to signal-only:

```text
v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

2. Keep core autoswitch timer active.
3. Lower failover cap:

```json
"autoswitch_max_failover_per_run": 3
```

4. Increase cooldown:

```json
"cooldown_seconds": 900
```

Expected effect:

- much less oscillation;
- no full autoswitch shutdown;
- Telegram signal still visible;
- only one apply authority remains.

### Option B — More Conservative

1. Sentinel stays as-is but dry-run only:

```text
--dry-run-autoswitch
```

2. Failover cap to `5`.
3. Cooldown to `600`.

Downside: sentinel can still run planner often and may write observation state depending on code path.

### Option C — Emergency Freeze

If user-visible instability is active:

- pause `v7-users-autoswitch.timer`;
- keep kill switch/routing untouched;
- manually inspect before re-enable.

This is not recommended unless instability is ongoing.

## Sprint 1 Final Verdict

V7 production runtime is working, but autoswitch is not calm enough.

Working:

- kill switch;
- route checks;
- state contracts;
- admin service;
- external command presence;
- identity DB at canonical live path.

Unsafe or unstable:

- autoswitch failover cap too high;
- sentinel can trigger apply too often;
- egress `1` Telegram degradation drives loop;
- health signals conflict;
- deploy baseline is file-based and cluttered.

First real stabilization should be:

1. make sentinel signal-only;
2. reduce failover cap;
3. increase cooldown;
4. add autoswitch instability incident summary;
5. align health semantics;
6. archive PATH backup executables later under maintenance.

