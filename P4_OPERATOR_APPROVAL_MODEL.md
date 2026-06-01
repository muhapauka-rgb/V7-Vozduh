# P4 Operator Approval Model

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Approval Flow

P4 defines this planning approval flow:

1. `PROPOSED`
2. `REVIEW_REQUIRED`
3. `APPROVED`
4. `REJECTED`
5. `EXPIRED`
6. `ABORTED_AFTER_RECHECK`

## Approval Roles

| Role | Capability |
| --- | --- |
| Approval author | Proposes and signs planning packet. |
| Approval reviewer | Independently reviews and approves/rejects. |
| Runtime owner | Can reject or require recheck when runtime facts changed. |
| Safety reviewer | Can block on rollback, observation or fail-closed gaps. |

## Override Rule

No single operator can override execution safeguards.

Any override must:

- be explicit
- be scoped
- be time-limited
- name the risk accepted
- still require immediate runtime recheck
- still preserve rollback and observation

## Approval Does Not Execute

Approval in P4 means approval of the action design, not approval to execute.

## Verdict

`approval_model_defined=true`

