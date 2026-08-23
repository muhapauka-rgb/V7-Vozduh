# VLESS continuing-failure scope binding: ownership decision and live proof

Date: 2026-08-23 (MSK)  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Logical block: `VLESS_CONTINUING_FAILURE_SCOPE_BINDING_OWNERSHIP`  
Result: `MODEL_B_ADOPTED_AND_READ_ONLY_SELECTION_PROVEN`

## Short result

A continuing VLESS failure can now be safely bound to the **current**
certification-only users without rewriting Matrix state. Matrix remains the
owner of the failure; `users.registry` remains the owner of current client
assignment. The real read-only VLESS selection is ready for exactly one
synthetic identity, `10.7.0.89`, from `vless` to the existing admitted target
`awg3`. No Packet, lease, route, client assignment or user movement was
created.

## Current blocker before this block

The current VLESS Matrix state was fresh and failed, and its latest
certification-only failure event was fresh, but the event's compact controlled
scope fingerprint no longer matched the current `users.registry` fingerprint.
The event was an immutable observation made before the certification membership
changed. The selector treated that historical snapshot as if it owned current
membership and returned `STOP_SAFE`.

A second live-only condition was discovered during verification: a real failed
source with 11 certification users carried an older prepared-condition marker.
The selector applied the prepared-condition one-user *source* limit before it
considered the fresh Matrix failure, even though the actual action remains one
user. This blocked the real failure before the binding could run.

## Facts and owners

| Fact | Current owner | Producer | Consumer | Canonical or snapshot? |
| --- | --- | --- | --- | --- |
| Egress health and failed services | Matrix | `tools/v7-service-matrix-test.update_matrix` | policy, controlled selector, Planner | canonical current observation |
| Failure episode/event | Matrix event ledger | `tools/v7-service-matrix-test.update_matrix` | passive consumer, controlled selector | immutable observation/lineage |
| Matrix generation/freshness | Matrix state and event | same Matrix owner | selector and downstream gates | current observation plus immutable receipt |
| User assignment | `users.registry` | existing user/route assignment owner | selector, Packet pipeline | canonical current membership |
| Ordinary affected scope | existing L3/current-scope owner | passive/L3 lifecycle | ordinary Planner/executor | canonical ordinary lifecycle projection |
| Certification scope | `users.registry` through existing controlled selector | existing registry owner | controlled selector | fresh in-memory binding, not persisted here |
| Scope fingerprint in Matrix event | Matrix event | Matrix source-scope snapshot | lineage/audit consumers | immutable snapshot only |
| Current controlled-scope fingerprint | selector reading `users.registry` | existing registry owner | Candidate/Packet/lease path | fresh in-memory binding |
| Exact selected identity | controlled selector | `tools/v7-users-autoswitch` | existing Candidate/Packet/lease pipeline | read-only selection; later frozen by Packet/lease |
| Target selection | existing availability-first target diagnostic | controlled target owner | controlled selector | current read-only admission |
| Execution identity lock | existing Packet/lease/restore-barrier owners | governed execution pipeline | apply/verification | canonical execution fence |

The durable boundary is also consistent with
`docs/reference/V7_MASTER_PROJECT_HANDOFF.md`: Matrix owns current health and
failure; registry/assignment owns durable current identity; Packet and lease
own the exact moment-of-execution fence.

## Neutral model comparison

### Model A — Matrix event owns and refreshes current affected scope

**Meaning.** Matrix would treat its event scope snapshot as the current client
scope and would need to re-emit/rewrite an event whenever controlled membership
changed.

**Result. Rejected.**

- It couples user assignment changes to a health-event writer.
- It makes append-only failure evidence behave as a mutable client registry.
- A late/duplicated event can create churn without a new health observation.
- It duplicates the ownership that already belongs to `users.registry`.
- It would make a membership update a prerequisite for a safe re-check even
  when the Matrix failure itself is still fresh.

No Model-A change was made to the Matrix writer.

### Model B — Matrix owns episode; current scope is bound from registry

**Meaning.** A fresh Matrix failure event identifies a continuing source
episode. The existing controlled selector reads the current source membership
from `users.registry`; a later Candidate/Packet/lease freezes the one selected
identity immediately before apply.

**Result. Adopted.**

- Preserves one health/event owner and one user-assignment owner.
- Does not make historical scope fingerprints mutable truth.
- Requires fresh Matrix state, a fresh capture-only event, certification-only
classification, zero ordinary users, a current failed correlated service and
one exact live membership binding.
- Allows safe membership changes during a continuing incident without moving
any client merely to update evidence.
- Leaves the ordinary L3/passive route and its accounting unchanged.

### Model C — hybrid/alternative owner

**Meaning.** Add a new scope watcher, registry, event stream or separate
binding state, or let a Matrix refresh become a user-scope authority.

**Result. Rejected.**

It would add a parallel source of truth and an additional failure/consistency
surface. The existing Matrix, registry, selector and Packet/lease owners cover
the required boundary once Model B is applied.

## Decision and failure-scope law

Decision: `MODEL_B_CURRENT_REGISTRY_SCOPE_ON_ACTIVE_MATRIX_EPISODE`.

For a certification-only continuing source failure:

```text
fresh Matrix says source is still failed
  + fresh capture-only Matrix event for the source
  + event still correlates to at least one currently failed service
  + source is controlled and has zero ordinary users
  + fresh users.registry membership is non-empty
  -> existing selector may choose one exact certification identity
  -> existing Candidate -> Packet -> lease later freezes identity/source/target
```

