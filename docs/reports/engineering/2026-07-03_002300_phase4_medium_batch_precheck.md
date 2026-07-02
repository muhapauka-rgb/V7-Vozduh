# Phase 4 MEDIUM_BATCH Certification Precheck

Timestamp: 2026-07-03T00:23:00+0700

Mode: Controlled Production Certification Program execution

Canonical source: `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`

## Summary

Phase 4 was started after Phase 3 reached PASS.

Phase 4 terminal state is:

`HOLD`

No production movement was executed during this precheck.

The current active failed-source incident has only three remaining enabled affected users on `openvpn-1779388847-d2ad7c`. The canonical MEDIUM_BATCH stage requires at least ten users on the incident source, and the program owner mapping still marks the "fewer remaining users than stage budget" certification rule as `NEEDED_OWNER_DECISION`.

Running `--max-users 10` against the current incident would not prove a ten-user MEDIUM_BATCH capability. It would only move the remaining three users or close the incident, producing useful production restoration but insufficient Stage 2 certification evidence.

## Current Phase

`PHASE4_MEDIUM_BATCH_CERTIFICATION`

## Terminal State

`HOLD`

## Canonical Evidence

The canonical batch ladder defines:

| Stage | Authority class | Maximum users |
| --- | --- | --- |
| Stage 2 | MEDIUM_BATCH | 10 |

The stage certification matrix defines MEDIUM_BATCH entry as:

- SMALL_BATCH certified;
- ten certification users on incident source;
- Authority allows MEDIUM_BATCH.

It also defines required users as:

`At least 10`

The owner mapping contains:

| Item | Owner | Status |
| --- | --- | --- |
| Fewer remaining users than stage budget | Planner / Authority / OMP policy owners | `NEEDED_OWNER_DECISION` |

## Production Evidence

Latest Phase 3 production certification moved five real users through the existing governed L3 path:

| Field | Value |
| --- | --- |
| final_verdict | `L3_PRODUCTION_PROVEN` |
| transaction_status | `COMPLETED` |
| users_moved | `5` |
| verification_result | `PASS` |
| rollback_result | `NOT_REQUIRED` |
| operation_terminal_state | `APPLIED` |
| operation_terminal_reason | `selected_moves_applied` |
| requested_max_users | `5` |
| authorized_l3_budget | `25` |
| authority_class | `POOL` |

Moved users:

- `10.7.0.6`
- `10.7.0.8`
- `10.7.0.9`
- `10.7.0.10`
- `10.7.0.11`

Post-run remaining users on failed source:

- `10.7.0.12`
- `10.7.0.13`
- `10.7.0.15`

Remaining count:

`3`

Incident status:

`OPEN`

Incident source:

`openvpn-1779388847-d2ad7c`

## Why Phase 4 Did Not Execute Runtime Apply

Phase 4 is a certification stage, not a generic restoration command.

The current production state cannot produce the required Stage 2 evidence because:

- MEDIUM_BATCH requires at least ten same-incident users.
- Current same-incident remaining affected users are three.
- Synthetic users are forbidden by Reality First.
- Switching to another execution or incident is forbidden by Candidate/Object Continuity.
- The program has not yet received an owner decision that fewer remaining users can certify MEDIUM_BATCH.

Therefore Runtime Apply was not invoked for Phase 4.

## Capability State

| Capability | State |
| --- | --- |
| CANARY | `CERTIFIED` |
| SMALL_BATCH | `CERTIFIED` |
| MEDIUM_BATCH | `HOLD` |
| LARGE_BATCH | `NOT_CERTIFIED` |
| XLARGE_BATCH | `NOT_CERTIFIED` |
| FULL_INCIDENT | `NOT_CERTIFIED` |

## Automation Audit

Manual action:

Read-only Phase 4 precheck.

Why manual:

The certification program does not yet have a single governed certification pipeline command that evaluates phase entry, current production reality, owner mapping, and terminal phase state.

Classification:

`BLOCKED_BY_FUTURE_CAPABILITY`

Automation candidate:

`CONTROLLED_CERTIFICATION_PHASE_EXECUTION_PIPELINE`

Automation debt delta:

`created=1; closed=1; remaining_unclassified=0`

## Workflow Audit

Workflow:

Phase transition precheck after Phase 3 PASS.

Why workflow exists:

Phase execution currently requires manual reading of the canonical program, current production evidence, Current Program State, and engineering reports.

Pipeline candidate:

`CONTROLLED_CERTIFICATION_PHASE_EXECUTION_PIPELINE`

Workflow debt delta:

`created=1; closed=1; remaining_unclassified=0`

## Synchronization Debt

Current Program State must be updated to reflect:

- Phase 4 terminal state `HOLD`;
- current capability state remains `SMALL_BATCH_CERTIFIED`;
- MEDIUM_BATCH requires either a future real incident with at least ten same-incident users or an explicit owner decision for fewer remaining users than stage budget.

Synchronization classification:

`SYNCHRONIZED_BY_THIS_REPORT`

## Root Cause

This is not an implementation defect.

Root cause:

`INSUFFICIENT_REAL_SAME_INCIDENT_USERS_FOR_MEDIUM_BATCH_CERTIFICATION`

Owner:

`Controlled Production Certification Program` with unresolved policy ownership assigned to Planner / Authority / OMP for the fewer-remaining-users-than-stage-budget rule.

## Required Resolution

Exactly one of the following is required before Phase 4 can proceed:

1. A real or controlled production incident with at least ten eligible affected users on the same `incident_source`.
2. An explicit Planner / Authority / OMP owner decision that fewer remaining users than the stage budget may certify MEDIUM_BATCH, including exact pass criteria and safety semantics.

Until then:

- Do not run MEDIUM_BATCH as a certification claim.
- Do not switch to another execution.
- Do not synthesize users.
- Do not create a new certification path.
- Do not promote to LARGE_BATCH.

## Final Phase Result

Current Phase:

`PHASE4_MEDIUM_BATCH_CERTIFICATION`

Terminal State:

`HOLD`

Evidence Produced:

- Phase 4 canonical entry check;
- production reality comparison;
- owner mapping check;
- Automation Audit;
- Workflow Audit;
- Current Program State synchronization requirement.

Current Capability State:

`SMALL_BATCH_CERTIFIED`

Next Phase:

`PHASE4_MEDIUM_BATCH_CERTIFICATION_RETRY_AFTER_REAL_EVIDENCE_OR_OWNER_DECISION`
