# Manual channel selection: Core-primary verification repair

Date: 2026-08-31  
Scope: V7 Admin v2 operator-selected channel change only.

## Production evidence before the repair

The mobile Admin response said both `Канал не переключён` and
`Operator profile rebind deadline exceeded`.  The audit shows that the
first operator action did invoke the existing `v7-user-switch` writer:

- `19:51:53 MSK`: `10.7.0.125` was written from `awg0` to `vless`.
- The Admin endpoint then returned verification failure.
- `19:52:24 MSK`: the normal V7 health recovery later moved that identity
  from unhealthy `vless` back to `awg0`.

Thus the visible rejection was not proof that the writer had done nothing.
It was a false negative in the Admin completion check.  The later automatic
recovery was left entirely to the normal Runtime caller.

## Cause

The Admin endpoint required the writer output to contain a legacy
per-user `dev <interface>` route observation.  The active V7 routing mode is
Core-primary class routing.  In that mode the authoritative completion signal
from the existing sole route writer is `V7_CORE_PRIMARY_SYNC=PASS`, emitted
only after its Core-primary map update commits.  Requiring the legacy text in
addition caused a successfully committed change to be reported as failed and
could trigger an unnecessary rollback.

## Repair

- Kept `v7-user-switch` as the sole route writer.
- Kept registry and assignment verification unchanged.
- Accepted kernel-path completion from either the existing Core-primary commit
  token or the legacy route observation; the response records which mode was
  used.
- Added `core_primary_committed` and `verification_mode` to the result and
  failure audit context.
- Did not change Matrix, Planner, Authority, health cadence, target choice,
  routing policy, locks, timers, queues, or state ownership.

## Verification before deployment

- Focused Admin, endpoint-inventory, and operator-execution tests: **37 passed**.
- `py_compile admin/v7-admin-api`: passed.
- `git diff --check`: passed.

## Remaining live proof

After deployment, a fresh operator click must produce
`APPLIED_AND_VERIFIED` when the governed writer commits.  If the chosen channel
is unhealthy, the separate live V7 health caller may subsequently move the
user to an admitted healthy channel; that automatic recovery must retain its
own provenance and timing evidence.

## Deployment and Runtime verification

- Published commit: `06e5d0d5e612b5df6a9e36ac112de9da20ec85af`
  (`Fix manual rebind Core-primary verification`) on `Updatesystem`.
- Existing `tools/v7-safe-deploy` gate: PASS; local and GitHub commits aligned.
- Safe deployment completed with the existing Admin restart path.
- Deployed `/usr/local/bin/v7-admin-api` SHA-256:
  `651db390b065f6eecb3bf360e6ec89f8bf8cfc43abc1867d4c0aaff00230381c`,
  equal to the deployed source.
- `v7-admin-api.service`: active.
- `v7-health.service`: active.
- Runtime source contains both the Core-primary completion token handling and
  the explicit response verification mode.
