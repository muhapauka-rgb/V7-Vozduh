# Runtime Commit Revalidation Audit

Status: COMPLETE
Language: Russian
Task: audit state-change protection between decision time and apply time
Runtime mutation: NO
Apply executed: NO
Users moved: NO
Code changed: NO
Backlog changed: NO
Canonical owners changed: NO

## Summary

Аудит проверил, выполняет ли V7 финальную runtime eligibility проверку непосредственно перед необратимым commit point.

Вывод:

```text
Final eligibility recheck: PARTIAL
```

V7 уже выполняет сильную финальную проверку идентичности, authority envelope, restore-barrier clearance, selected move hash, user/source/target identity, snapshot/source bundle и atomic execution envelope.

Но единая runtime eligibility arbitration, которая прямо перед commit заново решает:

```text
target health + freshness + authority + blast radius + rollback + anti-flap + verification + learning
-> EXECUTE or STOP_SAFE
```

еще не завершена. Она уже запланирована существующим backlog item `A6`.

## Action Performed

Проверена цепочка:

```text
Planner
-> Packet
-> Approval
-> Execution Lease
-> Snapshot Gate
-> Runtime Eligibility
-> Restore Barrier
-> Apply
-> Verify
-> Rollback
-> Outcome Closure
```

Проверены владельцы:

- `tools/v7-users-autoswitch`
- `admin_core/operator_execution.py`
- `admin_core/operator_execution_pipeline.py`
- `admin_core/autonomy_trust_acceleration.py`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`

## Commit Point

Истинный commit point находится в:

```text
tools/v7-users-autoswitch
AutoswitchPlanner.apply()
-> _run_switch()
-> subprocess.run(["v7-user-switch", ip, egress])
```

Необратимая операция:

```text
user route/channel assignment mutation
```

После вызова `v7-user-switch` решение уже нельзя изменить как pre-commit decision. Дальше допустимы только:

- verification;
- rollback;
- recovery;
- outcome closure;
- learning.

## Existing Pre-Commit Protections

Перед commit point уже существуют следующие защиты:

1. `approved_plan_lock_validation`

Проверяет:

- lock schema;
- selected moves exist;
- selected move count;
- selected move hash;
- snapshot bundle hash;
- allowed users;
- allowed targets;
- requested target scope;
- restore-barrier budget;
- lease/clearance expiry;
- user exists and enabled;
- user current source still matches approved source;
- target exists;
- target is not `disabled` or `down` in `egress.registry`;
- executor may not reselect, replace users, or replace targets.

2. Restore barrier generation check

Проверяет:

- generation token;
- expiry;
- planner generation;
- approved selected move hash;
- selected move count;
- atomic execution envelope;
- source bundle hash.

3. Intelligence snapshot gate

Проверяет required intelligence snapshot families and source hashes.

4. Atomic execution envelope validation inside `apply()`

Непосредственно перед `_run_switch()` проверяет:

- selected move hash;
- selected move count;
- runtime snapshot hash;
- source bundle hash;
- current source hashes from disk.

5. Source-bundle stability lease

Может разрешить только семантически стабильный drift, если strict sources не изменились and approved decision signature remains stable.

## What Is Revalidated

Currently revalidated before commit:

| Revalidated item | Status |
| --- | --- |
| Packet / selected move identity | YES |
| User identity | YES |
| User current source channel | YES |
| Target identity | YES |
| Target exists in registry | YES |
| Target not disabled/down in registry | YES |
| Selected move hash | YES |
| Selected move count | YES |
| Restore barrier clearance | YES |
| Generation / expiry | YES |
| Atomic envelope | YES |
| Strict source hashes: users, egress, service preferences | YES |
| Snapshot/source drift | PARTIAL |
| Fresh target health from service/quality evidence | PARTIAL |
| Unified runtime eligibility arbitration | NOT YET; backlog `A6` |

## Real-World Scenario

Scenario:

```text
t0 channel healthy
t1 planner selects channel
t2 operator approves packet
t3 destination channel fails
t4 runtime starts apply
```

Current behavior depends on where the failure is reflected.

### Case 1: Target is marked disabled/down in egress registry

Runtime stops before commit.

Reason:

```text
approved_plan_lock_target_disabled
```

or source/atomic envelope mismatch if strict source hash changed.

Production quality:

```text
GOOD
```

### Case 2: Target failure is visible only in service matrix / quality summary

Runtime may detect source/snapshot drift, but current source-bundle lease logic may allow service/quality drift if the approved decision signature is still stable.

In that case, Runtime can continue to `_run_switch()` using the approved locked move, then rely on verification and rollback/no-rollback path.

Production quality:

```text
PARTIAL
```

This is not a packet identity defect. It is the unfinished final eligibility arbitration layer covered by `A6`.

### Case 3: Target failure is not visible in any current source before t4

Runtime cannot know. It proceeds to commit and relies on verification / rollback / recovery.

Production quality:

```text
EXPECTED_LIMIT
```

No control plane can revalidate facts it has not observed.

## Commercial Comparison

Mature production control planes generally follow:

```text
Revalidate until commit.
After commit, do not mutate the decision.
Verify, rollback, recover, reconcile, or learn.
```

Comparable pattern:

- Kubernetes: desired/current state is rechecked by controllers; after mutation, reconciliation observes and corrects.
- Cloudflare / traffic control planes: health/readiness is checked before traffic movement; after traffic changes, health checks and rollback/failback logic handle outcome.
- AWS-style control planes: precondition checks happen before mutating state; after commit, systems rely on observed state, rollback/retry/reconciliation.

V7 matches the philosophy at the architecture level and for identity/source/restore safety.

V7 is still partial for health-aware final eligibility because the current apply path does not yet collapse all gate outputs into one final:

```text
EXECUTE
or
STOP_SAFE
```

immediately before `v7-user-switch`.

## Existing Owner

Primary existing owner:

```text
tools/v7-users-autoswitch
```

Supporting existing owners:

```text
admin_core/operator_execution.py
admin_core/autonomy_trust_acceleration.py
tools/v7-autonomy-trust-evidence-inventory
```

No new owner is required.

## Existing Backlog Mapping

Existing backlog item:

```text
A6
Implement action-class runtime eligibility arbitration using freshness, authority,
blast radius, rollback, anti-flap, verification, and learning gates.
```

Supporting backlog items:

```text
B18
Extend owner-issued version/lease pattern where available.

