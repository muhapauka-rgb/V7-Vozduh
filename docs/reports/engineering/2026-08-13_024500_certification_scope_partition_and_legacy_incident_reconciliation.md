# Partition certification scope and reconcile legacy active incident

Date: 2026-08-13

## Result

`PASS`: the ordinary Service Failure consumer no longer treats a source that
contains only certification identities as an ordinary-user failover cohort.

The correction is channel-agnostic. It applies to every source because it is
derived only from the existing `users.registry` classification and the existing
Matrix/L3/OMP owners.

## Root cause

The Matrix source-scope contract previously represented all enabled identities
on a failed source as one denominator. The existing controlled-certification
pool already knew how to distinguish certification identities, but that fact
was not connected to the passive failure -> ordinary advisory consumer chain.

For the active legacy incident, current production truth was:

```
affected = 12
protected = 1  (existing verified packet-bound Outcome)
ordinary unresolved = 0
certification-only remainder = 11
```

Before the repair, the 11 controlled identities appeared as unresolved ordinary
users and repeatedly selected `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.
There was no lawful ordinary action to take, so the bounded executor correctly
stopped with no actionable recommendation, but the consumer loop was misleading.

## Implemented existing-owner extension

1. `tools/v7-service-matrix-test` v2 source scope now records compact,
   no-raw-list partitions:
   - `ordinary_production_scope`;
   - `controlled_certification_scope`;
   - `total_assigned_scope`;
   - `scope_classification`.
   Compatibility `affected_scope_*` fields are the ordinary production
   denominator, the only scope admitted to ordinary failover.
2. `tools/v7-service-matrix-refresh-all` preserves certification-only failures
   for passive reconciliation, while preventing them from being admitted to
   ordinary action.
3. `tools/v7-users-autoswitch` consumes the partition in the existing L3
   incident projection and advisory.
4. A bounded legacy reconciliation preserves proven packet Outcome lineage and
   classifies the remaining live certification identities as
   `explicitly_excluded_or_recovered_scope`, not as protected or disappeared.

No new owner, timer, scheduler, queue, registry, Planner, Authority contract,
or runtime execution path was created.

## Production verification

Safe deploy manifests were strictly limited to the following approved owners:

| Commit | Deploy ID | Runtime files |
| --- | --- | --- |
| `6addb25c` | `deploy-z8-14-Updatesystem-6addb25-20260813T023315` | `tools/v7-service-matrix-test`, `tools/v7-service-matrix-refresh-all`, `tools/v7-users-autoswitch` |
| `fd5ee65d` | `deploy-z8-14-Updatesystem-fd5ee65-20260813T023816` | `tools/v7-users-autoswitch` |
| `75aef372` | `deploy-z8-14-Updatesystem-75aef37-20260813T024223` | `tools/v7-users-autoswitch` |

The next ordinary `v7-autoswitch-planner.timer` cycle, not a manual Matrix or
autoswitch invocation, produced the final compact owner-backed record:

```
incident_state = INTENT_CLOSED
attempt_terminal = CURRENT_SOURCE_SCOPE_EMPTY_NO_ACTION
affected_scope_count = 12
protected_scope_count = 1
unresolved_scope_count = 0
explicitly_excluded_or_recovered_scope_count = 11
scope_classification = CERTIFICATION_ONLY
scope_membership_law = LEGACY_ALL_ASSIGNED_SCOPE_RECONCILED_TO_CONTROLLED_CERTIFICATION_EXCLUSION
```

The invariant `affected = protected + unresolved + excluded` therefore holds.
The existing Matrix retains the channel failure as passive diagnostic evidence;
the repair does not call it recovery and does not erase historical events.

## Forbidden-effect proof

All deploys and the confirming ordinary production cycle reported:

- Candidate/Packet/lease created: `false`;
- Runtime apply/routing mutation/rollback apply: `false`;
- users moved: `0`;
- Authority expansion: `false`;
- Production Maturity change: `false`.

## Tests and truth

Focused affected suites passed:

```
tests.unit.test_service_failure_automation_evolution
tests.unit.test_service_failure_episode
tests.unit.test_operator_induced_passive_capture
```

They cover ordinary/certification partitioning, certification-only fast-consumer
reconciliation, legacy all-assigned reconciliation, and preservation of an
already verified Outcome while excluding the remaining controlled identities.

## Exact successor

`CT-M0F` remains a controlled-validation latency Mission. A normal production
failover requires a fresh failed source with a non-zero ordinary production
scope. A certification-only source is not a substitute and must be consumed
only through the existing controlled-certification owner and its active,
independently authorized contract.
