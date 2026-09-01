# Recovery stability hardening program section V3

**Date:** 2026-09-01
**Mission:** `V7_RECOVERY_STABILITY_HARDENING_PROGRAM_SECTION_V3`
**Type:** Program-contract edit only
**Result:** `PROGRAM_CONTRACT_V3_REGISTERED; IMPLEMENTATION_NOT_ADMITTED`

## Why added

Recent ordinary recovery observations established a product gap: V7 can
recover a user automatically, yet a later current recovery can be delayed or
blocked by residue from an earlier incident, cooldown, target decision,
operation or terminal projection.  A single successful recovery therefore is
not evidence that the recovery lifecycle stays correct as time and scope
change.

No Runtime mechanism, client assignment, route, Matrix generation, timer,
Authority, Candidate, Packet, Lease or Barrier was changed by this Mission.

## Contract added

The Program now requires `RECOVERY_STABILITY_CONSUMED` before the final
seven-second product SLO can close.

The binding law is:

```text
CURRENT FAILED OR PROFILE-UNSUITABLE SOURCE
+ CURRENT AFFECTED ENABLED USERS
+ CURRENT LAWFUL TARGET
+ NO ACTIVE EXACT CONFLICT
= CURRENT RECOVERY OBLIGATION OR ACTIVE GOVERNED RECOVERY
```

If this law is false, the existing Runtime diagnostics must expose
`RECOVERY_OBLIGATION_MISSING`.

V2 makes that diagnostic self-healing: the existing health/Matrix
reconciliation consumer must rematerialize the current obligation, prove an
already active governed recovery, or produce the exact current hard stop and
its re-entry condition. It is scheduled at the next owner-backed
reconciliation opportunity, not by a busy loop or an impossible synchronous
deadline.

## Current truth versus history

Fresh Matrix, current assignments/profile requirements, target health and
capacity, Authority, active exact operation ownership and current route state
override historical incident/closure rows, old `NO_SAFE_TARGET`, prior
cooldown, prior target choice and Learning.

History remains useful for audit, learning, exact-once protection and proof of
an active exact safety conflict.  It cannot make a failed channel healthy,
remove current users from scope or suppress a new lawful recovery.

An active safety block must match the current source/action generation and the
same identity or exactly overlapping scope, and must have a current non-expired
operation, Lease, Barrier or rollback dependency.  A completed or unrelated
operation is not such a block.

## Re-entry and exact-once

Exact-once applies to the same completed route mutation, not indefinitely to a
continuing incident.  New scope, newly eligible target, disappeared blocker or
fresh relevant Matrix generation requires new reconciliation.

Every `STOP_SAFE` must identify its current blocker, owner, scope, re-entry
condition and next existing reconciliation owner.  Re-entry is level-triggered
only by an existing relevant event; it is not a busy polling loop.

V2 also makes current anti-flap, cooldown, conflict generation, active
operation ownership and recovery probation explicit current safety facts.
They remain valid fail-closed safety gates, but historical cooldown/closure
rows cannot strand a fresh confirmed failure.

## V2 stability additions

After every successful or safely stopped transaction, existing owners must
prove the post-terminal residue invariant: no stale Candidate, Packet, Lease,
Barrier, execution window, target pin, handoff, scope or operation pointer may
block the next current recovery unless an exact current successor owns it.

The stability proof now has three complementary layers:

1. deterministic 50/100 transition soak;
2. virtual-clock before/at/after testing of every material existing-owner
   freshness and expiry boundary;
3. reproducible, seeded 500/1000-transition Polygon state-machine soak.

Randomized restart events are simulated only in the test/Polygon environment;
they cannot restart production services. The live five-to-ten cycle campaign
uses controlled/test profiles only, records one recovery-critical fingerprint,
and cannot intentionally disrupt ordinary users.

## Acceptance plan

The later implementation phase must complete:

1. current-truth precedence audit;
2. level-triggered reconciliation and STOP_SAFE re-entry;
3. stranded-recovery diagnostic through existing owners;
4. historical live-gate classification and cleanup;
5. post-terminal residue invariant;
6. deterministic 50-transition soak, repair, then 100-transition soak;
7. temporal before/at/after boundary soak;
8. seeded randomized 500-transition soak, repair, then 1000-transition soak;
9. five consecutive, preferably ten, approved same-fingerprint live operator
   bad-placement cycles without an intervening semantic repair;
10. real Matrix-to-S11 evidence for all applicable cases.

Required sequences include changed scope under a continuing incident, stale
`NO_SAFE_TARGET` becoming obsolete, cooldown on fresh confirmed failure,
restart reconstruction, two independent failures, multi-target recovery,
exact conflict completion, stale Lease/Barrier cleanup and target-pin
isolation.

