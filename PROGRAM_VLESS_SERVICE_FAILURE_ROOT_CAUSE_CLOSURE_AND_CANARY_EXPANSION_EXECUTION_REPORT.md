# PROGRAM VLESS SERVICE FAILURE ROOT CAUSE CLOSURE AND CANARY EXPANSION EXECUTION REPORT

Project: V7 Vozduh  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Date: 2026-06-06

## Executive Summary

The original blocker was closed.

`vless` was previously rejected because planner reported `instagram=FAIL` and `google_auth=FAIL`, producing `no_eligible_failover_target`.

Live production revalidation showed both services are currently reachable through `vless` interface `tun0`:

- `instagram`: HTTP 200, OK
- `google_auth`: HTTP 200, OK

The root cause was not a missing execution path, not authority, not restore barrier, and not a code deployment issue. The blocker was stale/transient service truth in the service matrix. After service matrix regeneration and pre-planner snapshot refresh, `vless` became eligible again for the required user priority set.

The governed 2-user bridge execution completed successfully:

- `10.0.0.3`: `awg3 -> vless`
- `10.0.0.6`: `awg3 -> vless`
- selected moves: 2
- verification: PASS
- rollback: not required
- outcome/trust/prediction/recommendation feedback: materialized
- SMALL_BATCH authority: certified and promoted in production policy

## Evidence Folder

`vless_service_failure_evidence/`

Key evidence:

- `phase1_vless_instagram_probe.json`
- `phase1_vless_google_auth_probe.json`
- `phase4_vless_full_service_matrix.json`
- `phase6_planner_after_service_revalidation.json`
- `phase8_fresh_approval_packet.json`
- `phase8_packet_recheck_only.json`
- `phase8_restore_barrier_execute.json`
- `phase9_governed_apply_verify.json`
- `phase10_feedback_materialize_10003.json`
- `phase10_feedback_materialize_10006.json`
- `phase11_target_user_assignments.txt`
- `phase11_snapshot_refresh_after_feedback.json`
- `phase12_post_feedback_planner_with_pre_refresh.json`
- `phase14_authority_policy_promotion_retry.json`
- `phase14_post_promotion_planner_retry.json`
- `phase14_policy_after_promotion_retry.json`

## Service Failure Trace

`tools/v7-service-matrix-test` defines:

- `instagram`: `https://www.instagram.com/`
- `google_auth`: `https://accounts.google.com/`
- `vless` egress interface: `tun0`

Probe method:

- `curl --interface tun0`
- HTTPS request with redirects enabled
- default timeout: 8 seconds
- HTTP 2xx/3xx accepted
- HTTP 401/403/429 treated as reachable but limited
- timeout or unreachable endpoint treated as failure

Production recheck:

- `instagram`: OK, HTTP 200
- `google_auth`: OK, HTTP 200

Full service matrix remained `WARN` because unrelated services still had issues:

- `anthropic`: HTTP 404 on `https://api.anthropic.com/`
- `openai_auth`: timeout on `https://auth.openai.com/`

Those were not blockers for the `VIDEO_OPTIMIZED`/priority services used by the selected users. Planner confirmed required service suitability for `vless`:

- `youtube`: OK
- `instagram`: OK
- `telegram`: OK
- `google`: OK
- `google_auth`: OK

## Root Cause Report

Root cause:

`instagram` and `google_auth` were stale/transient FAIL entries in production service truth. Direct live probes through `tun0` succeeded, and service matrix regeneration updated the runtime state.

No code fix was required.

No duplicate planner, duplicate execution path, or forced eligibility was created.

## Service Revalidation

After revalidation:

- `vless_eligible=true`
- service suitability aggregate for selected users was approximately `99.843`
- required missing services: none
- required low services: none
- route class fitness: OK

## Planner Retest

Planner dry-run with pre-planner refresh returned:

- `candidate_moves_total=14`
- `clearance_selected_moves_before_guard=2`
- allowed users: `10.0.0.3`, `10.0.0.6`
- allowed target: `vless`
- blocker at that stage: expired restore-barrier clearance generation

This was a valid governance blocker, not a service blocker.

## Approval Packet

Generated fresh approval packet:

