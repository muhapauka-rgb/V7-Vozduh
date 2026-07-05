# Canonical Truth Proof

Status: `COMPLETE`
Mode: `READ_ONLY_FORMAL_PROOF`
Runtime modified: `NO`
Planner modified: `NO`
Architecture modified: `NO`
Canonical documents modified: `NO`

## Summary

The single canonical truth that legally authorizes the first L3 emergency failover execution is not `Planner Selected Move`, not `CONFIRMED_L3_WAKE`, not `Incident Confirmed`, not `Authority Exists`, not `Packet Valid`, and not `Restore Barrier Valid` alone.

The canonical truth is the composite same-subject `EXECUTION_READY` truth:

```text
same assigned user
+ same failed current channel
+ failed required services on that current channel
+ safe target
+ fresh evidence
+ L3 authority
+ valid identity/selected move
+ valid restore barrier
+ rollback ready
+ verification ready
+ blast/budget/policy/movement gates pass
= one legal L3 execution may occur
```

This truth is canonical because L3 defines mandatory entry/readiness/execution gates, Autonomous Runtime names the permission state as `EXECUTION_READY`, Runtime defines the live execution plane, Decision Model defines `FAILOVER` only as vocabulary, and Policy 004 states that permission alone is not operational safety.

## Truth Inventory

| Truth | Type | Producer | Owner | Canonical source | Lifetime / freshness | Consumer |
| --- | --- | --- | --- | --- | --- | --- |
| User assigned to source channel | base fact | user registry / assignment state | user/assignment owners | Canonical Reference, SYSTEM_MAP | while assignment generation remains current | Planner, Runtime |
| Current channel failed | base/observed fact | service evidence / hard failure evidence | Policy 001 / service evidence owners | L3 Entry Conditions, Runtime observation plane | inside certified freshness window | Planner, Runtime, Incident |
| Required services failed on current channel | base/observed fact | service matrix / service suitability | service matrix / policy owners | L3 Entry Conditions, Canonical Reference Service Matrix | inside certified freshness window | Planner, Runtime |
| Users affected | derived fact | planner/user assignment owners | planner/autoswitch owners | L3 Entry Conditions | while user/source/failure evidence match | Planner, Incident, Runtime |
| Safe target exists | derived fact | planner/autoswitch | planner/autoswitch owners | L3 Entry Conditions, Planner Contract | while target remains eligible and fresh | Runtime |
| Planner selected move | decision candidate | planner/autoswitch | Decision Model / Planner | Decision Model vocabulary; L3 Planner Contract | valid while material assumptions remain identical | Runtime, packet/lock owners |
| FAILOVER | decision vocabulary | Decision Model / planner | Decision Model | Decision Model | semantic label only | Runtime/authority as input |
| Wake accepted | cycle-start fact | event/evidence owner | Autonomous Runtime Model | Wake Source rule | only starts observation | Runtime observation |
| Incident confirmed | visibility/lifecycle fact | incident/report owner | Autonomous Runtime Model / L3 Incident Contract | while incident generation remains active | Operator, Runtime |
| Authority exists | permission fact | OMP / Policy 004 / authority owners | Policy 004, L3 Authority Contract | while authority generation/envelope remains valid | Runtime eligibility |
| Restore barrier valid | safety fact | restore/rollback owners | Runtime Model / L3 Readiness + Execution Contract | must be live at execution boundary | Runtime execution |
| Rollback ready | safety fact | rollback owners | Policy 007 / L3 Readiness Contract | must be live before apply | Runtime execution |
| Verification ready | safety fact | verification owners | L3 Readiness + Verification Contract | must be live before apply | Runtime execution |
| Packet / transaction valid | execution artifact fact | packet / execution pipeline owners | Runtime Model / L3 Execution Contract | transient; valid only while identity and assumptions match | Runtime execution |
| Selected move hash matches | identity fact | packet/lease/restore/planner owners | Runtime Model / L3 Execution Contract | valid while selected move identity is unchanged | Runtime execution |
| EXECUTION_READY | derived permission-to-mutate truth | Runtime eligibility composition | Autonomous Runtime Model + Runtime Model + L3 | live execution boundary only | Execution owner |
| Verification passed | post-execution fact | verification owner | L3 Verification Contract | after apply, terminal proof | outcome/learning |
| Terminal outcome recorded | closure fact | feedback/outcome owner | Autonomous Runtime Model / L3 Learning Contract | durable after closure | learning, OMP |

