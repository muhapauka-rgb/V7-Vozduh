Mission ID: `V7_RECOVERY_GLOBAL_ROUTE_LOCK_BOUNDARY_AND_APPLY_CONCURRENCY_AUDIT`
Run Nonce: `V7_GLOBAL_ROUTE_LOCK_AUDIT_20260902_01`

# V7 Recovery global route-lock boundary and Apply concurrency

## Current frontier and method

The CPS/OMP-derived frontier remains
`RECOVERY_GOVERNED_APPLY_VERIFICATION_CURRENT_PATH_AUDIT`; only normal V7
Runtime may produce a recovery action. This audit read CPS, OMP, the route
writer, Core-primary, governed executor, execution-control owner and their
tests. No customer, route, registry, Candidate, Packet, Lease, Barrier,
Matrix, policy, timer or Runtime state was changed.

Local source: `8d1190835e268a5419abbf1f68373ff98f6c281f`. Remote branch
verification could not complete because this environment could not resolve
`github.com`. Production Runtime hashes were not credited because read-only
production access is unavailable here. Neither is evidence of a Runtime
change.

## Exact locks and protected state

| Item | Current implementation fact |
| --- | --- |
| Route-lock ID | `${V7_USERS_LOCK:-/tmp/v7-users.lock}` |
| Route-lock owner | sole route writer: `tools/runtime-support/v7-user-switch` |
| Acquire/release | outer `flock -E 75 -w ${V7_LOCK_WAIT:-20}` re-executes the whole writer; release happens only at child exit |
| Mutable invariant | coherent per-user policy route/rule, `user-<ip>.assign`, canonical `users.registry`, and Core-primary kernel projection |
| Core-primary lock | `v7-routing-sync` takes `${V7_ROUTING_LOCK:-/tmp/v7-routing.lock}` around its entire request |
| Operation-control | a separate Packet-bound Authority window, opened before Apply and finalized during terminal finalization |
| Operation concurrency | standing governed contract requires `max_concurrent_transactions == 1` |

Route lock and operation-control are distinct. The route lock protects
mutation. The operation-control window protects the exact authorized
transaction while verification and terminal handling complete.

## What executes inside the route lock

| Work | Inside | Must stay inside now | Scope / reason |
| --- | --- | --- | --- |
| Input and control-file revalidation | Yes | Yes | Per-operation closed, matching execution-control record; not a fresh Matrix reread. |
| Default route and source policy-rule writes | Yes | Yes | Per-user paired kernel mutation. |
| Assignment-file and registry writes | Yes | Yes | Per-user durable assignment plus atomic canonical registry rewrite. |
| Rollback preimage | Yes | Yes until full Core-primary success | Normal mode copies whole registry and this assignment before mutation. |
| Core-primary status call | Yes | Currently | Owner availability check. |
| Normal Core-primary apply | Yes | Yes under current preimage model | Rebuilds all users/classes, recreates nft table, writes class routes/rules and retires legacy rules. |
| Exact Core-primary delta | Not for ordinary one-user writer call | N/A | Existing primitive is limited to exact operator rebind or legal 2–4 member cohort. |
| Audit/switch log | Yes | No shared mutable invariant found | Small outcome/history emission included by whole-script lock. |
| Writer route observation and assignment read | Yes | Current post-Apply proof | Read-only per-user confirmation. |
| Governed route verification | No | No | Invoked only after writer returns. |
| Required-service probes and S11 | No | No | Invoked after writer returns. |
| Passive outcome, learning, history | No on persistent ordinary hot path | No | Existing finalizer defers it after required-service S11. |

The answer is neither “mutation only” nor “S11 under lock”. The lock covers
mutation, registry work, full Core-primary, small audit work and local
post-Apply observation. Required-service verification and S11 are already
outside it.

## Timing surface

Existing monotonic writer markers permit:

```
LOCK_WAIT_MS             = LOCK_STARTED -> ENTERED
LOCK_HELD_MS             = ENTERED -> POST_APPLY_OBSERVATION_COMPLETED
MUTATION+CONTROL_MS      = CONTROL_VALIDATED -> KERNEL_MUTATION_COMPLETED
ASSIGNMENT_WRITE_MS      = KERNEL_MUTATION_COMPLETED -> ASSIGNMENT_COMMITTED
REGISTRY_WRITE_MS        = ASSIGNMENT_COMMITTED -> REGISTRY_COMMITTED
CORE_PRIMARY+AUDIT_MS    = REGISTRY_COMMITTED -> AUDIT_COMPLETED
POST_WRITER_OBSERVE_MS   = AUDIT_COMPLETED -> POST_APPLY_OBSERVATION_COMPLETED
```

