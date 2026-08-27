# N10 bounded production consumption and N11 timer/L3 closure

Date: 2026-08-27

## Scope and decision

This is one continuation of `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`, not a new Mission or owner.  N10 bounded production was executed through the existing Matrix, Authority, Planner, Candidate, Packet, Lease, Barrier, `v7-user-switch`, Core-primary and S11 owners.  N11 then closed two proven replacement gaps: historical N10 outcomes leaking into L3 emergency feedback and three superseded standalone timer wake paths.

## N10 bounded-production evidence

Fresh owner selection admitted the exact four-member ordinary cohort `10.0.0.3`, `10.0.0.6`, `10.7.0.10`, `10.7.0.11`, from `awg3`.  The Planner selected `awg0`; no source, target or identity was manually substituted.

- Authority request: `accauth_r1_3ed7fbdefcbda17f10fac344`.
- One-use contract: `acc_36932a52907e060ca57c3c75`.
- Operation: `runtime_autoswitch_dfdbdaffe630b14920fd0504`.
- Packet: `pkt_ad8fb5543aff431d2fa647a0`.
- All four serial route writes, exact route/kernel verifications and service/path S11 checks returned success.
- The single affected-cohort Core-primary commit passed; the whole-system verifier later returned `CORE_PRIMARY_VERIFY_PASS`.
- The resulting checkpoint is `SUCCESS`; its closure obligation is `CONSUMED_BY_EXISTING_CLOSURE_OWNER`.
- No outside member was included and no rollback was required.

The initial attempt stopped safely before routing because obsolete recovered-episode identifiers changed an N10 source generation.  Commit `a5e8f9f2` made the generation depend on current source health while retaining invalidation for a current non-healthy state.  The fresh contract was then issued and consumed normally.

## N11 changes

Commit `25c81a6e6522a95891b8b2504d6a611fb60e2754`:

1. Rebuilds the existing L3 capability read projection from the existing Authority request-to-consumption lineage.  Exactly N10-tagged historical operations are excluded from L3 emergency feedback aggregation; their immutable audit and evidence records remain intact.
2. Keeps the previous direct guard: new N10 product operations never materialize L3 emergency learning feedback.
3. Removes the three standalone timer definitions (`v7-users-autoswitch`, Matrix refresh and Telegram sentinel).  `v7-health.service` remains the single active Matrix/Telegram health owner.  Static services remain explicit manual recovery fallbacks; the quality timer remains its separate deep-background role.
4. Makes deploy and truth checks prove the active `v7-health.service` Matrix owner instead of treating an absent standalone Matrix timer as a requirement.

## Verification

- Focused suites: 348 tests for autoswitch/Authority/route writer/Core-primary; 54 tests for truth, health and Matrix trigger contracts — all passed.
- Safe deploy: `deploy-z8-14-Updatesystem-25c81a6-20260827T150950`.
- Local, GitHub and deployed commit: `25c81a6e6522a95891b8b2504d6a611fb60e2754` at deployment verification time.
- `v7-health.service` is active.  The three removed timer units are `not-found` and inactive.  `v7-egress-quality-compact.timer` remains enabled and active.
- Existing outcome reconciliation passed with no route mutation, no user movement and no Authority change.  It excluded 48 historical N10 feedback rows from the L3 emergency projection; the latest L3 operation is now a genuine L3 operation, not N10.
- `v7-user-route-check` returned `V7_USER_ROUTE_CHECK=OK`; Core-primary verification passed.

## Remaining N11 frontier

The Program is not terminal yet.  The next work is the bounded N11 replacement-closure/resource audit: classify every remaining static service, installer/recovery caller and active JSONL reader as primary, fallback, deep background or no-current-consumer; delete only a fully migrated, non-recovery-dependent residue.  Existing `CONTAINED_STOP_SAFE` cohort checkpoints are historical safe terminals, not active operations: all have a consumed closure obligation and a published durable successor.

The accepted current 2-vCPU HARD rollout envelope remains P95 <= 7000 ms and max <= 8000 ms.  The historical 3-second HARD goal was not achieved.  Telegram functional S11 proof remains valid with its historical performance limitation.  Server-side S11 is proven; no independent end-client T11 claim is made.

