# Minimal Safe Experiment Design

Date: 2026-07-01 03:43 UTC

## Verdict

`SAFE_EXPERIMENT_DESIGNED`

## Hypothesis

`CURRENT_APPROVED_EMERGENCY_ENVELOPE` must be consumable by Runtime as legal execution authority for the first L3 One-User Production Validation rung.

This must not grant general autonomous authority.

## Current Rejecting Condition

The current rejection happens in `tools/v7-users-autoswitch`.

Flow:

```text
plan()
  -> _approved_plan_lock_validation()
  -> selected = approved_plan_lock["selected_moves"]
  -> _emergency_failover_authority_gate(selected, restore_barrier)
  -> gate["ok"] = bool(bounded) and not gate["blockers"]
  -> return [] when gate["ok"] is false
  -> apply() returns approved_plan_lock_selected_moves_missing
```

The exact unsafe behavior is not that the approved envelope is invalid. The approved plan lock is valid. The restore barrier was written. The selected move exists before the L3 emergency gate.

The rejecting condition is that `_emergency_failover_authority_gate()` treats the approved one-user production validation transaction as if it were normal autonomous emergency failover authority. When its autonomy blockers remain present, it clears the selected move.

## Safety Assessment

The condition is partially protecting real unsafe execution:

- no rollback must still stop;
- no verification must still stop;
- invalid target must still stop;
- stale/wrong/expired approved plan lock must still stop;
- wrong user/source/target/hash must still stop;
- normal autonomous runtime without certification must still stop.

But it is over-applying autonomous certification semantics to the first production validation rung.

The canonical graph permits:

```text
One User Production Validation
  -> approved operation / current approved emergency envelope
  -> one bounded execution
```

It does not require already-certified autonomous runtime for the first production proof.

## Smallest Experimental Patch

Patch only `tools/v7-users-autoswitch`.

Do not change:

- `admin_core/operator_execution_pipeline.py`;
- `admin_core/operator_execution.py`;
- restore barrier materialization;
- approved plan lock validation;
- packet/lease identity;
- verification;
- rollback;
- planner selection.

### Exact Condition To Change

Inside `plan()`, after:

```python
approved_plan_lock = self._approved_plan_lock_validation(restore_barrier)
```

and after restore barrier clearance/generation and snapshot gates pass, before or inside `_emergency_failover_authority_gate()`, recognize one narrow bridge:

```text
approved_l3_production_validation_envelope = TRUE
```

only if all are true:

- `args.apply == true`;
- `args.verify == true`;
- `args.rollback_on_verify_fail == true`;
- `emergency_failover_autonomy` mode was explicitly requested by the governed L3 production validation caller;
- `approved_plan_lock.present == true`;
- `approved_plan_lock.ok == true`;
- `approved_plan_lock.selected_move_count == 1`;
- restore barrier is `cleared == true`;
- restore barrier clearance generation/hash checks passed;
- selected move hash equals approved identity hash;
- allowed users exactly match the selected user;
- allowed targets exactly match the selected target;
- selected move type is `failover`;
- selected move has `current_egress != recommended_egress`;
- target is live and not disabled/down;
- user is live and still on the approved source;
- max selected moves / clearance budget is `1`;
- no approved-plan replacement/reselection flags are true.

When true:

```text
_emergency_failover_authority_gate()
  may mark gate.ok = true
  with decision = "authorize_one_user_production_validation_envelope"
  and selected_moves_after_gate = 1
```

This bridge must be recorded as:

```text
authority_source = current_approved_emergency_envelope
autonomy_certified = false
broad_automation_enabled = false
production_validation_only = true
```

### Files / Functions

Primary file:

- `tools/v7-users-autoswitch`

Primary functions:

- `AutoswitchPlanner.plan()`
- `AutoswitchPlanner._emergency_failover_authority_gate()`

Tests:

- `tests/unit/test_v7_users_autoswitch_policy.py`
- optionally `tests/unit/test_governed_canary_cli.py`

## Cases That Must Remain STOP_SAFE

