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

### Verification after deploy

- Published/deployed commit: `de9f67b82d16b5aba613231655c378fda6775a3c`.
- Safe deploy passed; Admin and Health services are active.
- The live shared execution control remains valid `OPEN`, while the explicit
  Admin freeze is now `false`; therefore profile issuance is no longer blocked.
- A fresh full VLESS Matrix run at 2026-08-28 15:09 UTC returned `WARN`, 8/14:
  Telegram, Google, Apple, Google Auth and Facebook passed, while YouTube,
  Instagram, WhatsApp, Spotify, SoundCloud and Anthropic had connection resets.
  Accordingly, the existing Planner still lawfully selects `awg0` rather than
  VLESS for a newly issued ordinary profile.

## Follow-up: instant issuance / separate recovery law

The former design still made issuance wait for the read-only full Planner
twice: once in the quick issue handler and again immediately before device
provisioning. Even the compacted result took about 1.53 seconds per Planner
call, while its health decision was not the profile/QR operation the operator
asked for.

The Program is therefore corrected with a strict separation:

- issuance reads only the existing enabled `egress.registry` entry and honours
  the selected configured channel;
- it makes no Matrix, Planner, capacity, remote probe or route-writer call;
- Matrix and the governed Autoswitch chain remain the only owners of
  health-based recovery after confirmed failure;
- the obsolete `--new-user-admission` Planner adapter is removed rather than
  retained as an unused compatibility branch.

### Fresh runtime reconciliation

- The existing `v7-health.service` is active.
- `v7-users-autoswitch.service` last ended with exit status 2 on 2026-08-28
  while trying to process an earlier VLESS incident; it made zero moves. This
  is a real recovery-liveness defect, not proof of automatic recovery.
- The currently active delegated policy permits a one-user ordinary
  service-failure class, but the fresh VLESS Matrix row is not a new complete
  channel-wide incident: it has a healthy channel-liveness row and a mixture
  of fresh failures and recovered services. It cannot lawfully cause a
  switch until Matrix emits the exact current failure obligation.

### Runtime result after deployment

- Published/deployed implementation: `c07deba32d7d9b236a41fb454e6089d35bd40c09`.
- Both `v7-admin-api.service` and `v7-health.service` are active and the
  deployed Admin hash matches the committed artifact.
- A full Admin quick-issue preview on a non-persistent test identity completed
  in **727.5 ms**. It selected the requested `vless` registry entry,
  recorded `health_checked=false`, created no profile and changed no route.
  The prior two synchronous Planner calls alone had cost roughly 3.06 seconds.
- One current governed Matrix consumption cycle was then run with no manually
  supplied source, target or user. It made **zero** moves. Current actionable
  Matrix scope belonged to unrelated `awg0`/`awg3` incidents, and the existing
  owner stopped safely because there was no owner-backed actionable
  recommendation. VLESS was not manufactured into that scope.

## Follow-up: manual existing-device channel selection and QR latency

The Admin update form exposed a channel selector but, for an already existing
device, it did not pass that choice to any movement path. The operation only
regenerated a profile and delivery link. Therefore an operator selecting
another enabled channel could reasonably expect a move while the device stayed
on its previous assignment.

The behaviour is now explicit and bounded:

- new-profile issuance remains local and does not wait for a health check;
- choosing a different channel while updating an existing device is an
  operator-confirmed, exact one-user rebind, not an automatic health decision;
- the existing operation-scoped control and the sole existing route writer,
  `v7-user-switch`, perform the change; the API does not write routes itself;
- the user and selected channel are re-read by exact fingerprint immediately
  before the writer; registry assignment, assignment state and the writer's
  observed kernel interface must agree afterwards;
- a failed verification attempts the existing certified rollback invocation
  and always finalizes the operation control window; no substitute target is
  selected.

The Profile section now describes that distinction plainly. It no longer says
that the selected channel is merely a preference or that profile issuance will
run a synchronous health check.

The repeat-issue slow path was also narrowed. A Karing/VLESS reissue previously
rewrote an unchanged inbound configuration, validated it and restarted the
shared public inbound on every QR refresh. The binding now compares the desired
configuration and existing binding first. If both are already current and the
service is active, it only regenerates the profile and one-time link; no shared
inbound restart occurs. A changed assignment still validates and restarts the
runtime, with configuration/binding restoration on validation or restart
failure. The API response now reports separate profile and one-time-link timing
so the one-second goal can be checked from the actual UI path.

### Focused verification before deploy

- `python3 -m py_compile admin/v7-admin-api` — PASS.
- `python3 -m unittest tests.unit.test_admin_realtime_truth tests.unit.test_operator_execution_pipeline` — **62 PASS**.
- New focused fixture proves an unchanged Karing/VLESS reissue performs only an
  active-service check and does not restart the public runtime.
- No Matrix, Planner, timer, registry, route writer or parallel state source
  was added. The existing `/api/actions/user-switch` direct endpoint remains
  fail-closed; the new profile-update action uses the existing operation
  control plus the existing writer for one explicitly confirmed device.

## Next step

Deploy this bounded Admin repair, then measure the actual existing-device
profile-and-link response on a safe current identity. The fast reissue target
is one second; an operator-selected move is reported separately because it
includes real route application and verification. In parallel, run a controlled
Matrix/Polygon recovery proof through the existing owners: it must show that a
newly issued identity on a confirmed failed source reaches governed recovery
without an operator action. Repair the existing consumer only if that proof
shows a concrete liveness defect; the current `awg0`/`awg3` STOP_SAFE
recommendation gap remains separate from issuance.
