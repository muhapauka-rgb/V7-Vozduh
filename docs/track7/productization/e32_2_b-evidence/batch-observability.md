# E32.2.B Batch Observability

batch_observability_defined=true

## Operator View

Operators must see enough to answer:

- what batch is this?
- what type is it?
- who is affected?
- what target is used?
- where is rollback?
- what is the risk?
- what capacity state applies?
- is execution eligible?
- why is it blocked?
- what is the next safe action?
- where is the audit lineage?

## Required Display Fields

```text
batch_id
batch_status
batch_type
allowed_users
source_targets
destination_target
rollback_targets
movement_budget
blast_radius
risk_score
capacity_state
execution_eligibility
blocked_reasons
next_safe_action
audit_lineage_id
evidence_paths
```

## Status Display

Operator status display must distinguish:

- draft/modeling state;
- approved but not executable state;
- scheduled state;
- executing state;
- observing state;
- rollback-ready state;
- rolling-back state;
- completed state;
- failed-closed state;
- replay-denied state;
- cancelled state;
- expired state.

## Blocked Reasons

Blocked reason examples:

- packet expired;
- runtime drift;
- capacity conflict;
- target not eligible;
- restore-settle not GO;
- runtime checkers failed;
- selected moves nonzero;
- hidden movers present;
- rollback manifest incomplete;
- audit lineage conflict.

## Next Safe Action

Each blocked state must show one next safe action:

- refresh packet;
- rerun precheck;
- repair metadata;
- recertify capacity;
- wait for restore-settle;
- investigate hidden movers;
- rollback/contain;
- human review.

## Audit Drilldown

Operators must be able to inspect:

- approval packet;
- execution-time recheck;
- forward event;
- rollback event;
- replay denial;
- tests;
- final report.

## Observability Verdict

Batch observability is defined.
