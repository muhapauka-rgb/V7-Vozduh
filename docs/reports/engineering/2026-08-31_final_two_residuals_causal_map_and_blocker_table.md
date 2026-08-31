# V7 final two residuals — causal map and repair admission

Date: 2026-08-31 (MSK)
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Current fact base

The live ordinary recovery chain is functional and remains system-owned:
`v7-health.service -> Matrix -> affected scope -> Authority -> Planner -> Candidate -> Packet -> Lease -> Barrier -> v7-user-switch -> Core-primary -> route and required-service verification`.

The attached acceptance evidence remains separate and is not averaged:

| Sample | Measured result |
|---|---:|
| VLESS, first valid failure to obligation ready | 9.648 s |
| VLESS, first valid failure to execution lease | 14.205 s |
| Separate automatic three-member governed transaction | 41.827 s total; Apply + verification 39.037 s |

Fresh Runtime inspection at 2026-08-31 22:47 MSK found `v7-health.service=active`. VLESS has current failing Matrix observations (for example YouTube and Google timeouts) under the continuing current VLESS incident. This proves that a visible green/admin indication is not sufficient for profile eligibility.

The most recent current governed attempt was a different source (`awg0`) and stopped safely without a route mutation. It is useful only for decomposition, not as a recovery-success sample: its execution receipt shows a 23,799.776 ms `apply_and_verification` parent interval while its actual apply returned STOP_SAFE.

## Complete causal map available now

| Interval | Evidence | Status |
|---|---|---|
| first valid failure -> obligation ready | 9.648 s, supplied live sample | measured historical acceptance baseline |
| first valid failure -> execution lease | 14.205 s, supplied live sample | measured historical acceptance baseline |
| Matrix -> current attempt | current Matrix owns failure/currentness; next exact per-stage timing is not retained in the old compact receipt | needs bounded owner instrumentation on next sample |
| Planner/Authority/Packet/Lease/Barrier | latest receipt: Planner 1,183.944 ms; packet + lease 623.127 ms; feedback 350.086 ms | measured for the current STOP_SAFE attempt, not a success credit |
| Apply + required-service S11 | 39.037 s in the valid three-member sample | measured historical acceptance baseline; internal split was not preserved after the next Matrix refresh |
| Latest finalization tail | 23,651.096 ms: passive 12,218.749 ms + learning closure 11,345.156 ms | directly measured current Runtime receipt |

No unavailable clock has been fabricated. The next successful V7-owned sample must retain the full required map through global all-affected S11.

## Blocker table, sorted by expected gain

| Blocker | Residual | Existing owner | Observed delay | Mandatory before S11? | Avoidable? | Repair |
|---|---|---:|---:|---|---|---|
| Passive event consumption after apply | B | `v7-users-autoswitch.finalize_operation`; already has Matrix passive consumer | 12,218.749 ms | no | yes | omit duplicate synchronous finalization on the Runtime hot path; leave existing Matrix consumer as asynchronous reconciliation |
| Learning/trust/recommendation/closure materialization after apply | B | `v7-users-autoswitch.finalize_operation` | 11,345.156 ms | no | yes | mark it as non-critical deferred finalization on the Runtime hot path; route/service S11 remains unchanged |
| Full current-incident readiness path | A | existing Matrix / obligation / Authority / Planner owners | 9,648–14,205 ms | partly | unknown until next fully decomposed sample | preserve existing stage receipt and diagnose next live sample; no speculative changes before the measured P0 tail is removed |
| Stale prepared projection triggers full Planner fallback | A | Matrix prepared decision consumer | observed on latest STOP_SAFE; planner-side measured cost 336.649 ms | yes when stale | not a P0 in current receipt | retain bounded invalidation and measure it; do not weaken currentness |
| Repeated Core-primary verification per cohort member | B | existing Core-primary verifier | standalone check ~0.26 s, at most ~0.8 s for 3 members | yes, exact member evidence | partially | instrument; defer until P0/P1 tail removal is validated |

## Coherent repair block admitted

The first repair changes only finalization ordering for an already governed **ordinary service-failure Runtime hot path**. It preserves, before the caller receives success:

- route-writer mutation and canonical assignment;
- affected-cohort Core-primary commit;
- exact per-member route/kernel proof;
- required-service S11;
- rollback on failed verification;
- terminal audit reference, lease completion and execution-control finalization.

It defers only passive history reconciliation and learning/reporting work. No new owner, Planner, Matrix, queue, timer, registry, route writer or state source is introduced. The existing Matrix/health lifecycle remains the asynchronous consumer of those records.

## Next executable step

Implement this bounded ordering change, add a focused regression that proves S11 is retained while non-critical finalization is deferred, safe-deploy it, and then let a normal V7 event produce the next acceptance receipt. No client is moved by Engineering.

## Implementation and local verification