## Truth Ownership

No single implementation object owns all truth. Ownership is by plane:

| Plane | Owns |
| --- | --- |
| Observation | current channel failure, required-service failure, freshness of reality |
| World Model | compact current state / assignment context |
| Planning | affected user, target, selected move, reason |
| Authority | approved envelope and generation |
| Execution | packet/transaction identity, selected move hash, restore barrier, apply |
| Verification | route/service/target proof |
| Feedback/Learning | terminal classification and learned evidence |
| OMP / Certification | capability state and certification |

Runtime owns orchestration and the execute-or-stop decision. Runtime does not own raw observation truth, planner truth, authority truth, or certification truth.

## Truth Dependency Graph

```text
User assigned to source
  + Current channel failed
  + Required services failed for that user on that source
  + Fresh evidence
    -> Affected user on failed current channel
      -> L3 emergency candidate
        + Safe target exists
          -> Planner selected FAILOVER move
            + L3 authority exists
            + blast/budget/policy gates pass
            + identity / selected_move_hash match
            + restore barrier valid
            + rollback ready
            + verification ready
              -> EXECUTION_READY
                -> Execute one user
                  -> Verify
                    -> Rollback / Success
                      -> Terminal outcome
                        -> Learning
                          -> OMP / capability state
```

## Minimal Truth Set

The smallest sufficient truth set for one legal L3 failover is:

1. One exact user is assigned to the source channel.
2. The source/current channel is failed for that user's required-service context.
3. The required services for that user fail on that current channel.
4. A safe target exists for the same user and service context.
5. Evidence is fresh enough for L3 mutation.
6. The move is inside L3 authority: `EMERGENCY_FAILOVER_AUTONOMY`, `FAILOVER`, `CURRENT_CHANNEL_FAILED`, one-user scope.
7. The selected move identity is stable and matches hash/user/source/target.
8. Restore barrier is valid for the same selected move.
9. Rollback or certified no-rollback is ready.
10. Verification is ready.
11. Blast radius, budget, policy, anti-flap, movement-protection, and circuit breaker gates pass.

Everything else is either input, explanation, lifecycle visibility, or post-execution proof.

## Truth Duplication

| Pair | Relationship | Finding |
| --- | --- | --- |
| Planner Selected Move vs Wake | different stages | Planner decision does not equal wake; wake starts observation and may not grant execution. |
| Planner Selected Move vs EXECUTION_READY | decision vs permission-to-mutate | Planner output is necessary but insufficient. |
| Incident Confirmed vs Current Channel Failed | visibility vs observed fact | Incident exposes failure; it does not independently prove all execution gates. |
| Authority Exists vs EXECUTION_READY | permission vs safety/readiness | Policy 004 explicitly states permission is not operational safety. |
| Restore Barrier Valid vs EXECUTION_READY | one safety gate vs composite truth | Restore barrier is necessary but insufficient. |
| Packet Valid vs EXECUTION_READY | execution artifact vs composite truth | Packet is transient and must match authority/readiness. |
| Verification Passed vs EXECUTION_READY | post-action proof vs pre-action permission | Verification cannot authorize the first apply because it occurs after apply. |

## Truth Contradiction

Observed contradiction:

```text
World: channel failed, 0/14 required services, users assigned
Planner: FAILOVER candidate exists
Runtime: required_service_failure not proven
```

These cannot all represent the same canonical L3 execution truth.

They can coexist only if:

- Planner `FAILOVER` was produced from a broader or weaker reason than L3's same-subject required-service-failure truth; or
- Runtime lost or did not consume the required-service evidence; or
- vocabulary mapped two different meanings to the same word.

At the truth level, the inconsistent fact is:

```text
Planner selected FAILOVER was treated as if it proved same-subject L3 EXECUTION_READY.
```

