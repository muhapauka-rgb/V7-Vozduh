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

## Deployment and runtime evidence

- Published commit: `022ca46968281eab0f10fb71756a3abd6477d8f3` on `Updatesystem`.
- `tools/v7-safe-deploy --apply` — PASS.
- Runtime hashes for `v7-admin-api` and `v7-users-autoswitch` match the
  deployed local artifacts; `v7-admin-api.service` and `v7-health.service`
  are active.
- Fresh read-only admission remained correct: `awg0` selected; `vless`
  rejected with `health_code_000`, `severity_FAIL`, and both throughput-floor
  blockers.  No user or route was changed.
- Admission response reduced from about 104 KB to 3.7 KB; measured read-only
  selection time was 1.53 s.  The restarted Admin process was at about 111 MB
  current / 133 MB peak memory at verification.

## Follow-up: Safe Mode semantic repair

The live error shown by the repaired UI was `safe_mode_enabled`.  Investigation
showed the shared existing execution-control record in its valid terminal
`OPEN` state, written by `governed-execution-finalizer` after a completed
transaction.  `OPEN` correctly suspends automatic forward route mutation until
a new operation-scoped window exists; it is not an operator request to freeze
ordinary Admin work.  Admin had incorrectly treated the shared top-level flag
as both concepts, permanently blocking profile issuance.

The repair preserves the existing execution-control owner and file.  It stores
an explicit Admin-only freeze under `admin_safe_mode` in that same canonical
record and refuses to change it while an operation-scoped control window is
active.  The terminal `OPEN` state no longer blocks profile/QR issuance.

## Next step

Publish and deploy through `tools/v7-safe-deploy`, then verify the deployed
read-only admission output and the real Admin issue screen.  Entering Admin
credentials in a separate browser session requires contemporaneous operator
confirmation.
