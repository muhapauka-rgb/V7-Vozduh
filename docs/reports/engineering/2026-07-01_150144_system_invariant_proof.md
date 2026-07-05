# System Invariant Proof

## Summary

Verdict: `SYSTEM_INVARIANT_VIOLATED`

The first violated system invariant is:

```text
FAILOVER_SEMANTIC_BINDING
```

Formal rule:

```text
IF Planner emits a selected move with action/move_type = FAILOVER for L3
THEN the selected move must be causally bound to proof that:
  1. the same selected current channel is failed for the affected user context;
  2. required services for that affected user context fail on that same current channel;
  3. the selected target is safe;
  4. this evidence is fresh enough for L3.
```

Runtime did not violate the invariant. Runtime enforced it and stopped safely.

## Canonical Owners Read

- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
- `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/policies/POLICY_001_HARD_FAILURE.md`
- `docs/policies/POLICY_004_AUTHORITY.md`
- `docs/policies/POLICY_008_FRESHNESS.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`

Engineering reports were used only as production evidence, not canonical truth.

## Complete Invariant Inventory

### Observation Truth Invariant

Canonical basis:

- Autonomous Runtime Model: Runtime observes reality and stops on stale, missing, contradictory, or unsafe evidence.
- Freshness policy: mutation must not rely on stale evidence.

Formal rule:

```text
IF runtime evidence is used for mutation
THEN it must be current, owner-produced, and distinguish healthy, failed, stale, and unknown.
```

Replay status: `PASS`

Production evidence was fresh enough to evaluate and stop.

### Hard Failure Evidence Invariant

Canonical basis:

- Policy 001: hard failure must be based on explicit liveness evidence.
- L3 Capability: current channel failed is a mandatory entry condition.

Formal rule:

```text
IF a channel is classified as failed for L3
THEN explicit liveness/service/route evidence must prove it is unable to carry expected traffic for the affected context.
```

Replay status: `PASS_FOR_OPENVPN`, `NOT_PROVEN_FOR_SELECTED_AWG0_MOVE`

The world evidence showed `openvpn-1779388847-d2ad7c` failure. The selected production validation move was `10.7.0.5 awg0 -> vless`; runtime did not find required-service failure evidence for `awg0`.

### Required-Service Failure Invariant

Canonical basis:

- L3 Capability Entry Conditions: required services for affected users fail on current channel.
- L3 Readiness: source eligibility requires current channel/user/failure evidence.

Formal rule:

```text
IF L3 enters emergency failover for a user/current-channel pair
THEN at least one required service for that user context must be failed on that same current channel.
```

Replay status: `FAIL`

Latest runtime evidence:

```text
selected move: 10.7.0.5 awg0 -> vless
move reason: current_egress_not_eligible
move_evidence.current_failures: []
gate blocker: required_service_failure_required
```

### Planner Truth Invariant

Canonical basis:

- L3 Planner Contract: Planner identifies affected users on failed current channel, candidate targets, unsafe targets, selected move identity and explanation.
- Decision Model vocabulary: `FAILOVER` means move affected users away from a failing channel.

Formal rule:

```text
IF Planner emits FAILOVER
THEN Planner output must carry enough same-subject evidence for Runtime to verify current-channel failure and affected-user required-service impact without inventing facts.
```

Replay status: `FAIL`

Planner produced a `FAILOVER` move whose source-specific required-service failure could not be proven by Runtime.

### Runtime Truth Invariant

Canonical basis:

- Runtime Model / Autonomous Runtime Model: Runtime consumes owner output and chooses only `EXECUTE`, `STOP_SAFE`, `ASK_OPERATOR`, `SUSPEND`, `INCIDENT`, or `SLEEP`.
- L3 Capability: any failed mandatory gate produces `STOP_SAFE`.

Formal rule:

```text
IF mandatory L3 evidence is missing or false
THEN Runtime must STOP_SAFE and must not execute.
```

Replay status: `PASS`

Runtime returned `STOP_SAFE`, `apply_executed=false`, `users_moved=0`.

### Authority Truth Invariant

Canonical basis:

- Policy 004: permission is not operational safety.
- L3 Authority Contract: authority allows only `EMERGENCY_FAILOVER_AUTONOMY`, `FAILOVER`, `CURRENT_CHANNEL_FAILED`.

Formal rule:

```text
IF authority exists
THEN it only permits execution inside the approved class/scope; it does not prove readiness or safety.
```

Replay status: `PASS`

Authority did not grant execution because source failure evidence was missing for the selected move.

### Execution Truth Invariant

Canonical basis:

- L3 Execution Contract: preserve identity, selected move hash, source, target, restore generation, packet/transaction identity.

Formal rule:

```text
IF execution reaches apply
THEN selected identity and restore/authority/verification/rollback identities must still match.
```

