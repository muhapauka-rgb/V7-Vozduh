# V7 Vozduh Block E3 Report

## Canary Blockers Resolution Planning & Safety Gates

Block E3 formalized the blockers that keep the one-user canary at NO-GO. No live canary, autoswitch hold, routing sync, user switch, policy apply, route mutation, nft mutation, kill switch mutation, restart, deploy, chmod/chown, cleanup, or runtime file mutation was performed.

## 1. Current Autoswitch Authority Risk

Autoswitch remains the largest immediate interference risk:

```text
v7-users-autoswitch.timer active/enabled
OnUnitActiveSec=20s
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

Even a correct one-user canary would be hard to interpret if autoswitch can move users during the observation window.

## 2. Safest Autoswitch Hold Model

The safest model is a separately approved, bounded autoswitch authority hold:

- capture pre-hold timer/service state;
- capture autoswitch safety state;
- prevent `v7-users-autoswitch --apply` from running during the canary window;
- confirm no autoswitch service instance is active;
- run only the approved one-user action;
- post-check and rollback if needed;
- restore the prior autoswitch timer state after observation.

This block did not apply the hold.

## 3. Root Cause Of Reconcile FAIL

`v7-reconcile-check` failed because it requires exact per-user `ip rule` lines:

```text
from <user-ip> lookup <table>
```

It reported 11 missing exact rules. Other read-only checks reported OK for kill switch, user route, and provisioning reconcile, so this is not proven datapath outage. It is an unresolved strict-contract failure and remains a hard canary blocker.

## 4. Real AWG3 Readiness Status

`awg3` is enabled, empty, load OK, and diagnostic OK. But sampled quality is below policy floor:

```text
1h avg_mbps=9.1
1h min_mbps=4.576
fail_rate=0.0716
stability=0.5101
```

## 5. Can AWG3 Ever Be Canary Target?

Yes, conditionally. It is reasonable for a one-user routing-mechanics canary because it is empty and routable. It is not GO-ready without either improved quality evidence or an explicit one-user quality waiver.

## 6. Updated GO / NO-GO

Current status:

```text
NO-GO
```

Hard blockers now include autoswitch active authority, unresolved reconcile FAIL, target egress quality below floor, candidate anti-flap penalty, stale Trusted RU state if relevant, and any need for routing-sync as first mutation.

## 7. Remaining Blockers

- autoswitch hold not approved/applied;
- reconcile FAIL unresolved;
- candidate user penalty history;
- target `awg3` below quality floor;
- Trusted RU/Gosuslugi-sensitive state stale;
- `v7-routing-sync`, policy apply, proxy apply, and kill-switch mutation remain high-risk.

## 8. Canary Status

```text
NO-GO
```

The canary is not conditional-GO yet because autoswitch and reconcile blockers are hard blockers.

## 9. Exact Next Step

Next step should be a read-only reconcile evidence packet:

```text
full ip -4 rule show
ip -4 route show table 1011
ip route get 8.8.8.8 from 10.7.0.13 iif wg0
v7-reconcile-check
v7-user-route-check
```

Then decide whether the reconcile failure is a false-positive checker contract issue or a routing rule repair requirement. Any repair remains out of scope until separately approved.

## 10. Runtime Mutation

```text
Runtime mutation performed: NO
Live canary executed: NO
Autoswitch hold executed: NO
v7-user-switch executed: NO
v7-routing-sync executed: NO
v7-users-autoswitch --apply executed by this block: NO
```

## 11. Files Created Or Updated

```text
docs/track7/control-plane/AUTOSWITCH_HOLD_GOVERNANCE.md
docs/track7/control-plane/RECONCILE_FAIL_ANALYSIS.md
docs/track7/control-plane/AWG3_CANARY_READINESS.md
docs/track7/control-plane/ONE_USER_CANARY_GOVERNANCE.md
docs/track7/control-plane/CANARY_GO_NO_GO.md
docs/track7/control-plane/CONTROL_PLANE_RISK_MATRIX.md
tools/v7-control-plane-governance-check
```

## 12. Verification Results

```text
tools/v7-run-tests: 39 tests OK, py_compile OK
tools/v7-control-plane-governance-check --pretty: OK, current_canary_status=NO-GO, execution_allowed_now=False
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: OK, critical lineage gaps known=33
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: OK, release object ready=True, remaining known unresolved=43
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile ...: OK
python3 -m json.tool canary preview artifacts: OK
git diff --check: OK
```
