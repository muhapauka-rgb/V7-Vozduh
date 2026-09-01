# V7 current live functional recovery and 7-second SLO — 2026-09-01

## Outcome of this logical block

`CURRENT_LIVE_AUTOMATIC_RECOVERY_FUNCTIONAL_CONSUMED` is proven for one live ordinary VLESS case.  This is **not** a 7-second SLO pass.

V7, rather than Codex, automatically moved the current ordinary identity `10.7.0.126` from `vless` to the Planner-selected `awg3`.  The governed transaction finished with route/application success and required-service S11 success.

## Current evidence

* Source: `vless`, Matrix incident `sfinc_0248075237e77090b3c2f7173c439a17`, identity generation `egid_be6367407f70e591005185a2`.
* Fresh Matrix observations recorded Google, Instagram and YouTube as transport timeouts.  The identity had five required services and remained an enabled ordinary user while assigned to VLESS.
* V7 health Runtime initiated the governed transaction.  Its causal binding says `event_provenance: V7_HEALTH_RUNTIME`, `scope_classification: ORDINARY_PRODUCTION_ONLY`, and selected the one current affected member.  No Codex route writer, target choice, assignment change, or recovery-consumer invocation occurred.
* Terminal receipt: `GOVERNED_TRANSACTION_COMPLETED`, `users_moved: 1`, `route_apply_failure_count: 0`, `verification_failure_count: 0`.
* Runtime registry after terminal: `ip=10.7.0.126 current=awg3 table=1124 enabled=1`.

## Repair consumed

Concurrent incidents previously invalidated an exact VLESS Packet lock because fallback validation compared the lock to a different, globally active emergency source.  The patch preserves an exact current ordinary service-failure source only when the current Matrix scope still proves it failed and every locked member is still in that exact scope.  It does not select a target, alter routing, or weaken stale/healthy-source rejection.

* Commit: `1a37ed4d58ed8c56403f199e8b0f165ea64d62e7` — `Fix exact source validation for concurrent failures`.
* Tests: new positive exact-source case and existing negative mismatched-source case passed; full `test_v7_users_autoswitch_policy`: 241 passed; Python compilation and `git diff --check` passed.
* Three failures in the broad service-failure/canary bundle predated this narrow repair and concern unrelated text/capture/baseline expectations; they were not hidden or changed.

## Deployment reconciliation

The initial safe-deploy manifest refresh marked the commit but did not replace the health Runtime binary because the required health restart flag was absent.  Runtime hash verification caught that mismatch before evidence was credited.  Safe deployment was rerun with the existing `--restart-health-if-changed` gate.

* Local and deployed `/usr/local/bin/v7-users-autoswitch` SHA-256: `f9e78267b52161dac8404887d84548a6efd5a0aa52821c3b5e52d789db3ed7e2`.
* The deployed file contains `approved_lock_current_source`.
* `v7-health.service` is active.

## Timing and SLO status

Current live retry that completed:

| Interval | Measured |
| --- | ---: |
| Matrix T0 to consumer start | 9,990 ms |
| Consumer execution | 19,862 ms |
| Matrix T0 to consumer completion | 29,853 ms |
| Planner | 2,049.612 ms |
| Packet and lease | 133.500 ms |
| Restore barrier | 110.960 ms |
| Apply and verification | 8,107.744 ms |
| Route writer | 2,373.122 ms |
| Required-service S11 | 4,737.877 ms |

The preceding retries stopped lawfully because another governed transaction held the one global operation-control window.  The final automatic retry ran when that owner completed.  This proves level-triggered re-entry, but also exposes the first timing blockers: cross-transaction control-window serialization and the combined route-writer/S11 interval.

`T_FIRST_VALID_FAILURE_OBSERVATION -> T_GLOBAL_ALL_AFFECTED_RECOVERED <= 7 s` is therefore still **ACTIVE and failing** for this evidence.  It must not be relabelled as a pass.

## Exact next step

Use the existing execution-control and governed-transaction owners to determine whether unrelated ordinary recovery scopes can use bounded independent operation windows without weakening exact Packet/Lease/Barrier ownership.  In parallel, measure which portion of required-service S11 is mandatory versus duplicated post-apply work.  Any change must preserve automatic V7 provenance and then be re-proved by a fresh live ordinary failure; Codex must not move the client.

## S11 residual correction deployed after the live receipt

The live S11 verifier spent `4,737.877 ms`.  The profile required Telegram together with other services, so its regular invocation included two optional Telegram diagnostic endpoints; one waited about four seconds.  Those endpoints are not part of the profile's S11 contract.

The existing Matrix verifier now accepts `--required-endpoints-only` for an observation-only service subset that *contains* Telegram, rather than only the legacy exact `telegram` subset.  The autoswitch owner applies that mode whenever Telegram is part of an ordinary profile.  All selected profile services remain checked in parallel; all five required Telegram endpoints remain checked; full canonical Matrix diagnostics remain unchanged.

* Commit: `61edfb75` — `Limit mixed-profile Telegram S11 to required endpoints`.
* Verification: focused mixed-profile and existing single-Telegram verifier tests passed; full autoswitch policy suite: 242 passed; syntax and whitespace checks passed.
* Deployed with the required health-service restart.  Runtime hashes now match the new local executables and both `v7-health.service` and `v7-admin-api.service` are active.

There is no current enabled ordinary user on VLESS after the completed automatic recovery; the remaining VLESS registry entry is disabled.  No new live SLO sample was manufactured.  The next lawful live ordinary failure/replacement must prove the new S11 timing.

### Non-mutating production verifier measurement

The deployed verifier was measured on current healthy `awg3` with the exact five-service profile (`google`, `google_auth`, `instagram`, `telegram`, `youtube`) in observation-only mode.  It changed neither Matrix state, routes, nor user assignments.

* all five required services passed;
* all five required Telegram endpoints passed;
* full S11 probe critical path: **824.718 ms**;
* the previous live mixed-profile S11 was **4,737.877 ms**.

This demonstrates a 3.9-second removable diagnostic delay has been removed while retaining the required profile contract.  It is a component measurement, not a replacement for a new complete automatic ordinary recovery receipt.
