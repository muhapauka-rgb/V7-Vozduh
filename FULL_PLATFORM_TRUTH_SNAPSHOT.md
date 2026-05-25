# V7 Vozduh Full Platform Truth Snapshot

## Scope

This is a read-only operational truth snapshot. No repair, optimization, canary, apply action, routing mutation, nft mutation, ip rule mutation, kill switch mutation, restart, deploy, chmod/chown, delete, or archive operation was performed.

Evidence:

```text
docs/track7/truth-snapshot/evidence/full-platform-readonly-combined.log
docs/track7/truth-snapshot/evidence/admin-endpoint-inventory.json
runtime-enumeration.json
tools/v7-control-plane-governance-check --pretty
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty
```

## 1. What Is Operationally Working

- Host is up: Ubuntu 26.04 LTS, kernel 7.0.0-14-generic, KVM VM.
- Core V7 services are active: admin API, local API, benchmark loop, health loop, client speed API, public gateway, proxy inbound test, OpenVPN egress, kill switch, MSS clamp.
- Interfaces are present: `wg0`, `tun0`, `awg0`, `awg3`, `v7e356a192b79`, `v7edb0c189291`, `v7e06a394c478`.
- `v7-user-route-check` is OK.
- `v7-killswitch-check` is OK.
- `v7-provisioning-reconcile-check` is OK.
- Direct/RU autosync state reports OK.
- Public gateway, admin API, client speed API, Caddy, and sing-box runtimes are active.

## 2. What Is Operationally Unstable

- Autoswitch is not quiet and not controlled by systemd timer/service alone.
- A non-systemd shell loop invokes `v7-users-autoswitch` every 30 seconds.
- Switch history shows many `autoswitch_failover` events on 2026-05-25.
- Quiet-window rehearsal was attempted and safely aborted because the external autoswitch loop remained active.
- `v7-reconcile-check` remains FAIL in read-only snapshots, with 9 errors in the latest full snapshot and 11 errors in E8 pre-hold evidence.

## 3. What Is Only Governance-Complete

- Runtime inventory is named.
- Many lineage batches are documented and repo-side resolved.
- Control-plane governance docs exist.
- Route movement preview exists.
- Quiet-window rehearsal governance exists.

These do not mean runtime is safe to mutate.

## 4. What Is Dangerous

- Autoswitch can move users and has multi-authority runtime control.
- `v7-routing-sync` can affect all enabled users.
- `v7-user-switch` affects live user assignment and route table behavior.
- Trusted RU / Direct RU / policy apply can influence sensitive route-class behavior.
- Proxy runtime apply can affect public and proxy surfaces.
- Kill switch mutation can affect leak protection globally.
- Rollback apply can restore broad runtime/config/auth/state targets.

## 5. What Is Blocked

```text
current_canary_status=NO-GO
current_quiet_window_status=unstable
quiet_window_verified=False
reconcile_under_quiet=NOT_SAMPLED_ABORTED
execution_allowed_now=False
```

Blocked:

- one-user canary;
- routing-sync;
- user-switch;
- autoswitch apply;
- policy apply;
- Direct/RU mutation;
- Trusted RU refresh;
- proxy runtime apply;
- kill switch mutation;
- rollback apply.

## 6. What Is NO-GO

Canary is NO-GO. The immediate blocker is not datapath failure; it is uncontrolled autoswitch authority. There is no trustworthy attribution if users can be moved concurrently by the external loop.

## 7. What Is Safe Enough

Safe enough now:

- read-only snapshots;
- static analysis;
- repo-side governance updates;
- lineage documentation;
- preview-only planning;
- local tests and py_compile;
- read-only runtime checks like route/killswitch/provisioning status.

## 8. Biggest Blast Radius

Largest blast radius layers:

1. `v7-routing-sync`: all enabled users.
2. Autoswitch apply / external autoswitch loop: potentially many users.
3. Policy/Direct/RU apply: route-class and sensitive traffic behavior.
4. Kill switch mutation: whole datapath safety.
5. Proxy runtime apply: public/proxy traffic.
6. Broad rollback apply: target-dependent, potentially platform-wide.

## 9. Rollback Clarity

Clearer:

- one-user switch rollback is conceptually clear but blocked until quiet window exists.

Unclear or dangerous:

- routing-sync rollback;
- policy/Direct/RU rollback;
- proxy runtime guard rollback;
- kill switch mutation rollback;
- broad `v7-rollback-last-change --apply`.

## 10. What Can Break The Platform

- Running canary while autoswitch loop is active.
- Running `v7-routing-sync` as first live mutation.
- Treating reconcile FAIL as harmless without quiet-window evidence.
- Running Trusted RU refresh/policy apply casually.
- Running proxy/kill-switch/rollback apply without bounded approval.
- Assuming release reproducibility is complete because the release object exists.

## 11. What The Next Chat Must Understand First

The platform is not broken in the simple sense: datapath, kill switch, provisioning, admin, proxy, and public surfaces are alive. The real blocker is control-plane authority. Autoswitch has at least one non-systemd authority that can move users outside timer/service hold. Until that is governed, quiet-window and canary are not trustworthy.

## 12. Snapshot Documents

```text
docs/track7/truth-snapshot/RUNTIME_IDENTITY_SNAPSHOT.md
docs/track7/truth-snapshot/RUNTIME_GOVERNANCE_SNAPSHOT.md
docs/track7/truth-snapshot/AUTOSWITCH_RUNTIME_SNAPSHOT.md
docs/track7/truth-snapshot/ROUTING_DATAPATH_SNAPSHOT.md
docs/track7/truth-snapshot/KILLSWITCH_RUNTIME_SNAPSHOT.md
docs/track7/truth-snapshot/TRUSTED_RU_RUNTIME_SNAPSHOT.md
docs/track7/truth-snapshot/PROXY_RUNTIME_SNAPSHOT.md
docs/track7/truth-snapshot/PROVISIONING_RUNTIME_SNAPSHOT.md
docs/track7/truth-snapshot/ADMIN_API_RUNTIME_SNAPSHOT.md
docs/track7/truth-snapshot/CONTROL_PLANE_STATUS_SNAPSHOT.md
docs/track7/truth-snapshot/RUNTIME_RISK_MATRIX.md
docs/track7/truth-snapshot/RECOMMENDED_NEXT_STEPS.md
```

## 13. Recommended Next Steps

Safe:

- Map and govern the non-systemd autoswitch loop owner and launch path.
- Prepare a second quiet-window rehearsal plan that can hold every autoswitch authority.
- Continue high-risk lineage resolution and static checks.

Conditional:

- Repeat quiet-window rehearsal only after non-systemd authority hold/restore is separately approved.
- Discuss canary only after successful quiet-window evidence.

Forbidden without separate approval:

- canary;
- user-switch;
- routing-sync;
- autoswitch apply;
- policy/proxy/Direct/RU/Trusted RU apply;
- kill switch mutation;
- rollback apply.

## 14. Verification

```text
tools/v7-run-tests: PASS, 39 tests
tools/v7-control-plane-governance-check --pretty: PASS
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: PASS, governance partial
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: PASS, release object ready with warnings
py_compile admin/v7-admin-api admin_core/*.py governance tools: PASS
admin endpoint inventory JSON validation: PASS
canary preview JSON validation: PASS
git diff --check: PASS
```

## 15. Runtime Mutation

```text
Runtime mutation performed: NO
Canary executed: NO
Apply actions executed: NO
Routing/datapath changed: NO
```