## N11 follow-up: stale Runtime and timer projections closed

Commit `d49e6d20efb455cb8a01e67007a425a7f5cf79bf` closes a stale Runtime-snapshot compatibility edge. Old snapshots may contain read-only cells for the two removed timers and lack the later `v7-health.service` cell. The existing truth owner now ignores only those retired cells and reads the missing health-owner status through its existing read-only Runtime access. It neither writes a snapshot nor starts a service. The focused suite is 55/55 PASS; safe deploy `deploy-z8-14-Updatesystem-d49e6d2-20260827T151935` and full local/GitHub/Runtime truth check are PASS.

The final static consumer scan found two live descriptive tails, not a second routing path: Telegram's handoff still named the deleted Matrix timer, and the recovery installer still issued harmless commands against the three retired timer names. They now name/use only `v7-health.service`; the installer cannot revive a removed periodic owner. The readiness review no longer retains a special exception for a timer that no longer exists. The Program marks pre-N11 timer wording as historical evidence and the existing atomic CPS owner now projects the real current re-entry owner. Focused tests are 56/56 PASS. `tools/v7-control-plane-governance-check` remains classified as a legacy read-only audit artifact: it is neither an installed Runtime entrypoint nor a recovery consumer, so no deletion is claimed without a separately proven replacement scope.

Commit `6aba757ee9aa6422ea5ada37612717d2959813ee` was safely deployed as `deploy-z8-14-Updatesystem-6aba757-20260827T152509`. The final truth check returned `FULLY_ALIGNED`: local, GitHub, CPS and Runtime agree. Direct Runtime verification confirmed `v7-health.service` active, all three retired timers `not-found`/inactive, `CORE_PRIMARY_VERIFY_PASS`, and `V7_USER_ROUTE_CHECK=OK`. No route change or user movement occurred during this N11 follow-up.

## N11 replacement-closure audit and bounded live-history repair

The fresh static/runtime audit classified the remaining surfaces as follows:

| Surface | Current classification | Evidence |
| --- | --- | --- |
| `v7-health.service` + `v7-health-loop` | `PRIMARY` Matrix/Telegram owner | Runtime owner status `LIVE_V7_HEALTH_MATRIX_OWNER_PROVEN`; service active/enabled |
| `v7-users-autoswitch.service`, `v7-service-matrix-refresh.service`, `v7-telegram-sentinel.service` | `FALLBACK`/manual recovery services | no active timer; all three retired timer units are `not-found`/inactive |
| `v7-egress-quality-compact.timer` | `DEEP_BACKGROUND` quality owner | independent quality-history role, not a failover wake path |
| removed timer names in truth-check/tests and old governance checker | `RETIRED_DELETED` compatibility/history | read-only snapshot compatibility or historical fixture; no Runtime consumer |
| `tools/v7-control-plane-governance-check` | `EXPLICITLY_DEFERRED` legacy read-only audit | static/runtime scan found no installed recovery caller; its old fixture verdict is not current N0–N11 truth |

The audit also found unbounded JSONL materialization in live advisory/decision
consumers.  Commit `44e17786c3f0c04a8f1f61e1a15ba6ce392c57a8` adds `read_live_owner_history_window`, reusing the
existing append-only owners with a 2,000-row/8 MB recent window.  The durable
history is unchanged; missing current evidence remains fail-closed.  Offline
reconciliation paths retain their full historical reads.  This closes the
N11 scale-law residue without adding an owner, cache, registry or alternate
truth source.  A focused bounded-window test and exact shadow-outcome test
pass; the complete 122-test module reports 107 passes and 15 pre-existing
fixture/environment errors (missing `matrix` setup, missing `state_dir` in a
legacy helper test, and sandbox socket denial), with no new assertion failure.

Before publication, `tools/v7-truth-check --all --json` returned `PASS` with no
blockers after independent GitHub verification.  The change was then published
and safely deployed as commit `cc73a7d8c265f8191042c41025ecd265922109d8`,
deployment `deploy-z8-14-Updatesystem-cc73a7d-20260827T155151`.  The first
deploy attempt correctly stopped because the health-loop restart flag was not
explicit; the second attempt restarted only the existing `v7-health.service`
and completed with `PASS`.  A fresh post-deploy truth check returned
`FULLY_ALIGNED`/`PASS`, with local, GitHub and Runtime commits equal and no
warnings or blockers.  No route or user assignment changed during this repair.

