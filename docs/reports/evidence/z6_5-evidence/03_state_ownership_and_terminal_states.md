# State Ownership and Terminal States

## State Ownership

| State | Primary Owner | Secondary Owner | Audit Owner | Closure Owner | Runtime Owner | Who May Enter | Who May Leave | Who May Block | Who May Close |
|---|---|---|---|---|---|---|---|---|---|
| `CREATED` | Admin/proposal or scheduler/runtime cycle source | Runtime owner | `v7-audit-log` if recorded | Admin closure | Autoswitch if scheduled | Admin/scheduler/runtime owner | Runtime owner/Admin | Admin gates | Admin closure |
| `PLANNED` | Runtime owner | Admin dry-run | `v7-audit-log` optional until terminal | Admin closure | Autoswitch | Runtime owner | Runtime owner | policy/trust/capacity/barrier | Admin closure after terminal only |
| `REVIEW_REQUIRED` | Admin gates | Runtime owner | `v7-audit-log` optional | Admin closure | Autoswitch provides facts | Admin gates/runtime owner | Admin approval/denial | Admin/gates | Admin closure if terminal denial/expiry |
| `APPROVED` | Admin/operator governance | Runtime owner | `v7-audit-log` | Admin closure | Autoswitch consumes | Admin/operator | Runtime owner | runtime recheck | Admin closure after terminal |
| `DENIED` | Runtime owner or Admin/gates | Admin/operator | `v7-audit-log` required for closure quality | Admin closure | Autoswitch if runtime denial | Runtime owner/Admin gates | Audit/closure only | Audit owner if missing evidence | Admin closure |
| `READY` | Runtime owner | Admin gates | `v7-audit-log` optional until execution | Admin closure | Autoswitch | Runtime owner | Runtime owner | runtime recheck/barrier | no direct closure unless cancelled/expired |
| `EXECUTING` | Runtime owner | Scheduler/Admin surface | `v7-audit-log` event should exist | Admin closure | Autoswitch | Runtime owner | Runtime owner | runtime owner | no |
| `VERIFYING` | Runtime owner | Admin/operator visibility | `v7-audit-log` event should exist | Admin closure | Autoswitch | Runtime owner | Runtime owner | runtime owner | no |
| `ROLLBACK_READY` | Runtime owner | Admin rollback surface | `v7-audit-log` should record failure/need | Admin closure | Autoswitch | Runtime owner | Runtime owner/Admin rollback path | audit/rollback availability | no |
| `ROLLING_BACK` | Runtime owner or rollback primitive under owner | Admin surface | `v7-audit-log` should record start | Admin closure | Autoswitch for movement | Runtime owner | Runtime owner | rollback failure | no |
| `COMPLETED` | Runtime owner | Admin/operator visibility | `v7-audit-log` required before closure | Admin closure | Autoswitch | Runtime owner | Audit owner then closure owner | audit insufficiency | Admin closure after audit |
| `FAILED_CLOSED` | Runtime owner | Admin/operator visibility | `v7-audit-log` required before closure | Admin closure | Autoswitch | Runtime owner | Audit/closure only | audit or rollback evidence missing | Admin closure after evidence |
| `ROLLED_BACK` | Runtime owner / rollback primitive result | Admin surface | `v7-audit-log` required before closure | Admin closure | Autoswitch for movement rollback | Runtime owner/rollback primitive | Audit/closure only | rollback audit missing | Admin closure |
| `REPLAY_DENIED` | Runtime owner or operator execution support | Admin/operator | `v7-audit-log` required before closure | Admin closure | Autoswitch/operator support | Runtime owner/recheck | Audit/closure only | audit missing | Admin closure |
| `CANCELLED` | Admin/operator or runtime owner | Runtime owner | `v7-audit-log` required before closure | Admin closure | Autoswitch if runtime cancellation | Admin/runtime owner | Audit/closure only | audit missing | Admin closure |
| `EXPIRED` | Admin/operator or runtime owner | Runtime owner | `v7-audit-log` required before closure | Admin closure | Autoswitch if runtime expiry | Admin/runtime owner | Audit/closure only | audit missing | Admin closure |
| `AUDITED` | Audit owner | Admin/operator | `v7-audit-log` | Admin closure | Runtime outcome provider | Audit owner/Admin wrapper | Closure owner | closure evidence missing | Admin closure |
| `CLOSED` | Closure owner | Audit owner/runtime owner | `v7-audit-log` | Admin closure | Runtime facts immutable | Admin closure | reopened only by Admin as new closure record | not applicable | Admin closure owner |

## Terminal States

| Terminal State | Meaning | Requirements | Evidence Required | Audit Required | Closure Required |
|---|---|---|---|---|---|
| `COMPLETED` | Runtime operation finished successfully or no-op completed intentionally | Runtime outcome from autoswitch; verification if movement occurred; no rollback required | plan/apply result, selected moves or no-op reason, verification result if applicable | yes before `CLOSED` | yes for lifecycle completion |
| `FAILED_CLOSED` | Runtime failed and system is contained/fail-closed | failure result; no unsafe forward continuation; rollback unavailable/failed/not applicable | failure output, containment reason, rollback status | yes | yes |
| `ROLLED_BACK` | Operation was reverted to known rollback target | rollback started and completed; post-rollback verification when applicable | rollback result, rollback target, verification/containment | yes | yes |
| `DENIED` | Operation did not execute because runtime/gate denied it | denial reason; no movement performed | gate/recheck/barrier/policy/trust/capacity reason | yes for closure quality | yes if operation intent existed |
| `REPLAY_DENIED` | Duplicate or replay attempt denied | replay detection evidence | replay key/approval id/operation id | yes | yes |
| `CANCELLED` | Operation intentionally cancelled before completion | cancellation actor/reason or runtime cancellation fact | cancellation reason, actor/source | yes | yes |
| `EXPIRED` | Operation intent or approval window expired | expiry timestamp/source | expiry evidence, freshness/approval data | yes | yes |

## Terminal Rule

Terminal runtime states are not closure states.

An operation reaches lifecycle completion only after:

runtime terminal state -> sufficient audit -> closure record.

