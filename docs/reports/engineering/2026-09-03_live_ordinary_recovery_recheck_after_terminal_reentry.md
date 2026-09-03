# V7 live ordinary recovery recheck after terminal re-entry

## Scope

Repeated observation and repair of a real mixed ordinary/certification
bad-placement recovery through the live V7 Runtime. Codex changed generic
implementation only. It did not choose a user or target, invoke the route
writer, create execution objects, or manually advance the transaction.

## Final result

- The live Runtime automatically moved `10.7.0.6` from failed `vless` to the
  Planner-selected `awg0`.
- Receipt: `action_attempted=true`, `action_completed=true`,
  `runtime_mutation_performed=true`, `users_moved=1`.
- Registry, assignment, and Core-primary routing converged on `awg0`.
- Whole-system verification: `V7_USER_ROUTE_CHECK=OK` (`RC=0`).
- `v7-health.service`: active.
- Functional automatic recovery: **PASS**.
- Binding `T0 -> ALL_AFFECTED_RECOVERED <= 7 s`: **FAIL**.

## Final post-fix monotonic timing

| Interval | Duration |
|---|---:|
| T0 -> consumer start | 0.391 s |
| consumer execution | 32.318 s |
| T0 -> consumer complete | 32.710 s |
| Planner | 1.827 s |
| Packet and Lease | 0.228 s |
| Restore Barrier | 0.213 s |
| Apply and verification | 7.474 s |
| Feedback and learning | 0.146 s |
| Timed governed stages total | 9.888 s |
| Consumer time outside timed governed stages | approximately 22.430 s |

Nested Apply evidence:

- route writer and low-level mutation: 3.410 s;
- route visibility verification: 0.420 s;
- required-service verification: 1.909 s;
- Planner initialization: 0.571 s.

The final live event is therefore functionally correct but is not 7-second
SLO acceptance evidence.

## Exact generic defects consumed

1. Simultaneous failures had been collapsed into a source-less aggregate
   handoff, causing `approved_plan_lock_incident_source_mismatch`. The health
   owner now preserves one exact source binding per current failed source.
2. An ordinary user without an explicit preference row was treated as having
   an empty profile by the advisory consumer, while health/Planner/S11 used
   the canonical default profile. The consumer now distinguishes an absent
   row from an explicitly empty row.
3. A terminal empty direct handoff could bypass the fresh advisory/re-entry
   owner. Direct execution now requires a positive current affected and
   unresolved scope.
4. On a mixed failed source, the ordinary L3 denominator and ordinary Planner
   cohort reabsorbed a certification identity. Matrix correctly owned
   `ordinary=1` and `certification=1`, while L3 produced a legacy scope of 2,
   causing `service_failure_obligation_scope_fingerprint_mismatch`. Ordinary
   partial-service and whole-channel recovery now preserve the Matrix
   partition; certification identities remain with their existing controlled
   reservation/operation owner.

No new owner, queue, timer, watcher, registry, Planner, route writer, or truth
source was introduced.

## Verification and provenance

- Health-loop focused regression: 38/38 PASS.
- Mixed-scope/re-entry focused regression: 5/5 PASS.
- Operator-induced handoff regression: 17/17 PASS.
- Current source commits, all published and safe-deployed:
  `e417c741`, `fd8ab649`, `4c0b4f7d`, `8f826744`, `f4393844`,
  `599d5247`, `96958569`.
- Final deployed commit: `969585693a80f6626334e79f1e239751b6d7da12`.
- Final deployed autoswitch hash:
  `27a75b7347d7188c8d2d5fa3e3ff1875f8d64875704ff8d72db23c37dbe4a2c1`.
- Full route verification after the automatic move: PASS, including
  `10.7.0.5`, `10.7.0.6`, and `10.7.0.127`.

## Verdict

`LIVE_AUTOMATIC_RECOVERY_FUNCTIONAL = PASS`

`LIVE_AUTOMATIC_RECOVERY_PROVENANCE = LIVE_V7_RUNTIME_ONLY`

`LIVE_AUTOMATIC_RECOVERY_7S_SLO = FAIL`

`CURRENT_DOMINANT_RESIDUAL = PRE_GOVERNED_CONSUMER_WORK_PLUS_APPLY_VERIFICATION`

The correctness blocker exposed by this live mixed-source case is consumed.
The next frontier is bounded latency reduction/attribution; this report does
not claim the 7-second Program SLO complete.

## Fresh repeated observation

A later read-only refresh of the same live admin owners showed:

- `10.7.0.5` and `10.7.0.6` remain on `awg0`;
- `10.7.0.125`, `10.7.0.126`, and `10.7.0.127` remain on `awg0`;
- `vless` has two current profiles: `10.7.0.7`, explicitly paused by an
  administrator, and `10.7.0.16` (`Митяй`);
- the last confirmed route mutation remains the automatic
  `10.7.0.6: vless -> awg0` event at
  `2026-09-03T21:30:27.654605+00:00`;
- subsequent automatic operations
  `runtime_autoswitch_8a5af74c65593265adf687d3` at
  `2026-09-03T21:35:24.059053+00:00` and
  `runtime_autoswitch_df461632d11733d2e535eba9` at
  `2026-09-03T21:36:44.786167+00:00` were `DENIED`;
- no later successful user route mutation was visible in the current log.

Therefore the repeated observation does not establish stable consecutive
automatic recovery. The single functional PASS remains valid, but the current
reliability verdict is:

`REPEATED_AUTOMATIC_RECOVERY_STABILITY = NOT_PROVEN`

`LATEST_AUTOMATIC_ATTEMPTS = DENIED`
