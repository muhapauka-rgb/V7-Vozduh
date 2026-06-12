# OA.1 Required Approval Model

## Existing Good Pieces

The existing system can already prepare:

- planner candidate;
- packet draft / approval packet evidence;
- approved-plan-lock preview;
- rollback manifest / rollback dry-run;
- restore barrier readiness/recheck;
- verification plan;
- feedback materialization plan;
- audit/closure preview;
- operator decision surface.

## Missing Product Component

Missing component:

`canonical operator-approved execution controller`

It must be one existing-governance wrapper, not a new executor.

Responsibilities:

1. accept exactly one operator decision: APPROVE or REJECT;
2. on REJECT: write denial/closure only;
3. on APPROVE: call existing owners in sequence:
   - planner freshness check;
   - packet generation;
   - runtime recheck;
   - restore barrier clearance;
   - guarded apply through `tools/v7-users-autoswitch --apply --verify`;
   - verification;
   - rollback readiness;
   - feedback materialization;
   - snapshot refresh;
   - closure/audit.
4. stop if any gate changes or becomes unknown;
5. never reselect users or targets after approval;
6. never create a new planner, governance owner, executor, feedback store or truth source.

## Why It Is Needed

Current UI and APIs expose preview/rehearsal surfaces and an approval intent action, but the live execution actions remain deliberately disabled or split across multiple operator/governance steps.

Therefore the operator cannot yet be reduced to exactly one Approve / Reject action.

