# V5.3 Telegram critical latency: root cause and safe reduction

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Mission:** `V7_TELEGRAM_CRITICAL_LATENCY_ROOT_CAUSE_AND_SAFE_REDUCTION`  
**State:** implementation safely deployed; controlled Telegram evidence paused at an authenticated administrative-lifecycle boundary.

## Scope and guardrails

This work retained the existing Matrix, Planner, Authority, route writer, state files and service-verification semantics. No ordinary user, ordinary route, Matrix cadence, service timer, product SLO or HARD-path logic was changed. The only intended test effect is one certification-only identity on an isolated source.

## Baseline and causal finding

The valid Telegram controlled sample `f428` was functionally correct but too slow:

| Interval | Measured value |
| --- | ---: |
| failure -> decision | 18,163.325 ms |
| decision -> Apply | 240.232 ms |
| Apply -> assignment | 685.845 ms |
| assignment -> kernel | 17.853 ms |
| kernel -> reported S11 | 6,247.165 ms |
| total failure -> S11 | 25,354.419 ms |

The evidence isolates two avoidable synchronous contributors before/around decision:

1. Telegram failure publication woke `v7-autoswitch-planner.service` through a separate systemd process instead of the already-running health/Matrix owner. The observed earlier Telegram event was published at 14:22:20.925 UTC and the external planner start appeared about five seconds later.
2. A stale prepared target performed a 5,158.93 ms target-refresh attempt even though its only lawful consequence was the existing full controlled fallback. The complete prepared-validation span was 7,972.373 ms.

The reported 6,247.165 ms after kernel visibility must **not** be interpreted as a pure required-service check: the Matrix-required service evidence in that sample was 3,251.291 ms; the broader field includes additional transaction work.

## Implemented and deployed reduction

Published commit: `ac1d6c20b6ebbbf5073b917e27d1d51a9e6b1d3a` (`perf: remove telegram matrix process boundary`).  
Deployment: `deploy-z8-14-Updatesystem-ac1d6c2-20260826T182822`, final safe-deploy verdict `PASS`.

Changes:

- `tools/runtime-support/v7-health-loop` now consumes a Telegram Matrix T0 through the existing persistent health/Matrix consumer when that consumer is ready. HARD remains on its existing path.
- `tools/v7-telegram-sentinel` suppresses only the duplicate external systemd wake while the existing persistent consumer owns this exact Telegram event; it preserves the former wake as its fallback.
- `tools/v7-service-matrix-refresh-all` skips the known stale prepared-target refresh only on the runtime certification hot path and enters the existing full fallback directly. Non-hot behavior is unchanged.
- New focused tests cover exact current-assignment Telegram T0 selection and suppression of the duplicate external wake.

Validation passed:

- 153 focused health/sentinel/service-episode tests;
- 18 V5.3 role-based recovery tests;
- 7 fast-signal coverage tests;
- 10 N7 causal Polygon tournament tests.

The broader `test_service_failure_automation_evolution` contains one unrelated pre-existing failure in the unchanged `v7-users-autoswitch` standing-policy fixture (`STOP_SAFE_NO_SAFE_TARGET` versus the fixture's expected fresh-event revalidation state). It was not hidden or changed by this mission.

## Runtime state after deployment

- `v7-health.service`: `active`.
- Old standalone Matrix timer: absent/not found; standalone Telegram timer: `disabled`, as intended.
- Runtime hashes were accepted by the safe-deploy alignment gate.
- Certification identity currently selected by the lawful one-user topology preflight: `10.7.0.108`, currently on `awg0`, table `1106`, certification group `t48-d27d985e237c`.
- It has no Telegram service profile yet (`{}`), so the normal required-profile sentinel correctly has no basis to generate a Telegram controlled failure for it.

## Controlled-baseline reconciliation

The existing one-user topology owner selected only the validated isolated draft `amneziawg-1779303737-a57ce8`, with an immutable contract:

- exactly one certification identity: `10.7.0.108`;
- expected assignment: `awg0 -> NEW_DEDICATED_SOURCE`;
- ordinary assignment and route deltas: `NONE`;
- no Candidate, Packet, Lease, routing or user move while requesting/deciding;
- bounded rollback and fresh Matrix/route verification required.

The existing Authority owner registered and approved this exact request:

- request `cstopauth_r1_10e2213949fe0f3afc3035b2`;
- decision `APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE`;
- decision record `cstopdec_23b1118726ebaf71cb7415be`.

Its first existing-owner consumer stopped safely before any mutation because the approved draft is not yet materialized into the existing disabled pool/runtime profile:

`approved_draft_not_materialized_to_existing_pool_source`, `approved_draft_pool_source_not_unique`, and `approved_draft_runtime_lifecycle_not_ready`.

This was an honest stop: no source reservation, identity move, route mutation or ordinary-user effect was performed.

## Current external boundary and exact continuation

The only lawful materialization path is the existing authenticated `v7-admin-api` lifecycle:

`egress-draft-pool-apply` (add disabled) -> `egress-draft-runtime-provision` -> guarded enable/validation -> existing topology consumer -> existing governed certification transaction.

It also owns `service-preferences-update`, the only discovered canonical writer for the temporary Telegram-required profile. It must later set that profile for the one certification identity and clear it during cleanup; direct JSON editing is not lawful.

The API has no current authenticated session in the available browser. A direct console construction of an administrative session was rejected and was **not** used. This is an authentication boundary, not a code or performance blocker.

**Exact next action:** the operator signs into V7 Admin in the opened browser tab. Then, through its existing API only, materialize the exact approved draft as a disabled isolated pool source, provision its runtime profile, conduct its guarded enable validation, and re-run the existing topology consumer. Once the one-identity baseline and temporary Telegram profile are proven, execute the first cold Telegram sample, followed by the warm/final homogeneous evidence series specified by the Mission.

## Current conclusion

The code-level causal reduction is live and ready to be measured. The mission has not claimed Telegram SLO success or failure because no post-deploy functionally valid Telegram sample exists. The remaining block is a single authenticated, existing-owner preparation step; no safety contract needs to be weakened and no new owner is required.