It does not.

## Truth Derivation Rules

| Derived truth | Can be derived? | Must be stored? | Must be recomputed? | Must never be recomputed? |
| --- | --- | --- | --- | --- |
| Affected user | yes, from assignment + failed current channel + service requirements | may be persisted as decision/incident evidence | recompute only before commit or as read-only freshness check | must not change after committed execution identity |
| L3 emergency candidate | yes, from affected user + L3 action class + safe target | may be stored in planner output | may refresh before commit | must not silently change after commit |
| Planner selected move | yes, by planner | must be preserved once committed/locked | may not be replaced after committed execution identity | must never be recomputed as a different executable move inside same lease |
| Wake accepted | yes, from approved event source | may be incident evidence | may reopen observation if generation is fresh | must not grant execution |
| EXECUTION_READY | yes, by composing all live gates | transient live truth | must be checked at the execution boundary | must not be cached across material changes |
| Terminal success | yes, after apply + verification + terminal outcome | durable outcome | not recomputed as intermediate apply success | must not ignore rollback/verification result |

## Vocabulary Audit

| Vocabulary | Canonical meaning | Relationship |
| --- | --- | --- |
| Current Channel Failed | current assigned channel is failed for affected user/service context | base L3 entry truth |
| Current Egress Not Eligible | broader planner/assignment phrase | may imply movement need, but not always L3 execution truth |
| Required Service Failure | required services fail for affected user on current channel | mandatory L3 entry truth |
| Emergency Candidate | derived candidate after L3 entry truths are present | derived truth |
| Wake | approved source to start observation | not execution truth |
| Incident | operator-visible lifecycle context | not execution truth |
| Planner Reason | explanation for selected move | not execution truth unless it carries same-subject evidence |
| Action Class | capability boundary | not execution truth by itself |
| Authority | permission envelope | not operational safety by itself |
| Packet / Lease | execution identity artifacts | not truth source by themselves |
| EXECUTION_READY | composite live permission-to-mutate | canonical pre-apply execution truth |

## One Canonical Truth

The first legal L3 execution becomes possible at the exact moment when the same assigned user is proven, with fresh same-subject evidence, to be on a failed current channel whose required services fail, a safe target exists, L3 authority is valid, and every live execution, restore, rollback, verification, identity, blast, budget, policy, and movement gate composes to `EXECUTION_READY`.

## Root Cause

Classification: `Truth Misinterpreted`.

The truth was not missing from canonical architecture. The canonical documents already distinguish:

- decision vocabulary from execution;
- wake from execution;
- authority from operational safety;
- packet/restore identity from permission-to-mutate;
- readiness from confidence.

The divergence is semantic: a planner `FAILOVER`/current-egress-not-eligible decision was treated as if it were the composite L3 execution truth. Canonically, it is only an input to `EXECUTION_READY`.

## Falsification

Attempted counterexamples:

1. `Planner Selected Move` alone authorizes movement.
   - Rejected: Decision Model says vocabulary is the decision interface; Runtime and L3 still require authority, readiness, restore, rollback, and verification gates.
2. `Wake Accepted` authorizes movement.
   - Rejected: Autonomous Runtime and L3 both state wake may start observation and may not grant execution.
3. `Authority Exists` authorizes movement.
   - Rejected: Policy 004 states permission does not prove operational safety or runtime eligibility.
4. `Packet Valid` authorizes movement.
   - Rejected: Runtime Model treats packet as transient artifact that must match committed decision, authority, policy, freshness, rollback, verification, and blast bounds.
5. `Restore Barrier Valid` authorizes movement.
   - Rejected: restore barrier is one readiness gate, not the composite execution truth.
6. `Verification Passed` authorizes movement.
   - Rejected: verification is post-apply proof and cannot authorize first apply.

No counterexample survived.

## Validation

Need New Truth Source: `FALSE`
Need New Owner: `FALSE`
Need New Architecture: `FALSE`
Need Runtime Change: `NO`
Need Planner Change: `NO`
Canonical documents updated: `NO`

Final verdict:

```text
CANONICAL_TRUTH_MISINTERPRETED
```
