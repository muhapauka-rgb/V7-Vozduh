# OA.1 Automation Candidate Audit

| Operator action | Classification | Reason |
|---|---|---|
| Read planner output | PREPARE_AUTOMATICALLY | planner already produces candidates and selected moves |
| Choose candidate from planner output | APPROVE_ONLY | system can propose; operator should accept/reject |
| Generate packet evidence | PREPARE_AUTOMATICALLY | `tools/v7-operator-execution-packet` already owns packet generation |
| Review blast radius | PREPARE_AUTOMATICALLY | selected move count, allowed users and rollback manifest are present |
| Review trust/risk | PREPARE_AUTOMATICALLY | decision surface exposes trust evolution and confidence |
| Write restore barrier clearance | APPROVE_ONLY | system can validate/recheck, but live clearance is a governed runtime action |
| Invoke guarded apply | APPROVE_ONLY | should remain existing executor, triggered only after approval |
| Verification | PREPARE_AUTOMATICALLY | guarded apply verifies and route checks exist |
| Rollback decision | KEEP_MANUAL for apply, PREPARE_AUTOMATICALLY for readiness | dry-run can be prepared; actual rollback apply needs operator/governance |
| Feedback materialization | PREPARE_AUTOMATICALLY after verified execution | FB.2 proved canonical materialization works |
| Operator-free execution | UNSAFE_TO_AUTOMATE | explicitly not certified |
| New planner/governance/executor | UNSAFE_TO_AUTOMATE | forbidden duplicate authority |

## Result

Operator Approved Autonomy is architecturally close, but not yet productized as one bounded approval action.

