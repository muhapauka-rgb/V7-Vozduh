# V5.3 Telegram-critical controlled proof and safe cleanup

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Scope:** one certification-only Telegram-critical controlled transaction,
its bounded lifecycle repairs and complete cleanup. This report is evidence;
the live status is in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

## Result

The automatic recovery chain is functional end to end. It used the existing
Matrix, Planner, Candidate, Packet, Lease, Barrier and the sole route writer;
the system, not an operator, selected `awg3` as the healthy target. The
synthetic identity completed route/kernel verification and route-bound
Telegram S11. No ordinary identity moved.

The one valid cold sample did not satisfy the active Telegram rollout contract:

| Interval | Measured |
| --- | ---: |
| controlled failure onset -> decision | 10,150.617 ms |
| decision -> Apply admission | 252.605 ms |
| assignment commit | 550.048 ms |
| kernel path visible | 22.757 ms |
| route-bound required-service verification | 7,618.150 ms |
| controlled onset -> S11 | **18,594.176 ms** |

The current two-vCPU Telegram contract is P95 `<=7 s` with no valid sample
above `8 s`. This valid sample exceeds the per-sample maximum, so it earns no
rollout credit. It is neither omitted nor reclassified as invalid.

The receipt also identifies an exact bounded residual: the Matrix-owned
prepared projection was fresh and had two eligible targets, but the governed
prepared-execution handoff required one exact target before T0. Because the
target is deliberately owner-selected after T0, that narrow mismatch correctly
fell back to the existing full Planner. The fallback is safe, but its dominant
`apply_and_verification` span was `13,068.382 ms`. This is a concrete
existing-owner target-binding reconciliation, not a basis for an SLO change or
a new architecture.

## Bounded repairs consumed

Three small existing-owner lifecycle gaps prevented a lawful controlled proof:

1. the automatic Telegram consumer did not recognize a nested
   certification-only source scope;
2. the compact Matrix handoff discarded that scope;
3. the controlled reservation expected a target before the owner was allowed
   to select one after T0.

The deployed repairs retain the certification scope, allow an empty pre-T0
target only for the existing `POST_T0_OWNER_SELECTED` contract, and reserve the
identity before target selection. They add no owner, writer, timer, Planner,
registry or alternate state source.

Focused verification passed: **378 tests**. The deployed commit is
`63bc020f7db75b7421b4383bd443e9509c8c0fdb`; the independent release manifest
is `deploy-z8-14-Updatesystem-63bc020-20260826T145345`.

## Exact controlled evidence

The certification identity was `10.7.0.124`, on its isolated execution source.
After the controlled source failure, the Matrix owner confirmed the episode,
the automatic existing consumer selected `awg3`, and the governed chain
created the transaction
`ctm0ftx_4cfd6602db3eef37a5f86a84` and sample
`ctm0fsample_e93cf73d76768c5e41458baa`.

The source was then restored and the existing reset owner returned the test
identity to its isolated source. No target was manually substituted and no
route command bypassed the governed writer.

## Runtime and production effect after cleanup

Independent Runtime observation after cleanup shows:

| Check | Result |
| --- | --- |
| deployed Runtime commit | `63bc020f7db75b7421b4383bd443e9509c8c0fdb` |
| `v7-health.service` | active |
| standalone Matrix timer | inactive as intended |
| standalone Telegram timer | inactive as intended |
| certification identity route | restored to table `1122`, `default dev v7execwg0` |
| temporary Telegram profile | absent |
| temporary nft rule/table | absent |
| ordinary-user effect | zero |

The temporary certification-only Telegram requirement and controlled failure
condition were removed. No active test transaction or lasting product-profile
change remains.

## Exact next step

This block is now consumed by commit
`74cd3f952ce8adc7747a0495d4b04888ccef1a72`: the fresh post-T0 owner-selected
target is carried into the prepared handoff without manual selection. A second
fully cleaned controlled transaction used that branch (`prepared_decision_reused`
was true; candidate validation was 0.671 ms) and no longer rebuilt the world
model or fell back to the full Planner. It exposed a distinct next residual:
the S11 command still included optional Telegram diagnostic endpoints, one of
which waited about four seconds despite all required Telegram endpoints passing.

That is a separate exact-S11 scope reconciliation, recorded in
`2026-08-26_v5_3_telegram_critical_required_service_s11_scope_reconciliation.md`.
Repeating client movements merely to manufacture a distribution remains
forbidden. N10 remains independently blocked: it requires its own
owner-admitted ordinary-like/cohort contract and must not borrow this
controlled Telegram evidence.
