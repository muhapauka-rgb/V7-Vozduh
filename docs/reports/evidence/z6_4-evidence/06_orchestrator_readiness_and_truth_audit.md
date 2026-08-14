# Orchestrator Readiness and Truth Source Audit

## A. Can ownership consolidation alone solve most current conflicts?

Yes, most conflicts are ownership ambiguity rather than missing primitives.

Ownership consolidation can address:

- duplicate selected-move authority;
- Admin/manual execution ambiguity;
- restore-barrier lifecycle ambiguity;
- rollback lifecycle ambiguity;
- audit/closure ambiguity.

It does not by itself implement new wiring or guards.

## B. How much of Runtime Orchestrator already exists?

A partial orchestrator exists in `tools/v7-users-autoswitch`.

Already present:

- planner;
- selected moves;
- restore-barrier enforcement;
- runtime apply;
- verification;
- local movement rollback;
- safety/reconnect/load state writes;
- timer-driven autonomous execution through systemd.

Missing:

- unified closure;
- canonical audit completion for every runtime cycle;
- global admission/recheck across manual and autonomous paths;
- restore-barrier creation/clearance/closure ownership;
- contract-connected execution path;
- authority reduction around direct/manual paths.

## C. Percentage of orchestrator functionality already exists

Estimated existing functionality: 65%.

Rationale:

- Core runtime execution loop exists.
- Planner/selected-move/execution/verification/local rollback are real.
- Major missing areas are ownership closure, unified admission, canonical audit completion, and manual bypass containment.

## D. Ownership gaps remaining

- restore-barrier creation and closure ownership;
- lifecycle closure truth;
- audit completion for autonomous cycles;
- direct Admin/CLI movement authority boundaries;
- generic rollback ownership boundary;
- execution contract connection boundary.

## E. Lifecycle gaps remaining

- no single operation terminal state;
- no guaranteed final audit event for every runtime cycle;
- no universal runtime recheck for manual paths;
- no unified rollback completion declaration;
- no canonical selected-move archive tied to closure.

## F. Truth-source gaps remaining

- selected moves: in-process truth versus persistent readers;
- closure: Admin closure records versus historical reports;
- rollback: runtime rollback versus generic rollback outputs;
- audit: event sink versus report-only closeout;
- barrier: file state versus lifecycle owner.

## G. Closure gaps remaining

- no formal rule for COMPLETE/FAILED/ROLLED_BACK/CANCELLED/EXPIRED across all paths;
- no required link between runtime outcome, audit event, and closure record;
- autonomous cycles can finish without closure record;
- rollback completion and audit completion are not a single lifecycle state.

## H. Smallest implementation required after this design

This is not an implementation proposal, but the smallest future implementation scope is ownership wiring around existing components:

- preserve autoswitch as the runtime owner;
- route execution outcomes to existing audit/closure surfaces;
- constrain manual/direct paths into operator surface or break-glass roles;
- define restore-barrier lifecycle records using existing Admin closure/audit surfaces and autoswitch validation;
- keep systemd as scheduler-only;
- avoid any new orchestrator, scheduler, planner, execution engine, rollback engine, audit sink, or closure truth source.

## Truth Source Audit

Proposed ownership model creates no duplicate truth sources:

- Runtime truth: `tools/v7-users-autoswitch`.
- Scheduler truth: systemd timer/service.
- Policy truth: policy files.
- Signal truth: specialized signal files.
- Audit truth: `v7-audit-log`.
- Closure truth: Admin closure records/operator observability.

Proposed ownership model creates no duplicate planners:

- Planner remains `tools/v7-users-autoswitch`.
- Draft planner remains legacy/do-not-touch.

Proposed ownership model creates no duplicate execution paths:

- Execution ownership belongs to autoswitch.
- Admin/CLI paths become surfaces/primitives/break-glass, not primary execution owners.

Proposed ownership model creates no duplicate rollback paths:

- Movement rollback ownership belongs to autoswitch.
- Generic rollback remains primitive.

Proposed ownership model creates no duplicate closure paths:

- Closure truth belongs to Admin closure records/operator observability.
- Reports become historical evidence only.

Proposed ownership model creates no duplicate audit sinks:

- `v7-audit-log` remains canonical.
- Other logs/events are supplemental evidence.

