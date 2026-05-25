# Canary Window Runbook

This is a future runbook. It was not executed.

## 1. Pre-Window Checks

- confirm named candidate, target, previous egress, and table;
- confirm preview JSON has `mutation=false`;
- confirm rollback preview exists;
- capture `users.registry` hash;
- capture `ip -4 rule show`;
- capture candidate route table;
- run `v7-killswitch-check`;
- run `v7-user-route-check`;
- run `v7-provisioning-reconcile-check`;
- confirm target egress readiness.

## 2. Autoswitch Hold Validation

- apply only a separately approved hold;
- confirm `v7-users-autoswitch --apply` cannot run;
- confirm no autoswitch process is active;
- confirm admin apply paths are operationally frozen;
- confirm no recent switch-history event after hold start.

## 3. Quiet-Window Confirmation

Observe at least 2 timer periods plus 10 seconds. During that time:

- registry hash remains stable;
- route/rule snapshots remain stable;
- autoswitch safety state does not churn;
- reconnect/load summaries do not change from autoswitch planner;
- no user movement events appear.

## 4. Preview Confirmation

Re-run non-mutating preview using current snapshots:

```text
tools/v7-route-movement-preview user-switch ...
```

Confirm:

```text
mutation=false
runtime_commands_executed=false
errors=[]
blast_radius=one_user
```

## 5. Canary Execution Authorization

Execution requires explicit operator approval after all gates pass. Approval is only for:

```text
one user
one target egress
one rollback egress
one bounded window
```

## 6. Post-Checks

Immediately after future execution:

- candidate registry assignment expected;
- candidate assignment file expected;
- candidate route table expected;
- `v7-user-route-check` OK;
- `v7-killswitch-check` OK;
- no unexpected switch-history entries;
- no autoswitch process ran.

## 7. Rollback Conditions

Rollback is mandatory if:

- route table mismatch;
- route check fails;
- kill switch fails;
- target egress fails;
- user impact unacceptable;
- autoswitch interferes;
- unknown mutation appears.

## 8. Autoswitch Restore Conditions

Restore autoswitch authority only after:

- canary final state is known;
- rollback is complete if needed;
- post-checks are OK;
- operator records outcome;
- restore verification plan is ready.

## Current Applicability

Current status is NO-GO. The runbook cannot be executed until autoswitch hold governance and reconcile truth blockers are resolved.