Any stale Matrix row, stale event, recovered source, missing correlation,
ordinary user, empty scope, uncontrolled source, changed target/policy/capacity
or later Packet/lease mismatch remains `STOP_SAFE`.

The event's old scope fingerprint is retained as a snapshot for lineage, but
is explicitly not a live membership lock. A changed event snapshot therefore
does not authorize action; it also no longer incorrectly blocks a separately
fresh registry binding.

## Minimal implementation

Changed existing owner only: `tools/v7-users-autoswitch`.

1. `ct_m0f_certification_only_matrix_failure_binding_projection` now binds
   fresh `users.registry` scope to the active Matrix episode.
2. It validates the Matrix event through the failed services it correlates,
   rather than requiring every currently failed service to carry one identical
   historical service-level incident identifier.
3. It exposes snapshot-versus-current scope status for diagnosis but stores no
   raw identities and creates no durable registry/event.
4. A real Matrix failure now takes precedence over an old prepared-condition
   marker. The action limit remains exactly one selected certification identity;
   the fix only prevents the marker from falsely requiring the whole existing
   11-user controlled source to already contain one user.
5. `docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md` now
   records the Model-B ownership law under M10.

Commits and production-safe deploys:

- `b8cbc735` — current-registry scope binding;
- `be88abd6` — real Matrix failure precedence over prepared-condition marker;
- `f1bb43c4` — live correlated-service event binding;
- production deploy `deploy-z8-14-Updatesystem-f1bb43c-20260823T101307`;
- independent GitHub and runtime truth checks: `PASS`.

## Regression and Polygon evidence

| Required case | Evidence | Result |
| --- | --- | --- |
| 1. unchanged scope | focused binding test | pass |
| 2. one certification user removed | `test_ct_m0f_certification_binding_uses_current_registry_not_event_snapshot` | pass |
| 3. certification user added | same focused test | pass |
| 4. scope empty | focused fail-closed variant | `STOP_SAFE` |
| 5. ordinary user appears | focused fail-closed variant | `STOP_SAFE` |
| 6. Matrix/event stale | focused fail-closed variants | `STOP_SAFE` |
| 7. source recovered | focused fail-closed variant | `STOP_SAFE` |
| 8. repeated unchanged checks | Matrix revalidation/exact-once regression | pass; no new binding owner |
| 9. ordinary path unchanged | ordinary passive and current-scope regressions | pass |
| 10. current identity only | selector test, including active prepared marker and failed source | pass |
| 11. Packet/lease identity fence | existing `admin_core/operator_execution.py` exact user/source/target consumption contract inspected; no bypass added | retained |
| 12. real VLESS selection | live read-only command below | pass |

Focused code tests: 11/11 passed.  
Polygon tests: 11/11 passed, including stale fail-closed, scope isolation,
short/full fallback and 7/50/100/1000 scale-contract scenarios. Local Polygon
uses a temporary loopback server only; it did not touch production.

## Real VLESS runtime observation

Production read-only observation after deploy:

```text
Matrix source: vless
Matrix state: fresh; 13 of 14 services failed
Current controlled source scope: 11 certification users, 0 ordinary users
Current event correlated failed services: 6
Event scope snapshot equals current scope: false (expected historical snapshot)
Selection: READY
Selected exact certification identity: 10.7.0.89
Selected target: awg3
Target admission: existing availability-first one-user admission
```

The selector returned:

```text
CT_M0F_STANDING_CONTROLLED_FAILURE_READY
EXECUTE_CONTROLLED_FAILURE_CUTOVER
CERTIFICATION_ONLY_MATRIX_FAILURE_BINDING_READY
CURRENT_REGISTRY_SCOPE_ON_ACTIVE_MATRIX_EPISODE
```

Its effect counters remained all zero:

```text
candidate_created=false
packet_created=false
lease_created=false
routing_mutation=false
user_movement=0
policy_write=false
authority_expansion=false
```

The temporary target-diagnostic file was removed immediately after the
read-only check.

## Production effect and limitations

This block changes only how a safe controlled selection is *read and bound*.
It does not alter Matrix cadence, timeout, FAST, routing policy, automatic
switching, ordinary user assignment, target capacity policy or authority.
No user was moved. `awg3` was admitted by its existing policy; no special
target or target-owner was created.

The selection is intentionally not a completed recovery. It is a proven
predecessor for the existing governed execution chain. Fresh Candidate, Packet,
lease, restore barrier, live rechecks, one-use consumption, apply,
verification, rollback/containment and outcome evidence are still required
before any movement. A later change in Matrix, registry, target, capacity,
policy or authority invalidates the selection and must recompute it.

## Exact next step

The ownership block is complete. The next block in the T0–T11 latency plan is
`ONE_USER_GOVERNED_PACKET_LEASE_PRE_APPLY_REVALIDATION`:

1. reuse this existing ready selection;
2. prove the existing caller can materialize a fresh one-user Candidate,
   Packet and lease from it without bypassing the binding;
3. recheck Matrix, source assignment, target, capacity and authority immediately
   before apply;
4. execute only if every existing live gate admits it; otherwise retain the
   exact `STOP_SAFE` receipt;
5. verify route and traffic recovery, then record T0–T11 timing and rollback
   evidence.

No new owner, Matrix writer, Runtime, Planner, queue, registry or authority is
needed for that step.
