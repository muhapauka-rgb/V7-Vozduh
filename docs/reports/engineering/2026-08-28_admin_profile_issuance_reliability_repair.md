# Engineering Report — Admin profile issuance reliability repair

Date: 2026-08-28

## Scope

Repair the current Admin profile/QR issuance path.  This is not a routing or
Matrix optimisation and does not move a user or change a route.

## Evidence before change

- The Admin process had previously been OOM-killed (`717.6M` peak); its current
  process remained large during investigation.
- The ordinary new-user admission was read-only and correctly selected `awg0`,
  while the currently requested `vless` was not admitted.  Its response carried
  full nested Planner diagnostics although the profile UI only needs the decision.
- The profile handlers rebuilt the full Admin overview synchronously after the
  profile/link/QR had already been created.  That expensive unrelated rebuild
  delayed the response that the browser needs to show the result.
- The UI showed all enabled channels as selectable and did not reliably surface
  an action error in the issuance result panel.

## Change

- Keep the same existing `AutoswitchPlanner` admission owner, but return its
  compact decision contract for profile issuance: egress, eligibility, score,
  blockers/reasons, state and capacity only.
- Return the completed profile/link/QR response immediately; the existing
  post-action browser refresh updates the broad overview afterwards.
- Show a clear issuance failure rather than leaving an ambiguous empty result.
- Rename the UI field to “Предпочтительный канал” and explain that V7 makes the
  final safety decision.  A failed VLESS request is therefore never silently
  forced onto a person.

## Verification

- `python3 -m py_compile admin/v7-admin-api tools/v7-users-autoswitch` — PASS.
- `python3 -m unittest tests.unit.test_admin_realtime_truth` — 5 PASS.
- No new owner, timer, registry, routing writer, Matrix logic or automatic user
  movement was added.

## Next step

Publish and deploy through `tools/v7-safe-deploy`, then verify the deployed
read-only admission output and the real Admin issue screen.  Entering Admin
credentials in a separate browser session requires contemporaneous operator
confirmation.
