# CT-M0F: repair of controlled-source preflight and Authority boundary

**Date:** 2026-08-12
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
**Parent Mission:** `CT-M0F` — controlled validation of control-plane and kernel-path cutover latency

## Result

`ENGINEERING_REPAIR_DEPLOYED_AND_CONSUMED; INDEPENDENT_ENGINEERING_AUTHORITY_REQUIRED_FOR_DEDICATED_CONTROLLED_SOURCE`.

The production CT-M0F predecessor now selects and binds an already-existing certification identity through the active standing CT-M0F policy.  It has reached a precise, independently decidable topology-provisioning boundary.  No customer or certification-user route was moved and no controlled failure was created.

## Root cause and repair

The existing controlled-source selector was coupled to the Tier-48 campaign capacity rule, although CT-M0F needs only a one-user isolated preflight.  Its shared-allocation reader also assumed a complete allocation record.  Finally, the active CT-M0F standing policy was not accepted as provenance for the existing topology Authority package when no legacy campaign was active.

The smallest existing-owner repairs were deployed:

- `ea02e279` — `CT_M0F_ONE_USER_CONTROLLED_CONDITION` profile: exact one-user source-scope and capacity-two draft admission; no Tier-48 credit.
- `ef314ef4` — partial or absent shared allocation is normalized before source selection.
- `6e6e93a7` — existing `admin_core/operator_execution.py` accepts the active `CT_M0F_STANDING_VALIDATION_POLICY` provenance; `tools/v7-users-autoswitch` binds it to the selected existing certification identity.

Focused owner tests passed:

- `tests.unit.test_service_failure_automation_evolution`
- `tests.unit.test_operator_execution_packet`

The deployed production caller returned `CONTROLLED_SOURCE_TOPOLOGY_PRODUCTION_PREFLIGHT_READY` with existing draft `1-1779291887-55965c`, certification identity `10.7.0.107`, and original source `amneziawg-exec-20260528-10-8-1-14`.

## Production and alignment evidence

Safe deploys were manifest-limited to the repaired runtime owners:

- `deploy-z8-14-Updatesystem-ea02e27-20260812T110712`
- `deploy-z8-14-Updatesystem-ef314ef-20260812T111125`
- `deploy-z8-14-Updatesystem-6e6e93a-20260812T112421`

`v7-truth-check --all --json`: local and GitHub `PASS`; non-blocking user documentation dirtiness only.
`v7-convergence-status --json`: `ALIGNED`; local, GitHub, and production are all `6e6e93a7195ed72810d1f25c1b0b7786a3bbe6a3`.

## Exact independent Authority request

- **Classification:** `ENGINEERING_AUTHORITY`
- **Request:** `cstopauth_r1_6b395c70d2db7a54d8a0425e`
- **Hash:** `6b395c70d2db7a54d8a0425e8bedf917e542d84b4e0edfeaa9e14ab52a15b8f9`
- **Expires:** `2026-08-13T08:27:21.620789+00:00`
- **Decision set:** `APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE` / `DECLINE`
- **Scope:** reserve one empty dedicated controlled source from existing ready draft `1-1779291887-55965c` for one existing certification identity (`10.7.0.107`); ordinary-user delta is exactly zero.

The request is append-only registered by the existing `admin_core/operator_execution.py` Authority audit owner.  It is bound to active standing contract `ctm0fsdpc_208482a67dc4103e5f0ef7b6` and its expiry `2026-09-05T09:32:42.689887+00:00`.

## Forbidden effects and next re-entry

This step performed only the required Authority-audit write.  It performed **no** policy write, registry write, identity creation, assignment change, Candidate/Packet/lease creation, restore-barrier write, runtime apply, routing mutation, user movement, rollback, Authority expansion, maturity change, controlled-production credit, or Natural L8 credit.

Approval may materialize only the manifest-bound isolated source and rerun fresh preflight.  It does not authorize a controlled failure or any cutover.  After an approved isolated source is proven healthy, the existing separate execution gates remain responsible for any subsequent CT-M0F sample.

**Legal terminal:** `AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION`.
**Re-entry condition:** append one exact decision for the registered request through the existing Authority owner.
