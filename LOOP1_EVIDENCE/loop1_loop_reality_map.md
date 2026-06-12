# LOOP.1 Loop Reality Map

Project: V7 Vozduh
Date: 2026-06-12
Mode: read-only certification from existing reports, evidence and code owners.

## Full Existing Cycle

| Stage | Owner | Inputs | Outputs | Storage / Evidence | Authority | Status |
|---|---|---|---|---|---|---|
| Observe | production runtime state, service matrix, registry readers, intelligence snapshots | users registry, egress registry, service state, snapshots | runtime/planner-visible state | `/opt/v7/egress/state`, intelligence snapshots, admin runtime views | read-only | CERTIFIED |
| Analyze | `admin_core/intelligence_workers.py`, `admin_core/intelligence_platform.py`, CTR advisory modules | service scores, trust stores, execution events, recommendation records | trust evolution, suitability, service confidence, decision evidence | `trust-evolution-summaries`, decision surface | advisory | CERTIFIED |
| Plan | `tools/v7-users-autoswitch` | runtime state, intelligence snapshots, trust/planner evidence | candidate moves, selected moves before/after governance gate | planner JSON, `selected_moves` surfaces | planner authority | CERTIFIED |
| Governance | `v7-operator-execution-packet`, `admin_core/operator_execution.py` | selected moves, planner generation, runtime hashes, constraints | approval packet, approved plan lock, restore barrier clearance, rollback manifest | packet evidence, restore barrier file, lifecycle/audit records | operator/governance authority | CERTIFIED |
| Execute | `tools/v7-users-autoswitch --mode guarded --apply --verify` | approved selected moves, restore barrier, allowed users/targets | real user movement, apply result | EXEC.2_4 / EXEC.5_6 apply evidence | execution authority | CERTIFIED |
| Verify | guarded apply verifier, route check, registry checks, truth/convergence checks | apply result and runtime state | verification PASS/FAIL, rollback decision | route check files, truth/convergence evidence | verification authority | CERTIFIED |
| Feedback | `admin_core/operator_execution_feedback.py`, `admin/v7-admin-api` `/api/actions/execution-feedback-materialize` | verified execution outcome | outcome, trust, prediction, recommendation, closure records | `execution-events.jsonl`, `runtime-trust.jsonl`, `proposal-records.jsonl`, `closure-records.jsonl` | append-only feedback materialization | CERTIFIED |
| Trust Update | `v7-intelligence-snapshot-refresh`, intelligence workers | canonical feedback stores | updated trust/prediction/service/suitability source hashes | FB2 before/after trust comparison | intelligence snapshot refresh | CERTIFIED |
| Future Decisions | `tools/v7-users-autoswitch`, admin decision surface | refreshed trust evolution snapshots | planner-facing evidence and future dry-run decisions | decision surface / planner consumption evidence | advisory/planner input, not autonomous execution | CERTIFIED |
| Observe Again | planner refresh dry-run and runtime views | updated state after movement and feedback | new observation cycle | FB2 planner refresh and runtime convergence evidence | read-only unless governed action starts | CERTIFIED |

## Ownership Conclusion

No new loop owner is needed.

The loop already uses existing owners:

- planner owner: `tools/v7-users-autoswitch`
- governance owner: `v7-operator-execution-packet` + `admin_core/operator_execution.py`
- restore barrier owner: `admin_core/operator_execution.py`
- execution owner: `tools/v7-users-autoswitch --apply --verify`
- feedback owner: `admin_core/operator_execution_feedback.py` + `admin/v7-admin-api`
- trust/snapshot owner: `v7-intelligence-snapshot-refresh` + `admin_core/intelligence_workers.py`

