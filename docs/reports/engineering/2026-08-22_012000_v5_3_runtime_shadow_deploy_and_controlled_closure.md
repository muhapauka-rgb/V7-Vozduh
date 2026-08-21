# V5.3 T0-T11 -- deployment, Runtime shadow and controlled closure

Date: 2026-08-22 01:20 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Block: deployment of the existing health lifecycle, Runtime shadow validation,
and closure of the remaining controlled evidence

## Result

The existing `v7-health.service` now runs the deployed single foreground
deadline loop.  Its FAST phase is live in observation-only mode, starts before
legacy work, and completed two consecutive Runtime phases successfully in
`9.588 s` and `9.951 s`.  The starts remained `30.000 s` apart, with no
deadline overrun.  No route, ordinary client, Candidate, Packet, lease or
execution record was created.

The controlled Matrix and governed recovery evidence is now complete: exact
subset and Full Matrix agree on healthy, required-service failure and
methodology-limited cases; the existing synthetic governed chain covers the
existing Candidate -> Packet -> Lease -> Barrier -> Apply -> verification
owners.  This is controlled/Polygon evidence, not a claim of an ordinary
production recovery.

## Root cause found during deployment

The new health loop initially returned `fast_rc=2` in 7-15 ms.  Read-only
inspection proved that `/usr/local/bin/v7-egress-diagnose` was an old runtime
file and did not recognise the already deployed loop's profile-service
arguments.  The safe-deploy manifest did not yet list that existing executable,
so the normal deploy transaction could not replace it.

Minimal repair:

- added the existing `tools/v7-egress-diagnose` ->
  `/usr/local/bin/v7-egress-diagnose` mapping to the existing safe-deploy
  allowlist and Runtime-entrypoint set;
- added a focused deployment-contract assertion;
- published commit `e73aa888149b7cbb76701880bf4efc87e07dc510`;
- deployed through the existing locked, backed-up safe-deploy transaction.

No owner, timer, queue, registry, state source, Matrix policy, route or client
rule was introduced or altered.

## Evidence and measurements

| Check | Result |
| --- | --- |
| C8, 1,000 active exact contracts, three Polygon phases | `19.441 / 22.324 / 22.030 s`; cap 8; no retained child |
| Live Runtime FAST phase after repair | `9.588 s`, `fast_rc=0`, no deadline miss |
| Next live Runtime FAST phase | `9.951 s`, `fast_rc=0`, 30-second start-to-start interval |
| Controlled Full vs exact subset | same decisive status; Full 14 checks vs subset 3 checks for one source |
| Controlled two-source before/after ledger | 28 -> 6 checks (`-78.6%`); 265.157 -> 67.306 ms (`-74.6%`) |
| Controlled Matrix/producer/governed regression | 139 tests passed in 6.395 s |
| GitHub / CPS / deployed Runtime convergence | `FULLY_ALIGNED` |

The previously observed Full Matrix lifecycle of about `85.675 s` remains the
production fallback baseline.  The 9.6-10.0 second Runtime FAST figures are
the whole observation-only health phase, so they are not presented as a direct
replacement for the Full Matrix duration.

## Runtime and production observation

- The deployed health process is active and uses the new foreground loop.
- A fresh Matrix state exists.  The live FAST producer only requests the
  existing Matrix observation-only receiver; it cannot invoke a route change.
- The Matrix planner is active but reports capture-only processing,
  `candidate_or_execution_forbidden`, and a certification-only scope.
- The user-autoswitch timer is inactive.  The execution-event file did not
  change during this block; observed movements: `0`.
- Full Matrix is still the canonical fallback.  Stale, unknown or conflicting
  evidence remains fail-closed.

## Controlled T0-T11 conclusion

The engineering/Polygon obligation is complete: the same existing owners have
been exercised through the short/full comparison, repeated-producer Matrix
write, and synthetic governed T0-T11 fixture.  The deliberate boundary remains
correct: FAST is a shadow observation, while a real ordinary-client move needs
fresh current scope, target, Packet/lease/barrier and verification context.

The remaining future production observation is not an engineering blocker and
must not be manufactured.  If an existing owner later supplies a lawful
ordinary failure with complete current context, it should compare the already
deployed shadow result with Full Matrix and follow the existing governed path.
Until then, automatic FAST admission is not enabled and Full Matrix remains
the safe live fallback.

## Verification commands

```text
python3 -m unittest \
  tests.unit.test_v5_3_matrix_controlled_comparison \
  tests.unit.test_v5_3_nontelegram_trigger_revalidation \
  tests.unit.test_governed_canary_cli
# 139 tests, OK

tools/v7-truth-check --all --json
# FULLY_ALIGNED, PASS
```

## Exact successor

No additional engineering action is open in this V5.3 block.  Keep the
deployed observation-only FAST phase and Full Matrix fallback.  A future
ordinary-production comparison may re-enter only from a fresh existing-owner
failure/action context; it must not be created by moving a customer or changing
a route for evidence.
