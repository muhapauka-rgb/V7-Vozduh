# V7 Admin Operator Write Feedback Recovery

**Date:** 2026-08-29  
**Scope:** Admin UI feedback for service-priority changes; revalidation of profile issuance and operator-selected channel binding.

## Finding

The reported priority change was not lost. The live audit records successful
writes for the affected operator-selected identity; the last one persisted the
chosen service groups in the canonical preference state.

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
- Safe deployment — PASS; local, GitHub and Runtime are aligned.
- Live `v7-admin-api.service` — active after deployment (16:02:09 MSK).
- The running admin program exactly matches the deployed source.

## Next step

Refresh the browser once, then choose a channel from a user row. The selected
channel must appear immediately; V7 confirms the actual route in the background
within seven seconds or restores the previous displayed channel with a clear
error.
