# Admin manual assignment: stale-session repair and bounded background retry

Date: 2026-08-31  
Scope: V7 Admin v2 manual channel selection only.

## Observed production symptom

The operator selected a channel in the Users table, but the UI returned
`Канал не переключён / Csrf не выполнено`. This response is emitted before
the mutation handler, so no user route, registry assignment, Candidate,
Packet, Lease, Barrier, or Matrix state was changed by the rejected click.

## Cause

The page retained a stale CSRF token while its signed authenticated session
was still usable. `postJson` sent that old token and treated the safe 403
rejection as a final operational failure.

The same interface already made an immediate in-browser pending projection,
but the current existing execution-control owner permits one exact
`USER_SWITCH` route-writer window at a time. A second simultaneous operator
click could therefore see `operator_profile_execution_control_unavailable`
and be unnecessarily rolled back, even though the first bounded window would
shortly close.

## Repair

- Added a shared `refreshCsrfToken` path. On exactly `403 csrf_failed`, the
  page reads the existing `/api/session` token and retries the original request
  exactly once. The server verifies CSRF before dispatch, so the rejected first
  attempt has no mutation effect.
- Kept the current immediate visual selection and governed endpoint.
  Independent user clicks now retain their pending display and retry only the
  existing busy execution-control window every 140 ms, up to the established
  seven-second deadline. Each retry is still an explicit operator request to
  the existing `operator-profile-egress-rebind` owner, which alone opens its
  exact control window and invokes `v7-user-switch`.
- No Matrix, Planner, target selection, health rule, route writer, Authority,
  registry schema, timer, queue, or alternate source of truth was added or
  changed.

## Safety and concurrency boundary

The route writer currently has a global lock and Core-primary/registry
transactional preimage. It is not safe to delete that lock merely to make
kernel writes parallel. The repair makes separate operator choices accepted
immediately in the UI and processed automatically as soon as the existing
single governed window is available. True concurrent route mutation requires
a separate owner-backed concurrency proof; it is not claimed here.

## Verification

- `tests.unit.test_admin_realtime_truth`
- `tests.contracts.endpoint_inventory_test`
- `tests.unit.test_operator_execution_feedback`
- Result: 36 passed.
- `py_compile admin/v7-admin-api` with an isolated bytecode cache: passed.
- `git diff --check`: passed.

## Next step

Publish through `tools/v7-safe-deploy`, verify the deployed Admin runtime
fingerprint and service, then observe a real operator click. The real click
must be accepted without CSRF failure; V7 must execute the user-selected
governed path and report its actual completion time. Three seconds remains a
measurement goal, not an unproven promise.

## Deployment and runtime verification

- Commit published: `ea632b6a7f5189707e5af27c19f53b61b0249732`
  (`Repair admin manual switch session retry`) on `Updatesystem`.
- `tools/v7-safe-deploy` gate: PASS; GitHub and local workspace aligned.
- Safe deployment applied with only the existing Admin service restart.
- Runtime `/usr/local/bin/v7-admin-api` SHA-256:
  `366ee5340df5397de0d0a52292aa065b838d6b02da2d20a77624b42cb199f97b`,
  equal to the deployed source.
- `v7-admin-api.service`: active.
- `v7-health.service`: active.
- Runtime source contains both `refreshCsrfToken` and
  `requestOperatorProfileEgressRebind`.

The final behavioural proof is intentionally left to a fresh real operator
click. Codex did not select a user or a target and did not invoke the route
writer, preserving the live-runtime provenance rule.
