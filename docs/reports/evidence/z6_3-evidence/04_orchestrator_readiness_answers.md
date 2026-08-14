# Orchestrator Readiness Answers

## A. Can ownership consolidation happen mostly through existing components?

Yes.

The repo already has a strong partial runtime owner (`tools/v7-users-autoswitch`), scheduler (`systemd/v7-users-autoswitch.timer/service`), operator surface (`admin/v7-admin-api`), audit sink (`v7-audit-log`), rollback primitive (`v7-rollback-last-change`), and observability/closure surfaces.

## B. Can `tools/v7-users-autoswitch` become the runtime owner without creating a new orchestrator?

Yes.

It already owns the live autonomous path: plan, selected moves, restore-barrier enforcement, apply, verify, local rollback, and runtime state updates. Consolidation should reuse and extend this ownership rather than create a separate orchestrator.

## C. Can systemd remain scheduler-only?

Yes.

Systemd should remain a timer/service launcher. It should not own selected moves, barrier closure, execution outcome, rollback decision, or audit completion.

## D. Can Admin become operator surface only?

Yes.

Admin already has strong suitability for operator visibility, dry-run, proposal, preview contracts, closure, audit search, and controlled action surfaces. It is not the best primary live runtime owner because its execution contracts are explicitly preview-only and its mutating endpoints currently bypass those contracts.

## E. Can execution paths be unified without replacing components?

Yes, based on existing reality.

The low-level primitives can remain, but independent lifecycle authority should converge around the existing autoswitch runtime engine. This is an ownership conclusion, not an implementation design.

## F. Can rollback ownership be centralized around existing logic?

Mostly yes.

Movement rollback should align with `tools/v7-users-autoswitch` as runtime owner. Broad file/config rollback can keep `v7-rollback-last-change` as a primitive. Admin remains operator surface and audit/closure wrapper.

## G. Can lifecycle closure be added without introducing duplicate truth?

Yes, if closure reuses the existing Admin closure model and `v7-audit-log` sink, with runtime outcomes supplied by autoswitch. A new closure truth source would duplicate current closure/audit infrastructure.

## H. Largest ownership conflicts

1. Autonomous autoswitch apply versus Admin execution contracts.
2. Admin direct user-switch versus autoswitch selected-move authority.
3. CLI `v7-user-switch` versus governed lifecycle.
4. Restore-barrier enforcement in autoswitch versus fragmented barrier creation/closure.
5. Generic rollback versus contract-scoped rollback expectations.
6. Multiple audit/event writers without one audit-completion owner.
7. Persistent selected-move file readers versus in-process selected-move truth.
8. Draft planner timer as latent duplicate scheduler/planner path.

## I. Smallest changes required for consolidation

This audit does not implement or design them. The smallest ownership changes implied by the evidence are:

- keep `tools/v7-users-autoswitch` as primary runtime/execution owner candidate;
- keep systemd as scheduler-only;
- keep Admin as operator surface, closure surface, and visibility layer;
- keep `v7-audit-log` as canonical audit sink candidate;
- keep `v7-user-switch` and `v7-rollback-last-change` as primitives rather than lifecycle owners;
- demote sentinel execution capability to advisory/signal-only ownership;
- avoid treating persistent selected-move files as canonical live selected-move truth;
- assign restore-barrier lifecycle suitability to the runtime owner while preserving Admin evidence/closure support.