| Case | Required behavior |
| --- | --- |
| No approved envelope | `STOP_SAFE`; no selected move |
| Stale/expired envelope | `STOP_SAFE`; existing approved plan lock expiry remains authoritative |
| Wrong user | `STOP_SAFE`; approved plan lock user validation fails |
| Wrong source | `STOP_SAFE`; approved plan lock source validation fails |
| Wrong target | `STOP_SAFE`; target scope mismatch or target validation fails |
| Hash mismatch | `STOP_SAFE`; selected move hash / clearance generation mismatch fails |
| More than one user | `STOP_SAFE`; selected count and clearance budget must be exactly one |
| Expired lock | `STOP_SAFE`; existing expiry validation remains authoritative |
| Missing rollback | `STOP_SAFE`; `rollback_on_verify_fail` required |
| Missing verification | `STOP_SAFE`; `verify` required |
| Target unsafe | `STOP_SAFE`; target disabled/down or services not ready still blocks |
| Source recovered | `STOP_SAFE`; live L3 eligibility must still catch recovered source |
| Non-L3 movement | `STOP_SAFE`; only failover/current-channel-failed L3 scope allowed |
| Normal autonomous runtime without certification | `STOP_SAFE`; bridge applies only to production validation envelope |
| Broad autoswitch | `STOP_SAFE`; no envelope, no one-user validation bridge |
| Timer-based movement | `STOP_SAFE`; no timer/daemon authority granted |
| Planner replacement/reselection | `STOP_SAFE`; approved plan lock forbids replacement |
| Restore barrier missing | `STOP_SAFE`; no clearance, no bridge |
| Restore barrier generation mismatch | `STOP_SAFE`; existing generation check remains authoritative |
| Atomic envelope mismatch | `STOP_SAFE`; existing apply validation remains authoritative |

## Tests To Add

1. Positive narrow test:
   - Build a valid one-user approved plan lock from an L3 production validation plan.
   - Restore barrier is cleared.
   - Verification and rollback flags are present.
   - Emergency autonomy enabled only as the L3 production validation execution mode.
   - Assert selected move survives `_emergency_failover_authority_gate()`.
   - Assert `gate.decision == authorize_one_user_production_validation_envelope`.
   - Assert `broad_automation_enabled == false`.
   - Assert `production_validation_only == true`.

2. Negative no envelope:
   - Emergency autonomy enabled, but no approved plan lock.
   - Assert selected moves are cleared and no apply happens.

3. Negative more than one user:
   - Approved plan lock contains two selected moves.
   - Assert `STOP_SAFE`.

4. Negative missing rollback:
   - Same valid envelope, but no `--rollback-on-verify-fail`.
   - Assert `rollback_required_for_emergency_failover` or equivalent blocker remains.

5. Negative missing verification:
   - Same valid envelope, but no `--verify`.
   - Assert verification blocker remains.

6. Negative target/user/source/hash drift:
   - Reuse existing approved-plan-lock tests:
     - changed user/source/target;
     - selected hash mismatch;
     - expired lock.
   - Assert all still fail before apply.

7. Negative normal autonomous runtime:
   - Emergency autonomy enabled without production validation envelope.
   - Assert it still requires certified/autonomous emergency evidence and does not use the bridge.

8. Integration-level governed cycle test:
   - L3 production validation routes through pipeline.
   - Fake apply path confirms the bridge is requested.
   - Assert runtime automation remains false and authority expansion remains false.

## Production Experiment

After tests pass and safe deploy succeeds, run exactly one production validation:

```bash
/usr/local/bin/v7-governed-canary-dry-run-cycle \
  --execute-l3-production-validation \
  --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED \
  --max-users 1
```

Expected success outcome:

- one fresh packet;
- one approved emergency envelope consumed;
- one selected move survives emergency gate;
- `_run_switch()` is reached;
- exactly one user moved if live gates and switch command pass;
- verification runs immediately;
- rollback runs if verification fails;
- learning/evidence closes terminal outcome;
- `production_proven = true` only after terminal closure;
- `certified = false` until OMP certification review;
- `active_capability = false` until certification/promotion;
- runtime automation remains disabled;
- authority remains unexpanded.

Expected safe failure:

- Any failed gate returns `STOP_SAFE`.
- No retry inside the same transaction.
- No user movement if the bridge conditions are incomplete.

## Rollback Plan

If the patch behaves unexpectedly:

1. Stop further L3 production validation attempts.
2. Revert the patch commit:

```bash
git revert <patch_commit>
```

3. Run:

```bash
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
tools/v7-truth-check --all --json
tools/v7-convergence-status --json
```

4. Deploy the reverted state using the existing safe deploy owner:

```bash
tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json
```

5. Re-run truth and convergence.

No runtime rollback user movement is needed unless the experiment already moved a user and verification failed; in that case the existing rollback-on-verification-fail path is the runtime rollback plan.

## Safety Invariants

- No new Runtime.
- No new Planner.
- No new Authority model.
- No new owner.
- No new execution path.
- No bypass of restore barrier.
- No bypass of approved plan lock.
- No bypass of atomic envelope validation.
- No bypass of L3 execution eligibility.
- No bypass of verification.
- No bypass of rollback.
- No broad autonomy.
- No timer.
- No daemon.
- No batch movement.
- No more than one user.
- No future reuse of the envelope.
- No certification or activation from the bridge alone.

## Final Verdict

`SAFE_EXPERIMENT_DESIGNED`
