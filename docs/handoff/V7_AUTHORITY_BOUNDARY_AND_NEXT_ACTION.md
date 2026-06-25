# V7 Authority Boundary And Next Action

Captured at: 2026-06-25T10:46:06+0700

## Boundary

Current stop reason: `AUTHORITY_BOUNDARY`.

V7 is stopped before:

- restore-barrier write;
- runtime apply;
- user movement;
- rollback apply;
- autonomous daemon/timer activation;
- authority expansion.

## Current Exact Decision Payload

| Field | Value |
| --- | --- |
| Candidate | `10.7.0.5` |
| Current channel | `vless` |
| Target channel | `awg3` |
| Reason | best available channel has higher advisory suitability |
| Authority tier | `TIER_1` |
| Authority status | `MARGINAL_OPERATOR_REVIEW` |
| Packet id | `pkt_preview_43f0151499620a00d2e50f7b` |
| Operation id | `govdry_c8f67c5437777091c9cf1f5d` |
| Selected move hash | `8e7785e058337f1db53fd929d7c175914510a401ff686391bef7bfcb088bfdac` |
| Risk | `3.678` |
| Confidence | `0.458` |
| Trust | `54.679` |
| Restore status | `RESTORE_AND_ROLLBACK_PREVIEW_READY` |
| Rollback target | `vless` |
| Rollback manifest id | `rb_preview_d25f7c3f7705ba558d2afcea` |
| Verification plan | `VERIFICATION_PLAN_READY` |
| Outcome closure plan | `OUTCOME_CLOSURE_PLAN_READY` |
| Learning path | `LEARNING_PATH_CONNECTED` |

## Knowledge Gates

Passed:

- service_user_sla_fit
- freshness_actionability
- recovery_admission
- anti_flapping
- decision_effectiveness
- knowledge_quality
- outcome_evidence

Blocked:

- routing_recommendation_readiness

Blockers:

- `service_user_sla_fit_not_clear`
- `decision_outcome_closure_incomplete`
- `recovery_admission_has_blocked_channels`
- `freshness_not_actionable:capacity,service`

## Safe Without Approval

These are safe because they are read-only:

```bash
tools/v7-truth-check --all --json
tools/v7-convergence-status --json
ssh v7-vps /usr/local/bin/v7-autonomy-trust-evidence-inventory
ssh v7-vps /usr/local/bin/v7-governed-canary-dry-run-cycle
```

Documentation updates are safe if they do not change runtime behavior.

## Requires Explicit Approval

These actions cross the authority boundary and require explicit approval:

1. Writing restore-barrier clearance.
2. Applying the governed packet.
3. Moving `10.7.0.5` from `vless` to `awg3`.
4. Running verification after apply.
5. Running rollback apply if verification fails.
6. Enabling any daemon/timer/autonomous execution.

## Exact Apply Command Shape

Do not run without approval:

```bash
tools/v7-operator-execution-packet --packet <approved-packet-for-pkt_preview_43f0151499620a00d2e50f7b> --execute-runtime-action
tools/v7-users-autoswitch --mode guarded --user 10.7.0.5 --target-egress awg3 --max-selected-moves 1 --apply --verify --rollback-on-verify-fail
```

## Exact Rollback Command Shape

Do not run without approval:

```bash
tools/v7-users-autoswitch --rollback-packet <rollback-packet-for-rb_preview_d25f7c3f7705ba558d2afcea> --apply --verify
```

## Verification Plan

After approved apply only:

- connection check;
- required service checks;
- route runtime check;
- quality check;
- rollback trigger evaluation.

Rollback triggers:

- user cannot connect;
- required service fails;
- route/runtime mismatch;
- quality regression after move;
- partial apply or verification failure.

## Outcome Closure Plan

After approved apply only, collect:

- apply result;
- post-action verification;
- service outcome;
- user outcome;
- prediction actual;
- rollback required;
- outcome observed at.

Synthetic evidence is forbidden.

## Learning Path

Existing connected path:

1. outcome - `admin_core/operator_execution_feedback.py`
2. feedback - `admin_core/operator_execution_feedback.py`
3. trust-evolution summary - `admin_core/intelligence_workers.py`
4. decision_outcome_learning - `admin_core/operator_execution_feedback.py`
5. knowledge_growth - `admin_core/autonomy_trust_acceleration.py`
6. future decision - `admin_core/operator_decision_surface.py`

## Next Action

Before any approval discussion, regenerate the dry-run:

```bash
ssh v7-vps /usr/local/bin/v7-governed-canary-dry-run-cycle
```

If packet fields changed, update OMP and this handoff before asking for approval.

If unchanged, ask the operator only this authority question:

Approve one governed TIER_1 canary movement for `10.7.0.5` from `vless` to `awg3`, using packet `pkt_preview_43f0151499620a00d2e50f7b`, with rollback to `vless` via `rb_preview_d25f7c3f7705ba558d2afcea` if verification fails?

Stop until explicit approval is given.
