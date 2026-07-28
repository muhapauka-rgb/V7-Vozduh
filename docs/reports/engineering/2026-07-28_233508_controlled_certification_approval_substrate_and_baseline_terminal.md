# Engineering Report: Controlled Certification Approval, Substrate And Baseline Terminal

Дата: 2026-07-28  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: существующая `T48-M8` controlled-certification campaign  
Verdict: `CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL_CONSUMED_SOURCE_BASELINE_EXTERNAL_OWNER_REQUIRED`

## 1. Authority result

- Request: `cpsauth_r1_d27d985e237c9582656b26e7`.
- Request hash: `d27d985e237c9582656b26e75e36a1dd3ef9a602cd8e87f7a793033d8e97cc5c`.
- Decision: `APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN`.
- Decision ID: `cpsdec_43ae9495e77bb0ac5ead232c`.
- Admitted subscopes: `IDENTITY_PROVISIONING`, `CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT`, `CONTROLLED_SOURCE_CONDITION`, `PROGRESSIVE_CAMPAIGN_EXECUTION`.
- Approval remains exact, hash-bound, non-transitive and self-expansion-forbidden.

## 2. Existing-owner substrate consumption

The existing identity, IPAM, registry and assignment owners were reused. They created, classified and assigned 48 dedicated certification identities to exact source `1`, group `t48-d27d985e237c`.

- Dedicated certification identities: `48`.
- Enabled ordinary users on source `1`: `0`.
- Isolated-source maximum: `48`.
- Identity-set fingerprint: `e05a0c90c2ab682861bcc6b2dbf44d47a752a0c9c718c46ea6d2831343ef2d0a`.
- Effect receipt: `cpsfx_3033aed2ec4998b9f9b7e986`.
- No ordinary customer was reclassified or moved.

## 3. Production baseline result

The existing Service Matrix owner observed exact source `1` after provisioning:

- services: `14`;
- reachable: `0`;
- hard failures: `14`;
- source interface: present and up;
- external peer: stale/unavailable;
- controlled maintenance-to-enabled restart: did not restore reachability.

The latest owner-backed source state is `STOP_SAFE_SOURCE_BASELINE_UNHEALTHY`. This is an external egress/substrate failure, not a controlled condition created by the campaign. It is therefore illegal to claim or execute the progressive `5 -> 10 -> 25 -> 48` stages from this state.

## 4. General producer-consumer repairs

Two reusable defects were repaired without creating new owners:

1. Controlled-source selection now requires both isolation and a fresh healthy Matrix baseline.
2. A controlled-certification cohort cannot enter the generic Matrix cohort execution path without exact approved campaign request ID, request hash and stage.

The CPS consistency layer was also extended to accept the exact transition:

`approved + isolated + unhealthy baseline -> EXTERNAL_OWNER_REQUIRED`

without relabelling it as Engineering or Operational Authority.

Commits and deploys:

- `cb093c58d55d9cea6c3b28dc72b64ec765a7328b` — source-health and campaign-binding guards;
- `128aed11d53a820be020a8593715a6f8fe7ce092` — atomic external-baseline terminal and missing registry boolean normalization;
- production deploy: `deploy-z8-14-Updatesystem-128aed1-20260728T232041`.

Safe-deploy delta for the final repair contained only:

- `tools/v7_sync_lib.py`;
- `tools/v7-governed-canary-dry-run-cycle`.

## 5. Production caller and consumer proof

The production non-test standing-policy reconciliation returned:

- `final_verdict=PASS`;
- `ATOMIC_CPS_UPDATE_APPLIED`;
- `current_stop=EXTERNAL_OWNER_REQUIRED`;
- `next_action=EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED`;
- `CURRENT_STATE_CONSISTENCY=PASS`;
- zero policy write, contract issuance, Candidate, Packet, lease, restore-barrier write, apply, routing mutation, user movement, rollback apply, Authority expansion or Production Maturity change.

A direct production Tier-48 caller without exact campaign binding returned:

- `GOVERNED_TRANSACTION_STOPPED`;
- `standing_delegated_cohort_policy_binding_invalid`;
- `apply_executed=false`;
- `users_moved=0`;
- `runtime_mutation_performed=false`;
- `restore_barrier_written_now=false`;
- `authority_expanded=false`.

This proves the generic path cannot bypass the approved progressive campaign.

## 6. Tests and truth

- Focused repaired-path tests: PASS.
- Full affected set after CPS/OMP pointer reconciliation: `252/252 PASS`.
- CPS/OMP pointer correction suite: `46/46 PASS`.
- CPS current state generation: `cpsgen_SFA_SDPC_36BB4D9CC58C_M8_SOURCE_BASELINE_BLOCKED`.
- CPS transition: `SERVICE_FAILURE_TIER48_M8_APPROVED_SOURCE_BASELINE_BLOCKED_V1`.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`, zero blockers.
- `tools/v7-convergence-status --json`: `PASS`.
- Runtime binary payload commit: `128aed11d53a820be020a8593715a6f8fe7ce092`.
- The final report commit is synchronized to GitHub and production through a zero-runtime-delta provenance deploy; its self-referential commit identity is intentionally not embedded in this report.

## 7. Exact legal terminal and re-entry

Current terminal:

`EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED`

Authority required now:

`NO_NEW_AUTHORITY_REQUIRED`

Durable automatic re-entry:

`fresh Matrix observation proves at least one reachable service and zero hard service failures on exact source 1`

The approval and 48 dedicated identities remain valid. Campaign stages remain unclaimed and unexecuted. After a healthy baseline is owner-backed, the existing campaign owner must create a fresh controlled condition and continue serially through `5 -> reset -> 10 -> reset -> 25 -> reset -> 48`, with fresh Candidate, Packet and lease at every stage.
