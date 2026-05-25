# V7 Vozduh Block E2 Report

## One-User Canary Readiness Audit & Operational Runbook

Block E2 prepared a real one-user canary plan and runbook, but did not execute the canary. No `v7-user-switch`, `v7-routing-sync`, `v7-users-autoswitch --apply`, route mutation, nft mutation, kill switch mutation, restart, deploy, chmod/chown, cleanup, or runtime file mutation was performed.

## 1. Current Autoswitch Authority

Autoswitch is currently live-authoritative:

```text
v7-users-autoswitch.timer active/enabled
OnUnitActiveSec=20s
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

This is the largest immediate canary interference blocker.

## 2. Current Canary Blockers

- Autoswitch can run `--apply` every 20 seconds.
- Most enabled users have recent autoswitch movement and penalty windows.
- Candidate `10.7.0.13` has `switches_1h=2`, `switches_24h=10`, and penalty until 2026-05-25T02:05:31Z.
- `v7-reconcile-check` returned FAIL with 11 missing `ip rule lookup table` errors.
- Target `awg3` is enabled and empty but below quality floor in the sampled quality summary.
- Trusted RU decision state is stale and Gosuslugi-sensitive.

## 3. Candidate User

Conditional candidate:

```text
user=10.7.0.13
current_egress=awg0
route_table=1011
```

This user is selected because route checks are OK and `v7-reconcile-check` did not flag table `1011`.

## 4. Candidate Target Egress

Conditional target:

```text
to_egress=awg3
target_interface=awg3
```

`awg3` is enabled and has 0 assigned users, but it is not GO-ready because its sampled quality is below policy floor.

## 5. Rollback Readiness

Rollback command for the future canary:

```text
v7-user-switch 10.7.0.13 awg0
```

Rollback preview exists at:

```text
docs/track7/control-plane/canary-previews/rollback-preview.json
```

Rollback is understandable but not live-proven.

## 6. Blast Radius

Forward preview:

```text
blast_radius=one_user
routes_would_change=ip route replace default dev awg3 table 1011
```

Registry-wide routing-sync preview:

```text
blast_radius=all_enabled_users_in_registry
routes_would_change=16
ip_rules_would_change=32
```

Therefore `v7-routing-sync` cannot be the first live mutation.

## 7. GO / NO-GO

Current status:

```text
NO-GO
```

The plan is specific enough for future approval review, but live execution is not safe under the current evidence.

## 8. What Must Change Before Live Canary

- Autoswitch apply authority must be held under separate approval.
- Candidate anti-flap penalty must clear or be explicitly waived by operator policy.
- `v7-reconcile-check` failure must be resolved or explained as non-blocking.
- Target egress must pass health/quality thresholds.
- Trusted RU relevance must be confirmed outside the canary path or separately refreshed under governance.
- Operator approval must be explicit for exactly one user.

## 9. Runtime Mutation

```text
Runtime mutation performed: NO
Live canary executed: NO
v7-user-switch executed: NO
v7-routing-sync executed: NO
v7-users-autoswitch --apply executed by this block: NO
```

Read-only checks and local preview generation only.

## 10. Verification Results

```text
tools/v7-run-tests: 39 tests OK, py_compile OK
tools/v7-control-plane-governance-check --pretty: OK, canary_executed=False, execution_allowed_now=False
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: OK, critical lineage gaps known=33
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: OK, release object ready=True, remaining known unresolved=43
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile ...: OK
python3 -m json.tool canary preview artifacts: OK
git diff --check: OK
```

## 11. Files Created Or Updated

```text
docs/track7/control-plane/LIVE_CANARY_READINESS_AUDIT.md
docs/track7/control-plane/CANARY_CANDIDATE_SELECTION.md
docs/track7/control-plane/CANARY_PREVIEW_OUTPUTS.md
docs/track7/control-plane/AUTOSWITCH_CANARY_INTERFERENCE.md
docs/track7/control-plane/CANARY_ROLLBACK_READINESS.md
docs/track7/control-plane/CANARY_BLAST_RADIUS.md
docs/track7/control-plane/CANARY_GO_NO_GO.md
docs/track7/control-plane/canary-previews/user-switch-preview.json
docs/track7/control-plane/canary-previews/rollback-preview.json
docs/track7/control-plane/canary-previews/routing-sync-preview.json
tools/v7-control-plane-governance-check
```

## 12. Recommendation

Continue governance. The next step should be resolving the canary blockers, especially autoswitch hold semantics and reconcile-check ambiguity. Do not proceed to live canary yet.
