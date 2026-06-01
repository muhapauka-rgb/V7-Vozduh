# Audit, Closure, Rollback, and No-Op Relationships

## Audit Relationship

When audit must be written:

- when a runtime operation is created from operator intent or scheduled runtime cycle if durable operation tracking is required;
- when execution starts;
- when execution completes;
- when execution fails;
- when verification starts/completes/fails;
- when rollback starts/completes/fails;
- when denial/cancel/expiry/replay denial occurs;
- when closure state changes.

Audit is complete when:

- terminal runtime state has a canonical `v7-audit-log` event or equivalent canonical audit evidence;
- event identifies operation scope, actor/source, runtime owner, affected users/targets when applicable, selected-move/no-op reason, result, and timestamp;
- rollback/audit evidence exists for rollback branches.

Audit is insufficient when:

- only stdout/journal exists for a movement operation;
- only markdown report exists for current lifecycle closure;
- runtime outcome lacks selected-move/no-op reason;
- rollback state is unknown;
- closure record exists without terminal runtime outcome;
- event cannot be tied to operation identity/scope.

Audit blocks closure when:

- runtime terminal state exists but canonical audit evidence is missing;
- rollback branch lacks start/completion/failure evidence;
- denial/cancel/expiry lacks reason;
- selected-move set or no-op reason cannot be reconstructed.

Minimum audit evidence:

- operation id or semantic operation identity;
- runtime owner;
- operation kind;
- timestamp;
- actor/source;
- terminal state;
- affected users/targets or explicit no-op scope;
- selected-move hash/count or no-op/denial reason;
- rollback state if applicable.

Closure-quality audit:

- minimum audit evidence plus verification result;
- rollback result if applicable;
- restore-barrier/generation context if it affected admission;
- closure actor/reason/timestamp;
- references to proposal/approval/evidence where applicable.

## Closure Relationship

Closure may begin when:

- operation has reached a runtime terminal state; or
- operation intent was denied/cancelled/expired before execution.

Closure may finish when:

- terminal state is known;
- audit is sufficient;
- rollback requirement is satisfied, failed-closed, or not applicable;
- closure reason and actor are present.

Can closure exist without audit?

- It may exist as `OPEN` or blocker metadata.
- It must not become lifecycle `CLOSED` without audit or explicit audit-missing blocker.

Can closure exist without runtime outcome?

- It may exist for proposals/evidence as non-runtime closure.
- Runtime Operation closure requires runtime outcome or denial/cancel/expiry reason.

Can closure exist after rollback?

- Yes. `ROLLED_BACK` should be audited and then closed.

Can closure exist after failure?

- Yes. `FAILED_CLOSED` can close if containment and audit evidence are sufficient.

Can closure be reopened?

- Yes, semantically by writing a later Admin closure record that changes state back to `OPEN` or `VERIFIED`; reopening is closure-owner authority and should be audited.

## Rollback Relationship

Rollback begins when:

- verification fails and rollback is configured/available;
- runtime owner declares forward state unsafe and rollback is required;
- Admin/operator invokes a governed rollback primitive with known scope.

Rollback ends when:

- movement rollback target is restored and verified;
- generic rollback primitive returns success and required post-check evidence exists;
- rollback fails and operation becomes `FAILED_CLOSED`.

Rollback becomes terminal when:

- `ROLLED_BACK` is reached with sufficient evidence; or
- `FAILED_CLOSED` is reached after rollback failure/containment.

Rollback becomes failed when:

- rollback command fails;
- rollback verification fails;
- rollback target is unknown;
- rollback manifest is missing when required;
- post-rollback state cannot be verified.

Rollback becomes closure blocker when:

- rollback is required but not attempted;
- rollback state is unknown;
- rollback evidence is missing;
- rollback failed and containment evidence is missing.

Relationship:

- Runtime owner owns movement rollback truth.
- Generic rollback primitive owns its command result only.
- Audit owner records rollback events.
- Closure owner closes only after rollback state is terminal and auditable.

## No-Op Operations

No-op cases:

- `selected_moves=0`;
- blocked by restore barrier;
- blocked by policy;
- blocked by trust;
- blocked by capacity;
- dry-run;
- observe mode;
- autoswitch disabled;
- generation/hash/count mismatch;
- replay denied.

Are these operations?

- Yes when a scheduled or operator-triggered runtime decision reached a terminal decision.
- No when only passive evidence exists and no runtime owner decision occurred.

Are they lifecycle objects?

- Yes semantically, if they have runtime owner decision, reason, timestamp, and scope.

Can they be closed?

- Yes. No-op may close as `COMPLETED` if normal empty/no-op, or `DENIED` if blocked/denied.

Can they be audited?

- Yes. No-op audit should record reason, selected-move count/hash, barrier/policy/trust/capacity blocker, and source.

No-op closure quality:

- no movement occurred;
- no rollback required;
- reason is explicit;
- selected-move count/hash known;
- blocker/gate source known;
- audit exists;
- Admin closure record exists.

