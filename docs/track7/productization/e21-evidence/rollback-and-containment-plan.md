# E21 Rollback And Containment Plan

## Selected First Action Rollback

selected_first_action=F_READONLY_TO_EXECUTION_TRANSITION_PACKET_WITH_ZERO_MOVE_GENERATION_CLEARANCE_AS_NEXT_BOUNDARY

User rollback commands:

- NONE

Routing rollback commands:

- NONE

Rollback is approval/audit revocation only:

- append immutable `approval_revoked` audit record;
- mark approval status `REVOKED_FAIL_CLOSED`;
- mark execution status `DENIED_NO_RUNTIME_ACTION`;
- leave UI execution controls disabled;
- do not touch users.registry;
- do not touch route tables;
- do not call v7-user-switch;
- do not call autoswitch apply.

## Future Zero-Move Generation-Clearance Rollback

If a later block advances from approval-record-only to zero-move generation clearance:

- revoke clearance before any apply timer restoration;
- require selected_moves=0;
- require apply timer held or explicitly proven safe;
- append immutable rollback/revocation record;
- keep runtime fail-closed if any recheck fails.

## Containment Triggers

- hidden mover observed;
- selected_moves becomes nonzero;
- generation mismatch;
- approval replay;
- target readiness changes;
- restore-settle becomes non-GO;
- kill switch or route checker fails;
- operator identity mismatch;
- audit chain mismatch.

## Containment Action

For selected first action:

- deny execution;
- append denial record;
- do not repair runtime manually;
- require operator review.

For any later runtime-affecting action:

- immediately hold apply timer if movement risk exists;
- collect switch-history;
- classify movement path;
- do not perform user rollback unless the approved rollback packet allows it.

## Delayed Monitoring

For approval-record-only action:

- verify no selected_moves drift;
- verify no hidden movers;
- verify audit chain append only.

For any future runtime-affecting action:

- collect at least 5 samples;
- verify users.registry hash;
- verify switch-history count;
- verify target readiness;
- verify selected_moves=0;
- verify no hidden movers.

## Plan Verdict

rollback_plan_complete=true
containment_plan_complete=true
execution_allowed_now=false
