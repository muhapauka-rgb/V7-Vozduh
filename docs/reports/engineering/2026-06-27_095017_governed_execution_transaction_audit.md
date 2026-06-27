# Engineering Report

## Summary

Existing architecture supports replacing `Approve Exact Packet` with `Approve One Governed Execution Transaction` for the current A4 governed learning flow.

This is not new authority, not a new runtime path, not new governance, and not new architecture. It is existing `OPERATIONAL_AUTHORITY` applied to a bounded execution transaction instead of a volatile packet id.

## Action Performed

Audited Product Specification, Runtime Model, Decision Model, OMP, Current Program State, Canonical Reference, SYSTEM_MAP, Action-Class Authority ADR, Delegated Autonomy Policy ADR, Decision Commit reports, Implementation Justification report, Operator Interaction audit, and A4 reports.

## Objective Observations

- Packet approval is documented as temporary `GOVERNED_ONLY` fallback.
- Runtime Model already separates authority, decision, packet, lease, live validation, execution, verification, rollback, outcome, and learning.
- Action-Class Authority and Delegated Autonomy Policy already treat packets as fresh runtime artifacts.
- A4 stale approvals prove that human approval separated from execution time can block real evidence collection.

## Transaction Definition

Start:

- operator explicitly approves one governed A4 execution transaction.

Flow:

```text
Transaction approval
  -> fresh governed dry-run
  -> Decision Commit
  -> execution lease
  -> live validation
  -> restore barrier
  -> apply or stop
  -> verify
  -> rollback/no-rollback closure
  -> learning
  -> transaction ends
```

Finish:

- verified outcome closed;
- rollback outcome closed;
- or safe stop recorded.

Maximum lifetime:

- one immediate execution attempt only; no delayed reuse.

Limits:

- action class: `single-user governed candidate failover`;
- max users: `1`;
- authority: `TIER_1 governed canary`;
- blast radius: one user;
- runtime rights: one bounded fresh packet inside the transaction envelope.

## Transaction Rights

The operator authorizes:

- one complete governed execution cycle for A4 evidence;
- fresh packet generation inside the approved envelope;
- lease/restore/apply/verify/rollback/no-rollback/learning only for that cycle.

The operator does not authorize:

- runtime automation;
- daemon/timer;
- authority expansion;
- class approval;
- policy approval;
- batch movement;
- stale packet execution;
- synthetic evidence.

## Stop Conditions

Abort transaction if:

- action class changes;
- more than one user is selected;
- authority tier changes;
- policy changes;
- blast radius exceeds one user;
- rollback or no-rollback plan is missing;
- verification plan is missing;
- freshness fails;
- target/source becomes ineligible;
- anti-flap or movement protection fails;
- restore barrier is unsafe;
- live validation fails;
- fresh packet is not `PACKET_PREVIEW_READY`;
- packet exits approved transaction envelope;
- apply cannot happen immediately.

## Engineering Conclusions

`Approve One Governed Execution Transaction` is a safe existing-owner extension of current operational authority.

It preserves fail-closed, rollback, verification, freshness, movement protection, anti-flap, restore barrier, learning, and authority boundaries because Runtime may only execute a fresh packet that passes all existing gates inside the bounded transaction.

## Commercial Comparison

This matches production control-plane practice:

- Cisco NSO / Crosswork: operator approves bounded transaction/workflow intent, not packet artifacts.
- Google SRE: one approved change/canary transaction runs through checks, rollback, and outcome closure.
- AWS: policy/change boundary authorizes controller action; runtime artifacts are fresh.
- Cloudflare: scoped operational actions run inside policy/risk envelopes.
- Kubernetes: controllers act from desired-state/permission envelope and reconcile live state before commit.

## Impact

No runtime behavior changed. No user moved. No authority expanded.

## Capability Progress

No percentage change.

## Backlog Progress

Existing backlog remains sufficient:

- `A4`: current governed learning evidence path;
- `A6`: generalized runtime eligibility arbitration;
- `A5` / `B13`: later certification and reliability gates.

## Production Maturity

No maturity change.

## Canonical Knowledge

No canonical owner update required. The model already exists across Product Specification, Runtime Model, OMP, Action-Class Authority ADR, Delegated Autonomy Policy ADR, and Current Program State.

## Evidence

Recent A4 attempts stopped because exact packet approval became stale before execution. This validates that exact packet approval is the wrong operational boundary for collecting A4 governed evidence.

## Next Step

Continue OMP. If operator approves one governed transaction, execute exactly one bounded A4 transaction through existing owners and stop on any envelope violation.

## Re-audit Rule

Re-audit only if transaction authority is proposed for more than one user, more than one action class, delayed reuse, automation, authority expansion, or policy/class promotion.
