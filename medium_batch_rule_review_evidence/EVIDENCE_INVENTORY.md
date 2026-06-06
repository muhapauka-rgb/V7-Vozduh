# EVIDENCE_INVENTORY

Project: V7 Vozduh

Scope: inventory of evidence accumulated since CANARY for the MEDIUM_BATCH rule challenge.

## Evidence Sources Reviewed

Primary reports:

- `PROGRAM_VLESS_SERVICE_FAILURE_ROOT_CAUSE_CLOSURE_AND_CANARY_EXPANSION_EXECUTION_REPORT.md`
- `PROGRAM_SMALL_BATCH_STABILITY_WINDOW_AND_MEDIUM_BATCH_REVIEW_REPORT.md`
- `PROGRAM_MEDIUM_BATCH_READINESS_TEST_SYSTEM_AND_BLOCKER_CLOSURE_REPORT.md`
- `PROGRAM_MEDIUM_BATCH_PREPARATION_AND_5_USER_GOVERNED_EXECUTION_READINESS_REPORT.md`
- `PROGRAM_MEDIUM_BATCH_AUTHORITY_PROMOTION_DECISION_AND_PACKET_PREPARATION_REPORT.md`

Primary evidence folders:

- `vless_service_failure_evidence/`
- `small_batch_stability_evidence/`
- `medium_batch_readiness_evidence/`
- `medium_batch_preparation_evidence/`
- `medium_batch_authority_evidence/`

## CANARY And Bridge Evidence

CANARY authority existed before the first SMALL_BATCH bridge.

The authority bridge model allowed a transitional path:

- `CANARY_CERTIFIED`
- `CANARY_EXPANSION`
- `PROVISIONAL_SMALL_BATCH`
- `SMALL_BATCH_CERTIFIED`

The bridge explicitly avoids creating a duplicate truth source, duplicate planner, or duplicate governance path.

## SMALL_BATCH Execution Evidence

One modern successful SMALL_BATCH execution is proven:

| Field | Value |
| --- | --- |
| operation_id | `runtime_autoswitch_b5063a475a06312ff23c90a7` |
| users | `10.0.0.3`, `10.0.0.6` |
| movement | `awg3 -> vless` |
| selected_moves | 2 |
| verification | PASS |
| rollback_required | false |
| rollback_attempted | false |
| feedback materialized | true |
| closure state | CLOSED |
| authority after completion | SMALL_BATCH certified |

## Verification Evidence

Verification passed for both moved users.

Post-apply registry showed:

- `10.0.0.3 current=vless`
- `10.0.0.6 current=vless`

No rollback was required.

## Rollback Readiness Evidence

The original approval packet included rollback manifest binding both users back to `awg3`.

Rollback was not executed because verification passed and no containment was required.

Rollback readiness is proven for the executed SMALL_BATCH packet; rollback execution for the second independent SMALL_BATCH run is not proven because that run does not exist.

## Feedback Evidence

Feedback records:

- `execfb_dfac3391a383f3f76793fea0`
- `execfb_e42729ab1d2fe5ffad827c56`

Feedback covered:

- trust
- prediction
- recommendation
- closure

Both users had successful feedback materialized.

## Service Truth Evidence

The original VLESS blocker was closed.

Evidence showed:

- `instagram` reachable through `vless`
- `google_auth` reachable through `vless`
- service truth stale/transient classification active
- required services for the selected users were healthy

This closed the service truth risk that caused the original failure.

## Snapshot And Planner Stability Evidence

Snapshot blocker was later closed:

| Field | Value |
| --- | --- |
| pre_planner_refresh_state | REFRESH_SUCCESS |
| snapshot_stop_required | false |
| source_mismatch_families | `[]` |
| truth-check | PASS / FULLY_ALIGNED |
| convergence-status | PASS |

MEDIUM_BATCH dry-run could discover a 5-user candidate surface, but the authority gate capped the runtime scope back to 2.

## MEDIUM_BATCH Preparation Evidence

MEDIUM_BATCH candidate surface exists:

- candidate moves total: 15
- first 5 review candidates visible
- eligible channels: `awg0`, `vless`
- snapshot gate clean

However, canonical packet generation remained capped to 2 users because certified authority remained `SMALL_BATCH`.

## Inventory Verdict

`evidence_inventory_complete=true`

The accumulated evidence is strong and broad. It proves service truth closure, snapshot lineage closure, planner dry-run stability, one successful SMALL_BATCH execution, verification, feedback, and closure.

It does not prove a second independent successful SMALL_BATCH governed execution cycle.

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO
