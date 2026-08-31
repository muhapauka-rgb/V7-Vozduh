# V7 final post-fix bad-placement 7-second preflight

Date: 2026-08-31  
Mission: `V7_FINAL_POST_FIX_BAD_PLACEMENT_7S_EXECUTION_AND_SLO_CLOSURE`

## Result

`READY_FOR_LIVE_OPERATOR_PLACEMENT`.

The bounded fix for the interrupted ordinary recovery transaction is already
present in both the checked local source and the deployed Runtime.  The Runtime
now passes the Packet-bound committed `plan` explicitly into the ordinary
required-service evidence helper.  It therefore cannot reach Apply with an
undefined local `plan`; a missing committed plan now stops explicitly with
`committed_apply_plan_missing` before any route mutation.

No ordinary user, route, Matrix cadence, policy, Authority, or service setting
was changed during this preflight.

## Reconciliation

| Item | Evidence | Result |
|---|---|---|
| Fix commit | `e06cc728 Repair ordinary recovery apply handoff` | Present locally |
| Local route writer source | `tools/v7-users-autoswitch:10397` calls `_ordinary_service_failure_move_evidence(plan, move)` | Correct |
| Deployed route writer | `/usr/local/bin/v7-users-autoswitch:10397`, source SHA `107569ba…` matches local | Correct |
| Health Runtime | `v7-health.service` active | Ready |
| Admin Runtime | `v7-admin-api.service` active | Ready |

## Focused verification

Two bounded runs passed without a manual recovery transition:

1. **9/9, 0.320 s** — current profile failure, fresh Matrix mode, stale
   secondary evidence handling, bounded ordinary cohort, missing-plan stop,
   source/target drift rejection, Packet/Barrier handoff integrity.
2. **9/9, 4.995 s** — fresh exact Matrix failure, live Runtime consumer
   admission, owner-only release, Packet/Lease/Apply identity, target drift,
   certification reservation isolation, event-driven successor and STOP_SAFE
   Authority boundary.

The earlier broad historical Polygon suite was intentionally terminated before
completion because it was not a bounded test of this fix; it receives no
acceptance credit.

## Live acceptance boundary

The only remaining setup action is external and deliberately operator-owned:
place the selected acceptance client or a compatible 2–4 member group on the
currently unsuitable VLESS source through the normal Admin UI.  Codex must not
perform that move or start the recovery transaction.

After placement, the live V7 caller must independently produce:

`FIRST_VALID_FAILURE_OBSERVATION -> Matrix -> affected scope -> Authority -> Planner -> Candidate -> Packet -> Lease -> Barrier -> Apply -> S11`.

The report must retain every measured sample.  Acceptance is only met when
`FIRST_VALID_FAILURE_OBSERVATION -> GLOBAL_ALL_AFFECTED_RECOVERED <= 7 s`, with
repeat P95 at most 7 s and no valid sample over 8 s.  Placement-to-observation
and placement-to-completion remain diagnostic timings, not substitutes for the
seven-second bound.

## Next action

Wait for the operator's normal Admin-UI placement of the next acceptance
client(s) onto VLESS, then observe the unassisted Runtime transaction and
record the complete causal timing table.