The N11 block is therefore complete for the proven replacement scope.  The
program-level successor is the existing OMP frontier reported by
`--omp-program-reconciliation`: `PHASE6A_SCENARIO:PHASE6V4_PARTIAL_APPLY_CIRCUIT_BREAKER`
and `PHASE6_PRODUCT_ENGINEERING:POLYGON-ACTION-CLASS-SERVICE_PLANE_PARTIAL_FAILURE-ENGINEERING-G1`.
The V7 Service Failure program itself remains non-terminal until its explicit
N0–N11 scale, hard/Telegram evidence and zero-residue conditions are consumed;
this report must not be read as a false terminal claim.

## OMP continuation: product-engineering frontier and CPS/OMP reconciliation

The next existing OMP frontier was executed through the bounded
`PHASE6V4_PARTIAL_APPLY_CIRCUIT_BREAKER` Polygon scenario.  It returned
`PASS`, was consumed by the existing scenario owner, and had no Runtime,
production, routing, user or Authority effect.  The following product
engineering obligation
`POLYGON-ACTION-CLASS-SERVICE_PLANE_PARTIAL_FAILURE-ENGINEERING-G1` was then
consumed through the existing OMP consumer.  Its result is engineering-only:
the L8 natural-observation window remains passive and no production credit was
created.

The first persistent CPS projection correctly stopped itself with
`cps_current_stop_divergence`: the old V5.3 `EXTERNAL_OWNER_REQUIRED` stop was
left underneath a terminal product-engineering result.  This was a bounded
existing-owner lifecycle defect, not a Runtime or policy defect.  The fix in
`tools/v7_sync_lib.py` makes the already-consumed result project its exact
read-only boundary (`REAL_WORLD_LIMIT`, no executable frontier, and the
existing natural-evidence re-entry action) while preserving mission-role
identity and the existing policy.  The same run atomically updated the CPS and
the existing OMP volatile pointers; post-write CPS and OMP consistency both
returned `PASS`.  No route, assignment, ordinary user, Matrix cadence or
Authority changed.

The focused regression for this transition passes, as does `py_compile` via
in-memory compilation.  The full OMP test module was started but exceeded the
interactive execution window; it produced no assertion failure before being
stopped.  The bounded reader and exact OMP transition tests remain passing.

Current frontier after this block: the executable OMP engineering frontier is
closed for this generation.  The existing OMP now waits for a qualifying
natural production outcome or a new owner-backed obligation; synthetic events
must not be manufactured.  This is a lane-local boundary, not a claim that the
overall V7 Service Failure Program is complete.

## Publication and Runtime evidence for the reconciliation fix

The lifecycle correction and its regression were committed as
`3a1a8b431b4ac68b2e6fc283766c65634b1e7428` (`fix(omp): reconcile consumed
product frontier`) and independently confirmed on GitHub branch `Updatesystem`.
Safe deploy completed with
`deploy-z8-14-Updatesystem-3a1a8b4-20260827T161951`.

Post-deploy Runtime truth is `PASS/KNOWN`: local, GitHub and deployed commit
are equal; binary hashes match the authoritative manifest; `v7-health.service`
is the active Matrix owner; the retired standalone autoswitch/Matrix/Telegram
timers remain inactive/not-found; and no ordinary-user route or assignment
changed.  The existing Core-primary and broad route proofs remain valid from
the preceding N10/N11 block.  No new owner, timer, registry, queue, or state
source was introduced.

The remaining Phase-6 action-class obligations were then consumed in order
through the same OMP consumer.  The continuation owner now preserves all
consumed obligation identities instead of replacing the previous one, and a
`REAL_WORLD_LIMIT` natural-evidence boundary no longer suppresses independent
read-only engineering work (Authority and production effects remain blocked).
The complete Phase-6/7 campaign finalizer returned `PASS` with 64/64 scenarios,
no executable frontier, no active Candidate/Packet/Lease and no pending wake.
Its separate report is
`docs/reports/engineering/2026-08-27_phase6_phase7_comprehensive_boundary_consumed.md`.
