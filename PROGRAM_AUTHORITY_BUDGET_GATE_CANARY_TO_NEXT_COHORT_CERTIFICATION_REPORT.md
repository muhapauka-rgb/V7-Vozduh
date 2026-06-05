# PROGRAM AUTHORITY BUDGET GATE CANARY TO NEXT COHORT CERTIFICATION REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Certification date: 2026-06-05

## Executive Verdict

V7 can now answer: how many users may be moved right now?

Current answer:

- Current authority class: `CANARY`
- Current allowed user budget: `1`
- Next allowed user budget: `2`
- Next class: `SMALL_BATCH`

This program implemented a hard lightweight authority budget gate inside the existing runtime executor: `tools/v7-users-autoswitch`.

No autonomy was enabled.

No users were moved by this program.

No new planner, governance system, execution path, rollback owner, truth source, or snapshot root was created.

## AUTHORITY_REALITY_REPORT

Starting production evidence was taken from the previously certified governed execution:

- one real governed production execution completed;
- user `10.0.0.2` moved from `awg3` to `vless`;
- execution verification passed;
- rollback was not required;
- trust feedback was active;
- prediction feedback was active;
- recommendation feedback was active;
- operator approval pipeline was active;
- production registry still shows `ip=10.0.0.2 current=vless table=100 enabled=1`.

Existing owners reused:

| Area | Existing Owner | Reuse Decision |
| --- | --- | --- |
| Planner | `tools/v7-users-autoswitch` | REUSE |
| Execution | `tools/v7-users-autoswitch --apply --verify` | EXTEND |
| Approval packet | `tools/v7-operator-execution-packet` | REUSE |
| Rollback | `tools/v7-users-autoswitch --rollback-packet --apply --verify` | REUSE |
| Trust/prediction/recommendation feedback | `admin_core/operator_execution_feedback.py` | REUSE |
| Blast radius evidence model | `admin_core/intelligence_platform.py` | REUSE |
| Runtime truth | `tools/v7-truth-check`, `tools/v7-convergence-owner` | REUSE |

Authority reality:

- The only live production movement evidence currently supports `CANARY`.
- Existing blast radius models can reason about larger tiers, but they remain evidence/model layers.
- Runtime authority must therefore default to `CANARY=1`.

## AUTHORITY_PRINCIPLES_REPORT

Applicable principles:

- Canary release: start with the smallest meaningful production unit.
- Progressive delivery: increase only after successful outcome evidence.
- Blast radius control: hard cap movement size at runtime.
- SRE error-budget thinking: failures, rollbacks, stale evidence, or verification misses demote/freeze.
- Staged rollout governance: the next class must be explicitly prepared and bounded.

Not applicable now:

- automatic production autonomy;
- unrestricted pool movement;
- percentage-based rollouts across the whole user base;
- heavy runtime analytics before apply;
- network-dependent runtime authority decisions.

## AUTHORITY_CLASS_MODEL

The model is conservative and evidence-gated:

| Class | Runtime Budget Ceiling | Evidence Meaning |
| --- | ---: | --- |
| `CANARY` | 1 | One governed production move is certified. |
| `SMALL_BATCH` | 2 | Next staged cohort after canary success, still operator-approved. |
| `MEDIUM_BATCH` | 5 | Requires successful small-batch outcomes and rollback confidence. |
| `LARGE_BATCH` | 10 | Requires repeated stable cohorts and no recent demotion signals. |
| `POOL` | 25 | Requires separate production certification; not current authority. |

The runtime enforces each class ceiling even if policy attempts to raise the budget above that class.

## CURRENT_AUTHORITY_CLASSIFICATION

Current class: `CANARY`

Current allowed user budget: `1`

Current promotion status:

- Eligible to prepare `SMALL_BATCH=2` under explicit operator approval and recheck.
- Not eligible for autonomy.
- Not eligible for medium/large/pool movement.

Current demotion risks:

