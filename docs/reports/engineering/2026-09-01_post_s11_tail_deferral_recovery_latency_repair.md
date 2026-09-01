# Ordinary recovery: post-S11 tail deferral repair

Date: 2026-09-01

## Current live evidence

After the preceding Matrix-current-source repair was deployed, the normal
`v7-health.service` caller automatically recovered two ordinary users from
failed source `1` to Planner-selected target `awg0`. No operator or Codex
route command was used. The deployed Runtime, repository and GitHub commit
were aligned at `0f074ad34cfd4362c0391328ece5f3abd355a382` before this repair.

The governed receipt showed 34,330.135 ms until the child exited. Its causal
breakdown proved that the client-critical apply through required service S11
portion was 4,669.544 ms, while the remaining 27,117.116 ms was post-S11
passive-event consumption (15,642.840 ms) plus learning closure
(11,356.039 ms). These tails delayed the health loop from taking the next
independent failed source even though the first cohort had already been
route- and service-verified.

Route writes were bounded (786.993 ms and 525.877 ms), one Core-primary
cohort commit was 238.141 ms, exact member route checks were 234.991 ms and
212.993 ms, and the shared required-service check was 327.456 ms. The
measured long tail was therefore not a required S11 safety action.

## Repair

`AutoswitchPlanner.finalize_operation` now recognises an exact immutable
ordinary-service-failure Packet binding when invoked by the existing
persistent Matrix Runtime. After successful S11 it still performs all
mandatory terminal work: terminal verdict, audit reference/emission,
execution-control finalisation, and any required lease finalisation. It then
returns immediately and defers only passive history and learning to their
existing consumers.

The prior explicit CLI flag remains supported. The immutable Packet binding
is only a fail-closed fallback if that transient flag is lost between the
existing Matrix, governed executor and route-owner process boundaries.

No target was selected manually; no client, Matrix state, Authority, Packet,
Lease, Barrier, route or Core-primary membership was changed by this repair.
No new owner, timer, queue, registry or state source was added.

## Verification

- New regression proves that a persistent Matrix Runtime invocation with an
  exact ordinary Packet binding defers passive/learning work even if the
  transient CLI flag is absent.
- Focused finalisation and Matrix-failure tests: 3 passed.
- Full `test_v7_users_autoswitch_policy`: 240 passed.
- `git diff --check`: passed.

## Next evidence frontier

Deploy through `tools/v7-safe-deploy`, confirm Runtime alignment, and wait
only for the next ordinary V7-generated recovery event. The normal Runtime
must then prove the full three clocks separately: placement-to-observation,
observation-to-last-member S11, and full visible recovery. This prior
standing incident remains functional proof, not a fresh 7-second SLO sample.