Implemented the admitted block in the existing owners:

- the Matrix hot-path flag is propagated only through the existing governed executor to an ordinary service-failure Planner apply;
- the Planner defers passive/learning only when every affected member has `SUCCESS` after required-service S11;
- terminal audit reference, lease finalization, execution-control close, rollback semantics and all route/service checks remain synchronous;
- an external operator CLI cannot request this ordering: the governed executor passes it only when the persistent Matrix Runtime environment is present;
- the existing cohort receipt now retains route-writer subspans, one affected-cohort Core-primary span and exact member route-verification spans for the next live sample.

Focused regressions: 2/2 passed. Full autoswitch policy suite: 237/237 passed. A combined broad regression command exposed three unrelated existing assertions in other suites; none refer to finalization ordering, the new flag, or the cohort timing receipt. They are retained as non-credit diagnostics and were not hidden or changed.

## Second residual A repair: one live Matrix consumer, not two

Fresh Runtime inspection after the first block found the ordinary detector
regularly exceeding its `3.5 s` cadence: recent completed `other_required`
passes were `3.7--5.6 s`, with repeated `PREVIOUS_INVOCATION_RUNNING` deadline
misses.  The source probe itself remains bounded; the avoidable boundary was a
second Matrix/Planner process that could be started by the detector after it
had already written a canonical profile failure, while the persistent health
owner was independently polling that same Matrix binding for the same live
recovery.

The repair keeps Matrix as the only writer and the health loop as the normal
Runtime caller.  Under the persistent-health environment, the detector now
only records the exact Matrix fact and returns; the running health owner reads
the same fresh binding within its existing `250 ms` bound and runs the one
loaded Matrix consumer.  The historical external wake remains unchanged for
non-persistent compatibility callers.  No route, user assignment, target,
Authority, Candidate, Packet, Lease, Barrier or verification behavior is
performed by the detector or changed by this repair.

Focused verification passes:

- the persistent-health detector leaves the source-bound Matrix fact for the
  parent and does not start a second consumer;
- the existing health-loop unit coverage still proves fresh exact binding,
  bounded parent polling and one-time parent consumption;
- whitespace validation passes.

This block is not yet production SLO evidence.  After safe deployment, the
normal V7 Runtime must produce the next real current failure transaction.  Its
receipt will retain the full timeline so the remaining mandatory work can be
classified from measured intervals rather than inferred from a later summary.

## Deployment and immediate Runtime observation

The second block was published as commit `7923987460cadd5a771a8206f4ea61628b471069`
and safely deployed as `deploy-z8-14-Updatesystem-7923987-20260831T232042`.
The deployed copies of `v7-egress-diagnose`, `v7-users-autoswitch`,
`v7-service-matrix-refresh-all`, and `v7-health-loop` have the same hashes as
their current local sources.  `v7-health.service` and `v7-admin-api.service`
are both active.

The immediately following normal Runtime cycles show the ordinary required
service role completing in `2.036--2.548 s`; the previous observed
`3.7--5.6 s` overshoots have not recurred in this observation window.  This is
operational evidence for removal of the duplicate consumer boundary, but it is
not yet a recovery-SLO credit because no customer was moved in the window.

At the observation point VLESS had zero enabled assigned users, so no new
VLESS recovery transaction existed to certify.  A separate current awg0
incident has nine affected assignments, but its existing advisory owner
returned `STOP_SAFE_NO_SAFE_TARGET`; its measured `3.593 s` planning span
therefore cannot be credited as a successful recovery or used to weaken target
eligibility.  The normal V7 caller retains this state and will retry only when
an owner-admitted target exists.

**Exact re-entry condition:** a fresh current Matrix profile-failure with an
ordinary affected scope and at least one owner-admitted target.  The already
deployed V7 health caller—not Engineering—must then produce the first new
receipt with the complete `T0 -> all affected S11` timeline.  If its measured
critical path still exceeds seven seconds, that receipt identifies the next
remaining mandatory span; no further speculative change is admitted before
then.

## Current detector peak measurement

A later normal observation showed that the ordinary detector is not uniformly
fast: although many passes remain near two seconds, some completed in
`9.641--11.989 s` and caused cadence misses.  The current diagnostic state
proves a bounded twelve-probe batch with no Matrix receiver invocation, but
did not separate the batch network wall time from post-probe canonical
handling.  No routing conclusion can be drawn from that aggregate.

The next compact diagnostic block therefore records, in the already-existing
detector state file only, three monotonic measurements: batch probe wall time,
post-probe processing wall time, and their total.  It does not change probe
membership, timeout, cadence, Matrix state, caller, eligibility, Authority or
any user effect.  Its focused batch regression and shell syntax validation
pass.  The next normal cycle will make the remaining peak either a measured
network/substrate limit or a concrete removable local processing span.
