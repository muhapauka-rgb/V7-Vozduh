# LOOP.1 Automation Gap Audit

| Stage | Current Mode | Why |
|---|---|---|
| Observe | AUTOMATIC / SEMI_AUTOMATIC | Runtime and snapshots can be read automatically; refresh may be explicitly triggered. |
| Analyze | AUTOMATIC | Intelligence workers and decision surfaces compute evidence from existing stores. |
| Plan | AUTOMATIC for dry-run, GOVERNED for movement | Planner can produce candidates and selected moves, but movement remains gated. |
| Approval packet | SEMI_AUTOMATIC | Packet can be generated, but approval remains operator/governance-controlled. |
| Restore barrier | SEMI_AUTOMATIC | Recheck and clearance are canonical, but writing clearance is a governed runtime action. |
| Execute | MANUAL / OPERATOR-GOVERNED | `--apply --verify` requires explicit governed action. No autonomous apply is enabled. |
| Verify | AUTOMATIC once execution starts | Guarded apply runs verification, and route/truth checks are available. |
| Rollback readiness | AUTOMATIC dry-run, MANUAL apply | Rollback packet and dry-run are certified; rollback apply remains explicit. |
| Feedback materialization | SEMI_AUTOMATIC | Canonical endpoint exists and works; latest closure required an explicit FB.2 step. |
| Trust update | SEMI_AUTOMATIC | Snapshot refresh can update trust/planner evidence, but refresh is explicitly triggered in the certified path. |
| Future decisions | AUTOMATIC / ADVISORY | Planner consumes updated evidence, but does not gain execution authority from it. |

## If No Human Intervenes

Today V7 can go this far without human approval:

`observe -> analyze -> plan/dry-run -> advisory evidence -> preview packet/restore/feedback surfaces`

Current hard stop:

`governed runtime action`

The system does not autonomously:

- approve packets,
- write restore barrier clearance for live movement,
- run apply,
- apply rollback,
- promote authority,
- enable autonomy.

