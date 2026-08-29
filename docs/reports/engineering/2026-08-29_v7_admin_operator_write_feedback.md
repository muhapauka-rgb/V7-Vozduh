# V7 Admin Operator Write Feedback Recovery

**Date:** 2026-08-29  
**Scope:** Admin UI feedback for service-priority changes; revalidation of profile issuance and operator-selected channel binding.

## Finding

The reported priority change was not lost.  The live audit records five successful
writes for `10.7.0.127` on 2026-08-29 12:35-12:36 UTC; the last one persisted
`google`, `google_auth`, `instagram`, and `telegram` in the canonical
`service-preferences.json`.

The UI nevertheless had a real operator-facing defect: `saveUserPriorities`
announced success even when the API returned an error, and could redraw from an
older overview snapshot immediately after a successful write.  This made a
failed or newly saved change look indistinguishable from a no-op.

## Change

- Reject an unsuccessful priority-save response visibly; do not show a success
  message in that case.
- Prefer the just-written canonical preference payload over an older overview
  snapshot during the redraw.
- Show the exact saved service groups in the confirmation.
- Save a priority change immediately when the operator toggles a service.
  The explicit button remains available, but is no longer required.
- Remove the synchronous full-admin-overview rebuild from this small write. The
  response now contains only the exact canonical preference state, so the
  affected table cell and picker update without waiting for unrelated checks.

No route, Matrix, Planner, Authority, timer, user assignment, or health policy
was changed.

## Existing operator semantics revalidated

- New profile issuance accepts an enabled configured channel without waiting for
  a health decision; subsequent automated recovery remains responsible for a
  failed source.
- An operator's explicit different-channel choice for an existing device uses
  the existing one-user governed route writer.  It does not manually bypass the
  routing owner or substitute a target.

## Operator channel choice simplification

- Removed the obsolete intermediate approval drawer from the user-row channel
  chooser. Selecting a channel now immediately updates the row to a bounded
  "switching" state and starts the existing governed one-user rebind in the
  background.
- The rebind still uses `v7-user-switch` as the only route writer, verifies
  assignment and route, and restores the displayed previous channel on failure.
- The route writer has a seven-second deadline. A timeout is an explicit failed
  transition, never a silently pending UI action. A later health failure of the
  chosen source remains the existing automatic-recovery owner's responsibility.

## Verification

- `python3 -m unittest tests.unit.test_admin_realtime_truth tests.unit.test_admin_service_preferences_lifecycle tests.contracts.endpoint_inventory_test` — 19 PASS.
- Python syntax compilation with a writable temporary bytecode cache — PASS.
- Live `v7-admin-api.service` — active before deployment.

## Next step

Publish and deploy this narrow UI-feedback repair, then verify that the running
admin API is aligned and that a priority save either displays the exact stored
groups or a clear rejection reason.
