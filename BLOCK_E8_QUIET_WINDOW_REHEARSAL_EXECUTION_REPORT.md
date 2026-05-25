# V7 Vozduh Block E8 Report

## Quiet-Window Rehearsal Execution

Block E8 executed the bounded quiet-window rehearsal attempt approved by the operator. The rehearsal did not run canary, did not run `v7-user-switch`, did not run `v7-routing-sync`, did not run autoswitch apply directly, and did not change routes, ip rules, nftables, kill switch, Direct/RU, Trusted RU, proxy runtime, or user registry.

The rehearsal aborted safely because autoswitch authority was broader than the systemd timer/service: after stopping `v7-users-autoswitch.timer` and `v7-users-autoswitch.service`, an external loop process still existed and invoked `v7-users-autoswitch`.

## 1. Autoswitch Timer Stopped

```text
systemctl stop v7-users-autoswitch.timer: rc=0
post-hold timer state: inactive
```

Evidence:

```text
docs/track7/control-plane/e8-evidence/hold-confirmation.txt
```

## 2. Autoswitch Service Stopped

```text
systemctl stop v7-users-autoswitch.service: rc=0
post-hold service state: failed
```

The service was not the only autoswitch authority. A separate loop process remained active.

## 3. User Movement

```text
Was any user moved by Block E8? NO evidence of E8-initiated user movement.
```

No `v7-user-switch`, `v7-routing-sync`, or canary command was executed by Block E8. The users registry hash stayed the same in the pre-rehearsal and post-abort read-only snapshots:

```text
90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
```

## 4. Routing Changed

```text
Was routing changed by Block E8? NO.
```

Block E8 did not execute route mutation commands. Route/rule evidence was captured read-only.

## 5. Quiet Window Verified

```text
quiet_window_verified=false
```

The quiet window was not verified because the rehearsal aborted immediately after hold confirmation.

Abort reason:

```text
active_control_plane_process_after_hold
```

The active process:

```text
/bin/bash -c while true; do v7-egress-history; v7-egress-stability; v7-egress-load; v7-egress-diagnose; v7-state-merge; v7-user-desired-state-save; v7-state-json-save; v7-users-autoswitch; sleep 30; done
```

## 6. Reconcile Under Quiet Window

```text
reconcile_under_quiet=NOT_SAMPLED_ABORTED
```

Pre-hold reconcile still reported:

```text
V7_RECONCILE_RESULT=FAIL
errors=11
```

Because quiet samples were not collected, Block E8 did not prove whether the reconcile failure disappears under a truly quiet control plane.

## 7. Users Registry Hash

```text
users.registry stable across pre and post-abort read-only snapshots: YES
```

The same hash appeared before hold and after restore:

```text
90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
```

## 8. IP Rules

```text
quiet-window ip rule stability: NOT VERIFIED
```

Reason: the rehearsal aborted before quiet samples A/B/C. Pre and post-abort read-only snapshots were captured and show the expected user lookup rules present, but they do not constitute a verified quiet-window stability sequence.

## 9. Route Tables

```text
quiet-window route table stability: NOT VERIFIED
```

Reason: the rehearsal aborted before quiet samples A/B/C. Pre and post-abort route table snapshots were captured read-only, and no route mutation was executed by Block E8.

## 10. Kill Switch

```text
pre-hold v7-killswitch-check: OK
post-abort v7-killswitch-check: OK
```

## 11. User Route Check

```text
pre-hold v7-user-route-check: OK
post-abort v7-user-route-check: OK
```

## 12. Provisioning Reconcile

```text
pre-hold v7-provisioning-reconcile-check: OK
post-abort v7-provisioning-reconcile-check: OK
```

## 13. Autoswitch Timer Restored

```text
systemctl start v7-users-autoswitch.timer: rc=0
post-restore timer state: active
post-restore timer enabled: enabled
```

Autoswitch timer authority was restored. The separate loop authority remained present before, during abort, and after restore.

## 14. Current Canary Status

```text
NO-GO
```

Canary is still blocked because the rehearsal did not create a quiet window and reconcile was not measured under quiet conditions.

## 15. Exact Next Recommendation

Do not run canary.

Next governance step:

```text
Map and govern the non-systemd autoswitch loop process, then prepare a second quiet-window rehearsal that can hold all autoswitch authorities, not only the systemd timer/service.
```

The next rehearsal must not proceed until the owner and safe hold/restore model for PID lineage `while true; ... v7-users-autoswitch; sleep 30` is documented and separately approved.

## 16. Runtime Mutation Outside Autoswitch Hold

```text
Runtime mutation outside approved autoswitch hold/restore: NO
Canary executed: NO
User switch executed: NO
Routing sync executed: NO
Autoswitch apply directly executed by Block E8: NO
Policy/proxy/Direct/RU/Trusted RU apply executed: NO
```

## 17. Evidence Files

```text
docs/track7/control-plane/e8-evidence/e8-combined.log
docs/track7/control-plane/e8-evidence/pre-rehearsal.txt
docs/track7/control-plane/e8-evidence/hold-confirmation.txt
docs/track7/control-plane/e8-evidence/abort.txt
docs/track7/control-plane/e8-evidence/post-restore.txt
docs/track7/control-plane/e8-evidence/post-abort-readonly.txt
docs/track7/control-plane/e8-evidence/summary.txt
docs/track7/control-plane/e8-evidence/remote-quiet-window-rehearsal.sh
```

## 18. Verification Results

```text
tools/v7-run-tests: PASS, 39 tests
tools/v7-control-plane-governance-check --pretty: PASS
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: PASS, runtime governance still partial
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: PASS, release object ready with lineage warnings
py_compile admin/v7-admin-api admin_core/*.py governance tools: PASS
JSON preview artifact validation: PASS
git diff --check: PASS
```

Important checker state:

```text
rehearsal_executed=True
rehearsal_aborted=True
autoswitch_restored=True
quiet_window_verified=False
reconcile_under_quiet=NOT_SAMPLED_ABORTED
rehearsal_abort_reason=active_control_plane_process_after_hold
current_operational_status=rehearsal_aborted_restored
current_canary_status=NO-GO
execution_allowed_now=False
```

Release object warning status remains intentionally conservative:

```text
runtime_lineage=partial
release_provenance=incomplete
known_43_production_only_tools_require_lineage
```
