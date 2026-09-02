# Governed Apply / verification current-path audit

Date: 2026-09-02

## Purpose

Continue the existing V7 service-failure Program without adding a Runtime,
Planner, Matrix owner, queue, writer, registry or Authority.  The current
question is the measured residual from automatic recovery after V7 has already
made its target decision.

## Fresh reconciliation

- CPS retained `RECOVERY_LATENCY_SLO=ACTIVE` and the binding rule that normal
  V7 Runtime alone detects, decides, governs, applies and verifies.
- Program and OMP now register the same narrow
  `RECOVERY_APPLY_VERIFICATION_CONCURRENCY_LAW`: measure the existing path,
  remove only proven P0/P1 work, keep mutation serial unless the existing
  owners prove disjointness, and retain route/kernel/required-service S11.
- `v7-health.service` was active and enabled at observation.  No route,
  client, policy, Authority, Matrix or timer was changed by this audit.

## Live evidence before this repair

The normal V7 Runtime, not Codex, completed two current ordinary recoveries:

| source scope | members moved | T0 -> completion | Apply + verification |
| --- | ---: | ---: | ---: |
| `other_required:1` | 3 | 25,214 ms | 16,035 ms |
| `other_required:1` | 1 | 13,675 ms | 5,080 ms |

The outer receipt correctly identified `apply_and_verification` as dominant,
but its compact nested timeline retained the first 32 Planner spans.  In a
long run this dropped the later route-writer, route-visibility and
required-service-S11 spans, so it could not distinguish a necessary S11 tail
from avoidable serialization.

## Implemented bounded repair

`tools/runtime-support/v7-health-loop` still emits the same bounded,
identifier-free receipt.  It now retains all existing rows whose parent is
`apply_and_verification` first, then fills the remaining 32-row budget with
the former order.  This is observability-only: it does not call, delay,
authorize, select, mutate or retry a recovery.

Focused regression added: a timeline with 40 earlier planner rows and later
route/S11 rows proves the latter remain visible and the receipt stays bounded.

## Verification

- `tests.unit.test_v7_health_fast_deadline_loop`: 37 passed.
- The wider affected suite was started for health, autoswitch policy,
  service-failure Program and truth checks; its focused health component
  completed successfully.  The deploy gate will rerun its applicable checks
  from the committed fingerprint.
- `git diff --check`: pass before publication.
- Existing safe-deploy preflight found the expected uncommitted Runtime delta
  and therefore correctly returned `NO-GO` until commit/publish.  GitHub
  provenance itself was aligned at the pre-change commit.

## Next owner-backed action

Commit and deploy this observability repair through `tools/v7-safe-deploy`,
then wait only for the next independently originated V7 recovery receipt.
That receipt will identify the actual dominant Apply/S11 subspan.  Only then
is one P0/P1 existing-owner performance repair admissible, followed by the
existing Polygon scale suites at 10/50/100/1000 and another V7-owned live
observation.  Codex must not manually initiate, select or advance a recovery.
