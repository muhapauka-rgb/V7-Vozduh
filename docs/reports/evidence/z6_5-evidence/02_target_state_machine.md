# Target Runtime Operation State Machine

## Design Rule

The target state machine derives from existing execution contract statuses and runtime outputs. It does not create a duplicate storage/API model.

## Canonical Runtime Operation States

| State | Derived From Existing Concepts | Meaning |
|---|---|---|
| `CREATED` | `DRAFT`, proposal/evidence intent | Operation intent exists but runtime owner has not produced final plan/admission. |
| `PLANNED` | autoswitch plan JSON, proposal-to-draft, selected-move calculation | Runtime owner has a plan/no-op/decision candidate. |
| `REVIEW_REQUIRED` | proposal/gate `REVIEW_REQUIRED`, `READY_WITH_REVIEW`, operator previews | Human/governance review required before execution/closure. |
| `APPROVED` | `APPROVED`, governed/manual operator approval | Operator/governance intent approved, but runtime owner has not yet executed. |
| `DENIED` | `REPLAY_DENIED`, `DENY_*`, gate `FAIL`, policy/trust/capacity/barrier denial | Execution denied before movement or terminally rejected by runtime/admission. |
| `READY` | `VALIDATED`, `RECHECKED`, `READY`, `PASS` | Runtime owner can proceed if execution is requested and not otherwise blocked. |
| `EXECUTING` | `EXECUTING`, `EXECUTION_STARTED`, autoswitch apply loop | Runtime owner is performing movement. |
| `VERIFYING` | `VERIFYING`, `VERIFICATION_STARTED`, autoswitch route verification | Runtime owner is verifying result. |
| `ROLLBACK_READY` | existing `ROLLBACK_READY`, failed verification with rollback available | Rollback is required or available but has not started. |
| `ROLLING_BACK` | `ROLLING_BACK`, `ROLLBACK_STARTED`, autoswitch rollback call | Rollback is in progress. |
| `COMPLETED` | `COMPLETED`, `EXECUTION_COMPLETED`, verified apply result, no-op completion | Runtime outcome terminal success/no-op; not necessarily audited or closed. |
| `FAILED_CLOSED` | existing `FAILED_CLOSED`, execution failed without safe forward continuation | Runtime failed and is contained/fail-closed. |
| `ROLLED_BACK` | existing `ROLLED_BACK`, `ROLLBACK_COMPLETED` | Rollback completed terminally. |
| `REPLAY_DENIED` | existing `REPLAY_DENIED`, `DENY_REPLAY` | Duplicate/replay execution denied terminally. |
| `CANCELLED` | existing `CANCELLED` | Operation was cancelled before runtime execution terminal. |
| `EXPIRED` | existing `EXPIRED`, approval/closure freshness expiry | Operation intent expired before completion or closure. |
| `AUDITED` | audit event exists, `v7-audit-log` evidence complete | Runtime terminal state has canonical audit evidence. |
| `CLOSED` | Admin closure `CLOSED` | Closure owner has closed the lifecycle after runtime/audit evidence. |

## Normal Movement Path

`CREATED`
-> `PLANNED`
-> `REVIEW_REQUIRED`
-> `APPROVED`
-> `READY`
-> `EXECUTING`
-> `VERIFYING`
-> `COMPLETED`
-> `AUDITED`
-> `CLOSED`

`REVIEW_REQUIRED` may be skipped for fully autonomous policy-approved cycles, but then audit/closure must still explain why execution was allowed.

## No-Op Path

`CREATED`
-> `PLANNED`
-> `COMPLETED`
-> `AUDITED`
-> `CLOSED`

Allowed no-op reasons include:

- `dry_run`;
- `autoswitch_disabled_by_policy`;
- `mode_observe_blocks_apply`;
- `no_selected_moves`;
- restore-barrier block;
- policy/trust/capacity block;
- replay denied;
- selected-move budget/generation mismatch.

If the no-op is a denial rather than ordinary empty plan, use `DENIED` before audit/closure:

`CREATED` -> `PLANNED` -> `DENIED` -> `AUDITED` -> `CLOSED`

## Failure with Rollback Path

`CREATED`
-> `PLANNED`
-> `APPROVED`
-> `READY`
-> `EXECUTING`
-> `VERIFYING`
-> `ROLLBACK_READY`
-> `ROLLING_BACK`
-> `ROLLED_BACK`
-> `AUDITED`
-> `CLOSED`

## Failure without Successful Rollback Path

`CREATED`
-> `PLANNED`
-> `APPROVED`
-> `READY`
-> `EXECUTING`
-> `VERIFYING`
-> `FAILED_CLOSED`
-> `AUDITED`
-> `CLOSED`

If audit is insufficient:

`FAILED_CLOSED` remains blocked from `CLOSED` until audit/closure evidence is sufficient.

## Cancel / Expire Path

`CREATED`
-> `PLANNED`
-> `CANCELLED`
-> `AUDITED`
-> `CLOSED`

or

`CREATED`
-> `PLANNED`
-> `EXPIRED`
-> `AUDITED`
-> `CLOSED`

## State Machine Notes

- `COMPLETED`, `FAILED_CLOSED`, `ROLLED_BACK`, `REPLAY_DENIED`, `DENIED`, `CANCELLED`, and `EXPIRED` are runtime terminal states.
- `AUDITED` is an evidence-completion state.
- `CLOSED` is a closure-completion state.
- Runtime terminal does not equal lifecycle closed.

