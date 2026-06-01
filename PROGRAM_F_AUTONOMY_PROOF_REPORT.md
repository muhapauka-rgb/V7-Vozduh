# Program F Autonomy Proof Report

Date: 2026-06-01
Project: V7 Vozduh
Program: F
Status: NOT_READY

## 1. Reality Audit

Fresh read-only evidence was collected. Current enabled users remain:

- execution target: `10`
- `awg0`: `3`
- `awg3`: `3`
- `vless`: `2`

The current proposal remains:

- `10.7.0.16`
- `vless -> awg3`
- rollback: `v7-user-switch 10.7.0.16 vless`
- budget: `1`

No movement was executed.

## 2. Conflict Audit

Existing implementations were reused:

- `v7-users-autoswitch`
- `v7-autoswitch-proposal-cap`
- `v7-autoswitch-safety-review`
- `v7-route-movement-preview`
- runtime checkers

No duplicate execution, approval, rollback, or autonomy system was created.

## 3. Truth Source Audit

Truth sources are clear for proposal, movement, rollback, verification, and observation.

The approval truth source is missing: no approved packet was provided.

## 4. Runtime Audit

Fresh runtime evidence:

- killswitch: OK
- user route check: OK
- runtime contract: OK
- safety: OK
- capacity: healthy

Wider observability blockers remain:

- channels unstable
- direct routing unknown
- routing degraded
- services blocked
- trusted RU unknown

## 5. Operator Approved Autoswitch

Not executed.

Reason: Program F says "Use approved packet", but the context still says `explicit approval pending`, and no exact approval packet was supplied.

## 6. Autonomous Execution

Not executed.

Reason: Stop Gate 1 blocked autonomy.

## 7. Reliability

Not certified.

No autonomous execution occurred, so repeated bounded autonomy cannot be proven.

## 8. Rollback Reliability

Rollback preview is ready:

`v7-user-switch 10.7.0.16 vless`

Rollback reliability is not fully certified because no forward approved movement occurred.

## 9. Fail Closed

Program F failed closed correctly on missing approval.

No packet bypass was performed.

## 10. Certification

Final verdict: NOT_READY

## 11. Remaining Risks

- approved packet missing
- runtime-installed D2 safety parser fix not deployed
- wider observability blockers remain
- live replay/expired/stale packet denial not exercised
- rollback reliability not proven by live rollback

## 12. Recommendation For Program G

Do not start Program G.

First provide exact operator approval for Program F Stage 1 or create an explicit approval packet artifact naming:

- user `10.7.0.16`
- movement `vless -> awg3`
- budget `1`
- rollback `v7-user-switch 10.7.0.16 vless`
- required pre/post checks

## Required Verdicts

- operator_autoswitch_certified=false
- autonomous_execution_successful=false
- autonomy_reliable=false
- rollback_reliable=false
- replay_protection_verified=false
- fail_closed_verified=true
- bounded_autonomy_certified=false
- safe_to_continue_to_program_g=false

## Safety Verdict

- autonomous_budget<=1
- scope_expanded=false
- autoswitch_apply_outside_packet=false
- routing_changed_outside_scope=false
- deploy_performed=false
- users_moved=false
- autoswitch_apply_run=false

