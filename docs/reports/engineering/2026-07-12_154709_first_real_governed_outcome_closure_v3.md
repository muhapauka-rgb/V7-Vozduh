Mission ID: `CAP-U01_FIRST_REAL_GOVERNED_OUTCOME_CLOSURE_V3`
Run Nonce: `V7_CAP_U01_OUTCOME_V3_678CF77D081C`
Mission started: `2026-07-12T15:47:09+0700`
Final verdict: `ROLLBACK_SUCCESS_RUNTIME_ROUTE_INTEGRITY_STOP_CONTINUE_OMP_READY`

# First Real Governed Outcome Closure V3

## Summary

`Continue OMP` выполнил ровно одну fresh bounded delegated production transaction внутри approved action class `single-user governed candidate failover`. Candidate/packet/hash approval не требовались. User `10.7.0.5` был перемещён `awg0 -> vless`; global verification вернула `FAIL`; existing rollback owner успешно восстановил `10.7.0.5 -> awg0`. Final Safe Mode `OPEN`.

Outcome классифицирован как `ROLLBACK_SUCCESS`. Он является реальным production outcome и learning evidence, но по OMP не является successful verified move или promotion success. CAP-U01 остаётся `ACTIVE`, Action-Class state остаётся `GOVERNED_ONLY`, authority не расширена.

## Transaction Identity

- packet: `pkt_preview_c6a5b48c9ee7a80d20859071`;
- decision: `decision_commit_fc77fe288714ff7f7839e0c7`;
- governed operation: `govdry_2cef3491744976a995c1fec6`;
- runtime operation: `runtime_autoswitch_592807059b2ddf3fd06becfc`;
- selected move hash: `2ad1cc99e6751dce6e3c48f94f7e6d531378dde4315ec976b94fbb302f4f1832`;
- execution lease: `execlease_068ea2459045b654fe6661a8`;
- one execution attempt: `TRUE`;
- user movement: `1` forward and certified rollback;
- terminal state: `ROLLED_BACK`;
- terminal reason: `verification_failed_rollback_completed`.

All identities are terminal, historical and non-reusable. No second transaction was executed.

## Verification And Rollback

Selected user rollback state is consistent:

```text
registry current = awg0
assignment egress = awg0
table 1003 default = awg0
route_get = awg0
rollback = ROLLBACK_COMPLETED
Safe Mode = OPEN
```

Global verification failed because two pre-existing enabled users reference disabled egress `wireguard-1779454504-c43409`, whose interface `v7e06a394c478` is absent:

```text
10.7.0.32 table 1030 -> no default; route_get leaks to public ens3
10.7.0.38 table 1036 -> no default; route_get leaks to public ens3
```

Verification scope was not weakened. The failed global safety gate is preserved as current Runtime truth.

## Outcome And Learning

- feedback ID: `execfb_1656430623bdd4467622c9d2`;
- outcome quality: `ROLLBACK_SUCCESS`;
- outcome status: `rollback_success`;
- learning value: `MEDIUM`;
- records written: outcome, prediction, trust, recommendation, closure;
- A4 evidence update: `TRUE`;
- synthetic evidence: `NO`;
- Production Maturity: remain `GOVERNED_ONLY`;
- promotion: blocked because successful verified current-class outcome remains absent.

## Existing Owner Resolution

No new owner, Runtime, Planner, action class or policy is required. Existing owners are:

- detection and verification: `v7-user-route-check`, `hardening/v7-provisioning-reconcile-check`;
- mutation/rollback: `v7-user-switch` under execution control;
- target advice: existing Planner and candidate-suitability read model;
- authority: existing Action-Class/Operational Authority owners;
- closure: existing feedback, learning, Production Maturity, CPS and OMP owners.

Current repair scope is outside the approved one-user policy because two stale assignments must be reconciled before global verification can pass. No repair mutation was performed in this Mission.

## Closure

```text
CURRENT_STOP_CONDITION = RUNTIME_ROUTE_INTEGRITY_FAILURE
CURRENT_NEXT_ACTION_ID = CONTINUE_OMP
CAP-U01 = ACTIVE
CURRENT_CLASS_OUTCOME = ROLLBACK_SUCCESS
CURRENT_ACTION_CLASS_STATE = GOVERNED_ONLY
SAFE_MODE_FINAL_STATE = OPEN
OLD_PACKETS_REUSABLE = NO
```

Next `Continue OMP` must prepare a fresh owner-backed repair for exactly the users still assigned to the disabled egress, revalidate healthy targets and capacity, classify the authority boundary, and stop before mutation unless existing authority legally admits the repair.

Final verdict: `ROLLBACK_SUCCESS_RUNTIME_ROUTE_INTEGRITY_STOP_CONTINUE_OMP_READY`