B17
Preserve stale-read reporting while blocking mutation.

C1
Record fail-open/fail-closed behavior per action class.

C6
Decide bounded stale allowance by action class.
```

No new backlog item is required.

## Architecture Match

Runtime Model already intends this behavior:

```text
Runtime consumes prepared decisions.
Runtime executes certified decisions.
Runtime either executes or stops safely.
Runtime verifies freshness, safety, rollback/no-rollback readiness,
verification readiness, authority, and policy before execution.
```

OMP also intends this behavior:

```text
Runtime must generate or consume a fresh packet immediately before execution
and verify class, authority, policy, subject/target, freshness, safety,
rollback/no-rollback readiness, verification readiness, and blast radius.
```

Implementation match:

```text
PARTIAL
```

Reason:

The apply owner has strong identity/source/restore pre-commit checks, but final runtime eligibility arbitration is not yet implemented as one authoritative gate before commit.

## Risk Assessment

Risk:

```text
MEDIUM before A6
LOW after A6 if implemented as documented
```

Why not high:

- runtime automation is disabled;
- exact packet approval is still required;
- restore barrier exists;
- selected move identity is preserved;
- target disabled/down in registry blocks pre-commit;
- atomic envelope detects hard source changes;
- verification and rollback/no-rollback handling exist.

Why not low yet:

- target health degradation in service/quality evidence may be treated as allowed semantic drift;
- no single final runtime eligibility decision currently owns all gates immediately before `_run_switch()`;
- A6 is still `TODO`.

## Capability Progress

| Capability | Progress |
| --- | ---: |
| Runtime Eligibility | `28.6%` |
| Production Autonomy | `0.0%` |
| Movement Protection | `35.7%` |
| Authority Evolution | `40.0%` |
| Production Readiness | `24.0%` |

## Backlog Progress

| Scope | Progress |
| --- | ---: |
| Tier A | `3 / 6` = `50.0%` |
| Overall actionable backlog | `3 / 34` = `8.8%` |
| Current item | `A4` remains blocked by real-world evidence |
| Relevant future item | `A6` owns final runtime eligibility arbitration |

## Production Maturity

| Dimension | Current |
| --- | ---: |
| Engineering Maturity | `100.0%` |
| Production Maturity | `24.0%` |
| Production remaining | `76.0%` |
| Current autonomy tier | `TIER_1_GOVERNED` |

## Engineering Conclusions

1. The architecture already intended production-grade commit philosophy.
2. The implementation partially matches it.
3. The exact gap is not packet approval, lease identity, or restore barrier.
4. The exact gap is final health-aware runtime eligibility arbitration immediately before commit.
5. Existing owner can be extended.
6. Need New Owner: FALSE.
7. Need New Backlog Item: FALSE.
8. Existing backlog mapping: `A6`, supported by `B17`, `B18`, `C1`, `C6`.

## Minimal Recommendation

Do not implement anything during this audit.

When OMP reaches `A6`, implement through existing owners only:

```text
Final Runtime Eligibility Gate
immediately before _run_switch()
```

It must consume current gate outputs and produce exactly one result:

```text
EXECUTE
or
STOP_SAFE
```

It must revalidate:

- target health/readiness;
- freshness;
- authority;
- policy;
- blast radius;
- rollback/no-rollback readiness;
- anti-flap;
- verification readiness;
- selected move identity;
- source/target/user identity.

Until then, A4 remains current OMP item and A6 remains the mapped implementation item for this audit finding.

## Re-audit Rule

Do not re-audit this path unless:

- `A6` is implemented;
- `tools/v7-users-autoswitch.apply()` changes materially;
- execution lease or restore barrier semantics change materially;
- production evidence shows stale target movement;
- operator explicitly requests re-audit.