- rollback required;
- verification failure;
- trust degradation;
- prediction miss;
- recommendation failure;
- snapshot mismatch;
- restore barrier mismatch;
- service/channel instability;
- disabled authority gate.

## CANARY_POLICY

Rule 16 decision/action state:

| Field | Value |
| --- | --- |
| Condition | One successful governed production execution exists; no rollback required; autonomy disabled. |
| Decision | Keep current runtime authority at `CANARY`. |
| Action | Allow at most one selected move after planner selection and before restore barrier/snapshot/apply. |
| Executor | `tools/v7-users-autoswitch` |
| Trigger | `planner_selected_moves_ready` |
| Written Evidence | `plan.safety.authority_budget_gate` |
| Blocked Actions | selected moves above authority budget; apply above authority budget |
| Next State | `SMALL_BATCH` only after explicit prepared policy and operator approval |

## ANTI_FLAPPING_POLICY

Existing anti-flapping protections remain active:

- existing cooldown from switch policy;
- existing autoswitch safety state;
- user freeze limits;
- target block penalties;
- pair reversal window;
- rollback penalties;
- egress quarantine after failed verification.

Authority gate adds explicit policy evidence fields:

- `minimum_residence_seconds=300`
- `cooldown_seconds=180`
- `promotion_delay_seconds=900`
- `demotion_delay_seconds=0`
- `rollback_penalty_seconds=3600`

No policy allows channel hopping every minute.

## PROMOTION_POLICY

Promotion from `CANARY` to `SMALL_BATCH` requires:

- one-user governed execution success;
- verification passed;
- rollback not required;
- trust feedback positive or non-negative;
- prediction feedback positive or non-negative;
- recommendation feedback positive or non-negative;
- no current restore barrier blocker;
- no snapshot gate blocker;
- explicit prepared `authority_budget` policy state;
- operator-approved next cohort.

Promotion does not enable autonomy.

## DEMOTION_POLICY

Immediate demotion/freeze triggers:

- rollback required;
- rollback failed;
- verification failed;
- trust feedback negative;
- prediction feedback negative;
- recommendation feedback negative;
- source hash mismatch without bounded refresh;
- snapshot gate stop;
- restore barrier mismatch;
- authority gate disabled;
- service/channel instability.

Demotion action:

- set current authority to `CANARY` or budget `0`;
- block movement above current budget;
- require operator review and fresh evidence before promotion.

## AUTHORITY_BUDGET_GATE

Implementation:

- File: `tools/v7-users-autoswitch`
- Runtime evidence path: `plan.safety.authority_budget_gate`
- Truth source: existing `policy.json` / `org-policy.json`
- Default if no policy is prepared: `CANARY`, budget `1`

Runtime behavior:

1. Planner selects candidate moves as before.
2. Existing request cap `--max-selected-moves` is applied as before.
3. Authority budget gate applies a hard cap.
4. Restore barrier and snapshot gates run after authority capping.
5. Apply can only operate on remaining selected moves.

Performance boundary:

- no network calls;
- no audit history scan;
- no per-user external scan;
- no new snapshot root;
- no new truth source;
- in-memory cap only.

Fail-closed behavior:

- if gate is disabled by policy, selected moves are dropped to zero;
- if a policy tries to set `CANARY` budget above `1`, runtime clamps it to `1`;
- if `SMALL_BATCH` is prepared, runtime clamps it to `2`.

## AUTHORITY_ACTION_MATRIX

