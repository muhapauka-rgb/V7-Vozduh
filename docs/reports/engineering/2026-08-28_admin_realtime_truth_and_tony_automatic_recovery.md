# V7 Admin realtime truth and Tony automatic recovery

Date: 2026-08-28  
Mission: `V7_ADMIN_REALTIME_TRUTH_AND_TONY_AUTOMATIC_RECOVERY_PROOF`  
Status: Block A deployed; Tony creation and visible-browser proof pending an explicit browser data-transmission confirmation.

## Scope and safety boundary

This report records two connected product rules:

1. Admin must show current client/channel truth, not a stale summary.
2. A new profile must never be placed on a channel which the existing Matrix/Planner currently rejects. Existing users remain subject to the existing automatic recovery path; this work did not move a user directly.

No new state owner, Planner, route writer, timer, registry, queue, or source of truth was added. No ordinary route was changed during this block.

## Root causes found

### Admin visible truth

* The admin overview had a 20-second cache and the visible page refreshed its cached overview every 8 seconds. Its worst-case assignment age could therefore exceed 20 seconds.
* `OverviewSnapshot.users` could prefer historical `v7-state.json` rows over `users.registry`. This allowed an old `vless` assignment to appear after the current routing owner had already moved the user to `awg0`.

### New-profile channel assignment

* The quick profile-issue path accepted an enabled requested channel, or chose the first enabled row of `egress.registry`.
* Being configured/enabled is not a safety admission. The existing Planner already owns the required Matrix, capacity, policy, service and reservation evaluation, but onboarding did not consume it.

## Implemented replacement

Commit `75c3b0d19890103d7802f7e0e62508f10c7bfcdc`:

* The overview now prioritizes nonempty `users.registry` over historical state rows.
* Added the read-only `/api/live-status` view. It reads the existing users registry, egress registry and Matrix directly and is returned with `Cache-Control: no-store`.
* The Admin page polls this compact operational truth every 500 ms and re-renders only routing/users/channels when it changes. The heavier overview remains at its established lower rate.

Commit `f6e2e638f9ccb3f17e674c9049eba68fc78a2537`:

* Added `v7-users-autoswitch --new-user-admission`, a read-only existing-Planner consumption for a not-yet-provisioned ordinary profile.
* The representative identity exists only in memory. Membership/load are rebuilt from canonical `users.registry`; health is read from the existing Matrix. It creates no identity, Packet, lease, route or client move.
* Both standard profile-issue paths in Admin now call this admission before IPAM/profile provisioning. A requested channel is used only if the Planner itself admits it; otherwise the Planner-selected admitted target is used. If there is no target, creation fails closed.

## Verification and deployment

Focused tests:

```text
237 tests passed
tests.unit.test_admin_realtime_truth
tests.unit.test_api4_overview_performance
tests.unit.test_v7_users_autoswitch_policy
tests.unit.test_service_aware_policy
```

Deploy:

```text
tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED \
  --restart-admin-if-changed --restart-health-if-changed
PASS
```

Post-deploy evidence:

* Runtime hashes equal the local hashes for both `/usr/local/bin/v7-admin-api` and `/usr/local/bin/v7-users-autoswitch`.
* `v7-admin-api.service` and `v7-health.service` are active.
* Unauthenticated `GET /api/live-status` returned `401` in `3.883 ms` with `Cache-Control: no-store`, proving the installed endpoint and no cacheable response.
* The normal Matrix owner was run for `vless`, `awg0`, and `awg3`; no user was moved by these observations.

## Fresh admission result

The current existing Planner received the default ordinary profile contract:

```text
services: youtube, instagram, telegram, google, google_auth
route class: VIDEO_OPTIMIZED
```

Result:

```text
VLESS: rejected
  health_code_000
  severity_FAIL
  avg_mbps_below_floor
  min_mbps_below_floor

automatic selected target: awg0
```

This is a system result, not a manual target substitution. It establishes the product rule `TONY_VLESS_INITIAL_ASSIGNMENT_CORRECTLY_REJECTED` when the requested identity is issued: Tony must be placed only on the current Planner-selected `awg0`, provided the same fresh admission remains valid at issuance time.

## Liza truth check

Current canonical registry entry:

```text
ip=10.7.0.125 current=awg0 table=1123 enabled=1
```

The automatic recovery completed earlier through the governed path; this work did not move Liza. The new Admin truth path now uses this current record over old snapshots.

## Remaining exact frontier

1. Authenticate in the visible Admin page and prove that Liza is displayed as `awg0` after an ordinary live read, with no manual page refresh.
2. Create the real ordinary identity `Тони`, phone `023456789`, exactly one device/profile through the existing Admin identity owner. Re-run the fresh admission at action time; VLESS must be rejected and the current Planner-selected healthy channel used.
3. Verify Tony's registry, visible Admin row, profile/device count, Matrix and automatic-recovery eligibility. Do not manually move Tony. If a natural source failure later occurs, the existing health/Matrix/Planner chain must perform the recovery and the final report will record it.

## Limitations

The browser-login and identity-form steps transmit administrator credentials and a person's phone number to the V7 Admin site. They await action-time confirmation under the browser safety policy. No production action is otherwise blocked.