Replay status: `NOT_REACHED`

Execution stopped before apply.

### Evidence Truth Invariant

Canonical basis:

- Decision Model: health/readiness are gates.
- Autonomous Runtime Model: high confidence cannot override failed readiness.

Formal rule:

```text
IF confidence or score indicates a candidate
THEN it may not replace mandatory failure evidence.
```

Replay status: `PASS`

Runtime rejected the move despite Planner confidence because required failure evidence was absent.

### Identity Truth Invariant

Canonical basis:

- Decision ownership reports and L3 Execution Contract: selected move identity binds user/source/target/hash.

Formal rule:

```text
IF failure evidence is used to justify a selected move
THEN that evidence must bind to the same selected user/source/target identity.
```

Replay status: `FAIL`

Evidence of a failed channel existed for `openvpn-1779388847-d2ad7c`, while the selected move requiring execution was `awg0 -> vless`.

### Capability Truth Invariant

Canonical basis:

- L3 Capability: L3 is emergency failover, not rebalance, optimization, preference movement, cleanup, pool optimization, or capacity balancing.

Formal rule:

```text
IF movement reason is not confirmed current-channel failure with required-service impact
THEN it is not L3 emergency failover.
```

Replay status: `FAIL`

`current_egress_not_eligible` alone is broader than L3 emergency failover.

### OMP Truth Invariant

Canonical basis:

- OMP execution closure and verified consumption.

Formal rule:

```text
IF a capability output is produced
THEN it must be consumed, verified, behavior-changing, and terminally closed or blocked by an allowed stop condition.
```

Replay status: `PASS`

The attempt reached terminal `STOP_SAFE` with no user movement.

## Production Replay

Latest production validation facts:

```text
final_verdict: STOP_SAFE
apply_executed: false
users_moved: 0
selected user: 10.7.0.5
source: awg0
target: vless
approved_plan_lock_validation.ok: true
approved_plan_lock.selected_moves contains semantic fields: true
gate blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
move_evidence.current_failures: []
```

Read-only planner evidence also showed a separate failed production channel:

```text
channel: openvpn-1779388847-d2ad7c
users: 14
service suitability: failed/degraded for multiple services
```

The failed-channel evidence and selected execution candidate were not bound to the same source identity.

## First Violated Invariant

The first violated invariant is not serialization, authority, restore barrier, or runtime execution.

It is:

```text
FAILOVER_SEMANTIC_BINDING
```

Earliest false statement:

```text
Planner emitted a FAILOVER selected move without Runtime-verifiable proof
that the selected source/user context had required-service failure.
```

Downstream effects:

```text
Runtime cannot infer confirmed L3 wake
Runtime cannot prove required_service_failure
Runtime STOP_SAFE
No apply
```

## Minimal Inconsistent Fact Set

These facts cannot all satisfy L3 invariants simultaneously:

```text
1. L3 FAILOVER requires selected current channel failure and required-service failure.
2. Planner selected FAILOVER for 10.7.0.5 awg0 -> vless.
3. Runtime found no required-service failure for awg0 in that selected move.
4. Runtime is not allowed to invent or borrow failure evidence from another channel.
```

Therefore the inconsistent set is not:

```text
openvpn failed
planner found some failover
runtime stopped
```

The inconsistent set is:

```text
selected move classified as L3 FAILOVER
same selected move lacks required-service failure evidence
```

## Root Cause Class

Classification:

```text
Planner violates invariant
```

More precisely:

```text
Planner/action-class semantic classification violates the L3 failover binding invariant.
```

Runtime preserved system safety.

## Falsification

Attempted refutations:

1. Could Runtime be wrong?
   - No. L3 explicitly requires failed mandatory gates to `STOP_SAFE`.

2. Could Authority be wrong?
   - No. Authority does not prove readiness or failure.

3. Could serialization still be wrong?
   - No. Latest approved plan lock contains semantic fields and validates successfully.

4. Could failed openvpn evidence justify awg0 failover?
   - No. Identity truth requires failure evidence to bind to the same selected source/user context.

5. Could `current_egress_not_eligible` be enough?
   - No. L3 requires failed current channel and required-service failure, not generic ineligibility.

Conclusion survived falsification.

## Minimal Invariant Restoration

Restore this invariant:

```text
Planner may emit L3 FAILOVER only when the selected move carries same-subject proof of:
  current channel failure
  required-service failure
  affected user assignment
  safe target
  fresh evidence
```

If those proofs are not present, Planner must not classify the move as L3 `FAILOVER`.

It must instead produce one of the existing non-L3 outcomes:

- `MOVE`
- `DRAIN`
- `PROBE_ONLY`
- `ASK_OPERATOR`
- `NO_ACTION`
- `STOP_SAFE`

No new architecture is required.

No new owner is required.

No new truth source is required.
