# OA.1 Operator Decision Audit

Project: V7 Vozduh
Date: 2026-06-12

## Recent Certified Executions

| Source | What happened | Operator / governance decision |
|---|---|---|
| EXEC.2_4 | one user moved `10.7.0.5 awg3 -> vless` | operator/governance selected fresh planner candidate, created packet, wrote restore barrier clearance, invoked governed apply, verified, prepared rollback dry-run |
| EXEC.5_6 Stage A | 2 users moved | operator/governance repeated fresh packet -> barrier -> apply -> verify -> rollback dry-run |
| EXEC.5_6 Stage B | 5 users moved | same governed chain |
| EXEC.5_6 Stage D | current full planner batch, 8 users moved | same governed chain |
| FB.2 | 16 execution outcomes materialized into feedback stores | operator/governance materialized feedback and refreshed snapshots; no users moved |

## What Operator Actually Decided

| Area | Operator decided |
|---|---|
| Packet | which fresh planner output to package and execute |
| Restore barrier | whether to write generation-bound clearance |
| Apply | whether to run guarded apply |
| Rollback | whether rollback was needed; in certified executions rollback was not needed, but rollback packet/dry-run was prepared |
| Feedback | whether to materialize post-execution feedback records |

## What Operator Did Not Decide Manually

| Area | Already machine-derived |
|---|---|
| Candidate scoring | planner and trust/service/snapshot evidence |
| Selected move hashes | planner/governance contract |
| Runtime recheck fields | `admin_core/operator_execution.py` |
| Rollback manifest structure | packet/rollback generator |
| Verification mechanics | guarded apply verifier and route checks |
| Feedback schemas | `admin_core/operator_execution_feedback.py` |

## Conclusion

Operator is already mostly deciding permission, not doing raw engineering.

The remaining gap is that permission is still spread across several governed steps instead of one final Approve / Reject boundary.

