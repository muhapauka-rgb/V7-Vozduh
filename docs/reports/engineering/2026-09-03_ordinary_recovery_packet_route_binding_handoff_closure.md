# V7 ordinary recovery Packet/route binding handoff closure

## Outcome

The live ordinary recovery chain was functionally blocked after
Candidate/Packet/Lease/Barrier.  The generic defect is fixed and deployed in
runtime commit `b860f6fd84b67b0cd9146c15491eaf3ca1e2179c`.

No user was switched manually.  The existing `v7-health.service` caller
automatically consumed the already-current incidents and completed governed
route changes after deployment.

## Root cause

`v7-governed-canary-dry-run-cycle` correctly opened an operation control
window using the immutable Packet representation.  The sole route writer,
`v7-users-autoswitch`, separately built the existing operation-scoped route
binding.  These owners intentionally hash different canonical payload shapes,
but the writer required their hashes to be equal.  Therefore valid ordinary
transactions reached the final Apply boundary and were denied indefinitely.

The correction keeps both validations and removes only the invalid cross-owner
hash equality:

- execution control remains bound to exact Packet operation, selected moves,
  action class, source/snapshot hashes and user budget;
- the current route-writer operation binding must independently remain
  `BOUND`;
- stale/foreign control windows, changed selected moves and missing bindings
  still fail closed;
- no owner, queue, timer, watcher, registry, retry loop or truth source was
  added;
- cadence, timeout and S11 semantics were not changed.

## Verification

- Focused Packet/control/binding tests: `4 PASS`.
- Full `test_v7_users_autoswitch_policy`: `247 PASS`.
- `git diff --check`: `PASS`.
- The wider governed-canary suite still exposes two failures that reproduce
  unchanged on parent commit `300dc9fc`; they are not introduced by this
  change (`in_process` fixture expectation and medium-budget source argument
  expectation).
- Safe-deploy allowlist/truth gate: `PASS`.
- GitHub/local semantic commit: `b860f6fd84b67b0cd9146c15491eaf3ca1e2179c`.
- Local and Runtime `v7-users-autoswitch` SHA-256:
  `bf2ab30ea16a27b3cfc729c15663a946b924b79139db5766f9e35e23cd6f0456`.
- `v7-health.service`: active and enabled.
- Old standalone autoswitch and Matrix refresh timers: inactive.

## Live automatic evidence

At `22:24:23 MSK`, the normal persistent health caller emitted
`ACTION_COMPLETED`, `runtime_mutation_performed=true`, `users_moved=2` for the
current VLESS failure.  The immutable Packet chain completed without a manual
operational transition.

At `22:25:08 MSK`, after the health service restart, the normal caller emitted
a second `ACTION_COMPLETED`, `runtime_mutation_performed=true`,
`users_moved=3`.  The current ordinary subjects are now:

| User | IP | Current egress | Route truth |
|---|---|---|---|
| Liza | `10.7.0.125` | `awg0` | registry = assignment; Core-primary PASS |
| Chuck | `10.7.0.126` | `awg0` | registry = assignment; Core-primary PASS |
| Chuck2 | `10.7.0.127` | `awg0` | registry = assignment; Core-primary PASS |

The remaining enabled identities on `vless`, `1` and the old OpenVPN source
are explicitly `certification_user=1`, group `polygon-l7-canary`; excluding
them from ordinary production recovery is the intended owner boundary.

## Timing

The change does not add waiting or increase cadence.  It converts a permanent
Apply denial into successful execution.  The first successful receipt was:

- current observation/receipt T0 to consumer start: `9.257 s`;
- consumer execution: `20.397 s`;
- current receipt T0 to completion: `29.654 s`;
- governed Apply and verification: `7.612 s`.

The next three-user receipt executed in `21.015 s`; its incident T0 was
historical and had accumulated before deployment, so its multi-minute
T0-to-completion value is not post-fix latency evidence.

Functional automatic recovery is restored, but the product latency SLO is not
claimed consumed.  The measured current residual remains the existing
governed Apply/verification and caller-to-consumer latency frontier; this
repair neither hides nor relaxes it.

## Final classification

`ORDINARY_RECOVERY_PACKET_ROUTE_BINDING_HANDOFF = CONSUMED`

`CURRENT_INCIDENT_ORDINARY_USERS_RECOVERED = YES`

`RECOVERY_LATENCY_SLO = NOT_CONSUMED`
