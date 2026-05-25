# V7 Vozduh Block E6 Report

## Quiet-Window Rehearsal Approval Packet & Read-Only Stability Validation

Block E6 prepared the first real quiet-window rehearsal approval packet. No rehearsal, autoswitch hold, timer stop/disable/restart, user-switch, routing-sync, autoswitch apply, canary, route mutation, ip rule mutation, nft mutation, kill switch mutation, runtime file mutation, or deploy was performed.

## 1. Exact Rehearsal Model

The rehearsal objective is quiet observation only:

- hold autoswitch apply authority;
- observe stable registry/rule/route/switch-history state;
- run read-only reconcile and datapath checks;
- restore autoswitch authority;
- move no users.

Success means autoswitch was held, no users moved, snapshots stayed stable, checks completed, and autoswitch was restored.

## 2. Exact Hold / Restore Commands

Copy-pasteable commands are documented in:

```text
docs/track7/control-plane/AUTOSWITCH_HOLD_RESTORE_PACKET.md
```

Core future hold sequence:

```bash
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Core future restore:

```bash
systemctl start v7-users-autoswitch.timer
```

These commands were not executed in Block E6.

## 3. Quiet-Window Verification Logic

Verification requires:

- pre/hold/quiet/after timer and process checks;
- `users.registry` hash stability;
- route/rule snapshot stability;
- no new switch-history entries;
- no production autoswitch planner writes;
- restored timer state after rehearsal.

## 4. Reconcile Experiment Plan

The experiment runs two reconcile samples under a quiet autoswitch hold, with ip-rule snapshots around them. Current canary remains blocked unless reconcile passes or a false-positive waiver is approved from stable quiet-window evidence.

## 5. Current Remaining Blockers

- rehearsal not approved or executed;
- autoswitch authority still active in current runtime;
- reconcile not proven under quiet window;
- canary target/candidate gates still require revalidation;
- Trusted RU/quality/penalty blockers from earlier blocks still require final review.

## 6. Rehearsal Status

```text
CONDITIONAL
```

The packet is ready for approval review. It is not GO until a human explicitly approves the bounded hold/restore rehearsal.

## 7. Missing Approval

Still missing:

- human approval for rehearsal;
- permission to stop/start `v7-users-autoswitch.timer`;
- maximum rehearsal duration confirmation;
- approval that no canary will be run during rehearsal;
- restore/failure handling owner.

## 8. Next Live Step After Rehearsal

If rehearsal succeeds, the next step is not canary automatically. The next step is reviewing rehearsal evidence and deciding whether one-user canary approval can be considered.

## 9. Runtime Mutation

```text
Runtime mutation performed: NO
Rehearsal executed: NO
Autoswitch hold executed: NO
Canary executed: NO
Routing/user mutation executed: NO
```

## 10. Verification Results

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
rehearsal_docs_missing=0
rehearsal_status=CONDITIONAL
canary_blocked_until_rehearsal_succeeds=True
current_quiet_window_status=unstable
execution_allowed_now=False
```

Release object warning status remains intentionally conservative:

```text
runtime_lineage=partial
release_provenance=incomplete
known_43_production_only_tools_require_lineage
```

## 11. Files Created Or Updated

```text
docs/track7/control-plane/QUIET_WINDOW_REHEARSAL_MODEL.md
docs/track7/control-plane/AUTOSWITCH_HOLD_RESTORE_PACKET.md
docs/track7/control-plane/QUIET_WINDOW_VERIFICATION.md
docs/track7/control-plane/RECONCILE_QUIET_WINDOW_EXPERIMENT.md
docs/track7/control-plane/MUTATION_FREEZE_SAFETY_MATRIX.md
docs/track7/control-plane/HUMAN_APPROVAL_MODEL.md
docs/track7/control-plane/CANARY_GO_NO_GO.md
tools/v7-control-plane-governance-check
BLOCK_E6_QUIET_WINDOW_REHEARSAL_REPORT.md
```
