# BLOCK E13 - Operator UX, Approval Contract, And Observability Design Report

## Executive Verdict

E13 completed the operator governance UX and productization design block. No
runtime mutation, deploy, UI implementation, user movement, routing mutation,
kill switch mutation, manual autoswitch apply, or canary was performed.

The orchestration core is mature enough for operator UX productization. The
next risk is no longer hidden runtime experimentation; it is letting operators
approve powerful bounded orchestration with fragmented, stale, or low-level
evidence. Therefore larger cohort execution should wait for productized
approval contracts, observability, and operator-safe workflows.

## Final Answers

operator_ux_design_complete=true
approval_contract_defined=true
observability_model_defined=true
topology_model_defined=true
operator_safety_model_defined=true
larger_cohort_should_wait_for_ux=true
orchestration_core_ready_for_productization=true
remaining_runtime_blockers=RUNTIME_REPO_LINEAGE_PARTIAL;RESTART_REPLAY_REHEARSAL_NOT_EXECUTED;LIVE_MATCHING_TOKEN_NONZERO_MOVEMENT_NOT_APPROVED;DEDICATED_TEST_EGRESS_NOT_READY
recommended_next_stage=E14_APPROVAL_CONTRACT_SCHEMA_AND_READ_ONLY_OPERATOR_OBSERVABILITY_FOUNDATION
execution_allowed_now=false

## Design Artifacts

- `docs/track7/productization/e13-operator-pain-analysis.md`
- `docs/track7/productization/e13-information-hierarchy.md`
- `docs/track7/productization/e13-operator-screens.md`
- `docs/track7/productization/e13-approval-contracts.md`
- `docs/track7/productization/e13-topology-visual-model.md`
- `docs/track7/productization/e13-operator-safety-model.md`
- `docs/track7/productization/e13-observability-model.md`
- `docs/track7/productization/e13-productization-roadmap.md`
- `docs/track7/productization/e13-design-consistency-review.md`

## Operator UX Decision

The UI should not be a generic VPN dashboard. It should be a governed routing
control plane:

- global operational truth first;
- movement and approval state second;
- target/runtime detail third;
- deep evidence last;
- serious actions centralized in Approval Center;
- no broad one-click autoswitch controls;
- no noisy network topology.

The design uses the existing V7 admin philosophy:

- premium dark-first surfaces;
- calm data density;
- restrained accents;
- minimal frames;
- progressive disclosure;
- clear status semantics;
- mobile-aware approval and evidence flows.

## Approval Contract Decision

Approvals must bind a human decision to exact runtime truth:

- movement preview;
- generation token;
- selected-move fingerprint;
- rollback manifest;
- blast radius;
- restore barrier;
- delayed monitoring;
- expiry and replay prevention.

Target readiness GO is not approval. A generation token is not approval by
itself. Nonzero selected movement budget requires explicit bounded approval.

## Observability Decision

Observability should be lineage-based:

- operation timeline;
- movement lineage;
- restore lineage;
- generation lineage;
- planner/apply lineage;
- selected_moves lineage;
- target pressure lineage;
- delayed movement lineage.

Raw evidence remains available, but the operator sees a readable verdict,
impact, freshness, and safe next action first.

## Larger Cohort Decision

larger_cohort_should_wait_for_ux=true

Reasons:

- larger cohort remains `CONDITIONAL_NO_GO` after E12;
- live matching-token nonzero movement has not been approved;
- restart replay rehearsal has not been executed;
- WireGuard hard limit 2 remains a capacity boundary;
- dedicated test egress is not ready;
- operator UX and approval workflow are not yet productized.

## Recommended Roadmap

1. E14 approval contract schema and read-only observability foundation.
2. E15 operator overview, target pool, operations history, evidence viewer, and
   delayed monitor UI.
3. E16 Approval Center, safe action UX, generation governance, and restore
   lifecycle controls.
4. E17 runtime/repo lineage convergence.
5. E18 dedicated test egress or capacity-safe target.
6. E19 larger-cohort approval packet.
7. E20 larger-cohort execution only if E19 is GO.

## Mandatory Design Reviews

All E13 design reviews passed:

- consistency review across all designed screens;
- approval flow consistency;
- rollback visibility consistency;
- observability hierarchy consistency;
- progressive disclosure consistency;
- mobile operator flow review;
- blast radius visibility review;
- dangerous-action UX review;
- topology scaling review;
- governance language consistency review.

## Final Mutation Statement

Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO

