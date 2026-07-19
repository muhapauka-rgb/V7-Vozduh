Mission ID: `V7_L7_L8_CONTROLLED_ROLLBACK_CONDITION_AUTHORITY_REQUEST_R1_V1`
Run Nonce: `V7_L7_L8_R1_20260719T232830+0700`

# L7/L8 R0 reconciliation and R1 Authority request

## Result

R0: `COMPLETE_CONSUMED`.

R1: `EXACT_REQUEST_PREPARED_AWAITING_INDEPENDENT_AUTHORITY_DECISION`.

Current legal terminal: `ENGINEERING_AUTHORITY`.

## R0 root cause and repair

The calibration-floor finalizer wrote current five-Passport L7/L8 state keys, but the canonical CPS renderer did not project those optional keys and the live-CPS reconstruction path did not load them. The idempotency gate also ignored the current L7/L8 projection fields. A later generation could therefore preserve or recreate a current-looking one-Passport/four-gap projection.

`tools/v7_sync_lib.py` now projects and reconstructs every current L7/L8 field used by the calibration-floor owner. Its finalizer validates the full current projection before returning idempotent success. The atomic regression corrupts the immutable-set and exact-gap fields and proves that the producer repairs them to the five-Passport/two-residual state.

Focused and full `tests.unit.test_cps_atomic_reconciliation`: `PASS`.

Implementation commit: `06519280c5c5d2dc0836d81dd9efece3d1a1c334`.

Safe deploy ID: `deploy-z8-14-Updatesystem-0651928-20260719T231945`.

Deploy manifest delta: only `tools/v7_sync_lib.py`.

Production deployed SHA-256: `e884a2b4d0b1c86534eb2083efeb0402601098c86d6e4e47b2b33606450ab5cb`.

Fresh production non-test caller `production_deployed_v7_sync_lib` consumed the real current CPS through `normalized_cps_reconstruction_to_render_projection` and preserved:

- five exact material Passport IDs;
- eligibility set `outset_428a4e2ff440ed64bde5cb56` with five eligible Passports;
- residual cells `natural_production_present; rollback_and_no_rollback_present`;
- next reentry `REQUEST_EXACT_CONTROLLED_ROLLBACK_CONDITION_ENGINEERING_AUTHORITY`.

Post-deploy `tools/v7-truth-check --all --json`: `PASS`; zero stale CPS projections.

Post-deploy `tools/v7-convergence-status --json`: `PASS / ALIGNED`; local, GitHub and production commit `06519280c5c5d2dc0836d81dd9efece3d1a1c334`; deploy delta empty.

## R1 discovery and reuse

The request reuses the existing Controlled Production Certification, egress lifecycle, certification-user registry, planner, delegated policy, Candidate/Packet/lease, Runtime apply, route/service verification, rollback, outcome, replay, Learning, M6/M7, CPS and OMP owners. No second registry, executor, watcher, queue, policy or truth source is created.

Current production evidence used read-only for preparation:

- certification user `10.7.0.16`, table `1014`, current `vless`, group `polygon-l7-canary`;
- controlled source `wireguard-1779454504-c43409`, interface `v7e06a394c478`, WireGuard, enabled, marked `controlled_certification_source=1`;
- target `vless`, interface `tun0`;
- source and target expose fresh successful Google and Telegram checks;
- the existing planner confirms no genuine current Candidate while the user remains on healthy `vless`, so a deliberate controlled condition is genuinely required;
- the existing Runtime already treats `required_service_verify_timeout` as non-success and routes it to its normal rollback branch when the real verifier reports failure.

## Exact R1 contract

Canonical packet: `docs/reports/engineering/evidence/2026-07-19_232830_controlled_rollback_authority_request.json`.

Request ID: `engauth_r1_33cc5e04f86c20ff0607f7db`.

Contract SHA-256: `33cc5e04f86c20ff0607f7dbde8c86267e89ff5f91d87a1503b9b6e80bf13016`.

The bounded design is:

`certification setup 10.7.0.16 -> controlled source -> controlled source maintenance -> normal planner selects vless -> one real apply -> terminal route acknowledgement -> controlled source restored -> existing service-matrix lifecycle contention -> normal verifier observes lock timeout -> normal rollback owner returns user to controlled source -> cleanup restores initial vless assignment -> complete Passport/temporal/replay/Learning -> M6/M7/CPS/OMP`.

The verifier, not the experiment coordinator, decides whether rollback is required. Direct rollback for manufacturing the terminal is forbidden. If the registered trigger does not occur, the result is recorded honestly and the coverage cell remains open.

## Safety and effects

R0 deploy effects: routing mutation `NONE`; user movement `NONE`; packet execution `NONE`; restore-barrier write `NONE`; rollback apply `NONE`; daemon/timer enablement `NONE`; Authority change `NONE`; Production Maturity change `NONE`.

R1 preparation effects: production apply `NONE`; routing mutation `NONE`; user movement `NONE`; deliberate condition activation `NONE`; Authority change `NONE`; Production Maturity change `NONE`.

The R1 request permits no action by itself. Only an unexpired exact R2 verdict may admit one transaction, and the approval must be atomically consumed with fresh Candidate, Packet, lease and transaction identity.

## R1 implementation, deploy and consumption

R1 packet/CPS/OMP commit: `119507672d78a8bede8671a6fb57f0ca734f0513`.

Safe deploy ID: `deploy-z8-14-Updatesystem-1195076-20260719T234136`.

Deploy manifest delta: only `tools/v7_sync_lib.py`.

Local and deployed SHA-256: `8372d7eb698877011a0c5e94a3acfac9c2eca75388199c70ae237737bfd0ca27`.

The fresh production non-test caller consumed the real current CPS through deployed `omp_functional_footprint_consistency` and proved that `L7_L8_R2_INDEPENDENT_AUTHORITY_DECISION_PENDING` remains a Phase 6 integration stage with `INTEGRATION_COMPLETION`; the historical `AEP_PHASE_6_STATUS` / `CURRENT_COMPLETION_CONTRACT` mismatch does not recur. Expected copied-runtime source-layout scan residuals were not used as completion evidence.

Focused packet, functional-footprint and full atomic-CPS suites: `PASS`.

Post-deploy `tools/v7-truth-check --all --json`: `PASS`; zero CPS contradictions; exact next action `DECIDE_CONTROLLED_ROLLBACK_AUTHORITY_REQUEST_engauth_r1_33cc5e04f86c20ff0607f7db`.

Post-deploy `tools/v7-convergence-status --json`: `PASS / ALIGNED`; local, GitHub and production commit `119507672d78a8bede8671a6fb57f0ca734f0513`; deploy delta empty.

## Exact next action

The independent Authority owner must return exactly one of:

- `APPROVE_ONCE_AS_SCOPED`;
- `APPROVE_WITH_NARROWER_SCOPE`;
- `DENY`;
- `EXPIRED`.

Until then, R3-R8 are not activated. R9-R11 remain outside this program and cannot start without the independent class-decision chain defined by the plan.
