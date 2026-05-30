# E32.3.A Policy Type Taxonomy

policy_type_taxonomy_defined=true

## CAPACITY_POLICY

Purpose:

Control use of capacity classes, confidence, freshness, hard limits, policy caps, and available capacity.

Allowed decisions:

- allow/deny target eligibility by capacity;
- require recertification;
- set active policy cap.

Forbidden decisions:

- grant capacity certification without evidence;
- bypass capacity failure modes.

Required inputs:

- capacity class;
- capacity status;
- confidence;
- effective batch cap;
- available capacity.

Fail-closed behavior:

Missing or stale capacity denies forward movement.

## BATCH_POLICY

Purpose:

Control batch type, scope, budget, blast radius, metadata completeness, and lifecycle status.

Allowed decisions:

- allow/deny batch type;
- require exact scope;
- deny invalid lifecycle transition.

Forbidden decisions:

- mutate batch scope after approval;
- resume terminal batches.

Required inputs:

- batch type;
- allowed users;
- destination target;
- rollback manifest;
- lifecycle state.

Fail-closed behavior:

Invalid or incomplete batch denies forward movement.

## RISK_POLICY

Purpose:

Evaluate operational risk.

Allowed decisions:

- require review;
- deny high-risk combinations;
- require staged execution.

Forbidden decisions:

- override hard safety denials.

Required inputs:

- batch size;
- target class;
- rollback completeness;
- audit state;
- incident state.

Fail-closed behavior:

Unknown risk becomes `REQUIRE_REVIEW` or `DENY` depending on severity.

## OPERATOR_POLICY

Purpose:

Control who can approve, schedule, execute, rollback, or revoke policies/batches.

Allowed decisions:

- require operator role;
- require dual confirmation;
- restrict emergency actions.

Forbidden decisions:

- authorize runtime mutation without batch and packet gates.

Required inputs:

- operator identity;
- operator role;
- action type;
- approval context.

Fail-closed behavior:

Unknown or insufficient role denies admission.

## SCHEDULING_POLICY

Purpose:

Control execution windows, queue rules, and future scheduler admission.

Allowed decisions:

- allow/deny schedule window;
- enforce max concurrent batches;
- enforce maintenance windows.

Forbidden decisions:

- bypass execution-time recheck;
- double-spend capacity reservations.

Required inputs:

- execution window;
- batch status;
- reservation state;
- scheduler state.

Fail-closed behavior:

Unknown scheduling state denies scheduling, not rollback containment.

## ROLLBACK_POLICY

Purpose:

Control rollback and containment decisions.

Allowed decisions:

- allow exact-scope rollback;
- require containment;
- deny unsafe rollback.

Forbidden decisions:

- expand rollback scope;
- rollback unknown users automatically.

Required inputs:

- rollback manifest;
- affected users;
- rollback targets;
- route table map.

Fail-closed behavior:

Unknown rollback scope requires human review.

## ROUTE_CLASS_POLICY

Purpose:

Control route classes and target eligibility by class.

Allowed decisions:

- prevent sensitive route class assignment;
- restrict target use by route class.

Forbidden decisions:

- broad route sync;
- route mutation outside approved batch.

Required inputs:

- source target;
- destination target;
- route class;
- excluded route classes.

Fail-closed behavior:

Unknown or forbidden route class denies forward movement.

## PRODUCTION_POOL_POLICY

Purpose:

Control future production-pool behavior.

Allowed decisions:

- enforce pool admission;
- require reservation ledger;
- enforce pool caps;
- require observability.

Forbidden decisions:

- certify production-pool execution without E32 production-pool controls.

Required inputs:

- pool id;
- target set;
- batch set;
- capacity/reservation state;
- scheduler state.

Fail-closed behavior:

Uncertified production-pool controls deny production-pool execution.

## Taxonomy Verdict

Policy type taxonomy is defined.
