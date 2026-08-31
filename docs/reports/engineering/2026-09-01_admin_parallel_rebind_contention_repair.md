# Admin parallel channel-switch contention repair — 2026-09-01

## Trigger and current evidence

Operator reports showed that one manual channel choice could work while two or
three simultaneous choices appeared to fail or required repeated clicks.  The
runtime audit established that the failures were not dropped HTTP requests:

- automatic recovery held the existing global `/tmp/v7-users.lock` while it
  completed bounded route work;
- `v7-user-switch` waited up to 20 seconds for that lock;
- the admin route endpoint stopped the subprocess after 7 seconds and exposed
  the result as a failed rebind (`writer_rc=124`);
- concurrent admin HTTP threads could both read the existing execution control
  as `OPEN` and race to write different one-user operation generations.

The route writer and the canonical execution-control file remain the existing
owners.  No user assignment, target selection, Matrix state, Planner state or
Authority was changed during this repair.

## Repair

1. The existing admin process now atomically reserves an exact one-user
   operation window for concurrent UI requests.  This is an in-process mutex
   around the existing control-file `OPEN -> CLOSED(operation)` transition,
   not a queue or a second state owner.
2. `v7-user-switch` now returns the stable code
   `ROUTE_WRITE_LOCK_BUSY` (exit `75`) when its existing global route lock is
   busy.  It does not mutate a route in that case.
3. The admin endpoint uses a one-second writer-lock wait inside its existing
   seven-second UI budget.  A held writer becomes a retryable response and the
   operation control is finalized back to `OPEN`.
4. The browser treats both a busy operation window and a busy route writer as
   retryable.  It retries with bounded backoff (140 ms to 700 ms) through the
   same endpoint and re-reads canonical state on each attempt.  The immediate
   optimistic row remains, while a confirmed route remains mandatory before
   success is shown.
5. If a Runtime-owned governed operation replaces the just-reserved control
   window, the admin request also yields rather than claiming a false failure.

## Verification

- `python3 -m unittest tests.unit.test_admin_realtime_truth tests.unit.test_v7_user_switch`
  — **40 PASS**.
- `bash -n tools/runtime-support/v7-user-switch` — **PASS**.
- Safe-deploy preflight — allowlist and GitHub truth **PASS**; the expected
  local Runtime changes require commit/publish before deployment.

## Publication and Runtime verification

- Commit: `2de154265723522fd98b563c04ce2037d0440c60`
  (`Stabilize parallel admin channel switches`), published to `Updatesystem`.
- Safe deploy: `deploy-z8-14-Updatesystem-2de1542-20260901T005009` — **PASS**.
- The deployed hashes match the committed runtime files:
  - `/usr/local/bin/v7-admin-api` —
    `c12e999119c28bab1dfa1a2494c1fd1aafe8e91fa476ae7f8827862b51c25faf`;
  - `/usr/local/bin/v7-user-switch` —
    `a9e530ad5d87e84640bb5987e06326f27e05b543a7eee33b9c4de40b09499fbf`.
- `v7-admin-api.service` and `v7-health.service` are both **active**.
- The existing execution-control owner is safely `OPEN/global` after deploy.

## Expected production effect and limit

Several clicks can now be made immediately.  They are not permitted to write
routes in parallel: the existing sole route writer still serializes mutations.
If an automatic recovery is actively changing routes, manual selections yield
briefly and retry rather than being falsely marked failed after seven seconds.
The actual number of successful switches inside seven seconds still depends on
the duration of each governed Core-primary route commit; this repair removes
the erroneous 20-second lock wait and execution-control overwrite, not the
safety verification itself.

## Next step

Commit, publish and safe-deploy this bounded repair; then observe several
independent operator clicks against the live Runtime without manually moving a
user from Codex.  Any remaining slow successful commit must be measured as a
route-writer/Core-primary duration issue, not hidden as an admin failure.