`CORE_PRIMARY+AUDIT_MS` is combined: the current receipt does not expose
separate full/Core-delta and audit timing. No production timing was invented
from that gap. Historical baselines stay historical: one member Apply plus
verification was about 5.080 s; three members about 16.035 s.

## Core-primary, amplification and rollback

| Current legal path | Writer calls | Route/assignment/registry writes | Core-primary |
| --- | ---: | ---: | --- |
| One ordinary governed recovery | 1 | 1 / 1 / 1 | 1 full `--core-primary-apply` |
| Legal 2–4 member, one-target emergency cohort | N staging calls | N / N / N | 1 existing bounded exact cohort commit, no stage-writer full rebuild |
| Generic multi-target bounded cohort | N | N / N / N | Current per-member governed path; shared delta is not assumed |

Normal automatic one-user recovery has a `GLOBAL_REBUILD_RESIDUAL`. Its
existing delta cannot be silently reused: it is explicitly limited to a
bound 2–4-member cohort or an explicit operator rebind. Expanding it changes
scope and rollback semantics.

Rollback prevents blind lock narrowing. Before normal full Core-primary
success, the writer has a whole-registry preimage and restores it with another
full rebuild on Core-primary failure. If another writer committed meanwhile,
that restore could overwrite the later assignment. After success the preimage
is deleted before writer exit. A later service/S11 failure uses a fresh
rollback writer against current canonical state. Therefore service verification
does not need the route lock, but it remains inside the one-at-a-time
operation-control window.

## Polygon and concurrency evidence

Focused existing owner-level tests passed:

```
tests.unit.test_v7_user_switch                         20 PASS
tests.unit.test_v5_3_n9_full_scale_tournament            6 PASS
total                                                   26 PASS
```

The existing 10/50/100 Polygon fixture again proves independent
**preparation only**, with no starvation. Its own contract excludes
`v7-user-switch`, Core-primary, kernel mutation and verification, so it cannot
credit Apply concurrency.

The local environment lacks the Linux `flock` executable used by the deployed
writer wrapper and cannot read live Runtime. A mock lock was not promoted to a
production conclusion. The honest result is:

```
10-source Apply:  FIDELITY_INSUFFICIENT_WITH_EXACT_REASON
50-source Apply:  FIDELITY_INSUFFICIENT_WITH_EXACT_REASON
100-source Apply: FIDELITY_INSUFFICIENT_WITH_EXACT_REASON
```

Static current-code consequences are exact:

* source 10 can wait behind nine whole current writer critical sections, not
  just nine `ip route replace` calls;
* same-user duplication is serialized/fail-closed by one-operation control
  and the exact Packet binding; the writer is not a second duplicate arbiter;
* disjoint preparation progresses, but disjoint ordinary Apply cannot overlap
  because `max_concurrent_transactions=1`; and
* a waiting writer revalidates immutable execution control, not a freshly
  rebuilt Matrix/Planner decision. Any future multi-operation admission needs
  an existing-owner final freshness proof before queued commit.

## Decision and next frontier

`CURRENT_DATA_PLANE_SERIALIZATION_BOUNDARY` is proven. The largest residual
is `GLOBAL_CORE_PRIMARY_REBUILD` coupled with intentional single-operation
control. Required-service probes, S11, learning and passive history are not
inside the global route lock.

No P0/P1 repair was deployed. An earlier unlock before full Core-primary
resolution would violate the current global-preimage rollback invariant. A
worker pool, new queue or lock manager is neither needed nor allowed. Moving
only audit/read-only observation cannot produce ordinary Apply concurrency
while operation control remains singular and would first require proof that a
post-mutation writer failure compensates correctly.

| Measure | Before | After |
| --- | --- | --- |
| Runtime owners/writers/locks | existing single writer | unchanged |
| Full rebuilds, ordinary one-user path | 1 | unchanged |
| Service verification under route lock | 0 | 0 |
| Independent ordinary Apply transactions admitted | 1 | 1 |
| 10/50/100 preparation starvation | 0 | 0 |
| 10/50/100 Apply fairness proof | absent | explicitly bounded; not fabricated |

Result: `COMPLEXITY_NEUTRAL_WITH_PROVEN_SAFETY_BOUNDARY` and
`RECOVERY_GLOBAL_ROUTE_SERIALIZATION_BOUNDARY_PROVEN`.

The next smallest safe frontier is a separate existing-routing-core decision:
prove whether the existing exact Core-primary delta can gain an
ordinary-recovery scope with exact per-member rollback, then decide whether
operation-control concurrency can be broadened. First it needs a
Linux/production-equivalent owner fixture that records lock acquire/release,
full-vs-delta timing, final generation freshness and A-after-B rollback.
Until then retain current serial Apply and normal Runtime-owned recovery.