## Safety and authority

The phase reuses Matrix, health loop, `users.registry`, Planner, Authority,
Candidate/Packet/Lease/Barrier, execution control, route writer and
Core-primary.  It creates no new operational owner or truth source.

Codex may repair generic implementation defects, test, deploy and observe. It
must not perform a user-specific recovery, choose a source/target, construct
an incident or governed transaction, call the route writer, or advance a
live recovery on V7's behalf.  Bounded live cycles use only explicitly approved
controlled/test profiles; a lawful target requires zero stranded users.

## Relationship to the 7-second SLO

The clocks remain unchanged:

```text
T_FIRST_VALID_FAILURE_OBSERVATION
-> T_GLOBAL_ALL_AFFECTED_RECOVERED
P95 <= 7000 ms; maximum <= 8000 ms
```

Stability and latency are independent:

- recovery in 20 seconds may be stability PASS but latency FAIL;
- a user left stranded with a healthy target is stability FAIL regardless of
  elapsed time.

Final Program closure now requires both `RECOVERY_STABILITY_CONSUMED` and
`GLOBAL_ALL_AFFECTED_RECOVERY_SLO_CONSUMED`, followed by the existing N11
residue closure.

## Repair discipline

Every defect requires a proven root cause, minimal existing-owner repair,
focused cause test, regression of the affected invariant family and previously
consumed stability corpus, safe deploy, Runtime observation and renewed
affected evidence. A failure is classified as pre-existing or introduced
before changing acceptance. Rollback is lawful only through the existing
safe-deploy/rollback owner; otherwise deployment stops safely.

## V3 change containment

V3 does not duplicate the V2 current-truth, residue, temporal or randomized
contracts. It adds the missing protection for subsequent repairs.

For every recovery-critical change, V7 derives the affected regression set
from existing owner/dependency/invalidation facts, runs focused and affected
prior evidence, deploys safely, verifies local/GitHub/Runtime provenance and
then observes the ordinary V7 caller. The result is tied to that exact change
fingerprint; it cannot be reused for another change.

The frozen baseline is a compact pointer set to existing Polygon/test receipts,
deployment provenance and reports. It is not a new database, registry,
evidence store or Runtime state surface. A small unrelated change need not run
all 1000 randomized transitions, but it cannot skip evidence proven affected
by its dependency map.

If a prior affected invariant regresses, new acceptance credit stops. The
existing safe rollback owner restores the last known-good fingerprint; when a
transition is non-reversible, the existing fail-closed forward-repair/migration
owner restores the invariant and reruns the affected baseline. Repeated
special-case branches trigger a bounded owner state-model review instead of
another compensating exception.

## Files changed

- `docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`

## Publication

- Commit: `bebea511` (`Strengthen recovery stability contract V2`).
- `git push origin Updatesystem`: accepted by the remote.
- Independent `git ls-remote` immediately afterwards could not resolve
  `github.com` from this host. The report therefore records publication as
  push-acknowledged, not independently remote-tree verified.

## Verification

- Prior V1 verification is retained below as historical evidence.
- V2 `git diff --check`: PASS.
- V2 focused contract verification:
  `tests.unit.test_v7_sync_tools` plus
  `tests.unit.test_omp_program_execution_reconciliation`: 68 PASS.
- V2 `tools/v7-truth-check --all --json`: CPS/OMP current-state and
  completion-order consistency PASS; this documentation-only change requires
  no Runtime deploy. The aggregate result remains `NO-GO` only because the
  checker could not read GitHub or live Runtime hashes at that moment
  (`github_remote_unreadable`, `canonical_branch_missing_on_remote`,
  `live_runtime_hashes_unavailable`). Those external observations do not
  invalidate the local document contract, and no Runtime effect is claimed.
- V3 `git diff --check`: PASS.
- V3 focused contract verification:
  `tests.unit.test_v7_sync_tools` plus
  `tests.unit.test_omp_program_execution_reconciliation`: 68 PASS.
- V3 `tools/v7-truth-check --all --json`: CPS current-state and completion
  order PASS; local document alignment PASS. Aggregate remote/live convergence
  remains `NO-GO` for the same external observation blockers only:
  `github_remote_unreadable`, `canonical_branch_missing_on_remote` and
  `live_runtime_hashes_unavailable`. V3 changes no deploy-required path and
  claims no Runtime effect.

## Exact next frontier

No implementation is admitted by this document Mission. When the existing
CPS/OMP reconciliation owner admits the next work, it must begin with a
current-truth/current-safety audit, map all recovery gates to their existing
owners, and then build the residue invariant before modifying Runtime behavior.
