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

No route, Matrix, Planner, Authority, timer, user assignment, or health policy
was changed.

## Existing operator semantics revalidated

- New profile issuance accepts an enabled configured channel without waiting for
  a health decision; subsequent automated recovery remains responsible for a
  failed source.
- An operator's explicit different-channel choice for an existing device uses
  the existing one-user governed route writer.  It does not manually bypass the
  routing owner or substitute a target.

## Verification

- `python3 -m unittest tests.unit.test_admin_realtime_truth tests.unit.test_admin_service_preferences_lifecycle` — 10 PASS.
- `python3 -m unittest tests.contracts.endpoint_inventory_test` — 7 PASS.
- Python syntax compilation with a writable temporary bytecode cache — PASS.
- Live `v7-admin-api.service` — active before deployment.

## Next step

Publish and deploy this narrow UI-feedback repair, then verify that the running
admin API is aligned and that a priority save either displays the exact stored
groups or a clear rejection reason.
