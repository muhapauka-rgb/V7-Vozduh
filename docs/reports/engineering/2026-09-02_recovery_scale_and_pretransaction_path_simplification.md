# Recovery scale-cost and pretransaction-path simplification — 2026-09-02

## Scope and decision

This report records one bounded Recovery Stability repair.  It changes neither
Matrix ownership, Planner/Authority semantics, route writer, S11, cadence,
timers nor the automatic caller.  V7 remains the only operational recovery
controller; this work only makes its existing Matrix invocation avoid proven
duplicate preparation.

The Program and OMP now carry one non-duplicating specialization,
`RECOVERY_SIMULTANEOUS_FAILURE_SCALE_COST_LAW`.  It is explicitly subordinate
to the existing Simplification First and Production Scale First laws.  It adds
no owner, queue, cache, registry, state store, Scheduler or parallel contract.

## Measured current cause

The live ordinary VLESS transaction observed on 2026-09-02 completed through
the normal V7 Runtime chain and moved one user.  Its Matrix receipt showed
that preparation was repeated before the governed transaction:

| Existing stage | Observed time | Finding |
| --- | ---: | --- |
| current source/L3 lookup | 8,922 ms | current Matrix scope plus newest durable event resolution |
| fresh advisory attempt | bounded at 5 s | a new Python process could miss its fast deadline before returning an obligation |
| passive consumer | 3,300 ms | historical/passive reconciliation ran because the fresh result was unavailable |
| post-passive source/L3 lookup | 8,224 ms | same current scope and handoff were reconstructed again after passive work |
| later advisory process | 3,761 ms outer Matrix span; internal work about 1.0–1.5 s | a second process invocation eventually materialized the same type of obligation |

This is a P0 duplication diagnosis with a concrete mechanism, not an inference
from elapsed time: the scope reader enumerated many historical occurrences of
each still-current incident, and the fast advisory path could time out during a
separate interpreter startup.  The first and second L3 reads remain distinct
where passive reconciliation has run, because that consumer can lawfully alter
the current handoff; they are not merged across that boundary.

## Implemented repair

1. `current_failed_source_scope` now asks the existing append-only JSONL owner
   for at most eight newest textual candidates per active Matrix incident.
   The existing exact JSON fields (`channel`, incident identity and current
   Matrix state) are still checked by the caller.  A false textual candidate
   can only produce no action and retain fail-closed behavior.
2. The existing fresh runtime-profile advisory owner is invoked in the current
   Matrix process when an exact source scope is already present.  It is the
   same `v7-users-autoswitch` entrypoint, with the same files, owner and
   current-data checks.  It has no Candidate/Packet/Lease/route authority.
   Any load/entrypoint failure returns to the existing bounded subprocess
   fallback.
3. Process-local reuse is confined to one Matrix invocation.  It carries no
   Planner state, no cross-event cache and no persisted projection.  Every
   Authority/policy, Matrix/source/scope and target invalidator remains
   rechecked by the existing later consumer and before apply/S11.

## Scale-cost gate

The applicable 100-source/1000-user structural cases reuse the existing
Polygon/future-scale facilities:

| Case | Required result | Current evidence |
| --- | --- | --- |
| A: many healthy sources, one affected source | source-bounded work only | Matrix incident marker and source scope are bounded |
| B: one failed source, many affected users | one source contract, no cross-source scan | existing 10k/one-source prepared projection test |
| C: many independent failed sources | no historical full-ledger expansion per source | newest-per-marker reader and existing full-scale tournament |
| D: profile partitions | only profile-required source may enter fresh advisory | existing runtime profile handoff tests |
| E: concurrent bindings | no cross-source reuse and no manual recovery | source/incident/scope fingerprint gates and Matrix caller provenance |

This is a structural/rejection check, not a claim that the current 2-vCPU
server has been capacity-certified for production at those numbers.

## Verification

- syntax compilation: PASS;
- new newest-per-marker exact-reader test: PASS;
- new in-process existing-advisory-owner test: PASS;
- `test_v5_3_n9_full_scale_tournament` plus
  `test_v5_3_pre_ready_and_staggered_deep`: 20 PASS;
- `test_service_failure_automation_evolution`: focused regression PASS;
- broad `test_service_failure_episode`: one pre-existing, unrelated failure:
  `test_source_bounded_planning_filters_before_decision_construction` asserts
  an obsolete single-line spelling and does not exercise this repair.  It was
  left unchanged and receives no acceptance credit.

## Deployment and re-entry

The code is to be published through the existing safe-deploy owner only.  A
valid runtime result requires a normal V7 health-originated event, Matrix
receipt, automatic governed execution and S11; no Codex-triggered recovery is
evidence.  The first post-deploy receipt must compare the exact pretransaction
spans above and show whether the two former high-cost mechanisms collapsed.

Next step: safe deploy this frozen repair, reconcile code/Runtime hashes, then
observe one naturally invoked automatic Matrix recovery.  If a source/scope or
Authority invalidator changes, V7 must re-read rather than reuse the prior
result.
