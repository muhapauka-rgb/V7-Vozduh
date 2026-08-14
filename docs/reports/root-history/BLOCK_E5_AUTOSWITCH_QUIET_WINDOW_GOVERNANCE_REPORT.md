# V7 Vozduh Block E5 Report

## Autoswitch Quiet Window Governance & Mutation Freeze Model

Block E5 formalized quiet-window governance for a future one-user canary. No autoswitch hold, timer stop/disable, service mutation, user-switch, routing-sync, autoswitch apply, canary, route mutation, ip rule mutation, nft mutation, kill switch mutation, restart, deploy, chmod/chown, or runtime file mutation was performed.

## 1. Who Can Move Users

User movement can be initiated by:

- `v7-users-autoswitch --apply`;
- `v7-users-autoswitch.timer` via its service;
- admin `/api/actions/autoswitch-apply-guarded`;
- channel-scoped autoswitch UI actions;
- admin `/api/actions/user-switch`;
- direct `v7-user-switch`;
- egress pause/delete migration flows that call `v7-user-switch`.

Advisory layers that can influence future movement:

- Telegram sentinel;
- reconnect observation;
- load/rebalance logic;
- failover logic;
- quality/service matrix state;
- policy settings.

## 2. Why Autoswitch Authority Is Dangerous Now

The service is configured to run:

```text
/usr/local/bin/v7-users-autoswitch --apply
```

The planner can also write load/reconnect summaries without applying moves. This means the control plane is not quiet enough for canary attribution.

## 3. Quiet Window Definition

A quiet window is a bounded interval where:

- autoswitch apply cannot run;
- no autoswitch process is active;
- registry snapshots are stable;
- route/rule snapshots are stable;
- no switch-history movement appears;
- no planner writes canary-critical observation state;
- only approved read-only checks run.

Minimum observation: 2 autoswitch timer periods plus 10 seconds.

## 4. Safest Hold Model

The safest model is a separately approved autoswitch hold:

1. capture current timer/service state;
2. capture autoswitch safety/reconnect/load/switch-history;
3. hold apply authority;
4. confirm no active autoswitch process;
5. observe quiet interval;
6. run canary only if all gates pass;
7. restore exact previous autoswitch state after post-checks.

This block did not execute the hold.

## 5. Mutation Freeze Boundaries

Forbidden during quiet window:

- autoswitch apply;
- autoswitch production dry-run;
- routing-sync;
- policy/Direct/RU/proxy/Trusted RU mutation;
- kill switch rebuild;
- generic rollback;
- any user-switch outside the approved candidate.

Allowed:

- read-only checks;
- route/rule show;
- local planner preview;
- approved one-user switch only after GO.

## 6. Current Control-Plane Stability

```text
current_quiet_window_status=unstable
control_plane_stability=unstable
current_canary_status=NO-GO
```

Reason: autoswitch authority remains active and production autoswitch planning paths can write state.

## 7. Can Future Canary Be Interpretable?

Yes, but only after a quiet window is created and verified. Without that, a canary result cannot be attributed to the operator action because autoswitch or planner writes may interfere.

## 8. Remaining Live Canary Blockers

- autoswitch hold not approved or executed;
- reconcile truth not proven under a quiet window;
- candidate penalty history;
- target egress readiness/quality;
- Trusted RU stale state where relevant.

## 9. Exact Next Step

Prepare a separate approval packet for a read-only quiet-window rehearsal:

```text
no canary
hold autoswitch authority under approval
observe quiet interval
run read-only rule/route/reconcile checks
restore autoswitch authority
```

Only after that should one-user canary approval be reconsidered.

## 10. Runtime Mutation

```text
Runtime mutation performed: NO
Autoswitch hold executed: NO
Autoswitch apply executed: NO
Canary executed: NO
Routing/user mutation executed: NO
```

## 11. Files Created Or Updated

```text
docs/track7/control-plane/AUTOSWITCH_AUTHORITY_MAP.md
docs/track7/control-plane/QUIET_WINDOW_DEFINITION.md
docs/track7/control-plane/AUTOSWITCH_FREEZE_MODEL.md
docs/track7/control-plane/MUTATION_FREEZE_BOUNDARIES.md
docs/track7/control-plane/CONTROL_PLANE_STABILITY_SIGNALS.md
docs/track7/control-plane/CANARY_WINDOW_RUNBOOK.md
tools/v7-control-plane-governance-check
```

## 12. Verification Results

```text
tools/v7-run-tests: 39 tests OK, py_compile OK
tools/v7-control-plane-governance-check --pretty: OK, current_quiet_window_status=unstable, execution_allowed_now=False
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: OK, critical lineage gaps known=33
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: OK, release object ready=True, remaining known unresolved=43
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile ...: OK
python3 -m json.tool canary preview artifacts: OK
git diff --check: OK
```
