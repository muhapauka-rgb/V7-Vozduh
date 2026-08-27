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