| Class | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CANARY` | selected moves <= 1 | allow within canary | continue existing lifecycle | `tools/v7-users-autoswitch` | planner selected moves ready | `plan.safety.authority_budget_gate` | moves above 1 | `SMALL_BATCH` |
| `SMALL_BATCH` | prepared policy and selected moves <= 2 | allow small batch | continue existing lifecycle | `tools/v7-users-autoswitch` | operator-approved next cohort | `plan.safety.authority_budget_gate` | moves above 2 | `MEDIUM_BATCH` |
| `MEDIUM_BATCH` | future certified evidence and selected moves <= 5 | allow medium batch | continue existing lifecycle | `tools/v7-users-autoswitch` | separate certification | `plan.safety.authority_budget_gate` | moves above 5 | `LARGE_BATCH` |
| `LARGE_BATCH` | future certified evidence and selected moves <= 10 | allow large batch | continue existing lifecycle | `tools/v7-users-autoswitch` | separate certification | `plan.safety.authority_budget_gate` | moves above 10 | `POOL` |
| `POOL` | future pool certification and selected moves <= 25 | allow pool cap | continue existing lifecycle | `tools/v7-users-autoswitch` | separate certification | `plan.safety.authority_budget_gate` | moves above 25 | `POOL_MONITOR` |

## PRODUCTION_EVIDENCE_VALIDATION

Read-only validation:

- production registry: `ip=10.0.0.2 current=vless table=100 enabled=1`
- production baseline dry-run before deploying this gate: `selected_move_count=0`
- production baseline dry-run before deploying this gate: `authority_budget_gate=null`

Interpretation:

- prior governed movement remains present on production;
- this program did not run `autoswitch --apply`;
- authority gate is local implementation until deploy/provenance sync.

## AUTHORITY_SIMULATION_REPORT

Simulated by unit tests:

- default `CANARY` caps a large requested movement set to `1`;
- prepared `SMALL_BATCH` permits `2` and caps above `2`;
- policy cannot raise `CANARY` above class ceiling `1`;
- disabled authority gate fails closed and drops selected moves to `0`;
- existing pool distribution tests pass when prepared authority explicitly permits larger batch tests.

Test results:

- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`: `30 tests OK`
- `python3 -m unittest tests.unit.test_best_available_pool_policy tests.unit.test_v7_users_autoswitch_policy`: `36 tests OK`
- `python3 -m unittest discover tests`: `315 tests OK`

## AUTHORITY_RUNTIME_IMPLEMENTATION

Implemented runtime fields:

- `plan.safety.authority_budget_cap_applied`
- `plan.safety.authority_budget_gate`
- `plan.safety.dynamic_blast_radius.selected_after_request_cap_count`
- `plan.safety.dynamic_blast_radius.selected_after_authority_budget_count`
- `plan.safety.dynamic_blast_radius.authority_allowed_user_budget`

The implementation extends the existing executor only.

No execution command was added.

No deploy-only truth source was added.

## AUTHORITY_DUPLICATION_AUDIT

| Check | Result |
| --- | --- |
| Second planner created | `false` |
| Second governance created | `false` |
| Second execution path created | `false` |
| Second rollback owner created | `false` |
| Second authority system created | `false` |
| Second truth source created | `false` |
| New snapshot root created | `false` |
| Heavy runtime calculation added | `false` |
| Network call in apply path added | `false` |
| Per-user runtime scan added | `false` |

## Final Verdicts

| Verdict | Value |
| --- | --- |
| `authority_model_defined` | `true` |
| `authority_budget_gate_implemented` | `true` |
| `anti_flapping_policy_defined` | `true` |
| `promotion_policy_defined` | `true` |
| `demotion_policy_defined` | `true` |
| `authority_action_matrix_complete` | `true` |
| `current_authority_class` | `CANARY` |
| `current_allowed_user_budget` | `1` |
| `next_allowed_user_budget` | `2` |
| `safe_for_next_cohort` | `true` |
| `safe_for_bounded_autonomy` | `false` |
| `safe_for_production_autonomy` | `false` |
| `new_truth_sources_created` | `false` |
| `duplicate_systems_created` | `false` |
| `users_moved` | `1` production evidence, `0` in this program |
| `autoswitch_apply_run` | `false` |

`SAFE_NEXT_STEP=DEPLOY_AUTHORITY_BUDGET_GATE_THEN_RUN_READ_ONLY_DRY_RUN_AND_PREPARE_OPERATOR_APPROVED_SMALL_BATCH_2`

Do not enable autonomy. Do not move more than one user until the authority budget gate is deployed and production dry-run evidence shows `authority_budget_gate` active.