- packet id: `pkt_091b10af7490aa5df886c39e`
- approval id: `appr_f782372f388f39b5fe4e2e8b`
- selected move count: 2
- selected move hash: `fcbbb6b0bb355003c3cf794875a78d68ce4a52d05c0c1ecfa94c761b7ef35438`
- users: `10.0.0.3`, `10.0.0.6`
- target: `vless`
- rollback manifest bound for both users back to `awg3`

Packet recheck verdict:

`ALLOW_RESTORE_BARRIER_CLEARANCE`

## Restore Barrier

Restore-barrier clearance was written through `v7-operator-execution-packet`.

Verdict:

`RESTORE_BARRIER_CLEARANCE_WRITTEN`

Execution readiness state:

`EXECUTION_READY`

No user movement occurred during barrier creation.

## Real Governed Apply

Command used existing governed autoswitch path only:

`v7-users-autoswitch --mode guarded --target-egress vless --max-selected-moves 2 --pre-planner-refresh write --allow-pre-planner-refresh-with-apply --apply --verify --rollback-on-verify-fail`

Result:

- terminal state: `APPLIED`
- terminal reason: `selected_moves_applied`
- selected moves: 2
- operation id: `runtime_autoswitch_b5063a475a06312ff23c90a7`

Moved users:

- `10.0.0.3`: `awg3 -> vless`, verify rc `0`
- `10.0.0.6`: `awg3 -> vless`, verify rc `0`

Post-apply registry:

- `ip=10.0.0.3 current=vless table=101 enabled=1`
- `ip=10.0.0.6 current=vless table=104 enabled=1`

Rollback:

- rollback required: false
- rollback attempted: false

## Outcome Feedback

Feedback was materialized through production admin API endpoint:

`/api/actions/execution-feedback-materialize`

Feedback records:

- `10.0.0.3`: `execfb_dfac3391a383f3f76793fea0`
- `10.0.0.6`: `execfb_e42729ab1d2fe5ffad827c56`

For both:

- outcome status: `success`
- trust delta: `+1.0`
- prediction delta: `+0.75`
- recommendation delta: `+1.0`
- closure state: `CLOSED`

Snapshot refresh after feedback:

- snapshot count: 11
- source stable: true
- runtime behavior changed: false
- governance behavior changed: false
- users moved by refresh: false

## Small Batch Certification

After successful 2-user governed execution, verification, feedback, and clean snapshot gate, production authority policy was promoted.

Backup created:

`/etc/v7/policy.json.backup.small-batch-certified-20260606T085458Z`

Final production policy:

- authority class: `SMALL_BATCH`
- certified authority class: `SMALL_BATCH`
- authority lifecycle state: `SMALL_BATCH_CERTIFIED`
- current allowed user budget: `2`
- next allowed user budget: `5`

Final planner verification normalized lifecycle to:

- runtime authority: `SMALL_BATCH`
- prepared authority: `SMALL_BATCH`
- certified authority: `SMALL_BATCH`
- lifecycle: `CERTIFIED`
- current allowed user budget: `2`
- next authority class: `MEDIUM_BATCH`
- snapshot gate stop required: false
- snapshot source mismatch families: none

Note:

The first authority policy patch attempt failed because of shell quoting in a Python `strftime` expression. It did not modify policy. A second corrected patch succeeded and was verified. Both attempts are visible in evidence; the successful result is `phase14_authority_policy_promotion_retry.json`.

## Final Verdicts

| Verdict | Value |
|---|---:|
| service_root_cause_identified | true |
| service_root_cause_fixed | true |
| vless_eligible | true |
| candidate_moves_total | 14 |
| selected_moves | 2 |
| canary_expansion_ready | true |
| users_moved | 2 |
| verification_passed | true |
| rollback_required | false |
| outcomes_materialized | true |
| trust_feedback_updated | true |
| prediction_feedback_updated | true |
| recommendation_feedback_updated | true |
| small_batch_certified | true |
| current_certified_authority | SMALL_BATCH |
| current_runtime_authority | SMALL_BATCH |
| current_allowed_user_budget | 2 |

## Safe Next Step

`SAFE_NEXT_STEP=OBSERVE_SMALL_BATCH_STABILITY_WINDOW_BEFORE_MEDIUM_BATCH`

Do not jump directly to `MEDIUM_BATCH`. The next proper stage is an observation window for the 2-user cohort, then a separate MEDIUM_BATCH readiness program for budget `5`.
